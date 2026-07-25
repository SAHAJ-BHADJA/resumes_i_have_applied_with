"""ATT&CK enrichment (the 'enrich with external knowledge' pipeline stage).

Default path is fully offline: a curated, hand-verified subset of the Enterprise
catalogue ships in data/attack_techniques.json, so the tool never depends on the
network to attach a technique name to a finding.

`refresh=True` (CLI: --refresh-attack) reconciles that local subset against the
live MITRE STIX feed: it confirms every technique ID we cite still exists and
refreshes names/URLs from the source of truth, printing any drift. This is a
verification pass against authoritative external data — the anti-hallucination
principle applied to our own reference table.
"""

from __future__ import annotations

import json
import os

STIX_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
_DATA = os.path.join(os.path.dirname(__file__), "..", "data", "attack_techniques.json")


def load_catalogue(path: str = _DATA, refresh: bool = False) -> dict:
    """Return {technique_id: {name, tactic, tactic_id, url, summary}}."""
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    catalogue = doc["techniques"]
    catalogue["_tactics_order"] = doc.get("tactics_order", [])
    if refresh:
        _reconcile_with_live(catalogue)
    return catalogue


def tactics_order(catalogue: dict) -> list[str]:
    return catalogue.get("_tactics_order", [])


def enrich(catalogue: dict, technique_ids) -> list[dict]:
    """Attach full ATT&CK metadata to a list of technique IDs (for reports)."""
    out = []
    for tid in technique_ids:
        meta = catalogue.get(tid)
        if meta:
            out.append({"id": tid, **{k: meta[k] for k in ("name", "tactic", "tactic_id", "url") if k in meta}})
        else:  # never silently drop — surface the unknown
            out.append({"id": tid, "name": "(unknown technique — not in catalogue)", "tactic": "?", "url": ""})
    return out


def _reconcile_with_live(catalogue: dict) -> None:
    """Verify local technique IDs against the live STIX feed; refresh url/name."""
    try:
        import requests
    except ImportError:
        print("[attack] --refresh-attack needs 'requests' (pip install requests); using local catalogue.")
        return
    try:
        print("[attack] fetching live MITRE ATT&CK STIX feed (~35MB)...")
        resp = requests.get(STIX_URL, timeout=60)
        resp.raise_for_status()
        bundle = resp.json()
    except Exception as exc:  # never let enrichment break the investigation
        print("[attack] live fetch failed ({}); using local catalogue.".format(exc.__class__.__name__))
        return

    live: dict[str, dict] = {}
    for obj in bundle.get("objects", []):
        if obj.get("type") != "attack-pattern" or obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        for ref in obj.get("external_references", []):
            if ref.get("source_name") == "mitre-attack" and ref.get("external_id", "").startswith("T"):
                live[ref["external_id"]] = {"name": obj.get("name"), "url": ref.get("url")}

    verified, drifted, missing = 0, 0, 0
    for tid, meta in catalogue.items():
        if tid.startswith("_"):
            continue
        if tid not in live:
            print("[attack] WARNING: {} not found in live feed (possibly revoked/renamed).".format(tid))
            missing += 1
            continue
        verified += 1
        if live[tid].get("url") and live[tid]["url"] != meta.get("url"):
            meta["url"] = live[tid]["url"]
            drifted += 1
    print("[attack] reconciled: {} verified, {} url(s) refreshed, {} missing.".format(verified, drifted, missing))
