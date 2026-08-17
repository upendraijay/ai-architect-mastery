# Pattern Mapping

The goal of this document is to identify where design patterns naturally fit into our existing LLD designs.

---

## 1. Coffee Machine

The design has five classes: `CoffeeMachine`, `Beverage`, `Inventory`, `Payment`, `Dispenser`.

**None of the three creational patterns has a problem to solve here.** That is a finding, not a gap.

### Factory — No Natural Fit

Factory answers **"which concrete class should I create?"** ([[Factory]]). This design never asks that question.

- `Beverage` is **data**, defined in configuration and loaded in — a new drink is new data, not new code. Creating one is a data load, not a choice between classes.
- `Payment` and `Dispenser` are **single concrete classes with one method each**. There is nothing to select between.

There is no scattered creation logic and no runtime type decision, so a Factory would centralise a decision nobody is making.

---

### Builder — No Natural Fit

`Beverage(name, price, ingredients)` is three parameters, which [[Builder]] §2 puts firmly in dataclass territory. `Inventory` holds a single dictionary.

No object in this design is assembled in steps, contributed to from different places, or invalid until a completion point. Builder applies when **construction is a process** ([[Builder]] §11), and nothing here is constructed as a process.

---

### Singleton — No Natural Fit

`Inventory` is the only candidate: one machine, one ingredient store.

But `CoffeeMachine` receives its `Inventory` through the constructor — the hollow diamond in the class diagram — so exactly one already exists per machine. The guarantee comes from how the application assembles the object graph, not from the class enforcing it on itself.

---

## 2. Vending Machine

The design has six classes: `VendingMachine`, `Product`, `Inventory`, `Cart`, `Payment` *(abstract)*, `Dispenser` *(abstract)*.

**One pattern fits.** The difference from the Coffee Machine is that this design has a class with **several real implementations**, and a runtime choice between them.

### Factory — Natural Fit, for Payment

#### Design Problem

`Payment` is abstract with three implementations — `CashPayment`, `CardPayment`, `UpiPayment` — and the customer picks the rail at checkout. Something has to turn that choice into the right object:

```python
if method == "cash":
    payment = CashPayment()
elif method == "card":
    payment = CardPayment()
elif method == "upi":
    payment = UpiPayment()
```

Every module that assembles a `VendingMachine` carries the same block.

#### Pattern Fit

**Factory**

```python
payment = PaymentFactory.create(method)
```

#### Why?

This is precisely the question Factory answers — *which concrete class should I create?* ([[Factory]]). The alternatives already exist in the design and the choice is made at runtime, which is what makes this a fit rather than a hypothetical.

#### Not for Product

`Product(id, name, price)` is pure data, and the catalogue is loaded in from outside. Creating a `Product` is a data load, not a choice between classes.

#### Not for Dispenser

`StandardDispenser` is the only real implementation. A mock is selected by how a test wires the machine, not by a runtime decision, so there is nothing to select between.

---

### Builder — No Natural Fit

`Product(id, name, price)` is three parameters — dataclass territory, per [[Builder]] §2.

`Cart` is the tempting candidate: items are added one at a time, which looks like the incremental construction Builder describes. **It is not a Builder.** A Builder is scaffolding that produces a finished object at `build()` and is then discarded. `Cart` has no completion step, and it is itself the domain object the machine reads from and clears.

Accumulating state is not the same as constructing an object.

---

### Singleton — No Natural Fit

`Inventory` and `Cart` are both created and owned by `VendingMachine` — the filled diamonds in the class diagram. One machine already means exactly one of each, guaranteed by composition rather than by the classes enforcing it on themselves.
