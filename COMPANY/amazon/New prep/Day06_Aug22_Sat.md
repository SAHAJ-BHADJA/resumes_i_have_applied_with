# Sat Aug 22 — Day 6 of 13
### Graphs  *(weekend — full track)*

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 6.**

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

Primitives **14, 15, 16, 17** (graph BFS, Kahn's topo sort, cycle detection, Union-Find).

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 207. Course Schedule  ·  *Topological sort ★*  ·  time: ____

**Given** numCourses and prerequisite pairs [a,b] meaning b must come before a. **Return** whether all courses can be finished.

#### ☐ 210. Course Schedule II  ·  *Same, ordered*  ·  time: ____

Same setup as Course Schedule. **Return** a valid completion order, or an empty array if impossible.

#### ☐ 133. Clone Graph  ·  *Register before recursing*  ·  time: ____

**Given** a reference to a node in a connected undirected graph. **Return** a deep copy. **Watch:** cycles.

#### ☐ 547. Number of Provinces  ·  *Union-Find*  ·  time: ____

**Given** an adjacency matrix of cities. **Return** the number of connected groups.

#### ☐ 721. Accounts Merge  ·  *Union-Find on emails*  ·  time: ____

**Given** accounts as [name, email…], merge accounts sharing any email. **Return** each merged account with its name followed by sorted emails.

#### ☐ 127. Word Ladder  ·  *BFS over generated neighbours ★★*  ·  time: ____

**Given** beginWord, endWord and a dictionary. **Return** the number of words in the shortest transformation chain changing one letter at a time, where every intermediate word is in the dictionary. 0 if impossible.

#### ☐ 399. Evaluate Division  ·  *Weighted graph DFS ★*  ·  time: ____

**Given** equations like a/b = 2.0 and queries. **Return** each query's value by chaining relations, or −1 when undetermined.

#### ☐ 684. Redundant Connection  ·  *Union-Find*  ·  time: ____

**Given** a graph that is a tree plus one extra edge. **Return** the edge that can be removed, choosing the last one in the input if several qualify.

#### ☐ 802. Find Eventual Safe States  ·  *Reverse graph + topo ★*  ·  time: ____

**Given** a directed graph. **Return** the sorted nodes from which every possible path reaches a terminal node.

#### ☐ 310. Minimum Height Trees  ·  *Peel leaves ★*  ·  time: ____

**Given** a tree as n nodes and n−1 edges. **Return** every root choice that minimises the tree's height. **Note:** there are at most two.

#### ☐ 752. Open the Lock  ·  *BFS on state space*  ·  time: ____

**Given** a 4-wheel lock starting at "0000", a list of deadends, and a target. **Return** the minimum turns, or −1.

#### ☐ 787. Cheapest Flights Within K Stops  ·  *Bellman-Ford ★*  ·  time: ____

**Given** flights with prices, a source, a destination, and k. **Return** the cheapest price using **at most k stops**, or −1. **Watch:** the stop cap breaks Dijkstra.

#### ☐ 542. 01 Matrix  ·  *Multi-source BFS*  ·  time: ____

**Given** a binary matrix. **Return** each cell's distance to the nearest 0 (4-directional).


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Conversion Rate — ✅ Verified (LeetCode 399 shape)  ·  time: ____

**Prompt:** given rates like `USD→EUR = 0.9`, answer arbitrary conversion queries by chaining. Reverse edges are reciprocals. Return `-1` when no path exists.

#### ☐ Friendship Path — 🟡 BFS  ·  time: ____

**Prompt:** given friendships and two users, return the shortest chain connecting them.


---

## Block D — Design

### LLD-6. Validation Framework 🟠

Register rules — not-null, length, regex, range, custom — run them against an object, aggregate results.
- **Classes:** `Validator<T>` interface returning `ValidationResult` · `ValidationRule<T>` · `NotNullValidator`, `LengthValidator`, `RegexValidator` · `CompositeValidator` · `ValidationError`
- **Patterns:** **Chain of Responsibility** + **Composite** · **Specification** (AND/OR composition of rules) · **Builder** to assemble rule sets
- **Follow-ups:** collect-all vs fail-fast · cross-field and conditional validation · rule severity · async/remote validators · i18n error messages · **add a rule without modifying the engine**
- *Closely related and widely reported: "design Unix `find`" using the Specification pattern. If you can do one you can do the other.*


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Stories #11–12.** Targets: **Think Big**, **Are Right, A Lot**.


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
