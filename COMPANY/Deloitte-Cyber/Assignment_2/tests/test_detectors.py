"""Detector correctness + the traceability invariant + precision (near-misses)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from siem_investigator import ingest, detectors, correlate
from siem_investigator.model import CONFIRMED, SUSPECTED, UNCERTAIN

LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "siem_logs.json")


def _findings():
    store = ingest.load(LOGS)
    return store, correlate.assign_ids_and_order(detectors.run_all(store))


def test_full_kill_chain_detected():
    _, findings = _findings()
    phases = {f.phase for f in findings}
    for expected in ("Initial Access", "Execution", "Command and Control", "Persistence",
                     "Discovery", "Credential Access", "Lateral Movement", "Privilege Escalation",
                     "Collection", "Exfiltration", "Defense Evasion"):
        assert expected in phases, "kill-chain phase not detected: {}".format(expected)


def test_traceability_invariant_no_phantom_citations():
    """THE anti-hallucination guarantee: every evidence ID a finding cites must
    be a real event in the store. A phantom citation is a hard failure."""
    store, findings = _findings()
    for f in findings:
        assert f.evidence, "finding {} has no evidence".format(f.id)
        for eid in f.evidence:
            assert store.get(eid) is not None, "finding {} cites phantom event {}".format(f.id, eid)


def test_lateral_movement_is_multi_source_confirmed():
    store, findings = _findings()
    files01 = [f for f in findings if f.phase == "Lateral Movement" and "SRV-FILES01" in f.hosts]
    assert files01, "lateral movement to file server not detected"
    f = files01[0]
    assert f.confidence == CONFIRMED
    # the value of this detector is cross-source triangulation: the evidence must
    # span at least two distinct log sources (auth + network and/or endpoint).
    sources = {store.get(eid).source for eid in f.evidence}
    assert len(sources) >= 2, "lateral movement should corroborate across >=2 sources, got {}".format(sources)
    assert "T1021.002" in f.technique_ids


def test_uncertain_host_not_overclaimed():
    """The SQL server was authenticated to but has no EDR -> must be UNCERTAIN,
    never CONFIRMED. Honest uncertainty is the whole point."""
    _, findings = _findings()
    sql = [f for f in findings if "SRV-SQL01" in f.hosts]
    assert sql, "SRV-SQL01 access not detected"
    assert all(f.confidence == UNCERTAIN for f in sql), "SRV-SQL01 must stay UNCERTAIN"


def test_precision_benign_activity_not_flagged():
    """Near-miss decoys must NOT become findings: no finding may implicate the
    benign IT admin (t.walsh) or the lockout user (m.chen)."""
    store, findings = _findings()
    implicated = {a for f in findings for a in f.accounts}
    assert "t.walsh" not in implicated, "benign admin wrongly flagged"
    assert "m.chen" not in implicated, "lockout user wrongly flagged"
    assert "svc_analytics" not in implicated, "benign analytics principal wrongly flagged"
    # and they ARE explicitly reviewed-and-dismissed
    benign = detectors.review_benign(store)
    verdicts = " ".join(n["activity"] + n["verdict"] for n in benign)
    assert "m.chen" in verdicts and "t.walsh" in verdicts


def test_all_confidences_valid():
    _, findings = _findings()
    for f in findings:
        assert f.confidence in (CONFIRMED, SUSPECTED, UNCERTAIN)
        assert f.severity in ("critical", "high", "medium", "low")


def test_c2_beacon_regularity():
    _, findings = _findings()
    c2 = [f for f in findings if f.phase == "Command and Control"]
    assert c2, "C2 beaconing not detected"
    assert len(c2[0].evidence) >= 6, "beacon needs multiple flows to establish periodicity"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all detector tests passed")
