# -*- coding: utf-8 -*-
"""Day 3 - Round Type C: intervals, heaps and top-K."""

DAY = "Day 3 · Thu 27 Aug · Round Type C (intervals, heaps, top-K)"

PROBLEMS = [

{
"num": 56, "title": "Merge Intervals", "stars": "★★  Amazon favourite", "day": DAY,
"pattern": "Sort by start, then one linear merge pass",
"opt_cx_short": "O(n log n) time, O(n) space",
"clarify": [
 "Are the intervals **given sorted**? If they already arrive sorted by start, the whole thing is a single O(n) pass and I should say so.",
 "Do intervals that merely **touch** count as overlapping &mdash; does `[1,4]` merge with `[4,5]`? That decides whether my comparison is `<=` or `<`. The standard version says yes, they merge.",
 "Can an interval be fully contained inside another, like `[1,10]` and `[2,3]`? This is the case that breaks the naive merge, so I want it confirmed.",
 "May I modify the input list, or should I sort a copy?",
 "Are the endpoints integers, and is `start <= end` guaranteed for every interval?",
],
"understand":
 "Given a list of intervals, merge all overlapping ones and return the resulting non-overlapping "
 "list covering the same total span.\n\n"
 "The reason sorting by **start** is the right move: after sorting, if the current interval "
 "does not overlap the last merged interval, then no later interval can overlap that merged one "
 "either &mdash; every later interval starts at or after the current one. That single fact "
 "turns a global, all-pairs problem into a purely local one, where each interval need only be "
 "compared against the single most recent output entry. It is the interval equivalent of the "
 "two-pointer trick: sort so that a local decision becomes globally correct.",
"brute_en":
 "Repeatedly look for any overlapping pair anywhere in the list and fuse it, until no "
 "overlapping pair remains. Concretely: scan every pair `(i, j)`; if they overlap, replace them "
 "with a single interval spanning `min` of the starts to `max` of the ends, restart the scan, "
 "and keep going until a full pass finds nothing to merge.\n\n"
 "It is correct because merging two overlapping intervals never destroys coverage and never "
 "creates new overlap that was not already implied, and the process terminates because each "
 "merge reduces the list length by one.",
"brute_ds":
 "- A mutable list of intervals, repeatedly rewritten.\n"
 "- A `changed` flag to know when the process has stabilised.",
"brute_algo": [
 "Set `changed = True`.",
 "While `changed`: set `changed = False`.",
 "Scan every pair of distinct indices `(i, j)` in the current list.",
 "Two intervals overlap when `a.start <= b.end` **and** `b.start <= a.end`.",
 "On finding an overlapping pair, replace interval `i` with `[min(a.start, b.start), max(a.end, b.end)]`, delete interval `j`, set `changed = True`, and break out to restart the scan on the modified list.",
 "When a complete scan finds no overlapping pair, return the list.",
],
"brute_cx":
 "**Time: O(n³) in the worst case.** Each full pass examines O(n²) pairs, and there can "
 "be up to n−1 merges, each of which restarts the scanning. Deleting from a Python list is "
 "itself O(n), adding another factor.\n\n"
 "**Space: O(n)** for the working list.",
"brute_code":
'''def merge_brute(intervals):
    """Repeatedly fuse any overlapping pair until a full pass finds none."""
    out = [list(iv) for iv in intervals]  # work on a copy
    changed = True
    while changed:
        changed = False
        n = len(out)
        for i in range(n):
            for j in range(i + 1, n):
                a, b = out[i], out[j]
                # overlap test for two unordered intervals
                if a[0] <= b[1] and b[0] <= a[1]:
                    out[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    out.pop(j)            # O(n) deletion
                    changed = True
                    break
            if changed:
                break                     # restart the scan on the modified list
    return out''',
"brute_limit":
 "Because the intervals are in arbitrary order, an interval could overlap anything anywhere in "
 "the list, so every merge forces a fresh all-pairs search. The algorithm never accumulates any "
 "knowledge about where overlapping partners might be.\n\n"
 "Sorting by start supplies exactly that knowledge. Once sorted, overlap can only ever occur "
 "with the immediately preceding merged interval, because every subsequent interval starts "
 "later still. The all-pairs search collapses to a single comparison per interval, and the "
 "whole algorithm becomes one pass after the sort.",
"opt_en":
 "Sort the intervals by start. Walk them in order, maintaining an output list whose last "
 "element is the interval currently being extended.\n\n"
 "For each interval `[start, end]`: if the output is non-empty and `start <= out[-1][1]`, this "
 "interval begins before the last merged one has finished, so they overlap and I extend the "
 "last one's end. Otherwise there is a genuine gap, so I append `[start, end]` as a new "
 "interval.\n\n"
 "The critical line is the extension: it must be `out[-1][1] = max(out[-1][1], end)`, **not** "
 "`= end`. A fully contained interval such as `[2, 3]` arriving while `[1, 10]` is being "
 "extended would otherwise shrink the merged interval from `[1, 10]` to `[1, 3]` and silently "
 "lose coverage. That is the one bug that decides this problem, and it is worth naming as you "
 "write the line.\n\n"
 "Using `<=` rather than `<` means touching intervals like `[1,4]` and `[4,5]` merge, which "
 "matches the standard requirement clarified up front.",
"opt_ds":
 "- The **sorted list** itself; sorting by start is the enabling step and the only reason a "
 "local comparison is sufficient.\n"
 "- An **output list**, whose last element acts as the running accumulator. No stack, no map, "
 "no auxiliary structure &mdash; the output doubles as the working state.",
"opt_algo": [
 "Sort `intervals` by start using `key=lambda x: x[0]`.",
 "Create an empty output list.",
 "For each `[start, end]` in sorted order:",
 "If the output is non-empty and `start <= out[-1][1]`, the intervals overlap or touch, so set `out[-1][1] = max(out[-1][1], end)`. The `max` is what protects against a fully contained interval.",
 "Otherwise append `[start, end]` to the output as a fresh interval.",
 "Return the output.",
],
"opt_code":
'''def merge(intervals):
    """Sort by START, then a single linear pass extending the last output entry."""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])    # sorting by start is the whole idea
    out = []

    for start, end in intervals:
        # `<=` so touching intervals ([1,4] and [4,5]) also merge
        if out and start <= out[-1][1]:
            # *** max(), not just `end` ***
            # [1,10] followed by [2,3] must stay [1,10], not shrink to [1,3].
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])      # a genuine gap: start a new interval

    return out''',
"opt_cx":
 "**Time: O(n log n)**, entirely dominated by the sort. The merging pass itself is O(n), with "
 "one comparison and at most one update per interval.\n\n"
 "**Space: O(n)** for the output, plus O(log n) to O(n) for the sort's internal working memory "
 "depending on the implementation. If the input arrives pre-sorted, the whole thing is O(n) "
 "time and O(1) extra space beyond the output.\n\n"
 "**Say this out loud:** \"Sorting by start means an interval can only overlap the most recent "
 "merged one, because everything after it starts later. So one comparison per interval "
 "suffices. Sort dominates at O(n log n), the merge pass is O(n).\"\n\n"
 "**The gotcha:** `max(out[-1][1], end)`, demonstrated with `[[1,10],[2,3]]`. **The family:** "
 "Insert Interval is the same pass with a pre-sorted list; Non-overlapping Intervals and "
 "Meeting Rooms II are the same shape but sort by **end** instead, because maximising how many "
 "intervals fit is a different objective from merging them.",
},

{
"num": 253, "title": "Meeting Rooms II", "stars": "★★  Amazon favourite", "day": DAY,
"pattern": "Min-heap of end times, or a sweep line",
"opt_cx_short": "O(n log n) time, O(n) space",
"clarify": [
 "If one meeting ends at 10 and another starts at 10, can they share a room? I will assume yes &mdash; end times are exclusive &mdash; and that determines whether my comparison is `<=` or `<`.",
 "Am I returning just the **number** of rooms, or an actual room assignment for each meeting? The heap version extends naturally to the assignment if you need it.",
 "Are the intervals sorted on input? I will assume not and sort them myself.",
 "Can meetings have zero duration, where start equals end?",
 "How large is n? That decides whether an O(n log n) sort is acceptable, which it almost always is.",
],
"understand":
 "Given a list of meeting intervals, return the minimum number of conference rooms required so "
 "that no two meetings in the same room overlap.\n\n"
 "The reframing that makes the answer obvious: the number of rooms needed is exactly the "
 "**maximum number of meetings that are simultaneously in progress** at any instant. If four "
 "meetings overlap at 10:15, you need four rooms at that moment; and conversely, if the peak "
 "concurrency is four, four rooms always suffice, because a greedy assignment can always place "
 "a meeting into some room whose previous occupant has already finished.\n\n"
 "So this is not really a scheduling problem, it is a **peak concurrency** problem. Both "
 "standard solutions compute that peak; they just track it differently.",
"brute_en":
 "Compute the concurrency at each meeting's start time directly. For every meeting `i`, count "
 "how many meetings &mdash; including `i` itself &mdash; are in progress at the instant "
 "`i` begins: that is, every meeting `j` with `start[j] <= start[i] < end[j]`. The answer is "
 "the maximum of those counts.\n\n"
 "This is correct because the concurrency of a set of intervals can only increase at a start "
 "point, so the global maximum is always attained at the start of some meeting. It is therefore "
 "sufficient to sample only at the n start times, rather than at every possible instant.",
"brute_ds":
 "- None beyond two loop counters and a running maximum. O(1) extra space.",
"brute_algo": [
 "Return 0 for an empty list.",
 "Set `best = 0`.",
 "Loop `i` over all meetings; let `t = start[i]`, the instant to sample.",
 "Set `count = 0`, then loop `j` over all meetings.",
 "If `start[j] <= t < end[j]`, meeting `j` is in progress at time `t`, so increment `count`. The strict `<` on the end is what implements the rule that a meeting ending at `t` frees its room for a meeting starting at `t`.",
 "Update `best` with `count`.",
 "Return `best`.",
],
"brute_cx":
 "**Time: O(n²).** For each of the n sample instants, all n meetings are tested for "
 "containment.\n\n"
 "**Space: O(1).** Nothing is stored beyond counters.\n\n"
 "Note that this is a genuinely better brute force than sampling every minute of the day, which "
 "would be O(n · T) and would break entirely if the times were not small integers.",
"brute_code":
'''def minMeetingRooms_brute(intervals):
    """Concurrency can only rise at a start time, so sample at the n starts.
    O(n^2), O(1) space."""
    if not intervals:
        return 0
    best = 0
    for i in range(len(intervals)):
        t = intervals[i][0]               # sample instant: when meeting i begins
        count = 0
        for j in range(len(intervals)):
            # `< end` (not <=): a meeting ending at t frees the room at t
            if intervals[j][0] <= t < intervals[j][1]:
                count += 1
        best = max(best, count)
    return best''',
"brute_limit":
 "Every sample instant re-examines all n meetings from scratch, even though moving from one "
 "start time to the next changes the set of in-progress meetings by only a handful of entries "
 "&mdash; one meeting begins, and some number end.\n\n"
 "Both optimal solutions exploit exactly that. Once the meetings are processed in "
 "chronological order, the running concurrency can be updated **incrementally**: add one when a "
 "meeting starts, subtract one when a meeting ends. All the redundant recounting disappears, "
 "and the only cost left is putting the events in time order, which is the sort.",
"opt_en":
 "**Way A, the min-heap of end times &mdash; present this one.** Sort the meetings by start "
 "time. Keep a min-heap holding the end times of the meetings currently occupying rooms; the "
 "heap's size is therefore the number of rooms in use, and its smallest element is the earliest "
 "moment any room becomes free. For each meeting in start order: if the heap is non-empty and "
 "its minimum end time is at or before this meeting's start, a room has freed up, so pop it. "
 "Then push this meeting's end time. The answer is the final heap size, which equals the "
 "maximum it ever reached, because a pop is always immediately followed by a push.\n\n"
 "**Way B, the sweep line &mdash; the elegant one.** Extract all start times into one sorted "
 "array and all end times into another, then decouple them entirely: the identity of which "
 "start belongs to which end is irrelevant to counting concurrency. Walk the two arrays "
 "together with two pointers. If the next start comes before the next end, a meeting is "
 "beginning, so increment the room count and record the new maximum. Otherwise a meeting is "
 "ending, so decrement. The maximum reached is the answer.\n\n"
 "Both are O(n log n). The heap generalises better if you also need to know *which* room each "
 "meeting was assigned to; the sweep line is easier to explain and has a smaller constant "
 "factor.",
"opt_ds":
 "- **Way A:** a **min-heap** of end times. A min-heap because the only question ever asked is "
 "\"what is the earliest a room becomes free?\", and that is precisely the operation a min-heap "
 "answers in O(1) with O(log n) removal.\n"
 "- **Way B:** two **sorted arrays**, one of starts and one of ends, plus two integer pointers "
 "and two counters. No heap at all.\n"
 "- Both require sorting, which is where the log factor comes from.",
"opt_algo": [
 "**Way A:** return 0 if the list is empty. Sort the meetings by start time.",
 "Create an empty min-heap. For each `[start, end]` in order:",
 "If the heap is non-empty and `heap[0] <= start`, the earliest-finishing meeting is already over, so pop it: that room is reusable.",
 "Push `end` onto the heap, occupying a room for this meeting.",
 "After all meetings, return `len(heap)` &mdash; the number of rooms in simultaneous use at the peak.",
 "**Way B:** build `starts` as the sorted list of all start times and `ends` as the sorted list of all end times.",
 "Set `rooms = 0`, `best = 0`, and two pointers `s = 0`, `e = 0`. While `s < len(starts)`: if `starts[s] < ends[e]`, a meeting begins, so increment `rooms`, update `best`, and advance `s`; otherwise a meeting ends, so decrement `rooms` and advance `e`.",
 "Return `best`.",
],
"opt_code":
'''import heapq

def minMeetingRooms(intervals):
    """WAY A -- min-heap of end times. Heap size == rooms currently in use."""
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])    # process meetings in start order
    heap = []                             # end times of ongoing meetings

    for start, end in intervals:
        # heap[0] is the EARLIEST end time == the soonest a room frees up.
        if heap and heap[0] <= start:
            heapq.heappop(heap)           # that room is free again -- reuse it
        heapq.heappush(heap, end)         # this meeting occupies a room

    return len(heap)                      # peak concurrency == rooms needed


def minMeetingRooms_sweep(intervals):
    """WAY B -- sweep line. Which start pairs with which end is irrelevant to
    counting how many meetings are simultaneously in progress."""
    if not intervals:
        return 0

    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)

    rooms = best = 0
    s = e = 0
    while s < len(starts):
        if starts[s] < ends[e]:           # a meeting begins before the next one ends
            rooms += 1
            best = max(best, rooms)
            s += 1
        else:                             # a meeting ends: free a room
            rooms -= 1
            e += 1
    return best''',
"opt_cx":
 "**Time: O(n log n)** for both. Way A sorts once and performs at most n pushes and n pops, "
 "each O(log n). Way B performs two sorts and then a single linear two-pointer sweep.\n\n"
 "**Space: O(n)** &mdash; the heap can hold every meeting when they all overlap; the sweep "
 "line stores two arrays of n elements.\n\n"
 "**Say this out loud:** \"The number of rooms is the maximum number of meetings in progress at "
 "once. I sort by start and keep a min-heap of end times, so the heap size is the rooms in use "
 "and the heap top is the soonest a room frees up. n pushes and pops at O(log n) each, plus "
 "the sort: O(n log n).\"\n\n"
 "**The related sorting rule, worth stating:** sort by **start** to merge intervals; sort by "
 "**end** to maximise how many non-overlapping intervals fit. Meeting Rooms I &mdash; can one "
 "person attend all meetings &mdash; is the same sort with a single adjacent-pair comparison.",
},

{
"num": 215, "title": "Kth Largest Element in an Array", "stars": "★", "day": DAY,
"pattern": "Min-heap of size k (alternative: Quickselect)",
"opt_cx_short": "O(n log k) time, O(k) space",
"clarify": [
 "Is this the kth largest **by value** or the kth **distinct** value? With `[3, 3, 2]` and `k = 2`, by value the answer is 3, distinct it would be 2. The standard problem means by value.",
 "Is `k` guaranteed to satisfy `1 <= k <= n`?",
 "May I modify or sort the input array? Quickselect partitions in place, so this matters if I choose that route.",
 "Is the data a fixed array, or is it **streaming**? If elements arrive over time, the heap is the only viable answer and Quickselect is not applicable &mdash; this is the follow-up they usually want.",
 "Are the values ordinary 32-bit integers, possibly with duplicates?",
],
"understand":
 "Return the kth largest element of an array, counting duplicates as separate elements.\n\n"
 "The observation that drives the efficient solution: **I do not need the array sorted.** I "
 "need one specific order statistic. Fully sorting produces n−1 pieces of ordering "
 "information when I only need one, and paying O(n log n) for that is over-solving the problem.\n\n"
 "The inversion that people find counter-intuitive and that is worth stating plainly: to keep "
 "track of the k **largest** elements, use a **min**-heap. The heap holds the k best "
 "candidates seen so far, and its root is the *weakest* of them &mdash; which is precisely the "
 "element to evict when a better one arrives, and, at the end, precisely the kth largest.",
"brute_en":
 "Find and remove the maximum, k times. Scan the array for the largest remaining value, mark it "
 "as used, and repeat. After k rounds, the last value found is the kth largest.\n\n"
 "The simpler alternative is to sort descending and index at `k - 1`, which is one line and "
 "O(n log n). Both are worth naming: the repeated-scan version is the true brute force, and the "
 "sort is the obvious-but-wasteful improvement that motivates the heap.",
"brute_ds":
 "- A copy of the array, or a `used` set of indices, so that removed maxima are not found "
 "again.\n"
 "- For the sort variant: whatever the sort allocates.",
"brute_algo": [
 "Make a working copy of the array so the input is not destroyed.",
 "Repeat `k` times: scan the whole copy tracking the index of the largest value.",
 "Record that value, then remove it from the copy, or mark its index as used.",
 "After `k` rounds, return the last value recorded.",
 "The one-line alternative: `return sorted(nums, reverse=True)[k - 1]`, which is O(n log n) and worth stating as the baseline you would improve on.",
],
"brute_cx":
 "**Time: O(n · k).** Each of the k rounds scans up to n elements. When k is close to n "
 "&mdash; the median, say &mdash; this is O(n²). The sorting variant is O(n log n), better "
 "for large k but still more than necessary.\n\n"
 "**Space: O(n)** for the working copy.",
"brute_code":
'''def findKthLargest_brute(nums, k):
    """Remove the maximum k times. O(n*k)."""
    arr = list(nums)                      # work on a copy
    value = None
    for _ in range(k):
        best_i = 0
        for i in range(1, len(arr)):      # full scan for the current maximum
            if arr[i] > arr[best_i]:
                best_i = i
        value = arr.pop(best_i)           # remove it so it is not found again
    return value


def findKthLargest_sort(nums, k):
    """The obvious baseline: O(n log n), computing far more order information
    than the question actually asks for."""
    return sorted(nums, reverse=True)[k - 1]''',
"brute_limit":
 "The repeated-scan version re-examines the entire array on every round, having learned nothing "
 "from the previous rounds. The sorting version has the opposite problem: it computes the "
 "complete ordering of all n elements when only a single order statistic was requested, and "
 "most of that work is discarded.\n\n"
 "The right frame is that this is a **top-K** question, and top-K questions never need the "
 "whole ordering. They need a bounded structure that holds only the k best candidates seen so "
 "far and can cheaply identify and evict the weakest of them. That structure is a heap of size "
 "k, and bounding the heap at k is what turns log n into log k.",
"opt_en":
 "Maintain a **min-heap containing at most k elements**, holding the k largest values seen so "
 "far. Push each element of the array. Whenever the heap grows past size k, pop the root, which "
 "is the smallest element in the heap and therefore the weakest candidate &mdash; it cannot be "
 "among the k largest overall if k better ones exist. After the whole array is processed, the "
 "heap contains exactly the k largest elements, and its root is the smallest of those, which is "
 "the kth largest overall.\n\n"
 "The push-then-pop ordering keeps the code to three lines and is correct: pushing first "
 "temporarily makes the heap size k+1, and popping the minimum then discards whichever element "
 "&mdash; possibly the one just pushed &mdash; is genuinely the weakest.\n\n"
 "The alternative to name is **Quickselect**: partition the array around a pivot as in "
 "quicksort, but recurse into only the side containing the target position. That gives O(n) "
 "average time, with an O(n²) worst case that randomising the pivot makes vanishingly "
 "unlikely. Quickselect is faster on a fixed in-memory array; the heap is the right answer when "
 "the data streams, because it never needs to see all n elements at once.",
"opt_ds":
 "- A **min-heap bounded at size k**. Min, not max, because the operation performed constantly "
 "is \"evict the weakest of my current best k\", and a min-heap exposes that element at its "
 "root in O(1). Bounded at k, because that is what makes each operation O(log k) rather than "
 "O(log n) and the space O(k) rather than O(n).\n"
 "- Python's `heapq` is a min-heap natively, which is exactly what is wanted here &mdash; no "
 "negation tricks required.",
"opt_algo": [
 "Create an empty heap.",
 "For each value `x` in the array: push `x` onto the heap.",
 "If the heap size now exceeds `k`, pop the root. The root is the smallest element currently held, so discarding it keeps the k largest seen so far.",
 "After processing every element, the heap holds exactly the k largest values.",
 "Return `heap[0]`, the smallest element of that set, which is the kth largest overall.",
 "The library shortcut to mention: `heapq.nlargest(k, nums)[-1]`, which does the same thing internally.",
],
"opt_code":
'''import heapq

def findKthLargest(nums, k):
    """Min-heap of size k. The root is the weakest of the current best k,
    so at the end it IS the kth largest."""
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)              # evict the SMALLEST -> keeps the k largest
    return h[0]                           # smallest of the k largest


import random

def findKthLargest_quickselect(nums, k):
    """O(n) average. Partition like quicksort, but recurse into ONE side only."""
    arr = list(nums)
    target = len(arr) - k                 # kth largest == index (n-k) when sorted asc
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        pivot_i = random.randint(lo, hi)  # randomise to dodge the O(n^2) worst case
        arr[pivot_i], arr[hi] = arr[hi], arr[pivot_i]
        pivot = arr[hi]

        store = lo
        for i in range(lo, hi):           # everything < pivot moves to the left
            if arr[i] < pivot:
                arr[i], arr[store] = arr[store], arr[i]
                store += 1
        arr[store], arr[hi] = arr[hi], arr[store]   # pivot lands at its final index

        if store == target:
            return arr[store]
        elif store < target:
            lo = store + 1                # recurse right only
        else:
            hi = store - 1                # recurse left only''',
"opt_cx":
 "**Time: O(n log k).** Each of the n elements causes one push and possibly one pop, and every "
 "heap operation on a heap of size k costs O(log k). When k is small this is effectively "
 "linear, and it is strictly better than the O(n log n) sort.\n\n"
 "**Space: O(k)** &mdash; the heap never exceeds k+1 elements.\n\n"
 "**Quickselect:** O(n) average, O(n²) worst case, O(1) extra space if partitioning in "
 "place. The average case comes from the recurrence T(n) = T(n/2) + O(n), which sums to 2n.\n\n"
 "**Say this out loud:** \"A min-heap of size k for the k *largest* &mdash; the root is the "
 "weakest of my current best, so it is the one to evict, and at the end it is the answer. n "
 "operations at O(log k) each. Sorting would be O(n log n) and computes far more than I need; "
 "Quickselect is O(n) average but needs the whole array in memory, so the heap is the right "
 "answer if the data is streaming.\"\n\n"
 "**The rule to memorise:** K largest ⇒ **min**-heap of size K. K smallest ⇒ **max**-heap "
 "of size K.",
},

{
"num": 973, "title": "K Closest Points to Origin", "stars": "★  Amazon favourite", "day": DAY,
"pattern": "Max-heap of size k by distance (alternative: Quickselect)",
"opt_cx_short": "O(n log k) time, O(k) space",
"clarify": [
 "Distance is the Euclidean distance from the origin, so `sqrt(x² + y²)`? I will note immediately that I can skip the square root, since it is monotonic and I only ever compare distances.",
 "If several points tie at the same distance, may I return any of them?",
 "Does the output order matter, or is any order of the k closest acceptable?",
 "Is `k` guaranteed to be at most the number of points?",
 "Can coordinates be negative or zero? Squaring handles both, so it makes no difference to the method.",
],
"understand":
 "Given a list of points on a plane and an integer `k`, return the `k` points closest to the "
 "origin.\n\n"
 "This is the same top-K shape as problem 215, with two differences worth naming. First, the "
 "ordering key is a **computed** value rather than the element itself, so I choose the "
 "comparison function. Second, the direction is inverted: I want the k **smallest** distances, "
 "so by the top-K rule I need a **max**-heap of size k, whose root is the *worst* of my current "
 "best and therefore the one to evict.\n\n"
 "The small optimisation that interviewers listen for: comparing `sqrt(x² + y²)` and "
 "comparing `x² + y²` produce identical orderings, because the square root is monotonically "
 "increasing on non-negative inputs. So I skip the square root entirely &mdash; it saves n "
 "floating-point operations and avoids any precision issues in the comparisons.",
"brute_en":
 "Compute the squared distance for every point, sort the points by that value, and return the "
 "first k. Alternatively, and more literally brute-force: scan the whole list k times, each "
 "time finding and removing the point with the smallest remaining distance.\n\n"
 "The sort version is one line and gets the right answer; it is the natural baseline. The "
 "repeated-scan version is what you would write with no data structures at all, and it is worth "
 "having in mind because its cost, O(n·k), is what the heap improves on when k is large.",
"brute_ds":
 "- A list of `(distance, point)` pairs, or a working copy of the points list.\n"
 "- No heap. The sort does all the work.",
"brute_algo": [
 "For each point `(x, y)`, compute `d = x*x + y*y`, skipping the square root because it does not change the ordering.",
 "Sort the points by `d` ascending.",
 "Return the first `k` points of the sorted list.",
 "The repeated-scan variant: repeat k times &mdash; scan all remaining points for the minimum `d`, append that point to the output, and remove it from the working list.",
],
"brute_cx":
 "**Time: O(n log n)** for the sort version, dominated entirely by sorting; O(n · k) for the "
 "repeated-scan version, which degrades to O(n²) when k is proportional to n.\n\n"
 "**Space: O(n)** to hold the distances or the working copy.",
"brute_code":
'''def kClosest_brute(points, k):
    """Sort everything by squared distance, take the first k. O(n log n)."""
    # No sqrt: it is monotonic, so it never changes the ordering.
    return sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])[:k]


def kClosest_scan(points, k):
    """The true brute force: find the closest remaining point, k times. O(n*k)."""
    remaining = list(points)
    out = []
    for _ in range(k):
        best_i = 0
        for i in range(1, len(remaining)):
            di = remaining[i][0] ** 2 + remaining[i][1] ** 2
            db = remaining[best_i][0] ** 2 + remaining[best_i][1] ** 2
            if di < db:
                best_i = i
        out.append(remaining.pop(best_i))
    return out''',
"brute_limit":
 "Sorting orders all n points when only the k smallest are wanted, and the relative order among "
 "the n−k discarded points is computed and then thrown away. The repeated-scan version has "
 "the opposite failing: it never accumulates information, so every round starts over.\n\n"
 "The correct framing is again top-K: I only ever need to hold k candidates and to know which "
 "of them is currently the worst, so that an incoming better point can displace it. That is a "
 "size-k heap, and bounding it at k reduces both the per-operation cost to O(log k) and the "
 "memory to O(k) &mdash; which also means the algorithm works when the points arrive as a "
 "stream too large to store.",
"opt_en":
 "Maintain a **max-heap of size k** keyed on squared distance. Python's `heapq` only provides a "
 "min-heap, so I obtain max-heap behaviour by pushing the **negated** distance: the largest "
 "true distance becomes the smallest stored value and therefore sits at the root.\n\n"
 "For each point, compute `d = x*x + y*y` and push `(-d, x, y)`. If the heap then exceeds size "
 "k, pop the root, which is the point with the **largest** true distance among the candidates "
 "&mdash; the worst one, correctly discarded. After every point is processed, the heap holds "
 "exactly the k closest, and I strip out the coordinates.\n\n"
 "Two details worth narrating. Skipping the square root is safe because it is monotonic. And "
 "storing `x` and `y` inside the tuple means comparisons fall through to them when two "
 "distances tie, which is harmless for integers &mdash; but with unorderable payloads it would "
 "raise a TypeError, exactly the trap that problem 23 turns on.\n\n"
 "As with 215, **Quickselect** is the O(n)-average alternative: partition on squared distance "
 "until the pivot lands at index k, at which point the first k entries are the answer in any "
 "order.",
"opt_ds":
 "- A **max-heap of size k**, simulated with `heapq` by negating the key. Max, not min, because "
 "I am collecting the k *smallest* distances and therefore need instant access to the largest "
 "one I am currently holding.\n"
 "- Tuples of `(-d, x, y)` so the heap orders by distance while carrying the point with it.\n"
 "- Squared distance as the key, never the square root.",
"opt_algo": [
 "Create an empty heap.",
 "For each point `(x, y)`: compute `d = x*x + y*y`.",
 "Push the tuple `(-d, x, y)`. Negating turns the min-heap into a max-heap on true distance.",
 "If the heap size now exceeds `k`, pop the root, which holds the largest true distance and is therefore the worst current candidate.",
 "After all points, the heap holds the k closest. Return `[[x, y] for _, x, y in heap]`.",
 "Mention the alternative: `heapq.nsmallest(k, points, key=...)`, and Quickselect for O(n) average time.",
],
"opt_code":
'''import heapq

def kClosest(points, k):
    """Max-heap of size k, keyed on NEGATED squared distance."""
    heap = []
    for x, y in points:
        d = x * x + y * y                 # no sqrt: monotonic, so ordering is identical
        heapq.heappush(heap, (-d, x, y))  # negate -> heapq's min-heap acts as a max-heap
        if len(heap) > k:
            heapq.heappop(heap)           # evict the FARTHEST of the current candidates
    return [[x, y] for _, x, y in heap]   # the k closest, in arbitrary order''',
"opt_cx":
 "**Time: O(n log k).** One push and at most one pop per point, each O(log k) on a heap "
 "bounded at k.\n\n"
 "**Space: O(k)** for the heap, plus the output.\n\n"
 "**Say this out loud:** \"Top-K, so a heap of size k rather than a full sort. I want the k "
 "smallest distances, so it is a max-heap: its root is the farthest point I am currently "
 "keeping, which is exactly what a closer point should displace. And I compare squared "
 "distances, because the square root is monotonic and changes nothing about the ordering.\"\n\n"
 "**The two things to volunteer:** skipping `sqrt`, and Quickselect as the O(n)-average "
 "alternative. **The follow-up:** if the points arrive as an unbounded stream, the heap is the "
 "only workable answer, since Quickselect requires random access to the entire dataset.",
},

{
"num": 23, "title": "Merge k Sorted Lists", "stars": "★★", "day": DAY,
"pattern": "Min-heap of list heads (alternative: divide and conquer)",
"opt_cx_short": "O(N log k) time, O(k) space",
"clarify": [
 "Each of the `k` lists is individually sorted ascending, and the output must be one sorted list?",
 "Can the input array contain **empty lists**, or be empty itself? Both need guarding, and a null head pushed into a heap is a crash.",
 "Should I **reuse the existing nodes** by relinking them, or allocate new ones? Relinking is O(1) extra per node and is what I will do.",
 "Roughly what are `k` and the total number of nodes `N`? That determines whether O(N log k) beats the alternatives.",
 "Can the values repeat across lists? Yes, and that is precisely why I need a tiebreaker in the heap tuple.",
],
"understand":
 "Given `k` sorted linked lists, merge them into one sorted linked list.\n\n"
 "The structural insight: at every step, the next node of the output must be the smallest among "
 "the **current heads** of the k lists. Nothing deeper in any list can be smaller than its own "
 "head, since each list is already sorted. So the whole problem reduces to repeatedly answering "
 "\"which of these k candidates is smallest?\", after which that list's head advances by one.\n\n"
 "\"Repeatedly extract the minimum from a small changing set\" is the textbook definition of a "
 "min-heap. Bounding the heap at k rather than N is what makes this O(N log k) instead of "
 "O(N log N).",
"brute_en":
 "Two natural brute forces, and both are worth naming.\n\n"
 "The first is **collect and sort**: walk every list, dump all N values into one array, sort it, "
 "and build a fresh linked list from the sorted values. Simple and reliable, but it discards the "
 "fact that the inputs were already sorted, which is the entire structure the problem hands you.\n\n"
 "The second is **repeated linear scan**: keep the k current heads in an array, and on each "
 "step scan all k of them to find the smallest, append it, and advance that pointer. This does "
 "use the sortedness, but it re-scans all k heads for every one of the N output nodes.",
"brute_ds":
 "- Collect-and-sort: an array of all N values, plus newly allocated nodes.\n"
 "- Repeated scan: an array of the k current head pointers.",
"brute_algo": [
 "**Collect and sort:** traverse every list, appending each node's value to one array.",
 "Sort the array ascending.",
 "Build a new linked list from the sorted values using a dummy head, and return `dummy.next`.",
 "**Repeated scan:** copy the k head pointers into an array.",
 "Repeat until every pointer is null: scan the array for the index holding the smallest non-null value, append that node to the output tail, and advance that entry to `node.next`.",
],
"brute_cx":
 "**Collect and sort: O(N log N) time, O(N) space** for the value array and the new nodes. The "
 "log N factor comes from sorting data that was already largely ordered.\n\n"
 "**Repeated scan: O(N · k) time, O(k) space.** Each of the N output nodes costs a linear "
 "scan over k heads. With k = 10,000 lists this becomes hopeless, and it is the version the "
 "heap directly improves.",
"brute_code":
'''def mergeKLists_collect(lists):
    """Brute force 1 -- dump every value, sort, rebuild. O(N log N), O(N) space.
    Throws away the fact that the inputs were already sorted."""
    values = []
    for node in lists:
        while node:
            values.append(node.val)
            node = node.next
    values.sort()

    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)           # allocates N new nodes
        tail = tail.next
    return dummy.next


def mergeKLists_scan(lists):
    """Brute force 2 -- scan all k heads for the minimum, N times. O(N*k)."""
    heads = list(lists)
    dummy = ListNode()
    tail = dummy
    while True:
        best_i = -1
        for i, node in enumerate(heads):
            if node and (best_i == -1 or node.val < heads[best_i].val):
                best_i = i
        if best_i == -1:
            break                         # every list exhausted
        tail.next = heads[best_i]         # relink, no allocation
        tail = tail.next
        heads[best_i] = heads[best_i].next
    return dummy.next''',
"brute_limit":
 "Collect-and-sort ignores the input structure entirely: the lists were already sorted, and "
 "re-sorting from scratch pays a log N factor for information that was handed to you for free. "
 "It also allocates N new nodes and holds all N values in memory at once, which rules it out if "
 "the lists are huge or streaming.\n\n"
 "Repeated scan uses the sortedness but re-derives the same comparison over and over: after "
 "taking the minimum, k−1 of the k heads are completely unchanged, yet all k are compared "
 "again on the next step.\n\n"
 "A min-heap fixes exactly that. It remembers the ordering among the k candidates, so replacing "
 "one candidate costs O(log k) rather than a fresh O(k) scan &mdash; and the heap holds only k "
 "entries, so memory stays proportional to the number of lists, not the number of nodes.",
"opt_en":
 "Push the head of every non-empty list into a min-heap. Then repeatedly pop the smallest node, "
 "append it to the output tail, and &mdash; if that node has a successor &mdash; push the "
 "successor. The heap therefore always holds exactly one candidate per still-live list, at most "
 "k entries.\n\n"
 "The detail that makes or breaks the implementation: the heap entries must be **tuples of "
 "`(value, index, node)`**. Python compares tuples element by element, so when two nodes have "
 "equal values it moves on to the next component. Without a tiebreaker it would reach the "
 "`ListNode` objects and raise `TypeError: '<' not supported between instances of 'ListNode'`. "
 "Inserting the list index as a second component guarantees the comparison always resolves on "
 "an integer and never touches the node. This is the single most common crash in this problem, "
 "so I would state it while typing the tuple.\n\n"
 "A **dummy head** node removes every special case around the first append: the tail pointer "
 "always has somewhere to write, and the real result is `dummy.next`.\n\n"
 "The alternative to mention is **divide and conquer**: merge the lists pairwise, halving the "
 "number of lists on each round, for log k rounds each costing O(N). Same O(N log k) time, but "
 "O(1) extra space instead of O(k), and no comparison-tiebreaker issue at all.",
"opt_ds":
 "- A **min-heap holding at most k entries**, one per live list. Bounded at k, which is why the "
 "log factor is log k and not log N.\n"
 "- **Tuples `(value, list_index, node)`** &mdash; the middle element is a pure tiebreaker to "
 "keep Python from comparing nodes.\n"
 "- A **dummy head** node plus a moving `tail` pointer, so no branch is needed for the first "
 "element.",
"opt_algo": [
 "Create an empty heap. For each list index `i` with a non-null head, push `(head.val, i, head)`. Skipping null heads is essential; pushing `None` crashes on the first comparison.",
 "Create `dummy = ListNode()` and set `tail = dummy`.",
 "While the heap is non-empty: pop `(value, i, node)`, the globally smallest current head.",
 "Link it in: `tail.next = node`, then `tail = node`. This relinks the existing node rather than allocating a new one.",
 "If `node.next` is not null, push `(node.next.val, i, node.next)`, replacing the list's candidate.",
 "When the heap empties, return `dummy.next`.",
 "Optionally set `tail.next = None` at the end for hygiene; here it is already correct because the final popped node was the tail of its own list.",
],
"opt_code":
'''import heapq

def mergeKLists(lists):
    """Min-heap holding one candidate per live list: at most k entries."""
    heap = []
    for i, node in enumerate(lists):
        if node:                          # never push a null head
            # *** i is a TIEBREAKER. Without it, equal values make Python compare
            # ListNode objects -> TypeError: '<' not supported. ***
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()                    # dummy head: no special case for the first node
    tail = dummy

    while heap:
        _, i, node = heapq.heappop(heap)  # globally smallest current head
        tail.next = node                  # relink the existing node (no allocation)
        tail = node
        if node.next:                     # refill this list's candidate slot
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next


def mergeKLists_divide(lists):
    """Alternative -- pairwise merge, halving the list count each round.
    Same O(N log k) time, but O(1) extra space and no tiebreaker needed."""
    def merge_two(a, b):
        dummy = ListNode()
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b                # attach whatever remains
        return dummy.next

    if not lists:
        return None
    while len(lists) > 1:                 # log k rounds, each O(N) total
        merged = []
        for i in range(0, len(lists), 2):
            second = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(lists[i], second))
        lists = merged
    return lists[0]''',
"opt_cx":
 "**Time: O(N log k)** where N is the total number of nodes. Each node is pushed once and "
 "popped once, and every heap operation costs O(log k) because the heap never exceeds k "
 "entries.\n\n"
 "**Space: O(k)** for the heap. The output reuses the input nodes, so no extra node allocation "
 "&mdash; unlike collect-and-sort, which allocates N.\n\n"
 "**Say this out loud:** \"The next output node is always the smallest of the k current heads, "
 "so this is repeated extract-min over a set of size k, which is exactly a min-heap. Each of "
 "the N nodes enters and leaves the heap once at O(log k), so O(N log k) time and O(k) space.\"\n\n"
 "**The gotcha to volunteer:** the index tiebreaker in the tuple, and why &mdash; equal values "
 "would otherwise force Python to compare `ListNode` objects and raise `TypeError`. **The "
 "alternative answer:** divide-and-conquer pairwise merging, same time bound, O(1) extra space.",
},

{
"num": 621, "title": "Task Scheduler", "stars": "★  Amazon favourite", "day": DAY,
"pattern": "Greedy counting / closed-form arithmetic",
"opt_cx_short": "O(n) time, O(26) space",
"clarify": [
 "The cooldown `n` is the number of intervals that must separate two runs of the **same** task, so identical tasks must be at least `n + 1` apart?",
 "May the CPU sit **idle**, and does each idle slot count as one unit of time? Yes on both, and that is what the answer is measuring.",
 "Are tasks always uppercase letters A&ndash;Z? That is what bounds the counting space at 26.",
 "Do I return only the total time, or the actual schedule? The formula gives the total; producing a schedule needs a different, simulation-based approach, so I want to know before I choose.",
 "Can `n` be 0? Then no cooldown applies and the answer is simply the number of tasks &mdash; a good check that my formula degrades correctly.",
],
"understand":
 "Given a list of tasks and a cooldown `n`, each unit of time the CPU runs one task or idles, "
 "and two identical tasks must be separated by at least `n` units. Return the least total time "
 "needed.\n\n"
 "The insight that removes all simulation: the answer is dictated entirely by the **most "
 "frequent** task. If task A occurs `max_freq` times, those occurrences must be spread out, "
 "creating a rigid skeleton of `max_freq - 1` blocks each of width `n + 1` &mdash; one slot for "
 "A and `n` slots of cooldown &mdash; followed by a final A. Every other task simply fills the "
 "cooldown slots inside that skeleton.\n\n"
 "It is worth drawing this on the whiteboard: a grid with `max_freq` rows and `n + 1` columns, "
 "the first column entirely A's, and the remaining cells filled with other tasks or left idle.",
"brute_en":
 "Simulate the clock one time unit at a time, greedily. Keep the remaining count of each task "
 "and the next time at which each task becomes legal again. At each tick, among the tasks that "
 "still have work left and are off cooldown, run the one with the **highest remaining count**; "
 "if none is available, idle. Either way advance the clock by one.\n\n"
 "The greedy choice of \"most remaining first\" is correct because the task with the most "
 "remaining occurrences is the most constrained &mdash; delaying it can only force idle slots "
 "later &mdash; so scheduling it as early as legally possible is never worse.",
"brute_ds":
 "- A **counter** of remaining occurrences per task.\n"
 "- A map from task to the next time it is allowed to run again.\n"
 "- An integer clock. Alternatively a max-heap of remaining counts plus a cooldown queue, which "
 "is the more idiomatic simulation and is still slower than the formula.",
"brute_algo": [
 "Build `remaining`, a counter of how many times each task must still run, and `available_at`, a map from task to the earliest legal time, initialised to 0.",
 "Set `time = 0` and `left` to the total number of tasks.",
 "While `left > 0`: among all tasks with `remaining > 0` and `available_at <= time`, choose the one with the largest `remaining`.",
 "If such a task exists, decrement its `remaining`, set its `available_at` to `time + n + 1`, and decrement `left`.",
 "If none exists, the CPU idles for this tick.",
 "Increment `time` and repeat.",
 "Return `time`.",
],
"brute_cx":
 "**Time: O(T · 26)** where T is the final answer, the total number of time units. Each "
 "tick scans the 26 possible tasks to pick the best available one. Since T can be roughly "
 "`n × max_freq`, and `n` may be large while the task list is short, this can be far larger "
 "than the input &mdash; it is output-sensitive rather than input-sensitive, which is the "
 "warning sign.\n\n"
 "**Space: O(26) = O(1)** for the two maps.",
"brute_code":
'''from collections import Counter

def leastInterval_brute(tasks, n):
    """Greedy tick-by-tick simulation: always run the task with the most
    remaining occurrences that is currently off cooldown."""
    remaining = Counter(tasks)
    available_at = {t: 0 for t in remaining}
    time = 0
    left = len(tasks)

    while left > 0:
        pick = None
        for t, cnt in remaining.items():
            if cnt > 0 and available_at[t] <= time:
                # most-remaining-first: the most constrained task goes earliest
                if pick is None or cnt > remaining[pick]:
                    pick = t
        if pick is not None:
            remaining[pick] -= 1
            available_at[pick] = time + n + 1   # cooldown before it may run again
            left -= 1
        # else: the CPU idles for this tick
        time += 1

    return time''',
"brute_limit":
 "The simulation's running time is proportional to the **answer**, not to the input. With "
 "`tasks = ['A', 'B']` and `n = 10⁶`, the input has two elements but the loop runs a "
 "million times. Any algorithm whose cost scales with the output value rather than the input "
 "size is a red flag in an interview.\n\n"
 "And the simulation is unnecessary, because the structure of the optimal schedule is fully "
 "determined in advance by the frequency counts. The most frequent task fixes the skeleton, and "
 "every other task either fits into the gaps or overflows them. Both cases can be evaluated "
 "with arithmetic in constant time once the counts are known.",
"opt_en":
 "Count the task frequencies. Let `max_freq` be the highest, and `num_max` the number of tasks "
 "achieving it.\n\n"
 "The most frequent task creates `max_freq - 1` gaps, each of which must be `n + 1` units wide "
 "&mdash; one slot for the task itself and `n` for its cooldown. That accounts for "
 "`(max_freq - 1) × (n + 1)` units. Then the final round must contain one slot for each task "
 "tied at the maximum frequency, adding `num_max`. So the skeleton has length "
 "`(max_freq - 1) * (n + 1) + num_max`.\n\n"
 "But that formula assumes the cooldown gaps have empty space to spare. If there are many "
 "distinct tasks, they fill every gap and then some, and the CPU never idles at all &mdash; in "
 "which case the answer is simply the total number of tasks. The two cases are unified by "
 "taking the maximum: `max(skeleton, len(tasks))`.\n\n"
 "That clamp is the part people miss, and it is where the whole solution is verified or broken. "
 "The formula can never *undercount*, because the skeleton is a genuine lower bound; and it can "
 "never *overcount*, because whenever extra tasks exist they land in idle slots that were "
 "already paid for.",
"opt_ds":
 "- A **`Counter`** over at most 26 tasks. Nothing else &mdash; no heap, no queue, no clock.\n"
 "- Two integers derived from it: `max_freq` and `num_max`.\n"
 "- The realisation that the answer depends only on those two numbers plus `len(tasks)`, not on "
 "the arrangement, is the entire optimisation.",
"opt_algo": [
 "Build `count = Counter(tasks)`.",
 "Let `max_freq = max(count.values())`, the highest frequency.",
 "Let `num_max` be the number of distinct tasks whose count equals `max_freq`.",
 "Compute `slots = (max_freq - 1) * (n + 1) + num_max`. The first term is the `max_freq - 1` full blocks of width `n + 1`; the second is the final partial round holding one slot per maximum-frequency task.",
 "Return `max(slots, len(tasks))`. The clamp handles the case where there is enough task variety that every cooldown gap is filled and no idling is ever required.",
 "On the whiteboard, draw a grid with `max_freq` rows and `n + 1` columns to make the derivation visible; it is far more convincing than stating the formula.",
],
"opt_code":
'''from collections import Counter

def leastInterval(tasks, n):
    """No simulation. The most frequent task fixes a rigid skeleton; every other
    task either fills the gaps or overflows them."""
    count = Counter(tasks)
    max_freq = max(count.values())                       # length of the tallest column
    num_max = sum(1 for v in count.values() if v == max_freq)   # ties at the top

    #   (max_freq - 1) full blocks, each (n + 1) wide  ... the cooldown skeleton
    # + num_max                                        ... the final partial round
    slots = (max_freq - 1) * (n + 1) + num_max

    # *** the clamp: with enough task variety, every gap is filled and the CPU
    # never idles, so the answer is just the number of tasks. ***
    return max(slots, len(tasks))''',
"opt_cx":
 "**Time: O(n)** where n is the number of tasks, spent building the counter. Everything after "
 "that is constant-time arithmetic over at most 26 counts.\n\n"
 "**Space: O(26) = O(1)** for the counter.\n\n"
 "**Say this out loud:** \"No simulation is needed. The most frequent task forces "
 "max_freq − 1 gaps of width n + 1, and the last round holds one slot per task tied at that "
 "frequency. That skeleton is a lower bound. If there is enough variety to fill every gap, "
 "there is no idling and the answer is just the number of tasks &mdash; hence the max. O(n) "
 "time, O(26) space.\"\n\n"
 "**The clamp `max(slots, len(tasks))` is what people miss.** Draw the grid: rows = max_freq, "
 "columns = n + 1. **The follow-up:** if the interviewer wants the actual schedule rather than "
 "its length, the formula does not suffice and you need the max-heap simulation &mdash; a "
 "max-heap of remaining counts plus a cooldown queue &mdash; which is worth naming.",
},

{
"num": 347, "title": "Top K Frequent Elements", "stars": "  (stretch)", "day": DAY,
"pattern": "Hash count + heap (O(n) follow-up: bucket sort)",
"opt_cx_short": "O(n log k) time, O(n) space",
"clarify": [
 "Is `k` guaranteed to be at most the number of **distinct** elements?",
 "If two elements tie in frequency at the boundary, may I return either one?",
 "Does the output order matter, or is any order of the k most frequent acceptable?",
 "Are the values arbitrary integers? Hashing handles that, but it rules out an array-indexed count.",
 "Is an O(n log k) solution acceptable, or do you want the strict O(n)? I have the bucket-sort version ready either way &mdash; it is the standard follow-up.",
],
"understand":
 "Given an integer array and an integer `k`, return the `k` most frequent elements.\n\n"
 "This decomposes cleanly into two independent steps. **Step one:** compute the frequency of "
 "each distinct value, which a hash map does in one linear pass. **Step two:** select the k "
 "largest by that frequency, which is a top-K problem exactly like 215 and 973.\n\n"
 "Keeping the two steps separate is the clean way to present it, because it makes obvious that "
 "only the second step has any room for optimisation &mdash; and that the second step is where "
 "the O(n) follow-up lives.",
"brute_en":
 "Count without a hash map, then sort. For each distinct value in the array, scan the whole "
 "array counting its occurrences, producing a list of `(value, frequency)` pairs. Sort that "
 "list by frequency descending and return the first `k` values.\n\n"
 "The counting-by-rescanning is the genuinely brute-force part; the sort is the obvious "
 "baseline for the selection step. Naming both separately is useful, because the two get "
 "optimised by different techniques &mdash; hashing for the first, a heap or bucket sort for "
 "the second.",
"brute_ds":
 "- A list of `(value, frequency)` pairs.\n"
 "- A `seen` set so each distinct value is only counted once.",
"brute_algo": [
 "Create an empty `seen` set and an empty list of pairs.",
 "For each value `x` in the array: if `x` is already in `seen`, skip it.",
 "Otherwise add `x` to `seen`, scan the entire array counting occurrences of `x`, and append `(x, count)` to the list.",
 "Sort the list by frequency descending.",
 "Return the first `k` values from it.",
],
"brute_cx":
 "**Time: O(n · d)** where d is the number of distinct values, so **O(n²)** when most "
 "elements are distinct, plus O(d log d) for the sort.\n\n"
 "**Space: O(d)** for the pair list and the seen set.",
"brute_code":
'''def topKFrequent_brute(nums, k):
    """Count each distinct value by rescanning the array, then sort. O(n^2)."""
    seen = set()
    pairs = []
    for x in nums:
        if x in seen:
            continue
        seen.add(x)
        c = 0
        for y in nums:                    # a FULL rescan per distinct value
            if y == x:
                c += 1
        pairs.append((x, c))
    pairs.sort(key=lambda p: p[1], reverse=True)
    return [v for v, _ in pairs[:k]]''',
"brute_limit":
 "Two separate inefficiencies, worth separating because they have different fixes.\n\n"
 "The counting rescans the array once per distinct value, when a single pass with a hash map "
 "computes every count at once &mdash; the same membership-versus-scan trade as Two Sum.\n\n"
 "The selection fully sorts all d distinct values when only the top k are needed, computing "
 "and discarding the ordering of the other d−k. A size-k heap reduces that to O(d log k), "
 "and because the frequencies are bounded integers, bucket sort removes the log factor "
 "entirely.",
"opt_en":
 "**Step one:** one pass with a `Counter` gives every frequency in O(n).\n\n"
 "**Step two, the O(n log k) version:** feed the `(value, frequency)` pairs into a size-k heap "
 "keyed on frequency, exactly as in problem 215. `heapq.nlargest(k, count.items(), key=...)` "
 "does this in one line and is the idiomatic answer.\n\n"
 "**Step two, the O(n) follow-up &mdash; bucket sort.** This is what the interviewer is usually "
 "fishing for. A frequency can never exceed `n`, so create `n + 1` buckets indexed by "
 "frequency, and place each value into the bucket matching its count. Then walk the buckets "
 "from the highest index downward, collecting values until `k` have been gathered. There is no "
 "comparison sorting at all, so no log factor: the bounded key range is what makes it possible, "
 "the same way counting sort beats comparison sort when the key range is small.\n\n"
 "I would present the heap version as the main answer for its clarity, then immediately offer "
 "bucket sort as the linear-time follow-up.",
"opt_ds":
 "- A **`Counter`** from value to frequency, built in one pass.\n"
 "- Either a **size-k heap** over the counter's items, giving O(n log k);\n"
 "- or a **bucket array of length n + 1**, indexed by frequency, each cell holding the list of "
 "values with that exact frequency, giving O(n). Indexing by frequency is legal only because "
 "frequencies are integers bounded by n &mdash; that bound is the whole justification.",
"opt_algo": [
 "Build `count = Counter(nums)` in a single O(n) pass.",
 "**Heap version:** return `[value for value, freq in heapq.nlargest(k, count.items(), key=lambda p: p[1])]`.",
 "**Bucket version:** create `buckets` as a list of `n + 1` empty lists, indexed by frequency.",
 "For each `(value, freq)` in the counter, append `value` to `buckets[freq]`.",
 "Walk `freq` downward from `n` to `1`, appending every value in `buckets[freq]` to the output.",
 "Stop as soon as the output holds `k` values, and return it.",
],
"opt_code":
'''import heapq
from collections import Counter

def topKFrequent(nums, k):
    """O(n log k) -- count in one pass, then a size-k heap over the counts."""
    count = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, count.items(), key=lambda p: p[1])]


def topKFrequent_buckets(nums, k):
    """The O(n) follow-up -- bucket sort by frequency.
    Legal because a frequency is an integer in [1, n], so it can index an array."""
    count = Counter(nums)

    # buckets[f] = every value that occurs exactly f times
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in count.items():
        buckets[freq].append(value)

    out = []
    for freq in range(len(nums), 0, -1):  # walk from the highest frequency down
        for value in buckets[freq]:
            out.append(value)
            if len(out) == k:
                return out
    return out''',
"opt_cx":
 "**Heap version &mdash; time: O(n log k).** O(n) to count, then O(d log k) to select over d "
 "distinct values, and d ≤ n. **Space: O(n)** for the counter plus O(k) for the heap.\n\n"
 "**Bucket version &mdash; time: O(n).** O(n) to count, O(d) to distribute into buckets, and "
 "O(n) to walk them. **Space: O(n)** for the counter and the bucket array.\n\n"
 "**Say this out loud:** \"Two steps: count with a hash map in O(n), then select the top k. "
 "Sorting the counts is O(d log d) and computes more than I need; a size-k heap is O(d log k). "
 "But frequencies are integers bounded by n, so I can bucket by frequency and walk the buckets "
 "downward &mdash; that is O(n) with no comparisons at all.\"\n\n"
 "**Offer the bucket-sort follow-up without being asked.** The general principle is worth "
 "stating too: when sort keys are integers from a small bounded range, counting or bucket sort "
 "beats any comparison sort, because the O(n log n) comparison lower bound simply does not "
 "apply.",
},

{
"num": 295, "title": "Find Median from Data Stream", "stars": "★★  (stretch)", "day": DAY,
"pattern": "Two heaps balanced around the median",
"opt_cx_short": "addNum O(log n), findMedian O(1)",
"clarify": [
 "How often is `findMedian` called relative to `addNum`? If reads are far more frequent than writes, I would consider making writes more expensive to make reads O(1) &mdash; and the two-heap design happens to give O(1) reads anyway.",
 "Are the numbers integers or floats, and is the range bounded? A bounded small integer range would allow a counting-based solution instead.",
 "For an even count, the median is the average of the two middle values, returned as a float?",
 "Can `findMedian` be called before any number is added? I will assume it is only called on a non-empty stream, but I would guard it if not.",
 "Is the total volume bounded? If it is unbounded and enormous, an approximate quantile sketch such as t-digest is the real production answer &mdash; worth naming.",
],
"understand":
 "Design a structure supporting `addNum(x)` to insert a value into a stream, and `findMedian()` "
 "to return the median of everything inserted so far.\n\n"
 "The median only depends on the **middle** of the sorted order, so maintaining a full sorted "
 "sequence is more than the problem requires. What is actually needed is the boundary between "
 "the lower half and the upper half, and access to the one or two elements adjacent to that "
 "boundary.\n\n"
 "That leads directly to the design: split the data into two halves and keep each half in a "
 "heap oriented so that the elements nearest the boundary sit at the roots. The lower half goes "
 "in a **max**-heap, whose root is the largest small value; the upper half in a **min**-heap, "
 "whose root is the smallest large value. Those two roots are exactly the candidates for the "
 "median, so reading it is O(1).",
"brute_en":
 "Keep every number in a plain list. `addNum` appends in O(1). `findMedian` sorts the list and "
 "picks the middle element, or averages the two middle elements when the count is even.\n\n"
 "A slightly better variant keeps the list sorted at all times by binary-searching for the "
 "insertion position and inserting there &mdash; the search is O(log n) but the insertion "
 "itself shifts elements and costs O(n). That gives O(n) writes and O(1) reads, which is the "
 "mirror image of the sort-on-read version's O(1) writes and O(n log n) reads.",
"brute_ds":
 "- A single **list** of all values seen so far.\n"
 "- For the sorted variant, `bisect.insort`, which finds the position in O(log n) but still "
 "performs an O(n) memory move.",
"brute_algo": [
 "**Sort on read:** `addNum(x)` appends `x` to the list, O(1).",
 "`findMedian()` sorts a copy of the list, then returns the middle element if the length is odd, or the average of the two middle elements if it is even.",
 "**Keep sorted on write:** `addNum(x)` uses `bisect.insort` to place `x` at its sorted position, O(log n) to locate plus O(n) to shift.",
 "`findMedian()` indexes the middle directly in O(1).",
 "Both are correct; both make one operation linear or worse.",
],
"brute_cx":
 "**Sort on read:** `addNum` O(1), `findMedian` **O(n log n)**. Over m calls that is "
 "O(m · n log n), which collapses if the median is queried often.\n\n"
 "**Keep sorted on write:** `addNum` **O(n)** because of the element shifting, `findMedian` "
 "O(1).\n\n"
 "**Space: O(n)** for either, which is unavoidable since every value must be retained.",
"brute_code":
'''import bisect

class MedianFinder_brute:
    """Sort on every read. addNum O(1), findMedian O(n log n)."""
    def __init__(self):
        self.data = []

    def addNum(self, num):
        self.data.append(num)

    def findMedian(self):
        s = sorted(self.data)             # re-sorts the whole stream every call
        n = len(s)
        mid = n // 2
        return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


class MedianFinder_sorted:
    """Keep the list sorted on write. addNum O(n) (the shift), findMedian O(1)."""
    def __init__(self):
        self.data = []

    def addNum(self, num):
        bisect.insort(self.data, num)     # O(log n) search + O(n) memory move

    def findMedian(self):
        n = len(self.data)
        mid = n // 2
        return self.data[mid] if n % 2 else (self.data[mid - 1] + self.data[mid]) / 2''',
"brute_limit":
 "Sorting on read redoes the entire ordering for a single number that has not changed since the "
 "last query. Keeping the list sorted avoids that but pays an O(n) memory shift on every "
 "insert, since arrays cannot insert in the middle cheaply.\n\n"
 "Both are over-solving: they maintain the complete ordering of the stream when the query only "
 "ever concerns the middle. If I stop trying to order everything and instead just maintain "
 "the **partition** into a lower half and an upper half, each side only needs to expose the "
 "single element closest to the boundary &mdash; and \"give me the extreme element of this "
 "set, with O(log n) inserts\" is exactly a heap.",
"opt_en":
 "Keep two heaps. `small` is a **max-heap** holding the lower half, simulated in Python by "
 "storing negated values so `heapq`'s min-heap surfaces the largest one. `large` is a "
 "**min-heap** holding the upper half. Two invariants are maintained at all times: every "
 "element of `small` is at most every element of `large`, and `len(small)` equals `len(large)` "
 "or exceeds it by exactly one.\n\n"
 "The elegant part is how `addNum` enforces both invariants with no comparisons at all. Push "
 "the new value onto `small`; immediately pop `small`'s maximum and push it onto `large`. That "
 "second step guarantees the ordering invariant unconditionally, because whatever now sits at "
 "the top of `small` is by construction no larger than everything in `large`. But it may have "
 "left `large` one too big, so finally, if `len(large) > len(small)`, move `large`'s minimum "
 "back to `small`. Three heap operations, no branching on values.\n\n"
 "`findMedian` is then O(1). If `small` is larger, the total count is odd and the median is "
 "`small`'s root. Otherwise the counts are equal, the total is even, and the median is the "
 "average of the two roots.",
"opt_ds":
 "- A **max-heap `small`** for the lower half, implemented by negating values on push and "
 "negating again on read. Max-oriented so its root is the largest of the small values &mdash; "
 "the left-hand median candidate.\n"
 "- A **min-heap `large`** for the upper half, whose root is the smallest of the large values "
 "&mdash; the right-hand median candidate.\n"
 "- No other state. The two roots are always exactly the elements adjacent to the median "
 "boundary, which is what makes reads O(1).",
"opt_algo": [
 "In the constructor, create `small = []` as the negated max-heap and `large = []` as the min-heap.",
 "**addNum(num):** push `-num` onto `small`.",
 "Pop the root of `small`, negate it back, and push it onto `large`. This unconditionally restores the ordering invariant: the value moved is the largest of the lower half, so after the move nothing in `small` exceeds anything in `large`.",
 "If `len(large) > len(small)`, pop `large`'s minimum and push its negation onto `small`, restoring the size invariant. `small` therefore holds the extra element when the count is odd.",
 "**findMedian():** if `len(small) > len(large)`, the count is odd, so return `-small[0]`.",
 "Otherwise the count is even, so return `(-small[0] + large[0]) / 2`.",
],
"opt_code":
'''import heapq

class MedianFinder:
    """Two heaps straddling the median.
       small: MAX-heap (values negated) holding the lower half
       large: MIN-heap holding the upper half
    Invariants: max(small) <= min(large), and len(small) - len(large) is 0 or 1."""

    def __init__(self):
        self.small = []                   # max-heap via negation -- lower half
        self.large = []                   # min-heap             -- upper half

    def addNum(self, num):
        # 1. Always enter through `small`.
        heapq.heappush(self.small, -num)

        # 2. Move small's maximum into large. This restores the ORDERING invariant
        #    unconditionally -- no value comparison is needed anywhere.
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # 3. Step 2 may have made large too big; restore the SIZE invariant.
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]         # odd count: small holds the extra element
        return (-self.small[0] + self.large[0]) / 2   # even: average the two roots''',
"opt_cx":
 "**addNum: O(log n).** A constant number of heap pushes and pops, each O(log n).\n\n"
 "**findMedian: O(1).** Only the two roots are read; nothing is removed or reordered.\n\n"
 "**Space: O(n)**, since every value must be retained across the two heaps.\n\n"
 "**Say this out loud:** \"I keep the lower half in a max-heap and the upper half in a "
 "min-heap, balanced so their sizes differ by at most one. The two roots are exactly the "
 "elements next to the median, so reading it is O(1). On insert I always push into small, move "
 "small's max into large &mdash; which guarantees the ordering with no comparisons &mdash; then "
 "rebalance if large got too big. Three heap operations, so O(log n).\"\n\n"
 "**Explain the push-to-small-then-move-to-large dance explicitly**; it is the part that looks "
 "like a trick until you say why it works. **The follow-ups:** if all values are in a small "
 "bounded range such as 0 to 100, a counting array with a running scan is simpler and O(1) "
 "amortised; and if 99% of values fall in a known range, keep exact counts inside it and heaps "
 "only for the outliers.",
},

]
