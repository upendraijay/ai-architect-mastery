# 0141. Linked List Cycle

## Problem

Given the head of a linked list, determine if it contains a cycle — that is, whether some node can be reached again by continuously following `next` pointers. Return `true` if a cycle exists, otherwise `false`.

---

## My Initial Thought

Walk the list and remember every node visited in a hash set. If a node is seen twice, there is a cycle; if the walk reaches `None`, there isn't.

Complexity:
- Time: O(n)
- Space: O(n)

This works and is worth mentioning in an interview, but it stores every node just to answer a yes/no question.

---

## Optimized Approach

**Floyd's Cycle Detection** (the tortoise and hare) — two pointers moving at different speeds.

1. Start `slow` and `fast` at the head.
2. Each iteration, move `slow` one node and `fast` two nodes.
3. If they ever land on the same node, there is a cycle.
4. If `fast` runs off the end, the list is straight and there is no cycle.

The key insight: once both pointers are inside a cycle, `fast` closes the gap on `slow` by **exactly one node per iteration**. A gap that shrinks by 1 can never be skipped over — it goes 3 → 2 → 1 → 0 — so a meeting is guaranteed rather than merely likely.

---

## Python Solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False
```

Result: 29/29 test cases passed — 56 ms (beats 43.62%), 22.62 MB (beats 28.80%).

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(n) |
| Space | O(1) |

The O(1) space is the entire reason to prefer this over the hash set — same time complexity, no extra memory.

---

## What I Learned

- **The comparison must come after both pointers move.** Checking `slow == fast` at the top of the loop returns `True` immediately for every list, because both pointers start at `head`.
- **The guard `while fast and fast.next` covers two distinct crashes**, one per parity:
  - `fast is None` — the list ended on an even-length walk.
  - `fast.next is None` — ended on an odd-length walk, and `fast.next.next` would raise `AttributeError`.

  Checking only one of them fails on the other case. It also handles `head = None` and a single node with no special-casing.
- Falling out of the loop *is* the "no cycle" answer — reaching the end proves the list terminates.
- Comparing nodes with `==` compares identity here (no `__eq__` defined on `ListNode`), which is what we want — two distinct nodes holding equal values must not count as a meeting.
- Runtime percentile is noisy on this problem: the work is a few pointer hops, so the measurement is dominated by harness overhead. Nothing to optimize.
- Same two-pointer machinery solves [[0876 Middle of the Linked List]] (when `fast` hits the end, `slow` is at the middle) and extends to [[0142 Linked List Cycle II]] for finding the cycle's entry point.
