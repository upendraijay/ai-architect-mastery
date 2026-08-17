# Builder Design Pattern

> **Axis:** Builder is not about *which* class to instantiate — that is Factory. Builder is about the **construction process of one known object**.

## The Design Problem

Sometimes an object is easy to understand once it exists, but **difficult to construct**.

The construction may involve:

* Multiple steps
* Different parts added at different times
* Construction rules
* Validation before the object is complete
* A final step that makes the object usable

In such cases, putting everything inside `__init__` can make construction difficult to manage.

Builder separates:

> **How an object is constructed** from **what the object is**.

---

## 1. Start With a Simple Class

Imagine we have an `LLMConfig`.

```python
class LLMConfig:

    def __init__(
        self,
        model,
        temperature=None,
        max_tokens=None,
        timeout=None,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
```

We can simply create it:

```python
config = LLMConfig(
    model="gpt-4o",
    temperature=0.2,
    max_tokens=512,
)
```

This is simple and readable.

### Do we need Builder?

**No.**

If a constructor is already simple, adding a Builder only adds unnecessary complexity.

---

## 2. Python Already Solves Many "Builder" Problems

In languages where constructors become difficult because of many optional parameters, Builder can be useful.

But Python already provides:

* Keyword arguments
* Default values
* Dataclasses
* Type hints
* `__post_init__` for validation

For example:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:

    model: str
    temperature: float | None = None
    max_tokens: int | None = None
    timeout: int | None = None
    streaming: bool = False
    retries: int = 3

    def __post_init__(self):

        if self.temperature is not None:
            if not 0 <= self.temperature <= 1:
                raise ValueError("temperature must be between 0 and 1")

        if self.max_tokens is not None:
            if self.max_tokens <= 0:
                raise ValueError("max_tokens must be positive")

        if self.streaming and self.timeout is None:
            raise ValueError("streaming requires timeout")
```

This already gives us:

```text
Optional parameters → keyword arguments + defaults

Validation → __post_init__

Immutability → frozen=True

Required fields → constructor
```

So a simple `LLMConfig` is actually a **weak Builder example in Python**.

---

## 3. When Does Builder Actually Make Sense?

Builder becomes useful when **construction itself is a process**.

For example, imagine building a workflow graph:

```python
graph = StateGraph(AgentState)

graph.add_node("classify", classify_asset)
graph.add_node("caption", generate_caption)

graph.add_edge("classify", "caption")

graph.set_entry_point("classify")

app = graph.compile()
```

Here, we are not simply passing values to a constructor.

We are gradually constructing something:

```text
Create graph
    ↓
Add nodes
    ↓
Add relationships
    ↓
Set entry point
    ↓
Validate structure
    ↓
Compile
    ↓
Runnable application
```

The object is not really usable until the construction process is complete.

This is a much stronger reason to use Builder.

---

## 4. What Problem Does Builder Solve?

Without Builder, we would need to somehow pass the entire graph structure at once:

```python
graph = Graph(
    nodes=...,
    edges=...,
    entry_point=...,
    ...
)
```

But a graph may be built incrementally.

Different parts of the application may contribute different pieces:

```text
Worker A
   ↓
adds nodes

Worker B
   ↓
adds edges

Configuration
   ↓
sets entry point

Builder
   ↓
validates and completes the graph
```

The Builder provides a controlled construction process.

---

## 5. A Simple Builder

For illustration, imagine our own workflow builder:

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

Now the caller constructs the workflow step by step:

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

The Builder handles the **construction process**.

---

## 6. Why Is `build()` Important?

`build()` represents the point where construction is complete.

Before `build()`:

```text
Incomplete configuration
```

After `build()`:

```text
Complete and validated object
```

For example:

```text
Builder
   ↓
Add nodes
   ↓
Add edges
   ↓
Set entry point
   ↓
Validate
   ↓
build()
   ↓
Complete Workflow
```

This is different from simply passing values to a constructor.

---

## 7. Builder and Validation

Validation is an important benefit, but it is **not the definition of Builder**.

The Builder can validate rules that depend on the whole construction process.

For example:

```python
def build(self):

    if not self._entry_point:
        raise ValueError("Entry point is required")

    if self._entry_point not in self._nodes:
        raise ValueError("Invalid entry point")

    return Workflow(
        nodes=self._nodes,
        edges=self._edges,
        entry_point=self._entry_point,
    )
```

The important point is:

> **The object is validated when construction is complete, before it is handed to the rest of the application.**

---

## 8. Builder Is Not About Presets

A common mistake is to write:

```python
LLMConfigBuilder().production("gpt-4o").build()
```

and call that Builder.

The `production()` method is actually describing a **complete construction recipe**.

That is closer to a **Factory or Director** concept.

Builder should primarily expose operations for constructing parts of the object:

```python
builder = (
    WorkflowBuilder()
        .add_node(...)
        .add_node(...)
        .add_edge(...)
        .set_entry_point(...)
)
```

The Builder knows:

> **How to assemble the object.**

A separate Director or Factory can know:

> **Which standard recipe should be used.**

---

## 9. Can Builder and Factory Be Used Together?

**Yes.**

They solve different problems.

### Factory

Answers:

> **Which object or family should I create?**

### Builder

Answers:

> **How should I construct it?**

For example, suppose we support multiple LLM providers:

```text
OpenAI
Azure OpenAI
Watsonx
```

A Factory could select the appropriate Builder:

```python
class BuilderFactory:

    _builders = {
        "openai": OpenAIConfigBuilder,
        "watsonx": WatsonxConfigBuilder,
    }

    @classmethod
    def create(cls, provider):
        return cls._builders[provider]()
```

The caller can then build the configuration:

```python
builder = BuilderFactory.create("openai")

config = (
    builder
        .model("gpt-4o")
        .temperature(0.2)
        .build()
)
```

The responsibilities are separated:

```text
Factory
   ↓
Which builder/provider?

Builder
   ↓
How should it be constructed?

build()
   ↓
Complete object
```

---

## 10. Factory vs Builder

| Pattern | Main Question | Main Problem |
| --- | --- | --- |
| **Factory** | Which object should I create? | Choosing between different implementations |
| **Builder** | How should I construct this object? | Complex or multi-step construction |

### Easy way to remember

```text
Factory
   ↓
Which object?

Builder
   ↓
How do I construct it?
```

---

## 11. When Should I Use Builder in Python?

Before introducing Builder, ask:

> **Can `__init__` or a `dataclass` express this clearly?**

If yes:

**Use the simpler solution.**

Use Builder when:

```text
Construction is a process
        OR
Construction is incremental
        OR
Different parts are contributed independently
        OR
The final object requires construction-time validation
        OR
The same construction process can produce different representations
```

Otherwise, Builder may simply add unnecessary indirection.

---

## 12. Key Interview Takeaway

If asked:

**"What is the Builder Pattern?"**

A strong answer is:

> **Builder is a creational pattern used when constructing an object is complex or involves multiple steps. It separates the construction process from the final object and allows us to build the object in a controlled way.**

And if the interviewer asks:

**"Do you always need Builder for many parameters?"**

Say:

> **No. Especially in Python, keyword arguments, defaults, and dataclasses often make a Builder unnecessary. I would use Builder when construction itself is a process rather than just passing a set of values.**

That distinction shows **design judgment**, rather than simply knowing the pattern.
