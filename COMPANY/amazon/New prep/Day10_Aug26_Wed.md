# Wed Aug 26 — Day 10 of 13
### Intervals, Greedy & DP Part 1

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 10.**

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

Primitive **24** (DP skeletons) + Tier 1 sweep.

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 56. Merge Intervals  ·  *Sort by START ★★*  ·  time: ____

**Given** a list of intervals. **Return** them with all overlapping intervals merged.

#### ☐ 57. Insert Interval  ·  *Three phases*  ·  time: ____

**Given** a sorted, non-overlapping interval list and one new interval. **Return** the list after inserting and merging.

#### ☐ 435. Non-overlapping Intervals  ·  *Sort by END*  ·  time: ____

**Given** intervals. **Return** the minimum number to remove so the rest don't overlap.

#### ☐ 253. Meeting Rooms II  ·  *Heap and sweep-line ★★*  ·  time: ____

**Given** meeting intervals. **Return** the minimum number of rooms needed to hold them all.

#### ☐ 1288. Remove Covered Intervals  ·  *Sort (start↑, end↓)*  ·  time: ____

**Given** intervals, remove any interval covered by another. **Return** how many remain.

#### ☐ 759. Employee Free Time  ·  *Flatten, merge, gaps ★*  ·  time: ____

**Given** each employee's sorted busy intervals. **Return** the finite intervals where **all** employees are free.

#### ☐ 55. Jump Game  ·  *Greedy reach*  ·  time: ____

**Given** an array of max jump lengths. **Return** whether the last index is reachable from index 0.

#### ☐ 45. Jump Game II  ·  *BFS-on-array levels*  ·  time: ____

**Given** an array where each value is the max jump length from that index. **Return** the minimum jumps to reach the last index (always reachable).

#### ☐ 134. Gas Station  ·  *Restart on deficit ★*  ·  time: ____

**Given** gas[i] at each station and cost[i] to reach the next, on a circular route. **Return** the starting index that lets you complete the loop, or −1. The answer is unique.

#### ☐ 70. Climbing Stairs  ·  *Fibonacci*  ·  time: ____

**Given** n stairs, climbing 1 or 2 at a time. **Return** the number of distinct ways to reach the top.

#### ☐ 198. House Robber  ·  *Skip-or-take*  ·  time: ____

**Given** amounts in each house along a street, you cannot rob two adjacent houses. **Return** the maximum you can take.

#### ☐ 213. House Robber II  ·  *Circular → two linear*  ·  time: ____

Same as House Robber, but the houses are in a **circle** — the first and last are adjacent.

#### ☐ 322. Coin Change  ·  *Unbounded knapsack ★★*  ·  time: ____

**Given** coin denominations and an amount. **Return** the fewest coins summing to the amount, or −1. Coins are unlimited. **Watch:** greedy is wrong.

#### ☐ 518. Coin Change II  ·  *Loop order = comb vs perm*  ·  time: ____

**Given** an amount and coin denominations. **Return** the number of distinct combinations making that amount. **Watch:** loop order decides combinations vs permutations.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Minimum Shipment — ✅ Verified  ·  time: ____

**Prompt:** `warehouses[i]` is the warehouse holding item `i`. Each shipment sends either two items **from different warehouses** or one item alone. Minimise shipments.
**Insight:** closed form. Let `f` = largest warehouse count, `n` = total. If `f > n − f` the surplus must ship alone, giving `f`. Otherwise everything pairs up: `ceil(n/2)`.

#### ☐ Minimize Absolute Differences — ✅ Verified  ·  time: ____

**Prompt:** arrays `a`, `b` of length `n`. Pair each `a[i]` with a distinct `b[j]`. Minimise `Σ |a[i] − b[π(i)]|`.
**Insight:** sort both and pair in order. The exchange argument: if `a1<a2` are paired to `b1>b2`, swapping never increases the sum.

#### ☐ Permutation Sorter — ✅ Verified  ·  time: ____

**Prompt:** a permutation of `1..n`. Two operations: (1) reverse the whole array, (2) move the first element to the end. Minimum operations to sort ascending; input is guaranteed sortable.
**Insight:** the array must be a rotation of ascending or of descending. Only three shapes are reachable cheaply — check each.


---

## Block D — Design

### SD-3. Financial Dashboard ✅ (verified as a real reported onsite scenario)

Aggregate a user's financial data across several **external providers**: balances, holdings, crypto, transactions, derived portfolio metrics. Providers differ in schema, refresh frequency, rate limits, outages, and partial responses.
- Design: provider **adapters** → normalisation → canonical model → current state + historical snapshots
- Must handle: retries, idempotency, reconciliation, provider corrections, permissions, **staleness exposed to the user rather than silently wrong totals**
> The distinguishing requirement is *never show a silently inconsistent total.* Lead with that.


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Rewrite the 4 weakest stories.** Any without a number in the Result gets a number.

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
