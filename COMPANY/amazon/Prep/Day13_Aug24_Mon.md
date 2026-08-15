# Mon Aug 24 — Day 13 of 18
### PHASE 3 — ADVANCED + DESIGN · Binary Search (incl. binary search on the answer)

**Answer key for reference: `Day6_KEY.md`** · Solutions for today's problems are at the bottom of this file.

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Read only the *Trigger* and *Insight* lines below — never the code. Close it, keep going. At 20 min, read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

> **CONFIRMED: coding is on LiveCode — typed, on your own laptop. Not a whiteboard.**
> - **Code: type it.** You must be able to *run* it. Handwritten code you can't execute hides your bugs.
> - **Design: paper or whiteboard, always.** The in-person design round will put you at a board. Practise managing the space.
> - **No-backspace first pass.** Signature → return statement → fill the middle. Delete nothing until you reach the end, then fix. This is the commit-before-you-type discipline that stops the freeze.

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

Primitives **1, 2, and 3 — drill #3 hardest.** Binary search on the answer is the highest-yield sub-pattern of the month.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything flagged in yesterday's debrief, plus overdue items.

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **The recognition rule:** the problem says *"minimum X such that..."* or *"maximum X such that..."*, and you can write an O(n) `feasible(x)` check ⇒ **binary search the answer space, not the array.**
>
> **Write `feasible` on the board first, before the search.** 90% of the work is in that function; the search is boilerplate.
>
> **410 and 1011 are literally the same function.** Saying that out loud is worth more than the code.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 704 | Binary Search | Template | ____ |
| ☐ | 34 | First and Last Position | Two boundary searches | ____ |
| ☐ | 33 | Search in Rotated Sorted Array ★★ | One half is sorted | ____ |
| ☐ | 153 | Find Minimum in Rotated | Compare against hi | ____ |
| ☐ | 162 | Find Peak Element | Follow the ascent | ____ |
| ☐ | 240 | Search a 2D Matrix II | Staircase from top-right | ____ |
| ☐ | 875 | Koko Eating Bananas ★ | BS on answer | ____ |
| ☐ | 1011 | Capacity To Ship Packages ★ | BS on answer | ____ |
| ☐ | 1482 | Min Days to Make Bouquets | BS on answer | ____ |
| ☐ | 410 | Split Array Largest Sum ★ | BS on answer | ____ |
| ☐ | 1283 | Smallest Divisor Given Threshold | BS on answer | ____ |

---

## Block D — Design

**HLD 8 — Distributed Job Scheduler.**

Cover:
- **API:** submit job (with a schedule — cron or one-shot), cancel, query status
- **Storage:** the job store and how you find "what's due in the next minute" efficiently (time-bucketed index, not a full scan)
- **Leader election:** exactly one scheduler should dispatch a given job. ZooKeeper/etcd lease, or a DB-backed lock with a TTL.
- **Idempotency:** the dispatcher crashes after dispatching but before recording it. The job runs twice. Design so that's survivable — idempotency keys, or at-least-once + idempotent tasks.
- **Worker failure:** heartbeats, lease expiry, re-queue. How do you distinguish "worker is slow" from "worker is dead"?
- **Backpressure:** 10,000 jobs all scheduled for midnight. Jitter, rate limiting, priority queues.
- **Exactly-once is the interview trap.** The correct answer is "at-least-once delivery plus idempotent execution" — say it that way and you sound like someone who has operated one of these.

---

## Block E — Leadership Principles

**Rehearse the five stories that came out weakest yesterday.**

Rewrite any that:
- lack a number in the Result
- run over 2.5 minutes
- say "we" more than twice
- end without a concrete outcome

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

- [ ] Can I write the binary-search-on-answer template from memory in 60 seconds?
- [ ] Did I write `feasible()` first on every one of those five problems?
- [ ] (If whiteboard confirmed) did I write today's solutions by hand on paper?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 704. Binary Search
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

---

---

### 34. Find First and Last Position ★
**Insight:** Two boundary searches. Don't hand-roll — use the `lower_bound` primitive twice.
```python
import bisect
def searchRange(nums, target):
    left = bisect.bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect.bisect_right(nums, target) - 1
    return [left, right]
```
*Hand-rolled (if they ban `bisect`):*
```python
def searchRange_manual(nums, target):
    def bound(is_left):
        lo, hi, ans = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                ans = mid
                if is_left: hi = mid - 1     # keep going left
                else:       lo = mid + 1     # keep going right
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
    return [bound(True), bound(False)]
```
**O(log n) / O(1)**

---

---

### 33. Search in Rotated Sorted Array ★★
**Insight:** At any `mid`, **one half is always properly sorted.** Identify which, then test whether the target lies inside that sorted half.
```python
def searchRotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:            # LEFT half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                # RIGHT half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```
**O(log n) / O(1)** — **Gotcha:** `nums[lo] <= nums[mid]` with `<=`, for the 2-element case.

---

---

### 153. Find Minimum in Rotated Sorted Array
**Insight:** Compare `mid` against `hi`, never against `lo`.
```python
def findMin(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1                 # min is strictly right of mid
        else:
            hi = mid                     # mid could BE the min
    return nums[lo]
```
**O(log n) / O(1)** — comparing against `lo` breaks on a non-rotated array. Know why.

---

---

### 162. Find Peak Element
```python
def findPeakElement(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1                 # ascending -> a peak lies to the right
        else:
            hi = mid
    return lo
```
**O(log n) / O(1)** — works because `nums[-1] = nums[n] = -∞`, so an ascending slope must eventually turn.

---

---

### 240. Search a 2D Matrix II — staircase
**Insight:** Start at the **top-right**. That corner is the largest in its row and smallest in its column, so every comparison eliminates a whole row or column.
```python
def searchMatrix(matrix, target):
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        v = matrix[r][c]
        if v == target:
            return True
        elif v > target:
            c -= 1                       # eliminate this column
        else:
            r += 1                       # eliminate this row
    return False
```
**O(m+n) / O(1)**

---

## PART B — BINARY SEARCH ON THE ANSWER ★★★

*This is the highest-yield sub-pattern of the entire week. All four below are the same code.*

---

### 875. Koko Eating Bananas
```python
import math
def minEatingSpeed(piles, h):
    def hours_needed(speed):
        return sum(math.ceil(p / speed) for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:       # feasible
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**O(n log(max pile)) / O(1)** — say out loud: "answer space is 1 to max(piles); feasibility is monotonic because eating faster never takes more hours."

---

---

### 1011. Capacity To Ship Packages Within D Days
```python
def shipWithinDays(weights, days):
    def days_needed(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = 0
            cur += w
        return d

    lo, hi = max(weights), sum(weights)  # lo = must fit the heaviest item
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**Gotcha:** `lo = max(weights)`, not 1 — a capacity smaller than the largest package is impossible.

---

---

### 1482. Minimum Number of Days to Make m Bouquets
```python
def minDays(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1                        # state this guard first
    def can(day):
        bouquets = run = 0
        for b in bloomDay:
            if b <= day:
                run += 1
                if run == k:
                    bouquets += 1
                    run = 0
            else:
                run = 0                  # adjacency broken
        return bouquets >= m

    lo, hi = min(bloomDay), max(bloomDay)
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

---

### 410. Split Array Largest Sum
```python
def splitArray(nums, k):
    def pieces(limit):
        cnt, cur = 1, 0
        for x in nums:
            if cur + x > limit:
                cnt += 1
                cur = 0
            cur += x
        return cnt

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**Point out loud that 410 and 1011 are literally the same function.** That recognition is worth more than the code.

---

---

### 1283. Find the Smallest Divisor Given a Threshold
```python
import math
def smallestDivisor(nums, threshold):
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(math.ceil(x / mid) for x in nums) <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

## PART C — INTERVALS

---
