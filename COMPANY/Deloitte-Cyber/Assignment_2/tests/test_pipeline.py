"""End-to-end pipeline + synthesis + LLM citation-verification tests."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from siem_investigator import pipeline, synthesize, llm

ID_RE = re.compile(r"\b(?:F-\d{3}|(?:EP|AU|NW|CS)-\d{3,4})\b")


def _incident():
    return pipeline.run()


def test_pipeline_builds_incident():
    inc = _incident()
    assert inc.stats["findings"] >= 10
    assert inc.stats["techniques_count"] >= 15
    assert inc.stats["tactics_covered"] >= 8
    assert len(inc.attack_path) >= 3, "expected a multi-hop attack path"


def test_every_technique_is_in_catalogue():
    inc = _incident()
    used = {t for f in inc.findings for t in f.technique_ids}
    for tid in used:
        meta = inc.techniques.get(tid)
        assert meta and meta.get("name"), "technique {} missing from catalogue".format(tid)
        assert meta["name"] != tid, "technique {} has no real name".format(tid)


def test_all_ten_queries_answered_and_grounded():
    inc = _incident()
    answers = synthesize.all_answers(inc)
    assert len(answers) == 10
    valid = llm.valid_ids(inc)
    for q, a in answers:
        assert a and len(a) > 40, "empty answer for: {}".format(q)
        # every citation in an answer must reference something real
        for cited in ID_RE.findall(a):
            assert cited in valid, "answer to '{}' cites unknown id {}".format(q, cited)


def test_exec_summary_is_three_sentences():
    inc = _incident()
    body = synthesize.q_exec_summary(inc).split("\n\n", 1)[-1]
    # 3 sentences (allow the compound last one); count sentence-final periods
    sentences = [s for s in re.split(r"(?<=[.])\s+", body.strip()) if s]
    assert 3 <= len(sentences) <= 4, "exec summary should be ~3 sentences, got {}".format(len(sentences))
    assert "CONFIRMED" in body


def test_intent_router_matches_queries():
    inc = _incident()
    cases = {
        "is there any data exfiltration?": "EXFILTRATION",
        "what is the blast radius": "BLAST RADIUS",
        "which mitre att&ck techniques were used": "ATT&CK",
        "give me an executive summary for the board": "EXECUTIVE SUMMARY",
        "where are the gaps in coverage": "COVERAGE GAPS",
        "what should we do in the next 2 hours": "NEXT 2 HOURS",
    }
    for q, marker in cases.items():
        assert marker in synthesize.answer(inc, q).upper(), "intent misrouted: {}".format(q)


def test_router_handles_all_ten_brief_queries():
    """The free-text router must land every one of the brief's exact example
    queries on the right synthesiser (these include phrasings that shadow each
    other, e.g. 'timeline from initial access', 'hosts ... after the foothold')."""
    inc = _incident()
    expected = {
        "Walk me through the full attack timeline from initial access to last observed activity.": "ATTACK TIMELINE",
        "What was the initial access vector and what evidence supports that conclusion?": "INITIAL ACCESS VECTOR",
        "Which MITRE ATT&CK techniques did the attacker use? List them with technique IDs.": "TECHNIQUES OBSERVED",
        "Which user accounts were compromised or used by the attacker?": "ABUSED ACCOUNTS",
        "Which internal hosts did the attacker move to after the initial foothold?": "HOSTS THE ATTACKER",
        "Is there evidence of data exfiltration? If so, what was accessed and when?": "DATA EXFILTRATION",
        "What is the blast radius — list every affected host and account.": "BLAST RADIUS",
        "Where are the gaps in our log coverage that limit your confidence in this reconstruction?": "COVERAGE GAPS",
        "Give me a 3-sentence executive summary suitable for a board briefing.": "EXECUTIVE SUMMARY",
        "What should the incident response team do in the next 2 hours to contain this?": "NEXT 2 HOURS",
    }
    for q, marker in expected.items():
        assert marker in synthesize.answer(inc, q).upper(), "misrouted: {}".format(q)


def test_llm_citation_verification_flags_fabrication():
    """Unit test for the verification pass (no API key needed)."""
    inc = _incident()
    allowed = llm.valid_ids(inc)
    real = next(iter(allowed))
    text = "The attacker moved via {} but also touched EP-9999 and CS-8888.".format(real)
    checked, bad = llm.verify_citations(text, allowed)
    assert "EP-9999[UNVERIFIED]" in checked
    assert "CS-8888[UNVERIFIED]" in checked
    assert real + "[UNVERIFIED]" not in checked, "a real ID must not be flagged"
    assert set(bad) == {"EP-9999", "CS-8888"}


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all pipeline tests passed")
