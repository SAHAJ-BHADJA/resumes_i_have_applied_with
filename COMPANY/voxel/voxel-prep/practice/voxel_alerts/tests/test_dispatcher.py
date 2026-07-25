import pytest

from alerting import EventDispatcher

from .conftest import make_detection


def test_handler_receives_the_detection():
    dispatcher = EventDispatcher()
    seen = []
    dispatcher.register("spill", seen.append)

    detection = make_detection(event_type="spill")
    dispatcher.dispatch(detection)

    assert seen == [detection]


def test_handlers_for_other_types_are_not_called():
    dispatcher = EventDispatcher()
    seen = []
    dispatcher.register("spill", seen.append)

    dispatcher.dispatch(make_detection(event_type="ppe_violation"))

    assert seen == []


def test_dispatch_with_no_handlers_is_a_noop():
    dispatcher = EventDispatcher()
    assert dispatcher.dispatch(make_detection(event_type="spill")) == []


def test_multiple_handlers_all_run():
    dispatcher = EventDispatcher()
    calls = []
    dispatcher.register("spill", lambda d: calls.append("first"))
    dispatcher.register("spill", lambda d: calls.append("second"))

    dispatcher.dispatch(make_detection(event_type="spill"))

    assert calls == ["first", "second"]


# ---------------------------------------------------------------- T3 lives here

def test_one_broken_handler_does_not_stop_the_others():
    """If the email provider is down, SMS must still go out.

    A handler that raises should be isolated: the remaining handlers still run,
    and dispatch() does not propagate the exception to the caller.
    """
    dispatcher = EventDispatcher()
    calls = []

    def healthy_before(detection):
        calls.append("before")

    def broken(detection):
        raise RuntimeError("email provider timed out")

    def healthy_after(detection):
        calls.append("after")

    dispatcher.register("spill", healthy_before)
    dispatcher.register("spill", broken)
    dispatcher.register("spill", healthy_after)

    dispatcher.dispatch(make_detection(event_type="spill"))

    assert calls == ["before", "after"]
