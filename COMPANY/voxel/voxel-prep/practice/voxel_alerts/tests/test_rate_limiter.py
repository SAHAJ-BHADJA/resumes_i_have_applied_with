from alerting import SlidingWindowRateLimiter


def test_first_event_is_allowed():
    limiter = SlidingWindowRateLimiter(max_events=3, window_seconds=60.0)
    assert limiter.allow("ana", now=1000.0) is True


def test_keys_are_independent():
    limiter = SlidingWindowRateLimiter(max_events=1, window_seconds=60.0)
    assert limiter.allow("ana", now=1000.0) is True
    assert limiter.allow("ben", now=1000.0) is True


def test_window_slides_forward():
    limiter = SlidingWindowRateLimiter(max_events=1, window_seconds=60.0)
    assert limiter.allow("ana", now=1000.0) is True
    assert limiter.allow("ana", now=1030.0) is False
    assert limiter.allow("ana", now=1061.0) is True


# ---------------------------------------------------------------- T2 lives here

def test_allows_exactly_max_events_then_rejects():
    """max_events=3 means three get through and the fourth does not."""
    limiter = SlidingWindowRateLimiter(max_events=3, window_seconds=60.0)

    assert limiter.allow("ana", now=1000.0) is True
    assert limiter.allow("ana", now=1001.0) is True
    assert limiter.allow("ana", now=1002.0) is True
    assert limiter.allow("ana", now=1003.0) is False


def test_cap_of_one_allows_exactly_one():
    limiter = SlidingWindowRateLimiter(max_events=1, window_seconds=60.0)
    assert limiter.allow("ana", now=1000.0) is True
    assert limiter.allow("ana", now=1001.0) is False
