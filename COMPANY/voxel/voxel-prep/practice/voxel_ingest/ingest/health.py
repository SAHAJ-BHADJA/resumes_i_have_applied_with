"""Track camera liveness. A camera that goes quiet is the failure mode that
matters most for a safety product — the site thinks an aisle is watched when
it isn't.

This module is intentionally minimal right now. It only knows ONLINE vs
OFFLINE. One of the practice tasks extends it.
"""

from typing import Dict, List

from .models import CameraState


class HealthMonitor:
    """Watches per-camera frame arrivals and reports liveness."""

    def __init__(self, offline_after_seconds: float = 10.0):
        self.offline_after_seconds = offline_after_seconds
        self._last_frame_at: Dict[str, float] = {}

    def record_frame(self, camera_id: str, timestamp: float) -> None:
        """Note that a frame arrived from this camera."""
        self._last_frame_at[camera_id] = timestamp

    def state_of(self, camera_id: str, now: float) -> CameraState:
        """Current liveness of one camera."""
        last = self._last_frame_at.get(camera_id)
        if last is None:
            return CameraState.OFFLINE
        if now - last > self.offline_after_seconds:
            return CameraState.OFFLINE
        return CameraState.ONLINE

    def offline_cameras(self, now: float) -> List[str]:
        """Every camera we currently consider offline."""
        return [
            camera_id
            for camera_id in self._last_frame_at
            if self.state_of(camera_id, now) == CameraState.OFFLINE
        ]
