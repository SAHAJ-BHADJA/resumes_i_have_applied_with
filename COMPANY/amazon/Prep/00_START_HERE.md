# START HERE — Amazon Prep, Aug 12 → Sept 1
### Herndon, VA (12900 Worldgate Dr, AWS office) · Interview Tue Sept 1

---

## How to use these files

**Open exactly one file per day. Do what it says. Don't read ahead.**

Each daily file is self-contained: the checklist, the primitives to drill, the problems with a timer column, the design brief, the LP task, the journal template, an end-of-day honest check — and **the full solutions at the bottom**, so you never have to go hunting.

**Every solution in every file has been executed and asserted against real test cases**, including the edge cases people actually fail on. Nothing here is untested pseudocode.

---

## The file list

| File | Date | Focus |
|---|---|---|
| `Day01_Aug12_Wed.md` | Wed Aug 12 | Setup + Arrays & Hashing |
| `Day02_Aug13_Thu.md` | Thu Aug 13 | Two Pointers · LLD 1 Parking Lot |
| `Day03_Aug14_Fri.md` | Fri Aug 14 | Sliding Window · HLD 1 Rate Limiter |
| `Day04_Aug15_Sat.md` | Sat Aug 15 | Prefix Sum + Stacks · HLD 2 KV Store |
| `Day05_Aug16_Sun.md` | Sun Aug 16 | Linked Lists · LLD 2 LRU/LFU |
| `Day06_Aug17_Mon.md` | Mon Aug 17 | **★ Consolidation #1 + mini-mock** · HLD 3 S3 |
| `Day07_Aug18_Tue.md` | Tue Aug 18 | Trees pt 1 · **HLD 4 IAM** |
| `Day08_Aug19_Wed.md` | Wed Aug 19 | Trees pt 2 · **HLD 5 Metering & Billing** |
| `Day09_Aug20_Thu.md` | Thu Aug 20 | Grids · LLD 3 Elevator |
| `Day10_Aug21_Fri.md` | Fri Aug 21 | Graphs · HLD 6 Message Queue |
| `Day11_Aug22_Sat.md` | Sat Aug 22 | Heaps + Top-K · HLD 7 Monitoring |
| `Day12_Aug23_Sun.md` | Sun Aug 23 | **★★ Mock Loop #1** (4 rounds) |
| `Day13_Aug24_Mon.md` | Mon Aug 24 | Binary Search · HLD 8 Job Scheduler |
| `Day14_Aug25_Tue.md` | Tue Aug 25 | Intervals + Greedy · LLD 4 Rate Limiter |
| `Day15_Aug26_Wed.md` | Wed Aug 26 | Dynamic Programming · Design review |
| `Day16_Aug27_Thu.md` | Thu Aug 27 | Backtracking/Tries · **★★ Mock Loop #2** |
| `Day17_Aug28_Fri.md` | Fri Aug 28 | **★★ Mock Loop #3** + weak-spot repair |
| `Day18_Aug29_Sat.md` | Sat Aug 29 | **★★★ Mock Loop #4** — dress rehearsal |
| `Day19-20_Aug30-31_TRAVEL.md` | Aug 30–31 + Sept 1 | Travel protocol + **interview day script** |

## New — Block C upgrade

| File | Use |
|---|---|
| `02_GPT_INTERVIEWER_AND_SOLUTION_BOOK.md` | The strict GPT voice-interviewer prompt, plus the solution-book template. **Read this before Day 1's Block C.** |

**The rule that makes it work:** talking is not solving. The session ends when your code *runs*, not when GPT agrees with your approach. And write the book entry **from memory, editor closed** — that second retrieval rep is where most of the value is.

---

## Supporting files (keep open alongside)

| File | Use |
|---|---|
| `00_PRIMITIVES.py` | **Every morning.** Type from memory, then compare. |
| `01_REFERENCE_RoundScript_Triggers_LPs_Design.md` | **The Round Script, all seven Pattern Trigger tables, the LP guide, the design framework, and logistics — consolidated.** This replaces having to dig through other files. |
| `Day1_KEY.md` – `Day7_KEY.md` | Full answer keys by pattern. The daily files already embed the solutions you need, so these are for cross-pattern browsing. |
| `MASTER_PLAN_Aug12_to_Sep1.md` | The overview, the readiness checklist, and the "what will not help" list |
| `Amazon_8_Day_Plan.md` | The original long-form guide. Everything you need day-to-day is already in the reference file above. |

---

## The three rules

**1. Blank page, always.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.

**2. Stuck at 8 minutes? Read only the *Trigger* and *Insight* lines — never the code.** Close it and keep going. At 20 minutes, read the code, then close it and rewrite from scratch twice, and add it to the re-solve queue.

**3. Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code, because every interviewer is assigned Leadership Principles to gather evidence against, and can only score what you say.

---

## The re-solve queue — the engine of the whole plan

Keep one file: `resolve_queue.md`. Every problem where you needed a hint, exceeded 25 minutes, or wrote buggy code gets an entry:

```
994 Rotting Oranges  |  failed Aug 20  |  due: Aug 21 ☐  Aug 23 ☐  Aug 27 ☐
```

**Schedule: +1 day, +3 days, +7 days.** Three clean cold re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If a day runs short, cut new problems — never the queue.** New problems build coverage. Re-solves build recall. Recall is what's broken.

---

## Confirmed format (from the recruiter thread)

- **4 interviews × 60 minutes**, in person at Herndon, VA
- **Coding is on LiveCode** — typed, your own laptop, Wi-Fi needed. **Not a whiteboard.**
- **GenAI is prohibited during the interview.** Exactly why the blank-page rule matters.
- Recruiting is via **Amazon University Talent Acquisition** — the new-grad pipeline, so likely **SDE-I**. If confirmed, weight design prep toward the **four LLDs** over the eight HLDs.
- Lunch buddy requested; vegetarian, no eggs, already communicated.

**Typing vs handwriting:**
- **Code → type it.** You must be able to run it; handwritten code hides your bugs.
- **Design → paper or whiteboard, always.** The in-person design round puts you at a board.
- **Primitives → type daily, handwrite once a week** (Saturdays).
- **No-backspace first pass** when coding: signature → return → fill the middle, delete nothing until you reach the end.

---

## Two things to do today, before any problem

1. **Disable Copilot and IntelliSense.** Five minutes. Non-negotiable.
2. **Email your recruiter** to confirm the team, the round breakdown, and the level — those change how you spend Days 13–18.

---

## On "100%"

Nobody can guarantee a score — there's a Bar Raiser with veto power and interviewers choose their own questions. What these 18 days deliver is: near-total pattern coverage, your recall deficit actually repaired, four full mock loops behind you, and no round you walk into cold. That turns the loop from a coin flip into a strong favourite.

Aim at that. Let the variance be variance.
