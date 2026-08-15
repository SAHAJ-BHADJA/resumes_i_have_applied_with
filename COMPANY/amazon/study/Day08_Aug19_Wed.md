# Wed Aug 19 — Day 8 of 18
### PHASE 2 — CORE STRUCTURES · Trees, Part 2

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

Primitives **12, 13** + Tier 1 sweep.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 18 (+1d), Aug 16 (+3d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **The 98 trap:** checking `left.val < node.val < right.val` locally is *wrong*. Failing case: `[5,4,6,null,null,3,7]` — 3 is a valid left child of 6 locally but violates the ancestor 5. You must pass the range **down**.
>
> **"Convert the tree to a graph with parent pointers" (863) is a top-5 reusable trick.** Remember it.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 98 | Validate BST | DOWN — pass the range | ____ |
| ☐ | 235 | LCA of a BST | Walk using ordering | ____ |
| ☐ | 236 | LCA of Binary Tree ★★ (do twice) | UP — both sides non-null | ____ |
| ☐ | 105 | Construct from Preorder + Inorder | Index map | ____ |
| ☐ | 297 | Serialize and Deserialize ★ | Preorder + null markers | ____ |
| ☐ | 863 | All Nodes Distance K ★ | Tree → graph | ____ |
| ☐ | 987 | Vertical Order Traversal | Sort by (col,row,val) | ____ |

---

## Block D — Design

**HLD 5 — Usage Metering & Billing Pipeline.**
*AWS Platform in Herndon publicly owns contractual billing systems.*

Cover:
- **Ingest:** millions of usage events/sec from every service. Buffer where? (queue / stream)
- **Aggregation:** per-customer, per-service, per-hour rollups. Streaming aggregation vs batch — and why you probably need both (lambda architecture, or a single stream engine with reprocessing).
- **The hard requirement: no double-billing, ever.** Idempotency keys on every event. Exactly-once is a lie at the transport layer — you get at-least-once delivery plus idempotent processing. Say it that way.
- **Late-arriving events:** an event timestamped 03:00 arrives at 05:00 and the 03:00 window is closed. Watermarks, grace periods, and a correction/adjustment path.
- **Auditability:** a customer disputes a bill. Can you reconstruct the exact events? Immutable event log, retention.
- **Failure:** the aggregator crashes mid-window. Checkpointing, replay from offset.

---

## Block E — Leadership Principles

**Write LP stories #13 and #14.**

Targets: **Frugality** + the mandatory **"tell me about a time you failed."**

The failure story is asked in almost every loop and is where people are weakest. Requirements: a real failure with real consequences, *your* fault (not "my teammate dropped the ball"), what it cost, what you changed afterwards, and evidence the change stuck. No redemption arc where it secretly turns out fine.

**You now have all 14 stories drafted. From here it's rehearsal, not writing.**

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

- [ ] 236 LCA — solved twice, cleanly, from a blank page?
- [ ] Can I explain the 98 failing case without looking?
- [ ] All 14 stories drafted, each ending in a number?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

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

---
