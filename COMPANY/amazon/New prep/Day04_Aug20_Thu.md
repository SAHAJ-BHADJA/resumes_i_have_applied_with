# Thu Aug 20 — Day 4 of 13
### Trees

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 4.**

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Open `ANSWER_KEY.md` and read only the *Trigger* and *Insight* lines — never the code. Close it, keep going. At 20 min read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

---

## TODAY'S CHECKLIST

| ☐ | Block | Full (~7h) | Compressed (~4.5h) |
|---|---|---|---|
| ☐ | A — Primitives from memory | 40 min | 30 min |
| ☐ | B — Re-solve queue | 30 min | 20 min |
| ☐ | C — Problems / mock | 3h 30m | 2h 15m |
| ☐ | D — Design | 60 min | 40 min |
| ☐ | E — Leadership Principles | 45 min | 25 min |
| ☐ | F — Solution book | 20 min | 15 min |

> **13 days, not 18.** If you fall behind inside a day, drop from the **bottom** of Block C. The ★ problems stay — those are the ones that recur in Amazon loops. Never cut Block B; re-solves build recall, and recall is the thing that's broken.

---

## Block A — Primitives (from memory, timed)

Primitives **12, 13** (tree BFS level snapshot, tree DFS up/down).

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 104. Maximum Depth of Binary Tree  ·  *UP*  ·  time: ____

**Given** a binary tree. **Return** the number of nodes on the longest root-to-leaf path.

#### ☐ 110. Balanced Binary Tree  ·  *UP with −1 sentinel*  ·  time: ____

**Given** a binary tree. **Return** whether every node's two subtrees differ in height by at most 1. **Watch:** the naive version is O(n²).

#### ☐ 543. Diameter of Binary Tree  ·  *Return one, track another ★*  ·  time: ____

**Given** a binary tree. **Return** the length of the longest path between any two nodes, measured in edges.

#### ☐ 102. Binary Tree Level Order Traversal  ·  *BFS level snapshot*  ·  time: ____

**Given** a binary tree. **Return** its values grouped level by level, top to bottom.

#### ☐ 199. Binary Tree Right Side View  ·  *BFS, last of level*  ·  time: ____

**Given** a binary tree. **Return** the values visible when looking at it from the right, top to bottom.

#### ☐ 662. Maximum Width of Binary Tree  ·  *Heap indexing ★*  ·  time: ____

**Given** a binary tree. **Return** the maximum width of any level, counting null gaps between the outermost non-null nodes.

#### ☐ 124. Binary Tree Maximum Path Sum  ·  *Same shape as 543 ★★*  ·  time: ____

**Given** a binary tree. **Return** the largest sum along any path between any two nodes (the path need not pass through the root).

#### ☐ 98. Validate Binary Search Tree  ·  *DOWN — pass the range*  ·  time: ____

**Given** a binary tree. **Return** whether it's a valid BST. **Watch:** comparing only against direct children is wrong — an ancestor can be violated.

#### ☐ 230. Kth Smallest Element in a BST  ·  *Iterative inorder*  ·  time: ____

**Given** a BST and k. **Return** the kth smallest value. **Follow-up:** frequent queries.

#### ☐ 105. Construct Binary Tree from Preorder and Inorder  ·  *Index map*  ·  time: ____

**Given** preorder and inorder traversals of a tree with unique values. **Return** the reconstructed tree.

#### ☐ 236. Lowest Common Ancestor of a Binary Tree  ·  *Both sides non-null ★★*  ·  time: ____

**Given** a binary tree and two nodes. **Return** their lowest common ancestor. A node may be its own ancestor.

#### ☐ 297. Serialize and Deserialize Binary Tree  ·  *Preorder + null markers ★*  ·  time: ____

**Design** methods to encode a binary tree to a string and decode it back. Any format is allowed as long as it round-trips.

#### ☐ 863. All Nodes Distance K in Binary Tree  ·  *Tree → graph ★*  ·  time: ____

**Given** a binary tree, a target node, and k. **Return** every node exactly k edges from the target.

#### ☐ 437. Path Sum III  ·  *Prefix sum + backtrack ★*  ·  time: ____

**Given** a binary tree and a target. **Return** how many downward paths (any start, any end) sum to the target.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Tree Kyoukai — 🟡 LeetCode 545 Boundary of Binary Tree  ·  time: ____

**Prompt:** return the tree boundary anticlockwise: root, then the left boundary top-down (excluding leaves), then all leaves left-to-right, then the right boundary bottom-up (excluding leaves). No node twice.

#### ☐ Employee Directory — 🟡 Design  ·  time: ____

**Prompt:** model employees (`id`, `name`, `manager`, `directReports`) and support: lookup by id, prefix search by name, and "everyone beneath employee X."


---

## Block D — Design

### LLD-4. Shipping Cost 🟡

Compute shipping cost from weight, dimensions, origin/destination zone, carrier, and service level.
- **Classes:** `ShippingCostCalculator` · `ShippingStrategy`/`Carrier` interface · `StandardShipping`, `ExpressShipping` · `RegionalPricing` · `Package`, `Address`
- **Patterns:** **Strategy** (carrier/service) · **Factory** (carrier selection) · **Decorator** (surcharges: fuel, residential, insurance)
- **Key domain detail to raise unprompted:** **dimensional (volumetric) weight** = `(L×W×H) / divisor`, and you charge on `max(actual, dimensional)`. Mentioning this shows domain thinking.
- **Follow-ups:** add a carrier without changing callers · zone lookup tables · surcharge stacking order · free-shipping thresholds · cheapest-carrier fallback


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Stories #7–8.** Targets: **Invent and Simplify**, **Earn Trust**.


**STAR+ format, ~250 words each:** Situation (2 sentences) · Task (what *you* owned) · **Action (60% of the story)** · Result (**with a number**) · + Learning.

**Two failure modes:** saying "we" (the interviewer cannot score "we"), and stories with no ending.

---

## Block F — Solution book (20 min)

Written **after** the session, **with your editor closed**, **from memory**. Reproducing the code from memory is a second free retrieval rep — that's where most of the value is.

```
#____  ______________________     Date: ____   Mode: ☐ solo  ☐ GPT voice
Time taken: ____ min    Result: ☐ clean  ☐ hint  ☐ ran over  ☐ failed

TRIGGER   (what in the wording should have told me the pattern?)
PATTERN
THOUGHT PROCESS  1. first thing I tried  2. why it failed  3. what made me switch
THE CODE  (from memory, editor closed)
COMPLEXITY  Time O(__) because ____   Space O(__) because ____
             ("one pass" is not a reason. "each index is pushed and popped once" is.)
THE BUG I HIT
EDGE CASES  ☐ empty ☐ single ☐ all-duplicates ☐ negatives ☐ ____
RE-SOLVE:  +1d ____   +3d ____
```

---

## END OF DAY — honest check

- [ ] Did I narrate out loud on every problem, or did I go quiet?
- [ ] Did I state my approach and ask for buy-in **before** coding?
- [ ] Did I dry-run without being prompted?
- [ ] Primitives from memory, no reference?
- [ ] Re-solve queue cleared?
