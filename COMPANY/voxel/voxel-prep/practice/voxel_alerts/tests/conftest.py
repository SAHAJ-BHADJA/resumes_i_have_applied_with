import pytest

from alerting import (
    AlertPipeline,
    Deduplicator,
    Detection,
    EmailChannel,
    Severity,
    SlidingWindowRateLimiter,
    SmsChannel,
    Subscription,
)


def make_detection(
    detection_id="d1",
    site_id="site-a",
    camera_id="cam-1",
    event_type="spill",
    severity=Severity.WARNING,
    timestamp=1000.0,
    **metadata,
):
    return Detection(
        detection_id=detection_id,
        site_id=site_id,
        camera_id=camera_id,
        event_type=event_type,
        severity=severity,
        timestamp=timestamp,
        metadata=metadata,
    )


@pytest.fixture
def detection_factory():
    return make_detection


@pytest.fixture
def email():
    return EmailChannel()


@pytest.fixture
def sms():
    return SmsChannel()


@pytest.fixture
def subscriptions():
    return [
        Subscription(
            user_id="ana",
            site_id="site-a",
            event_types={"spill", "ppe_violation", "blocked_exit"},
            min_severity=Severity.INFO,
            channel="email",
            address="ana@example.com",
        ),
        Subscription(
            user_id="ben",
            site_id="site-a",
            event_types={"forklift_speeding", "blocked_exit"},
            min_severity=Severity.CRITICAL,
            channel="sms",
            address="+15550001111",
        ),
        Subscription(
            user_id="cleo",
            site_id="site-b",
            event_types={"spill"},
            min_severity=Severity.INFO,
            channel="email",
            address="cleo@example.com",
        ),
    ]


@pytest.fixture
def pipeline(subscriptions, email, sms):
    return AlertPipeline(
        subscriptions=subscriptions,
        channels={"email": email, "sms": sms},
        deduplicator=Deduplicator(window_seconds=60.0),
        rate_limiter=SlidingWindowRateLimiter(max_events=100, window_seconds=3600.0),
    )
