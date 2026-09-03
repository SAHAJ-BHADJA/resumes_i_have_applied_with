# Fri Aug 21 — Day 5 of 13
### Grids & Backtracking

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 5.**

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

Primitives **10, 11, 18** (grid BFS, grid DFS, backtracking template).

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 200. Number of Islands  ·  *Both BFS and DFS ★★*  ·  time: ____

**Given** a grid of '1' (land) and '0' (water). **Return** the number of islands, where an island is land connected 4-directionally.

#### ☐ 695. Max Area of Island  ·  *DFS returning count*  ·  time: ____

**Given** a binary grid. **Return** the area of the largest 4-directionally connected island, or 0.

#### ☐ 130. Surrounded Regions  ·  *Start from the border*  ·  time: ____

**Given** a board of 'X' and 'O', flip every 'O' region that is **not** connected to a border. In place.

#### ☐ 417. Pacific Atlantic Water Flow  ·  *Reverse flow ★*  ·  time: ____

**Given** a height grid where the Pacific touches the top/left and the Atlantic the bottom/right, and water flows to equal-or-lower neighbours. **Return** every cell draining to both oceans.

#### ☐ 994. Rotting Oranges  ·  *Multi-source BFS ★★*  ·  time: ____

**Given** a grid of empty / fresh / rotten oranges, each minute rotten oranges rot 4-adjacent fresh ones. **Return** the minutes until none are fresh, or −1.

#### ☐ 79. Word Search  ·  *DFS **with** backtracking*  ·  time: ____

**Given** a character grid and a word. **Return** whether the word can be spelled by moving between adjacent cells, **using each cell at most once per path**.

#### ☐ 78. Subsets  ·  *Template*  ·  time: ____

**Given** an array of distinct integers. **Return** every possible subset (the power set).

#### ☐ 46. Permutations  ·  *used[] array*  ·  time: ____

**Given** an array of distinct integers. **Return** every possible ordering.

#### ☐ 39. Combination Sum  ·  *Reuse allowed*  ·  time: ____

**Given** distinct candidates and a target. **Return** all unique combinations summing to the target; **each candidate may be reused unlimited times**.

#### ☐ 22. Generate Parentheses  ·  *Prune during generation ★*  ·  time: ____

**Given** n. **Return** every well-formed combination of n pairs of parentheses.

#### ☐ 212. Word Search II  ·  *Trie + DFS + pruning ★★*  ·  time: ____

**Given** a character grid and a list of words. **Return** every word that can be spelled on the board (adjacent cells, no cell reused per word).


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Gold Thief — 🟡 LeetCode 1219 Path with Maximum Gold  ·  time: ____

**Prompt:** grid where `0` is empty and positive values are gold. Start anywhere with gold, move 4-directionally, collect on visit, never revisit a cell, never step on `0`. Maximise gold collected.

#### ☐ XO Game — 🟡 LeetCode 348 Design Tic-Tac-Toe  ·  time: ____

**Prompt:** design an `n × n` tic-tac-toe. `move(row, col, player)` returns `0` (no winner), `1`, or `2`. Follow-up: **O(1) per move**, no board rescan.


---

## Block D — Design

### LLD-5. Spell Checker 🟡

Load a dictionary; `isValid(word)`; `suggest(word)` returning plausible corrections.
- **Classes:** `Dictionary` backed by a **Trie** (or HashSet) · `SpellChecker` · `SuggestionStrategy` (**Strategy**)
- **Algorithms:** edit distance 1 (insert/delete/replace/transpose) or bounded Trie traversal; **BK-tree** as the fuzzy-match follow-up
- **Follow-ups:** ranking suggestions by frequency · large-dictionary memory · capitalisation and punctuation · context-aware correction · `suggest(word, maxDistance, maxSuggestions)`
- *Note: this is the one LLD title with a published Amazon-framed write-up (a mock, not a confirmed loop).*


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Stories #9–10.** Targets: **Insist on the Highest Standards**, **Learn and Be Curious**.


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
