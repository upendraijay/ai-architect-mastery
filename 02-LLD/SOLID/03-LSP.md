# Liskov Substitution Principle (LSP)

## Definition

The Liskov Substitution Principle (LSP) states that objects of a subclass should be able to **replace objects of their superclass without changing the expected behavior of the program**.

In other words, every subclass must preserve the behavior (or contract) promised by its parent. This makes inheritance safe and ensures that polymorphism works reliably.

---

## Problem it Solves

Inheritance creates an expectation that a subclass behaves like its parent. Problems occur when a subclass **changes** that behavior instead of **extending** it.

For example, suppose we have a common abstraction for different payment methods.

```python
class PaymentMethod:
    def pay(self, amount):
        pass
```

Two payment methods correctly implement this contract.

```python
class CreditCard(PaymentMethod):
    def pay(self, amount):
        print("Paid using Credit Card")


class UPI(PaymentMethod):
    def pay(self, amount):
        print("Paid using UPI")
```

The client code depends only on the parent abstraction.

```python
def checkout(payment: PaymentMethod):
    payment.pay(1000)
```

Now both subclasses work correctly.

```python
checkout(CreditCard())
checkout(UPI())
```

The `checkout()` function doesn't care whether it receives a `CreditCard` or a `UPI`. It simply trusts that every `PaymentMethod` knows how to process a payment.

This is **safe polymorphism**.

---

## LSP Violation

Now suppose someone introduces another subclass.

```python
class GiftCard(PaymentMethod):
    def pay(self, amount):
        raise Exception("Gift cards cannot be used for this purchase.")
```

The client code hasn't changed.

```python
checkout(GiftCard())
```

However, this time the program crashes.

Although `GiftCard` **is a** `PaymentMethod`, it does not preserve the behavior promised by its parent. Instead of processing the payment, it throws an exception.

The subclass **changed** the expected behavior instead of **extending** it, violating the Liskov Substitution Principle.

As a result:

- Polymorphism becomes unreliable, because not every `PaymentMethod` can be used interchangeably.
- Client code can no longer depend solely on the parent abstraction.
- Developers are forced to add special-case logic such as:

```python
if isinstance(payment, GiftCard):
    ...
```

Once client code starts checking concrete subclasses, the primary benefit of inheritance is lost.

---

## Why This Matters

When every subclass honors the parent's contract:

- Existing client code continues to work with new subclasses.
- New implementations can be added without modifying existing code.
- Client code remains simple, because it depends only on the parent abstraction.
- Polymorphism remains reliable.

This naturally supports the **Open/Closed Principle (OCP)**, because the system can be extended by adding new subclasses without modifying existing client code.

---

## Trade-offs

LSP encourages safe inheritance, but achieving that often requires additional design effort.

- **Careful inheritance design.** Real-world relationships can be misleading. A relationship that is true in English (for example, "a penguin is a bird") does not necessarily make a good inheritance relationship. In software, inheritance should be based on **behavior**, not vocabulary.
- **Composition may be a better choice.** If a subclass cannot fully honor the parent's contract, the inheritance hierarchy should be redesigned. In such cases, composition often provides a simpler and more flexible solution than inheritance.

### Example

Instead of this:

```text
PaymentMethod
      ▲
      │
   GiftCard
```

where `GiftCard.pay()` throws an exception and breaks `checkout()`, separate the paying behavior from the payment method itself:

```text
PaymentMethod
 │
 └── has a PaymentBehavior
        ├── PayableBehavior
        └── NonPayableBehavior
```

```python
from abc import ABC, abstractmethod


class PaymentBehavior(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class PayableBehavior(PaymentBehavior):
    def pay(self, amount):
        print(f"Paid {amount}")


class NonPayableBehavior(PaymentBehavior):
    def pay(self, amount):
        print("This payment method cannot be used for this purchase")


class PaymentMethod:
    def __init__(self, name, payment_behavior: PaymentBehavior):
        self.name = name
        self._payment_behavior = payment_behavior

    def pay(self, amount):
        self._payment_behavior.pay(amount)


credit_card = PaymentMethod("Credit Card", PayableBehavior())
upi = PaymentMethod("UPI", PayableBehavior())
gift_card = PaymentMethod("Gift Card", NonPayableBehavior())

checkout(credit_card)   # Paid 1000
checkout(upi)           # Paid 1000
checkout(gift_card)     # This payment method cannot be used for this purchase
```

`CreditCard` and `UPI` use `PayableBehavior`, while a gift card uses `NonPayableBehavior`. No inheritance contract is broken, and different payment methods simply have different behaviors. Nothing throws, and `checkout()` works for every payment method.
