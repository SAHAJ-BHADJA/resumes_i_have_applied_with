# DAY 1 ANSWER KEY — Arrays, Hashing, Two Pointers

> Open only after your 25-min attempt. Read **Trigger** and **Insight** first; look at code last.

---

## CORE

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

### 217. Contains Duplicate — Set
```python
def containsDuplicate(nums):
    return len(set(nums)) != len(nums)
```
**O(n) / O(n)** — say out loud: "O(1) space alternative is sorting first, at O(n log n) time."

---

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
