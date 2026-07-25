"""Optional Claude narration layer (--llm) — with a citation-verification pass.

Strict separation of duties, same as the rest of the system: the detectors
decide what happened and cite the evidence; Claude — if ANTHROPIC_API_KEY is
available — only rewrites the already-built, already-cited Incident IR into a
board-room narrative. Three guardrails make fabrication hard and detectable:

  1. Claude is given the STRUCTURED IR (findings + evidence IDs), never the raw
     logs. It cannot "reinterpret" a log line because it never sees one.
  2. The system prompt forbids new facts and requires citing the IDs we supply.
  3. A deterministic verification pass (verify_citations) extracts every event/
     finding ID in Claude's output and checks it against the IR's real ID set —
     any ID that isn't in the evidence is flagged in-line as UNVERIFIED.

If the key, SDK, or network is missing, the tool falls back to the deterministic
synthesis: the LLM is a bonus, never a dependency, and it can never invent or
change a finding.
"""

from __future__ import annotations

import json
import os
import re

from .model import Incident

DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
_ID_RE = re.compile(r"\b(?:F-\d{3}|(?:EP|AU|NW|CS)-\d{3,4})\b")

SYSTEM_PROMPT = (
    "You are a SOC incident-analysis writer. You are given a JSON Incident record produced by a "
    "deterministic correlation engine that has already reconstructed a multi-stage intrusion from SIEM "
    "logs and cited the exact log events behind every finding.\n"
    "Your job is to write a clear, board-ready narrative FROM THIS RECORD ONLY.\n"
    "Hard rules:\n"
    "- Use ONLY facts present in the JSON. Do NOT add hosts, accounts, IPs, times, techniques, or claims "
    "that are not there. If the JSON marks something UNCERTAIN or notes a gap, preserve that uncertainty.\n"
    "- Cite evidence using ONLY the exact IDs in the JSON (finding IDs like F-007 and event IDs like "
    "AU-0017). Never invent an ID.\n"
    "- Do not upgrade UNCERTAIN/SUSPECTED items to confirmed. Do not claim exfiltration volume the JSON "
    "says is unknown.\n"
    "Structure (plain text, no markdown headers, under 220 words): 1) Bottom line. 2) How it unfolded. "
    "3) Blast radius & confirmed data impact. 4) What we cannot yet confirm."
)


def _digest(incident: Incident) -> dict:
    """Compact, structured view of the IR for the model — findings + evidence
    IDs + blast radius + gaps. Deliberately NO raw log contents."""
    return {
        "window": {"start": incident.stats.get("first_malicious_activity"),
                   "end": incident.stats.get("last_malicious_activity"),
                   "duration_hours": incident.stats.get("attack_duration_hours")},
        "findings": [{
            "id": f.id, "phase": f.phase, "title": f.title, "confidence": f.confidence,
            "techniques": f.technique_ids, "hosts": f.hosts, "accounts": f.accounts,
            "evidence_event_ids": f.evidence[:8], "caveat": f.caveats,
        } for f in incident.timeline],
        "blast_radius": {
            "hosts": {h: {"status": r["status"], "role": r["role"]} for h, r in incident.hosts.items()},
            "accounts": {a: {"status": r["status"], "usage": r["usage"]} for a, r in incident.accounts.items()},
            "cloud": {b: r["type"] for b, r in incident.cloud.items()},
        },
        "coverage_gaps": [g["gap"] for g in incident.gaps],
    }


def valid_ids(incident: Incident) -> set[str]:
    ids = {f.id for f in incident.findings}
    for f in incident.findings:
        ids.update(f.evidence)
    return ids


def verify_citations(text: str, allowed: set[str]) -> tuple[str, list[str]]:
    """The verification pass. Flag any cited ID not present in the IR."""
    bad = []
    def mark(m):
        tok = m.group(0)
        if tok not in allowed:
            bad.append(tok)
            return "{}[UNVERIFIED]".format(tok)
        return tok
    checked = _ID_RE.sub(mark, text)
    return checked, sorted(set(bad))


def narrate(incident: Incident):
    """Return (brief_text, reason). brief_text is None on any failure."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None, "ANTHROPIC_API_KEY not set — showing the deterministic synthesis only"
    try:
        import anthropic
    except ImportError:
        return None, "the 'anthropic' package is not installed (pip install anthropic)"

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=1024,
            thinking={"type": "adaptive"},
            output_config={"effort": "medium"},
            system=SYSTEM_PROMPT,
            messages=[{"role": "user",
                       "content": "Incident record JSON:\n" + json.dumps(_digest(incident), ensure_ascii=False)}],
        )
    except anthropic.APIConnectionError:
        return None, "Claude API unreachable (network error)"
    except anthropic.AuthenticationError:
        return None, "Claude API rejected the API key"
    except anthropic.APIStatusError as exc:
        return None, "Claude API error HTTP {}".format(getattr(exc, "status_code", "?"))
    except Exception as exc:  # never let the bonus layer break the investigation
        return None, "unexpected LLM error: {}".format(exc.__class__.__name__)

    if getattr(response, "stop_reason", None) == "refusal":
        return None, "Claude declined to summarise this content"
    text = "".join(b.text for b in response.content if getattr(b, "type", None) == "text").strip()
    if not text:
        return None, "Claude returned an empty summary"

    checked, bad = verify_citations(text, valid_ids(incident))
    footer = "\n\n[verification pass] {} citation(s) checked against the evidence set; ".format(
        len(_ID_RE.findall(text)))
    footer += ("all valid." if not bad else
               "{} unverified ID(s) flagged inline and rejected: {}. The deterministic findings above are "
               "authoritative.".format(len(bad), ", ".join(bad)))
    return checked + footer, None
