"""Core domain objects for the site alerting service."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Set


class Severity(Enum):
    """How urgent a detection is. Higher value = more urgent."""

    INFO = 1
    WARNING = 2
    CRITICAL = 3


@dataclass(frozen=True)
class Detection:
    """A single event emitted by the perception service for one camera frame.

    Detections arrive continuously — a camera watching a spill will emit one of
    these on every frame for as long as the spill is visible.
    """

    detection_id: str
    site_id: str
    camera_id: str
    event_type: str  # "ppe_violation" | "spill" | "forklift_speeding" | ...
    severity: Severity
    timestamp: float  # unix seconds
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Subscription:
    """Who wants to hear about what, and where to reach them."""

    user_id: str
    site_id: str
    event_types: Set[str]
    min_severity: Severity
    channel: str  # must be a key in AlertPipeline.channels
    address: str


@dataclass
class DeliveryRecord:
    """Audit trail entry — one per successful send."""

    detection_id: str
    user_id: str
    channel: str
    sent_at: float
