# Round 3 — Systems Discussion
### ~45–50 min · Two confirmed questions · Both are Voxel's product with the labels filed off

---

## ⚠️ First: HLD or LLD? — read this before anything else

**This round is high-level design at ~85% confidence.** This file is aimed correctly. But confirm it in the first 30 seconds:

| They say | Go |
|---|---|
| "Design a system for…" / "**Architecturally** design…" / "How would you scale…" | **This file** |
| "Design a **library** / class / API for…" / "What are the classes here?" | **`06_LLD_INSURANCE.md`** |
| Bare "design X" | **Ask.** ↓ |

> "Quick scope check: do you want the distributed architecture — services, queues, storage, scaling — or the object model and API, the classes someone would code against? I can go either way, I just want to spend the time where you want it."

**Costs 10 seconds, saves 20 minutes, and reads as someone who knows they're different disciplines.** If they shrug, go HLD — that's where the evidence points.

**Why 85% and not 100%:** one Dec 2025 Glassdoor report logs *"Design a dense vector library"* — an LLD-shaped question. But that candidate was ghosted after the **technical screen** and describes the onsite as something they were told about, not sat. So it's most likely a screen question, and you've passed that. `06` is the 45-minute hedge. Everything else — "**architecturally** design a workflow-based task management system," "simple event notification **system design**," the 1P3A thread titled "**System Design** Interview," a Mar 2026 loop listed as "Coding-Debugging-**System Design**-Behavioral" — points here.

---

## What we know

| Source | The question asked |
|---|---|
| Glassdoor, Jan 2026 candidate | **"a simple event notification system design"** |
| 1Point3Acres onsite report | **"a workflow management system / job scheduler"** |

**These are not two questions. They're one question asked twice.** Producers → queue → workers → state → notifications. That's Voxel's pipeline: camera events → processing → notifications → task assignment. Their **Actions** feature is literally a workflow engine bolted to an alerting system.

**Learn one skeleton. Reskin it three ways.** That's this file.

---

## The bar you're being held to

From your notes:
> *"For a new-grad-level candidate they want fundamentals, not exotic scale: clear requirements gathering, sensible API + schema, one clean architecture diagram, and honest trade-off discussion."*

**Read that again.** This is not the FAANG design gauntlet. Nobody wants your CRDT opinions. What loses this round is:
- Jumping to boxes before establishing requirements
- Being unable to justify an arrow
- Bluffing scale you can't defend
- Never mentioning failure

What **wins** it is being the person who says *"I'd start with Postgres, and here's the specific number that would make me revisit that."*

---

## The 50-minute skeleton — run this exact clock

| Minutes | Phase | Deliverable |
|---|---|---|
| **0–5** | **Requirements** | Functional, non-functional, and 3 numbers |
| **5–8** | **API** | 3–5 endpoints. Method, path, payload. |
| **8–13** | **Data model** | Tables, keys, indexes. Say the index out loud. |
| **13–23** | **Architecture** | **One clean diagram.** Boxes and arrows. Explain each. |
| **23–40** | **Deep dive** | Whatever they poke. They will poke. |
| **40–48** | **Trade-offs & failure** | What breaks, what you'd do differently, what you'd monitor |
| **48–50** | **Wrap** | "Here's what I'd build first and what I deliberately deferred." |

**The two mistakes that cost the round:**
1. **Skipping requirements to draw boxes.** You'll design the wrong system beautifully.
2. **Never doing the numbers.** Three multiplications take 90 seconds and change everything downstream.

**To be explicit about what "high level" does and doesn't mean:**

| You DO | You DON'T |
|---|---|
| Draw the architecture | Implement a class |
| **Write the API sketch** (minutes 5–8) | Write working code |
| **Write the schema / DDL** (minutes 8–13) | Handle syntax errors |
| Sketch ~5 lines of pseudocode *if they ask* in the deep dive | Lead with pseudocode |

The API and schema are **specification, not implementation**. Nobody runs them. But skipping them because "this is high level" is the most common way to read as hand-wavy — **the schema is where you prove the design bottoms out in something real.** It's why `UNIQUE (event_id, user_id, channel)` below is worth more than any box on the diagram.

And around minute 30, expect *"okay, how would you actually implement the dedup?"* — sketch 5–10 lines, keep it short, come back up to the architecture. **That's a deep dive, not a switch into LLD.**

---

## The back-of-envelope kit — memorize these

```
1 day          ≈ 86,400 s  ≈ 10⁵ s        (use 10⁵, the error is 15% and nobody cares)
1M/day         ≈ 12/s
100M/day       ≈ 1,200/s
1B/day         ≈ 12,000/s
Peak           ≈ 2–3× average. Say this. Always.

Postgres single node:  ~5k writes/s comfortably, ~10k reads/s cached
Redis:                 ~100k ops/s
Kafka partition:       ~10 MB/s   → partition count = throughput / 10 MB/s
Disk seek: 10ms · SSD read: 100µs · Memory read: 100ns · Cross-region RTT: ~100ms

1 KB row × 1M/day = 1 GB/day = 365 GB/yr → fits on one box, don't shard
1 KB row × 1B/day = 1 TB/day             → now you shard. Say the number that flipped it.
```

**The move:** *"At 1,200 writes/sec a single Postgres handles this fine. I'd shard around 5–10k/sec, so we've got ~5× headroom. I'm not designing for shards today."* That sentence — a number, a threshold, a decision — is worth more than any diagram.

---
---

# DESIGN 1 — Event Notification System ⭐ CONFIRMED ASKED
### *"Design a simple event notification system."*
### At Voxel this is **Risk Insights**: analyze the stream, decide what's worth surfacing, deliver it to the right person on the right channel without flooding them.

---

## Phase 1 — Requirements (0–5 min)

**Ask, don't assume. Out loud:**
> "Before I design anything — who are the producers? Is this internal services publishing events, or user-generated? What channels do we deliver on — email, SMS, push, webhook? Do users configure preferences? And what's the latency expectation — is this 'within a second' or 'within a minute'?"

Then commit to a scope and **say you're committing**:

**Functional**
- Producers publish events
- Users subscribe to event types with preferences
- Fan out to matching subscribers
- Deliver over email / SMS / push / webhook
- Respect user preferences (channel, severity floor, quiet hours)
- Dedup and rate limit so alerts stay useful
- Track delivery status

**Non-functional**
- **At-least-once delivery** with idempotent consumers. *"I'd rather send twice than miss a fire alarm."* ← **say exactly this, the justification is the point**
- Ordering: **per-user, best effort.** Global ordering isn't worth what it costs.
- p99 end-to-end < 5s for critical
- Availability > durability of any single component
- Producer publish is non-blocking

**Numbers — do these out loud**
```
10k sites × 30 cameras × 1 detection/min       ≈ 5,000 detections/sec
After dedup (say 95% are repeats of ongoing)   ≈ 250 alertable events/sec
Fan-out ~5 subscribers each                    ≈ 1,250 notifications/sec
Peak 3×                                        ≈ 3,750/sec
Storage: 1 KB × 100M notifications/day         ≈ 100 GB/day → 90-day retention ≈ 9 TB
```
> "So: thousands per second, not millions. That's comfortably a single Postgres for state plus a queue for buffering. I'm not going to shard today and I'll tell you what would change my mind."

---

## Phase 2 — API (5–8 min)

```
POST /v1/events
  { "event_type": "spill", "site_id": "s-1", "camera_id": "c-3",
    "severity": "warning", "occurred_at": 1721000000, "metadata": {...},
    "idempotency_key": "det-abc123" }
  → 202 Accepted { "event_id": "evt_..." }

POST /v1/subscriptions
  { "user_id": "u-1", "site_id": "s-1", "event_types": ["spill","ppe_violation"],
    "min_severity": "warning", "channels": ["email","sms"],
    "quiet_hours": [22, 6] }
  → 201 Created

GET  /v1/notifications?user_id=u-1&since=...&limit=50   → paginated feed
POST /v1/notifications/{id}/ack                          → mark read
GET  /v1/notifications/{id}/status                       → queued|sent|delivered|failed
```

**Three things to say, unprompted:**
1. **`202 Accepted`, not `201`.** *"Publish returns immediately — the producer doesn't wait for fan-out. If a camera's ingest blocks on the notification path, we've coupled detection to delivery, and a slow email provider now stops us seeing hazards."*
2. **`idempotency_key`.** *"Producers retry. Without this, a network blip becomes a duplicate alert."*
3. **Cursor pagination, not offset.** *"Offset pagination on an append-heavy feed skips rows as new ones land."*

**These three lines take 40 seconds and are the difference between "designed an API" and "has shipped an API."**

---

## Phase 3 — Data model (8–13 min)

```sql
CREATE TABLE events (
    event_id        UUID PRIMARY KEY,
    event_type      TEXT NOT NULL,
    site_id         TEXT NOT NULL,
    camera_id       TEXT,
    severity        SMALLINT NOT NULL,
    occurred_at     TIMESTAMPTZ NOT NULL,
    metadata        JSONB,
    idempotency_key TEXT UNIQUE            -- the dedup guarantee lives here
);
CREATE INDEX ON events (site_id, occurred_at DESC);

CREATE TABLE subscriptions (
    subscription_id UUID PRIMARY KEY,
    user_id         TEXT NOT NULL,
    site_id         TEXT NOT NULL,
    event_types     TEXT[] NOT NULL,
    min_severity    SMALLINT NOT NULL,
    channels        TEXT[] NOT NULL,
    quiet_hours     INT4RANGE,
    enabled         BOOLEAN DEFAULT TRUE
);
CREATE INDEX ON subscriptions (site_id) WHERE enabled;   -- the fan-out lookup

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY,
    event_id        UUID REFERENCES events,
    user_id         TEXT NOT NULL,
    channel         TEXT NOT NULL,
    status          TEXT NOT NULL,          -- queued|sent|delivered|failed|suppressed
    attempts        SMALLINT DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT now(),
    delivered_at    TIMESTAMPTZ,
    UNIQUE (event_id, user_id, channel)     -- ← the exactly-once-ish guarantee
);
CREATE INDEX ON notifications (user_id, created_at DESC);  -- the feed query
```

**Say the indexes out loud and say *why*:**
> "Two indexes matter. `subscriptions(site_id) WHERE enabled` — that's the fan-out lookup, it runs on every single event, so it's the hottest read in the system, and the partial index keeps it small since most subscriptions are probably disabled or stale. And `notifications(user_id, created_at DESC)` because the feed query is 'my notifications, newest first' and without that index it's a full scan per page load."

**And the one that wins the round:**
> "`UNIQUE (event_id, user_id, channel)` is doing real work. It's how at-least-once delivery becomes at-most-once *observed*. Worker crashes and retries? The insert conflicts and we skip the send. That constraint is the idempotency guarantee, enforced by the database rather than by hoping the workers behave."

**The Voxel-specific flex:**
> "Events are time-series — always written with a timestamp, always queried by range, never updated. I'd put them in **TimescaleDB** rather than plain Postgres: hypertables partition by time automatically, so 90-day retention is `DROP CHUNK` instead of a `DELETE` that vacuums for an hour. And continuous aggregates give the Executive Hub its rollups for free."

*(TimescaleDB is in their backend job posting. This lands.)*

---

## Phase 4 — Architecture (13–23 min) — **one clean diagram**

```
  Perception / Producers
  (camera events, ML inference)
            │
            ▼
   ┌─────────────────┐
   │  Ingest API     │  validate · idempotency check · 202 immediately
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  Event Bus      │  Kafka / SQS — buffers bursts, decouples producers
   │  (partitioned   │  partition key = site_id  → per-site ordering
   │   by site_id)   │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐         ┌──────────────┐
   │  Fan-out        │◄────────│ Subscription │  (cached in Redis,
   │  Workers        │         │    Store     │   invalidated on write)
   │                 │         └──────────────┘
   │ • dedup         │◄────────┌──────────────┐
   │ • match subs    │         │    Redis     │  dedup keys w/ TTL
   │ • rate limit    │         │              │  rate limit counters
   │ • render        │         └──────────────┘
   └────────┬────────┘
            │  writes notification rows (status=queued)
            ▼
   ┌─────────────────┐
   │ Delivery Queue  │  per-channel queues → independent scaling & blast radius
   └────────┬────────┘
            │
   ┌────────┼─────────┬──────────┐
   ▼        ▼         ▼          ▼
 Email    SMS      Push      Webhook      ← workers, retry w/ exp. backoff
 (SES)  (Twilio)  (FCM)     (customer)
   │        │         │          │
   └────────┴────┬────┴──────────┘
                 │  failures after N attempts
                 ▼
          ┌──────────────┐
          │ Dead Letter  │  → alerting + manual replay
          │    Queue     │
          └──────────────┘

  Postgres/TimescaleDB ← events, subscriptions, notifications, delivery status
```

**Walk it in this order and justify each box:**

> "Ingest validates and returns 202 immediately — producers never block on delivery.
>
> The bus is the most important box. It decouples produce-rate from consume-rate, so a burst — a shift change where forty people walk in without hard hats — buffers instead of dropping. It gives us replay: if fan-out has a bug, we fix and reprocess. And **I'd partition by `site_id`**, which gets us per-site ordering for free while still letting us parallelize across sites. Ordering within a site is what actually matters — 'spill detected' should precede 'spill cleared' — and global ordering would mean one partition and no parallelism at all.
>
> Fan-out workers do the interesting work: dedup, match, rate limit, render. Stateless, so they scale horizontally; all the state is in Redis and Postgres.
>
> **Separate delivery queues per channel** — that's deliberate. If Twilio has an outage, SMS backs up while email keeps flowing. One shared queue means a slow channel head-of-line-blocks every channel.
>
> The DLQ is where things go after N failed attempts. Critically, **the DLQ having anything in it is itself an alert** — silent notification failure is the worst outcome for a safety product. Somebody didn't hear about a hazard and nobody knew."

---

## Phase 5 — The deep dives they'll pick (23–40 min)

### 🔍 "How do you guarantee delivery?"

> "**At-least-once with idempotent consumers.** Exactly-once doesn't really exist end-to-end — the moment delivery crosses a network to a third party like SES, you can't atomically 'send and record'. You either send-then-record and risk a duplicate on crash, or record-then-send and risk a silent drop.
>
> **For safety alerts, duplicate beats missed.** So: send-then-record, at-least-once, and make it idempotent at the edges. The `UNIQUE (event_id, user_id, channel)` constraint means a retry conflicts instead of double-sending. For webhooks we pass an idempotency key so the customer can dedupe on their side too.
>
> That gets exactly-once *observed behavior* out of at-least-once *delivery*, which is the thing that actually matters."

### 🔍 "How do you not spam people?" ← **they will absolutely ask this**

**Four layers. Name all four — this is Voxel's actual product problem.**

| Layer | Mechanism | Key |
|---|---|---|
| **1. Dedup** | Same hazard, same camera, within window → one alert | `(site, camera, event_type)`, Redis `SET NX EX 60` |
| **2. Rate limit** | Cap per recipient per window | Token bucket in Redis, per `user_id` |
| **3. Preferences** | Severity floor, channel choice, quiet hours | Subscription table |
| **4. Digest** | Roll low-severity into a daily summary | Batch job |

> "**Dedup and rate limiting are different mechanisms for different problems**, and conflating them is the classic mistake. Dedup asks 'is this the same ongoing thing?' — a spill firing 30 times a second is one spill. Rate limiting asks 'has this human had enough?' — that's about the person, not the hazard.
>
> **Critical severity bypasses rate limiting but *not* dedup.** Bypassing rate limiting is right: a blocked fire exit should never be suppressed because you already hit your hourly cap on PPE reminders. Bypassing dedup would be wrong: you'd get 30 notifications a second about a single blocked exit, which is strictly worse for the person trying to respond.
>
> Instead I'd shorten the dedup *window* for critical — 10 seconds instead of 60. Re-alert aggressively, don't flood."

**Making this distinction unprompted is a hire signal.** It's the exact problem their product has.

### 🔍 "Fan-out on read or fan-out on write?"

> "**Write, here.** Compute the recipient list when the event arrives and materialize a row per recipient.
>
> The trade-off is the classic Twitter one. Fan-out on read means one row and you compute recipients at query time — cheap writes, expensive reads, and it works for celebrities with 100M followers because you'd otherwise write 100M rows.
>
> But we don't have celebrities. Fan-out here is ~5 people, maybe 50 for a big site. And the read pattern is *push* — we're not waiting for someone to open an app, we're sending an SMS. You can't lazily compute a recipient list for a push. Plus materializing gives us per-recipient delivery status, which we need for the audit trail.
>
> The number that would change my mind: if some site had 50,000 subscribers, that's 50k rows per event and I'd reconsider. **But I'd want to know that's real before designing for it.**"

### 🔍 "SQL or NoSQL?"

> "**Postgres.** Three reasons, in order:
> 1. Subscriptions are relational and low-volume — joins and constraints are exactly what we want, and the schema is going to change as we add preference types.
> 2. We need transactions in the fan-out path.
> 3. **We're at thousands of writes/sec, not millions.** Postgres does that on one box.
>
> The one place I'd bend: `events` are append-only time-series, which is the pattern relational DBs handle worst at volume. I'd use **TimescaleDB** — still Postgres, so no operational split, but hypertables handle the time partitioning.
>
> **What would flip me to NoSQL:** sustained writes above ~10k/sec, or a schema that genuinely varies per event type — though `JSONB` covers most of that. **I'd rather start with Postgres and be forced off it by a real number than start with Cassandra and discover I need a join.**"

### 🔍 "A camera goes offline / the ML model false-positives"

> "Two very different failures.
>
> **Camera offline** is the absence of events, which no event-driven system notices by construction. You need a **heartbeat** — cameras report liveness, and a watchdog alerts on the gap. **A silently dead camera is worse than a noisy one**: the safety manager thinks that aisle is being watched and it isn't. For a safety product this is arguably the most important failure mode in the whole design, and it's the one that never shows up in the happy-path diagram.
>
> **False positives** are a product problem I'd support with engineering: a feedback loop where users mark an alert as wrong, which (a) feeds retraining, (b) drives per-site confidence thresholds — a site with reflective floors will false-positive spills constantly and should get a higher bar — and (c) auto-suppresses a detector that crosses a false-positive rate, because **an alert stream people learn to ignore is worse than no alert stream.** That's the real failure mode of this entire product category."

### 🔍 "What do you monitor?"

> "Four things, and the last one is the one people forget:
> 1. **End-to-end latency**, `occurred_at` → `delivered_at`, p50/p99. That's the SLO.
> 2. **Queue depth** and consumer lag — the leading indicator of everything.
> 3. **Delivery failure rate per channel** — catches a provider outage before customers do.
> 4. **DLQ depth > 0 pages someone.** Not a dashboard — a page. A notification that silently failed means a hazard nobody heard about."

---

## Phase 6 — Trade-offs & failure (40–48 min)

**Say these unprompted if they haven't asked:**

- **Thundering herd:** a whole shift arrives without PPE → 200 events in 10 seconds. The bus absorbs it; workers drain at their own pace. This is exactly why the bus exists.
- **Poison message:** one malformed event crashes the worker, which restarts, re-reads it, crashes again — forever, and the whole partition stalls. Fix: attempt counter, then DLQ. **Mention this. Almost nobody does, and it's the outage that actually happens.**
- **Slow consumer:** one customer's webhook is 30s. Per-channel queues contain it. Circuit-break after N failures.
- **Backpressure:** if the queue grows unboundedly, shed low-severity events first. Never shed critical. **Say the priority rule out loud.**
- **Privacy** ← **raise this yourself, unprompted:** *"This is video of real people at work. Voxel's stated position is 'visibility into hazards, not insights into individuals.' So: I'd store the detection and a bounding box, not an identity. Notification bodies say 'a worker' not a name. Retention windows measured in days. Role-based access on clips. This isn't a nice-to-have — a safety tool that becomes a surveillance tool loses worker trust, and then people work around it and the product stops working."*

**That last one is a differentiator.** Most candidates design the happy path and never mention that the subject of the video is a person with rights. Voxel has a whole blog post about this.

---
---

# DESIGN 2 — Job Scheduler / Workflow Management System ⭐ CONFIRMED ASKED
### At Voxel this is **Actions**: a detection becomes a task, assigned to an owner, with a deadline, tracked to completion.

---

## Phase 1 — Requirements (0–5 min)

**Functional**
- Submit a job: one-off, cron-scheduled, or event-triggered
- Jobs have dependencies → a **DAG**
- Workers pull and execute
- State machine per job: `PENDING → SCHEDULED → RUNNING → SUCCESS | FAILED | RETRYING | CANCELLED`
- Retry with backoff; max attempts
- Priority queues
- Query status; cancel

**Non-functional**
- **At-least-once execution** → **jobs must be idempotent, and that's a contract with the job author, not something the scheduler can guarantee.** Say this.
- No lost jobs — durability over latency, opposite of Design 1
- A worker dying must not lose its job
- Scheduling latency < 1s for the ready queue

**Numbers**
```
100k jobs/day  ≈ 1.2/s average, ~10/s peak.  Genuinely small.
Long tail: some jobs run 10ms, some run 6 hours. ← this shapes everything
```
> "The throughput is trivial. **The hard parts here are correctness, not scale**: exactly-once-ish semantics, dependency resolution, and detecting a worker that died mid-job. I'll spend my time there."

**Saying which part is hard, and being right, is most of this round.**

---

## Phase 2 — API (5–8 min)

```
POST /v1/jobs
  { "name": "clean_spill_aisle_4", "type": "action",
    "trigger": {"kind": "event", "event_id": "evt_..."},
    "payload": {...}, "priority": 5, "max_attempts": 3,
    "depends_on": ["job_abc"], "timeout_seconds": 3600 }
  → 201 { "job_id": "job_..." }

POST /v1/jobs/{id}/cancel
GET  /v1/jobs/{id}                      → status, attempts, timings, logs
GET  /v1/jobs?status=running&site=s-1

# Worker-facing — the interesting half
POST /v1/workers/lease   { "worker_id": "w-1", "capacity": 4 }
                         → [{ job_id, payload, lease_expires_at }]
POST /v1/workers/heartbeat { "worker_id": "w-1", "job_ids": [...] }
POST /v1/jobs/{id}/complete { "status": "success", "result": {...} }
```

> "**Workers pull, they don't get pushed to.** Pull means natural backpressure — a worker takes work when it has capacity, so we can't overwhelm it. Push means the scheduler has to model worker capacity, and it'll get it wrong.
>
> And **leases, not assignments.** A lease expires. That's how we detect a worker that died without telling us."

---

## Phase 3 — Data model (8–13 min)

```sql
CREATE TABLE jobs (
    job_id          UUID PRIMARY KEY,
    name            TEXT NOT NULL,
    payload         JSONB,
    status          TEXT NOT NULL,     -- pending|scheduled|running|success|failed|cancelled
    priority        SMALLINT DEFAULT 0,
    attempts        SMALLINT DEFAULT 0,
    max_attempts    SMALLINT DEFAULT 3,
    run_after       TIMESTAMPTZ,       -- backoff / cron next-fire
    lease_expires_at TIMESTAMPTZ,      -- ← the whole liveness story
    worker_id       TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    started_at      TIMESTAMPTZ,
    finished_at     TIMESTAMPTZ
);
-- THE hot query: "what should run next?"
CREATE INDEX ON jobs (status, priority DESC, run_after)
    WHERE status IN ('pending', 'scheduled');

CREATE TABLE job_dependencies (
    job_id       UUID REFERENCES jobs,
    depends_on   UUID REFERENCES jobs,
    PRIMARY KEY (job_id, depends_on)
);

CREATE TABLE job_attempts (          -- history, not current state
    attempt_id  UUID PRIMARY KEY,
    job_id      UUID REFERENCES jobs,
    worker_id   TEXT,
    started_at  TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    status      TEXT,
    error       TEXT
);
```

> "**`job_attempts` is separate from `jobs` on purpose.** `jobs` holds current state; attempts hold history. If you overwrite the error field on each retry you lose the debugging trail, and 'why did this fail three times differently' is the question you'll actually be asked at 3am."

---

## Phase 4 — Architecture (13–23 min)

```
  Triggers
  ├─ API (one-off)
  ├─ Cron (scheduled)          ┌──────────────────┐
  └─ Event bus (detections) ──►│    Scheduler     │
                               │                  │
                               │ • resolve deps   │  ← topological check
                               │ • check run_after│  ← backoff / cron
                               │ • enqueue ready  │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │  Ready Queue     │  priority ordered
                               │  (Postgres SKIP  │  (or Redis ZSET / SQS)
                               │   LOCKED, or     │
                               │   Redis)         │
                               └────────┬─────────┘
                                        │  lease (pull)
                        ┌───────────────┼───────────────┐
                        ▼               ▼               ▼
                   ┌────────┐      ┌────────┐      ┌────────┐
                   │Worker 1│      │Worker 2│      │Worker 3│
                   └───┬────┘      └───┬────┘      └───┬────┘
                       │ heartbeat     │               │
                       └───────────────┼───────────────┘
                                       ▼
                              ┌──────────────────┐
                              │  Postgres        │  jobs, deps, attempts
                              └──────────────────┘
                                       ▲
                              ┌────────┴─────────┐
                              │ Reaper (cron)    │  finds expired leases
                              │ → requeue or fail│  → requeue
                              └──────────────────┘
```

**The four things to explain:**

1. **The ready queue** — jobs whose dependencies are satisfied and whose `run_after` has passed. The scheduler's only job is moving things into it.
2. **`SELECT ... FOR UPDATE SKIP LOCKED`** — how you build a queue on Postgres without two workers grabbing the same job:
   ```sql
   UPDATE jobs SET status='running', worker_id=$1,
                   lease_expires_at = now() + interval '5 minutes',
                   attempts = attempts + 1, started_at = now()
   WHERE job_id = (
       SELECT job_id FROM jobs
       WHERE status='pending' AND (run_after IS NULL OR run_after <= now())
       ORDER BY priority DESC, created_at
       FOR UPDATE SKIP LOCKED
       LIMIT 1
   ) RETURNING *;
   ```
   > "`SKIP LOCKED` is the whole trick — concurrent workers skip rows another transaction has locked instead of blocking on them. **At 10 jobs/sec I don't need Kafka; Postgres is a perfectly good queue at this scale and it's one less system to operate.** That's a real trade-off, not a cop-out — I'd revisit above a few thousand/sec."
3. **The Reaper** — the box everyone forgets. It finds `lease_expires_at < now() AND status = 'running'` and requeues them.
   > "Without this, a worker that gets OOM-killed takes its job to the grave and it sits in `running` forever. **The reaper is how the system self-heals, and it's the single most important box on this diagram.**"
4. **Heartbeats extend leases** — a legitimately long job renews its lease. That's how you distinguish "slow" from "dead," which is *the* fundamental problem in distributed systems and you cannot solve it perfectly. Say that.

---

## Phase 5 — The deep dives

### 🔍 "How do you handle dependencies?" ← **the DAG question**

> "Topological sort. A job is ready when every job it depends on has `status = 'success'`. Two ways:
> - **Pull:** the scheduler polls for jobs whose deps are all done. Simple, but O(pending) per tick.
> - **Push:** on completion, decrement an in-degree counter on each dependent; hits zero → enqueue. That's **Kahn's algorithm**, O(1) per completion. Better.
>
> **And you must reject cycles at submission time** — if A depends on B depends on A, neither ever runs and it looks like a hang, not an error. Run the topological sort on submit and 400 if it doesn't produce a full ordering.
>
> **This is exactly LeetCode 207, Course Schedule** — Kahn's algorithm, and if you can't drain the queue, you have a cycle. Same code."

**Explicitly linking your Round 1 answer to your Round 3 answer is a strong move.** It shows the algorithms aren't trivia to you.

**Follow-up — "what if a dependency fails?"**
> "Product question, and I'd ask. Three policies: fail the whole DAG (`fail_fast`), skip dependents and continue siblings, or retry the dep and hold. **Airflow makes this configurable per-task and that's the right call** — for a safety action, 'notify the manager' shouldn't be skipped just because 'log to the EHS system' failed."

### 🔍 "Exactly-once execution?"

> "**Not achievable, and I'd push back on the requirement.** The classic case: worker completes the job, then dies before writing `success`. The lease expires. The reaper requeues. It runs twice. To prevent that you'd need an atomic 'do the work and record it,' but the work is on another machine, so there's no such transaction.
>
> **So: at-least-once, and require jobs to be idempotent.** That's a contract with the job author — 'send_email' takes an idempotency key, 'charge_card' checks for an existing charge. The scheduler *cannot* enforce this and shouldn't pretend to.
>
> What I'd add: an execution fence. Each attempt gets a monotonic token, and completion is rejected if the token is stale. That stops a zombie worker — one we thought was dead, whose job we requeued — from writing a `success` after the retry already ran. **That's fencing, and it's the thing that makes lease-based systems actually correct.**"

### 🔍 "Cron jobs — how?"

> "Store the cron expression and a `next_fire_at`. A ticker polls for `next_fire_at <= now()`, creates a job instance, computes the next fire time. Two traps:
> - **Missed fires.** Scheduler down for an hour with an every-15-min job — catch up all four, or just fire the next one? **Depends entirely on the job**, so it's config: `catchup: true/false`. Airflow's default catchup=true has surprised a lot of people at 3am.
> - **Timezones and DST.** '2:30am daily' happens zero times on one spring day and twice on one autumn day. Store the timezone, not the offset. **Nobody expects a new grad to raise this. Raise it.**"

### 🔍 "Priority — how do you prevent starvation?"

> "Strict priority ordering starves low-priority jobs forever if high-priority work keeps arriving. Fixes: **aging** (bump priority with wait time — simple, effective), **weighted fair queuing** (each class gets a guaranteed share), or **reserved capacity** (N workers only take low-priority).
>
> I'd start with aging: `effective_priority = priority + age_minutes / 10`. One line, solves 95% of it. **This is LeetCode 621, Task Scheduler, wearing a suit** — same starvation problem, same shape."

---

## Phase 6 — Trade-offs

- **Postgres-as-queue vs Kafka/SQS:** *"At 10/sec, Postgres. `SKIP LOCKED` is battle-tested, we get transactional enqueue with the state write — which is genuinely hard to do across two systems — and it's one less thing to operate. Above a few thousand/sec I'd move the ready queue to Redis or SQS and keep Postgres for state. **The mistake is reaching for Kafka at 10 jobs/sec because it feels more impressive.**"*
- **Poll vs push:** poll is simpler, one query per tick per worker; push needs the scheduler to track capacity. Poll at this scale.
- **Lease duration:** too short → healthy long jobs get killed and re-run. Too long → dead workers hold jobs. Heartbeats let you keep leases short (30s) while supporting 6-hour jobs. **Say the tension out loud; it's the real design decision here.**
- **Where it breaks first:** the reaper's scan, if `jobs` is huge and unpartitioned. Partial index on `status='running'`, or partition by month and only scan hot partitions.

---
---

# DESIGN 3 — Video Processing / Alerting Pipeline
### Their actual product. **Being able to relate your design back to Voxel is explicitly a plus** per your notes.
### Use this if they ask something open-ended, or offer it at the end.

```
 ┌──────────────────────────────────────────────────────────────┐
 │  CUSTOMER SITE (a warehouse — 30 existing security cameras)   │
 │                                                              │
 │   Cameras ──RTSP──►  ┌────────────────────┐                  │
 │   (existing          │   Edge Appliance   │                  │
 │    infra —           │                    │                  │
 │    the whole         │ • decode frames    │                  │
 │    business          │ • ML inference     │  ← runs HERE     │
 │    model)            │   (GPU/accelerator)│    not in cloud  │
 │                      │ • local buffer     │                  │
 │                      │ • send DETECTIONS  │                  │
 │                      │   not video        │  ← the key call  │
 │                      └─────────┬──────────┘                  │
 └────────────────────────────────┼─────────────────────────────┘
                                  │  detections (~1 KB) + clip refs
                                  │  (not 30 × 4 Mbps of raw video)
                                  ▼
                    ┌─────────────────────────┐
                    │   Ingest / Gateway      │  auth per site, backpressure
                    └────────────┬────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │      Event Bus          │  ← Design 1 starts here
                    │  (partition by site_id) │
                    └────────────┬────────────┘
                    ┌────────────┼─────────────┐
                    ▼            ▼             ▼
             ┌───────────┐ ┌───────────┐ ┌───────────┐
             │  Alerting │ │ Analytics │ │  Clip     │
             │  (Design1)│ │ (Timescale│ │  Service  │
             │           │ │  rollups) │ │ (S3 + CDN)│
             └─────┬─────┘ └─────┬─────┘ └───────────┘
                   │             │
                   ▼             ▼
             ┌───────────┐ ┌───────────┐
             │  Actions  │ │ Executive │
             │ (Design2) │ │    Hub    │
             └───────────┘ └───────────┘
```

## The four things to say about this one

**1. Inference at the edge, and here's the arithmetic:**
> "The single biggest decision is running inference at the edge rather than streaming video to the cloud. One camera at 1080p/15fps is roughly 4 Mbps. Thirty cameras is 120 Mbps *sustained*, per site, forever. Across 10,000 sites that's 1.2 Tbps of ingest and an egress bill that eats the company. Detections are ~1 KB and only when something happens.
>
> But it's not just cost. **Latency** — a forklift proximity warning needs sub-second, and a cloud round trip plus queue plus inference doesn't get there. **Availability** — the site's internet goes down and safety monitoring must not stop. **Privacy** — raw video never leaving the customer's building is a much easier procurement conversation than 'trust our S3 bucket.'
>
> The cost is fleet management: you're now shipping models to thousands of boxes you don't own, in buildings you can't visit, on networks that flake. That's a real operational burden and it's the trade you make."

**2. Clips are uploaded lazily.**
> "The edge keeps a rolling local buffer. When it detects something, it uploads only the ~10 seconds around the event, and the detection carries a reference. So you get the evidence without the firehose. Pre-signed S3 URLs so the appliance uploads directly and the clip never transits our API."

**3. Detections are time-series.**
> "TimescaleDB. Hypertables partitioned by time, continuous aggregates for the Executive Hub's rollups so the dashboard isn't scanning 90 days of raw detections on every page load, and retention is a chunk drop rather than a delete."

**4. The failure mode nobody mentions:**
> "The thing that scares me most isn't a flood of alerts — it's an edge box that goes quiet and nobody notices. Every appliance heartbeats independently of detections. **A camera that stops reporting must page someone**, because the safety manager thinks that aisle is covered and it isn't. In a safety product, silent failure is the worst possible failure — and it's the one an event-driven architecture is structurally blind to, because absence of events looks exactly like absence of hazards."

---
---

# Trade-off Drills — SUNDAY, 5:10–5:40
### 60 seconds each. Out loud. No notes. Repeat until fluent.

| Question | Your 60-second answer, compressed |
|---|---|
| **SQL vs NoSQL?** | Postgres unless proven otherwise. Relational data, transactions, schema evolution, thousands/sec not millions. TimescaleDB for the time-series slice. Flip at ~10k writes/sec sustained or genuinely schemaless data. *Start relational and get forced off it by a number.* |
| **Push vs pull?** | Push = low latency, server tracks capacity, can overwhelm. Pull = natural backpressure, simpler, adds poll latency. Workers pull. Notifications push. Hybrid: long-poll. |
| **Sync vs async?** | Sync when the caller needs the result to proceed. Async for anything that can fail independently or take unbounded time. Notification delivery is always async. *Never do network I/O inline in a fan-out loop.* |
| **At-least-once vs at-most-once?** | At-least-once + idempotent consumers, always, for alerts. Duplicate alert = annoying. Missed alert = someone got hurt. Exactly-once end-to-end is a marketing term; exactly-once *observed* is achievable with idempotency keys. |
| **Fan-out read vs write?** | Write, when fan-out is small and delivery is push. Read, for celebrity fan-out. Hybrid is what Twitter actually does. Here: write, ~5 recipients, and we need per-recipient status anyway. |
| **Cache invalidation?** | TTL for tolerable staleness (subscriptions: 60s is fine). Write-through when it must be fresh. Event-driven invalidation when you have a bus — you do. |
| **Monolith vs microservices?** | Monolith. Company is ~200 people. Microservices buy independent deploys at the cost of a distributed system you now have to debug. Split when a team boundary or a scaling boundary demands it, not before. *This answer being unfashionable is the point — say it anyway and defend it.* |
| **How do you shard?** | By `site_id`. Natural tenant boundary, keeps a customer's data co-located, no cross-shard joins for the common query. Hot shard risk if one customer is huge — sub-shard by camera. *Don't shard until a number forces it.* |
| **Consistency model?** | Strong for subscriptions (a preference change must take effect). Eventual for analytics and the feed. *A dashboard 5 seconds stale is fine; a quiet-hours setting 5 seconds stale pages someone at 2am.* |
| **CAP?** | Partitioned, we choose availability for alerting — deliver possibly-stale, don't stop alerting. But choose consistency for the scheduler — running a job twice is worse than running it late. *Different subsystems, different answers, same product.* |

---

# The Interviewer's Follow-Up Bank — rehearse cold answers

**On scale**
1. "10× the events tomorrow — what breaks first?"
2. "One customer is 50% of traffic. Problem?"
3. "What's your single point of failure?"
4. "Where's your bottleneck, and how do you know?"

**On correctness**
5. "A worker dies mid-job. Walk me through it."
6. "Duplicate alert goes out. How? How do you stop it?"
7. "Events arrive out of order. Does it matter?"
8. "Two subscription updates race. Who wins?"

**On product**
9. "The model false-positives 10% of the time. What do you build?"
10. "Users say they get too many alerts. What do you change first?"
11. "A customer wants alerts in their own system. How?"
12. "How do you know a notification was actually seen?"

**On operations**
13. "What's your SLO? How do you measure it?"
14. "What pages someone at 3am and what waits till morning?"
15. "How do you deploy a change to the fan-out logic safely?"
16. "How do you replay 6 hours of events after a bug?"

**On judgment** ← the ones that actually differentiate
17. **"What would you build first?"** → *"Ingest → queue → one channel → delivery status. Ship the skinny end-to-end path, then add dedup, then rate limiting, then preferences. Every one of those is a feature you add because a customer complained, and they'll complain in that order."*
18. **"What did you deliberately not design?"** → *"Multi-region. Exactly-once. Sharding. All three because the numbers don't justify them yet, and I'd rather have a system I can debug than one I can brag about."*
19. **"What are you least confident about?"** → **Answer honestly.** *"Quiet hours and timezones. I've seen that go wrong more than once and I'd want to look at how the site location data is modeled before committing."* Feigning total confidence is a bad signal; naming a specific uncertainty is a good one.

---

# The line that ends the round well

> "One thing I'd flag: this design is basically what your Actions and Risk Insights features do — detection to notification to assigned task to resolution. The interesting problem isn't the throughput, it's that the alerts have to stay *worth reading*. A safety alert stream people learn to ignore is worse than no alert stream, because now everyone thinks the aisle is being watched. That's why I spent most of my time on dedup and rate limiting rather than on scaling."

**That's the sentence.** It says: I researched you, I understand your product, and I know which problem is actually hard.
