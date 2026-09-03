# Mon Aug 24 — Day 8 of 13
### Heaps & Top-K

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 8.**

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

Primitive **21** (heap idioms) + Tier 2 sweep.

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 215. Kth Largest Element in an Array  ·  *Min-heap of size k ★*  ·  time: ____

**Given** an unsorted array and k. **Return** the kth largest value (in sorted order, not the kth distinct).

#### ☐ 347. Top K Frequent Elements  ·  *Counter + heap*  ·  time: ____

**Given** an array and k. **Return** the k most frequent values, in any order.

#### ☐ 692. Top K Frequent Words  ·  *Mixed sort direction ★*  ·  time: ____

**Given** words and k. **Return** the k most frequent, sorted by count descending then **lexicographically ascending**.

#### ☐ 23. Merge k Sorted Lists  ·  *Heap of heads ★★*  ·  time: ____

**Given** an array of k sorted linked lists. **Return** them merged into one sorted list.

#### ☐ 973. K Closest Points to Origin  ·  *Max-heap of size k ★*  ·  time: ____

**Given** points and k. **Return** the k closest to the origin, in any order.

#### ☐ 295. Find Median from Data Stream  ·  *Two heaps ★★*  ·  time: ____

**Design** a structure that accepts numbers one at a time and can return the running median at any point.

#### ☐ 767. Reorganize String  ·  *Max-heap + hold-back ★*  ·  time: ____

**Given** a string, rearrange it so no two adjacent characters are equal. **Return** any valid result, or "" if impossible.

#### ☐ 621. Task Scheduler  ·  *Formula, not simulation ★*  ·  time: ____

**Given** task labels and a cooldown n, identical tasks must be at least n intervals apart. **Return** the minimum total intervals including idles.

#### ☐ 502. IPO  ·  *Two heaps ★*  ·  time: ____

**Given** k projects you may complete, starting capital w, and each project's profit and capital requirement. **Return** the maximum final capital.

#### ☐ 1834. Single-Threaded CPU  ·  *Heap simulation + idle jump ★*  ·  time: ____

**Given** tasks as [enqueueTime, processingTime], the CPU picks the shortest available task (ties by index) and runs it to completion. **Return** the processing order.

#### ☐ 378. Kth Smallest Element in a Sorted Matrix  ·  *BS on value*  ·  time: ____

**Given** an n×n matrix with sorted rows and columns, and k. **Return** the kth smallest element in the whole matrix.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Bid Fulfillment — ✅ Verified  ·  time: ____

**Prompt:** Fixed `inventory` and a list of requests `[customerId, quantity, bid, timestamp]`. Higher bid gets priority. Within the same bid, allocate **round-robin in increasing timestamp**: each round gives one unit to every still-unfulfilled customer in that bid group. Drop a customer once fully fulfilled. Stop when inventory hits 0. Return the IDs of customers who received **zero** units, in original input order.
**Trap:** it is *not* "sort by bid and give the top customer everything." The equal-bid round-robin is the whole question.

#### ☐ Minimum Possible Cost — ✅ Verified  ·  time: ____

**Prompt:** `n` item types; the `j`-th unit bought of type `i` costs `a[i] + (j-1)*b[i]`. Buy exactly `m` items total, minimising cost.
**Insight:** greedy with a min-heap — always buy the globally cheapest next unit, then push that type's new next price.


---

## Block D — Design

### SD-1. CloudWatch 🟠

Design a distributed monitoring service. Metric and log ingestion at very high throughput · dimensions/tags · time-series storage · aggregation windows · dashboards · alarms (`CPU > 80% for 5 min`) · retention and downsampling · multi-tenancy · out-of-order and delayed data · hot vs cold storage · millions of hosts.
> **Raise cardinality unprompted.** Every extra dimension multiplies series count — that's the thing operators know and candidates miss. Also: *who monitors the monitoring system?*


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Rehearse #1–7 out loud, timed.** Anything over 2.5 min gets cut. Listen for 'we' — change every one to 'I'.

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
