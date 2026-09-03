'''
notification system

3 main channels
- email
- push
- sms

same message can be sent from various channels

no privider implementation needed

also we are tracking delivery status


entities:
User
Notification
NotificationService
NotificationChannel
EmailChannel
SMSChannel
PushChannel


User
+
Notification
+
[EmailChannel, SMSChannel]
    |
Notification Service
    |       |
email    SMS channel
    |       |
provider   provider




Notification Service -> send()
Email and SMS will implement -> send(User, notification)
Email - email provider


Strategy Design pattern

'''

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

@dataclass
class User:
    id: int
    email: str = None
    phone: str = None
    device_token: str = None

@dataclass
class Notification:
    message: str
    status: dict = field(default_factory=dict)

{
    "EMAIL": Status.SENT,
    "PUSH": Status.FAILED
}

class NotificationChannel(ABC):

    @abstractmethod
    def send(self, user: User, notification: Notification):
        pass

class EmailChannel(NotificationChannel):

    def send(self, user, notification):
        print(
            f"Sending email to {user.email}: "
            f"{notification.message}"
        )

class SMSChannel(NotificationChannel):

    def send(self, user, notification):
        print(
            f"Sending SMS to {user.phone}: "
            f"{notification.message}"
        )

class PushChannel(NotificationChannel):

    def send(self, user, notification):
        print(
            f"Sending push to {user.device_token}: "
            f"{notification.message}"
        )

class NotificationService:

    def send(
        self,
        user: User,
        notification: Notification,
        channels: list[NotificationChannel]
    ):

        for channel in channels:

            channel_name = channel.__class__.__name__

            try:
                channel.send(user, notification)

                notification.status[channel_name] = Status.SENT

            except Exception:
                notification.status[channel_name] = Status.FAILED



user = User(
    id=1,
    email="user@example.com",
    phone="1234567890",
    device_token="device123"
)

notification = Notification(
    message="Your order has shipped."
)

channels = [
    EmailChannel(),
    PushChannel()
]

service = NotificationService()

service.send(
    user,
    notification,
    channels
)

print(notification.status)