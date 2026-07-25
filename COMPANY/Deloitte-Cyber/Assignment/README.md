# IOC Enrichment & Threat Intelligence Agent

A lightweight agentic CLI that lets a SOC analyst submit one or more IOCs (IPs,
domains, URLs, file hashes — all four types) and get back a **grounded,
source-cited enrichment verdict** from the abuse.ch feeds (ThreatFox, URLhaus,
MalwareBazaar) — fast enough, and traceable enough, to hand to an incident
commander in the next five minutes.

Built for the Deloitte Cyber Engineering pre-interview assignment
(*IOC Enrichment & Threat Intelligence Agent*), time-boxed to ~1 hour of build.

```
┌────────────────────── 185.220.101.45  [IPv4 address] ────────────────────────┐
│ Verdict : MALICIOUS - confidence HIGH (ThreatFox reporter confidence 75/100; │
│           corroborated by 2 independent feeds)                               │
│ Class   : Botnet command & control (C2)                                      │
│ Malware : Cobalt Strike  (aliases: Agentemis, BEACON, CobaltStrike)          │
│ Seen    : first 2025-10-19 04:12 UTC   last 2026-05-18 11:02 UTC  [ACTIVE]   │
│ Action  : P1 - Act now - block at proxy/firewall and hunt for related        │
│           traffic; indicator is online or active within the last 90 days     │
│ Evidence:                                                                    │
│   - ThreatFox IOC #1128873: 185.220.101.45:443, threat_type botnet_cc,       │
│     malware Cobalt Strike, confidence 75/100 -> threatfox.abuse.ch/ioc/...   │
│   - URLhaus host: 2 malicious URL(s) recorded -> urlhaus.abuse.ch/host/...   │
│ Sources : ThreatFox: hit | URLhaus: hit   (queried 2026-07-20 20:15 UTC)     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Quickstart

```powershell
cd Assignment
python -m pip install -r requirements.txt      # requests + rich (+ anthropic, optional)

# 10-second offline demo - zero setup, zero network, always runs:
python -m ioc_agent --demo --file sample_iocs.txt

python -m ioc_agent "Is 185.220.101.45 a known malicious IP? What is it associated with?"
python -m ioc_agent --file sample_iocs.txt     # batch + overall threat picture
python -m ioc_agent --stats 7                  # most active families, last 7 days
python -m ioc_agent                            # interactive analyst session
python -m ioc_agent --json "8.8.8.8"           # machine-readable audit output

# Self-checks:
python tests/test_iocs.py
```

### The abuse.ch auth key (one real-world wrinkle)

The brief says the feeds "require no authentication" — **that changed in
mid-2025**: abuse.ch now requires a free `Auth-Key` for all API queries
(verified live during development: unauthenticated calls return
`HTTP 401 {"error": "Unauthorized"}`). Getting one takes ~2 minutes:

1. Register (free) at **https://auth.abuse.ch/** and generate an auth key.
2. Provide it via any of: `ABUSECH_AUTH_KEY` env var, `--auth-key KEY`,
   or a local `abusech_auth.key` file next to this README.

Without a key the tool still runs and fails **honestly**: each source reports
an actionable auth error and the verdict is `ERROR — treat as unknown, not
clean`. And `--demo` mode always works — canned fixtures shaped exactly
like real API replies, clearly banner-labelled — so the walkthrough can never
be killed by conference-room Wi-Fi.

### Optional: Claude analyst brief (`--llm`)

With `ANTHROPIC_API_KEY` set (and `pip install anthropic`), `--llm` appends a
short Claude-written incident-commander brief **generated strictly from the
already-synthesised evidence JSON** — the prompt forbids adding facts and
requires per-claim source citations. Without a key the flag degrades to a
one-line notice. The LLM never decides a verdict (see "Trust" below).

---

## Requirements from the brief → where they're met

| Requirement | Where |
|---|---|
| Accept IOC inputs (≥2 of the 4 types) | All **four** types handled: IP, domain, URL, MD5/SHA1/SHA256 hashes (`iocs.py`), incl. defanged forms (`hxxp://`, `185.220.101[.]45`) |
| Return enriched context (type, classification, family, confidence, first/last seen, source feed in every answer) | Every card: verdict + classification + family/aliases + confidence w/ rationale + seen-window + per-record source citations with links (`verdict.py`, `report.py`) |
| Handle unknowns honestly | `UNKNOWN — no records in the queried feeds` verdict with per-source "no records as of <time>" lines + explicit caveat that absence ≠ clean; source outages produce `ERROR`, never a guess; invalid input is flagged separately and never queried (`verdict.py`, `cli.py`) |
| Agentic approach: query parsing → feed lookup → result synthesis | parse → plan → act → synthesise → report loop (`cli.py` docstring maps it); intent routing sends "most active families…" to stats, "summarise…" to the session summary |
| Bonus: batch + overall threat picture | `--file`, parallel lookups, summary table + threat-picture panel with P1/P2 call-outs and next steps |
| Something that runs | 5 passing self-tests incl. an end-to-end pipeline check of all 7 sample IOCs; `--demo` guarantees it runs anywhere |

Every example query in the brief works verbatim — paste it as the argument (or
into the interactive prompt).

---

## Architecture: the agentic loop

```
 analyst free text ──► PARSE    extract + classify IOCs (refang defanged); detect
        │                       intents ("most active families", "summarise")
        ▼
      PLAN     per-IOC lookup plan by type          ip/domain → ThreatFox + URLhaus(host)
        │                                           url       → URLhaus(url) + ThreatFox
        ▼                                           hash      → MalwareBazaar + ThreatFox + URLhaus(payload)
      ACT      execute feed calls (parallel across IOCs, bounded workers,
        │      timeouts; a failed source is recorded, never fatal)
        ▼
   SYNTHESISE  deterministic rules fold evidence → verdict + confidence +
        │      priority, every bullet citing feed + record ID + link
        ▼
     REPORT    analyst cards • batch summary table • overall threat picture
               • optional Claude brief (grounded on the same evidence)
```

| Module | Responsibility |
|---|---|
| `ioc_agent/iocs.py` | Extraction/classification (strict regexes + `ipaddress` validation, refanging, appearance-order, dedupe) |
| `ioc_agent/feeds.py` | ThreatFox / URLhaus / MalwareBazaar clients; auth; timeouts; never-raise error model; demo-fixture switch |
| `ioc_agent/enrich.py` | Per-IOC lookup plan + bounded-parallel batch execution |
| `ioc_agent/verdict.py` | Deterministic synthesis: verdict, confidence ladder, priority, EICAR special-case, honest unknowns |
| `ioc_agent/report.py` | Rich/plain rendering, batch threat picture, JSON audit output, LLM evidence digest |
| `ioc_agent/llm.py` | Optional Claude narration (Anthropic SDK, `claude-opus-4-8`), strictly grounded, fails soft |
| `ioc_agent/cli.py` | Arg parsing, intent routing, interactive session (with session memory for "summarise") |
| `ioc_agent/demo_fixtures.py` | Offline API-shaped fixtures for the sample IOC list |

## How verdicts are derived (deterministic, explainable)

| Verdict | When | Priority |
|---|---|---|
| `MALICIOUS` | Any feed returns records for the IOC | **P1** if URL online or last activity ≤ 90 days; else **P2** (block + retro-hunt) |
| `TEST FILE (EICAR)` | Hash/tags/AV names identify the EICAR AV test file | **P3** informational — reporting it "malicious" would be a textbook false positive |
| `UNKNOWN` (no records) | Every queried feed answered and none matched | **P4** — "no evidence in these feeds as of <time>", explicitly *not* "clean" |
| `ERROR` (inconclusive) | No hits **and** ≥1 source errored (network/auth/timeout) | **P3** — treat as unknown, re-run; names the failed source |
| `INVALID` input | Token looks like an attempted IOC but fails validation (bad IPv4 octets, wrong-length hash, unparseable line in a batch file) | Skipped **before** any lookup, listed in notices and the batch summary — never conflated with UNKNOWN |

Confidence ladder: ThreatFox's own reporter-confidence score when present
(≥75 high / ≥50 medium / else low) → else exact MalwareBazaar sample match
(high) → else URLhaus URL online (high) / historical (medium); **corroboration
by a second independent feed bumps one level**. The rationale is printed next
to the number, so an analyst can always answer "why does it say high?".

Known-infrastructure context notes (8.8.8.8 = Google DNS, microsoft.com, …)
are printed as *"local analyst note, not a feed verdict"* — they aid
recognition but never alter a verdict.

## Trust & traceability (why an analyst can defend this to an IC)

- **Verdicts are a pure function of feed records.** No model in the loop for
  judgement. Same inputs → same verdict, every time.
- **Every claim is cited**: feed name, record ID, and a clickable
  threatfox/urlhaus/bazaar.abuse.ch link the analyst can open to verify.
- **Every card shows what was checked**: `Sources: ThreatFox: hit | URLhaus:
  no records (queried <UTC time>)` — including what *couldn't* be checked.
- **`--json` is an audit record**: verdict + the raw, unmodified API responses
  that produced it. Pipe to a file and attach to the ticket.
- **The optional LLM only narrates.** It receives the already-decided evidence
  digest, is instructed to add nothing and cite per-claim, and if it's
  unavailable the deterministic summary stands. Trust does not depend on it.
- **Demo mode is labelled** with a banner on every run — canned data can never
  masquerade as live intel.

## Design decisions & tradeoffs (1-hour box)

- **CLI over UI** — closest to SOC muscle memory, trivially scriptable
  (`--json` into a SOAR), and no build/deploy risk for "it must run".
- **All four IOC types** — the brief allows two, but ThreatFox covers every
  type through one endpoint, so full coverage cost little extra.
- **Deterministic core, optional LLM shell** — the fastest way to make an
  analyst trust an "AI" tool is to make the AI unable to invent verdicts.
- **Never-raise feed clients** — one dead feed degrades the answer, not the
  triage session; partial evidence is labelled as such.
- **Bounded parallelism (4 workers), 15s timeouts** — an 80-IOC incident batch
  finishes in ~1–2 min without hammering free community APIs.
- **Graceful-degradation ladder** — no `rich` → plain ASCII; no `requests` →
  demo still runs; no auth key → honest INCONCLUSIVE + how to fix; no
  `ANTHROPIC_API_KEY` → deterministic summary. Nothing takes the demo down.
- **Shortcuts taken, knowingly**: no response caching, no retry/backoff, no
  IPv6/email/CVE IOC types, no allowlist feed (top-1M) integration, minimal
  test surface, single-file audit via `--json` rather than a run store.

## Reducing false-positive risk (discussion)

1. **No inference on absence** — unknowns are reported as "no records", never
   scored or guessed at. The feeds only contain *reported-malicious*
   indicators, and the output says exactly that.
2. **EICAR special-case** — the canonical trap for naive lookups: it appears
   in MalwareBazaar, but the tool labels it a harmless test artifact instead
   of a detection.
3. **Confidence is sourced, not invented** — ThreatFox's own reporter
   confidence is surfaced with its number; corroboration across independent
   feeds, and current online status, are the only boosters.
4. **Recency drives urgency** — a 2019 offline malware URL is P2
   "investigate/retro-hunt", not a P1 fire alarm (see the tsunami.arm7 sample).
5. **Context notes for famous infrastructure** reduce the classic
   "analyst blocks 8.8.8.8" class of mistake — without whitelisting anything
   out of the verdict logic.
6. **Human stays in the loop** — output is decision support with links to
   primary sources; it recommends blocks, it doesn't execute them.

**What it's good for today**: first-five-minutes triage of an IOC batch during
an active incident; consistent, citable answers instead of N analysts × N
browser tabs; a threat picture an IC can act on. **What it is not**: a
detection system, a replacement for multi-source corroboration (VT, AbuseIPDB,
passive DNS, internal telemetry), coverage of nation-state/low-prevalence
indicators (abuse.ch skews crimeware), or an auto-blocker.

## What I'd improve next

Retry/backoff + response caching (abuse.ch rate limits); AbuseIPDB and a
top-1M allowlist as additional corroboration lanes; IPv6/email/CVE types;
STIX 2.1 / MISP export and a SOAR webhook; a persistent per-incident case file
(dedupe across re-runs, verdict diffing over time); richer LLM mode (natural-
language follow-up questions over the evidence store); container packaging.

---

## 5-minute walkthrough script (interview deliverable #2)

1. **Problem framing (30s).** 80+ IOCs per incident, copy-paste triage, three
   analysts three answers. Bar: an answer the IC can trust in 5 minutes.
2. **Run it (90s).** `python -m ioc_agent --demo --file sample_iocs.txt` —
   walk one malicious card top to bottom: verdict → confidence *with reason* →
   family → seen-window → P1 action → cited evidence → sources line. Then the
   batch table + threat picture: "this last panel is the IC handoff."
3. **Honest unknowns (45s).** Point at 8.8.8.8 and the synthetic hash: "no
   records as of now" + caveat + context note; and EICAR: a lookup tool that
   *doesn't* cry wolf on the AV test file.
4. **Agentic loop (60s).** parse → plan → act → synthesise → report in
   `cli.py`; intent routing (`"most active families...?"` → stats mode) —
   `python -m ioc_agent --demo "What malware families have been most active in
   ThreatFox in the last 7 days?"`.
5. **Trust story (45s).** Deterministic verdicts, per-claim citations,
   `--json` raw-response audit trail; LLM narrates but never judges (show
   `--llm` if a key is handy).
6. **Judgment under pressure (30s).** The brief said "no auth" — live probing
   showed abuse.ch now 401s without a free Auth-Key (mid-2025 change), so the
   tool ships key handling, honest ERROR degradation, and an offline demo
   mode. Close with the shortcut list + next steps above.

*(Live-mode fallback: if the room has no network or no key, every command in
this script works with `--demo` — and says so on screen.)*
