# DAY 2 ANSWER KEY — Sliding Window + Prefix Sum

> **The universal sliding-window shape.** Every problem today is this with a different `INVALID` test:
> ```
> for right in range(n):
>     add nums[right] to window
>     while window is INVALID:
>         remove nums[left]; left += 1
>     update answer          # <- for "longest"; for "shortest" update INSIDE the while
> ```
> **Longest → update after the while. Shortest → update inside the while.** That one distinction covers 90% of these.

---

## CORE

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

### 76. Minimum Window Substring — the boss ★★★
**Trigger:** smallest window in s containing all chars of t (with multiplicity)
**Insight:** Track `have` vs `need` as *counts of satisfied characters*, not raw char counts. That makes validity an O(1) check.

```python
from collections import Counter
def minWindow(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    need_count = len(need)               # distinct chars still to satisfy
    window = {}
    have = 0
    left = 0
    best_len = float('inf')
    best_start = 0

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1                    # this char just became satisfied

        while have == need_count:        # VALID -> shrink
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            out = s[left]
            window[out] -= 1
            if out in need and window[out] < need[out]:
                have -= 1                # broke it -> stop shrinking
            left += 1

    return "" if best_len == float('inf') else s[best_start:best_start + best_len]
```
**O(|s| + |t|) / O(|s| + |t|)**
**Gotchas:** (1) `== need[ch]` not `>=`, or you double-count. (2) `< need[out]` not `<=`. (3) Store `best_start` and slice at the end — don't build substrings inside the loop.

---

## STRETCH — Prefix Sum

### 974. Subarray Sums Divisible by K
**Insight:** `sum(i..j) % k == 0` ⟺ `prefix[j] % k == prefix[i-1] % k`. Count matching remainders.

```python
from collections import defaultdict
def subarraysDivByK(nums, k):
    count = defaultdict(int)
    count[0] = 1
    running = total = 0
    for x in nums:
        running = (running + x) % k      # Python's % is already non-negative
        total += count[running]
        count[running] += 1
    return total
```
**O(n) / O(k)** — in Java/C++ you must do `((r % k) + k) % k` for negatives. Mention it.

---

### 525. Contiguous Array — equal 0s and 1s
**Insight:** Map `0 → -1`. Then "equal counts" becomes "subarray sums to 0", i.e. two equal prefix sums.

```python
def findMaxLength(nums):
    first = {0: -1}                      # prefix 0 seen before index 0
    running = best = 0
    for i, x in enumerate(nums):
        running += 1 if x == 1 else -1
        if running in first:
            best = max(best, i - first[running])
        else:
            first[running] = i           # store EARLIEST index only
    return best
```
**O(n) / O(n)** — store only the first occurrence; that maximises length.

---

### 304. Range Sum Query 2D (Immutable)
**Insight:** 2D prefix sums with a 1-row/1-col pad so you never write boundary conditions.

```python
class NumMatrix:
    def __init__(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        self.pre = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self.pre[r + 1][c + 1] = (matrix[r][c]
                                          + self.pre[r][c + 1]
                                          + self.pre[r + 1][c]
                                          - self.pre[r][c])

    def sumRegion(self, r1, c1, r2, c2):
        P = self.pre
        return (P[r2 + 1][c2 + 1] - P[r1][c2 + 1]
                - P[r2 + 1][c1] + P[r1][c1])
```
**Build O(mn), query O(1)** — inclusion–exclusion. Draw the four rectangles when you explain it.

---

## DAY 2 PATTERN TRIGGERS

| If the problem says... | Reach for |
|---|---|
| "longest substring/subarray with [property]" | sliding window, update **after** the shrink |
| "shortest/minimum subarray with [property]" | sliding window, update **inside** the shrink |
| "at most K distinct / at most K flips" | window, invalid when count exceeds K |
| "exactly K distinct" | `atMost(K) - atMost(K-1)` — memorise this trick |
| "all permutations/anagrams of p in s" | fixed-size window + Counter equality |
| "count subarrays with sum = K", **negatives allowed** | prefix sum + hashmap — **window will not work** |
| "subarray divisible by K" | prefix sum modulo K |
| "equal number of X and Y" | map one to −1, then find sum-zero subarrays |
| repeated range-sum queries, no updates | precomputed prefix array |

**The single most common Day-2 mistake:** using a sliding window when the array contains negative numbers. Windows require monotonic growth/shrink of the running value. Negatives break that — switch to prefix sum + hashmap.
