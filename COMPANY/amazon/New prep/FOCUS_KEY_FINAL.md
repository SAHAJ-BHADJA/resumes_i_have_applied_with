# FINAL ANSWER KEY — the 32 problems, Aug 25 → Aug 29

*Every solution executed and asserted. Read the **Trigger** and **Insight** lines first; the code last.*

---

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

### 236. LCA of a Binary Tree (UP) ★★ Amazon favourite
**Insight:** Return the node if you find p or q. If both subtrees return non-null, *this* node is the LCA.

```python
def lowestCommonAncestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root                      # p and q split here
    return left or right                 # both on one side (or neither)
```
**O(n) / O(h)** — do this one twice. Then be ready for "what if p or q might not exist?" (you'd need a found-count).

---

### 102. Binary Tree Level Order Traversal
```python
from collections import deque
def levelOrder(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # snapshot size FIRST
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
```
**O(n) / O(width)** — `for _ in range(len(q))` is the only idea here. Everything else today reuses it.

---

### 1. Two Sum — Hashmap
**Trigger:** find a pair summing to target, unsorted, return indices
**Insight:** For each `x`, the partner is `target - x`. Store what you've *already seen*, so you never match an element with itself.

```python
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```
**O(n) / O(n)** — **Gotcha:** check `seen` *before* inserting `x`, or `[3,3]` with target 6 breaks.

---

### 560. Subarray Sum Equals K — Prefix sum + hashmap  ★★
**Insight:** `sum(i..j) = prefix[j] - prefix[i-1]`. So for each `j`, count how many earlier prefixes equal `prefix[j] - k`.

```python
from collections import defaultdict
def subarraySum(nums, k):
    count = defaultdict(int)
    count[0] = 1                         # the empty prefix
    running = total = 0
    for x in nums:
        running += x
        total += count[running - k]      # look up BEFORE inserting
        count[running] += 1
    return total
```
**O(n) / O(n)** — **Gotcha:** `count[0] = 1` handles subarrays starting at index 0. Forgetting it is the classic bug. Sliding window does **not** work here (negatives allowed).

---

### 3. Longest Substring Without Repeating Characters — the archetype ★★★
**Trigger:** longest substring with all-distinct characters
**Insight:** Window is invalid when a char appears twice. Shrink from the left until it doesn't.

```python
def lengthOfLongestSubstring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1          # jump left past the previous occurrence
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```
**O(n) / O(min(n, charset))**
**Gotcha:** the `last[ch] >= left` check. Without it, a stale occurrence *outside* the window drags `left` backwards.

*Count-map variant (closer to the universal template — know both):*
```python
def lengthOfLongestSubstring_v2(s):
    from collections import defaultdict
    count = defaultdict(int)
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while count[ch] > 1:             # INVALID
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

### 424. Longest Repeating Character Replacement ★
**Trigger:** longest substring after changing at most k characters
**Insight:** A window is valid if `window_length - count_of_most_frequent_char <= k`. Those are the chars you'd have to replace.

```python
from collections import defaultdict
def characterReplacement(s, k):
    count = defaultdict(int)
    left = best = max_freq = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        while (right - left + 1) - max_freq > k:     # INVALID
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```
**O(n) / O(26)**
**The famous subtlety:** `max_freq` is never decreased. That's *intentional* — a stale `max_freq` only makes the window fail to grow, never produce a wrong answer, and the final answer is still correct. Be ready to defend this; interviewers probe it.

---

### 15. 3Sum — Sort + two pointers  ★
**Trigger:** triplets summing to 0, no duplicates in output
**Insight:** Sort, fix `i`, then it's Two-Sum-on-sorted for the rest. Dedupe by skipping equal neighbours — **at both the outer and inner level.**

```python
def threeSum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                                # sorted: no way to reach 0
        if i > 0 and nums[i] == nums[i - 1]:
            continue                             # dedupe the fixed element
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1                      # dedupe the pair
                hi -= 1
    return res
```
**O(n²) / O(1)** extra. **This is the #1 dedup-bug problem.** Do it twice.

---

### 42. Trapping Rain Water — TWO WAYS ★★
**Trigger:** elevation map, trapped water
**Insight:** Water above index `i` = `min(maxLeft[i], maxRight[i]) - height[i]`. Everything else is how you compute those maxima.

**Way A — two pointers, O(1) space (the one to present):**
```python
def trap(height):
    if not height:
        return 0
    lo, hi = 0, len(height) - 1
    left_max, right_max = height[lo], height[hi]
    water = 0
    while lo < hi:
        if left_max < right_max:
            lo += 1
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]   # safe: right side guarantees a wall
        else:
            hi -= 1
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
    return water
```
**O(n) / O(1)**

**Way B — monotonic stack (present as the alternative):**
```python
def trap_stack(height):
    stack, water = [], 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break                     # no left wall
            left = stack[-1]
            width = i - left - 1
            depth = min(height[left], h) - height[bottom]
            water += width * depth
        stack.append(i)
    return water
```
**Key line to say:** "The stack version fills water *horizontally, layer by layer*; the two-pointer version fills it *vertically, column by column*."

---

---

### 56. Merge Intervals ★★ (Amazon favourite)
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])   # sort by START
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)    # max! not just `end`
        else:
            out.append([start, end])
    return out
```
**O(n log n) / O(n)** — **Gotcha:** `max(out[-1][1], end)`. A fully-contained interval like `[1,10],[2,3]` breaks the naive version.

---

### 253. Meeting Rooms II ★★ (Amazon favourite)
**Way A — min-heap of end times (present this):**
```python
import heapq
def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []                            # end times of ongoing meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)          # a room freed up — reuse it
        heapq.heappush(heap, end)
    return len(heap)
```
**Way B — sweep line / chronological ordering (the elegant one):**
```python
def minMeetingRooms_sweep(intervals):
    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)
    rooms = best = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1
            best = max(best, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    return best
```
**O(n log n) / O(n)** — the heap version generalises better to follow-ups; the sweep is easier to explain.

---

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

### 973. K Closest Points to Origin ★ (Amazon favourite)
```python
import heapq
def kClosest(points, k):
    heap = []                            # max-heap of size k, by negative distance
    for x, y in points:
        d = x * x + y * y                # no sqrt needed — monotonic
        heapq.heappush(heap, (-d, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
```
**O(n log k) / O(k)** — **say this:** skipping `sqrt` is safe because it's monotonic. Mention Quickselect for O(n) average.

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

### 875. Koko Eating Bananas
```python
import math
def minEatingSpeed(piles, h):
    def hours_needed(speed):
        return sum(math.ceil(p / speed) for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:       # feasible
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**O(n log(max pile)) / O(1)** — say out loud: "answer space is 1 to max(piles); feasibility is monotonic because eating faster never takes more hours."

---

### 33. Search in Rotated Sorted Array ★★
**Insight:** At any `mid`, **one half is always properly sorted.** Identify which, then test whether the target lies inside that sorted half.
```python
def searchRotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:            # LEFT half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                # RIGHT half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```
**O(log n) / O(1)** — **Gotcha:** `nums[lo] <= nums[mid]` with `<=`, for the 2-element case.

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

### 146. LRU Cache
**Trigger:** fixed-capacity cache, evict the least recently used
**Insight:** Hashmap gives O(1) lookup; doubly linked list gives O(1) reordering. Sentinel head and tail nodes remove every null check.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head = Node()               # most-recent side
        self.tail = Node()               # least-recent side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]        # *** node must store its key ***
```
**get/put O(1) / O(capacity)** — **Gotcha:** the node must carry its own `key`, or you can't delete it from the map on eviction. `OrderedDict` with `move_to_end` is the shortcut, but interviewers usually want the manual version.

---

## 138. Copy List with Random Pointer ★★

### BRUTE FORCE

**Idea**
- Create the copied nodes one at a time as you walk the original.
- For each node's random pointer, figure out its position by counting from the head of the original.
- Then walk that many steps into the copy to find the corresponding node.

**Data Structures Used:** the new nodes; no map.

**Algorithm**
- First create a plain copy of the `next` chain.
- For each original node, walk from the original head counting steps until you reach `node.random`, giving an index.
- Walk that many steps into the copied list to find the clone, and assign it.

**Time Complexity: O(n²).** Every random pointer costs two linear walks.
**Space Complexity: O(n)** for the copied nodes.

### WHY THIS ISN'T GOOD ENOUGH

You're recomputing "which node is this?" over and over. A random pointer can also point *forward* to a node you haven't created yet, which makes single-pass copying awkward. Both problems vanish if you first create every clone, then wire the pointers — and if you keep a direct map from original to clone, lookup becomes O(1) instead of a walk.

### OPTIMAL A — hashmap (lead with this)

**Idea**
- Pass one: create a clone for every original node and record the pairing. Don't link anything yet.
- Pass two: now every clone exists, so `next` and `random` can be set by looking up the clone of whatever the original points at.

**Data Structures Used:** a **hashmap** from original node → cloned node.

**Algorithm**
- Pass one: `old_to_new[cur] = Node(cur.val)` for every node.
- Pass two: `old_to_new[cur].next = old_to_new.get(cur.next)` and `old_to_new[cur].random = old_to_new.get(cur.random)`.
- Use `.get(...)` not `[...]` — `cur.next` is `None` at the tail, and `.get(None)` returns `None` instead of raising `KeyError`.
- Return `old_to_new[head]`.

**Time Complexity: O(n).** Two passes, O(1) hash lookups.
**Space Complexity: O(n)** for the map.

```python
def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}
    cur = head
    while cur:                                # PASS 1: create every clone first
        old_to_new[cur] = Node(cur.val)       # so forward randoms already exist in pass 2
        cur = cur.next
    cur = head
    while cur:                                # PASS 2: wire pointers between clones
        old_to_new[cur].next   = old_to_new.get(cur.next)    # .get handles the None tail
        old_to_new[cur].random = old_to_new.get(cur.random)  # random may be None
        cur = cur.next
    return old_to_new[head]
```

### OPTIMAL B — O(1) space (the follow-up they want)

**Idea**
- Instead of a map, store the pairing *inside the list itself*: put each clone immediately after its original.
- The list temporarily reads `A → A' → B → B' → C → C'`.
- Now the clone of any node `X` is just `X.next`, so `X.random.next` is exactly the clone of `X.random`.
- After setting all randoms, unweave the two lists.

**Data Structures Used:** none — the list structure encodes the map.

**Algorithm**
- Weave: for each original, `cur.next = Node(cur.val, cur.next)` then jump `cur = cur.next.next`.
- Randoms: `if cur.random: cur.next.random = cur.random.next` — read it as *"my clone's random is the clone of my random."*
- Unweave: restore each original's `next` and link the clones together, guarding the tail with `if new.next`.

**Time Complexity: O(n)** — three passes.
**Space Complexity: O(1)** excluding the output.

```python
def copyRandomList_O1(head):
    if not head:
        return None
    cur = head                                # 1. weave: A -> A' -> B -> B'
    while cur:
        cur.next = Node(cur.val, cur.next)    # clone sits right after its original
        cur = cur.next.next                   # skip over the clone we just made
    cur = head                                # 2. set randoms using the weave
    while cur:
        if cur.random:
            cur.next.random = cur.random.next # my clone's random = clone of my random
        cur = cur.next.next
    old, new = head, head.next                # 3. unweave into two separate lists
    new_head = head.next
    while old:
        old.next = old.next.next              # restore the original chain
        new.next = new.next.next if new.next else None   # guard the tail
        old, new = old.next, new.next
    return new_head
```

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

---

### 863. All Nodes Distance K in Binary Tree ★
**Insight:** A tree only has downward edges. Add parent pointers to make it an undirected **graph**, then plain BFS from target.
```python
from collections import deque, defaultdict
def distanceK(root, target, k):
    parent = {}
    def wire(node, par):
        if not node:
            return
        parent[node] = par
        wire(node.left, node)
        wire(node.right, node)
    wire(root, None)

    seen = {target}
    q = deque([target])
    dist = 0
    while q:
        if dist == k:
            return [n.val for n in q]
        for _ in range(len(q)):
            node = q.popleft()
            for nei in (node.left, node.right, parent[node]):
                if nei and nei not in seen:
                    seen.add(nei)
                    q.append(nei)
        dist += 1
    return []
```
**O(n) / O(n)** — "convert the tree to a graph" is a top-5 reusable trick.

---

### 76. Minimum Window Substring — the boss ★★★
**Trigger:** smallest window in s containing all chars of t (with multiplicity)
**Insight:** Track `have` vs `need` as *counts of satisfied characters*, not raw char counts. That makes validity an O(1) check.

```python
from collections import Counter
def minWindow(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    need_count = len(need)               # distinct chars still to satisfy
    window = {}
    have = 0
    left = 0
    best_len = float('inf')
    best_start = 0

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1                    # this char just became satisfied

        while have == need_count:        # VALID -> shrink
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            out = s[left]
            window[out] -= 1
            if out in need and window[out] < need[out]:
                have -= 1                # broke it -> stop shrinking
            left += 1

    return "" if best_len == float('inf') else s[best_start:best_start + best_len]
```
**O(|s| + |t|) / O(|s| + |t|)**
**Gotchas:** (1) `== need[ch]` not `>=`, or you double-count. (2) `< need[out]` not `<=`. (3) Store `best_start` and slice at the end — don't build substrings inside the loop.

---

---

### 239. Sliding Window Maximum ★★
**Trigger:** max of every window of size k
**Insight:** Monotonic **decreasing deque of indices**. The front is always the current max; anything smaller than the incoming value can never be a max again, so pop it.

```python
from collections import deque
def maxSlidingWindow(nums, k):
    dq = deque()                         # indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] < x:
            dq.pop()                     # smaller values are now useless
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                 # front slid out of the window
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
```
**O(n) / O(k)** — each index enters and leaves once. **Gotcha:** evict the front *by index*, not by value.

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

---

### 1011. Capacity To Ship Packages Within D Days
```python
def shipWithinDays(weights, days):
    def days_needed(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = 0
            cur += w
        return d

    lo, hi = max(weights), sum(weights)  # lo = must fit the heaviest item
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**Gotcha:** `lo = max(weights)`, not 1 — a capacity smaller than the largest package is impossible.

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
