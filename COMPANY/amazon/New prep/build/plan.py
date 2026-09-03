# -*- coding: utf-8 -*-
"""Part I: the 5-day plan, the story block and the design block."""

PLAN_HTML = """
<div class="cover">
  <div class="kicker">Amazon SDE-I &middot; Onsite Loop</div>
  <h1>The 5-Day Final Plan<br>&amp; Complete Answer Key</h1>
  <h2>Tue 1 Sept &middot; Herndon, VA &middot; 4 &times; 60 min &middot; LiveCode (typed)<br>
      Prep window: Tue 25 Aug &rarr; Sat 29 Aug &middot; 32 problems</h2>
  <div class="rule"></div>
  <div class="fmt">
    <h3>Every answer in this book follows one order</h3>
    <ol>
      <li>Clarification communication</li>
      <li>Understanding of the question</li>
      <li>Brute-force approach in English</li>
      <li>Data structures used</li>
      <li>Step-by-step algorithm</li>
      <li>Time &amp; space complexity with explanation</li>
      <li>Fully commented brute-force code</li>
      <li>Limitation of brute force</li>
      <li>Optimal approach in English</li>
      <li>Optimal data structures</li>
      <li>Step-by-step optimal algorithm</li>
      <li>Fully commented optimal code</li>
    </ol>
  </div>
  <div class="foot">Part I &mdash; the plan, the story block, the design block.
    Part II &mdash; all 32 problems in the twelve-section format above.</div>
</div>

<h1 class="part">Part I &mdash; The 5-Day Plan</h1>
<p class="partsub">Five prep days: Tue 25 Aug through Sat 29 Aug. 30&ndash;31 Aug
are travel days, not prep days.</p>

<h3>Read this first</h3>
<p>This plan is organised by <strong>round type</strong>, not by topic &mdash; so each
day rehearses the shape of an actual interview rather than a chapter of a textbook.</p>

<div class="callout">
<p><strong>One important correction to the round table:</strong> there is no separate
behavioural round at Amazon. Every interviewer is assigned 2&ndash;3 Leadership
Principles and must return evidence, so ownership and failure questions land
<em>inside</em> your coding rounds &mdash; usually in the first 10 minutes. That is why
there is a 30-minute story block every day rather than a single behavioural day.</p>
</div>

<h3>Daily shape &mdash; about 3.5 hours</h3>
<table>
<tr><th style="width:16%">Block</th><th style="width:16%">Time</th><th>What</th></tr>
<tr><td>Coding</td><td>2h 30m</td><td>The 6 problems for today, 25-minute timer each</td></tr>
<tr><td>Stories</td><td>30 min</td><td>Leadership Principle stories (see the story block below)</td></tr>
<tr><td>Design</td><td>30 min</td><td>One topic, out loud, on paper</td></tr>
</table>
<p>If you run short, cut the stretch problems first, then the design block.
<strong>Never cut the stories</strong> &mdash; with zero prepared stories you are exposed
in all four rounds, and 30 minutes a day fixes that.</p>

<h3>The three rules</h3>
<ol>
<li><strong>Blank page.</strong> Copilot and IntelliSense off. Plain editor. Paste into
LeetCode only when the whole solution is written.</li>
<li><strong>25-minute timer.</strong> Stuck at 8 minutes &rarr; read only the
<em>Understanding</em> and <em>Optimal approach</em> sections here, never the code.
At 20 minutes &rarr; read the code, close the book, rewrite it from scratch.</li>
<li><strong>Four sentences out loud after every problem</strong>, including the easy ones:
<em>&ldquo;This is a [pattern]. My [structure] holds [what it means]. I [movement rule],
because [why that is correct]. Each element is [counted work], so O(&hellip;) time,
O(&hellip;) space.&rdquo;</em></li>
</ol>

<div class="day">
<h2>Day 1 &middot; Tue 25 Aug</h2>
<p class="roundtype"><strong>ROUND TYPE A &mdash; Graph &amp; tree traversal under
constraints.</strong> <em>&ldquo;Given a graph/tree, find or optimize a path/traversal
under constraints.&rdquo;</em> The single most likely coding round for an SDE-I loop, and
where Amazon&rsquo;s own repeat questions cluster.</p>
<table>
<tr><th style="width:7%">#</th><th style="width:38%">Problem</th><th>What to watch</th></tr>
<tr><td>200</td><td>Number of Islands &#9733;&#9733;</td><td>Do it BFS <strong>and</strong> DFS. Ask: may I mutate the grid?</td></tr>
<tr><td>994</td><td>Rotting Oranges &#9733;&#9733;</td><td>Multi-source BFS. Seed every rotten cell before you start.</td></tr>
<tr><td>207</td><td>Course Schedule &#9733;</td><td>Kahn&rsquo;s topo sort. <code>[a,b]</code> means b before a, so the edge is b&rarr;a.</td></tr>
<tr><td>127</td><td>Word Ladder &#9733;</td><td>BFS generating neighbours (26 swaps per position), not pairwise compare.</td></tr>
<tr><td>236</td><td>LCA of a Binary Tree &#9733;&#9733;</td><td>Both subtrees return non-null &rArr; this node. Solve it twice.</td></tr>
<tr><td>102</td><td>Level Order Traversal</td><td><code>for _ in range(len(q))</code> is the level-size snapshot.</td></tr>
<tr><td colspan="3"><em>Stretch &mdash; only if the six above are done and clean</em></td></tr>
<tr><td>417</td><td>Pacific Atlantic Water Flow</td><td>Invert it: start from each ocean and walk uphill.</td></tr>
<tr><td>863</td><td>All Nodes Distance K</td><td>Add parent pointers &rarr; it is a graph &rarr; plain BFS.</td></tr>
</table>
<div class="callout"><p><strong>Say out loud before coding, every time:</strong> shortest
path &rArr; BFS, always. Reachability, area, counting &rArr; DFS is fine. Choosing DFS for
a shortest-path question is the single most common way to fail this round.</p></div>
</div>

<div class="day">
<h2>Day 2 &middot; Wed 26 Aug</h2>
<p class="roundtype"><strong>ROUND TYPE B &mdash; Reduce an O(n&sup2;) solution.</strong>
<em>&ldquo;Use a hash map / sliding window / two-pointer technique to reduce an
O(n&sup2;) solution.&rdquo;</em> Note the phrasing: the interviewer <strong>expects</strong>
you to state the brute force first, then improve it. That sequence is the answer, not
just the final code.</p>
<table>
<tr><th style="width:7%">#</th><th style="width:38%">Problem</th><th>What to watch</th></tr>
<tr><td>1</td><td>Two Sum</td><td>5-minute warm-up. Longer than that is a signal.</td></tr>
<tr><td>560</td><td>Subarray Sum Equals K &#9733;</td><td>Prefix sum + hashmap seeded <code>{0:1}</code>. Negatives break sliding window &mdash; say so.</td></tr>
<tr><td>3</td><td>Longest Substring Without Repeating &#9733;&#9733;</td><td>The archetype. Should be automatic by now.</td></tr>
<tr><td>424</td><td>Longest Repeating Character Replacement</td><td>Invalid when <code>len(window) &minus; maxFreq &gt; k</code>.</td></tr>
<tr><td>15</td><td>3Sum &#9733;</td><td>Sort, fix one, two-pointer the rest. Dedupe at BOTH levels.</td></tr>
<tr><td>42</td><td>Trapping Rain Water &#9733;&#9733;</td><td>Two-pointer and monotonic stack. Budget 45 min.</td></tr>
<tr><td colspan="3"><em>Stretch</em></td></tr>
<tr><td>76</td><td>Minimum Window Substring &#9733;&#9733;</td><td>have/need counters &mdash; the boss of this pattern.</td></tr>
<tr><td>239</td><td>Sliding Window Maximum &#9733;</td><td>Monotonic deque of indices.</td></tr>
</table>
<div class="callout"><p><strong>The script this round rewards:</strong> &ldquo;The brute
force is O(n&sup2;) &mdash; check every pair. The repeated work is the inner scan, so a
hashmap of what I have already seen gets me to O(n). Does that sound reasonable before
I code it?&rdquo; Rehearse those three sentences.</p></div>
</div>

<div class="day">
<h2>Day 3 &middot; Thu 27 Aug</h2>
<p class="roundtype"><strong>ROUND TYPE C &mdash; Intervals, heaps and top-K.</strong>
<em>&ldquo;Solve an interval, heap or top-K problem and explain complexity.&rdquo;</em>
Amazon asks these constantly &mdash; Meeting Rooms and Merge Intervals are perennial
repeats.</p>
<table>
<tr><th style="width:7%">#</th><th style="width:38%">Problem</th><th>What to watch</th></tr>
<tr><td>56</td><td>Merge Intervals &#9733;&#9733;</td><td>Sort by START. Use <code>max(end)</code> or contained intervals break it.</td></tr>
<tr><td>253</td><td>Meeting Rooms II &#9733;&#9733;</td><td>Min-heap of end times, and the sweep-line version. Know both.</td></tr>
<tr><td>215</td><td>Kth Largest Element</td><td>Min-heap of size k. Yes &mdash; min-heap for <em>largest</em>.</td></tr>
<tr><td>973</td><td>K Closest Points to Origin &#9733;</td><td>Skip the sqrt; it is monotonic. Say that.</td></tr>
<tr><td>23</td><td>Merge k Sorted Lists &#9733;&#9733;</td><td>Heap of heads. Index tiebreaker, or Python raises TypeError.</td></tr>
<tr><td>621</td><td>Task Scheduler &#9733;</td><td><code>(maxFreq&minus;1)*(n+1)+numMax</code>, clamped by <code>len(tasks)</code>.</td></tr>
<tr><td colspan="3"><em>Stretch</em></td></tr>
<tr><td>347</td><td>Top K Frequent Elements</td><td>Bucket sort is the O(n) follow-up.</td></tr>
<tr><td>295</td><td>Find Median from Data Stream &#9733;&#9733;</td><td>Two heaps, kept balanced.</td></tr>
</table>
<div class="callout"><p><strong>Memorise the inversion:</strong> &ldquo;K largest&rdquo;
&rArr; <strong>min</strong>-heap of size K. &ldquo;K smallest&rdquo; &rArr;
<strong>max</strong>-heap of size K. And for intervals: <strong>sort by start to merge,
sort by end to maximise how many fit.</strong></p></div>
</div>

<div class="day">
<h2>Day 4 &middot; Fri 28 Aug</h2>
<p class="roundtype"><strong>ROUND TYPE D &mdash; Justify the paradigm +
design-in-code.</strong> <em>&ldquo;Choose between BFS/DFS, DP, heap or binary search
and justify the choice.&rdquo;</em> This round grades your <strong>reasoning about the
choice</strong>, not just the implementation. Expect &ldquo;why not X?&rdquo; for every
decision.</p>
<table>
<tr><th style="width:7%">#</th><th style="width:38%">Problem</th><th>What to watch</th></tr>
<tr><td>875</td><td>Koko Eating Bananas &#9733;</td><td>Binary search the ANSWER. Write <code>feasible()</code> on the board first.</td></tr>
<tr><td>33</td><td>Search in Rotated Sorted Array &#9733;</td><td>One half is always sorted &mdash; identify which.</td></tr>
<tr><td>322</td><td>Coin Change &#9733;</td><td><strong>Greedy is wrong.</strong> Counterexample ready: coins [1,3,4], amount 6.</td></tr>
<tr><td>139</td><td>Word Break</td><td>DP over prefixes. Why not greedy? A longer match can dead-end.</td></tr>
<tr><td>146</td><td>LRU Cache &#9733;&#9733;</td><td>Hashmap + doubly linked list. The node must store its own key.</td></tr>
<tr><td>138</td><td>Copy List with Random Pointer &#9733;&#9733;</td><td>Hashmap first, then the O(1) interleave follow-up.</td></tr>
<tr><td colspan="3"><em>Stretch</em></td></tr>
<tr><td>1011</td><td>Capacity To Ship Packages &#9733;</td><td>Literally the same function as Split Array Largest Sum.</td></tr>
<tr><td>380</td><td>Insert Delete GetRandom O(1) &#9733;</td><td>Array + index map, swap-with-last on delete.</td></tr>
</table>
<div class="callout"><p><strong>The recognition rule for binary search on the
answer:</strong> the problem says <em>&ldquo;minimum X such that&hellip;&rdquo;</em> or
<em>&ldquo;maximum X such that&hellip;&rdquo;</em>, and you can write an O(n)
<code>feasible(x)</code> check. When you spot it, say the rule out loud &mdash; it is
the fastest way to show you recognised the pattern rather than pattern-matched a
template.</p></div>
</div>

<div class="day">
<h2>Day 5 &middot; Sat 29 Aug &mdash; Revision + full simulation</h2>
<p class="roundtype">Morning (2h 30m) &mdash; re-solve cold, blank page, timed.
Afternoon (2h) &mdash; one full recorded simulation. Evening &mdash; logistics, stop
by 8pm.</p>
<p>These are the ones Amazon actually repeats. If any takes over 25 minutes, mark it
and drill the <em>four sentences</em> for it tonight &mdash; not the code.</p>
<table>
<tr><th>Re-solve cold</th><th>Re-solve cold</th></tr>
<tr><td>200. Number of Islands</td><td>42. Trapping Rain Water</td></tr>
<tr><td>994. Rotting Oranges</td><td>560. Subarray Sum Equals K</td></tr>
<tr><td>236. LCA of a Binary Tree</td><td>56. Merge Intervals</td></tr>
<tr><td>127. Word Ladder</td><td>253. Meeting Rooms II</td></tr>
<tr><td>3. Longest Substring Without Repeating</td><td>23. Merge k Sorted Lists</td></tr>
<tr><td>146. LRU Cache</td><td>138. Copy List with Random Pointer</td></tr>
</table>
<h3>Afternoon &mdash; one full recorded simulation</h3>
<ul>
<li>Pick <strong>2 problems you have not solved</strong> from the Amazon tag. Any medium.</li>
<li>60 minutes. Record on your phone. Narrate the entire time.</li>
<li>Full sequence: clarify &rarr; small example &rarr; brute force and its complexity
&rarr; state the optimal &rarr; <strong>&ldquo;does that sound reasonable before I code
it?&rdquo;</strong> &rarr; code &rarr; dry-run out loud tracking variables &rarr;
complexity &rarr; edge cases.</li>
<li>Open with one Leadership Principle question, answered out loud, before any coding.</li>
<li><strong>Watch the recording.</strong> Note every silence over 20 seconds, and whether
you skipped the dry run.</li>
</ul>
<h3>Evening &mdash; logistics, then stop by 8pm</h3>
<ul>
<li>Print 4 resumes; photo ID out; clothes laid out; laptop and charger packed
(LiveCode runs on your machine).</li>
<li><strong>Confirm the exact building and suite with your recruiter.</strong> Amazon has
several Northern Virginia sites and people arrive at the wrong one.</li>
<li>Two questions per interviewer ready.</li>
</ul>
</div>

<div class="day">
<h2>The story block &mdash; 30 minutes a day</h2>
<p class="roundtype">Five stories cover essentially everything you will be asked. Write
one per day, about 250 words, in STAR+ form.</p>
<table>
<tr><th style="width:14%">Day</th><th style="width:24%">Story</th><th>Prompt it answers</th><th style="width:22%">Leadership Principle</th></tr>
<tr><td>25 Aug</td><td><strong>Ownership</strong></td><td><em>&ldquo;a time you took ownership beyond your assigned responsibility&rdquo;</em></td><td>Ownership</td></tr>
<tr><td>26 Aug</td><td><strong>Failure</strong></td><td><em>&ldquo;a disagreement or failure and what you changed afterward&rdquo;</em></td><td>Earn Trust / Learn and Be Curious</td></tr>
<tr><td>27 Aug</td><td><strong>Incomplete information</strong></td><td><em>&ldquo;you had incomplete information but still had to deliver&rdquo;</em></td><td>Bias for Action</td></tr>
<tr><td>28 Aug</td><td><strong>Most impactful project</strong></td><td>asked in almost every loop</td><td>Deliver Results</td></tr>
<tr><td>29 Aug</td><td><strong>Tell me about yourself</strong></td><td>the first 90 seconds of every round</td><td>&mdash;</td></tr>
</table>
<div class="callout">
<p><strong>STAR+:</strong> Situation (2 sentences) &middot; Task (what <strong>you</strong>
owned) &middot; <strong>Action (60% of the story)</strong> &middot; Result
(<strong>with a number</strong>) &middot; plus what you would do differently.</p>
<p><strong>The two things that sink these:</strong> saying <em>&ldquo;we&rdquo;</em> &mdash;
an interviewer cannot score &ldquo;we&rdquo;, so every one becomes <em>&ldquo;I
decided,&rdquo; &ldquo;I wrote,&rdquo; &ldquo;I convinced&rdquo;</em> &mdash; and stories
with no ending. &ldquo;Then it got deprioritised&rdquo; is a non-answer.</p>
<p><strong>Rehearse each one out loud, timed. Over 2.5 minutes gets cut.</strong></p>
</div>

<h2 style="margin-top:18px">The design block &mdash; 30 minutes a day, 3 topics only</h2>
<p>Do each on <strong>paper</strong>, out loud &mdash; the in-person design round uses a
whiteboard even though coding is typed.</p>
<table>
<tr><th style="width:14%">Day</th><th style="width:22%">Topic</th><th>What to cover</th></tr>
<tr><td>26 Aug</td><td><strong>Rate limiter</strong></td><td>Token bucket vs sliding window vs fixed window. Where the counter lives in a distributed setting. <strong>The question they will ask: what happens when the counter store is unavailable?</strong> For a rate limiter, fail-<em>open</em> is usually right &mdash; the limiter must not become the thing that takes the service down.</td></tr>
<tr><td>27 Aug</td><td><strong>Cache</strong></td><td>Read-through vs write-through vs write-back. Eviction (LRU/LFU). TTL. Invalidation. Thundering herd on a cold key. This pairs with the LRU coding problem on 28 Aug &mdash; say so if it comes up.</td></tr>
<tr><td>28 Aug</td><td><strong>Notification / messaging service</strong></td><td>Fan-out, queues, retries with exponential backoff <strong>plus jitter</strong>, dead-letter queues, idempotency so a retry does not double-send, per-user preferences and rate limits.</td></tr>
</table>
<div class="callout"><p><strong>The framework, every time:</strong> functional requirements
&rarr; scale numbers &rarr; API signatures &rarr; data model &rarr; boxes &rarr;
<strong>one failure mode</strong> &rarr; trade-offs stated aloud. The failure-mode answer
is what separates candidates at AWS; anyone can draw boxes.</p></div>

<h2 style="margin-top:18px">30&ndash;31 Aug &mdash; travel. Not prep days.</h2>
<ul>
<li>45 minutes writing core patterns <strong>by hand on paper</strong>: binary search,
sliding window, grid BFS, tree DFS, heap top-K.</li>
<li>Rehearse your five stories in your head. No notes.</li>
<li><strong>No LeetCode, no new problems.</strong> A bad attempt the night before sits in
your head and costs more than the practice gains.</li>
<li>31 Aug: physically find <strong>12900 Worldgate Dr</strong>. Eat properly, stop by
8pm, sleep 8 hours.</li>
</ul>
</div>
"""
