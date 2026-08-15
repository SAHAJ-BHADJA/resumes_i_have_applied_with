# Wed Aug 26 — Day 15 of 18
### PHASE 3 — ADVANCED + DESIGN · Dynamic Programming

**Answer key for reference: `Day7_KEY.md`** · Solutions for today's problems are at the bottom of this file.

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Read only the *Trigger* and *Insight* lines below — never the code. Close it, keep going. At 20 min, read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

> **If your recruiter confirmed whiteboard:** write every solution today **by hand on paper first**, then type it. Handwritten code is much harder and you must not discover that on Sept 1.

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

Primitive **24** + Tier 1.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 25 (+1d), Aug 23 (+3d), Aug 19 (+7d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **DP in four questions. Answer them out loud before writing anything:**
> 1. What is the **state**? *"Let me define dp[i] as..."* — say this sentence out loud; it unfreezes almost everyone.
> 2. What is the **transition**?
> 3. What are the **base cases**?
> 4. What **order** do I iterate so dependencies are ready?
>
> **Two distinctions that get tested:**
> - **0/1 knapsack iterates amounts BACKWARDS. Unbounded iterates FORWARDS.** (416 vs 322)
> - **Coins in the outer loop ⇒ combinations. Amount in the outer loop ⇒ permutations.** (518)
>
> **322's follow-up:** greedy is *wrong*. Counterexample ready: `coins=[1,3,4], amount=6` → greedy gives 3, DP gives 2.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 70 | Climbing Stairs | Fibonacci | ____ |
| ☐ | 746 | Min Cost Climbing Stairs | 1D | ____ |
| ☐ | 198 | House Robber | 1D, skip-or-take | ____ |
| ☐ | 213 | House Robber II | Circular → two linear | ____ |
| ☐ | 322 | Coin Change ★★ | Unbounded knapsack | ____ |
| ☐ | 518 | Coin Change II | Loop order = comb vs perm | ____ |
| ☐ | 139 | Word Break | 1D over prefixes | ____ |
| ☐ | 53 | Maximum Subarray | Kadane | ____ |
| ☐ | 152 | Maximum Product Subarray | Track both extremes | ____ |
| ☐ | 62 | Unique Paths | 2D grid | ____ |
| ☐ | 63 | Unique Paths II | 2D with obstacles | ____ |
| ☐ | 64 | Minimum Path Sum | 2D grid | ____ |
| ☐ | 221 | Maximal Square ★ | min of three neighbours | ____ |
| ☐ | 300 | Longest Increasing Subsequence ★★ | Both versions | ____ |
| ☐ | 1143 | Longest Common Subsequence ★ | 2D two-string | ____ |
| ☐ | 416 | Partition Equal Subset Sum | 0/1 knapsack, backwards | ____ |
| ☐ | 72 | Edit Distance | 2D two-string | ____ |
| ☐ | 91 | Decode Ways | 1D, all the zero cases | ____ |

---

## Block D — Design

**DESIGN REVIEW — no new design today.**

Go back through **HLD 1–8**. For each one, without notes, can you state:
- [ ] The API (actual signatures)
- [ ] The data model and the access pattern
- [ ] The partitioning strategy
- [ ] **One failure mode and how you degrade**

Whichever two you can't do, redo those two properly tonight.

**The AWS differentiator is the failure-mode answer.** Anyone can draw boxes. Fewer can say what happens when an AZ goes dark.

---

## Block E — Leadership Principles

**Full LP run — all 14 stories plus the mandatory set, timed, out loud.**

Target: every story under 2.5 minutes, every one ending in a number.

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

- [ ] Did I say "let me define dp[i] as..." out loud on every DP problem?
- [ ] 0/1 vs unbounded — do I know which way the loop runs, and why?
- [ ] Can I do all 8 HLDs with an API, a data model, and a failure mode?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

### 746. Min Cost Climbing Stairs
```python
def minCostClimbingStairs(cost):
    a, b = 0, 0                          # cost to reach step i-2, i-1
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i-1], a + cost[i-2])
    return b
```

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

### 221. Maximal Square ★
**dp[r][c] = side length of the largest square whose BOTTOM-RIGHT corner is (r,c).**
```python
def maximalSquare(matrix):
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * (cols + 1) for _ in range(rows + 1)]
    best = 0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if matrix[r-1][c-1] == '1':
                dp[r][c] = 1 + min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1])
                best = max(best, dp[r][c])
    return best * best
```
**The `min` of three neighbours** is the insight — a square needs all three to support it. Pad by 1 to skip boundary checks.

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

## PART B — 2D DP

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

## PART C — BACKTRACKING

*One template, six problems. Notice how little changes.*

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

### 91. Decode Ways
```python
def numDecodings(s):
    if not s or s[0] == '0':
        return 0
    prev2, prev1 = 1, 1                  # dp[0]=1, dp[1]=1
    for i in range(1, len(s)):
        cur = 0
        if s[i] != '0':
            cur += prev1                 # single digit
        two = int(s[i-1:i+1])
        if 10 <= two <= 26:
            cur += prev2                 # two digits
        if cur == 0:
            return 0                     # dead end
        prev2, prev1 = prev1, cur
    return prev1
```
**Every bug in this problem is a zero.** Enumerate: leading `'0'`, `'0'` mid-string, `'30'`, `'06'`.

---

---
