# Amazon Onsite Prep — 8 Day Plan (Aug 3 → Aug 10)
### Target: Herndon, VA (12900 Worldgate Dr — AWS office) | First 3 rounds, unassisted, in person

---

## PART 0 — READ THIS FIRST (the actual diagnosis)

Your stated problem: *"I understand any code, I can spec it to GPT, I know the approach — but I can't write it myself."*

This is **recognition without recall.** They are different skills stored differently:

| Skill | You have it | Trained by |
|---|---|---|
| Reading & explaining code | ✅ Strong | Reading solutions |
| Choosing the right approach | ✅ Strong | Reading solutions |
| Producing syntax from blank page | ❌ Missing | **Only** by writing from blank page |
| Producing it in 25 min with someone watching | ❌ Missing | **Only** by timed, out-loud practice |

**The trap:** when you read a solution and think *"yes, obviously, I knew that"* — that feeling is recognition firing. It produces zero recall gain. It's the single reason people plateau for months.

### The three non-negotiable rules for the next 8 days

**RULE 1 — Blank page, always.**
No autocomplete. No Copilot. No GPT. No looking at a previous solution while writing. Turn off IDE suggestions entirely. Write in a plain text editor (Notepad / VS Code with IntelliSense disabled / Google Docs). Only *after* you've written the full solution do you paste it into LeetCode and run it.

**RULE 2 — If you're stuck for 8 minutes, you don't look at the solution. You look at the *pattern name* only.**
Give yourself one word: "monotonic stack." Then close it and keep going. Looking at code = you burned the rep. If after 20 min you still can't, *then* read the solution — and then you must **close it and rewrite it from scratch, twice**, and mark it for re-solve at 24h and 72h.

**RULE 3 — Narrate out loud, every single problem, from Day 1.**
Not "in your head." Actually speak. This feels stupid alone in a room. Do it anyway. In an Amazon room, silent correct code scores *worse* than narrated near-correct code — the interviewer is assigned specific Leadership Principles to grade you on and they can only grade what you say. This also frees working memory; talking forces sequential thought, which is exactly what you lack when you freeze.

---

## PART 1 — THE 25 PRIMITIVES (your highest-leverage 8 days)

This is the core intervention. Your freeze isn't conceptual — it's that you don't have **motor-memory skeletons** to fall back on. Strong candidates aren't inventing a BFS at the whiteboard; they're typing a memorized 9-line block and then modifying it.

**Your daily obligation: 45–60 minutes of primitive drilling, every single day, before anything else.**

Method: open a blank file. Type the primitive from memory. Time it. Target is **under 90 seconds each, zero syntax errors, no reference.** If you fail, write it again immediately, then again. Do 8–10 per morning, cycling through all 25 so each gets hit 3+ times across the 8 days.

### The list

**Tier 1 — must be reflexive (drill every single day)**
1. `binary_search` — exact match
2. `lower_bound` / `upper_bound` — first index ≥ target, first index > target
3. **Binary search on the answer** — `lo, hi = min_ans, max_ans; while lo < hi: mid; if feasible(mid): hi = mid else lo = mid+1`
4. Variable-size sliding window — `while right < n: expand; while invalid: shrink; update answer`
5. Fixed-size sliding window
6. Two pointers from opposite ends
7. Fast/slow pointer — cycle detection **and** find middle
8. Reverse a linked list, iterative — `prev, cur = None, head`
9. Merge two sorted lists using a **dummy head** (dummy head is itself a primitive — it removes 80% of linked-list bugs)
10. Grid BFS — `deque`, `dirs = [(0,1),(0,-1),(1,0),(-1,0)]`, visited marking
11. Grid DFS / flood fill, recursive
12. Tree BFS level-order — the `for _ in range(len(queue))` level-size trick
13. Tree DFS — pre/in/post order recursive, and the "return value up, pass value down" shape

**Tier 2 — must be solid (drill every other day)**
14. Graph BFS on adjacency list
15. Topological sort — Kahn's (in-degree + queue)
16. Cycle detection in directed graph — 3-color / white-gray-black
17. Union-Find — `find` with path compression, `union` by rank
18. Backtracking template — `choose → recurse → un-choose`
19. Monotonic stack — increasing and decreasing variants, and the "pop while" shape
20. Trie — node class, insert, search, startsWith
21. Heap idioms — min-heap, max-heap via negation, heap of tuples, `heapify`, k-sized heap
22. Prefix sum + hashmap (`count[0] = 1` seed — memorize why)

**Tier 3 — know cold but lower frequency**
23. Dijkstra (heap-based)
24. 1D DP and 2D grid DP skeletons — including base-row/base-column initialization
25. LRU Cache — hashmap + doubly linked list (and the `OrderedDict` shortcut, but know the manual one)

> **Write these into one file called `primitives.py` today.** Then delete it and rewrite it from memory tomorrow. Repeat daily. By Day 8 you should be able to reproduce the entire file in ~25 minutes.

---

## PART 2 — THE ROUND SCRIPT (memorize this sequence)

You freeze because you have no procedure. Here is the procedure. It never changes, regardless of problem.

**Minutes 0–3 — Clarify (out loud)**
- Restate the problem in your own words. "So I'm given X, I need to return Y — is that right?"
- Ask about: input size / constraints, duplicates, negatives, empty input, sorted?, in-place required?, return index or value?
- **Amazon-specific:** ask "what's the expected scale?" — it signals Customer Obsession and Think Big.

**Minutes 3–6 — Examples**
- Write one small example and the expected output. Then one edge case (empty, single element, all-same).
- This is where you *find* the pattern. Don't skip it — this is the step that unfreezes you.

**Minutes 6–10 — Brute force, out loud**
- State it. State its complexity. **Do not code it.**
- "The brute force is O(n²) — check every pair. Let me see if I can do better."

**Minutes 10–14 — Optimize + get buy-in**
- Name the pattern out loud: "The repeated work is the inner scan, so a hashmap of seen values gets me to O(n)."
- **Then ask: "Does that approach sound reasonable before I code it?"** — this single question is the highest-value sentence in the round. It prevents 20 wasted minutes and reads as Earn Trust.

**Minutes 14–32 — Code**
- Write the **function signature first.** Then the return statement. Then fill the middle. Blank page paralysis dies when the skeleton exists.
- Narrate while typing: "I'll initialize a hashmap here to store value → index..."
- **Amazon values working code over clever code.** If you're at minute 28 and the optimal is shaky — write the brute force, make it *correct*, then say "this is O(n²); the O(n) version uses a hashmap, I can code that next." Correct brute force > buggy optimal, at Amazon specifically.

**Minutes 32–38 — Dry run**
- Take your small example. Walk the code line by line, out loud, tracking variable values. **This is your superpower** — you said you can explain any code by looking at it. Use exactly that strength here. This step will catch most of your bugs and reads as Dive Deep.

**Minutes 38–42 — Complexity + edge cases**
- Time and space, stated confidently.
- "Edge cases: empty array returns 0, single element returns itself, all negatives — let me check that path."

**Minutes 42–45 — Offer improvements**
- "If the input were streaming instead, I'd switch to..." — Think Big signal.

**Print this. Tape it above your desk. Follow it on every practice problem starting today, including easy ones.**

---

## PART 3 — YOUR QUESTION BANK, COMPRESSED

Your bank has 644 problems. You cannot do 644. You do not need to. The bank collapses into **16 patterns**, and roughly 110 problems give you near-total coverage. Everything below is pulled from *your* file.

### Tier S — Amazon signature. If you do nothing else, do these 25.
These recur across Amazon loops year after year, and several are in your bank multiple times.

| # | Problem | Pattern |
|---|---|---|
| 146 | LRU Cache | Design |
| 200 | Number of Islands | Grid DFS/BFS |
| 56 | Merge Intervals | Intervals |
| 1 | Two Sum | Hashmap |
| 3 | Longest Substring Without Repeating Characters | Sliding window |
| 42 | Trapping Rain Water | Two pointer / stack |
| 138 | Copy List with Random Pointer | Linked list + hashmap |
| 994 | Rotting Oranges | Multi-source BFS |
| 207 / 210 | Course Schedule I & II | Topological sort |
| 23 | Merge k Sorted Lists | Heap |
| 253 | Meeting Rooms II | Intervals + heap |
| 236 | Lowest Common Ancestor of a Binary Tree | Tree recursion |
| 5 | Longest Palindromic Substring | Expand around center |
| 692 | Top K Frequent Words | Heap + custom sort |
| 767 | Reorganize String | Greedy + heap |
| 621 | Task Scheduler | Greedy + counting |
| 1268 | Search Suggestions System | Trie / sorting |
| 1152 | Analyze User Website Visit Pattern | Hashmap + combinatorics |
| 127 | Word Ladder | BFS |
| 297 | Serialize and Deserialize Binary Tree | Tree + design |
| 863 | All Nodes Distance K in Binary Tree | Tree → graph BFS |
| 1192 | Critical Connections in a Network | Tarjan bridges |
| 2402 | Meeting Rooms III | Heap simulation |
| 472 | Concatenated Words | Trie / DP |
| 239 | Sliding Window Maximum | Monotonic deque |

### Tier A — Pattern coverage (do these to make the patterns automatic)

**Hashmap & counting:** 242, 49, 560, 128, 347, 217, 383, 974, 525
**Two pointers:** 125, 15, 11, 88, 977, 680, 167, 75
**Sliding window:** 424, 209, 76, 438, 567, 904, 1004, 1456
**Prefix sum:** 238, 303/304, 1480
**Monotonic stack:** 739, 496, 503, 84, 853, 901, 907, 316, 402
**Stack (general):** 20, 155, 394, 227, 224, 735, 150, 71
**Linked list:** 206, 21, 141, 142, 143, 19, 2, 25, 92, 328, 160, 234
**Trees:** 104, 226, 102, 199, 98, 543, 124, 105, 110, 235, 987, 173, 449
**Grid / graph:** 695, 733, 417, 130, 79, 1091, 542, 133, 547, 269, 721, 990, 787, 743, 1584
**Heap / top-K:** 215, 1046, 373, 295, 1235, 502, 378, 895
**Binary search:** 704, 33, 153, 34, 162, 875, 1011, 410, 1482, 4, 240
**Intervals:** 57, 435, 986, 1353, 1235
**Greedy:** 55, 45, 134, 763, 135, 881, 1046
**DP:** 70, 198, 213, 322, 300, 139, 53, 152, 62, 63, 1143, 416, 72, 91, 221, 518, 746
**Backtracking:** 78, 46, 39, 22, 17, 79, 131, 51, 212, 90
**Design (coding-round design):** 155, 208, 211, 380, 981, 1472, 460, 355, 362, 359, 706, 622, 2013, 1166
**Matrix:** 48, 54, 73, 36, 59
**Bit / math:** 136, 191, 190, 268, 7, 50, 371, 202, 13, 273

### Tier B — skip unless you have spare time
Everything SQL (175, 181, 182, 183, 184, 185, 197, 577, 584, 595, 626, ...), the JS/pandas ones (2667, 2620, 2703, 2704, 2879), and the very-high-numbered recent contest problems (3xxx). These appear in your bank but are near-zero probability for an SDE loop.

---

## PART 4 — DAY BY DAY

**Format each day:** a **Core track (~6h)** you must complete, and a **Stretch (~3h)** if you have the time. If you're working a job, do Core only and move the design/LP blocks to the weekend.

**Every single day, without exception:**
- Morning: 45 min primitive drill
- Before new problems: 30 min re-solving *yesterday's failures* cold, from blank page
- End of day: 20 min writing your **Pattern Journal** (see Part 7)

---

### DAY 1 — Mon Aug 3 | Arrays, Hashing, Two Pointers + Establish the system

**Core (6h)**
- **0:00–0:45** Write `primitives.py` from scratch for the first time. Primitives 1, 2, 4, 6, 7, 8. Reference allowed *today only*. Time each.
- **0:45–1:00** Print the Round Script (Part 2). Set up your blank-page environment: disable Copilot, disable IntelliSense, open a plain editor.
- **1:00–3:30** Problems — **blank page, 25 min timer each, narrate out loud:**
  - 1 Two Sum, 242 Valid Anagram, 49 Group Anagrams, 217 Contains Duplicate
  - 125 Valid Palindrome, 15 3Sum, 11 Container With Most Water
  - 88 Merge Sorted Array, 977 Squares of a Sorted Array
- **3:30–4:00** Break.
- **4:00–5:00** Hard block: **42 Trapping Rain Water.** Do it two ways — two-pointer and monotonic stack. This one problem teaches both patterns.
- **5:00–5:45** **LP block.** Read all 16 Leadership Principles once, slowly. Then list every project/incident from your career on one page — bugs you fixed, deadlines you hit, conflicts, failures, things you shipped. Just the raw list, ~20 items. Don't write stories yet.
- **5:45–6:00** Pattern Journal.

**Stretch (3h)**
- 128 Longest Consecutive Sequence, 238 Product of Array Except Self, 560 Subarray Sum Equals K, 75 Sort Colors, 167 Two Sum II
- **LLD intro:** watch/read one walkthrough of *Design a Parking Lot*, then close it and produce the class diagram yourself on paper.

---

### DAY 2 — Tue Aug 4 | Sliding Window + Prefix Sum

**Core (6h)**
- **0:00–0:45** Rewrite `primitives.py` from memory. Focus: 3, 4, 5, 22. **Delete the file at the end.**
- **0:45–1:15** Re-solve cold: any Day 1 problem you failed or needed a hint on.
- **1:15–4:00** Problems (25 min each, blank page, narrated):
  - 3 Longest Substring Without Repeating Characters ← *do this until it's automatic; it's the archetype*
  - 424 Longest Repeating Character Replacement
  - 209 Minimum Size Subarray Sum
  - 438 Find All Anagrams in a String
  - 567 Permutation in String
  - 904 Fruit Into Baskets, 1004 Max Consecutive Ones III
- **4:00–5:00** **76 Minimum Window Substring** (hard, but it's the boss of this pattern — worth the hour)
- **5:00–5:45** **LP block:** write 3 full STAR stories (see Part 6 for format). Target LPs: *Ownership, Deliver Results, Customer Obsession.*
- **5:45–6:00** Pattern Journal.

**Stretch (3h)**
- Prefix sum: 560 (again, faster), 974, 525, 304
- **LLD:** Design a **Rate Limiter** — classes, interfaces, token bucket vs sliding window log. Write actual code for the token bucket. *(Highly relevant to an AWS platform team.)*

---

### DAY 3 — Wed Aug 5 | Stacks, Monotonic Stacks, Linked Lists

**Core (6h)**
- **0:00–0:45** Primitives from memory: 8, 9, 19, plus Tier 1 review.
- **0:45–1:15** Re-solve Day 1–2 failures cold.
- **1:15–3:15** Stack problems:
  - 20 Valid Parentheses, 155 Min Stack, 150 Evaluate RPN, 394 Decode String
  - 739 Daily Temperatures, 496 + 503 Next Greater Element I & II
  - 735 Asteroid Collision, 853 Car Fleet
- **3:15–3:30** Break.
- **3:30–5:00** Linked lists — **all on blank page, all using dummy head where applicable:**
  - 206 Reverse Linked List, 21 Merge Two Sorted Lists, 141 + 142 Cycle
  - 19 Remove Nth Node From End, 143 Reorder List, 2 Add Two Numbers
  - **138 Copy List with Random Pointer** ← Amazon favorite
- **5:00–5:45** **LP block:** 3 more stories. Target: *Dive Deep, Bias for Action, Insist on the Highest Standards.*
- **5:45–6:00** Pattern Journal.

**Stretch (3h)**
- 84 Largest Rectangle in Histogram, 227 Basic Calculator II, 71 Simplify Path, 25 Reverse Nodes in k-Group, 92 Reverse Linked List II
- **LLD:** Implement **146 LRU Cache** from scratch — manual doubly linked list, no `OrderedDict`. Then extend to **460 LFU.** These are asked as *both* coding and LLD questions at Amazon.

---

### DAY 4 — Thu Aug 6 | Trees + Grid Traversal

**Core (6h)**
- **0:00–0:45** Primitives: 10, 11, 12, 13. Grid BFS/DFS and tree traversal must be **typed without thinking** by end of today.
- **0:45–1:15** Re-solve failures cold.
- **1:15–3:30** Trees:
  - 104 Max Depth, 226 Invert, 110 Balanced, 543 Diameter, 100 Same Tree
  - 102 Level Order, 199 Right Side View, 103 Zigzag
  - 98 Validate BST, 235 + **236 LCA** (do 236 twice)
  - 105 Construct from Preorder & Inorder
- **3:30–3:45** Break.
- **3:45–5:00** Grid:
  - **200 Number of Islands** ← do it BFS *and* DFS
  - 695 Max Area of Island, 733 Flood Fill, 130 Surrounded Regions
  - **994 Rotting Oranges** ← multi-source BFS, extremely common at Amazon
  - 417 Pacific Atlantic Water Flow
- **5:00–5:45** **HLD block #1 — Design a distributed key-value store / object store (S3-like).** Cover: API, partitioning/consistent hashing, replication, quorum, consistency model, hot-key handling. *(See Part 5.)*
- **5:45–6:00** Pattern Journal.

**Stretch (3h)**
- 124 Binary Tree Maximum Path Sum, 297 Serialize/Deserialize, 863 All Nodes Distance K, 987 Vertical Order Traversal, 79 Word Search

---

### DAY 5 — Fri Aug 7 | Graphs + Heaps

**Core (6h)**
- **0:00–0:45** Primitives: 14, 15, 16, 17, 21. Union-Find and Kahn's must be typed from memory today.
- **0:45–1:15** Re-solve failures cold.
- **1:15–3:15** Graphs:
  - **207 + 210 Course Schedule I & II** (topological sort, both Kahn's and DFS)
  - 133 Clone Graph, 547 Number of Provinces, 721 Accounts Merge (Union-Find)
  - **127 Word Ladder** ← Amazon classic
  - 1091 Shortest Path in Binary Matrix, 542 01 Matrix
  - 743 Network Delay Time (Dijkstra), 787 Cheapest Flights Within K Stops
- **3:15–3:30** Break.
- **3:30–5:00** Heaps / Top-K:
  - 215 Kth Largest Element, 347 Top K Frequent Elements, **692 Top K Frequent Words**
  - **23 Merge k Sorted Lists**, 373 K Pairs with Smallest Sums
  - **767 Reorganize String**, **621 Task Scheduler**
  - 295 Find Median from Data Stream (two heaps)
- **5:00–5:45** **HLD block #2 — Design a metering & billing system.** Ingest usage events at high volume, aggregate per-customer per-hour, guarantee no double-billing, handle late-arriving events. *(AWS Platform in Herndon owns billing systems — this is a live question.)*
- **5:45–6:00** Pattern Journal.

**Stretch (3h)**
- 1584 Min Cost to Connect All Points (MST), 990 Satisfiability of Equality Equations, 269 Alien Dictionary, **1192 Critical Connections in a Network**, 1235 Maximum Profit in Job Scheduling

---

### DAY 6 — Sat Aug 8 | Binary Search on Answer + Intervals + Greedy

**Core (6h)**
- **0:00–0:45** Primitives: 1, 2, **3 (binary search on answer — drill this hardest)**, 24.
- **0:45–1:15** Re-solve failures cold.
- **1:15–3:00** Binary search:
  - 704 Binary Search, 34 First & Last Position, 33 Search in Rotated, 153 Find Minimum in Rotated, 162 Find Peak
  - **Binary search on the answer** — this is the pattern people miss most: **875 Koko Eating Bananas**, **1011 Capacity to Ship Packages**, 1482 Min Days to Make Bouquets, **410 Split Array Largest Sum**, 1283 Smallest Divisor
  - 240 Search a 2D Matrix II
- **3:00–4:15** Intervals:
  - **56 Merge Intervals**, 57 Insert Interval, 435 Non-overlapping Intervals
  - **253 Meeting Rooms II**, 986 Interval List Intersections, **2402 Meeting Rooms III**
- **4:15–5:00** Greedy: 55 Jump Game, 45 Jump Game II, 134 Gas Station, 763 Partition Labels, 881 Boats to Save People
- **5:00–5:45** **HLD block #3 — Design an authorization / IAM service.** Policy evaluation, caching, sub-10ms p99 at massive read volume, propagation delay on policy change, fail-closed vs fail-open. *(Herndon hosts AWS Identity and Automated Reasoning in Identity — highest-probability design topic at this site.)*
- **5:45–6:00** Pattern Journal.

**Stretch (3h)**
- 4 Median of Two Sorted Arrays, 1353 Max Events, 135 Candy, 1648 Sell Diminishing-Valued Colored Balls
- **LP block:** 4 more stories. Target: *Have Backbone / Disagree and Commit, Learn and Be Curious, Earn Trust, Invent and Simplify.*

---

### DAY 7 — Sun Aug 9 | DP + Backtracking + Design-in-Code

**Core (6h)**
- **0:00–0:45** Primitives: 18, 20, 24, 25. Backtracking template and Trie must be reflexive.
- **0:45–1:15** Re-solve failures cold.
- **1:15–3:15** DP (don't chase depth — chase the *shape* of the recurrence):
  - 70 Climbing Stairs, 746 Min Cost Climbing Stairs, **198 + 213 House Robber**
  - **322 Coin Change**, 518 Coin Change II, 139 Word Break
  - 53 Maximum Subarray, 152 Maximum Product Subarray
  - 62 + 63 Unique Paths, 64 Minimum Path Sum, 221 Maximal Square
  - **300 Longest Increasing Subsequence**, 1143 LCS, 416 Partition Equal Subset Sum
- **3:15–3:30** Break.
- **3:30–4:30** Backtracking (one template, five problems):
  - 78 Subsets, 90 Subsets II, 46 Permutations, 39 Combination Sum, **22 Generate Parentheses**, 17 Letter Combinations, 79 Word Search
- **4:30–5:30** **Design-in-code round prep** — these get asked *as coding problems*:
  - 208 Implement Trie, 211 Add and Search Words, **1268 Search Suggestions System**
  - 380 Insert Delete GetRandom O(1), 981 Time Based Key-Value Store
  - 359 Logger Rate Limiter, 362 Design Hit Counter, 1472 Design Browser History
- **5:30–6:00** Pattern Journal + LP rehearsal out loud.

**Stretch (3h)**
- 72 Edit Distance, 91 Decode Ways, 1235 Max Profit in Job Scheduling
- **LLD:** Design an **Elevator System** *or* a **Distributed Job Scheduler** — full class design, interfaces, state machine, concurrency notes.
- 1152 Analyze User Website Visit Pattern, 472 Concatenated Words

---

### DAY 8 — Mon Aug 10 | Full Loop Simulation + Repair

Today you do **not** learn new material. Today you rehearse the actual performance.

**Core (6h)**
- **0:00–0:30** Reproduce the entire `primitives.py` from memory, timed. Target: 25 min, zero errors. Whatever you fumble → drill it 3× immediately.
- **0:30–1:35** **MOCK ROUND 1 — Coding.** Set a 60-min timer. Pick two problems you have *not* seen from Tier S. Record yourself on your phone. Full Round Script: clarify, examples, brute force, get buy-in, code, dry run, complexity. Answer one LP question at the start, out loud.
- **1:35–2:00** Watch the recording. Note: silences over 20 seconds, skipped dry run, jumping to code before stating approach.
- **2:00–3:05** **MOCK ROUND 2 — Coding.** Same protocol, two fresh problems. Include one linked list and one graph.
- **3:05–3:30** Break.
- **3:30–4:35** **MOCK ROUND 3 — Design.** 60 min. Do one HLD (pick from Part 5) *and* be ready to pivot to LLD. Draw on paper, talk the whole time.
- **4:35–5:30** **LP rehearsal.** Say all 12–14 stories out loud, timed, 2 minutes each. Any story over 3 minutes gets cut down.
- **5:30–6:00** Logistics + weak-spot list. Re-drill your 3 worst primitives.

**Evening:** stop by 8pm. Lay out clothes, ID, printed resume copies. Sleep 8 hours. **Do not cram the night before or the morning of** — it measurably degrades retrieval, which is precisely your weak axis.

---

## PART 5 — SYSTEM DESIGN, TAILORED TO HERNDON

### Why this matters for your site specifically

Herndon (12900 Worldgate Dr) is an **AWS office**, not a retail/consumer Amazon office. Publicly, the teams anchored there include **EC2**, **AWS Platform** (identity & access management, cryptography, console, builder/developer tools, and contractual billing systems), and **Automated Reasoning in Identity**. AWS Platform publicly describes sustaining on the order of **750 million transactions per second.**

Practical translation: your design round will lean toward **infrastructure and platform primitives**, not consumer product design. Prepare Design-a-Rate-Limiter over Design-Instagram.

### The design framework (use this exact order, every time)

1. **Functional requirements** — 3–5 bullets. Ask, don't assume.
2. **Non-functional** — scale (QPS, data volume), latency target (p50/p99), availability, consistency, durability.
3. **Back-of-envelope** — QPS, storage/day, bandwidth. Do the arithmetic out loud.
4. **API design** — actual endpoint signatures. This is where AWS interviewers pay attention.
5. **Data model** — what's the key? What's the access pattern? *Access pattern before schema* — that's the DynamoDB way of thinking and it lands well at AWS.
6. **High-level architecture** — draw the boxes.
7. **Deep dive** — the interviewer will pick one. Have opinions ready on partitioning, replication, and caching.
8. **Failure modes** — this is the AWS differentiator. What happens on a host failure, an AZ failure, a region failure? What's your blast radius? How do you degrade?
9. **Trade-offs, stated explicitly** — "I chose eventual consistency here because..."

### Two vocabulary items that signal you understand AWS

- **Control plane vs. data plane.** Control plane = configuration, provisioning, low volume, can tolerate higher latency. Data plane = the actual request path, massive volume, must stay up even if the control plane is down. *Saying "the data plane must have static stability — it keeps serving even if the control plane is unavailable" is a strong AWS-native signal.*
- **Cell-based architecture / blast radius.** Partition into independent cells so a failure affects 1/N of customers, not everyone. Shuffle sharding as the refinement.

### Prepare these 8 designs (in priority order for this site)

| # | Design | Why it's likely here |
|---|---|---|
| 1 | **Rate limiter / throttling service** | Every AWS service has one; also a great LLD |
| 2 | **Distributed key-value store (DynamoDB-like)** | Partitioning, replication, quorum, consistent hashing |
| 3 | **Object storage (S3-like)** | Durability math, metadata vs. blob separation, multipart upload |
| 4 | **Authorization / IAM policy evaluation service** | Herndon hosts AWS Identity |
| 5 | **Usage metering & billing pipeline** | AWS Platform owns billing systems |
| 6 | **Distributed message queue (SQS-like)** | Visibility timeout, at-least-once, dedup, DLQ |
| 7 | **Health-check / monitoring & alarming (CloudWatch-like)** | Time-series ingest, aggregation, alarm evaluation |
| 8 | **Distributed job scheduler / task orchestration** | Leader election, idempotency, exactly-once semantics |

**Fallback consumer designs** in case your interviewer goes generic: URL shortener, web crawler, notification service, top-K trending. Prepare these at 60% depth.

### LLD — prepare 4 class designs
Amazon frequently swaps HLD for **object-oriented low-level design**, especially for SDE-I/II. Be ready to produce real classes, interfaces, and a state machine on a whiteboard.

1. **Parking Lot** (the canonical one — do it first)
2. **LRU / LFU Cache** (you'll have written these on Day 3)
3. **Elevator system** (state machine + scheduling strategy)
4. **Rate limiter** (Strategy pattern: token bucket / leaky bucket / sliding window)

Know these patterns by name and be able to justify one: **Strategy, Factory, Observer, Singleton, Builder.** Mention SOLID once, naturally — specifically *"I'd put this behind an interface so we can swap the strategy without touching the caller"* (Open/Closed).

---

## PART 6 — LEADERSHIP PRINCIPLES (do not treat this as optional)

**This is where strong coders fail Amazon.** Every interviewer in your loop is assigned 2–3 specific Leadership Principles and must return concrete evidence — positive or negative — against them. LPs are graded *inside your coding round*, not in a separate round. Multiple candidates report LP questioning consuming **more than half** of a supposedly technical interview.

### What you need: 12–14 stories, not 16

You do **not** need one story per LP. You need 12–14 rich stories, each mapped to 2–3 LPs, that you can re-angle on demand.

### STAR+ format (write each one out, ~250 words)

- **S**ituation — 2 sentences. Context only.
- **T**ask — what *you specifically* owned. Not "we."
- **A**ction — 60% of the story. What *you* did, decisions you made, alternatives you rejected and why.
- **R**esult — **with a number.** "Reduced p99 latency from 800ms to 120ms." "Cut the deploy from 45 min to 6." If you don't have a number, estimate one and say "roughly."
- **+ Learning** — what you'd do differently. Amazon actively probes this.

### The 6 LPs that appear most often — have 2 stories each

1. **Customer Obsession** — a time you pushed back on an internal preference for the user's benefit
2. **Ownership** — you fixed something that wasn't your job / you were on the hook past your scope
3. **Dive Deep** — a bug nobody could find; how you instrumented and root-caused it
4. **Deliver Results** — a hard deadline you hit, and what you cut to hit it
5. **Have Backbone; Disagree and Commit** — you disagreed with your manager or team, and what happened after the decision went against you
6. **Invent and Simplify** — you removed complexity, not added it

Also prepare at least one each for: **Bias for Action, Learn and Be Curious, Earn Trust, Insist on the Highest Standards, Are Right, A Lot, Frugality, Think Big.**

### Mandatory stories regardless of LP
- Tell me about yourself (90 seconds, rehearsed)
- Your most impactful project
- A time you failed / a project that didn't work
- Tough feedback you received and what you changed
- A conflict with a teammate
- Why Amazon / why this team

### Two failure modes to avoid
- **Saying "we."** The interviewer cannot score "we." Say "I decided," "I wrote," "I convinced."
- **Stories with no ending.** Every story needs a concrete outcome. "And then the project got deprioritized" is a non-answer.

---

## PART 7 — THE PATTERN JOURNAL (20 min/day, non-negotiable)

One page per problem you struggled with. Handwritten is better than typed — the motor act aids encoding.

```
Problem:      994 Rotting Oranges
Trigger:      "grid" + "simultaneous spread" + "minimum time"
Pattern:      Multi-source BFS
Key insight:  Seed the queue with ALL rotten cells at once, then
              process level by level; each level = 1 minute.
Where I got stuck:  I tried DFS first. DFS gives you *a* path,
              not the *shortest* — shortest ⇒ BFS. Always.
Primitive used:  #10 grid BFS
Re-solve on:  Aug 6, Aug 9
```

The **Trigger** line is the most important. You already know approaches — what you lack is the reflex mapping *problem phrasing → pattern*. Build that mapping explicitly.

**Re-solve schedule:** every problem you failed gets re-solved cold at **+24h** and **+72h**. Keep a running list. This is the mechanism that converts recognition into recall.

---

## PART 8 — INTERVIEW DAY LOGISTICS (Herndon)

- **Address:** Amazon Web Services, 12900 Worldgate Dr, Herndon, VA 20170. Confirm the exact building and suite with your recruiter — Amazon has multiple Northern Virginia sites (Herndon, Reston, Arlington/HQ2) and people show up at the wrong one.
- **Ask your recruiter two questions this week**, by email:
  1. *"Will the coding rounds be on a whiteboard or a laptop?"* — this changes your practice. If whiteboard, spend Days 6–8 writing code **on paper by hand.** Handwritten code is dramatically harder than typed and you must not discover that on the day.
  2. *"Which team is the loop for, and what's the tech stack?"* — Amazon loops are team-specific, and recruiters will usually tell you. If they name the team, look them up and re-weight your design prep accordingly.
- **Arrive 20 minutes early.** Traffic on the Dulles Toll Road / Route 267 is genuinely unpredictable. There's a Metro Silver Line stop (Herndon) if you'd rather not drive.
- **Bring:** photo ID, 4 printed resumes, a pen, a notebook, water, a snack for between rounds. The loop is long and blood sugar is a real variable.
- **Between rounds:** do not replay the previous round. Each interviewer scores independently and does not see the others' feedback until the debrief. A bad round 1 is fully recoverable — the debrief weighs the whole picture.
- **Have 2 questions ready for every interviewer.** Good ones: *"What does on-call look like for this team?"* / *"What's the biggest technical debt you're carrying right now?"* / *"How does this team decide what to build next?"*

---

## PART 9 — THE ONE-PAGE CHECKLIST

Print this. Tick it daily.

**Daily**
- [ ] 45 min primitives from memory, timed
- [ ] 30 min cold re-solve of prior failures
- [ ] 6–9 new problems, blank page, timed, **narrated out loud**
- [ ] 1 design (HLD or LLD)
- [ ] 2–3 LP stories written or rehearsed
- [ ] 20 min Pattern Journal

**By Aug 10 you must be able to:**
- [ ] Type all 25 primitives from memory, error-free
- [ ] Solve a fresh Medium in 25 minutes, unassisted, talking the whole time
- [ ] Recite the Round Script from memory
- [ ] Deliver 12+ STAR stories, each under 2.5 minutes, each ending in a number
- [ ] Whiteboard 4 designs from the Herndon list without notes
- [ ] Write code by hand on paper (if the recruiter confirms whiteboard)

**Things that will NOT help and that you must not do:**
- Reading editorial solutions to feel productive
- Watching solution videos
- Adding more problems to the list
- Using GPT to generate or debug anything before you've finished a full blank-page attempt
- Cramming on Aug 10 evening

---

*The single highest-leverage change in this entire document: **never let yourself read a solution before you've produced 25 minutes of your own broken code.** Broken code you wrote teaches you more than perfect code you read. Your specific deficit is production, and production is only trained by producing.*
