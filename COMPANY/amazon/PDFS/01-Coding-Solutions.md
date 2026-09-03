# Coding Solution Pack — Amazon SDE-I (L4), Storage-Weighted

**How to read each entry**

- **Ask** — what the problem wants, in plain words.
- **S3 lens** — why a storage interviewer would reach for this. (Inference, not insider info.)
- **Idea in one breath** — the insight, stated so you could explain it to a non-programmer.
- **Algorithm** — numbered steps. Follow them literally and you get working code.
- **Code** — Python 3, interview-length.
- **Complexity** — time and space, with the bottleneck named.
- **Traps** — the edge case that fails you.
- **Follow-up they'll ask** — prepare the answer, it's free points.

`n` = input size unless stated otherwise.

---

## Contents

- [A. Arrays, Two Pointers, Prefix Sums](#a-arrays-two-pointers-prefix-sums) — 8
- [B. Sliding Window](#b-sliding-window) — 4
- [C. Hashing & Strings](#c-hashing--strings) — 5
- [D. Intervals](#d-intervals) — 4
- [E. Heaps & Top-K](#e-heaps--top-k) — 8
- [F. Binary Search (incl. on the answer)](#f-binary-search) — 4
- [G. Trees](#g-trees) — 7
- [H. Graphs](#h-graphs) — 8
- [I. Tries](#i-tries) — 4
- [J. Linked Lists](#j-linked-lists) — 5
- [K. Design Data Structures](#k-design-data-structures) — 7 ← *highest S3 signal*
- [L. Dynamic Programming](#l-dynamic-programming) — 8
- [M. Rapid-fire appendix](#m-rapid-fire-appendix) — 25 more

**72 fully worked solutions + 25 rapid-fire = 97 problems.**

---

# A. Arrays, Two Pointers, Prefix Sums

## A1. Two Sum — LC 1 · Easy

**Ask.** Given an array of numbers and a target, return the positions of the two numbers that add to the target.

**S3 lens.** Pure warm-up. Its real job is checking whether you reach for a hash map without being told.

**Idea in one breath.** Instead of checking every pair, remember every number you've already walked past. Then for each new number you only have to ask one question: "have I already seen the partner I need?"

**Algorithm.**
1. Make an empty dictionary mapping *value → index*.
2. Walk the array once, index `i`, value `x`.
3. Compute `need = target - x`.
4. If `need` is already a key in the dictionary, return `[dict[need], i]`.
5. Otherwise store `dict[x] = i` and keep going.

The reason you look up *before* inserting is that it stops an element from pairing with itself.

```python
def two_sum(nums, target):
    seen = {}                      # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []
```

**Complexity.** Time **O(n)** — one pass, each lookup O(1) average. Space **O(n)** for the dictionary.

**Traps.** Duplicates (`[3,3]`, target 6) — the look-before-insert order handles it. Don't sort; sorting destroys the original indices.

**Follow-up they'll ask.** *"What if the array were sorted and you couldn't use extra space?"* → Two pointers from both ends: if the sum is too big move `right` in, too small move `left` out. O(n) time, O(1) space.

---

## A2. Product of Array Except Self — LC 238 · Medium

**Ask.** For each position, return the product of every *other* element. No division allowed.

**S3 lens.** Tests whether you can decompose a problem into two directional passes — the same reflex used for prefix-checksum work.

**Idea in one breath.** Everything except me = (everything to my left) × (everything to my right). Compute those two running products in two sweeps.

**Algorithm.**
1. Create `out` of length n, filled with 1.
2. Left-to-right: keep a running `prefix = 1`. At each index i, set `out[i] = prefix`, then multiply `prefix *= nums[i]`. Now `out[i]` holds the product of everything left of i.
3. Right-to-left: keep a running `suffix = 1`. At each index i, do `out[i] *= suffix`, then `suffix *= nums[i]`.
4. Return `out`.

The trick is that you write into `out` *before* folding the current element into the running product — that's what excludes yourself.

```python
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]
    return out
```

**Complexity.** Time **O(n)** (two passes). Space **O(1)** extra — the output array doesn't count by convention. Say that out loud; it's the point of the problem.

**Traps.** Zeros. A naive "multiply everything then divide" breaks on a single zero and explodes on two. This approach handles both automatically — mention that you noticed.

**Follow-up.** *"Now allow division."* → Count zeros. Zero zeros: total product / nums[i]. One zero: only that index gets the product of the non-zeros, everything else is 0. Two or more: all zeros.

---

## A3. Trapping Rain Water — LC 42 · Hard

**Ask.** Given bar heights, how much water sits in the dips after rain?

**S3 lens.** The classic Amazon hard. It shows up because the two-pointer version requires a genuine invariant argument.

**Idea in one breath.** Water above any single bar is capped by the *shorter* of the tallest wall to its left and the tallest wall to its right. So walk in from both ends, and always advance the side whose wall is shorter — because that shorter side is the one deciding the water level.

**Algorithm.**
1. Pointers `l = 0`, `r = n-1`. Trackers `left_max = 0`, `right_max = 0`. `total = 0`.
2. While `l < r`:
   - If `height[l] < height[r]`: the left side is the binding constraint.
     - If `height[l] >= left_max`, update `left_max = height[l]` (this bar is a new wall, holds no water).
     - Else add `left_max - height[l]` to `total`.
     - `l += 1`.
   - Else do the mirror on the right with `right_max`, `r -= 1`.
3. Return `total`.

Why it's safe: if `height[l] < height[r]`, then there is *definitely* some wall on the right at least as tall as `height[r]`, so the left maximum alone determines the water at `l`. You never need to know the exact right maximum.

```python
def trap(height):
    if not height:
        return 0
    l, r = 0, len(height) - 1
    left_max = right_max = 0
    total = 0
    while l < r:
        if height[l] < height[r]:
            if height[l] >= left_max:
                left_max = height[l]
            else:
                total += left_max - height[l]
            l += 1
        else:
            if height[r] >= right_max:
                right_max = height[r]
            else:
                total += right_max - height[r]
            r -= 1
    return total
```

**Complexity.** Time **O(n)**, single pass. Space **O(1)**.

**Traps.** Empty array. Strictly increasing input (answer is 0). Getting the comparison backwards — dry-run `[0,1,0,2]` before you claim it works.

**Follow-up.** *"Explain the O(n) space version first."* → Precompute `leftMax[]` and `rightMax[]` arrays, then sum `min(leftMax[i], rightMax[i]) - height[i]`. Offer this first as the "obvious correct" solution, then optimize. That sequencing is exactly what Amazon rewards.

---

## A4. Container With Most Water — LC 11 · Medium

**Ask.** Pick two bars so the rectangle between them holds the most water. Area = distance × shorter bar.

**Idea in one breath.** Start as wide as possible. Since width can only shrink from here, the only way to win is a taller *shorter* wall — so always throw away the shorter of the two current walls.

**Algorithm.**
1. `l = 0`, `r = n-1`, `best = 0`.
2. While `l < r`: compute `area = (r - l) * min(h[l], h[r])`, update `best`.
3. Move the pointer at the shorter bar inward. Ties: move either.
4. Return `best`.

Why discarding the shorter bar is safe: keeping it can only produce narrower rectangles capped by that same short height, all of which are ≤ what you just measured.

```python
def max_area(height):
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        best = max(best, (r - l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Traps.** Don't confuse this with Trapping Rain Water — here bars have no thickness and only two walls matter.

---

## A5. Sort Colors (Dutch National Flag) — LC 75 · Medium

**Ask.** Sort an array containing only 0s, 1s, and 2s, in one pass, in place.

**S3 lens.** Three-way partitioning is the core of quickselect and of any tiered-storage bucketing.

**Idea in one breath.** Keep three regions growing: confirmed-0s at the front, confirmed-2s at the back, and unknown in the middle. Shrink the unknown region until it's empty.

**Algorithm.**
1. `low = 0`, `mid = 0`, `high = n-1`.
2. While `mid <= high`:
   - `nums[mid] == 0`: swap `nums[low], nums[mid]`; `low += 1`; `mid += 1`.
   - `nums[mid] == 1`: `mid += 1`.
   - `nums[mid] == 2`: swap `nums[mid], nums[high]`; `high -= 1`. **Do not advance mid** — the value you just swapped in is unexamined.
3. Done.

That "don't advance mid on a 2" is the entire problem. Say it out loud when you write it.

```python
def sort_colors(nums):
    low = mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

**Complexity.** Time **O(n)** single pass. Space **O(1)**.

**Traps.** Loop condition is `mid <= high`, not `<`. Advancing `mid` after a 2-swap silently corrupts the result.

---

## A6. Subarray Sum Equals K — LC 560 · Medium

**Ask.** Count how many contiguous subarrays sum to exactly `k`. Negatives allowed.

**S3 lens.** Reported in a 2026 Amazon phone screen. Also: "how many time windows had exactly K bytes transferred" is the same question.

**Idea in one breath.** A subarray sums to k exactly when (running total here) minus (running total at some earlier point) equals k. So carry a running total and count how many times you've previously seen `running - k`.

**Algorithm.**
1. `counts = {0: 1}` — the empty prefix. This seeds the case where a subarray starting at index 0 works.
2. `running = 0`, `answer = 0`.
3. For each `x`: `running += x`; add `counts.get(running - k, 0)` to `answer`; then `counts[running] += 1`.
4. Return `answer`.

**Why not sliding window?** Sliding window needs monotonic growth — negatives break it. Say this before they ask.

```python
from collections import defaultdict

def subarray_sum(nums, k):
    counts = defaultdict(int)
    counts[0] = 1
    running = answer = 0
    for x in nums:
        running += x
        answer += counts[running - k]
        counts[running] += 1
    return answer
```

**Complexity.** Time **O(n)**. Space **O(n)** for the prefix-count map.

**Traps.** Forgetting `counts[0] = 1`. Counting before incrementing (otherwise `k = 0` double-counts).

---

## A7. Maximum Subarray (Kadane) — LC 53 · Medium

**Ask.** Find the contiguous subarray with the largest sum.

**Idea in one breath.** At each element ask one question: is the running sum I've been carrying actually helping me? If it's negative, drop it and start fresh here.

**Algorithm.**
1. `current = best = nums[0]`.
2. For each remaining `x`: `current = max(x, current + x)`; `best = max(best, current)`.
3. Return `best`.

```python
def max_subarray(nums):
    current = best = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Traps.** All-negative input. Initializing `best = 0` returns 0 instead of the least-negative element — initialize from `nums[0]`.

**Follow-up.** *"Return the indices too."* → Track `start` when you reset `current = x`, and snapshot `(start, i)` whenever `best` improves.

---

## A8. Best Time to Buy and Sell Stock — LC 121 · Easy

**Ask.** One buy, one sell, later than the buy. Maximum profit.

**Idea in one breath.** Walk forward remembering the cheapest price so far, and at every step ask what you'd make selling today.

**Algorithm.**
1. `cheapest = prices[0]`, `best = 0`.
2. For each price `p`: `best = max(best, p - cheapest)`; `cheapest = min(cheapest, p)`.
3. Return `best`.

```python
def max_profit(prices):
    if not prices:
        return 0
    cheapest, best = prices[0], 0
    for p in prices:
        best = max(best, p - cheapest)
        cheapest = min(cheapest, p)
    return best
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Traps.** Monotonically falling prices → answer is 0, not negative.

---

# B. Sliding Window

**The pattern, once, so you can reuse it:** expand `right` to grow the window; while the window is invalid, shrink from `left`; record the answer at each valid state. Everything below is that skeleton with a different validity test.

## B1. Longest Substring Without Repeating Characters — LC 3 · Medium

**Ask.** Length of the longest stretch with no repeated character.

**S3 lens.** Tier-1 Amazon frequency. Also the shape of "longest span of distinct request IDs."

**Idea in one breath.** Slide a window right. The moment you hit a character already inside the window, jump the left edge to just past that character's previous position.

**Algorithm.**
1. `last = {}` mapping char → most recent index. `left = 0`, `best = 0`.
2. For each `right`, char `c`:
   - If `c` is in `last` **and** `last[c] >= left`, set `left = last[c] + 1`.
   - `last[c] = right`.
   - `best = max(best, right - left + 1)`.
3. Return `best`.

The `last[c] >= left` guard matters: a stale entry from before the window shouldn't drag `left` backwards.

```python
def length_of_longest_substring(s):
    last = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1
        last[c] = right
        best = max(best, right - left + 1)
    return best
```

**Complexity.** Time **O(n)** — each index visited once. Space **O(min(n, alphabet))**.

**Traps.** The stale-index guard. `"abba"` is the test case that catches it — without the guard you get 3.

**Follow-up.** *"Return the substring itself."* → Store `best_left` alongside `best`, slice at the end.

---

## B2. Minimum Window Substring — LC 76 · Hard

**Ask.** Smallest substring of `s` containing every character of `t`, counting multiplicities.

**Idea in one breath.** Grow the window until it covers everything you need, then squeeze from the left as long as it still covers, recording the smallest. Repeat. The key is a single counter tracking how many *distinct required characters* are fully satisfied, so you never rescan the map.

**Algorithm.**
1. Build `need` = frequency map of `t`. `required = len(need)`.
2. `window = {}`, `formed = 0`, `left = 0`, `best = (∞, 0, 0)`.
3. For each `right`, char `c`:
   - `window[c] += 1`.
   - If `c in need` and `window[c] == need[c]`, then `formed += 1`. (Exactly `==`, so it fires once.)
   - While `formed == required`:
     - If this window is shorter than `best`, record it.
     - Shrink: `d = s[left]`; `window[d] -= 1`; if `d in need` and `window[d] < need[d]`, `formed -= 1`; `left += 1`.
4. Return the recorded slice, or `""`.

```python
from collections import Counter, defaultdict

def min_window(s, t):
    if not s or not t:
        return ""
    need = Counter(t)
    required = len(need)
    window = defaultdict(int)
    formed = left = 0
    best = (float('inf'), 0, 0)
    for right, c in enumerate(s):
        window[c] += 1
        if c in need and window[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            d = s[left]
            window[d] -= 1
            if d in need and window[d] < need[d]:
                formed -= 1
            left += 1
    return "" if best[0] == float('inf') else s[best[1]:best[2] + 1]
```

**Complexity.** Time **O(|s| + |t|)** — each pointer moves forward at most |s| times. Space **O(|s| + |t|)**.

**Traps.** Using `>=` instead of `==` when incrementing `formed` (over-counts). Duplicate characters in `t` — that's why it's a Counter, not a set.

---

## B3. Sliding Window Maximum — LC 239 · Hard

**Ask.** For every window of size k, report the maximum.

**S3 lens.** "Peak request rate in every rolling 5-minute bucket" is literally this.

**Idea in one breath.** Keep a queue of *candidate* indices, ordered so their values decrease. When a new value arrives, anything smaller behind it can never be a maximum again — evict it. The front is always the answer.

**Algorithm.**
1. `dq` = deque of indices. `out = []`.
2. For each index `i`:
   - Pop from the **front** while `dq[0] <= i - k` (slid out of the window).
   - Pop from the **back** while `nums[dq[-1]] <= nums[i]` (dominated by the newcomer).
   - Append `i`.
   - If `i >= k - 1`, append `nums[dq[0]]` to `out`.
3. Return `out`.

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    out = []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```

**Complexity.** Time **O(n)** — each index is pushed once and popped once, so amortized O(1) per step. Say "amortized"; interviewers listen for it. Space **O(k)**.

**Traps.** Storing values instead of indices — then you can't tell what fell out of the window. Emitting output before the first full window forms.

**Follow-up.** *"Why not a heap?"* → A heap gives O(n log k) and needs lazy deletion for stale entries. The deque is strictly better here.

---

## B4. Longest Repeating Character Replacement — LC 424 · Medium

**Ask.** You may change up to `k` characters. Longest run of one repeated character you can create?

**Idea in one breath.** A window is legal when (its length) minus (count of its most common character) ≤ k — that difference is exactly how many changes you'd need.

**Algorithm.**
1. `counts = {}`, `left = 0`, `max_count = 0`, `best = 0`.
2. For each `right`, char `c`: `counts[c] += 1`; `max_count = max(max_count, counts[c])`.
3. While `(right - left + 1) - max_count > k`: `counts[s[left]] -= 1`; `left += 1`.
4. `best = max(best, right - left + 1)`.

**The subtle bit:** `max_count` is never decreased. That's intentional — a stale `max_count` can only make the window look *more* legal than it is, so the window never shrinks below the true best, and the answer stays correct. Explain this; it's the whole interview.

```python
from collections import defaultdict

def character_replacement(s, k):
    counts = defaultdict(int)
    left = max_count = best = 0
    for right, c in enumerate(s):
        counts[c] += 1
        max_count = max(max_count, counts[c])
        while (right - left + 1) - max_count > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Complexity.** Time **O(n)**. Space **O(alphabet)** — O(26) here, effectively O(1).

---

# C. Hashing & Strings

## C1. Group Anagrams — LC 49 · Medium

**Ask.** Bucket words together when they're rearrangements of each other.

**S3 lens.** Canonicalization — reducing many representations to one key — is exactly what content-addressed storage and dedup do.

**Idea in one breath.** Give every word a fingerprint that's identical for anagrams. Sorted letters works; a 26-slot letter count works and is faster.

**Algorithm (count version).**
1. Make a dict mapping fingerprint → list of words.
2. For each word, build a 26-length count array, convert it to a tuple (tuples are hashable, lists aren't).
3. Append the word under that key.
4. Return the dict's values.

```python
from collections import defaultdict

def group_anagrams(words):
    buckets = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for ch in w:
            counts[ord(ch) - ord('a')] += 1
        buckets[tuple(counts)].append(w)
    return list(buckets.values())
```

**Complexity.** Time **O(n · L)** where L is average word length. Space **O(n · L)**.
The sorted-key version is O(n · L log L) — mention you chose counting to drop the log factor.

**Traps.** Unicode or mixed case breaks the 26-slot assumption. Ask about the alphabet up front; if it's open, use `Counter` frozen into a `frozenset(counter.items())` or just sort.

---

## C2. Valid Parentheses — LC 20 · Easy

**Ask.** Are the brackets balanced and correctly nested?

**Idea in one breath.** A stack is a memory of what's still open. Every closer must match the most recently opened thing.

**Algorithm.**
1. `pairs = {')': '(', ']': '[', '}': '{'}`. Empty stack.
2. For each char: if it's an opener, push it. If it's a closer, the stack must be non-empty *and* its top must equal `pairs[char]` — otherwise return False. Pop.
3. Return `len(stack) == 0`.

```python
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

**Complexity.** Time **O(n)**. Space **O(n)** worst case (all openers).

**Traps.** Returning True while the stack still has unclosed openers. Popping an empty stack.

---

## C3. Longest Palindromic Substring — LC 5 · Medium

**Ask.** Find the longest substring that reads the same both ways.

**Idea in one breath.** Every palindrome has a center. There are 2n−1 possible centers (each character, and each gap between characters). Try them all and push outward.

**Algorithm.**
1. Helper `expand(l, r)`: while in bounds and `s[l] == s[r]`, move `l` left and `r` right. Return the substring `s[l+1:r]` (the last successful window).
2. For each index i: run `expand(i, i)` for odd-length centers and `expand(i, i+1)` for even-length.
3. Keep the longest seen.

```python
def longest_palindrome(s):
    if not s:
        return ""
    best = ""
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l + 1:r]
    for i in range(len(s)):
        for cand in (expand(i, i), expand(i, i + 1)):
            if len(cand) > len(best):
                best = cand
    return best
```

**Complexity.** Time **O(n²)** — n centers, each expanding up to O(n). Space **O(1)** beyond the output.

**Traps.** Forgetting even-length centers (`"abba"` fails). Off-by-one in the returned slice.

**Follow-up.** *"Can you do better?"* → Manacher's algorithm is O(n). Nobody expects you to code it at L4 — just name it and say it preprocesses the string with separators so every palindrome becomes odd-length, then reuses mirror information.

---

## C4. Longest Consecutive Sequence — LC 128 · Medium

**Ask.** Longest run of consecutive integers present in an unsorted array. Must be O(n).

**Idea in one breath.** Put everything in a set. Only start counting from a number that has no predecessor in the set — that way each run is walked exactly once.

**Algorithm.**
1. `pool = set(nums)`.
2. For each `x` in `pool`: if `x - 1` is in `pool`, skip — `x` isn't the start of a run.
3. Otherwise walk `x+1, x+2, …` while present, counting length. Track the max.

The skip condition is what keeps it linear. Without it you'd re-walk runs and it degrades toward O(n²).

```python
def longest_consecutive(nums):
    pool = set(nums)
    best = 0
    for x in pool:
        if x - 1 in pool:
            continue
        length = 1
        while x + length in pool:
            length += 1
        best = max(best, length)
    return best
```

**Complexity.** Time **O(n)** — every element is the inner-loop target at most once across the whole run. Space **O(n)**.

**Traps.** Iterating `nums` instead of `pool` wastes work on duplicates. Empty input.

---

## C5. String Compression — LC 443 · Medium

**Ask.** Run-length encode in place: `aabbbb` → `a2b4`. Counts of 1 are written as just the character. Return the new length.

**S3 lens.** RLE is real storage work. Also the in-place write pointer is a nice test of care.

**Idea in one breath.** Two pointers: `read` scans runs, `write` lays down output behind it. Because a run of length ≥ 2 always compresses to ≤ its own size, the write pointer never overtakes the read pointer.

**Algorithm.**
1. `write = 0`, `read = 0`.
2. While `read < n`:
   - `ch = chars[read]`, `start = read`.
   - Advance `read` while the character stays the same.
   - `chars[write] = ch`; `write += 1`.
   - `count = read - start`. If `count > 1`, write each digit of `str(count)` and advance `write`.
3. Return `write`.

```python
def compress(chars):
    write = read = 0
    n = len(chars)
    while read < n:
        ch = chars[read]
        start = read
        while read < n and chars[read] == ch:
            read += 1
        chars[write] = ch
        write += 1
        count = read - start
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write
```

**Complexity.** Time **O(n)**. Space **O(1)** in place.

**Traps.** Counts ≥ 10 are multiple characters — that's the whole difficulty. Count of exactly 1 writes no digit.

---

# D. Intervals

**S3 lens for the whole section:** byte-range requests, multipart upload part boundaries, lifecycle-policy time windows, and log-segment compaction are all interval problems. If an S3 interviewer picks a "practical" question, it lands here often.

**The pattern:** sort by start, then sweep, merging or counting as you go. Say "sort by start time" before you write anything.

## D1. Merge Intervals — LC 56 · Medium

**Ask.** Collapse overlapping ranges into the minimal set of disjoint ranges.

**Idea in one breath.** Sort by start. Then walk left to right holding one "current" interval — either the next one touches it (extend the end) or it doesn't (ship the current, start a new one).

**Algorithm.**
1. Sort intervals by start.
2. `out = [intervals[0]]`.
3. For each subsequent `[s, e]`: let `last = out[-1]`.
   - If `s <= last[1]`, they overlap → `last[1] = max(last[1], e)`.
   - Else append `[s, e]`.
4. Return `out`.

The `max` matters — the next interval can be fully swallowed by the current one.

```python
def merge(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    out = [intervals[0][:]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

**Complexity.** Time **O(n log n)** — the sort dominates; the sweep is O(n). Space **O(n)** for output, O(log n) for sort recursion.

**Traps.** Touching intervals `[1,4]` and `[4,5]` — ask whether those merge. Using `last[1] = e` instead of `max`.

**Follow-up.** *"Streaming, can't sort."* → Keep a balanced BST or sorted list of disjoint intervals; each insert is O(log n) to locate plus O(k) to absorb the k intervals it swallows.

---

## D2. Insert Interval — LC 57 · Medium

**Ask.** Given already-sorted disjoint intervals, insert a new one and re-merge.

**Idea in one breath.** Three phases: copy everything strictly before, absorb everything that overlaps into one interval, copy everything strictly after.

**Algorithm.**
1. `out = []`, `i = 0`, `n = len(intervals)`.
2. **Before:** while `i < n` and `intervals[i][1] < new[0]`: append and `i += 1`.
3. **Absorb:** while `i < n` and `intervals[i][0] <= new[1]`: `new[0] = min(new[0], intervals[i][0])`; `new[1] = max(new[1], intervals[i][1])`; `i += 1`. Then append `new`.
4. **After:** append the rest.

```python
def insert(intervals, new_interval):
    out = []
    i, n = 0, len(intervals)
    s, e = new_interval
    while i < n and intervals[i][1] < s:
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    out.append([s, e])
    while i < n:
        out.append(intervals[i]); i += 1
    return out
```

**Complexity.** Time **O(n)** — no sort needed, input is already ordered. Space **O(n)**.

**Traps.** Mutating the caller's `new_interval`. Insert before all / after all.

---

## D3. Meeting Rooms II (Minimum Rooms) — LC 253 · Medium

**Ask.** Fewest rooms needed so no two meetings share a room.

**S3 lens.** Identical to "peak concurrent connections" or "how many hosts do I need at once."

**Idea in one breath — the version to actually use.** Forget rooms. Split each meeting into two events: +1 at the start, −1 at the end. Sort all events by time, sweep, and the highest running count is your answer.

**Algorithm (sweep line).**
1. Build a list of `(start, +1)` and `(end, -1)` for every meeting.
2. Sort by time; on a tie put `-1` **before** `+1` (a room freed at 10:00 is reusable at 10:00).
3. Sweep, maintaining `active`; track its maximum.

```python
def min_meeting_rooms(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort(key=lambda x: (x[0], x[1]))   # -1 sorts before +1 on ties
    active = best = 0
    for _, delta in events:
        active += delta
        best = max(best, active)
    return best
```

**Complexity.** Time **O(n log n)**. Space **O(n)**.

**Traps.** The tie-break. If ends don't sort before starts you over-count rooms. Confirm with the interviewer whether meetings are half-open `[s, e)`.

**Alternative to mention.** Sort by start, push end times into a min-heap; if the earliest end ≤ current start, pop (reuse a room). Heap size is the answer. Same complexity — say you know both.

---

## D4. Non-overlapping Intervals — LC 435 · Medium

**Ask.** Fewest intervals to delete so none overlap.

**Idea in one breath.** Greedy: always keep the meeting that **ends earliest**, because it leaves the most room for everything after it. Sort by end time, not start.

**Algorithm.**
1. Sort by end.
2. `kept = 0`, `last_end = -∞`.
3. For each `[s, e]`: if `s >= last_end`, keep it (`kept += 1`, `last_end = e`). Else it overlaps — drop it.
4. Return `n - kept`.

```python
def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    kept, last_end = 0, float('-inf')
    for s, e in intervals:
        if s >= last_end:
            kept += 1
            last_end = e
    return len(intervals) - kept
```

**Complexity.** Time **O(n log n)**. Space **O(1)** beyond sorting.

**Traps.** Sorting by start is the classic wrong answer here. Be ready to justify the exchange argument: swapping any optimal solution's first interval for the earliest-ending one never makes things worse.

---

# E. Heaps & Top-K

**The pattern:** for "top k largest," keep a **min-heap of size k** — the smallest of your winners sits on top, ready to be evicted. For "top k smallest," use a max-heap. Getting this backwards is the single most common heap mistake in interviews.

Python's `heapq` is a min-heap only. For a max-heap, push negated values.

## E1. Top K Frequent Elements — LC 347 · Medium

**Ask.** The k most frequently occurring values.

**S3 lens.** "Which bucket prefixes are hottest?" — direct hot-key detection.

**Idea in one breath.** Count everything, then keep only the k best counts in a size-k min-heap so anything worse gets evicted immediately.

**Algorithm.**
1. `counts = Counter(nums)`.
2. Heap of `(frequency, value)`. Push each; if the heap exceeds k, `heappop` (removes the least frequent).
3. Return the values remaining.

```python
import heapq
from collections import Counter

def top_k_frequent(nums, k):
    counts = Counter(nums)
    heap = []
    for value, freq in counts.items():
        heapq.heappush(heap, (freq, value))
        if len(heap) > k:
            heapq.heappop(heap)
    return [value for freq, value in heap]
```

**Complexity.** Time **O(n log k)**. Space **O(n)** for the counter.

**Follow-up — know this one.** *"Can you do O(n)?"* → **Bucket sort.** Frequencies are bounded by n, so make `buckets[0..n]`, put each value into `buckets[its frequency]`, then read from the high end until you have k. O(n) time, O(n) space.

```python
def top_k_frequent_buckets(nums, k):
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)
    out = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            out.append(value)
            if len(out) == k:
                return out
    return out
```

---

## E2. K Closest Points to Origin — LC 973 · Medium

**Ask.** The k points nearest (0,0).

**Idea in one breath.** Same size-k heap trick, but "closest" means smallest distance, so you need a **max-heap** to evict the current worst. Negate the distance.

Never take a square root — it's monotonic, so comparing `x²+y²` gives the same ordering and avoids floating point.

**Algorithm.**
1. For each point compute `d = x*x + y*y`.
2. Push `(-d, point)`. If heap size > k, pop (removes the largest distance).
3. Return the points left.

```python
import heapq

def k_closest(points, k):
    heap = []
    for x, y in points:
        d = x * x + y * y
        heapq.heappush(heap, (-d, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
```

**Complexity.** Time **O(n log k)**. Space **O(k)**.

**Follow-up.** *"O(n) average?"* → Quickselect on squared distance. Partition around a pivot; recurse only into the side containing index k. O(n) average, O(n²) worst case — mention both.

---

## E3. Kth Largest Element in an Array — LC 215 · Medium

**Ask.** The k-th largest value (not the k-th distinct).

**Idea in one breath.** Min-heap of size k. Whatever survives at the top after seeing everything *is* the k-th largest.

```python
import heapq

def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

**Complexity.** Time **O(n log k)**. Space **O(k)**.

**Quickselect version — be able to sketch it.** Partition around a random pivot. If the pivot lands at the target index, done. Otherwise recurse into one side only. **O(n) average, O(n²) worst**, O(1) extra space. Random pivot selection is what makes the worst case vanishingly unlikely — say that.

**Traps.** "K-th largest" counts duplicates. In `[3,3,3,3]`, the 2nd largest is 3.

---

## E4. Merge k Sorted Lists — LC 23 · Hard

**Ask.** Merge k already-sorted linked lists into one sorted list.

**S3 lens.** This *is* log compaction and multi-shard result merging. Strong storage-team question.

**Idea in one breath.** Keep one candidate from each list in a min-heap. Repeatedly take the global smallest and immediately refill from the list it came from.

**Algorithm.**
1. Push `(node.val, list_index, node)` for each non-empty list head. The list index is a tie-breaker so Python never tries to compare two `ListNode` objects.
2. Use a dummy head and a `tail` pointer.
3. While the heap is non-empty: pop the smallest, attach it to `tail`, advance `tail`; if the popped node has a `next`, push it.
4. Return `dummy.next`.

```python
import heapq

def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = tail = ListNode(0)
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    tail.next = None
    return dummy.next
```

**Complexity.** Let N = total nodes. Time **O(N log k)** — every node enters and leaves a heap of size ≤ k. Space **O(k)**.

**Traps.** Forgetting the tie-breaker index → `TypeError` on equal values. Forgetting `tail.next = None` can leave a stale pointer.

**Follow-up.** *"What if the lists don't fit in memory?"* → External k-way merge: buffer a block from each sorted run on disk, merge through the same heap, flush output in blocks. This is the honest S3 answer and it lands well.

---

## E5. Find Median from Data Stream — LC 295 · Hard

**Ask.** Support `addNum(x)` and `findMedian()` on a growing stream.

**S3 lens.** Streaming percentiles for latency monitoring.

**Idea in one breath.** Cut the data in half and hold each half in a heap facing the middle: a max-heap for the lower half, a min-heap for the upper half. The median is then always sitting on top.

**Algorithm.**
1. `low` = max-heap (store negated values). `high` = min-heap.
2. `addNum(x)`: push onto `low`, then immediately move `low`'s largest into `high`. (That push-then-transfer guarantees ordering.) If `high` is now bigger than `low`, move its smallest back.
3. `findMedian()`: if sizes are equal, average the two tops; else the top of `low` (which we keep as the larger or equal heap).

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.low = []    # max-heap via negation
        self.high = []   # min-heap

    def addNum(self, num):
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2.0
```

**Complexity.** `addNum` **O(log n)**, `findMedian` **O(1)**. Space **O(n)**.

**Traps.** Rebalancing in the wrong order lets a small value sit in `high`. The push-then-transfer idiom makes this impossible — use it verbatim.

**Follow-up.** *"All values are 0–100."* → Just keep a 101-slot count array. `findMedian` scans it in O(100) = O(1). This answer impresses.

---

## E6. Min Cost to Connect Ropes / Sticks — LC 1167 · Medium

**Ask.** Repeatedly combine two ropes at a cost equal to their combined length, until one rope remains. Minimize total cost.

**S3 lens.** A long-standing Amazon favorite. Also the shape of merge-tree cost in compaction.

**Idea in one breath.** Every merge's cost gets re-paid in every later merge that contains it. So merge the two *shortest* ropes first — that keeps the big numbers out of the total for as long as possible. It's Huffman coding.

**Algorithm.**
1. Heapify all lengths (min-heap).
2. While more than one rope remains: pop two smallest, `cost = a + b`, add to total, push `cost` back.
3. Return total.

```python
import heapq

def min_cost_to_connect(ropes):
    if len(ropes) <= 1:
        return 0
    heapq.heapify(ropes)
    total = 0
    while len(ropes) > 1:
        a = heapq.heappop(ropes)
        b = heapq.heappop(ropes)
        cost = a + b
        total += cost
        heapq.heappush(ropes, cost)
    return total
```

**Complexity.** Time **O(n log n)**. Space **O(1)** if you heapify in place, else O(n).

**Traps.** 0 or 1 rope → cost 0. Greedy-by-largest is wrong; be ready to say why with a 3-element counterexample.

---

## E7. Task Scheduler — LC 621 · Medium

**Ask.** CPU tasks with a mandatory cooldown `n` between identical tasks. Minimum total time slots including idles?

**S3 lens.** Throttling and per-key rate limits.

**Idea in one breath.** The most frequent task sets the skeleton. It creates `(maxFreq - 1)` gaps of size `n`, and everything else fills those gaps. If there's more work than gap space, there are no idles at all and the answer is just the number of tasks.

**Algorithm.**
1. Count frequencies. `f_max` = highest. `k` = how many tasks tie at `f_max`.
2. `slots = (f_max - 1) * (n + 1) + k`.
3. Answer is `max(slots, total_tasks)`.

```python
from collections import Counter

def least_interval(tasks, n):
    counts = Counter(tasks)
    f_max = max(counts.values())
    k = sum(1 for v in counts.values() if v == f_max)
    return max((f_max - 1) * (n + 1) + k, len(tasks))
```

**Complexity.** Time **O(n)**. Space **O(26)** = O(1).

**Traps.** Forgetting the `max(..., len(tasks))` guard — that's the "no idle needed" case and it's the test they use. `n = 0` must return `len(tasks)`.

**Follow-up.** *"Give me the actual schedule."* → Then use a max-heap plus a cooldown queue of `(task, ready_time)`. Simulate tick by tick. O(total_time · log 26).

---

## E8. Reorganize String — LC 767 · Medium

**Ask.** Rearrange a string so no two adjacent characters are the same, or report it's impossible.

**Idea in one breath.** Always place the character you have the most of, but never the one you just placed. A max-heap plus a one-slot "cooling" buffer does exactly that.

**Algorithm.**
1. Count characters. If any count > `(n+1)//2`, return `""` — impossible by pigeonhole. State this check first; it's the insight.
2. Max-heap of `(-count, char)`.
3. Repeatedly pop the top, append it, decrement its count, and hold it aside. Push the *previous* held item back before popping again.

```python
import heapq
from collections import Counter

def reorganize_string(s):
    counts = Counter(s)
    n = len(s)
    if max(counts.values()) > (n + 1) // 2:
        return ""
    heap = [(-c, ch) for ch, c in counts.items()]
    heapq.heapify(heap)
    out = []
    prev = None
    while heap:
        c, ch = heapq.heappop(heap)
        out.append(ch)
        if prev:
            heapq.heappush(heap, prev)
        c += 1                      # one fewer remaining (c is negative)
        prev = (c, ch) if c else None
    return "".join(out)
```

**Complexity.** Time **O(n log 26)** = **O(n)**. Space **O(26)** = O(1).

**Traps.** Pushing the held character back *before* popping the next one — that lets it repeat.

---

# F. Binary Search

**Two flavors.** (1) Search a sorted array. (2) **Binary search on the answer** — when the answer is a number in a known range and "is X feasible?" is monotonic (once true, always true for larger X). Flavor 2 is heavily favored by infrastructure teams because capacity questions have exactly that shape.

## F1. Search in Rotated Sorted Array — LC 33 · Medium

**Ask.** A sorted array was rotated at some unknown pivot. Find a target in O(log n).

**Idea in one breath.** Cut in the middle. One of the two halves is *always* still properly sorted. Figure out which, check whether the target lies inside that sorted half, and throw away the other half.

**Algorithm.**
1. `lo = 0`, `hi = n-1`.
2. While `lo <= hi`: `mid = (lo + hi) // 2`. If `nums[mid] == target`, return mid.
   - If `nums[lo] <= nums[mid]`: the **left** half is sorted.
     - If `nums[lo] <= target < nums[mid]`, search left (`hi = mid - 1`), else right.
   - Else the **right** half is sorted.
     - If `nums[mid] < target <= nums[hi]`, search right (`lo = mid + 1`), else left.
3. Return −1.

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

**Complexity.** Time **O(log n)**. Space **O(1)**.

**Traps.** The `<=` in `nums[lo] <= nums[mid]` handles the two-element case. Duplicates break the O(log n) guarantee entirely — if they're allowed (LC 81), worst case is O(n) and you must shrink `lo`/`hi` by one when `nums[lo] == nums[mid] == nums[hi]`. Ask about duplicates.

---

## F2. Capacity to Ship Packages Within D Days — LC 1011 · Medium

**Ask.** Given package weights in fixed order and D days, find the smallest ship capacity that gets everything shipped in time.

**S3 lens.** This is the storage-team question in disguise: *"smallest host size / throughput that meets the deadline."* If you learn one binary-search-on-answer problem, learn this one.

**Idea in one breath.** If capacity C works, so does anything bigger. That monotonicity means the space of capacities splits cleanly into "too small" then "works" — so binary search the capacity and test feasibility with a simple greedy pass.

**Algorithm.**
1. Search range: `lo = max(weights)` (must fit the biggest single package), `hi = sum(weights)` (ship everything in one day).
2. `feasible(C)`: walk the weights, greedily filling the current day; when adding the next package would exceed C, start a new day. Return `days_used <= D`.
3. Standard lower-bound binary search: if `feasible(mid)`, `hi = mid`, else `lo = mid + 1`.
4. Return `lo`.

```python
def ship_within_days(weights, days):
    def feasible(cap):
        used, load = 1, 0
        for w in weights:
            if load + w > cap:
                used += 1
                load = 0
            load += w
        return used <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Complexity.** Time **O(n · log(sum − max))**. Space **O(1)**.

**Traps.** Starting `lo` at 1 — a capacity below the heaviest package can never work and your feasibility check must not loop forever. Using `hi = mid - 1` in a lower-bound search overshoots; the pattern is `hi = mid` on success, and the loop condition is `lo < hi`.

**Say this out loud:** *"The answer is monotonic in capacity, so I can binary search it."* That one sentence is what the question is testing.

---

## F3. Koko Eating Bananas — LC 875 · Medium

**Ask.** Piles of bananas, H hours. Find the minimum eating speed that finishes them all, where eating a pile takes `ceil(pile / speed)` hours and she can't move to another pile mid-hour.

Same template as F2 — recognize the family and you get this free.

**Algorithm.**
1. `lo = 1`, `hi = max(piles)`.
2. `feasible(k)`: `sum(ceil(p / k) for p in piles) <= H`.
3. Lower-bound binary search.

```python
import math

def min_eating_speed(piles, h):
    def feasible(k):
        return sum(math.ceil(p / k) for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Complexity.** Time **O(n log(max pile))**. Space **O(1)**.

**Traps.** `lo` must be 1, not 0 (division by zero). Use `-(-p // k)` if you want integer ceiling without floats.

---

## F4. Find First and Last Position of Element — LC 34 · Medium

**Ask.** In a sorted array with duplicates, find the first and last index of a target.

**Idea in one breath.** Run binary search twice with different tie-breaking: once biased left, once biased right.

**Algorithm.**
1. `lower_bound(t)`: first index with value `>= t`. On `nums[mid] < t` do `lo = mid + 1`, else `hi = mid`.
2. `start = lower_bound(target)`. If out of range or `nums[start] != target`, return `[-1, -1]`.
3. `end = lower_bound(target + 1) - 1`.
4. Return `[start, end]`.

```python
def search_range(nums, target):
    def lower_bound(t):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < t:
                lo = mid + 1
            else:
                hi = mid
        return lo

    start = lower_bound(target)
    if start == len(nums) or nums[start] != target:
        return [-1, -1]
    return [start, lower_bound(target + 1) - 1]
```

**Complexity.** Time **O(log n)**. Space **O(1)**.

**Traps.** `hi` initialized to `len(nums)`, not `len(nums) - 1`, for the lower-bound form. Target absent entirely.

---

# G. Trees

Assume `class TreeNode: def __init__(self, val=0, left=None, right=None)`.

**Universal opener:** "BST or plain binary tree?" and "Can values be negative?" Both change the answer.

## G1. Binary Tree Level Order Traversal — LC 102 · Medium

**Ask.** Return node values grouped by depth.

**Idea in one breath.** BFS with a queue, but process a whole level at a time by snapshotting the queue's length before you start popping.

**Algorithm.**
1. If root is None, return [].
2. Queue containing root.
3. While the queue is non-empty: `size = len(queue)` — that is exactly one level. Pop `size` nodes, collect values, push non-None children. Append the level to output.

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out
```

**Complexity.** Time **O(n)**. Space **O(w)**, w = widest level (up to n/2).

**Traps.** Reading `len(q)` after you have already pushed children. Snapshot it first.

**Follow-ups they love.** *Zigzag* → reverse alternate levels. *Right side view* → last element of each level. Both are one-line changes; say so.

---

## G2. Lowest Common Ancestor — LC 236 · Medium

**Ask.** Deepest node with both p and q below it (a node counts as its own descendant).

**S3 lens.** Reported verbatim in a 2026 Amazon SDE-1 loop. Also: deepest shared key prefix in a hierarchical namespace.

**Idea in one breath.** Recurse. If a subtree finds p or q, it reports upward "found something." The first node getting a positive report from **both** children is the answer.

**Algorithm.**
1. Base: node is None, or node is p, or node is q → return node.
2. `left = recurse(node.left)`, `right = recurse(node.right)`.
3. Both non-None → this node is the split point → return it.
4. Otherwise return whichever is non-None.

```python
def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

**Complexity.** Time **O(n)**. Space **O(h)** stack — O(n) if the tree is a chain.

**Traps.** This assumes both nodes exist. If they might not, count found nodes and only answer when the count is 2. Ask about it — it is a real follow-up.

**BST version.** Walk down: both smaller → go left, both larger → go right, first node that splits them is the LCA. O(h) time, O(1) space iteratively.

---

## G3. Validate Binary Search Tree — LC 98 · Medium

**Ask.** Is this a valid BST?

**Idea in one breath.** Checking `left < node < right` locally is **not enough** — a node deep in the left subtree can still violate a distant ancestor's bound. Pass an allowed `(low, high)` range downward and tighten it at every step.

**Algorithm.**
1. `check(node, low, high)`. None → True.
2. If not `low < node.val < high` → False.
3. Return `check(left, low, node.val)` and `check(right, node.val, high)`.
4. Start with `(-inf, +inf)`.

```python
def is_valid_bst(root):
    def check(node, low, high):
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)
    return check(root, float('-inf'), float('inf'))
```

**Complexity.** Time **O(n)**. Space **O(h)**.

**Traps.** The local-only check is the wrong answer they are fishing for — name it and reject it out loud. Ask whether duplicates are allowed and on which side.

**Alternative.** In-order traversal must be strictly increasing; track only the previous value.

---

## G4. Serialize and Deserialize Binary Tree — LC 297 · Hard

**Ask.** Turn a tree into a string and back.

**S3 lens.** Encode/decode with an exact round-trip guarantee is bread-and-butter storage work.

**Idea in one breath.** Preorder, but write an explicit marker for every missing child. Those markers are what make the structure recoverable — a preorder string without them is ambiguous.

**Algorithm.**
- *Serialize:* preorder DFS; emit `str(val)` at each node and `#` at each None; join with commas.
- *Deserialize:* split, wrap in an iterator. `build()` takes the next token; `#` → None; else make a node, then `node.left = build()` and `node.right = build()` in that exact order.

```python
class Codec:
    def serialize(self, root):
        parts = []
        def dfs(node):
            if node is None:
                parts.append('#')
                return
            parts.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(parts)

    def deserialize(self, data):
        tokens = iter(data.split(','))
        def build():
            token = next(tokens)
            if token == '#':
                return None
            node = TreeNode(int(token))
            node.left = build()
            node.right = build()
            return node
        return build()
```

**Complexity.** Both directions **O(n)** time, **O(n)** space.

**Traps.** Negative values — do not pick a delimiter that collides with `-`. If values can be arbitrary strings, define an escape scheme and say so.

**Follow-up.** *"Make it compact."* → BFS level order with trailing nulls trimmed; for a **BST** you can drop null markers entirely and rebuild using value ranges.

---

## G5. Diameter of Binary Tree — LC 543 · Easy problem, Medium pattern

**Ask.** Longest path between any two nodes, in edges. Need not pass through the root.

**Idea in one breath.** For each node, the best path *through* it is (left height) + (right height). Compute heights bottom-up and keep a running max of that sum along the way.

This "return one thing, record another" shape recurs constantly. Learn it here.

```python
def diameter_of_binary_tree(root):
    best = 0
    def height(node):
        nonlocal best
        if node is None:
            return 0
        l = height(node.left)
        r = height(node.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    height(root)
    return best
```

**Complexity.** Time **O(n)**. Space **O(h)**.

**Traps.** Confusing what you *return* (height, for the parent) with what you *record* (diameter, globally). Say the difference out loud while coding.

---

## G6. Binary Tree Maximum Path Sum — LC 124 · Hard

**Ask.** Highest-sum path between any two nodes. Values can be negative.

**Idea in one breath.** Same shape as diameter. Best path *through* a node is `val + max(0, left) + max(0, right)`. But what you hand your parent must go down only one side, so you return `val + max(0, max(left, right))`.

The `max(0, ...)` is the trick: a negative subtree is worth skipping entirely.

```python
def max_path_sum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if node is None:
            return 0
        l = max(0, gain(node.left))
        r = max(0, gain(node.right))
        best = max(best, node.val + l + r)
        return node.val + max(l, r)
    gain(root)
    return best
```

**Complexity.** Time **O(n)**. Space **O(h)**.

**Traps.** Initializing `best = 0` fails on an all-negative tree. Returning `val + l + r` to the parent creates an invalid V-shaped path.

---

## G7. Subtree of Another Tree — LC 572 · Easy

**Ask.** Does `sub` appear as an entire subtree of `root`?

**Idea in one breath.** Two nested recursions: one walks the big tree looking for candidate starting points, the other checks exact structural equality from a given point.

```python
def is_subtree(root, sub):
    def same(a, b):
        if a is None and b is None:
            return True
        if a is None or b is None or a.val != b.val:
            return False
        return same(a.left, b.left) and same(a.right, b.right)
    if root is None:
        return False
    return same(root, sub) or is_subtree(root.left, sub) or is_subtree(root.right, sub)
```

**Complexity.** Time **O(m·n)** worst case. Space **O(h)**.

**Follow-up.** *"Faster?"* → Serialize both with null markers and run KMP substring search. O(m+n). Wrap values in delimiters so `12` does not match inside `123`.

---

# H. Graphs

**Openers for every graph problem:** directed or undirected? weighted? cycles possible? self-loops or multi-edges? how are edges given — adjacency list, edge list, or an implicit grid?

**Picking the traversal:** BFS for shortest path in an *unweighted* graph or anything spreading simultaneously. DFS for connectivity, cycle detection, topological order. Dijkstra for non-negative weights. Union-Find when you only need connectivity and edges arrive incrementally.

## H1. Number of Islands — LC 200 · Medium

**Ask.** Count connected groups of `'1'` in a grid.

**S3 lens.** Connected components over a rack/AZ topology. Tier-1 Amazon frequency — expect it.

**Idea in one breath.** Scan every cell. When you hit unvisited land, that is a new island; then flood-fill everything reachable so you never count it twice.

**Algorithm.**
1. `count = 0`. For each cell, if it is `'1'`, increment `count` and flood-fill from it.
2. The flood fill sinks each visited cell by writing `'0'` — that is your visited marker, no extra memory.

```python
from collections import deque

def num_islands(grid):
    if not grid:
        return 0
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
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'
                        q.append((nx, ny))
    return count
```

**Complexity.** Time **O(R·C)**. Space **O(min(R,C))** for BFS; O(R·C) worst case for DFS recursion.

**Traps.** Marking visited when you *dequeue* instead of when you *enqueue* lets the same cell enter the queue many times. Mark on enqueue.

**Follow-up.** *"Cannot modify the input."* → separate `visited` set, O(R·C) space. *"Grid does not fit in memory."* → process in row bands and stitch components across band boundaries with Union-Find. That is the storage-team answer.

---

## H2. Rotting Oranges — LC 994 · Medium

**Ask.** Rotten oranges infect four-neighbours each minute. Minutes until none are fresh, or −1 if impossible.

**Idea in one breath.** Multi-source BFS. Start with *every* rotten orange already in the queue, and each queue level is one minute.

**Algorithm.**
1. Scan: enqueue all rotten cells, count fresh ones. If `fresh == 0`, return 0.
2. BFS level by level; each level rots fresh neighbours and decrements `fresh`.
3. Return `minutes` if `fresh == 0`, else −1.

```python
from collections import deque

def oranges_rotting(grid):
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
        return 0
    minutes = 0
    while q and fresh:
        minutes += 1
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                    grid[nx][ny] = 2
                    fresh -= 1
                    q.append((nx, ny))
    return minutes if fresh == 0 else -1
```

**Complexity.** Time **O(R·C)**. Space **O(R·C)**.

**Traps.** Returning 0 vs −1 when there are no fresh oranges at all. The `while q and fresh` guard is what stops you counting one extra empty minute.

---

## H3. Course Schedule I & II — LC 207 / 210 · Medium

**Ask.** Given prerequisite pairs, is a valid ordering possible (I), and what is it (II)?

**S3 lens.** Deployment ordering and dependency resolution. A 2026 report shows a harder variant with a per-semester cap and depth-based priority.

**Idea in one breath.** Repeatedly take any course with zero remaining prerequisites, decrementing its dependents. Get stuck before taking everything → there is a cycle.

**Algorithm (Kahn's).**
1. Build adjacency `prereq → [dependents]` and an `indegree` array.
2. Queue every course with indegree 0.
3. Pop `u`, append to `order`; for each dependent `v`, decrement indegree; if it hits 0, enqueue.
4. `len(order) == numCourses` → return it, else `[]`.

```python
from collections import deque

def find_order(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    q = deque(i for i in range(num_courses) if indegree[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []
```

**Complexity.** Time **O(V + E)**. Space **O(V + E)**.

**Traps.** Edge direction. `[a, b]` means "b before a" — get it backwards and everything inverts. Read the spec twice.

**Follow-up (the 2026 variant).** *"At most K courses per semester, preferring the deepest downstream chain."* → Same Kahn's loop, but replace the queue with a max-heap keyed on precomputed longest-downstream-depth and pop at most K per round; count rounds. Compute depth with a reverse-topological DP first.

---

## H4. Clone Graph — LC 133 · Medium

**Ask.** Deep-copy a connected undirected graph.

**Idea in one breath.** Walk the original, keeping a map from original node to its copy. Checking that map before recursing into a neighbour is what stops infinite loops on cycles.

```python
def clone_graph(node):
    seen = {}
    def clone(cur):
        if cur is None:
            return None
        if cur in seen:
            return seen[cur]
        copy = Node(cur.val)
        seen[cur] = copy          # register BEFORE recursing
        for nb in cur.neighbors:
            copy.neighbors.append(clone(nb))
        return copy
    return clone(node)
```

**Complexity.** Time **O(V + E)**. Space **O(V)**.

**Traps.** Registering the copy *after* the recursion is an infinite loop on any cycle. That single line ordering is the whole question.

---

## H5. Word Ladder — LC 127 · Hard

**Ask.** Fewest single-letter transformations from `begin` to `end`, with every intermediate word in the dictionary.

**Idea in one breath.** Unweighted shortest path, so BFS. The only real design decision is finding neighbours cheaply: do not compare against every dictionary word — generate the 25·L single-letter mutations and test set membership.

```python
from collections import deque

def ladder_length(begin, end, word_list):
    pool = set(word_list)
    if end not in pool:
        return 0
    q = deque([(begin, 1)])
    while q:
        word, dist = q.popleft()
        if word == end:
            return dist
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + ch + word[i + 1:]
                if nxt in pool:
                    pool.discard(nxt)        # visited marker
                    q.append((nxt, dist + 1))
    return 0
```

**Complexity.** Time **O(N·L·26)**, N = dictionary size, L = word length. Space **O(N·L)**.

**Traps.** Not removing visited words → exponential blowup. `begin` need not be in the dictionary.

**Follow-up.** *"Faster?"* → **Bidirectional BFS**: expand from both ends, always growing the smaller frontier, stop when they meet. Roughly halves the exponent. Name it even if you do not code it.

---

## H6. Critical Connections in a Network — LC 1192 · Hard

**Ask.** Find every edge whose removal disconnects the network (bridges).

**S3 lens.** The most infrastructure-flavored hard on this list. *"Which links, if they fail, partition the fleet?"* is a real AWS networking question.

**Idea in one breath.** DFS stamps each node with a discovery time. Each node also computes the earliest discovery time reachable from its subtree via any back-edge. Edge `(u,v)` is a bridge exactly when v's subtree cannot reach anything at or above u — meaning there is no alternate route around it.

**Algorithm.**
1. Arrays `disc` (−1 = unvisited) and `low`, plus a timer.
2. On visiting `u`: `disc[u] = low[u] = timer++`.
3. For each neighbour `v`: skip the parent; if unvisited, recurse then `low[u] = min(low[u], low[v])` and **if `low[v] > disc[u]` record a bridge**; if already visited, `low[u] = min(low[u], disc[v])`.

```python
def critical_connections(n, connections):
    graph = [[] for _ in range(n)]
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)
    disc = [-1] * n
    low = [0] * n
    bridges = []
    timer = [0]

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in graph[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])
            else:
                low[u] = min(low[u], disc[v])
    dfs(0, -1)
    return bridges
```

**Complexity.** Time **O(V + E)**. Space **O(V + E)**.

**Traps.** Using `low[v]` instead of `disc[v]` for back edges is a subtle wrong answer. Parallel edges break the plain `v == parent` skip — you would skip by edge id instead. Deep recursion on a long chain; mention going iterative for very large graphs.

---

## H7. Number of Provinces / Union-Find — LC 547 · Medium

**Ask.** Count connected components from an adjacency matrix.

**S3 lens.** Learn Union-Find *here*. It is the right tool whenever connectivity queries arrive incrementally, which is how real fleet topology changes work.

**Idea in one breath.** Every node starts as its own group; each merge reduces the count by one. Two optimizations keep it near-constant: attach the smaller tree under the larger (union by rank), and flatten paths during lookup (path compression).

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True


def find_circle_num(is_connected):
    n = len(is_connected)
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                dsu.union(i, j)
    return dsu.count
```

**Complexity.** Time **O(n²·α(n))** — the n² is just reading the matrix; the DSU operations are effectively constant. Space **O(n)**.

**Say this:** "α is the inverse Ackermann function — under 5 for any input that fits in the universe, so treat it as constant."

---

## H8. Network Delay Time / Dijkstra — LC 743 · Medium

**Ask.** Time for a signal from node k to reach every node in a weighted directed graph; −1 if unreachable.

**Idea in one breath.** Always expand the closest unfinished node next. A min-heap hands you that node in log time, and once popped, a node's distance is final — that is the guarantee non-negative weights buy you.

```python
import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue                     # lazy deletion of stale entries
        dist[u] = d
        for v, w in graph[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
```

**Complexity.** Time **O(E log V)**. Space **O(V + E)**.

**Traps.** Dijkstra is **wrong with negative weights** — say so unprompted and name Bellman-Ford, O(V·E), as the alternative. Nodes are 1-indexed here.

---

# I. Tries

**S3 lens for the whole section.** `ListObjectsV2` takes a prefix and a delimiter and returns matching keys plus "common prefixes." That is a trie walk. If an S3 interviewer wants a question that feels like their day job, this is where they would go. **Prioritize this section.**

## I1. Implement Trie — LC 208 · Medium

**Ask.** Support `insert(word)`, `search(word)` (exact), `startsWith(prefix)`.

**Idea in one breath.** A tree where each edge is one character, so a root-to-node path spells a prefix. A boolean flag marks where a real word ends — that flag is the only difference between `search` and `startsWith`.

```python
class TrieNode:
    __slots__ = ('children', 'is_word')
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
```

**Complexity.** All three operations **O(L)** in word length, independent of how many words are stored. That is the selling point over a hash set. Space **O(total characters)**.

**S3 follow-up to volunteer.** *"Now list all keys under a prefix."* → walk to the prefix node, then DFS collecting words: O(L + output). *"And with a delimiter, returning common prefixes?"* → during that DFS, stop descending at the first delimiter past the prefix and emit the truncated path as a common prefix instead of recursing. Saying this out loud shows you understand what S3 actually does.

---

## I2. Word Search II — LC 212 · Hard

**Ask.** Find every dictionary word hidden in a grid, moving through adjacent cells without reusing a cell within one word.

**Idea in one breath.** Searching for each word separately is far too slow. Put all words into one trie and DFS the grid *once*, walking the trie in lockstep. The moment the trie has no matching child, the whole branch is dead — that pruning is the algorithm.

**Algorithm.**
1. Build a trie; store the full word at its terminal node so you never rebuild strings.
2. DFS from every cell carrying the current trie node.
3. No matching child → return. Terminal marker present → record the word and clear the marker (prevents duplicates).
4. Mark the cell visited with `#`, recurse four ways, restore.
5. **Prune:** after recursing, delete an exhausted child node from its parent so the trie shrinks as words are found.

```python
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = w                      # terminal marker holds the word

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:
            return
        word = node.pop('$', None)
        if word:
            found.append(word)
        board[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, node)
        board[r][c] = ch
        if not node:                       # prune exhausted branch
            parent.pop(ch)

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return found
```

**Complexity.** Time **O(R·C·4^L)** worst case, L = longest word — but trie pruning makes real inputs dramatically faster. Space **O(total characters in words)**.

**Traps.** Not restoring the board after recursion. Duplicate results if you skip clearing the terminal marker.

---

## I3. Design Search Autocomplete System — LC 642 · Hard

**Ask.** As the user types, return the top 3 previously-entered sentences sharing the current prefix, ranked by frequency then lexicographically. `#` ends input and saves the sentence.

**S3 lens.** Prefix listing plus ranking — the console's key search bar.

**Idea in one breath.** A trie for prefixes, and at every node cache the counts of all sentences beneath it. Then a keystroke means walking to one node and sorting a small local list.

```python
class ACNode:
    def __init__(self):
        self.children = {}
        self.counts = {}

class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.root = ACNode()
        for s, t in zip(sentences, times):
            self._insert(s, t)
        self.cursor = self.root
        self.buffer = []

    def _insert(self, sentence, freq):
        node = self.root
        for ch in sentence:
            node = node.children.setdefault(ch, ACNode())
            node.counts[sentence] = node.counts.get(sentence, 0) + freq

    def input(self, c):
        if c == '#':
            self._insert("".join(self.buffer), 1)
            self.buffer = []
            self.cursor = self.root
            return []
        self.buffer.append(c)
        if self.cursor:
            self.cursor = self.cursor.children.get(c)
        if not self.cursor:
            return []
        top = sorted(self.cursor.counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return [s for s, _ in top[:3]]
```

**Complexity.** `input` is **O(k log k)**, k = sentences under the current node. Space **O(total characters × sentences per node)** — that is the real cost, so acknowledge it.

**Follow-up.** *"Too much memory."* → cache only the top 3 per node instead of full counts, accepting harder updates; or cap the cached list. Discussing that trade-off *is* the question.

---

## I4. Concatenated Words — LC 472 · Hard

**Ask.** Find every word built entirely from **two or more** shorter words in the same list.

**S3 lens.** A long-running Amazon favorite; the SDE-3 variant is "is this word a concatenation of two dictionary words."

**Idea in one breath.** Sort by length, so by the time you test a word, every possible building block is already in your pool. Then it is word-break with a DP.

**Algorithm.**
1. Sort ascending by length. Keep a growing `pool` set.
2. For each word: `dp[0] = True`; `dp[i] = True` if some `j < i` has `dp[j]` and `word[j:i]` in `pool`.
3. Because the word itself is not yet in `pool`, any success automatically uses at least 2 pieces. **That ordering is deliberate — say so.**
4. Add the word to `pool` afterward.

```python
def find_all_concatenated_words(words):
    words.sort(key=len)
    pool = set()
    out = []
    for w in words:
        if not w:
            continue
        n = len(w)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and w[j:i] in pool:
                    dp[i] = True
                    break
        if dp[n]:
            out.append(w)
        pool.add(w)
    return out
```

**Complexity.** Time **O(N·L²)** (substring hashing can add a factor of L worst case). Space **O(N·L)**.

**Traps.** Empty strings in the input. Forgetting the at-least-two-pieces requirement.

---

# J. Linked Lists

Assume `class ListNode: def __init__(self, val=0, next=None)`.

**Two habits that solve most of this section:** use a **dummy head** whenever the head might change, and use **slow/fast pointers** whenever you need the middle or a cycle.

## J1. Reverse Linked List — LC 206 · Easy

**Idea in one breath.** Walk forward flipping each `next` pointer backwards, carrying `prev` behind you. Save the next node *before* you overwrite the pointer, or you lose the rest of the list.

```python
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next      # save before overwriting
        head.next = prev
        prev = head
        head = nxt
    return prev
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Recursive version** is O(n) stack — mention it, but the iterative one is what you write.

---

## J2. Merge Two Sorted Lists — LC 21 · Easy

**Idea in one breath.** Dummy head plus a tail pointer; repeatedly take the smaller front node. When one list runs out, attach the remainder whole — no need to copy node by node.

```python
def merge_two_lists(a, b):
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

**Complexity.** Time **O(m + n)**. Space **O(1)**.

**Traps.** Use `<=` not `<` to keep the merge stable. Either list may be empty.

---

## J3. Copy List with Random Pointer — LC 138 · Medium

**Ask.** Deep-copy a list where each node also has a `random` pointer to any node or None.

**Idea in one breath.** You cannot set `random` on the first pass because the target may not exist yet. So do two passes: first clone all the nodes and record old→new, then wire up `next` and `random` using that map.

```python
def copy_random_list(head):
    if not head:
        return None
    mapping = {}
    cur = head
    while cur:                       # pass 1: clone nodes
        mapping[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                       # pass 2: wire pointers
        mapping[cur].next = mapping.get(cur.next)
        mapping[cur].random = mapping.get(cur.random)
        cur = cur.next
    return mapping[head]
```

**Complexity.** Time **O(n)**. Space **O(n)**.

**Follow-up — the good answer.** *"Do it in O(1) extra space."* → **Interleave**: insert each copy directly after its original (A→A'→B→B'). Then `A'.random = A.random.next` reads the copy's random in place. Finally unweave the two lists. Three passes, O(1) extra. Sketch this; it lands well.

---

## J4. Reorder List — LC 143 · Medium

**Ask.** Turn `L0→L1→…→Ln` into `L0→Ln→L1→Ln-1→…`.

**Idea in one breath.** Three known sub-problems chained: find the middle, reverse the second half, then zip the two halves together.

```python
def reorder_list(head):
    if not head or not head.next:
        return
    slow, fast = head, head            # 1. find middle
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next                 # 2. reverse second half
    slow.next = None
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev, second = second, nxt
    first, second = head, prev         # 3. zip
    while second:
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Traps.** Cutting the list at the middle (`slow.next = None`) — skip it and you build a cycle. Odd vs even length; dry-run both.

---

## J5. Linked List Cycle II — LC 142 · Medium

**Ask.** Return the node where a cycle begins, or None.

**Idea in one breath.** Slow and fast pointers must meet inside any cycle. Then a small piece of algebra: reset one pointer to the head and advance both one step at a time — they meet exactly at the cycle entrance.

**Why it works, in one line:** if the tail before the loop has length `a` and they meet `b` into a loop of length `c`, then `a ≡ (c − b) mod c`, which is exactly the remaining distance from the meeting point back to the entrance.

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Traps.** The meeting point is *not* the cycle start — that is the whole point of part II vs part I.

---

# K. Design Data Structures

**This is the highest-signal section for an S3 loop.** These are the questions where "build a component that meets a contract with tight complexity guarantees" is the actual job. If you are short on time, do this section before DP.

## K1. LRU Cache — LC 146 · Medium

**Ask.** `get` and `put` in O(1). When full, evict the least recently used entry.

**S3 lens.** Object metadata caching with a fixed memory budget. Tier-1 Amazon frequency, and near-certain if you get a storage interviewer.

**Idea in one breath.** You need two things at once: O(1) lookup by key, and O(1) knowledge of what is oldest. A hash map gives you the first; a doubly linked list gives you the second. Wire them together — the map's values *are* list nodes, so you can unlink any node in constant time.

**Why doubly linked, not singly?** To remove a node in O(1) you must know its predecessor. A `prev` pointer gives you that for free.

**Algorithm.**
1. Node has `key, value, prev, next`. Keep sentinel `head` and `tail` so no operation ever needs a null check.
2. Order: nearest `head` = most recent, nearest `tail` = least recent.
3. `get(k)`: miss → −1. Hit → unlink the node, re-insert right after `head`, return value.
4. `put(k, v)`: existing key → update value, move to front. New key → insert after `head`; if over capacity, unlink `tail.prev` and delete it from the map too.

**The bug everyone ships:** forgetting to delete the evicted key from the hash map. Store `key` inside the node specifically so eviction can find it.

```python
class _Node:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head = _Node()          # sentinels: no null checks anywhere
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.val

    def put(self, key, value):
        node = self.map.get(key)
        if node:
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]     # <-- the line people forget
        node = _Node(key, value)
        self.map[key] = node
        self._push_front(node)
```

**Complexity.** `get` and `put` both **O(1)**. Space **O(capacity)**.

**Follow-ups to have ready.**
- *"Make it thread-safe."* → A single lock around both operations is correct and simple; say that first. Then note the contention problem and offer sharding by key hash into N independently-locked segments — which is how real caches do it.
- *"Why not `OrderedDict`?"* → It works and is 10 lines, but the interviewer wants the underlying structure. Build it manually, then mention the shortcut exists.
- *"TTL expiry too?"* → Store an expiry timestamp per node; check lazily on `get` and evict expired entries opportunistically, or run a background sweep.

---

## K2. LFU Cache — LC 460 · Hard

**Ask.** Same contract, but evict the **least frequently** used; break frequency ties by least recently used. Still O(1).

**Idea in one breath.** Bucket keys by their access frequency. Each bucket is itself an ordered list (LRU within that frequency). Track the current minimum frequency, so eviction is "take the oldest thing in the min bucket" — no scanning.

**The key realization:** `min_freq` only ever increases by 1 (when the min bucket empties after a promotion) or resets to 1 (on insert). That is what keeps it O(1) instead of requiring a search.

**Algorithm.**
1. `vals[key] = value`, `freqs[key] = count`, `buckets[freq] = OrderedDict of keys`.
2. `_touch(key)`: remove from `buckets[f]`; if that bucket is now empty and `f == min_freq`, `min_freq += 1`; add to `buckets[f+1]`; `freqs[key] = f+1`.
3. `get`: miss → −1; else `_touch` and return.
4. `put`: existing → update value, `_touch`. New → if full, pop the first key from `buckets[min_freq]` and delete it everywhere; then insert with freq 1 and set `min_freq = 1`.

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.vals = {}
        self.freqs = {}
        self.buckets = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key):
        f = self.freqs[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        self.freqs[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.cap <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) >= self.cap:
            evict, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[evict]
            del self.freqs[evict]
        self.vals[key] = value
        self.freqs[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1
```

**Complexity.** `get` and `put` **O(1)**. Space **O(capacity)**.

**Traps.** `capacity == 0`. Forgetting `min_freq = 1` after an insert. Cleaning up all three dictionaries on eviction.

---

## K3. Time Based Key-Value Store — LC 981 · Medium

**Ask.** `set(key, value, timestamp)` and `get(key, timestamp)` returning the value with the largest stored timestamp **≤** the requested one.

**S3 lens.** This is object versioning. Ask S3 for an object "as of" a moment and this is the lookup. If I had to pick the single most on-theme medium in this pack, it is this one.

**Idea in one breath.** Timestamps arrive in increasing order, so each key's history is already a sorted array. Reading "as of time t" is therefore a binary search for the rightmost entry not exceeding t.

**Algorithm.**
1. `store[key] = [(timestamp, value), ...]`, appended in order.
2. `set`: append. O(1).
3. `get`: binary search for the **last** index with `timestamp <= target`. Use an upper-bound search: `lo=0, hi=len`; if `arr[mid][0] <= target` then `lo = mid+1` else `hi = mid`. The answer is at `lo - 1`, or `""` if `lo == 0`.

```python
from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)          # key -> [(ts, value)] ascending

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        arr = self.store.get(key)
        if not arr:
            return ""
        lo, hi = 0, len(arr)
        while lo < hi:                          # upper bound on timestamp
            mid = (lo + hi) // 2
            if arr[mid][0] <= timestamp:
                lo = mid + 1
            else:
                hi = mid
        return arr[lo - 1][1] if lo else ""
```

**Complexity.** `set` **O(1)**. `get` **O(log m)** where m is that key's version count. Space **O(total writes)**.

**Traps.** Returning `""` when the requested time predates every write. Off-by-one — write the upper-bound form and trust it rather than improvising.

**S3-flavored follow-ups.** *"Support delete markers."* → store a tombstone value; a `get` landing on one returns "not found." *"Bound the history."* → keep the newest N versions per key and drop older ones on write, which is exactly a lifecycle rule. *"Timestamps arrive out of order."* → you now need `bisect.insort` on write, O(m) per insert, or a balanced BST for O(log m) both ways.

---

## K4. Design In-Memory File System — LC 588 · Hard

**Ask.** Support `ls(path)`, `mkdir(path)`, `addContentToFile(path, content)` (appends, creating if absent), `readContentFromFile(path)`.

**S3 lens.** The closest LeetCode problem to S3's actual key namespace. Worth doing even at low reported frequency, because it doubles as LLD-round practice.

**Idea in one breath.** A trie whose edges are path segments instead of characters. Directories are internal nodes; files are nodes carrying content. `ls` on a directory lists sorted child names; `ls` on a file returns just that file's name.

**Algorithm.**
1. Node: `children` dict, `content` string, `is_file` flag.
2. `_traverse(path, create)`: split on `/`, drop empties, walk down creating nodes when asked.
3. `ls`: walk; if the node is a file, return `[last_segment]`; else return `sorted(children)`.
4. `mkdir`: walk with `create=True`.
5. `addContentToFile`: walk with create, set `is_file`, append content.
6. `readContentFromFile`: walk, return content.

```python
class FSNode:
    def __init__(self):
        self.children = {}
        self.content = ""
        self.is_file = False

class FileSystem:
    def __init__(self):
        self.root = FSNode()

    def _walk(self, path, create=False):
        node = self.root
        for part in path.split('/'):
            if not part:
                continue
            if part not in node.children:
                if not create:
                    return None
                node.children[part] = FSNode()
            node = node.children[part]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node is None:
            return []
        if node.is_file:
            return [path.rsplit('/', 1)[-1]]
        return sorted(node.children)

    def mkdir(self, path):
        self._walk(path, create=True)

    def addContentToFile(self, path, content):
        node = self._walk(path, create=True)
        node.is_file = True
        node.content += content

    def readContentFromFile(self, path):
        node = self._walk(path)
        return node.content if node else ""
```

**Complexity.** Let d = path depth, k = children in the listed directory. `mkdir`/`add`/`read` are **O(d)**. `ls` is **O(d + k log k)** because of the sort. Space **O(total path segments + content)**.

**Traps.** Root path `"/"` splits into empty strings — filter them. `ls` on a file must return the filename, not its contents.

**The S3 follow-up worth volunteering.** *"Real S3 has no directories — keys are flat strings and `ListObjectsV2` fakes hierarchy with a delimiter."* Then explain: keep keys in a sorted structure, seek to the prefix, scan forward, and for each key truncate at the first delimiter after the prefix — emit distinct truncations as "common prefixes." Saying this unprompted is a strong signal.

---

## K5. Design Hit Counter — LC 362 · Medium

**Ask.** `hit(timestamp)` and `getHits(timestamp)` returning hits in the trailing 300 seconds. Timestamps are non-decreasing.

**S3 lens.** Request-rate accounting and throttling.

**Idea in one breath.** You only ever care about a 300-second window, so keep exactly 300 buckets and reuse them cyclically. Each bucket remembers which second it currently represents; if that is stale, its count is treated as zero.

**Algorithm.**
1. Arrays `times[300]` and `counts[300]`.
2. `idx = timestamp % 300`.
3. `hit`: if `times[idx] != timestamp`, this slot is stale → overwrite `times[idx] = timestamp`, `counts[idx] = 1`. Else `counts[idx] += 1`.
4. `getHits`: sum `counts[i]` for every slot where `timestamp - times[i] < 300`.

```python
class HitCounter:
    def __init__(self):
        self.times = [0] * 300
        self.counts = [0] * 300

    def hit(self, timestamp):
        i = timestamp % 300
        if self.times[i] != timestamp:
            self.times[i] = timestamp
            self.counts[i] = 1
        else:
            self.counts[i] += 1

    def getHits(self, timestamp):
        return sum(c for t, c in zip(self.times, self.counts)
                   if timestamp - t < 300)
```

**Complexity.** `hit` **O(1)**. `getHits` **O(300)** = **O(1)**. Space **O(300)** = **O(1)**.

**Why this beats the queue version.** A queue of raw timestamps is O(hits) space and its cleanup is O(hits) — a burst of a million hits in one second costs a million entries. The ring buffer is bounded regardless of traffic. **Present the queue version first, then this.** That progression is the interview.

**Follow-up.** *"Now make the window configurable, and handle concurrency."* → parameterize the ring size; per-slot atomic counters or a striped lock.

---

## K6. Min Stack — LC 155 · Medium

**Ask.** A stack that also reports its minimum in O(1).

**Idea in one breath.** Each entry remembers the minimum of everything at or below it. Then popping automatically restores the previous minimum with no recomputation.

```python
class MinStack:
    def __init__(self):
        self.stack = []                       # (value, min_at_or_below)

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

**Complexity.** All operations **O(1)**. Space **O(n)**.

**Follow-up.** *"Less space?"* → Keep a second stack that only pushes when a value is ≤ the current min, and pops only when the popped value equals its top. Saves memory when minima are rare. Watch the `<=` — with `<` you break on duplicate minima.

---

## K7. Insert Delete GetRandom in O(1) — LC 380 · Medium

**Ask.** Insert, delete, and return a uniformly random element, all O(1).

**Idea in one breath.** An array gives O(1) random indexing but O(n) deletion. Fix deletion by never deleting from the middle: swap the doomed element with the last one, then pop. A hash map from value → index keeps you oriented.

**Algorithm.**
1. `values = []`, `index = {}`.
2. `insert(v)`: present → False. Else append, record its index, return True.
3. `remove(v)`: absent → False. Else look up `i`; move `values[-1]` into slot `i` and update its index entry; pop the array; delete `v` from the map.
4. `getRandom()`: `random.choice(values)`.

**Order matters in remove:** update the moved element's index *before* popping, and handle the case where the element being removed *is* the last one.

```python
import random

class RandomizedSet:
    def __init__(self):
        self.values = []
        self.index = {}

    def insert(self, val):
        if val in self.index:
            return False
        self.index[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        if val not in self.index:
            return False
        i = self.index[val]
        last = self.values[-1]
        self.values[i] = last
        self.index[last] = i
        self.values.pop()
        del self.index[val]
        return True

    def getRandom(self):
        return random.choice(self.values)
```

**Complexity.** All three **O(1)** average. Space **O(n)**.

**Traps.** Removing the last element: the swap makes `index[last] = i` and then `del self.index[val]` — since `last == val`, the delete must come after, which this ordering handles. Dry-run a single-element set.

---

# L. Dynamic Programming

**How to actually derive a DP in an interview, every time:**
1. **Name the state.** "`dp[i]` = the answer for the first i elements." If you cannot say this in one sentence, your state is wrong.
2. **Write the recurrence.** How does `dp[i]` depend on smaller entries?
3. **Set the base case.** Usually `dp[0]`, and it is usually the empty-input answer.
4. **Pick the order** so dependencies are computed first.
5. **Then compress space** if the recurrence only reaches back a fixed number of steps.

Say steps 1–3 out loud before coding. That is the visible reasoning the interviewer is grading.

## L1. Climbing Stairs / House Robber — LC 70 / 198 · Easy–Medium

**House Robber ask.** Maximum sum from a list where you cannot take two adjacent elements.

**State.** `dp[i]` = best loot considering the first i houses.
**Recurrence.** `dp[i] = max(dp[i-1], dp[i-2] + nums[i-1])` — skip this house, or take it plus the best from two back.
**Base.** `dp[0] = 0`, `dp[1] = nums[0]`.

Only two previous values are ever needed, so keep two variables.

```python
def rob(nums):
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Follow-up (LC 213, houses in a circle).** First and last are now adjacent, so run the linear version twice — once excluding the first house, once excluding the last — and take the max. Handle `n == 1` separately.

---

## L2. Coin Change — LC 322 · Medium

**Ask.** Fewest coins summing to `amount`, or −1.

**State.** `dp[a]` = fewest coins to make amount `a`.
**Recurrence.** `dp[a] = min(dp[a - coin] + 1)` over all coins that fit.
**Base.** `dp[0] = 0`. Everything else starts at infinity.

**Loop order matters:** amount outer, coins inner — that is the *unbounded* knapsack shape, allowing coin reuse.

```python
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]
```

**Complexity.** Time **O(amount × len(coins))**. Space **O(amount)**.

**Traps.** Greedy (always take the largest coin) is **wrong** — coins `[1,3,4]`, amount 6 gives greedy 3 coins but the answer is 2. Have that counterexample memorized; interviewers ask for it.

---

## L3. Word Break — LC 139 · Medium

**Ask.** Can the string be split entirely into dictionary words?

**State.** `dp[i]` = "the first i characters can be segmented."
**Recurrence.** `dp[i]` is true if some `j < i` has `dp[j]` true and `s[j:i]` in the dictionary.
**Base.** `dp[0] = True` (empty string).

```python
def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]
```

**Complexity.** Time **O(n²)** comparisons plus substring hashing. Space **O(n + dictionary)**.

**Optimization worth mentioning.** Cap the inner loop at the longest dictionary word — a real speedup on long strings. Or use a trie to walk forward from each `j` without building substrings.

---

## L4. Longest Increasing Subsequence — LC 300 · Medium

**Ask.** Length of the longest strictly increasing subsequence (not contiguous).

**The O(n²) version.** `dp[i]` = LIS length ending exactly at i; `dp[i] = 1 + max(dp[j])` over all `j < i` with `nums[j] < nums[i]`. Answer is `max(dp)`.

**The O(n log n) version — know what `tails` means.** Keep an array where `tails[k]` is the **smallest possible tail value** of any increasing subsequence of length `k+1`. For each number, binary search for the first tail ≥ it and overwrite that slot; if none, append. The array length is the answer.

**Critical caveat:** `tails` is **not** an actual subsequence. It only tracks lengths. Say this — interviewers probe it.

```python
import bisect

def length_of_lis(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)     # bisect_right for non-strict
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

**Complexity.** Time **O(n log n)**. Space **O(n)**.

**Traps.** `bisect_left` gives strictly increasing; `bisect_right` gives non-decreasing. Ask which one they want.

---

## L5. Edit Distance — LC 72 · Hard

**Ask.** Minimum insert/delete/replace operations to turn word1 into word2.

**State.** `dp[i][j]` = edits to convert the first i characters of word1 into the first j of word2.
**Recurrence.** Characters match → `dp[i-1][j-1]` (free). Otherwise `1 + min(dp[i-1][j-1] replace, dp[i-1][j] delete, dp[i][j-1] insert)`.
**Base.** `dp[i][0] = i` (delete everything), `dp[0][j] = j` (insert everything).

Naming which neighbour is which operation is the part interviewers listen for.

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[n]
```

**Complexity.** Time **O(m·n)**. Space **O(n)** — rolling one row instead of the full table. Mention that you started from the O(m·n) table and compressed.

---

## L6. Decode Ways — LC 91 · Medium

**Ask.** How many ways to decode a digit string where 1→A … 26→Z.

**State.** `dp[i]` = number of decodings of the first i characters.
**Recurrence.** Add `dp[i-1]` if `s[i-1]` is `'1'`–`'9'`; add `dp[i-2]` if `s[i-2:i]` is between `"10"` and `"26"`.
**Base.** `dp[0] = 1`.

It is Fibonacci with validity guards. The guards are the entire problem.

```python
def num_decodings(s):
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1
    for i in range(1, len(s)):
        cur = 0
        if s[i] != '0':
            cur += prev1
        two = int(s[i - 1:i + 1])
        if 10 <= two <= 26:
            cur += prev2
        if cur == 0:
            return 0
        prev2, prev1 = prev1, cur
    return prev1
```

**Complexity.** Time **O(n)**. Space **O(1)**.

**Traps.** Zeros everywhere. `"0"` → 0. `"06"` → 0 (a leading zero cannot start a code). `"100"` → 0. Test all of these out loud.

---

## L7. Unique Paths / Minimum Path Sum — LC 62 / 64 · Medium

**Ask.** Count paths from top-left to bottom-right moving only right or down (62), or minimize the sum along such a path (64).

**State.** `dp[i][j]` = answer for the cell at (i, j).
**Recurrence.** `dp[i][j] = dp[i-1][j] + dp[i][j-1]` for counting, or `grid[i][j] + min(dp[i-1][j], dp[i][j-1])` for the minimum.
**Base.** First row and first column.

```python
def min_path_sum(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols
    dp[0] = grid[0][0]
    for j in range(1, cols):
        dp[j] = dp[j - 1] + grid[0][j]
    for i in range(1, rows):
        dp[0] += grid[i][0]
        for j in range(1, cols):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])
    return dp[cols - 1]
```

**Complexity.** Time **O(R·C)**. Space **O(C)** with the rolling row.

**Note on the rolling array:** when you read `dp[j]` it still holds the row above (the "from above" value) and `dp[j-1]` already holds this row (the "from left" value). Explain that; it is the only subtle line.

---

## L8. 0/1 Knapsack (the template) · Medium

Not a LeetCode number, but the shape behind Partition Equal Subset Sum (416), Target Sum (494), and several Amazon variants. Learn the template once.

**Ask.** Items with weights and values, capacity W. Maximize value; each item used at most once.

**State.** `dp[w]` = best value achievable with capacity exactly ≤ w.
**Recurrence.** For each item: `dp[w] = max(dp[w], dp[w - weight] + value)`.
**Base.** All zeros.

**The one rule you must remember:** for 0/1, iterate capacity **descending**. Ascending order would let the same item be picked twice, which is the *unbounded* knapsack (Coin Change). That single loop direction is the difference between the two problem families — say it out loud.

```python
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for wt, val in zip(weights, values):
        for w in range(capacity, wt - 1, -1):     # DESCENDING = 0/1
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[capacity]
```

**Complexity.** Time **O(n · W)**. Space **O(W)**.

**Pseudo-polynomial warning.** O(n·W) looks polynomial but W is a *value*, not an input length — it is exponential in the bits of W. Knowing this term is a genuine differentiator.

---

# M. Rapid-Fire Appendix

Twenty-five more that appear in Amazon loops. Idea and complexity only — enough to recognize and reconstruct. Solve each once, then re-derive from these notes.

| # | Problem | Core idea | Time | Space |
|---|---|---|---|---|
| 1 | Valid Anagram (242) | Frequency counts must match | O(n) | O(1) |
| 2 | Contains Duplicate (217) | Set membership | O(n) | O(n) |
| 3 | Missing Number (268) | XOR all indices with all values, or sum formula | O(n) | O(1) |
| 4 | Single Number (136) | XOR cancels pairs | O(n) | O(1) |
| 5 | Majority Element (169) | Boyer-Moore voting: keep a candidate and a count | O(n) | O(1) |
| 6 | Rotate Image (48) | Transpose, then reverse each row | O(n²) | O(1) |
| 7 | Spiral Matrix (54) | Four shrinking boundaries; re-check bounds mid-loop | O(R·C) | O(1) |
| 8 | Set Matrix Zeroes (73) | Use row 0 and column 0 as your marker storage | O(R·C) | O(1) |
| 9 | Search a 2D Matrix (74) | Treat it as one sorted array; index math | O(log RC) | O(1) |
| 10 | Merge Sorted Array (88) | Fill from the **back** to avoid overwriting | O(m+n) | O(1) |
| 11 | 3Sum (15) | Sort, fix one element, two-pointer the rest, skip duplicates | O(n²) | O(1) |
| 12 | Two Sum II (167) | Sorted input → two pointers from both ends | O(n) | O(1) |
| 13 | Valid Palindrome (125) | Two pointers skipping non-alphanumerics | O(n) | O(1) |
| 14 | Implement strStr (28) | KMP failure function, or accept O(n·m) naive | O(n+m) | O(m) |
| 15 | Daily Temperatures (739) | Monotonic decreasing stack of indices | O(n) | O(n) |
| 16 | Largest Rectangle in Histogram (84) | Monotonic increasing stack; pop resolves a rectangle | O(n) | O(n) |
| 17 | Evaluate RPN (150) | Stack; pop two on each operator | O(n) | O(n) |
| 18 | Generate Parentheses (22) | Backtrack; only add `)` when close < open | O(4ⁿ/√n) | O(n) |
| 19 | Subsets (78) | Backtrack, or iterate bitmasks 0..2ⁿ−1 | O(n·2ⁿ) | O(n) |
| 20 | Permutations (46) | Backtrack with a used-mask | O(n·n!) | O(n) |
| 21 | Combination Sum (39) | Backtrack; pass the same index to allow reuse | O(n^(t/m)) | O(t/m) |
| 22 | Letter Combinations of a Phone Number (17) | Backtrack over the digit→letters map | O(4ⁿ) | O(n) |
| 23 | Kth Smallest in a BST (230) | In-order traversal, stop at k | O(h+k) | O(h) |
| 24 | Construct Tree from Preorder+Inorder (105) | First preorder value is the root; index map splits inorder | O(n) | O(n) |
| 25 | Meeting Rooms I (252) | Sort by start; any `start < previous end` → false | O(n log n) | O(1) |

---

## Complexity quick reference

| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| Sorted array | O(1) | O(log n) | O(n) | O(n) |
| Hash map | — | O(1) avg, O(n) worst | O(1) avg | O(1) avg |
| Balanced BST | O(log n) | O(log n) | O(log n) | O(log n) |
| Binary heap | O(1) for min/max only | O(n) | O(log n) | O(log n) |
| Trie | O(L) | O(L) | O(L) | O(L) |
| Doubly linked list | O(n) | O(n) | O(1) at a known node | O(1) at a known node |
| Union-Find | — | O(α(n)) | O(α(n)) | — |

**Sorts:** merge sort O(n log n) always, stable, O(n) space. Quicksort O(n log n) average / O(n²) worst, in place, not stable. Heapsort O(n log n) always, in place, not stable. Counting/radix O(n + k) when the value range is bounded — worth naming when an interviewer asks for sub-n-log-n.

---

## The five sentences that carry a coding round

1. *"Let me restate the problem to make sure I have it."*
2. *"Before I code — what are the input size bounds, and can the input be empty or contain duplicates?"*
3. *"The brute force is O(n²) because of X. I think I can get to O(n) using Y — does that direction sound right to you?"*
4. *"Let me trace this on `[example]`."* (then actually do it, pointing at your variables)
5. *"Final complexity is O(n) time, O(n) space, bottlenecked by the hash map. If memory were tight I'd trade back to the two-pointer version at O(n log n)."*
