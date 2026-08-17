# 0121. Best Time to Buy and Sell Stock

## Problem

Given an array `prices` where `prices[i]` is the price of a stock on day `i`, choose **one** day to buy and a **later** day to sell to maximize profit. Return the maximum profit, or `0` if no profit is possible.

---

## My Initial Thought

Try every pair: for each buy day, check every later sell day and track the best difference.

Complexity:
- Time: O(n²)
- Space: O(1)

This times out on large inputs, and it recomputes the same information repeatedly — for each new day it re-scans all the prices before it.

---

## Optimized Approach

Single pass, tracking the minimum price seen so far.

The insight: to sell on day `i` at the best possible profit, the only thing worth knowing about days `0..i-1` is the **cheapest** one. Everything else about the past is irrelevant. So one variable replaces the entire inner loop.

For each price:
1. If it's lower than `minPrice`, it becomes the new best buy point.
2. Otherwise, treat today as a sell day — compute `price - minPrice` and keep it if it beats the current best.

The buy always happens before the sell because `minPrice` is only ever drawn from days already visited.

---

## Python Solution

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        minPrice = float('inf')

        for price in prices:
            if price < minPrice:
                minPrice = price
            else:
                profit = price - minPrice
                if profit > maxProfit:
                    maxProfit = profit

        return maxProfit
```

Result: 212/212 test cases passed — 43 ms (beats 65.56%), 28.76 MB (beats 20.36%).

The memory percentile is noise here: the solution allocates two scalars, so nearly all 28.76 MB is the input array plus the Python interpreter. There is nothing left to optimize.

---

## Complexity

| Metric | Value |
|---------|-------|
| Time | O(n) |
| Space | O(1) |

---

## What I Learned

- Seeding with `float('inf')` removes the empty-array and first-element special cases — the first price is always less than infinity, so it becomes `minPrice` automatically.
- The `else` branch is correct and not just an optimization: when `price < minPrice` the profit would be negative, so there is nothing to evaluate. Skipping it is free.
- Starting `maxProfit` at `0` encodes the "you may decline to trade" rule directly, so no negative result can ever escape.
- General pattern: when a brute force asks "for each `i`, scan all `j < i`", ask what **single summary** of the prefix actually matters. Here it's the min. That collapse from O(n²) to O(n) is the same move behind Kadane's algorithm.
- This is really [[Kadane's Algorithm]] in disguise — max profit equals the maximum subarray sum of the day-to-day price differences.
