"""Domain objects for the edge frame-ingestion service.

This service runs on the edge appliance at a customer site. It pulls frames off
cameras, batches them, runs them past a detector, and tracks objects across
frames so a forklift seen in frame 100 and frame 101 is understood to be the
*same* forklift, not two.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class CameraState(Enum):
    ONLINE = "online"
    DEGRADED = "degraded"      # still sending, but dropping frames
    OFFLINE = "offline"


@dataclass(frozen=True)
class BBox:
    """Axis-aligned bounding box in pixel coords, (x1, y1) top-left corner."""

    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def area(self) -> float:
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


@dataclass(frozen=True)
class Frame:
    """One decoded frame from one camera."""

    camera_id: str
    frame_number: int
    timestamp: float
    width: int
    height: int


@dataclass
class Detection:
    """One detected object in one frame, before tracking assigns it an identity."""

    frame: Frame
    label: str                 # "person" | "forklift" | "spill" | ...
    confidence: float
    box: BBox
    track_id: Optional[int] = None    # filled in by the tracker


@dataclass
class Track:
    """An object followed across frames. One real-world forklift = one Track."""

    track_id: int
    label: str
    last_box: BBox
    last_seen_frame: int
    hit_count: int = 1         # how many frames we've matched it in
    history: List[BBox] = field(default_factory=list)
