"""Agent orchestration: the plan -> act -> synthesise middle of the loop.

For each IOC the agent builds a lookup plan (which feeds, which endpoints,
driven by the IOC type), executes it, and hands the collected evidence to the
verdict layer. Batches run IOCs concurrently with a small worker pool to stay
polite to the free APIs.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from . import feeds
from .iocs import IOC
from .verdict import Verdict, synthesize


def plan_for(ioc: IOC) -> list:
    """Ordered list of lookup callables for this IOC type."""
    if ioc.type == "ip":
        return [
            lambda: feeds.threatfox_search(ioc.value),
            lambda: feeds.urlhaus_host(ioc.value),
        ]
    if ioc.type == "domain":
        return [
            lambda: feeds.threatfox_search(ioc.value),
            lambda: feeds.urlhaus_host(ioc.value),
        ]
    if ioc.type == "url":
        return [
            lambda: feeds.urlhaus_url(ioc.value),
            lambda: feeds.threatfox_search(ioc.value),
        ]
    if ioc.type in ("md5", "sha256"):
        return [
            lambda: feeds.mb_hash(ioc.value),
            lambda: feeds.threatfox_search(ioc.value),
            lambda: feeds.urlhaus_payload(ioc.value, ioc.type),
        ]
    if ioc.type == "sha1":
        return [
            lambda: feeds.mb_hash(ioc.value),
            lambda: feeds.threatfox_search(ioc.value),
        ]
    return []


@dataclass
class Enrichment:
    ioc: IOC
    results: list       # list[feeds.FeedResult]
    verdict: Verdict


def enrich_one(ioc: IOC) -> Enrichment:
    results = [step() for step in plan_for(ioc)]
    return Enrichment(ioc=ioc, results=results, verdict=synthesize(ioc, results))


def enrich_many(iocs: list, max_workers: int = 4) -> list:
    """Enrich a batch. Order of the input list is preserved in the output."""
    if len(iocs) <= 1:
        return [enrich_one(i) for i in iocs]
    workers = max(1, min(max_workers, len(iocs)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(enrich_one, iocs))
