"""Delivery channels. Each one knows how to get a message to a person.

The concrete classes here are fakes that record what they were asked to send —
in production these wrap SES, Twilio, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class Channel(ABC):
    """Anything that can deliver a rendered alert to an address."""

    @abstractmethod
    def send(self, address: str, subject: str, body: str) -> bool:
        """Deliver the message. Return True on success."""
        raise NotImplementedError


class EmailChannel(Channel):
    def __init__(self) -> None:
        self.sent: List[Tuple[str, str, str]] = []

    def send(self, address: str, subject: str, body: str) -> bool:
        self.sent.append((address, subject, body))
        return True


class SmsChannel(Channel):
    MAX_LENGTH = 160

    def __init__(self) -> None:
        self.sent: List[Tuple[str, str]] = []

    def send(self, address: str, subject: str, body: str) -> bool:
        text = f"{subject}: {body}"[: self.MAX_LENGTH]
        self.sent.append((address, text))
        return True
