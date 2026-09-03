# -*- coding: utf-8 -*-
"""Day 4 - Round Type D: justify the paradigm, and design-in-code."""

DAY = "Day 4 · Fri 28 Aug · Round Type D (justify the paradigm)"

PROBLEMS = [

{
"num": 875, "title": "Koko Eating Bananas", "stars": "★", "day": DAY,
"pattern": "Binary search on the answer", "opt_cx_short": "O(n log(max pile)) time, O(1) space",
"clarify": [
 "If Koko's speed is `k` and a pile has fewer than `k` bananas, does she finish that pile and stop for the hour, rather than moving on to the next pile? Yes &mdash; that is what makes the cost per pile `ceil(pile / k)` rather than a continuous division.",
 "Is `h` guaranteed to be at least the number of piles? If it were smaller the task would be impossible, since each pile takes at least one hour.",
 "Are the pile sizes and `h` positive integers?",
 "Must the eating speed be an integer? Yes, which is what makes the answer space a discrete range I can binary search.",
 "How large can the piles get? That sets the upper bound of my search range and therefore the log factor.",
],
"understand":
 "Koko eats bananas at some integer speed `k` per hour, finishing at most one pile each hour. "
 "Given the piles and a deadline of `h` hours, find the minimum `k` that lets her finish in "
 "time.\n\n"
 "This is the archetype of **binary search on the answer**, and the recognition rule is worth "
 "stating out loud whenever it appears: the problem asks for the *minimum* (or maximum) value "
 "of something such that a condition holds, and I can write an O(n) function that checks "
 "whether a specific candidate value works.\n\n"
 "The property that makes binary search valid is **monotonicity**: if speed `k` finishes in "
 "time, then every speed greater than `k` also finishes in time, because eating faster can "
 "never take more hours. So the feasibility function looks like `False, False, …, False, True, "
 "True, …, True` across the range of speeds, and I am searching for the boundary. That is "
 "exactly what binary search finds.",
"brute_en":
 "Try every candidate speed in increasing order, starting at 1 and going up to the largest "
 "pile, and return the first one that finishes within `h` hours.\n\n"
 "Two bounds are worth justifying aloud. Speed 1 is the slowest possible, so nothing below it "
 "needs testing. And a speed equal to the largest pile means every pile takes exactly one hour, "
 "which is the fastest the task can ever be completed &mdash; going faster changes nothing, "
 "since Koko cannot start a second pile within the same hour. So the answer always lies in "
 "`[1, max(piles)]`.\n\n"
 "Because feasibility is monotonic, the first speed that works is by definition the minimum, so "
 "returning immediately on the first success is correct.",
"brute_ds":
 "- None. A loop counter and a helper that computes the hours needed for a candidate speed.\n"
 "- The helper is the important artefact: it is exactly the `feasible()` function the optimal "
 "solution reuses unchanged.",
"brute_algo": [
 "Write `hours_needed(speed)`: sum `ceil(p / speed)` over all piles. Using `ceil` is what encodes the rule that a partly eaten pile still consumes a whole hour.",
 "Loop `speed` from 1 up to `max(piles)`.",
 "If `hours_needed(speed) <= h`, return `speed`.",
 "The loop is guaranteed to succeed at or before `max(piles)`, provided `h` is at least the number of piles.",
],
"brute_cx":
 "**Time: O(n · max(piles)).** Each candidate speed costs an O(n) pass over the piles, and "
 "in the worst case every speed from 1 up to the maximum pile is tried. With piles up to "
 "10⁹ this is completely infeasible.\n\n"
 "**Space: O(1).**",
"brute_code":
'''import math

def minEatingSpeed_brute(piles, h):
    """Try every speed from 1 upward. O(n * max(piles))."""
    def hours_needed(speed):
        # ceil: a partly eaten pile still costs a whole hour
        return sum(math.ceil(p / speed) for p in piles)

    for speed in range(1, max(piles) + 1):
        if hours_needed(speed) <= h:
            return speed              # monotonic, so the first hit is the minimum
    return max(piles)''',
"brute_limit":
 "The linear scan tests thousands of speeds that are obviously too slow, one at a time, when a "
 "single test already reveals which entire half of the range can be discarded. If speed 500 "
 "misses the deadline, every speed below 500 misses it too &mdash; and the scan learns nothing "
 "from that and simply tries 501 next.\n\n"
 "That is precisely the structure binary search exploits. Because feasibility is monotonic in "
 "the speed, one O(n) evaluation halves the remaining search space, so the number of "
 "evaluations drops from `max(piles)` to `log₂(max(piles))` &mdash; about 30 evaluations "
 "instead of a billion.",
"opt_en":
 "Binary search over the **answer space** `[1, max(piles)]` rather than over the array.\n\n"
 "Maintain `lo` and `hi` as the inclusive bounds of the range still containing the answer. At "
 "each step, test the midpoint. If `hours_needed(mid) <= h`, then `mid` is a feasible speed "
 "&mdash; but possibly not the smallest &mdash; so I keep it as a candidate and search the "
 "lower half by setting `hi = mid`. If it is infeasible, `mid` and everything below it are "
 "ruled out, so `lo = mid + 1`.\n\n"
 "I use the `while lo < hi` form with `hi = mid` rather than `hi = mid - 1`. This is the "
 "**lower-bound** template, and it is the one to memorise for every \"minimum X such that\" "
 "problem: it converges on the smallest feasible value and terminates with `lo == hi` pointing "
 "at the answer, with no post-loop adjustment and no risk of skipping past the boundary. "
 "Because `mid` is computed by flooring and `lo < hi`, `mid` is always strictly less than `hi`, "
 "so the range shrinks on every iteration and the loop cannot spin forever.\n\n"
 "The move that makes this look easy in the interview is to write `hours_needed` on the "
 "whiteboard **first**, before any binary search code. That establishes the feasibility "
 "predicate as the thing being searched over, and the search itself is then a template.",
"opt_ds":
 "- **No data structure at all.** Two integer bounds. The insight is about the *search space*, "
 "not about storage &mdash; which is exactly why it belongs in a round about justifying the "
 "paradigm.\n"
 "- The `feasible` helper, here `hours_needed(speed) <= h`, is the reusable component. Problems "
 "1011, Split Array Largest Sum, and Minimum Days to Make Bouquets are all the same search with "
 "a different predicate.",
"opt_algo": [
 "Define `hours_needed(speed)` as the sum of `ceil(p / speed)` over all piles. This is the O(n) feasibility check.",
 "Set `lo = 1`, the slowest possible speed, and `hi = max(piles)`, beyond which nothing improves because each pile already takes exactly one hour.",
 "While `lo < hi`: compute `mid = (lo + hi) // 2`.",
 "If `hours_needed(mid) <= h`, `mid` is feasible, so it may be the answer or the answer may be smaller: set `hi = mid`, keeping `mid` inside the range.",
 "Otherwise `mid` is too slow, and so is everything below it: set `lo = mid + 1`.",
 "When the loop ends, `lo == hi` and that value is the smallest feasible speed. Return `lo`.",
],
"opt_code":
'''import math

def minEatingSpeed(piles, h):
    """Binary search the ANSWER SPACE, not the array.
    Valid because feasibility is monotonic: faster is never slower."""

    def hours_needed(speed):
        """O(n) feasibility check -- write this on the board FIRST."""
        return sum(math.ceil(p / speed) for p in piles)

    lo, hi = 1, max(piles)   # lo: slowest possible. hi: 1 hour per pile, the fastest useful.

    # Lower-bound template: converges on the SMALLEST value that satisfies the predicate.
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:
            hi = mid              # feasible -> keep mid as a candidate, search lower
        else:
            lo = mid + 1          # too slow -> mid and everything below is impossible

    return lo                     # lo == hi == the minimum feasible speed''',
"opt_cx":
 "**Time: O(n · log(max(piles))).** The binary search performs O(log(max pile)) iterations "
 "&mdash; about 30 for values up to 10⁹ &mdash; and each iteration runs the O(n) "
 "feasibility check.\n\n"
 "**Space: O(1).** Two integers and the generator inside the sum.\n\n"
 "**Say this out loud:** \"The answer is an integer between 1 and max(piles), and feasibility "
 "is monotonic &mdash; if a speed works, every faster speed works. So I binary search the "
 "answer space, using an O(n) check for whether a given speed finishes in time. About 30 "
 "iterations of O(n) work: O(n log max).\"\n\n"
 "**The recognition rule to state explicitly:** the problem says \"minimum X such that…\" or "
 "\"maximum X such that…\", and I can write an O(n) `feasible(x)`. Naming the rule out loud is "
 "the fastest way to show you recognised the pattern rather than recalled a template.",
},

{
"num": 33, "title": "Search in Rotated Sorted Array", "stars": "★★", "day": DAY,
"pattern": "Modified binary search on a pivoted array",
"opt_cx_short": "O(log n) time, O(1) space",
"clarify": [
 "Are the values **distinct**? This matters a great deal: with duplicates the worst case degrades to O(n), because `nums[lo] == nums[mid]` no longer tells you which half is sorted. The standard version guarantees distinct values.",
 "Was the array originally sorted ascending and then rotated left by some unknown amount?",
 "Could the rotation be zero, leaving the array fully sorted? My solution must handle that as a normal case.",
 "I return the **index** of the target, or −1 if it is absent?",
 "Is O(log n) required, or would O(n) be acceptable? I will assume O(log n) is the point of the question.",
],
"understand":
 "A sorted ascending array of distinct integers has been rotated at an unknown pivot. Find the "
 "index of a target in O(log n).\n\n"
 "The key structural fact: **wherever you split a rotated sorted array at its midpoint, at "
 "least one of the two halves is itself properly sorted.** The pivot can only fall in one half, "
 "so the other half is a clean ascending run. That is what rescues binary search &mdash; I "
 "cannot compare the target against `nums[mid]` alone to decide direction, but I *can* identify "
 "the sorted half and then test, with two simple comparisons, whether the target lies inside "
 "its known range. If it does, search there; if it does not, the target must be in the other "
 "half.\n\n"
 "So each iteration still discards half the array, and the complexity is unchanged from ordinary "
 "binary search.",
"brute_en":
 "Scan the array from left to right, returning the index as soon as an element equals the "
 "target, and −1 if the scan completes without a match.\n\n"
 "This is worth one sentence, not more. Its only virtue is that it ignores the ordering "
 "entirely and therefore does not care about the rotation &mdash; which is precisely why it is "
 "the wrong answer here: the rotation is the structure the question is testing whether you can "
 "exploit.",
"brute_ds":
 "- None. One index variable.",
"brute_algo": [
 "Loop `i` from 0 to `n - 1`.",
 "If `nums[i] == target`, return `i`.",
 "If the loop finishes without a match, return −1.",
],
"brute_cx":
 "**Time: O(n).** Every element may be examined.\n\n"
 "**Space: O(1).**\n\n"
 "Correct but it throws away the sortedness completely, which is the entire point of the "
 "problem. Stating it takes ten seconds and establishes the baseline the O(log n) solution "
 "improves on.",
"brute_code":
'''def searchRotated_brute(nums, target):
    """Linear scan. Correct, but ignores the sortedness entirely."""
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1''',
"brute_limit":
 "A linear scan on sorted data is always leaving information unused: after a single comparison "
 "against the midpoint of a sorted array, half the elements can be excluded, and the scan "
 "exploits none of that.\n\n"
 "The rotation makes the standard comparison insufficient but not useless. It only breaks the "
 "*direction* decision, and that is repairable, because at any midpoint one side is guaranteed "
 "to be a clean sorted run whose bounds are known. Two comparisons against that run's endpoints "
 "restore a correct direction decision, and binary search proceeds as normal.",
"opt_en":
 "Standard binary search with an extra layer of reasoning at each step.\n\n"
 "Compute `mid`. If `nums[mid]` is the target, return immediately. Otherwise decide which half "
 "is sorted by comparing `nums[lo]` with `nums[mid]`:\n\n"
 "- If `nums[lo] <= nums[mid]`, the **left** half is sorted. The target is in it exactly when "
 "`nums[lo] <= target < nums[mid]`. If so, set `hi = mid - 1`; otherwise the target must be in "
 "the unsorted right half, so `lo = mid + 1`.\n"
 "- Otherwise the **right** half is sorted. The target is in it exactly when "
 "`nums[mid] < target <= nums[hi]`. If so, `lo = mid + 1`; otherwise `hi = mid - 1`.\n\n"
 "The comparison must be `nums[lo] <= nums[mid]`, with the `<=`. When the range narrows to two "
 "elements, `mid` equals `lo`, so `nums[lo] == nums[mid]`; with a strict `<` the code would "
 "wrongly conclude the right half is sorted and could search the wrong side. That single "
 "character is the classic bug in this problem.\n\n"
 "The range bounds are inclusive and the loop runs `while lo <= hi`, so a final single-element "
 "range is still examined before the loop exits with −1.",
"opt_ds":
 "- **No data structure.** Three integer indices: `lo`, `hi`, `mid`. Constant extra space.\n"
 "- The alternative worth naming: first binary search for the pivot &mdash; the index of the "
 "minimum &mdash; then binary search the appropriate sorted segment. Two clean searches instead "
 "of one clever one, same O(log n), and easier to reason about if the branching feels risky "
 "under pressure.",
"opt_algo": [
 "Set `lo = 0` and `hi = n - 1`, an inclusive range.",
 "While `lo <= hi`: compute `mid = (lo + hi) // 2`.",
 "If `nums[mid] == target`, return `mid`.",
 "If `nums[lo] <= nums[mid]`, the left half is sorted. Note the `<=` &mdash; it is required for the two-element case where `mid == lo`.",
 "Within that branch: if `nums[lo] <= target < nums[mid]`, the target lies in the sorted left half, so set `hi = mid - 1`; otherwise set `lo = mid + 1`.",
 "Otherwise the right half is sorted. If `nums[mid] < target <= nums[hi]`, set `lo = mid + 1`; otherwise set `hi = mid - 1`.",
 "If the loop exits, the target is absent, so return −1.",
],
"opt_code":
'''def searchRotated(nums, target):
    """At any midpoint, at least ONE half is properly sorted -- the pivot can
    only fall in one of them. Identify that half, then test whether the target
    lies inside its known range."""
    lo, hi = 0, len(nums) - 1

    while lo <= hi:                       # inclusive range
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid

        # *** `<=` not `<`: when the range is two elements, mid == lo ***
        if nums[lo] <= nums[mid]:                 # LEFT half is sorted
            if nums[lo] <= target < nums[mid]:    # target inside that sorted range
                hi = mid - 1
            else:
                lo = mid + 1                      # must be in the messy right half
        else:                                     # RIGHT half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1''',
"opt_cx":
 "**Time: O(log n).** Each iteration performs O(1) comparisons and discards half the remaining "
 "range, exactly as in ordinary binary search &mdash; identifying the sorted half costs nothing "
 "asymptotically.\n\n"
 "**Space: O(1).**\n\n"
 "**Say this out loud:** \"Wherever I split it, one half is always properly sorted, because the "
 "pivot can only be in one of them. So I identify the sorted half by comparing nums[lo] with "
 "nums[mid], then check whether the target lies within that half's known range. Half the array "
 "is eliminated each step, so O(log n).\"\n\n"
 "**The gotcha:** `nums[lo] <= nums[mid]` with the equals sign, for the two-element case. "
 "**The follow-up to have ready:** with duplicates &mdash; problem 81 &mdash; `nums[lo]` can "
 "equal `nums[mid]` while telling you nothing, and the standard fix is to increment `lo` by one "
 "and retry, which pushes the worst case to O(n). Saying that unprompted is a strong signal.",
},

{
"num": 322, "title": "Coin Change", "stars": "★★", "day": DAY,
"pattern": "Bottom-up unbounded-knapsack DP",
"opt_cx_short": "O(amount · coins) time, O(amount) space",
"clarify": [
 "Is the supply of each coin **unlimited**? That is what makes it unbounded knapsack rather than 0/1, and it changes the loop structure.",
 "Should I return the **fewest coins**, or the number of ways to make the amount? Those are different problems &mdash; problem 518 is the counting version.",
 "What do I return when the amount cannot be formed at all &mdash; −1?",
 "Can the amount be 0? Then the answer is 0 coins, which is my DP base case.",
 "Are all coin denominations positive? And are the denominations arbitrary, or a canonical currency system? This matters because **greedy is wrong for arbitrary denominations**, and I would want to make that explicit before choosing an approach.",
],
"understand":
 "Given coin denominations and a target amount, return the fewest coins that sum to the amount, "
 "or −1 if it is impossible. Each denomination may be used any number of times.\n\n"
 "The first thing to say, unprompted, is that **greedy does not work here**, and to have the "
 "counterexample ready: with `coins = [1, 3, 4]` and `amount = 6`, greedy takes 4, then 1, then "
 "1, for three coins, while the optimum is 3 + 3, two coins. Greedy fails because taking the "
 "largest coin now can leave a remainder that is awkward to fill.\n\n"
 "What makes DP correct instead is **optimal substructure**: if the best solution for amount "
 "`a` uses a coin `c`, then the rest of that solution must itself be an optimal solution for "
 "`a - c` &mdash; otherwise I could substitute a better one and improve the whole. So "
 "`dp[a] = 1 + min(dp[a - c])` over all usable coins `c`, and the subproblems overlap heavily, "
 "which is exactly when DP beats recursion.",
"brute_en":
 "Recursive exhaustive search. To make amount `a`, try each coin `c` that does not exceed `a`, "
 "recursively solve for `a - c`, and take the smallest result plus one. The base case is `a == "
 "0`, which needs zero coins; if no coin leads to a solution, report infinity.\n\n"
 "This explores every distinct multiset of coins summing to the amount. It is obviously correct, "
 "and it is the version worth writing on the board first because the recurrence it exposes, "
 "`dp[a] = 1 + min(dp[a - c])`, is literally the DP transition. The optimisation is then just "
 "\"stop recomputing the same subproblems\", which is an easy story to tell.",
"brute_ds":
 "- The **call stack**, up to `amount` frames deep when the smallest coin is 1.\n"
 "- No memoisation at all &mdash; that absence is the entire problem.",
"brute_algo": [
 "Define `solve(rem)`, the fewest coins needed to make `rem`.",
 "If `rem == 0`, return 0.",
 "If `rem < 0`, this branch is invalid, so return infinity.",
 "Otherwise take the minimum of `1 + solve(rem - c)` over every coin `c`.",
 "Call `solve(amount)`; if the result is infinity, return −1, otherwise the result.",
],
"brute_cx":
 "**Time: O(cᵃ)** where c is the number of coins and a the amount &mdash; exponential. The "
 "recursion tree branches c ways at every level and can be up to `amount` levels deep when the "
 "smallest coin is 1. For `amount = 100` this is astronomically large.\n\n"
 "**Space: O(amount)** for the recursion depth.",
"brute_code":
'''def coinChange_brute(coins, amount):
    """Exhaustive recursion. Exposes the recurrence dp[a] = 1 + min(dp[a - c]),
    which is exactly what the DP fills in -- but recomputes it exponentially often."""
    INF = float('inf')

    def solve(rem):
        if rem == 0:
            return 0                      # base case: nothing left to pay
        if rem < 0:
            return INF                    # overshot: invalid branch
        best = INF
        for c in coins:
            best = min(best, 1 + solve(rem - c))
        return best

    result = solve(amount)
    return -1 if result == INF else result''',
"brute_limit":
 "The recursion recomputes identical subproblems an enormous number of times. With "
 "`coins = [1, 2, 5]`, the value of `solve(7)` is reached through 5+2, through 2+5, through "
 "1+1+... and dozens of other prefixes, and each arrival recomputes the entire subtree beneath "
 "it from scratch.\n\n"
 "But `solve(7)` has one fixed answer regardless of how it was reached. There are only "
 "`amount + 1` distinct subproblems in total, so the exponential blow-up is pure repetition. "
 "Storing each result the first time it is computed reduces the work to one evaluation per "
 "subproblem &mdash; that is memoisation, and turning the recursion inside out into a bottom-up "
 "table achieves the same thing without any recursion depth risk.",
"opt_en":
 "Build a table bottom-up. Let `dp[a]` be the fewest coins needed to make amount `a`. Initialise "
 "`dp[0] = 0`, since zero coins make zero, and every other entry to infinity, meaning "
 "\"not yet known to be reachable\".\n\n"
 "Then for each amount `a` from 1 to the target, and each coin `c` that does not exceed `a`, "
 "consider using `c` as the last coin: that costs `dp[a - c] + 1`. Take the minimum over all "
 "coins. Because the loop runs amounts in increasing order, `dp[a - c]` is always already final "
 "when it is read.\n\n"
 "Iterating **amounts on the outside and coins on the inside** is what makes this the unbounded "
 "version: each amount considers every coin freely, so a denomination can be reused any number "
 "of times. Reversing the loops and iterating amounts downward would give 0/1 knapsack, where "
 "each item is used at most once &mdash; a distinction worth naming, because it is the "
 "difference between this problem and the coin-counting variant.\n\n"
 "At the end, `dp[amount]` is either the answer or still infinity, in which case the amount "
 "cannot be formed and I return −1.",
"opt_ds":
 "- A **1-D DP array of length `amount + 1`**, where index `a` holds the fewest coins for "
 "amount `a`. One dimension suffices because the coin supply is unlimited, so there is no need "
 "to track which coins have been consumed.\n"
 "- `float('inf')` as the sentinel for unreachable, which makes the `min` comparison work "
 "without special cases.\n"
 "- Optionally a parallel `choice` array recording which coin was used at each amount, if the "
 "follow-up asks for the actual coins rather than the count.",
"opt_algo": [
 "Create `dp` of length `amount + 1`, with `dp[0] = 0` and every other entry set to infinity.",
 "Loop `a` from 1 to `amount` inclusive.",
 "For each coin `c`: if `c <= a` and `dp[a - c] + 1 < dp[a]`, set `dp[a] = dp[a - c] + 1`.",
 "The guard `c <= a` prevents a negative index; the comparison against `dp[a]` keeps the running minimum.",
 "Because amounts are processed in increasing order, `dp[a - c]` is already final whenever it is read.",
 "After the loops, return −1 if `dp[amount]` is still infinity, otherwise `dp[amount]`.",
],
"opt_code":
'''def coinChange(coins, amount):
    """dp[a] = fewest coins to make amount a.
    Unbounded supply => iterate AMOUNTS outward, coins inside."""
    INF = float('inf')
    dp = [0] + [INF] * amount             # dp[0] = 0: zero coins make zero

    for a in range(1, amount + 1):
        for c in coins:
            # `c <= a` guards the index; use c as the LAST coin and take the best
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1

    return -1 if dp[amount] == INF else dp[amount]

# Greedy is WRONG for arbitrary denominations:
#   coins = [1, 3, 4], amount = 6
#   greedy: 4 + 1 + 1 = 3 coins      DP: 3 + 3 = 2 coins
# Have this counterexample ready before they ask for it.''',
"opt_cx":
 "**Time: O(amount · number_of_coins).** Two nested loops with O(1) work inside. Each of "
 "the `amount` subproblems is solved exactly once, examining every coin.\n\n"
 "**Space: O(amount)** for the DP array. There is no recursion, so no stack-depth risk on large "
 "amounts &mdash; a real advantage of the bottom-up form over memoised recursion.\n\n"
 "**Say this out loud:** \"Greedy is wrong here, and the counterexample is coins [1,3,4] with "
 "amount 6. The problem has optimal substructure &mdash; the best way to make a, using coin c, "
 "contains the best way to make a−c &mdash; and the subproblems overlap heavily, so it is DP. "
 "dp[a] = 1 + min over coins of dp[a−c], filled bottom-up. O(amount × coins) time, O(amount) "
 "space.\"\n\n"
 "**Lead with the greedy counterexample before you are asked.** **The variants:** problem 518, "
 "Coin Change II, counts the *number of ways* and requires the loops swapped &mdash; coins "
 "outside, amounts inside &mdash; so that combinations are not double-counted as permutations. "
 "Knowing why the loop order differs is a strong signal.",
},

{
"num": 139, "title": "Word Break", "stars": "★", "day": DAY,
"pattern": "DP over prefixes", "opt_cx_short": "O(n² · k) time, O(n) space",
"clarify": [
 "May each dictionary word be reused **any number of times**?",
 "Do I return only a boolean, or the actual segmentation? Word Break II asks for all segmentations and needs backtracking with memoisation, which is a different shape.",
 "Are matches case-sensitive, and are there any characters outside the alphabet I should expect?",
 "Can the dictionary be large? That decides whether I convert it to a set, which I would do regardless.",
 "Can `s` be empty? By convention the empty string is segmentable, which is exactly my base case.",
],
"understand":
 "Given a string `s` and a dictionary of words, decide whether `s` can be segmented into a "
 "sequence of one or more dictionary words, with reuse allowed.\n\n"
 "The reason greedy fails, which is worth stating: taking the longest matching prefix at each "
 "step can dead-end. With `s = \"aaaab\"` and a dictionary of `[\"aaaa\", \"aaa\", \"ab\"]`, "
 "greedily taking `\"aaaa\"` leaves `\"b\"`, which is unmatchable, while taking `\"aaa\"` first "
 "leaves `\"ab\"`, which succeeds. A local choice cannot be validated locally.\n\n"
 "The DP formulation: let `dp[i]` mean \"the first `i` characters of `s` can be segmented\". "
 "Then `dp[i]` is true if there exists some split point `j < i` where `dp[j]` is true **and** "
 "the substring `s[j:i]` is a dictionary word. `dp[0]` is true because the empty prefix is "
 "trivially segmentable, and that base case is what seeds everything else.",
"brute_en":
 "Recursive exploration of every split. Starting at position `start`, try every end position "
 "`end` greater than `start`; if `s[start:end]` is a dictionary word, recurse from `end`. If "
 "any branch reaches the end of the string, the segmentation succeeds.\n\n"
 "This enumerates every possible way of cutting the string. It is clearly correct, and it "
 "exposes exactly the same recurrence the DP fills in &mdash; the only difference being that "
 "the recursion re-solves the same suffixes over and over.",
"brute_ds":
 "- A **set** of dictionary words for O(1) membership.\n"
 "- The call stack, up to n frames deep.\n"
 "- No memoisation, which is the flaw.",
"brute_algo": [
 "Convert the dictionary to a set.",
 "Define `can(start)`: true if `s[start:]` can be segmented.",
 "If `start == len(s)`, the whole string has been consumed, so return True.",
 "For each `end` from `start + 1` to `len(s)`: if `s[start:end]` is in the set and `can(end)` is true, return True.",
 "If no split works, return False.",
 "Call `can(0)`.",
],
"brute_cx":
 "**Time: O(2ⁿ) in the worst case.** Every position is either a cut point or not, giving "
 "2^(n−1) possible segmentations, and pathological inputs such as "
 "`s = \"aaaaaaaaab\"` with dictionary `[\"a\", \"aa\", \"aaa\"]` actually reach that bound, "
 "because almost every prefix matches and almost every branch fails only at the very end.\n\n"
 "**Space: O(n)** for the recursion depth, plus O(dictionary) for the set.",
"brute_code":
'''def wordBreak_brute(s, wordDict):
    """Try every cut point recursively. Exponential -- the same suffix is
    re-solved once per distinct path that reaches it."""
    words = set(wordDict)

    def can(start):
        if start == len(s):
            return True                   # consumed the whole string
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in words and can(end):
                return True
        return False

    return can(0)''',
"brute_limit":
 "The recursion asks \"can `s[7:]` be segmented?\" once for every distinct way of segmenting the "
 "first seven characters &mdash; and there can be exponentially many of those. But the answer "
 "for position 7 does not depend on how the search arrived there at all.\n\n"
 "There are only `n + 1` distinct subproblems, one per starting position. Computing each exactly "
 "once collapses the exponential to a polynomial. Memoising the recursion achieves this "
 "directly; the bottom-up table is the same computation with the dependency order made explicit "
 "and no recursion depth to worry about.",
"opt_en":
 "Build a boolean array `dp` of length `n + 1`, where `dp[i]` means the first `i` characters are "
 "segmentable. Set `dp[0] = True` for the empty prefix.\n\n"
 "For each end position `i` from 1 to n, look back at every possible split point `j` from 0 to "
 "`i - 1`. If `dp[j]` is true and the substring `s[j:i]` is in the dictionary, then `s[:i]` is "
 "segmentable, so set `dp[i] = True` and break out of the inner loop &mdash; one witness is "
 "enough, and continuing would only find more of them.\n\n"
 "The order matters and is what makes it correct: all values `dp[j]` for `j < i` are already "
 "final when `dp[i]` is computed, because the outer loop runs left to right. The answer is "
 "`dp[n]`.\n\n"
 "Two optimisations worth naming. Converting the dictionary to a **set** is essential &mdash; "
 "the inner membership test would otherwise be a linear scan. And the inner loop can be bounded "
 "by the **length of the longest dictionary word**, since a substring longer than that can "
 "never match, which in practice turns the O(n²) inner work into O(n · L).",
"opt_ds":
 "- A **boolean DP array of length n + 1** over prefix lengths. `dp[0] = True` is the base case "
 "that everything else is built from, and it is the analogue of `count[0] = 1` in problem 560 "
 "&mdash; the empty-prefix seed.\n"
 "- A **set** of dictionary words, making each substring test O(L) hashing rather than an "
 "O(dictionary) scan.\n"
 "- Optionally the maximum word length, used to bound the inner loop.",
"opt_algo": [
 "Convert `wordDict` to a set.",
 "Create `dp` of length `len(s) + 1`, all False, then set `dp[0] = True` for the empty prefix.",
 "Loop `i` from 1 to `len(s)` inclusive &mdash; the end of the prefix under consideration.",
 "Loop `j` from 0 to `i - 1` &mdash; the candidate split point.",
 "If `dp[j]` is True and `s[j:i]` is in the set, set `dp[i] = True` and break: one valid witness settles it.",
 "Return `dp[len(s)]`.",
 "Optional speed-up: start `j` at `max(0, i - max_word_len)` instead of 0, since any longer substring cannot be a dictionary word.",
],
"opt_code":
'''def wordBreak(s, wordDict):
    """dp[i] = 'the first i characters of s can be segmented'."""
    words = set(wordDict)                 # O(1) membership instead of a scan
    n = len(s)

    dp = [False] * (n + 1)
    dp[0] = True                          # the empty prefix is segmentable -- the seed

    for i in range(1, n + 1):             # end of the prefix
        for j in range(i):                # candidate split point, j < i
            # dp[j] is already final because i runs left to right
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break                     # one witness is enough

    return dp[n]

# Why not greedy? Taking the longest match can dead-end:
#   s = "aaaab", dict = ["aaaa", "aaa", "ab"]
#   greedy "aaaa" -> leaves "b" -> fails;  "aaa" -> leaves "ab" -> succeeds.''',
"opt_cx":
 "**Time: O(n² · k)** where k is the average word length. The two nested loops give "
 "O(n²) substring positions, and each `s[j:i]` slice plus hash costs O(k). Bounding the "
 "inner loop by the longest dictionary word improves this to O(n · L · k) in practice.\n\n"
 "**Space: O(n)** for the DP array, plus O(total dictionary size) for the set.\n\n"
 "**Say this out loud:** \"Greedy fails because a longer match can dead-end, so I need to "
 "consider every split. dp[i] means the first i characters are segmentable, and it is true if "
 "some earlier true position j has s[j:i] in the dictionary. dp[0] is true for the empty "
 "prefix. Two nested loops with an O(k) substring test: O(n²k) time, O(n) space.\"\n\n"
 "**The follow-up:** Word Break II asks for all valid segmentations, which needs backtracking "
 "with memoisation from position to the list of sentences &mdash; and the output itself can be "
 "exponentially large, so no polynomial bound is possible there. Saying that shows you "
 "understand why the two problems have different complexity classes.",
},

{
"num": 146, "title": "LRU Cache", "stars": "★★", "day": DAY,
"pattern": "Hash map + doubly linked list (design)",
"opt_cx_short": "get and put both O(1), O(capacity) space",
"clarify": [
 "Does a `get` on an existing key count as a **use**, moving it to most-recently-used? Yes, in the standard definition &mdash; and it is the detail people forget.",
 "Does `put` on an **existing** key also count as a use, updating the value and refreshing its recency?",
 "What does `get` return for a missing key &mdash; −1?",
 "Is the capacity guaranteed to be at least 1?",
 "Must both operations be **O(1)**, or is O(log n) acceptable? O(1) is what forces the hash map plus linked list design, so I want that confirmed &mdash; it is the whole point of the question.",
],
"understand":
 "Design a fixed-capacity cache supporting `get(key)` and `put(key, value)` in O(1), evicting "
 "the least recently used entry when the capacity is exceeded.\n\n"
 "The design tension is that two different requirements pull toward two different structures. "
 "**O(1) lookup by key** demands a hash map. **O(1) maintenance of a recency ordering**, with "
 "the ability to move an arbitrary item to the front and to drop the item at the back, demands "
 "a doubly linked list &mdash; an array cannot reorder in O(1), and a singly linked list cannot "
 "unlink a node without walking to its predecessor.\n\n"
 "The resolution is to use **both**, wired together: the hash map stores key → **node "
 "reference**, and the nodes live in the linked list. That combination gives O(1) lookup *and* "
 "O(1) reordering, because the map hands you the node directly and the doubly-linked structure "
 "lets you unlink it without any traversal. Recognising that no single structure can do the job "
 "is the insight the question is testing.",
"brute_en":
 "Store the entries in a plain list ordered from most to least recently used, and search it "
 "linearly. `get` scans the list for the key; if found, it removes the entry from its position "
 "and reinserts it at the front, then returns the value. `put` scans for the key, removes it if "
 "present, inserts the new entry at the front, and pops from the end if the capacity is "
 "exceeded.\n\n"
 "This is correct and easy to reason about &mdash; the list order *is* the recency order &mdash; "
 "but every operation involves a linear search and a list shift.",
"brute_ds":
 "- A single **list of `(key, value)` pairs** kept in recency order, most recent first.\n"
 "- No index structure of any kind, which is what forces the scan.",
"brute_algo": [
 "Store `self.data` as a list of `(key, value)` pairs, most recently used first, and `self.cap`.",
 "**get(key):** scan the list for a matching key. If absent, return −1.",
 "If found at index `i`, pop it and reinsert it at index 0, then return its value.",
 "**put(key, value):** scan for the key; if present, pop it.",
 "Insert `(key, value)` at index 0.",
 "If the list is now longer than the capacity, pop the last element, which is the least recently used.",
],
"brute_cx":
 "**Time: O(n) per operation**, where n is the current number of entries. The linear scan "
 "dominates, and `pop(i)` and `insert(0, …)` each shift O(n) elements in a Python list.\n\n"
 "**Space: O(capacity).**\n\n"
 "At a realistic cache size of 100,000 entries, this is roughly 100,000 times slower per "
 "operation than the target &mdash; and a cache is precisely the component that must not be "
 "slow.",
"brute_code":
'''class LRUCache_brute:
    """List in recency order, searched linearly. O(n) per operation."""

    def __init__(self, capacity):
        self.cap = capacity
        self.data = []                    # [(key, value)], most recent first

    def get(self, key):
        for i, (k, v) in enumerate(self.data):    # O(n) scan
            if k == key:
                self.data.pop(i)          # O(n) shift
                self.data.insert(0, (k, v))       # O(n) shift -- now most recent
                return v
        return -1

    def put(self, key, value):
        for i, (k, _) in enumerate(self.data):    # O(n) scan
            if k == key:
                self.data.pop(i)
                break
        self.data.insert(0, (key, value))
        if len(self.data) > self.cap:
            self.data.pop()               # drop the least recently used''',
"brute_limit":
 "Two independent O(n) costs. Finding the key requires a scan, because the list is ordered by "
 "recency and therefore carries no information about where a given key sits. And reordering "
 "requires shifting elements, because arrays store their order positionally.\n\n"
 "Each has a standard fix, and the design insight is that they are **different** fixes and both "
 "are needed. A hash map removes the search but has no notion of order. A linked list removes "
 "the shifting but has no notion of lookup. Combining them &mdash; a map whose *values are the "
 "list nodes themselves* &mdash; makes both operations O(1) simultaneously.",
"opt_en":
 "A doubly linked list holds the entries in recency order, with the most recently used next to "
 "the head and the least recently used next to the tail. A hash map maps each key directly to "
 "its **node** in that list.\n\n"
 "Use **sentinel head and tail nodes** that never hold data. This is the detail that makes the "
 "code short: every real node always has both a predecessor and a successor, so unlinking is "
 "four pointer assignments with no null checks and no special cases for the first or last "
 "element.\n\n"
 "`get(key)`: if the key is absent, return −1. Otherwise fetch the node from the map in O(1), "
 "unlink it from its current position, relink it just after the head to mark it most recent, "
 "and return its value.\n\n"
 "`put(key, value)`: if the key exists, unlink its old node. Create a new node, store it in the "
 "map, and insert it just after the head. If the map now exceeds the capacity, take the node "
 "just before the tail &mdash; the least recently used &mdash; unlink it, and delete its key "
 "from the map.\n\n"
 "**The node must store its own key.** Eviction begins from the list, giving you a node, and "
 "you then need to remove the corresponding entry from the map &mdash; which requires knowing "
 "the key. Without it you would have to scan the map, which reintroduces the O(n) you just "
 "eliminated. This is the single most important line in the whole design and is worth saying "
 "aloud.",
"opt_ds":
 "- A **hash map from key to node reference**. Not to the value &mdash; to the node &mdash; "
 "because the node is what needs to be repositioned.\n"
 "- A **doubly linked list** in recency order. Doubly, not singly, because unlinking a node "
 "requires its predecessor, and a singly linked list would need an O(n) walk to find it.\n"
 "- **Sentinel head and tail nodes**, eliminating every null check.\n"
 "- Each node stores `key`, `value`, `prev`, `next`. The `key` field exists solely so that "
 "eviction can clean up the map.",
"opt_algo": [
 "Define a `Node` class with `key`, `val`, `prev`, `next`.",
 "In the constructor, create sentinel `head` and `tail` nodes and link them to each other, so the list is never empty from the pointer logic's point of view. Store the capacity and an empty map.",
 "Write `_remove(node)`: set `node.prev.next = node.next` and `node.next.prev = node.prev`. Sentinels guarantee both neighbours exist.",
 "Write `_add_front(node)`: splice `node` between `head` and `head.next`, updating all four pointers.",
 "**get(key):** return −1 if the key is absent. Otherwise fetch the node, `_remove` it, `_add_front` it, and return `node.val`.",
 "**put(key, value):** if the key is present, `_remove` its existing node first.",
 "Create a new node, set `map[key] = node`, and `_add_front(node)`.",
 "If `len(map) > cap`: take `lru = tail.prev`, `_remove(lru)`, and `del map[lru.key]` &mdash; which is only possible because the node carries its key.",
],
"opt_code":
'''class Node:
    """Doubly linked node. It stores its own KEY so that eviction can also
    delete the corresponding map entry -- without this you would have to scan."""
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                     # key -> Node (the NODE, not the value)
        # Sentinels: every real node always has a prev and a next,
        # so there is not a single null check anywhere below.
        self.head = Node()                # most-recent side
        self.tail = Node()                # least-recent side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Unlink a node in O(1). Needs `prev`, hence a DOUBLY linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        """Splice a node in just after head == mark it most recently used."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)                # a read counts as a use...
        self._add_front(node)             # ...so refresh its recency
        return node.val

    def put(self, key, value):
        if key in self.map:
            self._remove(self.map[key])   # drop the stale node; a new one replaces it
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)

        if len(self.map) > self.cap:
            lru = self.tail.prev          # the node just before the tail sentinel
            self._remove(lru)
            del self.map[lru.key]         # *** only possible because Node stores key ***''',
"opt_cx":
 "**Time: O(1) for both `get` and `put`.** The map lookup is O(1) average, and every list "
 "operation is a fixed number of pointer assignments &mdash; no traversal anywhere.\n\n"
 "**Space: O(capacity)** for the map and the nodes.\n\n"
 "**Say this out loud:** \"Two requirements, two structures. O(1) lookup by key needs a hash "
 "map; O(1) reordering and eviction needs a doubly linked list. I combine them by mapping keys "
 "to nodes, so a lookup hands me the node directly and unlinking it is four pointer writes. "
 "Sentinel head and tail remove all the null checks, and the node stores its own key so "
 "eviction can clean up the map.\"\n\n"
 "**The shortcut and why to avoid it:** Python's `OrderedDict` with `move_to_end` and "
 "`popitem(last=False)` solves this in about eight lines. Mention that you know it, then write "
 "the manual version &mdash; interviewers ask this question specifically to see the pointer "
 "work. **The follow-up:** LFU Cache, problem 460, which needs a frequency map plus one linked "
 "list per frequency and a running minimum-frequency pointer.",
},

{
"num": 138, "title": "Copy List with Random Pointer", "stars": "★★", "day": DAY,
"pattern": "Hash map old→new, then the O(1)-space interleave",
"opt_cx_short": "O(n) time, O(n) space — or O(1) space with the weave",
"clarify": [
 "Can a `random` pointer be **null**, point **forward** to a node not yet created, point **backward**, or point at the node itself? All four occur, and the forward case is what makes single-pass copying awkward.",
 "Must this be a genuine **deep copy**, where no pointer in the new list refers to any node of the original?",
 "May I **modify the original list** during the process, as long as I restore it before returning? That is the precondition for the O(1)-space solution, so I want it confirmed.",
 "Can the list be empty?",
 "Is there a space constraint? If O(n) auxiliary space is acceptable I would lead with the hash map; the O(1) version is the standard follow-up either way.",
],
"understand":
 "Each node has a `next` pointer and a `random` pointer that may point anywhere in the list or "
 "be null. I must produce a deep copy in which every pointer refers only to copied nodes.\n\n"
 "The difficulty is entirely the `random` pointer. Copying `next` alone is a trivial single "
 "pass, but a `random` pointer may point **forward** to a node whose clone does not exist yet. "
 "So I cannot both create and fully wire a node in one step.\n\n"
 "The resolution in either solution is the same: **separate creation from wiring.** Create "
 "every clone first, so that by the time any pointer is assigned, its target already exists. "
 "The two solutions differ only in how they record the correspondence between an original node "
 "and its clone &mdash; an explicit hash map, or the structure of the list itself.",
"brute_en":
 "Copy the `next` chain first, producing a plain clone with all `random` pointers left null. "
 "Then, for each original node, determine the **position** of its `random` target by walking "
 "from the original head and counting steps until reaching that node. Then walk the same number "
 "of steps into the copied list to find the corresponding clone, and assign it.\n\n"
 "Position is the correspondence mechanism here: the kth node of the copy corresponds to the "
 "kth node of the original. It works, but establishing the position requires a linear walk, and "
 "using it requires a second one.",
"brute_ds":
 "- The newly created nodes.\n"
 "- **No map** &mdash; position is used as the correspondence, and computing a position is what "
 "costs the linear walk.",
"brute_algo": [
 "First pass: walk the original list creating a clone of each node, linked only by `next`. Remember the head of the copy.",
 "Second pass: for each original node `cur`, if `cur.random` is null, leave the clone's `random` as null and continue.",
 "Otherwise walk from the original head, counting steps, until reaching `cur.random`; record that count as `idx`.",
 "Walk `idx` steps from the copy's head to reach the corresponding clone.",
 "Assign that clone to the current clone's `random`.",
 "Return the head of the copy.",
],
"brute_cx":
 "**Time: O(n²).** Each of the n nodes requires up to two full linear walks &mdash; one to "
 "find the index of its random target, one to reach that index in the copy.\n\n"
 "**Space: O(n)** for the copied nodes, which is required output rather than overhead.",
"brute_code":
'''def copyRandomList_brute(head):
    """Position is the correspondence: the kth clone matches the kth original.
    Finding a position costs a linear walk, so this is O(n^2)."""
    if not head:
        return None

    # Pass 1: clone the `next` chain only.
    new_head = Node(head.val)
    cur, new_cur = head, new_head
    while cur.next:
        new_cur.next = Node(cur.next.val)
        cur, new_cur = cur.next, new_cur.next

    # Pass 2: resolve each random pointer by index.
    cur, new_cur = head, new_head
    while cur:
        if cur.random:
            idx = 0
            probe = head
            while probe is not cur.random:    # O(n): find the target's position
                probe = probe.next
                idx += 1
            target = new_head
            for _ in range(idx):              # O(n): walk to that position in the copy
                target = target.next
            new_cur.random = target
        cur, new_cur = cur.next, new_cur.next

    return new_head''',
"brute_limit":
 "The algorithm keeps re-answering the same question &mdash; \"which node is this, and where is "
 "its clone?\" &mdash; by walking the list, when the answer is fixed and could simply be "
 "recorded. Using position as the correspondence is the root of the problem: a position is "
 "expensive to compute and expensive to use, while the correspondence itself is just a mapping "
 "from one node to another.\n\n"
 "Storing that mapping directly, in a hash map from original node to clone, makes both "
 "directions O(1) and reduces the whole algorithm to two linear passes. And if even the map is "
 "too much memory, the correspondence can be encoded **into the list's own structure** by "
 "placing each clone immediately after its original &mdash; which removes the auxiliary space "
 "entirely.",
"opt_en":
 "**Optimal A &mdash; the hash map. Lead with this.** Pass one: walk the original list and "
 "create a clone of each node, recording `old_to_new[original] = clone`. Wire nothing yet. "
 "Pass two: now that every clone exists, walk again and set both pointers by lookup &mdash; "
 "`old_to_new[cur].next = old_to_new.get(cur.next)` and "
 "`old_to_new[cur].random = old_to_new.get(cur.random)`.\n\n"
 "Use `.get(...)` rather than `[...]`: `cur.next` is `None` at the tail and `cur.random` may be "
 "`None` anywhere, and `.get(None)` returns `None` instead of raising `KeyError`. That is a "
 "genuinely elegant use of `.get` &mdash; the null case is handled by the same expression as "
 "the normal case.\n\n"
 "**Optimal B &mdash; the O(1)-space weave. This is the follow-up they want.** Instead of a "
 "map, store the correspondence *inside the list*: insert each clone immediately after its "
 "original, so the list temporarily reads `A → A' → B → B' → C → C'`. Now the clone of any node "
 "`X` is simply `X.next`, with no lookup at all &mdash; which means the clone of `X.random` is "
 "`X.random.next`. So the random-wiring pass is the single line "
 "`cur.next.random = cur.random.next`, read aloud as *\"my clone's random is the clone of my "
 "random.\"*\n\n"
 "Then unweave: restore each original's `next` and link the clones to each other, guarding the "
 "final node where `new.next` is null. Three passes, no auxiliary structure.",
"opt_ds":
 "- **Optimal A:** a **hash map from original node to cloned node**. Keying on the node object "
 "itself, not on its value, since values may repeat.\n"
 "- **Optimal B:** **nothing.** The interleaved list structure *is* the map &mdash; the "
 "relationship \"clone of X\" is encoded as \"the node right after X\". That substitution of "
 "structure for storage is the idea worth naming.",
"opt_algo": [
 "**A, pass 1:** walk the list; for each `cur`, set `old_to_new[cur] = Node(cur.val)`. Creating every clone first is what makes forward random pointers resolvable in pass 2.",
 "**A, pass 2:** walk again; set `old_to_new[cur].next = old_to_new.get(cur.next)` and `old_to_new[cur].random = old_to_new.get(cur.random)`. Return `old_to_new[head]`.",
 "**B, pass 1 (weave):** for each original `cur`, set `cur.next = Node(cur.val, cur.next)`, then jump `cur = cur.next.next` to skip the clone just inserted.",
 "**B, pass 2 (randoms):** for each original `cur`, if `cur.random` is not null, set `cur.next.random = cur.random.next`. Advance by two.",
 "**B, pass 3 (unweave):** save `new_head = head.next`. Then for each pair, restore `old.next = old.next.next` and set `new.next = new.next.next if new.next else None`, guarding the tail.",
 "Return `new_head`. Restoring the original list matters: the caller may still hold a reference to it.",
],
"opt_code":
'''def copyRandomList(head):
    """OPTIMAL A -- hash map. O(n) time, O(n) space. Lead with this."""
    if not head:
        return None

    old_to_new = {}

    cur = head
    while cur:                            # PASS 1: create EVERY clone first,
        old_to_new[cur] = Node(cur.val)   # so forward randoms already exist in pass 2
        cur = cur.next

    cur = head
    while cur:                            # PASS 2: wire pointers between clones
        # .get(), not [] -- cur.next is None at the tail and random may be None;
        # .get(None) returns None instead of raising KeyError.
        old_to_new[cur].next   = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next

    return old_to_new[head]


def copyRandomList_O1(head):
    """OPTIMAL B -- the O(1)-space follow-up. The interleaved list IS the map:
    the clone of X is simply X.next."""
    if not head:
        return None

    # 1. WEAVE:  A -> A' -> B -> B' -> C -> C'
    cur = head
    while cur:
        cur.next = Node(cur.val, cur.next)   # clone sits directly after its original
        cur = cur.next.next                  # skip over the clone we just inserted

    # 2. RANDOMS: "my clone's random is the clone of my random"
    cur = head
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next

    # 3. UNWEAVE back into two independent lists.
    old, new = head, head.next
    new_head = head.next
    while old:
        old.next = old.next.next                        # restore the original chain
        new.next = new.next.next if new.next else None  # guard the tail
        old, new = old.next, new.next

    return new_head''',
"opt_cx":
 "**Optimal A &mdash; time O(n), space O(n).** Two passes with O(1) hash operations; the map "
 "holds n entries.\n\n"
 "**Optimal B &mdash; time O(n), space O(1)** excluding the output. Three passes, no auxiliary "
 "structure at all.\n\n"
 "**Say this out loud:** \"The obstacle is that a random pointer can point forward to a node "
 "whose clone does not exist yet, so I separate creation from wiring: create all clones in pass "
 "one, wire everything in pass two. The map version is O(n) space. The follow-up removes it by "
 "putting each clone directly after its original, so the clone of X is just X.next &mdash; the "
 "list structure replaces the map. Then unweave to restore the original.\"\n\n"
 "**Present A, then offer B unprompted.** **The detail to state in A:** `.get` rather than `[]` "
 "for the null tail. **The detail to state in B:** you must restore the original list before "
 "returning, since the caller still holds a reference to it.",
},

{
"num": 1011, "title": "Capacity To Ship Packages Within D Days", "stars": "★  (stretch)", "day": DAY,
"pattern": "Binary search on the answer", "opt_cx_short": "O(n log(sum weights)) time, O(1) space",
"clarify": [
 "Must packages be shipped in the **given order**, without reordering? Yes &mdash; that is what makes the feasibility check a simple greedy pass rather than a bin-packing problem, which would be NP-hard.",
 "Can a day be left with no packages shipped? It never helps, but confirming it means my greedy fill is optimal.",
 "Are the weights positive integers, and is `days` at least 1 and at most the number of packages?",
 "I return the **minimum** capacity such that everything ships within `days` days?",
 "How large can the total weight be? That sets the top of my search range and therefore the log factor.",
],
"understand":
 "Packages must be shipped in their given order within `days` days. Each day the ship carries a "
 "prefix of the remaining packages whose total weight does not exceed its capacity. Find the "
 "minimum capacity that makes this possible.\n\n"
 "This is the **same problem as Koko Eating Bananas** with a different feasibility function, "
 "and recognising that instantly is the point. Both ask for the minimum value of a parameter "
 "such that a condition holds; both have a feasibility predicate that is monotonic &mdash; a "
 "larger capacity never needs *more* days &mdash; and computable in O(n). So both are binary "
 "search on the answer.\n\n"
 "The bounds require a moment's thought and are where this problem differs. The lower bound is "
 "`max(weights)`, not 1: a capacity below the heaviest single package could never ship that "
 "package on any day, no matter how long you wait. The upper bound is `sum(weights)`, which "
 "ships everything in one day.",
"brute_en":
 "Try every capacity in increasing order, starting from `max(weights)`, and return the first "
 "one that ships everything within `days` days.\n\n"
 "The feasibility check itself is a greedy simulation: walk the packages in order, adding each "
 "to the current day's load; when the next package would overflow the capacity, start a new day. "
 "Greedy is optimal here precisely because the order is fixed &mdash; loading as much as "
 "possible each day can never require more days than any alternative, since any package left "
 "off today must still be carried later and cannot be swapped with a different one.",
"brute_ds":
 "- None. A day counter and a running load inside the check.\n"
 "- The `days_needed` helper is the reusable artefact, exactly as `hours_needed` was in "
 "problem 875.",
"brute_algo": [
 "Write `days_needed(cap)`: set `d = 1` and `cur = 0`, then for each weight `w`, if `cur + w > cap` start a new day by incrementing `d` and resetting `cur` to 0; then add `w` to `cur`. Return `d`.",
 "Loop `cap` from `max(weights)` up to `sum(weights)`.",
 "If `days_needed(cap) <= days`, return `cap`.",
 "Monotonicity means the first feasible capacity is the minimum.",
],
"brute_cx":
 "**Time: O(n · sum(weights)).** Each candidate capacity costs an O(n) simulation, and the "
 "range of candidates spans from the maximum weight to the total weight, which can be enormous.\n\n"
 "**Space: O(1).**",
"brute_code":
'''def shipWithinDays_brute(weights, days):
    """Try every capacity upward. O(n * sum(weights))."""
    def days_needed(cap):
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:             # would overflow -> start a new day
                d += 1
                cur = 0
            cur += w
        return d

    for cap in range(max(weights), sum(weights) + 1):
        if days_needed(cap) <= days:
            return cap
    return sum(weights)''',
"brute_limit":
 "Identical to problem 875: the linear scan tests every capacity individually, when a single "
 "test already eliminates an entire half of the range. If capacity 500 needs too many days, "
 "every capacity below 500 needs at least as many, and the scan makes no use of that.\n\n"
 "Since feasibility is monotonic in the capacity, binary search reduces the number of O(n) "
 "evaluations from `sum(weights)` to `log₂(sum(weights))` &mdash; roughly 25 evaluations "
 "instead of tens of millions.",
"opt_en":
 "Binary search the capacity range `[max(weights), sum(weights)]`, using the same greedy "
 "`days_needed` check unchanged.\n\n"
 "Take the midpoint. If `days_needed(mid) <= days`, the capacity is sufficient and might not be "
 "the smallest such, so keep it in the range with `hi = mid`. Otherwise it is too small, along "
 "with everything below it, so `lo = mid + 1`. The `while lo < hi` lower-bound template "
 "converges on the smallest feasible capacity with no post-loop adjustment.\n\n"
 "The lower bound deserves a sentence of its own in the interview: starting at 1 would be "
 "wrong-headed rather than merely slow, since no capacity below the heaviest package can ever "
 "work. Stating why `lo = max(weights)` demonstrates you reasoned about the search space rather "
 "than pasting a template.\n\n"
 "This is the same function as Split Array Largest Sum, problem 410, almost line for line "
 "&mdash; there, the array is split into `m` subarrays and you minimise the largest subarray "
 "sum, which is exactly this greedy check with the roles renamed.",
"opt_ds":
 "- **No data structure.** Two integer bounds plus the O(n) greedy feasibility check.\n"
 "- The transferable component is `days_needed`, which is the same shape as `hours_needed` in "
 "problem 875 and the partition check in problem 410.",
"opt_algo": [
 "Define `days_needed(cap)` as the greedy simulation: start on day 1 with an empty load; for each weight, open a new day if adding it would exceed `cap`, then add it. Return the day count.",
 "Set `lo = max(weights)` &mdash; the heaviest package must fit on some single day &mdash; and `hi = sum(weights)`, which ships everything at once.",
 "While `lo < hi`: compute `mid = (lo + hi) // 2`.",
 "If `days_needed(mid) <= days`, this capacity works, so set `hi = mid`, keeping `mid` as a candidate.",
 "Otherwise set `lo = mid + 1`.",
 "Return `lo`, which now equals `hi` and is the minimum feasible capacity.",
],
"opt_code":
'''def shipWithinDays(weights, days):
    """Same shape as Koko (875): binary search a monotonic answer space."""

    def days_needed(cap):
        """Greedy is optimal because the package ORDER is fixed."""
        d, cur = 1, 0
        for w in weights:
            if cur + w > cap:             # cannot fit today -> open a new day
                d += 1
                cur = 0
            cur += w
        return d

    # *** lo = max(weights), NOT 1: a capacity below the heaviest package
    # could never ship that package on any day. ***
    lo, hi = max(weights), sum(weights)

    while lo < hi:                        # lower-bound template
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid                      # feasible -> try smaller
        else:
            lo = mid + 1                  # too small -> and so is everything below

    return lo''',
"opt_cx":
 "**Time: O(n · log(sum(weights) − max(weights))).** Roughly 25 to 30 binary search "
 "iterations for realistic inputs, each running the O(n) greedy check.\n\n"
 "**Space: O(1).**\n\n"
 "**Say this out loud:** \"This is the same pattern as Koko: minimum X such that a condition "
 "holds, with an O(n) feasibility check and monotonic feasibility &mdash; more capacity never "
 "needs more days. So binary search the capacity range. The lower bound is max(weights), "
 "because nothing smaller can carry the heaviest package, and the upper bound is the total "
 "weight.\"\n\n"
 "**The gotcha:** `lo = max(weights)`, not 1, and be able to say why. **The family:** Koko "
 "Eating Bananas (875), Split Array Largest Sum (410), Minimum Number of Days to Make m "
 "Bouquets (1482) &mdash; all the same search with a different `feasible()`.",
},

{
"num": 380, "title": "Insert Delete GetRandom O(1)", "stars": "★  (stretch)", "day": DAY,
"pattern": "Dynamic array + index map, swap-with-last on delete",
"opt_cx_short": "insert / remove / getRandom all O(1), O(n) space",
"clarify": [
 "Must `getRandom` return each element with **equal probability**? That is the requirement that forces a contiguous array, since uniform sampling needs O(1) indexing by position.",
 "Are duplicate values allowed? The standard version says no &mdash; it is a set. Problem 381 allows duplicates and needs the map to hold a set of indices per value.",
 "Should `insert` return False when the value is already present, and `remove` return False when it is absent?",
 "Is `getRandom` only ever called on a non-empty structure?",
 "Does **average** O(1) suffice, given that hash operations are amortised, or is worst-case O(1) required?",
],
"understand":
 "Design a set supporting `insert`, `remove` and `getRandom`, all in average O(1), where "
 "`getRandom` returns a uniformly random current element.\n\n"
 "This is another two-structures-in-tension design. **Uniform random selection in O(1)** "
 "requires a contiguous array, so a random index maps directly to an element &mdash; a hash set "
 "cannot do this, because its internal layout is sparse and unordered, and picking a random "
 "element from one is O(n). **O(1) lookup and deletion by value** requires a hash map, because "
 "finding a value in an array is O(n).\n\n"
 "So again: array plus map, wired together. The array holds the values; the map holds value → "
 "**its index in that array**. The remaining problem is that deleting from the middle of an "
 "array is O(n) because of the shift &mdash; and the trick that resolves it is that the *order* "
 "of the array is irrelevant here. Nothing about the specification cares where an element sits, "
 "so a deleted element can be overwritten by the last element and the array simply truncated.",
"brute_en":
 "Pick one structure and accept that one operation will be slow.\n\n"
 "With a **list only**: `insert` appends in O(1), but must first scan for duplicates in O(n); "
 "`remove` scans for the value and then shifts, O(n); `getRandom` is O(1).\n\n"
 "With a **hash set only**: `insert` and `remove` are O(1), but `getRandom` must materialise "
 "the set into a list or iterate to a random offset, which is O(n).\n\n"
 "Naming both and identifying exactly which operation each one fails is the right way to open "
 "this problem &mdash; it frames the solution as combining them rather than inventing something "
 "new.",
"brute_ds":
 "- Either a single **list**, or a single **hash set**. The point is that neither alone can "
 "satisfy all three operations.",
"brute_algo": [
 "**List-only insert:** scan the list for the value; if present return False, otherwise append and return True. O(n).",
 "**List-only remove:** scan for the value; if absent return False, otherwise remove it, shifting the tail. O(n).",
 "**List-only getRandom:** return `random.choice(self.vals)`. O(1).",
 "**Set-only insert / remove:** direct O(1) hash operations.",
 "**Set-only getRandom:** `random.choice(list(self.data))` &mdash; building the list is O(n) on every single call.",
],
"brute_cx":
 "**List only:** insert O(n), remove O(n), getRandom O(1).\n\n"
 "**Set only:** insert O(1), remove O(1), getRandom O(n).\n\n"
 "**Space: O(n)** either way. Each design nails two of the three requirements and fails the "
 "third, which is exactly the tension the real solution has to resolve.",
"brute_code":
'''import random

class RandomizedSet_list:
    """List only: O(1) random, but O(n) insert and remove."""
    def __init__(self):
        self.vals = []

    def insert(self, val):
        if val in self.vals:              # O(n) scan
            return False
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.vals:          # O(n) scan
            return False
        self.vals.remove(val)             # O(n) shift
        return True

    def getRandom(self):
        return random.choice(self.vals)   # O(1)


class RandomizedSet_set:
    """Set only: O(1) insert and remove, but O(n) getRandom."""
    def __init__(self):
        self.data = set()

    def insert(self, val):
        if val in self.data:
            return False
        self.data.add(val)
        return True

    def remove(self, val):
        if val not in self.data:
            return False
        self.data.remove(val)
        return True

    def getRandom(self):
        return random.choice(list(self.data))   # O(n): rebuilds a list every call''',
"brute_limit":
 "The list fails because locating a value requires a scan and removing from the middle requires "
 "a shift. The set fails because hash tables have no positional index, so uniform sampling "
 "cannot be done in constant time.\n\n"
 "Adding a map on top of the list removes the scan immediately. What remains is the O(n) shift "
 "on deletion &mdash; and that is where the real insight lands: **the array's order carries no "
 "meaning here.** No operation depends on where an element sits. So instead of shifting "
 "everything after the hole, move the *last* element into the hole and shrink the array by one. "
 "That is O(1), and the only bookkeeping needed is updating the moved element's index in the "
 "map.",
"opt_en":
 "Keep a list `vals` of the elements and a map `idx` from value to its index in that list.\n\n"
 "`insert(val)`: return False if the value is already a key. Otherwise record "
 "`idx[val] = len(vals)` and append the value. Both O(1).\n\n"
 "`remove(val)`: return False if the value is absent. Otherwise let `i = idx[val]` and take "
 "`last = vals[-1]`. Write `last` into position `i`, update `idx[last] = i`, pop the final "
 "element, and delete `val` from the map. The array shrinks by one with no shifting.\n\n"
 "`getRandom()`: return `random.choice(vals)`, which is a single uniform index into a "
 "contiguous array.\n\n"
 "The edge case to walk through out loud is **removing the last element**, where `val` and "
 "`last` are the same value. The code writes `idx[last] = i`, which re-adds the key being "
 "removed &mdash; but the subsequent `del self.idx[val]` deletes that same key, since `last == "
 "val`, so the map ends up correct. The order of those two statements is what makes it safe, "
 "and interviewers do probe this case.",
"opt_ds":
 "- A **dynamic array `vals`** holding the elements, giving O(1) uniform random access by "
 "index. This is what a hash set cannot provide.\n"
 "- A **hash map `idx`** from value to its position in `vals`, giving O(1) lookup and O(1) "
 "location for deletion. This is what an array cannot provide.\n"
 "- The **swap-with-last** technique, which exploits the fact that the array's order is "
 "semantically irrelevant. That is the observation the whole design turns on.",
"opt_algo": [
 "Constructor: create an empty list `vals` and an empty dict `idx`.",
 "**insert(val):** if `val` is in `idx`, return False. Otherwise set `idx[val] = len(vals)`, append `val` to `vals`, and return True.",
 "**remove(val):** if `val` is not in `idx`, return False.",
 "Let `i = idx[val]` and `last = vals[-1]`.",
 "Write `vals[i] = last`, filling the hole with the final element instead of shifting everything after it.",
 "Set `idx[last] = i` so the moved element's recorded position stays correct.",
 "Pop the final element of `vals`, then `del idx[val]`. This ordering is what makes the val-is-last case correct.",
 "**getRandom():** return `random.choice(vals)` &mdash; uniform because every element occupies exactly one array slot.",
],
"opt_code":
'''import random

class RandomizedSet:
    """Array for O(1) uniform random access; map for O(1) lookup.
    Deletion is O(1) because the array's ORDER is irrelevant here."""

    def __init__(self):
        self.vals = []                    # the elements, in arbitrary order
        self.idx = {}                     # value -> its index inside self.vals

    def insert(self, val):
        if val in self.idx:
            return False
        self.idx[val] = len(self.vals)    # its index is the current end
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.idx:
            return False
        i = self.idx[val]
        last = self.vals[-1]

        self.vals[i] = last               # move the LAST element into the hole
        self.idx[last] = i                # ...and fix its recorded index
        self.vals.pop()                   # shrink by one -- no shifting at all
        del self.idx[val]

        # Edge case, worth walking through aloud: if val IS the last element,
        # then last == val, so `self.idx[last] = i` re-adds the key -- and the
        # `del self.idx[val]` on the next line removes it again. Correct because
        # the delete comes second.
        return True

    def getRandom(self):
        return random.choice(self.vals)   # uniform: one array slot per element''',
"opt_cx":
 "**Time: O(1) average for all three operations.** Insert is a hash write plus an amortised "
 "O(1) append. Remove is a constant number of hash and array operations with no shifting. "
 "GetRandom is one index into a contiguous array. Hash operations are average-case O(1); "
 "worst-case collision behaviour is O(n), which is worth acknowledging if asked for strict "
 "worst-case bounds.\n\n"
 "**Space: O(n)** for the array and the map.\n\n"
 "**Say this out loud:** \"Uniform random selection in O(1) needs a contiguous array; lookup "
 "and delete by value in O(1) needs a hash map. So I keep both, with the map storing each "
 "value's index in the array. Deleting from the middle would normally be O(n), but the array's "
 "order does not matter here, so I overwrite the hole with the last element, fix that element's "
 "index in the map, and pop. All three operations are O(1).\"\n\n"
 "**Walk the val-is-last case out loud** &mdash; it is the thing interviewers check. **The "
 "follow-up:** problem 381 allows duplicates, which changes the map to value → *set of "
 "indices*, and the same swap-with-last still works, with a little more bookkeeping when the "
 "moved element's index set is updated.",
},

]
