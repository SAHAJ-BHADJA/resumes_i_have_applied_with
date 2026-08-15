# Tue Aug 18 — Day 7 of 18
### PHASE 2 — CORE STRUCTURES · Trees, Part 1

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

Primitives **12, 13**.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 15 (+3d), Aug 17 leftovers.

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **Ask this out loud on every tree problem, before coding:**
> *"Am I sending information UP from the children, or DOWN from the parent?"*
> - **UP** (return a value, combine children): height, diameter, sum, LCA, max path
> - **DOWN** (pass constraints as parameters): validate BST, path targets, depth tracking
>
> Get it right in 30 seconds and the code writes itself.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 104 | Maximum Depth | UP | ____ |
| ☐ | 226 | Invert Binary Tree | UP | ____ |
| ☐ | 100 | Same Tree | Parallel recursion | ____ |
| ☐ | 110 | Balanced Binary Tree | UP with −1 sentinel | ____ |
| ☐ | 543 | Diameter of Binary Tree ★ | Return one, track another | ____ |
| ☐ | 102 | Level Order Traversal | BFS level snapshot | ____ |
| ☐ | 199 | Right Side View | BFS, last of level | ____ |
| ☐ | 103 | Zigzag Level Order | BFS + reverse output | ____ |
| ☐ | 124 | Binary Tree Maximum Path Sum ★★ | Same shape as 543 | ____ |

---

## Block D — Design

**HLD 4 — Authorization / IAM Policy Evaluation Service.**
*Herndon publicly hosts AWS Identity and the Automated Reasoning in Identity team. This is the highest-probability design topic at your site — prepare it properly.*

Cover:
- **The request path:** principal + action + resource + context → allow/deny. Explicit deny always wins.
- **Latency:** this sits in front of *every* API call. Sub-10ms p99 is the requirement. That constraint drives every other decision.
- **Caching:** cache the *decision* or the *policy*? Decision caching is faster but harder to invalidate. What's your TTL and what does it cost you in staleness?
- **Propagation:** a customer revokes access — how long until every host honours it? Say the number and defend it.
- **Fail-closed.** Unlike a rate limiter, an authz service that fails open is a security incident. Be explicit that you know the difference.
- **Scale:** policy evaluation is CPU-bound. Where does it run — centrally, or as a sidecar/library on every host?
- **Blast radius:** cell-based architecture so one bad policy push affects 1/N of customers.

---

## Block E — Leadership Principles

**Write LP stories #11 and #12.**

Targets: **Think Big** · **Are Right, A Lot**

Think Big: *you proposed something bigger than your remit* — a platform instead of a fix, a rewrite instead of a patch — and what happened.
Are Right, A Lot: *you made a judgement call on thin evidence and it held up.* Say what signals you used. This one needs the reasoning, not just the outcome.

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

- [ ] Can I state UP vs DOWN for each of today's problems?
- [ ] 124 and 543 — did I notice they're the same shape and say so?
- [ ] IAM: can I explain why authz fails closed but rate limiting fails open?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 104. Maximum Depth (UP)
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```
**O(n) / O(h)**

---

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

---

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

---
