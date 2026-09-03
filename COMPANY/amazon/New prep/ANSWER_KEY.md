# ANSWER KEY — Amazon prep, Aug 17 → Sept 1

*Every solution has been executed and asserted against real test cases, including the edge cases people actually fail on.*


> **Open this only after your 25-minute attempt has expired, or after your code runs.**
> Read the **Trigger** and **Insight** lines first; the code last. Dropping straight to the code is the rep that doesn't count.


---

## Index

- **DAY 1 — Mon Aug 17** · Setup · Arrays, Hashing & Two Pointers
  1, 49, 128, 238, 560, 41, 15, 11, 42 · Common Manager, Friends Purchases
- **DAY 2 — Tue Aug 18** · Sliding Window & Prefix Sum
  3, 424, 209, 438, 567, 76, 992, 1658, 239, 974, 525 · Destination Cache, Top Customers
- **DAY 3 — Wed Aug 19** · Stacks, Monotonic Stacks & Linked Lists
  20, 155, 150, 394, 739, 735, 84, 206, 21, 142, 19, 143, 138, 148 · VM Load, Block Words
- **DAY 4 — Thu Aug 20** · Trees
  104, 110, 543, 102, 199, 662, 124, 98, 230, 105, 236, 297, 863, 437 · Tree Kyoukai, Employee Directory
- **DAY 5 — Fri Aug 21** · Grids & Backtracking
  200, 695, 130, 417, 994, 79, 78, 46, 39, 22, 212 · Gold Thief, XO Game
- **DAY 6 — Sat Aug 22** · Graphs  *(weekend — full track)*
  207, 210, 133, 547, 721, 127, 399, 684, 802, 310, 752, 787, 542 · Conversion Rate, Friendship Path
- **DAY 8 — Mon Aug 24** · Heaps & Top-K
  215, 347, 692, 23, 973, 295, 767, 621, 502, 1834, 378 · Bid Fulfillment, Minimum Possible Cost
- **DAY 9 — Tue Aug 25** · Binary Search (incl. binary search on the answer)
  704, 34, 33, 153, 162, 540, 74, 240, 875, 1011, 410, 1552, 528 · Inconvenience, Optimal Packing, Travel Time
- **DAY 10 — Wed Aug 26** · Intervals, Greedy & DP Part 1
  56, 57, 435, 253, 1288, 759, 55, 45, 134, 70, 198, 213, 322, 518 · Minimum Shipment, Minimize Absolute Differences, Permutation Sorter
- **DAY 11 — Thu Aug 27** · DP Part 2 & Design-in-Code
  139, 53, 152, 918, 300, 1143, 72, 416, 494, 62, 64, 146, 211, 380, 981, 588 · Binary String Errors, Warehouse Stock, Config Reconstruction
- **DAY 12 — Fri Aug 28** · ★★ MOCK LOOP #2 + Weak-Spot Repair
   · Smart Processor, Sign In Pages, Faulty Server Detection, Count Discount Pairs

---


# ══════════════════════════════════
# DAY 1 — Mon Aug 17
# Setup · Arrays, Hashing & Two Pointers
# ══════════════════════════════════

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

### 41. First Missing Positive ★★
**Trigger:** smallest missing positive, O(n) time **and** O(1) space
**Insight:** The answer is in `[1, n+1]`. Use the array itself as a hash table — put value `v` at index `v-1` by cyclic swapping.

```python
def firstMissingPositive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            target = nums[i] - 1
            nums[i], nums[target] = nums[target], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
```
**O(n) / O(1)** — **Gotcha:** the swap condition is `nums[nums[i]-1] != nums[i]`, not `nums[i] != i+1`; otherwise duplicates loop forever.

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

### IDB16. Common Manager — ✅ Verified
**Prompt:** an org tree where each manager has zero or more direct reports. Given two employees, return their **lowest common manager**. Follow-up: generalise to `k` employees.

```python
class Employee:
    def __init__(self, name, reports=None):
        self.name = name
        self.reports = reports or []

def lowest_common_manager(top, a, b):
    def helper(node):
        """Returns (num_targets_found, lcm_or_None)."""
        if node is None:
            return 0, None
        found = 0
        for r in node.reports:
            cnt, res = helper(r)
            if res:
                return cnt, res                          # already resolved below
            found += cnt
        if node is a or node is b:
            found += 1
        return found, (node if found == 2 else None)
    return helper(top)[1]

def lowest_common_manager_k(top, targets):
    """Follow-up: k employees. Same shape, compare against len(targets)."""
    need = len(targets)
    tset = set(targets)
    def helper(node):
        if node is None:
            return 0, None
        found = 1 if node in tset else 0
        for r in node.reports:
            cnt, res = helper(r)
            if res:
                return cnt, res
            found += cnt
        return found, (node if found == need else None)
    return helper(top)[1]
```
**O(n) / O(h)** — this is LCA on an n-ary tree. **Ask whether parent pointers exist**; if they do, the two-pointer depth-walk is cleaner.

---

---

### IDB17. Friends Purchases — ✅ Verified
**Prompt:** given `getFriends(person)` and `getPurchases(person)`, return the most popular products among a user's friends. **Popularity = number of distinct friends who bought it**, not total quantity. Common variant: exclude products the user already owns.

```python
from collections import Counter
def friends_purchases(person, get_friends, get_purchases, k=None, exclude_own=True):
    own = set(get_purchases(person)) if exclude_own else set()
    counts = Counter()
    for friend in get_friends(person):
        for product in set(get_purchases(friend)):       # DISTINCT per friend
            if product not in own:
                counts[product] += 1
    ranked = sorted(counts, key=lambda p: (-counts[p], p))
    return ranked if k is None else ranked[:k]
```
**O(F·P log) / O(P)** — **the `set()` per friend is the entire question.** Buying a product three times still counts once. Follow-up: friends-of-friends via BFS to depth `d`.

---

---


# ══════════════════════════════════
# DAY 2 — Tue Aug 18
# Sliding Window & Prefix Sum
# ══════════════════════════════════

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

### 992. Subarrays with K Different Integers ★★
**Insight:** "Exactly K" isn't directly windowable. **`exactly(K) = atMost(K) − atMost(K−1)`.** Memorise this identity — it converts a whole family of problems into standard windows.

```python
from collections import defaultdict
def subarraysWithKDistinct(nums, k):
    def at_most(limit):
        count = defaultdict(int)
        left = total = 0
        for right, x in enumerate(nums):
            count[x] += 1
            while len(count) > limit:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            total += right - left + 1    # all windows ending at `right`
        return total
    return at_most(k) - at_most(k - 1)
```
**O(n) / O(n)** — `total += right - left + 1` counts every valid subarray ending here. That line is reusable on its own.

---

---

### 1658. Minimum Operations to Reduce X to Zero ★
**Insight:** Removing a prefix and suffix summing to `x` ⟺ finding the **longest middle subarray** summing to `total − x`. Inversion turns it into a standard window.

```python
def minOperations(nums, x):
    target = sum(nums) - x
    if target < 0:
        return -1
    if target == 0:
        return len(nums)
    left = cur = 0
    best = -1
    for right, v in enumerate(nums):
        cur += v
        while cur > target and left <= right:
            cur -= nums[left]
            left += 1
        if cur == target:
            best = max(best, right - left + 1)
    return -1 if best == -1 else len(nums) - best
```
**O(n) / O(1)** — the inversion is the interview point. Say it out loud before coding.

---

---

### 239. Sliding Window Maximum ★★
**Trigger:** max of every window of size k
**Insight:** Monotonic **decreasing deque of indices**. The front is always the current max; anything smaller than the incoming value can never be a max again, so pop it.

```python
from collections import deque
def maxSlidingWindow(nums, k):
    dq = deque()                         # indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] < x:
            dq.pop()                     # smaller values are now useless
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                 # front slid out of the window
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```
**O(n) / O(k)** — each index enters and leaves once. **Gotcha:** evict the front *by index*, not by value.

---

---

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

---

### IDB28. Destination Cache — 🟠 LRU shape (title verified, prompt not recovered)
**Do not assume plain LRU** — "destination" may imply routing results with a TTL. Practise both. LRU is in `00_PRIMITIVES.py` #25; here is the TTL variant.

```python
from collections import OrderedDict
class DestinationCache:
    def __init__(self, capacity, ttl=None):
        self.cap = capacity
        self.ttl = ttl
        self.store = OrderedDict()                       # key -> (value, inserted_at)

    def get(self, key, now=0):
        if key not in self.store:
            return -1
        value, ts = self.store[key]
        if self.ttl is not None and now - ts > self.ttl:
            del self.store[key]
            return -1
        self.store.move_to_end(key)
        return value

    def put(self, key, value, now=0):
        if key in self.store:
            del self.store[key]
        self.store[key] = (value, now)
        if len(self.store) > self.cap:
            self.store.popitem(last=False)
```
**O(1) / O(capacity)** — be ready to hand-roll the doubly linked list instead of `OrderedDict`.

---

---

### IDB27. Top Customers — 🟡 Heap aggregation
**Prompt:** given transactions, return the top `k` customers by total spend, ties broken by customer id.

```python
import heapq
from collections import defaultdict
def top_customers(transactions, k):
    """transactions: [(customer_id, amount)]"""
    totals = defaultdict(int)
    for cid, amt in transactions:
        totals[cid] += amt
    return heapq.nsmallest(k, totals.items(), key=lambda p: (-p[1], p[0]))
```
**O(n + u log k) / O(u)** — the `(-total, id)` key gives spend-descending, id-ascending in one pass. Follow-up: streaming updates ⇒ keep a size-k min-heap.

---

---


# ══════════════════════════════════
# DAY 3 — Wed Aug 19
# Stacks, Monotonic Stacks & Linked Lists
# ══════════════════════════════════

### 20. Valid Parentheses
```python
def isValid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack                     # leftovers = unclosed
```
**O(n) / O(n)** — **Gotcha:** the `not stack` check before popping, and `return not stack` (not `True`).

---

---

### 155. Min Stack
**Insight:** Store the running min *alongside* each element. Then min is O(1) and pop needs no recomputation.

```python
class MinStack:
    def __init__(self):
        self.stack = []                  # (value, min_so_far)

    def push(self, val):
        cur_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, cur_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]
```
**All O(1) / O(n)** — mention the O(1)-amortised-space variant (a second stack that only pushes on new minima).

---

---

### 150. Evaluate Reverse Polish Notation
```python
def evalRPN(tokens):
    stack = []
    ops = {'+', '-', '*', '/'}
    for t in tokens:
        if t in ops:
            b = stack.pop()
            a = stack.pop()              # ORDER MATTERS: a op b
            if t == '+':   stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else:          stack.append(int(a / b))   # truncate toward ZERO
        else:
            stack.append(int(t))
    return stack[0]
```
**Gotcha:** `int(a/b)` not `a//b`. Python floor-divides toward −∞; the problem wants truncation toward 0. `-7//2 == -4`, but the answer is `-3`.

---

---

### 394. Decode String ★
**Trigger:** nested `k[substring]` expansion
**Insight:** On `[`, push the *state so far* (accumulated string + repeat count) and reset. On `]`, pop and combine.

```python
def decodeString(s):
    stack = []                           # (prev_string, repeat_count)
    cur = ""
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)     # multi-digit numbers
        elif ch == '[':
            stack.append((cur, num))
            cur, num = "", 0
        elif ch == ']':
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur
```
**O(output length) / O(depth)** — **Gotchas:** multi-digit `num`, and resetting *both* `cur` and `num` on `[`.

---

---

### 739. Daily Temperatures — monotonic stack
```python
def dailyTemperatures(temperatures):
    res = [0] * len(temperatures)
    stack = []                           # indices, decreasing temperatures
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j               # distance -> this is why we store indices
        stack.append(i)
    return res
```
**O(n) / O(n)** — each index is pushed and popped at most once. Say that when asked why it isn't O(n²).

---

---

### 735. Asteroid Collision ★
**Insight:** Only a positive (right-moving) on the stack meeting a negative (left-moving) incoming causes a collision. Everything else just gets pushed.

```python
def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()              # existing one explodes, keep checking
            elif stack[-1] == -a:
                stack.pop()              # both explode
                alive = False
            else:
                alive = False            # incoming explodes
        if alive:
            stack.append(a)
    return stack
```
**O(n) / O(n)** — **Gotcha:** the three-way comparison. Write the truth table on the board first; that's what the interviewer wants to see.

---

---

### 84. Largest Rectangle in Histogram ★★
**Insight:** For each bar, find how far left and right it can extend while staying the tallest. Increasing monotonic stack gives both boundaries.

```python
def largestRectangleArea(heights):
    stack = []                           # indices, increasing heights
    best = 0
    for i, h in enumerate(heights + [0]):    # sentinel flushes the stack
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best
```
**O(n) / O(n)** — the `+ [0]` sentinel is the trick that avoids a second cleanup loop. (Note `heights + [0]` makes a copy; `heights[stack[-1]]` still indexes the original safely because popped indices are always < len(heights).)

---

---

### 206. Reverse Linked List
```python
def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```
*Recursive version (know it, they sometimes ask):*
```python
def reverseList_rec(head):
    if not head or not head.next:
        return head
    new_head = reverseList_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

---

### 21. Merge Two Sorted Lists
```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
```

---

---

### 141 / 142. Linked List Cycle I & II ★
**Insight for 142 (why it works — be ready to prove it):** slow travels `k` to the cycle entry, meets fast after the cycle length relationship works out such that the distance from the meeting point to the entry equals the distance from head to the entry. So reset one pointer to head and advance both by 1.

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False

def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head                  # reset one to head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
```
**O(n) / O(1)**

---

---

### 19. Remove Nth Node From End
```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)            # dummy handles "remove the head"
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next
```
**O(n) / O(1)** — **without the dummy**, removing the head is a special case you will get wrong under pressure.

---

---

### 143. Reorder List ★
**Insight:** Three primitives composed: find middle → reverse second half → interleave.

```python
def reorderList(head):
    if not head or not head.next:
        return
    # 1. middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    # 2. reverse second half
    second = slow.next
    slow.next = None                     # cut
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    # 3. interleave
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
```
**O(n) / O(1)** — say "this is three known sub-routines" out loud; it's exactly the decomposition they're testing.

---

---

### 138. Copy List with Random Pointer ★★ (Amazon favourite)
**Way A — hashmap, O(n) space (lead with this):**
```python
def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}
    cur = head
    while cur:                           # pass 1: create all nodes
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                           # pass 2: wire the pointers
        old_to_new[cur].next = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next
    return old_to_new[head]
```
**Way B — interleaving, O(1) space (the follow-up they want):**
```python
def copyRandomList_O1(head):
    if not head:
        return None
    cur = head                           # 1. A -> A' -> B -> B'
    while cur:
        cur.next = Node(cur.val, cur.next)
        cur = cur.next.next
    cur = head                           # 2. set randoms
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    # 3. unweave
    old, new = head, head.next
    new_head = head.next
    while old:
        old.next = old.next.next
        new.next = new.next.next if new.next else None
        old, new = old.next, new.next
    return new_head
```
**Gotcha:** `.get(cur.next)` returns `None` gracefully; `old_to_new[cur.next]` would KeyError on the tail.

---

### 148. Sort List
**Insight:** Merge sort. Split with fast/slow, sort halves, merge with a dummy head.

```python
def sortList(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next         # fast starts ahead -> slow lands on 1st middle
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid = slow.next
    slow.next = None                     # cut
    left, right = sortList(head), sortList(mid)
    dummy = ListNode()
    tail = dummy
    while left and right:
        if left.val <= right.val:
            tail.next, left = left, left.next
        else:
            tail.next, right = right, right.next
        tail = tail.next
    tail.next = left or right
    return dummy.next
```
**O(n log n) / O(log n)** — **Gotcha:** `fast = head.next`. With `fast = head` the split never shrinks on 2 nodes and you recurse forever.

---

---

### IDB15. VM Load — ✅ Verified (pattern)
**Prompt:** route each request to the **least-loaded** server, breaking ties by lowest index. Return the target server per request (or the final loads).

```python
import heapq
def find_request_target(num_servers, requests):
    heap = [(0, i) for i in range(num_servers)]          # (load, index)
    heapq.heapify(heap)
    out = []
    for cost in requests:
        load, idx = heapq.heappop(heap)
        out.append(idx)
        heapq.heappush(heap, (load + cost, idx))
    return out
```
**O(n log k) / O(k)** — the tuple `(load, index)` gives the tie-break for free. Say that out loud.

---

---

### IDB29. Block Words — 🟡 Trie / Aho–Corasick
**Prompt:** given text and a list of blocked words, determine whether the text contains any blocked word.
**Clarify first:** substring vs whole-word matching, case sensitivity, punctuation. GPT's research confirmed the core but not these rules — and they change the algorithm.

```python
def has_blocked_word_tokens(text, blocked):
    """Whole-word matching, case-insensitive."""
    banned = {w.lower() for w in blocked}
    import re
    return any(tok in banned for tok in re.findall(r"[a-z0-9']+", text.lower()))

class BlockedTrie:
    """Substring matching over a large blocked set."""
    def __init__(self, words):
        self.root = {}
        for w in words:
            node = self.root
            for ch in w.lower():
                node = node.setdefault(ch, {})
            node['$'] = True

    def contains_any(self, text):
        t = text.lower()
        for i in range(len(t)):
            node = self.root
            for j in range(i, len(t)):
                if t[j] not in node:
                    break
                node = node[t[j]]
                if '$' in node:
                    return True
        return False
```
**Tokens O(n); Trie substring O(n·L)** — say "Aho–Corasick gives O(n + total) for many patterns"; that's the senior answer.

---


# ══════════════════════════════════
# DAY 4 — Thu Aug 20
# Trees
# ══════════════════════════════════

### 104. Maximum Depth (UP)
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```
**O(n) / O(h)**

---

---

### 110. Balanced Binary Tree (UP, with a sentinel)
**Insight:** Return height, but use `-1` as "already unbalanced" so you don't recompute heights — that's the difference between O(n) and O(n²).

```python
def isBalanced(root):
    def height(node):
        if not node:
            return 0
        lh = height(node.left)
        if lh == -1:
            return -1
        rh = height(node.right)
        if rh == -1:
            return -1
        if abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)
    return height(root) != -1
```
**O(n) / O(h)** — the naive version calls `maxDepth` inside `isBalanced` and is O(n²). Say that you avoided it.

---

---

### 543. Diameter of Binary Tree (UP, with a side-effect global)  ★
**Insight:** The classic "return one thing, track another." Return *height* upward; update the *diameter* as a side effect.

```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        best = max(best, lh + rh)        # path THROUGH this node
        return 1 + max(lh, rh)           # but only ONE side goes up
    height(root)
    return best
```
**O(n) / O(h)** — this shape (return one, track another) also solves 124. Recognise it.

---

---

### 102. Binary Tree Level Order Traversal
```python
from collections import deque
def levelOrder(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # snapshot size FIRST
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
```
**O(n) / O(width)** — `for _ in range(len(q))` is the only idea here. Everything else today reuses it.

---

---

### 199. Binary Tree Right Side View
```python
from collections import deque
def rightSideView(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:            # last node of the level
                out.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
    return out
```

---

---

### 662. Maximum Width of Binary Tree
**Insight:** Index nodes as in a heap: children of `i` are `2i` and `2i+1`. Width per level is `last − first + 1`.

```python
from collections import deque
def widthOfBinaryTree(root):
    if not root:
        return 0
    best = 0
    q = deque([(root, 0)])
    while q:
        _, first = q[0]
        last = first
        for _ in range(len(q)):
            node, idx = q.popleft()
            last = idx
            if node.left:
                q.append((node.left, 2 * idx))
            if node.right:
                q.append((node.right, 2 * idx + 1))
        best = max(best, last - first + 1)
    return best
```
**O(n) / O(width)** — normalising by `first` each level prevents index overflow in other languages. Mention it.

---

---

### 124. Binary Tree Maximum Path Sum ★★
**Same shape as 543:** return one thing, track another. Clamp negatives to 0.
```python
def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)   # drop negative branches
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)     # path through node
        return node.val + max(left, right)            # only one side goes up
    gain(root)
    return best
```
**O(n) / O(h)**

---

---

### 98. Validate BST (DOWN)  ★
**Insight:** Checking `left.val < node.val < right.val` locally is **wrong**. You must pass down the allowed range.

```python
def isValidBST(root):
    def check(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))
```
**O(n) / O(h)** — the classic failing test is `[5,4,6,null,null,3,7]`: 3 is a valid left child of 6 locally, but violates the ancestor 5.

---

---

### 230. Kth Smallest Element in a BST
**Insight:** Inorder traversal is sorted. Iterative version lets you stop early.

```python
def kthSmallest(root, k):
    stack = []
    cur = root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
    return -1
```
**O(h + k) / O(h)** — **follow-up:** frequent queries ⇒ store subtree sizes in each node for O(h) lookups.

---

---

### 105. Construct Binary Tree from Preorder + Inorder ★
**Insight:** Preorder gives you the root; inorder tells you how many nodes are on each side. Use an index map to avoid O(n) searches.

```python
def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    self_pos = 0

    def build(lo, hi):
        nonlocal self_pos
        if lo > hi:
            return None
        root_val = preorder[self_pos]
        self_pos += 1
        root = TreeNode(root_val)
        mid = idx[root_val]
        root.left = build(lo, mid - 1)   # LEFT FIRST — preorder consumes in that order
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(inorder) - 1)
```
**O(n) / O(n)** — **Gotcha:** left must be built before right, because the shared `self_pos` walks preorder in order.

---

### 236. LCA of a Binary Tree (UP) ★★ Amazon favourite
**Insight:** Return the node if you find p or q. If both subtrees return non-null, *this* node is the LCA.

```python
def lowestCommonAncestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root                      # p and q split here
    return left or right                 # both on one side (or neither)
```
**O(n) / O(h)** — do this one twice. Then be ready for "what if p or q might not exist?" (you'd need a found-count).

---

---

### 297. Serialize and Deserialize Binary Tree ★
**Insight:** Preorder with explicit null markers is uniquely decodable. Use an iterator so deserialize is a clean recursion.
```python
class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):
            if not node:
                out.append('#')
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(out)

    def deserialize(self, data):
        vals = iter(data.split(','))
        def build():
            v = next(vals)
            if v == '#':
                return None
            node = TreeNode(int(v))
            node.left = build()
            node.right = build()
            return node
        return build()
```
**O(n) / O(n)** — **null markers are mandatory.** Preorder alone is not uniquely decodable.

---

---

### 863. All Nodes Distance K in Binary Tree ★
**Insight:** A tree only has downward edges. Add parent pointers to make it an undirected **graph**, then plain BFS from target.
```python
from collections import deque, defaultdict
def distanceK(root, target, k):
    parent = {}
    def wire(node, par):
        if not node:
            return
        parent[node] = par
        wire(node.left, node)
        wire(node.right, node)
    wire(root, None)

    seen = {target}
    q = deque([target])
    dist = 0
    while q:
        if dist == k:
            return [n.val for n in q]
        for _ in range(len(q)):
            node = q.popleft()
            for nei in (node.left, node.right, parent[node]):
                if nei and nei not in seen:
                    seen.add(nei)
                    q.append(nei)
        dist += 1
    return []
```
**O(n) / O(n)** — "convert the tree to a graph" is a top-5 reusable trick.

---

---

### 437. Path Sum III ★
**Insight:** Prefix sums on a root-to-node path, in a hashmap, with backtracking on the way out.

```python
from collections import defaultdict
def pathSum(root, targetSum):
    count = defaultdict(int)
    count[0] = 1                         # empty prefix
    def dfs(node, running):
        if not node:
            return 0
        running += node.val
        total = count[running - targetSum]
        count[running] += 1
        total += dfs(node.left, running) + dfs(node.right, running)
        count[running] -= 1              # *** undo on the way out ***
        return total
    return dfs(root, 0)
```
**O(n) / O(h)** — the decrement is the backtracking step; without it, sibling subtrees contaminate each other.

---

---

### IDB20. Tree Kyoukai — 🟡 LeetCode 545 Boundary of Binary Tree
**Prompt:** return the tree boundary anticlockwise: root, then the left boundary top-down (excluding leaves), then all leaves left-to-right, then the right boundary bottom-up (excluding leaves). No node twice.

```python
def boundary_of_binary_tree(root):
    if not root:
        return []
    def is_leaf(n):
        return not n.left and not n.right
    out = [root.val] if not is_leaf(root) else [root.val]
    def left_bound(node):
        while node:
            if not is_leaf(node):
                out.append(node.val)
            node = node.left if node.left else node.right
    def leaves(node):
        if not node:
            return
        if is_leaf(node):
            out.append(node.val)
            return
        leaves(node.left)
        leaves(node.right)
    def right_bound(node):
        stack = []
        while node:
            if not is_leaf(node):
                stack.append(node.val)
            node = node.right if node.right else node.left
        out.extend(reversed(stack))
    if is_leaf(root):
        return out
    left_bound(root.left)
    leaves(root.left)
    leaves(root.right)
    right_bound(root.right)
    return out
```
**O(n) / O(h)** — **the three traps:** a single-node tree, excluding leaves from the boundaries, and reversing the right side.

---

---

### IDB26. Employee Directory — 🟡 Design
**Prompt:** model employees (`id`, `name`, `manager`, `directReports`) and support: lookup by id, prefix search by name, and "everyone beneath employee X."

```python
class Directory:
    def __init__(self):
        self.by_id = {}
        self.reports = {}                                # id -> [ids]

    def add(self, emp_id, name, manager_id=None):
        self.by_id[emp_id] = {'name': name, 'manager': manager_id}
        self.reports.setdefault(emp_id, [])
        if manager_id is not None:
            self.reports.setdefault(manager_id, []).append(emp_id)

    def get(self, emp_id):
        return self.by_id.get(emp_id)

    def search_by_prefix(self, prefix):
        return sorted(i for i, e in self.by_id.items()
                      if e['name'].startswith(prefix))

    def all_below(self, emp_id):
        out, stack = [], list(self.reports.get(emp_id, []))
        while stack:
            cur = stack.pop()
            out.append(cur)
            stack.extend(self.reports.get(cur, []))
        return sorted(out)

    def chain_to_top(self, emp_id):
        chain, cur = [], emp_id
        while cur is not None:
            chain.append(cur)
            cur = self.by_id[cur]['manager']
        return chain
```
**Follow-up to prepare:** swap the prefix scan for a **Trie** when the directory is large — that's the upgrade they're looking for.

---

---


# ══════════════════════════════════
# DAY 5 — Fri Aug 21
# Grids & Backtracking
# ══════════════════════════════════

### 200. Number of Islands ★★ (do both)
**DFS version:**
```python
def numIslands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != '1':
            return
        grid[r][c] = '0'                 # mark visited by mutating
        sink(r + 1, c); sink(r - 1, c)
        sink(r, c + 1); sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                sink(r, c)
    return count
```
**BFS version (mention this if the grid could be huge — avoids stack overflow):**
```python
from collections import deque
def numIslandsBFS(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1':
                continue
            count += 1
            q = deque([(r, c)])
            grid[r][c] = '0'
            while q:
                x, y = q.popleft()
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'   # mark ON ENQUEUE, not on dequeue
                        q.append((nx, ny))
    return count
```
**O(mn) / O(mn)** — **Gotcha:** mark visited when you *enqueue*, not when you dequeue, or you'll add duplicates.
**Always ask:** "May I modify the input grid?" If no, use a `visited` set.

---

---

### 695. Max Area of Island
```python
def maxAreaOfIsland(grid):
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)
    return max((dfs(r, c) for r in range(rows) for c in range(cols)), default=0)
```

---

---

### 130. Surrounded Regions ★
**Insight:** Inverted thinking. Don't find enclosed regions — find the ones touching the **border** and protect them. Everything else flips.

```python
def solve(board):
    if not board:
        return
    rows, cols = len(board), len(board[0])
    def mark(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != 'O':
            return
        board[r][c] = 'S'                # safe
        mark(r+1,c); mark(r-1,c); mark(r,c+1); mark(r,c-1)

    for r in range(rows):
        mark(r, 0); mark(r, cols - 1)
    for c in range(cols):
        mark(0, c); mark(rows - 1, c)

    for r in range(rows):
        for c in range(cols):
            board[r][c] = 'O' if board[r][c] == 'S' else 'X'
```
**"Start from the edges" is a reusable idea** — it also solves 417.

---

---

### 417. Pacific Atlantic Water Flow ★
**Insight:** Same inversion as 130. Don't simulate water flowing down from each cell — start at each ocean and walk **uphill**. Answer = intersection.

```python
def pacificAtlantic(heights):
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()

    def dfs(r, c, seen, prev_height):
        if (r, c) in seen or not (0 <= r < rows and 0 <= c < cols):
            return
        if heights[r][c] < prev_height:  # can't flow uphill
            return
        seen.add((r, c))
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(r + dr, c + dc, seen, heights[r][c])

    for c in range(cols):
        dfs(0, c, pac, 0)
        dfs(rows - 1, c, atl, 0)
    for r in range(rows):
        dfs(r, 0, pac, 0)
        dfs(r, cols - 1, atl, 0)
    return [list(x) for x in pac & atl]
```
**O(mn) / O(mn)**

---

### 994. Rotting Oranges ★★ Amazon favourite
**Insight:** Multi-source BFS. Seed the queue with **every** rotten orange at once; each BFS level = one minute.

```python
from collections import deque
def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0                         # nothing to rot -> 0, not -1

    minutes = 0
    while q and fresh:
        minutes += 1
        for _ in range(len(q)):          # one minute per level
            r, c = q.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
    return minutes if fresh == 0 else -1
```
**O(mn) / O(mn)** — **Gotchas:** the `fresh == 0` early return; and `while q and fresh` so you don't overcount the final minute.

---

---

### 79. Word Search
```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        tmp = board[r][c]
        board[r][c] = '#'                # mark for THIS path only
        found = (dfs(r+1,c,i+1) or dfs(r-1,c,i+1)
                 or dfs(r,c+1,i+1) or dfs(r,c-1,i+1))
        board[r][c] = tmp                # *** restore — this is backtracking ***
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```
**O(mn·4^L) / O(L)** — **Gotcha:** restoring the cell. Grid *counting* problems mark permanently; grid *path* problems must un-mark.

---

### 78. Subsets
```python
def subsets(nums):
    res, path = [], []
    def bt(start):
        res.append(path[:])              # COPY
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1)
            path.pop()
    bt(0)
    return res
```

---

### 46. Permutations
```python
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)
    def bt():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            bt()
            path.pop()
            used[i] = False
    bt()
    return res
```
**Permutations start the loop at 0 with a `used` array; combinations start at `start`.** That's the whole difference.

---

### 39. Combination Sum — reuse allowed
```python
def combinationSum(candidates, target):
    res, path = [], []
    candidates.sort()
    def bt(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                    # sorted -> prune the rest
            path.append(candidates[i])
            bt(i, remain - candidates[i])    # `i`, not `i+1` -> reuse
            path.pop()
    bt(0, target)
    return res
```

---

### 22. Generate Parentheses ★
**Insight:** Prune by counting, never by validating afterwards. Open if `open < n`; close only if `close < open`.
```python
def generateParenthesis(n):
    res = []
    def bt(s, open_count, close_count):
        if len(s) == 2 * n:
            res.append(s)
            return
        if open_count < n:
            bt(s + '(', open_count + 1, close_count)
        if close_count < open_count:
            bt(s + ')', open_count, close_count + 1)
    bt('', 0, 0)
    return res
```
**Catalan number of results.** "Prune during generation rather than filter afterwards" is the transferable idea.

---

### 212. Word Search II ★★
**Insight:** Build a Trie of the words, then DFS the board **once**, walking the Trie alongside. Prune finished branches.

```python
def findWords(board, words):
    trie = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = w                    # store the whole word at the end

    rows, cols = len(board), len(board[0])
    out = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node:
            return
        nxt = node[ch]
        word = nxt.pop('$', None)
        if word:
            out.append(word)             # found; removing '$' dedupes
        board[r][c] = '#'
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, nxt)
        board[r][c] = ch                 # restore
        if not nxt:
            node.pop(ch)                 # prune exhausted branch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie)
    return out
```
**O(mn·4^L) worst / O(total chars)** — **the pruning is what makes this pass.** Say it: without it you re-walk dead branches forever.

---

---

### IDB19. Gold Thief — 🟡 LeetCode 1219 Path with Maximum Gold
**Prompt:** grid where `0` is empty and positive values are gold. Start anywhere with gold, move 4-directionally, collect on visit, never revisit a cell, never step on `0`. Maximise gold collected.

```python
def get_maximum_gold(grid):
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == 0:
            return 0
        gold = grid[r][c]
        grid[r][c] = 0                                   # mark for THIS path
        best = max(dfs(r+1,c), dfs(r-1,c), dfs(r,c+1), dfs(r,c-1))
        grid[r][c] = gold                                # *** restore ***
        return gold + best
    return max((dfs(r, c) for r in range(rows) for c in range(cols)), default=0)
```
**O(mn·4^k) / O(k)** — backtracking, so the cell **must** be restored. This is Word Search's shape, not Number of Islands'.

---

---

### IDB21. XO Game — 🟡 LeetCode 348 Design Tic-Tac-Toe
**Prompt:** design an `n × n` tic-tac-toe. `move(row, col, player)` returns `0` (no winner), `1`, or `2`. Follow-up: **O(1) per move**, no board rescan.

```python
class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.rows = [0]*n
        self.cols = [0]*n
        self.diag = 0
        self.anti = 0

    def move(self, row, col, player):
        delta = 1 if player == 1 else -1
        self.rows[row] += delta
        self.cols[col] += delta
        if row == col:
            self.diag += delta
        if row + col == self.n - 1:
            self.anti += delta
        if self.n in (abs(self.rows[row]), abs(self.cols[col]),
                      abs(self.diag), abs(self.anti)):
            return player
        return 0
```
**O(1) per move / O(n)** — the +1/−1 counter trick is what they're testing. Lead with the O(n)-per-move version only if you're stuck.

---

---


# ══════════════════════════════════
# DAY 6 — Sat Aug 22
# Graphs  *(weekend — full track)*
# ══════════════════════════════════

### 207. Course Schedule (cycle detection) ★
```python
from collections import defaultdict, deque
def canFinish(numCourses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * numCourses
    for course, prereq in prerequisites:
        adj[prereq].append(course)       # prereq -> course
        indeg[course] += 1
    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    done = 0
    while q:
        node = q.popleft()
        done += 1
        for nei in adj[node]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                q.append(nei)
    return done == numCourses            # leftover nodes ⇒ cycle
```
**O(V+E) / O(V+E)** — **Gotcha:** get the edge direction right. `[a, b]` means "to take a you must first take b", so the edge is `b → a`.

---

---

### 210. Course Schedule II (the order itself)
```python
from collections import defaultdict, deque
def findOrder(numCourses, prerequisites):
    adj = defaultdict(list)
    indeg = [0] * numCourses
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        indeg[course] += 1
    q = deque([i for i in range(numCourses) if indeg[i] == 0])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in adj[node]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                q.append(nei)
    return order if len(order) == numCourses else []
```
Identical to 207 with the order recorded. Say that.

---

---

### 133. Clone Graph
**Insight:** Hashmap `old → new`, created *before* recursing, so cycles terminate.
```python
def cloneGraph(node):
    old_to_new = {}
    def dfs(cur):
        if not cur:
            return None
        if cur in old_to_new:
            return old_to_new[cur]       # cycle guard
        copy = Node(cur.val)
        old_to_new[cur] = copy           # register BEFORE recursing
        for nei in cur.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy
    return dfs(node)
```
**O(V+E) / O(V)** — registering before recursing is the whole problem.

---

---

### 547. Number of Provinces — Union-Find
```python
def findCircleNum(isConnected):
    n = len(isConnected)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    count = n
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j]:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj
                    count -= 1
    return count
```
**O(n²·α) / O(n)** — DFS also works; Union-Find is the better answer when they follow up with "now edges arrive as a stream."

---

---

### 721. Accounts Merge ★
**Insight:** Union accounts that share any email. Emails are the join key.
```python
from collections import defaultdict
def accountsMerge(accounts):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    email_to_name = {}
    for acc in accounts:
        name, emails = acc[0], acc[1:]
        for e in emails:
            email_to_name[e] = name
            union(emails[0], e)          # union all to the first email

    groups = defaultdict(list)
    for e in email_to_name:
        groups[find(e)].append(e)

    return [[email_to_name[emails[0]]] + sorted(emails)
            for emails in groups.values()]
```
**O(n·k·α + sorting) / O(n·k)**

---

---

### 127. Word Ladder ★★ Amazon favourite
**Insight:** Shortest transformation ⇒ BFS. The trick is generating neighbours in O(L·26) instead of comparing against all words.
```python
from collections import deque
def ladderLength(beginWord, endWord, wordList):
    words = set(wordList)
    if endWord not in words:
        return 0
    q = deque([(beginWord, 1)])
    seen = {beginWord}
    while q:
        word, steps = q.popleft()
        if word == endWord:
            return steps
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                cand = word[:i] + c + word[i+1:]
                if cand in words and cand not in seen:
                    seen.add(cand)       # mark on ENQUEUE
                    q.append((cand, steps + 1))
    return 0
```
**O(N·L·26) / O(N·L)** — mention **bidirectional BFS** as the optimisation; that's the follow-up.

---

---

### 399. Evaluate Division ★
**Insight:** A weighted graph. `a/b = 2` is an edge `a→b` with weight 2 and `b→a` with weight 0.5. Each query is a DFS multiplying edge weights.

```python
from collections import defaultdict
def calcEquation(equations, values, queries):
    graph = defaultdict(dict)
    for (a, b), v in zip(equations, values):
        graph[a][b] = v
        graph[b][a] = 1 / v

    def dfs(src, dst, seen):
        if src not in graph or dst not in graph:
            return -1.0
        if src == dst:
            return 1.0
        seen.add(src)
        for nei, w in graph[src].items():
            if nei in seen:
                continue
            sub = dfs(nei, dst, seen)
            if sub != -1.0:
                return w * sub
        return -1.0

    return [dfs(a, b, set()) for a, b in queries]
```
**O(Q·(V+E)) / O(V+E)** — Union-Find with weights is the optimisation; mention it.

---

---

### 684. Redundant Connection
**Insight:** Union-Find. The first edge whose endpoints already share a root is the answer.

```python
def findRedundantConnection(edges):
    parent = list(range(len(edges) + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
    return []
```
**O(n·α) / O(n)**

---

---

### 802. Find Eventual Safe States
**Insight:** A node is safe if every path from it leads to a terminal node. Reverse the graph and topologically sort from out-degree-zero nodes.

```python
from collections import deque, defaultdict
def eventualSafeNodes(graph):
    n = len(graph)
    rev = defaultdict(list)
    outdeg = [0] * n
    for u, nbrs in enumerate(graph):
        outdeg[u] = len(nbrs)
        for v in nbrs:
            rev[v].append(u)
    q = deque(u for u in range(n) if outdeg[u] == 0)
    safe = [False] * n
    while q:
        u = q.popleft()
        safe[u] = True
        for p in rev[u]:
            outdeg[p] -= 1
            if outdeg[p] == 0:
                q.append(p)
    return [u for u in range(n) if safe[u]]
```
**O(V+E) / O(V+E)** — "reverse the graph and topo-sort" is a reusable move.

---

---

### 310. Minimum Height Trees
**Insight:** Peel leaves layer by layer, like an onion. The last 1 or 2 nodes remaining are the centroids.

```python
from collections import deque
def findMinHeightTrees(n, edges):
    if n <= 2:
        return list(range(n))
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    leaves = deque(u for u in range(n) if len(adj[u]) == 1)
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        for _ in range(len(leaves)):
            leaf = leaves.popleft()
            nei = adj[leaf].pop()
            adj[nei].discard(leaf)
            if len(adj[nei]) == 1:
                leaves.append(nei)
    return list(leaves)
```
**O(V+E) / O(V+E)** — **at most 2 centroids**, always. Know why: a path graph has 1 or 2.

---

---

### 752. Open the Lock
**Insight:** Plain BFS over a 10,000-node state space. Deadends are just pre-marked visited.

```python
from collections import deque
def openLock(deadends, target):
    dead = set(deadends)
    if "0000" in dead:
        return -1
    if target == "0000":
        return 0
    q = deque([("0000", 0)])
    seen = {"0000"}
    while q:
        state, steps = q.popleft()
        for i in range(4):
            d = int(state[i])
            for nd in ((d + 1) % 10, (d - 1) % 10):
                nxt = state[:i] + str(nd) + state[i+1:]
                if nxt in dead or nxt in seen:
                    continue
                if nxt == target:
                    return steps + 1
                seen.add(nxt)
                q.append((nxt, steps + 1))
    return -1
```
**O(10⁴·4·2) / O(10⁴)** — bidirectional BFS is the follow-up.

---

---

### 787. Cheapest Flights Within K Stops ★
**Insight:** The K-stop cap breaks Dijkstra's greedy invariant. Use **Bellman-Ford**: exactly K+1 relaxation rounds.
```python
def findCheapestPrice(n, flights, src, dst, k):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):               # k stops = k+1 edges
        tmp = dist[:]                    # *** snapshot — critical ***
        for u, v, w in flights:
            if dist[u] != INF and dist[u] + w < tmp[v]:
                tmp[v] = dist[u] + w
        dist = tmp
    return dist[dst] if dist[dst] != INF else -1
```
**O(K·E) / O(V)** — **Gotcha:** the `tmp` copy. Without it, one round can use edges relaxed *in the same round*, letting you exceed K stops.

---

### 542. 01 Matrix — multi-source BFS
**Insight:** Seed the queue with all zeros. Distance from any zero = BFS level.
```python
from collections import deque
def updateMatrix(mat):
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
```
**O(mn) / O(mn)** — same shape as Rotting Oranges. Point out the similarity.

---

---

### IDB25. Conversion Rate — ✅ Verified (LeetCode 399 shape)
**Prompt:** given rates like `USD→EUR = 0.9`, answer arbitrary conversion queries by chaining. Reverse edges are reciprocals. Return `-1` when no path exists.

```python
from collections import defaultdict
def conversion_rate(rates, queries):
    """rates: [(from, to, rate)]"""
    graph = defaultdict(dict)
    for a, b, v in rates:
        graph[a][b] = v
        graph[b][a] = 1 / v
    def dfs(src, dst, seen):
        if src not in graph or dst not in graph:
            return -1.0
        if src == dst:
            return 1.0
        seen.add(src)
        for nei, w in graph[src].items():
            if nei in seen:
                continue
            sub = dfs(nei, dst, seen)
            if sub != -1.0:
                return w * sub
        return -1.0
    return [dfs(a, b, set()) for a, b in queries]
```
**O(Q·(V+E)) / O(V+E)** — weighted Union-Find is the "can you do better" answer.

---

---

### IDB18. Friendship Path — 🟡 BFS
**Prompt:** given friendships and two users, return the shortest chain connecting them.

```python
from collections import deque
def friendship_path(graph, start, end):
    if start == end:
        return [start]
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nei in graph.get(cur, []):
            if nei in prev:
                continue
            prev[nei] = cur
            if nei == end:
                path = [end]
                while path[-1] is not None and prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return path[::-1]
            q.append(nei)
    return []
```
**O(V+E) / O(V)** — BFS, not DFS: DFS gives *a* path, not the shortest.

---

---


# ══════════════════════════════════
# DAY 8 — Mon Aug 24
# Heaps & Top-K
# ══════════════════════════════════

### 215. Kth Largest Element ★
```python
import heapq
def findKthLargest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)             # evict smallest -> keeps k largest
    return h[0]
```
**O(n log k) / O(k)** — **say this:** "min-heap of size k for k *largest*. Also `heapq.nlargest(k, nums)[-1]`, or Quickselect for O(n) average."

---

---

### 347. Top K Frequent Elements
```python
import heapq
from collections import Counter
def topKFrequent(nums, k):
    count = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, count.items(), key=lambda p: p[1])]
```
**O(n log k) / O(n)** — the O(n) follow-up is **bucket sort** by frequency (buckets indexed 1..n). Mention it.

---

---

### 692. Top K Frequent Words ★ (Amazon favourite)
**Insight:** Tie-break is *lexicographically smaller first*, which is the **opposite** direction from frequency. Negate frequency so a single min-heap sorts both correctly.
```python
import heapq
from collections import Counter
def topKFrequentWords(words, k):
    count = Counter(words)
    heap = [(-freq, word) for word, freq in count.items()]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(k)]
```
**O(n + k log n) / O(n)** — the mixed sort direction is the entire difficulty. Explain it out loud.

---

---

### 23. Merge k Sorted Lists ★★
```python
import heapq
def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))   # i breaks val ties
    dummy = ListNode()
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```
**O(N log k) / O(k)** — **Gotcha:** the tiebreaker `i`. Without it Python tries to compare `ListNode` objects and raises TypeError. Alternative answer: divide-and-conquer pairwise merge, same complexity, O(1) extra.

---

---

### 973. K Closest Points to Origin ★ (Amazon favourite)
```python
import heapq
def kClosest(points, k):
    heap = []                            # max-heap of size k, by negative distance
    for x, y in points:
        d = x * x + y * y                # no sqrt needed — monotonic
        heapq.heappush(heap, (-d, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
```
**O(n log k) / O(k)** — **say this:** skipping `sqrt` is safe because it's monotonic. Mention Quickselect for O(n) average.

---

---

### 295. Find Median from Data Stream ★★
**Insight:** Two heaps. `small` is a max-heap (negated) of the lower half; `large` is a min-heap of the upper half. Keep `len(small)` equal to or one more than `len(large)`.
```python
import heapq
class MedianFinder:
    def __init__(self):
        self.small = []                  # max-heap (negated) — lower half
        self.large = []                  # min-heap — upper half

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        # ensure every element in small <= every element in large
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```
**add O(log n), find O(1)** — the push-to-small-then-move-to-large dance guarantees the ordering invariant without any comparison logic. Explain that.

---

### 767. Reorganize String ★ (Amazon favourite)
**Insight:** Always place the most frequent *available* character, but never the one you just placed. Hold it aside for one round.
```python
import heapq
from collections import Counter
def reorganizeString(s):
    count = Counter(s)
    if max(count.values()) > (len(s) + 1) // 2:
        return ""                        # impossible — state this check first
    heap = [(-freq, ch) for ch, freq in count.items()]
    heapq.heapify(heap)
    out = []
    prev = None
    while heap:
        freq, ch = heapq.heappop(heap)
        out.append(ch)
        if prev:
            heapq.heappush(heap, prev)   # release the held-back char
        freq += 1                        # freq is negative -> +1 decrements count
        prev = (freq, ch) if freq else None
    return ''.join(out)
```
**O(n log 26) / O(26)** — lead with the feasibility check `maxFreq <= (n+1)//2`; interviewers score that.

---

---

### 621. Task Scheduler ★ (Amazon favourite)
**Insight:** No simulation needed. The most frequent task builds a skeleton of `(maxFreq - 1)` gaps of size `n`, and other tasks fill them.
```python
from collections import Counter
def leastInterval(tasks, n):
    count = Counter(tasks)
    max_freq = max(count.values())
    num_max = sum(1 for v in count.values() if v == max_freq)
    slots = (max_freq - 1) * (n + 1) + num_max
    return max(slots, len(tasks))        # if plenty of variety, no idling
```
**O(n) / O(26)** — the `max(..., len(tasks))` clamp is what people miss. Draw the grid on the whiteboard: rows = max_freq, columns = n+1.

---

---

### 502. IPO ★
**Insight:** Two structures — a min-heap on capital (what's unlocked next) and a max-heap on profit (best available now).

```python
import heapq
def findMaximizedCapital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))
    available = []                       # max-heap of profits (negated)
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(available, -projects[i][1])
            i += 1
        if not available:
            break                        # nothing affordable
        w += -heapq.heappop(available)
    return w
```
**O(n log n) / O(n)**

---

---

### 1834. Single-Threaded CPU ★
**Insight:** Sort by enqueue time, then simulate with a heap keyed on `(processing_time, index)`. Jump the clock forward when idle.

```python
import heapq
def getOrder(tasks):
    indexed = sorted((t[0], t[1], i) for i, t in enumerate(tasks))
    heap = []
    out = []
    time = 0
    i = 0
    while len(out) < len(tasks):
        while i < len(indexed) and indexed[i][0] <= time:
            heapq.heappush(heap, (indexed[i][1], indexed[i][2]))
            i += 1
        if not heap:
            time = indexed[i][0]         # idle — jump to the next arrival
            continue
        dur, idx = heapq.heappop(heap)
        time += dur
        out.append(idx)
    return out
```
**O(n log n) / O(n)** — **Gotcha:** the idle jump. Without it you loop forever on gaps.

---

---

### 378. Kth Smallest Element in a Sorted Matrix
**Insight:** Binary search on the *value*, not the index. Count how many entries are ≤ mid using the staircase walk.

```python
def kthSmallest(matrix, k):
    n = len(matrix)
    def count_le(x):
        cnt = 0
        r, c = n - 1, 0                  # bottom-left staircase
        while r >= 0 and c < n:
            if matrix[r][c] <= x:
                cnt += r + 1             # whole column above counts
                c += 1
            else:
                r -= 1
        return cnt
    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**O(n log(max−min)) / O(1)** — binary search on the answer again. Point that out.

---

---

### IDB1. Bid Fulfillment — ✅ Verified
**Prompt:** Fixed `inventory` and a list of requests `[customerId, quantity, bid, timestamp]`. Higher bid gets priority. Within the same bid, allocate **round-robin in increasing timestamp**: each round gives one unit to every still-unfulfilled customer in that bid group. Drop a customer once fully fulfilled. Stop when inventory hits 0. Return the IDs of customers who received **zero** units, in original input order.
**Trap:** it is *not* "sort by bid and give the top customer everything." The equal-bid round-robin is the whole question.

```python
from collections import defaultdict
def bid_fulfillment(inventory, requests):
    groups = defaultdict(list)
    for cid, qty, bid, ts in requests:
        groups[bid].append((ts, cid, qty))
    received = defaultdict(int)
    for bid in sorted(groups, reverse=True):            # highest bid first
        active = sorted(groups[bid])                    # round-robin by timestamp
        while inventory > 0 and active:
            nxt = []
            for ts, cid, qty in active:
                if inventory == 0:
                    nxt.append((ts, cid, qty))
                    continue
                received[cid] += 1
                inventory -= 1
                if received[cid] < qty:
                    nxt.append((ts, cid, qty))
            active = nxt
        if inventory == 0:
            break
    return [cid for cid, _, _, _ in requests if received[cid] == 0]
```
**O(inventory + n log n) / O(n)** — the outer `while` gives one unit per customer per pass, so total work is bounded by units allocated.

---

---

### IDB8. Minimum Possible Cost — ✅ Verified
**Prompt:** `n` item types; the `j`-th unit bought of type `i` costs `a[i] + (j-1)*b[i]`. Buy exactly `m` items total, minimising cost.
**Insight:** greedy with a min-heap — always buy the globally cheapest next unit, then push that type's new next price.

```python
import heapq
def min_possible_cost(a, b, m):
    heap = [(a[i], i, 1) for i in range(len(a))]
    heapq.heapify(heap)
    total = 0
    for _ in range(m):
        cost, i, j = heapq.heappop(heap)
        total += cost
        heapq.heappush(heap, (a[i] + j * b[i], i, j + 1))
    return total
```
**O((n + m) log n) / O(n)** — example: `a=[2,1,1], b=[1,2,3], m=4 → 7`.

---

---


# ══════════════════════════════════
# DAY 9 — Tue Aug 25
# Binary Search (incl. binary search on the answer)
# ══════════════════════════════════

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

### 540. Single Element in a Sorted Array
**Insight:** Before the single element, pairs start at even indices. After it, they start at odd. Binary search that property.

```python
def singleNonDuplicate(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2 == 1:
            mid -= 1                     # snap to even
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2                 # single element is to the right
        else:
            hi = mid
    return nums[lo]
```
**O(log n) / O(1)**

---

---

### 74. Search a 2D Matrix
**Insight:** Fully sorted row-major ⇒ treat it as one flat array and binary search once.

```python
def searchMatrix(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // cols][mid % cols]
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```
**O(log(mn)) / O(1)** — **contrast with 240**, where rows aren't globally sorted so you need the staircase.

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

### 1552. Magnetic Force Between Two Balls
```python
def maxDistance(position, m):
    position.sort()
    def can_place(gap):
        count, last = 1, position[0]
        for p in position[1:]:
            if p - last >= gap:
                count += 1
                last = p
        return count >= m
    lo, hi = 1, position[-1] - position[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2         # *** +1: searching for the LARGEST ***
        if can_place(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```
**O(n log(range)) / O(1)** — **this is the "largest feasible" variant**: `mid = (lo+hi+1)//2` with `lo = mid`, or you infinite-loop. Know both directions.

---

---

### 528. Random Pick with Weight ★
**Insight:** Prefix sums plus a binary search on a uniform random draw.

```python
import random, bisect, itertools
class Solution:
    def __init__(self, w):
        self.prefix = list(itertools.accumulate(w))
        self.total = self.prefix[-1]

    def pickIndex(self):
        target = random.uniform(0, self.total)
        return bisect.bisect_left(self.prefix, target)
```
**init O(n), pick O(log n) / O(n)** — a very common Amazon design-flavoured question.

---

---

### IDB6. Inconvenience — ✅ Verified
**Prompt:** binary grid, `1` = service center. Distance is **Chebyshev**: `max(|dx|, |dy|)`. The grid's inconvenience is the maximum, over all `0` cells, of the distance to the nearest center. You may flip **at most one** `0` to `1`. Minimise inconvenience.
**Insight:** binary search the answer. For a candidate `d`, the cells still uncovered must all fit inside one Chebyshev ball of radius `d` — which is a rectangle test on their bounding box.

```python
from collections import deque
def min_inconvenience(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1]*cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dist[r][c] = 0
                q.append((r, c))
    if not q:
        return -1                                        # no centers at all
    while q:                                             # 8-dir BFS == Chebyshev
        r, c = q.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

    def feasible(d):
        bad = [(r, c) for r in range(rows) for c in range(cols) if dist[r][c] > d]
        if not bad:
            return True
        xs = [p[0] for p in bad]; ys = [p[1] for p in bad]
        lo_r, hi_r = max(xs) - d, min(xs) + d             # centre must sit here
        lo_c, hi_c = max(ys) - d, min(ys) + d
        return lo_r <= hi_r and lo_c <= hi_c and \
               max(lo_r, 0) <= min(hi_r, rows-1) and max(lo_c, 0) <= min(hi_c, cols-1)

    lo, hi = 0, max(max(row) for row in dist)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**O(mn log(mn)) / O(mn)** — example: `[[0,0,0,1],[0,0,0,1]] → 1`.

---

---

### IDB23. Optimal Packing — 🟡 LeetCode 1889 Minimum Space Wasted From Packaging
**Prompt:** choose a **single** supplier whose boxes fit all packages (each package in one box ≥ its size), minimising total wasted space. Return −1 if impossible, mod 1e9+7.
**Insight:** sort packages, prefix sums, then binary search each box size to find how many packages it absorbs.

```python
import bisect
def min_wasted_space(packages, boxes):
    MOD = 10**9 + 7
    packages.sort()
    n = len(packages)
    pref = [0]*(n+1)
    for i, p in enumerate(packages):
        pref[i+1] = pref[i] + p
    best = float('inf')
    for supplier in boxes:
        supplier.sort()
        if supplier[-1] < packages[-1]:
            continue                                     # can't fit the biggest
        waste = 0
        prev = 0
        for b in supplier:
            i = bisect.bisect_right(packages, b)
            waste += b * (i - prev) - (pref[i] - pref[prev])
            prev = i
        best = min(best, waste)
    return -1 if best == float('inf') else best % MOD
```
**O((n + m) log n) / O(n)** — **take the modulus only at the end**, or comparisons between suppliers break.

---

---

### IDB13. Travel Time — ✅ Verified (Chinese source)
**Prompt:** `m` hubs in a circle (hub 1 adjacent to hub `m`). `transitionTime[i]` is the travel time on the edge between hub `i+1` and hub `i+2` (wrapping). Start at hub 1 and visit `requestedHubs` **in order**, choosing clockwise or counter-clockwise per leg. Return minimum total time.
**Insight:** prefix sums round the circle. One direction is `|pref[b] − pref[a]|`; the other is `total − that`.

```python
def travel_time(m, transitionTime, requestedHubs):
    pref = [0] * (m + 1)
    for i in range(m):
        pref[i + 1] = pref[i] + transitionTime[i]
    total = pref[m]
    cur = 1
    ans = 0
    for dest in requestedHubs:
        one_way = abs(pref[dest - 1] - pref[cur - 1])
        ans += min(one_way, total - one_way)
        cur = dest
    return ans
```
**O(m + q) / O(m)** — example: `m=3, transitionTime=[3,2,1], requestedHubs=[1,3,3,2] → 3`.
**Clarify first:** which edge each `transitionTime[i]` refers to. Reports differ, and getting it wrong silently produces a plausible wrong answer.

---

---


# ══════════════════════════════════
# DAY 10 — Wed Aug 26
# Intervals, Greedy & DP Part 1
# ══════════════════════════════════

### 56. Merge Intervals ★★ (Amazon favourite)
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])   # sort by START
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)    # max! not just `end`
        else:
            out.append([start, end])
    return out
```
**O(n log n) / O(n)** — **Gotcha:** `max(out[-1][1], end)`. A fully-contained interval like `[1,10],[2,3]` breaks the naive version.

---

---

### 57. Insert Interval
**Insight:** Three phases: everything strictly before, the overlapping merge, everything strictly after.
```python
def insert(intervals, newInterval):
    out = []
    i, n = 0, len(intervals)
    start, end = newInterval

    while i < n and intervals[i][1] < start:      # entirely before
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:       # overlapping
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    while i < n:                                  # entirely after
        out.append(intervals[i])
        i += 1
    return out
```
**O(n) / O(n)** — no sort needed; input is already sorted.

---

---

### 435. Non-overlapping Intervals
**Insight:** Sort by **END**. Greedily keep the interval that finishes earliest — it leaves the most room. This is the classic activity-selection proof.
```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])   # sort by END
    kept = 0
    prev_end = float('-inf')
    for start, end in intervals:
        if start >= prev_end:
            kept += 1
            prev_end = end
    return len(intervals) - kept
```
**O(n log n) / O(1)** — **sort by end, not start.** This is the difference between correct and subtly wrong.

---

---

### 253. Meeting Rooms II ★★ (Amazon favourite)
**Way A — min-heap of end times (present this):**
```python
import heapq
def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []                            # end times of ongoing meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)          # a room freed up — reuse it
        heapq.heappush(heap, end)
    return len(heap)
```
**Way B — sweep line / chronological ordering (the elegant one):**
```python
def minMeetingRooms_sweep(intervals):
    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)
    rooms = best = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1
            best = max(best, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    return best
```
**O(n log n) / O(n)** — the heap version generalises better to follow-ups; the sweep is easier to explain.

---

---

### 1288. Remove Covered Intervals
**Insight:** Sort by start ascending, **end descending**. Then any interval whose end ≤ the running max end is covered.

```python
def removeCoveredIntervals(intervals):
    intervals.sort(key=lambda x: (x[0], -x[1]))
    count = 0
    prev_end = 0
    for _, end in intervals:
        if end > prev_end:
            count += 1
            prev_end = end
    return count
```
**O(n log n) / O(1)** — the `-x[1]` tiebreak is what handles equal starts correctly.

---

---

### 759. Employee Free Time ★
**Insight:** Flatten every interval, sort, then merge — the gaps between merged blocks are the free time.

```python
def employeeFreeTime(schedule):
    all_iv = sorted((iv[0], iv[1]) for emp in schedule for iv in emp)
    res = []
    cur_end = all_iv[0][1]
    for start, end in all_iv[1:]:
        if start > cur_end:
            res.append([cur_end, start]) # gap
            cur_end = end
        else:
            cur_end = max(cur_end, end)
    return res
```
**O(n log n) / O(n)** — the heap-based k-way merge is the "can you do better" answer.

---

---

### 55. Jump Game
```python
def canJump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False                 # unreachable
        reach = max(reach, i + x)
    return True
```
**O(n) / O(1)**

---

---

### 45. Jump Game II ★
**Insight:** This is BFS on an array. `cur_end` marks the boundary of the current "level"; crossing it costs one jump.
```python
def jump(nums):
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):       # stop before the last index
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                 # exhausted the current level
            jumps += 1
            cur_end = farthest
    return jumps
```
**O(n) / O(1)** — **Gotcha:** `range(len(nums) - 1)`. Including the last index adds a phantom jump.

---

---

### 134. Gas Station ★
**Insight:** If total gas ≥ total cost, a solution exists and is unique. If you run dry at station `i`, no station between the old start and `i` can work either — so jump the start to `i+1`.
```python
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1                # restart here
            tank = 0
    return start
```
**O(n) / O(1)** — the "why can't the start be in between?" argument is the actual interview question. Rehearse it.

---

---

### 70. Climbing Stairs
```python
def climbStairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```
**dp[i] = ways to reach step i = dp[i-1] + dp[i-2]** — it's Fibonacci. Say so.

---

---

### 198. House Robber ★
**dp[i] = max loot from houses 0..i = max(skip this house, rob it + dp[i-2])**
```python
def rob(nums):
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```
**O(n) / O(1)**

---

---

### 213. House Robber II — circular
**Insight:** First and last are adjacent, so you can't take both. Run the linear version twice: excluding the last, and excluding the first.
```python
def rob2(nums):
    if len(nums) == 1:
        return nums[0]
    def linear(arr):
        prev2, prev1 = 0, 0
        for x in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
    return max(linear(nums[:-1]), linear(nums[1:]))
```
"Reduce the circular case to two linear cases" is reusable.

---

---

### 322. Coin Change ★★
**dp[a] = fewest coins to make amount a.** Unbounded ⇒ iterate amounts outward.
```python
def coinChange(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]
```
**O(amount·len(coins)) / O(amount)** — greedy (always take the biggest coin) is **wrong**; be ready with the counterexample `coins=[1,3,4], amount=6` → greedy gives 3, DP gives 2.

---

---

### 518. Coin Change II — count combinations
**Insight:** The loop order encodes the answer. **Coins outside** ⇒ combinations. **Amount outside** ⇒ permutations.
```python
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:                      # coin loop OUTSIDE -> combinations
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
```
This loop-order distinction is a favourite follow-up. Know it cold.

---

---

### IDB9. Minimum Shipment — ✅ Verified
**Prompt:** `warehouses[i]` is the warehouse holding item `i`. Each shipment sends either two items **from different warehouses** or one item alone. Minimise shipments.
**Insight:** closed form. Let `f` = largest warehouse count, `n` = total. If `f > n − f` the surplus must ship alone, giving `f`. Otherwise everything pairs up: `ceil(n/2)`.

```python
from collections import Counter
def min_shipments(warehouses):
    n = len(warehouses)
    f = max(Counter(warehouses).values())
    return f if f > n - f else (n + 1) // 2
```
**O(n) / O(n)** — derive it out loud; don't just state it.

---

---

### IDB7. Minimize Absolute Differences — ✅ Verified
**Prompt:** arrays `a`, `b` of length `n`. Pair each `a[i]` with a distinct `b[j]`. Minimise `Σ |a[i] − b[π(i)]|`.
**Insight:** sort both and pair in order. The exchange argument: if `a1<a2` are paired to `b1>b2`, swapping never increases the sum.

```python
def minimize_abs_differences(a, b):
    return sum(abs(p - q) for p, q in zip(sorted(a), sorted(b)))
```
**O(n log n) / O(n)** — be ready to *prove* the exchange argument; that's the interview.

---

---

### IDB10. Permutation Sorter — ✅ Verified
**Prompt:** a permutation of `1..n`. Two operations: (1) reverse the whole array, (2) move the first element to the end. Minimum operations to sort ascending; input is guaranteed sortable.
**Insight:** the array must be a rotation of ascending or of descending. Only three shapes are reachable cheaply — check each.

```python
def permutation_sorter(nums):
    n = len(nums)
    asc = sorted(nums)
    desc = asc[::-1]
    best = float('inf')
    for k in range(n):                                   # k rotations
        rot = nums[k:] + nums[:k]
        if rot == asc:
            best = min(best, k)                          # rotations only
        if rot == desc:
            best = min(best, k + 1)                      # rotate then reverse
    rev = nums[::-1]
    for k in range(n):                                   # reverse first, then rotate
        if rev[k:] + rev[:k] == asc:
            best = min(best, 1 + k)
    return best if best < float('inf') else -1
```
**O(n²) as written / O(n)** — the O(n) version finds the single descent point instead of testing every rotation. Mention that.

---

---


# ══════════════════════════════════
# DAY 11 — Thu Aug 27
# DP Part 2 & Design-in-Code
# ══════════════════════════════════

### 139. Word Break ★
**dp[i] = can s[:i] be segmented?**
```python
def wordBreak(s, wordDict):
    words = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True                         # empty string is breakable
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[-1]
```
**O(n²·k) / O(n)**

---

---

### 53. Maximum Subarray — Kadane
**Insight:** At each element, either extend the previous subarray or start fresh here.
```python
def maxSubArray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)            # start fresh vs extend
        best = max(best, cur)
    return best
```
**O(n) / O(1)** — the divide-and-conquer O(n log n) version is the standard follow-up. Mention it exists.

---

---

### 152. Maximum Product Subarray ★
**Insight:** A negative flips min into max. Track **both** running extremes.
```python
def maxProduct(nums):
    best = cur_max = cur_min = nums[0]
    for x in nums[1:]:
        candidates = (x, cur_max * x, cur_min * x)
        cur_max, cur_min = max(candidates), min(candidates)
        best = max(best, cur_max)
    return best
```
**O(n) / O(1)** — **Gotcha:** compute both from the *old* values simultaneously. Updating `cur_max` first corrupts `cur_min`.

---

---

### 918. Maximum Sum Circular Subarray ★
**Insight:** Either the answer doesn't wrap (plain Kadane) or it does — and wrapping means the *complement* is a minimum subarray, so `total − minSum`. Guard the all-negative case.

```python
def maxSubarraySumCircular(nums):
    total = 0
    cur_max = best_max = nums[0]
    cur_min = best_min = nums[0]
    for i, x in enumerate(nums):
        total += x
        cur_max = x if i == 0 else max(x, cur_max + x)
        best_max = max(best_max, cur_max)
        cur_min = x if i == 0 else min(x, cur_min + x)
        best_min = min(best_min, cur_min)
    if best_max < 0:
        return best_max                  # all negative: wrapping would be empty
    return max(best_max, total - best_min)
```
**O(n) / O(1)** — the all-negative guard is the whole difficulty.

---

---

### 300. Longest Increasing Subsequence ★★
**O(n²) DP (lead with this):**
```python
def lengthOfLIS(nums):
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```
**O(n log n) patience sorting (the follow-up they want):**
```python
import bisect
def lengthOfLIS_fast(nums):
    tails = []                           # tails[k] = smallest tail of an LIS of length k+1
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```
**Important caveat to state:** `tails` is *not* a valid subsequence — only its **length** is meaningful.

---

### 1143. Longest Common Subsequence ★
```python
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1      # match -> diagonal
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```
**O(mn) / O(mn)** — the *shape* of all two-string DP. Learn this one and 72 comes free.

---

---

### 72. Edit Distance ★
```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                     # delete everything
    for j in range(n + 1):
        dp[0][j] = j                     # insert everything
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],      # delete
                                   dp[i][j-1],      # insert
                                   dp[i-1][j-1])    # replace
    return dp[m][n]
```
**Say which operation each of the three terms is.** That's what's being scored.

---

---

### 416. Partition Equal Subset Sum — 0/1 knapsack
```python
def canPartition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for a in range(target, x - 1, -1):       # BACKWARDS for 0/1
            dp[a] = dp[a] or dp[a - x]
    return dp[target]
```
**O(n·target) / O(target)** — **the backwards inner loop is what makes it 0/1 instead of unbounded.** Forwards = each item reusable. This distinction gets asked.

---

### 494. Target Sum
**Insight:** Assigning +/− signs ⟺ choosing a positive subset `P` where `sum(P) = (total + target) / 2`. That's subset-sum counting.

```python
def findTargetSumWays(nums, target):
    total = sum(nums)
    if (total + target) % 2 or abs(target) > total:
        return 0
    subset = (total + target) // 2
    dp = [0] * (subset + 1)
    dp[0] = 1
    for x in nums:
        for a in range(subset, x - 1, -1):    # backwards = 0/1
            dp[a] += dp[a - x]
    return dp[subset]
```
**O(n·subset) / O(subset)** — the parity guard rejects impossible targets.

---

---

### 62 / 63. Unique Paths (+ obstacles)
```python
def uniquePaths(m, n):
    row = [1] * n
    for _ in range(m - 1):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]

def uniquePathsWithObstacles(grid):
    n = len(grid[0])
    row = [0] * n
    row[0] = 1
    for r in range(len(grid)):
        for c in range(n):
            if grid[r][c] == 1:
                row[c] = 0               # blocked
            elif c > 0:
                row[c] += row[c - 1]
    return row[-1]
```
**O(mn) / O(n)** — the rolling-row optimisation is worth showing.

---

---

### 64. Minimum Path Sum
```python
def minPathSum(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for c in range(1, cols):
        dp[0][c] = dp[0][c-1] + grid[0][c]
    for r in range(1, rows):
        dp[r][0] = dp[r-1][0] + grid[r][0]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
    return dp[-1][-1]
```
**Always fill the base row and base column before the main loops.**

---

---

### 146. LRU Cache
**Trigger:** fixed-capacity cache, evict the least recently used
**Insight:** Hashmap gives O(1) lookup; doubly linked list gives O(1) reordering. Sentinel head and tail nodes remove every null check.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head = Node()               # most-recent side
        self.tail = Node()               # least-recent side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]        # *** node must store its key ***
```
**get/put O(1) / O(capacity)** — **Gotcha:** the node must carry its own `key`, or you can't delete it from the map on eviction. `OrderedDict` with `move_to_end` is the shortcut, but interviewers usually want the manual version.

---

---

### 211. Design Add and Search Words (with `.` wildcard) ★
**Insight:** `.` forces you to branch over all children — DFS instead of a linear walk.
```python
class WordDictionary:
    def __init__(self):
        self.root = {}                   # nested dicts; '$' marks end of word

    def addWord(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return '$' in node
            ch = word[i]
            if ch == '.':
                return any(dfs(child, i + 1)
                           for key, child in node.items() if key != '$')
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
```
**add O(L); search O(L) typical, O(26^L) worst with all wildcards.**

---

---

### 380. Insert Delete GetRandom O(1) ★
**Insight:** Array for O(1) random access, hashmap for O(1) lookup. To delete, **swap the target with the last element** so removal is O(1).
```python
import random
class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.idx = {}                    # value -> index in vals

    def insert(self, val):
        if val in self.idx:
            return False
        self.idx[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.idx:
            return False
        i = self.idx[val]
        last = self.vals[-1]
        self.vals[i] = last              # move last into the hole
        self.idx[last] = i
        self.vals.pop()
        del self.idx[val]
        return True

    def getRandom(self):
        return random.choice(self.vals)
```
**All O(1) / O(n)** — **Gotcha:** if `val` *is* the last element, order matters; this version is safe because `self.idx[last] = i` is then overwritten by `del self.idx[val]`... which removes it correctly since `last == val`. Walk that case out loud.

---

---

### 981. Time Based Key-Value Store ★
```python
import bisect
from collections import defaultdict
class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)   # key -> [(timestamp, value)] ascending

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        arr = self.store[key]
        i = bisect.bisect_right(arr, (timestamp, chr(127))) - 1
        return arr[i][1] if i >= 0 else ""
```
**set O(1), get O(log n)** — timestamps arrive strictly increasing, so the list is already sorted. Say that; it justifies skipping a sort.

---

---

### 588. Design In-Memory File System ★
```python
class FileSystem:
    def __init__(self):
        self.root = {}                   # dirs are dicts; files stored under '__content__'

    def _walk(self, path, create=False):
        node = self.root
        if path == '/':
            return node
        for part in path.split('/')[1:]:
            if part not in node:
                if not create:
                    return None
                node[part] = {}
            node = node[part]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node is None:
            return []
        if '__content__' in node:
            return [path.split('/')[-1]]     # it's a file
        return sorted(k for k in node if k != '__content__')

    def mkdir(self, path):
        self._walk(path, create=True)

    def addContentToFile(self, filePath, content):
        node = self._walk(filePath, create=True)
        node['__content__'] = node.get('__content__', '') + content

    def readContentFromFile(self, filePath):
        node = self._walk(filePath)
        return node.get('__content__', '') if node else ''
```
**ls O(k log k), others O(path length)** — nested dicts *are* a Trie. Say that; it connects two patterns.

---

---

### IDB2. Binary String Errors — ✅ Verified
**Prompt:** `errorString` of `0`,`1`,`!`; integers `x`,`y`. Replace every `!` with `0` or `1`. Each subsequence `01` costs `x`; each `10` costs `y`. Minimise total cost, mod 1e9+7.
**Insight (the whole problem):** the optimal assignment of the `!`s has **threshold structure** — all `0`s then all `1`s, or all `1`s then all `0`s. Among the `!`s themselves, mixing costs more. So enumerate the split point and evaluate in O(1) per step.

```python
MOD = 10**9 + 7
def min_errors(errorString, x, y):
    n = len(errorString)
    bangs = [i for i, c in enumerate(errorString) if c == '!']
    m = len(bangs)
    # fixed prefix/suffix counts
    f0b = [0]*(n+1); f1b = [0]*(n+1)
    for i, c in enumerate(errorString):
        f0b[i+1] = f0b[i] + (c == '0')
        f1b[i+1] = f1b[i] + (c == '1')
    tot0, tot1 = f0b[n], f1b[n]
    f0a = lambda p: tot0 - f0b[p+1]
    f1a = lambda p: tot1 - f1b[p+1]

    def base_cost(assign):
        """Full cost with '!' replaced per `assign` (list of chars)."""
        s = list(errorString)
        for r, i in enumerate(bangs):
            s[i] = assign[r]
        zeros = ones = 0
        cost = 0
        for c in s:
            if c == '1':
                cost += x * zeros
                ones += 1
            else:
                cost += y * ones
                zeros += 1
        return cost

    best = None
    # Arrangement A: ranks [0,t) -> '0', [t,m) -> '1'; sweep t from m down to 0
    cost = base_cost(['0']*m)
    best = cost
    for t in range(m, 0, -1):
        p = bangs[t-1]                                   # flip this one 0 -> 1
        zeros_before = f0b[p] + (t-1)                    # bangs before it are all '0'
        ones_before  = f1b[p]
        zeros_after  = f0a(p)                            # bangs after it are all '1'
        ones_after   = f1a(p) + (m - t)
        cost += x*zeros_before + y*zeros_after - y*ones_before - x*ones_after
        best = min(best, cost)
    # Arrangement B: ranks [0,t) -> '1', [t,m) -> '0'
    cost = base_cost(['1']*m)
    best = min(best, cost)
    for t in range(m, 0, -1):
        p = bangs[t-1]                                   # flip this one 1 -> 0
        zeros_before = f0b[p]
        ones_before  = f1b[p] + (t-1)
        zeros_after  = f0a(p) + (m - t)
        ones_after   = f1a(p)
        cost += y*ones_before + x*ones_after - x*zeros_before - y*zeros_after
        best = min(best, cost)
    return best % MOD
```
**O(n) / O(n)** — examples: `"101!1", x=2, y=3 → 9`; `"01!0", x=y=2 → 6`.

---

---

### IDB14. Warehouse Stock — ✅ Verified
**Prompt:** `stock[0..n-1]`, each either `-1` (missing) or a known value in `1..200`. Replace every `-1` with a value in `1..200` so that `a[0] <= a[1]`, `a[n-1] <= a[n-2]`, and `a[i] <= max(a[i-1], a[i+1])` for interior `i`. Count valid completions mod `998244353`.
**Insight:** the constraints say exactly **"no strict local maximum anywhere."** Sweep left to right with a two-state DP: state 1 = "this element is already satisfied because it's ≤ its left neighbour"; state 0 = "it still needs the next element to be ≥ it." Prefix sums make each step O(V).

```python
MOD2 = 998244353
V = 200
def warehouse_stock(stock):
    n = len(stock)
    if n == 1:
        return V if stock[0] == -1 else 1
    def allowed(i):
        return range(1, V + 1) if stock[i] == -1 else [stock[i]]
    dp0 = [0]*(V+2)                                      # needs next >= v
    dp1 = [0]*(V+2)                                      # already satisfied
    for v in allowed(0):
        dp0[v] = 1                                       # a[0] must be <= a[1]
    for i in range(1, n):
        # suffix sums of dp1, prefix sums of dp0/dp1
        suf1 = [0]*(V+2)
        for v in range(V, 0, -1):
            suf1[v] = (suf1[v+1] + dp1[v]) % MOD2
        pre0 = [0]*(V+2); pre1 = [0]*(V+2)
        for v in range(1, V+1):
            pre0[v] = (pre0[v-1] + dp0[v]) % MOD2
            pre1[v] = (pre1[v-1] + dp1[v]) % MOD2
        n0 = [0]*(V+2); n1 = [0]*(V+2)
        for w in allowed(i):
            # from state 0 we must have w >= v; satisfied only when w == v
            n1[w] = (dp0[w] + suf1[w]) % MOD2
            n0[w] = (pre0[w-1] + pre1[w-1]) % MOD2
        dp0, dp1 = n0, n1
    return sum(dp1[1:V+1]) % MOD2                        # last must be <= previous
```
**O(n·V) / O(V)** — examples: `[-1,-1] → 200`; `[1,-1,2] → 1`.

---

---

### IDB3. Config Reconstruction — ✅ Verified
**Prompt:** digit string `config`, integers `x`,`y`. Start `curr = 0`. Repeatedly add `x` or `y` to `curr` and append `curr % 10` to a generated string. Find the **shortest** generated string that contains `config` as a subsequence.
**Insight:** only `curr % 10` matters, so the state space is tiny — BFS over `(last_digit, matched_prefix_length)`, 10 × (len+1) states.

```python
from collections import deque
def config_reconstruction(config, x, y):
    target = len(config)
    start = (0, 0)                                      # (curr % 10, matched)
    q = deque([start])
    parent = {start: None}
    while q:
        d, j = q.popleft()
        for add in (x, y):
            nd = (d + add) % 10
            nj = j + 1 if j < target and config[j] == str(nd) else j
            state = (nd, nj)
            if state in parent:
                continue
            parent[state] = ((d, j), nd)
            if nj == target:
                out = []
                cur = state
                while parent[cur] is not None:
                    prev, digit = parent[cur]
                    out.append(str(digit))
                    cur = prev
                return ''.join(reversed(out))
            q.append(state)
    return ""
```
**O(10·len) / O(10·len)** — example: `config="27", x=2, y=3 → "247"`.

---

---


# ══════════════════════════════════
# DAY 12 — Fri Aug 28
# ★★ MOCK LOOP #2 + Weak-Spot Repair
# ══════════════════════════════════

### IDB12. Smart Processor — ✅ Verified
**Prompt:** array `arr` and a list of inclusive ranges `[l,r]`. In order, append `arr[l..r]` to a new array `efficient` (indices may repeat). For each original index `i`: efficiency is `0` if `i` was covered by any range; otherwise it's the count of elements in `efficient` **strictly less than** `arr[i]`. Return the sum.

```python
import bisect
def smart_processor(arr, ranges):
    n = len(arr)
    diff = [0] * (n + 1)
    efficient = []
    for l, r in ranges:
        diff[l] += 1
        diff[r + 1] -= 1
        efficient.extend(arr[l:r + 1])
    efficient.sort()
    covered = 0
    total = 0
    for i in range(n):
        covered += diff[i]
        if covered == 0:
            total += bisect.bisect_left(efficient, arr[i])
    return total
```
**O(E log E + n log E) / O(E)** — example: `arr=[1,2,3,2,4,5]`, ranges `[[0,1],[3,4],[0,0],[3,4]] → 12`.
**Gotcha:** coverage is a difference array; building a set of every covered index is fine here but doesn't scale if ranges are huge.

---

---

### IDB11. Sign In Pages — ✅ Verified
**Prompt:** process ordered auth requests. `register(user, pass)` fails if the user exists. `login(user, pass)` fails if the user doesn't exist, the password is wrong, or the user is already signed in. `logout(user)` fails if not signed in. Case-sensitive; store starts empty.

```python
def sign_in_pages(requests):
    users = {}
    active = set()
    out = []
    for req in requests:
        parts = req.split()
        action = parts[0]
        if action == 'register':
            _, u, p = parts
            if u in users:
                out.append("Registration Unsuccessful")
            else:
                users[u] = p
                out.append("Registered Successfully")
        elif action == 'login':
            _, u, p = parts
            if u not in users or users[u] != p or u in active:
                out.append("Login Unsuccessful")
            else:
                active.add(u)
                out.append("Logged In Successfully")
        else:                                            # logout
            _, u = parts
            if u in active:
                active.discard(u)
                out.append("Logged Out Successfully")
            else:
                out.append("Logout Unsuccessful")
    return out
```
**O(n) / O(users)** — **clarify the exact output strings and the already-signed-in rule before coding.** They vary between reports.

---

---

### IDB5. Faulty Server Detection — ✅ Verified
**Prompt:** chronological logs `"<server> <error|success>"`. Per server, `error` increments a consecutive-failure counter and `success` resets it. On reaching **3 consecutive errors** the server is replaced and its counter resets. Return total replacements.

```python
from collections import defaultdict
def count_faults(logs, threshold=3):
    streak = defaultdict(int)
    replacements = 0
    for line in logs:
        server, status = line.split()
        if status == 'error':
            streak[server] += 1
            if streak[server] == threshold:
                replacements += 1
                streak[server] = 0                       # replaced -> reset
        else:
            streak[server] = 0
    return replacements
```
**O(n) / O(servers)**

---

---

### IDB4. Count Discount Pairs — ✅ Verified
**Prompt:** array `prices`, integer `x`. Count index pairs `i < j` with `(prices[i] + prices[j]) % x == 0`.
**Insight:** bucket by remainder. Pair `r` with `x-r`; handle `r == 0` and `r == x/2` as self-pairs.

```python
def count_discount_pairs(prices, x):
    freq = [0] * x
    for p in prices:
        freq[p % x] += 1
    total = freq[0] * (freq[0] - 1) // 2
    for r in range(1, x // 2 + 1):
        c = x - r
        if r == c:
            total += freq[r] * (freq[r] - 1) // 2
        else:
            total += freq[r] * freq[c]
    return total
```
**O(n + x) / O(x)** — the O(n²) double loop is the thing you're being tested against.

---

---
