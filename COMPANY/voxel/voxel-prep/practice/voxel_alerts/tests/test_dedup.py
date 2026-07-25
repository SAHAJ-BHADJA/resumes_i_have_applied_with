from alerting import Deduplicator, Severity

from .conftest import make_detection


def test_first_detection_is_never_a_duplicate():
    dedup = Deduplicator(window_seconds=60.0)
    assert dedup.is_duplicate(make_detection(timestamp=1000.0)) is False


def test_immediate_repeat_is_a_duplicate():
    dedup = Deduplicator(window_seconds=60.0)
    dedup.is_duplicate(make_detection(detection_id="d1", timestamp=1000.0))
    assert dedup.is_duplicate(make_detection(detection_id="d2", timestamp=1001.0)) is True


def test_different_camera_is_not_a_duplicate():
    dedup = Deduplicator(window_seconds=60.0)
    dedup.is_duplicate(make_detection(camera_id="cam-1", timestamp=1000.0))
    assert dedup.is_duplicate(make_detection(camera_id="cam-2", timestamp=1001.0)) is False


def test_different_event_type_is_not_a_duplicate():
    dedup = Deduplicator(window_seconds=60.0)
    dedup.is_duplicate(make_detection(event_type="spill", timestamp=1000.0))
    assert (
        dedup.is_duplicate(make_detection(event_type="ppe_violation", timestamp=1001.0))
        is False
    )


def test_repeat_after_the_window_is_not_a_duplicate():
    dedup = Deduplicator(window_seconds=60.0)
    dedup.is_duplicate(make_detection(timestamp=1000.0))
    assert dedup.is_duplicate(make_detection(timestamp=1061.0)) is False


# ---------------------------------------------------------------- T1 lives here

def test_ongoing_hazard_realerts_every_window():
    """A spill that stays on the floor for 5 minutes should produce a reminder
    every 60s, not one alert and then silence forever.

    The perception service emits a detection every 30 seconds while the spill
    is visible. With a 60s dedup window we expect an alert at t=0, t=60, t=120,
    t=180, t=240 -- five alerts across the five minutes.
    """
    dedup = Deduplicator(window_seconds=60.0)

    alerted_at = []
    for tick in range(0, 300, 30):  # a detection every 30s for 5 minutes
        timestamp = 1000.0 + tick
        if not dedup.is_duplicate(make_detection(timestamp=timestamp)):
            alerted_at.append(tick)

    assert alerted_at == [0, 60, 120, 180, 240]
