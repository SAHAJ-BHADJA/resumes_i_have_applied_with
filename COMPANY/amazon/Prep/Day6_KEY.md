# DAY 6 ANSWER KEY — Binary Search, Intervals, Greedy

> **Binary search on the answer — the recognition rule.**
> If the problem says *"minimum X such that..."* or *"maximum X such that..."*, and you can write a `feasible(x)` check in O(n), you binary search over the **answer space**, not the array.
> The template never changes:
> ```
> lo, hi = smallest_possible_answer, largest_possible_answer
> while lo < hi:
>     mid = (lo + hi) // 2
>     if feasible(mid): hi = mid
>     else:             lo = mid + 1
> return lo
> ```
> **90% of the work is writing `feasible`. Write it first, on the board, before the search.**
>
> **Interval rule:** sort by **start** to merge; sort by **end** to maximise how many fit.

---

## PART A — CLASSIC BINARY SEARCH

### 704. Binary Search
```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

---

### 34. Find First and Last Position ★
**Insight:** Two boundary searches. Don't hand-roll — use the `lower_bound` primitive twice.
```python
import bisect
def searchRange(nums, target):
    left = bisect.bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect.bisect_right(nums, target) - 1
    return [left, right]
```
*Hand-rolled (if they ban `bisect`):*
```python
def searchRange_manual(nums, target):
    def bound(is_left):
        lo, hi, ans = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                ans = mid
                if is_left: hi = mid - 1     # keep going left
                else:       lo = mid + 1     # keep going right
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
    return [bound(True), bound(False)]
```
**O(log n) / O(1)**

---

### 33. Search in Rotated Sorted Array ★★
**Insight:** At any `mid`, **one half is always properly sorted.** Identify which, then test whether the target lies inside that sorted half.
```python
def searchRotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:            # LEFT half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                # RIGHT half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```
**O(log n) / O(1)** — **Gotcha:** `nums[lo] <= nums[mid]` with `<=`, for the 2-element case.

---

### 153. Find Minimum in Rotated Sorted Array
**Insight:** Compare `mid` against `hi`, never against `lo`.
```python
def findMin(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1                 # min is strictly right of mid
        else:
            hi = mid                     # mid could BE the min
    return nums[lo]
```
**O(log n) / O(1)** — comparing against `lo` breaks on a non-rotated array. Know why.

---

### 162. Find Peak Element
```python
def findPeakElement(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1                 # ascending -> a peak lies to the right
        else:
            hi = mid
    return lo
```
**O(log n) / O(1)** — works because `nums[-1] = nums[n] = -∞`, so an ascending slope must eventually turn.

---

### 240. Search a 2D Matrix II — staircase
**Insight:** Start at the **top-right**. That corner is the largest in its row and smallest in its column, so every comparison eliminates a whole row or column.
```python
def searchMatrix(matrix, target):
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        v = matrix[r][c]
        if v == target:
            return True
        elif v > target:
            c -= 1                       # eliminate this column
        else:
            r += 1                       # eliminate this row
    return False
```
**O(m+n) / O(1)**

---

## PART B — BINARY SEARCH ON THE ANSWER ★★★

*This is the highest-yield sub-pattern of the entire week. All four below are the same code.*

### 875. Koko Eating Bananas
```python
import math
def minEatingSpeed(piles, h):
    def hours_needed(speed):
        return sum(math.ceil(p / speed) for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:       # feasible
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**O(n log(max pile)) / O(1)** — say out loud: "answer space is 1 to max(piles); feasibility is monotonic because eating faster never takes more hours."

---

### 1011. Capacity To Ship Packages Within D Days
```python
def shipWithinDays(weights, days):
    def days_needed(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:
                d += 1
                cur = 0
            cur += w
        return d

    lo, hi = max(weights), sum(weights)  # lo = must fit the heaviest item
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**Gotcha:** `lo = max(weights)`, not 1 — a capacity smaller than the largest package is impossible.

---

### 1482. Minimum Number of Days to Make m Bouquets
```python
def minDays(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1                        # state this guard first
    def can(day):
        bouquets = run = 0
        for b in bloomDay:
            if b <= day:
                run += 1
                if run == k:
                    bouquets += 1
                    run = 0
            else:
                run = 0                  # adjacency broken
        return bouquets >= m

    lo, hi = min(bloomDay), max(bloomDay)
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

### 410. Split Array Largest Sum
```python
def splitArray(nums, k):
    def pieces(limit):
        cnt, cur = 1, 0
        for x in nums:
            if cur + x > limit:
                cnt += 1
                cur = 0
            cur += x
        return cnt

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**Point out loud that 410 and 1011 are literally the same function.** That recognition is worth more than the code.

---

### 1283. Find the Smallest Divisor Given a Threshold
```python
import math
def smallestDivisor(nums, threshold):
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(math.ceil(x / mid) for x in nums) <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

---

## PART C — INTERVALS

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

### 4. Median of Two Sorted Arrays ★★★ (hard)
**Insight:** Binary search the **partition point** in the smaller array. A correct partition has `maxLeft <= minRight` on both sides.
```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1      # always search the SHORTER one
    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2               # elements taken from nums1
        j = half - i                     # elements taken from nums2
        left1  = nums1[i-1] if i > 0 else float('-inf')
        right1 = nums1[i]   if i < m else float('inf')
        left2  = nums2[j-1] if j > 0 else float('-inf')
        right2 = nums2[j]   if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:          # correct partition
            if (m + n) % 2:
                return max(left1, left2)
            return (max(left1, left2) + min(right1, right2)) / 2
        elif left1 > right2:
            hi = i - 1                   # took too many from nums1
        else:
            lo = i + 1
    return 0.0
```
**O(log min(m,n)) / O(1)** — draw the partition diagram before writing a line. If you can't get it, offer the O(m+n) merge — a working suboptimal answer beats a broken optimal one at Amazon.

---

### 1353. Maximum Number of Events That Can Be Attended
```python
import heapq
def maxEvents(events):
    events.sort()
    heap = []
    i = 0
    attended = 0
    day = 0
    while i < len(events) or heap:
        if not heap:
            day = max(day, events[i][0])
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(heap, events[i][1])       # push END days
            i += 1
        while heap and heap[0] < day:
            heapq.heappop(heap)                      # expired
        if heap:
            heapq.heappop(heap)                      # attend the one ending soonest
            attended += 1
        day += 1
    return attended
```
**Greedy rule:** each day, attend the event that expires soonest.

---

### 135. Candy
**Insight:** Two passes. Left-to-right fixes the ascending constraint; right-to-left fixes descending. Take the max.
```python
def candy(ratings):
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candies[i] = max(candies[i], candies[i+1] + 1)
    return sum(candies)
```
**O(n) / O(n)** — "two passes, one per direction" is a reusable idea (also solves Trapping Rain Water).

---

## DAY 6 PATTERN TRIGGERS

| If the problem says... | Reach for |
|---|---|
| "find target in sorted array" | plain binary search |
| "first/last occurrence", "count of X" | lower_bound / upper_bound |
| "rotated sorted array" | one half is always sorted — identify which |
| "sorted matrix, rows and cols sorted" | staircase from top-right |
| **"minimum X such that..." / "maximum X such that..."** | **binary search on the answer — write `feasible()` first** |
| "minimum speed / capacity / divisor / days" | same as above; answer space is the search space |
| "split into k parts, minimise the largest" | binary search the largest-sum limit |
| "merge overlapping intervals" | sort by **start** |
| "maximum non-overlapping intervals / fewest removals" | sort by **end** |
| "minimum rooms / max concurrency" | heap of end times, or sweep line |
| "intersection of two interval lists" | two pointers; max of starts, min of ends |
| "can you reach the end / fewest jumps" | greedy reach, or level-based BFS-on-array |
| "circular tour / gas station" | total-feasibility check + restart on deficit |
| "partition so each element appears in one part" | last-occurrence map + extend the boundary |
| pair up light with heavy | sort + two pointers from the ends |
