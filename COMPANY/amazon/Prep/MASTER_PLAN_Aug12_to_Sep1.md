# AMAZON PREP — MASTER PLAN
### Aug 12 → Sept 1, 2026 | Herndon, VA (12900 Worldgate Dr, AWS)
### Starting from zero prep. 18 working days + 2 travel days.

---

## PART 0 — READ THIS BEFORE ANYTHING ELSE

### On "100%"

I'm going to be straight with you, because a plan built on a false premise fails on the day.

**Nobody can guarantee 100% on an Amazon loop, and anyone who tells you otherwise is selling something.** There's a Bar Raiser with veto power, interviewers pick their own questions, and the variance is real — strong engineers get rejected and recover on the re-apply. That is not a reason to aim lower. It's a reason to aim at the thing you actually control.

Here's what you *can* get to by Aug 29, and what I've built this plan to deliver:

- **Pattern coverage near-total.** By Aug 29, a fresh Medium from your question bank should be a pattern you've drilled, not a pattern you're meeting.
- **Recall fixed.** Your specific deficit — knowing the approach but freezing on the blank page — is a trainable motor skill, and 18 days is genuinely enough. It was tight at 8. It isn't now.
- **No round you walk into cold.** Coding, LLD, HLD, LP: all four rehearsed under time, out loud, before you fly.

That combination is what "ready" means. It converts the loop from a coin flip into a strong-favourite. Take that, and let the variance be variance.

### The good news about 18 days

The 8-day version was triage. This is real training. Three things become possible that weren't before:

1. **Spaced repetition.** Every problem you fail gets re-solved at +1 day, +3 days, and +7 days. That schedule is the actual mechanism that converts "I recognise this" into "I can produce this." It needs calendar room, and now it has it.
2. **LP stories done properly.** 14 stories at one per day is relaxed. Crammed into three days they come out generic, and generic LP answers are the single most common reason strong coders fail Amazon.
3. **Four full mock loops** instead of one. Performance is its own skill, separate from knowing the material.

### Your existing files

You already have these. Don't re-derive anything:

| File | Use |
|---|---|
| `00_PRIMITIVES.py` | Every single morning. The daily drill. |
| `Day1_KEY.md` – `Day7_KEY.md` | Answer keys. **After** your attempt, never before. |
| `Amazon_8_Day_Plan.md` | Parts 2, 5, 6, 7, 8 (Round Script, System Design, LPs, Pattern Journal, Logistics) still apply verbatim. This document replaces only the day-by-day schedule. |

The KEY files map onto the new calendar — each day below tells you which one to open.

### The three rules — unchanged, and now they matter more

**RULE 1 — Blank page, always.** No Copilot, no IntelliSense, no GPT. Plain editor. Paste into LeetCode only after you've written the whole thing.

**RULE 2 — Stuck at 8 minutes? Read only the *Trigger* and *Insight* lines of the key. Not the code.** Close it, keep going. At 20 minutes, read the code — then close it and rewrite from scratch twice, and add it to the re-solve queue.

**RULE 3 — Narrate out loud on every problem, from today.** Silent correct code scores worse at Amazon than narrated near-correct code, because every interviewer is assigned Leadership Principles to gather evidence against and can only score what you say.

---

## PART 1 — THE CALENDAR AT A GLANCE

| Phase | Dates | Days | Focus |
|---|---|---|---|
| **1 — Foundation** | Aug 12–17 (Wed–Mon) | 6 | Arrays, hashing, two pointers, sliding window, stacks, linked lists |
| **2 — Core structures** | Aug 18–23 (Tue–Sun) | 6 | Trees, grids, graphs, heaps |
| **3 — Advanced + design** | Aug 24–27 (Mon–Thu) | 4 | Binary search, intervals, greedy, DP, backtracking, tries |
| **4 — Performance** | Aug 28–29 (Fri–Sat) | 2 | Full mock loops, weak-spot repair, dress rehearsal |
| **Travel** | Aug 30–31 (Sun–Mon) | 2 | Light review only. No new material. |
| **INTERVIEW** | **Tue Sept 1** | — | Herndon, VA |

**Checkpoints:** Aug 17 (consolidation), Aug 23 (Mock Loop 1), Aug 27 (Mock Loop 2), Aug 28 (Mock Loop 3), Aug 29 (Mock Loop 4 — dress rehearsal).

### Two tracks — pick honestly on day one

You never told me your hours, so both are built:

- **FULL (~7h/day)** — if you're not working, or on weekends. Core + Stretch.
- **COMPRESSED (~4h/day)** — if you're working full-time. Core only; move Stretch to weekends.

**Choose one and hold it.** Setting a 7-hour target you miss on day two is worse than a 4-hour target you hit for 18 days straight. Consistency beats intensity here, because spaced repetition only works if the spacing actually happens.

### The daily skeleton — every single day, both tracks

| Block | Full | Compressed | What |
|---|---|---|---|
| A | 45 min | 30 min | **Primitives from memory**, timed, blank file |
| B | 30 min | 20 min | **Re-solve queue** — cold, no notes |
| C | 3h 30m | 2h | **New problems**, 25-min timer each, narrated |
| D | 60 min | 40 min | **Design** (HLD or LLD) |
| E | 45 min | 20 min | **LP stories** — write or rehearse |
| F | 20 min | 15 min | **Pattern Journal** |

---

## PART 2 — THE SPACED REPETITION SYSTEM

This is the engine of the whole plan. Do not skip it because it feels less productive than new problems. It is the part that fixes your actual deficit.

**Keep one running file: `resolve_queue.md`.** Every problem where you needed a hint, exceeded 25 minutes, or produced buggy code gets an entry:

```
994 Rotting Oranges  |  failed Aug 20  |  due: Aug 21 ✓, Aug 23 ✓, Aug 27 ☐
```

**The schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list.

**"Re-solve" means from a blank page, cold, no notes, no glance at the key first.** If you fail a repeat, the clock resets: it's due again at +1, +3, +7 from that day.

**If your Block B runs long, cut Block C, not Block B.** A re-solve is worth more than a new problem. New problems build coverage; re-solves build recall, and recall is what's broken.

---

## PART 3 — DAY BY DAY

---

# PHASE 1 — FOUNDATION (Aug 12–17)

### DAY 1 — Wed Aug 12 | Setup + Arrays & Hashing
**Key file: `Day1_KEY.md`**

**Setup first (45 min) — do this before any problem:**
- Disable Copilot and IntelliSense. Open a plain editor. This is non-negotiable and takes 5 minutes.
- Print the **Round Script** (`Amazon_8_Day_Plan.md`, Part 2). Tape it above your desk.
- Create `resolve_queue.md` and `pattern_journal.md`.
- **Email your recruiter today.** Three questions:
  1. *"Will the coding rounds be on a whiteboard or a laptop?"* — if whiteboard, you'll add handwritten practice from Aug 24.
  2. *"Which team is the loop for?"* — this re-weights your entire design prep.
  3. *"Can you confirm the round structure and level?"* — SDE-1 loops lean LLD; SDE-2+ lean HLD.

**Block A (45m):** Write `00_PRIMITIVES.py` for the first time. Primitives 1, 2, 6. **Reference allowed today only.** Time each one.

**Block C (3h30m):** Blank page, 25-min timer, narrate out loud:
- 1 Two Sum · 242 Valid Anagram · 217 Contains Duplicate
- 49 Group Anagrams · 128 Longest Consecutive Sequence
- 238 Product of Array Except Self · 560 Subarray Sum Equals K

**Block D (60m):** Read all 16 Leadership Principles slowly. Then read Part 5 of `Amazon_8_Day_Plan.md` (the design framework). No design work yet — just absorb the framework.

**Block E (45m):** **LP brain dump.** One page, ~20 raw items from your career: bugs you fixed, deadlines you hit, conflicts, failures, things you shipped, times you pushed back. Bullet points only. No stories yet.

**Block F (20m):** Pattern Journal.

---

### DAY 2 — Thu Aug 13 | Two Pointers
**Key file: `Day1_KEY.md`**

**A (45m):** Primitives 1, 2, 6, 7 — **from memory now.** Delete the file after.
**B (30m):** Re-solve queue (Aug 12 failures).
**C (3h30m):**
- 125 Valid Palindrome · 15 3Sum ★ (do this twice — it's the #1 dedup-bug problem)
- 11 Container With Most Water · 88 Merge Sorted Array · 977 Squares of a Sorted Array
- 75 Sort Colors · 167 Two Sum II
- **42 Trapping Rain Water** — both ways, two-pointer and monotonic stack. Budget a full hour.

**D (60m):** **LLD 1 — Parking Lot.** The canonical one. Classes, interfaces, the `Strategy` pattern for pricing. Produce a class diagram on paper without looking anything up first, *then* compare.
**E (45m):** Write LP stories #1 and #2. Target: **Ownership**, **Deliver Results**. Use STAR+ (Part 6). Every story ends in a number.
**F (20m):** Journal.

---

### DAY 3 — Fri Aug 14 | Sliding Window
**Key file: `Day2_KEY.md`**

**A (45m):** Primitives 4, 5, 22 + Tier 1 review.
**B (30m):** Re-solve queue.
**C (3h30m):**
- **3 Longest Substring Without Repeating Characters** — the archetype. Do it until automatic.
- 424 Longest Repeating Character Replacement · 209 Minimum Size Subarray Sum
- 438 Find All Anagrams · 567 Permutation in String
- 904 Fruit Into Baskets · 1004 Max Consecutive Ones III

**D (60m):** **HLD 1 — Rate Limiter / Throttling Service.** Token bucket vs sliding window log vs fixed window counter. Distributed state. What happens when the counter store is down (fail-open or fail-closed?). *Every AWS service has one of these — high probability at your site.*
**E (45m):** LP stories #3, #4. Target: **Customer Obsession**, **Dive Deep**.
**F (20m):** Journal.

---

### DAY 4 — Sat Aug 15 | Prefix Sum + Stacks *(weekend — full track)*
**Key files: `Day2_KEY.md`, `Day3_KEY.md`**

**A (45m):** Primitives 19, 22 + Tier 1.
**B (30m):** Re-solve queue.
**C (4h):**
- Prefix sum: 974 Subarray Sums Divisible by K · 525 Contiguous Array · 304 Range Sum Query 2D
- Stacks: 20 Valid Parentheses · 155 Min Stack · 150 Evaluate RPN · 394 Decode String
- Monotonic: 739 Daily Temperatures · 496 + 503 Next Greater Element I & II · 735 Asteroid Collision

**D (75m):** **HLD 2 — Distributed Key-Value Store (DynamoDB-like).** Consistent hashing, replication factor, quorum reads/writes (R+W>N), vector clocks vs last-write-wins, hot partitions. **Learn the phrase "control plane vs data plane" and use it.**
**E (45m):** LP stories #5, #6. Target: **Bias for Action**, **Insist on the Highest Standards**.
**F (20m):** Journal.

**Stretch:** 84 Largest Rectangle in Histogram · 853 Car Fleet · 227 Basic Calculator II · 71 Simplify Path

---

### DAY 5 — Sun Aug 16 | Linked Lists *(weekend — full track)*
**Key file: `Day3_KEY.md`**

**A (45m):** Primitives 7, 8, 9, 25. Dummy-head must be reflexive by tonight.
**B (30m):** Re-solve queue — **first +3 day repeats land today.**
**C (4h):** All with dummy head where applicable:
- 206 Reverse Linked List · 21 Merge Two Sorted Lists · 141 + 142 Cycle I & II
- 19 Remove Nth From End · 143 Reorder List · 2 Add Two Numbers
- **138 Copy List with Random Pointer** ★ — both hashmap and O(1) interleaving
- 25 Reverse Nodes in k-Group · 92 Reverse Linked List II

**D (75m):** **LLD 2 — LRU Cache, then LFU.** Code both from scratch, manual doubly linked list, no `OrderedDict`. These get asked as *both* coding and design questions at Amazon.
**E (45m):** LP stories #7, #8. Target: **Have Backbone / Disagree and Commit**, **Learn and Be Curious**.
**F (20m):** Journal.

---

### DAY 6 — Mon Aug 17 | CONSOLIDATION #1
**No new patterns today. Today you find out what actually stuck.**

**A (45m):** Reproduce **all Tier 1 primitives** (1–13) from memory, timed. Anything you fumble, drill 3× immediately.
**B (90m):** **Clear the entire re-solve queue.** Everything overdue, cold.
**C (2h):** **Mini-mock — one 60-minute round.** Two problems you have *not* seen, from Phase 1 patterns only. Record on your phone. Full Round Script. One LP question first.
Then **watch the recording** (25 min). Note only three things:
- Silences longer than 20 seconds
- Did you skip the dry run?
- Did you code before stating the approach?

**D (60m):** **HLD 3 — Object Storage (S3-like).** Metadata vs blob separation, durability math (why 11 nines), multipart upload, eventual vs strong consistency for reads-after-write.
**E (45m):** LP stories #9, #10. Target: **Invent and Simplify**, **Earn Trust**.
**F (20m):** Journal + honest self-assessment. Write down your three weakest patterns. They get extra time in Phase 2.

---

# PHASE 2 — CORE STRUCTURES (Aug 18–23)

### DAY 7 — Tue Aug 18 | Trees, Part 1
**Key file: `Day4_KEY.md`**

**A (45m):** Primitives 12, 13.
**B (30m):** Re-solve queue.
**C (3h30m):**
- 104 Max Depth · 226 Invert · 100 Same Tree · 110 Balanced · **543 Diameter** ★
- 102 Level Order · 199 Right Side View · 103 Zigzag
- **124 Binary Tree Maximum Path Sum** — same shape as 543 (return one thing, track another). Say that out loud.

**Ask yourself on every tree problem, out loud, before coding:** *"Am I sending information UP from the children, or DOWN from the parent?"* Get that right in 30 seconds and the code writes itself.

**D (60m):** **HLD 4 — Authorization / IAM Policy Evaluation.** Sub-10ms p99 at enormous read volume, policy caching and invalidation, propagation delay on change, fail-closed. *Herndon hosts AWS Identity and Automated Reasoning in Identity — this is the highest-probability design topic at your site.*
**E (45m):** LP stories #11, #12. Target: **Think Big**, **Are Right, A Lot**.
**F (20m):** Journal.

---

### DAY 8 — Wed Aug 19 | Trees, Part 2
**Key file: `Day4_KEY.md`**

**A (45m):** Primitives 12, 13 + Tier 1 sweep.
**B (30m):** Re-solve queue.
**C (3h30m):**
- **98 Validate BST** (the DOWN shape) · 235 LCA of BST · **236 LCA of Binary Tree** ★★ — do 236 twice
- 105 Construct from Preorder + Inorder
- **297 Serialize and Deserialize Binary Tree** ★
- **863 All Nodes Distance K** ★ — the "convert tree to graph with parent pointers" trick
- 987 Vertical Order Traversal

**D (60m):** **HLD 5 — Usage Metering & Billing Pipeline.** High-volume event ingest, per-customer per-hour aggregation, exactly-once / no double-billing, late-arriving events, idempotency keys. *AWS Platform in Herndon publicly owns contractual billing systems.*
**E (45m):** LP stories #13, #14. Target: **Frugality**, plus the mandatory **"tell me about a failure"**.
**F (20m):** Journal.

---

### DAY 9 — Thu Aug 20 | Grids
**Key file: `Day4_KEY.md`**

**A (45m):** Primitives 10, 11. Grid BFS/DFS must be typed without thinking by tonight.
**B (30m):** Re-solve queue.
**C (3h30m):**
- **200 Number of Islands** ★★ — both BFS and DFS
- 695 Max Area of Island · 733 Flood Fill · 130 Surrounded Regions (the "start from the border" inversion)
- **994 Rotting Oranges** ★★ — multi-source BFS, extremely common at Amazon
- 417 Pacific Atlantic Water Flow · 79 Word Search (DFS **with** backtracking — restore the cell)

**The rule: shortest path ⇒ BFS, always. Never DFS.** Reachability, area, and counting are fine with DFS.

**D (60m):** **LLD 3 — Elevator System.** State machine, scheduling strategy, request queue, concurrency. Name the design patterns you use.
**E (45m):** **Rehearse** stories #1–#5 out loud, timed. Any story over 2.5 minutes gets cut down. This is the first rehearsal pass — expect them to be flabby.
**F (20m):** Journal.

---

### DAY 10 — Fri Aug 21 | Graphs
**Key file: `Day5_KEY.md`**

**A (45m):** Primitives 14, 15, 16, 17. Kahn's and Union-Find from memory today.
**B (30m):** Re-solve queue.
**C (3h30m):**
- **207 + 210 Course Schedule I & II** ★ — topological sort
- 133 Clone Graph · 547 Number of Provinces · 721 Accounts Merge (Union-Find)
- **127 Word Ladder** ★★ — Amazon classic. Mention bidirectional BFS as the optimisation.
- 542 01 Matrix (same shape as Rotting Oranges — say so) · 1091 Shortest Path in Binary Matrix
- 743 Network Delay Time (Dijkstra) · **787 Cheapest Flights Within K Stops** (Bellman-Ford — the K cap breaks Dijkstra)

**Run this decision tree out loud in the first 60 seconds of any graph problem:** unweighted shortest path → BFS · weighted → Dijkstra · ≤K edges → Bellman-Ford · prerequisites → topo sort · connectivity/merging → Union-Find · connect-everything-cheapest → MST.

**D (60m):** **HLD 6 — Distributed Message Queue (SQS-like).** Visibility timeout, at-least-once vs exactly-once, dead-letter queues, ordering guarantees, consumer scaling.
**E (45m):** Rehearse stories #6–#10 out loud, timed.
**F (20m):** Journal.

---

### DAY 11 — Sat Aug 22 | Heaps + Top-K *(weekend — full track)*
**Key file: `Day5_KEY.md`**

**A (45m):** Primitive 21 + Tier 2 sweep.
**B (30m):** Re-solve queue.
**C (4h):**
- 215 Kth Largest · 347 Top K Frequent Elements · **692 Top K Frequent Words** ★ (the mixed sort direction)
- **23 Merge k Sorted Lists** ★★ (remember the index tiebreaker or Python raises TypeError)
- **767 Reorganize String** ★ · **621 Task Scheduler** ★ (the formula, not simulation)
- **295 Find Median from Data Stream** ★★ — two heaps
- 373 K Pairs with Smallest Sums

**Memorise the inversion: "K largest" ⇒ MIN-heap of size K. "K smallest" ⇒ MAX-heap of size K.**

**D (75m):** **HLD 7 — Monitoring & Alarming (CloudWatch-like).** Time-series ingest at scale, downsampling/rollups, alarm evaluation, avoiding alert storms.
**E (45m):** Rehearse stories #11–#14. Then the mandatory set: *tell me about yourself* (90 seconds, rehearsed), *most impactful project*, *why Amazon / why this team*.
**F (20m):** Journal.

**Stretch:** 1584 Min Cost to Connect All Points (MST) · 269 Alien Dictionary · **1192 Critical Connections** · 1235 Maximum Profit in Job Scheduling

---

### DAY 12 — Sun Aug 23 | MOCK LOOP #1 *(weekend — full track)*
**The first full dress rehearsal. Treat it as real. Phone off.**

**A (30m):** Full Tier 1 + Tier 2 primitives from memory, timed.

**Mock Round 1 (60m) — Coding.** Two unseen problems from Tier S. Record it. LP question first, then full Round Script.
**Review (25m).** Watch the recording.

**Mock Round 2 (60m) — Coding.** Two fresh problems: one linked list, one graph. Record.
**Review (25m).**

**Break (30m).** Actually break. The real loop has these and you need to practise recovering.

**Mock Round 3 (60m) — Design.** Pick one HLD you've prepared. Draw on paper. Talk the entire time. Then have someone (or yourself, on camera) push back on one design decision and defend it.
**Review (20m).**

**LP block (45m):** Full run-through of all 14 stories, timed.

**Debrief (30m):** Write down every gap. This list drives Phase 3 and Phase 4. Be brutal — this is the most useful document you'll produce all month.

---

# PHASE 3 — ADVANCED + DESIGN (Aug 24–27)

### DAY 13 — Mon Aug 24 | Binary Search
**Key file: `Day6_KEY.md`**

> **If your recruiter said whiteboard: from today, write every solution by hand on paper first.** Handwritten code is dramatically harder than typed and you must not discover that on Sept 1.

**A (45m):** Primitives 1, 2, **3 (binary search on the answer — drill this hardest)**.
**B (30m):** Re-solve queue.
**C (3h30m):**
- 704 · 34 First & Last Position · **33 Search in Rotated** ★★ · 153 Find Minimum in Rotated · 162 Find Peak · 240 Search a 2D Matrix II
- **Binary search on the answer** — the single highest-yield sub-pattern of the month:
  **875 Koko Eating Bananas** · **1011 Capacity to Ship Packages** · 1482 Min Days for Bouquets · **410 Split Array Largest Sum** · 1283 Smallest Divisor

**410 and 1011 are literally the same function.** Recognising that out loud is worth more than the code. The recognition rule: *"minimum/maximum X such that..."* + you can write an O(n) `feasible(x)` ⇒ binary search the answer space. **Write `feasible` on the board first, before the search.**

**D (60m):** **HLD 8 — Distributed Job Scheduler.** Leader election, idempotency, exactly-once semantics, handling a worker that dies mid-task.
**E (45m):** Rehearse the 5 stories that came out weakest on Aug 23. Rewrite any that lack a number.
**F (20m):** Journal.

---

### DAY 14 — Tue Aug 25 | Intervals + Greedy
**Key file: `Day6_KEY.md`**

**A (45m):** Primitives — full Tier 1 + 2 sweep.
**B (30m):** Re-solve queue.
**C (3h30m):**
- **56 Merge Intervals** ★★ · 57 Insert Interval · 435 Non-overlapping Intervals
- **253 Meeting Rooms II** ★★ — both heap and sweep-line · 986 Interval List Intersections · **2402 Meeting Rooms III** ★
- Greedy: 55 Jump Game · 45 Jump Game II · **134 Gas Station** ★ · 763 Partition Labels · 881 Boats to Save People

**The interval rule: sort by START to merge. Sort by END to maximise how many fit.** That single distinction is the difference between correct and subtly wrong.

**D (60m):** **LLD 4 — Rate Limiter (object-oriented).** Strategy pattern so you can swap token bucket / leaky bucket / sliding window without touching the caller. Mention Open/Closed naturally, once.
**E (45m):** Mandatory-story rehearsal: failure, tough feedback, conflict with a teammate.
**F (20m):** Journal.

---

### DAY 15 — Wed Aug 26 | Dynamic Programming
**Key file: `Day7_KEY.md`**

**A (45m):** Primitive 24 + Tier 1.
**B (30m):** Re-solve queue.
**C (4h):**
- 70 · 746 · **198 + 213 House Robber** · **322 Coin Change** ★★ · 518 Coin Change II (loop order = combinations vs permutations)
- 139 Word Break · 53 Maximum Subarray (Kadane) · 152 Maximum Product Subarray
- 62 + 63 Unique Paths · 64 Minimum Path Sum · **221 Maximal Square** ★
- **300 LIS** ★★ (both O(n²) and patience sorting) · **1143 LCS** ★ · **416 Partition Equal Subset Sum** (backwards loop = 0/1)
- 72 Edit Distance · 91 Decode Ways

**Say this out loud before writing a line, every time: "Let me define dp[i] as..."** That one sentence unfreezes almost everyone. Then: transition, base cases, iteration order.

**D (60m):** **Design review.** Go back through HLD 1–8. For each, can you state the API, the data model, the partitioning strategy, and *one failure mode* without notes? Whichever two you can't, redo them.
**E (45m):** LP rehearsal — full set, timed.
**F (20m):** Journal.

---

### DAY 16 — Thu Aug 27 | Backtracking, Tries, Design-in-Code + MOCK LOOP #2
**Key file: `Day7_KEY.md`**

**A (45m):** Primitives 18, 20.
**B (30m):** Re-solve queue.
**C (2h30m):**
- Backtracking (one template, six problems): 78 Subsets · 90 Subsets II · 46 Permutations · 39 Combination Sum · **22 Generate Parentheses** · 17 Letter Combinations
- Design-in-code (these get asked *as coding problems* at Amazon): 208 Implement Trie · 211 Add and Search Words · **1268 Search Suggestions System** ★ · **380 Insert Delete GetRandom O(1)** ★ · 981 Time Based Key-Value Store · 362 Design Hit Counter · 1472 Design Browser History

**Combinations loop from `start`. Permutations loop from 0 with a `used[]`. Duplicates ("II" variants) need `if i > start and a[i] == a[i-1]: continue`.** That's the whole family.

**MOCK LOOP #2 (2h30m):** Two coding rounds, 60 min each, recorded, unseen problems. Then review both.
**E (30m):** LP — the three weakest stories only.

---

# PHASE 4 — PERFORMANCE (Aug 28–29)

### DAY 17 — Fri Aug 28 | MOCK LOOP #3 + Weak-Spot Repair

**A (30m):** All 25 primitives from memory, timed. **Target: 25 minutes, zero errors.**
**B (30m):** Re-solve queue — should be nearly empty by now. Anything still on it is a red flag; drill it 3×.

**Mock Round 1 (60m) — Coding.** Unseen. Recorded.
**Mock Round 2 (60m) — LLD.** Unseen prompt. Whiteboard/paper. Full class design.
**Mock Round 3 (60m) — HLD.** Unseen prompt from your list of 8. Paper. Defend two decisions under pushback.
**Review (45m):** All three recordings.

**Repair block (90m):** Your three weakest patterns from the Aug 23 debrief. Two fresh problems each, blank page.

**E (45m):** Full LP run, all 14 + the mandatory set. Anything over 2.5 minutes gets cut.

---

### DAY 18 — Sat Aug 29 | MOCK LOOP #4 — Dress Rehearsal
**Simulate the real thing end to end. Same start time as your actual interview if you know it.**

**A (30m):** Primitives, final timed run.

**Full simulated loop, back to back, minimal breaks:**
- Round 1 (60m): Coding + LP
- Round 2 (60m): Coding + LP
- Round 3 (60m): Design (LLD or HLD — have someone pick, or roll a die)
- Break (20m)
- Round 4 (60m): Bar-Raiser style — heavy LP, one coding problem

**Review (60m).** Last honest look.

**Consolidation (90m):**
- Re-read all seven Pattern Trigger tables (the tables at the end of each KEY file). ~30 min. **This is the highest-value review you can do** — it's the phrasing→pattern reflex, which is your actual gap.
- Skim your Pattern Journal end to end.
- Re-read the Round Script until you can recite it.

**Logistics (45m):**
- Print 4 copies of your resume. Photo ID out. Clothes laid out. Bag packed.
- Confirm the exact building and suite with your recruiter — Amazon has multiple Northern Virginia sites (Herndon, Reston, Arlington/HQ2) and people genuinely show up at the wrong one.
- Prepare 2 questions per interviewer. Good ones: *"What does on-call look like for this team?"* · *"What's the biggest technical debt you're carrying?"* · *"How does this team decide what to build next?"*

**Stop by 8pm. Sleep 8 hours.**

---

# TRAVEL — Aug 30–31

**These are not prep days. Attempting to learn anything new here will cost you more in fatigue than it gains you in knowledge.**

### Sun Aug 30 — Travel
- **On the plane / in transit:** write primitives **by hand on paper**. 45 min. That's it.
- **Audio rehearsal:** run your 14 LP stories in your head, or mutter them. No notes.
- Read the Pattern Trigger tables once. Passive read, no problems.
- **No LeetCode. No new patterns.**

### Mon Aug 31 — Arrival
- **Scout the location.** Physically go to 12900 Worldgate Dr, or at least drive/ride past. Find the parking, find the entrance. This removes a real source of morning-of stress. The Metro Silver Line has a Herndon stop if you'd rather not drive; the Dulles Toll Road / Route 267 is genuinely unpredictable.
- **One easy problem.** Two Sum or Valid Parentheses. Purely to confirm your hands work. Do not do a Medium — a bad attempt tonight will sit in your head.
- Re-read the Round Script.
- Rehearse *"tell me about yourself"* three times out loud.
- **Eat properly. Stop by 8pm. Sleep 8 hours.**
- **Do not cram.** Cramming measurably degrades retrieval, which is precisely your weak axis. This is the single most tempting mistake available to you and it will cost you real points.

---

# INTERVIEW DAY — Tue Sept 1

**Morning:**
- Eat something real. Arrive **20 minutes early**.
- Bring: photo ID, 4 printed resumes, pen, notebook, water, a snack for between rounds. The loop is long and blood sugar is a real variable.
- In the car or the lobby: read the Round Script one final time. Nothing else.

**In each round:**
- Clarify before coding. Ask about scale — it signals Customer Obsession.
- **State your approach and ask "does that sound reasonable before I code it?"** Highest-value sentence available to you. Prevents 20 wasted minutes and reads as Earn Trust.
- Narrate continuously.
- **Dry run your code out loud, line by line, tracking variables.** This is your existing superpower — you told me you can explain any code by looking at it. Use exactly that. It catches most bugs and reads as Dive Deep.
- If time is short: **working brute force beats buggy optimal.** Amazon interviewers value correct code over clever code. Get it correct, state the better approach, offer to code it.

**Between rounds:**
- **Do not replay the last round.** Each interviewer scores independently and doesn't see the others' feedback until the debrief. A bad round 1 is fully recoverable — the debrief weighs the whole picture.

---

## PART 4 — READINESS CHECKLIST

Tick these on Aug 29. Any unticked item tells you where the last hours go.

**Mechanical**
- [ ] All 25 primitives typed from memory in ≤25 min, zero syntax errors
- [ ] Round Script recitable from memory
- [ ] Fresh Medium solved in ≤25 min, unassisted, narrating throughout
- [ ] Re-solve queue empty
- [ ] (If whiteboard) comfortable writing code by hand on paper

**Coverage**
- [ ] All seven Pattern Trigger tables read in the final 48 hours
- [ ] All 25 Tier S problems solved cleanly at least twice
- [ ] Three weakest patterns identified on Aug 23 and repaired by Aug 28

**Design**
- [ ] 8 HLD topics: API, data model, partitioning, and one failure mode — no notes
- [ ] 4 LLD designs whiteboarded without notes
- [ ] Can explain control plane vs data plane, and blast radius / cell-based architecture

**Behavioural**
- [ ] 14 STAR+ stories, each ≤2.5 minutes, each ending in a number
- [ ] Mandatory set ready: yourself · most impactful project · a failure · tough feedback · a conflict · why Amazon
- [ ] Every story says "I," not "we"
- [ ] 2 questions prepared per interviewer

**Performance**
- [ ] 4 full mock loops completed and reviewed on video
- [ ] Practised recovering after a round that went badly

---

## PART 5 — WHAT WILL NOT HELP

Listed because with 18 days you now have enough time to waste some, and these are the ways people do it:

- Reading editorial solutions to feel productive
- Watching solution videos
- Adding more problems to the list — coverage is not your bottleneck, recall is
- Using GPT to write or debug anything before you've finished a full blank-page attempt
- Skipping the re-solve queue because new problems feel like more progress
- Doing 9 hours on a Saturday and zero on Monday
- Cramming on Aug 31

---

*The single highest-leverage sentence in this document, unchanged from the last version: **never let yourself read a solution before you've produced 25 minutes of your own broken code.** Broken code you wrote teaches you more than perfect code you read. Your deficit is production. Production is trained only by producing.*
