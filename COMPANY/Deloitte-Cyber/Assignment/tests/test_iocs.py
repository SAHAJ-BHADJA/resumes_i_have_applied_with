"""Quick self-checks for IOC parsing and verdict synthesis.

Run with plain Python (no pytest needed):  python tests/test_iocs.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from ioc_agent.iocs import IOC, classify, extract_iocs, extract_with_invalid, refang  # noqa: E402


def test_refang():
    assert refang("hxxp://194.165.16[.]11/bins/tsunami.arm7") == "http://194.165.16.11/bins/tsunami.arm7"
    assert refang("185.220.101[.]45") == "185.220.101.45"
    assert refang("hxxps://evil(.)example{.}com") == "https://evil.example.com"


def test_classify():
    assert classify("185.220.101.45") == IOC("185.220.101.45", "ip")
    assert classify("185.220.101.45:9001") == IOC("185.220.101.45", "ip")
    assert classify("999.1.1.1") is None
    assert classify("emotet-c2-update.xyz").type == "domain"
    assert classify("MICROSOFT.COM").value == "microsoft.com"
    assert classify("44d88612fea8a8f36de82e1278abb02f").type == "md5"
    assert classify("3395856ce81f2b7382dee72602f798b642f14140").type == "sha1"
    assert classify("a" * 64).type == "sha256"
    assert classify("http://194.165.16.11/bins/tsunami.arm7").type == "url"
    assert classify("hello") is None
    assert classify("") is None


def test_extract_from_sentence():
    text = (
        "Is 185.220.101.45 a known malicious IP? Also check emotet-c2-update.xyz, "
        "hxxp://194.165.16[.]11/bins/tsunami.arm7 and hash 44d88612fea8a8f36de82e1278abb02f."
    )
    got = {(i.type, i.value) for i in extract_iocs(text)}
    assert ("ip", "185.220.101.45") in got
    assert ("domain", "emotet-c2-update.xyz") in got
    assert ("url", "http://194.165.16.11/bins/tsunami.arm7") in got
    assert ("md5", "44d88612fea8a8f36de82e1278abb02f") in got


def test_invalid_candidates_are_separated():
    text = "check 8.8.8.8 and 999.1.1.1 plus hash a3d5a6d5e4e2b8f1c9c4e2b8f1c9d4e"
    iocs, invalid = extract_with_invalid(text)
    assert [(i.type, i.value) for i in iocs] == [("ip", "8.8.8.8")]
    assert "999.1.1.1" in invalid                                # bad octet -> INVALID
    assert "a3d5a6d5e4e2b8f1c9c4e2b8f1c9d4e" in invalid          # 31 hex chars -> INVALID
    # Valid hashes and plain numbers are NOT flagged invalid.
    _, invalid2 = extract_with_invalid("44d88612fea8a8f36de82e1278abb02f on 2026-07-20 12345678")
    assert invalid2 == []


def test_extract_no_false_positives():
    assert extract_iocs("What malware families have been most active in ThreatFox in the last 7 days?") == []
    # An IP inside a URL is one URL IOC, not URL + IP.
    assert [i.type for i in extract_iocs("http://194.165.16.11/a")] == ["url"]
    # Duplicates collapse.
    assert len(extract_iocs("8.8.8.8 and again 8.8.8.8")) == 1


def test_verdict_demo_pipeline():
    """End-to-end on fixtures: verdicts must match the brief's expected behaviour."""
    from ioc_agent import feeds
    from ioc_agent.demo_fixtures import FIXTURES
    from ioc_agent.enrich import enrich_many

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
    by_value = {e.ioc.value: e.verdict for e in enrich_many(iocs)}

    assert by_value["185.220.101.45"].level == "malicious"
    assert by_value["185.220.101.45"].confidence == "high"          # TF 75 + corroboration
    assert by_value["8.8.8.8"].level == "no-records"
    assert by_value["8.8.8.8"].context_note                          # Google DNS note
    assert by_value["emotet-c2-update.xyz"].level == "malicious"
    assert "Emotet" in by_value["emotet-c2-update.xyz"].families
    assert by_value["microsoft.com"].level == "no-records"
    assert by_value["http://194.165.16.11/bins/tsunami.arm7"].level == "malicious"
    assert by_value["http://194.165.16.11/bins/tsunami.arm7"].priority == "P2"  # offline/stale
    assert by_value["44d88612fea8a8f36de82e1278abb02f"].level == "test-file"    # EICAR, not FP
    assert by_value["a3d5a6d5e4e2b8f1c9c4e2b8f1c9d4e5"].level == "no-records"
    # Every verdict must cite at least one source line.
    for value, verdict in by_value.items():
        assert verdict.evidence, "no evidence bullets for {}".format(value)
        assert verdict.sources_line, "no sources line for {}".format(value)


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_") and callable(fn)]
    for name, fn in tests:
        fn()
        print("{}: ok".format(name))
    print("all {} tests passed".format(len(tests)))
