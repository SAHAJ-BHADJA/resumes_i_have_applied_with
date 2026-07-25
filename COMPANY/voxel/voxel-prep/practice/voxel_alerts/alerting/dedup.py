"""Suppress repeat detections of the same ongoing hazard.

A spill on camera 3 produces a detection on every frame. We only want to notify
about it once per window, not thirty times a second — but we DO want a fresh
reminder each window while the hazard is still there.
"""

from typing import Dict, Optional, Tuple

from .models import Detection


class Deduplicator:
    """Collapses repeat detections of the same hazard into one alert per window."""

    def __init__(self, window_seconds: float = 60.0):
        self.window_seconds = window_seconds
        self._last_alerted: Dict[Tuple[str, str, str], float] = {}

    @staticmethod
    def _key(detection: Detection) -> Tuple[str, str, str]:
        """Two detections are 'the same hazard' if site, camera, and type match."""
        return (detection.site_id, detection.camera_id, detection.event_type)

    def is_duplicate(self, detection: Detection) -> bool:
        """True if we already alerted on this hazard recently."""
        key = self._key(detection)
        last: Optional[float] = self._last_alerted.get(key)

        self._last_alerted[key] = detection.timestamp

        if last is None:
            return False
        return detection.timestamp - last < self.window_seconds
