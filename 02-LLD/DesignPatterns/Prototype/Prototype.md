# Prototype Pattern

> **Prototype solves the problem of recreating a complex configured object by copying an existing object and changing only what is different.**

---

## 1. Suppose we have a `Dashboard`

A dashboard can contain widgets, filters, queries, layout, formatting, and permissions.

```python
class Dashboard:

    def __init__(self, name, widgets, filters, queries, layout, formatting, permissions):
        self.name = name
        self.widgets = widgets
        self.filters = filters
        self.queries = queries
        self.layout = layout
        self.formatting = formatting
        self.permissions = permissions
```

Assume we already have a fully configured Sales Dashboard.

---

## 2. Now suppose we need a Marketing Dashboard

The Marketing Dashboard should start almost the same as the Sales Dashboard, with different queries and a different name.

```python
marketing_dashboard = Dashboard(
    name="Marketing Dashboard",
    widgets=sales_widgets,
    filters=sales_filters,
    queries=["Campaign Query", "Leads Query"],
    layout=sales_layout,
    formatting=sales_formatting,
    permissions=sales_permissions,
)
```

---

## 3. But now notice the creation problem

The caller must know every part required to construct a dashboard, including the parts that should be identical to the Sales Dashboard.

If several callers need variations of that dashboard, this copying and construction logic becomes repeated and error-prone.

### Now we have the problem

The caller is rebuilding a known, valid configuration just to change a few fields.

This is the problem Prototype solves.

---

## 4. Now the Prototype becomes useful

We let the existing, configured object clone itself:

```python
from copy import deepcopy


class Dashboard:

    def clone(self):
        return deepcopy(self)
```

Now the caller starts from the Sales Dashboard and specifies only the differences:

```python
marketing_dashboard = sales_dashboard.clone()

marketing_dashboard.name = "Marketing Dashboard"
marketing_dashboard.queries = [
    "Campaign Query",
    "Leads Query",
]
```

---

## 5. But copying needs a deliberate policy

Not every field should necessarily be copied in the same way.

```text
Deep copy: widgets, filters, layout
Share: query engine, cache
Reset: id, owner, version
```

`deepcopy` is a simple starting point. In a real application, the prototype should explicitly control which state is copied, shared, or reset.

---

## The complete story

This is the important part to remember for your interview:

```text
Sales Dashboard
(fully configured prototype)
          |
       clone()
          |
          v
Marketing Dashboard
(same starting configuration)
          |
   customize differences
          |
          v
Marketing-specific Dashboard
```

Prototype is about **which existing configured instance to copy**. Factory is about **which concrete type to create**. Builder is about **how an object is assembled step by step**.

Use Prototype when an object is expensive or complex to construct and you frequently need valid variations of an existing instance. For simple objects, use a constructor instead.
