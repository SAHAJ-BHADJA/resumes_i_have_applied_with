# Fri Aug 28 — Day 12 of 13
### ★★ MOCK LOOP #2 + Weak-Spot Repair

**Solutions for everything below are in `ANSWER_KEY.md`, section DAY 12.**

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Open `ANSWER_KEY.md` and read only the *Trigger* and *Insight* lines — never the code. Close it, keep going. At 20 min read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

---

## TODAY'S CHECKLIST

| ☐ | Block | Full (~7h) | Compressed (~4.5h) |
|---|---|---|---|
| ☐ | A — Primitives from memory | 40 min | 30 min |
| ☐ | B — Re-solve queue | 30 min | 20 min |
| ☐ | C — Problems / mock | 3h 30m | 2h 15m |
| ☐ | D — Design | 60 min | 40 min |
| ☐ | E — Leadership Principles | 45 min | 25 min |
| ☐ | F — Solution book | 20 min | 15 min |

> **13 days, not 18.** If you fall behind inside a day, drop from the **bottom** of Block C. The ★ problems stay — those are the ones that recur in Amazon loops. Never cut Block B; re-solves build recall, and recall is the thing that's broken.

---

## Block A — Primitives (from memory, timed)

**All 25 primitives from memory, timed. Target: 25 minutes, zero errors.**

Blank file, type from memory, **then** compare against `00_PRIMITIVES.py`. Target: under 90 seconds each, zero syntax errors. Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Everything due today at **+1 day** and **+3 days**. Blank page, no notes, no peeking at the key first. Fail a repeat and its clock resets.

---

## Block C — Mock loop

### THE LOOP (3h 45m)

- [ ] **Round 1 (60 min) — Coding.** Unseen problems. Recorded.
- [ ] **Round 2 (60 min) — LLD.** An unseen prompt: *design a vending machine* / *a library system* / *a food-delivery order flow*. Paper. Classes, state machine, patterns named.
- [ ] **Round 3 (60 min) — System design.** One of SD-1..SD-4. Paper. Defend two decisions under pushback.
- [ ] **Review all three recordings (45 min).**

### REPAIR BLOCK (90 min)
Your three worst areas from the Aug 23 debrief.
- [ ] Weak area 1: ____________ → two fresh problems, blank page
- [ ] Weak area 2: ____________ → two fresh problems, blank page
- [ ] Weak area 3: ____________ → two fresh problems, blank page

**This is the last day new problems help.** Tomorrow is rehearsal; after that, rest.


### ★ Block C2 — InterviewDB bank (reported Amazon questions)

Same rules: blank page, 25-min timer, narrated. **Read the confidence mark** — ✅ means the statement is real; 🟠 means the title is confirmed but details are inferred, so practise the shape and don't memorise the wording.

#### ☐ Smart Processor — ✅ Verified  ·  time: ____

**Prompt:** array `arr` and a list of inclusive ranges `[l,r]`. In order, append `arr[l..r]` to a new array `efficient` (indices may repeat). For each original index `i`: efficiency is `0` if `i` was covered by any range; otherwise it's the count of elements in `efficient` **strictly less than** `arr[i]`. Return the sum.

#### ☐ Sign In Pages — ✅ Verified  ·  time: ____

**Prompt:** process ordered auth requests. `register(user, pass)` fails if the user exists. `login(user, pass)` fails if the user doesn't exist, the password is wrong, or the user is already signed in. `logout(user)` fails if not signed in. Case-sensitive; store starts empty.

#### ☐ Faulty Server Detection — ✅ Verified  ·  time: ____

**Prompt:** chronological logs `"<server> <error|success>"`. Per server, `error` increments a consecutive-failure counter and `success` resets it. On reaching **3 consecutive errors** the server is replaced and its counter resets. Return total replacements.

#### ☐ Count Discount Pairs — ✅ Verified  ·  time: ____

**Prompt:** array `prices`, integer `x`. Count index pairs `i < j` with `(prices[i] + prices[j]) % x == 0`.
**Insight:** bucket by remainder. Pair `r` with `x-r`; handle `r == 0` and `r == x/2` as self-pairs.


---

## Block D — Design

**Final LLD review — all six, no notes.** For each: name the classes, the pattern, and the one extension follow-up, out loud.

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

## Block E — Leadership Principles

**Full LP run.** Anything over 2.5 minutes gets cut tonight, not tomorrow.

---

## Block F — Solution book (20 min)

Written **after** the session, **with your editor closed**, **from memory**. Reproducing the code from memory is a second free retrieval rep — that's where most of the value is.

```
#____  ______________________     Date: ____   Mode: ☐ solo  ☐ GPT voice
Time taken: ____ min    Result: ☐ clean  ☐ hint  ☐ ran over  ☐ failed

TRIGGER   (what in the wording should have told me the pattern?)
PATTERN
THOUGHT PROCESS  1. first thing I tried  2. why it failed  3. what made me switch
THE CODE  (from memory, editor closed)
COMPLEXITY  Time O(__) because ____   Space O(__) because ____
             ("one pass" is not a reason. "each index is pushed and popped once" is.)
THE BUG I HIT
EDGE CASES  ☐ empty ☐ single ☐ all-duplicates ☐ negatives ☐ ____
RE-SOLVE:  +1d ____   +3d ____
```

---

## END OF DAY — honest check

- [ ] Did I narrate out loud on every problem, or did I go quiet?
- [ ] Did I state my approach and ask for buy-in **before** coding?
- [ ] Did I dry-run without being prompted?
- [ ] Primitives from memory, no reference?
- [ ] Re-solve queue cleared?
