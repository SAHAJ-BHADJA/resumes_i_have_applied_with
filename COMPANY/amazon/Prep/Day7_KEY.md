# DAY 7 ANSWER KEY — DP, Backtracking, Design-in-Code

> **DP in four questions. Answer these out loud before writing anything:**
> 1. What is the **state**? (what do the indices of `dp` mean)
> 2. What is the **transition**? (how does `dp[i]` use earlier entries)
> 3. What are the **base cases**?
> 4. What order do I **iterate** so dependencies are ready?
>
> Say "let me define dp[i] as..." out loud. That single sentence unfreezes almost everyone.
>
> **Backtracking is one template.** `choose → recurse → un-choose`. The only things that vary are the base case and the pruning.

---

## PART A — 1D DP

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

### 746. Min Cost Climbing Stairs
```python
def minCostClimbingStairs(cost):
    a, b = 0, 0                          # cost to reach step i-2, i-1
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i-1], a + cost[i-2])
    return b
```

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

### 90. Subsets II — with duplicates
```python
def subsetsWithDup(nums):
    nums.sort()                          # sorting enables dedupe
    res, path = [], []
    def bt(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue                 # skip duplicate at THIS level
            path.append(nums[i])
            bt(i + 1)
            path.pop()
    bt(0)
    return res
```
**`i > start`, not `i > 0`.** That's the entire dedupe rule for every "II" variant.

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

### 17. Letter Combinations of a Phone Number
```python
def letterCombinations(digits):
    if not digits:
        return []
    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl',
               '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    res = []
    def bt(i, path):
        if i == len(digits):
            res.append(path)
            return
        for ch in mapping[digits[i]]:
            bt(i + 1, path + ch)
    bt(0, '')
    return res
```
**Gotcha:** the empty-input guard. It's the only failing test most people hit.

---

## PART D — DESIGN-IN-CODE

### 208. Implement Trie — see `00_PRIMITIVES.py` #20

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

### 1268. Search Suggestions System ★ (Amazon favourite)
**Simplest correct answer — sort + binary search (present this first):**
```python
import bisect
def suggestedProducts(products, searchWord):
    products.sort()
    res = []
    prefix = ""
    start = 0
    for ch in searchWord:
        prefix += ch
        start = bisect.bisect_left(products, prefix, start)
        matches = []
        for p in products[start:start + 3]:
            if p.startswith(prefix):
                matches.append(p)
        res.append(matches)
    return res
```
**O(n log n + L·log n) / O(1)** extra.
**Trie answer (mention it):** store up to 3 sorted suggestions at each node during insertion; then each query is an O(1) lookup per character. Say "the Trie version is better if the product catalogue is static and queried constantly — which, for a retail search bar, it is." *That sentence is Customer Obsession + Think Big in one line.*

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

### 359. Logger Rate Limiter
```python
class Logger:
    def __init__(self):
        self.last = {}

    def shouldPrintMessage(self, timestamp, message):
        if message in self.last and timestamp - self.last[message] < 10:
            return False
        self.last[message] = timestamp
        return True
```
**O(1)** — **the follow-up is the real question:** memory grows forever. Answer: a queue of `(timestamp, message)` evicted lazily, or a sliding two-map bucket scheme. Have that ready.

---

### 362. Design Hit Counter
```python
from collections import deque
class HitCounter:
    def __init__(self):
        self.hits = deque()              # (timestamp, count)

    def hit(self, timestamp):
        if self.hits and self.hits[-1][0] == timestamp:
            self.hits[-1] = (timestamp, self.hits[-1][1] + 1)
        else:
            self.hits.append((timestamp, 1))

    def getHits(self, timestamp):
        while self.hits and self.hits[0][0] <= timestamp - 300:
            self.hits.popleft()
        return sum(c for _, c in self.hits)
```
**Follow-up:** "what if hits arrive out of order, or at millions per second?" → bucketed circular array of 300 slots with a stored timestamp per slot. Know this; it's the same idea as a real rate limiter.

---

### 1472. Design Browser History
```python
class BrowserHistory:
    def __init__(self, homepage):
        self.stack = [homepage]
        self.cur = 0

    def visit(self, url):
        del self.stack[self.cur + 1:]    # forward history is discarded
        self.stack.append(url)
        self.cur += 1

    def back(self, steps):
        self.cur = max(0, self.cur - steps)
        return self.stack[self.cur]

    def forward(self, steps):
        self.cur = min(len(self.stack) - 1, self.cur + steps)
        return self.stack[self.cur]
```
Array + cursor beats two stacks here. Mention the doubly-linked-list alternative for O(1) visit.

---

## STRETCH

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

### 1152. Analyze User Website Visit Pattern ★ (Amazon favourite)
```python
from collections import defaultdict
from itertools import combinations
from collections import Counter
def mostVisitedPattern(username, timestamp, website):
    visits = defaultdict(list)
    for t, u, w in sorted(zip(timestamp, username, website)):
        visits[u].append(w)              # per user, in time order

    count = Counter()
    for sites in visits.values():
        for pattern in set(combinations(sites, 3)):     # set -> count each user ONCE
            count[pattern] += 1

    return list(max(count, key=lambda p: (count[p], [-ord(c) for c in ''.join(p)])))
```
Simpler and safer tiebreak:
```python
def mostVisitedPattern_v2(username, timestamp, website):
    visits = defaultdict(list)
    for t, u, w in sorted(zip(timestamp, username, website)):
        visits[u].append(w)
    count = Counter()
    for sites in visits.values():
        for pattern in set(combinations(sites, 3)):
            count[pattern] += 1
    best = max(count.values())
    return list(min(p for p in count if count[p] == best))
```
**Gotchas:** sort by timestamp first; `set(combinations(...))` so one user can't double-count a pattern; ties broken lexicographically smallest.

---

### 472. Concatenated Words ★
**Insight:** Sort by length. A word is concatenated iff it can be word-broken using only **shorter** words already processed.
```python
def findAllConcatenatedWordsInADict(words):
    word_set = set()
    res = []
    for w in sorted(words, key=len):
        if not w:
            continue
        if can_form(w, word_set):
            res.append(w)
        word_set.add(w)
    return res

def can_form(word, word_set):
    if not word_set:
        return False
    dp = [False] * (len(word) + 1)
    dp[0] = True
    for i in range(1, len(word) + 1):
        for j in range(i):
            if dp[j] and word[j:i] in word_set:
                dp[i] = True
                break
    return dp[-1]
```
**Processing shortest-first is what prevents a word matching itself.** State that.

---

## DAY 7 PATTERN TRIGGERS

| If the problem says... | Reach for |
|---|---|
| "how many ways / count the arrangements" | DP, sum the transitions |
| "min/max cost, can't take adjacent" | House Robber shape, `dp[i-1]` vs `dp[i-2]+x` |
| "fewest coins / can I reach exactly N" | unbounded knapsack, iterate amounts forward |
| "can I split into equal halves / subset sum" | 0/1 knapsack, iterate amounts **backwards** |
| "longest increasing subsequence" | O(n²) DP, then patience sorting for O(n log n) |
| "two strings, edit/align/common" | 2D DP, `dp[i][j]` over prefixes |
| "largest square / rectangle of 1s" | 2D DP, min of three neighbours |
| "max/min path through a grid" | 2D DP, base row and column first |
| "contiguous subarray with max sum/product" | Kadane; track both extremes if products |
| "all subsets / all combinations" | backtracking, loop from `start` |
| "all permutations" | backtracking, loop from 0 + `used[]` |
| "with duplicates (a 'II' variant)" | sort, then `if i > start and a[i]==a[i-1]: continue` |
| "generate all valid X" | backtrack with pruning, never generate-then-filter |
| "prefix / autocomplete / starts-with" | Trie |
| "insert, delete, and get random in O(1)" | array + index hashmap, swap-with-last on delete |
| "value at a given time / versioned key" | sorted list per key + binary search |
| "rate limit / count events in the last N seconds" | deque of timestamps, or bucketed circular array |
