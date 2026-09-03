# THE INTERVIEWDB BANK — Amazon reported questions
### Merged from two independent research passes. Every solution here has been executed and asserted.

---

## How to read this

| Mark | Meaning |
|---|---|
| ✅ **Verified** | An independent public report reproduces the actual problem. Treat the statement as real. |
| 🟡 **Strong match** | Almost certainly the underlying known problem, but the original wording wasn't recovered. |
| 🟠 **Reconstruction** | The title is confirmed; the details are inferred. Practise it; don't memorise it as exact. |
| ❌ **Not recovered** | Title confirmed, prompt not found in English or Chinese sources. **No statement is given — a fabricated prompt is worse than none.** |

**The honest framing:** InterviewDB publishes titles and tags publicly but gates the bodies. Both research passes agree that these titles are *not* invented — several map to independently reported Amazon questions with unusually specific details (Smart Processor, Config Reconstruction, Warehouse Stock, Travel Time, Binary String Errors). Chinese sources (一亩三分地, Nowcoder) carried detail that English exact-title search did not.

**But:** Amazon randomises names and constraints, and interviewers pick their own questions. A title match does not guarantee your prompt. Drill the pattern, not the wording.

**Where the two passes disagreed, I kept the better-sourced answer and noted it:**
- *Optimal Packing* — pass 1 mapped it confidently to LeetCode 1889; pass 2 called it unrecoverable. I've included 1889 because the mapping is defensible, marked 🟡 rather than ✅.
- *Shima / VM Load* — pass 1 inferred islands and min-heap load balancing; pass 2 refused both. I've included the VM Load min-heap (a dated OA screenshot supports it) and **excluded a Shima statement** (the island decode is a guess, not evidence).
- *Increment One, Number of Paths, Course Completion, Word Trail, Word Decomposition, Top Visit Sequence* — both passes agree these are LeetCode re-skins. Already in your daily files as 66, 62, 207/210, 127, 139/472, 1152.

---

## Priority order for your loop

You have **4 onsite rounds** and have already passed the OA. So:

1. **Six LLD titles** — Config Manager, Discount, Query Builder, Shipping Cost, Spell Checker, Validation Framework. Six LLD entries in one bank is the strongest signal here, and it matches an AUTA/SDE-I loop shape. **This is your highest-value block.**
2. **Onsite / Phone+Onsite coding** — Common Manager, Friends Purchases, Gold Thief, Tree Kyoukai, XO Game, Destination Cache, Top Customers, Employee Directory, Friendship Path.
3. **System design** — CloudWatch, Config Distribution, Financial Dashboard, Jihanki Network.
4. **OA-tagged** — lowest value for you, but several are excellent algorithm practice (Warehouse Stock, Binary String Errors, Inconvenience are genuinely hard and worth the reps).

---

## NOT RECOVERED — drill the family, do not memorise a guess

Both passes searched English and Chinese sources and found the title but no trustworthy prompt. **I am deliberately not inventing statements for these.**

| Title | Stage | What to drill instead |
|---|---|---|
| ASIN Average Price | Phone/Onsite | Streaming aggregation, group-by, running/weighted averages |
| Fulfillment | Phone/Onsite | Greedy allocation, heap scheduling |
| Shima | Phone/Onsite | Grid DFS/BFS *and* union-find — but do **not** assume Number of Islands |
| Streak Number | Phone/Onsite | Longest run scan, LC 128 consecutive sequence |
| Usage Tracker | Phone/Onsite | Rolling-window counters, LC 359/362 |
| Sawtooth Pattern String Builder | Phone/Onsite | String simulation, LC 6 zigzag |
| Raffle Winners | Phone/Onsite | Weighted random (LC 528), reservoir sampling |
| Delivery Time | Phone/Onsite | Heaps, scheduling, shortest path |
| Non-Returning Users | Phone/Onsite | Set difference over event logs |
| Playlist | Phone/Onsite | Heap + iterator design, `getNext()` |
| Minimal Conflicts | OA | Interval/scheduling conflict minimisation |
| Prepare Time | OA | — |
| Test Utility Service | OA | — |
| Time to Stablize | OA | BFS simulation to convergence |
| Distributed Sort-Softmax | MLE SD | Sharded reductions, numerically stable softmax, all-reduce. **Likely out of scope unless you're matched to an AI/ML org — confirm with your recruiter.** |

---

# PART A — LOW LEVEL DESIGN (your highest-value block)

All six are 🟠 reconstructions: the titles are confirmed, the requirements are inferred from the canonical form of each problem. **Practise the class design and the extension follow-up — that is what's actually graded**, and it transfers even if the exact requirements differ.

For every one of these, the interviewer is checking the same four things: do you write real compilable code (not boxes), do you put behaviour behind an interface, can you add a new variant **without modifying existing callers** (Open/Closed), and do you name your patterns.

### LLD-1. Config Manager 🟠
Retrieve and update configuration values, with typed access, defaults, layered overrides, and change notification.
- **Classes:** `ConfigManager` (facade) · `ConfigSource` interface (in-memory / file / env / remote) · `ConfigValue<T>` · `ConfigListener` · `ConfigValidator`
- **Patterns:** **Strategy** (source) · **Observer** (listeners) · precedence chain across sources
- **Operations:** `get(key)`, typed getters, `set(key, value)`, defaults, `reload()`, `subscribe(listener)`
- **Follow-ups to have answers for:** thread safety on concurrent read/write · hot reload · precedence when two sources define the same key · type coercion failures · caching and TTL · **adding a new source without touching callers**

### LLD-2. Discount 🟡
A discount/promotion engine for a cart: percentage-off, flat amount, BOGO, item- and category-level, coupon codes.
- **Classes:** `DiscountStrategy` interface with `apply(Cart)` · `PercentageDiscount` · `FixedDiscount` · `BogoDiscount` · `EligibilityRule` · `DiscountEngine` · `Cart`, `LineItem`, `Product`
- **Patterns:** **Strategy** (discount type) · **Decorator** (stacking) · **Chain of Responsibility** (ordered application) · **Factory** (build from coupon code)
- **Follow-ups:** stacking vs mutually exclusive · maximum-discount cap · order of application (percentage before or after flat — it changes the total) · rounding and money precision · per-customer eligibility and expiry
- Example requirement seen in reports: *a product becomes eligible for 30% off only after a quantity threshold is met.*

### LLD-3. Query Builder 🟠
A fluent, SQL-like builder: `select(...).from(...).where(...).and(...).orderBy(...).limit(...).build()`.
- **Classes:** `QueryBuilder` (fluent, returns `this`) · `Predicate`/`Condition` hierarchy · `Query`
- **Patterns:** **Builder** · **Composite** (nested AND/OR) · optionally **Interpreter** for the expression tree · **Strategy** for SQL dialects
- **Follow-ups:** nested grouping `(a OR b) AND c` · parameterisation and injection safety · joins and aggregations · builder immutability/reuse · multiple dialects

### LLD-4. Shipping Cost 🟡
Compute shipping cost from weight, dimensions, origin/destination zone, carrier, and service level.
- **Classes:** `ShippingCostCalculator` · `ShippingStrategy`/`Carrier` interface · `StandardShipping`, `ExpressShipping` · `RegionalPricing` · `Package`, `Address`
- **Patterns:** **Strategy** (carrier/service) · **Factory** (carrier selection) · **Decorator** (surcharges: fuel, residential, insurance)
- **Key domain detail to raise unprompted:** **dimensional (volumetric) weight** = `(L×W×H) / divisor`, and you charge on `max(actual, dimensional)`. Mentioning this shows domain thinking.
- **Follow-ups:** add a carrier without changing callers · zone lookup tables · surcharge stacking order · free-shipping thresholds · cheapest-carrier fallback

### LLD-5. Spell Checker 🟡
Load a dictionary; `isValid(word)`; `suggest(word)` returning plausible corrections.
- **Classes:** `Dictionary` backed by a **Trie** (or HashSet) · `SpellChecker` · `SuggestionStrategy` (**Strategy**)
- **Algorithms:** edit distance 1 (insert/delete/replace/transpose) or bounded Trie traversal; **BK-tree** as the fuzzy-match follow-up
- **Follow-ups:** ranking suggestions by frequency · large-dictionary memory · capitalisation and punctuation · context-aware correction · `suggest(word, maxDistance, maxSuggestions)`
- *Note: this is the one LLD title with a published Amazon-framed write-up (a mock, not a confirmed loop).*

### LLD-6. Validation Framework 🟠
Register rules — not-null, length, regex, range, custom — run them against an object, aggregate results.
- **Classes:** `Validator<T>` interface returning `ValidationResult` · `ValidationRule<T>` · `NotNullValidator`, `LengthValidator`, `RegexValidator` · `CompositeValidator` · `ValidationError`
- **Patterns:** **Chain of Responsibility** + **Composite** · **Specification** (AND/OR composition of rules) · **Builder** to assemble rule sets
- **Follow-ups:** collect-all vs fail-fast · cross-field and conditional validation · rule severity · async/remote validators · i18n error messages · **add a rule without modifying the engine**
- *Closely related and widely reported: "design Unix `find`" using the Specification pattern. If you can do one you can do the other.*

---

# PART B — SYSTEM DESIGN

🟠 reconstructions. Use the framework in `01_REFERENCE_...md` §4: functional → non-functional → back-of-envelope → API → data model → architecture → deep dive → **failure modes** → trade-offs.

### SD-1. CloudWatch 🟠
Design a distributed monitoring service. Metric and log ingestion at very high throughput · dimensions/tags · time-series storage · aggregation windows · dashboards · alarms (`CPU > 80% for 5 min`) · retention and downsampling · multi-tenancy · out-of-order and delayed data · hot vs cold storage · millions of hosts.
> **Raise cardinality unprompted.** Every extra dimension multiplies series count — that's the thing operators know and candidates miss. Also: *who monitors the monitoring system?*

### SD-2. Config Distribution 🟠
Publish config changes and distribute them safely to a huge fleet. Versioning · push vs poll · very low read latency · staged rollout and rollback · audit history · regional/global · local caching · **clients that boot while the control plane is down** · stale config · eventual vs strong consistency · watch/subscribe API · failure isolation.
> This is the distributed sibling of LLD-1. Say **"the data plane needs static stability — hosts keep serving with their cached config even if the control plane is unavailable."**

### SD-3. Financial Dashboard ✅ (verified as a real reported onsite scenario)
Aggregate a user's financial data across several **external providers**: balances, holdings, crypto, transactions, derived portfolio metrics. Providers differ in schema, refresh frequency, rate limits, outages, and partial responses.
- Design: provider **adapters** → normalisation → canonical model → current state + historical snapshots
- Must handle: retries, idempotency, reconciliation, provider corrections, permissions, **staleness exposed to the user rather than silently wrong totals**
> The distinguishing requirement is *never show a silently inconsistent total.* Lead with that.

### SD-4. Jihanki Network 🟠
*Jihanki* (自販機) = vending machine. Design a platform managing a large fleet: registration · per-machine inventory · purchase events · pricing · cashless payment · health telemetry · online/offline status · restocking · remote configuration · low-stock alerts · retries when machines lose connectivity · central analytics.
> The **LLD core is the classic vending-machine state machine** (State pattern: Idle → HasMoney → Dispensing). Be ready to drop from the fleet architecture down into that. If asked for one round, ask which level they want.

---

# PART C — CODING (recovered)

Everything below has been executed and asserted, including randomised brute-force cross-checks on Binary String Errors and Warehouse Stock.

### IDB1. Bid Fulfillment — ✅ Verified
**Prompt:** Fixed `inventory` and a list of requests `[customerId, quantity, bid, timestamp]`. Higher bid gets priority. Within the same bid, allocate **round-robin in increasing timestamp**: each round gives one unit to every still-unfulfilled customer in that bid group. Drop a customer once fully fulfilled. Stop when inventory hits 0. Return the IDs of customers who received **zero** units, in original input order.
**Trap:** it is *not* "sort by bid and give the top customer everything." The equal-bid round-robin is the whole question.

```python
from collections import defaultdict
def bid_fulfillment(inventory, requests):
    groups = defaultdict(list)
    for cid, qty, bid, ts in requests:
        groups[bid].append((ts, cid, qty))
    received = defaultdict(int)
    for bid in sorted(groups, reverse=True):            # highest bid first
        active = sorted(groups[bid])                    # round-robin by timestamp
        while inventory > 0 and active:
            nxt = []
            for ts, cid, qty in active:
                if inventory == 0:
                    nxt.append((ts, cid, qty))
                    continue
                received[cid] += 1
                inventory -= 1
                if received[cid] < qty:
                    nxt.append((ts, cid, qty))
            active = nxt
        if inventory == 0:
            break
    return [cid for cid, _, _, _ in requests if received[cid] == 0]
```
**O(inventory + n log n) / O(n)** — the outer `while` gives one unit per customer per pass, so total work is bounded by units allocated.

---

### IDB2. Binary String Errors — ✅ Verified
**Prompt:** `errorString` of `0`,`1`,`!`; integers `x`,`y`. Replace every `!` with `0` or `1`. Each subsequence `01` costs `x`; each `10` costs `y`. Minimise total cost, mod 1e9+7.
**Insight (the whole problem):** the optimal assignment of the `!`s has **threshold structure** — all `0`s then all `1`s, or all `1`s then all `0`s. Among the `!`s themselves, mixing costs more. So enumerate the split point and evaluate in O(1) per step.

```python
MOD = 10**9 + 7
def min_errors(errorString, x, y):
    n = len(errorString)
    bangs = [i for i, c in enumerate(errorString) if c == '!']
    m = len(bangs)
    # fixed prefix/suffix counts
    f0b = [0]*(n+1); f1b = [0]*(n+1)
    for i, c in enumerate(errorString):
        f0b[i+1] = f0b[i] + (c == '0')
        f1b[i+1] = f1b[i] + (c == '1')
    tot0, tot1 = f0b[n], f1b[n]
    f0a = lambda p: tot0 - f0b[p+1]
    f1a = lambda p: tot1 - f1b[p+1]

    def base_cost(assign):
        """Full cost with '!' replaced per `assign` (list of chars)."""
        s = list(errorString)
        for r, i in enumerate(bangs):
            s[i] = assign[r]
        zeros = ones = 0
        cost = 0
        for c in s:
            if c == '1':
                cost += x * zeros
                ones += 1
            else:
                cost += y * ones
                zeros += 1
        return cost

    best = None
    # Arrangement A: ranks [0,t) -> '0', [t,m) -> '1'; sweep t from m down to 0
    cost = base_cost(['0']*m)
    best = cost
    for t in range(m, 0, -1):
        p = bangs[t-1]                                   # flip this one 0 -> 1
        zeros_before = f0b[p] + (t-1)                    # bangs before it are all '0'
        ones_before  = f1b[p]
        zeros_after  = f0a(p)                            # bangs after it are all '1'
        ones_after   = f1a(p) + (m - t)
        cost += x*zeros_before + y*zeros_after - y*ones_before - x*ones_after
        best = min(best, cost)
    # Arrangement B: ranks [0,t) -> '1', [t,m) -> '0'
    cost = base_cost(['1']*m)
    best = min(best, cost)
    for t in range(m, 0, -1):
        p = bangs[t-1]                                   # flip this one 1 -> 0
        zeros_before = f0b[p]
        ones_before  = f1b[p] + (t-1)
        zeros_after  = f0a(p) + (m - t)
        ones_after   = f1a(p)
        cost += y*ones_before + x*ones_after - x*zeros_before - y*zeros_after
        best = min(best, cost)
    return best % MOD
```
**O(n) / O(n)** — examples: `"101!1", x=2, y=3 → 9`; `"01!0", x=y=2 → 6`.

---

### IDB3. Config Reconstruction — ✅ Verified
**Prompt:** digit string `config`, integers `x`,`y`. Start `curr = 0`. Repeatedly add `x` or `y` to `curr` and append `curr % 10` to a generated string. Find the **shortest** generated string that contains `config` as a subsequence.
**Insight:** only `curr % 10` matters, so the state space is tiny — BFS over `(last_digit, matched_prefix_length)`, 10 × (len+1) states.

```python
from collections import deque
def config_reconstruction(config, x, y):
    target = len(config)
    start = (0, 0)                                      # (curr % 10, matched)
    q = deque([start])
    parent = {start: None}
    while q:
        d, j = q.popleft()
        for add in (x, y):
            nd = (d + add) % 10
            nj = j + 1 if j < target and config[j] == str(nd) else j
            state = (nd, nj)
            if state in parent:
                continue
            parent[state] = ((d, j), nd)
            if nj == target:
                out = []
                cur = state
                while parent[cur] is not None:
                    prev, digit = parent[cur]
                    out.append(str(digit))
                    cur = prev
                return ''.join(reversed(out))
            q.append(state)
    return ""
```
**O(10·len) / O(10·len)** — example: `config="27", x=2, y=3 → "247"`.

---

### IDB4. Count Discount Pairs — ✅ Verified
**Prompt:** array `prices`, integer `x`. Count index pairs `i < j` with `(prices[i] + prices[j]) % x == 0`.
**Insight:** bucket by remainder. Pair `r` with `x-r`; handle `r == 0` and `r == x/2` as self-pairs.

```python
def count_discount_pairs(prices, x):
    freq = [0] * x
    for p in prices:
        freq[p % x] += 1
    total = freq[0] * (freq[0] - 1) // 2
    for r in range(1, x // 2 + 1):
        c = x - r
        if r == c:
            total += freq[r] * (freq[r] - 1) // 2
        else:
            total += freq[r] * freq[c]
    return total
```
**O(n + x) / O(x)** — the O(n²) double loop is the thing you're being tested against.

---

### IDB5. Faulty Server Detection — ✅ Verified
**Prompt:** chronological logs `"<server> <error|success>"`. Per server, `error` increments a consecutive-failure counter and `success` resets it. On reaching **3 consecutive errors** the server is replaced and its counter resets. Return total replacements.

```python
from collections import defaultdict
def count_faults(logs, threshold=3):
    streak = defaultdict(int)
    replacements = 0
    for line in logs:
        server, status = line.split()
        if status == 'error':
            streak[server] += 1
            if streak[server] == threshold:
                replacements += 1
                streak[server] = 0                       # replaced -> reset
        else:
            streak[server] = 0
    return replacements
```
**O(n) / O(servers)**

---

### IDB6. Inconvenience — ✅ Verified
**Prompt:** binary grid, `1` = service center. Distance is **Chebyshev**: `max(|dx|, |dy|)`. The grid's inconvenience is the maximum, over all `0` cells, of the distance to the nearest center. You may flip **at most one** `0` to `1`. Minimise inconvenience.
**Insight:** binary search the answer. For a candidate `d`, the cells still uncovered must all fit inside one Chebyshev ball of radius `d` — which is a rectangle test on their bounding box.

```python
from collections import deque
def min_inconvenience(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1]*cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dist[r][c] = 0
                q.append((r, c))
    if not q:
        return -1                                        # no centers at all
    while q:                                             # 8-dir BFS == Chebyshev
        r, c = q.popleft()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

    def feasible(d):
        bad = [(r, c) for r in range(rows) for c in range(cols) if dist[r][c] > d]
        if not bad:
            return True
        xs = [p[0] for p in bad]; ys = [p[1] for p in bad]
        lo_r, hi_r = max(xs) - d, min(xs) + d             # centre must sit here
        lo_c, hi_c = max(ys) - d, min(ys) + d
        return lo_r <= hi_r and lo_c <= hi_c and \
               max(lo_r, 0) <= min(hi_r, rows-1) and max(lo_c, 0) <= min(hi_c, cols-1)

    lo, hi = 0, max(max(row) for row in dist)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```
**O(mn log(mn)) / O(mn)** — example: `[[0,0,0,1],[0,0,0,1]] → 1`.

---

### IDB7. Minimize Absolute Differences — ✅ Verified
**Prompt:** arrays `a`, `b` of length `n`. Pair each `a[i]` with a distinct `b[j]`. Minimise `Σ |a[i] − b[π(i)]|`.
**Insight:** sort both and pair in order. The exchange argument: if `a1<a2` are paired to `b1>b2`, swapping never increases the sum.

```python
def minimize_abs_differences(a, b):
    return sum(abs(p - q) for p, q in zip(sorted(a), sorted(b)))
```
**O(n log n) / O(n)** — be ready to *prove* the exchange argument; that's the interview.

---

### IDB8. Minimum Possible Cost — ✅ Verified
**Prompt:** `n` item types; the `j`-th unit bought of type `i` costs `a[i] + (j-1)*b[i]`. Buy exactly `m` items total, minimising cost.
**Insight:** greedy with a min-heap — always buy the globally cheapest next unit, then push that type's new next price.

```python
import heapq
def min_possible_cost(a, b, m):
    heap = [(a[i], i, 1) for i in range(len(a))]
    heapq.heapify(heap)
    total = 0
    for _ in range(m):
        cost, i, j = heapq.heappop(heap)
        total += cost
        heapq.heappush(heap, (a[i] + j * b[i], i, j + 1))
    return total
```
**O((n + m) log n) / O(n)** — example: `a=[2,1,1], b=[1,2,3], m=4 → 7`.

---

### IDB9. Minimum Shipment — ✅ Verified
**Prompt:** `warehouses[i]` is the warehouse holding item `i`. Each shipment sends either two items **from different warehouses** or one item alone. Minimise shipments.
**Insight:** closed form. Let `f` = largest warehouse count, `n` = total. If `f > n − f` the surplus must ship alone, giving `f`. Otherwise everything pairs up: `ceil(n/2)`.

```python
from collections import Counter
def min_shipments(warehouses):
    n = len(warehouses)
    f = max(Counter(warehouses).values())
    return f if f > n - f else (n + 1) // 2
```
**O(n) / O(n)** — derive it out loud; don't just state it.

---

### IDB10. Permutation Sorter — ✅ Verified
**Prompt:** a permutation of `1..n`. Two operations: (1) reverse the whole array, (2) move the first element to the end. Minimum operations to sort ascending; input is guaranteed sortable.
**Insight:** the array must be a rotation of ascending or of descending. Only three shapes are reachable cheaply — check each.

```python
def permutation_sorter(nums):
    n = len(nums)
    asc = sorted(nums)
    desc = asc[::-1]
    best = float('inf')
    for k in range(n):                                   # k rotations
        rot = nums[k:] + nums[:k]
        if rot == asc:
            best = min(best, k)                          # rotations only
        if rot == desc:
            best = min(best, k + 1)                      # rotate then reverse
    rev = nums[::-1]
    for k in range(n):                                   # reverse first, then rotate
        if rev[k:] + rev[:k] == asc:
            best = min(best, 1 + k)
    return best if best < float('inf') else -1
```
**O(n²) as written / O(n)** — the O(n) version finds the single descent point instead of testing every rotation. Mention that.

---

### IDB11. Sign In Pages — ✅ Verified
**Prompt:** process ordered auth requests. `register(user, pass)` fails if the user exists. `login(user, pass)` fails if the user doesn't exist, the password is wrong, or the user is already signed in. `logout(user)` fails if not signed in. Case-sensitive; store starts empty.

```python
def sign_in_pages(requests):
    users = {}
    active = set()
    out = []
    for req in requests:
        parts = req.split()
        action = parts[0]
        if action == 'register':
            _, u, p = parts
            if u in users:
                out.append("Registration Unsuccessful")
            else:
                users[u] = p
                out.append("Registered Successfully")
        elif action == 'login':
            _, u, p = parts
            if u not in users or users[u] != p or u in active:
                out.append("Login Unsuccessful")
            else:
                active.add(u)
                out.append("Logged In Successfully")
        else:                                            # logout
            _, u = parts
            if u in active:
                active.discard(u)
                out.append("Logged Out Successfully")
            else:
                out.append("Logout Unsuccessful")
    return out
```
**O(n) / O(users)** — **clarify the exact output strings and the already-signed-in rule before coding.** They vary between reports.

---

### IDB12. Smart Processor — ✅ Verified
**Prompt:** array `arr` and a list of inclusive ranges `[l,r]`. In order, append `arr[l..r]` to a new array `efficient` (indices may repeat). For each original index `i`: efficiency is `0` if `i` was covered by any range; otherwise it's the count of elements in `efficient` **strictly less than** `arr[i]`. Return the sum.

```python
import bisect
def smart_processor(arr, ranges):
    n = len(arr)
    diff = [0] * (n + 1)
    efficient = []
    for l, r in ranges:
        diff[l] += 1
        diff[r + 1] -= 1
        efficient.extend(arr[l:r + 1])
    efficient.sort()
    covered = 0
    total = 0
    for i in range(n):
        covered += diff[i]
        if covered == 0:
            total += bisect.bisect_left(efficient, arr[i])
    return total
```
**O(E log E + n log E) / O(E)** — example: `arr=[1,2,3,2,4,5]`, ranges `[[0,1],[3,4],[0,0],[3,4]] → 12`.
**Gotcha:** coverage is a difference array; building a set of every covered index is fine here but doesn't scale if ranges are huge.

---

### IDB13. Travel Time — ✅ Verified (Chinese source)
**Prompt:** `m` hubs in a circle (hub 1 adjacent to hub `m`). `transitionTime[i]` is the travel time on the edge between hub `i+1` and hub `i+2` (wrapping). Start at hub 1 and visit `requestedHubs` **in order**, choosing clockwise or counter-clockwise per leg. Return minimum total time.
**Insight:** prefix sums round the circle. One direction is `|pref[b] − pref[a]|`; the other is `total − that`.

```python
def travel_time(m, transitionTime, requestedHubs):
    pref = [0] * (m + 1)
    for i in range(m):
        pref[i + 1] = pref[i] + transitionTime[i]
    total = pref[m]
    cur = 1
    ans = 0
    for dest in requestedHubs:
        one_way = abs(pref[dest - 1] - pref[cur - 1])
        ans += min(one_way, total - one_way)
        cur = dest
    return ans
```
**O(m + q) / O(m)** — example: `m=3, transitionTime=[3,2,1], requestedHubs=[1,3,3,2] → 3`.
**Clarify first:** which edge each `transitionTime[i]` refers to. Reports differ, and getting it wrong silently produces a plausible wrong answer.

---

### IDB14. Warehouse Stock — ✅ Verified
**Prompt:** `stock[0..n-1]`, each either `-1` (missing) or a known value in `1..200`. Replace every `-1` with a value in `1..200` so that `a[0] <= a[1]`, `a[n-1] <= a[n-2]`, and `a[i] <= max(a[i-1], a[i+1])` for interior `i`. Count valid completions mod `998244353`.
**Insight:** the constraints say exactly **"no strict local maximum anywhere."** Sweep left to right with a two-state DP: state 1 = "this element is already satisfied because it's ≤ its left neighbour"; state 0 = "it still needs the next element to be ≥ it." Prefix sums make each step O(V).

```python
MOD2 = 998244353
V = 200
def warehouse_stock(stock):
    n = len(stock)
    if n == 1:
        return V if stock[0] == -1 else 1
    def allowed(i):
        return range(1, V + 1) if stock[i] == -1 else [stock[i]]
    dp0 = [0]*(V+2)                                      # needs next >= v
    dp1 = [0]*(V+2)                                      # already satisfied
    for v in allowed(0):
        dp0[v] = 1                                       # a[0] must be <= a[1]
    for i in range(1, n):
        # suffix sums of dp1, prefix sums of dp0/dp1
        suf1 = [0]*(V+2)
        for v in range(V, 0, -1):
            suf1[v] = (suf1[v+1] + dp1[v]) % MOD2
        pre0 = [0]*(V+2); pre1 = [0]*(V+2)
        for v in range(1, V+1):
            pre0[v] = (pre0[v-1] + dp0[v]) % MOD2
            pre1[v] = (pre1[v-1] + dp1[v]) % MOD2
        n0 = [0]*(V+2); n1 = [0]*(V+2)
        for w in allowed(i):
            # from state 0 we must have w >= v; satisfied only when w == v
            n1[w] = (dp0[w] + suf1[w]) % MOD2
            n0[w] = (pre0[w-1] + pre1[w-1]) % MOD2
        dp0, dp1 = n0, n1
    return sum(dp1[1:V+1]) % MOD2                        # last must be <= previous
```
**O(n·V) / O(V)** — examples: `[-1,-1] → 200`; `[1,-1,2] → 1`.

---

### IDB15. VM Load — ✅ Verified (pattern)
**Prompt:** route each request to the **least-loaded** server, breaking ties by lowest index. Return the target server per request (or the final loads).

```python
import heapq
def find_request_target(num_servers, requests):
    heap = [(0, i) for i in range(num_servers)]          # (load, index)
    heapq.heapify(heap)
    out = []
    for cost in requests:
        load, idx = heapq.heappop(heap)
        out.append(idx)
        heapq.heappush(heap, (load + cost, idx))
    return out
```
**O(n log k) / O(k)** — the tuple `(load, index)` gives the tie-break for free. Say that out loud.

---

### IDB16. Common Manager — ✅ Verified
**Prompt:** an org tree where each manager has zero or more direct reports. Given two employees, return their **lowest common manager**. Follow-up: generalise to `k` employees.

```python
class Employee:
    def __init__(self, name, reports=None):
        self.name = name
        self.reports = reports or []

def lowest_common_manager(top, a, b):
    def helper(node):
        """Returns (num_targets_found, lcm_or_None)."""
        if node is None:
            return 0, None
        found = 0
        for r in node.reports:
            cnt, res = helper(r)
            if res:
                return cnt, res                          # already resolved below
            found += cnt
        if node is a or node is b:
            found += 1
        return found, (node if found == 2 else None)
    return helper(top)[1]

def lowest_common_manager_k(top, targets):
    """Follow-up: k employees. Same shape, compare against len(targets)."""
    need = len(targets)
    tset = set(targets)
    def helper(node):
        if node is None:
            return 0, None
        found = 1 if node in tset else 0
        for r in node.reports:
            cnt, res = helper(r)
            if res:
                return cnt, res
            found += cnt
        return found, (node if found == need else None)
    return helper(top)[1]
```
**O(n) / O(h)** — this is LCA on an n-ary tree. **Ask whether parent pointers exist**; if they do, the two-pointer depth-walk is cleaner.

---

### IDB17. Friends Purchases — ✅ Verified
**Prompt:** given `getFriends(person)` and `getPurchases(person)`, return the most popular products among a user's friends. **Popularity = number of distinct friends who bought it**, not total quantity. Common variant: exclude products the user already owns.

```python
from collections import Counter
def friends_purchases(person, get_friends, get_purchases, k=None, exclude_own=True):
    own = set(get_purchases(person)) if exclude_own else set()
    counts = Counter()
    for friend in get_friends(person):
        for product in set(get_purchases(friend)):       # DISTINCT per friend
            if product not in own:
                counts[product] += 1
    ranked = sorted(counts, key=lambda p: (-counts[p], p))
    return ranked if k is None else ranked[:k]
```
**O(F·P log) / O(P)** — **the `set()` per friend is the entire question.** Buying a product three times still counts once. Follow-up: friends-of-friends via BFS to depth `d`.

---

### IDB18. Friendship Path — 🟡 BFS
**Prompt:** given friendships and two users, return the shortest chain connecting them.

```python
from collections import deque
def friendship_path(graph, start, end):
    if start == end:
        return [start]
    prev = {start: None}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nei in graph.get(cur, []):
            if nei in prev:
                continue
            prev[nei] = cur
            if nei == end:
                path = [end]
                while path[-1] is not None and prev[path[-1]] is not None:
                    path.append(prev[path[-1]])
                return path[::-1]
            q.append(nei)
    return []
```
**O(V+E) / O(V)** — BFS, not DFS: DFS gives *a* path, not the shortest.

---

### IDB19. Gold Thief — 🟡 LeetCode 1219 Path with Maximum Gold
**Prompt:** grid where `0` is empty and positive values are gold. Start anywhere with gold, move 4-directionally, collect on visit, never revisit a cell, never step on `0`. Maximise gold collected.

```python
def get_maximum_gold(grid):
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == 0:
            return 0
        gold = grid[r][c]
        grid[r][c] = 0                                   # mark for THIS path
        best = max(dfs(r+1,c), dfs(r-1,c), dfs(r,c+1), dfs(r,c-1))
        grid[r][c] = gold                                # *** restore ***
        return gold + best
    return max((dfs(r, c) for r in range(rows) for c in range(cols)), default=0)
```
**O(mn·4^k) / O(k)** — backtracking, so the cell **must** be restored. This is Word Search's shape, not Number of Islands'.

---

### IDB20. Tree Kyoukai — 🟡 LeetCode 545 Boundary of Binary Tree
**Prompt:** return the tree boundary anticlockwise: root, then the left boundary top-down (excluding leaves), then all leaves left-to-right, then the right boundary bottom-up (excluding leaves). No node twice.

```python
def boundary_of_binary_tree(root):
    if not root:
        return []
    def is_leaf(n):
        return not n.left and not n.right
    out = [root.val] if not is_leaf(root) else [root.val]
    def left_bound(node):
        while node:
            if not is_leaf(node):
                out.append(node.val)
            node = node.left if node.left else node.right
    def leaves(node):
        if not node:
            return
        if is_leaf(node):
            out.append(node.val)
            return
        leaves(node.left)
        leaves(node.right)
    def right_bound(node):
        stack = []
        while node:
            if not is_leaf(node):
                stack.append(node.val)
            node = node.right if node.right else node.left
        out.extend(reversed(stack))
    if is_leaf(root):
        return out
    left_bound(root.left)
    leaves(root.left)
    leaves(root.right)
    right_bound(root.right)
    return out
```
**O(n) / O(h)** — **the three traps:** a single-node tree, excluding leaves from the boundaries, and reversing the right side.

---

### IDB21. XO Game — 🟡 LeetCode 348 Design Tic-Tac-Toe
**Prompt:** design an `n × n` tic-tac-toe. `move(row, col, player)` returns `0` (no winner), `1`, or `2`. Follow-up: **O(1) per move**, no board rescan.

```python
class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.rows = [0]*n
        self.cols = [0]*n
        self.diag = 0
        self.anti = 0

    def move(self, row, col, player):
        delta = 1 if player == 1 else -1
        self.rows[row] += delta
        self.cols[col] += delta
        if row == col:
            self.diag += delta
        if row + col == self.n - 1:
            self.anti += delta
        if self.n in (abs(self.rows[row]), abs(self.cols[col]),
                      abs(self.diag), abs(self.anti)):
            return player
        return 0
```
**O(1) per move / O(n)** — the +1/−1 counter trick is what they're testing. Lead with the O(n)-per-move version only if you're stuck.

---

### IDB22. Increment One — 🟡 LeetCode 66 Plus One
```python
def plus_one(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits                                  # all nines
```
**O(n) / O(1)**

---

### IDB23. Optimal Packing — 🟡 LeetCode 1889 Minimum Space Wasted From Packaging
**Prompt:** choose a **single** supplier whose boxes fit all packages (each package in one box ≥ its size), minimising total wasted space. Return −1 if impossible, mod 1e9+7.
**Insight:** sort packages, prefix sums, then binary search each box size to find how many packages it absorbs.

```python
import bisect
def min_wasted_space(packages, boxes):
    MOD = 10**9 + 7
    packages.sort()
    n = len(packages)
    pref = [0]*(n+1)
    for i, p in enumerate(packages):
        pref[i+1] = pref[i] + p
    best = float('inf')
    for supplier in boxes:
        supplier.sort()
        if supplier[-1] < packages[-1]:
            continue                                     # can't fit the biggest
        waste = 0
        prev = 0
        for b in supplier:
            i = bisect.bisect_right(packages, b)
            waste += b * (i - prev) - (pref[i] - pref[prev])
            prev = i
        best = min(best, waste)
    return -1 if best == float('inf') else best % MOD
```
**O((n + m) log n) / O(n)** — **take the modulus only at the end**, or comparisons between suppliers break.

---

### IDB24. Character Separation — 🟡 LeetCode 358 Rearrange String k Distance Apart
**Prompt:** rearrange a string so identical characters are at least `k` apart. Return `""` if impossible. (With `k = 2` this is Reorganize String / LC 767.)
**Insight:** greedy with a max-heap plus a cooldown queue of length `k`.

```python
import heapq
from collections import Counter, deque
def rearrange_string(s, k):
    if k <= 1:
        return s
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    out = []
    cooldown = deque()                                   # (available_index, cnt, ch)
    while heap or cooldown:
        if cooldown and cooldown[0][0] <= len(out):
            _, cnt, ch = cooldown.popleft()
            heapq.heappush(heap, (cnt, ch))
        if not heap:
            return ""                                    # forced gap -> impossible
        cnt, ch = heapq.heappop(heap)
        out.append(ch)
        if cnt + 1 < 0:
            cooldown.append((len(out) + k - 1, cnt + 1, ch))
    return ''.join(out)
```
**O(n log 26) / O(n)** — the cooldown queue *is* the k-distance constraint.

---

### IDB25. Conversion Rate — ✅ Verified (LeetCode 399 shape)
**Prompt:** given rates like `USD→EUR = 0.9`, answer arbitrary conversion queries by chaining. Reverse edges are reciprocals. Return `-1` when no path exists.

```python
from collections import defaultdict
def conversion_rate(rates, queries):
    """rates: [(from, to, rate)]"""
    graph = defaultdict(dict)
    for a, b, v in rates:
        graph[a][b] = v
        graph[b][a] = 1 / v
    def dfs(src, dst, seen):
        if src not in graph or dst not in graph:
            return -1.0
        if src == dst:
            return 1.0
        seen.add(src)
        for nei, w in graph[src].items():
            if nei in seen:
                continue
            sub = dfs(nei, dst, seen)
            if sub != -1.0:
                return w * sub
        return -1.0
    return [dfs(a, b, set()) for a, b in queries]
```
**O(Q·(V+E)) / O(V+E)** — weighted Union-Find is the "can you do better" answer.

---

### IDB26. Employee Directory — 🟡 Design
**Prompt:** model employees (`id`, `name`, `manager`, `directReports`) and support: lookup by id, prefix search by name, and "everyone beneath employee X."

```python
class Directory:
    def __init__(self):
        self.by_id = {}
        self.reports = {}                                # id -> [ids]

    def add(self, emp_id, name, manager_id=None):
        self.by_id[emp_id] = {'name': name, 'manager': manager_id}
        self.reports.setdefault(emp_id, [])
        if manager_id is not None:
            self.reports.setdefault(manager_id, []).append(emp_id)

    def get(self, emp_id):
        return self.by_id.get(emp_id)

    def search_by_prefix(self, prefix):
        return sorted(i for i, e in self.by_id.items()
                      if e['name'].startswith(prefix))

    def all_below(self, emp_id):
        out, stack = [], list(self.reports.get(emp_id, []))
        while stack:
            cur = stack.pop()
            out.append(cur)
            stack.extend(self.reports.get(cur, []))
        return sorted(out)

    def chain_to_top(self, emp_id):
        chain, cur = [], emp_id
        while cur is not None:
            chain.append(cur)
            cur = self.by_id[cur]['manager']
        return chain
```
**Follow-up to prepare:** swap the prefix scan for a **Trie** when the directory is large — that's the upgrade they're looking for.

---

### IDB27. Top Customers — 🟡 Heap aggregation
**Prompt:** given transactions, return the top `k` customers by total spend, ties broken by customer id.

```python
import heapq
from collections import defaultdict
def top_customers(transactions, k):
    """transactions: [(customer_id, amount)]"""
    totals = defaultdict(int)
    for cid, amt in transactions:
        totals[cid] += amt
    return heapq.nsmallest(k, totals.items(), key=lambda p: (-p[1], p[0]))
```
**O(n + u log k) / O(u)** — the `(-total, id)` key gives spend-descending, id-ascending in one pass. Follow-up: streaming updates ⇒ keep a size-k min-heap.

---

### IDB28. Destination Cache — 🟠 LRU shape (title verified, prompt not recovered)
**Do not assume plain LRU** — "destination" may imply routing results with a TTL. Practise both. LRU is in `00_PRIMITIVES.py` #25; here is the TTL variant.

```python
from collections import OrderedDict
class DestinationCache:
    def __init__(self, capacity, ttl=None):
        self.cap = capacity
        self.ttl = ttl
        self.store = OrderedDict()                       # key -> (value, inserted_at)

    def get(self, key, now=0):
        if key not in self.store:
            return -1
        value, ts = self.store[key]
        if self.ttl is not None and now - ts > self.ttl:
            del self.store[key]
            return -1
        self.store.move_to_end(key)
        return value

    def put(self, key, value, now=0):
        if key in self.store:
            del self.store[key]
        self.store[key] = (value, now)
        if len(self.store) > self.cap:
            self.store.popitem(last=False)
```
**O(1) / O(capacity)** — be ready to hand-roll the doubly linked list instead of `OrderedDict`.

---

### IDB29. Block Words — 🟡 Trie / Aho–Corasick
**Prompt:** given text and a list of blocked words, determine whether the text contains any blocked word.
**Clarify first:** substring vs whole-word matching, case sensitivity, punctuation. GPT's research confirmed the core but not these rules — and they change the algorithm.

```python
def has_blocked_word_tokens(text, blocked):
    """Whole-word matching, case-insensitive."""
    banned = {w.lower() for w in blocked}
    import re
    return any(tok in banned for tok in re.findall(r"[a-z0-9']+", text.lower()))

class BlockedTrie:
    """Substring matching over a large blocked set."""
    def __init__(self, words):
        self.root = {}
        for w in words:
            node = self.root
            for ch in w.lower():
                node = node.setdefault(ch, {})
            node['$'] = True

    def contains_any(self, text):
        t = text.lower()
        for i in range(len(t)):
            node = self.root
            for j in range(i, len(t)):
                if t[j] not in node:
                    break
                node = node[t[j]]
                if '$' in node:
                    return True
        return False
```
**Tokens O(n); Trie substring O(n·L)** — say "Aho–Corasick gives O(n + total) for many patterns"; that's the senior answer.
