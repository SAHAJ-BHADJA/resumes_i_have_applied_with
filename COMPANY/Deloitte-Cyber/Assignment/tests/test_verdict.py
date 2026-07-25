"""Verdict-safety, feed-normalization and batch-summary checks.

These encode the safety properties the tool must never violate:
- an API failure is ERROR, never UNKNOWN, and never silently dropped
- a clean lookup with no matches is UNKNOWN, never "safe"
- partial source failure is disclosed even when another source confirms
- nothing (families, confidence, dates) is ever invented for empty evidence

Run with plain Python (no pytest needed):  python tests/test_verdict.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from ioc_agent import feeds  # noqa: E402
from ioc_agent.feeds import FeedResult  # noqa: E402
from ioc_agent.iocs import classify  # noqa: E402
from ioc_agent.verdict import (  # noqa: E402
    LEVEL_INCONCLUSIVE,
    LEVEL_MALICIOUS,
    LEVEL_NO_RECORDS,
    synthesize,
)


def _ok_empty(source, query="q"):
    return FeedResult(source, query, ok=True, found=False, queried_at="2026-07-20 00:00:00 UTC")


def _errored(source, msg="network error: ConnectTimeout"):
    return FeedResult(source, "q", ok=False, found=False, error=msg, queried_at="2026-07-20 00:00:00 UTC")


def _tf_hit(confidence=60):
    rec = {
        "id": "42",
        "ioc": "203.0.113.7:80",
        "threat_type": "botnet_cc",
        "malware": "win.testfam",
        "malware_printable": "TestFam",
        "confidence_level": confidence,
        "first_seen": "2026-06-01 00:00:00 UTC",
        "last_seen": "2026-07-01 00:00:00 UTC",
        "tags": ["c2"],
    }
    return FeedResult("ThreatFox", "q", ok=True, found=True, records=[rec], queried_at="t")


def _mb_hit():
    rec = {
        "sha256_hash": "ab" * 32,
        "file_name": "payload.exe",
        "file_type": "exe",
        "file_size": 1024,
        "signature": "TestFam",
        "tags": ["exe"],
        "intelligence": {"clamav": []},
        "first_seen": "2026-06-15 00:00:00 UTC",
    }
    return FeedResult("MalwareBazaar", "q", ok=True, found=True, records=[rec], queried_at="t")


def test_all_clean_is_unknown_not_safe():
    v = synthesize(classify("203.0.113.7"), [_ok_empty("ThreatFox"), _ok_empty("URLhaus")])
    assert v.level == LEVEL_NO_RECORDS
    assert v.confidence == "n/a"
    # Nothing invented for empty evidence:
    assert v.families == [] and v.first_seen is None and v.last_seen is None
    # And the honesty caveat is present (absence of evidence != clean):
    assert any("not" in c and "clean" in c for c in v.caveats)


def test_all_errors_is_error_not_unknown():
    v = synthesize(classify("203.0.113.7"), [_errored("ThreatFox"), _errored("URLhaus")])
    assert v.level == LEVEL_INCONCLUSIVE
    assert v.level != LEVEL_NO_RECORDS
    assert any("ERROR" in b for b in v.evidence)
    assert "UNKNOWN, not clean" in v.priority_detail


def test_partial_error_without_hit_is_error_not_unknown():
    # One source answered clean, the other failed: must NOT claim "no records".
    v = synthesize(classify("203.0.113.7"), [_ok_empty("ThreatFox"), _errored("URLhaus")])
    assert v.level == LEVEL_INCONCLUSIVE


def test_partial_error_with_hit_is_malicious_with_disclosed_gap():
    v = synthesize(classify("203.0.113.7"), [_tf_hit(confidence=90), _errored("URLhaus")])
    assert v.level == LEVEL_MALICIOUS
    assert any("URLhaus" in c for c in v.caveats)  # the gap is disclosed


def test_confidence_from_source_and_corroboration_bump():
    # Single-source ThreatFox 60/100 -> medium, quoting the source's number.
    v_single = synthesize(classify("a1" * 16), [_tf_hit(confidence=60), _ok_empty("MalwareBazaar")])
    assert v_single.confidence == "medium"
    assert "60/100" in v_single.confidence_detail
    # Same score corroborated by a second independent feed -> bumped to high.
    v_corr = synthesize(classify("a1" * 16), [_tf_hit(confidence=60), _mb_hit()])
    assert v_corr.confidence == "high"
    assert "corroborated" in v_corr.confidence_detail


def test_feeds_error_on_unexpected_response_shape():
    # A malformed/unknown API reply must surface as an ERROR result, not a hit
    # and not a clean miss.
    feeds.enable_demo({("threatfox_search", "203.0.113.7"): {"query_status": "totally_new_status"}})
    res = feeds.threatfox_search("203.0.113.7")
    assert res.ok is False and res.found is False
    assert res.error and "unexpected" in res.error


def test_feeds_no_result_is_clean_miss():
    feeds.enable_demo({})  # defaults: every lookup answers "nothing found"
    res = feeds.threatfox_search("203.0.113.7")
    assert res.ok is True and res.found is False and res.error is None
    mb = feeds.mb_hash("a1" * 16)
    assert mb.ok is True and mb.found is False


def test_summary_counts_and_sources():
    from ioc_agent.demo_fixtures import FIXTURES
    from ioc_agent.enrich import enrich_many
    from ioc_agent.report import summary_data

    feeds.enable_demo(FIXTURES)
    iocs = [
        classify("185.220.101.45"),
        classify("8.8.8.8"),
        classify("emotet-c2-update.xyz"),
        classify("microsoft.com"),
        classify("http://194.165.16.11/bins/tsunami.arm7"),
        classify("44d88612fea8a8f36de82e1278abb02f"),
        classify("a3d5a6d5e4e2b8f1c9c4e2b8f1c9d4e5"),
    ]
    d = summary_data(enrich_many(iocs), invalid_inputs=["999.1.1.1"])
    assert d["total"] == 7
    assert d["total_submitted"] == 8              # 7 enriched + 1 invalid
    assert d["counts"]["malicious"] == 3
    assert d["counts"]["unknown"] == 3
    assert d["counts"]["test artifact"] == 1
    assert d["invalid_count"] == 1 and d["invalid_inputs"] == ["999.1.1.1"]
    assert d["sources_consulted"] == ["ThreatFox", "URLhaus", "MalwareBazaar"]
    assert set(d["p1_act_now"]) == {"185.220.101.45", "emotet-c2-update.xyz"}
    # Unknowns are never counted as clean/safe anywhere in the summary:
    assert "clean" not in d["counts"] and "safe" not in d["counts"]


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_") and callable(fn)]
    for name, fn in tests:
        fn()
        print("{}: ok".format(name))
    print("all {} tests passed".format(len(tests)))
