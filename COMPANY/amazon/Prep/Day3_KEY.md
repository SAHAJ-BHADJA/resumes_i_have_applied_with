# DAY 3 ANSWER KEY — Stacks, Monotonic Stacks, Linked Lists

> **Two rules that kill most bugs today:**
> 1. **Every linked-list problem where the head might change gets a dummy node.** No exceptions.
> 2. **Monotonic stack: store INDICES, not values.** You almost always need the distance.

---

## PART A — STACKS

### 20. Valid Parentheses
```python
def isValid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack                     # leftovers = unclosed
```
**O(n) / O(n)** — **Gotcha:** the `not stack` check before popping, and `return not stack` (not `True`).

---

### 155. Min Stack
**Insight:** Store the running min *alongside* each element. Then min is O(1) and pop needs no recomputation.

```python
class MinStack:
    def __init__(self):
        self.stack = []                  # (value, min_so_far)

    def push(self, val):
        cur_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, cur_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]
```
**All O(1) / O(n)** — mention the O(1)-amortised-space variant (a second stack that only pushes on new minima).

---

### 150. Evaluate Reverse Polish Notation
```python
def evalRPN(tokens):
    stack = []
    ops = {'+', '-', '*', '/'}
    for t in tokens:
        if t in ops:
            b = stack.pop()
            a = stack.pop()              # ORDER MATTERS: a op b
            if t == '+':   stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else:          stack.append(int(a / b))   # truncate toward ZERO
        else:
            stack.append(int(t))
    return stack[0]
```
**Gotcha:** `int(a/b)` not `a//b`. Python floor-divides toward −∞; the problem wants truncation toward 0. `-7//2 == -4`, but the answer is `-3`.

---

### 394. Decode String ★
**Trigger:** nested `k[substring]` expansion
**Insight:** On `[`, push the *state so far* (accumulated string + repeat count) and reset. On `]`, pop and combine.

```python
def decodeString(s):
    stack = []                           # (prev_string, repeat_count)
    cur = ""
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)     # multi-digit numbers
        elif ch == '[':
            stack.append((cur, num))
            cur, num = "", 0
        elif ch == ']':
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur
```
**O(output length) / O(depth)** — **Gotchas:** multi-digit `num`, and resetting *both* `cur` and `num` on `[`.

---

### 739. Daily Temperatures — monotonic stack
```python
def dailyTemperatures(temperatures):
    res = [0] * len(temperatures)
    stack = []                           # indices, decreasing temperatures
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j               # distance -> this is why we store indices
        stack.append(i)
    return res
```
**O(n) / O(n)** — each index is pushed and popped at most once. Say that when asked why it isn't O(n²).

---

### 496. Next Greater Element I
```python
def nextGreaterElement(nums1, nums2):
    nxt = {}
    stack = []
    for x in nums2:
        while stack and stack[-1] < x:
            nxt[stack.pop()] = x
        stack.append(x)
    return [nxt.get(x, -1) for x in nums1]
```
**O(n+m) / O(n)** — values are fine here because they're guaranteed unique.

---

### 503. Next Greater Element II — circular
**Insight:** Circular ⇒ iterate `2n` times with `i % n`. Only push indices during the first pass conceptually; simplest is to push always and let the second pass only resolve.

```python
def nextGreaterElements(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        cur = nums[i % n]
        while stack and nums[stack[-1]] < cur:
            res[stack.pop()] = cur
        if i < n:
            stack.append(i)              # only push in the first pass
    return res
```
**O(n) / O(n)**

---

### 735. Asteroid Collision ★
**Insight:** Only a positive (right-moving) on the stack meeting a negative (left-moving) incoming causes a collision. Everything else just gets pushed.

```python
def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()              # existing one explodes, keep checking
            elif stack[-1] == -a:
                stack.pop()              # both explode
                alive = False
            else:
                alive = False            # incoming explodes
        if alive:
            stack.append(a)
    return stack
```
**O(n) / O(n)** — **Gotcha:** the three-way comparison. Write the truth table on the board first; that's what the interviewer wants to see.

---

### 853. Car Fleet
**Insight:** Sort by starting position **descending**. Compute each car's time to target. A car joins the fleet ahead if its time is ≤ the fleet's time. Count the distinct times that survive.

```python
def carFleet(target, position, speed):
    pairs = sorted(zip(position, speed), reverse=True)
    fleets = 0
    slowest = 0.0
    for pos, spd in pairs:
        time = (target - pos) / spd
        if time > slowest:               # can't catch the one ahead -> new fleet
            fleets += 1
            slowest = time
    return fleets
```
**O(n log n) / O(n)** — this is a monotonic stack in disguise; you only ever need the top.

---

## PART B — LINKED LISTS

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

### 84. Largest Rectangle in Histogram ★★
**Insight:** For each bar, find how far left and right it can extend while staying the tallest. Increasing monotonic stack gives both boundaries.

```python
def largestRectangleArea(heights):
    stack = []                           # indices, increasing heights
    best = 0
    for i, h in enumerate(heights + [0]):    # sentinel flushes the stack
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best
```
**O(n) / O(n)** — the `+ [0]` sentinel is the trick that avoids a second cleanup loop. (Note `heights + [0]` makes a copy; `heights[stack[-1]]` still indexes the original safely because popped indices are always < len(heights).)

---

### 227. Basic Calculator II
**Insight:** Handle `*` and `/` immediately by modifying the stack top; push `+`/`−` as signed numbers. Sum at the end.

```python
def calculate(s):
    stack = []
    num = 0
    op = '+'
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if (not ch.isdigit() and ch != ' ') or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))    # truncate toward zero
            op = ch
            num = 0
    return sum(stack)
```
**O(n) / O(n)** — **Gotcha:** the `i == len(s)-1` clause flushes the final number.

---

### 71. Simplify Path
```python
def simplifyPath(path):
    stack = []
    for part in path.split('/'):
        if part == '' or part == '.':
            continue
        if part == '..':
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return '/' + '/'.join(stack)
```

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

### 146. LRU Cache — see `00_PRIMITIVES.py` #25
### 460. LFU Cache ★
**Insight:** Two maps + a `min_freq` counter. `key → (value, freq)` and `freq → OrderedDict of keys`. Evict from `freq_map[min_freq]`, oldest first.

```python
from collections import defaultdict, OrderedDict
class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key):
        f = self.key_to_freq[key]
        del self.freq_to_keys[f][key]
        if not self.freq_to_keys[f]:
            del self.freq_to_keys[f]
            if self.min_freq == f:
                self.min_freq += 1       # only place min_freq can increase
        self.key_to_freq[key] = f + 1
        self.freq_to_keys[f + 1][key] = None

    def get(self, key):
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key, value):
        if self.cap <= 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return
        if len(self.key_to_val) >= self.cap:
            evict, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val[evict]
            del self.key_to_freq[evict]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1                # a brand-new key resets min_freq
```
**All O(1) / O(capacity)** — the two lines that break people: `min_freq += 1` on bucket emptying, and `min_freq = 1` on insert.

---

## DAY 3 PATTERN TRIGGERS

| If the problem says... | Reach for |
|---|---|
| "matching / nesting / valid brackets" | stack |
| "next greater / next smaller / span / warmer" | monotonic stack of **indices** |
| "largest rectangle / max area under bars" | increasing monotonic stack + sentinel |
| "evaluate an expression" | stack, handle `*` `/` eagerly |
| "collision / annihilation" | stack, compare against the top |
| "get min/max in O(1) alongside a stack" | store the running extreme with each element |
| head of the list might be removed/changed | **dummy node** |
| "nth from the end" / "middle" / "cycle" | fast & slow pointers |
| "reverse a portion / in groups" | head-insertion or recursive group reverse |
| deep copy with extra pointers | hashmap old→new, or interleave for O(1) space |
| "least recently / frequently used" | hashmap + doubly linked list (LRU) or freq buckets (LFU) |
