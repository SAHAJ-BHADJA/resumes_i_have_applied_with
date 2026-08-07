# Code walkthrough

## End-to-end flow

Both `python -m siem_investigator` and `python -m siem_investigator ui` enter through `siem_investigator/__main__.py` and `cli.py`. The CLI calls `pipeline.run()` directly; the UI command starts the loopback server in `web.py`, whose investigation endpoint calls the same pipeline entry point.

1. `ingest.py` reads the JSON and adds canonical aliases for the supplied field names (`source_type`, `event_name`, `hostname`, `username`, and related fields). The exact input object remains available as `original_event`.
2. `model.py` creates the sorted `EventStore`, indexes event IDs, and resolves observed host/IP pairs.
3. `detectors.py` evaluates explicit behavioural rules. It does not read the dataset's `ATTACK:` validation notes.
4. `correlate.py` orders findings, assigns stable `F-###` identifiers, and builds the directional attack path.
5. `attack.py` attaches technique names and URLs from `data/attack_techniques.json`.
6. `blast_radius.py` rolls findings into affected hosts, accounts, cloud resources, and telemetry gaps.
7. `synthesize.py` answers the assignment questions and produces evidence-conditioned containment advice.
8. `report.py` renders the terminal view and the self-contained HTML artifact.

## Live UI request flow

```text
Browser: click Run investigation
  -> POST /api/investigate
  -> web.InvestigationHandler._run_investigation()
  -> pipeline.run(data/siem_logs.json)
  -> Incident
  -> web._incident_payload()
  -> overview, timeline, ATT&CK, scope, gaps, actions, questions
```

Evidence remains server-side until requested:

```text
Browser: click EVT-0238
  -> GET /api/evidence/EVT-0238
  -> EventStore.get("EVT-0238")
  -> normalized aliases + exact original_event
  -> evidence drawer
```

Question answering uses the completed in-memory incident:

```text
Browser: ask a question
  -> POST /api/ask
  -> synthesize.answer(incident, query, use_llm=False)
  -> grounded answer with clickable event IDs
```

The browser never implements detection, confidence, correlation, or ATT&CK mapping. It is a thin presentation layer over the structured Incident IR.

### UI files

- `siem_investigator/web.py` - loopback HTTP server, API validation, incident serialization, and on-demand evidence retrieval.
- `siem_investigator/ui/index.html` - semantic application layout and accessible controls.
- `siem_investigator/ui/app.css` - responsive analyst workspace design.
- `siem_investigator/ui/app.js` - calls the APIs and renders the Incident IR.
- `tests/test_web_ui.py` - exercises dataset preflight, live investigation, evidence retrieval, grounded Q&A, and the pre-investigation guard.

## Key correlation examples

### Initial access

`detect_initial_access()` identifies Office-to-command-interpreter lineage. In this dataset, `EVT-0221` records `WINWORD.EXE -> cmd.exe`; `EVT-0222` records the encoded PowerShell child process.

### Credential-enabled pivot

`detect_lsass_dump()` connects LSASS access (`EVT-0226`) with the temp dump (`EVT-0227`). `detect_valid_account_pivot()` then connects that credential access to the `jdavis` network logon from `WKSTN-07` to `AUTH-SRV-01` (`EVT-0228`).

### PsExec lateral movement

`detect_lateral_movement()` correlates three independently collected records:

- `EVT-0231`: SMB from `AUTH-SRV-01` to `FILE-SRV-02`
- `EVT-0232`: `PSEXESVC` service created on `FILE-SRV-02`
- `EVT-0233`: SYSTEM-level shell launched by `PSEXESVC.exe`

### Collection and exfiltration

`EVT-0236` starts 7-Zip against the `finance-data` share and `EVT-0237` records the resulting 2.3 GiB archive. `EVT-0238` records its upload to bucket `ext-drop-xf9q2`, whose owner is explicitly `EXTERNAL`.

## Verification

`tests/test_supplied_dataset.py` is the authoritative regression suite. It asserts the exact event count/source distribution, two-hop path, blast radius, key evidence IDs, dataset-specific summary, safe containment language, and preservation of original source records.

`tests/test_web_ui.py` verifies that the UI is a working client of the real pipeline rather than a static mock.

Run:

```powershell
python -m pytest -q
python -m siem_investigator doctor
python -m siem_investigator ui
```
