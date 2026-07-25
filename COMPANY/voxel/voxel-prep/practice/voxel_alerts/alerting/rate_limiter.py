"""Per-recipient rate limiting.

Even after dedup, a busy site can generate a lot of distinct alerts. We cap how
many any one person receives in a rolling window so the notifications stay
useful instead of becoming noise people learn to ignore.
"""

from collections import defaultdict, deque
from typing import Deque, Dict


class SlidingWindowRateLimiter:
    """Allow at most `max_events` per key in any `window_seconds` window."""

    def __init__(self, max_events: int, window_seconds: float):
        self.max_events = max_events
        self.window_seconds = window_seconds
        self._timestamps: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str, now: float) -> bool:
        """Record and permit an event for `key`, or reject it if over the cap."""
        window = self._timestamps[key]

        while window and window[0] <= now - self.window_seconds:
            window.popleft()

        if len(window) <= self.max_events:
            window.append(now)
            return True
        return False
