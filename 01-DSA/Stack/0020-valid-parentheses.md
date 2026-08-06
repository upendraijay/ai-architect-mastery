# 0020. Valid Parentheses

## Problem

Given a string containing just the characters `(`, `)`, `{`, `}`, `[`, `]`, determine if the input string is valid — every opening bracket must be closed by the same type, and in the correct order.

---

## My Initial Thought

Nested structures need to be closed in reverse order of how they were opened. The last opening bracket must be the first one closed — that's Last In, First Out (LIFO), which a stack models directly.

---

## Optimized Approach

Use a Stack.

For each character:
1. If it's an opening bracket, push it onto the stack.
2. If it's a closing bracket, check it against the top of the stack.
3. If it matches, pop the stack. If it doesn't match (or the stack is empty), the string is invalid.
4. At the end, the string is valid only if the stack is empty.

---

## Python Solution

```python
class Solution:
    def isValid(self, s: str) -> bool:
        op_map = {
            "(": ")",
            "{": "}",
            "[": "]"
        }

        stack = []

        for ch in s:
            if ch in op_map:
                stack.append(ch)
            else:
                if not stack or op_map[stack.pop()] != ch:
                    return False

        return len(stack) == 0
```

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(n) |
| Space | O(n) |

---

## What I Learned

- Nested/balanced structure problems map naturally onto a stack.
- Encoding valid pairs in a map keeps the matching logic clean.
- The final "stack must be empty" check is easy to forget but essential.
