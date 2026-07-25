"""siem_investigator — an agentic incident-investigation prototype.

Reconstructs a multi-stage attack from raw SIEM logs by running a deterministic,
fully-traceable pipeline:

    ingest -> parse/normalise -> detect -> correlate -> enrich (ATT&CK)
           -> assess blast radius -> synthesise answers (+ optional LLM narration)

Design principle: the machine that *finds and judges* the attack is deterministic
code, so every claim is a pure function of real log events and cites them by ID.
The LLM, when enabled, only *narrates* the already-built evidence — it cannot
invent findings, and a citation-verification pass strips any event ID it names
that is not in the evidence set. See README.md for the full rationale.
"""

__version__ = "1.0.0"
