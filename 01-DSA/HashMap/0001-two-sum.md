# 0001. Two Sum

## Problem

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

---

## My Initial Thought

I first thought of checking every pair using two loops.

Complexity:
- Time: O(n²)
- Space: O(1)

---

## Optimized Approach

Use a HashMap.

For each number:
1. Compute the complement (`target - current`).
2. Check if it already exists in the map.
3. If yes, return both indices.
4. Otherwise, store the current number and its index.

---

## Python Solution

```python
def twoSum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i
```

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(n) |
| Space | O(n) |

---

## What I Learned

- HashMap enables O(1) average lookups.
- Always look for repeated searches that can be cached.
- Explaining the optimization path is as important as the final code.
