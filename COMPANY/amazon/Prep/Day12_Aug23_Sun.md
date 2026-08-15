# Sun Aug 23 — Day 12 of 18
### PHASE 2 — CORE STRUCTURES · ★★ MOCK LOOP #1 — full dress rehearsal

**Answer key for reference: `none — no new material`** · Solutions for today's problems are at the bottom of this file.

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Read only the *Trigger* and *Insight* lines below — never the code. Close it, keep going. At 20 min, read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

---

## TODAY'S CHECKLIST

| ☐ | Block | Full | Compressed |
|---|---|---|---|
| ☐ | A — Primitives from memory | 45 min | 30 min |
| ☐ | B — Re-solve queue | 30 min | 20 min |
| ☐ | C — Problems / mock | 3h 30m | 2h |
| ☐ | D — Design | 60 min | 40 min |
| ☐ | E — Leadership Principles | 45 min | 20 min |
| ☐ | F — Pattern Journal | 20 min | 15 min |

---

## Block A — Primitives (from memory, timed)

**Full Tier 1 + Tier 2 from memory, timed (30 min).**

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Skip today. The mock is the priority.

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C

### THE LOOP — treat this as real. Phone off. Door shut.

**Round 1 (60 min) — Coding.**
- [ ] Two unseen problems from the pool at the bottom of this file
- [ ] Record it
- [ ] LP question first, then full Round Script
- [ ] **Review the recording (25 min)**

**Round 2 (60 min) — Coding.**
- [ ] Two fresh problems: one linked list, one graph
- [ ] Record it
- [ ] **Review (25 min)**

**Break (30 min).** Actually break. The real loop has these and you need to practise coming back cold.

**Round 3 (60 min) — Design.**
- [ ] One HLD from the six you've prepared. Paper only.
- [ ] Talk the entire time
- [ ] **Then push back on your own design** — on camera, argue against one decision you made, and defend it
- [ ] **Review (20 min)**

**LP block (45 min).** All 14 stories, timed, out loud, back to back.

### DEBRIEF (30 min) — the most valuable document you'll write this month

Write down, honestly:
1. Which patterns did I freeze on?
2. Where did I go silent?
3. Did I skip clarifying questions under time pressure?
4. Did I skip the dry run?
5. Which LP stories came out weak or over-long?
6. **My three worst areas:** ______, ______, ______

**That list drives Phase 3 and Phase 4.** Be brutal. Nobody sees it but you.

---

## Block D — Design

Included in the loop above (Round 3). No separate design block today.

---

## Block E — Leadership Principles

Included in the loop above. No separate LP block.

---

### Block F — Pattern Journal (20 min)

One entry per problem you struggled with. Handwritten beats typed.

```
Problem:            ____
Trigger phrase:     ____   <- the words in the prompt that should have tipped you off
Pattern:            ____
Key insight:        ____
Where I got stuck:  ____
Primitive used:     #__
Re-solve on:        +1d ____   +3d ____   +7d ____
```

**The Trigger line matters most.** You already know approaches. What you lack is the reflex mapping *problem phrasing → pattern*. Build it explicitly.

---

## END OF DAY — honest check

- [ ] All four rounds completed without skipping?
- [ ] All recordings actually watched?
- [ ] Debrief written, with three named weak areas?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

**⚠ MOCK POOL — do not read until your mock is finished.** These are the unseen problems for today's simulated round.

### 54. Spiral Matrix
**Trigger:** traverse a matrix in spiral order
**Insight:** Four moving boundaries. Shrink one after each pass, and re-check before the two reverse passes.

```python
def spiralOrder(matrix):
    if not matrix:
        return []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                # *** re-check ***
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                # *** re-check ***
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out
```
**O(mn) / O(1)** extra — **Gotcha:** the two re-checks. A single-row or single-column remainder double-counts without them.

---

---

### 48. Rotate Image
**Insight:** Transpose, then reverse each row. Two simple passes beat index arithmetic.

```python
def rotate(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):        # c starts at r+1, not 0
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()
```
**O(n²) / O(1)** — **Gotcha:** `range(r+1, n)`. Starting at 0 transposes twice and undoes itself.

---

---

### 73. Set Matrix Zeroes
**Insight:** Use the first row and first column as the marker storage. Handle their own state with two separate flags.

```python
def setZeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))

    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0
```
**O(mn) / O(1)** — the O(m+n) set-based version is fine too; the O(1) one is the follow-up.

---

---

### 189. Rotate Array
**Insight:** Reverse the whole array, then reverse the two pieces.

```python
def rotate(nums, k):
    n = len(nums)
    k %= n                               # k can exceed n
    def rev(lo, hi):
        while lo < hi:
            nums[lo], nums[hi] = nums[hi], nums[lo]
            lo += 1
            hi -= 1
    rev(0, n - 1)
    rev(0, k - 1)
    rev(k, n - 1)
```
**O(n) / O(1)**

---

---

### 287. Find the Duplicate Number
**Insight:** Treat values as pointers — `i → nums[i]`. A duplicate value means two nodes point to the same place, so the "linked list" has a cycle. Floyd's algorithm finds its entrance.

```python
def findDuplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
```
**O(n) / O(1)** — the constraints (no modification, O(1) space) are what force this. Say that; it shows you read them.

---

---

### 445. Add Two Numbers II
**Insight:** Digits are most-significant-first, so you can't walk forward. Push both onto stacks and build the result backwards.

```python
def addTwoNumbers(l1, l2):
    s1, s2 = [], []
    while l1:
        s1.append(l1.val); l1 = l1.next
    while l2:
        s2.append(l2.val); l2 = l2.next
    carry = 0
    head = None
    while s1 or s2 or carry:
        total = carry
        if s1: total += s1.pop()
        if s2: total += s2.pop()
        carry, digit = divmod(total, 10)
        node = ListNode(digit)
        node.next = head                 # prepend
        head = node
    return head
```
**O(m+n) / O(m+n)** — the follow-up is "without reversing"; stacks are the accepted answer.

---

---

### 179. Largest Number
**Insight:** Sort by the comparator "does `a+b` beat `b+a`?", not by numeric value.

```python
from functools import cmp_to_key
def largestNumber(nums):
    strs = list(map(str, nums))
    strs.sort(key=cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
    return '0' if strs[0] == '0' else ''.join(strs)
```
**O(n log n · L) / O(n)** — **Gotcha:** the all-zeros case returns `"0"`, not `"000"`.

---

---

### 1046. Last Stone Weight
```python
import heapq
def lastStoneWeight(stones):
    heap = [-s for s in stones]          # max-heap via negation
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)
        b = -heapq.heappop(heap)
        if a != b:
            heapq.heappush(heap, -(a - b))
    return -heap[0] if heap else 0
```
**O(n log n) / O(n)**

---
