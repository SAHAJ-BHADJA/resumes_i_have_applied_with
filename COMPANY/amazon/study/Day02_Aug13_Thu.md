# Thu Aug 13 — Day 2 of 18
### PHASE 1 — FOUNDATION · Two Pointers

**Answer key for reference: `Day1_KEY.md`** · Solutions for today's problems are at the bottom of this file.

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

Primitives **1, 2, 6, 7** — from memory now. Write the file, then **delete it**.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 12 failures.

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 125 | Valid Palindrome | Two pointers + skip | ____ |
| ☐ | 15 | 3Sum ★ (do twice) | Sort + two pointers | ____ |
| ☐ | 11 | Container With Most Water | Two pointers | ____ |
| ☐ | 88 | Merge Sorted Array | Fill from the back | ____ |
| ☐ | 977 | Squares of a Sorted Array | Two pointers | ____ |
| ☐ | 75 | Sort Colors | Dutch flag | ____ |
| ☐ | 167 | Two Sum II | Two pointers | ____ |
| ☐ | 42 | Trapping Rain Water ★★ (budget 60 min) | Two ways | ____ |

---

## Block D — Design

**LLD 1 — Parking Lot.** The canonical low-level design. Do it on paper first, *then* compare against anything.

Cover:
- **Classes:** `ParkingLot`, `Level`, `ParkingSpot`, `Vehicle` (+ subtypes), `Ticket`, `PricingStrategy`
- **Spot sizing:** motorcycle / compact / large — which vehicle fits which spot, and the fallback rules
- **Assignment:** how do you find a free spot in O(1) rather than scanning? (per-size free lists)
- **Pricing behind an interface** so hourly / flat / tiered swap without touching the caller — that's the Strategy pattern and the Open/Closed principle
- **Concurrency:** two cars arriving at the last spot simultaneously. What's your lock?
- **Entry/exit flow:** ticket issue, payment, spot release

Say the pattern names out loud as you use them.

---

## Block E — Leadership Principles

**Write LP stories #1 and #2.** Full STAR+ format, ~250 words each.

Targets: **Ownership** · **Deliver Results**

Format:
- **S**ituation — 2 sentences, context only
- **T**ask — what *you* owned. Not "we."
- **A**ction — 60% of the story. Your decisions, alternatives you rejected and why.
- **R**esult — **with a number.** "p99 from 800ms to 120ms." No number? Estimate and say "roughly."
- **+Learning** — what you'd do differently. Amazon probes this.

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

- [ ] 3Sum: did I get the dedup right at *both* the outer and inner level?
- [ ] Trapping Rain Water: can I explain why moving the shorter pointer is safe?
- [ ] Both stories end in a number?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 125. Valid Palindrome — Two pointers
**Trigger:** palindrome + ignore non-alphanumeric
**Insight:** Skip junk with inner `while` loops, don't pre-clean the string (interviewer wants O(1) space).

```python
def isPalindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        while lo < hi and not s[lo].isalnum():
            lo += 1
        while lo < hi and not s[hi].isalnum():
            hi -= 1
        if s[lo].lower() != s[hi].lower():
            return False
        lo += 1
        hi -= 1
    return True
```
**O(n) / O(1)** — **Gotcha:** the inner loops need `lo < hi` too, or you run off the end on `",."`.

---

---

### 15. 3Sum — Sort + two pointers  ★
**Trigger:** triplets summing to 0, no duplicates in output
**Insight:** Sort, fix `i`, then it's Two-Sum-on-sorted for the rest. Dedupe by skipping equal neighbours — **at both the outer and inner level.**

```python
def threeSum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                                # sorted: no way to reach 0
        if i > 0 and nums[i] == nums[i - 1]:
            continue                             # dedupe the fixed element
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                      # dedupe the pair
                hi -= 1
    return res
```
**O(n²) / O(1)** extra. **This is the #1 dedup-bug problem.** Do it twice.

---

---

### 11. Container With Most Water — Two pointers
**Trigger:** maximise area between two lines
**Insight:** Area is limited by the *shorter* wall. Moving the taller wall inward can never help — width shrinks and height is still capped by the short one. So always move the shorter pointer.

```python
def maxArea(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(height[lo], height[hi]))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best
```
**O(n) / O(1)** — say the "why moving the shorter one is safe" argument out loud; that's the whole interview.

---

---

### 88. Merge Sorted Array — Two pointers **from the back**
**Trigger:** merge in-place into nums1 which has trailing zeros
**Insight:** Filling from the front overwrites unread data. Fill from the **back**, where the space is already free.

```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:                        # only nums2 must be exhausted
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```
**O(m+n) / O(1)** — **Gotcha:** loop on `j >= 0` only. If nums1 runs out first, its remaining elements are already in place.

---

---

### 977. Squares of a Sorted Array — Two pointers
**Insight:** Largest square is at one of the two ends (negatives square big). Fill the output **backwards**.

```python
def sortedSquares(nums):
    n = len(nums)
    res = [0] * n
    lo, hi = 0, n - 1
    for k in range(n - 1, -1, -1):
        if abs(nums[lo]) > abs(nums[hi]):
            res[k] = nums[lo] ** 2
            lo += 1
        else:
            res[k] = nums[hi] ** 2
            hi -= 1
    return res
```
**O(n) / O(n)**

---

---

### 75. Sort Colors — Dutch national flag
```python
def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                    # do NOT advance mid — unknown value swapped in
        else:
            mid += 1
```
**O(n) / O(1)** — the "don't advance mid on the 2-case" line is the only bug in this problem.

---

---

### 167. Two Sum II (sorted)
```python
def twoSumII(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]      # 1-indexed
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []
```

---

## DAY 1 PATTERN TRIGGERS — memorise this table

| If the problem says... | Reach for |
|---|---|
| "pair / two numbers that sum to X", unsorted | hashmap of seen |
| same, but **sorted** | two pointers from ends |
| "triplet" / "quadruplet" | sort, fix one, two-pointer the rest |
| "group / categorise items that are equivalent" | hashmap with canonical key |
| "maximise area / container / distance" | two pointers, move the limiting side |
| "in-place merge with spare room at the end" | fill from the back |
| "count subarrays with sum = K" | prefix sum + hashmap, seed `{0:1}` |
| "longest consecutive / sequence in unsorted data" | set + only start at sequence heads |
| "trapped water / bounded by walls both sides" | two pointers or monotonic stack |

---

### 42. Trapping Rain Water — TWO WAYS ★★
**Trigger:** elevation map, trapped water
**Insight:** Water above index `i` = `min(maxLeft[i], maxRight[i]) - height[i]`. Everything else is how you compute those maxima.

**Way A — two pointers, O(1) space (the one to present):**
```python
def trap(height):
    if not height:
        return 0
    lo, hi = 0, len(height) - 1
    left_max, right_max = height[lo], height[hi]
    water = 0
    while lo < hi:
        if left_max < right_max:
            lo += 1
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]   # safe: right side guarantees a wall
        else:
            hi -= 1
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
    return water
```
**O(n) / O(1)**

**Way B — monotonic stack (present as the alternative):**
```python
def trap_stack(height):
    stack, water = [], 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break                     # no left wall
            left = stack[-1]
            width = i - left - 1
            depth = min(height[left], h) - height[bottom]
            water += width * depth
        stack.append(i)
    return water
```
**Key line to say:** "The stack version fills water *horizontally, layer by layer*; the two-pointer version fills it *vertically, column by column*."

---

## STRETCH

---
