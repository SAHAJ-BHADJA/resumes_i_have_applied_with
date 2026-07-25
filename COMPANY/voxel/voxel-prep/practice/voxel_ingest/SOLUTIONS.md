# Solutions — `voxel_ingest`. Read only after attempting.

---

## Exercise A — what a good 5-minute walkthrough sounds like

> "This runs on the edge appliance — the box at the customer site. Entry points are `FrameBatcher.add` and `Tracker.update`; those are the two things a capture loop would call per frame.
>
> The nouns are in `models.py`: `Frame` is one decoded image from one camera, `Detection` is one object found in a frame *before* it has an identity, `Track` is an object followed across frames — so one real forklift is one `Track` accumulating `Detection`s. `BBox` is a frozen box with `area` and `center` helpers.
>
> Flow: frames come off cameras → `FrameBatcher` accumulates them and flushes a batch to a detector when it's full or stale → detector produces `Detection`s → `Tracker.update` matches each detection to an existing track by label and IoU overlap, creates tracks for the unmatched, and ages out tracks not seen recently. Separately, `HealthMonitor` watches frame arrivals per camera and reports liveness.
>
> The core abstraction is the track-matching in `Tracker.update` — everything else feeds it. The geometry module is load-bearing because matching *is* IoU.
>
> One thing I'd flag immediately: `HealthMonitor` defines a `DEGRADED` state in the enum but never emits it — so there's a designed-for case that isn't implemented. I'd want to know if that's intentional or unfinished."

**Why it's good:** entry points first, nouns second, flow third, names the load-bearing piece, and spots the unimplemented enum value — which is literally T3. Noticing dead/unfinished code during the read is exactly the attentiveness this round rewards.

---

## T1 — the four bugs

### Bug 1 — Mutable default argument *(the footgun)*

```python
def __init__(self, sink, max_batch_size=8, max_wait_seconds=0.5, buffer=[]):
                                                                 # ↑ evaluated ONCE
```

`buffer=[]` is evaluated a single time, when the function is *defined* — not per call. Every `FrameBatcher` built without an explicit `buffer` shares **the same list object**. One camera's frames land in another camera's batch.

**Fix:**
```python
def __init__(self, sink, max_batch_size=8, max_wait_seconds=0.5, buffer=None):
    ...
    self.buffer = buffer if buffer is not None else []
```

**What to say:**
> "Classic mutable-default-argument bug. `buffer=[]` is bound once at definition, so every instance without an explicit buffer shares one list. On an appliance running many cameras through many batchers, their frames cross-contaminate. The fix is the standard `None` sentinel — default to `None`, allocate a fresh list in the body."

**Note the test fixtures pass `buffer=[]` explicitly** — that's why only the *one* test that omits it catches this. Point that out: *"the other tests accidentally hide the bug by passing buffer explicitly; only the test that constructs two batchers the natural way exposes it. That's a lesson about tests too — a fixture that's too careful can mask the exact bug you'd hit in prod."*

---

### Bug 2 — Off-by-one in the flush condition

```python
if len(self.buffer) > self.max_batch_size or ...:   # ← > lets it reach max+1
```

The append happens, *then* the check. With `> max_batch_size`, the buffer has to exceed the max before flushing, so batches come out one too big — size 5 for a max of 4.

**Fix:** `>=`.

**What to say:**
> "Append-then-check with a strict `>`, so it only flushes once the buffer is already over the limit — batches are `max + 1`. `>=` fixes it. Same family as the rate-limiter off-by-one, actually — the check runs relative to the wrong side of the append."

*(If you did repo #1: yes, this is deliberately the same shape as that rate limiter's `<=` bug. Two reps of "where does the boundary check sit relative to the mutation" on different code.)*

---

### Bug 3 — Intersection of disjoint boxes *(the important one)*

```python
width = right - left       # can be NEGATIVE when boxes don't overlap
height = bottom - top      # also negative
return width * height      # negative × negative = POSITIVE → phantom overlap
```

When boxes don't overlap, `right < left`, so `width` is negative. Same for height. Their product is *positive* — a phantom intersection. Disjoint boxes report overlap, IoU is nonzero, and the tracker starts matching objects that are nowhere near each other.

**Fix:**
```python
width = max(0.0, right - left)
height = max(0.0, bottom - top)
return width * height
```

**What to say — this is the one that shows understanding:**
> "This is the bug that silently corrupts everything downstream. When two boxes are disjoint, `right - left` is negative and so is `bottom - top`, and negative times negative is positive — so the function reports a real-looking overlap for boxes that don't touch. IoU comes out nonzero, and now every object weakly matches every other object, so track identities scramble. It passes a casual read because the code *looks* like standard intersection math, and it passes a demo because objects that actually overlap still work. It only shows up as mysterious identity-swapping in production. Clamp each dimension to zero and it's correct."

**Why it fools the union guard sometimes:** for boxes that are far apart, the phantom intersection can exceed the box areas, making `union` negative, which the `union <= 0` guard catches and returns 0.0 — so the bug is *inconsistent*, which is even worse than being always-wrong. Mention this: *"and it's not even consistently wrong — for distant boxes the phantom area is huge and the union guard accidentally masks it, so you get zero sometimes and garbage other times. Inconsistent bugs are the hardest to track down, which is another reason to clamp at the source."*

---

## T2 — the tracker loses an object

### The bug
`Tracker.update` matches each detection to the best track independently, and **never removes a track from contention once it's claimed.** Two detections in the same frame can both pick the same track. The first assigns it, the second *re-assigns* it (overwriting `last_box`, incrementing `hit_count` again), and the second detection's real predecessor is never matched — so one object silently merges into another.

Note the code already has a `matched_track_ids` set, but it's only used for aging bookkeeping, not consulted during matching. The fix threads it into the match loop.

### The fix
```python
for track in self._tracks.values():
    if track.label != detection.label:
        continue
    if track.track_id in matched_track_ids:   # ← already claimed this frame
        continue
    score = iou(track.last_box, detection.box)
    if score >= best_iou:
        best_iou = score
        best_track = track
```

### What to say
> "It's greedy per-detection matching with no exclusion — each detection independently grabs its favourite track, and nothing stops two detections in one frame from grabbing the same track. The second overwrites the first's assignment and the second object's real track never gets matched, so two objects collapse into one. The set to track claims already exists in the code, it's just not consulted during matching — I thread it in so a claimed track is skipped."

### The follow-up — the principled version
> "This greedy approach is order-dependent and locally optimal — if detection A slightly prefers track 1 but detection B *strongly* needs track 1, greedy might give it to A and strand B. The correct formulation is a **global optimal assignment** — build the full IoU cost matrix between detections and tracks and solve it with the **Hungarian algorithm**, which minimizes total assignment cost. That's what real trackers like SORT do.
>
> **But I would not write that in a 45-minute interview**, and I'd say so. Greedy-with-exclusion handles the common case, it's obviously correct to a reader, and Hungarian is O(n³) plus a chunk of code that's easy to get subtly wrong under time pressure. I'd take the two-line fix, leave a comment noting the greedy limitation, and mention Hungarian as the upgrade path if matching quality became a problem. Knowing when *not* to reach for the fancy algorithm is part of the answer."

**That last paragraph is the whole point of the task.** It shows you know the real solution *and* have the judgment not to over-engineer.

---

## T3 — the DEGRADED state

```python
from collections import deque
from typing import Deque, Dict, List

class HealthMonitor:
    def __init__(
        self,
        offline_after_seconds: float = 10.0,
        min_fps: float = 5.0,           # below this (but still online) → degraded
        fps_window: int = 30,           # how many arrivals to keep per camera
    ):
        self.offline_after_seconds = offline_after_seconds
        self.min_fps = min_fps
        self.fps_window = fps_window
        self._last_frame_at: Dict[str, float] = {}
        self._arrivals: Dict[str, Deque[float]] = {}

    def record_frame(self, camera_id: str, timestamp: float) -> None:
        self._last_frame_at[camera_id] = timestamp
        window = self._arrivals.setdefault(camera_id, deque(maxlen=self.fps_window))
        window.append(timestamp)        # maxlen bounds it automatically — no leak

    def frames_per_second(self, camera_id: str) -> float:
        window = self._arrivals.get(camera_id)
        if window is None or len(window) < 2:
            return 0.0
        span = window[-1] - window[0]
        if span <= 0:
            return 0.0
        return (len(window) - 1) / span

    def state_of(self, camera_id: str, now: float) -> CameraState:
        last = self._last_frame_at.get(camera_id)
        if last is None or now - last > self.offline_after_seconds:
            return CameraState.OFFLINE
        if self.frames_per_second(camera_id) < self.min_fps:
            return CameraState.DEGRADED
        return CameraState.ONLINE
```

### The three things being graded
1. **You need bounded history.** `deque(maxlen=...)` is the clean answer — it drops old entries automatically, so a box running for months doesn't leak. **Say "maxlen bounds it, so no leak" out loud** — the unbounded-list trap is exactly what they're watching for on an edge device.
2. **You asked about the threshold.** `min_fps` and the window are constructor parameters, not magic numbers buried in a comparison. In the interview you'd ask "what fps counts as degraded, over what window?" — here you make the assumption explicit and configurable.
3. **You didn't break the existing tests.** The four original health tests never trigger the degraded path (they don't feed enough frames to compute fps), so they still pass. Confirm that by running them.

### Watch for
`frames_per_second` needs ≥2 samples to compute a rate (you need a span). Returning 0.0 for a single frame means a camera that *just* came online reads as degraded for one frame — arguably fine, but call it out: *"a just-connected camera shows degraded until it has two samples; I could seed it as online for a grace period if that's noisy."*

---

## T4 — flush stranded frames

```python
def flush_if_stale(self, now: float) -> None:
    """Flush a partial batch if it's been sitting too long. The capture loop
    calls this every tick, independent of whether frames are arriving."""
    if not self.buffer or self._oldest_timestamp is None:
        return
    if now - self._oldest_timestamp >= self.max_wait_seconds:
        self.flush()
```

```python
def test_stale_partial_batch_flushes_even_without_new_frames():
    batches = []
    b = FrameBatcher(sink=batches.append, max_batch_size=100,
                     max_wait_seconds=0.5, buffer=[])
    b.add(make_frame(frame_number=0, timestamp=0.0))
    # no more frames arrive — but time passes and the loop ticks
    b.flush_if_stale(now=0.6)
    assert len(batches) == 1
    assert len(batches[0]) == 1
```

### What to say
> "The bug is that `add` is the only thing that can trigger a flush, so if frames stop — camera drops, shift ends — a partial batch is stranded forever. That's the same shape as an alert that fires once and never repeats: works on the happy path, fails silently at the boundary.
>
> The real fix is a **time-driven flush independent of arrivals**. In production that's a background timer; here I model it as `flush_if_stale(now)` that the capture loop calls every tick, with the clock injected as a parameter so it's testable — I'm not going to call `time.time()` inside and make the test wall-clock-dependent.
>
> The deeper issue is that the original `add` conflated two different triggers — 'a frame arrived' and 'enough time passed' — into one code path. Those are genuinely different events and the batcher needs to respond to both. Separating them is the actual fix; `flush_if_stale` is just the seam that lets the time-based trigger exist."

**Recognizing that two distinct events were collapsed into one is the senior observation** — same lesson as repo #1's clock injection, on different code, which is why it's here.

---

## Escalation answers (short form)

1. **O(det × tracks).** Fine to ~hundreds. Beyond that, **spatial hashing**: bucket boxes into a coarse grid, only compare a detection to tracks in the same and adjacent cells. Turns the quadratic into roughly linear for spatially spread objects.
2. **`Track.history` unbounded.** `deque(maxlen=N)`. You rarely need more than the last few dozen positions; keeping every box for a forklift that's been on-site for a week is pure leak.
3. **No "track ended" event.** Aged-out tracks just vanish from the dict. Downstream — analytics, dwell-time, "forklift left the hazard zone" — needs to know. Emit a lifecycle event on creation and on aging-out; `update` should return not just active tracks but transitions.
4. **`_next_id` never resets.** It's a Python int, unbounded, so no overflow — but at extreme scale the concern would be ID reuse across restarts (there is none, since it resets to 1 on restart, which could *collide* with persisted IDs). Say you checked and why it's fine here.
5. **Thread safety.** If the sink runs on another thread, `flush` reassigning `self.buffer` while `add` appends is a race — a frame can land in a list that's already been handed off, or be lost. For a single-threaded capture loop it's a non-issue; if the sink is async, you'd want a lock around the buffer swap or a lock-free hand-off. **Say which deployment you're assuming.**
6. **Per-camera / per-label IoU threshold.** Pass a `threshold_for(label) -> float` callable, or a dict, into the tracker. Keeps the matching loop clean while letting a doorway camera and a dock camera differ. Don't hardcode a branch per camera.
7. **Testing against drift.** Property-style: generate a smooth 100-frame trajectory (box translating a few px per frame), feed it through, and assert `track_id` is constant and `hit_count == 100`. That tests the thing you actually care about — identity persistence — rather than a single hand-picked pair.
