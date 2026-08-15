# Fri Aug 14 — Day 3 of 18
### PHASE 1 — FOUNDATION · Sliding Window

**Answer key for reference: `Day2_KEY.md`** · Solutions for today's problems are at the bottom of this file.

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

Primitives **4, 5, 22** + Tier 1 review.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 12 (+3d) and Aug 13 (+1d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **The universal sliding-window shape** — every problem today is this with a different `INVALID` test:
> ```
> for right in range(n):
>     add nums[right]
>     while window is INVALID:
>         remove nums[left]; left += 1
>     update answer
> ```
> **Longest → update after the while. Shortest → update inside the while.** That one distinction covers 90% of these.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 3 | Longest Substring Without Repeating ★★★ | The archetype | ____ |
| ☐ | 424 | Longest Repeating Character Replacement | Window + max_freq | ____ |
| ☐ | 209 | Minimum Size Subarray Sum | Shortest variant | ____ |
| ☐ | 438 | Find All Anagrams in a String | Fixed window | ____ |
| ☐ | 567 | Permutation in String | Fixed window | ____ |
| ☐ | 904 | Fruit Into Baskets | At most K distinct | ____ |
| ☐ | 1004 | Max Consecutive Ones III | At most K flips | ____ |

---

## Block D — Design

**HLD 1 — Rate Limiter / Throttling Service.**
*Every AWS service has one. High probability at your site.*

Cover:
- **Functional:** limit N requests per window, per API key / per customer / per IP
- **Algorithms and their trade-offs:** fixed window counter (boundary burst problem), sliding window log (memory), sliding window counter (the usual compromise), token bucket (allows bursts), leaky bucket (smooths output)
- **Distributed state:** the counter lives where? Redis? Per-host with a gossip sync? What's the accuracy/latency trade-off?
- **The key question they will ask: what happens when the counter store is unavailable?** Fail-open (let traffic through, risk overload) or fail-closed (reject, risk an outage)? *Say which and why — for a rate limiter in the data plane, fail-open is usually correct because the limiter must not become the thing that takes the service down.*
- **Response:** 429 plus `Retry-After`; how the client should back off (exponential + jitter)
- Hot keys: one customer hammering a single partition

---

## Block E — Leadership Principles

**Write LP stories #3 and #4.**

Targets: **Customer Obsession** · **Dive Deep**

For Customer Obsession, the strongest shape is: *you pushed back on an internal preference (a deadline, a design your team liked, a shortcut) because it would have hurt the user.*
For Dive Deep: *a bug nobody could find — how you instrumented it, what you measured, how you root-caused it.* Include the actual numbers you looked at.

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

- [ ] Can I write problem 3 from a blank page in under 5 minutes?
- [ ] Can I state, out loud, why sliding window fails when the array has negatives?
- [ ] Rate limiter: did I pick fail-open or fail-closed and can I defend it?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 3. Longest Substring Without Repeating Characters — the archetype ★★★
**Trigger:** longest substring with all-distinct characters
**Insight:** Window is invalid when a char appears twice. Shrink from the left until it doesn't.

```python
def lengthOfLongestSubstring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1          # jump left past the previous occurrence
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```
**O(n) / O(min(n, charset))**
**Gotcha:** the `last[ch] >= left` check. Without it, a stale occurrence *outside* the window drags `left` backwards.

*Count-map variant (closer to the universal template — know both):*
```python
def lengthOfLongestSubstring_v2(s):
    from collections import defaultdict
    count = defaultdict(int)
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while count[ch] > 1:             # INVALID
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

---

### 424. Longest Repeating Character Replacement ★
**Trigger:** longest substring after changing at most k characters
**Insight:** A window is valid if `window_length - count_of_most_frequent_char <= k`. Those are the chars you'd have to replace.

```python
from collections import defaultdict
def characterReplacement(s, k):
    count = defaultdict(int)
    left = best = max_freq = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:     # INVALID
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```
**O(n) / O(26)**
**The famous subtlety:** `max_freq` is never decreased. That's *intentional* — a stale `max_freq` only makes the window fail to grow, never produce a wrong answer, and the final answer is still correct. Be ready to defend this; interviewers probe it.

---

---

### 209. Minimum Size Subarray Sum — "shortest" variant
**Insight:** Shortest ⇒ update the answer **inside** the shrink loop.

```python
def minSubArrayLen(target, nums):
    left = 0
    total = 0
    best = float('inf')
    for right, x in enumerate(nums):
        total += x
        while total >= target:                       # VALID -> try to shrink
            best = min(best, right - left + 1)       # update INSIDE
            total -= nums[left]
            left += 1
    return 0 if best == float('inf') else best
```
**O(n) / O(1)** — only works because all values are positive. Say that out loud.

---

---

### 438. Find All Anagrams in a String — fixed window
```python
from collections import Counter
def findAnagrams(s, p):
    if len(p) > len(s):
        return []
    need = Counter(p)
    window = Counter(s[:len(p)])
    res = [0] if window == need else []
    for i in range(len(p), len(s)):
        window[s[i]] += 1
        window[s[i - len(p)]] -= 1
        if window[s[i - len(p)]] == 0:
            del window[s[i - len(p)]]    # *** must delete, or == comparison fails ***
        if window == need:
            res.append(i - len(p) + 1)
    return res
```
**O(n) / O(26)** — **Gotcha:** deleting zero-count keys. `Counter({'a':1,'b':0}) != Counter({'a':1})`.

---

---

### 567. Permutation in String — same shape, boolean answer
```python
from collections import Counter
def checkInclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True
    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        out = s2[i - len(s1)]
        window[out] -= 1
        if window[out] == 0:
            del window[out]
        if window == need:
            return True
    return False
```
**O(n) / O(26)** — this is 438 with early return. Point that out; it reads as pattern recognition.

---

---

### 904. Fruit Into Baskets — at most 2 distinct
```python
from collections import defaultdict
def totalFruit(fruits):
    count = defaultdict(int)
    left = best = 0
    for right, f in enumerate(fruits):
        count[f] += 1
        while len(count) > 2:            # INVALID
            count[fruits[left]] -= 1
            if count[fruits[left]] == 0:
                del count[fruits[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```
**O(n) / O(1)** — generalises to "longest substring with at most K distinct." Say that.

---

---

### 1004. Max Consecutive Ones III
**Insight:** "Flip at most k zeros" = "longest window containing at most k zeros."

```python
def longestOnes(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:                 # INVALID
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```
**O(n) / O(1)**

---

---
