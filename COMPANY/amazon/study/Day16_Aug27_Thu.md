# Thu Aug 27 — Day 16 of 18
### PHASE 3 — ADVANCED + DESIGN · Backtracking, Tries, Design-in-Code + MOCK LOOP #2

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

Primitives **18, 20**.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 26 (+1d), Aug 24 (+3d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **The whole backtracking family in three lines:**
> - **Combinations** loop from `start`. **Permutations** loop from 0 with a `used[]`.
> - **Duplicates ("II" variants):** `if i > start and a[i] == a[i-1]: continue` — note `i > start`, not `i > 0`.
> - **Always `res.append(path[:])`** — a copy, not the list itself.
>
> **The design-in-code problems get asked as coding questions at Amazon**, not as design questions. Treat them as coding practice with a design flavour.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 78 | Subsets | Template | ____ |
| ☐ | 90 | Subsets II | Sort + skip duplicates | ____ |
| ☐ | 46 | Permutations | used[] array | ____ |
| ☐ | 39 | Combination Sum | Reuse allowed | ____ |
| ☐ | 22 | Generate Parentheses ★ | Prune during generation | ____ |
| ☐ | 17 | Letter Combinations | Map + recurse | ____ |
| ☐ | 208 | Implement Trie | Nested nodes | ____ |
| ☐ | 211 | Add and Search Words | Trie + wildcard DFS | ____ |
| ☐ | 1268 | Search Suggestions System ★ | Sort+BS or Trie | ____ |
| ☐ | 380 | Insert Delete GetRandom O(1) ★ | Array + index map | ____ |
| ☐ | 981 | Time Based Key-Value Store | Sorted list + BS | ____ |
| ☐ | 362 | Design Hit Counter | Deque of timestamps | ____ |
| ☐ | 1472 | Design Browser History | Array + cursor | ____ |


### ★ MOCK LOOP #2 (2h 30m) — after the problem block

- [ ] **Round 1 (60 min) — Coding.** Two unseen problems from the pool at the bottom. Recorded.
- [ ] **Round 2 (60 min) — Coding.** Two more. Recorded.
- [ ] **Review both recordings (30 min).**

Compare against the Aug 23 debrief. Are the same three weaknesses still showing up? If yes, they get all of tomorrow's repair block.

---

## Block D — Design

Covered by the design-in-code problems above. No separate design block — the mock takes the time.

---

## Block E — Leadership Principles

**30 min — your three weakest stories only.** Not the full set today; the mock is the priority.

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

- [ ] Combinations vs permutations vs duplicates — can I state all three rules?
- [ ] Did the same weaknesses from Aug 23 show up again in the mock?
- [ ] Trie from memory in under 90 seconds?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

---

### 208. Implement Trie (Prefix Tree)
**Trigger:** prefix lookup, autocomplete, "starts with"
**Insight:** Each node is a dict of children plus an end-of-word flag. Insert and search are both a straight walk.

```python
class TrieNode:
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
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
```
**insert/search/startsWith all O(L) / O(total chars)** — **Gotcha:** `search` needs the `is_word` flag. Without it, "app" returns True after inserting only "apple".

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

---


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

**⚠ MOCK POOL — do not read until your mock is finished.** These are the unseen problems for today's simulated round.

### 31. Next Permutation
**Insight:** Find the rightmost ascent, swap it with the smallest value to its right that still exceeds it, then reverse the suffix.

```python
def nextPermutation(nums):
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1                           # find the pivot
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    left, right = i + 1, len(nums) - 1
    while left < right:                  # reverse the suffix
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```
**O(n) / O(1)** — the fully-descending case (`[3,2,1]`) falls through to a plain reverse. Walk that case out loud.

---

---

### 402. Remove K Digits
**Insight:** Greedy with a monotonic increasing stack — pop any digit larger than the incoming one while you still have removals left.

```python
def removeKdigits(num, k):
    stack = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k:
        stack = stack[:-k]               # digits were non-decreasing: trim the tail
    return ''.join(stack).lstrip('0') or '0'
```
**O(n) / O(n)** — **Gotchas:** leftover `k`, leading zeros, and the empty-result case.

---

---

### 316. Remove Duplicate Letters
**Insight:** Monotonic stack, but only pop a character if it appears again later. Track last-occurrence and what's already placed.

```python
def removeDuplicateLetters(s):
    last = {ch: i for i, ch in enumerate(s)}
    stack = []
    seen = set()
    for i, ch in enumerate(s):
        if ch in seen:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            seen.discard(stack.pop())    # safe to drop — it reappears later
        stack.append(ch)
        seen.add(ch)
    return ''.join(stack)
```
**O(n) / O(26)** — the `last[stack[-1]] > i` guard is the whole problem.

---

---

### 636. Exclusive Time of Functions
**Insight:** Stack of function IDs. On any event, credit the elapsed time to whoever is currently on top.

```python
def exclusiveTime(n, logs):
    res = [0] * n
    stack = []
    prev = 0
    for log in logs:
        fid, typ, ts = log.split(':')
        fid, ts = int(fid), int(ts)
        if typ == 'start':
            if stack:
                res[stack[-1]] += ts - prev
            stack.append(fid)
            prev = ts
        else:
            res[stack.pop()] += ts - prev + 1     # end is INCLUSIVE
            prev = ts + 1
    return res
```
**O(n) / O(n)** — **Gotcha:** the `+1` on end and `prev = ts + 1`. End timestamps are inclusive; start timestamps are not.

---

---

### 2013. Detect Squares
**Insight:** For each stored point that could be the diagonal opposite, check the two remaining corners. Multiply the counts.

```python
from collections import defaultdict
class DetectSquares:
    def __init__(self):
        self.count = defaultdict(int)    # (x, y) -> how many times added

    def add(self, point):
        self.count[tuple(point)] += 1

    def count_squares(self, point):
        px, py = point
        total = 0
        for (x, y), c in list(self.count.items()):
            if abs(x - px) != abs(y - py) or x == px or y == py:
                continue                 # must be a true diagonal
            total += c * self.count[(px, y)] * self.count[(x, py)]
        return total
```
**add O(1), count O(n) / O(n)** — **Gotcha:** `x == px or y == py` excludes degenerate zero-area "squares".
*(LeetCode names the second method `count`; renamed here to avoid clashing with the attribute.)*

---

---

### 443. String Compression
```python
def compress(chars):
    write = 0
    read = 0
    while read < len(chars):
        ch = chars[read]
        count = 0
        while read < len(chars) and chars[read] == ch:
            read += 1
            count += 1
        chars[write] = ch
        write += 1
        if count > 1:
            for digit in str(count):     # multi-digit counts
                chars[write] = digit
                write += 1
    return write
```
**O(n) / O(1)** — **Gotcha:** counts of 10+ take multiple slots; a count of 1 writes nothing.

---

---
