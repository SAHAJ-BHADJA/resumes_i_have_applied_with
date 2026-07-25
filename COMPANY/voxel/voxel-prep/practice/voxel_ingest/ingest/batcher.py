"""Batch frames before handing them to the (expensive) detector.

Running the detector once per frame is wasteful — GPU inference likes batches.
We accumulate frames and flush when the batch is full or enough time has passed.
"""

from typing import Callable, List

from .models import Frame


class FrameBatcher:
    """Accumulates frames and flushes them in batches to a sink."""

    def __init__(
        self,
        sink: Callable[[List[Frame]], None],
        max_batch_size: int = 8,
        max_wait_seconds: float = 0.5,
        buffer: List[Frame] = [],
    ):
        self.sink = sink
        self.max_batch_size = max_batch_size
        self.max_wait_seconds = max_wait_seconds
        self.buffer = buffer
        self._oldest_timestamp: float | None = None

    def add(self, frame: Frame) -> None:
        """Add a frame; flush automatically if the batch is full or stale."""
        if self._oldest_timestamp is None:
            self._oldest_timestamp = frame.timestamp

        self.buffer.append(frame)

        age = frame.timestamp - self._oldest_timestamp
        if len(self.buffer) > self.max_batch_size or age > self.max_wait_seconds:
            self.flush()

    def flush(self) -> None:
        """Send whatever's buffered to the sink and reset."""
        if not self.buffer:
            return
        self.sink(self.buffer)
        self.buffer = []
        self._oldest_timestamp = None
