# START HERE — 13 days to the Amazon onsite
### Mon Aug 17 → Sat Aug 29 · travel Aug 30–31 · **interview Tue Sept 1**
### Herndon, VA (12900 Worldgate Dr, AWS) · 4 rounds × 60 min · coding on LiveCode

---

## How this pack works

**Two files matter each day:**

| File | What it is |
|---|---|
| `DayNN_...md` | **The only thing you follow.** Full question statements, the design brief, the LP task, the checklist. No solutions. |
| `ANSWER_KEY.md` | **Every solution, for all 13 days**, organised by day with an index at the top. Open only after your attempt. |

Everything else is supporting reference you'll touch occasionally:

| File | Use |
|---|---|
| `00_PRIMITIVES.py` | Every morning, Block A. Type from memory, *then* compare. |
| `01_REFERENCE_...md` | The Round Script, the Pattern Trigger tables, the LP guide, logistics. |
| `02_GPT_INTERVIEWER_...md` | The strict GPT voice-interviewer prompt and the solution-book template. |
| `03_INTERVIEWDB_BANK.md` | The full reported-question bank, including the ~15 titles that could **not** be recovered and what to drill instead. |

---

## What changed — you lost 5 days, so this is a different plan

The old plan assumed 18 days. You have 13. I did not just delete days off the end; I re-cut the whole thing.

**What got compressed:** trees went from two days to one · stacks and linked lists merged · sliding window and prefix sum merged · four mock loops became three · 175 problems became **153**, and the ones I cut were the redundant second and third examples of patterns you've already met.

**What did *not* get cut, and why:**
- **All six LLD briefs.** Six LLD titles in the reported bank, on an AUTA/SDE-I loop, is the strongest single signal in the whole dataset. One per day, Days 1–6.
- **All 14 LP stories.** These fail more strong coders than algorithms do, and there's no way to cram them in two days.
- **All 29 recovered InterviewDB questions.** These are the closest thing you have to your actual prompts.
- **The re-solve queue.** Cutting this would defeat the entire plan.

**What this costs you:** less slack. On the old plan a bad day was recoverable. Now, if you lose a day, drop from the **bottom** of Block C rather than skipping a day entirely — the ★ problems are the recurring ones.

---

## The 13 days

| Day | Date | Focus | Design |
|---|---|---|---|
| 1 | Mon Aug 17 | Setup · Arrays, Hashing, Two Pointers | LLD-1 Config Manager |
| 2 | Tue Aug 18 | Sliding Window & Prefix Sum | LLD-2 Discount |
| 3 | Wed Aug 19 | Stacks, Monotonic Stacks & Linked Lists | LLD-3 Query Builder |
| 4 | Thu Aug 20 | Trees | LLD-4 Shipping Cost |
| 5 | Fri Aug 21 | Grids & Backtracking | LLD-5 Spell Checker |
| 6 | Sat Aug 22 | Graphs | LLD-6 Validation Framework |
| 7 | Sun Aug 23 | **★★ MOCK LOOP #1** (3 rounds + debrief) | — |
| 8 | Mon Aug 24 | Heaps & Top-K | SD-1 CloudWatch |
| 9 | Tue Aug 25 | Binary Search (incl. on the answer) | SD-2 Config Distribution |
| 10 | Wed Aug 26 | Intervals, Greedy & DP Part 1 | SD-3 Financial Dashboard |
| 11 | Thu Aug 27 | DP Part 2 & Design-in-Code | SD-4 Jihanki Network |
| 12 | Fri Aug 28 | **★★ MOCK LOOP #2** + weak-spot repair | LLD review, all six |
| 13 | Sat Aug 29 | **★★★ MOCK LOOP #3** — dress rehearsal | — |

**Aug 30–31 — travel.** Primitives by hand on paper, LP rehearsal in your head, scout the building. No LeetCode, no new material, no cramming. Cramming degrades retrieval, which is precisely the axis you've spent 13 days repairing.

---

## The three rules

**1. Blank page, always.** Copilot off, IntelliSense off, no GPT while solving. Plain editor. Paste into LeetCode only after the whole solution is written.

**2. Stuck at 8 minutes? Open `ANSWER_KEY.md` and read only the *Trigger* and *Insight* lines — never the code.** Close it and keep going. At 20 minutes read the code, then close it and rewrite from scratch twice, and add it to the re-solve queue.

**3. Narrate out loud on every problem.** Every Amazon interviewer is assigned Leadership Principles to gather evidence against, and can only score what you say. Silent correct code scores worse than narrated near-correct code.

---

## The re-solve queue — the engine of the whole plan

Keep one file, `resolve_queue.md`. Any problem where you needed a hint, ran over 25 minutes, or wrote buggy code:

```
994 Rotting Oranges  |  failed Aug 20  |  due: Aug 21 ☐   Aug 23 ☐
```

**On 13 days the schedule is +1 day and +3 days** (the old +7 no longer fits). Two clean cold re-solves and it graduates.

**If a day runs short, cut new problems — never the queue.** You have ~224 problems solved already. Coverage is not your bottleneck; production from a blank page is. Re-solves are the only thing that trains it.

---

## Confirmed loop format

- **4 interviews × 60 minutes**, in person, Herndon VA
- **Coding is LiveCode on your own laptop** — typed, not a whiteboard. Bring a laptop and expect Wi-Fi.
- **Design is on a whiteboard** even though coding isn't. Do every LLD and SD brief on paper.
- **GenAI is prohibited during the interview** — which is exactly why the blank-page rule matters now.
- Recruiting is via **Amazon University Talent Acquisition**, so likely **SDE-I**. That's why the six LLDs outrank the four SDs in this plan.

---

## On "100%"

Nobody can guarantee a score — there's a Bar Raiser with veto power and interviewers choose their own questions. What 13 focused days deliver is: your recall deficit repaired, 153 concept-dense problems produced cold rather than recognised, three mock loops behind you, six LLD designs rehearsed, 14 LP stories that end in numbers, and no round you walk into unprepared.

That's the part you control, and it's enough to make you a strong favourite. Aim at that and let the variance be variance.
