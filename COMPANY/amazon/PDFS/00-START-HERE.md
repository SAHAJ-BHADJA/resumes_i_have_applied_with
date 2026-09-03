# Amazon S3 · SDE-I (L4) New Grad · Complete Interview Pack
### Built for the US loop, with a Virginia (Herndon / Arlington) lens

---

## 0. Read this first — the honest calibration

You asked for "questions the S3 team asks, ideally the Virginia team." Here is what is actually knowable, so you spend your prep on real signal instead of folklore.

**What is verifiable:**

- S3 genuinely has engineering headcount in Virginia. Public job postings show **"Senior SDE, S3 Request Processing" in Arlington, VA** and **"Software Development Engineer, S3" in Herndon, VA** (including the S3 "Broken" team, which works on reclaiming unusable storage capacity at planetary scale). Amazon's entry-level SDE requisitions list Herndon, VA and Arlington, VA alongside Seattle. So the location is real, and the work is core storage systems — not app development.
- The L4 loop shape is well documented and consistent across 2025–2026 reports.

**What is NOT verifiable, and why:**

- There is no published, team-specific question list for S3. Amazon interviewers pull from a **centralized, org-wide bank**; interviewers are explicitly discouraged from reusing leaked questions. New grads frequently interview *generically* and get **team-matched afterward**, which means your interviewers may not even be S3 engineers.
- Every "S3 team asks X" list you find online is either scraped Amazon-tagged LeetCode or someone's single data point.
- Anyone selling you an exact team-level list is guessing.

**So what did I actually do?** Two things:

1. Took the **Amazon-wide SDE-I bank** (the part that is well-attested from 2025–2026 loop reports) and ranked it by frequency.
2. **Weighted the selection toward storage-systems flavor** — the problem shapes an S3 engineer naturally reaches for, and the shapes an S3 interviewer is most likely to pick when told "ask a medium." That's things like key-prefix tries (`ListObjectsV2`), interval merging (byte ranges and multipart uploads), versioned key-value lookup (S3 object versioning), LRU/LFU (metadata caching), k-way merge (log compaction), and binary-search-on-answer (capacity planning).

That second part is inference, clearly labeled as such throughout. It is a bet on *shape*, not a claim of insider knowledge. But it's a good bet, and worst case you've studied the highest-frequency Amazon list anyway.

---

## 1. What the L4 loop actually looks like (2025–2026)

**Stage 1 — Online Assessment (OA)**
- 2 coding problems, ~105 minutes, HackerRank-style. Typically LC easy→medium.
- A work-style / Leadership Principles survey (15 min). This is scored. Take it seriously.
- Some reports mention a longer behavioral + work-simulation section.

**Stage 2 — Phone screen** — sometimes skipped for new grads who did well on the OA.

**Stage 3 — Virtual onsite loop.** For new grad L4, this is commonly **3 rounds × 45–60 min**, sometimes 4:

| Round | Content | Weight for L4 |
|---|---|---|
| DSA / coding | 1–2 problems, mostly LC medium + LP questions | High |
| "Logical & Maintainable Code" | **Object-Oriented Design (LLD)** — parking lot, cache, elevator class | High |
| Behavioral / Bar Raiser | Pure Leadership Principles, deep STAR drilling | **Highest** |
| GenAI fluency | *New in 2026.* "How do you use GenAI day-to-day?" | Medium, easy to prep |

**Three things candidates consistently get wrong:**

1. **The design round at L4 is LLD, not distributed system design.** Multiple reports confirm: *"If you're L4 loop, then maybe not system but OOP."* You will be asked to write **actual classes with methods**, not draw boxes. Don't burn 20 minutes on a UML diagram — one candidate report is explicit that interviewers want "one step past the UML." Ask the interviewer which they want; asking is itself a positive signal.
2. **LP is not the soft part.** Reported repeatedly: ~70% of a new grad loop can be behavioral. Amazon's bar is that a technically strong candidate with weak LP answers gets rejected. The Bar Raiser has veto power.
3. **Working code beats optimal code.** Amazon interviewers reward a correct brute force that runs over an elegant solution with bugs. Get something working, state its complexity, *then* optimize out loud.

**Every round mixes in LP questions.** Budget ~10–15 min of each technical round for behavioral. That means your 45-minute coding round is really a 30-minute coding round. Plan accordingly — don't over-explain.

---

## 2. The GenAI round (new for 2026, easy points)

Prepare a 90-second answer covering:
- **Where you use it:** boilerplate, test generation, unfamiliar API exploration, first-draft docs, rubber-ducking a design.
- **Where you don't, and why:** anything where you can't verify the output; security-sensitive code; algorithm correctness you haven't reasoned through yourself.
- **A concrete example** with a specific outcome ("cut my test-writing time roughly in half on X; caught two edge cases I'd missed").
- **The honest caveat:** you review everything it produces, because you own the code.

Amazon is checking that you're neither a Luddite nor someone who ships unverified output. Say both halves.

---

## 3. The 16 Leadership Principles — L4 priority order

For new grads, community reporting consistently says **Hire and Develop the Best**, **Frugality**, and **Are Right, A Lot** are tested *least*. Prioritize:

**Tier 1 (expect these):** Customer Obsession · Ownership · Dive Deep · Learn and Be Curious · Bias for Action · Deliver Results
**Tier 2:** Invent and Simplify · Earn Trust · Insist on the Highest Standards · Have Backbone; Disagree and Commit
**Tier 3:** Think Big · Strive to be Earth's Best Employer · Success and Scale Bring Broad Responsibility · the three above

**Strategy that works:** build **4–6 deep stories**, not 16 shallow ones. One strong project story, framed three different ways, covers Ownership + Deliver Results + Dive Deep. Write headline bullets on paper and keep them off-screen but in view.

**Non-negotiable mechanics:**
- Say **"I"**, not "we." Interviewers are trained to dig for your individual contribution.
- Have **numbers**. "Reduced p99 from 400ms to 90ms" beats "made it faster."
- Have a **failure story** where you own the failure without excuses. Every loop asks for one.
- Expect 3–5 follow-ups per story. Depth is the whole point of Dive Deep.

---

## 4. Why storage flavor matters for your prep

If you get an S3 interviewer, the framing will often be wrapped in storage language even when the underlying problem is standard. The reduction is what you're being tested on. Examples of the mapping:

| S3-sounding framing | What it actually is |
|---|---|
| "List all object keys under this prefix" | Trie / prefix tree traversal |
| "Coalesce these byte ranges from a multipart upload" | Merge Intervals |
| "Return the object as of this timestamp" | Time-based key-value store (binary search on versions) |
| "Which buckets are hottest right now?" | Top-K frequent elements (heap) |
| "Cache object metadata with a fixed memory budget" | LRU / LFU Cache |
| "Merge these N sorted log streams" | K-way merge with a min-heap |
| "Fewest hosts to absorb this load in D days" | Binary search on the answer |
| "Which links, if they fail, partition the fleet?" | Bridges in a graph (Tarjan) |
| "Find the placement group boundaries in this rack topology" | Connected components / Union-Find |
| "Deduplicate these checksums" | Hash set / two-pass hashing |

**How to use this:** when a problem arrives dressed in storage clothing, say out loud: *"Let me restate this as a data-structure problem — I think this reduces to X."* That sentence alone reads as senior.

---

## 5. Files in this pack

| File | Contents |
|---|---|
| `00-START-HERE.md` | This file — loop, calibration, study plan |
| `01-Coding-Solutions.md` | 72 fully worked solutions + 25 rapid-fire. Plain-English idea → algorithm steps → code → complexity → follow-ups |
| `02-System-Design-and-LLD.md` | 8 LLD + 6 HLD, each in your 5-part format: clarify → final idea → entities & functions → OOP + design pattern → runnable code |

**Language choice:** Python for the DSA file (compact, readable, and accepted in every Amazon round). Java for the design file, because the OOP round is *about* types, interfaces, and encapsulation, and Java makes that visible. Use whatever you're fastest in — just be fluent, not fancy.

---

## 6. A 6-week plan that respects the actual weights

| Week | Coding (60%) | Design (20%) | LP (20%) |
|---|---|---|---|
| 1 | Arrays, two pointers, sliding window, hashing | — | Draft 6 stories |
| 2 | Trees, BFS/DFS, graphs, topological sort | Read the LLD section end-to-end | Add metrics to each story |
| 3 | Heaps/Top-K, intervals, binary-search-on-answer | Code Parking Lot + LRU from scratch, no notes | Practice 3 out loud, timed |
| 4 | Tries, linked lists, the Design chapter (LRU/LFU/TimeMap) | Code Rate Limiter + In-Memory File System | Rehearse failure story |
| 5 | DP (the 8 that matter), rapid-fire list | 2 HLD walkthroughs out loud | Full mock LP round |
| 6 | Timed mocks only; re-solve everything you missed | Re-code your two weakest LLDs | Final polish + GenAI answer |

**Volume target: 150–200 problems solved well.** Community consensus is blunt about this — one engineer with multiple offers did ~450 and believes 150–200 would have sufficed. Re-solving a missed problem three days later beats adding a new one.

**Ratio: roughly 1 easy : 3 mediums : 1 hard.** Medium is the interview.

---

## 7. Round mechanics — the 8 minutes that decide the round

1. **Restate the problem** in your own words. Confirm you have it right.
2. **Ask 2–3 clarifying questions** before writing anything. Input size? Duplicates? Empty input? Sorted? Can I mutate the input? Unicode or ASCII?
3. **Give the brute force out loud with its complexity**, then say why you're improving it. Never write the brute force unless you're stuck.
4. **State your approach and its complexity before you type.** Get a nod first. Coding for 15 minutes toward an approach the interviewer didn't buy is the most common way to fail.
5. **Narrate while coding.** Silence reads as being lost.
6. **Dry-run on a small example**, out loud, pointing at your own variables. Find your own bug before they do.
7. **State final time and space complexity unprompted**, and name the bottleneck.
8. **Offer one follow-up yourself:** "If the input didn't fit in memory, I'd switch to an external merge sort." That's the sentence that gets you an inclined vote.

---

*Nothing in this pack is confidential Amazon material. It's compiled from public interview reports, public job postings, and standard algorithm work. Assume specifics have drifted by the time you interview — the patterns won't have.*
