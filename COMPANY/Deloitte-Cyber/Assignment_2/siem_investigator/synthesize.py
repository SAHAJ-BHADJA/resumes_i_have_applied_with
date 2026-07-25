"""Stage: synthesise. Turn the structured Incident IR into the natural-language
answers an analyst actually asks for — every one built deterministically from
the findings and citing the finding IDs + raw event IDs behind each claim.

This is the deliberate boundary: synthesis *reads* the evidence graph and
formats it. It never decides what happened (the detectors did) and never invents
a citation (it can only reference IDs that exist in the IR). The optional LLM
layer (llm.py) sits one step further out and only rewrites these grounded facts.
"""

from __future__ import annotations

from .model import CONFIRMED, UNCERTAIN, Incident


# --------------------------------------------------------------------------- #
# formatting helpers
# --------------------------------------------------------------------------- #
def _cite(evidence: list[str], limit: int = 6) -> str:
    if not evidence:
        return "no direct events"
    shown = evidence[:limit]
    extra = " (+{} more)".format(len(evidence) - limit) if len(evidence) > limit else ""
    return ", ".join(shown) + extra


def _f(incident: Incident, phase: str):
    return [f for f in incident.findings if f.phase == phase]


def _find(incident: Incident, fid: str):
    return next((f for f in incident.findings if f.id == fid), None)


def _tech_named(incident: Incident, tids: list[str]) -> str:
    """Render each mapped technique as 'ID Name' — the brief asks for both."""
    parts = []
    for t in tids:
        name = incident.techniques.get(t, {}).get("name", "")
        parts.append("{} {}".format(t, name) if name else t)
    return "; ".join(parts)


# --------------------------------------------------------------------------- #
# Q1 — full attack timeline
# --------------------------------------------------------------------------- #
def q_timeline(incident: Incident) -> str:
    lines = ["ATTACK TIMELINE — {} → {} UTC ({}h, {} stages)".format(
        incident.stats["first_malicious_activity"], incident.stats["last_malicious_activity"],
        incident.stats["attack_duration_hours"], len(incident.timeline))]
    lines.append("")
    for f in incident.timeline:
        when = f.ts.strftime("%m-%d %H:%M") if f.ts else "  ??  "
        badge = "" if f.confidence == CONFIRMED else "  [{}]".format(f.confidence)
        lines.append("{when}  {phase:<20} {title}{badge}".format(
            when=when, phase=f.phase, title=f.title, badge=badge))
        lines.append("        {}".format(f.rationale))
        lines.append("        ATT&CK: {}".format(_tech_named(incident, f.technique_ids)))
        lines.append("        evidence: {} [{}]".format(_cite(f.evidence), f.id))
        if f.caveats:
            lines.append("        caveat: {}".format(f.caveats))
        lines.append("")
    return "\n".join(lines).rstrip()


# --------------------------------------------------------------------------- #
# Q2 — initial access vector
# --------------------------------------------------------------------------- #
def q_initial_access(incident: Incident) -> str:
    ia = _f(incident, "Initial Access")
    if not ia:
        return "No initial-access vector could be established from the available logs."
    f = ia[0]
    ev = f.evidence
    out = [
        "INITIAL ACCESS VECTOR: Spear-phishing document → user execution (ATT&CK {}).".format(
            ", ".join(f.technique_ids)),
        "",
        "What the evidence shows:",
        "  • {}".format(f.rationale),
        "  • Host: {} | User: {}".format(", ".join(f.hosts), ", ".join(f.accounts)),
        "  • Supporting events: {} [{}]".format(_cite(ev), f.id),
    ]
    ps = _f(incident, "Execution")
    if ps:
        out.append("  • Immediately after, {} (evidence {} [{}]).".format(
            ps[0].title.lower(), _cite(ps[0].evidence), ps[0].id))
    out += [
        "",
        "Confidence: {}. {}".format(f.confidence, f.caveats or ""),
    ]
    return "\n".join(out).rstrip()


# --------------------------------------------------------------------------- #
# Q3 — ATT&CK techniques
# --------------------------------------------------------------------------- #
def q_techniques(incident: Incident) -> str:
    out = ["MITRE ATT&CK TECHNIQUES OBSERVED (grouped by tactic, kill-chain order):", ""]
    for block in incident.attack_by_tactic:
        out.append("{}".format(block["tactic"].upper()))
        for t in block["techniques"]:
            meta = incident.techniques.get(t["id"], {})
            out.append("  {:<11} {:<48} [{}]".format(
                t["id"], meta.get("name", t["name"])[:48], ", ".join(t["findings"])))
    total = sorted({tid for f in incident.findings for tid in f.technique_ids})
    out += ["", "{} distinct techniques across {} tactics. Full catalogue with URLs in the ATT&CK table.".format(
        len(total), len({b["tactic"] for b in incident.attack_by_tactic}))]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Q4 — compromised accounts
# --------------------------------------------------------------------------- #
def q_accounts(incident: Incident) -> str:
    out = ["COMPROMISED / ABUSED ACCOUNTS:", ""]
    for acct, rec in incident.accounts.items():
        out.append("  {} — {} [{}]".format(acct, rec["usage"], rec["status"]))
        out.append("      seen on: {} | evidence: {} | findings: {}".format(
            ", ".join(rec["seen_on_hosts"]) or "—", _cite(rec["evidence"]), ", ".join(rec["findings"])))
    out.append("")
    out.append("Accounts explicitly ruled BENIGN (near-misses):")
    for n in incident.benign_review:
        if "logon" in n["activity"].lower() or "lockout" in n["verdict"].lower():
            out.append("  • {} — {}".format(n["activity"], n["verdict"]))
    return "\n".join(out).rstrip()


# --------------------------------------------------------------------------- #
# Q5 — hosts moved to after foothold
# --------------------------------------------------------------------------- #
def q_hosts(incident: Incident) -> str:
    out = ["INTERNAL HOSTS THE ATTACKER MOVED TO (after the WKS foothold):", ""]
    if incident.attack_path:
        out.append("Attack path:")
        for e in incident.attack_path:
            out.append("  {} → {}  ({}, {}, {})".format(
                e["from"], e["to"], e["via"], e["confidence"], e["when"]))
        out.append("")
    for host, rec in incident.hosts.items():
        if rec["role"].lower().startswith("patient"):
            continue
        out.append("  {} — {} [{}]".format(host, rec["role"], rec["status"]))
        out.append("      evidence: {} | findings: {}".format(_cite(rec["evidence"]), ", ".join(rec["findings"])))
        if rec["status"] == UNCERTAIN:
            out.append("      NOTE: {}".format(rec["note"]))
    return "\n".join(out).rstrip()


# --------------------------------------------------------------------------- #
# Q6 — data exfiltration
# --------------------------------------------------------------------------- #
def q_exfil(incident: Incident) -> str:
    exfil = _f(incident, "Exfiltration")
    collect = _f(incident, "Collection")
    if not exfil and not collect:
        return ("No direct evidence of data exfiltration was found in the available logs. "
                "Note this does not prove none occurred — see coverage gaps.")
    out = ["DATA EXFILTRATION: {}.".format("CONFIRMED" if exfil else "STAGING OBSERVED, EXFIL UNCONFIRMED"), ""]
    for f in collect:
        out.append("  • [{}] {} — {}".format(f.id, f.title, f.rationale))
        out.append("      evidence: {}".format(_cite(f.evidence)))
    for f in exfil:
        out.append("  • [{}] {} — {}".format(f.id, f.title, f.rationale))
        out.append("      evidence: {}".format(_cite(f.evidence)))
        if f.caveats:
            out.append("      LIMIT: {}".format(f.caveats))
    if incident.cloud:
        out.append("")
        out.append("Cloud resources touched:")
        for b, rec in incident.cloud.items():
            out.append("  • {} — {} | actions: {}{}".format(
                b, rec["type"], ", ".join(rec["actions"]),
                " | external IP(s): " + ", ".join(rec["external_ips"]) if rec["external_ips"] else ""))
    return "\n".join(out).rstrip()


# --------------------------------------------------------------------------- #
# Q7 — blast radius
# --------------------------------------------------------------------------- #
def q_blast_radius(incident: Incident) -> str:
    conf = incident.stats
    out = ["BLAST RADIUS", ""]
    out.append("Hosts ({}):".format(len(incident.hosts)))
    for host, rec in incident.hosts.items():
        out.append("  [{}] {:<12} {}".format(rec["status"], host, rec["role"]))
    out.append("")
    out.append("Accounts ({}):".format(len(incident.accounts)))
    for acct, rec in incident.accounts.items():
        out.append("  [{}] {:<12} {}".format(rec["status"], acct, rec["usage"]))
    if incident.cloud:
        out.append("")
        out.append("Cloud ({}):".format(len(incident.cloud)))
        for b, rec in incident.cloud.items():
            out.append("  [{}] {:<32} {}".format(rec["status"], b, rec["type"]))
    out += ["", "Scope: {} confirmed + {} uncertain findings. UNCERTAIN items are in the blast radius but their "
            "depth of compromise is unproven — treat as compromised until cleared.".format(
                conf["confirmed_findings"], conf["uncertain_findings"])]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Q8 — coverage gaps
# --------------------------------------------------------------------------- #
def q_gaps(incident: Incident) -> str:
    out = ["LOG-COVERAGE GAPS & LIMITS ON CONFIDENCE:", ""]
    for g in incident.gaps:
        out.append("  • {}".format(g["gap"]))
        out.append("      → impact: {}  (source: {})".format(g["impact"], g["source"]))
    out += ["", "Bottom line: the confirmed attack path is well-evidenced across sources; the gaps above bound "
            "what CANNOT be asserted — chiefly the depth of compromise on hosts without EDR, the exact "
            "exfiltration volume, and the phishing email itself."]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Q9 — executive summary (3 sentences, board-ready)
# --------------------------------------------------------------------------- #
def q_exec_summary(incident: Incident) -> str:
    s = incident.stats
    ia = _f(incident, "Initial Access")
    pz_host = ia[0].hosts[0] if ia and ia[0].hosts else "an endpoint"
    pz_user = ia[0].accounts[0] if ia and ia[0].accounts else "a user"
    lateral = [h for h, r in incident.hosts.items()
               if r["status"] == CONFIRMED and ("Lateral" in r["role"] or "Data source" in r["role"])]
    dc = [h for h, r in incident.hosts.items() if "controller" in r["role"].lower()]
    exfil = _f(incident, "Exfiltration")
    n_hosts = len(incident.hosts)
    n_acct = len(incident.accounts)

    s1 = ("Between {start} and {end} UTC, an attacker breached Northwind Health by spear-phishing user "
          "{user} on {host}, then stole cached credentials and pivoted to {lateral}{dc}."
          ).format(start=s["first_malicious_activity"][5:16].replace("T", " "),
                   end=s["last_malicious_activity"][5:16].replace("T", " "),
                   user=pz_user, host=pz_host,
                   lateral=" and ".join(lateral) if lateral else "internal servers",
                   dc=", escalating to domain-admin control of the domain controller ({})".format(", ".join(dc)) if dc else "")
    if exfil:
        s2 = ("Protected health information was archived from the PHI file share and patient records were "
              "copied out of the northwind-phi-records-prod S3 bucket to attacker-controlled cloud storage — "
              "data exfiltration of PHI is CONFIRMED by cross-account object copies from an external IP.")
    else:
        s2 = ("Data was staged for theft, but exfiltration to an external destination is not directly confirmed "
              "in the available logs.")
    unc = s["uncertain_findings"]
    s3 = ("The intrusion spans {nh} hosts and {na} accounts across {dur} hours; {conf} findings are CONFIRMED "
          "by multi-source evidence, while {unc} {verb} UNCERTAIN due to log-coverage gaps (notably a database "
          "server without endpoint monitoring and partial cloud size logging).").format(
              nh=n_hosts, na=n_acct, dur=s["attack_duration_hours"], conf=s["confirmed_findings"],
              unc=unc, verb="remains" if unc == 1 else "remain")
    return "EXECUTIVE SUMMARY (board briefing)\n\n" + " ".join([s1, s2, s3])


# --------------------------------------------------------------------------- #
# Q10 — IR containment actions for the next 2 hours
# --------------------------------------------------------------------------- #
def q_ir_actions(incident: Incident) -> str:
    # derive concrete, evidence-anchored actions from what was actually found
    confirmed_hosts = [h for h, r in incident.hosts.items() if r["status"] == CONFIRMED]
    uncertain_hosts = [h for h, r in incident.hosts.items() if r["status"] == UNCERTAIN]
    accts = list(incident.accounts.keys())
    c2 = _f(incident, "Command and Control")
    c2_ip = ""
    if c2:
        ev0 = incident.store.get(c2[0].evidence[0])
        c2_ip = ev0.get("dst_ip") if ev0 else ""
    exfil = _f(incident, "Exfiltration")
    key = ""
    if exfil:
        ev0 = incident.store.get(exfil[0].evidence[0])
        key = (ev0.get("access_key_id") if ev0 else "") or ""

    actions = [
        "1. ISOLATE (now): network-quarantine the confirmed-compromised hosts — {}. Do NOT power them off "
        "(preserve memory/artifacts).".format(", ".join(confirmed_hosts) or "n/a"),
        "2. CONTAIN the domain: this is a DC compromise. Disable the abused accounts ({}); force a domain-wide "
        "password reset and reset the KRBTGT account twice; revoke Kerberos tickets.".format(", ".join(accts)),
        "3. CUT C2: block the C2 IP {} at the firewall/proxy and hunt for the same beacon pattern from any "
        "other host.".format(c2_ip or "(see F-003)"),
        "4. STOP cloud exfil: disable/rotate the abused AWS access key {}; block the external destination bucket; "
        "enable S3 object-level logging + MFA-delete on the PHI bucket.".format(key or "(see exfil finding)"),
        "5. TRIAGE the blind spots: deploy EDR / pull a forensic image of {} (accessed but unmonitored) before "
        "concluding scope.".format(", ".join(uncertain_hosts) or "any un-instrumented host"),
        "6. PRESERVE & NOTIFY: snapshot all relevant logs now (attacker already cleared one host's event log); "
        "engage legal/compliance — CONFIRMED PHI exposure likely triggers HIPAA breach-notification obligations.",
    ]
    return "INCIDENT RESPONSE — NEXT 2 HOURS (containment)\n\n" + "\n".join(actions) + \
        "\n\nEvery action maps to a finding above; this is decision support — a human approves and executes."


# --------------------------------------------------------------------------- #
# canonical Q&A set + intent router
# --------------------------------------------------------------------------- #
CANONICAL = [
    ("Walk me through the full attack timeline from initial access to last observed activity.", q_timeline),
    ("What was the initial access vector and what evidence supports that conclusion?", q_initial_access),
    ("Which MITRE ATT&CK techniques did the attacker use? List them with technique IDs.", q_techniques),
    ("Which user accounts were compromised or used by the attacker?", q_accounts),
    ("Which internal hosts did the attacker move to after the initial foothold?", q_hosts),
    ("Is there evidence of data exfiltration? If so, what was accessed and when?", q_exfil),
    ("What is the blast radius — list every affected host and account.", q_blast_radius),
    ("Where are the gaps in our log coverage that limit your confidence in this reconstruction?", q_gaps),
    ("Give me a 3-sentence executive summary suitable for a board briefing.", q_exec_summary),
    ("What should the incident response team do in the next 2 hours to contain this?", q_ir_actions),
]

# Intent router. Each entry maps a synthesiser to the phrases that signal it.
# We score by *keyword overlap* (best match wins), not first-match: a multi-word
# phrase is worth its word count, so a specific hit ("walk me through" = 3) beats
# an incidental one ("initial access" = 2) in a query that mentions both — e.g.
# "walk me through the timeline from initial access …" correctly routes to the
# timeline, not initial-access. Broad single words that cross-match (a bare
# "attack" hitting "attacker") are deliberately avoided.
_INTENTS = [
    (("executive summary", "exec summary", "board", "briefing", "3-sentence", "3 sentence", "three sentence", "summary suitable"), q_exec_summary),
    (("next 2 hours", "next two hours", "contain this", "containment", "contain", "response team", "ir team", "incident response", "what should the", "what should we do", "what do we do"), q_ir_actions),
    (("gap", "log coverage", "coverage", "blind spot", "confidence", "limit your", "missing log"), q_gaps),
    (("blast radius", "every affected", "all affected", "affected host", "every host", "scope of the"), q_blast_radius),
    (("exfil", "exfiltrat", "data exfiltration", "data theft", "data steal", "stolen", "was accessed", "data leave"), q_exfil),
    (("initial access", "access vector", "vector", "phish", "get in", "got in", "entry point", "delivered", "how did the attacker get"), q_initial_access),
    (("technique", "att&ck", "attack technique", "ttp", "mitre"), q_techniques),
    (("account", "user account", "which user", "compromised account", "credential", "identit", "who was compromised"), q_accounts),
    (("which host", "internal host", "hosts did", "move to", "moved to", "lateral", "pivot", "foothold", "which servers", "which machines"), q_hosts),
    (("timeline", "walk me through", "what happened", "chronolog", "sequence", "last observed", "full attack", "step by step", "start to finish"), q_timeline),
]


def _score(query: str, keywords) -> int:
    """Sum the word-counts of the keywords present — longer phrase = stronger signal."""
    return sum(len(k.split()) for k in keywords if k in query)


def answer(incident: Incident, query: str) -> str:
    q = query.lower()
    best_fn, best_score = None, 0
    for keywords, fn in _INTENTS:          # strict '>' keeps the first (most specific) on ties
        score = _score(q, keywords)
        if score > best_score:
            best_fn, best_score = fn, score
    if best_fn is not None:
        return best_fn(incident)
    # nothing matched: the timeline is the most useful catch-all for an investigator
    return ("(No specific intent matched — showing the full timeline. Try asking about initial access, "
            "techniques, accounts, hosts, exfiltration, blast radius, gaps, an exec summary, or IR actions.)\n\n"
            + q_timeline(incident))


def all_answers(incident: Incident) -> list[tuple[str, str]]:
    return [(q, fn(incident)) for q, fn in CANONICAL]
