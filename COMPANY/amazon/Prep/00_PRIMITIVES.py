"""
THE 25 PRIMITIVES — daily drill reference
=========================================
Goal: type each of these from memory in under 90 seconds, zero syntax errors.
Method: blank file -> type from memory -> compare against this -> delete -> repeat tomorrow.

Do NOT copy-paste from here. Look, close, type.
"""

from collections import deque, defaultdict, Counter
import heapq

# =============================================================
# TIER 1 — must be reflexive (drill EVERY day)
# =============================================================

# ---- 1. Binary search, exact match --------------------------
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:                      # <= because lo==hi is a valid candidate
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ---- 2. lower_bound / upper_bound ---------------------------
def lower_bound(nums, target):
    """First index with nums[i] >= target. Returns len(nums) if none."""
    lo, hi = 0, len(nums)                # hi = len, NOT len-1
    while lo < hi:                       # < because hi is exclusive
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def upper_bound(nums, target):
    """First index with nums[i] > target."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ---- 3. BINARY SEARCH ON THE ANSWER  *** highest value *** ---
def binary_search_answer(lo, hi, feasible):
    """
    Find the SMALLEST x in [lo, hi] where feasible(x) is True.
    Requires monotonicity: F F F T T T
    For the LARGEST x that is feasible: flip to `if feasible(mid): lo = mid`
    with mid = (lo + hi + 1) // 2 to avoid infinite loop.
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid                     # mid might be the answer -> keep it
        else:
            lo = mid + 1
    return lo


# ---- 4. Variable-size sliding window ------------------------
def longest_valid_window(s):
    """Archetype. Expand right always; shrink left only while invalid."""
    window = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        while len(window) > 2:           # <-- the INVALID condition
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


# ---- 5. Fixed-size sliding window ---------------------------
def max_sum_fixed(nums, k):
    cur = sum(nums[:k])
    best = cur
    for i in range(k, len(nums)):
        cur += nums[i] - nums[i - k]     # add new, drop old
        best = max(best, cur)
    return best


# ---- 6. Two pointers, opposite ends -------------------------
def two_pointer_opposite(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []


# ---- 7. Fast / slow pointer ---------------------------------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def find_middle(head):
    """Returns 2nd middle for even length. Start fast=head.next for 1st middle."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# ---- 8. Reverse a linked list, iterative --------------------
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next                   # save
        cur.next = prev                  # flip
        prev = cur                       # advance
        cur = nxt
    return prev


# ---- 9. Merge two sorted lists (DUMMY HEAD) -----------------
def merge_two(a, b):
    dummy = ListNode()
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b                   # attach the remainder
    return dummy.next


# ---- 10. Grid BFS -------------------------------------------
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def grid_bfs(grid, starts):
    rows, cols = len(grid), len(grid[0])
    q = deque(starts)
    seen = set(starts)
    steps = 0
    while q:
        for _ in range(len(q)):          # level = one step
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols \
                        and (nr, nc) not in seen and grid[nr][nc] != 1:
                    seen.add((nr, nc))
                    q.append((nr, nc))
        steps += 1
    return steps


# ---- 11. Grid DFS / flood fill ------------------------------
def grid_dfs(grid, r, c, target):
    rows, cols = len(grid), len(grid[0])
    if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != target:
        return 0
    grid[r][c] = '#'                     # mark visited IN PLACE
    total = 1
    for dr, dc in DIRS:
        total += grid_dfs(grid, r + dr, c + dc, target)
    return total


# ---- 12. Tree BFS level order -------------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # *** snapshot the size FIRST ***
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out


# ---- 13. Tree DFS — the three shapes ------------------------
def inorder(root, out=None):
    if out is None:
        out = []
    if root:
        inorder(root.left, out)
        out.append(root.val)             # preorder: before; postorder: after
        inorder(root.right, out)
    return out

def dfs_return_up(root):
    """Shape A: compute from children upward (height, sum, diameter)."""
    if not root:
        return 0
    return 1 + max(dfs_return_up(root.left), dfs_return_up(root.right))

def dfs_pass_down(root, lo, hi):
    """Shape B: carry constraints downward (validate BST, path sums)."""
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return dfs_pass_down(root.left, lo, root.val) and \
           dfs_pass_down(root.right, root.val, hi)


# =============================================================
# TIER 2 — must be solid (drill every other day)
# =============================================================

# ---- 14. Graph BFS on adjacency list ------------------------
def graph_bfs(adj, start):
    q = deque([start])
    dist = {start: 0}
    while q:
        node = q.popleft()
        for nei in adj[node]:
            if nei not in dist:
                dist[nei] = dist[node] + 1
                q.append(nei)
    return dist


# ---- 15. Topological sort — Kahn's --------------------------
def topo_sort(n, edges):
    """edges = [(u, v)] meaning u must come before v."""
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in adj[node]:
            indeg[nei] -= 1
            if indeg[nei] == 0:
                q.append(nei)
    return order if len(order) == n else []   # [] means a cycle exists


# ---- 16. Cycle detection, directed (3-colour) ---------------
def has_cycle_directed(n, adj):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(u):
        color[u] = GRAY                  # on the current recursion stack
        for v in adj[u]:
            if color[v] == GRAY:
                return True              # back edge -> cycle
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK                 # fully explored, safe
        return False

    return any(color[i] == WHITE and dfs(i) for i in range(n))


# ---- 17. Union-Find -----------------------------------------
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                 # already connected
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True


# ---- 18. Backtracking template ------------------------------
def backtrack_template(nums):
    res, path = [], []

    def bt(start):
        res.append(path[:])              # *** COPY, not path ***
        for i in range(start, len(nums)):
            path.append(nums[i])         # choose
            bt(i + 1)                    # explore
            path.pop()                   # un-choose

    bt(0)
    return res


# ---- 19. Monotonic stack ------------------------------------
def next_greater(nums):
    """Decreasing stack of INDICES -> next strictly greater element."""
    res = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = x         # x is the answer for that index
        stack.append(i)
    return res
# Increasing stack (pop while nums[stack[-1]] > x) -> next SMALLER element.


# ---- 20. Trie -----------------------------------------------
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

    def _walk(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def startsWith(self, prefix):
        return self._walk(prefix) is not None


# ---- 21. Heap idioms ----------------------------------------
def heap_idioms(nums, k):
    heapq.heapify(nums)                          # O(n) min-heap in place
    smallest = heapq.heappop(nums)

    max_heap = [-x for x in nums]                # max-heap via negation
    heapq.heapify(max_heap)
    largest = -heapq.heappop(max_heap)

    # k largest: keep a MIN-heap of size k
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)                     # evict the smallest
    kth_largest = h[0] if h else None

    # tuple heap: sorts by first element, then second
    th = [(2, 'b'), (1, 'a')]
    heapq.heapify(th)

    heapq.heappushpop(h, 5)                      # push then pop (cheaper)
    return smallest, largest, kth_largest


# ---- 22. Prefix sum + hashmap -------------------------------
def subarrays_summing_to_k(nums, k):
    count = defaultdict(int)
    count[0] = 1                         # *** the empty prefix — memorise this ***
    running = 0
    total = 0
    for x in nums:
        running += x
        total += count[running - k]      # look up BEFORE inserting
        count[running] += 1
    return total


# =============================================================
# TIER 3 — know cold, lower frequency
# =============================================================

# ---- 23. Dijkstra -------------------------------------------
def dijkstra(adj, start, n):
    """adj[u] = [(v, weight)]"""
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                     # stale entry, skip
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


# ---- 24. DP skeletons ---------------------------------------
def dp_1d(nums):
    """House Robber shape: dp[i] depends on dp[i-1], dp[i-2]."""
    if not nums:
        return 0
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def dp_2d_grid(grid):
    """Min path sum shape. Base row and base column FIRST."""
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])
    return dp[-1][-1]


# ---- 25. LRU Cache (hashmap + doubly linked list) -----------
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
        self._add_front(node)            # touch = move to front
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
            del self.map[lru.key]        # *** must delete by KEY -> store key in node ***
