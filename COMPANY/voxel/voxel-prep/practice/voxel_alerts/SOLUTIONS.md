# Solutions — read only after you've attempted each task

---

## Exercise A — what a good 5-minute walkthrough sounds like

> "The entry point is `AlertPipeline.process` in `pipeline.py` — the docstring at the top of the module actually lays out the whole flow, which is a nice touch. One `Detection` comes in, and it returns the list of user_ids that got notified.
>
> The core domain objects are in `models.py`. `Detection` is what perception emits — frozen, so it's immutable, which makes sense for an event. `Subscription` is a routing rule: who wants what, at what severity floor, on which channel. `Severity` is an int enum, which matters because the matching logic compares `.value`, so the ordering is load-bearing.
>
> Tracing one detection: it hits `process`, first stop is `Deduplicator.is_duplicate`, which keys on site+camera+event_type — so 'the same hazard' means the same detector firing on the same camera. If it's a dupe we bail immediately and nobody gets told. Otherwise we render a subject and body, then loop over every subscription, filter with `_matches` on site / type / severity, then rate-limit per user, then dispatch to the channel, then append to the audit log.
>
> The design decision I'd call out: the pipeline takes its collaborators through the constructor — dedup, rate limiter, channels are all injected. That's good, it means all of this is testable without mocking, and the `conftest.py` confirms it. `EventDispatcher` seems to be a separate seam that isn't wired into the pipeline yet — I'd want to ask what the intended relationship is.
>
> One thing I'd change: `_render_body` is an if/elif chain on `event_type`. There's presumably one branch per detector type, and I'd guess perception ships new detectors regularly, so that's going to grow. I'd move it to a registry. Though at four branches it's honestly not urgent yet."

**Why this is good:** structure before detail. Names the abstraction, not just the file list. Traces a real object. Notices `Severity.value` is load-bearing. Notices `EventDispatcher` is unwired and **asks instead of assuming**. Ends with a criticism that's immediately qualified — that's the "curious, humble" signal from their JD.

---

## T1 — Deduplicator

### The bug
`is_duplicate` writes `self._last_alerted[key] = detection.timestamp` **unconditionally**, before deciding. So the stored timestamp isn't "when we last alerted" despite the variable being named that — it's "when we last *saw* a detection."

Every duplicate slides the window forward. As long as detections keep arriving faster than the window, the hazard **never re-alerts**. A spill that generates traffic every 30 seconds with a 60-second window produces exactly one alert, forever.

**Why it's nasty:** it gets *worse* the more severe the hazard is. A hazard nobody's fixing generates the most detections and therefore the most suppression. The name of the field (`_last_alerted`) tells you the intent; the code doesn't match it.

### The fix
```python
def is_duplicate(self, detection: Detection) -> bool:
    """True if we already alerted on this hazard recently."""
    key = self._key(detection)
    last: Optional[float] = self._last_alerted.get(key)

    if last is not None and detection.timestamp - last < self.window_seconds:
        return True

    self._last_alerted[key] = detection.timestamp
    return False
```
Only record the timestamp when we're actually going to alert.

### What to say
> "The field is called `_last_alerted` but it's being written on every call, so it's really tracking `_last_seen`. That means each suppressed duplicate pushes the deadline out, and a continuous stream of detections holds the window open indefinitely. The fix is to only stamp it when we actually let one through — then the window is anchored to the last *alert*, which is what the name says and what the test expects."

**Bonus point:** *"Worth noting this is a side-effecting predicate — `is_duplicate` both answers a question and mutates state. That's why the bug was easy to write. If it were `should_alert()` returning a decision, or if the recording were a separate explicit call, this would've been harder to get wrong. I wouldn't necessarily change it now, but it's the root cause of the root cause."* **That observation is a hire-level comment.**

---

## T2 — Rate limiter

### The bug
```python
if len(window) <= self.max_events:   # ← should be <
```
The length check happens **before** the append. When the window already holds exactly `max_events`, `len(window) <= max_events` is still true, so one more gets through. The effective cap is `max_events + 1`.

All three failing tests share this single root cause. `test_window_slides_forward` uses `max_events=1`, so the off-by-one is why the second event at t=1030 wrongly passes.

### The fix
```python
if len(window) < self.max_events:
    window.append(now)
    return True
return False
```

### What to say
> "One bug, three red tests. The check runs before the append, so a full window still has room by the comparison's logic — the cap is effectively `max_events + 1`. Changing `<=` to `<` fixes all three. Let me verify: with `max_events=3`, after three appends `len` is 3, `3 < 3` is false, rejected. Correct."

### The follow-up they'll ask
*"What about the eviction boundary — `window[0] <= now - window_seconds`?"*

> "That's a policy question, not a bug: it makes the window half-open. An event at exactly `now - 60` is evicted, so the window is `(now-60, now]`. That's a defensible choice and it's consistent, but it should be documented — someone will eventually write a test that assumes the other convention."

### The escalation
*"This is a sliding window log. What are the alternatives?"*
| Approach | Memory | Accuracy | Notes |
|---|---|---|---|
| Sliding window log (this) | O(max_events) per key | Exact | What we have |
| Fixed window counter | O(1) per key | Allows 2× burst at boundaries | Cheapest |
| Sliding window counter | O(1) per key | Approximate, weights prev window | Good middle ground |
| Token bucket | O(1) per key | Exact, allows controlled burst | **Best for alerts** — a real incident *should* burst |

> "For safety alerting I'd actually argue token bucket: when a genuine incident kicks off, you want the first few notifications to go out immediately rather than being smoothed. Bursting is a feature here, not a bug."

---

## T3 — Dispatcher isolation

### The bug
No isolation. The loop calls each handler directly, so the first exception propagates out of `dispatch` and every subsequent handler is skipped.

### The fix
```python
import logging
from collections import defaultdict
# ...
logger = logging.getLogger(__name__)


def dispatch(self, detection: Detection) -> List[Any]:
    """Run every handler registered for this detection's type.

    Handlers are isolated: one raising does not prevent the others from running.
    """
    results: List[Any] = []
    for handler in self._handlers[detection.event_type]:
        try:
            results.append(handler(detection))
        except Exception:
            logger.exception(
                "handler %r failed for detection %s", handler, detection.detection_id
            )
    return results
```

### The answers to their follow-ups

**"Swallow or re-raise?"**
> "Swallow, but never silently — hence `logger.exception`, which captures the traceback. This is a fan-out; the whole point is that subscribers are independent. If one raised out of `dispatch`, an unrelated handler's bug becomes an outage for everyone. That said, swallowing means a systematically broken handler is invisible unless someone reads logs — so in production I'd also increment a per-handler error counter and alert on the rate. The failure should be loud in metrics and quiet in the call path."

**"How does the caller learn?"**
> "Right now it can't distinguish 'handler returned nothing' from 'handler exploded' — both just shrink the results list. I'd return a richer result: a list of `(handler, ok, value_or_error)`, or a `DispatchResult` with `successes` and `failures`. Depends whether any caller actually needs it. I'd ask."

**"Bare `except Exception`?"**
> "`except Exception` is right here — it deliberately doesn't catch `BaseException`, so `KeyboardInterrupt` and `SystemExit` still propagate and Ctrl-C still works. If I'd written `except BaseException` or a bare `except:` I'd have made the process unkillable during dispatch. That distinction is the whole reason the exception hierarchy is shaped the way it is."

**"Retries?"**
> "Not here. `dispatch` is synchronous and in the hot path — retrying inline means a slow handler blocks every other handler and backs up the detection stream. Retries belong at the channel/queue layer where you can do exponential backoff off the critical path, with a dead-letter queue for what never succeeds. Putting them here would be solving the right problem in the wrong place."

**That last answer is the one that wins the round** — knowing *where* logic belongs is the thing that separates people who've operated systems from people who've only written them.

---

## T4 — WebhookChannel

```python
class WebhookChannel(Channel):
    """Posts alerts to a customer-supplied HTTP endpoint.

    The address is the target URL. This fake records calls instead of making
    them, matching the pattern used by the other channels.
    """

    def __init__(self, timeout_seconds: float = 5.0) -> None:
        self.timeout_seconds = timeout_seconds
        self.sent: List[Tuple[str, dict]] = []

    def send(self, address: str, subject: str, body: str) -> bool:
        payload = {"subject": subject, "body": body}
        self.sent.append((address, payload))
        return True
```

```python
def test_webhook_posts_a_payload():
    webhook = WebhookChannel()
    assert webhook.send("https://hooks.example.com/x", "subj", "body") is True
    url, payload = webhook.sent[0]
    assert url == "https://hooks.example.com/x"
    assert payload["subject"] == "subj"
```

### The discussion
- **`bool` isn't enough.** A webhook can fail as 4xx (never retry — their config is wrong) or 5xx/timeout (retry — they're having a bad minute). Collapsing those into `False` throws away the only information that determines what to do next. Return a result object with a status, or raise typed exceptions.
- **Slow endpoints block everyone.** `process` loops subscriptions synchronously. A customer with a 30-second endpoint stalls every subscriber behind them. Real fix: `send` enqueues, workers deliver. The pipeline should never do network I/O inline.
- **Retries + DLQ** live at the queue/worker layer, not in `Channel`.
- **Say this:** *"Adding this class is five minutes. The interesting part is that adding it exposes that the pipeline does synchronous I/O in a loop, which was already a problem for email and SMS — I just noticed it now because webhooks make it obvious."* **Noticing that the new feature reveals an existing flaw is exactly the kind of thing that gets you hired.**

---

## T5 — Critical bypasses rate limiting

### The minimal change
```python
if (
    detection.severity is not Severity.CRITICAL
    and not self.rate_limiter.allow(subscription.user_id, detection.timestamp)
):
    continue
```

**Note the short-circuit:** critical alerts don't even consume a token. If you'd written it the other way — always call `allow()`, then ignore the result for critical — critical traffic would silently eat the budget of the non-critical alerts that follow. **Say that out loud.** It's a two-line difference with completely different behavior, and spotting it unprompted is a strong signal.

### The design discussion
- **Hardcoded vs configurable:** hardcoding is right *today* — it's one rule, and a policy object for one rule is speculative generality. But it's genuinely a business rule, so if a second one appears ("VIP subscribers bypass too") I'd extract it immediately. **The honest answer is "hardcode it now, and here's the specific trigger that would make me extract it."**
- **Attack surface:** yes. If the model starts false-positiving CRITICAL, the bypass turns into an unbounded notification firehose *with the rate limiter explicitly disabled*. Mitigation: a separate, much higher cap for critical rather than no cap — a safety valve, not a bypass. Raise this yourself; it shows you think about what happens when your own assumptions break.
- **Should critical bypass dedup?** **No, and this is the interesting one.** Dedup and rate limiting solve different problems. Rate limiting protects the human from volume. Dedup answers "is this the same ongoing thing?" A blocked exit firing 30×/sec is still *one* blocked exit — bypassing dedup means 30 notifications per second about a single hazard, which is strictly worse for the person trying to respond to it. Instead, shorten the dedup *window* for critical (10s instead of 60s) so it re-alerts more aggressively without flooding. **Distinguishing these two mechanisms is the whole point of the question.**

---

## T6 — Quiet hours

```python
# models.py — note: must have a default, or it breaks every existing construction
@dataclass(frozen=True)
class Subscription:
    user_id: str
    site_id: str
    event_types: Set[str]
    min_severity: Severity
    channel: str
    address: str
    quiet_hours: Optional[Tuple[int, int]] = None  # (start_hour, end_hour), site-local
```

```python
# pipeline.py
@staticmethod
def _in_quiet_hours(quiet_hours: Optional[Tuple[int, int]], hour: int) -> bool:
    if quiet_hours is None:
        return False
    start, end = quiet_hours
    if start <= end:
        return start <= hour < end        # e.g. (1, 5) — same day
    return hour >= start or hour < end    # e.g. (22, 6) — wraps midnight
```

### The three things being tested
1. **The midnight wrap.** `(22, 6)` with the naive `start <= hour < end` is *always false* — quiet hours would silently never fire and no test would catch it unless someone wrote one. **This is the bug you write if you rush.**
2. **The timezone question you're supposed to ask.** "Site-local or subscriber-local?" A regional manager covering Ohio and Nevada has one set of quiet hours and two site timezones. There is no correct answer without asking. **A candidate who codes this silently has failed the task even if the code is perfect** — the whole point is surfacing the ambiguity. Say: *"Before I write this — whose midnight? The site's, or the person's? Because those diverge and the answer changes the data model: if it's site-local I need a timezone on the site, which we don't seem to have yet."*
3. **The default.** A dataclass field without a default after fields with defaults is a `TypeError` at class-definition time. And every existing `Subscription(...)` in `conftest.py` must keep working — `Optional[...] = None` is the compatible choice. **Run the tests immediately after touching `models.py`**, not at the end.

### Wire it in
```python
if detection.severity is not Severity.CRITICAL and self._in_quiet_hours(
    subscription.quiet_hours, self._site_local_hour(detection)
):
    continue
```

---

## T7 — Refactor `_render_body`

```python
def _render_ppe_violation(detection: Detection) -> str:
    missing = detection.metadata.get("missing_ppe", "required PPE")
    return f"Worker detected without {missing}."


def _render_spill(detection: Detection) -> str:
    area = detection.metadata.get("area", "the floor")
    return f"Possible spill detected on {area}. Cordon and clean."


def _render_forklift_speeding(detection: Detection) -> str:
    speed = detection.metadata.get("speed_mph", "?")
    return f"Forklift travelling at {speed} mph, above the site limit."


def _render_blocked_exit(detection: Detection) -> str:
    exit_id = detection.metadata.get("exit_id", "an exit")
    return f"Emergency exit {exit_id} appears obstructed."


BODY_RENDERERS: Dict[str, Callable[[Detection], str]] = {
    "ppe_violation": _render_ppe_violation,
    "spill": _render_spill,
    "forklift_speeding": _render_forklift_speeding,
    "blocked_exit": _render_blocked_exit,
}


# in AlertPipeline:
def _render_body(self, detection: Detection) -> str:
    renderer = BODY_RENDERERS.get(detection.event_type)
    if renderer is None:
        return f"Detection of type '{detection.event_type}' recorded."
    return renderer(detection)
```

**Why a plain dict and not a class hierarchy or a decorator-registry:** each renderer is a pure function of one argument. A `Renderer` ABC with one method per subclass is a class pretending to be a function. A decorator-based auto-registry adds import-order magic for zero benefit at this size. **The dict is the answer.** If you reach for something fancier, you're optimizing for looking clever rather than for the next person reading it — and Voxel's notes explicitly say they value clean over clever.

**Do run the tests after this.** `test_unknown_event_type_renders_a_fallback_body` exists precisely to catch you dropping the fallback.

### "Was it worth it?"
> "Honestly? At four branches, marginal. The if/elif was readable and nobody was confused by it. What makes it worth doing is the *rate of change* — if perception ships a new detector every sprint, this file becomes a merge-conflict magnet and every renderer change forces a rebuild of the pipeline class. The dict decouples that. But if detector types are stable, I'd have left it alone and said so. My rule of thumb is roughly: refactor when the branches start changing independently and different people own them, not when you hit a branch count."

**Being willing to say "this refactor might not be worth it" is a senior signal.** Most candidates cheerlead for whatever abstraction they just built.

---

## T8 — Inject the clock

```python
from typing import Callable

class AlertPipeline:
    def __init__(
        self,
        subscriptions: List[Subscription],
        channels: Dict[str, Channel],
        deduplicator: Deduplicator,
        rate_limiter: SlidingWindowRateLimiter,
        clock: Callable[[], float] = time.time,
    ):
        ...
        self.clock = clock
```
```python
sent_at=self.clock(),
```
```python
def test_delivery_log_uses_the_injected_clock(subscriptions, email, sms):
    pipeline = AlertPipeline(
        subscriptions=subscriptions,
        channels={"email": email, "sms": sms},
        deduplicator=Deduplicator(60.0),
        rate_limiter=SlidingWindowRateLimiter(100, 3600.0),
        clock=lambda: 12345.0,
    )
    pipeline.process(make_detection(event_type="spill", severity=Severity.WARNING))
    assert pipeline.delivery_log[0].sent_at == 12345.0
```

### The discussion
- **Constructor injection with a `time.time` default** — every existing caller keeps working, tests get a seam, no mocking library required. `unittest.mock.patch("alerting.pipeline.time.time")` also works but couples the test to the module's import structure, so a refactor breaks tests that should be indifferent to it. **Injection is a design choice; patching is a workaround.**
- **"Should `sent_at` just use `detection.timestamp`?"** — **the actually-interesting question.** They're the same only if processing is instantaneous. They diverge when the queue backs up: `detection.timestamp` is when the hazard happened, `sent_at` is when the human was told. **The gap between them is your notification latency SLO, and it's the single most valuable number in the system** — "we detected the spill at 14:02 and told someone at 14:47" is exactly the incident-review question a customer asks. So: keep both. They're different facts. Answering "just reuse the timestamp, it's simpler" misses that you'd be deleting your own observability.
- **`time.time()` vs `time.monotonic()`** — audit log wants `time.time()`: it's a wall-clock fact that must correlate with other systems' logs. The rate limiter wants `monotonic()`: it measures *elapsed* time and must not go backwards when NTP corrects the clock. **Same word, opposite requirements.** (The current rate limiter takes `now` as a parameter, which sidesteps this — but note the pipeline hands it `detection.timestamp`, which is wall-clock and *can* go backwards. Worth flagging.)

---

## Escalation answers (short form)

1. **Unbounded dedup map.** (a) TTL sweep — evict entries older than the window on every Nth call, O(1) amortized. (b) Bounded LRU — cap it; worst case is a rare duplicate alert, which is a *safe* failure. (c) Redis with native TTL — moves state out of the process, which you need anyway once you run more than one instance. **The last point is the real one: this whole class only works single-process, and nobody runs one alerting box.**
2. **Same for the rate limiter.** Same three answers. Redis with a sorted set per key and `ZREMRANGEBYSCORE` is the standard production shape.
3. **O(subscriptions) per detection.** Build `Dict[site_id, List[Subscription]]` once, then `Dict[(site_id, event_type), ...]`. Cuts 50k comparisons to ~5. Rebuild the index on subscription change; it's read-heavy, so pay on write.
4. **Thread safety.** `deque.append`/`popleft` are individually atomic under the GIL, but `if len(window) < max: window.append(now)` is check-then-act — two threads both see room and both append, so you exceed the cap. Same for dedup's get-then-set. **Does it matter?** For a rate limiter, slightly over-delivering under a race is usually acceptable; for dedup, a rare duplicate alert is also acceptable. **The honest answer is "these are benign races for this domain — but I'd want that written down, because the next person will assume it's a bug and add a lock to the hot path."**
5. **`KeyError` on unknown channel.** Yes — and it kills the loop mid-way, so subscribers *after* the bad one silently don't get told, while the ones before did. Partial delivery with no record of it. Validate subscriptions at load time, and wrap the per-subscription body so one bad row can't poison the batch. Same class as T3.
6. **Exactly-once.** You can't get it here. Crash after `send` but before `append` → delivered, unlogged. Crash the other way → logged, undelivered. The real answer: make it **at-least-once with an idempotency key** (`detection_id + user_id`), have the channel dedupe on it, and accept that "exactly once" is a property of the *observed effect*, not of the delivery. Then persist the log before sending (write-ahead) so you never lose the record of intent.
7. **Frozen dataclass with a mutable dict.** `frozen=True` only blocks attribute rebinding — `detection.metadata["x"] = 1` still works, and `hash()` on a frozen dataclass containing a dict raises anyway. Not biting us today because nothing mutates it. It would bite the moment a handler decided to annotate the detection and every other handler saw the change. If it mattered I'd use `MappingProxyType`.
