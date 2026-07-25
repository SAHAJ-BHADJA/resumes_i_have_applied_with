"""Ingest + entity-resolution tests."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from siem_investigator import ingest
from siem_investigator.ingest import load_doc, IngestError

LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "siem_logs.json")


def test_loads_all_sources():
    store = ingest.load(LOGS)
    assert len(store) >= 250, "expected ~300 events"
    by_source = store.ingest_stats["by_source"]
    for src in ("endpoint", "auth", "network", "cloud_storage"):
        assert by_source.get(src, 0) > 0, "source {} missing".format(src)


def test_entity_resolution():
    store = ingest.load(LOGS)
    # host<->ip resolution must work both ways for a known asset
    assert store.host_to_ip.get("WKS-2471") == "10.20.14.71"
    assert store.resolve_host("10.20.14.71") == "WKS-2471"
    assert store.resolve_host("10.20.8.12") == "SRV-FILES01"


def test_events_sorted_and_indexed():
    store = ingest.load(LOGS)
    ts = [e.ts for e in store.events]
    assert ts == sorted(ts), "events must be chronologically sorted"
    first = store.events[0]
    assert store.get(first.id) is first, "id index must resolve"


def test_malformed_rows_skipped_not_fatal():
    doc = {"metadata": {}, "events": [
        {"event_id": "X-1", "timestamp": "2026-07-19T00:00:00Z", "source": "endpoint"},
        {"event_id": "X-2", "source": "endpoint"},              # no timestamp
        {"timestamp": "2026-07-19T00:00:00Z", "source": "auth"},  # no id
        {"event_id": "X-3", "timestamp": "not-a-date", "source": "auth"},  # bad ts
    ]}
    store = load_doc(doc)
    assert len(store) == 1
    assert store.ingest_stats["skipped_malformed"] == 3


def test_missing_events_key_raises():
    try:
        load_doc({"metadata": {}})
        assert False, "should have raised"
    except IngestError:
        pass


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok:", name)
    print("all ingest tests passed")
