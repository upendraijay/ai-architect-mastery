# UML Basics

UML (Unified Modeling Language) is a visual language. It helps developers and architects describe classes, objects, and the relationships between them **before writing code**.

---

## 1. UML Class Diagram

```text
+----------------------+
|       Car            |   ← Class Name
+----------------------+
| - brand : String     |   ← Attributes (State)
| - speed : int        |
+----------------------+
| + accelerate()       |   ← Methods (Behavior)
| + brake()            |
+----------------------+
```

---

## 2. Visibility Symbols

| Symbol | Meaning |
|---|---|
| `+` | Public |
| `-` | Private |
| `#` | Protected |

---

## 3. Relationships

### 3.1 Association

Association means two classes know about each other and collaborate, but neither owns the other.

```text
Driver ------------- GPS
```

---

### 3.2 Aggregation

Aggregation means the parent stores the child, but the child can exist independently.

```text
Department ◇──────── Professor
```

---

### 3.3 Composition

Composition means the parent owns the child. The child cannot exist independently.

```text
Car ◆──────── Engine
```

---

### 3.4 Multiplicity

| Multiplicity | Meaning | Example |
|---|---|---|
| `1` | Exactly one | Person ↔ Passport |
| `0..1` | Zero or one | Car ↔ Sunroof |
| `*` or `0..*` | Zero or many | Customer ↔ Orders |
| `1..*` | One or more | Order ↔ LineItem |
