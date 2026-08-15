# CONSOLIDATED REFERENCE — Round Script, Pattern Triggers, LP guide, Design framework

*Everything the daily files point to, in one place. Keep this open alongside whichever day you're on.*


---

# 1 · THE ROUND SCRIPT

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

---

# 2 · PATTERN TRIGGER TABLES — all seven

*Read these every morning during your primitive drill (~4 minutes total). In the final 48 hours, read them again — this is the phrasing→pattern reflex, which is the actual gap.*


## Sliding Window & Prefix Sum

| If the problem says... | Reach for |
|---|---|
| "longest substring/subarray with [property]" | sliding window, update **after** the shrink |
| "shortest/minimum subarray with [property]" | sliding window, update **inside** the shrink |
| "at most K distinct / at most K flips" | window, invalid when count exceeds K |
| "exactly K distinct" | `atMost(K) - atMost(K-1)` — memorise this trick |
| "all permutations/anagrams of p in s" | fixed-size window + Counter equality |
| "count subarrays with sum = K", **negatives allowed** | prefix sum + hashmap — **window will not work** |
| "subarray divisible by K" | prefix sum modulo K |
| "equal number of X and Y" | map one to −1, then find sum-zero subarrays |
| repeated range-sum queries, no updates | precomputed prefix array |

**The single most common Day-2 mistake:** using a sliding window when the array contains negative numbers. Windows require monotonic growth/shrink of the running value. Negatives break that — switch to prefix sum + hashmap.


## Stacks & Linked Lists

| If the problem says... | Reach for |
|---|---|
| "matching / nesting / valid brackets" | stack |
| "next greater / next smaller / span / warmer" | monotonic stack of **indices** |
| "largest rectangle / max area under bars" | increasing monotonic stack + sentinel |
| "evaluate an expression" | stack, handle `*` `/` eagerly |
| "collision / annihilation" | stack, compare against the top |
| "get min/max in O(1) alongside a stack" | store the running extreme with each element |
| head of the list might be removed/changed | **dummy node** |
| "nth from the end" / "middle" / "cycle" | fast & slow pointers |
| "reverse a portion / in groups" | head-insertion or recursive group reverse |
| deep copy with extra pointers | hashmap old→new, or interleave for O(1) space |
| "least recently / frequently used" | hashmap + doubly linked list (LRU) or freq buckets (LFU) |


## Trees & Grids

| If the problem says... | Reach for |
|---|---|
| "depth / height / diameter / max path sum" | DFS returning a value **up**, track best in a nonlocal |
| "validate BST / path must satisfy a range" | DFS passing constraints **down** |
| "level by level / right side / zigzag / min depth" | BFS with `for _ in range(len(q))` |
| "lowest common ancestor", BST | walk down using ordering |
| "lowest common ancestor", general tree | return node if found; both sides non-null ⇒ LCA |
| "reconstruct tree from traversals" | preorder gives root, inorder gives the split; index map |
| "distance K from a node in a tree" | add parent pointers → graph → BFS |
| count islands / regions / area | DFS, mark visited permanently |
| **shortest** path / minimum time in a grid | **BFS** — never DFS |
| something spreads from many sources at once | multi-source BFS, seed all sources |
| "enclosed / surrounded / can't reach the edge" | invert it: start from the border |
| find a *path* spelling a word | DFS **with backtracking** — restore the cell |


## Graphs & Heaps

| If the problem says... | Reach for |
|---|---|
| "prerequisites / build order / dependencies" | topological sort (Kahn's) |
| "can it be completed / is there a cycle" | topo sort, check `len(order) == n` |
| "shortest path", unweighted | BFS |
| "shortest/cheapest path", weighted | Dijkstra |
| "at most K stops/edges" | **Bellman-Ford** with a snapshot copy — not Dijkstra |
| "connected components / merge groups / same set?" | Union-Find |
| "minimum cost to connect all nodes" | MST (Prim with a heap) |
| "word transformation / minimum moves" | BFS over generated neighbours |
| "deep copy a graph" | hashmap old→new, register before recursing |
| "top K / Kth largest" | min-heap of size K |
| "top K with a tie-break in the opposite direction" | negate one key in the tuple |
| "median of a stream" | two heaps, balanced |
| "merge K sorted things" | heap of K heads, with an index tiebreaker |
| "arrange so no two adjacent are equal" | max-heap + hold-back previous |
| "schedule with cooldown n" | the `(maxFreq-1)*(n+1)+numMax` formula |
| "single edge whose removal disconnects" | Tarjan bridges |


## Binary Search, Intervals, Greedy

| If the problem says... | Reach for |
|---|---|
| "find target in sorted array" | plain binary search |
| "first/last occurrence", "count of X" | lower_bound / upper_bound |
| "rotated sorted array" | one half is always sorted — identify which |
| "sorted matrix, rows and cols sorted" | staircase from top-right |
| **"minimum X such that..." / "maximum X such that..."** | **binary search on the answer — write `feasible()` first** |
| "minimum speed / capacity / divisor / days" | same as above; answer space is the search space |
| "split into k parts, minimise the largest" | binary search the largest-sum limit |
| "merge overlapping intervals" | sort by **start** |
| "maximum non-overlapping intervals / fewest removals" | sort by **end** |
| "minimum rooms / max concurrency" | heap of end times, or sweep line |
| "intersection of two interval lists" | two pointers; max of starts, min of ends |
| "can you reach the end / fewest jumps" | greedy reach, or level-based BFS-on-array |
| "circular tour / gas station" | total-feasibility check + restart on deficit |
| "partition so each element appears in one part" | last-occurrence map + extend the boundary |
| pair up light with heavy | sort + two pointers from the ends |


## DP, Backtracking, Design-in-Code

| If the problem says... | Reach for |
|---|---|
| "how many ways / count the arrangements" | DP, sum the transitions |
| "min/max cost, can't take adjacent" | House Robber shape, `dp[i-1]` vs `dp[i-2]+x` |
| "fewest coins / can I reach exactly N" | unbounded knapsack, iterate amounts forward |
| "can I split into equal halves / subset sum" | 0/1 knapsack, iterate amounts **backwards** |
| "longest increasing subsequence" | O(n²) DP, then patience sorting for O(n log n) |
| "two strings, edit/align/common" | 2D DP, `dp[i][j]` over prefixes |
| "largest square / rectangle of 1s" | 2D DP, min of three neighbours |
| "max/min path through a grid" | 2D DP, base row and column first |
| "contiguous subarray with max sum/product" | Kadane; track both extremes if products |
| "all subsets / all combinations" | backtracking, loop from `start` |
| "all permutations" | backtracking, loop from 0 + `used[]` |
| "with duplicates (a 'II' variant)" | sort, then `if i > start and a[i]==a[i-1]: continue` |
| "generate all valid X" | backtrack with pruning, never generate-then-filter |
| "prefix / autocomplete / starts-with" | Trie |
| "insert, delete, and get random in O(1)" | array + index hashmap, swap-with-last on delete |
| "value at a given time / versioned key" | sorted list per key + binary search |
| "rate limit / count events in the last N seconds" | deque of timestamps, or bucketed circular array |


---

# 3 · LEADERSHIP PRINCIPLES

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

---

# 4 · SYSTEM DESIGN FRAMEWORK (Herndon-specific)

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

---

# 5 · LOGISTICS

- **Address:** Amazon Web Services, 12900 Worldgate Dr, Herndon, VA 20170. Confirm the exact building and suite with your recruiter — Amazon has multiple Northern Virginia sites (Herndon, Reston, Arlington/HQ2) and people show up at the wrong one.
- **Ask your recruiter two questions this week**, by email:
  1. *"Will the coding rounds be on a whiteboard or a laptop?"* — this changes your practice. If whiteboard, spend Days 6–8 writing code **on paper by hand.** Handwritten code is dramatically harder than typed and you must not discover that on the day.
  2. *"Which team is the loop for, and what's the tech stack?"* — Amazon loops are team-specific, and recruiters will usually tell you. If they name the team, look them up and re-weight your design prep accordingly.
- **Arrive 20 minutes early.** Traffic on the Dulles Toll Road / Route 267 is genuinely unpredictable. There's a Metro Silver Line stop (Herndon) if you'd rather not drive.
- **Bring:** photo ID, 4 printed resumes, a pen, a notebook, water, a snack for between rounds. The loop is long and blood sugar is a real variable.
- **Between rounds:** do not replay the previous round. Each interviewer scores independently and does not see the others' feedback until the debrief. A bad round 1 is fully recoverable — the debrief weighs the whole picture.
- **Have 2 questions ready for every interviewer.** Good ones: *"What does on-call look like for this team?"* / *"What's the biggest technical debt you're carrying right now?"* / *"How does this team decide what to build next?"*

---
