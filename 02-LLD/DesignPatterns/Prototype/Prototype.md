# Prototype Design Pattern

> **Prototype is a creational design pattern where we create a new object by cloning an existing, fully configured object instead of constructing it from scratch.**

## Problem

Suppose we have a complex `Dashboard`:

```text
Dashboard
├── Widgets
├── Filters
├── Queries
├── Layout
├── Formatting
└── Permissions
```

We already have a fully configured **Sales Dashboard**.

Now the user says:

> "Create a Marketing Dashboard similar to the Sales Dashboard."

Without Prototype, we may need to pass all the existing configuration again:

```python
marketing = Dashboard(
    widgets=sales_widgets,
    filters=sales_filters,
    queries=sales_queries,
    layout=sales_layout,
    formatting=sales_formatting,
    permissions=sales_permissions,
)
```

The caller needs to understand **how the Dashboard is constructed**.

---

## Prototype Solution

Instead, we use the existing dashboard as a template:

```python
marketing = sales_dashboard.clone()

marketing.name = "Marketing Dashboard"
marketing.queries = [
    "Campaign Query",
    "Leads Query"
]
```

Conceptually:

```text
             Sales Dashboard
            Fully configured
                    │
                  clone()
                    │
                    ▼
          Marketing Dashboard
             Same starting
             configuration
                    │
              customize
                    ▼
          Marketing-specific
              dashboard
```

The key benefit is:

> **The caller doesn't need to know how the complex object is constructed. It only needs to specify what is different.**

---

## Simple Python Implementation

```python
from copy import deepcopy


class Dashboard:

    def clone(self):
        return deepcopy(self)
```

Usage:

```python
sales_dashboard = Dashboard()

marketing_dashboard = sales_dashboard.clone()
```

In a real application, we may need to control what gets copied, shared, or reset.

For example:

```text
Deep copy:
  widgets
  filters
  layout

Share:
  query engine
  cache

Reset:
  id
  owner
  version
```

---

## Prototype vs Factory vs Builder

This is the easiest way to explain the difference in an interview:

| Pattern | Question |
| --- | --- |
| **Factory** | "What type of object do you want?" |
| **Builder** | "How do you want to construct it?" |
| **Prototype** | "Which existing object should this be based on?" |

### Factory

```python
dashboard = DashboardFactory.create("sales")
```

Factory creates based on a **recipe/type**.

### Builder

```python
dashboard = (
    DashboardBuilder()
    .add_widget("Revenue Chart")
    .add_filter("Region")
    .set_layout("3-column")
    .build()
)
```

Builder creates through **step-by-step construction**.

### Prototype

```python
dashboard = sales_dashboard.clone()
```

Prototype creates from an **existing configured instance**.

---

## When Would You Use Prototype?

I would use Prototype when:

1. The object is **complex to construct**.
2. We frequently need **variations of an existing object**.
3. The existing object is already a valid, configured template.
4. Templates may need to be created or registered **at runtime**.

For example:

```text
Sales Dashboard Template
Finance Dashboard Template
HR Dashboard Template
Marketing Dashboard Template
```

Each can be stored as a prototype and cloned when needed.

---

## Important Trade-off

Prototype isn't automatically better than a constructor.

If the object is simple:

```python
User("Upendra", 35)
```

there is no reason to use Prototype.

The decision is:

> **If I need an instance of a known type → Factory.**

> **If I need to construct something step by step → Builder.**

> **If I need a variation of an existing configured instance → Prototype.**

---

## 🎯 30-Second Interview Answer

If the interviewer simply asks **"Explain Prototype Design Pattern"**, I'd answer:

> **Prototype is a creational design pattern used when we want to create a new object by cloning an existing object instead of constructing it from scratch.**
>
> For example, suppose we have a complex Sales Dashboard containing widgets, filters, queries, layout, and permissions. If a user wants a Marketing Dashboard similar to it, instead of passing all those configurations to the constructor again, we can clone the Sales Dashboard and modify only the differences.
>
> The main benefit is that the caller doesn't need to know how the complex object is constructed. It only needs to know which existing object it wants to use as a template.
>
> So, **Factory creates from a recipe, Builder assembles step by step, and Prototype creates from an existing configured instance.**
