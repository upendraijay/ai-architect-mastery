# 0206. Reverse Linked List

## Problem

Given the head of a singly linked list, reverse the list and return the new head.

---

## My Initial Thought

Walk the list, push every value into an array, then rebuild the list from the array backwards.

Complexity:
- Time: O(n)
- Space: O(n)

It works, but it copies data that never needed to move. The nodes are already there — only the `next` pointers need to change direction.

---

## Optimized Approach

Iterative pointer reversal with three references.

For each node, flip its `next` pointer to point backwards, then step forward:

1. Save `next_node = current.next` — **before** overwriting the link, or the rest of the list is lost.
2. Reverse the link: `current.next = previous`.
3. Slide both pointers forward: `previous = current`, `current = next_node`.

When `current` reaches `None`, `previous` is sitting on the last node visited — the new head.

```text
None <- 1    2 -> 3 -> None
        ^    ^
     previous current
```

---

## Python Solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        previous = None
        current = head

        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        return previous
```

Result: Accepted — 0 ms (beats 100%), 20.42 MB (beats 65.41%).

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(n) |
| Space | O(1) |

---

## What I Learned

- **Save the next pointer before overwriting it.** `current.next = previous` destroys the only reference to the rest of the list. That one temporary variable is the entire trick.
- **Return `previous`, not `current`.** The loop exits when `current is None`, so `current` is always `None` at that point. `previous` holds the final node, which is the new head.
- **Seeding `previous = None` does double duty:** it terminates the reversed list correctly (the old head's `next` becomes `None`), and it makes the empty-list case return `None` with no special-casing.
- The order of the four lines is not interchangeable — each one depends on the previous. Writing them out of order is the most common way to get this wrong under pressure.
- A recursive version exists and reads elegantly, but costs O(n) stack space and risks `RecursionError` on long lists. The iterative version is the one to give unless asked otherwise.
- This is a **building block**, not just an exercise. It appears inside [[0143 Reorder List]], [[0234 Palindrome Linked List]], and [[0092 Reverse Linked List II]].
