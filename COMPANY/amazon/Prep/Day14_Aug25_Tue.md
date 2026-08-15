# Tue Aug 25 — Day 14 of 18
### PHASE 3 — ADVANCED + DESIGN · Intervals + Greedy

**Answer key for reference: `Day6_KEY.md`** · Solutions for today's problems are at the bottom of this file.

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Read only the *Trigger* and *Insight* lines below — never the code. Close it, keep going. At 20 min, read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

> **CONFIRMED: coding is on LiveCode — typed, on your own laptop. Not a whiteboard.**
> - **Code: type it.** You must be able to *run* it. Handwritten code you can't execute hides your bugs.
> - **Design: paper or whiteboard, always.** The in-person design round will put you at a board. Practise managing the space.
> - **No-backspace first pass.** Signature → return statement → fill the middle. Delete nothing until you reach the end, then fix. This is the commit-before-you-type discipline that stops the freeze.

---

## TODAY'S CHECKLIST

| ☐ | Block | Full | Compressed |
|---|---|---|---|
| ☐ | A — Primitives from memory | 45 min | 30 min |
| ☐ | B — Re-solve queue | 30 min | 20 min |
| ☐ | C — Problems / mock | 3h 30m | 2h |
| ☐ | D — Design | 60 min | 40 min |
| ☐ | E — Leadership Principles | 45 min | 20 min |
| ☐ | F — Pattern Journal | 20 min | 15 min |

---

## Block A — Primitives (from memory, timed)

Full Tier 1 + Tier 2 sweep.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 24 (+1d), Aug 22 (+3d).

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **The interval rule: sort by START to merge. Sort by END to maximise how many fit.** That single distinction is the difference between correct and subtly wrong, and it gets tested.
>
> **56's classic bug:** `out[-1][1] = max(out[-1][1], end)`. A fully-contained interval like `[1,10],[2,3]` breaks the naive version.
>
> **134's real interview question** isn't the code — it's *"why can't the answer be a station between the old start and the failure point?"* Rehearse that argument out loud.

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 56 | Merge Intervals ★★ | Sort by START | ____ |
| ☐ | 57 | Insert Interval | Three phases | ____ |
| ☐ | 435 | Non-overlapping Intervals | Sort by END | ____ |
| ☐ | 253 | Meeting Rooms II ★★ | Heap and sweep-line | ____ |
| ☐ | 986 | Interval List Intersections | Two pointers | ____ |
| ☐ | 2402 | Meeting Rooms III ★ | Two heaps | ____ |
| ☐ | 55 | Jump Game | Greedy reach | ____ |
| ☐ | 45 | Jump Game II | BFS-on-array levels | ____ |
| ☐ | 134 | Gas Station ★ | Restart on deficit | ____ |
| ☐ | 763 | Partition Labels | Last-occurrence map | ____ |
| ☐ | 881 | Boats to Save People | Sort + two pointers | ____ |

---

## Block D — Design

**LLD 4 — Rate Limiter (object-oriented this time).**

You did the *system* on Aug 14. Today do the *classes*.

- **Interface:** `RateLimiter` with `allow(clientId) -> bool`
- **Implementations:** `TokenBucketLimiter`, `LeakyBucketLimiter`, `SlidingWindowLimiter` — Strategy pattern
- **Why the interface matters:** you can swap algorithms without touching a single caller. That's the Open/Closed principle — mention it *once*, naturally, not as a recitation.
- **Config:** per-client rules, defaults, hot reload
- **Storage abstraction:** in-memory for one host, Redis-backed for distributed, behind the same interface
- **Thread safety:** where's the lock? Can you do it lock-free with an atomic compare-and-swap?

**Know these five patterns by name and be able to justify one:** Strategy, Factory, Observer, Singleton, Builder.

---

## Block E — Leadership Principles

**Mandatory-story rehearsal — the ones asked in nearly every loop:**
- [ ] A time you failed
- [ ] Tough feedback you received, and what you actually changed
- [ ] A conflict with a teammate

For the feedback story, the follow-up is always *"what did you change, and how do you know it stuck?"* Have the evidence ready.

---

### Block F — Pattern Journal (20 min)

One entry per problem you struggled with. Handwritten beats typed.

```
Problem:            ____
Trigger phrase:     ____   <- the words in the prompt that should have tipped you off
Pattern:            ____
Key insight:        ____
Where I got stuck:  ____
Primitive used:     #__
Re-solve on:        +1d ____   +3d ____   +7d ____
```

**The Trigger line matters most.** You already know approaches. What you lack is the reflex mapping *problem phrasing → pattern*. Build it explicitly.

---

## END OF DAY — honest check

- [ ] Sort-by-start vs sort-by-end — can I say which and why, instantly?
- [ ] Can I do 253 both ways (heap and sweep-line)?
- [ ] Can I name five design patterns and justify my choice of one?


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 56. Merge Intervals ★★ (Amazon favourite)
```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])   # sort by START
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)    # max! not just `end`
        else:
            out.append([start, end])
    return out
```
**O(n log n) / O(n)** — **Gotcha:** `max(out[-1][1], end)`. A fully-contained interval like `[1,10],[2,3]` breaks the naive version.

---

---

### 57. Insert Interval
**Insight:** Three phases: everything strictly before, the overlapping merge, everything strictly after.
```python
def insert(intervals, newInterval):
    out = []
    i, n = 0, len(intervals)
    start, end = newInterval

    while i < n and intervals[i][1] < start:      # entirely before
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:       # overlapping
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    while i < n:                                  # entirely after
        out.append(intervals[i])
        i += 1
    return out
```
**O(n) / O(n)** — no sort needed; input is already sorted.

---

---

### 435. Non-overlapping Intervals
**Insight:** Sort by **END**. Greedily keep the interval that finishes earliest — it leaves the most room. This is the classic activity-selection proof.
```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])   # sort by END
    kept = 0
    prev_end = float('-inf')
    for start, end in intervals:
        if start >= prev_end:
            kept += 1
            prev_end = end
    return len(intervals) - kept
```
**O(n log n) / O(1)** — **sort by end, not start.** This is the difference between correct and subtly wrong.

---

---

### 253. Meeting Rooms II ★★ (Amazon favourite)
**Way A — min-heap of end times (present this):**
```python
import heapq
def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []                            # end times of ongoing meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)          # a room freed up — reuse it
        heapq.heappush(heap, end)
    return len(heap)
```
**Way B — sweep line / chronological ordering (the elegant one):**
```python
def minMeetingRooms_sweep(intervals):
    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)
    rooms = best = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:
            rooms += 1
            best = max(best, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    return best
```
**O(n log n) / O(n)** — the heap version generalises better to follow-ups; the sweep is easier to explain.

---

---

### 986. Interval List Intersections
```python
def intervalIntersection(firstList, secondList):
    out = []
    i = j = 0
    while i < len(firstList) and j < len(secondList):
        lo = max(firstList[i][0], secondList[j][0])
        hi = min(firstList[i][1], secondList[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if firstList[i][1] < secondList[j][1]:
            i += 1                       # advance whichever ends first
        else:
            j += 1
    return out
```
**O(m+n) / O(1)** — "intersection = max of starts, min of ends" is the reusable line.

---

---

### 2402. Meeting Rooms III ★ (Amazon favourite)
**Insight:** Two heaps — free rooms (by index) and busy rooms (by end time). If nothing's free, the meeting is *delayed*, not dropped.
```python
import heapq
def mostBooked(n, meetings):
    meetings.sort()
    free = list(range(n))
    heapq.heapify(free)
    busy = []                            # (end_time, room)
    count = [0] * n

    for start, end in meetings:
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)   # release finished rooms
        if free:
            room = heapq.heappop(free)
            heapq.heappush(busy, (end, room))
        else:
            finish, room = heapq.heappop(busy)          # wait for the earliest
            heapq.heappush(busy, (finish + (end - start), room))
        count[room] += 1

    return count.index(max(count))       # lowest index wins ties
```
**O(m log m + m log n) / O(n)** — **Gotchas:** delay keeps the *duration*, not the original end time; ties go to the lowest room number.

---

## PART D — GREEDY

---

### 55. Jump Game
```python
def canJump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False                 # unreachable
        reach = max(reach, i + x)
    return True
```
**O(n) / O(1)**

---

---

### 45. Jump Game II ★
**Insight:** This is BFS on an array. `cur_end` marks the boundary of the current "level"; crossing it costs one jump.
```python
def jump(nums):
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):       # stop before the last index
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                 # exhausted the current level
            jumps += 1
            cur_end = farthest
    return jumps
```
**O(n) / O(1)** — **Gotcha:** `range(len(nums) - 1)`. Including the last index adds a phantom jump.

---

---

### 134. Gas Station ★
**Insight:** If total gas ≥ total cost, a solution exists and is unique. If you run dry at station `i`, no station between the old start and `i` can work either — so jump the start to `i+1`.
```python
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1                # restart here
            tank = 0
    return start
```
**O(n) / O(1)** — the "why can't the start be in between?" argument is the actual interview question. Rehearse it.

---

---

### 763. Partition Labels
**Insight:** Record each character's last occurrence, then extend the partition until you reach the furthest last-occurrence in it.
```python
def partitionLabels(s):
    last = {ch: i for i, ch in enumerate(s)}
    out = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end:                     # nothing inside reaches beyond here
            out.append(end - start + 1)
            start = i + 1
    return out
```
**O(n) / O(26)**

---

---

### 881. Boats to Save People
```python
def numRescueBoats(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1                      # lightest rides with heaviest
        hi -= 1                          # heaviest always boards
        boats += 1
    return boats
```
**O(n log n) / O(1)**

---

## STRETCH

---
