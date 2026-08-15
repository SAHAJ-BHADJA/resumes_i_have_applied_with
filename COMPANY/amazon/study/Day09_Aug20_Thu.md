# Thu Aug 20 — Day 9 of 18
### PHASE 2 — CORE STRUCTURES · Grids

**Answer key for reference: `Day4_KEY.md`** · Solutions for today's problems are at the bottom of this file.

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

Primitives **10, 11**. Grid BFS/DFS must be typed without thinking by tonight.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 19 (+1d), Aug 17 (+3d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **The rule: shortest path ⇒ BFS. Always. Never DFS.** Reachability, area, and counting are fine with DFS.
>
> **Grid *counting* marks visited permanently. Grid *path* problems must un-mark (79).** That's the single difference between 200 and 79.
>
> **Always ask: "May I modify the input grid?"** If no, use a `visited` set. Asking scores points.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 200 | Number of Islands ★★ (both BFS and DFS) | Grid traversal | ____ |
| ☐ | 695 | Max Area of Island | DFS returning count | ____ |
| ☐ | 733 | Flood Fill | DFS + guard | ____ |
| ☐ | 130 | Surrounded Regions | Start from the border | ____ |
| ☐ | 994 | Rotting Oranges ★★ | Multi-source BFS | ____ |
| ☐ | 417 | Pacific Atlantic Water Flow | Reverse flow from oceans | ____ |
| ☐ | 79 | Word Search | DFS **with** backtracking | ____ |

---

## Block D — Design

**LLD 3 — Elevator System.**

Cover:
- **Classes:** `ElevatorSystem`, `Elevator`, `Request` (internal vs external), `Floor`, `SchedulingStrategy`
- **State machine per car:** IDLE / MOVING_UP / MOVING_DOWN / DOORS_OPEN. Draw the legal transitions.
- **Two request types:** external (floor + direction) and internal (destination floor). They're handled differently — say why.
- **Scheduling behind an interface:** FCFS vs SCAN/elevator algorithm vs nearest-car. Strategy pattern again.
- **Multi-car dispatch:** which elevator answers a hall call? What's your cost function?
- **Concurrency:** the request queue is written by many floors, read by the scheduler.
- **Edge cases:** overload sensor, emergency stop, a car out of service mid-journey.

---

## Block E — Leadership Principles

**First rehearsal pass — out loud, timed. Stories #1–#5.**

- Any story over **2.5 minutes** gets cut down. Time them.
- Listen for "we." Every "we" becomes "I."
- Listen for stories that end without a concrete outcome. "And then it got deprioritised" is a non-answer — fix or replace those.

Expect these to be flabby on the first pass. That's what the pass is for.

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

- [ ] Grid BFS and DFS from memory, under 90 seconds each?
- [ ] 994: did I remember the `fresh == 0` early return and `while q and fresh`?
- [ ] Did any of stories #1–5 run over 2.5 minutes?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

### 733. Flood Fill
```python
def floodFill(image, sr, sc, color):
    start = image[sr][sc]
    if start == color:
        return image                     # *** or you infinite-loop ***
    rows, cols = len(image), len(image[0])
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or image[r][c] != start:
            return
        image[r][c] = color
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
    dfs(sr, sc)
    return image
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

## STRETCH

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

## DAY 4 PATTERN TRIGGERS

| If the problem says... | Reach for |
|---|---|
| "depth / height / diameter / max path sum" | DFS returning a value **up**, track best in a nonlocal |
| "validate BST / path must satisfy a range" | DFS passing constraints **down** |
| "level by level / right side / zigzag / min depth" | BFS with `for _ in range(len(q))` |
| "lowest common ancestor", BST | walk down using ordering |
| "lowest common ancestor", general tree | return node if found; both sides non-null ⇒ LCA |
| "reconstruct tree from traversals" | preorder gives root, inorder gives the split; index map |
| "distance K from a node in a tree" | add parent pointers → graph → BFS |
| count islands / regions / area | DFS, mark visited permanently |
| **shortest** path / minimum time in a grid | **BFS** — never DFS |
| something spreads from many sources at once | multi-source BFS, seed all sources |
| "enclosed / surrounded / can't reach the edge" | invert it: start from the border |
| find a *path* spelling a word | DFS **with backtracking** — restore the cell |

---
