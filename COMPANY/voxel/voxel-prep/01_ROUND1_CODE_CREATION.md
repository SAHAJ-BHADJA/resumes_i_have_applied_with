# Round 1 — Code Creation
### ~45 min · LC easy + medium · 2 problems · The differentiator is communication, not algorithms

---

## What we actually know (not guesses)

| Source | Evidence |
|---|---|
| Glassdoor, Jan 2026 candidate | "LC easy for the technical screen, LC easy + medium for Code Creation" |
| Glassdoor, earlier | **"LeetCode medium question on parentheses"** |
| **Glassdoor, Mar 2026 (Platform role)** | **"Coding round had 2 problems (leetcode style) 1. Easy-Medium 2. Medium-Hard"** ← harder than the Jan report |
| 1Point3Acres OA | **graph paths**, **binary tree symmetry**, **string/array tasks** — "emphasis on clarity and concise coding" |
| Your notes | ~2 problems in 45 min. Pace: ~12 min on the first, 25+ on the second. |

**Translation:** Stacks/parentheses, trees, and graphs are not optional. Everything else is insurance.

> **⚠️ On difficulty:** your notes say easy + medium, and that's the Jan 2026 SWE data point. But a **Mar 2026 Platform-role** candidate reports the second problem hitting **Medium-Hard**. Different role, possibly a different round — but plan for the worse case. **Don't skip the problems marked "stretch"** in Pattern 4 (Longest Valid Parentheses) and Pattern 3 (Minimum Window Substring, Sliding Window Maximum). If problem two lands Medium-Hard and you've only drilled mediums, you'll be narrating your way through something you've never seen — which is survivable, but only if you've practiced narrating while stuck.

---

## The Script — say this every single time

At easy/medium difficulty, everyone solves it. The person who gets hired is the one who narrated it. Memorize these five beats until they're reflex.

### Beat 1 — Clarify (2 min). Keyboard untouched.
> "Before I start — a few questions. What's the input size range? Can the array be empty? Can there be duplicates? Are the values bounded? Should I optimize for time or space if there's a trade-off? And do you want me to handle invalid input or assume it's well-formed?"

Then **restate the problem in your own words** and confirm. This catches misunderstandings for free and it's the single cheapest signal in the round.

> "So to make sure I have it: given X, I return Y, and Z is the tricky case. Right?"

### Beat 2 — Brute force + complexity (1 min). **Never skip this, even when it's trivial.**
> "The naive approach is nested loops — for each element, scan the rest. That's O(n²) time, O(1) space. It works but we can do better."

Skipping this reads as jumping to a memorized answer. Stating it reads as reasoning.

### Beat 3 — Optimal + complexity (2 min). Get the nod before you code.
> "If I trade space for time, I can use a hash map to remember what I've seen — one pass, O(n) time, O(n) space. Want me to code that up?"

**Wait for them to say yes.** That pause is where they'd redirect you if you're off track. Candidates who barrel into code lose 20 minutes to the wrong approach.

### Beat 4 — Code (12–20 min). Narrate the *why*, not the *what*.
- ❌ "I'm setting i to zero" — they can see that
- ✅ "I'm using a dict keyed by value so lookup is O(1) — the whole trick is that I only need the complement, not the pair"

**Voxel values clean over clever.** Meaningful names. No one-liner comprehension golf. If you'd need a comment to explain it, write it as three lines instead.

### Beat 5 — Dry run (3–5 min). **Before** you say "done."
> "Let me trace this with `[2, 7, 11, 15]`, target 9. i=0, num=2, complement=7, not in seen, so seen = {2: 0}. i=1, num=7, complement=2 — that *is* in seen, return [0, 1]. Correct. Now edge cases: empty array returns empty, single element returns empty, no valid pair returns empty. Duplicates: [3,3] target 6 — i=0 stores 3, i=1 finds complement 3 in seen, returns [0,1]. Good."

**Then** say done. Never say "done" before tracing. A bug caught by you is a strength; a bug caught by them is a weakness.

---

## The Edge Case Checklist — run it mentally on every problem

```
Empty input           →  [], "", None, empty tree/graph
Single element        →  [x], one node, one vertex
Two elements          →  where off-by-ones live
All identical         →  [3,3,3,3]
Already sorted / reverse sorted
Negative numbers / zero
Duplicates
Overflow / very large n
Target not found      →  return what? -1, [], None?
Cycles (graphs)       →  will your DFS terminate?
Disconnected (graphs) →  do you loop over all starts?
Skewed tree           →  recursion depth — say "Python caps at ~1000, iterative if needed"
```

Say two or three of these out loud in Beat 1. It's a 15-second investment that reads as senior.

---

## The Templates — write these from memory before Friday ends

```python
# ── Two pointers, opposite ends ────────────────────────────────
def two_pointer(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        if condition(arr[lo], arr[hi]):
            lo += 1
        else:
            hi -= 1
    return result

# ── Sliding window, variable size ──────────────────────────────
def sliding_window(s):
    window = {}          # or a counter / set
    left = 0
    best = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        while invalid(window):           # shrink until valid again
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best

# ── BFS on a grid ──────────────────────────────────────────────
from collections import deque
def bfs(grid, start):
    rows, cols = len(grid), len(grid[0])
    q = deque([start])
    seen = {start}
    steps = 0
    while q:
        for _ in range(len(q)):          # level by level
            r, c = q.popleft()
            for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        steps += 1
    return steps

# ── DFS on a graph (adjacency list) ────────────────────────────
def dfs(graph, node, seen):
    if node in seen:
        return
    seen.add(node)
    for nxt in graph[node]:
        dfs(graph, nxt, seen)

# ── Backtracking ───────────────────────────────────────────────
def backtrack(path, choices, results):
    if is_solution(path):
        results.append(path[:])          # copy!
        return
    for choice in choices:
        path.append(choice)
        backtrack(path, next_choices(choice), results)
        path.pop()                       # undo

# ── Binary search (leftmost) ───────────────────────────────────
def bisect_left_custom(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

# ── Monotonic stack ────────────────────────────────────────────
def monotonic(arr):
    stack = []                            # holds indices
    result = [0] * len(arr)
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] < x:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result

# ── Topological sort (Kahn's) ──────────────────────────────────
def topo_sort(n, edges):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    q = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)
    return order if len(order) == n else []   # [] means cycle
```

---
---

# PATTERN 4 — STACKS & PARENTHESES ⭐ CONFIRMED ASKED
> **Do this pattern first. A LeetCode medium on parentheses is documented on Glassdoor.**
> **FRIDAY, 1:00–2:30.** Order: 4.1 → 4.2 → 4.3 → 4.6 → 4.7.

### 4.1 Valid Parentheses · LC 20 · Easy · ★★★★★

**How they'd say it:**
> "Given a string containing just `(`, `)`, `{`, `}`, `[`, `]`, determine if the input string is valid. Brackets must close in the correct order."

**Voxel-flavored variant they might use:**
> "We have a config DSL for camera zone definitions. Validate that the nesting is balanced."

```python
def is_valid(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:                       # it's a closer
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:                                 # it's an opener
            stack.append(ch)
    return not stack                          # leftovers = unclosed
```
**Insight:** the stack *is* the "what am I waiting to close" memory. **O(n) / O(n).**
**Trap:** returning `True` at the end without checking `not stack` — `"((("` must fail.

---

### 4.2 Minimum Remove to Make Valid Parentheses · LC 1249 · Medium · ★★★★★
> **If I had to bet on one problem, it's this one.** It's the most-asked parentheses medium in industry, it has letters mixed in (so it's also a "string task"), and it rewards clean code.

**How they'd say it:**
> "Given a string of `(`, `)`, and lowercase letters, remove the minimum number of parentheses so the result is valid. Return any valid result."

```python
def min_remove_to_make_valid(s: str) -> str:
    chars = list(s)
    open_idx = []                             # indices of unmatched '('

    for i, ch in enumerate(chars):
        if ch == '(':
            open_idx.append(i)
        elif ch == ')':
            if open_idx:
                open_idx.pop()                # matched — keep both
            else:
                chars[i] = ''                 # unmatched ')' — drop it

    for i in open_idx:                        # leftover '(' — drop them
        chars[i] = ''

    return ''.join(chars)
```
**Insight:** two passes conceptually, one loop plus a cleanup. Mark-then-sweep instead of building strings. **O(n) / O(n).**
**Say this out loud:** *"I'm marking rather than deleting in place because deleting shifts indices — mark-then-join is cleaner and still O(n)."* That sentence alone signals experience.

---

### 4.3 Generate Parentheses · LC 22 · Medium · ★★★★☆

**How they'd say it:**
> "Given n pairs of parentheses, generate all combinations of well-formed parentheses."

```python
def generate_parenthesis(n: int) -> list[str]:
    results = []

    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            results.append(''.join(path))
            return
        if open_count < n:                    # can always open if we have room
            path.append('(')
            backtrack(path, open_count + 1, close_count)
            path.pop()
        if close_count < open_count:          # can only close what's open
            path.append(')')
            backtrack(path, open_count, close_count + 1)
            path.pop()

    backtrack([], 0, 0)
    return results
```
**Insight:** the two invariants (`open < n`, `close < open`) prune the whole invalid space — you never generate a bad string and filter it. **O(4ⁿ/√n)** (Catalan).
**Trap:** `results.append(path)` instead of `''.join(path)` / `path[:]` — you'd append a reference that later mutates.

---

### 4.4 Score of Parentheses · LC 856 · Medium · ★★★☆☆
```python
def score_of_parentheses(s: str) -> int:
    stack = [0]                               # score of current depth
    for ch in s:
        if ch == '(':
            stack.append(0)
        else:
            inner = stack.pop()
            stack[-1] += max(2 * inner, 1)    # "()" scores 1, "(A)" scores 2A
    return stack[0]
```
**Insight:** `max(2*inner, 1)` elegantly handles both base case and nesting. **O(n) / O(n).**

---

### 4.5 Longest Valid Parentheses · LC 32 · Hard · ★★★☆☆
> Stretch. If they ask this, they're probing your ceiling — narrate hard even if you don't finish.

```python
def longest_valid_parentheses(s: str) -> int:
    stack = [-1]                              # sentinel base index
    best = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)               # new base for the next segment
            else:
                best = max(best, i - stack[-1])
    return best
```
**Insight:** the stack holds the index *before* the current valid run. The `-1` sentinel is the whole trick. **O(n) / O(n).**

---

### 4.6 Min Stack · LC 155 · Medium · ★★★★☆
> Design-flavored. Fits Voxel's "design a small class" taste and could appear in Round 2 too.

```python
class MinStack:
    def __init__(self):
        self._stack = []                      # (value, min_so_far)

    def push(self, val: int) -> None:
        current_min = min(val, self._stack[-1][1]) if self._stack else val
        self._stack.append((val, current_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def get_min(self) -> int:
        return self._stack[-1][1]
```
**Insight:** carry the min alongside each entry. All ops **O(1)**.
**Follow-up they'll ask:** "can you do it with less space?" → store mins in a second stack, only pushing when `val <= current_min`.

---

### 4.7 Daily Temperatures · LC 739 · Medium · ★★★★☆
> The canonical monotonic stack. Voxel-flavored: *"for each sensor reading, how many ticks until a higher reading?"*

```python
def daily_temperatures(temps: list[int]) -> list[int]:
    answer = [0] * len(temps)
    stack = []                                # indices, temps decreasing
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            prev = stack.pop()
            answer[prev] = i - prev
        stack.append(i)
    return answer
```
**Insight:** each index pushed and popped once → **O(n)**, not O(n²), despite the nested-looking `while`. **Say that out loud** — the amortized-analysis observation is exactly the kind of thing that separates candidates.

---

### 4.8 Asteroid Collision · LC 735 · Medium · ★★★☆☆
```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()                   # left one dies, keep colliding
            elif stack[-1] == -a:
                stack.pop()                   # both die
                alive = False
            else:
                alive = False                 # incoming dies
        if alive:
            stack.append(a)
    return stack
```
**Insight:** collision only when a right-mover (`stack[-1] > 0`) meets a left-mover (`a < 0`). Sign encodes direction.

---

### 4.9 Also drill (do these fast)
| Problem | LC | Insight |
|---|---|---|
| Evaluate Reverse Polish Notation | 150 | Push operands, pop two on operator. Watch Python's `//` truncating toward -∞ — use `int(a/b)`. |
| Decode String | 394 | Two stacks: counts and partial strings. |
| Remove All Adjacent Duplicates | 1047 | `if stack and stack[-1] == ch: stack.pop() else: stack.append(ch)` |
| Basic Calculator II | 227 | Push signed numbers; resolve `*` and `/` immediately, sum at the end. |
| Simplify Path | 71 | Split on `/`, `..` pops, `.` and `''` skip. |

---
---

# PATTERN 5 — BINARY TREES ⭐ CONFIRMED ASKED
> **"Binary tree symmetry" is explicitly in the 1Point3Acres OA report.** Do 5.1 twice.
> **FRIDAY, 2:45–4:00.** Order: 5.1 → 5.1 iteratively → 5.4 → 5.5 → 5.6 → 5.7.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### 5.1 Symmetric Tree · LC 101 · Easy · ★★★★★ CONFIRMED

**How they'd say it:**
> "Given the root of a binary tree, check whether it is a mirror of itself around its center."

**Know both. They will ask for the other one.**

```python
# Recursive
def is_symmetric(root: TreeNode) -> bool:
    def mirror(a, b):
        if not a and not b:
            return True                       # both empty → symmetric
        if not a or not b:
            return False                      # one empty → not
        return (a.val == b.val
                and mirror(a.left, b.right)   # outer pair
                and mirror(a.right, b.left))  # inner pair
    return mirror(root, root) if root else True

# Iterative — the follow-up
from collections import deque
def is_symmetric_iter(root: TreeNode) -> bool:
    if not root:
        return True
    q = deque([(root.left, root.right)])
    while q:
        a, b = q.popleft()
        if not a and not b:
            continue
        if not a or not b or a.val != b.val:
            return False
        q.append((a.left, b.right))
        q.append((a.right, b.left))
    return True
```
**The one insight that matters:** you are **not** comparing a tree to itself — you're comparing two pointers walking in *opposite* directions. `left.left` pairs with `right.right`. Say this out loud; it's the whole problem.
**O(n) / O(h)** where h is height.

---

### 5.2 Same Tree · LC 100 · Easy · ★★★★☆
```python
def is_same_tree(p, q) -> bool:
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```
**Note:** this is Symmetric Tree with the recursive calls *not* crossed. If you can articulate that difference, you understand both.

---

### 5.3 Invert Binary Tree · LC 226 · Easy · ★★★★☆
```python
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

---

### 5.4 Maximum Depth · LC 104 · Easy · ★★★★★
```python
def max_depth(root) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```
**The follow-up is always Diameter or Balanced.** Know that this is the base primitive.

---

### 5.5 Diameter of Binary Tree · LC 543 · Easy(ish) · ★★★★☆
```python
def diameter_of_binary_tree(root) -> int:
    best = 0
    def depth(node):
        nonlocal best
        if not node:
            return 0
        left, right = depth(node.left), depth(node.right)
        best = max(best, left + right)        # path through this node
        return 1 + max(left, right)           # depth reported upward
    depth(root)
    return best
```
**The insight worth narrating:** *"The function returns one thing (depth) but computes another as a side effect (the best diameter). The diameter through a node is left+right, but the value I report to my parent is 1+max — those are different questions and conflating them is the classic bug."*
**This pattern — "return one value, track another with nonlocal" — is the single most reusable tree trick.** It's also LC 124 (Max Path Sum) and LC 110 (Balanced).

---

### 5.6 Binary Tree Level Order Traversal · LC 102 · Medium · ★★★★★
```python
from collections import deque
def level_order(root) -> list[list[int]]:
    if not root:
        return []
    result, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):               # snapshot size = this level
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result
```
**The `for _ in range(len(q))` is the whole trick** — it freezes the level boundary before you start adding the next level. Right Side View (LC 199) is this with `level[-1]`.

---

### 5.7 Validate Binary Search Tree · LC 98 · Medium · ★★★★☆
```python
def is_valid_bst(root) -> bool:
    def check(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return (check(node.left, low, node.val)
                and check(node.right, node.val, high))
    return check(root, float('-inf'), float('inf'))
```
**The trap everyone falls into:** checking only `node.left.val < node.val < node.right.val`. That passes `[5,1,6,null,null,4,7]` which is invalid — 4 is in the right subtree of 5 but less than 5. **You must carry bounds down.** Mention this trap unprompted; it shows you've thought about it rather than memorized it.

---

### 5.8 Lowest Common Ancestor · LC 236 (binary tree) · Medium · ★★★★☆
```python
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root                           # p and q split here → this is the LCA
    return left or right                      # both on one side, or neither
```
**For the BST version (LC 235) it's simpler** — walk down, go left if both smaller, right if both larger, else you're at the LCA. If they give you a BST and you use the generic solution, they'll ask why you ignored the ordering.

---

### 5.9 Also drill
| Problem | LC | Insight |
|---|---|---|
| Balanced Binary Tree | 110 | Same nonlocal trick as Diameter; return -1 as a sentinel for "unbalanced". |
| Path Sum | 112 | Subtract as you descend; check `not node.left and not node.right`. |
| Path Sum II | 113 | Backtracking on trees — `path.pop()` after recursing. |
| Binary Tree Right Side View | 199 | Level order, take `level[-1]`. |
| Serialize/Deserialize | 297 | Preorder with `#` for null; deserialize with an iterator. Hard but very "design-y". |
| Binary Tree Max Path Sum | 124 | Diameter with values; clamp negatives with `max(0, ...)`. |
| Count Good Nodes | 1448 | Pass max-so-far down. |

---
---

# PATTERN 6 — GRAPHS, BFS & DFS ⭐ CONFIRMED ASKED
> **"Graph paths" is explicitly in the 1Point3Acres OA report.** 6.1 and 6.2 first.
> **FRIDAY, 4:15–5:30.** Order: 6.1 → 6.2 → 6.3 → 6.4.

### 6.1 All Paths From Source to Target · LC 797 · Medium · ★★★★★ CONFIRMED SHAPE
> This is literally "graph paths."

**How they'd say it:**
> "Given a directed acyclic graph of n nodes, find all possible paths from node 0 to node n-1."

```python
def all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    target = len(graph) - 1
    results = []

    def backtrack(node, path):
        if node == target:
            results.append(path[:])           # copy — path keeps mutating
            return
        for nxt in graph[node]:
            path.append(nxt)
            backtrack(nxt, path)
            path.pop()                        # undo

    backtrack(0, [0])
    return results
```
**Insight:** it's a DAG, so **no `visited` set is needed** — you can't revisit and loop. Say this. If the interviewer's follow-up is *"what if there were cycles?"* the answer is: add a `visited` set to the current path (not global), add on entry, remove on backtrack.
**O(2ⁿ · n)** worst case — exponential is *correct* here because the output itself is exponential. Point that out: *"we can't beat this asymptotically because there can be exponentially many paths — we're output-bound, not algorithm-bound."*

---

### 6.2 Number of Islands · LC 200 · Medium · ★★★★★

**How they'd say it (very likely in Voxel dressing):**
> "You have a grid where each cell is a camera's coverage area. `1` means a hazard was detected, `0` means clear. Count the number of distinct hazard zones, where adjacent detections (4-directionally) form one zone."

```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def sink(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != '1':
            return
        grid[r][c] = '0'                      # mark visited by sinking
        sink(r + 1, c); sink(r - 1, c)
        sink(r, c + 1); sink(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                sink(r, c)                    # erase the whole island
    return count
```
**Insight:** the outer loop counts *starts*; the DFS erases everything reachable so you never double-count.
**The question they'll ask:** *"You mutated the input — is that OK?"* Correct answer: *"It's O(1) extra space, but it's destructive. In production I'd use a separate `visited` set, or copy the grid. Which do you prefer?"* — **that answer wins the round.** It shows you know the trade-off rather than not having noticed.
**Follow-up:** "what if the grid is too big for recursion?" → iterative BFS with a deque.

---

### 6.3 Rotting Oranges · LC 994 · Medium · ★★★★★
> **The most Voxel-shaped problem on this list** — a hazard spreading through a facility over time steps. Multi-source BFS.

```python
from collections import deque
def oranges_rotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0

    for r in range(rows):                     # seed ALL rotten cells at once
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while q and fresh:
        for _ in range(len(q)):               # one minute per level
            r, c = q.popleft()
            for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1

    return minutes if fresh == 0 else -1
```
**Insight:** **multi-source BFS** — seed every rotten cell before you start, and the wavefront naturally gives you minimum time. Trying to BFS from each source separately is the wrong instinct and much slower.
**Trap:** `while q and fresh` — if you write `while q` you'll count one extra minute after the last spread.

---

### 6.4 Course Schedule · LC 207 · Medium · ★★★★★
> **High priority** — cycle detection in a DAG is *exactly* the job-scheduler dependency problem from your systems round. Solving this and then saying *"this is the same check a workflow engine runs before executing a DAG of tasks"* connects two rounds.

```python
from collections import deque
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)          # prereq → course
        indegree[course] += 1

    q = deque(i for i in range(num_courses) if indegree[i] == 0)
    completed = 0
    while q:
        node = q.popleft()
        completed += 1
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    return completed == num_courses           # short → there's a cycle
```
**Insight:** Kahn's algorithm. If you can't drain the queue, a cycle blocked you. **O(V + E).**
**LC 210 (Course Schedule II)** is identical but returns the order — just collect `node` into a list. **Know both.**

---

### 6.5 Clone Graph · LC 133 · Medium · ★★★★☆
```python
def clone_graph(node):
    if not node:
        return None
    clones = {}                               # original → copy

    def dfs(cur):
        if cur in clones:
            return clones[cur]
        copy = Node(cur.val)
        clones[cur] = copy                    # register BEFORE recursing — breaks cycles
        for nbr in cur.neighbors:
            copy.neighbors.append(dfs(nbr))
        return copy

    return dfs(node)
```
**The one line that matters:** `clones[cur] = copy` must come **before** the neighbor loop. Otherwise a cycle sends you into infinite recursion. Narrate this — it's the entire difficulty of the problem.

---

### 6.6 Find if Path Exists in Graph · LC 1971 · Easy · ★★★★☆
> The easy version of "graph paths" — likely the warm-up problem.

```python
from collections import deque, defaultdict
def valid_path(n: int, edges: list[list[int]], source: int, destination: int) -> bool:
    if source == destination:
        return True
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)                    # undirected

    seen = {source}
    q = deque([source])
    while q:
        node = q.popleft()
        for nxt in graph[node]:
            if nxt == destination:
                return True
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return False
```
**Don't forget** the `source == destination` early return — it's the edge case they're checking for.

---

### 6.7 Also drill
| Problem | LC | Insight |
|---|---|---|
| Max Area of Island | 695 | Number of Islands, but DFS returns a size. |
| Number of Connected Components | 323 | Union-Find or DFS-count. Know Union-Find exists; you probably won't need it. |
| Pacific Atlantic Water Flow | 417 | **Reverse the flow** — BFS inward from both borders, intersect. |
| Word Ladder | 127 | BFS on implicit graph; precompute `h*t` wildcard buckets or you'll TLE. |
| Network Delay Time | 743 | Dijkstra with a heap. Know it; unlikely at this level. |
| Surrounded Regions | 130 | Mark from the border inward, then flip. Same "reverse it" trick as 417. |
| Course Schedule II | 210 | 6.4 but collect the order. |

---
---

# PATTERN 1 — HASH MAPS & COUNTING
> ⚪ **CUT FROM THE 4-DAY PLAN — reference only.** Unconfirmed pattern. Skim if the Friday diagnostic exposes a gap here, otherwise skip. "String/array tasks" from the OA report live here, so it's the most likely of the cut patterns to appear.

### 1.1 Two Sum · LC 1 · Easy · ★★★★★
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}                                 # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```
**Insight:** you never need the pair, only the complement — one pass. **O(n) / O(n).**
**Narrate:** *"Brute force is nested loops, O(n²). I'll trade O(n) space for O(n) time with a hash map."* This is where you practice Beat 2.

---

### 1.2 Group Anagrams · LC 49 · Medium · ★★★★★
```python
from collections import defaultdict
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))                # canonical form
        groups[key].append(s)
    return list(groups.values())
```
**Insight:** the whole problem is "what's the canonical key?" **O(n · k log k).**
**Follow-up they will ask:** *"can you avoid the sort?"* → use a 26-length count tuple as the key: `key = tuple(counts)` where `counts[ord(c)-97] += 1`. That's **O(n · k)**. Have this ready.

---

### 1.3 Top K Frequent Elements · LC 347 · Medium · ★★★★★
```python
from collections import Counter
import heapq
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return heapq.nlargest(k, counts.keys(), key=counts.get)   # O(n log k)
```
**But know the O(n) bucket-sort version — this is the follow-up:**
```python
def top_k_frequent_bucket(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]   # index = frequency
    for num, freq in counts.items():
        buckets[freq].append(num)
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```
**Insight:** frequency is bounded by `len(nums)`, so it can index an array. That's the trick that beats the heap.

---

### 1.4 Subarray Sum Equals K · LC 560 · Medium · ★★★★☆
```python
from collections import defaultdict
def subarray_sum(nums: list[int], k: int) -> int:
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1                      # empty prefix — the crucial seed
    running, count = 0, 0
    for num in nums:
        running += num
        count += prefix_counts[running - k]   # how many prefixes make a valid window end here
        prefix_counts[running] += 1
    return count
```
**Insight:** `sum(i..j) = prefix[j] - prefix[i-1]`. So "does a valid subarray end here?" becomes "have I seen `running - k` before?"
**The trap:** `prefix_counts[0] = 1`. Without it you miss every subarray starting at index 0. **Note:** this does *not* work as a sliding window because negatives break monotonicity — say that if they ask.

---

### 1.5 Longest Consecutive Sequence · LC 128 · Medium · ★★★★☆
```python
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 in num_set:
            continue                          # not a sequence start — skip
        length = 1
        while num + length in num_set:
            length += 1
        best = max(best, length)
    return best
```
**Insight:** the `if num - 1 in num_set: continue` guard is what makes this **O(n)** instead of O(n²) — every element is only walked as part of exactly one sequence. **Narrate the amortized argument.** Without that line it looks quadratic and interviewers will challenge you.

---

### 1.6 Also drill
| Problem | LC | Insight |
|---|---|---|
| Valid Anagram | 242 | `Counter(s) == Counter(t)`. Follow-up: unicode? |
| Contains Duplicate II | 219 | Map value → last index; check `i - last <= k`. |
| Product of Array Except Self | 238 | Prefix × suffix, no division. Classic. |
| First Unique Character | 387 | Counter, then scan for `count == 1`. |
| Ransom Note | 383 | Counter subtraction. |
| Isomorphic Strings | 205 | **Two** maps — bijection needs both directions. |
| Word Pattern | 290 | Same as 205 but words. |
| Find All Anagrams in a String | 438 | Hash map **+ sliding window** — bridges Pattern 1 and 3. |

---
---

# PATTERN 2 — TWO POINTERS
> ⚪ **CUT FROM THE 4-DAY PLAN — reference only.** Unconfirmed pattern. Skim only if the diagnostic exposes a gap.

### 2.1 Valid Palindrome · LC 125 · Easy · ★★★★☆
```python
def is_palindrome(s: str) -> bool:
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
**The `lo < hi` guard inside the inner whiles** is the bug everyone ships. Without it, `",."` walks off the end.

---

### 2.2 3Sum · LC 15 · Medium · ★★★★★
> The most-asked two-pointer medium. The difficulty is **duplicates**, not the algorithm.

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    results = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                             # sorted — no way to reach 0 anymore
        if i > 0 and nums[i] == nums[i - 1]:
            continue                          # skip duplicate anchors
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                results.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                   # skip duplicate seconds
    return results
```
**O(n²) / O(1)** extra (ignoring output). **Narrate the three dedup guards separately** — that's what they're grading. Do not use a set of tuples to dedup; it works but reads as avoiding the actual problem.

---

### 2.3 Container With Most Water · LC 11 · Medium · ★★★★☆
```python
def max_area(height: list[int]) -> int:
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, (hi - lo) * min(height[lo], height[hi]))
        if height[lo] < height[hi]:
            lo += 1                           # only moving the shorter side can help
        else:
            hi -= 1
    return best
```
**The proof is the answer.** *"Width always shrinks. So the only way area grows is if height grows. Moving the taller wall can never increase `min(h[lo], h[hi])`. So moving the shorter wall is the only move that can possibly help — that's why greedy is safe here."* **Say this.** Candidates who state the invariant get the point; candidates who just write the code get half.

---

### 2.4 Sort Colors · LC 75 · Medium · ★★★★☆
```python
def sort_colors(nums: list[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1      # Dutch national flag
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:                                 # == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                         # do NOT advance mid — unexamined value swapped in
    return
```
**The trap:** advancing `mid` in the `2` branch. You just swapped in an unknown value from the right. **This is the single most-checked detail in this problem.**

---

### 2.5 Also drill
| Problem | LC | Insight |
|---|---|---|
| Two Sum II (sorted) | 167 | Converge from both ends. |
| Merge Sorted Array | 88 | **Fill from the back** — avoids shifting. |
| Remove Duplicates from Sorted Array | 26 | Slow/fast write pointer. |
| Move Zeroes | 283 | Same slow/fast. |
| Trapping Rain Water | 42 | Hard. Two pointers + running maxes. Stretch goal. |
| Squares of Sorted Array | 977 | Fill from the back — biggest square is at one of the ends. |
| Longest Palindromic Substring | 5 | Expand from each center (2n-1 centers). |

---
---

# PATTERN 3 — SLIDING WINDOW
> ⚪ **CUT FROM THE 4-DAY PLAN — reference only.** Unconfirmed pattern. Skim only if the diagnostic exposes a gap.

### 3.1 Best Time to Buy and Sell Stock · LC 121 · Easy · ★★★★★
```python
def max_profit(prices: list[int]) -> int:
    min_price = float('inf')
    best = 0
    for price in prices:
        min_price = min(min_price, price)
        best = max(best, price - min_price)
    return best
```
Technically a running-min, but it's the mental warm-up for windows. **O(n) / O(1).**

---

### 3.2 Longest Substring Without Repeating Characters · LC 3 · Medium · ★★★★★
```python
def length_of_longest_substring(s: str) -> int:
    last_seen = {}                            # char → last index
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1          # jump — don't crawl
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```
**The trap:** `last_seen[ch] >= left`. Without it, a stale index from *before* the window drags `left` backwards. Test `"abba"` — it's the case that catches it. **Trace `"abba"` out loud in Beat 5**; the interviewer is waiting for exactly that.

---

### 3.3 Longest Repeating Character Replacement · LC 424 · Medium · ★★★★☆
```python
from collections import defaultdict
def character_replacement(s: str, k: int) -> int:
    counts = defaultdict(int)
    left = 0
    max_freq = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] += 1
        max_freq = max(max_freq, counts[ch])
        while (right - left + 1) - max_freq > k:   # replacements needed > budget
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```
**Insight:** `window_size - max_freq` = how many chars you'd have to replace. If that exceeds `k`, shrink.
**The subtle bit interviewers love:** `max_freq` is never decremented, so it can be stale. That's *fine* — a stale max only means the window doesn't grow, never that we return a wrong answer, because `best` only updates when the window is valid. **Volunteering this explanation is a strong signal.**

---

### 3.4 Permutation in String · LC 567 · Medium · ★★★★☆
```python
from collections import Counter
def check_inclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return True
    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1                    # add right
        window[s2[i - len(s1)]] -= 1          # drop left
        if window[s2[i - len(s1)]] == 0:
            del window[s2[i - len(s1)]]       # required for == to work
        if window == need:
            return True
    return False
```
**Fixed-size window.** The `del` on zero matters — `Counter({'a': 0})` != `Counter()`.

---

### 3.5 Also drill
| Problem | LC | Insight |
|---|---|---|
| Max Consecutive Ones III | 1004 | Window where zeros ≤ k. |
| Minimum Size Subarray Sum | 209 | Shrink while `total >= target`. |
| Minimum Window Substring | 76 | Hard. Two counters + a `have/need` counter. Stretch. |
| Find All Anagrams | 438 | Fixed window + Counter. Twin of 567. |
| Sliding Window Maximum | 239 | Hard. **Monotonic deque** — this is the one worth knowing from the hards. |
| Fruit Into Baskets | 904 | "At most 2 distinct" — window with a dict. |

---
---

# PATTERN 7 — INTERVALS & HEAPS
> **SUNDAY, 5:40–6:00** (7.1 and 7.3 only). **Very Voxel** — merging overlapping detection events is literally their problem.

### 7.1 Merge Intervals · LC 56 · Medium · ★★★★★
> **How they'd say it, Voxel-style:** *"A camera fires a detection event every frame while a hazard is present. You get a list of [start, end] timestamps. Collapse overlapping ones into single incidents."* That is exactly what their pipeline does.

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])        # sort by start — always the first move
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # overlap → extend
        else:
            merged.append([start, end])
    return merged
```
**The `max` matters** — `[[1,10],[2,3]]` must stay `[[1,10]]`, not become `[[1,3]]`.
**O(n log n)** dominated by the sort.

---

### 7.2 Meeting Rooms II · LC 253 · Medium · ★★★★★
> **Voxel-style:** *"Given detection events with durations, what's the max number of concurrent incidents? That's how many reviewers we need staffed."*

```python
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []                                 # end times of active meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)               # a room freed up — reuse it
        heapq.heappush(heap, end)
    return len(heap)
```
**Insight:** the heap size *is* the answer — it's the number of rooms in use at peak.
**The alternative worth mentioning:** a sweep line — `+1` at each start, `-1` at each end, sort all events, track the running max. Say *"there's also a sweep-line formulation that generalizes better if you also want to know **when** the peak happened"* — that's the kind of comment that ends a round well.

---

### 7.3 Task Scheduler · LC 621 · Medium · ★★★★☆
> **Directly relevant to your systems round.** Solve it and then say "this is the same starvation problem a real job scheduler has."

```python
from collections import Counter
def least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    max_count = max(counts.values())
    num_maxed = sum(1 for c in counts.values() if c == max_count)
    # (max_count - 1) full frames of size (n + 1), plus the final row
    slots = (max_count - 1) * (n + 1) + num_maxed
    return max(slots, len(tasks))             # if there are enough distinct tasks, no idling
```
**Insight:** it's a math problem, not a simulation. The `max(..., len(tasks))` handles the case where you have so many distinct tasks that idle slots get filled naturally.

---

### 7.4 Also drill
| Problem | LC | Insight |
|---|---|---|
| Insert Interval | 57 | Three phases: before, merge, after. |
| Non-overlapping Intervals | 435 | Greedy — sort by **end**, not start. |
| Kth Largest Element | 215 | Min-heap of size k, or quickselect. |
| Merge k Sorted Lists | 23 | Heap of heads. *"Same as merging k camera streams by timestamp."* |
| Find Median from Data Stream | 295 | Two heaps. Design-y; know it exists. |

---
---

# PATTERN 8 — DESIGN PROBLEMS
> **SUNDAY, 5:40–6:00** (8.2 especially). **These bridge Round 1 and Round 2** — your notes explicitly say to practice "a simple in-memory rate limiter, cache, or event dispatcher class."

### 8.1 LRU Cache · LC 146 · Medium · ★★★★★
> Named in your prep notes. Know it cold.

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)           # mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)    # evict least-recently-used
```
**Use `OrderedDict` first — it's the clean, readable answer and Voxel values clean code.** But **immediately** add: *"`OrderedDict` is doing a hash map plus a doubly-linked list under the hood. If you'd rather I implement that by hand to show the mechanics, I can — it's a `Node` class with `prev`/`next` and sentinel head/tail nodes."* Then do it if they say yes. Volunteering that you know what the library is hiding is the difference between "used a library" and "chose a library."

---

### 8.2 Logger Rate Limiter · LC 359 · Easy · ★★★★★
> **This is the most Voxel-shaped design problem that exists.** "Don't spam the safety manager with the same alert." Your notes mention alert rate limiting and deduplication explicitly.

```python
class Logger:
    def __init__(self):
        self._last_printed = {}               # message → timestamp

    def should_print_message(self, timestamp: int, message: str) -> bool:
        last = self._last_printed.get(message)
        if last is None or timestamp - last >= 10:
            self._last_printed[message] = timestamp
            return True
        return False
```
**The follow-up that decides the round:** *"This map grows forever. What do you do?"*
Have three answers ready:
1. **Lazy cleanup** — sweep expired entries periodically or on every Nth call
2. **Bounded LRU** — cap the map size and accept rare false-allows
3. **Two-bucket rotation** — old/new dicts swapped every window; O(1) amortized cleanup, bounded memory

**Then connect it:** *"At Voxel this is the alert dedup problem — if a forklift parks in a hazard zone, the model fires every frame, and you can't page the manager 30 times a second."*

---

### 8.3 Design Hit Counter · LC 362 · Medium · ★★★★☆
```python
from collections import deque
class HitCounter:
    def __init__(self):
        self._hits = deque()                  # (timestamp, count)

    def hit(self, timestamp: int) -> None:
        if self._hits and self._hits[-1][0] == timestamp:
            self._hits[-1] = (timestamp, self._hits[-1][1] + 1)
        else:
            self._hits.append((timestamp, 1))

    def get_hits(self, timestamp: int) -> int:
        while self._hits and self._hits[0][0] <= timestamp - 300:
            self._hits.popleft()              # expire the window
        return sum(count for _, count in self._hits)
```
**Follow-ups:** "what if hits are out of order?" (sorted structure / accept approximation) · "what if there are millions per second?" (bucket by second in a fixed 300-slot ring buffer).

---

### 8.4 Token Bucket Rate Limiter — not on LeetCode, very likely here
> Your notes literally say *"practice with things like a simple in-memory rate limiter."* Write this from memory.

```python
import time
class TokenBucket:
    """Allow `rate` events/sec, bursting up to `capacity`."""
    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self._tokens = capacity
        self._last = time.monotonic()         # monotonic, NOT time.time()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self._last
        self._last = now
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        if self._tokens >= cost:
            self._tokens -= cost
            return True
        return False
```
**Two things to say out loud:**
1. *"`time.monotonic()` not `time.time()` — wall clock can jump backwards on NTP sync and you'd get negative elapsed."* **This one line makes you sound like you've shipped production code.**
2. *"Tokens refill lazily on access rather than on a timer thread — no background work, and it's exact."*

**Then the trade-off:** *"Token bucket allows bursts, which is usually what you want for alerts — a real incident should be able to fire a few notifications immediately. A fixed window would smooth them out and delay the first one. Sliding window log is exact but O(n) memory per key."*

---

### 8.5 Also drill
| Problem | LC | Insight |
|---|---|---|
| Time Based Key-Value Store | 981 | Map key → sorted list; `bisect_right` on get. |
| Design Twitter | 355 | **Fan-out on read vs write** — the exact trade-off in Design 1. Do this one. |
| Design Underground System | 1396 | Two maps: in-progress and completed averages. |
| Insert Delete GetRandom O(1) | 380 | List + index map; swap-with-last on delete. |

---
---

# PATTERN 9 — LINKED LISTS (low probability, cheap insurance)

| Problem | LC | Insight |
|---|---|---|
| Reverse Linked List | 206 | `prev, cur = None, head`; the three-line dance. Know iterative **and** recursive. |
| Merge Two Sorted Lists | 21 | **Dummy head** — eliminates the empty-list special case. |
| Linked List Cycle | 141 | Floyd's slow/fast. |
| Linked List Cycle II | 142 | Floyd's + the reset-to-head trick to find the entry node. |
| Remove Nth From End | 19 | Two pointers n apart, one pass. |
| Reorder List | 143 | Find middle → reverse second half → interleave. Three sub-problems in one. |

```python
# The one to have cold:
def reverse_list(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev
```

---

# PATTERN 10 — BINARY SEARCH (low probability, cheap insurance)

| Problem | LC | Insight |
|---|---|---|
| Binary Search | 704 | `lo + (hi - lo) // 2`. Get the boundary conditions right. |
| Search in Rotated Sorted Array | 33 | One half is always sorted — figure out which, then decide. |
| Find Minimum in Rotated Sorted Array | 153 | Compare `nums[mid]` to `nums[hi]`, never to `nums[lo]`. |
| Koko Eating Bananas | 875 | **Binary search on the answer.** *"Same as sizing a worker pool — search the throughput space."* |
| First Bad Version | 278 | The template for leftmost-true. |

**The one insight:** most binary search problems aren't "search a sorted array," they're **"binary search the answer space"** — you have a monotonic predicate (`is k enough?`) and you're finding the boundary. Koko is the canonical example. Say this if binary search comes up.

---

# PATTERN 11 — DP (lowest probability — but don't get zeroed)

| Problem | LC | Insight |
|---|---|---|
| Climbing Stairs | 70 | Fibonacci. The "hello world" of DP. |
| House Robber | 198 | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` |
| Coin Change | 322 | Unbounded knapsack. `dp[amount]` from the bottom. |
| Longest Increasing Subsequence | 300 | O(n²) DP, or O(n log n) with patience sorting + bisect. |
| Word Break | 139 | `dp[i] = any(dp[j] and s[j:i] in words)` |
| Unique Paths | 62 | Grid DP; also just a binomial coefficient. |

If DP shows up at all it's `Climbing Stairs` or `House Robber` as the *easy* problem. **Don't over-invest here** — spend that hour on stacks instead. It's not where the evidence points.

---
---

# 🔬 The Friday Diagnostic — run it exactly like this

**Setup:** 45-minute timer. Camera on. Screen recording. Plain editor, **autocomplete off**, no test runner.

**Problem 1 (target: 12 min):** Valid Parentheses (LC 20)
**Problem 2 (target: 25–30 min):** Number of Islands (LC 200)

**Then watch it back and score yourself honestly:**

| | ✅ / ❌ |
|---|---|
| Did I ask clarifying questions before typing? | |
| Did I state the brute force *and* its complexity? | |
| Did I state the optimal complexity **before** coding? | |
| Did I go silent for more than ~15 seconds at any point? | |
| Are my variable names something a stranger could read? | |
| Did I dry-run on a real example before saying "done"? | |
| Did I name at least two edge cases unprompted? | |
| Did I finish in time? | |

**Any ❌ is a point Voxel deducts.** Score it, then apply the decision rule in `00`, §The decision rule — it tells you whether the compressed Code Creation plan is safe for you. Rerun this as the Monday mock (with LC 101 + LC 1249) and compare. **The algorithm was never the hard part — this checklist is.**
