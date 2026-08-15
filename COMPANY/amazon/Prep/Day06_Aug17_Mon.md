# Mon Aug 17 — Day 6 of 18
### PHASE 1 — FOUNDATION · ★ CONSOLIDATION #1 — no new patterns

**Answer key for reference: `all of Day1–Day3`** · Solutions for today's problems are at the bottom of this file.

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

**Reproduce all Tier 1 primitives (1–13) from memory, timed.** Anything you fumble, drill 3× immediately.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

**Clear the entire queue (90 min).** Everything overdue, cold, blank page.

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C

### Block C — MINI-MOCK (2h)

**One 60-minute round, simulated properly.**

- [ ] Pick **two problems you have not seen** from the pool at the bottom of this file. Don't look at the solutions.
- [ ] **Record yourself on your phone.** This is the part people skip and it's the part that works.
- [ ] Start with one LP question, answered out loud, before the coding.
- [ ] Full Round Script: clarify → examples → brute force → state approach → **ask "does that sound reasonable?"** → code → dry run → complexity → edge cases.

**Then watch the recording (25 min).** Note only three things:
1. Every silence longer than 20 seconds
2. Did you skip the dry run?
3. Did you start coding before you stated the approach?

Write those three answers down. They're your behaviour targets for Phase 2.

---

## Block D — Design

**HLD 3 — Object Storage (S3-like).**

Cover:
- **API:** `PUT /bucket/key`, `GET`, multipart upload (why it exists: a 5TB single PUT can't retry cheaply)
- **Metadata vs blob separation:** metadata in a strongly-consistent store, blobs on dumb cheap storage. Why they scale differently.
- **Durability:** erasure coding vs replication. Why 11 nines is a *math* claim, not a marketing one — walk through the arithmetic roughly.
- **Consistency:** read-after-write for new objects vs eventual for overwrites, and why overwrite is the hard case.
- **Partitioning:** key-prefix hot-spotting, and why randomised prefixes used to be advice.
- **Failure:** disk, host, rack, AZ. What's the blast radius of each?

---

## Block E — Leadership Principles

**Write LP stories #9 and #10.**

Targets: **Invent and Simplify** · **Earn Trust**

Invent and Simplify is best told as *removing* something — you deleted a service, collapsed three systems into one, cut a process. Adding a clever feature is a weaker version of this principle.
Earn Trust: *you were wrong publicly and owned it,* or *you delivered bad news early instead of hiding it.*

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

- [ ] All 13 Tier-1 primitives from memory, no reference?
- [ ] Re-solve queue empty?
- [ ] **Write down your three weakest patterns.** They get extra time in Phase 2. Be honest — this list is the most useful thing you produce today.


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
