# 0155. Min Stack

## Problem

Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element — **all in O(1) time**.

---

## My Initial Thought

`push`, `pop`, and `top` are already O(1) on a plain list. The only hard requirement is `getMin()`.

Scanning the stack for the minimum is O(n), so that fails. Keeping a single `min` variable also fails: it works until you pop the minimum, and then there is no way to recover the *previous* minimum — that information was never stored.

So the minimum has to be **remembered as history, not as a single value**. History that unwinds in reverse order is itself a stack.

---

## Optimized Approach

Keep a second stack that tracks the minimum at each point in time.

| Operation | `stack` | `min_stack` |
|---|---|---|
| `push(v)` | always append | append **only if** `v <= min_stack[-1]` (or it's empty) |
| `pop()` | always pop | pop **only if** `stack[-1] == min_stack[-1]` |
| `top()` | `stack[-1]` | — |
| `getMin()` | — | `min_stack[-1]` |

`min_stack[-1]` is the minimum of everything currently in `stack`, by construction. When the current minimum is popped off the main stack, the value beneath it in `min_stack` is exactly the minimum that was in effect before it arrived.

### The `<=` is not a typo

Using `<` instead of `<=` breaks on duplicate minimums:

```text
push(1) → stack [1]    min_stack [1]
push(1) → stack [1,1]  min_stack [1]     ← with '<', the second 1 is not recorded
pop()   → stack [1]    min_stack []      ← but it still matches the top, so min_stack empties
getMin()                                 ← IndexError; the 1 still on the stack is lost
```

With `<=`, every value equal to the current minimum gets its own entry, so each pop removes exactly one.

---

## Python Solution

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_stack or value <= self.min_stack[-1]:
            self.min_stack.append(value)

    def pop(self) -> None:
        if self.stack[-1] == self.min_stack[-1]:
            self.min_stack.pop()
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

Accepted — 45/45 test cases. Runtime 86 ms (beats 76.53%), memory 32.12 MB.

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(1) for every operation |
| Space | O(n) worst case |

Worst case for space is a strictly decreasing sequence of pushes — every value is a new minimum, so `min_stack` grows to the same size as `stack`.

---

## Alternative — one stack of pairs

```python
self.stack.append((value, min(value, self.stack[-1][1] if self.stack else value)))
```

Store `(value, min_so_far)` in a single stack. Simpler to reason about and impossible to get wrong on duplicates, but it pays O(n) extra space *always*, whereas the two-stack version only pays it in the decreasing-sequence worst case. Worth mentioning in an interview as the trade-off you considered.

---

## What I Learned

- "O(1) minimum" is not solved by caching a value — it's solved by caching the **history** of that value.
- When popping must restore a previous state, the structure holding that state is almost always another stack.
- `<=` vs `<` on the min comparison is the entire correctness of the solution, and duplicates are the test case that exposes it.
- An auxiliary data structure that mirrors the main one is a recurring pattern; the same shape appears in monotonic-stack problems.
