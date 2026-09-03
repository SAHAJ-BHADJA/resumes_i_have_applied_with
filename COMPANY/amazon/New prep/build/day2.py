# -*- coding: utf-8 -*-
"""Day 2 - Round Type B: reduce an O(n^2) solution."""

DAY = "Day 2 · Wed 26 Aug · Round Type B (reduce an O(n²) solution)"

PROBLEMS = [

{
"num": 1, "title": "Two Sum", "stars": "", "day": DAY,
"pattern": "Hash map of complements", "opt_cx_short": "O(n) time, O(n) space",
"clarify": [
 "Is there **exactly one** valid answer guaranteed, or could there be several? If several, do you want any one of them or all of them?",
 "May I use the same element twice? The standard statement says no, and that is what forces the ordering of the lookup and the insert in my code.",
 "Do you want the **indices** or the values? Indices, which rules out sorting the array in place unless I also carry the original positions.",
 "Can the array contain negatives, zeros or duplicates? All three are fine for a hash map, but duplicates are what break a careless implementation.",
 "What should I return if no pair exists &mdash; an empty list?",
],
"understand":
 "Given an array of integers and a target, return the indices of the two numbers that add up "
 "to the target.\n\n"
 "The reframing that makes it trivial: for a fixed element `x`, there is exactly one value "
 "that could pair with it, namely `target - x`. So the question is not \"which two elements "
 "work together\" &mdash; a pairing question, quadratic by nature &mdash; but \"for this `x`, "
 "**have I already seen** its complement?\" That is a membership question, and membership "
 "questions are what hash maps answer in O(1). This is the smallest possible instance of the "
 "pattern that this whole round is about: replace a repeated inner scan with a lookup.",
"brute_en":
 "Try every pair. For each index `i`, walk every index `j` strictly greater than `i` and test "
 "whether `nums[i] + nums[j]` equals the target. Return `[i, j]` on the first hit.\n\n"
 "Starting `j` at `i + 1` rather than 0 does two useful things at once: it prevents pairing an "
 "element with itself, and it avoids examining each unordered pair twice.",
"brute_ds":
 "- None. Two index variables and the input array. This is the baseline against which the "
 "optimisation is measured, and it is worth saying out loud that it uses O(1) extra space, "
 "because that is the one thing the brute force is better at.",
"brute_algo": [
 "Loop `i` from 0 to `n - 1`.",
 "For each `i`, loop `j` from `i + 1` to `n - 1`.",
 "If `nums[i] + nums[j] == target`, return `[i, j]`.",
 "If both loops complete without a match, return an empty list.",
],
"brute_cx":
 "**Time: O(n²).** The inner loop runs n−1 times for the first `i`, n−2 for the "
 "second, and so on, which sums to n(n−1)/2 pair checks &mdash; quadratic. Each check is "
 "O(1).\n\n"
 "**Space: O(1).** Only two loop counters; nothing is stored.",
"brute_code":
'''def twoSum_brute(nums, target):
    """Check every unordered pair exactly once."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):         # j > i: no self-pairing, no repeated pairs
            if nums[i] + nums[j] == target:
                return [i, j]
    return []''',
"brute_limit":
 "For each `i`, the inner loop re-scans the tail of the array asking the same question every "
 "time: \"is the value `target - nums[i]` present?\" That is a membership query being answered "
 "by linear search, over and over, on data that never changes.\n\n"
 "At n = 100,000 this is about 5 × 10⁹ comparisons, which will not run in time. Any "
 "membership query answered by scanning is the signal to reach for a hash map.",
"opt_en":
 "One pass. Keep a dictionary mapping each value already seen to the index where it was seen. "
 "For the current element `x` at index `i`, compute `target - x` and check whether that "
 "complement is already in the dictionary. If it is, I have found the pair immediately and can "
 "return the stored index together with `i`. If it is not, record `x` with its own index and "
 "move on.\n\n"
 "The ordering matters and is worth narrating: I **look up before I insert**. Looking up first "
 "means the dictionary only ever contains elements strictly before `i`, which is exactly what "
 "guarantees I never pair an element with itself. With `nums = [3, 3]` and `target = 6`, the "
 "look-up-first order finds index 0 paired with index 1, while insert-first would match the "
 "single element at index 0 against itself.\n\n"
 "Because the complement of the complement is the original number, one pass is enough: "
 "whichever of the two partners appears second will find the first one waiting in the map.",
"opt_ds":
 "- A **hash map** from value to index. Value-to-index rather than a plain set, because the "
 "problem asks for indices &mdash; a set would tell me the pair exists but not where it is.\n"
 "- If duplicates exist and only one answer is needed, keeping the *first* index of a repeated "
 "value is fine; the look-up-first ordering means the second occurrence finds the first.",
"opt_algo": [
 "Create an empty dictionary `seen`, mapping value → index.",
 "Iterate over the array with both index `i` and value `x`.",
 "Compute `need = target - x`.",
 "If `need` is a key in `seen`, return `[seen[need], i]`. The stored index is strictly smaller than `i`, so the pair is ordered and distinct.",
 "Otherwise set `seen[x] = i`. **This must come after the lookup**, never before.",
 "If the loop ends with no match, return an empty list.",
],
"opt_code":
'''def twoSum(nums, target):
    """One pass, hash map of complements."""
    seen = {}                             # value -> index where we saw it
    for i, x in enumerate(nums):
        need = target - x                 # the ONLY value that can pair with x
        if need in seen:                  # *** look up BEFORE inserting x ***
            return [seen[need], i]        # seen[need] < i, so the pair is distinct
        seen[x] = i
    return []''',
"opt_cx":
 "**Time: O(n).** A single pass, with one O(1) average-case hash lookup and one O(1) insert "
 "per element. Worst-case hashing is O(n) per operation under adversarial collisions, but that "
 "does not occur with ordinary integer keys.\n\n"
 "**Space: O(n).** The map may hold up to n−1 entries before the answer is found. This is "
 "the trade being made: O(n) memory buys an O(n) reduction in time.\n\n"
 "**Say this out loud:** \"The brute force checks every pair, O(n²). The repeated work is "
 "scanning for the complement, and a complement lookup is a membership query, so a hash map "
 "makes it O(1) and the whole algorithm O(n). I look up before inserting so an element can "
 "never pair with itself.\"\n\n"
 "**The gotcha:** the lookup-then-insert ordering, demonstrated with `[3, 3]`. "
 "**The follow-up:** if the array were sorted and only values were needed, two pointers give "
 "O(n) time with O(1) space &mdash; but here the indices are required, so sorting would "
 "destroy the answer unless I first paired every value with its original index.",
},

{
"num": 560, "title": "Subarray Sum Equals K", "stars": "★★", "day": DAY,
"pattern": "Prefix sum + hash map of counts", "opt_cx_short": "O(n) time, O(n) space",
"clarify": [
 "Are the values allowed to be **negative**? This is the decisive question. With negatives, a sliding window is invalid, because extending the window no longer moves the sum monotonically. I want to confirm this before I choose an approach.",
 "Do I count the **number** of subarrays, or return the actual subarrays? Just the count.",
 "Must subarrays be contiguous and non-empty? Yes on both, I assume.",
 "Can `k` be zero or negative? Both are fine for the prefix-sum method.",
 "Can subarrays overlap? Yes &mdash; every distinct index range counts separately.",
],
"understand":
 "Given an integer array and an integer `k`, count how many **contiguous** subarrays sum "
 "exactly to `k`.\n\n"
 "The key algebraic step: let `prefix[i]` be the sum of the first `i` elements. Then the sum of "
 "the subarray from index `i` to index `j` inclusive is `prefix[j+1] - prefix[i]`. Setting "
 "that equal to `k` and rearranging gives `prefix[i] = prefix[j+1] - k`.\n\n"
 "That rearrangement converts the problem completely. Instead of asking \"which ranges sum to "
 "k\", which is quadratic in nature, I fix the right end `j` and ask \"**how many earlier "
 "prefix sums equal `prefix[j+1] - k`?**\" &mdash; a counting-membership question a hash map "
 "answers in O(1). It is Two Sum, applied to prefix sums, counting matches instead of "
 "stopping at the first.",
"brute_en":
 "Enumerate every contiguous subarray and test it. Fix the start index `i`, then extend the end "
 "index `j` rightward, maintaining a running total so each extension costs O(1) rather than "
 "re-summing the range. Every time the running total equals `k`, increment the counter.\n\n"
 "Keeping the running sum is what makes this O(n²) rather than the fully naive O(n³) "
 "version that re-adds the whole range for each pair of endpoints. It is worth mentioning both "
 "in the interview: it shows you already removed one layer of waste before proposing the real "
 "optimisation.",
"brute_ds":
 "- A single running-sum integer and a counter. No auxiliary structure.\n"
 "- Space O(1), which is the brute force's only advantage over the optimal solution.",
"brute_algo": [
 "Set `count = 0`.",
 "Loop `i` from 0 to `n - 1`. This is the start of the subarray.",
 "Set `running = 0`.",
 "Loop `j` from `i` to `n - 1`, adding `nums[j]` to `running`. After the addition, `running` is the sum of the subarray from `i` to `j`.",
 "If `running == k`, increment `count`. Do **not** break: with negative numbers a longer subarray from the same start can also hit `k`.",
 "Return `count`.",
],
"brute_cx":
 "**Time: O(n²).** There are n(n+1)/2 contiguous subarrays and the running sum makes "
 "each one O(1) to evaluate.\n\n"
 "**Space: O(1).** Only two integers.",
"brute_code":
'''def subarraySum_brute(nums, k):
    """Every contiguous subarray, with a running sum so each extension is O(1)."""
    n = len(nums)
    count = 0
    for i in range(n):                    # start of the subarray
        running = 0
        for j in range(i, n):             # extend the end rightward
            running += nums[j]            # sum of nums[i..j], updated in O(1)
            if running == k:
                count += 1                # do NOT break: negatives allow more hits
    return count''',
"brute_limit":
 "The two loops recompute overlapping information constantly: the sum of `nums[2..7]` is "
 "recomputed from scratch when the start moves to 3, even though it differs from "
 "`nums[3..7]` by a single element. Across the array, the same prefix arithmetic is repeated "
 "O(n) times.\n\n"
 "It is also worth stating explicitly why the usual O(n²)-to-O(n) trick, the sliding "
 "window, does **not** apply. A sliding window relies on the window sum increasing when you "
 "extend right and decreasing when you shrink left; with negative numbers neither holds, so "
 "there is no valid rule for when to move `left`. Prefix sums plus a hash map work regardless "
 "of sign, which is exactly why they are the right tool here.",
"opt_en":
 "Sweep left to right maintaining the running prefix sum. Also maintain a dictionary counting "
 "**how many times each prefix-sum value has occurred so far**. At each index, the number of "
 "subarrays ending here that sum to `k` is precisely the number of earlier positions whose "
 "prefix sum equals `running - k`, so I add that stored count to the answer. Then I record the "
 "current prefix sum in the dictionary and continue.\n\n"
 "The dictionary must start containing `{0: 1}`. That entry represents the empty prefix "
 "&mdash; the sum before any element is consumed &mdash; and it is what allows a subarray "
 "that starts at index 0 to be counted. Without it, `nums = [3]` with `k = 3` returns 0 "
 "instead of 1. Forgetting this single line is the classic bug in this problem, so I would say "
 "it aloud as I type it.\n\n"
 "As with Two Sum, the lookup happens before the insert, so a subarray is never matched "
 "against its own endpoint, which would produce a spurious zero-length hit when `k = 0`.",
"opt_ds":
 "- A **hash map from prefix-sum value to a count of occurrences**. A count, not a single "
 "index, because the same prefix sum can occur many times and each occurrence is a distinct "
 "valid subarray start. Using a set here is the second most common bug.\n"
 "- Seeded with `{0: 1}` for the empty prefix.\n"
 "- Two integers: the running sum and the total count.",
"opt_algo": [
 "Create `count` as a dictionary of prefix sum → occurrences, initialised with `count[0] = 1` for the empty prefix.",
 "Set `running = 0` and `total = 0`.",
 "For each value `x` in the array, add `x` to `running`, so `running` is now the prefix sum through the current index.",
 "Add `count[running - k]` to `total`. Every earlier position holding that prefix sum marks the start of a subarray ending here that sums to `k`.",
 "Then increment `count[running]` by one. **After** the lookup, always.",
 "Return `total`.",
],
"opt_code":
'''from collections import defaultdict

def subarraySum(nums, k):
    """sum(i..j) == prefix[j] - prefix[i-1], so for each j count the earlier
    prefixes equal to prefix[j] - k."""
    count = defaultdict(int)
    count[0] = 1                          # *** the empty prefix: without this,
                                          # subarrays starting at index 0 are missed ***
    running = 0
    total = 0
    for x in nums:
        running += x                      # prefix sum through the current index
        total += count[running - k]       # look up BEFORE inserting
        count[running] += 1               # register this prefix for future indices
    return total''',
"opt_cx":
 "**Time: O(n).** One pass, with one O(1) average hash lookup and one O(1) increment per "
 "element.\n\n"
 "**Space: O(n).** In the worst case every prefix sum is distinct and the map holds n+1 "
 "entries.\n\n"
 "**Say this out loud:** \"Because the sum of a range is a difference of two prefix sums, I "
 "rewrite the condition as prefix[j] − prefix[i] = k. Fixing the right endpoint turns it into "
 "counting how many earlier prefixes equal prefix[j] − k, and a hash map of prefix counts "
 "answers that in O(1). One pass, O(n) time, O(n) space.\"\n\n"
 "**The three things to say unprompted:** `count[0] = 1` and why; the map stores counts, not "
 "indices, because a prefix sum can repeat; and sliding window does **not** work here because "
 "negative values break the monotonicity that a window depends on. That last point is often "
 "the real thing being tested.",
},

{
"num": 3, "title": "Longest Substring Without Repeating Characters", "stars": "★★★",
"day": DAY, "pattern": "Sliding window with a last-seen map",
"opt_cx_short": "O(n) time, O(min(n, charset)) space",
"clarify": [
 "Do you want the **length**, or the substring itself? Length, I assume &mdash; if you want the substring I just record the start index too.",
 "Substring means contiguous, as opposed to subsequence?",
 "What is the character set &mdash; lowercase letters, ASCII, or full Unicode? It does not change the algorithm, only the space bound.",
 "Is the empty string a valid input? It should return 0.",
 "Are spaces and symbols ordinary characters here? I will assume yes, nothing is excluded.",
],
"understand":
 "Given a string, find the length of the longest contiguous substring containing no repeated "
 "character.\n\n"
 "This is the archetype of the sliding-window pattern, and every window problem has the same "
 "three parts. **The window** is a contiguous range `[left, right]`. **The validity "
 "condition** is \"no character appears twice inside the window\". **The movement rule** is: "
 "extend `right` unconditionally, and whenever the window becomes invalid, advance `left` "
 "until it is valid again. Because a window that is valid stays valid when you shrink it from "
 "the left, and validity is only ever broken by the newly added right-hand character, this "
 "single pass is enough &mdash; you never need to move `left` backwards.",
"brute_en":
 "Test every substring for distinctness. For each start index `i`, extend the end index `j` "
 "rightward, keeping a set of the characters seen since `i`. The moment `s[j]` is already in "
 "that set, the substring starting at `i` cannot be extended any further, so record the length "
 "`j - i` and break to the next start. Track the maximum across all starts.\n\n"
 "The set makes each extension O(1). The fully naive alternative &mdash; slicing out each "
 "substring and checking `len(set(sub)) == len(sub)` &mdash; is O(n³), and mentioning that "
 "you already avoided it is a good sign.",
"brute_ds":
 "- One **set** of characters, rebuilt from scratch for each start index. Rebuilding it is "
 "precisely the waste.\n"
 "- An integer holding the best length so far.",
"brute_algo": [
 "Set `best = 0`.",
 "Loop `i` from 0 to `n - 1`, the start of the candidate substring.",
 "Create an empty set `seen`.",
 "Loop `j` from `i` to `n - 1`. If `s[j]` is already in `seen`, break: no longer substring starting at `i` can be distinct.",
 "Otherwise add `s[j]` to `seen` and update `best` with `j - i + 1`.",
 "Return `best`.",
],
"brute_cx":
 "**Time: O(n²).** There are n start indices, and for each the inner loop can run to the "
 "end of the string. Set operations are O(1), so the total is quadratic. The slicing version "
 "would be O(n³).\n\n"
 "**Space: O(min(n, c))** where c is the alphabet size, for the set.",
"brute_code":
'''def lengthOfLongestSubstring_brute(s):
    """Every start index, extended until a duplicate appears."""
    n = len(s)
    best = 0
    for i in range(n):
        seen = set()                      # rebuilt from scratch for every i
        for j in range(i, n):
            if s[j] in seen:
                break                     # no longer substring from i can be distinct
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best''',
"brute_limit":
 "When the substring starting at `i` fails at position `j`, the algorithm throws away "
 "everything it learned and restarts at `i + 1` from scratch, re-reading nearly the same "
 "characters. But the failure told me something precise: the only reason `[i, j]` is invalid "
 "is the earlier copy of `s[j]`, so **every** start index at or before that earlier copy is "
 "also doomed. Restarting at `i + 1` ignores that, when I could jump `left` past the "
 "duplicate in one move.\n\n"
 "That is the whole optimisation: replace \"restart the left end at `i + 1`\" with \"advance "
 "the left end only as far as the duplicate forces\", which lets `left` move monotonically "
 "forward across the entire run and never backwards.",
"opt_en":
 "Keep a window `[left, right]` and a dictionary `last` recording the most recent index at "
 "which each character was seen. Move `right` across the string one character at a time. If "
 "the incoming character `ch` has been seen before **and its last occurrence is at or after "
 "`left`** &mdash; that is, it is actually inside the current window &mdash; then the window "
 "is invalid, and I jump `left` to `last[ch] + 1`, which is the nearest position that excludes "
 "the duplicate. Then I update `last[ch]` to `right` and record the window length.\n\n"
 "The condition `last[ch] >= left` is the subtle part and the thing interviewers probe. "
 "Without it, a stale occurrence from far earlier in the string &mdash; already outside the "
 "window &mdash; would drag `left` *backwards*, silently producing lengths that are too large. "
 "With the check, `left` is monotonically non-decreasing, which is also why the algorithm is "
 "linear.\n\n"
 "I would also mention the count-map variant, which is closer to the universal window template: "
 "increment a counter for the incoming character and, while that counter exceeds 1, shrink from "
 "the left. It is slightly slower in the worst case but generalises directly to problems 424 "
 "and 76, so knowing both is worth the extra minute.",
"opt_ds":
 "- A **hash map from character to its last-seen index**. Storing the index rather than a "
 "boolean is what allows `left` to jump straight past the duplicate instead of creeping one "
 "step at a time.\n"
 "- Two integer pointers, `left` and `right`, and a best-length integer.\n"
 "- For the variant: a **count map** of characters currently inside the window.",
"opt_algo": [
 "Create an empty dictionary `last`, and set `left = 0` and `best = 0`.",
 "Iterate `right` over the string, letting `ch = s[right]`.",
 "If `ch` is in `last` **and** `last[ch] >= left`, the duplicate is inside the current window, so set `left = last[ch] + 1`, which is the smallest left endpoint that excludes it.",
 "Set `last[ch] = right`, recording this as the most recent occurrence. This happens whether or not the window moved.",
 "Update `best` with `right - left + 1`, the current window length.",
 "Return `best`.",
 "Note that `left` never decreases, so `right` and `left` each traverse the string once.",
],
"opt_code":
'''def lengthOfLongestSubstring(s):
    """Sliding window; `last` lets the left edge JUMP past a duplicate."""
    last = {}                             # character -> index of its last occurrence
    left = 0
    best = 0
    for right, ch in enumerate(s):
        # *** `last[ch] >= left` is the crux: without it, a stale occurrence
        # from OUTSIDE the window would drag `left` backwards. ***
        if ch in last and last[ch] >= left:
            left = last[ch] + 1           # smallest left that excludes the duplicate
        last[ch] = right                  # always refresh the last-seen index
        best = max(best, right - left + 1)
    return best


from collections import defaultdict

def lengthOfLongestSubstring_v2(s):
    """Count-map variant: closer to the universal window template, and the one
    that generalises to problems 424 and 76."""
    count = defaultdict(int)
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while count[ch] > 1:              # window INVALID: shrink until it is not
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best''',
"opt_cx":
 "**Time: O(n).** `right` advances n times, and `left` only ever moves forward, so across "
 "the whole run the two pointers perform at most 2n moves. Every dictionary operation is O(1).\n\n"
 "**Space: O(min(n, c))** where c is the alphabet size &mdash; the map holds at most one entry "
 "per distinct character, so it is bounded by 26 for lowercase letters or 128 for ASCII.\n\n"
 "**Say this out loud:** \"Sliding window. My map holds the last index of each character. The "
 "window is invalid exactly when the incoming character already sits inside it, and then I jump "
 "left past its previous occurrence, because every start at or before that point is also "
 "invalid. Left never moves backwards, so each pointer crosses the string once: O(n).\"\n\n"
 "**The gotcha to volunteer:** the `last[ch] >= left` guard, with `\"abba\"` as the "
 "demonstration &mdash; at the final `a`, the stale index 0 is outside the window and must be "
 "ignored, or `left` snaps back to 1 and the answer becomes 3 instead of 2.",
},

{
"num": 424, "title": "Longest Repeating Character Replacement", "stars": "★", "day": DAY,
"pattern": "Sliding window with a frequency map", "opt_cx_short": "O(n) time, O(26) space",
"clarify": [
 "Am I replacing **any** character with **any** other uppercase letter, at most `k` times total within the chosen substring?",
 "Is the alphabet restricted to uppercase A&ndash;Z? That is what makes the space O(26) rather than O(n).",
 "Can `k` be 0? Then the answer is the longest run of a single repeated character, which is a good sanity test.",
 "Can `k` exceed the string length? Then the whole string is achievable and the answer is `len(s)`.",
 "Do you want the length only, not the resulting string?",
],
"understand":
 "Given a string of uppercase letters and an integer `k`, I may change at most `k` characters "
 "to any other letter. I must return the length of the longest substring that can be made to "
 "consist of a single repeated character.\n\n"
 "The reframing that turns this into a window problem: for a fixed substring, the best possible "
 "play is obviously to keep whichever character is already most frequent and convert everything "
 "else. So the number of changes required is `window_length - count_of_most_frequent_character`. "
 "The window is therefore **valid** exactly when that quantity is at most `k`, and I want the "
 "longest valid window. Same three-part window structure as problem 3, with a different validity "
 "predicate.",
"brute_en":
 "Check every substring against the validity rule directly. For each start index `i`, extend "
 "the end index `j` rightward while maintaining a frequency count of the characters in "
 "`[i, j]` and the running maximum of those counts. After each extension, evaluate whether "
 "`(j - i + 1) - max_frequency <= k`. If it holds, the substring is achievable and I update "
 "the best length; if it does not, no longer substring from this same start can help either, "
 "so I break to the next start.\n\n"
 "That break is legitimate because extending the window by one character increases the length "
 "by one but can increase the maximum frequency by at most one, so the number of required "
 "changes never decreases as the window grows from a fixed start.",
"brute_ds":
 "- A **frequency map** of 26 letters, rebuilt for each start index.\n"
 "- An integer for the maximum frequency within the current substring, and one for the best "
 "answer so far.",
"brute_algo": [
 "Set `best = 0`.",
 "Loop `i` from 0 to `n - 1`.",
 "Reset an empty frequency map and `max_freq = 0`.",
 "Loop `j` from `i` to `n - 1`. Increment the count for `s[j]` and update `max_freq` with it.",
 "Compute `window = j - i + 1` and `changes_needed = window - max_freq`.",
 "If `changes_needed <= k`, update `best` with `window`. Otherwise break out to the next start index.",
 "Return `best`.",
],
"brute_cx":
 "**Time: O(n²).** n start indices, each extending up to n positions, with O(1) work per "
 "extension because the frequency map is updated incrementally rather than recomputed. "
 "Recomputing the counts for each substring instead would make it O(n² · 26).\n\n"
 "**Space: O(26) = O(1).** One fixed-size frequency map, discarded and rebuilt per start.",
"brute_code":
'''def characterReplacement_brute(s, k):
    """Every start index, extended while the window stays achievable."""
    from collections import defaultdict
    n = len(s)
    best = 0
    for i in range(n):
        count = defaultdict(int)          # rebuilt for every start index
        max_freq = 0
        for j in range(i, n):
            count[s[j]] += 1
            max_freq = max(max_freq, count[s[j]])
            window = j - i + 1
            # keep the most common char, change all the others
            if window - max_freq <= k:
                best = max(best, window)
            else:
                break                     # from this start, longer is only worse
    return best''',
"brute_limit":
 "When the window from `i` becomes unachievable, the algorithm discards the entire frequency "
 "map and rebuilds it from `i + 1`, re-reading almost the same characters. But moving the start "
 "forward by one only removes a single character from the window &mdash; the counts for "
 "everything else are unchanged and were already correct.\n\n"
 "So instead of restarting, I should keep the same map and simply decrement the count of the "
 "character leaving on the left. That makes `left` move forward monotonically across the whole "
 "string, and both pointers together do O(n) work rather than O(n²).",
"opt_en":
 "Maintain one window and one frequency map for the entire pass. Extend `right`, incrementing "
 "the count of the incoming character and updating `max_freq`. If the window is now invalid "
 "&mdash; `(right - left + 1) - max_freq > k` &mdash; advance `left` by one, decrementing the "
 "count of the outgoing character. Record the best window length at each step.\n\n"
 "Now the famous subtlety, which interviewers reliably probe: **`max_freq` is never "
 "decreased**, even after characters leave the window, so it can become stale and overstate the "
 "true maximum frequency. This is deliberate and it is safe. A stale, too-large `max_freq` "
 "makes the validity test *easier* to pass, so the window can never be wrongly shrunk; the "
 "worst that happens is the window fails to grow for a while. And crucially, `best` can only "
 "ever be updated by a window that is at least as long as the previous best, and to beat the "
 "previous best the window must at some point have contained a genuinely higher character "
 "frequency. So the recorded answer is always achievable, and the true optimum is always found.\n\n"
 "I would present the `while` form rather than the `if` form. Both give the correct answer "
 "here, but `while` is the honest sliding-window template and it keeps the invariant \"the "
 "window is always valid at the bottom of the loop\", which is easier to defend.",
"opt_ds":
 "- A **frequency map over the 26 uppercase letters**, maintained incrementally across the "
 "entire pass rather than per start index. This is the single change from the brute force.\n"
 "- Two pointers, `left` and `right`.\n"
 "- Two integers: `max_freq`, intentionally never decremented, and `best`.",
"opt_algo": [
 "Create an empty frequency map. Set `left = 0`, `best = 0`, `max_freq = 0`.",
 "Iterate `right` over the string with `ch = s[right]`.",
 "Increment `count[ch]`, then update `max_freq = max(max_freq, count[ch])`.",
 "While `(right - left + 1) - max_freq > k`, the window needs more than `k` replacements, so decrement `count[s[left]]` and advance `left` by one.",
 "Update `best` with `right - left + 1`, which is now guaranteed to be a valid window length.",
 "Return `best`.",
 "Do not decrement `max_freq` when a character leaves. Be ready to explain why that is safe rather than a bug.",
],
"opt_code":
'''from collections import defaultdict

def characterReplacement(s, k):
    """A window is achievable when (length - most_frequent_count) <= k, because
    you keep the most frequent character and replace everything else."""
    count = defaultdict(int)
    left = 0
    best = 0
    max_freq = 0                          # deliberately NEVER decreased -- see below

    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])

        # INVALID: this window would need more than k replacements.
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best

# Why a stale max_freq is safe, not a bug:
#   A too-large max_freq only makes the validity test EASIER to pass, so the
#   window is never shrunk when it should not be. And `best` can only grow when
#   the window is genuinely longer than before, which requires a real character
#   frequency at least that high to have occurred. So the answer stays correct.''',
"opt_cx":
 "**Time: O(n).** `right` advances n times; `left` only moves forward and therefore advances "
 "at most n times in total. Every map operation is O(1).\n\n"
 "**Space: O(26) = O(1).** The frequency map holds at most one entry per uppercase letter, "
 "independent of the input size.\n\n"
 "**Say this out loud:** \"Sliding window. My map holds character frequencies inside the "
 "window. The window is valid when its length minus the highest frequency is at most k, "
 "because that difference is exactly how many characters I would have to replace. Both pointers "
 "move forward only, so O(n) time and O(26) space.\"\n\n"
 "**Have the `max_freq` defence ready before they ask** &mdash; volunteering it is one of the "
 "highest-signal things you can do on this problem, because it demonstrates you understand why "
 "the code is correct rather than having memorised it.",
},

{
"num": 15, "title": "3Sum", "stars": "★", "day": DAY,
"pattern": "Sort + two pointers, with dedup at two levels",
"opt_cx_short": "O(n²) time, O(1) extra space",
"clarify": [
 "The output should be **unique triplets by value**, not by index? That is the entire difficulty of this problem, so I want it confirmed.",
 "May I **sort the input**? Sorting is what makes the two-pointer scan possible, and it destroys the original indices &mdash; but since the answer is values, not indices, that is fine.",
 "Can the array contain duplicates, and can the same value be used more than once if it appears more than once? For example, does `[0, 0, 0]` yield `[[0,0,0]]`?",
 "Does the order of the triplets in the output matter, or the order within a triplet?",
 "Is the target always zero, or should I write it for a general target so it extends to 3Sum Closest and 4Sum?",
],
"understand":
 "Given an integer array, return all unique triplets `[a, b, c]` with `a + b + c == 0`, where "
 "no triplet may be a duplicate of another by value.\n\n"
 "There are two distinct sub-problems here, and conflating them is why this question has such a "
 "high failure rate. The first is **finding** the triplets efficiently. The second is "
 "**deduplicating** the results. Sorting solves both at once: once sorted, fixing the first "
 "element reduces the rest to Two Sum on a sorted array, which two pointers solve in linear "
 "time and constant space; and equal values become adjacent, so duplicates can be skipped by "
 "comparing against the immediate neighbour. But the skipping has to happen at **both** levels "
 "&mdash; the fixed element and the pair &mdash; and forgetting the second is the classic bug.",
"brute_en":
 "Three nested loops over all index triples `i < j < l`, testing whether the three values sum "
 "to zero. To handle uniqueness, sort each qualifying triplet's values and put the resulting "
 "tuple into a set, so that different index combinations producing the same three values "
 "collapse to one entry. At the end, convert the set back into a list of lists.\n\n"
 "The index ordering `i < j < l` guarantees each element is used at most once per triplet and "
 "that each combination is examined only once.",
"brute_ds":
 "- A **set of sorted value tuples**, used solely for deduplication. Tuples because they are "
 "hashable; sorted so that `(−1, 0, 1)` and `(0, −1, 1)` collapse to one key.\n"
 "- Three loop indices.",
"brute_algo": [
 "Create an empty set `found`.",
 "Loop `i` from 0 to `n - 3`.",
 "Loop `j` from `i + 1` to `n - 2`.",
 "Loop `l` from `j + 1` to `n - 1`.",
 "If `nums[i] + nums[j] + nums[l] == 0`, build the tuple `tuple(sorted((nums[i], nums[j], nums[l])))` and add it to `found`. Sorting inside the tuple is what makes equal-valued triplets hash to the same key.",
 "Return `[list(t) for t in found]`.",
],
"brute_cx":
 "**Time: O(n³).** Three nested loops give roughly n³/6 triples, each tested in O(1) "
 "plus an O(3 log 3) = O(1) sort of three elements.\n\n"
 "**Space: O(number of unique triplets)** for the set, which can itself be O(n²) in the "
 "worst case.\n\n"
 "At n = 3000 this is on the order of 4.5 × 10⁹ iterations, far past any time limit.",
"brute_code":
'''def threeSum_brute(nums):
    """All index triples i < j < l, deduplicated through a set of sorted tuples."""
    n = len(nums)
    found = set()
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for l in range(j + 1, n):
                if nums[i] + nums[j] + nums[l] == 0:
                    # sorted() so (-1,0,1) and (0,-1,1) collapse to one key
                    found.add(tuple(sorted((nums[i], nums[j], nums[l]))))
    return [list(t) for t in found]''',
"brute_limit":
 "The innermost loop is a linear search for the value `-(nums[i] + nums[j])`, repeated for "
 "every pair, over unsorted data that reveals nothing about where that value might be. That is "
 "the same inefficiency as Two Sum, one level deeper.\n\n"
 "The deduplication is also being handled after the fact, by hashing every result. That works "
 "but it means doing all the wasted work first and cleaning up afterwards, and it costs "
 "O(n²) memory in the worst case.\n\n"
 "Sorting fixes both problems at once. On a sorted array the inner search becomes a two-pointer "
 "sweep that is linear rather than quadratic, and duplicates become adjacent so they can be "
 "skipped *before* the work is done rather than filtered out afterwards.",
"opt_en":
 "Sort the array first. Then fix the leftmost element at index `i` and solve Two Sum on the "
 "sorted remainder with two pointers: `lo` just after `i`, `hi` at the end. Compute the sum of "
 "the three. If it is too small, the only way to increase it is to move `lo` right; if it is "
 "too large, move `hi` left; if it is exactly zero, record the triplet and move both inward.\n\n"
 "Two dedup rules, and both are required. At the **outer** level, if `nums[i]` equals "
 "`nums[i-1]` then every triplet using this value as the fixed element was already generated, "
 "so skip it. At the **inner** level, after recording a hit, advance `lo` past any run of equal "
 "values, otherwise the identical triplet is emitted once per duplicate.\n\n"
 "One more early exit worth including: because the array is sorted, once `nums[i] > 0` every "
 "remaining element is positive and no three of them can sum to zero, so the loop can break "
 "entirely.\n\n"
 "This structure generalises cleanly: 4Sum is the same idea with one more fixed level, and "
 "3Sum Closest is the same sweep tracking the minimum absolute difference instead of exact "
 "equality.",
"opt_ds":
 "- The **sorted array itself** &mdash; sorting is the enabling step, providing both the "
 "ordering that makes two pointers valid and the adjacency that makes dedup a neighbour "
 "comparison.\n"
 "- Two integer pointers, `lo` and `hi`. No hash set is needed, which is why the extra space "
 "is O(1) rather than O(n²).\n"
 "- The output list.",
"opt_algo": [
 "Sort `nums` ascending.",
 "Loop `i` from 0 to `n - 3`.",
 "If `nums[i] > 0`, break. The array is sorted, so all remaining values are positive and cannot sum to zero.",
 "If `i > 0` and `nums[i] == nums[i - 1]`, continue &mdash; this is the **outer** dedup, skipping a fixed value already fully processed.",
 "Set `lo = i + 1` and `hi = n - 1`.",
 "While `lo < hi`, compute `s = nums[i] + nums[lo] + nums[hi]`.",
 "If `s < 0`, increment `lo` to increase the sum. If `s > 0`, decrement `hi` to decrease it.",
 "If `s == 0`, append the triplet, then increment `lo` once and, while `lo < hi` and `nums[lo] == nums[lo - 1]`, keep incrementing &mdash; this is the **inner** dedup. Then decrement `hi` once.",
 "Return the result list.",
],
"opt_code":
'''def threeSum(nums):
    """Sort, fix the first element, two-pointer the rest. Dedup at BOTH levels."""
    nums.sort()
    res = []
    n = len(nums)

    for i in range(n - 2):
        if nums[i] > 0:
            break                          # sorted: everything left is positive
        if i > 0 and nums[i] == nums[i - 1]:
            continue                       # DEDUP LEVEL 1: the fixed element

        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1                    # too small -> need a bigger value
            elif s > 0:
                hi -= 1                    # too big -> need a smaller value
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                # DEDUP LEVEL 2: skip the run of equal values at `lo`,
                # otherwise the same triplet is emitted once per duplicate.
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                hi -= 1

    return res''',
"opt_cx":
 "**Time: O(n²).** The sort is O(n log n), then the outer loop runs n times and each inner "
 "two-pointer sweep is O(n) because `lo` and `hi` only ever move toward each other. "
 "O(n log n) + O(n²) = O(n²).\n\n"
 "**Space: O(1) extra**, ignoring the output list and whatever the sort uses internally "
 "(O(log n) for Timsort's stack, or O(n) if you must not modify the input and copy it first).\n\n"
 "**Say this out loud:** \"Sorting buys me two things: the two-pointer sweep becomes valid, so "
 "the inner search drops from O(n) hashing to O(n) scanning with no extra memory, and equal "
 "values become adjacent so I can dedup by comparing with the neighbour. Fix one element, "
 "two-pointer the rest: O(n²).\"\n\n"
 "**This is the number-one dedup-bug problem in the set.** Solve it twice, and each time say "
 "\"outer dedup\" and \"inner dedup\" aloud as you type each line. `[0, 0, 0, 0]` and "
 "`[-2, 0, 0, 2, 2]` are the two test cases that catch a missing skip.",
},

{
"num": 42, "title": "Trapping Rain Water", "stars": "★★", "day": DAY,
"pattern": "Two pointers with running maxima (also: monotonic stack)",
"opt_cx_short": "O(n) time, O(1) space",
"clarify": [
 "Each bar has width 1, and the elevation map is non-negative integers?",
 "I return the **total** units of water trapped, not the shape or per-column amounts?",
 "Can the array be empty or of length 1 or 2? Any of those trap zero water, since water needs a wall on both sides.",
 "Are there constraints that would make an O(n) space solution unacceptable? I have an O(1) space version and I will lead with it, but I want to know if that matters to you.",
 "Water can only rest between bars, not run off the ends?",
],
"understand":
 "Given an elevation map where the width of each bar is 1, compute how much rainwater is "
 "trapped after it rains.\n\n"
 "The single observation the entire problem rests on: **the water sitting above index `i` "
 "depends only on `i`, not on the shape of the terrain between it and the walls.** Column `i` "
 "holds `min(max_to_the_left, max_to_the_right) - height[i]` units, because water rises until "
 "it would spill over the shorter of the two enclosing walls. If that quantity is negative, the "
 "bar is taller than one of its walls and it holds nothing.\n\n"
 "Once that formula is stated, every solution to this problem is just a different strategy for "
 "obtaining the two maxima: recompute them (brute force), precompute them into arrays (DP), or "
 "derive them on the fly with two converging pointers (optimal).",
"brute_en":
 "Apply the formula literally, one index at a time. For each index `i`, scan leftward from `i` "
 "to find the tallest bar at or before it, then scan rightward to find the tallest bar at or "
 "after it. Take the smaller of the two, subtract `height[i]`, and add the result to the total "
 "if it is positive.\n\n"
 "This is transparently correct because it is a direct translation of the water-level formula, "
 "which makes it an excellent thing to state first: it establishes the formula, and everything "
 "after it is an optimisation of *how the maxima are obtained*, not a new idea.",
"brute_ds":
 "- None. Two local integers per index for the left and right maxima, and a running total.\n"
 "- Space O(1), which is genuinely as good as the optimal solution &mdash; only the time is bad.",
"brute_algo": [
 "Set `water = 0`.",
 "Loop `i` from 0 to `n - 1`.",
 "Scan `j` from 0 to `i` inclusive, tracking the maximum height. Call it `left_max`.",
 "Scan `j` from `i` to `n - 1` inclusive, tracking the maximum height. Call it `right_max`.",
 "Add `min(left_max, right_max) - height[i]` to `water`. Including `i` itself in both scans means this quantity is never negative, so no clamp is needed.",
 "Return `water`.",
],
"brute_cx":
 "**Time: O(n²).** Each of the n indices performs two scans that together cover the whole "
 "array, so roughly n work per index.\n\n"
 "**Space: O(1).** Only a few integers.",
"brute_code":
'''def trap_brute(height):
    """water[i] = min(maxLeft[i], maxRight[i]) - height[i], computed by rescanning."""
    n = len(height)
    water = 0
    for i in range(n):
        left_max = 0
        for j in range(i + 1):            # tallest bar at or left of i
            left_max = max(left_max, height[j])
        right_max = 0
        for j in range(i, n):             # tallest bar at or right of i
            right_max = max(right_max, height[j])
        # both scans include i itself, so this is never negative
        water += min(left_max, right_max) - height[i]
    return water''',
"brute_limit":
 "The left maximum at index `i` differs from the left maximum at `i - 1` by at most one "
 "comparison &mdash; it is `max(previous_left_max, height[i])` &mdash; yet the brute force "
 "recomputes it from index 0 every single time. The same is true on the right. It is "
 "recomputing prefix and suffix maxima that could each be built in one pass.\n\n"
 "The first fix is the obvious one: precompute two arrays, `left_max` and `right_max`, in two "
 "linear sweeps, then combine them in a third. That is O(n) time but costs O(n) space, and it "
 "is worth presenting as the intermediate step.\n\n"
 "The second fix removes the arrays too. The formula only needs `min(left_max, right_max)`, "
 "and if I know that one side's maximum is already smaller than the other's, that side alone "
 "determines the water level &mdash; I never need the other side's exact value. That "
 "observation is what makes two converging pointers work in O(1) space.",
"opt_en":
 "**The two-pointer solution, the one to present.** Start `lo` at the left end and `hi` at the "
 "right, tracking `left_max` and `right_max` as the tallest bars seen so far from each side. "
 "At each step, compare the two maxima and process the **smaller** side.\n\n"
 "The reason this is valid: suppose `left_max < right_max`. Then for the position just right of "
 "`lo`, whatever the true right-hand maximum turns out to be, it is at least `right_max`, which "
 "is already greater than `left_max`. So `min(true_left, true_right)` is determined entirely by "
 "the left side, and I can safely add `left_max - height[lo]` without knowing anything more "
 "about the right. Symmetrically when the right side is smaller. Each step advances one "
 "pointer, so the pointers meet after n steps.\n\n"
 "**The monotonic-stack alternative, worth mentioning.** Keep a stack of indices with "
 "decreasing heights. When a bar arrives that is taller than the top of the stack, that bar and "
 "the element below the popped index form the two walls of a horizontal basin whose floor is "
 "the popped bar. Compute `width × depth` for that layer and add it. The two versions fill "
 "water in different directions, and saying that difference out loud is the most memorable "
 "thing you can say about this problem: **the stack fills water horizontally, layer by layer; "
 "the two-pointer version fills it vertically, column by column.**",
"opt_ds":
 "- **Two pointers plus two running maxima** &mdash; four integers, no arrays. O(1) space.\n"
 "- The intermediate DP version instead uses **two arrays of length n**, `left_max` and "
 "`right_max`; same time, O(n) space. Present it as the stepping stone.\n"
 "- The alternative uses a **monotonic decreasing stack of indices**, O(n) space, which is the "
 "same structure as problem 239 and the Largest Rectangle in Histogram family.",
"opt_algo": [
 "Return 0 if the array is empty.",
 "Set `lo = 0`, `hi = n - 1`, `left_max = height[lo]`, `right_max = height[hi]`, `water = 0`.",
 "While `lo < hi`: compare `left_max` and `right_max`.",
 "If `left_max < right_max`, the left wall is the binding constraint, so advance `lo` by one, update `left_max` with the new bar, and add `left_max - height[lo]` to `water`. This is non-negative because `left_max` was just updated to include `height[lo]`.",
 "Otherwise advance `hi` by one to the left, update `right_max`, and add `right_max - height[hi]`.",
 "When the pointers meet, return `water`.",
 "For the stack version: iterate over indices; while the stack is non-empty and the current bar is taller than the bar at the stack top, pop that index as the basin floor, and if the stack is now empty break because there is no left wall; otherwise compute `width = i - stack[-1] - 1` and `depth = min(height[stack[-1]], h) - height[floor]`, and add their product. Push the current index.",
],
"opt_code":
'''def trap(height):
    """WAY A -- two pointers, O(1) space. Process whichever side has the SMALLER
    running maximum: that side alone determines the water level there."""
    if not height:
        return 0

    lo, hi = 0, len(height) - 1
    left_max, right_max = height[lo], height[hi]
    water = 0

    while lo < hi:
        if left_max < right_max:
            # The right side already guarantees a wall taller than left_max,
            # so the level here is fixed by the left side alone.
            lo += 1
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]      # never negative
        else:
            hi -= 1
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]

    return water


def trap_stack(height):
    """WAY B -- monotonic decreasing stack of indices. Fills water in horizontal
    layers instead of vertical columns."""
    stack = []                            # indices, heights decreasing
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()          # the floor of this basin
            if not stack:
                break                     # no left wall -> nothing can be trapped
            left = stack[-1]              # left wall
            width = i - left - 1
            depth = min(height[left], h) - height[bottom]
            water += width * depth        # one horizontal layer
        stack.append(i)
    return water


def trap_dp(height):
    """The intermediate step worth naming: precompute both maxima. O(n) time,
    O(n) space -- the version the two-pointer solution improves on."""
    if not height:
        return 0
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))''',
"opt_cx":
 "**Time: O(n)** for all three optimal variants. The two-pointer version advances exactly one "
 "pointer per iteration and the pointers meet after n steps. The stack version pushes and pops "
 "each index at most once. The DP version makes three linear passes.\n\n"
 "**Space: O(1)** for two pointers, **O(n)** for the stack, **O(n)** for the DP arrays. Lead "
 "with the two-pointer version precisely because of that column.\n\n"
 "**Say this out loud:** \"Water above column i is min of the left and right maxima, minus the "
 "column height. The brute force recomputes those maxima, which is O(n²). Two pointers "
 "derive them on the fly: I always advance the side with the smaller running maximum, because "
 "the other side is already guaranteed to be at least that tall, so the level there is fully "
 "determined. O(n) time, O(1) space.\"\n\n"
 "**Budget 45 minutes for this one in practice**, and finish by naming the difference between "
 "the two methods &mdash; horizontal layers versus vertical columns. That sentence is what "
 "interviewers remember.",
},

{
"num": 76, "title": "Minimum Window Substring", "stars": "★★★  (stretch)", "day": DAY,
"pattern": "Sliding window with have/need satisfaction counters",
"opt_cx_short": "O(|s| + |t|) time, O(|s| + |t|) space",
"clarify": [
 "Does `t` have **multiplicity** &mdash; if `t` is `\"aab\"`, must the window contain at least two `a`s?  That is the detail that decides the data structure.",
 "If several minimum windows tie in length, may I return any of them, or specifically the leftmost?",
 "If no valid window exists, I return the empty string?",
 "May the window contain extra characters not in `t`? Yes, it need only *contain* `t`, not equal it.",
 "Are `s` and `t` case-sensitive, and can `t` be longer than `s`, in which case the answer is immediately empty?",
],
"understand":
 "Given strings `s` and `t`, return the shortest substring of `s` that contains every character "
 "of `t` including repeats, or the empty string if there is none.\n\n"
 "This is the hardest member of the sliding-window family, and the reason is the validity test. "
 "Naively, checking whether the window contains all of `t` means comparing two frequency maps, "
 "which is O(alphabet) on every single step. The idea that fixes it is to track "
 "**satisfaction** rather than raw counts: keep an integer `have` counting *how many distinct "
 "characters of `t` currently meet or exceed their required quota*, and a constant "
 "`need_count` equal to the number of distinct characters in `t`. The window is valid exactly "
 "when `have == need_count`, which is an O(1) test.\n\n"
 "The window then follows the standard two-phase rhythm: grow the right edge until valid, then "
 "shrink the left edge while it stays valid, recording the best length each time.",
"brute_en":
 "Generate every substring of `s` and test each one. For each start index `i`, extend the end "
 "index `j`, maintaining a frequency map of the window's characters, and after each extension "
 "check whether the window covers `t` &mdash; that is, whether for every character in `t` the "
 "window's count is at least the required count. The first `j` at which the window becomes "
 "valid gives the shortest valid window for that start, so record its length and break to the "
 "next start. Track the global minimum.\n\n"
 "Breaking at the first valid `j` is a legitimate optimisation: extending further from the same "
 "start can only make the window longer, never shorter.",
"brute_ds":
 "- A **frequency map of the required characters** built once from `t`.\n"
 "- A **frequency map of the current window**, rebuilt for each start index.\n"
 "- Integers tracking the best length and the best start position.",
"brute_algo": [
 "Build `need`, the frequency map of `t`. If `t` is empty or longer than `s`, return the empty string.",
 "Set `best_len` to infinity and `best_start` to 0.",
 "Loop `i` from 0 to `n - 1`, resetting an empty `window` map.",
 "Loop `j` from `i` to `n - 1`, incrementing `window[s[j]]`.",
 "Test coverage: for every character `c` in `need`, check `window.get(c, 0) >= need[c]`. This costs O(distinct characters in t).",
 "If covered, and `j - i + 1 < best_len`, record `best_len` and `best_start = i`, then break to the next `i`.",
 "Return the empty string if `best_len` is still infinity, otherwise the slice of length `best_len` starting at `best_start`.",
],
"brute_cx":
 "**Time: O(|s|² · |t|).** There are O(|s|²) substrings, and each coverage test costs "
 "up to the number of distinct characters in `t`. Rebuilding the window map from scratch for "
 "each start adds another factor if done carelessly.\n\n"
 "**Space: O(|s| + |t|)** for the two frequency maps.",
"brute_code":
'''def minWindow_brute(s, t):
    """Every substring, tested for coverage. O(|s|^2 * |t|)."""
    from collections import Counter
    if not s or not t or len(t) > len(s):
        return ""

    need = Counter(t)
    n = len(s)
    best_len = float('inf')
    best_start = 0

    for i in range(n):
        window = {}                       # rebuilt for every start index
        for j in range(i, n):
            window[s[j]] = window.get(s[j], 0) + 1
            # full coverage check -- O(distinct chars in t) EVERY step
            if all(window.get(c, 0) >= need[c] for c in need):
                if j - i + 1 < best_len:
                    best_len = j - i + 1
                    best_start = i
                break                     # shortest window for THIS start
    return "" if best_len == float('inf') else s[best_start:best_start + best_len]''',
"brute_limit":
 "Two layers of waste. The window map is discarded and rebuilt for every start index, even "
 "though moving the start forward by one only removes a single character. And the coverage "
 "test walks all of `t`'s distinct characters on every single extension, re-deriving a fact "
 "that changes by at most one character per step.\n\n"
 "Both are fixed by tracking a **derivative** instead of recomputing a **state**. Rather than "
 "asking \"is this window covered?\" from scratch, maintain a counter of how many required "
 "characters are currently satisfied, and update it by ±1 exactly when a character crosses "
 "its required quota. Coverage then becomes a single integer comparison, and the window map "
 "survives across the whole pass rather than being rebuilt.",
"opt_en":
 "Two pointers, one pass. Maintain `need`, the frequency map of `t`; `window`, the frequency "
 "map of the current window; `need_count`, the number of distinct characters in `t`; and "
 "`have`, how many of those are currently satisfied.\n\n"
 "Extend `right`, incrementing `window[ch]`. If `ch` is required and its window count has just "
 "become **exactly equal** to its required count, increment `have` &mdash; that character is "
 "now satisfied. The equality is essential: using `>=` would increment `have` again on every "
 "additional copy and permanently corrupt the count.\n\n"
 "While `have == need_count` the window is valid, so shrink from the left: record the length if "
 "it beats the best, then remove `s[left]` from the window and advance `left`. If the removed "
 "character was required and its count has **dropped below** its requirement, decrement `have`, "
 "which ends the shrinking phase. The condition here is strictly `<`, not `<=`, for the "
 "symmetric reason.\n\n"
 "Record `best_start` and `best_len` rather than materialising the substring inside the loop; "
 "slicing on every improvement would add an O(|s|) cost inside an O(|s|) loop.",
"opt_ds":
 "- A **`Counter` of `t`** giving the required multiplicity of each character.\n"
 "- A **frequency map of the window**, maintained incrementally for the whole pass.\n"
 "- Two integers, `have` and `need_count`, which reduce the validity test from O(alphabet) to "
 "O(1). This is the core idea of the problem.\n"
 "- Two integers `best_len` and `best_start`, so the result is sliced exactly once at the end.",
"opt_algo": [
 "Return the empty string if either `s` or `t` is empty.",
 "Build `need = Counter(t)` and set `need_count = len(need)`, the number of **distinct** required characters.",
 "Initialise `window = {}`, `have = 0`, `left = 0`, `best_len = infinity`, `best_start = 0`.",
 "Iterate `right` over `s` with `ch = s[right]`. Increment `window[ch]`.",
 "If `ch` is in `need` and `window[ch] == need[ch]` exactly, increment `have`.",
 "While `have == need_count`: if the current window is shorter than `best_len`, update `best_len` and `best_start`.",
 "Then let `out = s[left]`, decrement `window[out]`, and if `out` is in `need` and `window[out] < need[out]`, decrement `have`, which will exit the shrink loop.",
 "Advance `left` by one and repeat the while test.",
 "After the main loop, return the empty string if `best_len` is still infinity, otherwise `s[best_start : best_start + best_len]`.",
],
"opt_code":
'''from collections import Counter

def minWindow(s, t):
    """Track SATISFACTION (have vs need_count), not raw counts, so the validity
    test is O(1) instead of O(alphabet)."""
    if not t or not s:
        return ""

    need = Counter(t)
    need_count = len(need)                # number of DISTINCT chars still to satisfy
    window = {}
    have = 0
    left = 0
    best_len = float('inf')
    best_start = 0

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        # *** == not >= : otherwise every extra copy re-increments `have` ***
        if ch in need and window[ch] == need[ch]:
            have += 1

        while have == need_count:         # VALID -> try to shrink from the left
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left         # store the index; slice once at the end

            out = s[left]
            window[out] -= 1
            # *** < not <= : we only lose satisfaction when we drop BELOW need ***
            if out in need and window[out] < need[out]:
                have -= 1                 # window just became invalid; stop shrinking
            left += 1

    return "" if best_len == float('inf') else s[best_start:best_start + best_len]''',
"opt_cx":
 "**Time: O(|s| + |t|).** Building `need` is O(|t|). In the main loop `right` advances |s| "
 "times and `left` only moves forward, so at most |s| times overall; every operation inside is "
 "O(1) because the validity test is an integer comparison.\n\n"
 "**Space: O(|s| + |t|)** for the two maps, bounded in practice by the alphabet size.\n\n"
 "**Say this out loud:** \"Sliding window, but the trick is what I track. Comparing two "
 "frequency maps on every step would be O(alphabet); instead I keep a count of how many "
 "required characters are currently satisfied, and I only change it when a character crosses "
 "its quota. That makes validity O(1), so the whole thing is linear.\"\n\n"
 "**The three gotchas, all worth stating before you type them:** `== need[ch]` on the way in, "
 "not `>=`; `< need[out]` on the way out, not `<=`; and store `best_start` rather than slicing "
 "inside the loop.",
},

{
"num": 239, "title": "Sliding Window Maximum", "stars": "★★  (stretch)", "day": DAY,
"pattern": "Monotonic decreasing deque of indices",
"opt_cx_short": "O(n) time, O(k) space",
"clarify": [
 "The window has fixed size `k` and slides one position at a time, so the output has `n - k + 1` entries?",
 "Is `k` guaranteed to be between 1 and `n`? If `k` is 1 the answer is the array itself, which is a useful sanity check.",
 "Can the values be negative or duplicated? Duplicates matter for whether I pop on `<` or `<=`, so I want to be explicit about that.",
 "Do you want the maximum values themselves, or their indices?",
 "Is a heap-based O(n log n) acceptable, or are you looking for the O(n) solution? I will go straight for O(n) but I will mention the heap as the intermediate step.",
],
"understand":
 "Given an array and a window size `k`, return the maximum of every contiguous window of size "
 "`k` as the window slides from left to right.\n\n"
 "The insight that makes a linear solution possible is a **dominance** argument. Suppose index "
 "`j` is to the right of index `i` and `nums[j] >= nums[i]`. Then `nums[i]` can never again be "
 "the maximum of any window: any future window containing `i` must also contain `j`, since `j` "
 "is further right and windows only move right, and `j` holds a value at least as large. So "
 "`nums[i]` is permanently useless and can be discarded the moment `j` arrives.\n\n"
 "Discarding dominated elements leaves behind a sequence of indices whose values are strictly "
 "decreasing, with the current window maximum always at the front. That structure is a "
 "**monotonic deque**, and it needs both ends: new elements are compared and appended at the "
 "back, while indices that slide out of the window are removed at the front.",
"brute_en":
 "For each of the `n - k + 1` window positions, scan all `k` elements of that window and take "
 "the largest. Append it to the output and slide one position right.\n\n"
 "Directly correct and trivial to write, which makes it a good thing to state in one sentence "
 "before immediately noting its cost. The intermediate improvement worth naming is a max-heap "
 "of `(value, index)` pairs with lazy deletion: push each new element, and before reading the "
 "top, pop any entries whose index has fallen out of the window. That gets to O(n log n) but "
 "still is not linear.",
"brute_ds":
 "- None beyond the output list. A nested loop and a local maximum.\n"
 "- The heap variant would add a max-heap holding up to n entries.",
"brute_algo": [
 "Return an empty list if the array is empty or `k` is 0.",
 "Loop `i` from 0 to `n - k` inclusive; this is the start of each window.",
 "Set `best` to the smallest possible value.",
 "Loop `j` from `i` to `i + k - 1`, updating `best` with `nums[j]`.",
 "Append `best` to the output.",
 "Return the output.",
],
"brute_cx":
 "**Time: O(n · k).** There are n − k + 1 windows and each is scanned in full. When "
 "`k` is proportional to `n` &mdash; for example k = n/2 &mdash; this is O(n²).\n\n"
 "**Space: O(1)** beyond the required output.",
"brute_code":
'''def maxSlidingWindow_brute(nums, k):
    """Rescan every window from scratch. O(n*k)."""
    n = len(nums)
    if n == 0 or k == 0:
        return []
    out = []
    for i in range(n - k + 1):            # each window start
        best = nums[i]
        for j in range(i, i + k):         # rescan all k elements
            if nums[j] > best:
                best = nums[j]
        out.append(best)
    return out''',
"brute_limit":
 "Consecutive windows share `k - 1` of their `k` elements, yet every maximum is recomputed from "
 "nothing. Sliding by one position removes exactly one element on the left and adds exactly one "
 "on the right, so almost all the comparison work is repeated.\n\n"
 "A heap fixes the additions cheaply but handles the removals badly: you cannot delete an "
 "arbitrary element from a binary heap in better than O(n), so the standard workaround is lazy "
 "deletion, which leaves the complexity at O(n log n) and the heap potentially holding all n "
 "elements.\n\n"
 "The dominance argument is what gets to linear: most elements never need to be stored at all, "
 "because a later, larger element makes them permanently irrelevant. Keeping only the "
 "non-dominated candidates gives a structure where the maximum is always at the front, with no "
 "search and no log factor.",
"opt_en":
 "Maintain a deque of **indices** whose corresponding values are in decreasing order. For each "
 "new index `i`:\n\n"
 "- **Pop from the back** while the value at the back index is less than `nums[i]`. Those "
 "elements are dominated by `i` &mdash; they are older and smaller &mdash; so they can never "
 "be a maximum again.\n"
 "- **Append `i`** to the back, preserving the decreasing order.\n"
 "- **Pop from the front** if the front index is `<= i - k`, meaning it has slid out of the "
 "current window. Evicting by **index**, not by value, is essential; a value-based test cannot "
 "distinguish two equal values at different positions.\n"
 "- Once `i >= k - 1`, a full window exists, so append `nums[dq[0]]` to the output &mdash; the "
 "front index always holds the largest value in the current window.\n\n"
 "Storing indices rather than values is what makes the window-eviction test possible at all, "
 "and it is the design decision to state explicitly.",
"opt_ds":
 "- A **deque of indices**, kept monotonically decreasing by value. Both ends are used, which "
 "is exactly why a deque rather than a stack or a queue: dominated elements leave from the "
 "back, expired elements leave from the front.\n"
 "- Indices rather than values, so expiry can be tested positionally.\n"
 "- The output list.",
"opt_algo": [
 "Create an empty deque and an empty output list.",
 "Iterate over the array with index `i` and value `x`.",
 "While the deque is non-empty and `nums[deque[-1]] < x`, pop from the back. Those older, smaller elements are permanently dominated by `x`.",
 "Append `i` to the back of the deque.",
 "If `deque[0] <= i - k`, the front index has fallen out of the window, so pop it from the front. A single `if` suffices, because at most one index expires per step.",
 "If `i >= k - 1`, the first full window has been formed, so append `nums[deque[0]]` to the output.",
 "Return the output.",
 "On duplicates: popping on strict `<` keeps equal values in the deque, which is safe because the older duplicate expires first and the newer one remains to serve later windows.",
],
"opt_code":
'''from collections import deque

def maxSlidingWindow(nums, k):
    """Monotonic decreasing deque of INDICES. The front is always the maximum
    of the current window."""
    dq = deque()                          # indices; nums[dq] is decreasing
    out = []

    for i, x in enumerate(nums):
        # 1. Anything smaller than x, and older than x, can never be a max again.
        while dq and nums[dq[-1]] < x:
            dq.pop()

        # 2. x is now a live candidate.
        dq.append(i)

        # 3. Evict the front BY INDEX if it has slid out of the window.
        #    (By index, not by value -- equal values must stay distinguishable.)
        if dq[0] <= i - k:
            dq.popleft()

        # 4. Once a full window exists, the front holds its maximum.
        if i >= k - 1:
            out.append(nums[dq[0]])

    return out''',
"opt_cx":
 "**Time: O(n).** This needs the amortised argument: each index is appended to the deque "
 "exactly once and removed at most once, either from the back as dominated or from the front as "
 "expired. So although the inner `while` can pop several items in one iteration, the total "
 "number of pops across the whole run is bounded by n. Two operations per element, so linear.\n\n"
 "**Space: O(k).** The deque never holds more than one window's worth of indices, since older "
 "ones are evicted as they expire.\n\n"
 "**Say this out loud:** \"Monotonic decreasing deque of indices. If a later element is at "
 "least as large as an earlier one, the earlier one can never be a maximum again, so I discard "
 "it. That leaves the front of the deque as the current window's maximum. Each index is pushed "
 "and popped at most once, so the total is O(n) even though one step can pop many items.\"\n\n"
 "**The gotcha:** evict the front by index, not by value. **The related problems:** this same "
 "monotonic-stack-or-deque structure solves Next Greater Element, Daily Temperatures, Largest "
 "Rectangle in Histogram, and the stack version of Trapping Rain Water.",
},

]
