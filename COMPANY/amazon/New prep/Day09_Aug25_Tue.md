# Tue Aug 25 — Day 9 of 13
### Binary Search (incl. binary search on the answer)

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 9.**

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

Primitives **1, 2, 3** — drill **#3 hardest**.

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 704. Binary Search  ·  *Template*  ·  time: ____

**Given** a sorted array and a target. **Return** its index or −1, in O(log n).

#### ☐ 34. Find First and Last Position  ·  *Two boundary searches*  ·  time: ____

**Given** a sorted array with duplicates and a target. **Return** the first and last index of the target, or [−1,−1]. O(log n).

#### ☐ 33. Search in Rotated Sorted Array  ·  *One half is sorted ★★*  ·  time: ____

**Given** a sorted array rotated at an unknown pivot, and a target. **Return** its index or −1, in O(log n).

#### ☐ 153. Find Minimum in Rotated Sorted Array  ·  *Compare against hi*  ·  time: ____

**Given** a sorted array of distinct values rotated at an unknown pivot. **Return** the minimum, in O(log n).

#### ☐ 162. Find Peak Element  ·  *Follow the ascent*  ·  time: ____

**Given** an array where no two adjacent values are equal. **Return** the index of any element greater than both neighbours, in O(log n). Out-of-bounds counts as −∞.

#### ☐ 540. Single Element in a Sorted Array  ·  *Parity binary search ★*  ·  time: ____

**Given** a sorted array where every value appears twice except one. **Return** the single value in O(log n) time and O(1) space.

#### ☐ 74. Search a 2D Matrix  ·  *Flatten*  ·  time: ____

**Given** a matrix where each row is sorted and each row's first value exceeds the previous row's last. **Return** whether a target exists, in O(log(mn)).

#### ☐ 240. Search a 2D Matrix II  ·  *Staircase*  ·  time: ____

**Given** a matrix where each row and each column is sorted ascending (but rows aren't globally ordered). **Return** whether a target exists.

#### ☐ 875. Koko Eating Bananas  ·  *BS on answer ★*  ·  time: ____

**Given** banana piles and h hours, Koko eats at speed k per hour (one pile at a time, remainder of the hour wasted). **Return** the minimum k that finishes in time.

#### ☐ 1011. Capacity To Ship Packages Within D Days  ·  *BS on answer ★*  ·  time: ____

**Given** package weights (shipped in order) and days. **Return** the minimum ship capacity that finishes within the days.

#### ☐ 410. Split Array Largest Sum  ·  *Same function as 1011 ★*  ·  time: ____

**Given** an array and k. Split it into k non-empty contiguous subarrays. **Return** the minimised largest subarray sum.

#### ☐ 1552. Magnetic Force Between Two Balls  ·  *BS on answer, LARGEST variant ★*  ·  time: ____

**Given** basket positions and m balls. **Return** the **largest** possible minimum gap between any two balls.

#### ☐ 528. Random Pick with Weight  ·  *Prefix + BS ★*  ·  time: ____

**Design** a structure that, given weights, returns an index with probability proportional to its weight.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Inconvenience — ✅ Verified  ·  time: ____

**Prompt:** binary grid, `1` = service center. Distance is **Chebyshev**: `max(|dx|, |dy|)`. The grid's inconvenience is the maximum, over all `0` cells, of the distance to the nearest center. You may flip **at most one** `0` to `1`. Minimise inconvenience.
**Insight:** binary search the answer. For a candidate `d`, the cells still uncovered must all fit inside one Chebyshev ball of radius `d` — which is a rectangle test on their bounding box.

#### ☐ Optimal Packing — 🟡 LeetCode 1889 Minimum Space Wasted From Packaging  ·  time: ____

**Prompt:** choose a **single** supplier whose boxes fit all packages (each package in one box ≥ its size), minimising total wasted space. Return −1 if impossible, mod 1e9+7.
**Insight:** sort packages, prefix sums, then binary search each box size to find how many packages it absorbs.

#### ☐ Travel Time — ✅ Verified (Chinese source)  ·  time: ____

**Prompt:** `m` hubs in a circle (hub 1 adjacent to hub `m`). `transitionTime[i]` is the travel time on the edge between hub `i+1` and hub `i+2` (wrapping). Start at hub 1 and visit `requestedHubs` **in order**, choosing clockwise or counter-clockwise per leg. Return minimum total time.
**Insight:** prefix sums round the circle. One direction is `|pref[b] − pref[a]|`; the other is `total − that`.


---

## Block D — Design

### SD-2. Config Distribution 🟠

Publish config changes and distribute them safely to a huge fleet. Versioning · push vs poll · very low read latency · staged rollout and rollback · audit history · regional/global · local caching · **clients that boot while the control plane is down** · stale config · eventual vs strong consistency · watch/subscribe API · failure isolation.
> This is the distributed sibling of LLD-1. Say **"the data plane needs static stability — hosts keep serving with their cached config even if the control plane is unavailable."**


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Rehearse #8–14 out loud, timed.**

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
