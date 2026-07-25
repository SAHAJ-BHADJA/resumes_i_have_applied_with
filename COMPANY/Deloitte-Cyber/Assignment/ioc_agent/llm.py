"""Optional Claude narration layer (--llm).

Strict separation of duties: the abuse.ch feeds decide the facts, the
deterministic rules in verdict.py decide the verdicts, and Claude - if an
ANTHROPIC_API_KEY is available - only rewrites the already-synthesised
evidence as a short brief for an incident commander. If the key, the SDK, or
the network is missing the tool silently falls back to the deterministic
summary: the LLM is a bonus, never a dependency, and it can never invent or
change a verdict.
"""

from __future__ import annotations

import json
import os

DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")

SYSTEM_PROMPT = (
    "You write short incident-triage briefs for a SOC incident commander. You are "
    "given a JSON evidence digest produced by deterministic lookups against the "
    "abuse.ch feeds (ThreatFox, URLhaus, MalwareBazaar).\n"
    "Hard rules:\n"
    "- Use ONLY facts present in the JSON. Never add indicators, malware names, "
    "dates, or numbers that are not there.\n"
    "- Cite the source feed for every claim, e.g. (ThreatFox #1128873) or (URLhaus).\n"
    "- Where the JSON says no records were found, say exactly that - do not "
    "speculate about maliciousness.\n"
    "- Keep the verdicts as given; you summarise, you do not re-judge.\n"
    "Structure: 1) Bottom line. 2) Act now. 3) Gaps & unknowns. "
    "Plain text, no markdown headers, under 180 words."
)


def narrate(payload: dict):
    """Return (brief_text, None) on success or (None, reason) on any failure."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None, "ANTHROPIC_API_KEY not set - showing the deterministic summary only"

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
            messages=[
                {
                    "role": "user",
                    "content": "Evidence digest JSON:\n" + json.dumps(payload, ensure_ascii=False),
                }
            ],
        )
    except anthropic.APIConnectionError:
        return None, "Claude API unreachable (network error)"
    except anthropic.AuthenticationError:
        return None, "Claude API rejected the API key"
    except anthropic.APIStatusError as exc:
        return None, "Claude API error HTTP {}".format(exc.status_code)
    except Exception as exc:  # never let the bonus layer break triage
        return None, "unexpected LLM error: {}".format(exc.__class__.__name__)

    if response.stop_reason == "refusal":
        return None, "Claude declined to summarise this content"

    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if not text:
        return None, "Claude returned an empty summary"
    return text, None
