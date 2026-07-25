# Round 2 — Code Modification
### ~45 min · Unfamiliar Python codebase · Read → extend / fix / refactor, with the interviewer
### **This is the round that decides your loop.**

---

## Why this round is your biggest opportunity

Everyone interviewing at Voxel on the 21st has ground LeetCode. Almost none of them have practiced *this*. Your own notes say it: **"This is the round most people under-prepare for."**

It's also the round with the highest signal-to-noise for Voxel specifically, because look at what their job posting says the role is:

> <cite index="21-1">an engineer with 0-4 years of professional experience who wants to grow quickly by **pairing with senior engineers**, owning features, and working across the application lifecycle</cite>

**Round 2 is not a coding test. It is a simulation of your first week.** They are answering one question: *is pairing with this person pleasant and productive?* Everything below serves that.

---

## What you'll be handed

From your notes, their stack, and a **April 2026 Glassdoor report**:
- **Python.** Near-certain.
- **Larger than you'd expect.** An April 2026 candidate described this exact round: <cite index="67-1">the problem had an unnecessarily lengthy description, and the codebase was quite large — it took time to understand the pattern and get up to speed</cite>. **They ran out of runway on comprehension, not coding.** Your practice repo is ~280 lines; budget for 2–3× that plus a wall of prose to read first.
- **Domain-flavored** — "don't be surprised if the code models something like sensors, events, cameras, or alerts."
- One of three task shapes:
  1. *"Add a new method/feature to this class"*
  2. *"This test fails — find and fix the bug"* ← a Mar 2026 report calls this round **"Debugging"** outright
  3. *"Extend this system to handle a new event type"*

Your `practice/voxel_alerts/` repo is built to be exactly this. Eight tasks, all three shapes, right domain.

> **The size warning changes one thing:** the structure-first skim in Phase 1 isn't a stylistic preference, it's the only way through. The April candidate's failure mode was reading linearly and running out of time. **Do Exercise A until 5 minutes is genuinely enough.**

---

## The workflow — follow it in this order, every time

### Phase 1 — Skim structure (3–5 min). **Do not read line by line.**

The instinct is to start at line 1 of the first file and read down. **Resist it.** You'll burn 15 of your 45 minutes and still not know how it fits together.

Instead, in this order:
1. **File list.** What are the modules? The names tell you the architecture for free.
2. **The entry point.** What does a caller actually invoke? Start there and read *outward*.
3. **The data model.** What are the nouns? What's immutable, what's mutable, what's an enum?
4. **The tests.** Tests are documentation that can't lie. If there's a test suite, it tells you the intended behavior faster than the source.
5. **Only then** read implementation, and only the parts on the path to your task.

**Say what you're doing while you do it:**
> "I'm going to skim the structure before diving in — I see six modules, and the names suggest models, a pipeline, and then three collaborators: dedup, rate limiting, channels. Let me start at the pipeline since that looks like the orchestrator... yeah, `process` is the entry point and there's a flow docstring at the top. Great."

### Phase 2 — Verbalize your model (2–3 min). **The free-points phase.**

Say your understanding back to them **before** you touch anything:

> "So my read is: a detection comes in, gets deduped against recent hazards on the same camera, then we fan out to matching subscriptions, rate limit per person, render, and send. The dispatcher module looks like a separate seam that isn't wired in yet. Is that right — am I missing anything?"

**This is the single highest-value 30 seconds of the round.** Three reasons:
- If you're wrong, they correct you **now** instead of after you've written 40 lines against a bad model.
- It demonstrates you can build a mental model of unfamiliar code, which is *literally the skill being tested*.
- It's collaborative. It makes them a participant. The round is named "pair programming" for a reason.

### Phase 3 — Confirm the requirement (1–2 min)

**Never start coding off the first statement of the task.** Play it back with your assumptions made explicit:

> "So you want quiet hours per subscription, and critical alerts should still get through. Two things I want to check: is the window site-local or subscriber-local time? And should existing subscriptions without quiet hours keep working unchanged — I'm assuming yes, so I'd default it to None?"

Voxel's Round 2 is explicitly collaborative. **Under-specification is often deliberate.** T6 in your practice repo is built this way on purpose.

### Phase 4 — Minimal, clean changes

**From your notes, verbatim:** *"Don't rewrite everything; interviewers grade whether you respect existing patterns and conventions."*

Match what's there:
- Type hints? **Use them.** No type hints? Don't add them to code you didn't touch.
- Docstring style? Copy it exactly.
- Naming? `snake_case`, `_private` — mirror the file.
- `dataclass` used elsewhere? Use `dataclass`, not a hand-rolled `__init__`.

**Things that will cost you the round:**
- ❌ Rewriting a working function because you'd have written it differently
- ❌ Introducing a new dependency
- ❌ Reformatting the file
- ❌ Adding an abstraction "for the future"
- ❌ Changing three things when the task asked for one

**The mental model:** you're opening a PR against a codebase you joined yesterday. A 12-line diff that does exactly the thing gets merged. A 200-line diff that "improves" things gets a very awkward comment thread.

### Phase 5 — Run or trace the tests

Run them if you can. If not, **trace by hand out loud**:
> "Let me trace `test_ongoing_hazard_realerts_every_window`. First call, t=1000, `last` is None so it returns False and stamps 1000. Second call, t=1030, `last` is 1000, diff is 30, less than 60, so True — duplicate, correct. But watch: it *also* stamped 1030. So at t=1060, `last` is 1030, diff is 30... still a duplicate. There it is."

**Finding a bug by tracing values out loud is the best thing that can happen to you in this round.** It's the exact skill they're hiring for.

### Phase 6 — Ask questions constantly

**From your notes:** *"Treat the interviewer like a teammate doing pair programming, not an examiner."*

Good questions, banked and ready:
- "Is there a test suite I should be running, or do you want me to trace by hand?"
- "Should I match this existing pattern, or is that something you'd want changed?"
- "Do you want me to handle that edge case now or note it and move on?"
- "Is this code you'd want a test for, or is that out of scope for the exercise?"
- "I notice X seems unused — is that intentional or am I missing a caller?"
- "Would you rather I fix this properly or do the minimal thing that unblocks the task?"

**That last one is a genuinely great question.** It surfaces the scope/quality trade-off explicitly and lets them tell you what they're grading.

---

## Reading unfamiliar code fast — the drill

**Do this daily. It's a trainable skill and almost nobody trains it.**

1. Clone a Python repo you've never seen. Good targets: `httpx`, `rich`, `pydantic`, `click`, `flask`, `requests`.
2. Pick one module.
3. **5-minute timer. Recorded.** Explain out loud:
   - The entry point
   - The core abstraction
   - The data flow
   - One design decision the author made and why
   - One thing you'd change
4. Then read properly and see what you missed.

**Do this three times.** By the third, you'll notice you've stopped reading top-to-bottom and started reading structure-first. That's the whole skill.

---

## The four sentences that win this round

Bank these. Say them when they apply — they apply constantly.

1. **"Let me say back what I think this does before I change anything."** → catches misunderstandings for free
2. **"I could fix this properly or do the minimal thing — which do you want?"** → surfaces scope explicitly
3. **"That's a better idea than mine, let's do that."** → their JD says **coachable**. Prove it.
4. **"This isn't part of the task, but I noticed X — want me to note it or handle it?"** → attentive without scope-creeping

---

## The failure modes — and how you avoid each one

| Failure | What it looks like | The fix |
|---|---|---|
| **Silent reading** | 8 minutes of scrolling, no words | Narrate your skim. Say what you're looking for and what you found. |
| **Line-by-line** | Starting at line 1, running out of time | Structure first. Entry point second. Details only on the path to your task. |
| **Assumption coding** | Building the wrong thing correctly | Phase 3. Always. Play the requirement back. |
| **The rewrite** | "Actually I'd restructure this whole class" | Minimal diff. You are a new hire, not the architect. |
| **Ego defense** | Arguing when they suggest something | "Oh, that's cleaner — let's do it." Coachable is on their JD. |
| **Patching the symptom** | `<=` → `<` with no explanation | Explain the *mechanism*. Why did it happen? |
| **Test amnesia** | Never running them | Run after every change. Say "let me re-run." |
| **The freeze** | Stuck and silent | Say what you tried, what you expected, what you got. Being stuck is fine. Being stuck *silently* is not. |

**On being stuck:** this is the one people handle worst. You are *allowed* to be stuck. This is pair programming — your partner is *right there*. What kills you is going quiet. Say:

> "I expected the window to reset here but it isn't. Let me check whether the timestamp is what I think it is... I'm going to add a print. Actually — wait. It's stamping on every call, not just when it alerts."

**That's not a failure. That's the recording they'd play for the hiring committee.**

---

## Two practice codebases — use them differently

You have **two** full mock codebases, deliberately different so the second is a fair test of cold reading:

| Repo | Domain | Bug classes | When |
|---|---|---|---|
| **`practice/voxel_alerts/`** | Alerting pipeline (dedup, rate limit, fan-out) | State/timing, off-by-one, exception isolation | **Saturday** — learn the workflow on it, 8 tasks |
| **`practice/voxel_ingest/`** | Edge frame ingestion (batching, object tracking) | Mutable default, geometry, greedy matching | **Monday mock** — fully cold, 4 tasks |

**Do `voxel_alerts` Saturday. Save `voxel_ingest` for Monday's dress rehearsal**, unopened, so you get one genuine cold read under real conditions — which is the actual skill this round tests. Each repo has its own `README.md` (tasks) and `SOLUTIONS.md` (check yourself after).

---

## Your SATURDAY schedule (mapped to `practice/voxel_alerts/`)

| Time | Task | Skill |
|---|---|---|
*(Setup happens Friday 5:30–6:00 so you start Saturday with the repo already running.)*

| Time | Task | Skill |
|---|---|---|
| 0:00–0:30 | Re-read this file, §The workflow | Loading the process |
| **0:30–2:00** | 🎯 **Exercise A** — 5-min comprehension drill, recorded, **4–5 reps till clean** | **Reading fast — the block that matters most** |
| 2:00–2:15 | Break | |
| **2:15–4:00** | 🐛 **T1, T2, T3** — the bugs | Debugging out loud |
| 4:00–4:15 | Break | |
| 4:15–5:15 | ➕ **T4, T5, T6** — the features | Extending without breaking |
| 5:15–6:00 | 🔨 **T7, T8** + a wild OSS repo drill | Refactoring + cold reading |

**Save one task for Monday's dress rehearsal.** You want one genuinely unseen problem under real conditions.

> **Why Exercise A gets 90 minutes:** the April 2026 candidate failed this round on comprehension runway, not coding. Everything else on this schedule assumes you can build a mental model of the codebase fast. If you can't, the tasks don't matter.

---

## The 60 seconds before Round 2 starts

Read this. Nothing else.

> **Skim structure. Say it back. Confirm the ask. Minimal diff. Run the tests. Never go quiet.**
>
> They are not testing whether I can code. They're testing whether pairing with me is pleasant.
>
> Being stuck out loud is a pass. Being stuck silently is a fail.
