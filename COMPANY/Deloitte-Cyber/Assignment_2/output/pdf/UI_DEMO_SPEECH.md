# Short UI demo speech

## 0. Preflight and launch

- **Command:** `python -m siem_investigator doctor`
- **Say:** “This preflight checks the dataset, source coverage, evidence references, attack path, and exfiltration result before I begin the demo.”

- **Command:** `python -m siem_investigator ui`
- **Expected:** The browser opens at `http://127.0.0.1:8765/`.
- **Say:** “This starts the local investigation workspace. The forensic engine runs locally and does not require an API key.”

## 1. Launch screen

- **Do:** Show the dataset preflight card.
- **Say:** “The system first validates the input: 242 events across endpoint, authentication, network, and cloud storage. At this point the dataset is ready, but no investigation conclusions have been generated.”

## 2. Run investigation

- **Do:** Click **Run investigation**.
- **Say:** “This executes the real Python pipeline, not a saved dashboard. It normalizes the logs, detects behaviors, correlates evidence, adds ATT&CK context, calculates scope, and creates one structured Incident record.”

## 3. Ingest and normalize

- **Say:** “The first stage converts different source schemas into one common event format. The exact original record is also preserved, so every transformation remains auditable.”

## 4. Detect

- **Say:** “Deterministic rules identify behaviors such as encoded PowerShell, C2 beaconing, credential access, lateral movement, collection, and exfiltration. Every finding must reference real supporting event IDs.”

## 5. Correlate

- **Say:** “Correlation connects different records using time, host, account, network direction, and process behavior. This is how isolated alerts become one attack path rather than a list of unrelated events.”

## 6. Enrich and assess

- **Say:** “Confirmed findings are mapped to MITRE ATT&CK and grouped into affected hosts, accounts, and cloud resources. ATT&CK adds standard context; it does not decide whether compromise occurred.”

## 7. Synthesize and present

- **Say:** “The final Incident record powers the UI, CLI, JSON, report, and grounded questions. This keeps every presentation consistent with the same forensic evidence.”

---

## 8. Overview

- **Do:** Open **Overview**.
- **Say:** “The investigation produced 12 evidence-backed findings over 11.9 hours. It reconstructs two pivots from WKSTN-07 to AUTH-SRV-01 and FILE-SRV-02, followed by confirmed external exfiltration.”

## 9. Reconstructed attack path

- **Do:** Point to the three hosts.
- **Say:** “WKSTN-07 was the initial foothold, AUTH-SRV-01 was the first account-based pivot, and FILE-SRV-02 was the final target where finance data was collected and uploaded externally.”

## 10. Attack timeline

- **Do:** Open **Attack timeline**.
- **Say:** “The timeline shows the investigation chronologically. Each finding includes its time, confidence, severity, ATT&CK techniques, caveats, and clickable source evidence.”

## 11. Initial access evidence

- **Do:** Open `EVT-0221`, then `EVT-0222`.
- **Say:** “The endpoint directly shows Word launching a command shell, followed by encoded PowerShell. The execution is observed, but the phishing email itself remains inferred because email telemetry was not provided.”

## 12. Lateral-movement evidence

- **Do:** Open finding `F-007`, then `EVT-0231`, `EVT-0232`, and `EVT-0233`.
- **Say:** “This is the strongest correlation example: SMB traffic is followed by PSEXESVC creation and a SYSTEM shell on the destination. Network and endpoint evidence together confirm PsExec lateral movement.”

## 13. Evidence drawer

- **Do:** Switch between **Original event** and **Normalized view**.
- **Say:** “The normalized view gives detectors consistent fields, while the original event preserves the exact supplied record. This makes the complete transformation and conclusion auditable.”

## 14. Exfiltration evidence

- **Do:** Open `EVT-0238`.
- **Say:** “This cloud audit event directly records `backup_archive.zip`, approximately 2.3 GiB, being uploaded from FILE-SRV-02 to the externally owned bucket `ext-drop-xf9q2`. That is why exfiltration is confirmed.”

## 15. ATT&CK mapping

- **Do:** Open **ATT&CK mapping**.
- **Say:** “The investigation maps established behaviors to 14 ATT&CK techniques across nine tactics. This gives analysts a standard vocabulary and coverage view without allowing ATT&CK labels to replace evidence.”

## 16. Blast radius

- **Do:** Open **Blast radius**.
- **Say:** “The supported scope is three hosts, the `jdavis` account, and one external cloud destination. The same view also reports missing email, DNS, and proxy telemetry so the system does not overstate certainty.”

## 17. Response actions

- **Do:** Open **Response actions**.
- **Say:** “These are evidence-conditioned priorities for the next two hours: isolate affected hosts, contain the account, block C2 and the external destination, preserve evidence, and investigate blind spots.”

- **Say:** “The system recommends actions but never executes containment. High-impact response remains behind a human approval gate.”

## 18. Ask investigation

- **Do:** Open **Ask investigation**.
- **Say:** “This is grounded question answering over the completed Incident record, not unrestricted forensic chat. The supported intents are bounded, and answers are generated from the current evidence.”

## 19. Demonstrate a question

- **Do:** Ask: `Was anything stolen, and which event proves it?`
- **Say:** “The answer should identify the confirmed upload and cite EVT-0238. A user can click the evidence instead of trusting an unsupported generated statement.”

## 20. Closing

- **Say:** “The main design decision was to keep forensic conclusions deterministic and traceable while using agentic structure and optional AI for communication. The result is faster investigation without sacrificing evidence, uncertainty, or human control.”

---

## Emergency 60-second version

- **Overview:** “The system analyzed 242 events and reconstructed a two-hop attack across three hosts, ending in confirmed exfiltration.”
- **Timeline:** “Every finding is chronological, confidence-labelled, and linked to its original evidence.”
- **Correlation:** “F-007 joins SMB, PSEXESVC creation, and a SYSTEM shell to confirm lateral movement.”
- **Exfiltration:** “EVT-0238 directly records a 2.3 GiB upload to an externally owned bucket.”
- **Trust:** “Detection and correlation are deterministic; optional AI only communicates the established Incident record.”
- **Close:** “The system accelerates defensible decisions but keeps containment under human approval.”
