# DAY 5 ANSWER KEY — Graphs + Heaps

> **Graph decision tree — run this in the first 60 seconds:**
> - Unweighted shortest path → **BFS**
> - Weighted, non-negative → **Dijkstra**
> - Weighted, ≤ K edges / K stops → **Bellman-Ford** (K rounds)
> - Ordering with prerequisites → **topological sort**
> - "Are these connected?" / merging groups → **Union-Find**
> - Minimum cost to connect everything → **MST** (Prim/Kruskal)
>
> **Heap decision tree:**
> - "K largest" → **min**-heap of size K. "K smallest" → **max**-heap of size K. (Yes, inverted. Memorise it.)
> - "streaming median" → two heaps
> - "always process the most/least X next" → heap-driven simulation

---

## PART A — GRAPHS

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

### 373. K Pairs with Smallest Sums
**Insight:** Seed with `(nums1[i], nums2[0])`. Popping `(i, j)` only ever unlocks `(i, j+1)`.
```python
import heapq
def kSmallestPairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(heap)
    out = []
    while heap and len(out) < k:
        _, i, j = heapq.heappop(heap)
        out.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j+1], i, j + 1))
    return out
```
**O(k log k) / O(k)**

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

## STRETCH

### 1584. Min Cost to Connect All Points — MST (Prim)
```python
import heapq
def minCostConnectPoints(points):
    n = len(points)
    visited = set()
    pq = [(0, 0)]                        # (cost, point index)
    total = 0
    while len(visited) < n:
        cost, i = heapq.heappop(pq)
        if i in visited:
            continue
        visited.add(i)
        total += cost
        xi, yi = points[i]
        for j in range(n):
            if j not in visited:
                xj, yj = points[j]
                heapq.heappush(pq, (abs(xi-xj) + abs(yi-yj), j))
    return total
```
**O(n² log n) / O(n²)**

---

### 990. Satisfiability of Equality Equations — Union-Find
**Insight:** Process **all** `==` first, then check `!=` against the resulting components.
```python
def equationsPossible(equations):
    parent = {c: c for c in 'abcdefghijklmnopqrstuvwxyz'}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for eq in equations:
        if eq[1] == '=':
            parent[find(eq[0])] = find(eq[3])
    for eq in equations:
        if eq[1] == '!' and find(eq[0]) == find(eq[3]):
            return False
    return True
```
Two-pass ordering is the whole insight.

---

### 269. Alien Dictionary ★
**Insight:** Build edges from the **first differing character** of adjacent words, then topological sort.
```python
from collections import defaultdict, deque
def alienOrder(words):
    adj = defaultdict(set)
    indeg = {c: 0 for w in words for c in w}
    for a, b in zip(words, words[1:]):
        for ca, cb in zip(a, b):
            if ca != cb:
                if cb not in adj[ca]:
                    adj[ca].add(cb)
                    indeg[cb] += 1
                break
        else:
            if len(a) > len(b):
                return ""                # "abc" before "ab" is invalid
    q = deque([c for c in indeg if indeg[c] == 0])
    out = []
    while q:
        c = q.popleft()
        out.append(c)
        for nei in adj[c]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                q.append(nei)
    return ''.join(out) if len(out) == len(indeg) else ""
```
**Gotcha:** the prefix case (`for...else`). Miss it and you fail a hidden test.

---

### 1192. Critical Connections (Tarjan bridges) ★
**Insight:** An edge `(u,v)` is a bridge iff the subtree at `v` has no back-edge reaching `u` or above: `low[v] > disc[u]`.
```python
from collections import defaultdict
def criticalConnections(n, connections):
    adj = defaultdict(list)
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    disc = [-1] * n
    low = [0] * n
    res = []
    timer = [0]

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in adj[u]:
            if v == parent:
                continue
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    res.append([u, v])   # bridge
            else:
                low[u] = min(low[u], disc[v])   # back edge: use disc, not low

    dfs(0, -1)
    return res
```
**O(V+E) / O(V+E)** — if you don't know Tarjan, say so honestly and offer the O(E·(V+E)) "remove each edge and test connectivity" version. Honest fallback scores better than a fumbled Tarjan.

---

### 1235. Maximum Profit in Job Scheduling — DP + binary search
```python
import bisect
def jobScheduling(startTime, endTime, profit):
    jobs = sorted(zip(endTime, startTime, profit))
    ends = [0]                           # end times, ascending
    best = [0]                           # best profit achievable by that end time
    for e, s, p in jobs:
        i = bisect.bisect_right(ends, s) - 1      # last job ending <= s
        cand = best[i] + p
        if cand > best[-1]:
            ends.append(e)
            best.append(cand)
    return best[-1]
```
**O(n log n) / O(n)**

---

## DAY 5 PATTERN TRIGGERS

| If the problem says... | Reach for |
|---|---|
| "prerequisites / build order / dependencies" | topological sort (Kahn's) |
| "can it be completed / is there a cycle" | topo sort, check `len(order) == n` |
| "shortest path", unweighted | BFS |
| "shortest/cheapest path", weighted | Dijkstra |
| "at most K stops/edges" | **Bellman-Ford** with a snapshot copy — not Dijkstra |
| "connected components / merge groups / same set?" | Union-Find |
| "minimum cost to connect all nodes" | MST (Prim with a heap) |
| "word transformation / minimum moves" | BFS over generated neighbours |
| "deep copy a graph" | hashmap old→new, register before recursing |
| "top K / Kth largest" | min-heap of size K |
| "top K with a tie-break in the opposite direction" | negate one key in the tuple |
| "median of a stream" | two heaps, balanced |
| "merge K sorted things" | heap of K heads, with an index tiebreaker |
| "arrange so no two adjacent are equal" | max-heap + hold-back previous |
| "schedule with cooldown n" | the `(maxFreq-1)*(n+1)+numMax` formula |
| "single edge whose removal disconnects" | Tarjan bridges |
