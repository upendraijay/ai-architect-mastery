# Coffee Machine — SOLID Review


## SRP — mostly holds up

> A class should have **one, and only one, reason to change.**

| Class | Reason to change |
|---|---|
| `Beverage` | a new drink, a price change, or a change to what a drink is made of |
| `Inventory` | stock rules, refill policy |
| `Payment` | new payment rail |
| `Dispenser` | new machine model |
| `CoffeeMachine` | Nobody, ideally — it only sequences |

Four of the five hold a single responsibility cleanly. `CoffeeMachine` is the best of them: it owns no data of its own, so a change to stock rules, pricing, or hardware does not reach it.

---


### Weakness — `Beverage` has two reasons to change

```python
class Beverage:
    name: str
    price: float
    ingredients: dict[str, int]
```

`name` and `price` are **commercial** facts. `ingredients` is a **formulation** fact. They change at different times, for different reasons, at the request of different people:

| Change | Who asks for it |
|---|---|
| The price of a latte | Business / pricing |
| The quantity of milk in a latte | Product / operations |

Strictly, that is an SRP violation. It is accepted here because the alternative — a separate class holding one dictionary and no behaviour — buys a second class without buying a second responsibility worth isolating.

The signal to revisit it is **behaviour**, not size. If formulation ever gains logic — scaling quantities by cup size, substituting oat milk for dairy — that logic needs somewhere to live, and the split pays for itself.

---

## OCP — excellent for data, broken for behaviour

> Open for extension, closed for modification.

Let's evaluate each part.

| Scenario | Need to modify existing code? | OCP? |
|---|---|---|
| Add a new beverage | ❌ No | ✅ Yes |
| Change a beverage's ingredients | ❌ No | ✅ Yes |
| Refill ingredients | ❌ No | ✅ Yes |
| Change ingredient quantities | ❌ No | ✅ Yes |
| Add more inventory | ❌ No | ✅ Yes |
| Add a new payment method | ✅ Yes | ❌ No |
| Add a new dispenser type | ✅ Yes | ❌ No |

The split is clean: **everything expressed as data extends freely, everything expressed as behaviour does not.** A new beverage is a new `Beverage` object, so the machine never changes. A new payment rail is not.


### What breaks

#### Payment

`Payment` is a single concrete class with one method:

```python
class Payment:
    def process(self, amount: float) -> bool: ...
```

Now add cash, card, and UPI — three payment rails, which is the minimum any real machine supports. `process()` becomes:

```python
class Payment:
    def process(self, amount, method):
        if method == "cash":
            ...
        elif method == "card":
            ...
        elif method == "upi":
            ...
```


#### Dispenser

`Dispenser` has the same shape. Suppose two dispensers are needed later:

- **Coffee dispenser** — drives the real hardware
- **Simulator** — prints instead of pouring, for testing

With this design, `Dispenser` would need modification:

```python
class Dispenser:
    def dispense(self, beverage, mode):
        if mode == "hardware":
            ...
        elif mode == "simulator":
            ...
```



## LSP — satisfied

> Subtypes must be substitutable for their base types.

LSP only becomes relevant when you have **inheritance**, or interfaces with multiple implementations. This design has **composition but no inheritance hierarchy** — not one `extends`, not one abstract class.

### Does the design satisfy LSP?

**Yes.** There are no subclasses, so there is nothing that can violate substitutability.

That is satisfaction by absence, not by design. It is worth saying out loud, because the moment the OCP fix introduces a `PaymentProcessor` interface, LSP starts to matter.

### If we extend the design

`CoffeeMachine` should work with **any** `PaymentProcessor` without changing its behaviour.

```text
CoffeeMachine
        │
        ▼
PaymentProcessor.process(amount)
```

Whether the implementation is:

- `CashPayment`
- `CardPayment`
- `UPIPayment`

Each must honour the same contract — return a boolean, raise the same kinds of error, and not require the caller to know which one it received.


## ISP

> Clients should not be forced to depend on interfaces they do not use.

This design does not define any interfaces. Each class exposes only the methods it needs, so there are no "fat" interfaces that force unnecessary dependencies.

`Inventory` is the clearest case. It takes a plain `Dict<String, int>`:

```python
check_stock(required: dict[str, int]) -> bool
deduct_stock(required: dict[str, int]) -> None
```

It depends on nothing but ingredient names and quantities — it does not know that `Beverage` exists. Nothing about a beverage is forced on a class that only counts ingredients.

---

## DIP — Dependency Inversion Principle

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

### Does the design satisfy DIP?

**Partially.**

`CoffeeMachine` is the **high-level module** because it coordinates the coffee-making workflow. It does not create its sub-systems — they arrive through the constructor, which is why the UML shows aggregation rather than composition:

```python
class CoffeeMachine:

    def __init__(self, inventory: Inventory, payment: Payment, dispenser: Dispenser):
        self.inventory = inventory
        self.payment = payment
        self.dispenser = dispenser
```

But injection alone is not inversion. The **types are concrete**:

```text
CoffeeMachine
    ├── Payment      ← concrete class
    └── Dispenser    ← concrete class
```

So the business workflow remains coupled to the implementation. As the system evolves, the machine may need to support additional payment methods or different dispensing mechanisms.

| Current Dependency | New Requirement | Impact on `CoffeeMachine` |
|---|---|---|
| `Payment` | Support `CardPayment`, `UpiPayment`, `CashPayment` | May require code changes |
| `Dispenser` | Support `CupDispenser`, `MockDispenser` | May require code changes |

This violates the Dependency Inversion Principle because the high-level module depends on concrete implementations rather than abstractions.

> **The distinction worth carrying into an interview:** constructor injection is *dependency injection* — it decides who builds the object and when. *Dependency inversion* is about what the parameter is typed as. This design has the first and not the second.

---

### How can the design follow DIP?

Instead of depending on concrete classes, `CoffeeMachine` should depend on abstractions.

```text
                    CoffeeMachine
                  /               \
                 ▼                 ▼
          Dispenser         PaymentProcessor
         /         \         /             \
        ▼           ▼       ▼               ▼
CupDispenser  MockDispenser CardPayment  UpiPayment
```

In this design:

- `CoffeeMachine` depends only on the `PaymentProcessor` and `Dispenser` abstractions.
- `CardPayment` and `UpiPayment` implement `PaymentProcessor`.
- `CupDispenser` and `MockDispenser` implement `Dispenser`.

As a result:

- New payment methods can be added without modifying `CoffeeMachine`.
- Different dispenser implementations can be introduced without changing the business workflow.
- Mock implementations can be substituted during testing.
- The high-level workflow remains independent of implementation details.

---

### The Fix — an abstract base class for each

The wiring is already correct. `CoffeeMachine` takes its dependencies as constructor parameters, and the client assembles the object graph:

```python
machine = CoffeeMachine(
    Inventory(),
    CardPayment(),
    CupDispenser()
)

test_machine = CoffeeMachine(
    Inventory(),
    FakePayment(),
    MockDispenser()
)
```

What is missing is the abstraction those arguments are typed against:

```python
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...


class Dispenser(ABC):
    @abstractmethod
    def dispense(self, beverage: Beverage) -> None: ...
```

With those in place and the constructor re-typed, the same `CoffeeMachine` works with any class implementing `PaymentProcessor` or `Dispenser` — flexible, testable, and extensible without modifying the high-level business logic.
