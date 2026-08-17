# Dependency Inversion Principle (DIP)

## Definition

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**


The **Dependency Inversion Principle (DIP)** states, Instead of the business layer depending directly on a database, payment gateway, or email service, both the business layer and the implementation should depend on a common abstraction.

---
## Understanding the Terms

A **high-level module** contains the application's business logic.

Examples:

- `OrderService`
- `NotificationService`

---

A **low-level module** contains the implementation details.

Examples:

- `MySQLDatabase`
- `PostgreSQLDatabase`
- `StripePaymentGateway`

Example:

```python
class MySQLDatabase:

    def save(self, order):
        ...
```

---

## Problem Without DIP

Suppose the business logic directly creates the database.

```python
class MySQLDatabase:

    def save(self, order):
        print("Saving order")


class OrderService:

    def __init__(self):
        self.database = MySQLDatabase()

    def place_order(self, order):
        self.database.save(order)
```


Here the business logic knows exactly which database it is using. This creates **tight coupling**. If tomorrow the company switches to PostgreSQL,

```python
self.database = PostgreSQLDatabase()
```

`OrderService` must change. The business logic changed because of a database decision.

That is exactly what DIP tries to avoid.

---

## Applying DIP

Instead of depending directly on a database, introduce an abstraction.

```python
from abc import ABC, abstractmethod


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order):
        pass
```

`OrderService` now depends only on the abstraction.

```python
class OrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def place_order(self, order):
        # Business rules...
        self.repository.save(order)
```

Concrete implementations provide the actual behavior.

```python
class MySQLRepository(OrderRepository):

    def save(self, order):
        print("Saving to MySQL")


class PostgreSQLRepository(OrderRepository):

    def save(self, order):
        print("Saving to PostgreSQL")
```

The dependency now looks like this:

```text
               OrderRepository
               ▲             ▲
               │             │
       OrderService   MySQLRepository
                      PostgreSQLRepository
```

Notice what has changed.

- `OrderService` no longer depends on `MySQLRepository` or `PostgreSQLRepository`. It depends only on the `OrderRepository` abstraction.
- The concrete repositories depend on the abstraction by implementing it.


Switching databases requires changing only the implementation supplied to `OrderService`, not the service itself.

```python
# MySQL
service = OrderService(MySQLRepository())

# PostgreSQL
service = OrderService(PostgreSQLRepository())
```

The business logic remains unchanged because it depends on an abstraction rather than a concrete implementation.

---

## Why is it called "Dependency Inversion"?

Without DIP:

```text
OrderService
      │
      ▼
MySQLDatabase
```

The business layer depends directly on the implementation.

With DIP:

```text
OrderService
      │
      ▼
OrderRepository
      ▲
      │
MySQLRepository
```

Now both the business logic and the implementation depend on the same abstraction.

This reversal of the dependency direction is called **Dependency Inversion**.

---

## Problem it Solves

- Business logic is independent of implementation details.
- Databases, APIs, and third-party services can be replaced easily.
- Business logic becomes easy to unit test using fake implementations.
- The code becomes more flexible and maintainable.

---

## Trade-offs

- Introduces additional abstractions and indirection.
- Object creation becomes more complex and often requires dependency injection or factories.
- Overusing abstractions for classes that will never change increases unnecessary complexity.

---

## DIP vs Dependency Injection

These terms are often confused.

| Concept | Description |
| --- | --- |
| **Dependency Inversion Principle (DIP)** | A design principle that says depend on abstractions instead of concrete implementations. |
| **Dependency Injection (DI)** | A technique for supplying dependencies from outside instead of creating them internally. |

Example of Dependency Injection:

```python
class OrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository
```
