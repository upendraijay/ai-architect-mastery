# Builder Pattern

> **Builder solves the problem of constructing one known object when that construction happens in multiple steps.**

---

## 1. Suppose we need to create a `Workflow`

A workflow has nodes, edges, and one entry point:

```python
class Workflow:

    def __init__(self, nodes, edges, entry_point):
        self.nodes = nodes
        self.edges = edges
        self.entry_point = entry_point
```

The finished object is simple. The difficult part is collecting and validating all of its pieces.

---

## 2. Suppose different parts are added over time

```python
graph.add_node("classify", classify_asset)
graph.add_node("caption", generate_caption)

graph.add_edge("classify", "caption")

graph.set_entry_point("classify")
```

The workflow cannot be created in one useful constructor call because its configuration is assembled incrementally.

---

## 3. But now notice the construction problem

Without Builder, the caller must manage partially constructed state and eventually pass every detail to the constructor:

```python
nodes = {}
edges = []
entry_point = None

nodes["classify"] = classify_asset
nodes["caption"] = generate_caption
edges.append(("classify", "caption"))
entry_point = "classify"

workflow = Workflow(nodes, edges, entry_point)
```

### Now we have the problem

The caller owns the construction rules. Every caller must know how to collect the parts, when the workflow is complete, and how to validate it.

This is the problem Builder solves.

---

## 4. Now the Builder becomes useful

We move the step-by-step construction and final validation into one place:

```python
class WorkflowBuilder:

    def __init__(self):
        self._nodes = {}
        self._edges = []
        self._entry_point = None

    def add_node(self, name, handler):
        self._nodes[name] = handler
        return self

    def add_edge(self, source, target):
        self._edges.append((source, target))
        return self

    def set_entry_point(self, name):
        self._entry_point = name
        return self

    def build(self):
        if not self._entry_point:
            raise ValueError("Entry point is required")

        if self._entry_point not in self._nodes:
            raise ValueError("Entry point must reference a node")

        return Workflow(
            nodes=self._nodes,
            edges=self._edges,
            entry_point=self._entry_point,
        )
```

Now the caller expresses the construction process clearly:

```python
workflow = (
    WorkflowBuilder()
        .add_node("classify", classify_asset)
        .add_node("caption", generate_caption)
        .add_edge("classify", "caption")
        .set_entry_point("classify")
        .build()
)
```

---

## 5. Why `build()` matters

`build()` is the boundary between an incomplete configuration and a usable object. It validates rules that only make sense after all parts have been supplied.

```text
WorkflowBuilder
      |
add nodes and edges
      |
set entry point
      |
validate
      |
build()
      |
Complete Workflow
```

---

## The complete story

This is the important part to remember for your interview:

```text
Caller
  |
  | adds construction steps
  v
WorkflowBuilder
  |
  | collects parts and validates them
  v
build()
  |
  v
Workflow
(complete object)
```

Builder is about **how one known object is assembled**. Factory is about **which concrete object to create**.

Use Builder when construction is incremental, has multiple optional parts, needs final validation, or receives contributions from different places. If a clear constructor or `dataclass` is enough, prefer that simpler option.
