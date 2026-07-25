"""Stage: correlate. Fold independent detector findings into one incident —
assign stable, chronological finding IDs, order the attack timeline, and build
the host/account entity graph (including the directional attack path).

Correlation here is entity- and time-based, not model-based: findings belong to
the same incident because they share hosts/accounts/IPs and sit on a continuous
timeline — a relationship a human can check, not one an LLM asserted.
"""

from __future__ import annotations

from collections import defaultdict

from .model import CONFIRMED, SUSPECTED, UNCERTAIN, EventStore, Finding


def assign_ids_and_order(findings: list[Finding]) -> list[Finding]:
    """Chronological timeline; stable F-### IDs assigned in that order."""
    ordered = sorted(findings, key=lambda f: (f.ts is None, f.ts))
    for i, f in enumerate(ordered, 1):
        f.id = "F-{:03d}".format(i)
    return ordered


def build_stats(store: EventStore, findings: list[Finding]) -> dict:
    times = [f.ts for f in findings if f.ts]
    first, last = (min(times), max(times)) if times else store.window
    techniques = sorted({t for f in findings for t in f.technique_ids})
    tactics = [f.phase for f in findings]
    dwell_h = (last - first).total_seconds() / 3600.0 if times else 0.0
    return {
        "events_ingested": len(store),
        "events_by_source": getattr(store, "ingest_stats", {}).get("by_source", {}),
        "findings": len(findings),
        "techniques_count": len(techniques),
        "tactics_covered": len(set(tactics)),
        "first_malicious_activity": first.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_malicious_activity": last.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "attack_duration_hours": round(dwell_h, 1),
        "confirmed_findings": sum(1 for f in findings if f.confidence == CONFIRMED),
        "suspected_findings": sum(1 for f in findings if f.confidence == SUSPECTED),
        "uncertain_findings": sum(1 for f in findings if f.confidence == UNCERTAIN),
    }


def attack_path(findings: list[Finding]) -> list[dict]:
    """Directional host->host hops reconstructed from lateral/priv-esc findings."""
    edges = []
    seen = set()
    for f in sorted(findings, key=lambda x: (x.ts is None, x.ts)):
        src, dst = f.data.get("src_host"), f.data.get("dst_host")
        if src and dst and (src, dst) not in seen:
            seen.add((src, dst))
            edges.append({"from": src, "to": dst, "via": f.data.get("edge", ""),
                          "finding": f.id, "confidence": f.confidence,
                          "when": f.ts.strftime("%Y-%m-%dT%H:%M:%SZ") if f.ts else None})
    return edges


def techniques_by_tactic(findings: list[Finding], catalogue: dict) -> list[dict]:
    """ATT&CK coverage grouped by tactic, in kill-chain order, for the report."""
    order = catalogue.get("_tactics_order", [])
    by_tactic: dict[str, dict] = defaultdict(dict)
    for f in findings:
        for tid in f.technique_ids:
            meta = catalogue.get(tid, {})
            tactic = meta.get("tactic", f.phase)
            by_tactic[tactic][tid] = {
                "id": tid, "name": meta.get("name", tid), "url": meta.get("url", ""),
                "findings": sorted({x.id for x in findings if tid in x.technique_ids}),
            }
    out = []
    for tactic in order:
        if tactic in by_tactic:
            out.append({"tactic": tactic, "techniques": list(by_tactic[tactic].values())})
    for tactic, techs in by_tactic.items():        # any tactic not in the canonical order
        if tactic not in order:
            out.append({"tactic": tactic, "techniques": list(techs.values())})
    return out
