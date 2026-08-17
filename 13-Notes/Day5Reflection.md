# Day 5 Reflection

**Date:** August 17, 2026

## 1. What problem does a Factory solve?

Factory solves duplicated or scattered object-creation logic by moving the decision of which concrete implementation object to create into one place.

## 2. Factory vs Builder — what's the difference?

Factory centralizes object creation, while Builder simplifies the step-by-step construction of a complex object.

## 3. Why can Singleton be dangerous?

Singleton can be dangerous because it introduces global shared state and hidden dependencies, making code harder to test, maintain, and reason about.

## 4. Which pattern did you find most useful?

Factory Pattern was the most useful for me because it clearly showed me how to separate object creation from the business logic. I also learned that having multiple implementations doesn't automatically mean I need a Factory — it becomes useful when object-creation logic is duplicated or scattered.

## 5. Which pattern do you think is overused?

Singleton is a pattern I think is often overused. It can make dependencies hidden and make testing harder. In many cases, dependency injection is a cleaner alternative.

## 6. Can you identify a Design Pattern from your current enterprise/AEM/AI work?

No

## 7. Confidence (1–10)

**6/10**

---

## 🎤 Interview Questions

Don't memorize these. Write your own answers first.

### Q1. What is a Design Pattern?

A design pattern is a proven way of organizing classes and objects to solve a common software design problem.

### Q2. Factory Pattern vs Builder Pattern?

### Q3. Why shouldn't we use Design Patterns everywhere?

Design patterns should solve a real design problem. Using them everywhere makes the code more complex, harder to understand, and sometimes adds unnecessary classes and abstractions.

### Q4. Why is Singleton often considered an anti-pattern?

Singleton is often considered an anti-pattern because it introduces global shared state, creates hidden dependencies, and makes testing harder.

### Q5. Where would you use Factory in a real enterprise system?

I would use Factory when the application can use multiple implementations and the concrete implementation is selected from configuration or runtime input.
