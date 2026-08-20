# 0739. Daily Temperatures

## Problem

Given an array of daily temperatures, return an array where each position contains the number of days until a warmer temperature. If no warmer day occurs later, return `0` for that position.

---

## My Initial Thought

For each day, I need to find the next day with a higher temperature. Checking every later day would work, but it can take O(n²) time.

The important observation is that a day only needs to wait until the first warmer temperature appears. Days still waiting can be kept in a stack.

---

## Optimized Approach

Use a monotonic decreasing stack of indices.

For each temperature at index `i`:

1. While the current temperature is warmer than the temperature at the index on top of the stack, pop that previous index.
2. The current index is its first warmer day, so set the answer to `i - previous`.
3. Push `i` onto the stack to wait for a future warmer temperature.

Any indices left in the stack have no warmer future day, so their answers remain `0`.

---

## Python Solution

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        output = [0] * len(temperatures)
        stack = []

        for i, temp in enumerate(temperatures):
            while stack and temp > temperatures[stack[-1]]:
                previous = stack.pop()
                output[previous] = i - previous
            stack.append(i)

        return output
```

---

## Complexity

| Metric | Complexity |
|---|---|
| Time | O(n) |
| Space | O(n) |

Each index is pushed once and popped at most once, making the total stack work linear.

---

## What I Learned

- A monotonic stack is useful when each element needs the next greater or smaller element.
- Store indices when the answer depends on the distance between elements.
- Elements left in the stack have no warmer future day, so their answer stays `0`.

Accepted — 48/48 test cases. Runtime 83 ms (beats 89.85%), memory 28.66 MB (beats 46.42%).
