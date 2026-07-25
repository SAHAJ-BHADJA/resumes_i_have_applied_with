"""Core data structures: the normalised Event, the EventStore (indices + entity
resolution), and the Finding / Incident intermediate representation.

Everything downstream (detectors, correlation, synthesis, reporting) reads these
types only. The IR is deliberately plain-old-data so it serialises cleanly to
`investigation.json` — the machine-readable audit trail an analyst can diff.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Optional


# --------------------------------------------------------------------------- #
# Confidence + severity vocabularies (small, fixed, explainable)
# --------------------------------------------------------------------------- #
CONFIRMED = "CONFIRMED"    # corroborated across >=2 sources, or a single unambiguous artifact
SUSPECTED = "SUSPECTED"    # single-source signal, consistent with the attack but not corroborated
UNCERTAIN = "UNCERTAIN"    # indirect/absent evidence; flagged so it is never over-stated

SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW = "critical", "high", "medium", "low"


def parse_ts(value: str) -> datetime:
    """Parse an ISO-8601 'Z' timestamp into an aware UTC datetime."""
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


# --------------------------------------------------------------------------- #
# Event
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Event:
    """A single normalised log event. `raw` keeps every original field so the
    report can drill down to the untouched source record for verification."""

    id: str
    source: str
    ts: datetime
    raw: dict

    # convenience accessors (None when a source doesn't have the field) --------
    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)

    @property
    def host(self) -> Optional[str]:
        return self.raw.get("host")

    @property
    def user(self) -> Optional[str]:
        return self.raw.get("user") or self.raw.get("principal")

    @property
    def ts_str(self) -> str:
        return self.ts.strftime("%Y-%m-%dT%H:%M:%SZ")

    def citation(self) -> str:
        loc = self.host or self.raw.get("principal") or self.raw.get("src_host") or ""
        return "{} ({}, {}{})".format(self.id, self.source, (loc + ", ") if loc else "", self.ts_str)


# --------------------------------------------------------------------------- #
# Finding — the atomic unit of the investigation. Every Finding is produced by a
# deterministic detector and carries the exact events that justify it.
# --------------------------------------------------------------------------- #
@dataclass
class Finding:
    id: str
    title: str
    phase: str                       # kill-chain phase (== ATT&CK tactic name)
    technique_ids: list[str]         # ATT&CK technique IDs, e.g. ["T1059.001"]
    severity: str
    confidence: str                  # CONFIRMED / SUSPECTED / UNCERTAIN
    rationale: str                   # plain-English "why this fired"
    evidence: list[str]              # event IDs — the traceability backbone
    hosts: list[str] = field(default_factory=list)
    accounts: list[str] = field(default_factory=list)
    ts: Optional[datetime] = None    # representative time (earliest evidence)
    caveats: str = ""                # honest limits on this specific finding
    data: dict = field(default_factory=dict)   # structured extras (e.g. src/dst host) for graphs

    def to_dict(self, techniques: dict | None = None) -> dict:
        d = {
            "id": self.id, "title": self.title, "phase": self.phase,
            "technique_ids": self.technique_ids, "severity": self.severity,
            "confidence": self.confidence, "rationale": self.rationale,
            "hosts": self.hosts, "accounts": self.accounts,
            "timestamp": self.ts.strftime("%Y-%m-%dT%H:%M:%SZ") if self.ts else None,
            "evidence": self.evidence, "caveats": self.caveats,
        }
        if techniques is not None:
            d["techniques"] = [
                {"id": t, **{k: v for k, v in techniques.get(t, {}).items() if k in ("name", "tactic", "url")}}
                for t in self.technique_ids
            ]
        return d


# --------------------------------------------------------------------------- #
# EventStore — indices + host<->ip<->account entity resolution
# --------------------------------------------------------------------------- #
class EventStore:
    def __init__(self, events: list[Event], metadata: dict):
        self.events = sorted(events, key=lambda e: e.ts)
        self.metadata = metadata
        self._by_id = {e.id: e for e in self.events}

        # entity resolution: build a host<->ip map from the CMDB hint plus any
        # (src_host, src_ip) pairs actually observed in the logs.
        self.host_to_ip: dict[str, str] = {}
        self.ip_to_host: dict[str, str] = {}
        hint = (metadata.get("asset_inventory_hint") or {}).get("hosts") or {}
        for host, ip in hint.items():
            self._link(host, ip)
        for e in self.events:
            if e.raw.get("src_host") and e.raw.get("src_ip"):
                self._link(e.raw["src_host"], e.raw["src_ip"])
            if e.host and e.source == "auth" and e.raw.get("src_ip"):
                pass  # host here is the *target*, not the src — don't link

    def _link(self, host: str, ip: str) -> None:
        if not host or not ip or host == "vpn-client":
            return
        self.host_to_ip.setdefault(host, ip)
        self.ip_to_host.setdefault(ip, host)

    # lookups ----------------------------------------------------------------
    def get(self, event_id: str) -> Optional[Event]:
        return self._by_id.get(event_id)

    def resolve_host(self, ip: Optional[str]) -> Optional[str]:
        return self.ip_to_host.get(ip) if ip else None

    def by_source(self, source: str) -> list[Event]:
        return [e for e in self.events if e.source == source]

    def where(self, predicate) -> list[Event]:
        return [e for e in self.events if predicate(e)]

    @property
    def window(self) -> tuple[datetime, datetime]:
        if not self.events:
            now = datetime.now(timezone.utc)
            return now, now
        return self.events[0].ts, self.events[-1].ts

    def __len__(self) -> int:
        return len(self.events)


# --------------------------------------------------------------------------- #
# Incident — the top-level IR the reporter and synthesiser consume.
# --------------------------------------------------------------------------- #
@dataclass
class Incident:
    findings: list[Finding]
    timeline: list[Finding]              # findings ordered for narrative (phase, then time)
    hosts: dict                          # blast-radius host records
    accounts: dict                       # blast-radius account records
    cloud: dict                          # affected cloud resources
    gaps: list[dict]                     # coverage gaps / uncertainty
    techniques: dict                     # id -> ATT&CK metadata (enrichment)
    store: EventStore
    stats: dict = field(default_factory=dict)
    attack_path: list[dict] = field(default_factory=list)         # directional host hops
    attack_by_tactic: list[dict] = field(default_factory=list)    # ATT&CK grouped by tactic
    benign_review: list[dict] = field(default_factory=list)       # near-misses ruled benign

    def to_dict(self) -> dict:
        return {
            "summary_stats": self.stats,
            "findings": [f.to_dict(self.techniques) for f in self.timeline],
            "attack_techniques": sorted(
                {t for f in self.findings for t in f.technique_ids},
                key=lambda t: (t[:5], t)
            ),
            "attack_by_tactic": self.attack_by_tactic,
            "attack_path": self.attack_path,
            "blast_radius": {"hosts": self.hosts, "accounts": self.accounts, "cloud": self.cloud},
            "coverage_gaps": self.gaps,
            "reviewed_benign": self.benign_review,
            "technique_catalogue": {
                t: self.techniques.get(t, {}) for t in
                sorted({t for f in self.findings for t in f.technique_ids})
            },
        }

    def dumps(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
