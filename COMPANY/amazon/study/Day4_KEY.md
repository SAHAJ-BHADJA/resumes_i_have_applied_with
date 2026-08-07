# DAY 4 ANSWER KEY — Trees + Grid Traversal

> **The single question to ask yourself on every tree problem:**
> *Am I sending information UP from the children, or DOWN from the parent?*
> - **UP** (return a value, combine children): height, diameter, sum, LCA, max path
> - **DOWN** (pass constraints as parameters): validate BST, path targets, depth tracking
> Get this right in the first 30 seconds and the code writes itself.
>
> **Grid rule:** shortest path ⇒ **BFS**. Reachability / area / count ⇒ **DFS** is fine. Never use DFS for shortest path.

---

## PART A — TREES

### 104. Maximum Depth (UP)
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```
**O(n) / O(h)**

---

### 226. Invert Binary Tree (UP)
```python
def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

---

### 110. Balanced Binary Tree (UP, with a sentinel)
**Insight:** Return height, but use `-1` as "already unbalanced" so you don't recompute heights — that's the difference between O(n) and O(n²).

```python
def isBalanced(root):
    def height(node):
        if not node:
            return 0
        lh = height(node.left)
        if lh == -1:
            return -1
        rh = height(node.right)
        if rh == -1:
            return -1
        if abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)
    return height(root) != -1
```
**O(n) / O(h)** — the naive version calls `maxDepth` inside `isBalanced` and is O(n²). Say that you avoided it.

---

### 543. Diameter of Binary Tree (UP, with a side-effect global)  ★
**Insight:** The classic "return one thing, track another." Return *height* upward; update the *diameter* as a side effect.

```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        best = max(best, lh + rh)        # path THROUGH this node
        return 1 + max(lh, rh)           # but only ONE side goes up
    height(root)
    return best
```
**O(n) / O(h)** — this shape (return one, track another) also solves 124. Recognise it.

---

### 100. Same Tree
```python
def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

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

### 199. Binary Tree Right Side View
```python
from collections import deque
def rightSideView(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:            # last node of the level
                out.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
    return out
```

---

### 103. Zigzag Level Order
```python
from collections import deque
def zigzagLevelOrder(root):
    if not root:
        return []
    out, q, left_to_right = [], deque([root]), True
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right
    return out
```
Reverse the *output list*, not the traversal — much less error-prone.

---

### 98. Validate BST (DOWN)  ★
**Insight:** Checking `left.val < node.val < right.val` locally is **wrong**. You must pass down the allowed range.

```python
def isValidBST(root):
    def check(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))
```
**O(n) / O(h)** — the classic failing test is `[5,4,6,null,null,3,7]`: 3 is a valid left child of 6 locally, but violates the ancestor 5.

---

### 235. LCA of a **BST** (DOWN)
**Insight:** BST ordering tells you which way to walk. No recursion needed.
```python
def lowestCommonAncestorBST(root, p, q):
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur                   # split point = LCA
    return None
```
**O(h) / O(1)**

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

### 105. Construct Binary Tree from Preorder + Inorder ★
**Insight:** Preorder gives you the root; inorder tells you how many nodes are on each side. Use an index map to avoid O(n) searches.

```python
def buildTree(preorder, inorder):
    idx = {v: i for i, v in enumerate(inorder)}
    self_pos = 0

    def build(lo, hi):
        nonlocal self_pos
        if lo > hi:
            return None
        root_val = preorder[self_pos]
        self_pos += 1
        root = TreeNode(root_val)
        mid = idx[root_val]
        root.left = build(lo, mid - 1)   # LEFT FIRST — preorder consumes in that order
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(inorder) - 1)
```
**O(n) / O(n)** — **Gotcha:** left must be built before right, because the shared `self_pos` walks preorder in order.

---

## PART B — GRIDS

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

### 124. Binary Tree Maximum Path Sum ★★
**Same shape as 543:** return one thing, track another. Clamp negatives to 0.
```python
def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)   # drop negative branches
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)     # path through node
        return node.val + max(left, right)            # only one side goes up
    gain(root)
    return best
```
**O(n) / O(h)**

---

### 297. Serialize and Deserialize Binary Tree ★
**Insight:** Preorder with explicit null markers is uniquely decodable. Use an iterator so deserialize is a clean recursion.
```python
class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):
            if not node:
                out.append('#')
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(out)

    def deserialize(self, data):
        vals = iter(data.split(','))
        def build():
            v = next(vals)
            if v == '#':
                return None
            node = TreeNode(int(v))
            node.left = build()
            node.right = build()
            return node
        return build()
```
**O(n) / O(n)** — **null markers are mandatory.** Preorder alone is not uniquely decodable.

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

### 987. Vertical Order Traversal
**Insight:** Sort by (column, row, value). The value tiebreak is what makes this harder than it looks.
```python
from collections import defaultdict
def verticalTraversal(root):
    nodes = defaultdict(list)            # col -> [(row, val)]
    def dfs(node, r, c):
        if not node:
            return
        nodes[c].append((r, node.val))
        dfs(node.left, r + 1, c - 1)
        dfs(node.right, r + 1, c + 1)
    dfs(root, 0, 0)
    return [[val for _, val in sorted(nodes[c])] for c in sorted(nodes)]
```
**O(n log n) / O(n)**

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
