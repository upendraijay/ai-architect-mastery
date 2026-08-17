# Single Responsibility Principle (SRP)

## Definition

> A class should have **one, and only one, reason to change**.

If the Finance team and the Operations team can both demand a change to the same class, that class has two responsibilities.

---

## Problem it Solves

If a class has multiple responsibilities:

- A change for one feature can accidentally break another feature.
- The class grows larger and becomes difficult to understand and maintain.
- Multiple developers often modify the same class, leading to merge conflicts.

A class that does too many things becomes harder to understand, maintain, test, and extend. The Single Responsibility Principle solves this by ensuring each class has one responsibility and one reason to change.

---

## Bad Design Example

```python
class OrderService:
    def validate_order(self):
        """Validate order details."""

    def save_order(self):
        """Save the order to the database."""

    def send_confirmation_email(self):
        """Send confirmation email to the customer."""

    def generate_invoice(self):
        """Generate the invoice PDF."""
```

### Why is this bad?

`OrderService` has multiple responsibilities:

- Validating orders
- Storing data
- Sending emails
- Generating invoices

Each responsibility can change for a different reason:

- Validation rules change.
- Database implementation changes.
- Email template changes.
- Invoice format changes.

This means `OrderService` has multiple reasons to change, violating the Single Responsibility Principle.

---

## Good Design Example

```python
class OrderValidator:
    def validate(self):
        pass


class OrderRepository:
    def save(self):
        pass


class EmailService:
    def send_confirmation(self):
        pass


class InvoiceService:
    def generate(self):
        pass
```

Now each class has one responsibility and one reason to change.

---

## Trade-offs

Like any design principle, SRP should be applied when it adds value. Overusing it can make the code unnecessarily complex.

- **More classes and files.** Splitting responsibilities creates additional classes, which can make the project structure larger. Understanding one feature may then require looking at multiple classes, which sometimes makes the code harder to follow.

---

## Related

- [[WhySOLID]] — when to apply SOLID and when not to
- [[Principles]] — encapsulation and abstraction, which SRP builds on
