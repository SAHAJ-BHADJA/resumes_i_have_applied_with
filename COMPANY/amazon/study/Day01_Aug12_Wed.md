# Wed Aug 12 — Day 1 of 18
### PHASE 1 — FOUNDATION · Setup + Arrays & Hashing

**Answer key for reference: `Day1_KEY.md`** · Solutions for today's problems are at the bottom of this file.

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Read only the *Trigger* and *Insight* lines below — never the code. Close it, keep going. At 20 min, read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

---

### ⚠ SETUP — do this before any problem (45 min)

- [ ] **Disable Copilot and IntelliSense.** Open a plain text editor. Takes 5 minutes, non-negotiable.
- [ ] Print the **Round Script** (`Amazon_8_Day_Plan.md`, Part 2). Tape it above your desk.
- [ ] Create two files: `resolve_queue.md` and `pattern_journal.md`.
- [ ] **Email your recruiter today.** Three questions:
  1. *"Will the coding rounds be on a whiteboard or a laptop?"* — if whiteboard, you add handwritten practice from Aug 24.
  2. *"Which team is the loop for?"* — this re-weights your entire design prep.
  3. *"Can you confirm the level and round structure?"* — SDE-1 loops lean LLD; SDE-2+ lean HLD.

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

Primitives **1, 2, 6**. *Reference allowed today only* — this is the one day you may look. Time each one.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Nothing yet. Queue starts empty.

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 1 | Two Sum | Hashmap | ____ |
| ☐ | 242 | Valid Anagram | Counting | ____ |
| ☐ | 217 | Contains Duplicate | Set | ____ |
| ☐ | 49 | Group Anagrams | Canonical key | ____ |
| ☐ | 128 | Longest Consecutive Sequence | Set + sequence heads | ____ |
| ☐ | 238 | Product of Array Except Self | Prefix/suffix | ____ |
| ☐ | 560 | Subarray Sum Equals K | Prefix sum + hashmap | ____ |

---

## Block D — Design

**No design work today — absorb the framework instead.**

- [ ] Read all **16 Leadership Principles** slowly, once.
- [ ] Read Part 5 of `Amazon_8_Day_Plan.md` (the design framework and the Herndon-specific notes).
- [ ] Learn two phrases you'll use all month: **control plane vs data plane**, and **blast radius**.

---

## Block E — Leadership Principles

**LP brain dump — no stories yet.**

One page, ~20 raw bullets from your career. Don't write prose. Just list:
- Bugs you fixed that nobody else could
- Deadlines you hit, and what you cut to hit them
- Times you disagreed with your manager or team
- Things that failed
- Things you shipped
- Times you pushed back for the user

This raw list feeds every story you write for the next two weeks. Aim for 20 items; 12 is a floor.

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

- [ ] Can I type primitives 1, 2, 6 without looking? *(If no, drill them 3× now.)*
- [ ] Did I narrate out loud on every problem, or did I go silent?
- [ ] Recruiter email sent?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 1. Two Sum — Hashmap
**Trigger:** find a pair summing to target, unsorted, return indices
**Insight:** For each `x`, the partner is `target - x`. Store what you've *already seen*, so you never match an element with itself.

```python
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```
**O(n) / O(n)** — **Gotcha:** check `seen` *before* inserting `x`, or `[3,3]` with target 6 breaks.

---

---

### 242. Valid Anagram — Counting
**Trigger:** same characters, different order
**Insight:** Two strings are anagrams iff their character counts match.

```python
from collections import Counter
def isAnagram(s, t):
    return len(s) == len(t) and Counter(s) == Counter(t)
```
**O(n) / O(1)** (26 letters). **Follow-up they will ask:** Unicode? Then the dict is O(k) not O(1).

---

---

### 217. Contains Duplicate — Set
```python
def containsDuplicate(nums):
    return len(set(nums)) != len(nums)
```
**O(n) / O(n)** — say out loud: "O(1) space alternative is sorting first, at O(n log n) time."

---

---

### 49. Group Anagrams — Hashmap with canonical key
**Trigger:** group items that are "the same" under some transformation
**Insight:** You need a *canonical form* as the dict key. Sorted string works; a 26-tuple count is faster.

```python
from collections import defaultdict
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = [0] * 26
        for ch in s:
            key[ord(ch) - ord('a')] += 1
        groups[tuple(key)].append(s)     # tuple because lists aren't hashable
    return list(groups.values())
```
**O(n·k) / O(n·k)** — sorted-key version is O(n·k log k).

---

---

### 128. Longest Consecutive Sequence — Set  ★
**Insight:** Only start counting from a number whose predecessor is absent. That makes it O(n), not O(n²).

```python
def longestConsecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:
            continue                     # not a sequence start — skip
        length = 1
        while x + length in s:
            length += 1
        best = max(best, length)
    return best
```
**O(n) / O(n)** — the `continue` is the entire trick. Without it you're O(n²).

---

---

### 238. Product of Array Except Self — Prefix/suffix
**Insight:** answer[i] = (product of everything left) × (product of everything right). Two passes, no division.

```python
def productExceptSelf(nums):
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res
```
**O(n) / O(1)** extra (output doesn't count).

---

---

### 560. Subarray Sum Equals K — Prefix sum + hashmap  ★★
**Insight:** `sum(i..j) = prefix[j] - prefix[i-1]`. So for each `j`, count how many earlier prefixes equal `prefix[j] - k`.

```python
from collections import defaultdict
def subarraySum(nums, k):
    count = defaultdict(int)
    count[0] = 1                         # the empty prefix
    running = total = 0
    for x in nums:
        running += x
        total += count[running - k]      # look up BEFORE inserting
        count[running] += 1
    return total
```
**O(n) / O(n)** — **Gotcha:** `count[0] = 1` handles subarrays starting at index 0. Forgetting it is the classic bug. Sliding window does **not** work here (negatives allowed).

---

---
