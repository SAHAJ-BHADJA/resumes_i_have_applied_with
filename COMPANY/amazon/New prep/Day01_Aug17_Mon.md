# Mon Aug 17 — Day 1 of 13
### Setup · Arrays, Hashing & Two Pointers

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 1.**

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Open `ANSWER_KEY.md` and read only the *Trigger* and *Insight* lines — never the code. Close it, keep going. At 20 min read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

---

## ⚠ SETUP — before anything else (30 min)

- [ ] **Disable Copilot and IntelliSense.** Plain text editor. Five minutes, non-negotiable — with autocomplete on, the whole day is wasted.
- [ ] Create `resolve_queue.md` and your solution book (paper is better than typed).
- [ ] Print the Round Script (`01_REFERENCE...md` §1). Tape it above your desk.
- [ ] **Email your recruiter** — confirm the team, the round breakdown, and the level. Coding is already confirmed as LiveCode on your own laptop, so don't ask that one.

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

Primitives **1, 2, 6** (binary search, lower/upper bound, two pointers from ends). *Reference allowed today only.*

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Problems (25-min timer each, narrated out loud)

**You have ~224 of these already solved. That is not a reason to skip them.**

A problem you cleared two months ago with three failed submissions and a peek at the editorial is not a problem you can produce cold. If something below looks familiar, that is the best possible reason to do it again — blank page, timed, narrated. Familiarity is the illusion this plan exists to break.

#### ☐ 1. Two Sum  ·  *Hashmap — 5 min warm-up*  ·  time: ____

**Given** an unsorted integer array and a target. **Return** the indices of the two values that sum to the target; exactly one answer exists. **Watch:** an element can't pair with itself.

#### ☐ 49. Group Anagrams  ·  *Canonical key*  ·  time: ____

**Given** a list of strings. **Return** them grouped so that each group contains only mutual anagrams.

#### ☐ 128. Longest Consecutive Sequence  ·  *Set + sequence heads*  ·  time: ____

**Given** an unsorted array. **Return** the length of the longest run of consecutive integers. **Watch:** must be O(n) — no sorting.

#### ☐ 238. Product of Array Except Self  ·  *Prefix/suffix*  ·  time: ____

**Given** an array. **Return** an array where each position holds the product of every other element. **Watch:** no division, O(n).

#### ☐ 560. Subarray Sum Equals K  ·  *Prefix sum + hashmap ★*  ·  time: ____

**Given** an array (**may contain negatives**) and k. **Return** the number of contiguous subarrays summing to k.

#### ☐ 41. First Missing Positive  ·  *Index-as-hash, O(1) space ★★*  ·  time: ____

**Given** an unsorted array. **Return** the smallest missing positive integer. **Watch:** must be O(n) time and O(1) extra space.

#### ☐ 15. 3Sum  ·  *Sort + two pointers ★*  ·  time: ____

**Given** an integer array. **Return** all unique triplets summing to zero. **Watch:** the output must contain no duplicate triplets — dedupe at both the outer and inner level.

#### ☐ 11. Container With Most Water  ·  *Move the limiting side*  ·  time: ____

**Given** heights of vertical lines on an x-axis. **Return** the largest water area between two lines (area = width × shorter height).

#### ☐ 42. Trapping Rain Water  ·  *Two ways ★★ — budget 60 min*  ·  time: ____

**Given** an elevation map of bar heights. **Return** the total water trapped after rain.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Common Manager — ✅ Verified  ·  time: ____

**Prompt:** an org tree where each manager has zero or more direct reports. Given two employees, return their **lowest common manager**. Follow-up: generalise to `k` employees.

#### ☐ Friends Purchases — ✅ Verified  ·  time: ____

**Prompt:** given `getFriends(person)` and `getPurchases(person)`, return the most popular products among a user's friends. **Popularity = number of distinct friends who bought it**, not total quantity. Common variant: exclude products the user already owns.


---

## Block D — Design

### LLD-1. Config Manager 🟠

Retrieve and update configuration values, with typed access, defaults, layered overrides, and change notification.
- **Classes:** `ConfigManager` (facade) · `ConfigSource` interface (in-memory / file / env / remote) · `ConfigValue<T>` · `ConfigListener` · `ConfigValidator`
- **Patterns:** **Strategy** (source) · **Observer** (listeners) · precedence chain across sources
- **Operations:** `get(key)`, typed getters, `set(key, value)`, defaults, `reload()`, `subscribe(listener)`
- **Follow-ups to have answers for:** thread safety on concurrent read/write · hot reload · precedence when two sources define the same key · type coercion failures · caching and TTL · **adding a new source without touching callers**


**How to run a design block:** requirements → non-functional → API signatures → data model → classes or architecture → **one failure mode** → trade-offs stated out loud. Draw it on paper — the in-person design round puts you at a whiteboard even though coding is on a laptop.

---

## Block E — Leadership Principles

**LP brain dump + stories #1–2.** One page of ~20 raw career bullets first (bugs fixed, deadlines hit, conflicts, failures, things shipped). Then write two full STAR+ stories. Targets: **Ownership**, **Deliver Results**.


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
