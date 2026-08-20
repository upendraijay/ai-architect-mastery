"""Factory Pattern — notification dispatch.

The client asks `NotificationFactory` for a provider by name and receives a
`Notification`. It never imports or constructs a concrete notification class.

Run: python notification_factory.py
"""

from abc import ABC, abstractmethod


# --- abstraction ----------------------------------------------------------


class Notification(ABC):
    """The contract every notification channel implements."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Deliver the message through this channel."""


# --- implementations ------------------------------------------------------


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending EMAIL: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending PUSH: {message}")


# --- factory --------------------------------------------------------------


class NotificationFactory:

    @staticmethod
    def create(provider: str) -> Notification:

        if provider == "email":
            return EmailNotification()

        elif provider == "sms":
            return SMSNotification()

        elif provider == "push":
            return PushNotification()

        raise ValueError(f"Unknown provider: {provider}")


# --- clients --------------------------------------------------------------
# Both depend on the Notification abstraction, never on a concrete channel.


class OrderService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def place_order(self) -> None:
        # order logic
        self.notification.send("Order placed successfully")


class PaymentService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def make_payment(self) -> None:
        # payment logic
        self.notification.send("Payment successful")


# --- demo -----------------------------------------------------------------


if __name__ == "__main__":

    config = {"notification_provider": "email"}
    provider = config["notification_provider"]

    notification = NotificationFactory.create(provider)

    OrderService(notification).place_order()
    PaymentService(notification).make_payment()