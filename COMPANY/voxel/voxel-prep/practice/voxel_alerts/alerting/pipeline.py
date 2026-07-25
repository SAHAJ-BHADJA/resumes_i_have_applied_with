"""The alert pipeline. This is the entry point — start reading here.

    Detection
        -> dedup       (is this the same hazard we just alerted on?)
        -> match subs  (who cares about this site / type / severity?)
        -> rate limit  (has this person had enough for now?)
        -> render      (turn the detection into human words)
        -> send        (hand off to the channel)
        -> record      (audit trail)
"""

import time
from typing import Dict, List

from .channels import Channel
from .dedup import Deduplicator
from .models import DeliveryRecord, Detection, Severity, Subscription
from .rate_limiter import SlidingWindowRateLimiter


class AlertPipeline:
    def __init__(
        self,
        subscriptions: List[Subscription],
        channels: Dict[str, Channel],
        deduplicator: Deduplicator,
        rate_limiter: SlidingWindowRateLimiter,
    ):
        self.subscriptions = subscriptions
        self.channels = channels
        self.deduplicator = deduplicator
        self.rate_limiter = rate_limiter
        self.delivery_log: List[DeliveryRecord] = []

    # ------------------------------------------------------------------ render

    def _render_subject(self, detection: Detection) -> str:
        return f"[{detection.severity.name}] {detection.site_id} / {detection.camera_id}"

    def _render_body(self, detection: Detection) -> str:
        if detection.event_type == "ppe_violation":
            missing = detection.metadata.get("missing_ppe", "required PPE")
            return f"Worker detected without {missing}."
        elif detection.event_type == "spill":
            area = detection.metadata.get("area", "the floor")
            return f"Possible spill detected on {area}. Cordon and clean."
        elif detection.event_type == "forklift_speeding":
            speed = detection.metadata.get("speed_mph", "?")
            return f"Forklift travelling at {speed} mph, above the site limit."
        elif detection.event_type == "blocked_exit":
            exit_id = detection.metadata.get("exit_id", "an exit")
            return f"Emergency exit {exit_id} appears obstructed."
        else:
            return f"Detection of type '{detection.event_type}' recorded."

    # ------------------------------------------------------------------ match

    def _matches(self, subscription: Subscription, detection: Detection) -> bool:
        """Does this person want this detection?"""
        if subscription.site_id != detection.site_id:
            return False
        if detection.event_type not in subscription.event_types:
            return False
        if detection.severity.value < subscription.min_severity.value:
            return False
        return True

    # ------------------------------------------------------------------ process

    def process(self, detection: Detection) -> List[str]:
        """Handle one detection. Returns the user_ids we actually notified."""
        if self.deduplicator.is_duplicate(detection):
            return []

        subject = self._render_subject(detection)
        body = self._render_body(detection)
        notified: List[str] = []

        for subscription in self.subscriptions:
            if not self._matches(subscription, detection):
                continue

            if not self.rate_limiter.allow(subscription.user_id, detection.timestamp):
                continue

            channel = self.channels[subscription.channel]
            ok = channel.send(subscription.address, subject, body)
            if not ok:
                continue

            self.delivery_log.append(
                DeliveryRecord(
                    detection_id=detection.detection_id,
                    user_id=subscription.user_id,
                    channel=subscription.channel,
                    sent_at=time.time(),
                )
            )
            notified.append(subscription.user_id)

        return notified
