# Thu Aug 27 — Day 11 of 13
### DP Part 2 & Design-in-Code

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 11.**

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

Primitives **20, 24, 25** (Trie, DP skeletons, LRU).

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 139. Word Break  ·  *1D over prefixes*  ·  time: ____

**Given** a string and a dictionary. **Return** whether the string can be segmented entirely into dictionary words (words reusable).

#### ☐ 53. Maximum Subarray  ·  *Kadane*  ·  time: ____

**Given** an integer array. **Return** the largest sum of any contiguous subarray (at least one element).

#### ☐ 152. Maximum Product Subarray  ·  *Track both extremes*  ·  time: ____

**Given** an integer array (may contain negatives and zeros). **Return** the largest product of any contiguous subarray.

#### ☐ 918. Maximum Sum Circular Subarray  ·  *total − minSum ★*  ·  time: ____

**Given** a **circular** array. **Return** the maximum non-empty subarray sum, where a subarray may wrap around once.

#### ☐ 300. Longest Increasing Subsequence  ·  *Both versions ★★*  ·  time: ____

**Given** an array. **Return** the length of the longest strictly increasing subsequence. **Follow-up:** O(n log n).

#### ☐ 1143. Longest Common Subsequence  ·  *2D two-string ★*  ·  time: ____

**Given** two strings. **Return** the length of their longest common subsequence (not substring).

#### ☐ 72. Edit Distance  ·  *2D two-string*  ·  time: ____

**Given** two strings. **Return** the minimum number of insert / delete / replace operations to turn the first into the second.

#### ☐ 416. Partition Equal Subset Sum  ·  *0/1, backwards*  ·  time: ____

**Given** an array of positive integers. **Return** whether it can be split into two subsets of equal sum.

#### ☐ 494. Target Sum  ·  *Reduce to subset-sum ★*  ·  time: ____

**Given** an array and a target, assign + or − to each element. **Return** how many assignments reach the target.

#### ☐ 62. Unique Paths  ·  *2D grid*  ·  time: ____

**Given** an m×n grid, a robot starts top-left and may move only right or down. **Return** how many distinct paths reach the bottom-right.

#### ☐ 64. Minimum Path Sum  ·  *2D grid*  ·  time: ____

**Given** a grid of non-negative costs, moving only right or down. **Return** the minimum total cost from top-left to bottom-right.

#### ☐ 146. LRU Cache  ·  *Hashmap + DLL ★★*  ·  time: ____

**Design** a fixed-capacity cache with `get(key)` and `put(key,value)`, both **O(1)**, evicting the least recently used entry when full.

#### ☐ 211. Design Add and Search Words  ·  *Trie + wildcard DFS*  ·  time: ____

**Design** a structure supporting `addWord` and `search`, where a search string may contain `.` matching any single letter.

#### ☐ 380. Insert Delete GetRandom O(1)  ·  *Array + index map ★*  ·  time: ____

**Design** a set supporting insert, remove, and uniform-random element access — **all in average O(1)**.

#### ☐ 981. Time Based Key-Value Store  ·  *Sorted list + BS*  ·  time: ____

**Design** a store with `set(key,value,timestamp)` and `get(key,timestamp)` returning the value at the largest timestamp ≤ the query.

#### ☐ 588. Design In-Memory File System  ·  *Nested dicts = Trie ★*  ·  time: ____

**Design** a file system supporting `ls`, `mkdir`, `addContentToFile`, and `readContentFromFile`. `ls` on a file returns its name; on a directory, its sorted contents.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Binary String Errors — ✅ Verified  ·  time: ____

**Prompt:** `errorString` of `0`,`1`,`!`; integers `x`,`y`. Replace every `!` with `0` or `1`. Each subsequence `01` costs `x`; each `10` costs `y`. Minimise total cost, mod 1e9+7.
**Insight (the whole problem):** the optimal assignment of the `!`s has **threshold structure** — all `0`s then all `1`s, or all `1`s then all `0`s. Among the `!`s themselves, mixing costs more. So enumerate the split point and evaluate in O(1) per step.

#### ☐ Warehouse Stock — ✅ Verified  ·  time: ____

**Prompt:** `stock[0..n-1]`, each either `-1` (missing) or a known value in `1..200`. Replace every `-1` with a value in `1..200` so that `a[0] <= a[1]`, `a[n-1] <= a[n-2]`, and `a[i] <= max(a[i-1], a[i+1])` for interior `i`. Count valid completions mod `998244353`.
**Insight:** the constraints say exactly **"no strict local maximum anywhere."** Sweep left to right with a two-state DP: state 1 = "this element is already satisfied because it's ≤ its left neighbour"; state 0 = "it still needs the next element to be ≥ it." Prefix sums make each step O(V).

#### ☐ Config Reconstruction — ✅ Verified  ·  time: ____

**Prompt:** digit string `config`, integers `x`,`y`. Start `curr = 0`. Repeatedly add `x` or `y` to `curr` and append `curr % 10` to a generated string. Find the **shortest** generated string that contains `config` as a subsequence.
**Insight:** only `curr % 10` matters, so the state space is tiny — BFS over `(last_digit, matched_prefix_length)`, 10 × (len+1) states.


---

## Block D — Design

### SD-4. Jihanki Network 🟠

*Jihanki* (自販機) = vending machine. Design a platform managing a large fleet: registration · per-machine inventory · purchase events · pricing · cashless payment · health telemetry · online/offline status · restocking · remote configuration · low-stock alerts · retries when machines lose connectivity · central analytics.
> The **LLD core is the classic vending-machine state machine** (State pattern: Idle → HasMoney → Dispensing). Be ready to drop from the fleet architecture down into that. If asked for one round, ask which level they want.


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Full LP run — all 14 + the mandatory set, timed.**

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
