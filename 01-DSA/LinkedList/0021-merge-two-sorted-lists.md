# 0021. Merge Two Sorted Lists

## Problem

Given the heads of two sorted linked lists `list1` and `list2`, splice them together into one sorted list and return its head. The result should be made by reusing the existing nodes.

---

## My Initial Thought

The obvious first idea is to collect all values into an array, sort it, and rebuild a list. That works but throws away the fact that both inputs are *already* sorted — and it costs O(n log n) time plus O(n) extra space.

---

## Optimized Approach

Two-pointer merge (the merge step of merge sort).

1. Create a dummy node so there is no special case for picking the head.
2. Keep a `current` tail pointer at the end of the merged list.
3. While both lists have nodes, append whichever head is smaller and advance that list.
4. When one list runs out, the other is already sorted — attach it wholesale instead of looping.
5. Return `dummy.next`.

The key insight: at every step the smallest unused node is at the head of one of the two lists, so a single comparison is enough.

---

## Python Solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        current = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next

            current = current.next

        # One list is exhausted; the remainder is already sorted.
        current.next = list1 if list1 else list2

        return dummy.next
```

Result: 208/208 test cases passed — 0 ms (beats 100%), 19.19 MB (beats 94.48%).

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(n + m) |
| Space | O(1) |

Space is O(1) because nodes are **relinked**, not copied — the only allocation is the single dummy node.

---

## What I Learned

- A **dummy (sentinel) head** removes the "is this the first node?" branch from every linked-list build. This is the single most reusable linked-list trick.
- Using `<=` rather than `<` keeps the merge **stable** — equal values retain their relative order (`list1` before `list2`). It doesn't matter for this problem's output, but it matters when nodes carry payloads.
- Attaching the leftover tail in one assignment beats looping through it; the remainder is already sorted and already linked.
- `current.next = list1 if list1 else list2` collapses the trailing if/else — one of the two is always `None`, and assigning `None` is the correct terminator anyway.
- This is exactly the merge step of merge sort, which is why it generalizes to [[0023 Merge k Sorted Lists]] via a heap.
