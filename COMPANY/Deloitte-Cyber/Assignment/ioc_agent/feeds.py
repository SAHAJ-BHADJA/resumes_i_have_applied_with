"""Clients for the three abuse.ch threat-intelligence feeds.

- ThreatFox      https://threatfox-api.abuse.ch/api/v1/   (IOCs of all types)
- URLhaus        https://urlhaus-api.abuse.ch/v1/         (malicious URLs/hosts)
- MalwareBazaar  https://mb-api.abuse.ch/api/v1/          (malware samples by hash)

Design rules:

- Every lookup returns a FeedResult and never raises. Network, auth, and API
  errors are recorded on the result so the verdict layer can report the gap
  honestly instead of crashing mid-triage.
- Since mid-2025 abuse.ch requires a free Auth-Key (https://auth.abuse.ch/)
  for API access, even though older docs say "no authentication". The key is
  sent when configured; auth failures produce an actionable message.
- ``enable_demo`` swaps live HTTP for canned fixtures so the tool can be
  demonstrated fully offline; the report clearly labels demo output.
- ``requests`` is imported lazily so demo mode runs on a bare Python install.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

THREATFOX_API = "https://threatfox-api.abuse.ch/api/v1/"
URLHAUS_API = "https://urlhaus-api.abuse.ch/v1"
MALWAREBAZAAR_API = "https://mb-api.abuse.ch/api/v1/"

AUTH_HINT = (
    "abuse.ch requires a free Auth-Key for API access (policy change of mid-2025). "
    "Create one at https://auth.abuse.ch/ then set the ABUSECH_AUTH_KEY environment "
    "variable, pass --auth-key, or put the key in an abusech_auth.key file. "
    "For a no-network demo, run with --demo"
)

_auth_key: str | None = None
_timeout: float = 15.0
_demo_fixtures: dict | None = None

# Responses used in demo mode when an indicator has no dedicated fixture —
# shaped exactly like the real APIs' "nothing found" replies.
_DEMO_DEFAULTS = {
    "threatfox_search": {"query_status": "no_result", "data": "Your search did not yield any results"},
    "threatfox_recent": {"query_status": "ok", "data": []},
    "urlhaus_url": {"query_status": "no_results"},
    "urlhaus_host": {"query_status": "no_results"},
    "urlhaus_payload": {"query_status": "no_results"},
    "mb_hash": {"query_status": "hash_not_found"},
}

_AUTH_FAIL_STATUSES = {
    "missing_auth_key",
    "unknown_auth_key",
    "unauthorized",
    "not_authorized",
    "no_auth_key",
}


def set_auth_key(key: str | None) -> None:
    global _auth_key
    _auth_key = key.strip() if key else None


def has_auth_key() -> bool:
    return bool(_auth_key)


def set_timeout(seconds: float) -> None:
    global _timeout
    _timeout = seconds


def enable_demo(fixtures: dict) -> None:
    global _demo_fixtures
    _demo_fixtures = fixtures


def demo_enabled() -> bool:
    return _demo_fixtures is not None


@dataclass
class FeedResult:
    source: str                  # ThreatFox | URLhaus | MalwareBazaar
    query: str                   # human-readable description of the API call made
    ok: bool = False             # source answered authoritatively (hit OR clean miss)
    found: bool = False          # at least one record returned
    records: list = field(default_factory=list)
    error: str | None = None
    queried_at: str = ""
    raw: object = None           # exact parsed API response (traceability / --json)

    @property
    def status_word(self) -> str:
        if not self.ok:
            return "ERROR"
        return "hit" if self.found else "no records"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _call(kind: str, key: str, url: str, *, json_body=None, form=None):
    """Perform one API call (or fixture lookup). Returns (parsed_json, error)."""
    if _demo_fixtures is not None:
        fx = (
            _demo_fixtures.get((kind, key))
            or _demo_fixtures.get((kind, "*"))
            or _DEMO_DEFAULTS[kind]
        )
        return fx, None

    try:
        import requests
    except ImportError:
        return None, "the 'requests' package is not installed (pip install -r requirements.txt), or use --demo"

    headers = {"User-Agent": "ioc-enrichment-agent/0.1 (interview prototype)"}
    if _auth_key:
        headers["Auth-Key"] = _auth_key

    try:
        resp = requests.post(url, json=json_body, data=form, headers=headers, timeout=_timeout)
    except requests.RequestException as exc:
        return None, "network error: {}".format(exc.__class__.__name__)

    try:
        parsed = resp.json()
    except ValueError:
        parsed = None

    qs = str((parsed or {}).get("query_status", "")).lower() if isinstance(parsed, dict) else ""
    if resp.status_code in (401, 403) or qs in _AUTH_FAIL_STATUSES:
        return parsed, AUTH_HINT
    if resp.status_code != 200:
        return parsed, "HTTP {} from {}".format(resp.status_code, url)
    if parsed is None:
        return None, "response was not valid JSON"
    return parsed, None


# ---------------------------------------------------------------- ThreatFox

def threatfox_search(term: str) -> FeedResult:
    res = FeedResult("ThreatFox", 'search_ioc "{}"'.format(term), queried_at=_now())
    raw, err = _call(
        "threatfox_search", term.lower(), THREATFOX_API,
        json_body={"query": "search_ioc", "search_term": term},
    )
    res.raw = raw
    if err:
        res.error = err
        return res
    qs = str(raw.get("query_status", "")).lower()
    if qs == "ok" and isinstance(raw.get("data"), list):
        res.ok = True
        res.records = raw["data"]
        res.found = bool(res.records)
    elif qs in ("no_result", "no_results"):
        res.ok = True
    else:
        res.error = "unexpected ThreatFox response (query_status={!r})".format(qs or None)
    return res


def threatfox_recent(days: int) -> FeedResult:
    days = max(1, min(int(days), 7))  # the API serves at most 7 days
    res = FeedResult("ThreatFox", "get_iocs last {} day(s)".format(days), queried_at=_now())
    raw, err = _call(
        "threatfox_recent", str(days), THREATFOX_API,
        json_body={"query": "get_iocs", "days": days},
    )
    res.raw = raw
    if err:
        res.error = err
        return res
    qs = str(raw.get("query_status", "")).lower()
    if qs == "ok" and isinstance(raw.get("data"), list):
        res.ok = True
        res.records = raw["data"]
        res.found = bool(res.records)
    elif qs in ("no_result", "no_results"):
        res.ok = True
    else:
        res.error = "unexpected ThreatFox response (query_status={!r})".format(qs or None)
    return res


# ------------------------------------------------------------------ URLhaus

def urlhaus_url(url_value: str) -> FeedResult:
    res = FeedResult("URLhaus", "url lookup", queried_at=_now())
    raw, err = _call("urlhaus_url", url_value, URLHAUS_API + "/url/", form={"url": url_value})
    res.raw = raw
    if err:
        res.error = err
        return res
    qs = str(raw.get("query_status", "")).lower()
    if qs == "ok":
        res.ok = True
        res.found = True
        res.records = [raw]
    elif qs in ("no_results", "no_result"):
        res.ok = True
    elif qs == "invalid_url":
        res.error = "URLhaus rejected the URL as invalid"
    else:
        res.error = "unexpected URLhaus response (query_status={!r})".format(qs or None)
    return res


def urlhaus_host(host: str) -> FeedResult:
    res = FeedResult("URLhaus", 'host lookup "{}"'.format(host), queried_at=_now())
    raw, err = _call("urlhaus_host", host.lower(), URLHAUS_API + "/host/", form={"host": host})
    res.raw = raw
    if err:
        res.error = err
        return res
    qs = str(raw.get("query_status", "")).lower()
    if qs == "ok":
        rec = dict(raw)
        urls = rec.get("urls") or []
        if isinstance(urls, list) and len(urls) > 20:
            rec["urls"] = urls[:20]
            rec["urls_truncated_from"] = len(urls)
        try:
            count = int(rec.get("url_count") or 0)
        except (TypeError, ValueError):
            count = 0
        res.ok = True
        res.found = count > 0 or bool(rec.get("urls"))
        res.records = [rec] if res.found else []
    elif qs in ("no_results", "no_result"):
        res.ok = True
    elif qs == "invalid_host":
        res.error = "URLhaus rejected the host as invalid"
    else:
        res.error = "unexpected URLhaus response (query_status={!r})".format(qs or None)
    return res


def urlhaus_payload(hash_value: str, hash_type: str) -> FeedResult:
    param = {"md5": "md5_hash", "sha256": "sha256_hash"}.get(hash_type)
    res = FeedResult("URLhaus", "payload lookup ({})".format(hash_type), queried_at=_now())
    if param is None:
        res.ok = True  # URLhaus payload lookup only supports md5/sha256
        return res
    raw, err = _call(
        "urlhaus_payload", hash_value.lower(), URLHAUS_API + "/payload/",
        form={param: hash_value},
    )
    res.raw = raw
    if err:
        res.error = err
        return res
    qs = str(raw.get("query_status", "")).lower()
    if qs == "ok":
        res.ok = True
        res.found = True
        res.records = [raw]
    elif qs in ("no_results", "no_result"):
        res.ok = True
    else:
        res.error = "unexpected URLhaus response (query_status={!r})".format(qs or None)
    return res


# ------------------------------------------------------------ MalwareBazaar

def mb_hash(hash_value: str) -> FeedResult:
    res = FeedResult("MalwareBazaar", "get_info hash", queried_at=_now())
    raw, err = _call(
        "mb_hash", hash_value.lower(), MALWAREBAZAAR_API,
        form={"query": "get_info", "hash": hash_value},
    )
    res.raw = raw
    if err:
        res.error = err
        return res
    qs = str(raw.get("query_status", "")).lower()
    if qs == "ok" and isinstance(raw.get("data"), list):
        res.ok = True
        res.records = raw["data"]
        res.found = bool(res.records)
    elif qs == "hash_not_found":
        res.ok = True
    elif qs == "illegal_hash":
        res.error = "MalwareBazaar rejected the hash as malformed"
    else:
        res.error = "unexpected MalwareBazaar response (query_status={!r})".format(qs or None)
    return res
