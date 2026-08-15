# Fri Aug 21 — Day 10 of 18
### PHASE 2 — CORE STRUCTURES · Graphs

**Answer key for reference: `Day5_KEY.md`** · Solutions for today's problems are at the bottom of this file.

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

Primitives **14, 15, 16, 17**. Kahn's and Union-Find from memory today.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 20 (+1d), Aug 18 (+3d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **Run this decision tree out loud in the first 60 seconds of any graph problem:**
> - Unweighted shortest path → **BFS**
> - Weighted, non-negative → **Dijkstra**
> - Weighted with a **≤ K edges** cap → **Bellman-Ford** (K rounds, with a snapshot copy)
> - Prerequisites / build order → **topological sort**
> - "Are these connected?" / merging groups → **Union-Find**
> - Cheapest way to connect everything → **MST**
>
> **787 is the trap:** the K-stop cap breaks Dijkstra's greedy invariant. If you reach for Dijkstra there, you'll produce a confidently wrong answer.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 207 | Course Schedule ★ | Topological sort | ____ |
| ☐ | 210 | Course Schedule II | Same, ordered | ____ |
| ☐ | 133 | Clone Graph | Map old→new before recursing | ____ |
| ☐ | 547 | Number of Provinces | Union-Find | ____ |
| ☐ | 721 | Accounts Merge | Union-Find on emails | ____ |
| ☐ | 127 | Word Ladder ★★ | BFS over generated neighbours | ____ |
| ☐ | 542 | 01 Matrix | Multi-source BFS | ____ |
| ☐ | 1091 | Shortest Path in Binary Matrix | 8-dir BFS | ____ |
| ☐ | 743 | Network Delay Time | Dijkstra | ____ |
| ☐ | 787 | Cheapest Flights Within K Stops | Bellman-Ford | ____ |

---

## Block D — Design

**HLD 6 — Distributed Message Queue (SQS-like).**

Cover:
- **API:** `SendMessage`, `ReceiveMessage`, `DeleteMessage`. Note that *receive doesn't delete* — that's the whole design.
- **Visibility timeout:** why it exists (consumer might die mid-processing), and what happens if processing outlives it (duplicate delivery — hence idempotent consumers).
- **Delivery semantics:** at-least-once is the default and the honest one. Exactly-once requires dedup IDs + a dedup window; say what that costs.
- **Ordering:** standard queues don't guarantee it. FIFO queues do, at much lower throughput, via message-group IDs. Explain the trade.
- **Dead-letter queues:** after N failed receives, move it aside so one poison message can't block a partition forever.
- **Storage & scale:** partition by queue, replicate each partition. Long polling vs short polling.
- **Failure:** broker dies holding in-flight messages. What's lost, what's replayed?

---

## Block E — Leadership Principles

**Rehearsal pass — out loud, timed. Stories #6–#10.**

Same criteria: under 2.5 minutes, "I" not "we", ends in a number and an outcome.

Then pick your **two weakest** from #1–#10 and rewrite them tonight.

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

- [ ] Kahn's algorithm and Union-Find from memory, no reference?
- [ ] Did I get the edge direction right in 207? (`[a,b]` = "b before a" = edge `b→a`)
- [ ] Can I say why Dijkstra fails on 787?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

### 1091. Shortest Path in Binary Matrix — 8-directional BFS
```python
from collections import deque
def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n-1][n-1]:
        return -1
    q = deque([(0, 0, 1)])
    grid[0][0] = 1                       # mark blocked = visited
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc, d + 1))
    return -1
```

---

---

### 743. Network Delay Time — Dijkstra
```python
import heapq
from collections import defaultdict
def networkDelayTime(times, n, k):
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
    dist = {}
    pq = [(0, k)]
    while pq:
        d, node = heapq.heappop(pq)
        if node in dist:
            continue                     # already finalised
        dist[node] = d
        for nei, w in adj[node]:
            if nei not in dist:
                heapq.heappush(pq, (d + w, nei))
    return max(dist.values()) if len(dist) == n else -1
```
**O(E log V) / O(V+E)**

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

## PART B — HEAPS

---
