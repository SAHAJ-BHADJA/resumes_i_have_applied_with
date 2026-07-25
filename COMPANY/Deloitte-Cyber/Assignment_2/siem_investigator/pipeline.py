"""The agentic pipeline, wired end-to-end.

    ingest -> detect -> correlate -> enrich (ATT&CK) -> assess blast radius
           -> package the Incident IR

Each stage consumes the previous stage's structured output and adds one layer.
The whole thing is deterministic: same logs in, same Incident out. `run()` is the
single entry point every consumer (CLI, report, tests, LLM narration) shares, so
there is exactly one source of truth for "what happened".
"""

from __future__ import annotations

import os

from . import attack, blast_radius, correlate, detectors, ingest
from .model import Incident

DEFAULT_LOGS = os.path.join(os.path.dirname(__file__), "..", "data", "siem_logs.json")


def run(logs_path: str = DEFAULT_LOGS, refresh_attack: bool = False, verbose: bool = False) -> Incident:
    def step(msg):
        if verbose:
            print("[pipeline] " + msg)

    # 1. ingest + normalise
    store = ingest.load(logs_path)
    step("ingested {} events {}".format(len(store), store.ingest_stats["by_source"]))

    # 2. detect (deterministic) + record what we reviewed-and-dismissed
    findings = detectors.run_all(store)
    benign = detectors.review_benign(store)
    step("detected {} findings; reviewed {} benign near-misses".format(len(findings), len(benign)))

    # 3. correlate: stable IDs + chronological timeline + stats
    findings = correlate.assign_ids_and_order(findings)
    stats = correlate.build_stats(store, findings)

    # 4. enrich with ATT&CK external knowledge
    catalogue = attack.load_catalogue(refresh=refresh_attack)
    step("enriched with ATT&CK ({} techniques mapped)".format(stats["techniques_count"]))

    # 5. assess blast radius + coverage gaps
    hosts = blast_radius.hosts_blast(findings)
    accounts = blast_radius.accounts_blast(findings, store)
    cloud = blast_radius.cloud_blast(findings, store)
    gaps = blast_radius.coverage_gaps(store, findings, hosts)
    step("blast radius: {} hosts, {} accounts, {} cloud resources, {} gaps".format(
        len(hosts), len(accounts), len(cloud), len(gaps)))

    incident = Incident(
        findings=findings, timeline=findings, hosts=hosts, accounts=accounts,
        cloud=cloud, gaps=gaps, techniques=catalogue, store=store, stats=stats,
    )
    # attach derived views used by report/synthesis
    incident.attack_path = correlate.attack_path(findings)
    incident.attack_by_tactic = correlate.techniques_by_tactic(findings, catalogue)
    incident.benign_review = benign
    return incident
