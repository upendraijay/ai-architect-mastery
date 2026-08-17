# Factory Pattern

This is the better story because it first shows **good OCP/abstraction**, and then shows the **separate problem of object creation**.

---

## 1. Start with an interface

We have different ways of sending notifications.

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

## 2. First client module

Suppose we have `OrderService`.

It only depends on the interface:

```python
class OrderService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def place_order(self):
        # order logic
        self.notification.send("Order placed successfully")
```

We can create it like this:

```python
notification = EmailNotification()

order_service = OrderService(notification)
order_service.place_order()
```

This is already good.

`OrderService` doesn't know whether the notification is email or SMS.

It only knows:

```text
I have a Notification.
I can call send().
```

---

## 3. Another module needs notifications

Now suppose we have `PaymentService`.

It also needs to send notifications:

```python
class PaymentService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def make_payment(self):
        # payment logic
        self.notification.send("Payment successful")
```

We now have two modules:

```text
OrderService
      ↓
Notification

PaymentService
      ↓
Notification
```

So far, everything is good.

---

## 4. Tomorrow we add Push Notification

Business asks:

> We also want to support Push Notifications.

We create another implementation:

```python
class PushNotification(Notification):

    def send(self, message: str):
        print(f"Sending PUSH: {message}")
```

Notice something important:

### Do we need to change `OrderService`?

**No.**

```python
class OrderService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def place_order(self):
        self.notification.send("Order placed successfully")
```

### Do we need to change `PaymentService`?

**No.**

```python
class PaymentService:

    def __init__(self, notification: Notification):
        self.notification = notification

    def make_payment(self):
        self.notification.send("Payment successful")
```

This is **OCP + Dependency Injection working correctly**.

We can simply inject the new implementation:

```python
notification = PushNotification()

order_service = OrderService(notification)
payment_service = PaymentService(notification)
```

So far, **we don't need a Factory.**

---

## 5. But now notice the creation problem

Imagine we don't want the caller to directly decide:

```python
EmailNotification()
SMSNotification()
PushNotification()
```

Instead, the notification type comes from configuration:

```python
provider = config["notification_provider"]
```

For example:

```text
notification_provider = "email"
```

Now the caller has to create the correct object.

We might write:

```python
if provider == "email":
    notification = EmailNotification()

elif provider == "sms":
    notification = SMSNotification()

elif provider == "push":
    notification = PushNotification()
```

And then:

```python
order_service = OrderService(notification)
```

But `PaymentService` needs the same thing.

So we end up with:

```python
# Order module

if provider == "email":
    notification = EmailNotification()
elif provider == "sms":
    notification = SMSNotification()
elif provider == "push":
    notification = PushNotification()

order_service = OrderService(notification)
```

And:

```python
# Payment module

if provider == "email":
    notification = EmailNotification()
elif provider == "sms":
    notification = SMSNotification()
elif provider == "push":
    notification = PushNotification()

payment_service = PaymentService(notification)
```

### Now we have a problem.

Both caller modules know:

* EmailNotification
* SMSNotification
* PushNotification
* How to decide which one to create

The **business services are still clean**, but the **creation logic is duplicated in the caller modules**.

---

## 6. Now the Factory becomes useful

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

## 7. Now add another notification type

Tomorrow:

```python
class WhatsAppNotification(Notification):

    def send(self, message: str):
        print(f"Sending WHATSAPP: {message}")
```

Before Factory:

```text
Order module       → change
Payment module     → change
Other modules      → change
```

Every caller that creates notifications has to know about `WhatsAppNotification`.

With Factory:

```text
NotificationFactory → change
Order module         → NO change
Payment module       → NO change
Other modules        → NO change
```

Just add:

```python
elif provider == "whatsapp":
    return WhatsAppNotification()
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
          (Client)               (Client)
```

### What did OCP solve?

The interface solved the **usage/dependency problem**:

> `OrderService` and `PaymentService` don't depend on concrete notification classes.

### What did Factory solve?

The Factory solved the **creation problem**:

> Caller modules don't need to know which concrete notification class to create.

So don't think:

> **"OCP requires Factory."**

Think:

> **OCP solves how clients depend on objects. Factory solves how objects are created.**

That's the distinction you want to carry into your LLD interviews.
