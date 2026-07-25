from alerting import Severity

from .conftest import make_detection


def test_matching_subscriber_is_notified(pipeline, email):
    detection = make_detection(
        site_id="site-a", event_type="spill", severity=Severity.WARNING, area="aisle 4"
    )
    notified = pipeline.process(detection)

    assert notified == ["ana"]
    assert len(email.sent) == 1
    address, subject, body = email.sent[0]
    assert address == "ana@example.com"
    assert "aisle 4" in body


def test_other_sites_are_not_notified(pipeline, email):
    pipeline.process(make_detection(site_id="site-b", event_type="spill"))
    addresses = [address for address, _, _ in email.sent]
    assert "ana@example.com" not in addresses


def test_severity_floor_is_respected(pipeline, sms):
    """Ben only wants CRITICAL. A WARNING blocked_exit should not reach him."""
    pipeline.process(
        make_detection(event_type="blocked_exit", severity=Severity.WARNING)
    )
    assert sms.sent == []


def test_critical_reaches_the_sms_subscriber(pipeline, sms):
    notified = pipeline.process(
        make_detection(event_type="blocked_exit", severity=Severity.CRITICAL, exit_id="E2")
    )
    assert "ben" in notified
    assert len(sms.sent) == 1


def test_unsubscribed_event_type_is_skipped(pipeline, email):
    pipeline.process(
        make_detection(event_type="forklift_speeding", severity=Severity.CRITICAL)
    )
    assert email.sent == []


def test_duplicate_detection_notifies_nobody(pipeline, email):
    pipeline.process(make_detection(detection_id="d1", timestamp=1000.0))
    notified = pipeline.process(make_detection(detection_id="d2", timestamp=1005.0))
    assert notified == []
    assert len(email.sent) == 1


def test_unknown_event_type_renders_a_fallback_body(pipeline):
    body = pipeline._render_body(make_detection(event_type="mystery_event"))
    assert "mystery_event" in body


def test_sms_body_is_truncated(pipeline, sms):
    pipeline.process(
        make_detection(
            event_type="blocked_exit",
            severity=Severity.CRITICAL,
            exit_id="E" * 400,
        )
    )
    _, text = sms.sent[0]
    assert len(text) <= 160


def test_delivery_log_records_each_send(pipeline):
    pipeline.process(make_detection(event_type="spill", severity=Severity.WARNING))
    assert len(pipeline.delivery_log) == 1
    assert pipeline.delivery_log[0].user_id == "ana"
    assert pipeline.delivery_log[0].channel == "email"
