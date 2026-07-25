"""Voxel edge frame-ingestion service (practice codebase #2)."""

from .batcher import FrameBatcher
from .geometry import intersection_area, iou
from .health import HealthMonitor
from .models import BBox, CameraState, Detection, Frame, Track
from .tracker import Tracker

__all__ = [
    "BBox",
    "CameraState",
    "Detection",
    "Frame",
    "FrameBatcher",
    "HealthMonitor",
    "Tracker",
    "Track",
    "intersection_area",
    "iou",
]
