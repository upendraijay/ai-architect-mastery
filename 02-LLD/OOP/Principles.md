# The Four Principles of OOP

The four pillars of Object-Oriented Programming. Architects rely on them to build **maintainable, scalable, and resilient** systems — each one addresses a specific challenge in large-scale software design.

---

## 1. Encapsulation — Protecting Business Invariants

Encapsulation bundles **state (data)** with **behavior (methods)** and prevents external code from directly modifying an object's internal state.

An object should never be reachable into. Instead of this:

```python
account.balance = -1000
```

Expose controlled methods that enforce business rules:

```python
account.deposit(1000)
account.withdraw(200)
```

The object retains total control over its own state, so an invalid state becomes unreachable rather than merely discouraged.

**Architectural Value**

- Prevents invalid object states.
- Improves security.

---

## 2. Abstraction — Managing System Complexity

Abstraction exposes **what** an object does while hiding **how** it does it.

```python
paymentService.process(order)
```

The caller doesn't need to know whether the implementation performs:

- Database transactions
- Third-party API calls
- Authentication

Those implementation details remain hidden behind a simple interface. The caller depends on the **contract**, not the mechanism — which means the mechanism can change without breaking the caller.

**Architectural Value**

- Reduces system complexity.
- Decouples components.

---

## 3. Inheritance — Reusing Common Behavior

Inheritance allows a child class to reuse and extend the functionality of a parent class.

```python
class Vehicle:
    def start(self):
        print("Starting vehicle")


class Car(Vehicle):
    pass


class Truck(Vehicle):
    pass
```

Both `Car` and `Truck` inherit `start()` without duplicating code.

> **Architect's Note:** Modern architects prefer **composition over inheritance** unless there is a true Is-A relationship. Inheritance is the most tightly coupled relationship in OOP — a child depends on its parent's internals, so a change to the parent can break every descendant. Excessive inheritance produces rigid, fragile hierarchies.

**Architectural Value**

- Promotes code reuse.
- Reduces duplication.

---

## 4. Polymorphism — Building Plug-and-Play Systems

Polymorphism allows different objects to respond to the same method call in their own way.

### Without Polymorphism (Brittle Design)

```python
def process_checkout(payment_type, amount):

    if payment_type == "credit_card":
        connect_to_visa_gateway(amount)

    elif payment_type == "upi":
        verify_upi_pin_and_transfer(amount)

    elif payment_type == "paypal":
        redirect_to_paypal_api(amount)
```

**Problem**

Supporting Apple Pay means modifying this function:

```python
    elif payment_type == "apple_pay":
        process_apple_pay(amount)
```

As the application grows, this branching logic gets duplicated across many places — refunds, receipts, reconciliation. Every new payment method requires editing working code, which is where bugs come from.

### With Polymorphism (Flexible Design)

Define a common interface:

```python
from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def process(self, amount): ...
```

Each payment type implements its own version:

```python
class CreditCardPayment(Payment):
    def process(self, amount):
        print("Processing Credit Card")


class UPIPayment(Payment):
    def process(self, amount):
        print("Processing UPI")
```

The checkout code collapses to:

```python
def process_checkout(payment, amount):
    payment.process(amount)
```

The checkout system no longer needs to know the payment type. It simply sends the `process()` message, and each payment object decides how to handle it. Adding Apple Pay is now a **new class** — no existing code is touched.

**Architectural Value**

- Follows the **Open/Closed Principle (OCP)** — open for extension, closed for modification.
- Makes systems extensible and easier to maintain.
- Enables plug-and-play architecture.
