"""Deterministic verdict synthesis.

Why deterministic? Analysts distrust AI-generated threat verdicts because they
cannot see where a claim came from. Here every verdict is a pure function of
the feed records: each rationale bullet names its source and record ID, and an
IOC with no matches is reported as "no records", never inferred malicious.
The optional LLM layer may re-narrate the report, but it never decides a
verdict.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

LEVEL_MALICIOUS = "malicious"
LEVEL_TEST = "test-file"
LEVEL_NO_RECORDS = "no-records"
LEVEL_INCONCLUSIVE = "inconclusive"

# The EICAR anti-virus test file: present in malware feeds by design, but not
# a threat. Reporting it as "malicious" would be a textbook false positive.
EICAR_HASHES = {
    "44d88612fea8a8f36de82e1278abb02f",                                  # md5
    "3395856ce81f2b7382dee72602f798b642f14140",                          # sha1
    "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",  # sha256
}

THREAT_TYPE_LABELS = {
    "botnet_cc": "Botnet command & control (C2)",
    "payload_delivery": "Payload delivery",
    "payload": "Malware payload",
    "malware_download": "Malware distribution",
    "phishing": "Phishing",
    "credential_theft": "Credential theft",
    "adware": "Adware",
    "unknown": "Unclassified threat",
}

# Informational only. NOT a threat-intel source and never changes a verdict;
# it just helps an analyst instantly recognise well-known infrastructure.
CONTEXT_NOTES = {
    "8.8.8.8": "Google Public DNS resolver - ubiquitous, expected in most environments",
    "8.8.4.4": "Google Public DNS resolver",
    "1.1.1.1": "Cloudflare public DNS resolver",
    "1.0.0.1": "Cloudflare public DNS resolver",
    "9.9.9.9": "Quad9 public DNS resolver",
    "microsoft.com": "Microsoft's primary corporate domain",
    "google.com": "Google's primary domain",
    "windowsupdate.com": "Microsoft Windows Update infrastructure",
}

# "Recently active" window used for the P1/P2 escalation decision.
RECENT_ACTIVITY_DAYS = 90

_DT_FORMATS = (
    "%Y-%m-%d %H:%M:%S UTC",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)


@dataclass
class Verdict:
    level: str = LEVEL_NO_RECORDS
    confidence: str = "n/a"          # high | medium | low | n/a
    confidence_detail: str = ""
    classification: str | None = None
    families: list = field(default_factory=list)
    aliases: list = field(default_factory=list)
    first_seen: str | None = None
    last_seen: str | None = None
    active: bool = False             # online now, or seen within RECENT_ACTIVITY_DAYS
    priority: str = ""
    priority_detail: str = ""
    evidence: list = field(default_factory=list)   # source-cited bullets
    caveats: list = field(default_factory=list)
    context_note: str | None = None
    sources_line: str = ""


def _parse_dt(value) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    v = value.strip()
    for fmt in _DT_FORMATS:
        try:
            return datetime.strptime(v, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _fmt_dt(dt: datetime | None) -> str | None:
    return dt.strftime("%Y-%m-%d %H:%M UTC") if dt else None


def _looks_like_eicar(ioc, positives) -> bool:
    if ioc.value.lower() in EICAR_HASHES:
        return True
    for r in positives:
        if r.source != "MalwareBazaar":
            continue
        for rec in r.records:
            clamav = (rec.get("intelligence") or {}).get("clamav") or []
            blob = " ".join([
                str(rec.get("signature") or ""),
                str(rec.get("file_name") or ""),
                " ".join(str(t) for t in (rec.get("tags") or [])),
                " ".join(str(c) for c in clamav),
            ]).lower()
            if "eicar" in blob:
                return True
    return False


def synthesize(ioc, results) -> Verdict:
    """Fold all feed results for one IOC into a single, source-cited verdict."""
    positives = [r for r in results if r.ok and r.found]
    failures = [r for r in results if not r.ok]
    clean = [r for r in results if r.ok and not r.found]

    v = Verdict()
    v.context_note = CONTEXT_NOTES.get(ioc.value.lower())
    v.sources_line = " | ".join("{}: {}".format(r.source, r.status_word) for r in results)

    first_dt = None
    last_dt = None
    tf_conf = None
    families: list = []
    aliases: list = []
    classification = None
    url_online = False
    urlhaus_url_hit = False
    mb_hit = False
    host_url_count = 0
    evidence: list = []

    def add_family(name) -> None:
        if not name:
            return
        name = str(name)
        if name.lower() in ("unknown malware", "unknown", "none"):
            return
        if name not in families:
            families.append(name)

    def touch_dates(*values) -> None:
        nonlocal first_dt, last_dt
        for s in values:
            dt = _parse_dt(s)
            if dt is None:
                continue
            if first_dt is None or dt < first_dt:
                first_dt = dt
            if last_dt is None or dt > last_dt:
                last_dt = dt

    for r in positives:
        if r.source == "ThreatFox":
            shown = 0
            for rec in r.records:
                fam = rec.get("malware_printable") or rec.get("malware")
                add_family(fam)
                for alias in str(rec.get("malware_alias") or "").split(","):
                    alias = alias.strip()
                    if alias and alias.lower() != "none" and alias not in aliases:
                        aliases.append(alias)
                try:
                    conf = int(rec.get("confidence_level"))
                except (TypeError, ValueError):
                    conf = None
                if conf is not None:
                    tf_conf = conf if tf_conf is None else max(tf_conf, conf)
                threat_type = rec.get("threat_type")
                if classification is None and threat_type:
                    classification = THREAT_TYPE_LABELS.get(str(threat_type), str(threat_type))
                touch_dates(rec.get("first_seen"), rec.get("last_seen"))
                if shown < 4:
                    bits = ["ThreatFox IOC #{}: {}".format(rec.get("id", "?"), rec.get("ioc", ioc.value))]
                    if threat_type:
                        bits.append("threat_type {}".format(threat_type))
                    if fam:
                        bits.append("malware {}".format(fam))
                    if conf is not None:
                        bits.append("confidence {}/100".format(conf))
                    if rec.get("first_seen"):
                        bits.append("first seen {}".format(rec["first_seen"]))
                    tags = rec.get("tags") or []
                    if tags:
                        bits.append("tags [{}]".format(", ".join(str(t) for t in tags[:6])))
                    link = "https://threatfox.abuse.ch/ioc/{}/".format(rec.get("id", ""))
                    evidence.append("{} -> {}".format(", ".join(bits), link))
                    shown += 1
            extra = len(r.records) - shown
            if extra > 0:
                evidence.append("ThreatFox: {} additional record(s) not shown".format(extra))

        elif r.source == "URLhaus":
            for rec in r.records:
                if "url_status" in rec:  # /url/ endpoint response
                    urlhaus_url_hit = True
                    status = str(rec.get("url_status") or "unknown")
                    if status == "online":
                        url_online = True
                    threat = rec.get("threat")
                    if classification is None and threat:
                        classification = THREAT_TYPE_LABELS.get(str(threat), str(threat))
                    touch_dates(rec.get("date_added"), rec.get("last_online"))
                    payloads = rec.get("payloads") or []
                    for p in payloads:
                        add_family(p.get("signature"))
                    bits = [
                        "URLhaus entry #{}: status {}".format(rec.get("id", "?"), status.upper()),
                        "threat {}".format(threat or "n/a"),
                        "added {}".format(rec.get("date_added", "?")),
                    ]
                    tags = rec.get("tags") or []
                    if tags:
                        bits.append("tags [{}]".format(", ".join(str(t) for t in tags[:6])))
                    if payloads:
                        p0 = payloads[0]
                        pay = "payload {} ({})".format(
                            p0.get("filename") or str(p0.get("response_sha256", "?"))[:16],
                            p0.get("file_type", "?"),
                        )
                        if p0.get("signature"):
                            pay += ", signature {}".format(p0["signature"])
                        bits.append(pay)
                    ref = rec.get("urlhaus_reference") or "https://urlhaus.abuse.ch/"
                    evidence.append("{} -> {}".format(", ".join(bits), ref))
                else:  # /host/ endpoint response
                    try:
                        count = int(rec.get("url_count") or 0)
                    except (TypeError, ValueError):
                        count = 0
                    host_url_count = max(host_url_count, count)
                    touch_dates(rec.get("firstseen"))
                    urls = rec.get("urls") or []
                    online = sum(1 for u in urls if u.get("url_status") == "online")
                    if online:
                        url_online = True
                    for u in urls:
                        touch_dates(u.get("date_added"))
                    head = "URLhaus host: {} malicious URL(s) recorded".format(count)
                    if online:
                        head += " ({} currently ONLINE)".format(online)
                    bits = [head]
                    blacklists = rec.get("blacklists") or {}
                    listed = [
                        "{}: {}".format(k, val)
                        for k, val in blacklists.items()
                        if val and str(val) != "not listed"
                    ]
                    if listed:
                        bits.append("blocklists [{}]".format("; ".join(listed)))
                    ref = rec.get("urlhaus_reference") or "https://urlhaus.abuse.ch/host/{}/".format(ioc.value)
                    evidence.append("{} -> {}".format(", ".join(bits), ref))
                    if classification is None and count:
                        classification = "Host distributing malicious URLs"

        elif r.source == "MalwareBazaar":
            for rec in r.records:
                mb_hit = True
                add_family(rec.get("signature"))
                touch_dates(rec.get("first_seen"), rec.get("last_seen"))
                sha = str(rec.get("sha256_hash") or "")
                clamav = (rec.get("intelligence") or {}).get("clamav") or []
                bits = [
                    "MalwareBazaar sample {}..".format(sha[:16]) if sha else "MalwareBazaar sample",
                    "file {} ({}, {} bytes)".format(
                        rec.get("file_name", "?"), rec.get("file_type", "?"), rec.get("file_size", "?")
                    ),
                ]
                if rec.get("signature"):
                    bits.append("signature {}".format(rec["signature"]))
                tags = rec.get("tags") or []
                if tags:
                    bits.append("tags [{}]".format(", ".join(str(t) for t in tags[:6])))
                if clamav:
                    bits.append("ClamAV [{}]".format("; ".join(str(c) for c in clamav[:3])))
                if rec.get("first_seen"):
                    bits.append("first seen {}".format(rec["first_seen"]))
                link = "https://bazaar.abuse.ch/sample/{}/".format(sha) if sha else "https://bazaar.abuse.ch/"
                evidence.append("{} -> {}".format(", ".join(bits), link))
                if classification is None:
                    classification = "Known malware sample"

    v.families = families
    v.aliases = aliases[:6]
    v.first_seen = _fmt_dt(first_dt)
    v.last_seen = _fmt_dt(last_dt)
    v.evidence = evidence

    now = datetime.now(timezone.utc)
    recently_seen = last_dt is not None and (now - last_dt) <= timedelta(days=RECENT_ACTIVITY_DAYS)
    v.active = bool(url_online or recently_seen)

    if positives and _looks_like_eicar(ioc, positives):
        v.level = LEVEL_TEST
        v.classification = "EICAR anti-virus test file - harmless by design"
        v.confidence = "high"
        v.confidence_detail = "exact hash match on the industry-standard AV test file"
        v.active = False
        v.priority = "P3"
        v.priority_detail = (
            "Informational - EICAR is used to test AV pipelines. Worth asking why it "
            "appeared in telemetry, but it is not malware"
        )
        for r in failures:
            v.caveats.append("{} could not be checked ({})".format(r.source, r.error))

    elif positives:
        v.level = LEVEL_MALICIOUS
        v.classification = classification or "Known-bad indicator (see evidence)"
        n_sources = len({r.source for r in positives})
        if tf_conf is not None:
            base = "high" if tf_conf >= 75 else ("medium" if tf_conf >= 50 else "low")
            detail = "ThreatFox reporter confidence {}/100".format(tf_conf)
        elif mb_hit:
            base, detail = "high", "exact sample match in MalwareBazaar"
        elif urlhaus_url_hit:
            if url_online:
                base, detail = "high", "URL is currently ONLINE per URLhaus"
            else:
                base, detail = "medium", "URLhaus entry is historical (URL currently offline)"
        else:
            base = "medium"
            detail = "host has {} recorded malicious URL(s) in URLhaus".format(host_url_count)
        if n_sources >= 2:
            base = {"low": "medium", "medium": "high", "high": "high"}[base]
            detail += "; corroborated by {} independent feeds".format(n_sources)
        v.confidence = base
        v.confidence_detail = detail

        if v.active:
            v.priority = "P1"
            v.priority_detail = (
                "Act now - block at proxy/firewall/mail gateway and hunt for related "
                "traffic; indicator is online or active within the last {} days".format(RECENT_ACTIVITY_DAYS)
            )
        else:
            v.priority = "P2"
            v.priority_detail = (
                "Investigate - confirmed malicious but stale/offline; block cheaply, "
                "then hunt logs retrospectively around the first/last-seen window"
            )
        for r in failures:
            v.caveats.append(
                "{} could not be checked ({}); verdict is based on the remaining sources".format(r.source, r.error)
            )

    elif failures:
        v.level = LEVEL_INCONCLUSIVE
        v.priority = "P3"
        v.priority_detail = (
            "Treat as UNKNOWN, not clean - one or more sources could not be checked; "
            "re-run when they are reachable"
        )
        for r in clean:
            v.evidence.append("{}: no records ({}, as of {})".format(r.source, r.query, r.queried_at))
        for r in failures:
            v.evidence.append("{}: ERROR - {}".format(r.source, r.error))

    else:
        v.level = LEVEL_NO_RECORDS
        v.priority = "P4"
        v.priority_detail = (
            "No action indicated by these feeds. Absence of evidence is not proof of "
            "benign - cross-check other sources (VirusTotal, AbuseIPDB, passive DNS) "
            "before closing"
        )
        for r in clean:
            v.evidence.append("{}: no records for this indicator ({}, as of {})".format(r.source, r.query, r.queried_at))
        v.caveats.append(
            "abuse.ch feeds index reported-malicious indicators only; a miss means "
            "'not in these feeds today', not 'clean'"
        )

    return v
