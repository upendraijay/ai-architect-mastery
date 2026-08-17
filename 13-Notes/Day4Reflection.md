# Day 4 Reflection

**Date:** August 15, 2026

## 1. Which SOLID principle felt most intuitive?

**DIP — Dependency Inversion.**

It was the most intuitive because the fix is something I can *see* in the code. The problem is concrete — `CoffeeMachine` names `Payment` and `Dispenser` directly — and so is the remedy: define the abstraction, and pass the implementation in through the constructor.

```python
def __init__(self, inventory, payment: PaymentProcessor, dispenser: Dispenser):
```

Once the dependency arrives from outside, the high-level workflow stops caring which implementation it got. The testing benefit made it click: the same machine class works with `CardPayment` in production and `FakePayment` in a test, with no change to the machine.

## 2. Which one was hardest?

**ISP — Interface Segregation.**

It was hardest because my design had **no interfaces to segregate**. Every class exposed exactly the methods it needed, so the principle was technically satisfied — but satisfied by accident, not by design. It is difficult to build intuition for a principle when the design has no way to violate it yet.

I found the concrete case while designing the Vending Machine. If `Payment` grows from one method to three:

```text
pay(amount)
refund(amount)
return_change(amount)
```

then `CardPayment` is forced to implement `return_change()`, which is meaningless for a card. That is the ISP violation — and the fix is to split the interface so a class only depends on what it actually uses.

So ISP is not about how many methods an interface has. It is about whether every implementer genuinely needs all of them.

## 3. Did my Coffee Machine violate any SOLID principle?

**Yes — OCP and DIP.** Both for the same root cause: `Payment` and `Dispenser` were concrete classes rather than abstractions.

| Principle | Verdict | Reason |
|---|---|---|
| SRP | ✅ Held | Each class had one reason to change. Only weakness was naming — `add_ingredient()` meant two unrelated things on `Recipe` and `Inventory`. |
| OCP | ❌ Violated | Adding cash/card/UPI meant editing `Payment.process()` into an `if/elif` ladder. Open for data (new beverages), closed for behaviour. |
| LSP | ✅ Held | Vacuously — there was no inheritance anywhere in the design, so nothing could break substitutability. |
| ISP | ✅ Held | No interfaces defined, so no fat interfaces to depend on. |
| DIP | ❌ Violated | `CoffeeMachine` depended on concrete `Payment` and `Dispenser` instead of abstractions. |

Full analysis in [[SOLID-Review]].

The useful part was that **OCP and DIP failed together**. They were not two separate mistakes — depending on a concrete class *is* what forces modification when a new variant arrives. Fixing the dependency direction fixed both.

I carried that forward: in the [[VendingMachine]] design, `Payment` and `Dispenser` were abstract from the start, and adding UPI is a new subclass rather than an edit.

## 4. What is the difference between OOP and SOLID?

**OOP gives me the tools. SOLID tells me how to use them well.**

- **OOP** is the mechanism — classes, objects, encapsulation, inheritance, polymorphism, and the relationships between them.
- **SOLID** is the judgment — a set of guidelines for arranging those mechanisms so the system survives change.

The key realisation is that **valid OOP can still be bad design**. A single 2000-line class with private fields and getters is perfectly legal OOP. It violates SRP immediately. OOP will not stop me; SOLID is what tells me it is wrong.

This continues the ladder from Day 3:

```text
Writing classes   →  the building blocks
OOP               →  assigning responsibility and defining collaboration
SOLID             →  keeping that structure maintainable as it changes
```

Also worth remembering from [[WhySOLID]]: these are **guidelines, not rules**. Applied too aggressively, a simple feature becomes dozens of tiny classes and the business logic disappears into file navigation.

## 5. Confidence (1–10)

**6/10**

Up from 5 on Day 3. I can now name all five principles, spot OCP and DIP violations in my own earlier design, and apply the fix structurally rather than by memorising an example. Still shaky on ISP and on judging *when* an abstraction is worth its cost versus premature.
