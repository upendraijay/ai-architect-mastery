# Factory Pattern

> **Factory solves the problem of having duplicated or scattered object-creation logic by moving object creation to one place.**

---

## 1. Start with an interface

```python
from abc import ABC, abstractmethod


class Notification(ABC):

    @abstractmethod
    def send(self, message: str):
        pass
```

### Implementations

```python
class EmailNotification(Notification):

    def send(self, message: str):
        print(f"Sending EMAIL: {message}")


class SMSNotification(Notification):

    def send(self, message: str):
        print(f"Sending SMS: {message}")
```

---

## 2. Suppose we have `PaymentService`

After payment succeeds, it sends a payment-success notification.

```python
class PaymentService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def make_payment(self):
        # payment logic
        self.notification.send("Payment successful")
```
---

## 3. Now suppose we have `OrderService`

After order confirmation, it sends a notification.

```python
class OrderService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def place_order(self):
        # order logic
        self.notification.send("Order placed successfully")
```

---

## 4. But now notice the creation problem

The notification provider comes from configuration:

```python
provider = config["notification_provider"]
```

Both `OrderService` and `PaymentService` need to decide which concrete notification object to create.

### Order module

```python
if provider == "email":
    notification = EmailNotification()

elif provider == "sms":
    notification = SMSNotification()

elif provider == "push":
    notification = PushNotification()

order_service = OrderService(notification)
```

### Payment module

```python
if provider == "email":
    notification = EmailNotification()

elif provider == "sms":
    notification = SMSNotification()

elif provider == "push":
    notification = PushNotification()

payment_service = PaymentService(notification)
```

### Now we have the problem

Both caller modules contain the **same object-creation logic**.

The business services are clean, but the **creation logic is duplicated across the caller modules**.

This is the problem Factory solves.

---

## 5. Now the Factory becomes useful

We move creation into one place:

```python
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
```

Now both modules become simple.

### Order module

```python
notification = NotificationFactory.create(provider)

order_service = OrderService(notification)
order_service.place_order()
```

### Payment module

```python
notification = NotificationFactory.create(provider)

payment_service = PaymentService(notification)
payment_service.make_payment()
```

---

## The complete story

This is the important part to remember for your interview:

```text
                    Notification
                    (Interface)
                         ↑
          ┌──────────────┼──────────────┐
          │              │              │
        Email           SMS            Push
      Notification   Notification   Notification
          │              │              │
          └──────────────┼──────────────┘
                         │
                  NotificationFactory
                         │
              creates the right object
                         │
              ┌──────────┴──────────┐
              │                     │
        OrderService          PaymentService
          (Caller)                (Caller)
```
