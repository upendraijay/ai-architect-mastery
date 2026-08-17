# 0232. Implement Queue using Stacks

## Problem

Implement a FIFO queue (`push`, `pop`, `peek`, `empty`) using **only two stacks**. The stacks may only expose the standard operations: push to top, pop from top, peek at top, size, and is-empty.

Follow-up: can each operation be **amortized O(1)**?

---

## My Initial Thought

A stack is LIFO, a queue is FIFO — the two are exact reversals of each other. So the whole problem is "where does the reversal happen?"

Pouring one stack into another reverses it: the bottom of the first becomes the top of the second. That gives the naive solution — on every `push`, drain the main stack into a helper, push the new element, then pour everything back so the oldest element sits on top. That works, but it pays O(n) on every single push.

The insight is that **the reversal doesn't need to happen on every push**. It only needs to have happened by the time someone asks to read from the front.

---

## Optimized Approach

Two stacks with a **lazy transfer**:

| Stack | Role |
|---|---|
| `stack` (in) | receives everything that gets pushed, newest on top |
| `reverseStack` (out) | holds the reversed order, oldest on top — ready to be popped |

- `push(x)` → append to `stack`. Always O(1). Never touches `reverseStack`.
- `pop()` / `peek()` → if `reverseStack` is empty, drain **all** of `stack` into it, then read the top.
- `empty()` → true only when **both** stacks are empty.

### The `if not reverseStack` guard is the whole solution

The transfer must happen **only when `reverseStack` is empty**. Draining into a non-empty `reverseStack` puts newer elements on top of older ones and destroys the FIFO order:

```text
push(1) push(2)   → in [1,2]     out []
pop()             → in []        out [2,1]   → returns 1
push(3)           → in [3]       out [2]
transfer anyway   → in []        out [2,3]   ← 3 is now above 2
pop()             → returns 3                ← wrong, 2 is older
```

With the guard, the elements sitting in `reverseStack` are always strictly older than everything in `stack`, so they must all be drained before the next batch is allowed in.

---

## Python Solution

```python
class MyQueue:

    def __init__(self):
        self.stack = []
        self.reverseStack = []

    def push(self, x: int) -> None:
        self.stack.append(x)

    def pop(self) -> int:
        if not self.reverseStack:
            while self.stack:
                self.reverseStack.append(self.stack.pop())

        return self.reverseStack.pop()

    def peek(self) -> int:
        if not self.reverseStack:
            while self.stack:
                self.reverseStack.append(self.stack.pop())

        return self.reverseStack[-1]

    def empty(self) -> bool:
        return not self.stack and not self.reverseStack
```

Accepted — 23/23 test cases. Runtime 0 ms (beats 100.00%), memory 19.43 MB (beats 53.21%).

### Worth cleaning up

`pop` and `peek` share the identical transfer block. In an interview, factor it out — it shows intent and removes the risk of fixing a bug in one copy but not the other:

```python
    def _transfer(self) -> None:
        if not self.reverseStack:
            while self.stack:
                self.reverseStack.append(self.stack.pop())

    def pop(self) -> int:
        self._transfer()
        return self.reverseStack.pop()

    def peek(self) -> int:
        self._transfer()
        return self.reverseStack[-1]
```

`in_stack` / `out_stack` also reads better than `stack` / `reverseStack`, since neither one is "the" stack.

---

## Complexity

| Operation | Time | Note |
|---|---|---|
| `push` | O(1) | always |
| `pop` | **Amortized O(1)** | O(n) on the transfer, O(1) otherwise |
| `peek` | **Amortized O(1)** | same |
| `empty` | O(1) | |
| Space | O(n) | each element lives in exactly one stack at a time |

### Why amortized O(1) is the honest answer

A single `pop` can cost O(n) when it triggers a transfer, so worst-case-per-operation is O(n). But **each element moves at most four times over its entire lifetime**: pushed onto `stack`, popped off `stack`, pushed onto `reverseStack`, popped off `reverseStack`. That's a constant amount of work per element, so n operations cost O(n) total → O(1) amortized.

The expensive transfer also can't happen twice in a row — it always leaves `stack` empty and pays for the cheap pops that follow it.

---

## What I Learned

- Two stacks compose into a queue because a stack is a *reversal*, and reversing twice restores the original order.
- The optimization was not a better data structure — it was **deferring work until it's actually needed**, and doing it in a batch. Same idea as lazy evaluation or write-back caching.
- "Worst case O(n)" and "amortized O(1)" are both true here. Saying only the first undersells the solution; saying only the second hides a real latency spike. State both.
- The correctness of the whole thing lives in one `if` — the guard preventing a transfer into a non-empty output stack. Ordering bugs like this pass the simple tests and fail on interleaved push/pop, which is exactly what the test suite probes.
