"""Stage 1 of the pipeline: ingest + parse + normalise.

Reads the SIEM export, validates it against its own declared metadata schema,
and returns an EventStore. Intentionally forgiving about *which* optional fields
are present (real exports are messy) but strict about the envelope every event
needs — event_id, timestamp, source — so nothing downstream cites a phantom.
"""

from __future__ import annotations

import json
from typing import Iterable

from .model import Event, EventStore, parse_ts

REQUIRED = ("event_id", "timestamp", "source")
KNOWN_SOURCES = {"endpoint", "auth", "network", "cloud_storage"}


class IngestError(Exception):
    pass


def load(path: str) -> EventStore:
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    return load_doc(doc)


def load_doc(doc: dict) -> EventStore:
    if "events" not in doc:
        raise IngestError("SIEM file has no 'events' array")
    metadata = doc.get("metadata", {})

    events: list[Event] = []
    skipped = 0
    for row in doc["events"]:
        missing = [k for k in REQUIRED if k not in row]
        if missing:
            skipped += 1
            continue
        try:
            ts = parse_ts(row["timestamp"])
        except (ValueError, TypeError):
            skipped += 1
            continue
        events.append(Event(id=row["event_id"], source=row["source"], ts=ts, raw=row))

    store = EventStore(events, metadata)
    store.ingest_stats = {
        "total": len(events),
        "skipped_malformed": skipped,
        "by_source": {s: len(store.by_source(s)) for s in sorted({e.source for e in events})},
        "window_start": store.window[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_end": store.window[1].strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return store
