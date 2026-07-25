# Mock Round 2 — Codebase #2: `voxel_ingest`

**The cold-read repo.** Save this one for **Monday's dress rehearsal** (and the second half of Saturday if you're moving fast). The whole point is to practice on code you have *not* already memorized — `voxel_alerts` stops being a fair test once you've done it four times.

Different domain (edge frame ingestion, not alerting), different bug classes (geometry, mutable defaults, greedy matching — none of which appear in repo #1), so nothing transfers by muscle memory. You have to actually read it.

**~230 lines across 5 modules. 4 planted bugs (5 failing tests). 4 tasks.**

---

## Setup

```bash
cd practice/voxel_ingest
pip install -r requirements.txt
python -m pytest -q
```

Expect **5 failed, 14 passed**. Four bugs, but two of them each trip two tests — so five red. Part of the exercise is realizing that five failures doesn't mean five bugs.

---

## What this service does

It runs on Voxel's **edge appliance** — the box physically at a customer site. It pulls frames off cameras, batches them for the detector (GPU inference likes batches), and **tracks objects across frames** so the same forklift in consecutive frames is understood as one object, not many. Plus a health monitor, because a camera going silent is the failure mode that matters most for a safety product.

Read in this order: `models.py` (the nouns) → `geometry.py` (boxes) → `tracker.py` (the core) → `batcher.py` → `health.py`.

---

## Run it exactly like Monday's interview

1. **45-minute timer.** One sitting.
2. **Record it.** Screen + audio.
3. **5-minute comprehension pass first** — before touching anything, explain the whole service out loud. Entry points, the core abstraction, the data flow, one thing you'd change. *Then* start.
4. **Narrate everything.** Hypothesis before reading for a bug.
5. **Don't open `SOLUTIONS.md`** until you're done.
6. **Match the existing style.** Type hints, frozen dataclasses, docstrings.

---

## The Tasks

### 🔴 T1 — Four bugs, five red tests. Find them.

```
FAILED tests/test_geometry.py::test_disjoint_boxes_have_zero_iou
FAILED tests/test_geometry.py::test_intersection_of_disjoint_is_zero_not_positive
FAILED tests/test_batcher.py::test_two_batchers_do_not_share_a_buffer
FAILED tests/test_batcher.py::test_flushes_when_full
FAILED tests/test_batcher.py::test_batch_size_is_exactly_max_not_one_over
```

**Do NOT assume five tests means five bugs.** Group them first. Say out loud which failures you think share a root cause *before* you start reading. Two of these bugs each break two tests.

The four bugs, by rough difficulty:

- **One is a classic Python footgun** that every experienced Python dev has been bitten by exactly once and then never forgets. The two-batchers test points right at it. If you know the footgun you'll spot it in ten seconds; if you don't, the *test* will teach it to you, which is worth more than me telling you.
- **One is an off-by-one** in a boundary comparison. The batches come out one too big.
- **One is a geometry bug** that produces a *silently plausible* wrong answer — disjoint boxes reporting a small positive overlap. This is THE bug that quietly destroys a tracker, because every object starts weakly matching every other object. Trace the intersection arithmetic by hand for two boxes that don't touch. **This one is worth the most — it's exactly the kind of bug that passes a casual read and a demo, then corrupts data in production.**
- **The fourth isn't in this list** — it's a logic bug the failing tests above don't cover, hiding in T2. Read on.

> **Difficulty: mixed.** The footgun and the off-by-one are fast once seen. The geometry bug rewards someone who traces values instead of reading for intent. Narrate the trace out loud — that *is* the skill this round grades.

---

### 🔴 T2 — `test_each_detection_claims_a_distinct_track` is failing

```
FAILED tests/test_tracker.py::test_each_detection_claims_a_distinct_track
```

Two forklifts in one frame, both moving slightly into the next frame. You should end with two tracks, each matched to its own predecessor. Instead one forklift silently vanishes.

**This is a real tracking bug and a genuinely instructive one.** Read `Tracker.update` and think about what happens when two detections in the *same frame* both find the same existing track most attractive.

**Then answer out loud:**
- What does "greedy matching" mean here and where does it fall short?
- The fix keeps a set of already-claimed tracks. Where does the check go, and where does the set get populated? (Careful — there's already a `matched_track_ids` set in the code. Is it being used for matching, or only for aging? Those are different jobs.)
- This is the *simplest possible* tracker. What's the principled version? (Say the words "Hungarian algorithm" and "global optimal assignment" and explain why you would *not* reach for it in a 45-minute interview.)

> **Difficulty: medium.** The fix is two lines. Explaining *why* greedy per-detection matching loses an object — and what the real solution would be — is the whole point.

---

### 🟡 T3 — Add a `DEGRADED` state to the health monitor

`HealthMonitor` only knows `ONLINE` and `OFFLINE`. But `CameraState` already defines a third value: `DEGRADED` — "still sending, but dropping frames." A camera limping along at 2fps when it should do 15 is arguably more dangerous than a dead one, because nobody notices.

Extend the monitor to detect it. A camera is `DEGRADED` if it's technically still online (a recent frame) but its **frame rate** has fallen below some threshold.

**The parts that are actually the task:**
- Frame rate needs *history*, not just the last timestamp. What do you store, and how much? An unbounded list per camera is a memory leak on a box that runs for months — say that, and bound it.
- What's the interface? A `frames_per_second(camera_id, now)` helper, then fold it into `state_of`?
- **Confirm the requirement before coding:** what threshold counts as degraded? Over what window? These aren't yours to invent — in the interview you'd ask. Here, state your assumption out loud and make it a constructor parameter.
- Don't break the four existing health tests. Run them after every change.

> The "add a feature to this class" shape. The trick is that doing it properly forces a bounded-history decision, which is the interesting part.

---

### 🟢 T4 — The batcher never flushes a partial final batch

There's a lurking correctness problem the tests don't cover. If frames stop arriving — camera goes offline, shift ends — whatever is sitting in the buffer below `max_batch_size` **never gets flushed**, because `add()` is the only thing that triggers a flush and nothing is calling `add()` anymore. Those frames are silently stranded.

This is the same class of bug as the alerting repo's "ongoing hazard never re-alerts" — a thing that works on the happy path and quietly fails at the boundary.

**Discuss and then implement:**
- The real fix is time-driven: a periodic flush, independent of arrivals. In a synchronous practice repo, how do you model that testably? (A `flush_if_stale(now)` the caller's loop invokes every tick — inject the clock, don't call `time.time()` inside.)
- Write the test that proves stranded frames get flushed.
- **The deeper point:** the current design conflates "a frame arrived" with "time passed." Those are different triggers and the batcher needs both. Say that out loud — recognizing that two distinct events were collapsed into one is the senior observation.

> The "extend this to handle a new case" shape, and a reprise of the injected-clock idea from repo #1's T8 — deliberately, so you get a second rep at it on unfamiliar code.

---

## Escalation — if you finish early

Out loud, no code needed:

1. **The tracker is O(detections × tracks) per frame.** Fine for tens of objects. At what point does it hurt, and what would you do? (Spatial hashing / grid so you only compare nearby boxes.)
2. **`Track.history` grows without bound** — every box for every object forever. On an appliance running for weeks, then what? (Ring buffer, or store only the last N.)
3. **The tracker never emits "track ended" events.** A forklift that leaves frame just... disappears from the dict when it ages out. Who needs to know it left, and how would you tell them?
4. **`_next_id` monotonically increases and never resets.** On a box that runs for months, is that a problem? (Probably not — it's an int — but say why you checked.)
5. **Nothing here is thread-safe.** The batcher's sink might run on another thread. Where's the race, and does it matter for this deployment?
6. **The IoU threshold is a single global constant.** A camera watching a loading dock (big, slow forklifts) and one watching a doorway (small, fast people) want different thresholds. How would you make it per-camera or per-label without uglifying the tracker?
7. **How would you test the tracker against real drift** — an object that moves a little each frame for 100 frames? (Property-style test: generate a smooth trajectory, assert the track_id stays constant.)

---

## Score yourself

Same rubric as repo #1 — watch the recording and check:

| | ✅ / ❌ |
|---|---|
| Did I do the 5-minute comprehension pass before touching code? | |
| Did I group the failing tests and hypothesize shared causes *first*? | |
| Did I trace the geometry bug with actual numbers, out loud? | |
| Did I confirm the T3 threshold assumption instead of silently inventing it? | |
| Minimal diffs — did I avoid rewriting working code? | |
| Did I run the tests after every change? | |
| Did I stay narrating, never silent >20s? | |
| For each bug: did I explain the *mechanism*, not just patch it? | |

**The geometry bug is the tell.** "I added `max(0, ...)`" is a patch. "Disjoint boxes gave a negative width times a negative height, which is a *positive* area, so non-overlapping objects reported overlap and the whole tracker's matching was quietly corrupt" is understanding — and it's the difference between the two candidates this round is designed to separate.
