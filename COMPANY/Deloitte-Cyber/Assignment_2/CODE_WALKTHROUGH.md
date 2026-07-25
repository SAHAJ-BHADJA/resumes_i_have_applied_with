# Code Walkthrough — every file, and how a request flows through them

This is the companion to [`README.md`](README.md). The README explains *what* the
system is and *why* it's designed this way; this document explains *how the code
works*, file by file, and then traces exactly what happens — function by function
— when a user asks a question. Read the README first for the mental model, then
use this as the map.

## Table of contents

1. [The 30-second mental model](#1-the-30-second-mental-model)
2. [Repository layout](#2-repository-layout)
3. [The three core data types (the "IR")](#3-the-three-core-data-types-the-ir)
4. [File-by-file, in pipeline order](#4-file-by-file-in-pipeline-order)
   - [tools/generate_dataset.py](#41-toolsgenerate_datasetpy--the-synthetic-data)
   - [data/siem_logs.json](#42-datasiem_logsjson--the-input)
   - [data/attack_techniques.json](#43-dataattack_techniquesjson--the-attck-catalogue)
   - [model.py](#44-siem_investigatormodelpy--the-data-types)
   - [ingest.py](#45-siem_investigatoringestpy--stage-1-ingest--parse)
   - [detectors.py](#46-siem_investigatordetectorspy--stage-2-detect)
   - [attack.py](#47-siem_investigatorattackpy--stage-4-enrich)
   - [correlate.py](#48-siem_investigatorcorrelatepy--stage-3-correlate)
   - [blast_radius.py](#49-siem_investigatorblast_radiuspy--stage-5-assess)
   - [synthesize.py](#410-siem_investigatorsynthesizepy--stage-6-synthesise--answer)
   - [llm.py](#411-siem_investigatorllmpy--optional-narration--verification)
   - [report.py](#412-siem_investigatorreportpy--rendering)
   - [pipeline.py](#413-siem_investigatorpipelinepy--the-wiring)
   - [cli.py + __main__.py](#414-siem_investigatorclipy--__main__py--the-entry-point)
   - [tests/](#415-tests--what-is-guaranteed)
5. [How a user request is executed, end to end](#5-how-a-user-request-is-executed-end-to-end)
6. [Every example query, traced](#6-every-example-query-traced)
7. [Where trust lives in the code](#7-where-trust-lives-in-the-code)
8. [How to extend it](#8-how-to-extend-it)

---

## 1. The 30-second mental model

Data flows through **three types** and **six stages**. Everything is plain data
(dataclasses + dicts), so it serialises cleanly and there is nothing hidden.

```
                 raw JSON            Event[]            Finding[]                Incident
                    │                  │                   │                       │
 siem_logs.json ─► INGEST ─────────► DETECT ───────────► CORRELATE ─► ENRICH ─► ASSESS ─► (Incident)
 (305 events)     ingest.load      detectors.run_all   correlate.*   attack.*  blast_radius.*
                    │                  │                   │                       │
                    ▼                  ▼                   ▼                       ▼
                 EventStore         12 detectors +      F-### IDs +   ATT&CK    hosts/accounts/
                 (indices +         review_benign       timeline +    names/    cloud + gaps
                  host↔ip map)      (precision pass)    attack path   urls
                                                                                  │
                                          the Incident is then handed to:         ▼
                                   synthesize.answer()  ─►  cited text answers  (SYNTHESISE → ANSWER)
                                   report.build_html()  ─►  interactive report
                                   llm.narrate()        ─►  optional AI brief (verified)
```

- **`Event`** — one normalised log line (model.py).
- **`Finding`** — one thing a detector concluded, carrying the event IDs that
  prove it (model.py).
- **`Incident`** — the whole reconstructed picture: findings + timeline + blast
  radius + gaps + ATT&CK enrichment (model.py). This is the **intermediate
  representation (IR)** every consumer reads.

The golden rule the code enforces: **detectors decide what is true; everything
downstream only formats it.** No language model is in the decision path.

---

## 2. Repository layout

```
Assignment_2/
├── README.md                     ← what/why (start here)
├── CODE_WALKTHROUGH.md           ← this file (how)
├── requirements.txt              ← core needs zero deps; optional: anthropic, requests, pytest
├── data/
│   ├── siem_logs.json            ← INPUT: 305 synthetic events + metadata schema
│   └── attack_techniques.json    ← ATT&CK catalogue (21 techniques, verified)
├── siem_investigator/            ← the package (the actual system)
│   ├── __init__.py               ← package docstring + __version__
│   ├── __main__.py               ← `python -m siem_investigator` entry → cli.main()
│   ├── model.py                  ← Event, Finding, EventStore, Incident (the IR)
│   ├── ingest.py                 ← Stage 1: load + parse + normalise
│   ├── detectors.py              ← Stage 2: 12 detectors + benign-review (the brains)
│   ├── correlate.py              ← Stage 3: timeline, IDs, attack path
│   ├── attack.py                 ← Stage 4: ATT&CK enrichment (+ live reconcile)
│   ├── blast_radius.py           ← Stage 5: hosts/accounts/cloud + coverage gaps
│   ├── synthesize.py             ← Stage 6: cited NL answers + intent router
│   ├── llm.py                    ← optional Claude narration + citation verifier
│   ├── report.py                 ← terminal report + interactive HTML
│   ├── pipeline.py               ← wires stages 1–5 into one run() → Incident
│   └── cli.py                    ← argument parsing + command dispatch (the loop)
├── tools/
│   └── generate_dataset.py       ← reproducible synthetic-data generator
├── tests/                        ← 19 tests (incl. the traceability invariant)
│   ├── test_ingest.py
│   ├── test_detectors.py
│   └── test_pipeline.py
└── out/                          ← generated artifacts
    ├── incident_report.html      ← the board-ready interactive report
    └── investigation.json        ← the machine-readable IR / audit trail
```

---

## 3. The three core data types (the "IR")

All defined in **`model.py`**. Understand these and the rest of the code reads
itself.

### `Event` — one normalised log line
```python
@dataclass(frozen=True)
class Event:
    id: str          # "EP-0004", "AU-0018", "NW-0038", "CS-0056"
    source: str      # "endpoint" | "auth" | "network" | "cloud_storage"
    ts: datetime     # parsed, timezone-aware UTC
    raw: dict        # the ORIGINAL record, untouched — this is what drill-down shows
```
Convenience accessors: `.host`, `.user` (falls back to `principal` for cloud),
`.ts_str` (the `Z` string), `.get(field)`, and `.citation()` which formats
`"AU-0018 (auth, SRV-FILES01, 2026-07-20T02:17:04Z)"` — source + host + time.
`raw` is never mutated, so a citation always resolves to the real record.

### `Finding` — one detector conclusion, with its evidence
```python
@dataclass
class Finding:
    id: str                 # "F-007" (assigned in correlate, chronological)
    title: str              # "Lateral movement to SRV-FILES01"
    phase: str              # kill-chain phase == ATT&CK tactic ("Lateral Movement")
    technique_ids: list     # ["T1021.002", "T1078.002", "T1569.002"]
    severity: str           # "critical" | "high" | "medium" | "low"
    confidence: str         # "CONFIRMED" | "SUSPECTED" | "UNCERTAIN"
    rationale: str          # plain-English "why this fired"
    evidence: list          # ["AU-0018","NW-0038","EP-0026"] — THE traceability backbone
    hosts: list             # hosts involved
    accounts: list          # accounts involved
    ts: datetime            # earliest evidence time (used to order the timeline)
    caveats: str            # honest limits on THIS finding
    data: dict              # structured extras, e.g. {"src_host","dst_host"} for the graph
```
The `evidence` list is the heart of the whole system: it is a list of real
`Event.id`s, and a test guarantees every one resolves to a real event.

### `EventStore` — the indexed corpus + entity resolution
Built once in ingest. Holds:
- `events` — all Events, **sorted by time**.
- `_by_id` — `id → Event` (so `get("AU-0018")` is O(1)).
- `host_to_ip` / `ip_to_host` — the **entity-resolution map**, built from the
  dataset's `metadata.asset_inventory_hint.hosts` plus any `(src_host, src_ip)`
  pairs observed in the logs. This is what lets a firewall flow (`10.20.8.12`)
  and an auth event (`SRV-FILES01`) be recognised as the *same host*.
- `ingest_stats` — counts per source, window, skipped malformed rows.

Methods: `.get(id)`, `.resolve_host(ip)`, `.by_source("auth")`, `.where(pred)`,
`.window`, `len(store)`.

### `Incident` — the whole reconstruction
```python
@dataclass
class Incident:
    findings, timeline,          # list[Finding] (timeline == findings, time-ordered)
    hosts, accounts, cloud,      # blast-radius dicts
    gaps,                        # coverage-gap dicts
    techniques,                  # the ATT&CK catalogue (id → metadata)
    store, stats,                # the EventStore + summary numbers
    attack_path,                 # directional host→host hops
    attack_by_tactic,            # ATT&CK grouped by tactic (for the matrix)
    benign_review                # near-misses ruled benign
```
`.to_dict()` / `.dumps()` serialise it to `out/investigation.json` — the audit
trail. Every consumer (CLI, report, synthesiser, LLM) reads **only** an
`Incident`, so there is one source of truth.

---

## 4. File-by-file, in pipeline order

### 4.1 `tools/generate_dataset.py` — the synthetic data
Standalone script (`python tools/generate_dataset.py`) that writes
`data/siem_logs.json`. Deterministic: `random.seed(1337)` → identical output
every run. Structure:
- **Inventory** — `HOSTS` (host→IP), users, the C2 IP (`45.83.140.77`), the S3
  buckets and abused access key.
- **`build_attack()`** — scripts the intrusion event-by-event across 9 stages
  (phish → C2 → persistence → discovery → LSASS → lateral → domain-admin →
  collection → exfil → anti-forensics), emitting precise, realistic records into
  the four source buckets.
- **`build_decoys()`** — plants the two "near-miss" decoys: a benign IT-admin
  PsExec and a self-inflicted account lockout.
- **`build_noise()`** — procedurally generates ~250 benign events
  (`business_hours_ts()` weights them toward working hours), including the
  high-volume-but-benign `svc_analytics` S3 baseline (decoy #3).
- **`METADATA`** — the schema section: describes every source's fields, the
  `logon_type` map, the deliberate `coverage_note` gaps, and the
  `asset_inventory_hint` used for entity resolution.
- **`main()`** — assembles, sorts each source by time, assigns zero-padded IDs
  (`EP-`, `AU-`, `NW-`, `CS-`), and writes the file.

### 4.2 `data/siem_logs.json` — the input
Two top-level keys: `metadata` (schemas, window, coverage notes, asset hint) and
`events` (the 305 records). Every event has the envelope `event_id`,
`timestamp`, `source`; the rest of the fields are source-specific (documented in
`metadata.sources`). The system reads **only documented fields**, so a real
export in this schema runs unchanged.

### 4.3 `data/attack_techniques.json` — the ATT&CK catalogue
A curated, offline subset of MITRE ATT&CK Enterprise: `techniques` maps each
`Txxxx[.yyy]` → `{name, tactic, tactic_id, url, summary}`. `tactics_order` gives
kill-chain ordering for the matrix. The four least-common IDs were verified live
against attack.mitre.org (see `_meta.verified_against_live_site`).

### 4.4 `siem_investigator/model.py` — the data types
Covered in §3. Also defines the vocabularies `CONFIRMED / SUSPECTED / UNCERTAIN`
and `SEV_*`, and `parse_ts()` (ISO-8601 `Z` → aware UTC datetime). Pure data, no
logic beyond formatting — deliberately, so it can't hide behaviour.

### 4.5 `siem_investigator/ingest.py` — Stage 1 (ingest + parse)
- **`load(path)`** → reads the JSON file, calls `load_doc`.
- **`load_doc(doc)`** → validates the envelope (`event_id`, `timestamp`,
  `source`) on every row, **skips malformed rows instead of crashing** (counts
  them), parses timestamps, constructs `Event`s, and builds the `EventStore`
  (which builds the host↔ip map). Sets `store.ingest_stats`.
- Raises `IngestError` only if the file has no `events` array at all.

Design point: forgiving about *optional* fields (real logs are messy), strict
about the *envelope* (so nothing downstream can cite a phantom).

### 4.6 `siem_investigator/detectors.py` — Stage 2 (detect) — the brains
This is where the attack is actually *found and judged*, deterministically. It
has helpers, twelve detectors, a registry, and a precision pass.

**Helpers**
- `is_internal(ip)` — RFC1918/private check via `ipaddress`.
- `off_hours(ts)` — outside 08:00–18:00 UTC.
- `basename(proc)` — `"...\\WINWORD.EXE"` → `"winword.exe"`.
- `decode_encoded_ps(cmd)` — base64-decodes a PowerShell `-enc` blob (UTF-16LE)
  to reveal intent (this is how the report shows the C2 URL the payload fetches).
- `_mk(...)` — the `Finding` factory (dedups + sorts evidence/hosts/accounts).

**The twelve detectors** (each takes the `EventStore`, returns `list[Finding]`):

| Function | Looks for | Emits (ATT&CK) | Confidence rule |
|---|---|---|---|
| `detect_initial_access` | Office app → script-host process lineage | T1566.001, T1204.002, T1059.001 | CONFIRMED |
| `detect_encoded_powershell` | `-enc` / hidden+bypass PowerShell | T1059.001, T1027.010 | CONFIRMED if encoded |
| `detect_c2_beaconing` | ≥6 flows to one external IP, regular interval (coefficient of variation < 0.35) | T1071.001 | CONFIRMED |
| `detect_persistence` | `schtasks /create`, Run-key | T1053.005 | CONFIRMED |
| `detect_discovery` | ≥2 recon commands on a host | T1033/T1087.002/T1018/T1016/T1082 | CONFIRMED |
| `detect_lsass_dump` | `comsvcs.dll MiniDump`, procdump lsass | T1003.001 | CONFIRMED |
| `detect_lateral_movement` | type-3 logon to a **server from a known internal host**, corroborated by SMB flow and/or remote exec | T1021.002, T1078.002, (+T1569.002) | **CONFIRMED if ≥2 sources; UNCERTAIN if target has no EDR** |
| `detect_domain_admin_abuse` | admin logon to a DC (4672 / off-hours / from a compromised server) | T1078.002 | CONFIRMED |
| `detect_data_staging` | archiver (7z/rar…) over a share | T1560.001 (+T1039) | CONFIRMED |
| `detect_cloud_mass_access` | ≥5 reads of a sensitive bucket from an external IP | T1530 | CONFIRMED |
| `detect_cloud_exfil` | Copy/Put to a non-org (external) bucket | T1567.002 | CONFIRMED |
| `detect_defense_evasion` | Defender disabled / `wevtutil cl` | T1562.001, T1070.001 | CONFIRMED |

The star is **`detect_lateral_movement`** — it's the cross-source one. For each
network-logon to a server, it looks for (a) a matching SMB flow within ±120s and
(b) a remote-service process on the target within +600s. If it finds either, the
finding is CONFIRMED and its `evidence` spans **two or three sources**; if the
target has no endpoint telemetry at all, it drops to **UNCERTAIN** with a caveat
rather than over-claiming. Two guards prevent false positives: the source must
resolve to a *known internal host* (excludes VPN remote-access), and a benign
admin acting in business hours on a workstation is left for `review_benign`.

**`run_all(store)`** — runs every detector, concatenates the findings.

**`review_benign(store)`** — the **precision pass**. It finds the near-misses and
explicitly rules them benign *with reasons*: a failed-logon burst that is a
self-inflicted lockout (all from the user's own workstation), and a PsExec that
is a business-hours signed-MSI push by an admin. Returns `list[dict]` — this is
what powers "Activity reviewed and ruled benign" in the report and proves the
tool isn't an alert cannon.

### 4.7 `siem_investigator/attack.py` — Stage 4 (enrich)
- **`load_catalogue(path, refresh=False)`** — loads `attack_techniques.json`.
  With `refresh=True` (CLI `--refresh-attack`) it calls `_reconcile_with_live`.
- **`_reconcile_with_live(catalogue)`** — fetches the live MITRE STIX feed
  (needs `requests`), confirms every technique ID we cite still exists, refreshes
  URLs, and prints any drift. Fails soft (keeps local on any error). This is a
  *verification pass against authoritative external data*.
- **`enrich(catalogue, ids)`** — attaches `{name, tactic, url}` to a list of IDs
  (used by reports); surfaces `(unknown technique)` rather than dropping silently.

### 4.8 `siem_investigator/correlate.py` — Stage 3 (correlate)
Turns a bag of findings into one ordered incident.
- **`assign_ids_and_order(findings)`** — sorts by `ts`, assigns `F-001…` in
  chronological order (so IDs and the timeline agree).
- **`build_stats(store, findings)`** — the summary numbers (events, findings,
  technique/tactic counts, first/last activity, duration, confirmed/uncertain).
- **`attack_path(findings)`** — reads each finding's `data.src_host/dst_host`
  (set by the lateral/priv-esc detectors) into directional hops:
  `WKS-2471 → SRV-FILES01 → DC01 / SRV-SQL01`.
- **`techniques_by_tactic(findings, catalogue)`** — groups techniques under their
  tactic in kill-chain order, for the ATT&CK matrix.

### 4.9 `siem_investigator/blast_radius.py` — Stage 5 (assess)
Rolls findings up into the CISO's questions.
- **`hosts_blast(findings)`** — every host mentioned, with a **status = the
  strongest finding touching it** (`_strongest` — uncertainty is never rounded
  up), a role (`_role_for_host`), its findings, techniques, and evidence.
- **`accounts_blast(findings, store)`** — every account, classified by how it was
  used (phished / harvested / domain-admin) from the phases it appears in.
- **`cloud_blast(findings, store)`** — buckets touched (source + external
  destination), actions, external IPs — read from Collection/Exfiltration
  findings' evidence.
- **`coverage_gaps(store, findings, hosts)`** — the honest limits, grounded in:
  (1) the dataset's own `coverage_note`s, (2) whole source types absent (email/
  DNS/proxy), (3) any host whose **rolled-up** status is UNCERTAIN, and (4) the
  observed log-clearing. Keying #3 on the rolled-up status (not raw finding
  membership) is why a CONFIRMED host that merely *sourced* an uncertain hop is
  not mislabelled as un-monitored.

### 4.10 `siem_investigator/synthesize.py` — Stage 6 (synthesise + answer)
Turns the `Incident` into the analyst's answers. **Every function here only
reads the IR and formats it — it never decides anything.**

Ten builders, one per question type:

| Function | Answers | Pulls from the Incident |
|---|---|---|
| `q_timeline` | "walk me through the timeline" | `incident.timeline` (each finding: time, phase, title, rationale, **ID + name**, evidence, caveat) |
| `q_initial_access` | "what was the initial access vector" | Initial-Access + Execution findings |
| `q_techniques` | "which ATT&CK techniques" | `incident.attack_by_tactic` (grouped, ID + name) |
| `q_accounts` | "which accounts" | `incident.accounts` + benign account review |
| `q_hosts` | "which hosts did they move to" | `incident.attack_path` + `incident.hosts` |
| `q_exfil` | "is there exfiltration" | Collection + Exfiltration findings + `incident.cloud` |
| `q_blast_radius` | "what is the blast radius" | `incident.hosts/accounts/cloud` + stats |
| `q_gaps` | "where are the coverage gaps" | `incident.gaps` |
| `q_exec_summary` | "3-sentence board summary" | stats + IA/lateral/DC/exfil findings (templated, grounded) |
| `q_ir_actions` | "next 2 hours" | confirmed/uncertain hosts, accounts, C2 IP, abused key — all read from findings |

Helpers: `_cite(evidence)` formats the ID list; `_f(incident, phase)` fetches
findings by phase; `_tech_named` renders `"T1566.001 Spearphishing Attachment"`.

**The intent router** (`answer`) is how free-text questions reach the right
builder. It **scores by keyword overlap**, not first-match: `_score` sums the
word-count of each matching phrase (a multi-word phrase is a stronger signal),
and the highest-scoring intent wins. This is why *"walk me through the timeline
from initial access…"* routes to the **timeline** (`walk me through`=3 +
`timeline`=1 beats `initial access`=2) instead of initial-access. Broad words
that cross-match (a bare `"attack"` hitting "attacker") are deliberately absent.
`CANONICAL` holds the exact 10 brief questions mapped to their builders (used by
`all_answers` / the `questions` command and the HTML "Ask" panel).

### 4.11 `siem_investigator/llm.py` — optional narration + verification
The only place a language model appears, and it is fenced on all sides.
- **`_digest(incident)`** — builds a compact JSON view of the IR (findings +
  evidence IDs + blast radius + gaps). **Deliberately contains no raw logs** — the
  model cannot "reinterpret" a log line it never sees.
- **`narrate(incident)`** — sends the digest to Claude (`claude-opus-4-8`) with a
  strict system prompt ("use only facts in the JSON, cite only supplied IDs,
  preserve UNCERTAIN"), then runs the verification pass and returns
  `(text, reason)`. Fails soft: no key / no SDK / network error → returns
  `(None, reason)` and the deterministic synthesis stands.
- **`verify_citations(text, allowed)`** — the guardrail. Regexes every `F-###` /
  event ID out of the model's output and flags any not in the IR's real ID set
  by rewriting it inline as `EP-9999[UNVERIFIED]`. `valid_ids(incident)` builds
  the allowed set (all finding IDs + all evidence IDs). A unit test proves a
  fabricated ID is flagged and a real one is not.

### 4.12 `siem_investigator/report.py` — rendering
Two renderers over the same `Incident`.
- **`render_cli(incident)`** — the terminal report: header stats, then reuses the
  synthesiser (`q_exec_summary`, `q_timeline`, `q_blast_radius`, `q_gaps`,
  `q_ir_actions`) plus the benign review.
- **`build_html(incident, llm_brief=None)`** — the self-contained interactive
  report. Section builders (`_timeline_html`, `_attack_path_html`,
  `_attack_matrix_html`, `_blast_html`, `_gaps_html`, `_benign_html`, `_qa_html`)
  return HTML fragments that are slotted into `_TEMPLATE` (inline CSS + JS, no
  external requests). Key pieces:
  - `_evchip` renders each evidence ID as a clickable chip with a **source·time
    tooltip**; `showEv()` (JS) opens a drawer showing the raw record.
  - `_evidence_json` embeds the raw JSON of exactly the **cited** events (the
    only clickable ones) so drill-down works fully offline.
  - `_linkify` turns technique IDs into attack.mitre.org links and event IDs into
    drawer triggers inside prose.
  - The "Ask the investigation" panel pre-renders all 10 `CANONICAL` answers;
    `askQ()` (JS) scores a typed question against them client-side.
  - `esc()` HTML-escapes everything (command lines contain quotes/backslashes).
- **`write_html(incident, path, llm_brief)`** — writes the file.

### 4.13 `siem_investigator/pipeline.py` — the wiring
One function, **`run(logs_path, refresh_attack, verbose) → Incident`**, that
calls stages 1–5 in order and packages the `Incident` (attaching `attack_path`,
`attack_by_tactic`, `benign_review`). This is the single entry point every
consumer shares — the guarantee that the CLI, the report, and the tests all see
the same reconstruction. It is pure: same logs in → same `Incident` out.

### 4.14 `siem_investigator/cli.py` + `__main__.py` — the entry point
`__main__.py` is a two-line shim so `python -m siem_investigator` calls
`cli.main()`.
- **`build_parser()`** — argparse: a positional `command` (default `run`), an
  optional `query`, and flags `--logs --out --llm --refresh-attack --no-html
  --json -v`.
- **`main(argv)`** — (1) UTF-8 the streams; (2) parse args; (3) if the first
  token isn't a known command, treat the whole thing as an `ask` query (so you
  can paste a question directly); (4) **always run `pipeline.run()`**; (5)
  dispatch on the command.
- Commands: `run` (default → terminal report + write artifacts), `ask [Q]`
  (answer one question, or start `_interactive` REPL), `questions` (all 10),
  `timeline`, `report` (HTML only), `json` (print the IR).
- **`_write_artifacts`** writes `out/investigation.json` and
  `out/incident_report.html`. **`_maybe_llm`** runs narration only with `--llm`
  and prints the reason to stderr if it falls back.

### 4.15 `tests/` — what is guaranteed
19 tests, runnable via `pytest` or standalone (`python tests/test_x.py`).
- **`test_ingest.py`** (5) — all sources load, host↔ip resolution both ways,
  events sorted + indexed, malformed rows skipped (not fatal), missing `events`
  raises.
- **`test_detectors.py`** (7) — full kill chain detected; **the traceability
  invariant** (no finding cites a phantom event); lateral movement is
  multi-source CONFIRMED; the SQL server stays UNCERTAIN (not over-claimed);
  **precision** (benign `t.walsh`/`m.chen`/`svc_analytics` never become
  findings); all confidence/severity values valid; C2 beacon needs multiple
  flows.
- **`test_pipeline.py`** (7) — incident builds; every technique is in the
  catalogue with a real name; all 10 answers non-empty and **every cited ID is
  real**; exec summary is ~3 sentences; the router matches queries; the LLM
  verifier flags fabrication; and **all 10 brief queries route correctly**.

---

## 5. How a user request is executed, end to end

There are two request shapes. Both start at `__main__.py → cli.main()` and both
run the **entire pipeline** first (it's fast — ~150 ms — and every command needs
the `Incident`).

### Flow A — a full run: `python -m siem_investigator`

```
python -m siem_investigator
        │
__main__.py ─► cli.main(argv=[])
        │
        ├─ _reconfigure_stdout()                      # UTF-8 stdout/stderr
        ├─ build_parser().parse_args([])              # command="run", query=[]
        │
        ├─ incident = pipeline.run("data/siem_logs.json")
        │      1. store   = ingest.load(path)                 # 305 Events + EventStore (indices, host↔ip)
        │      2. findings = detectors.run_all(store)          # 14 Findings, each with evidence IDs
        │         benign   = detectors.review_benign(store)    # 2 dismissed near-misses
        │      3. findings = correlate.assign_ids_and_order(findings)   # F-001…F-014, time-ordered
        │         stats    = correlate.build_stats(store, findings)
        │      4. catalogue = attack.load_catalogue()          # ATT&CK names/tactics/urls
        │      5. hosts    = blast_radius.hosts_blast(findings)
        │         accounts = blast_radius.accounts_blast(findings, store)
        │         cloud    = blast_radius.cloud_blast(findings, store)
        │         gaps     = blast_radius.coverage_gaps(store, findings, hosts)
        │         Incident(...) + attack_path + attack_by_tactic + benign_review
        │
        ├─ llm_brief = _maybe_llm(incident, args.llm)   # None unless --llm
        ├─ print(report.render_cli(incident))           # terminal report
        └─ _write_artifacts(incident, args, llm_brief)
                 ├─ out/investigation.json  = incident.dumps()
                 └─ out/incident_report.html = report.build_html(incident, llm_brief)
```

### Flow B — a question: `python -m siem_investigator ask "is there evidence of data exfiltration?"`

```
cli.main(argv=["ask", "is there evidence of data exfiltration?"])
        │
        ├─ parse → command="ask", query=["is there evidence of data exfiltration?"]
        ├─ incident = pipeline.run(...)                 # same Incident as Flow A
        └─ command=="ask" and query → print( synthesize.answer(incident, query) )
                 │
                 answer(incident, "is there evidence of data exfiltration?")
                 ├─ q = query.lower()
                 ├─ score every intent:  exfil = _score(q, {"exfil","exfiltrat","data exfiltration",…})
                 │        "exfil"(1) + "exfiltrat"(1) + "data exfiltration"(2) = 4   ← highest
                 ├─ best_fn = q_exfil
                 └─ return q_exfil(incident)
                          ├─ collect = _f(incident,"Collection")     # [F-010, F-011]
                          ├─ exfil   = _f(incident,"Exfiltration")   # [F-012]
                          ├─ builds "DATA EXFILTRATION: CONFIRMED." + bullets w/ evidence + caveats
                          └─ appends incident.cloud (buckets, actions, external IPs)
```

The output is a string; `print()` sends it to stdout. Nothing in the answer path
invented anything — `q_exfil` only reformats findings that `detect_cloud_exfil` /
`detect_cloud_mass_access` / `detect_data_staging` already produced, citing their
`evidence` IDs.

### Flow C — the HTML "Ask" box (fully offline, in the browser)
`build_html` pre-rendered all 10 `CANONICAL` answers into the page. Typing a
question and pressing Enter runs `askQ()` (JavaScript): it scores the text
against each question's keywords (`data-q` attribute) and reveals the
best-matching pre-computed answer. No server, no model — the same grounded text,
selected client-side.

---

## 6. Every example query, traced

The brief lists ten example queries. Each is in `CANONICAL` (exact routing) and
each also routes correctly through the free-text scoring router. Here is what
each one triggers and what it reads:

| # | Example query | Router winner (why) | Builder | Reads from Incident | Answer headline |
|---|---|---|---|---|---|
| 1 | "Walk me through the full attack timeline…" | timeline: `walk me through`(3)+`timeline`(1)+`last observed`(2)+`full attack`(2)=8 beats `initial access`(2) | `q_timeline` | `timeline` (all findings) | `ATTACK TIMELINE — … (14 stages)` with ID+name + evidence per step |
| 2 | "What was the initial access vector…" | initial-access: `initial access`(2)+`access vector`(2)+`vector`(1)=5 | `q_initial_access` | Initial-Access + Execution findings | `INITIAL ACCESS VECTOR: Spear-phishing… [F-001]` |
| 3 | "Which MITRE ATT&CK techniques…" | techniques: `technique`+`att&ck`+`mitre`=3 (no bare "attack") | `q_techniques` | `attack_by_tactic` | techniques grouped by tactic, ID + name |
| 4 | "Which user accounts were compromised…" | accounts: `account`(1)+`user account`(2)+`which user`(2)=5 (no "attack" cross-match) | `q_accounts` | `accounts` + benign review | `COMPROMISED / ABUSED ACCOUNTS` (a.novak, j.reyes, svc_backup) |
| 5 | "Which internal hosts did the attacker move to after the initial foothold?" | hosts: `internal host`(2)+`hosts did`(2)+`move to`(2)+`foothold`(1)=7 beats initial-access(0) | `q_hosts` | `attack_path` + `hosts` | attack path + per-host status |
| 6 | "Is there evidence of data exfiltration…" | exfil: `data exfiltration`(2)+`exfil`(1)+`exfiltrat`(1)+`was accessed`(2)=6 | `q_exfil` | Collection/Exfil findings + `cloud` | `DATA EXFILTRATION: CONFIRMED.` |
| 7 | "What is the blast radius — list every affected host and account." | blast: `blast radius`(2)+`every affected`(2)+`affected host`(2)=6 | `q_blast_radius` | `hosts/accounts/cloud` + stats | `BLAST RADIUS` (4 hosts, 3 accounts, 2 cloud) |
| 8 | "Where are the gaps in our log coverage…" | gaps: `gap`(1)+`log coverage`(2)+`coverage`(1)+`confidence`(1)+`limit your`(2)=7 | `q_gaps` | `gaps` | `LOG-COVERAGE GAPS & LIMITS ON CONFIDENCE` (6) |
| 9 | "Give me a 3-sentence executive summary…" | exec: `3-sentence`(2)+`executive summary`(2)+`summary suitable`(2)+`board`(1)+`briefing`(1)=8 | `q_exec_summary` | stats + key findings | `EXECUTIVE SUMMARY (board briefing)` — 3 sentences |
| 10 | "What should the incident response team do in the next 2 hours…" | ir: `what should the`(3)+`incident response`(2)+`response team`(2)+`next 2 hours`(2)+`contain this`(2)=11 | `q_ir_actions` | hosts/accounts/C2 IP/key | `INCIDENT RESPONSE — NEXT 2 HOURS` (6 steps) |

Run any of them:
```powershell
python -m siem_investigator ask "which internal hosts did the attacker move to after the initial foothold?"
python -m siem_investigator questions      # runs all ten at once
```
`test_router_handles_all_ten_brief_queries` in `tests/test_pipeline.py` asserts
every row above lands on the right builder, so this table can't silently rot.

---

## 7. Where trust lives in the code

If you want to audit the anti-fabrication story, these are the exact places:

1. **No model decides anything** — the decision path is `detectors.py →
   correlate.py → blast_radius.py`, all deterministic. `llm.py` is only reached
   from `cli._maybe_llm` behind the `--llm` flag.
2. **Every claim carries evidence** — `Finding.evidence` is a list of real
   `Event.id`s, set by the detector that created it. `test_detectors.
   test_traceability_invariant_no_phantom_citations` fails CI if any evidence ID
   doesn't resolve in the store.
3. **Uncertainty isn't rounded up** — `blast_radius._strongest` and the
   UNCERTAIN branch in `detect_lateral_movement` keep the SQL server honest.
4. **The LLM is checked** — `llm.verify_citations` rewrites any fabricated ID as
   `[UNVERIFIED]`; `test_llm_citation_verification_flags_fabrication` proves it.
5. **The audit trail is real** — `Incident.dumps()` → `out/investigation.json`,
   and `report._evidence_json` embeds the raw cited records in the HTML.

## 8. How to extend it

- **Add a detector:** write `detect_x(store) -> list[Finding]` in `detectors.py`
  (use `_mk(...)`, set real `evidence` IDs and a `confidence`), then add it to the
  `DETECTORS` list. Everything downstream (timeline, ATT&CK, blast radius,
  answers, report) picks it up automatically.
- **Add an ATT&CK technique:** add the ID to `data/attack_techniques.json`; run
  `--refresh-attack` to verify it against the live feed.
- **Add a question type:** write `q_x(incident) -> str` in `synthesize.py`, add
  it to `CANONICAL`, and add its keyword set to `_INTENTS`.
- **Point at a real dataset:** drop a schema-compatible `siem_logs.json` into
  `data/` (or pass `--logs path`). No code changes — the system reads only
  documented fields.
```
