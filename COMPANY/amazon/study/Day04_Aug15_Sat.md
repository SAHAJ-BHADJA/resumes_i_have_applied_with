# Sat Aug 15 — Day 4 of 18
### PHASE 1 — FOUNDATION · Prefix Sum + Stacks  *(weekend — full track)*

**Answer key for reference: `Day2_KEY.md and Day3_KEY.md`** · Solutions for today's problems are at the bottom of this file.

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

Primitives **19, 22** + Tier 1.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 13 (+3d), Aug 14 (+1d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **Monotonic stack rule: store INDICES, not values.** You almost always need the distance.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 974 | Subarray Sums Divisible by K | Prefix mod K | ____ |
| ☐ | 525 | Contiguous Array | Map 0→−1 | ____ |
| ☐ | 304 | Range Sum Query 2D | 2D prefix | ____ |
| ☐ | 20 | Valid Parentheses | Stack | ____ |
| ☐ | 155 | Min Stack | Store running min | ____ |
| ☐ | 150 | Evaluate RPN | Stack | ____ |
| ☐ | 394 | Decode String | Stack of state | ____ |
| ☐ | 739 | Daily Temperatures | Monotonic stack | ____ |
| ☐ | 496 | Next Greater Element I | Monotonic stack | ____ |
| ☐ | 503 | Next Greater Element II | Circular | ____ |
| ☐ | 735 | Asteroid Collision | Stack | ____ |

**Stretch — only if the core block is done and clean:**

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 84 | Largest Rectangle in Histogram | Monotonic + sentinel | ____ |
| ☐ | 853 | Car Fleet | Sort desc + times | ____ |
| ☐ | 227 | Basic Calculator II | Stack, eager * / | ____ |
| ☐ | 71 | Simplify Path | Stack | ____ |

---

## Block D — Design

**HLD 2 — Distributed Key-Value Store (DynamoDB-like).**

Cover:
- **API:** `get(key)`, `put(key, value)`, conditional put. Write the actual signatures.
- **Partitioning:** consistent hashing with virtual nodes. Why plain `hash(key) % N` is wrong (every node addition reshuffles everything).
- **Replication:** replication factor N, and quorum — **R + W > N gives strong consistency**; R=1, W=1 gives fast-and-eventual.
- **Conflict resolution:** last-write-wins vs vector clocks. What breaks with LWW under clock skew.
- **Hot partitions:** one key taking all the traffic. Mitigations: write sharding with a suffix, adaptive capacity.
- **Failure:** node dies mid-write. Hinted handoff, read repair, Merkle-tree anti-entropy.
- **Say this:** *"the data plane needs static stability — reads and writes keep working even if the control plane is unavailable."* That's a strong AWS-native signal.

---

## Block E — Leadership Principles

**Write LP stories #5 and #6.**

Targets: **Bias for Action** · **Insist on the Highest Standards**

Bias for Action wants: *a reversible decision you made fast with incomplete information.* Amazon distinguishes one-way from two-way doors — use that language if it fits.
Highest Standards wants: *you refused to ship something that met the requirement but wasn't good enough,* and what it cost you.

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

- [ ] Can I write a monotonic stack from memory in under 90 seconds?
- [ ] 84 Largest Rectangle: do I understand why the sentinel `+ [0]` exists?
- [ ] KV store: can I state R + W > N and explain what it buys?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

---

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

### 496. Next Greater Element I
```python
def nextGreaterElement(nums1, nums2):
    nxt = {}
    stack = []
    for x in nums2:
        while stack and stack[-1] < x:
            nxt[stack.pop()] = x
        stack.append(x)
    return [nxt.get(x, -1) for x in nums1]
```
**O(n+m) / O(n)** — values are fine here because they're guaranteed unique.

---

---

### 503. Next Greater Element II — circular
**Insight:** Circular ⇒ iterate `2n` times with `i % n`. Only push indices during the first pass conceptually; simplest is to push always and let the second pass only resolve.

```python
def nextGreaterElements(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        cur = nums[i % n]
        while stack and nums[stack[-1]] < cur:
            res[stack.pop()] = cur
        if i < n:
            stack.append(i)              # only push in the first pass
    return res
```
**O(n) / O(n)**

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

### 853. Car Fleet
**Insight:** Sort by starting position **descending**. Compute each car's time to target. A car joins the fleet ahead if its time is ≤ the fleet's time. Count the distinct times that survive.

```python
def carFleet(target, position, speed):
    pairs = sorted(zip(position, speed), reverse=True)
    fleets = 0
    slowest = 0.0
    for pos, spd in pairs:
        time = (target - pos) / spd
        if time > slowest:               # can't catch the one ahead -> new fleet
            fleets += 1
            slowest = time
    return fleets
```
**O(n log n) / O(n)** — this is a monotonic stack in disguise; you only ever need the top.

---

## PART B — LINKED LISTS

---

### 227. Basic Calculator II
**Insight:** Handle `*` and `/` immediately by modifying the stack top; push `+`/`−` as signed numbers. Sum at the end.

```python
def calculate(s):
    stack = []
    num = 0
    op = '+'
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if (not ch.isdigit() and ch != ' ') or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))    # truncate toward zero
            op = ch
            num = 0
    return sum(stack)
```
**O(n) / O(n)** — **Gotcha:** the `i == len(s)-1` clause flushes the final number.

---

---

### 71. Simplify Path
```python
def simplifyPath(path):
    stack = []
    for part in path.split('/'):
        if part == '' or part == '.':
            continue
        if part == '..':
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return '/' + '/'.join(stack)
```

---

---
