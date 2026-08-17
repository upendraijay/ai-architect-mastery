# Open/Closed Principle (OCP)

## Definition

> Software entities should be **open for extension, but closed for modification**.

Adding new behaviour should mean **adding new code**, not editing existing, working code.

---

## Problem it Solves

If adding new behaviour means editing existing, working code then:

- Every edit to working code carries risk.
- Code that already worked has to be re-tested.

In short: Every new feature requires modifying existing code, increasing the risk of bugs and inconsistencies. The Open/Closed Principle solves this by allowing new behavior to be added through extension, without changing existing, tested code.

---

## Bad Design Example

Every service branches on `customer_type`:

```python
class DiscountCalculator:
    def calculate(self, customer_type, amount):
        if customer_type == "regular":
            return amount * 0.05
        elif customer_type == "vip":
            return amount * 0.20


class ShippingCalculator:
    def calculate(self, customer_type):
        if customer_type == "regular":
            return 100
        elif customer_type == "vip":
            return 0


class LoyaltyPointsCalculator:
    def calculate(self, customer_type, amount):
        if customer_type == "regular":
            return int(amount)
        elif customer_type == "vip":
            return int(amount * 2)
```

### Why is this bad?

The same 2-way branch appears three times. Adding a customer type means editing all three — and nothing forces you to remember the third. Miss one and the system silently gives an Employee customer the wrong shipping fee, with no error anywhere.

---

## Good Design Example

Instead of asking **"What type of customer is this?"**, let the **customer object decide** how it behaves.

The behavior is moved into separate classes. When a new customer type is introduced, you **add a new class** instead of modifying existing ones. 
**This is polymorphism.**

```python
from abc import ABC, abstractmethod


class Customer(ABC):
    @abstractmethod
    def discount(self):
        pass

    @abstractmethod
    def shipping_fee(self):
        pass

    @abstractmethod
    def loyalty_points(self, amount):
        pass


class RegularCustomer(Customer):
    def discount(self):
        return 0.05

    def shipping_fee(self):
        return 100

    def loyalty_points(self, amount):
        return int(amount)


class VIPCustomer(Customer):
    def discount(self):
        return 0.20

    def shipping_fee(self):
        return 0

    def loyalty_points(self, amount):
        return int(amount * 2)
```

Now the services become much simpler.

```python
class DiscountCalculator:
    def calculate(self, customer, amount):
        return amount * customer.discount()


class ShippingCalculator:
    def calculate(self, customer):
        return customer.shipping_fee()


class LoyaltyCalculator:
    def calculate(self, customer, amount):
        return customer.loyalty_points(amount)
```

---

## Adding a New Customer Type

Business says:

> "Employee customers get 30% discount, free shipping, and 3x loyalty points."

We **don't modify any existing class**.

We simply add:

```python
class EmployeeCustomer(Customer):
    def discount(self):
        return 0.30

    def shipping_fee(self):
        return 0

    def loyalty_points(self, amount):
        return int(amount * 3)
```

That's it.

Notice what **didn't change**:

- ✅ `DiscountCalculator`
- ✅ `ShippingCalculator`
- ✅ `LoyaltyCalculator`
- ✅ `RegularCustomer`
- ✅ `VIPCustomer`

Only **one new class** was added.

---

## Advantages

- **Easier to extend.** New functionality can be added by creating new classes instead of modifying existing ones.
- **Lower risk of regressions.** Existing, tested code remains unchanged, reducing the chance of breaking current functionality.
- **Better maintainability.** Each implementation is independent, making the code easier to understand and modify.
- **Improved testability.** New implementations can be tested independently without affecting existing ones.

---

## Trade-offs

Like any design principle, OCP should be applied only when there is a real need.

- **More classes and abstractions.** Supporting extension often requires additional interfaces and implementations, increasing the number of files.
- **Harder to navigate.** Understanding the program flow may require jumping between interfaces and concrete implementations.

---

## Related

- [[WhySOLID]] — the cost/benefit of applying these principles
- [[Principles]] — polymorphism, the mechanism OCP relies on
- [[DIP]] — depending on abstractions, which makes OCP possible
