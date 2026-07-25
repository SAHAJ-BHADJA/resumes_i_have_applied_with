"""Stage: assess blast radius. Roll findings up into the questions a CISO asks —
which hosts, which accounts, which data — each with an explicit confidence badge
and the evidence behind it, plus an honest enumeration of the log-coverage gaps
that cap how far the reconstruction can go.

The confidence badge on a host/account is the *strongest* finding that touches
it: a host reached only by an UNCERTAIN finding stays UNCERTAIN. We never round
uncertainty up.
"""

from __future__ import annotations

from collections import defaultdict

from .model import CONFIRMED, SUSPECTED, UNCERTAIN, EventStore, Finding

_RANK = {CONFIRMED: 3, SUSPECTED: 2, UNCERTAIN: 1}


def _strongest(confidences: list[str]) -> str:
    return max(confidences, key=lambda c: _RANK.get(c, 0)) if confidences else UNCERTAIN


def _role_for_host(host: str, findings: list[Finding]) -> str:
    phases = {f.phase for f in findings}
    if "Initial Access" in phases:
        return "Patient zero (initial foothold)"
    if "Privilege Escalation" in phases:
        return "Domain controller (domain compromise)"
    if "Collection" in phases:
        return "Data source (PHI staged here)"
    if "Lateral Movement" in phases:
        return "Lateral-movement target"
    return "Involved host"


def hosts_blast(findings: list[Finding]) -> dict:
    by_host: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        for h in f.hosts:
            by_host[h].append(f)

    out = {}
    for host, fs in sorted(by_host.items()):
        status = _strongest([f.confidence for f in fs])
        out[host] = {
            "status": status,
            "role": _role_for_host(host, fs),
            "findings": sorted({f.id for f in fs}),
            "techniques": sorted({t for f in fs for t in f.technique_ids}),
            "first_seen": min(f.ts for f in fs if f.ts).strftime("%Y-%m-%dT%H:%M:%SZ") if any(f.ts for f in fs) else None,
            "evidence": sorted({e for f in fs for e in f.evidence})[:12],
            "note": _host_note(host, fs, status),
        }
    return out


def _host_note(host: str, fs: list[Finding], status: str) -> str:
    if status == UNCERTAIN:
        return ("Access confirmed but actions unobservable — see coverage gaps. "
                "In the blast radius, but the depth of compromise is unknown.")
    if status == CONFIRMED:
        return "Compromise confirmed by direct, multi-source evidence."
    return "Involvement indicated by a single-source signal; corroborate before final scoping."


def accounts_blast(findings: list[Finding], store: EventStore) -> dict:
    by_acct: dict[str, list[Finding]] = defaultdict(list)
    for f in findings:
        for a in f.accounts:
            by_acct[a].append(f)

    out = {}
    for acct, fs in sorted(by_acct.items()):
        phases = {f.phase for f in fs}
        if "Initial Access" in phases:
            usage = "Phished — the user whose session executed the initial payload"
        elif "Privilege Escalation" in phases:
            usage = "Domain-admin credentials abused for domain takeover"
        elif "Credential Access" in phases:
            usage = "Credentials exposed via LSASS dump on a compromised host"
        elif any(p in phases for p in ("Lateral Movement", "Collection", "Exfiltration")):
            usage = "Harvested credentials used for lateral movement / data theft"
        else:
            usage = "Used in attacker activity"
        out[acct] = {
            "status": _strongest([f.confidence for f in fs]),
            "usage": usage,
            "findings": sorted({f.id for f in fs}),
            "seen_on_hosts": sorted({h for f in fs for h in f.hosts}),
            "evidence": sorted({e for f in fs for e in f.evidence})[:10],
        }
    return out


def cloud_blast(findings: list[Finding], store: EventStore) -> dict:
    resources: dict[str, dict] = {}
    for f in findings:
        if f.phase not in ("Collection", "Exfiltration"):
            continue
        for e in f.evidence:
            ev = store.get(e)
            if not ev or ev.source != "cloud_storage":
                continue
            b = ev.get("bucket")
            if b:
                r = resources.setdefault(b, {"type": "S3 bucket (source)", "status": CONFIRMED,
                                             "actions": set(), "findings": set(), "external_ips": set()})
                r["actions"].add(ev.get("event_type"))
                r["findings"].add(f.id)
                if not _is_internal(ev.get("src_ip")):
                    r["external_ips"].add(ev.get("src_ip"))
            if ev.get("dst_bucket"):
                resources.setdefault(ev.get("dst_bucket"), {
                    "type": "S3 bucket (external / attacker-controlled destination)",
                    "status": CONFIRMED, "actions": {"CopyObject"}, "findings": {f.id}, "external_ips": set()})
    # jsonify sets
    for r in resources.values():
        r["actions"] = sorted(a for a in r["actions"] if a)
        r["findings"] = sorted(r["findings"])
        r["external_ips"] = sorted(ip for ip in r["external_ips"] if ip)
    return resources


def _is_internal(ip):
    import ipaddress
    try:
        return ipaddress.ip_address(ip).is_private
    except (ValueError, TypeError):
        return False


# --------------------------------------------------------------------------- #
# Coverage gaps — grounded in the dataset metadata + finding caveats, so the
# "here's what I can't tell you" answer is as evidence-based as the findings.
# --------------------------------------------------------------------------- #
def coverage_gaps(store: EventStore, findings: list[Finding], hosts: dict | None = None) -> list[dict]:
    gaps: list[dict] = []
    meta_sources = (store.metadata.get("sources") or {})

    # 1) declared collection gaps straight from the export's own metadata
    notes_blob = ""
    for src, spec in meta_sources.items():
        note = spec.get("coverage_note")
        if note:
            notes_blob += " " + note.lower()
            gaps.append({
                "gap": note,
                "source": "{} metadata".format(src),
                "impact": _impact_for_note(note),
            })

    # 2) whole source types absent from this SIEM (named so the reader knows the
    #    frame) -- but skip any already described by a metadata coverage note.
    for kw, label, why in [
        ("email", "email/messaging", "the spear-phishing email that delivered initial access cannot be examined directly"),
        ("dns", "DNS", "C2 and exfil destinations cannot be resolved to domains"),
        ("proxy", "web-proxy/URL", "URL-level C2 and web-based exfiltration cannot be inspected"),
    ]:
        if kw not in notes_blob:
            gaps.append({
                "gap": "No {} logs are collected.".format(label),
                "source": "source inventory",
                "impact": why.capitalize() + ".",
            })

    # 3) hosts whose OVERALL status is UNCERTAIN -> observability blind spot.
    #    Keyed on the rolled-up blast-radius status, not raw finding membership,
    #    so a CONFIRMED host that merely *sourced* an uncertain hop is not flagged.
    for host, rec in sorted((hosts or {}).items()):
        if rec.get("status") == UNCERTAIN:
            gaps.append({
                "gap": "No endpoint telemetry on {} despite confirmed authenticated access.".format(host),
                "source": "correlation ({} UNCERTAIN)".format(host),
                "impact": "Cannot determine what the attacker did on {}; scoped as accessed-but-unexplained.".format(host),
            })

    # 4) anti-forensic destruction observed in-band
    if any("clear" in f.title.lower() or "T1070.001" in f.technique_ids for f in findings):
        gaps.append({
            "gap": "The attacker cleared the Security event log on at least one host.",
            "source": "finding (T1070.001)",
            "impact": "Local evidence after the clear is destroyed; absence of later events on that host is not "
                      "proof of inactivity.",
        })
    return gaps


def _impact_for_note(note: str) -> str:
    low = note.lower()
    if "sql" in low or "edr" in low:
        return "Actions on that host are a blind spot; its compromise depth is UNCERTAIN."
    if "size" in low or "bytes" in low:
        return "Exact exfiltrated data volume cannot be computed; object counts are a floor, not a total."
    if "dns" in low or "proxy" in low:
        return "C2/exfil destinations cannot be resolved to domains or URLs."
    return "Limits confidence in the affected part of the reconstruction."
