# Tue Aug 18 — Day 2 of 13
### Sliding Window & Prefix Sum

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 2.**

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

Primitives **3, 4, 5, 22** (binary search on answer, variable + fixed window, prefix sum + hashmap).

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 3. Longest Substring Without Repeating Characters  ·  *The archetype ★★★*  ·  time: ____

**Given** a string. **Return** the length of the longest substring with no repeated characters.

#### ☐ 424. Longest Repeating Character Replacement  ·  *Window + max_freq*  ·  time: ____

**Given** a string and k. You may change up to k characters. **Return** the longest possible substring of one repeating letter.

#### ☐ 209. Minimum Size Subarray Sum  ·  *Shortest variant*  ·  time: ____

**Given** an array of **positive** integers and a target. **Return** the length of the shortest contiguous subarray with sum ≥ target, or 0.

#### ☐ 438. Find All Anagrams in a String  ·  *Fixed window*  ·  time: ____

**Given** strings s and p. **Return** the start indices of every substring of s that is an anagram of p.

#### ☐ 567. Permutation in String  ·  *Fixed window*  ·  time: ____

**Given** s1 and s2. **Return** whether s2 contains any permutation of s1 as a substring.

#### ☐ 76. Minimum Window Substring  ·  *have/need counters ★★★*  ·  time: ____

**Given** strings s and t. **Return** the shortest substring of s containing every character of t **including duplicates**, or "".

#### ☐ 992. Subarrays with K Different Integers  ·  *atMost(K)−atMost(K−1) ★★*  ·  time: ____

**Given** an array and k. **Return** the number of contiguous subarrays containing **exactly** k distinct values.

#### ☐ 1658. Minimum Operations to Reduce X to Zero  ·  *Invert to longest middle ★*  ·  time: ____

**Given** an array and x, remove elements from either end summing exactly to x. **Return** the minimum removals, or −1.

#### ☐ 239. Sliding Window Maximum  ·  *Monotonic deque ★★*  ·  time: ____

**Given** an array and window size k. **Return** the maximum of every window as it slides one step at a time.

#### ☐ 974. Subarray Sums Divisible by K  ·  *Prefix mod K*  ·  time: ____

**Given** an array and k. **Return** the number of contiguous subarrays whose sum is divisible by k.

#### ☐ 525. Contiguous Array  ·  *Map 0→−1*  ·  time: ____

**Given** a binary array. **Return** the length of the longest subarray with equal numbers of 0s and 1s.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Destination Cache — 🟠 LRU shape (title verified, prompt not recovered)  ·  time: ____

**Do not assume plain LRU** — "destination" may imply routing results with a TTL. Practise both. LRU is in `00_PRIMITIVES.py` #25; here is the TTL variant.

#### ☐ Top Customers — 🟡 Heap aggregation  ·  time: ____

**Prompt:** given transactions, return the top `k` customers by total spend, ties broken by customer id.


---

## Block D — Design

### LLD-2. Discount 🟡

A discount/promotion engine for a cart: percentage-off, flat amount, BOGO, item- and category-level, coupon codes.
- **Classes:** `DiscountStrategy` interface with `apply(Cart)` · `PercentageDiscount` · `FixedDiscount` · `BogoDiscount` · `EligibilityRule` · `DiscountEngine` · `Cart`, `LineItem`, `Product`
- **Patterns:** **Strategy** (discount type) · **Decorator** (stacking) · **Chain of Responsibility** (ordered application) · **Factory** (build from coupon code)
- **Follow-ups:** stacking vs mutually exclusive · maximum-discount cap · order of application (percentage before or after flat — it changes the total) · rounding and money precision · per-customer eligibility and expiry
- Example requirement seen in reports: *a product becomes eligible for 30% off only after a quantity threshold is met.*


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**Stories #3–4.** Targets: **Customer Obsession**, **Dive Deep**.


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
