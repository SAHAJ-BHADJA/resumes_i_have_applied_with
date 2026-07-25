"""Bounding-box geometry. The tracker leans on this heavily."""

from .models import BBox


def intersection_area(a: BBox, b: BBox) -> float:
    """Area of overlap between two boxes. Zero if they don't overlap."""
    left = max(a.x1, b.x1)
    right = min(a.x2, b.x2)
    top = max(a.y1, b.y1)
    bottom = min(a.y2, b.y2)

    width = right - left
    height = bottom - top
    return width * height


def iou(a: BBox, b: BBox) -> float:
    """Intersection over union — 0.0 (no overlap) to 1.0 (identical)."""
    inter = intersection_area(a, b)
    union = a.area + b.area - inter
    if union <= 0:
        return 0.0
    return inter / union
