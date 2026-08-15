# Sun Aug 16 — Day 5 of 18
### PHASE 1 — FOUNDATION · Linked Lists  *(weekend — full track)*

**Answer key for reference: `Day3_KEY.md`** · Solutions for today's problems are at the bottom of this file.

---

> **The three rules. Every day. No exceptions.**
> 1. **Blank page.** Copilot off, IntelliSense off, no GPT. Plain editor. Paste into LeetCode only after the whole solution is written.
> 2. **Stuck at 8 min?** Read only the *Trigger* and *Insight* lines below — never the code. Close it, keep going. At 20 min, read the code, then close it and rewrite twice, and add it to the re-solve queue.
> 3. **Narrate out loud on every problem.** Silent correct code scores worse at Amazon than narrated near-correct code.

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

Primitives **7, 8, 9, 25**. Dummy-head must be reflexive by tonight.

Open a blank file. Type from memory. Only then compare against `00_PRIMITIVES.py`. **Target: under 90 seconds each, zero syntax errors.** Fail one → write it again immediately, then again.

---

## Block B — Re-solve queue (cold, blank page)

Aug 14 (+3d), Aug 15 (+1d). **First +7d repeats appear soon — keep the queue honest.**

**Schedule: +1 day, +3 days, +7 days.** Three clean re-solves and it graduates off the list. Fail a repeat and the clock resets.

**If your day runs short, cut Block C — never Block B.** New problems build coverage; re-solves build recall, and recall is what's broken.

---

## Block C — Problems (25-min timer each, narrated out loud)

> **Rule that kills most bugs today: every linked-list problem where the head might change gets a dummy node. No exceptions.**

| ☐ | # | Problem | Pattern | Time |
|---|---|---|---|---|
| ☐ | 206 | Reverse Linked List | prev/cur/next | ____ |
| ☐ | 21 | Merge Two Sorted Lists | Dummy head | ____ |
| ☐ | 141 | Linked List Cycle | Fast/slow | ____ |
| ☐ | 142 | Linked List Cycle II | Floyd + reset | ____ |
| ☐ | 19 | Remove Nth From End | Dummy + gap | ____ |
| ☐ | 143 | Reorder List | Three primitives composed | ____ |
| ☐ | 2 | Add Two Numbers | Carry loop | ____ |
| ☐ | 138 | Copy List with Random Pointer ★★ | Both ways | ____ |
| ☐ | 25 | Reverse Nodes in k-Group | Group reverse | ____ |
| ☐ | 92 | Reverse Linked List II | Head insertion | ____ |

---

## Block D — Design

**LLD 2 — LRU Cache, then LFU.** Code both from scratch. Manual doubly linked list. **No `OrderedDict`.**

These get asked as *both* coding problems and design problems at Amazon, so this block doubles as problem practice.

For LRU cover: why hashmap + DLL (O(1) lookup *and* O(1) reorder), why sentinel head/tail nodes, why the node must store its own key.
For LFU cover: the two-map structure (`key→freq`, `freq→ordered keys`), and the two lines everyone gets wrong — `min_freq += 1` when a bucket empties, `min_freq = 1` on insert.

Then the design question: **how would you make this a distributed cache?** Sharding, invalidation, TTL, thundering herd on a cold key.

---

## Block E — Leadership Principles

**Write LP stories #7 and #8.**

Targets: **Have Backbone; Disagree and Commit** · **Learn and Be Curious**

Have Backbone is the most commonly botched one. The strong shape: *you disagreed, you escalated it properly, the decision went **against** you, and you committed fully anyway* — and you say what you did to make the chosen path succeed. A story where you disagreed and turned out right is weaker than one where you disagreed, lost, and executed anyway.

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

- [ ] Can I write `reverse_list` and `merge_two` in under 90 seconds each, no typos?
- [ ] 138: can I do the O(1)-space interleaving version, not just the hashmap?
- [ ] LRU: does my node store its key? (If not, eviction is broken.)


---

# ══════════════════════════════════════
# SOLUTIONS — read only after your attempt
# ══════════════════════════════════════

### 206. Reverse Linked List
```python
def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```
*Recursive version (know it, they sometimes ask):*
```python
def reverseList_rec(head):
    if not head or not head.next:
        return head
    new_head = reverseList_rec(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

---

### 21. Merge Two Sorted Lists
```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
```

---

---

### 141 / 142. Linked List Cycle I & II ★
**Insight for 142 (why it works — be ready to prove it):** slow travels `k` to the cycle entry, meets fast after the cycle length relationship works out such that the distance from the meeting point to the entry equals the distance from head to the entry. So reset one pointer to head and advance both by 1.

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False

def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head                  # reset one to head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
```
**O(n) / O(1)**

---

---

### 141 / 142. Linked List Cycle I & II ★
**Insight for 142 (why it works — be ready to prove it):** slow travels `k` to the cycle entry, meets fast after the cycle length relationship works out such that the distance from the meeting point to the entry equals the distance from head to the entry. So reset one pointer to head and advance both by 1.

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False

def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head                  # reset one to head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
```
**O(n) / O(1)**

---

---

### 19. Remove Nth Node From End
```python
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)            # dummy handles "remove the head"
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next
```
**O(n) / O(1)** — **without the dummy**, removing the head is a special case you will get wrong under pressure.

---

---

### 143. Reorder List ★
**Insight:** Three primitives composed: find middle → reverse second half → interleave.

```python
def reorderList(head):
    if not head or not head.next:
        return
    # 1. middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    # 2. reverse second half
    second = slow.next
    slow.next = None                     # cut
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    # 3. interleave
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
```
**O(n) / O(1)** — say "this is three known sub-routines" out loud; it's exactly the decomposition they're testing.

---

---

### 2. Add Two Numbers
```python
def addTwoNumbers(l1, l2):
    dummy = ListNode()
    cur = dummy
    carry = 0
    while l1 or l2 or carry:             # `or carry` handles the final 1
        total = carry
        if l1:
            total += l1.val
            l1 = l1.next
        if l2:
            total += l2.val
            l2 = l2.next
        carry, digit = divmod(total, 10)
        cur.next = ListNode(digit)
        cur = cur.next
    return dummy.next
```

---

---

### 138. Copy List with Random Pointer ★★ (Amazon favourite)
**Way A — hashmap, O(n) space (lead with this):**
```python
def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}
    cur = head
    while cur:                           # pass 1: create all nodes
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                           # pass 2: wire the pointers
        old_to_new[cur].next = old_to_new.get(cur.next)
        old_to_new[cur].random = old_to_new.get(cur.random)
        cur = cur.next
    return old_to_new[head]
```
**Way B — interleaving, O(1) space (the follow-up they want):**
```python
def copyRandomList_O1(head):
    if not head:
        return None
    cur = head                           # 1. A -> A' -> B -> B'
    while cur:
        cur.next = Node(cur.val, cur.next)
        cur = cur.next.next
    cur = head                           # 2. set randoms
    while cur:
        if cur.random:
            cur.next.random = cur.random.next
        cur = cur.next.next
    # 3. unweave
    old, new = head, head.next
    new_head = head.next
    while old:
        old.next = old.next.next
        new.next = new.next.next if new.next else None
        old, new = old.next, new.next
    return new_head
```
**Gotcha:** `.get(cur.next)` returns `None` gracefully; `old_to_new[cur.next]` would KeyError on the tail.

---

## STRETCH

---

### 25. Reverse Nodes in k-Group ★
```python
def reverseKGroup(head, k):
    # check there are k nodes left
    node = head
    for _ in range(k):
        if not node:
            return head                  # fewer than k -> leave as is
        node = node.next
    # reverse this group; `node` is the head of the remainder
    prev = reverseKGroup(node, k)        # recursively handle the rest
    cur = head
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
```
**O(n) / O(n/k)** recursion. Iterative version is O(1) space — mention it exists.

---

---

### 92. Reverse Linked List II
```python
def reverseBetween(head, left, right):
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    cur = prev.next
    for _ in range(right - left):        # head-insertion: pull each node to the front
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next
```
**O(n) / O(1)** — the head-insertion idiom. Draw it before coding.

---

---
