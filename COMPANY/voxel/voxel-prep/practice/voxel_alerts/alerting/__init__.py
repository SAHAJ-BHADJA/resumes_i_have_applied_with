"""Voxel site alerting service (practice codebase)."""

from .channels import Channel, EmailChannel, SmsChannel
from .dedup import Deduplicator
from .dispatcher import EventDispatcher
from .models import DeliveryRecord, Detection, Severity, Subscription
from .pipeline import AlertPipeline
from .rate_limiter import SlidingWindowRateLimiter

__all__ = [
    "AlertPipeline",
    "Channel",
    "Deduplicator",
    "DeliveryRecord",
    "Detection",
    "EmailChannel",
    "EventDispatcher",
    "Severity",
    "SlidingWindowRateLimiter",
    "SmsChannel",
    "Subscription",
]
