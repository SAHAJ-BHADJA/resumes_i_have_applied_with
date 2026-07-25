# Voxel — Company Cheat Sheet
### Everything you need loaded before Jul 21. Read it Friday morning, again Monday, and once the night before.

---

## The one-paragraph version

Voxel is a San Francisco applied-AI company that turns a factory's or warehouse's **existing security cameras** into a real-time workplace-safety system. Computer vision watches the video streams, detects leading indicators of risk (PPE violations, ergonomic hazards, forklift speeding, spills, blocked exits), and then — critically — **routes those detections into workflows**: alerts, assigned tasks, owners, deadlines, and executive reporting. Detection *to resolution*, not just detection.

**Why that matters for your interview:** their entire product is a pipeline that turns events into notifications into assigned work. Which is exactly why the two confirmed system design questions are "event notification system" and "job scheduler / workflow management system." You are being asked to design their product with the labels filed off.

---

## Hard facts (memorize the bolded ones)

| | |
|---|---|
| **Founded** | 2020 |
| **HQ** | San Francisco, team members worldwide |
| **CEO** | **Vernon O'Donnell** |
| **Founders** | Anurag Kanungo, Harishma Dayanidhi, Tilia Gode, Alex Kaveh Senemar, Troy Carlson |
| **Stage** | **Series B — $44M, June 2025**, led by NewRoad Capital Partners |
| **Series B participants** | Eclipse, Rite-Hite, Tokio Marine, MTech, HG Ventures, Whitestone |
| **Strategic investor** | **Ericsson Ventures** (Oct 2025) — aligns with their edge-compute roadmap |
| **Total raised** | ~$64M after Ericsson; some trackers list ~$83M across 6 rounds |
| **Employees call themselves** | **"Voxelitos"** |
| **Board** | Chris Sultemeier (former Walmart EVP) joined Jul 2025 |

## The numbers that make the mission real

- <cite index="7-1">Almost **3 million people in the US per year** are injured in the workplace for entirely preventable and at times fatal or debilitating causes</cite>. **This is the number to quote in "why Voxel." It's their own LinkedIn language.**
- <cite index="2-1">**2.78M workers** lose their lives every year to work-related incidents globally</cite>
- Workers' comp, general liability, and property damage <cite index="20-1">cost employers over **$500 billion annually**</cite>
- Voxel's AI is <cite index="6-1">trained on more than **5 billion hours** of real-world industrial workplace scenarios</cite>
- Customer proof: Vertical Cold Storage saw a **98% decrease in near misses** and a **21% reduction in recordable injuries**
- Reported **147% YoY revenue growth**, **202% net revenue retention**, sites recording up to **91% fewer injuries** (~$2.2M saved over two years)

## Customers & industries

<cite index="19-1">Fortune 500 companies across major grocers and retailers, manufacturers, food and beverage warehousers, and supply chain and logistics service providers</cite>. Also insurance (which is why Tokio Marine invested — carriers want provable risk reduction).

---

## The product surface — know these four by name

| Feature | What it does | Why it's interview-relevant |
|---|---|---|
| **Site Intelligence / Industrial Intelligence Platform** | The core: CV on existing cameras, 24/7, across people, vehicles, equipment, environment | This is the video pipeline in Design 3 |
| **Actions** | <cite index="40-1">Turns a detection into an assigned task; assignee marks it completed</cite> | **This is a job scheduler / workflow engine.** Design 2 is literally this. |
| **Executive Hub** (Oct 2025) | Macro view across all locations: top risks, impact measurement, team accountability | Aggregation, rollups, time-series — TimescaleDB territory |
| **Risk Insights** (Apr 2026, Beta) | <cite index="43-1">Continuously analyzes facility data, surfaces critical risks and emerging trends as concise summaries delivered via portal, email, and SMS</cite> | **This is an event notification system with multi-channel fan-out.** Design 1 is literally this. |

**The killer line for your systems round:** *"This is essentially what Risk Insights does — analyze the stream, decide what's worth surfacing, and fan it out to the right person over the right channel without flooding them."*

---

## The tech stack — from their own job posts

> <cite index="19-1">Our stack spans **Go, TypeScript, React, Python, AI systems, and large-scale data workflows.** We don't expect candidates to have deep expertise in every area. We value strong engineering fundamentals, learning velocity, and thoughtful problem solving over checking every technology box.</cite>

More specifically, across their backend/platform postings:

- **Languages:** Python, Go, Node/TypeScript
- **APIs:** GraphQL, REST
- **Data:** <cite index="20-1">PostgreSQL, MongoDB, TimescaleDB</cite>
- **Cloud:** AWS (IAM, S3, RDS, **EKS**) and GCP
- **Infra:** Docker, Kubernetes, **Terraform** (infrastructure-as-code)
- **Frameworks seen:** Django, Flask
- **Domain:** <cite index="24-1">architectures for running AI on realtime video at scale</cite>; ML pipeline, web platform, and **edge devices**

**Interview implications:**
- Round 2 will be **Python**. Your notes say so and the stack confirms it.
- **TimescaleDB in the stack is a gift.** If you say "detections are time-series data — I'd use a time-series store like TimescaleDB rather than raw Postgres tables, with continuous aggregates for the dashboard rollups," you sound like you already work there.
- **Edge matters.** They run inference at the edge, not just cloud. Mentioning edge-vs-cloud trade-offs (bandwidth cost, latency, privacy, intermittent connectivity) in Design 3 is a differentiator.
- Don't fake Go depth. Their own posting says they don't expect it. Say "I've worked mostly in Python; I'd pick up Go quickly and I'm looking forward to it."

---

## Culture signals to mirror

From the Applications Engineer posting (the 0–4 YOE role):

> <cite index="19-1">Experience in companies ~50-500 people, where engineers own end-to-end product flows. [...] The most successful engineers at Voxel are **curious, humble, coachable, and eager to grow** alongside the team as we continue to scale.</cite>

> <cite index="21-1">This is an ideal role for an engineer with 0-4 years of professional experience who wants to grow quickly by **pairing with senior engineers**, owning features, and working across the application lifecycle. This is a **hands-on coding role** with deep mentorship.</cite>

**Decode this:**
- "**Pairing with senior engineers**" → that's why Round 2 exists. They are testing whether pairing with you is pleasant. Be the person who thinks out loud and takes suggestions well.
- "**Coachable**" → in Round 2, when the interviewer suggests something, *take it* and say why it's better. Do not defend your first idea out of ego.
- "**Owns end-to-end product flows**" → your STAR stories should have you touching more than one layer.
- "**Humble**" → the "receiving hard feedback" story matters more here than at a big company.

## Their stated AI ethics position (worth one sentence in behavioral)

> <cite index="8-1">You gain visibility into hazards, not insights into individuals.</cite>

They are explicit that the CV is <cite index="8-1">precisely engineered to protect worker privacy and company information</cite>. If privacy comes up in your system design — and it should, because you should raise it yourself — say you'd blur/anonymize identities, store detections not raw identity, and keep retention windows short with role-based access. **This is a real differentiator: most candidates design the happy path and never mention that the subject of the video is a human being with rights.**

---

## Recent news timeline (so you sound current)

| Date | Event |
|---|---|
| Jun 2025 | $44M Series B |
| Jul 2025 | Chris Sultemeier (ex-Walmart EVP) joins board |
| Jun 2025 | International expansion across five continents; TT Club/ICHCA Innovation in Safety Award |
| Oct 2025 | **Executive Hub** launched |
| Oct 2025 | **Ericsson Ventures** strategic investment |
| Dec 2025 | Named 2025 Top Tech Startup by Food Logistics |
| Feb 2026 | Sponsored Safety Executives of New York conference |
| **Apr 2026** | **Risk Insights launched at Modex26** (most recent product news — mention this one) |

---

## Sources worth a 10-minute skim (Friday, or any downtime)

- `voxelai.com` — the Solutions and Product pages
- `voxelai.com/blog/introducing-actions-closing-the-gap-between-safety-detection-resolution` — read this one properly, it's the shape of Design 2
- `voxelai.com/blog/ai-for-good` — the privacy position
- Their LinkedIn posts feed — the mission language you'll echo back

---

## Three sentences you should be able to say cold

1. *"Voxel takes the cameras a warehouse already has and turns them into a real-time risk detection system — but the part I find interesting is Actions, because detection without resolution is just a dashboard nobody reads."*
2. *"Almost three million people in the US get hurt at work every year from causes that were preventable. That's the whole pitch, and it's a rare case where the engineering problem and the reason to care are the same problem."*
3. *"You're running inference on realtime video at scale across edge and cloud, on a stack that's Python and Go and large-scale data workflows — that's the kind of problem I want to be pairing on for the next few years."*
