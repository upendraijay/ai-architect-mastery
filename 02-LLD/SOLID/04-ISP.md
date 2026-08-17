# Interface Segregation Principle (ISP)

## Definition

The ISP states that instead of creating one large, general-purpose interface, you should split it into multiple **small, focused interfaces** so that each client relies on the smallest possible contract.

---

## Problem it Solves

As software grows, interfaces often accumulate more and more functionality. New methods are frequently added to existing interfaces because it seems convenient. Over time, these interfaces become **fat interfaces** that try to serve too many different clients.

A fat interface forces every implementing class to provide an implementation for every method, even when some of those methods are irrelevant to that class.

This leads to several problems:

1. **Incorrect implementations**, such as empty methods or methods that raise `NotImplementedError`, simply to satisfy the interface.
2. **Unnecessary coupling.** Implementing classes become dependent on methods they do not actually use. As the interface evolves, every implementing class must be reviewed and potentially updated, even when the changes are irrelevant to that class.

ISP solves this problem by splitting large interfaces into smaller ones.

---

## Bad Design Example

```python
from abc import ABC, abstractmethod


class Machine(ABC):
    @abstractmethod
    def print_document(self, doc): ...

    @abstractmethod
    def scan(self, doc): ...

    @abstractmethod
    def fax(self, doc): ...


class OldPrinter(Machine):
    def print_document(self, doc):
        print(f"Printing {doc}")

    def scan(self, doc):
        raise NotImplementedError("This printer cannot scan")

    def fax(self, doc):
        raise NotImplementedError("This printer cannot fax")
```

`OldPrinter` is forced to implement operations that it does not actually support. The `Machine` interface promises that every implementation can print, scan, and fax, but `OldPrinter` can only print. To satisfy the interface, it resorts to workarounds such as:

```python
raise NotImplementedError("This printer cannot scan")
```

This is a sign that the interface is **too broad**. An implementation should not be forced to provide methods it cannot meaningfully support. The design should be improved by splitting the large interface into smaller, focused interfaces so that each class implements only the capabilities it actually provides.

---

## Good Design Example

```python
from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_document(self, doc: str) -> None:
        pass


class Scanner(ABC):
    @abstractmethod
    def scan(self, doc: str) -> None:
        pass


class OldPrinter(Printer):
    def print_document(self, doc: str) -> None:
        print(f"Printing {doc}")


class MultiFunctionPrinter(Printer, Scanner):
    def print_document(self, doc: str) -> None:
        print(f"Printing {doc}")

    def scan(self, doc: str) -> None:
        print(f"Scanning {doc}")
```

### Explanation

Instead of one large `Machine` interface, the design has been split into two smaller interfaces:

- `Printer` contains only printing behavior.
- `Scanner` contains only scanning behavior.

`OldPrinter` implements only the `Printer` interface because it can only print.

`MultiFunctionPrinter` implements both `Printer` and `Scanner` because it supports both capabilities.

As a result, no class is forced to implement methods it does not support. Each class implements only the interfaces that represent its actual capabilities, which is exactly what the Interface Segregation Principle recommends.

---

## Trade-offs

Like any design principle, ISP should be applied only when it improves the design. Splitting interfaces too aggressively can create unnecessary complexity.

- **Too many interfaces.** Creating very small interfaces for every capability can make the design harder to understand, navigate, and maintain.

---

## Related

- [[WhySOLID]] — guidelines, not rules
- [[SRP]] — the same idea applied to implementations rather than contracts
- [[LSP]] — fat interfaces cause substitutability violations
- [[DIP]] — small interfaces are what high-level code should depend on
