# Mock Round 2 — `voxel_alerts`

A small Python service that turns camera detections into notifications. It is deliberately shaped like Voxel's real product: perception fires detections → dedup → match subscribers → rate limit → render → send.

**~280 lines across 6 modules.** That is roughly what you'll be handed on the 21st.

Three real bugs are planted. Two refactors are waiting. Nothing here is a trick — every bug is one that ships to production in real companies.

---

## Setup

```bash
cd practice/voxel_alerts
pip install -r requirements.txt
python -m pytest -q
```

You should see **5 failed, 20 passed**. That's correct. Those five failures are your work.

---

## How to use this (read before you start)

This is not a puzzle. It's a **rehearsal**. The point is not to fix the bugs — you could do that in twenty minutes. The point is to fix them **while narrating**, the way you will on the 21st.

**Rules for every task:**
1. **Record yourself.** Screen + audio. You'll watch it back.
2. **Talk the entire time.** If you go quiet for 20 seconds, you've failed the rep.
3. **Set a timer.** Real rounds are 45 minutes.
4. **Don't read `SOLUTIONS.md` until you're done.** It's there to check yourself, not to learn from.
5. **Match the existing style.** Type hints, docstrings, naming. They are grading whether you respect the codebase's conventions. Do not introduce your own.

---

## Exercise A — Comprehension drill (do this first, 5-minute timer)

Before you touch a single bug: **read the codebase and explain it out loud in 5 minutes, recorded, without scrolling back.**

Hit these five things:
1. Where's the entry point? What's the one function a caller actually invokes?
2. What are the core abstractions and how do they relate?
3. Trace one detection all the way through. What happens to it?
4. What's the most important design decision someone made here?
5. Name one thing you'd change and why.

**Then check yourself against §Exercise A in `SOLUTIONS.md`.** Repeat until it's clean. This drill *is* the first five minutes of your Round 2 and it's the part that sets the interviewer's opinion of you.

---

## The Tasks

### 🔴 T1 — `test_ongoing_hazard_realerts_every_window` is failing

```
FAILED tests/test_dedup.py::test_ongoing_hazard_realerts_every_window
```

A spill sits on the floor for five minutes. The perception service fires a detection every 30 seconds. With a 60-second dedup window, the safety manager should get a reminder at t=0, 60, 120, 180, 240 — five alerts.

They get one. Then silence, for as long as the spill exists.

**Find it. Fix it. Explain why it happens.**

> **Difficulty: medium.** The code looks right on a casual read. This is the kind of bug where you need to trace actual values rather than read for correctness. Say the numbers out loud as you trace them.

---

### 🔴 T2 — Three rate limiter tests are failing

```
FAILED tests/test_rate_limiter.py::test_window_slides_forward
FAILED tests/test_rate_limiter.py::test_allows_exactly_max_events_then_rejects
FAILED tests/test_rate_limiter.py::test_cap_of_one_allows_exactly_one
```

**Before you look:** three red tests does not mean three bugs. Ask yourself whether one root cause explains all three. Say that hypothesis out loud *before* you start reading — hypothesis-first debugging is exactly what the interviewer wants to see, and "let me check whether these share a cause" is a sentence that scores.

> **Difficulty: easy.** But the *diagnosis narration* is what's being graded, not the fix.

---

### 🔴 T3 — `test_one_broken_handler_does_not_stop_the_others` is failing

```
FAILED tests/test_dispatcher.py::test_one_broken_handler_does_not_stop_the_others
```

The email provider times out. Its handler raises. Now the SMS handler never runs — so a CRITICAL blocked-exit alert reaches nobody, because an unrelated service had a bad afternoon.

Fix the isolation.

**Then answer out loud, because they will ask:**
- Should `dispatch` swallow the exception, or re-raise after running the others?
- How does the caller learn a handler failed?
- Is a bare `except Exception` acceptable here? What about `except BaseException`? (Think about `KeyboardInterrupt`.)
- Should a failed handler be retried? Where would that logic live?

> **Difficulty: easy to fix, hard to fix *well*.** The fix is four lines. The conversation around it is the whole round.

---

### 🟡 T4 — Add a `WebhookChannel`

Customers want alerts posted to their own systems (Slack, ServiceNow, their EHS platform).

Add a `WebhookChannel` to `channels.py` that fits the existing `Channel` interface. Don't make real HTTP calls — follow the fake-and-record pattern the other channels use so it stays testable. **Write a test for it.**

**Questions to answer out loud:**
- Webhooks fail. `send()` returns `bool` — is that enough? What would you want instead?
- What happens if the customer's endpoint is slow? Does that block every other subscriber?
- Where would retries and a dead-letter queue live in this design?

> This is the classic "add a new method/feature to this class" task from your notes.

---

### 🟡 T5 — CRITICAL alerts must bypass the rate limiter

Right now a `CRITICAL` blocked-exit alert can get dropped because the recipient already hit their hourly cap on `INFO` noise. That is a genuinely dangerous bug — someone could be hurt because we were being polite about notification volume.

Make `Severity.CRITICAL` skip rate limiting.

**Do it with a minimal, clean change.** Do not restructure the pipeline. Then argue the design out loud:
- Should this be hardcoded, or a per-subscription setting, or a policy object?
- Isn't "critical bypasses the limit" an attack surface if the model starts false-positiving CRITICAL?
- Should critical bypass **dedup** too? (Think carefully — probably not. Say why.)

> The interviewer's follow-up will be *"where else could this rule have gone?"* Have an answer.

---

### 🟡 T6 — Add quiet hours

Add an optional `quiet_hours` field to `Subscription` — e.g. `(22, 6)` meaning "don't page me between 10pm and 6am." Non-critical alerts during quiet hours are suppressed. Critical alerts always go through.

**The interesting parts, which are the point of the task:**
- The window **wraps midnight**. `(22, 6)` is not `22 <= hour <= 6`. This is the bug you'll write if you rush.
- Whose timezone? The detection's site is in Ohio; the subscriber is in California. Sites have locations. **Ask the interviewer** — this is exactly the requirement you're supposed to surface rather than assume.
- `detection.timestamp` is a unix float. Converting it to an hour requires a timezone. Where does that come from?
- Existing subscriptions have no `quiet_hours`. Does your change break them? (Default value. Dataclass field ordering. Try it.)

> This one is deliberately underspecified. **That's the test.** A candidate who codes it silently fails; a candidate who says "wait, whose midnight?" passes.

---

### 🟢 T7 — Refactor `_render_body` out of the if/elif chain

`AlertPipeline._render_body` is a four-branch `if/elif` on `event_type` and it grows every time perception ships a new detector. Voxel has dozens of detector types.

Refactor it into something extensible — a registry, a dict of renderers, a strategy per event type. Your call.

**Constraints that make this realistic:**
- **Do not break a single test.** Run them after every step.
- The fallback for unknown types must still work.
- Keep it simple. A metaclass-based plugin system is a *worse* answer than a dict, and reaching for one signals you optimize for cleverness over the reader.

**The question they'll ask:** *"was this refactor worth it?"* Have a real answer. Sometimes an if/elif with four branches is fine and the honest answer is "at four branches, no — at fifteen, yes, and here's where the line is for me." **Being willing to say a refactor isn't worth it is a senior signal.** Don't just cheerlead for the abstraction.

---

### 🟢 T8 — Make the delivery log testable

`AlertPipeline.process` calls `time.time()` directly to stamp `DeliveryRecord.sent_at`. So the audit trail can't be asserted on — you can't write a test that says "this was logged at t=1000."

Inject the clock. Then write the test that was impossible before.

**Discussion:**
- Constructor injection, default parameter, or a module-level seam? Trade-offs?
- Everything else in this pipeline uses `detection.timestamp`. Should `sent_at` just use that too? (**When would those two differ, and does the difference matter?** This is the actually-interesting question — think about queue lag.)
- `time.time()` vs `time.monotonic()` — which is right for an audit timestamp, and which is right for the rate limiter? They're not the same answer.

---

## Escalation — if you finish early

These are the questions a strong interviewer asks after you've solved the stated task. Answer them **out loud** even without writing code.

1. **The dedup map grows forever.** Every `(site, camera, event_type)` ever seen stays in memory. At 10k cameras × 30 detector types, what happens? Fix it three different ways and state the trade-offs.
2. **Same for the rate limiter's `defaultdict(deque)`** — every user_id ever seen, permanently.
3. **`AlertPipeline.process` is O(subscriptions) per detection.** 50k subscriptions × 1000 detections/sec = 50M comparisons/sec. Fix it. (Hint: index by `site_id` first.)
4. **None of this is thread-safe.** Where are the races? Does it matter given how it's deployed?
5. **`self.channels[subscription.channel]` raises `KeyError`** on a bad channel name and kills the whole detection's processing — including subscribers who would have succeeded. Same class of bug as T3. Find the others like it.
6. **How would you test that an alert is delivered exactly once** when the process crashes between `channel.send()` and `delivery_log.append()`? (You can't, with this design. What would you change? This is the at-least-once vs exactly-once conversation from your systems round, showing up in code.)
7. **`Detection` is frozen but `metadata: Dict` is mutable.** `@dataclass(frozen=True)` doesn't deep-freeze. Is that a bug here? When would it bite?

---

## Scoring yourself

After each task, watch the recording and check:

| | ✅ / ❌ |
|---|---|
| Did I skim the structure before diving into one file? | |
| Did I say my hypothesis out loud **before** reading for the bug? | |
| Did I confirm the requirement with the "interviewer" before changing code? | |
| Did I make the **minimal** change, or did I rewrite things I wasn't asked to? | |
| Does my code look like it belongs in this codebase (types, docstrings, naming)? | |
| Did I run the tests after changing anything? | |
| Did I go quiet for more than 20 seconds? | |
| Did I ask at least three questions? | |
| When I found the bug, did I explain the *mechanism* or just patch the symptom? | |

**The last one is the big one.** "I changed `<=` to `<`" is a fail. "The check happens before the append, so a full window still admits one more — the cap is effectively `max_events + 1`" is a pass.
