# Voxel AI — 4-Day Prep Plan
### Fri Jul 17 → Mon Jul 20 · Interviews Tue Jul 21 & Wed Jul 22 · ~6 hrs/day · 24 hours

---

## Do this before you start (5 minutes, today)

**Email your recruiter. Two questions, one paragraph:**
1. **Which rounds fall on which day?** You have two days; the public reports describe a one-day loop. You need the split.
2. **What tool does the Systems Discussion round use** — a whiteboard app (Excalidraw/Miro), a shared text editor, or just talking?

Question 2 is the one nobody asks, and it changes how you rehearse Sunday. Whiteboard tool → practice *in it*, with a trackpad, on a timer. Shared editor → you're typing ASCII, and the diagrams in `03` are already in that format. Voice only → your verbal structure carries everything.

---

## How the time is allocated, and why

You asked to weight toward Code Modification and System Design. **That's the right call. Here's the arithmetic:**

| Round | Hours | Why |
|---|---|---|
| **Code Modification / Debugging** | **~9.5** | Least public prep material. Highest differentiation. The round people bomb — your notes say so, and Voxel's own JD ("pairing with senior engineers") says so. |
| **System Design** | **~7** | Two confirmed questions. High signal. Reproducible — one skeleton, three reskins. |
| **Code Creation** | **~4** | Most public prep material. Confirmed Easy+Medium. You've likely done most of it already. |
| **Behavioral** | **~2.5** | The stories are already yours. This is rehearsal, not learning. |

### On "Code Creation is just LeetCode medium, right?"

**Mostly yes — but the difficulty was never the risk.**

- ✅ **True:** Easy + Medium per the Jan 2026 Glassdoor report. Most-documented round. Compressing it is correct.
- ⚠️ **But:** a Mar 2026 Platform-role candidate reports problem 2 hitting **Medium-Hard**. Different role, possibly a different round — but don't treat "medium" as a ceiling.
- 🚨 **And the real one:** at easy/medium, *everyone solves it*. The differentiator is **narration and bug-free execution** — a completely separate skill from solving. You can have 500 LeetCode problems behind you and still lose this round by going quiet for 90 seconds or saying "done" before tracing an example.

**So the compression is: cut the pattern coverage hard, keep every narration rep.**

Friday drills only the three **confirmed** areas — parentheses, tree symmetry, graph paths. Hash maps, two pointers, sliding window, DP, binary search, and linked lists are now **reference only**. They're still in `01` if a gap opens. They're not on the schedule.

### One correction: "Code Modification" and "Code Debugging" are the same round

Not two. The Jan 2026 candidate calls it **Code Modification**; the Mar 2026 candidate calls it **Debugging**. Same slot, same 45 minutes. That's useful news — it means the round leans *harder* toward bug-hunting than "modification" implies, which is exactly the shape of your practice repo (3 planted bugs, 5 red tests).

---

## Your four rounds

| Round | Length | What it really tests | File |
|---|---|---|---|
| **1. Code Creation** *(a.k.a. Coding)* | ~45 min | LC easy + medium. **Communication + zero fumbles.** | `01_ROUND1_CODE_CREATION.md` |
| **2. Code Modification** *(a.k.a. Debugging)* | ~45 min | Read unfamiliar Python — **bigger than you expect** — fix/extend it collaboratively. | `02` + **two** practice repos |
| **3. Systems Discussion** | ~45–50 min | **High-level design.** Event notification / job scheduler. | `03_ROUND3_SYSTEM_DESIGN.md` |
| **4. Communication & Collaboration** | ~45 min | STAR stories. Collaboration is the theme. | `04_ROUND4_BEHAVIORAL.md` |

Company facts: `05_COMPANY_BRIEF.md` · LLD hedge (45 min, Sunday): `06_LLD_INSURANCE.md`

**On Round 3 being HLD:** boxes, arrows, trade-offs. You are **not** implementing classes. But you *do* write the API sketch and the schema — that's specification, not coding, and it's 13 of your 50 minutes. Hearing "high level" and staying purely verbal is how you read as hand-wavy.

---

## The arc

```
FRI  ██▓▓░░   Diagnostic → the 3 confirmed patterns → Code Mod head start
SAT  ██████   CODE MODIFICATION — the whole day. Your edge.
SUN  ██████   SYSTEM DESIGN — the whole day + the LLD hedge.
MON  ██▓▓▓▓   Behavioral → full dress rehearsal, all 4 rounds → taper.
```

**Non-negotiables, every day:**
1. **Talk out loud.** Every problem. Silent solving trains the wrong muscle.
2. **Record once a day.** Watch two minutes back. Unpleasant; highest-ROI two minutes in the plan.
3. **Autocomplete off** for at least one problem a day. CoderPad has no linter.

---
---

# FRIDAY — Jul 17
## Diagnostic → the three confirmed patterns → Code Mod head start

> **Today is the only Code Creation day.** It's compressed on purpose. The diagnostic tells you whether that compression is safe for *you*.

| Time | Block | What you do |
|---|---|---|
| **0:00–0:45** | 🔬 **THE DIAGNOSTIC** | 45-min timer. Recorded. No IDE help, autocomplete off. **LC 20 (Valid Parentheses)**, then **LC 200 (Number of Islands)**. Narrate the whole time. Full script: `01`, §The Script. |
| 0:45–1:00 | **Score it** | Watch it back against the checklist below. **Be honest.** Apply the decision rule. |
| 1:00–2:30 | ⭐ **Stacks & parentheses** | `01`, §Pattern 4. **A LC medium on parentheses is confirmed on Glassdoor.** Order: 4.1 → 4.2 → 4.3 → 4.6 → 4.7. **4.2 (Min Remove to Make Valid) is my single biggest bet — do it twice.** |
| 2:30–2:45 | Break | Away from the screen. |
| 2:45–4:00 | ⭐ **Binary trees** | `01`, §Pattern 5. **Symmetry is confirmed in the 1P3A OA report.** Order: 5.1 → 5.1 again *iteratively* → 5.4 → 5.5 → 5.6 → 5.7. |
| 4:00–4:15 | Break | |
| 4:15–5:30 | ⭐ **Graphs, BFS/DFS** | `01`, §Pattern 6. **"Graph paths" is confirmed in the OA report.** Order: 6.1 → 6.2 → 6.3 → 6.4. (6.4 Course Schedule pays off again Sunday — it's the DAG check in the job scheduler.) |
| 5:30–6:00 | 🔧 **Code Mod head start** | Set up `practice/voxel_alerts/`: `pip install -r requirements.txt && python -m pytest -q` → confirm **5 failed, 20 passed**. Read `02` end to end. Stop there. |

### 🔬 The Diagnostic — score yourself honestly

| | ✅ / ❌ |
|---|---|
| 1. Asked clarifying questions **before** typing | |
| 2. Stated the brute force **and** its complexity | |
| 3. Stated the optimal complexity **before** coding | |
| 4. Never went silent longer than ~15 seconds | |
| 5. Variable names a stranger could read | |
| 6. **Dry-ran a real example out loud before saying "done"** | |
| 7. Named ≥2 edge cases unprompted | |
| 8. Finished both inside 45 minutes | |

### The decision rule — apply it at 1:00

| Score | Verdict |
|---|---|
| **7–8 ✅, finished in time** | **The compressed plan is safe.** Proceed exactly as written. Code Creation is not your problem. |
| **5–6 ✅** | **Proceed — but your gaps are narration gaps, not algorithm gaps.** Every problem today is a talk-out-loud rep. No silent solving. Re-check at 5:30. |
| **≤4 ✅, or you didn't finish** | **Stop. Change the plan.** Take today's 5:30–6:00 block *and* Saturday's 5:15–6:00 block (T7/T8 refactor) and spend both on `01` Patterns 1–3. You lose the refactor reps — the least likely task shape. You keep coverage. **This is the documented failure mode; the trade is worth it.** |

**Whatever the score: do not skip the recording.** Item 6 is the one people fail, and you cannot self-assess it from memory.

**Friday done when:** you can write the BFS and DFS templates cold, and you've said Symmetric Tree's core insight out loud — *"I'm not comparing a tree to itself, I'm walking two pointers in opposite directions."*

---
---

# SATURDAY — Jul 18
## 🔧 CODE MODIFICATION — the whole day
### The round with the least public prep material. This is where you win.

> ⚠️ **A real April 2026 candidate, on this exact round:** *"the problem had an unnecessarily lengthy description, and the codebase was quite large. It took some time to understand the pattern and get up to speed."*
>
> **They ran out of runway on comprehension, not coding.** Your repo is 280 lines; theirs was bigger. That's why Exercise A gets 90 minutes today.

| Time | Block | What you do |
|---|---|---|
| 0:00–0:30 | **Re-read `02`** | Specifically §The workflow. You read it last night; today you execute it. |
| **0:30–2:00** | 🎯 **Exercise A — comprehension** | **The most important block in the whole plan.** 5-min timer, recorded, no scrolling back. Explain the flow out loud. Check against `SOLUTIONS.md` §Exercise A. **Repeat until 5 minutes is genuinely enough** — four or five reps. This is precisely the skill the April candidate lacked. |
| 2:00–2:15 | Break | |
| **2:15–4:00** | 🐛 **T1 · T2 · T3 — the bugs** | The three planted bugs. Narrate every second. **Say your hypothesis out loud *before* reading for the bug.** T2 is three red tests from one root cause — spot that, say it. |
| 4:00–4:15 | Break | |
| 4:15–5:15 | ➕ **T4 · T5 · T6 — extend** | Features without breaking existing patterns. **T6 (quiet hours) is deliberately under-specified — the test is whether you ask "whose midnight?" instead of coding silently.** |
| 5:15–6:00 | 🔨 **T7 · T8 + cold-read warm-up** | Refactor + inject the clock. Then open **`practice/voxel_ingest/`** — the second codebase, which you have *not* seen — and do just the 5-minute comprehension pass on it. Don't solve it yet; save that for Monday. |

**Leave one task unopened for Monday's rehearsal.** Pick whichever you're least drawn to — you want one genuinely unseen problem under real conditions.

**Saturday done when:** you can open an unfamiliar 300-line Python codebase and, in five minutes, name the entry point, the core abstraction, the data flow, and one thing you'd change — **without scrolling back**.

---
---

# SUNDAY — Jul 19
## 🏛 SYSTEM DESIGN — the whole day
### Both confirmed questions are the same shape. Learn one skeleton, reskin it three ways.

| Time | Block | What you do |
|---|---|---|
| 0:00–0:20 | **The skeleton** | `03`, §The 50-minute skeleton + §Back-of-envelope kit. **Memorize the clock and the numbers.** Everything today runs on this. |
| **0:20–1:45** | ⭐ **Design 1 — Event notification** | ✅ Confirmed asked. Read §Design 1 → **close the file** → rebuild from scratch, out loud, 45-min timer → compare. **The gap between your version and the file is your study list.** |
| 1:45–2:00 | Break | |
| **2:00–3:25** | ⭐ **Design 2 — Job scheduler** | ✅ Confirmed asked. Same drill: read → close → rebuild cold. Notice how much of the skeleton carried over from Design 1. That's the point. |
| 3:25–3:40 | Break | |
| 3:40–4:25 | **Design 3 — Video pipeline** | Voxel's actual architecture. Connecting your design back to their product is explicitly a plus. Lighter — read it, say the four key points out loud, move on. |
| 4:25–5:10 | 🛡 **LLD hedge** | `06_LLD_INSURANCE.md`. Say the dense-vector memory-layout paragraph out loud twice. Skim the IoU trap. **45 min, then stop.** Insurance, not the main event. |
| 5:10–5:40 | ⚖️ **Trade-off rapid fire** | `03`, §Trade-off Drills. 60 seconds each, out loud, no notes. SQL vs NoSQL · push vs pull · sync vs async · at-least-once vs exactly-once. |
| 5:40–6:00 | 🔗 **Bridge problems** | `01`, §7.1 Merge Intervals · §7.3 Task Scheduler · §8.2 Logger Rate Limiter. These sit between coding and design. Quick reps. |

**Sunday done when:** you can draw the event-notification architecture in 4 minutes, defend every arrow, and say in one sentence which part is genuinely hard — *dedup and rate limiting, not throughput*.

---
---

# MONDAY — Jul 20
## Behavioral → full dress rehearsal → **taper**

| Time | Block | What you do |
|---|---|---|
| 0:00–1:15 | 🗣 **The Six STAR stories** | `04`, §The Six. Write all six. Then say each out loud, **timed to 2:00**, recorded. **Every story ends on a number** — dig through old PRs if you have to. |
| 1:15–1:45 | **"Why Voxel" + your questions** | `04`, §Why Voxel and §Questions To Ask Them. Rehearse until it's conviction, not recitation. |
| 1:45–2:00 | Break | |
| **2:00–2:45** | 🎬 **MOCK — Round 1** | 45 min. **LC 101 (Symmetric Tree) + LC 1249 (Min Remove).** Both confirmed/high-bet. Timed, recorded, no help. Score the 8-point checklist again — compare to Friday. |
| **2:45–3:30** | 🎬 **MOCK — Round 2** | 45 min. **`practice/voxel_ingest/` — the second codebase, fully cold.** This is why it exists: real unfamiliar code, not the repo you've done four times. |
| 3:30–3:45 | Break | |
| **3:45–4:35** | 🎬 **MOCK — Round 3** | 50 min. Pick a design at random. Full skeleton, on the clock. |
| **4:35–5:20** | 🎬 **MOCK — Round 4** | 45 min. Have a friend fire questions from `04`, §The Question Bank. Random order, no warning. |
| 5:20–5:45 | **Logistics** | Test Meet: camera, mic, screen share. Charge everything. Print `04`, §The Card. Two alarms. |
| 5:45–6:00 | **Stop** | Close the laptop. |

**Monday is done when you stop.** No cramming Monday night or Tuesday night. Fatigue in the final round is the documented failure mode, and sleep is a prep activity — not a reward.

---
---

# Interview Day Playbook

## The night before each day
Re-read **only** `04`, §The Card. Ten minutes. Nothing else. Sleep 8 hours.

## 60 minutes before
One **easy problem you've already solved**, out loud, to warm the narration muscle. **Not** a new problem — you're warming up, not learning. Read "why Voxel" once. Eat something real.

## Round 1 — Code Creation
The five beats, no exceptions:
1. **Clarify** constraints + edge cases, keyboard untouched (2 min)
2. **Brute force + complexity** (1 min) — *never skip, even when obvious*
3. **Optimal + complexity**, get the nod (2 min)
4. **Code**, narrating the *why* (12–20 min)
5. **Dry run out loud, line by line, before saying "done"** (3–5 min)

Pace: ~12 min on the first, 25+ on the second.

## Round 2 — Code Modification / Debugging
1. **Skim structure first** — entry points, classes, data flow. Say what you see.
2. **Verbalize your model back to them.** Free correction, free signal.
3. **Confirm the requirement.** "So you want X, and Y keeps working — right?"
4. **Minimal, clean diff.** Match their style. Do not rewrite.
5. **Run or trace the tests.**
6. **Ask questions constantly.** Silence reads as a fail.

> **Stuck out loud is a pass. Stuck silently is a fail.**

## Round 3 — Systems
Requirements + numbers (5) → API (3) → schema (5) → **one clean diagram** (10) → deep dive (15) → trade-offs + failure (8) → wrap (2).

**First 30 seconds:** if they say "design a *library* / class / API" → switch to `06`. If bare "design X" → *"Quick scope check: distributed architecture, or the object model and API?"* If they shrug → HLD.

Fundamentals, not exotic scale. Say *"I'd start with Postgres and revisit above ~10k writes/sec."* Raise privacy yourself. Raise the silent-camera-failure mode yourself. Close with *"this is basically what Actions does."*

## Round 4 — Collaboration
STAR, 2 min, land the **result with a number**. Every story has another human in it. Ask your questions.

## Immediately after each day
- ☐ **Same-day thank-you note.** A candidate got positive verbal feedback and was then ghosted — don't be quiet.
- ☐ **Log every question you were asked**, while it's fresh. It preps you for day 2.
- ☐ **Recruiter follow-up at +3 business days** if you hear nothing.

---

## The five things that actually decide this

1. **You never go silent.** At easy/medium, communication *is* the evaluation.
2. **You don't fumble Round 2.** Least-prepped round, most differentiating. You'll have 9+ hours and 8 reps in it.
3. **Your design connects to their product.** *"This is basically what Actions does"* is a line that wins rounds.
4. **Your "why Voxel" is real.** ~3M preventable US workplace injuries a year — a rare case where the engineering problem and the reason to care are the same problem.
5. **You're not tired.** Taper Monday. Sleep. Show up fresh.

---

## One honest note

Nobody can promise 100%. A March 2026 candidate had every remaining round cancelled mid-loop for headcount reasons — no amount of prep touches that. What prep *does* touch is the thing that sank the last documented rejection: his own retrospective says the rounds weren't hard, he was **underprepared across all of them**. Breadth beats depth here, and breadth is a four-day problem.

Go.
