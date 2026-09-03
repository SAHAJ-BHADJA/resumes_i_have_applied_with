# 5-DAY FINAL PLAN — Aug 25 → Aug 29
### Amazon SDE-I onsite · **Tue Sept 1** · Herndon VA · 4 × 60 min · LiveCode (typed)

---

## Read this first

**You have 5 prep days.** Today (Aug 25) through Saturday (Aug 29). You travel Aug 30–31; those are not prep days.

This plan is organised by **round type**, not by topic — so each day rehearses the shape of an actual interview rather than a chapter of a textbook.

**One important correction to the round table:** there is no separate behavioural round at Amazon. Every interviewer is assigned 2–3 Leadership Principles and must return evidence, so ownership/failure questions land *inside* your coding rounds — usually the first 10 minutes. That's why there's a 30-minute story block every day rather than a single behavioural day.

**Solutions: `FOCUS_KEY_FINAL.md`.** Every one executed and asserted.

---

## Daily shape — about 3.5 hours

| Block | Time | What |
|---|---|---|
| Coding | 2h 30m | The 6 problems for today, 25-min timer each |
| Stories | 30 min | Leadership Principle stories (see the bottom of this file) |
| Design | 30 min | One topic, out loud, on paper |


**If you run short, cut the stretch problems first, then the design block. Never cut the stories** — with zero prepared stories you are exposed in all four rounds, and 30 minutes a day fixes that.

---

## The three rules

1. **Blank page.** Copilot and IntelliSense off. Plain editor. Paste into LeetCode only when the whole solution is written.

2. **25-minute timer.** Stuck at 8 minutes → read only the *Trigger/Insight* line in the key, never the code. At 20 → read the code, close it, rewrite from scratch.

3. **Four sentences out loud after every problem**, including easy ones:

   > *"This is a **[pattern]**. My [structure] holds **[what it means]**. I **[movement rule]**, because **[why that's correct]**. Each element is **[counted work]**, so **O(…)** time, **O(…)** space."*


---


# Day 1 · Tue Aug 25 (today)
## ROUND TYPE A — Graph & tree traversal under constraints

*"Given a graph/tree, find or optimize a path/traversal under constraints."* This is the single most likely coding round for an SDE-I loop, and it's where Amazon's own repeat questions cluster.

### Coding (2h 30m) — 25-min timer each

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 200 | Number of Islands ★★ | Do it BFS **and** DFS. Ask: may I mutate the grid? | ____ |
| ☐ | 994 | Rotting Oranges ★★ | Multi-source BFS. Seed every rotten cell before you start. | ____ |
| ☐ | 207 | Course Schedule ★ | Kahn's topo sort. `[a,b]` means b before a ⇒ edge b→a. | ____ |
| ☐ | 127 | Word Ladder ★ | BFS generating neighbours (26 swaps per position), not pairwise compare. | ____ |
| ☐ | 236 | LCA of a Binary Tree ★★ | Both subtrees return non-null ⇒ this node. Solve it twice. | ____ |
| ☐ | 102 | Level Order Traversal | `for _ in range(len(q))` is the level-size snapshot. | ____ |

**Stretch — only if the six above are done and clean:**

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 417 | Pacific Atlantic Water Flow | Invert it: start from each ocean and walk uphill. | ____ |
| ☐ | 863 | All Nodes Distance K | Add parent pointers → it's a graph → plain BFS. | ____ |

**Say out loud before coding, every time:** *shortest path ⇒ BFS, always. Reachability, area, counting ⇒ DFS is fine.* Choosing DFS for a shortest-path question is the single most common way to fail this round.

---


# Day 2 · Wed Aug 26
## ROUND TYPE B — Reduce an O(n²) solution

*"Use a hash map / sliding window / two-pointer technique to reduce an O(n²) solution."* Note the phrasing: the interviewer **expects** you to state the brute force first, then improve it. That sequence is the answer, not just the final code.

### Coding (2h 30m) — 25-min timer each

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 1 | Two Sum | 5-minute warm-up. Longer than that is a signal. | ____ |
| ☐ | 560 | Subarray Sum Equals K ★ | Prefix sum + hashmap seeded `{0:1}`. Negatives break sliding window — say so. | ____ |
| ☐ | 3 | Longest Substring Without Repeating ★★ | The archetype. Should be automatic by now. | ____ |
| ☐ | 424 | Longest Repeating Character Replacement | Invalid when `len(window) − maxFreq > k`. | ____ |
| ☐ | 15 | 3Sum ★ | Sort, fix one, two-pointer the rest. Dedupe at BOTH levels. | ____ |
| ☐ | 42 | Trapping Rain Water ★★ | Two-pointer and monotonic stack. Budget 45 min. | ____ |

**Stretch — only if the six above are done and clean:**

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 76 | Minimum Window Substring ★★ | have/need counters — the boss of this pattern. | ____ |
| ☐ | 239 | Sliding Window Maximum ★ | Monotonic deque of indices. | ____ |

**The script this round rewards:** "The brute force is O(n²) — check every pair. The repeated work is the inner scan, so a hashmap of what I've already seen gets me to O(n). Does that sound reasonable before I code it?" Rehearse those three sentences.

---


# Day 3 · Thu Aug 27
## ROUND TYPE C — Intervals, heaps and top-K

*"Solve an interval, heap or top-K problem and explain complexity."* Amazon asks these constantly — Meeting Rooms and Merge Intervals are perennial repeats.

### Coding (2h 30m) — 25-min timer each

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 56 | Merge Intervals ★★ | Sort by START. `max(end)` or contained intervals break it. | ____ |
| ☐ | 253 | Meeting Rooms II ★★ | Min-heap of end times, and the sweep-line version. Know both. | ____ |
| ☐ | 215 | Kth Largest Element | Min-heap of size k. Yes — min-heap for *largest*. | ____ |
| ☐ | 973 | K Closest Points to Origin ★ | Skip the sqrt; it's monotonic. Say that. | ____ |
| ☐ | 23 | Merge k Sorted Lists ★★ | Heap of heads. Index tiebreaker or Python raises TypeError. | ____ |
| ☐ | 621 | Task Scheduler ★ | `(maxFreq−1)*(n+1)+numMax`, clamped by `len(tasks)`. | ____ |

**Stretch — only if the six above are done and clean:**

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 347 | Top K Frequent Elements | Bucket sort is the O(n) follow-up. | ____ |
| ☐ | 295 | Find Median from Data Stream ★★ | Two heaps, kept balanced. | ____ |

**Memorise the inversion:** "K largest" ⇒ **min**-heap of size K. "K smallest" ⇒ **max**-heap of size K. And for intervals: **sort by start to merge, sort by end to maximise how many fit.**

---


# Day 4 · Fri Aug 28
## ROUND TYPE D — Justify the paradigm + design-in-code

*"Choose between BFS/DFS, DP, heap or binary search and justify the choice."* This round grades your **reasoning about the choice**, not just the implementation. Expect to be asked "why not X?" for every decision.

### Coding (2h 30m) — 25-min timer each

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 875 | Koko Eating Bananas ★ | Binary search the ANSWER. Write `feasible()` on the board first. | ____ |
| ☐ | 33 | Search in Rotated Sorted Array ★ | One half is always sorted — identify which. | ____ |
| ☐ | 322 | Coin Change ★ | **Greedy is wrong.** Counterexample ready: coins [1,3,4], amount 6. | ____ |
| ☐ | 139 | Word Break | DP over prefixes. Why not greedy? Because a longer match can dead-end. | ____ |
| ☐ | 146 | LRU Cache ★★ | Hashmap + doubly linked list. The node must store its own key. | ____ |
| ☐ | 138 | Copy List with Random Pointer ★★ | Hashmap first, then the O(1) interleave follow-up. | ____ |

**Stretch — only if the six above are done and clean:**

| ☐ | # | Problem | What to watch | Time |
|---|---|---|---|---|
| ☐ | 1011 | Capacity To Ship Packages ★ | Literally the same function as Split Array Largest Sum. | ____ |
| ☐ | 380 | Insert Delete GetRandom O(1) ★ | Array + index map, swap-with-last on delete. | ____ |

**The recognition rule for binary search on the answer:** the problem says *"minimum X such that…"* or *"maximum X such that…"*, and you can write an O(n) `feasible(x)` check. When you spot it, say the rule out loud — it's the fastest way to show you recognised the pattern rather than pattern-matched a template.

---


# Day 5 · Sat Aug 29 — Revision + full simulation

## Morning (2h 30m) — re-solve cold, blank page, timed

These are the ones Amazon actually repeats. If any takes over 25 minutes, mark it and drill the *four sentences* for it tonight — not the code.

- [ ] **200. Number of Islands**
- [ ] **994. Rotting Oranges**
- [ ] **236. LCA of a Binary Tree**
- [ ] **127. Word Ladder**
- [ ] **3. Longest Substring Without Repeating**
- [ ] **42. Trapping Rain Water**
- [ ] **560. Subarray Sum Equals K**
- [ ] **56. Merge Intervals**
- [ ] **253. Meeting Rooms II**
- [ ] **23. Merge k Sorted Lists**
- [ ] **146. LRU Cache**
- [ ] **138. Copy List with Random Pointer**

## Afternoon (2h) — one full recorded simulation

- Pick **2 problems you have not solved** from the Amazon tag. Any medium.

- 60 minutes. Record on your phone. Narrate the entire time.

- Full sequence: clarify → small example → brute force + its complexity → state the optimal → **"does that sound reasonable before I code it?"** → code → dry-run out loud tracking variables → complexity → edge cases.

- Open with one Leadership Principle question, answered out loud, before any coding.

- **Watch the recording.** Note every silence over 20 seconds and whether you skipped the dry run.


## Evening — logistics, then stop by 8pm

- Print 4 resumes · photo ID out · clothes laid out · laptop and charger packed (LiveCode runs on your machine).

- **Confirm the exact building and suite with your recruiter.** Amazon has several Northern Virginia sites and people arrive at the wrong one.

- Two questions per interviewer ready.


---

# The story block — 30 minutes a day

Your round table lists three behavioural prompts. They map to specific Amazon Leadership Principles, and **five stories cover essentially everything you'll be asked.** Write one per day, ~250 words, in STAR+ form.

| Day | Story | Prompt it answers | LP |
|---|---|---|---|
| Aug 25 | **Ownership** | *"a time you took ownership beyond your assigned responsibility"* | Ownership |
| Aug 26 | **Failure** | *"a disagreement or failure and what you changed afterward"* | Earn Trust / Learn and Be Curious |
| Aug 27 | **Incomplete information** | *"you had incomplete information but still had to deliver"* | Bias for Action |
| Aug 28 | **Most impactful project** | asked in almost every loop | Deliver Results |
| Aug 29 | **Tell me about yourself** | the first 90 seconds of every round | — |


**STAR+:** Situation (2 sentences) · Task (what **you** owned) · **Action (60% of the story)** · Result (**with a number**) · + what you'd do differently.


**The two things that sink these:** saying *"we"* (an interviewer cannot score "we" — every one becomes *"I decided," "I wrote," "I convinced"*), and stories with no ending. "Then it got deprioritised" is a non-answer.


**Rehearse each one out loud, timed. Over 2.5 minutes gets cut.**


---

# The design block — 30 minutes a day, 3 topics only

Your table names exactly the right three. Do each on **paper**, out loud — the in-person design round uses a whiteboard even though coding is typed.


**Aug 26 — Rate limiter.** Token bucket vs sliding window vs fixed window. Where the counter lives in a distributed setting. **The question they'll ask: what happens when the counter store is unavailable?** For a rate limiter, fail-*open* is usually right — the limiter must not become the thing that takes the service down.


**Aug 27 — Cache.** Read-through vs write-through vs write-back. Eviction (LRU/LFU). TTL. Invalidation. Thundering herd on a cold key. This pairs with the LRU coding problem on Aug 28 — say so if it comes up.


**Aug 28 — Notification / messaging service.** Fan-out, queues, retries with exponential backoff **plus jitter**, dead-letter queues, idempotency so a retry doesn't double-send, per-user preferences and rate limits.


**The framework, every time:** functional requirements → scale numbers → API signatures → data model → boxes → **one failure mode** → trade-offs stated aloud. The failure-mode answer is what separates candidates at AWS; anyone can draw boxes.


---

# Aug 30–31 — travel. Not prep days.

- 45 minutes writing core patterns **by hand on paper**: binary search, sliding window, grid BFS, tree DFS, heap top-K.

- Rehearse your five stories in your head. No notes.

- **No LeetCode, no new problems.** A bad attempt the night before sits in your head and costs more than the practice gains.

- Aug 31: physically find **12900 Worldgate Dr**. Eat properly, stop by 8pm, sleep 8 hours.
