"""Fan detections out to any number of registered handlers.

Handlers are things like: the alert pipeline, the metrics recorder, the audit
logger, the ML feedback collector. They are independent of each other.
"""

from collections import defaultdict
from typing import Any, Callable, Dict, List

from .models import Detection

Handler = Callable[[Detection], Any]


class EventDispatcher:
    """A simple pub/sub registry keyed by event type."""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Handler]] = defaultdict(list)

    def register(self, event_type: str, handler: Handler) -> None:
        """Subscribe `handler` to detections of `event_type`."""
        self._handlers[event_type].append(handler)

    def dispatch(self, detection: Detection) -> List[Any]:
        """Run every handler registered for this detection's type."""
        results: List[Any] = []
        for handler in self._handlers[detection.event_type]:
            results.append(handler(detection))
        return results
