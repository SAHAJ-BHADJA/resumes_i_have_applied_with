# 06 — LLD Insurance
### The hedge. **SUNDAY, 4:25–5:10.** Read it, don't grind it.

---

## Why this file exists

I crawled every Voxel interview report I could reach. **The Systems Discussion round is high-level design at ~85% confidence.** `03_ROUND3_SYSTEM_DESIGN.md` is aimed correctly and remains your primary prep.

But there's one outlier worth 45 minutes:

| Date | Source | Phrasing | Shape |
|---|---|---|---|
| Jan 2026 | Glassdoor, **"Systems Discussion"** named explicitly | "Simple event notification system design" | HLD |
| — | Glassdoor, Voxel (CA) | **"Architecturally design a workflow-based task management system"** | **HLD, decisive** |
| — | 1Point3Acres, titled "System Design Interview" | "workflow management system / job scheduler" | HLD |
| Mar 2026 | Glassdoor, SWE-Platform | loop = "Coding-**Debugging**-**System Design**-Behavioral" | HLD |
| **Dec 2025** | Glassdoor | **"Design a dense vector library"** | **LLD** ← this one |

**The case that "dense vector library" doesn't apply to you:** that candidate said they did well in the *technical screen*, got positive verbal feedback, and were then ghosted. They describe the onsite rounds as something they were *told about*, not something they sat. So their one logged question is most likely from the **technical screen** — which you've already cleared.

**The case for reading this anyway:** it's real evidence that someone at Voxel asks API/library-design questions. It's a computer vision company, so "dense vector" means embeddings, which is squarely their domain. And the hedge costs 45 minutes because **you've already done most of the work** — see the coverage note at the bottom.

---

## How to tell which round you're in — in the first 30 seconds

The interviewer's verb tells you everything.

| They say | You're in | You do |
|---|---|---|
| "**Design a system for**..." | HLD | `03`. Requirements → numbers → API → schema → **diagram** |
| "**Architecturally** design..." | HLD | `03`. The word is a gift. |
| "How would you **scale**..." | HLD | `03`. |
| "**Design a library / class / API for**..." | **LLD** | This file. Classes → interfaces → the hard part |
| "What are the **classes** here?" | **LLD** | This file. |
| "Let's **write** the interface" | **LLD** | This file. |
| "**Design X**" *(bare)* | **Ask.** | ↓ |

**If it's ambiguous — and "design an event notification system" genuinely is — ask. Don't guess.**

> "Quick clarification on scope: do you want the distributed architecture — services, queues, storage, how it scales — or do you want the object model and API, like the classes and interfaces someone would actually code against? I can go either way, I just want to spend the time where you want it."

**This question costs 10 seconds and is itself a good signal.** It says you know the two are different disciplines. Nobody penalizes it. Guessing wrong costs you 20 minutes.

**If they say "whatever you think" — go HLD.** That's what the evidence points to, it's what the round name implies, and you can always drill into classes during the deep dive.

---

## The LLD framework — 45 minutes

Structurally parallel to the HLD skeleton, so it's cheap to hold both.

| Min | Phase | Deliverable |
|---|---|---|
| **0–5** | **Clarify + scope** | Use case, constraints, what's in/out |
| **5–10** | **Core entities** | The nouns. 3–5 classes, no more. |
| **10–20** | **The interface** | Method signatures. **Write these down.** |
| **20–35** | **The one hard part** | Every LLD question has exactly one. Find it. Spend the time there. |
| **35–43** | **Extensibility + errors** | What changes next? What can fail? |
| **43–45** | **Trade-offs** | What you chose and what you gave up |

### The four rules

1. **Signatures before bodies.** Write the whole interface, get agreement, *then* implement whichever method they care about. Implementing method 1 fully before showing method 2 exists is how you run out of time with a quarter of the design visible.
2. **Find the one hard part.** Every LLD question has exactly one genuinely interesting decision and a lot of CRUD around it. Rate limiter → the clock. LRU → the O(1) eviction. Dense vector → the memory layout. **Name it out loud and spend your time there.** Candidates who distribute effort evenly look like they can't tell what matters.
3. **Don't build a class hierarchy for one implementation.** An ABC with a single subclass is a class pretending to be a function. Voxel's notes say they value clean over clever — and reaching for patterns is the most common way to look clever and read as junior.
4. **Say what you're *not* building.** "I'm not going to make this thread-safe unless you want it — locks in the hot path have a real cost and I'd want to know it's shared first." That's judgment, and judgment is the thing being graded.

---
---

# The One Documented Question — "Design a dense vector library"

### Phase 1 — Clarify (this is where the question is won)

> "A few things before I design. When you say **dense** — I'm reading that as: most elements are non-zero, so we store contiguously rather than as index/value pairs like a sparse vector. Is that the distinction you mean?
>
> What's the use case — is this ML embeddings, or general numerical computing? I'd guess embeddings given what Voxel does, and that changes things: embeddings are fixed-dimension, float32, and the operation that matters is similarity.
>
> Am I building on top of numpy, or is the point that I implement the storage myself?
>
> And do you want just the vector type, or also a collection with search over it? Those are pretty different scopes."

**"Dense" is not decoration. It's the whole question, and it's telling you the answer.** If you don't unpack the word in the first two minutes, you've missed what you're being asked.

### Phase 2 — The one hard part: memory layout

**Say this early. It's the answer.**

> "The most important decision here is storage, and 'dense' dictates it. A Python `list` of 768 floats is 768 *pointers* to individually heap-allocated float objects — roughly 8 KB of pointers plus ~24 bytes per boxed float, so ~25 KB for something that should be 3 KB. And they're scattered across the heap, so every dot product is a pointer chase and you get zero cache locality.
>
> A dense vector wants **one contiguous block of float32**. `array.array('f')` in the standard library, or a numpy `ndarray`, or a `memoryview` over a buffer. 768 × 4 bytes = 3 KB, one cache-friendly run.
>
> That's an 8× memory difference and probably a 20×+ speed difference on dot products. For a million embeddings that's 3 GB versus 25 GB — the difference between fitting in RAM and not. **Everything else in this design is bookkeeping around that one choice.**"

**That paragraph is the interview.** Deliver it and the rest is downhill.

### Phase 3 — The interface

```python
from __future__ import annotations
import array, math
from typing import Iterable, Iterator


class DimensionMismatch(ValueError):
    """Raised when two vectors of different dimension are combined."""


class Vector:
    """A dense, fixed-dimension float32 vector.

    Backed by a single contiguous buffer. Immutable by default; use the
    in-place ops when you're in a hot loop and can prove you own the buffer.
    """

    __slots__ = ("_data",)          # no per-instance __dict__ — 
                                    # saves ~56 bytes × millions of vectors

    def __init__(self, values: Iterable[float]) -> None:
        self._data = array.array("f", values)

    # ---- construction
    @classmethod
    def zeros(cls, dim: int) -> Vector: ...
    @classmethod
    def from_buffer(cls, buf: memoryview) -> Vector: ...   # zero-copy

    # ---- sequence protocol — makes it feel native
    def __len__(self) -> int: ...
    def __getitem__(self, i: int) -> float: ...
    def __iter__(self) -> Iterator[float]: ...
    def __eq__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

    # ---- arithmetic — returns new vectors
    def __add__(self, other: Vector) -> Vector: ...
    def __sub__(self, other: Vector) -> Vector: ...
    def __mul__(self, scalar: float) -> Vector: ...        # v * 2.0
    def __rmul__(self, scalar: float) -> Vector: ...       # 2.0 * v  ← don't forget

    # ---- in-place — for hot loops, avoids allocation
    def __iadd__(self, other: Vector) -> Vector: ...

    # ---- the operations that actually matter
    def dot(self, other: Vector) -> float: ...
    def norm(self) -> float: ...
    def normalized(self) -> Vector: ...
    def cosine_similarity(self, other: Vector) -> float: ...
    def euclidean_distance(self, other: Vector) -> float: ...

    # ---- internal
    def _check_dim(self, other: Vector) -> None:
        if len(self._data) != len(other._data):
            raise DimensionMismatch(f"{len(self._data)} vs {len(other._data)}")
```

**Then implement two or three, not all of them:**

```python
    def dot(self, other: Vector) -> float:
        self._check_dim(other)
        return sum(a * b for a, b in zip(self._data, other._data))

    def norm(self) -> float:
        return math.sqrt(self.dot(self))          # reuse — don't rewrite the loop

    def normalized(self) -> Vector:
        n = self.norm()
        if n == 0.0:
            raise ValueError("cannot normalize a zero vector")   # ← the edge case
        return Vector(x / n for x in self._data)

    def cosine_similarity(self, other: Vector) -> float:
        self._check_dim(other)
        denom = self.norm() * other.norm()
        if denom == 0.0:
            raise ValueError("cosine similarity undefined for a zero vector")
        return self.dot(other) / denom
```

### Phase 4 — The five things that separate you from everyone else

**1. Pre-normalize and cosine collapses into dot.**
> "If the workload is similarity search — which it is, for embeddings — normalize once at insert. Then `cosine(a, b)` is just `dot(a, b)`, because the denominator is 1. That kills two `sqrt`s and two full passes per comparison. Over a million-vector scan that's the difference between usable and not. I'd have the store hold a `normalized: bool` flag, or better, a distinct `UnitVector` type so the invariant is in the type system and you can't forget."

**2. `__slots__` isn't a micro-optimization here.**
> "`__slots__` drops the per-instance `__dict__`. That's ~56 bytes an object, which is noise for one vector and 56 MB for a million. At embedding scale, per-object overhead is a real line item."

**3. Batch beats loop — and it's an API question, not an implementation one.**
> "One dot product at a time is the wrong API for the actual workload. Searching a million embeddings should be one matrix-vector multiply, not a million Python-level calls — that's a BLAS call versus a million interpreter round trips, easily 100×. So I'd add a `VectorStore` holding an `(n, d)` contiguous matrix with a `search(query, k)` that does the whole thing in one shot. **The `Vector` class is for ergonomics; the store is where the performance lives.** Designing only the singular type is the trap in this question."

**4. float32, and say why.**
> "float32, not float64. Embeddings don't need the precision — models are trained in fp32 or fp16 and the extra mantissa bits are noise. It halves memory and doubles effective cache and SIMD width. For pure storage you can go float16 or int8-quantized and eat a small recall hit for 4× the memory."

**5. Then extend it — and know where brute force stops.**
> "Brute-force search is O(n·d). At a million 768-dim vectors that's ~768M float ops per query — tens of milliseconds with BLAS, which is fine. At a hundred million it isn't, and you'd move to approximate nearest neighbor: HNSW for recall, IVF-PQ for memory. **But I'd stay brute force until a number forces the move** — exact search you can reason about beats approximate search you can't debug, and ANN indexes bring build time, memory overhead, and a recall parameter nobody knows how to tune."

### The Voxel tie-in — land this at the end

> "For what it's worth, I'd guess this is embeddings for re-identification — tracking the same person or forklift across cameras, or 'find me detections that look like this one.' If so, the thing I'd want to nail down early is the update pattern: embeddings for a live site are append-heavy and rarely deleted, which is exactly the workload where a flat contiguous store beats a fancy index for longer than you'd expect."

---
---

# Three more LLD questions worth 10 minutes each

Voxel's domain narrows the space a lot. If it's LLD, it's near-certainly one of these shapes.

### 1. "Design a bounding box / geometry library" ← **most likely after dense vector**
Same shape as the vector question, dead center of their domain.

**The one hard part: IoU and the coordinate convention.**
> "First question: `(x1, y1, x2, y2)` or `(x, y, w, h)`? Pick one internally, convert at the edges. **Mixing them is the bug that ships** — it's the single most common bug in computer vision code and it's silent, because both are four floats.
>
> Core ops: `area`, `intersection`, `union`, `iou`, `contains`, `clip_to_image`.
>
> The subtlety in IoU is the empty intersection: `max(0, min(x2s) - max(x1s))` — without the `max(0, ...)` you get a *negative* width times a negative height, which is a positive area, and non-overlapping boxes report a healthy IoU. Fails silently, ruins your NMS, and nobody notices for a month.
>
> Then the extension is **NMS** — sort by confidence, greedily keep, suppress anything above an IoU threshold. That's O(n²) naive, fine for hundreds of boxes per frame, and it's a real algorithm they'd recognize."

### 2. "Design a ring buffer for video frames" ← **very edge-device**
> "Fixed capacity, overwrite oldest. Preallocate the whole array once — a frame buffer that allocates per frame will GC-thrash and drop frames.
>
> The one hard part: **full vs empty are the same state** when `head == tail`. You either keep a `size` counter, or waste one slot, or use a generation counter. Say which and why — I'd take the counter, it's one int and it's obvious to the reader.
>
> This is literally Voxel's edge appliance: hold the last N seconds so that when a detection fires you can upload the clip *around* it, including the part that already happened. **The buffer is the reason you can ship evidence of an event you didn't know was coming.**"

### 3. "Design a rate limiter / cache / event dispatcher"
**You already have all three.** Token bucket → `01`, §8.4. LRU → `01`, §8.1. Event dispatcher → the entire `practice/voxel_alerts/` repo. Nothing new to learn.

---

## What you already have — the coverage note

**The hedge is cheap because you've mostly done it.** Your existing prep already covers LLD:

| LLD skill | Where you already have it |
|---|---|
| Class design in Python | `practice/voxel_alerts/` — 6 modules of it |
| Interface / ABC design | `alerting/channels.py` |
| Registry over if/elif | Practice **T7** |
| Dependency injection | Practice **T8** |
| Extensibility | Practice **T4, T5, T6** |
| Rate limiter | `01` §8.4 — token bucket, monotonic clock |
| LRU cache | `01` §8.1 |
| Pub/sub dispatcher | `alerting/dispatcher.py` + **T3** |
| Bounded structures | `01` §8.2, §8.3 |

**So the honest Sunday adjustment is 45 minutes, not a rewrite:** read this file, say the dense-vector memory-layout paragraph out loud twice, and skim the bounding-box IoU trap. That's it. Then go back to `03` — because that's still where 85% of the probability mass sits.

---

## The 30-second version

> **Systems Discussion is HLD. Design `03`.**
>
> If the verb is "library," "class," "interface," or "API" → switch to this file.
> If it's bare "design X" → **ask which they want.** Costs 10 seconds, saves 20 minutes.
> If they shrug → HLD.
>
> LLD: signatures before bodies. Find the one hard part. Don't build a hierarchy for one implementation.
> Dense vector's hard part is **contiguous float32, not a list of boxed floats.** Everything else is bookkeeping.
