# SIEM Incident Investigation Intelligence

An agentic incident-investigation prototype. It ingests raw multi-source SIEM
logs, **reconstructs a multi-stage attack timeline**, maps every step to **MITRE
ATT&CK**, computes the **blast radius**, and answers an analyst's questions in
natural language — with the **specific log event(s) cited behind every single
claim**. The 6–8 hour manual correlation the brief describes runs here in about
**150 milliseconds**, and produces a board-ready report an analyst can defend
line by line.

Built for the Deloitte Cyber Engineering Round-2 assignment (*Cyber Incident
Investigation Intelligence*).

> The bar in the brief is *"can the CISO hand this reconstructed attack timeline
> to their board and legal team with confidence?"* — so the whole design is
> organised around **trust**: a deterministic engine finds and judges the
> attack (no model in the loop for judgement), every conclusion is a function of
> cited events, and the system states what it **cannot** confirm as plainly as
> what it can.

```
07-19 09:14  Initial Access       Malicious document detonation — winword.exe → powershell.exe   [CONFIRMED]
                                   ATT&CK T1566.001, T1204.002, T1059.001 | evidence EP-0004, EP-0005 [F-001]
07-19 09:14  Command and Control  C2 beaconing — 42 TLS conns to 45.83.140.77 at ~59-min interval [CONFIRMED]
07-19 14:05  Credential Access    LSASS memory dumped via comsvcs.dll MiniDump                    [CONFIRMED]
07-20 02:17  Lateral Movement     svc_backup → SRV-FILES01  (auth 4624 + SMB flow + remote exec)  [CONFIRMED]
07-20 02:41  Privilege Escalation a.novak → DC01 with 4672 elevated token (domain takeover)       [CONFIRMED]
07-20 03:05  Lateral Movement     svc_backup → SRV-SQL01  (authenticated, but no EDR on target)   [UNCERTAIN]
07-21 01:18  Exfiltration         6 PHI objects copied to external bucket exfil-stage-4d2a        [CONFIRMED]
```

---

## Quickstart

```powershell
cd Assignment_2
# Core pipeline needs NO third-party packages — pure standard library.

python -m siem_investigator                     # full run: terminal report + writes out/ artifacts
#   -> out/incident_report.html   (open in any browser — the board-ready artifact)
#   -> out/investigation.json     (machine-readable IR / audit trail)

# Ask the investigation anything (grounded, cited answers):
python -m siem_investigator ask "walk me through the full attack timeline"
python -m siem_investigator ask "is there evidence of data exfiltration?"
python -m siem_investigator ask "what should we do in the next 2 hours?"
python -m siem_investigator ask                 # interactive analyst session

python -m siem_investigator questions           # answer all 10 brief example queries at once
python -m siem_investigator timeline            # just the chronological timeline
python -m siem_investigator json                # emit the structured IR

# Optional layers (degrade gracefully if the dep/key/network is missing):
python -m siem_investigator --llm               # + Claude-narrated, citation-verified brief
python -m siem_investigator --refresh-attack    # reconcile ATT&CK catalogue vs the live STIX feed

python tools/generate_dataset.py                # regenerate the synthetic dataset (deterministic)
python -m pytest tests/ -q                       # 18 tests incl. the traceability invariant
```

**Headline artifact:** open [`out/incident_report.html`](out/incident_report.html)
— a self-contained, offline, interactive report. Click any evidence ID to see
the untouched raw log record; click any technique ID to open attack.mitre.org;
type a question into "Ask the investigation."

---

## One honest note up front: the dataset

The brief references a provided `siem_logs.json`, but **that file was not
included in the copy of the assignment I received** (only the PDF was). Rather
than block, I wrote [`tools/generate_dataset.py`](tools/generate_dataset.py) to
produce a faithful stand-in to the schema the brief describes: **305 events**
across the four source types (endpoint / auth / network / cloud_storage) over a
72-hour window, with a realistic multi-stage intrusion embedded in background
noise, three near-miss decoys, four deliberate coverage gaps, and a metadata
section documenting every schema.

Crucially, **the pipeline is schema-driven** — it reads only the documented
fields and resolves entities from the metadata's asset hint. Drop the real
`siem_logs.json` in `data/` and re-run; nothing else changes. I'd treat the
generator as a bonus (it shows I understand what a realistic attack looks like
end-to-end), not as the deliverable.

---

## What it found (on the synthetic data)

A textbook healthcare breach, fully reconstructed and cross-source corroborated:

- **Initial access** — a spear-phishing document opened by `j.reyes` on `WKS-2471`
  (`winword.exe → powershell.exe -enc …`; the encoded payload decodes to an
  `http://45.83.140.77/a` stager).
- **C2 / persistence / discovery / credential theft** — hidden beaconing to
  `45.83.140.77`, a scheduled task, host+domain recon, and an LSASS memory dump.
- **Lateral movement** — `svc_backup` → `SRV-FILES01`, caught by **triangulating
  three sources at the same instant**: a type-3 logon (auth), an SMB flow to
  :445 (network), and remote service execution (endpoint). *This is exactly the
  class of event the previous "grep with a UI" tool missed.*
- **Privilege escalation** — `a.novak` (domain admin) onto `DC01` with a 4672
  elevated token, from the just-compromised file server → **domain takeover**.
- **Collection + exfiltration** — a 5 GB archive of the PHI file share, then a
  mass read of the `northwind-phi-records-prod` S3 bucket **and** a cross-account
  copy of PHI objects to an attacker-owned bucket → **PHI exfiltration CONFIRMED**.
- **Anti-forensics** — Defender disabled and the Security event log cleared.

**14 findings · 21 ATT&CK techniques · 11 tactics · 4 hosts · 3 accounts · 40.5h.**
13 findings CONFIRMED; **1 held at UNCERTAIN** — `SRV-SQL01` was authenticated to
but has no EDR agent, so the tool refuses to claim what happened there.

---

## Requirements from the brief → where they're met

| Requirement | Where |
|---|---|
| **Multi-source correlation** (endpoint, auth, network, cloud) | `ingest.py` normalises all 4 sources into one event model + host↔ip↔account entity resolution; `detectors.py` correlates *across* them — the lateral-movement finding fuses auth + network + endpoint (`F-007`) |
| **Attack timeline reconstruction** (initial access → priv-esc → lateral → exfil) | `correlate.py` assigns chronological IDs and orders the kill chain; every phase from Initial Access to Exfiltration is reconstructed (`timeline` command / HTML timeline) |
| **MITRE ATT&CK TTP mapping** with technique ID + name per event | `attack.py` + `data/attack_techniques.json` (21 techniques, verified against the live site); every mapped event cites **technique ID + full name** inline in the timeline, grouped by **tactic** in the ATT&CK matrix, and every ID links to attack.mitre.org |
| **Blast radius** + gaps/uncertainty flagged | `blast_radius.py` — hosts/accounts/cloud each with a CONFIRMED/SUSPECTED/UNCERTAIN badge + 6 enumerated coverage gaps |
| **Full traceability** — cite source, timestamp, event ID per claim | Every `Finding` carries the exact event IDs; the HTML report drills each one down to the raw record; a **unit test enforces that no finding can cite a phantom event** |
| **"Correct 'I can't confirm X' beats a fabricated conclusion"** | `SRV-SQL01` stays UNCERTAIN; exfil volume is explicitly *not* quantified; the phishing email is flagged as inferred-not-observed |
| **Agentic workflow** (ingest→parse→correlate→enrich→synthesise→answer) | `pipeline.py` wires the stages; `cli.py` is the loop; intent routing sends each question to the right synthesiser |
| **Verification passes** | `llm.verify_citations()` checks every ID the LLM emits against the real evidence set and flags fabrications inline |

Every example query in the brief works verbatim — see the bottom of this file.

---

## Architecture: the agentic pipeline

```
 raw siem_logs.json (305 events, 4 sources)
        │
        ▼
   INGEST        parse envelope, normalise per-source schemas, resolve
  (ingest.py)    host↔ip↔account entities, build time/host/user indices
        │
        ▼
   DETECT        12 deterministic detectors scan for behaviours; each emits a
 (detectors.py)  Finding with ATT&CK IDs + the EXACT event IDs as evidence +
        │        an explicit confidence (multi-source ⇒ CONFIRMED, no-EDR ⇒ UNCERTAIN)
        │        …and a benign-review pass records near-misses ruled NOT malicious
        ▼
  CORRELATE      cluster into one incident by shared host/account/IP + time;
 (correlate.py)  chronological timeline, stable F-### IDs, directional attack path
        │
        ▼
   ENRICH        attach ATT&CK name/tactic/URL from a local catalogue
  (attack.py)    (verified vs the live MITRE STIX feed with --refresh-attack)
        │
        ▼
   ASSESS        roll up blast radius (hosts/accounts/cloud, strongest-badge-wins)
(blast_radius.py) + enumerate coverage gaps grounded in metadata + finding caveats
        │
        ▼
  SYNTHESISE     deterministic, cited answers to the analyst's questions
 (synthesize.py) ── optional ──►  LLM narration (llm.py): rewrites the IR only,
        │                         then a verification pass rejects any invented ID
        ▼
    ANSWER       terminal report · interactive HTML · JSON audit trail · Q&A
 (report.py/cli) 
```

| Module | Responsibility |
|---|---|
| `ingest.py` | Load + validate against the file's own metadata; normalise 4 schemas; entity resolution |
| `model.py` | `Event`, `Finding`, `EventStore` (indices), `Incident` IR — plain data, serialises to JSON |
| `detectors.py` | 12 deterministic detectors + the benign-review (precision) pass |
| `attack.py` | ATT&CK catalogue load + optional live-STIX reconciliation |
| `correlate.py` | Timeline ordering, stable IDs, attack-path graph, ATT&CK-by-tactic |
| `blast_radius.py` | Affected hosts/accounts/cloud + confidence + coverage gaps |
| `synthesize.py` | Grounded natural-language answers + intent router for the 10 queries |
| `llm.py` | Optional Claude narration (`claude-opus-4-8`), strictly grounded, **citation-verified** |
| `report.py` | Terminal report + self-contained interactive HTML (evidence drill-down) |
| `pipeline.py` / `cli.py` | The wired pipeline + the command-line agentic loop |

> **Want the code-level tour?** [`CODE_WALKTHROUGH.md`](CODE_WALKTHROUGH.md) explains every file in detail, traces exactly how a user request executes function-by-function, and maps all ten example queries to the code that answers them.

## How findings are derived (deterministic, explainable)

| Detector | Fires on | ATT&CK | Confidence logic |
|---|---|---|---|
| Initial access | Office app → script interpreter lineage | T1566.001, T1204.002, T1059.001 | CONFIRMED (unambiguous lineage) |
| Obfuscated PowerShell | `-enc` / hidden+bypass; decodes the blob | T1059.001, T1027.010 | CONFIRMED if encoded |
| C2 beaconing | ≥6 flows to one external IP at a regular interval (CV < 0.35) | T1071.001 | CONFIRMED |
| Persistence | `schtasks /create` / Run-key | T1053.005 | CONFIRMED |
| Discovery | ≥2 recon commands on a host | T1033/T1087.002/T1018/T1016/T1082 | CONFIRMED |
| LSASS dump | `comsvcs.dll MiniDump` / procdump lsass | T1003.001 | CONFIRMED |
| **Lateral movement** | type-3 logon to a server **corroborated by** SMB flow and/or remote exec | T1021.002, T1078.002, T1569.002 | **CONFIRMED if ≥2 sources; UNCERTAIN if target has no EDR** |
| Domain-admin abuse | admin logon to DC (4672 / off-hours / from a compromised server) | T1078.002 | CONFIRMED |
| Data staging | archiver (7z/rar) over a share | T1560.001, T1039 | CONFIRMED |
| Cloud mass access | ≥5 reads of a sensitive bucket from an external IP | T1530 | CONFIRMED |
| Cloud exfil | Copy/Put to a non-org (external) bucket | T1567.002 | CONFIRMED |
| Defense evasion | Defender disabled / `wevtutil cl` | T1562.001, T1070.001 | CONFIRMED |

Confidence is **sourced, not guessed**: CONFIRMED = corroborated across ≥2 log
sources or an unambiguous single artifact; UNCERTAIN = access is visible but the
target has no telemetry, so actions there are a blind spot. The badge on a host
is the *strongest* finding touching it — uncertainty is never rounded up.

---

## Trust & traceability (why a CISO can defend this)

Fabrication is uniquely dangerous in an incident: a hallucinated "no exfiltration"
gets a breach mis-classified and mis-reported to regulators; a hallucinated host
sends a response team to the wrong place. The design attacks this on five fronts:

1. **No model decides what happened.** Detection and judgement are pure
   deterministic code. Same logs in → same findings out, every time. There is no
   temperature, no prompt, nothing to hallucinate in the part that matters.
2. **Every claim cites primary evidence.** Each finding carries the exact event
   IDs; the HTML report drills each down to the raw JSON record. A **test
   enforces the invariant that no finding can reference an event that isn't in
   the store** — a phantom citation fails CI.
3. **Uncertainty is a first-class output.** CONFIRMED / SUSPECTED / UNCERTAIN
   badges, six enumerated coverage gaps, and explicit refusals: `SRV-SQL01`'s
   depth of compromise is "unknown — no EDR," and the exfil *volume* is left
   unquantified because per-object size logging is partial. The tool is built to
   say "I can see access but cannot confirm actions."
4. **The LLM only narrates, and is checked.** With `--llm`, Claude receives the
   **already-built structured IR — never the raw logs** — and is instructed to add
   no facts and cite only supplied IDs. Then a deterministic **verification pass
   extracts every ID in its output and flags any that aren't real** (`EP-9999`
   → `EP-9999[UNVERIFIED]`). If the LLM is unavailable, the deterministic answers
   stand. Trust never depends on the model.
5. **The audit trail is the product.** `out/investigation.json` is the full IR;
   the raw events are embedded in the HTML. An analyst, an auditor, or opposing
   counsel can reproduce or refute any line.

**Where it can still fail** (stated plainly): the *dataset* can lie to us — if a
log is forged or missing, the reconstruction inherits that (we mitigate by
cross-source corroboration and by flagging the log-clearing event); detector
rules have blind spots (a slow beacon under the interval floor, novel TTPs with
no signature); confidence labels are heuristics, not ground truth. This is
**decision support with a human in the loop**, not an autonomous adjudicator.

## Where AI/agents are used — and where they are deliberately not

The brief explicitly asks this, and it's the crux of the design.

- **Deterministic (no LLM):** ingest, detection, cross-source correlation,
  ATT&CK mapping, blast radius, confidence scoring, and all citations. Anything
  that decides *what is true* about the incident is code, because in an
  investigation, reproducibility and traceability outrank fluency.
- **LLM, optional and fenced (`--llm`):** only the final *narration* — turning
  the structured, already-cited findings into board-room prose. It is given the
  IR (not the logs), forbidden from adding facts, and **post-checked** for
  invented citations.
- **AI in *building* this:** implementation was AI-assisted (Claude Code). The
  interesting judgement was architectural — deciding the LLM must be a narrator
  behind a verification gate, not the investigator — which is the point the brief
  is probing.

The mental model: **agentic *structure*, deterministic *substance*.** The
multi-step tool-using workflow (parse → correlate → enrich → synthesise → verify)
is the "agent"; the steps that could hallucinate are replaced with code.

---

## Design decisions & tradeoffs (time-boxed)

- **Deterministic engine + optional LLM shell** — fastest way to make an analyst
  trust an "AI" tool is to make the AI structurally unable to invent a finding.
- **Rule-based detectors over ML** — with ~300 events and a need to *explain
  every alert to a board*, transparent rules beat a black-box classifier; each
  detector's logic is one readable function and one table row.
- **Standard-library core** — the whole pipeline runs on a bare Python install
  (no `pip install` to see the value), so the demo can't be killed by a laptop
  environment; optional layers fail soft.
- **Interactive HTML as the hero artifact** — the deliverable is literally "hand
  it to the board," so the primary output is a self-contained report with
  evidence drill-down, not a wall of terminal text.
- **Precision matters as much as recall** — three near-miss decoys (a benign
  admin PsExec, an account lockout, a high-volume analytics principal) are
  *reviewed and explicitly dismissed with reasons*, so the tool reads as an
  investigator, not an alert cannon. The previous tool lost trust by missing an
  event; the second-fastest way to lose trust is crying wolf.

### Scope cuts (explicit — "strong candidates make thoughtful cuts")

- **Mapped only clearly-evidenced techniques.** I did not claim, e.g., a specific
  encryption sub-technique for the C2 (`T1573`) — from a firewall flow we can see
  port 443 and periodicity but not the crypto, so claiming it would be
  over-reading. Web-protocol C2 (`T1071.001`) is as far as the evidence goes.
- **Confirmed attack path only.** Background noise is separated but not itself
  deeply analysed; I focused the timeline on the intrusion.
- **No live threat-intel enrichment** of the C2 IP (that was Round 1's tool —
  they compose: this reconstructs the incident, that would score the indicators).
- **Single incident assumption.** The correlator folds findings into one incident;
  multi-campaign disambiguation is out of scope for a prototype.

---

## Product thinking: who is this for, and what would make it production-ready?

**Today it best serves a SOC Tier-2/IR analyst under pressure** — the person who
would otherwise spend 6–8 hours correlating by hand. It compresses that to
seconds and hands them a cited draft they can verify and edit, plus a
CISO/board-ready summary and a next-2-hours action list. The CISO and legal team
are *consumers* of its output (the HTML report), not operators.

**To make it production-ready** (in rough priority):

1. **Real connectors** — ingest from Splunk/Sentinel/Elastic + CloudTrail/EDR
   APIs instead of a JSON file; stream, don't batch.
2. **A detection content pipeline** — express detectors as Sigma rules, version
   them, test them, and let content authors add coverage without touching code.
3. **Human-in-the-loop case management** — analyst can confirm/dismiss/annotate
   each finding; those decisions feed back and persist per incident.
4. **Scale & entity resolution from a real CMDB/IdP** — not a metadata hint; and
   time-series baselining so "anomalous" is per-environment, not hard-coded.
5. **Hardened LLM layer** — grounded retrieval over the case store, the citation
   verifier as a hard gate, evals for hallucination rate, and audit logging of
   every prompt/response.
6. **SOAR handoff** — the "next 2 hours" actions become approvable, executable
   playbooks (isolate host, disable account, block IP) with an audit trail.

---

## What I'd improve with another day / week

Sigma-rule detectors + a small rule-test harness; time-series baselining to
replace fixed thresholds; graph-based correlation (a real entity graph with
path-finding) instead of the current entity+time clustering; multi-incident
disambiguation; a diffable per-incident case store so re-runs show what changed;
richer LLM mode (follow-up Q&A grounded via retrieval over the IR); STIX/OpenCTI
export of the reconstructed incident; and packaging (container + a thin web UI
over the same pipeline).

---

## 5-minute walkthrough script (interview deliverable #2)

1. **Problem framing (30s).** 300 log lines, 4 sources, a senior analyst's 6–8
   hours. Bar: a timeline the CISO can hand to the board. The last tool was "grep
   with a UI" and missed a lateral-movement event.
2. **Run it (60s).** `python -m siem_investigator` → open
   `out/incident_report.html`. Top-to-bottom: stat row → 3-sentence exec summary
   → attack path → timeline.
3. **The money shot — traceability (60s).** In the timeline, click the lateral
   movement finding's evidence chips (`AU-0018`, `NW-0038`, `EP-0026`): "three
   independent sources — auth, network, endpoint — agree on one event. That's the
   class of thing the old tool missed, and here's the raw log behind each."
4. **Honesty (45s).** Point at `SRV-SQL01` [UNCERTAIN]: "authenticated access
   confirmed, but no EDR on that box, so we refuse to say what happened there —
   see the coverage gaps." Then the exfil finding: "PHI copy to an external bucket
   is CONFIRMED, but we explicitly *don't* quote a volume — size logging is
   partial."
5. **Precision (30s).** "Activity reviewed and ruled benign" — the admin PsExec
   and the account lockout: "it considered these and dismissed them with reasons."
6. **Agentic + trust story (60s).** The pipeline diagram: parse → correlate →
   enrich → synthesise → **verify**. "A deterministic engine finds and judges;
   the LLM only narrates and is citation-checked." Show `--llm` if a key is handy;
   show a fabricated ID getting `[UNVERIFIED]`.
7. **Close (30s).** The scope cuts + the product/production-ready slide.

*(Fallback: everything runs offline with zero packages; `--llm` degrades to a
one-line notice, so the walkthrough can't be killed by conference-room Wi-Fi.)*

---

## The brief's example queries → all handled

Run any of these verbatim (`python -m siem_investigator ask "…"`), or click them
in the HTML report's "Ask the investigation" panel:

- "Walk me through the full attack timeline from initial access to last observed activity." → **timeline**
- "What was the initial access vector and what evidence supports that conclusion?" → **initial access**
- "Which MITRE ATT&CK techniques did the attacker use? List them with technique IDs." → **ATT&CK table**
- "Which user accounts were compromised or used by the attacker?" → **accounts**
- "Which internal hosts did the attacker move to after the initial foothold?" → **hosts + attack path**
- "Is there evidence of data exfiltration? If so, what was accessed and when?" → **exfiltration**
- "What is the blast radius — list every affected host and account." → **blast radius**
- "Where are the gaps in our log coverage that limit your confidence?" → **coverage gaps**
- "Give me a 3-sentence executive summary suitable for a board briefing." → **exec summary**
- "What should the incident response team do in the next 2 hours to contain this?" → **IR actions**
