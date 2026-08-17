# Why OOP — Fundamentals and the Architect's Case

Classes, objects, message passing, and object relationships — followed by the architectural justification for using OOP at all.

---

## What is a Class?

A class is a **blueprint or template** for creating objects.

A class defines two things:

1. **Attributes** — what information each object will store.
2. **Methods** — what actions each object can perform.

### Example

```python
class Car:
    def __init__(self, brand, speed):
        self.brand = brand
        self._speed = speed

    def accelerate(self, amount):
        self._speed += amount

    def brake(self, amount):
        self._speed = max(0, self._speed - amount)
```

This class defines that every object of `Car` can store the `brand` and `_speed` information, and can perform the actions `accelerate()` and `brake()`.

---

## What is an Object?

An object is an **instance** of a class — a concrete entity created from a class blueprint.

```python
car1 = Car("Toyota", 60)
car2 = Car("Toyota", 60)
```

Objects have two things.

### 1. State

The state represents the current values stored within an object's attributes. Each object maintains its own isolated memory:

- **State of `car1`:** `brand = "Toyota"`, `_speed = 60`
- **State of `car2`:** `brand = "Toyota"`, `_speed = 60`

**Independence:** even though `car1` and `car2` start with identical values, changing one object's state never affects the other.

### 2. Behavior

Behavior defines the actions an object can perform:

- `car1.accelerate(15)` → modifies `_speed` state.
- `car1.brake(10)` → modifies `_speed` state.

---

## Message Passing

Message passing is the process by which objects communicate with each other by **sending requests** rather than directly accessing or modifying each other's internal data.

In OOP, when you call a method on an object, you are technically sending it a request.

### The 3 Parts of a Request

| Part | Meaning |
|---|---|
| **Receiver** | The target object receiving the request |
| **Selector / Method** | The action or behavior being requested |
| **Arguments (Payload)** | The extra data needed to perform that action |

```python
# Receiver . Selector ( Arguments )
  car1     . accelerate(20)
```

The caller sends a message to `car1` requesting it to execute `accelerate` with the argument `20`. The sender does **not** directly change `car1._speed = 80` — it asks `car1` to update itself.

### Why Message Passing Matters

- **Preserves encapsulation** — the sender doesn't need to know how the receiver works internally. It only cares about the response or result.
- **State control** — the receiving object retains total control over its own internal state, preventing unauthorized or invalid external changes.

---

## Object Relationships in OOP

The four relationships, ordered from **weakest to strongest coupling**.

### 1. Association

Association is the **weakest** relationship between two objects. One object uses another object to perform a task, but does not store or own it.

```python
class GPS:
    def navigate(self):
        print("Navigating...")


class Driver:
    def drive(self, gps):
        gps.navigate()      # Uses GPS temporarily


gps = GPS()
driver = Driver()

driver.drive(gps)
```

**Explanation**

- `Driver` uses a `GPS`.
- The `GPS` object is passed as a method parameter.
- `Driver` does not store the `GPS`.
- After `drive()` finishes, the relationship ends.
- Both objects can exist independently.

---

### 2. Aggregation

Aggregation is a relationship where one object **has** another object. The parent stores a reference to the child, but does not create or own it.

```python
class Professor:
    def __init__(self, name):
        self.name = name


class Department:
    def __init__(self, professor):
        self.professor = professor      # Stores Professor


prof = Professor("John")
dept = Department(prof)
```

**Explanation**

- `Department` has a `Professor`.
- The `Professor` is created **outside** the `Department`.
- The `Department` stores a reference to it.
- If the `Department` is deleted, the `Professor` still exists.

---

### 3. Composition

Composition is a **strong** relationship where the parent creates and owns the child object.

```python
class Engine:
    pass


class Car:
    def __init__(self):
        self.engine = Engine()      # Creates Engine


car = Car()
```

**Explanation**

- `Car` has an `Engine`.
- The `Engine` is created **inside** the `Car`.
- The `Engine` belongs only to that `Car`.
- If the `Car` is destroyed, its `Engine` is destroyed as well.

---

### 4. Inheritance

Inheritance allows one class to inherit the attributes and methods of another class.

```python
class Car:
    def drive(self):
        print("Driving...")


class ElectricCar(Car):
    def charge(self):
        print("Charging battery...")


tesla = ElectricCar()

tesla.drive()      # inherited
tesla.charge()     # own method
```

**Explanation**

- `ElectricCar` **is a** `Car`.
- It inherits the `drive()` method.
- It also defines its own `charge()` method.

---

## Why Do Architects Still Use OOP?

Software architects use OOP because its four pillars help manage complexity in enterprise systems. **Encapsulation** protects business rules by keeping data and behavior together. **Abstraction** hides implementation details behind clean interfaces, reducing coupling. **Inheritance** promotes code reuse where a true Is-A relationship exists, while **polymorphism** enables plug-and-play extensibility by allowing new implementations to be added without changing existing code. Together, these principles make enterprise applications easier to maintain, extend, test, and scale.
