# Wed Aug 19 — Day 3 of 13
### Stacks, Monotonic Stacks & Linked Lists

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 3.**

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

Primitives **7, 8, 9, 19, 25** (fast/slow, reverse list, dummy-head merge, monotonic stack, LRU).

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 20. Valid Parentheses  ·  *Stack*  ·  time: ____

**Given** a string of `()[]{}`. **Return** whether every bracket is correctly opened and closed in order.

#### ☐ 155. Min Stack  ·  *Store running min*  ·  time: ____

**Design** a stack supporting push, pop, top, and `getMin` — all in **O(1)**.

#### ☐ 150. Evaluate Reverse Polish Notation  ·  *Truncate toward zero*  ·  time: ____

**Given** tokens in postfix notation. **Return** the evaluated result. **Watch:** division truncates toward zero.

#### ☐ 394. Decode String  ·  *Stack of state*  ·  time: ____

**Given** an encoded string like `3[a2[c]]`. **Return** the expansion. Nesting is arbitrary; repeat counts may be multi-digit.

#### ☐ 739. Daily Temperatures  ·  *Monotonic stack*  ·  time: ____

**Given** daily temperatures. **Return** for each day how many days until a warmer one, or 0.

#### ☐ 735. Asteroid Collision  ·  *Stack comparison*  ·  time: ____

**Given** asteroids where sign is direction and magnitude is size, moving right-movers and left-movers collide and the smaller explodes (both if equal). **Return** the survivors.

#### ☐ 84. Largest Rectangle in Histogram  ·  *Increasing stack + sentinel ★★*  ·  time: ____

**Given** bar heights of equal width. **Return** the area of the largest rectangle fitting inside the histogram.

#### ☐ 206. Reverse Linked List  ·  *prev/cur/next*  ·  time: ____

**Given** a linked list. **Return** it reversed. Know both the iterative and recursive versions.

#### ☐ 21. Merge Two Sorted Lists  ·  *Dummy head*  ·  time: ____

**Given** two sorted linked lists. **Return** one sorted list built by splicing the nodes together.

#### ☐ 142. Linked List Cycle II  ·  *Floyd + reset ★*  ·  time: ____

**Given** a linked list. **Return** the node where the cycle begins, or null. O(1) space.

#### ☐ 19. Remove Nth Node From End of List  ·  *Dummy + gap*  ·  time: ____

**Given** a linked list and n. **Return** the list with the nth node from the end removed, in one pass.

#### ☐ 143. Reorder List  ·  *Three primitives composed*  ·  time: ____

**Given** a list L0→L1→…→Ln, reorder it in place to L0→Ln→L1→Ln−1→… Values may not be changed.

#### ☐ 138. Copy List with Random Pointer  ·  *Both ways ★★*  ·  time: ____

**Given** a linked list where each node also has a random pointer to any node or null. **Return** a deep copy. **Follow-up:** O(1) extra space.

#### ☐ 148. Sort List  ·  *Merge sort on a list ★*  ·  time: ____

**Given** a linked list. **Return** it sorted, in O(n log n) time and O(log n) space.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ VM Load — ✅ Verified (pattern)  ·  time: ____

**Prompt:** route each request to the **least-loaded** server, breaking ties by lowest index. Return the target server per request (or the final loads).

#### ☐ Block Words — 🟡 Trie / Aho–Corasick  ·  time: ____

**Prompt:** given text and a list of blocked words, determine whether the text contains any blocked word.
**Clarify first:** substring vs whole-word matching, case sensitivity, punctuation. GPT's research confirmed the core but not these rules — and they change the algorithm.


---

## Block D — Design

### LLD-3. Query Builder 🟠

A fluent, SQL-like builder: `select(...).from(...).where(...).and(...).orderBy(...).limit(...).build()`.
- **Classes:** `QueryBuilder` (fluent, returns `this`) · `Predicate`/`Condition` hierarchy · `Query`
- **Patterns:** **Builder** · **Composite** (nested AND/OR) · optionally **Interpreter** for the expression tree · **Strategy** for SQL dialects
- **Follow-ups:** nested grouping `(a OR b) AND c` · parameterisation and injection safety · joins and aggregations · builder immutability/reuse · multiple dialects


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Stories #5–6.** Targets: **Bias for Action**, **Have Backbone / Disagree and Commit**.


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
