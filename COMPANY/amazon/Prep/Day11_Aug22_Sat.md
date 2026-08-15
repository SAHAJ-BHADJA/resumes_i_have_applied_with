# Sat Aug 22 — Day 11 of 18
### PHASE 2 — CORE STRUCTURES · Heaps + Top-K  *(weekend — full track)*

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

Primitive **21** + full Tier 2 sweep.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

**Once a week (today), handwrite the primitives instead of typing them.** It slows you down enough that you're genuinely retrieving rather than letting your fingers pattern-complete. Good honesty check.

---

## Block B — Re-solve queue (cold, blank page)

Aug 21 (+1d), Aug 19 (+3d), Aug 15 (+7d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **Memorise the inversion: "K largest" ⇒ MIN-heap of size K. "K smallest" ⇒ MAX-heap of size K.** Yes, it's backwards from intuition. That's why it's worth memorising.
>
> **23 will raise `TypeError` without the index tiebreaker** — Python tries to compare `ListNode` objects when the values tie.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 215 | Kth Largest Element ★ | Min-heap of size k | ____ |
| ☐ | 347 | Top K Frequent Elements | Counter + heap | ____ |
| ☐ | 692 | Top K Frequent Words ★ | Mixed sort direction | ____ |
| ☐ | 23 | Merge k Sorted Lists ★★ | Heap of heads | ____ |
| ☐ | 767 | Reorganize String ★ | Max-heap + hold-back | ____ |
| ☐ | 621 | Task Scheduler ★ | Formula, not simulation | ____ |
| ☐ | 295 | Find Median from Data Stream ★★ | Two heaps | ____ |
| ☐ | 373 | K Pairs with Smallest Sums | Heap of frontier | ____ |

**Stretch — only if the core block is done and clean:**

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 1584 | Min Cost to Connect All Points | MST / Prim | ____ |
| ☐ | 269 | Alien Dictionary | Topo sort on chars | ____ |
| ☐ | 1192 | Critical Connections | Tarjan bridges | ____ |
| ☐ | 1235 | Maximum Profit in Job Scheduling | DP + binary search | ____ |

---

## Block D — Design

**HLD 7 — Monitoring & Alarming (CloudWatch-like).**

Cover:
- **Ingest:** millions of metric data points/sec. Push vs pull (agent posts vs scraper polls) — and why AWS chose push.
- **Storage:** time-series. Why a general-purpose DB struggles: append-heavy, time-ordered, queried by range. Rollups/downsampling — keep 1-second data for hours, 1-minute for days, 1-hour for years.
- **Cardinality** is the killer. Every extra dimension multiplies series count. Say this — it's the thing people who've operated these systems know.
- **Alarm evaluation:** periodic evaluation over a window, with M-of-N datapoints to avoid flapping. Where does evaluation run and how does it scale with alarm count?
- **Alert storms:** one root cause fires 400 alarms. Grouping, suppression, dependency-aware silencing.
- **The meta-question they love: who monitors the monitoring system?** Have an answer.

---

## Block E — Leadership Principles

**Rehearsal — stories #11–#14, timed.**

Then the **mandatory set**, which gets asked regardless of principle:
- [ ] *Tell me about yourself* — **90 seconds, rehearsed word-for-word.** This is the first thing every interviewer hears; do not improvise it.
- [ ] *Most impactful project*
- [ ] *Why Amazon / why this team*

For "why this team": you know it's an AWS office. If your recruiter named the team, use it. If not, speak to AWS infrastructure and platform work specifically — not generic "I love Amazon's culture."”

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

- [ ] Two-heap median: can I explain the push-to-small-then-move-to-large dance?
- [ ] 621: do I know the formula and the `max(..., len(tasks))` clamp?
- [ ] Is "tell me about yourself" actually rehearsed, or am I planning to wing it?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

---

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

---
