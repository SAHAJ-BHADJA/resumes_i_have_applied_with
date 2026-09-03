# -*- coding: utf-8 -*-
"""Day 1 - Round Type A: graph and tree traversal under constraints."""

DAY = "Day 1 · Tue 25 Aug · Round Type A (graph & tree traversal)"

PROBLEMS = [

{
"num": 200, "title": "Number of Islands", "stars": "★★", "day": DAY,
"pattern": "Grid flood fill (DFS / BFS)", "opt_cx_short": "O(m·n) time, O(m·n) space",
"clarify": [
 "Are the cells characters `'1'`/`'0'` or integers `1`/`0`? LeetCode gives characters, and comparing against the wrong type silently returns 0.",
 "**May I modify the input grid?** This is the important one. If yes I mark visited cells in place and use O(1) extra space; if no I keep a separate `visited` set.",
 "Is connectivity 4-directional or 8-directional (do diagonals connect)? The default is 4-directional.",
 "Can the grid be empty, or a single row/column? I want to confirm the empty grid returns 0 rather than throwing.",
 "How large can the grid get? If it can be very large I will prefer BFS over recursive DFS to avoid blowing the call stack.",
],
"understand":
 "I am given a 2-D grid where `'1'` is land and `'0'` is water. An island is a maximal "
 "group of land cells connected horizontally or vertically. I must return how many "
 "distinct islands there are.\n\n"
 "Reframed as a graph problem: each land cell is a vertex, and there is an edge between "
 "two land cells that are vertically or horizontally adjacent. The question is then "
 "simply **how many connected components does this graph have**. Every counting-connected-"
 "components problem has the same shape: iterate over all vertices, and every time you "
 "find one you have not visited yet, increment the counter and exhaustively consume its "
 "whole component.",
"brute_en":
 "Without the idea of \"consume the whole component at once\", the natural first attempt is "
 "iterative label propagation. Give every land cell a unique label to begin with, then "
 "repeatedly sweep the entire grid, and on each sweep replace each land cell's label with "
 "the smallest label among itself and its four neighbours. Labels leak outward one cell "
 "per sweep, so connected cells slowly converge on a shared label. Keep sweeping until a "
 "full pass changes nothing, then count how many distinct labels survive.\n\n"
 "It is correct because within one connected component the smallest label eventually "
 "reaches every cell, and a label can never cross water, so two different components can "
 "never merge.",
"brute_ds":
 "- A second 2-D array `label` of the same dimensions, holding one integer per land cell.\n"
 "- A boolean `changed` flag to know when the sweeps have stabilised.\n"
 "- A set at the end, to count the distinct surviving labels.",
"brute_algo": [
 "Allocate `label` with the same shape as the grid. Walk the grid once and give each land cell a unique id, for example `r * cols + c`. Water gets a sentinel such as `-1`.",
 "Set `changed = True`.",
 "While `changed` is True: set `changed = False`, then scan every cell of the grid.",
 "For each land cell, look at its four neighbours. If any neighbour is land and carries a smaller label, copy that smaller label into this cell and set `changed = True`.",
 "When a whole sweep completes with `changed` still False, the labels have stabilised.",
 "Collect all labels of land cells into a set and return the size of that set.",
],
"brute_cx":
 "**Time: O((m·n)²) in the worst case.** One sweep costs O(m·n) because it visits "
 "every cell and does constant work per cell. The number of sweeps needed is the length "
 "of the longest path a label must travel inside a component. A snake-shaped island that "
 "winds through the whole grid is roughly m·n cells long, so the smallest label needs "
 "on the order of m·n sweeps to reach the far end. Multiply the two: O((m·n)²).\n\n"
 "**Space: O(m·n)** for the `label` grid plus the set of distinct labels at the end.",
"brute_code":
'''def numIslands_brute(grid):
    """Label propagation. Correct, but re-sweeps the whole grid until labels settle."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    # Step 1: every land cell starts with its OWN unique label; water gets -1.
    label = [[-1] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                label[r][c] = r * cols + c        # unique id derived from position

    # Step 2: sweep until a full pass changes nothing.
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '1':
                    continue                       # water carries no label
                best = label[r][c]
                # Take the smallest label among me and my 4 neighbours.
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                        best = min(best, label[nr][nc])
                if best != label[r][c]:
                    label[r][c] = best             # a smaller label leaked in
                    changed = True                 # so another sweep is required

    # Step 3: one label survives per connected component.
    distinct = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                distinct.add(label[r][c])
    return len(distinct)''',
"brute_limit":
 "The waste is that the algorithm has no memory of what it already resolved. Each sweep "
 "re-examines every cell in the grid, including whole islands that stabilised many sweeps "
 "ago, just to discover that nothing changed. Information moves only one cell per pass, so "
 "a long winding island forces an enormous number of nearly-useless passes.\n\n"
 "On a 1000 × 1000 grid that is up to 10¹² cell visits, which will not finish. "
 "The fix is to stop letting information trickle: when I land on an unvisited land cell, I "
 "should walk its entire component immediately in one traversal, mark it, and never look at "
 "it again.",
"opt_en":
 "Scan the grid once. The moment I hit a land cell that has not been visited, I know I have "
 "found a brand-new island that no previous scan has touched, because any earlier island "
 "would already have marked this cell. So I increment the counter by one and then flood fill "
 "outward from that cell, marking every land cell reachable from it as visited. The outer "
 "scan then continues and simply skips over everything the flood fill consumed.\n\n"
 "The flood fill can be DFS (recursion, or an explicit stack) or BFS (a queue). Both visit "
 "exactly the same set of cells and cost the same. I lead with DFS because it is shorter to "
 "write, and I mention BFS as the version to use when the grid is large enough that "
 "recursion depth could overflow the stack.",
"opt_ds":
 "- The **grid itself, mutated**, as the visited marker: setting a consumed cell to `'0'` "
 "means I need no extra structure at all. If the interviewer says the input is read-only, I "
 "swap in a `visited` set of `(r, c)` tuples, which costs O(m·n) space instead.\n"
 "- For the DFS version, the **call stack**; for the BFS version, a **deque** used as a FIFO queue.\n"
 "- A single integer counter.",
"opt_algo": [
 "Handle the empty grid up front and return 0.",
 "Loop over every cell `(r, c)` of the grid.",
 "If the cell is not `'1'`, skip it: it is either water or part of an island already counted.",
 "Otherwise increment `count` by one, because this cell begins a new island.",
 "Flood fill from `(r, c)`: visit the cell, immediately set it to `'0'` so it is never revisited, then recurse (or enqueue) into its four neighbours, ignoring anything out of bounds or not equal to `'1'`.",
 "In the BFS variant, mark a neighbour as visited **at the moment you enqueue it**, not when you dequeue it. Marking on dequeue lets the same cell be pushed several times before it is first popped.",
 "When the flood fill returns, the whole island has been erased. Continue the outer scan.",
 "Return `count`.",
],
"opt_code":
'''def numIslands(grid):
    """DFS flood fill. Each land cell is visited once and then erased."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):
        # Guard first: off the grid, or water / already-consumed land -> stop.
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != '1':
            return
        grid[r][c] = '0'                  # mark visited by mutating the input
        sink(r + 1, c)                    # down
        sink(r - 1, c)                    # up
        sink(r, c + 1)                    # right
        sink(r, c - 1)                    # left

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':         # unvisited land => a brand-new island
                count += 1
                sink(r, c)                # consume the entire island now
    return count


from collections import deque

def numIslandsBFS(grid):
    """BFS flood fill. Same complexity; use it when the grid is huge, because
    it keeps the frontier on the heap instead of on the call stack."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1':
                continue
            count += 1
            q = deque([(r, c)])
            grid[r][c] = '0'              # mark the seed immediately
            while q:
                x, y = q.popleft()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'   # *** mark ON ENQUEUE, not on dequeue ***
                        q.append((nx, ny))   # otherwise duplicates pile up in q
    return count''',
"opt_cx":
 "**Time: O(m·n).** The outer loop touches each cell once. Across all flood fills each "
 "land cell is pushed and popped at most once, because it is set to `'0'` the first time it "
 "is reached. Every cell therefore does O(1) work in total.\n\n"
 "**Space: O(m·n) worst case.** For DFS that is the recursion depth when the whole grid is "
 "one snaking island; for BFS it is the maximum queue size. If I may not mutate the grid, add "
 "O(m·n) for the `visited` set.\n\n"
 "**Say this out loud:** \"This is counting connected components. My grid doubles as the "
 "visited marker. I erase each island as I count it, because that guarantees I never count "
 "the same component twice. Each cell is visited once, so O(m·n) time.\"\n\n"
 "**The one gotcha:** in BFS, mark on enqueue. **The follow-up:** union-find also solves it "
 "in near-O(m·n), and is the right answer if the grid streams in cell by cell, or if the "
 "follow-up is Number of Islands II (islands added one at a time).",
},

{
"num": 994, "title": "Rotting Oranges", "stars": "★★  Amazon favourite", "day": DAY,
"pattern": "Multi-source BFS, level by level", "opt_cx_short": "O(m·n) time, O(m·n) space",
"clarify": [
 "To confirm the encoding: `0` is empty, `1` is fresh, `2` is rotten.",
 "Rot spreads to the four orthogonal neighbours only, not diagonally, and it spreads to **all** neighbours simultaneously each minute?",
 "If there are no fresh oranges at all, should I return 0? I want to confirm it is 0 and not −1, because that edge case is what most wrong submissions get wrong.",
 "If some fresh orange is unreachable, I return −1 for the whole grid?",
 "May I modify the grid in place to mark newly rotten cells?",
],
"understand":
 "Every minute, any fresh orange orthogonally adjacent to a rotten one becomes rotten. I "
 "must return the number of minutes until no fresh orange remains, or −1 if that never "
 "happens.\n\n"
 "The key reframing: this is a **shortest-path** question in disguise. The answer is the "
 "maximum, over all fresh oranges, of the distance from that orange to its nearest rotten "
 "orange. Shortest path on an unweighted grid means BFS. The twist is that there are many "
 "starting points, not one, so it is a **multi-source** BFS: I put every rotten orange into "
 "the queue before the search begins, which is exactly equivalent to adding a virtual super-"
 "source connected to all of them at distance zero. Each BFS level is then one minute of "
 "simulated time.",
"brute_en":
 "Simulate the clock literally. For each minute, scan the entire grid and build a list of "
 "every fresh orange that has a rotten neighbour right now. After the scan finishes, turn all "
 "of those to rotten together. Repeat, counting minutes, until a full scan finds nothing new "
 "to rot. Then scan once more: if any fresh orange remains it is unreachable, so return "
 "−1; otherwise return the minute count.\n\n"
 "The one detail that must be right is that the newly-rotten cells are collected first and "
 "committed afterwards. If I flip cells to rotten during the scan, the rot can cascade several "
 "steps within a single minute and the answer comes out too small.",
"brute_ds":
 "- A list `to_rot` holding the coordinates that will turn rotten at the end of the current minute.\n"
 "- The grid itself, mutated after each minute.\n"
 "- An integer minute counter.",
"brute_algo": [
 "Set `minutes = 0`.",
 "Loop forever: clear `to_rot`, then scan every cell of the grid.",
 "For each cell holding a `1`, check its four neighbours. If any neighbour holds a `2`, append this cell's coordinates to `to_rot`.",
 "If `to_rot` is empty, the process has stalled: break out of the loop.",
 "Otherwise set every coordinate in `to_rot` to `2` and increment `minutes` by one. Committing after the scan is what keeps the rot to exactly one step per minute.",
 "After the loop, scan the grid one final time. If any `1` remains, return −1.",
 "Otherwise return `minutes`. Note that a grid with no fresh oranges never enters a productive iteration, so it naturally returns 0.",
],
"brute_cx":
 "**Time: O((m·n)²) in the worst case.** One minute of simulation costs a full grid "
 "scan, O(m·n). The number of minutes is the largest distance from a fresh orange to the "
 "nearest rotten one, which for a snaking corridor of oranges is on the order of m·n. "
 "Multiplying gives O((m·n)²).\n\n"
 "**Space: O(m·n)** for the `to_rot` list, which in the first minute can hold a constant "
 "fraction of the grid.",
"brute_code":
'''def orangesRotting_brute(grid):
    """Literal minute-by-minute simulation with a full grid scan per minute."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    minutes = 0

    while True:
        to_rot = []
        # Scan the WHOLE grid to find what rots this minute.
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 1:
                    continue
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 2:
                        to_rot.append((r, c))
                        break
        if not to_rot:
            break                          # nothing changed -> the process stalled

        # *** Commit AFTER the scan. Flipping cells during the scan would let
        # the rot cascade several steps inside a single minute. ***
        for r, c in to_rot:
            grid[r][c] = 2
        minutes += 1

    # Anything still fresh was unreachable.
    for row in grid:
        if 1 in row:
            return -1
    return minutes''',
"brute_limit":
 "Every minute I rescan the entire grid even though only the cells next to last minute's "
 "newly-rotten oranges can possibly change. In a 1000 × 1000 grid with a long corridor, "
 "that is a million cells examined per minute for perhaps a million minutes.\n\n"
 "The realisation is that I already know exactly which cells rotted last minute; those are "
 "the only useful frontier. Keeping that frontier explicitly in a queue removes the scan "
 "entirely, and a queue processed one level at a time is just BFS.",
"opt_en":
 "Do a single BFS whose queue is seeded with **every** rotten orange at once, and count the "
 "fresh oranges while seeding. Then process the queue one full level at a time: pop exactly "
 "the number of items currently in the queue, rot each of their fresh neighbours, push those "
 "neighbours, and decrement the fresh counter for each. One completed level equals one minute.\n\n"
 "Because BFS expands in order of distance, the level at which a fresh orange is reached is "
 "precisely its distance to the nearest rotten orange, which is when it actually rots. When "
 "the queue empties, if the fresh counter is zero every orange was reached and the level count "
 "is the answer; if it is positive, those oranges are in a region no rot can enter, so I "
 "return −1.",
"opt_ds":
 "- A **deque** as a FIFO queue holding the coordinates of the current rot frontier.\n"
 "- An integer `fresh` counting remaining fresh oranges, which gives an O(1) termination "
 "test and removes the need for a final full scan.\n"
 "- The grid itself, mutated to `2`, doubling as the visited marker.",
"opt_algo": [
 "Scan the grid once. Push every cell containing `2` into the queue, and count every cell containing `1` into `fresh`.",
 "If `fresh == 0`, return 0 immediately. There is nothing to rot, so the answer is zero minutes, never −1.",
 "Set `minutes = 0`.",
 "While the queue is non-empty **and** `fresh > 0`: increment `minutes`, then snapshot `len(q)` and pop exactly that many cells, which is precisely the previous minute's frontier.",
 "For each popped cell, look at its four neighbours. For a neighbour that is in bounds and equal to `1`, set it to `2`, decrement `fresh`, and push it.",
 "The `and fresh` in the loop condition matters: after the last orange rots the queue still holds that final frontier, and looping again would increment `minutes` one time too many for a minute in which nothing happens.",
 "After the loop, return `minutes` if `fresh == 0`, otherwise −1.",
],
"opt_code":
'''from collections import deque

def orangesRotting(grid):
    """Multi-source BFS. One BFS level == one minute of wall-clock time."""
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    q = deque()
    fresh = 0
    # Seed the queue with EVERY rotten orange before the search starts.
    # This is equivalent to a virtual super-source at distance 0 from them all.
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0          # *** nothing to rot -> 0 minutes, NOT -1 ***

    minutes = 0
    # "and fresh" stops us counting one extra minute after the last orange rots.
    while q and fresh:
        minutes += 1
        for _ in range(len(q)):        # snapshot the level size FIRST
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2   # rot it now == mark visited on enqueue
                    fresh -= 1
                    q.append((nr, nc))

    # Anything still fresh sits in a region the rot could never reach.
    return minutes if fresh == 0 else -1''',
"opt_cx":
 "**Time: O(m·n).** The seeding scan is O(m·n). Each cell is enqueued at most once, "
 "because it is flipped to `2` the instant it is queued, and each dequeue does constant work "
 "over four neighbours.\n\n"
 "**Space: O(m·n).** In the worst case the initial frontier is most of the grid.\n\n"
 "**Say this out loud:** \"Shortest time to reach every cell from any of several starting "
 "points is multi-source BFS. I seed all rotten oranges before starting, and I process the "
 "queue one level at a time so a level equals a minute. Each cell enters the queue once, so "
 "O(m·n).\"\n\n"
 "**The two gotchas that decide this problem:** the `fresh == 0` early return, which must be "
 "0 and not −1; and `while q and fresh`, which prevents an off-by-one extra minute. Both "
 "are worth stating before you write them.",
},

{
"num": 207, "title": "Course Schedule", "stars": "★", "day": DAY,
"pattern": "Cycle detection / topological sort (Kahn)", "opt_cx_short": "O(V + E) time, O(V + E) space",
"clarify": [
 "To pin the edge direction: does `[a, b]` mean \"to take course a you must first take b\"? Then the dependency edge runs **b → a**. Getting this backwards is the single most common bug here, so I want to confirm it explicitly.",
 "Can the prerequisite list contain duplicate pairs, or a self-loop like `[1, 1]`? A self-loop is an immediate cycle.",
 "Is the graph guaranteed connected? I will assume not, and handle a forest.",
 "Do I only need the boolean, or will you also want the actual ordering? Kahn's algorithm gives me the order for free, so I will build it in a way that extends to Course Schedule II.",
],
"understand":
 "There are `numCourses` courses labelled `0` to `numCourses - 1`, and a list of prerequisite "
 "pairs. I must decide whether it is possible to finish all courses.\n\n"
 "Modelled as a directed graph with courses as vertices and \"must come before\" as edges, "
 "the schedule is feasible exactly when the graph is a **DAG** &mdash; it has no directed "
 "cycle. A cycle means a set of courses each waiting on another, which can never start. So "
 "the entire question is: **does this directed graph contain a cycle?**",
"brute_en":
 "Check each course independently by brute-force path exploration. For a given course, walk "
 "every directed path leaving it, following prerequisites forward, and see whether any path "
 "ever returns to that same course. If it does, that course sits on a cycle and the answer is "
 "False. Repeat for all courses; if no course is ever reachable from itself, the answer is True.\n\n"
 "Crucially this version keeps no memoisation across explorations and no global visited set. "
 "It only tracks the nodes on the current path, which is enough to avoid looping forever, but "
 "means the same subgraph is re-explored along every path that reaches it.",
"brute_ds":
 "- An **adjacency list**, a dict mapping each course to the list of courses that depend on it.\n"
 "- A `path` set holding the nodes on the current recursion stack, used to stop infinite descent.\n"
 "- The call stack for the recursion.",
"brute_algo": [
 "Build the adjacency list: for each pair `[course, prereq]`, append `course` to `adj[prereq]`, giving the edge `prereq → course`.",
 "Define `reaches(node, start, path)` returning True if a directed path from `node` gets back to `start`.",
 "Inside it, iterate over every neighbour of `node`. If the neighbour equals `start`, a cycle through `start` exists, so return True.",
 "If the neighbour is already in `path`, skip it: continuing would loop forever, and any cycle it belongs to will be discovered when that node is itself used as `start`.",
 "Otherwise add the neighbour to `path`, recurse into it, and remove it again on the way out so other branches can still explore it.",
 "Call `reaches(c, c, {c})` for every course `c`. If any call returns True, return False from the outer function.",
 "If no course reaches itself, return True.",
],
"brute_cx":
 "**Time: O(V · (V + E)) at best and exponential in the worst case.** Each of the V "
 "starting courses launches its own exploration, and because there is no memoisation across "
 "branches, a graph shaped like a chain of diamonds forces the same downstream subgraph to be "
 "re-walked once per distinct path reaching it, and the number of distinct paths can double "
 "with each diamond. That is the exponential blow-up.\n\n"
 "**Space: O(V + E)** for the adjacency list, plus O(V) for the recursion depth and the `path` set.",
"brute_code":
'''from collections import defaultdict

def canFinish_brute(numCourses, prerequisites):
    """For every course, ask 'can I get back to myself?'. No memoisation at all,
    so shared subgraphs are re-explored along every path that reaches them."""
    adj = defaultdict(list)
    for course, prereq in prerequisites:
        adj[prereq].append(course)        # edge prereq -> course

    def reaches(node, start, path):
        """True if some directed path from `node` returns to `start`."""
        for nxt in adj[node]:
            if nxt == start:
                return True               # closed the loop back to start
            if nxt in path:
                continue                  # already on this path; do not recurse forever
            path.add(nxt)
            if reaches(nxt, start, path):
                return True
            path.remove(nxt)              # backtrack: other branches may still use it
        return False

    for c in range(numCourses):
        if reaches(c, c, {c}):            # c lies on a cycle
            return False
    return True''',
"brute_limit":
 "Two separate wastes. First, the answer is a single global property &mdash; \"is there a "
 "cycle anywhere?\" &mdash; yet I ask it V times, once per course. Second, within a single "
 "exploration nothing is remembered, so a vertex reachable by many different paths is expanded "
 "many times, which is where the exponential behaviour comes from.\n\n"
 "The insight that fixes both: a course is takeable as soon as all of its prerequisites are "
 "done. If I peel off courses that currently have zero outstanding prerequisites and remove "
 "their outgoing edges, a DAG collapses completely. Anything left over is, by definition, "
 "waiting on itself &mdash; a cycle. That turns V explorations into one linear pass.",
"opt_en":
 "Use Kahn's algorithm, which is topological sort by indegree peeling. The indegree of a "
 "course is the number of prerequisites it is still waiting on. Any course with indegree 0 can "
 "be taken right now, so seed a queue with all of them. Pop a course, count it as completed, "
 "and for every course that depended on it decrement that course's indegree; if a decrement "
 "brings an indegree to 0, that course has just become takeable, so push it.\n\n"
 "When the queue empties, compare the number of completed courses to `numCourses`. If they "
 "match, every course was scheduled and the graph is a DAG. If some courses are left over, "
 "none of them ever reached indegree 0, which means each is waiting on another leftover: that "
 "is exactly a cycle.\n\n"
 "As an alternative I would mention DFS with three colours &mdash; white unvisited, grey on "
 "the current stack, black fully finished &mdash; where meeting a grey node means a back edge "
 "and therefore a cycle. Same complexity; Kahn is easier to explain and gives the ordering "
 "directly for the Course Schedule II follow-up.",
"opt_ds":
 "- An **adjacency list** `adj`, mapping prerequisite → list of dependent courses.\n"
 "- An **indegree array** of length `numCourses`, the count of unmet prerequisites per course. "
 "This is the structure that replaces all the repeated searching.\n"
 "- A **deque** as a FIFO queue of currently-takeable courses. A stack would work equally "
 "well here, since any topological order is acceptable.\n"
 "- An integer counter of completed courses.",
"opt_algo": [
 "Create `adj` as an empty adjacency list and `indeg` as an array of `numCourses` zeros.",
 "For each pair `[course, prereq]`: append `course` to `adj[prereq]`, and increment `indeg[course]` by one.",
 "Initialise the queue with every course `i` whose `indeg[i]` is 0. These need no prerequisites and can be taken immediately.",
 "Set `done = 0`.",
 "While the queue is non-empty: pop a course, increment `done`.",
 "For each dependent `nei` in `adj[course]`, decrement `indeg[nei]`. If it reaches 0, all of that course's prerequisites are now satisfied, so push it.",
 "After the loop, return `done == numCourses`.",
 "For Course Schedule II, append each popped course to an output list; that list is a valid ordering, and if `done < numCourses` return an empty list instead.",
],
"opt_code":
'''from collections import defaultdict, deque

def canFinish(numCourses, prerequisites):
    """Kahn's topological sort. If we cannot schedule every course, the leftovers
    form a cycle."""
    adj = defaultdict(list)
    indeg = [0] * numCourses

    for course, prereq in prerequisites:
        adj[prereq].append(course)        # *** direction: prereq -> course ***
        indeg[course] += 1                # `course` waits on one more thing

    # Everything with no outstanding prerequisites can be taken right now.
    q = deque(i for i in range(numCourses) if indeg[i] == 0)

    done = 0
    while q:
        node = q.popleft()
        done += 1                         # this course is now completed
        for nei in adj[node]:
            indeg[nei] -= 1               # one prerequisite satisfied
            if indeg[nei] == 0:           # all satisfied -> it just became takeable
                q.append(nei)

    # Leftover courses never hit indegree 0 => each waits on another leftover => cycle.
    return done == numCourses''',
"opt_cx":
 "**Time: O(V + E).** Building the graph touches every edge once. Each vertex is enqueued and "
 "dequeued at most once, and each edge is relaxed exactly once, when its source vertex is "
 "popped.\n\n"
 "**Space: O(V + E)** for the adjacency list and indegree array, plus O(V) for the queue.\n\n"
 "**Say this out loud:** \"Feasibility of a dependency schedule is the same as asking whether "
 "the directed graph is acyclic. My indegree array holds how many prerequisites each course "
 "is still waiting on. I pop courses whose count has reached zero, because those are exactly "
 "the ones that are now takeable. Every vertex and every edge is handled once, so O(V + E).\"\n\n"
 "**The gotcha:** the edge direction. `[a, b]` means b before a, so the edge is b → a and "
 "the indegree belongs to a. Say this while you type it.",
},

{
"num": 127, "title": "Word Ladder", "stars": "★★  Amazon favourite", "day": DAY,
"pattern": "BFS on an implicit graph", "opt_cx_short": "O(N · L · 26) time, O(N · L) space",
"clarify": [
 "Do all words have the same length? And are they lowercase English letters only? That decides whether generating neighbours over a 26-letter alphabet is valid.",
 "Does the returned length count the words in the sequence including `beginWord` and `endWord`? So a direct one-letter change gives 2, not 1.",
 "Does `beginWord` need to be in `wordList`? Standard statement says no, but `endWord` must be, otherwise the answer is 0.",
 "Roughly how many words and how long are they? If N is large and L is small, generating neighbours beats comparing pairs; if L were enormous the trade-off flips.",
 "Do you want just the length, or the actual sequence? The sequence variant (Word Ladder II) needs parent tracking, so I want to know before I choose the structure.",
],
"understand":
 "I am given a start word, an end word, and a dictionary. Each step may change exactly one "
 "letter, and every intermediate word must exist in the dictionary. I must return the number "
 "of words in the shortest such sequence, or 0 if none exists.\n\n"
 "This is a graph problem where the vertices are dictionary words and an edge joins two words "
 "differing in exactly one position. The graph is **implicit**: nobody hands me the adjacency "
 "list, I have to produce neighbours on demand. And because every edge costs the same one "
 "step, shortest path on an unweighted graph means **BFS** &mdash; not DFS, and not Dijkstra. "
 "The whole design problem is how to produce a word's neighbours cheaply.",
"brute_en":
 "Explore transformation sequences exhaustively with DFS. From the current word, try every "
 "dictionary word that differs from it in exactly one position and has not been used in the "
 "current chain, recurse into it, and when the end word is reached record the chain length. "
 "Take the minimum over every chain found.\n\n"
 "This is correct because it literally enumerates every valid ladder, but it explores whole "
 "families of long detours before it ever finds a short route, and it can revisit the same "
 "word through a different prefix over and over.",
"brute_ds":
 "- The word list, scanned linearly each time neighbours are needed.\n"
 "- A `used` set holding the words on the current chain, to keep the recursion finite.\n"
 "- The call stack, and a running best-length integer.",
"brute_algo": [
 "Write a helper `differs_by_one(a, b)` that walks both words in parallel, counts positions where the characters differ, and returns True only if the count is exactly 1. This is O(L).",
 "Define `dfs(word, depth)`. If `word == endWord`, update the global best with `depth` and return.",
 "Otherwise loop over every word `w` in the dictionary.",
 "Skip `w` if it is already in `used`, or if `differs_by_one(word, w)` is False.",
 "Add `w` to `used`, call `dfs(w, depth + 1)`, then remove `w` from `used` so a different branch can still use it.",
 "Start with `dfs(beginWord, 1)` and `used = {beginWord}`.",
 "Return the best length found, or 0 if the end word was never reached.",
],
"brute_cx":
 "**Time: O(N! · L) in the worst case.** At the first level up to N words are candidates, "
 "at the second up to N−1, and so on, because backtracking removes words from `used` "
 "again. Each candidacy test costs O(L). In a densely connected dictionary this is factorial "
 "behaviour.\n\n"
 "**Space: O(N · L)** &mdash; recursion depth up to N frames, each holding a word.",
"brute_code":
'''def ladderLength_brute(beginWord, endWord, wordList):
    """Exhaustive DFS over every valid ladder. Correct, catastrophically slow."""
    words = list(wordList)
    if endWord not in words:
        return 0

    def differs_by_one(a, b):
        """True iff a and b differ in exactly one position. O(L)."""
        diff = 0
        for x, y in zip(a, b):
            if x != y:
                diff += 1
                if diff > 1:
                    return False
        return diff == 1

    best = [float('inf')]
    used = {beginWord}

    def dfs(word, depth):
        if word == endWord:
            best[0] = min(best[0], depth)
            return
        if depth >= best[0]:
            return                        # this branch can no longer win
        for w in words:                   # O(N) scan, O(L) test => O(N*L) per node
            if w in used or not differs_by_one(word, w):
                continue
            used.add(w)
            dfs(w, depth + 1)
            used.remove(w)                # backtrack -> the same word is reusable

    dfs(beginWord, 1)
    return 0 if best[0] == float('inf') else best[0]''',
"brute_limit":
 "Two independent problems. First, **DFS is the wrong search order for a shortest-path "
 "question**: it dives down one arbitrary branch to the end before considering the alternative "
 "one step away, so it must explore essentially everything before it can be sure it found the "
 "minimum. BFS finds the shortest path the first time it touches the target, and can stop.\n\n"
 "Second, **finding neighbours by scanning the dictionary is O(N·L) per word**. There are "
 "only L × 26 possible one-letter variants of a word regardless of how big the dictionary "
 "is, so I can generate those directly and test each for membership in a set in O(1). For a "
 "large dictionary of short words that is dramatically cheaper.",
"opt_en":
 "Run BFS from `beginWord`, with the queue holding `(word, steps_so_far)`. Because BFS visits "
 "vertices in nondecreasing distance order, the first time `endWord` is popped, the recorded "
 "step count is the shortest possible, and I return immediately.\n\n"
 "To generate the neighbours of a word without touching the dictionary, I take each of its L "
 "positions in turn and substitute each of the 26 lowercase letters, giving L × 26 "
 "candidate strings. A candidate is a real neighbour precisely when it is in the dictionary "
 "**set**, which is an O(L) hash lookup rather than an O(N·L) scan.\n\n"
 "The visited set must be updated **when a word is enqueued**, not when it is dequeued. If I "
 "wait until dequeue, the same word can be pushed by several nodes on the same level and gets "
 "expanded several times.",
"opt_ds":
 "- A **hash set** of the dictionary, converting the neighbour test from an O(N·L) scan "
 "into an O(L) lookup. This is the single change that makes the algorithm fast.\n"
 "- A **deque** as a FIFO queue of `(word, steps)` pairs. Storing the step count in the queue "
 "avoids needing a separate distance map.\n"
 "- A **`seen` set** of already-enqueued words, which prevents both cycles and duplicate work.",
"opt_algo": [
 "Convert `wordList` to a set. If `endWord` is not in it, return 0 straight away, since no valid ladder can end there.",
 "Initialise the queue with `(beginWord, 1)` &mdash; 1 because the count includes the start word &mdash; and `seen = {beginWord}`.",
 "While the queue is non-empty, pop `(word, steps)` from the front.",
 "If `word == endWord`, return `steps`. BFS guarantees this is the minimum.",
 "Otherwise, for each index `i` in the word and each letter `c` from `'a'` to `'z'`, form `cand = word[:i] + c + word[i+1:]`.",
 "If `cand` is in the dictionary set and not in `seen`, add it to `seen` **now**, and push `(cand, steps + 1)`.",
 "If the queue drains without finding `endWord`, return 0: no ladder exists.",
],
"opt_code":
'''from collections import deque

def ladderLength(beginWord, endWord, wordList):
    """BFS over an implicit graph. Neighbours are GENERATED (L*26 of them),
    not found by scanning the dictionary."""
    words = set(wordList)                 # O(1) membership instead of an O(N) scan
    if endWord not in words:
        return 0                          # unreachable by definition

    q = deque([(beginWord, 1)])           # 1: the count includes beginWord itself
    seen = {beginWord}

    while q:
        word, steps = q.popleft()
        if word == endWord:
            return steps                  # BFS => the first arrival is the shortest

        # Generate every one-letter mutation: L positions x 26 letters.
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                cand = word[:i] + c + word[i + 1:]
                if cand in words and cand not in seen:
                    seen.add(cand)        # *** mark ON ENQUEUE ***
                    q.append((cand, steps + 1))

    return 0                              # queue drained, endWord never reached''',
"opt_cx":
 "**Time: O(N · L²), often written O(N · L · 26).** Each of the N words is "
 "dequeued at most once. For each, I build L × 26 candidates, and building one candidate "
 "string plus hashing it is O(L). So per word it is O(26 · L · L), and 26 is a "
 "constant.\n\n"
 "**Space: O(N · L)** for the dictionary set, the seen set and the queue.\n\n"
 "**Say this out loud:** \"Shortest transformation means unweighted shortest path, so BFS, not "
 "DFS. The graph is implicit, so my real design decision is how to enumerate neighbours: L "
 "× 26 generated candidates tested against a hash set, rather than comparing against all "
 "N words.\"\n\n"
 "**The follow-up they want:** **bidirectional BFS.** Search forward from `beginWord` and "
 "backward from `endWord` at the same time, always expanding the smaller frontier, and stop "
 "when the two frontiers touch. Since a frontier grows roughly like b^d, two searches of depth "
 "d/2 cost about 2·b^(d/2) instead of b^d &mdash; a large constant-factor win. Mentioning "
 "this unprompted is what distinguishes a strong answer here.",
},

{
"num": 236, "title": "Lowest Common Ancestor of a Binary Tree", "stars": "★★  Amazon favourite",
"day": DAY, "pattern": "Post-order DFS returning information upward",
"opt_cx_short": "O(n) time, O(h) space",
"clarify": [
 "Are `p` and `q` **guaranteed to exist** in the tree? The standard problem guarantees it, and my clean solution relies on that guarantee. If they might be absent I need a different return protocol, which I will describe.",
 "Is a node allowed to be its own ancestor? The usual definition says yes, so if `p` is an ancestor of `q` the answer is `p`.",
 "Are the node values unique, and am I comparing by identity or by value? I will compare by identity with `is`, which is safe even with duplicate values.",
 "Is this a plain binary tree or a BST? A BST admits a simpler O(h) solution using value comparisons; I am assuming a plain binary tree.",
 "Do the nodes have parent pointers? If they did, this reduces to finding the intersection of two linked lists.",
],
"understand":
 "Given the root of a binary tree and two nodes `p` and `q`, I must return their lowest common "
 "ancestor: the deepest node that has both `p` and `q` somewhere in its subtree, where a node "
 "counts as a descendant of itself.\n\n"
 "The structural fact that drives everything: for the LCA node, `p` and `q` lie in "
 "**different** subtrees &mdash; one on the left, one on the right &mdash; unless one of them "
 "*is* the LCA. Above the LCA both targets are on the same side; below it, at most one target "
 "is present. So the LCA is exactly the unique node where the two targets \"split\". That "
 "makes it a bottom-up question, which means post-order DFS: solve both children first, then "
 "decide about the current node.",
"brute_en":
 "Directly encode the definition. Write a helper `contains(node, target)` that reports whether "
 "a target lives anywhere in a given subtree. Then walk every node of the tree and ask: does "
 "my left subtree, my right subtree, or I myself hold both `p` and `q`? Every node that "
 "contains both is a common ancestor. Among all of them, the answer is the deepest, so track "
 "depth and keep the deepest one seen.\n\n"
 "It is obviously correct because it is a literal translation of the definition, but the "
 "`contains` calls repeat enormous amounts of work.",
"brute_ds":
 "- The call stack for two nested recursions, the outer walk and the inner containment check.\n"
 "- Two variables holding the best node found so far and its depth.",
"brute_algo": [
 "Write `contains(node, target)`: return False for a null node, True if `node is target`, otherwise the OR of the recursive calls on the two children. This is O(n).",
 "Write `walk(node, depth)` that visits every node in the tree.",
 "At each node, evaluate `contains(node, p) and contains(node, q)`.",
 "If both are true, this node is a common ancestor; if its `depth` exceeds the best depth seen so far, record it as the new answer.",
 "Recurse into both children with `depth + 1`.",
 "Call `walk(root, 0)` and return the recorded node.",
],
"brute_cx":
 "**Time: O(n²).** The outer walk visits n nodes, and at each one the two `contains` calls "
 "each cost O(size of that subtree), which is O(n) near the root. Summed over a balanced tree "
 "this is O(n log n); over a degenerate, list-shaped tree it is O(n²), since the subtree "
 "sizes are n, n−1, n−2 and so on.\n\n"
 "**Space: O(h)** for the recursion, where h is the height &mdash; O(log n) balanced, O(n) "
 "degenerate.",
"brute_code":
'''def lowestCommonAncestor_brute(root, p, q):
    """Literal definition: find every node containing both targets, keep the deepest."""

    def contains(node, target):
        """Does `target` appear anywhere in this subtree? O(size of subtree)."""
        if not node:
            return False
        if node is target:
            return True
        return contains(node.left, target) or contains(node.right, target)

    best = [None, -1]                     # [node, depth of that node]

    def walk(node, depth):
        if not node:
            return
        # Two full subtree scans at EVERY node -- this is the quadratic part.
        if contains(node, p) and contains(node, q):
            if depth > best[1]:           # deeper common ancestor wins
                best[0], best[1] = node, depth
        walk(node.left, depth + 1)
        walk(node.right, depth + 1)

    walk(root, 0)
    return best[0]''',
"brute_limit":
 "Every `contains` call re-descends a subtree that the outer walk is about to descend anyway, "
 "and a node near the root is scanned once for itself and again as part of each of its "
 "ancestors' checks. The same subtree is traversed over and over to answer the same question.\n\n"
 "The realisation: a single post-order traversal can compute, for every node at once, whether "
 "its subtree contains a target &mdash; because that answer is just the OR of what its "
 "children report plus whether the node is itself a target. If each recursive call *returns* "
 "that information upward, one traversal replaces all of the nested scans.",
"opt_en":
 "One post-order DFS in which each call returns a single node, under this contract: *return "
 "the LCA if it is inside this subtree; otherwise return `p` or `q` if exactly one of them is "
 "here; otherwise return null.*\n\n"
 "The base case does the finding: if the current node is null, or is `p`, or is `q`, return it "
 "as is. Otherwise recurse into both children and inspect the two results. If **both** are "
 "non-null, then one target was found on the left and the other on the right, so the two "
 "targets split exactly here and the current node is the LCA. If only one side is non-null, "
 "both targets live on that side (or only one target exists at all), so I pass that result "
 "straight up. If both are null, this subtree is irrelevant and I return null.\n\n"
 "The elegant part is that the case \"`p` is an ancestor of `q`\" needs no special handling: "
 "the recursion stops at `p` and returns it, and since `q` lies below `p` no other branch "
 "returns anything, so `p` propagates to the top &mdash; which is the correct answer.",
"opt_ds":
 "- No auxiliary data structure at all. The **call stack** carries the state, and the "
 "**return value** is the channel that carries information from the leaves back to the root.\n"
 "- That is the whole point of the optimisation: replacing an explicit search with a "
 "well-chosen return contract.",
"opt_algo": [
 "If `root` is null, return null &mdash; nothing here.",
 "If `root is p` or `root is q`, return `root`. Do not keep searching below: if the other target is beneath this one, this node is already the answer.",
 "Recurse on the left child, storing the result in `left`.",
 "Recurse on the right child, storing the result in `right`.",
 "If `left` and `right` are both non-null, the two targets were found on opposite sides, so `root` is the LCA. Return `root`.",
 "Otherwise return whichever of `left` and `right` is non-null, or null if neither is. In Python that is exactly `left or right`.",
 "Note the order: the two recursive calls happen before any decision. That is what makes it post-order, and post-order is what lets information flow upward.",
],
"opt_code":
'''def lowestCommonAncestor(root, p, q):
    """Post-order DFS. Contract for the return value:
         - the LCA, if it is inside this subtree; else
         - p or q, if exactly one of them is in this subtree; else
         - None.
    """
    # Base case: nothing here, or we just landed on one of the targets.
    # Returning immediately also handles 'p is an ancestor of q' for free.
    if not root or root is p or root is q:
        return root

    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    if left and right:
        return root       # p and q were found on OPPOSITE sides -> they split here

    # Exactly one side (or neither) reported something: pass it straight up.
    return left or right''',
"opt_cx":
 "**Time: O(n).** Each node is visited exactly once and does O(1) work beyond its two "
 "recursive calls.\n\n"
 "**Space: O(h)** for the recursion stack &mdash; O(log n) for a balanced tree, O(n) for a "
 "degenerate one. There is no auxiliary structure.\n\n"
 "**Say this out loud:** \"This is post-order DFS with information flowing upward. Each call "
 "returns the LCA if it is in that subtree, otherwise whichever target it found. When both "
 "children return something non-null, the targets split at me, so I am the LCA. Each node is "
 "visited once, so O(n) time and O(h) stack.\"\n\n"
 "**The follow-up to have ready:** *what if `p` or `q` might not be in the tree?* This version "
 "would wrongly return `p` when `q` is absent, because it cannot distinguish \"found both\" "
 "from \"found one\". The fix is to keep two boolean flags set at the moment each target is "
 "matched, run the same recursion to completion without early-returning, and only accept the "
 "computed node if both flags ended up true.",
},

{
"num": 102, "title": "Binary Tree Level Order Traversal", "stars": "", "day": DAY,
"pattern": "BFS with a level-size snapshot", "opt_cx_short": "O(n) time, O(w) space",
"clarify": [
 "Should the output be a list of lists, one inner list per level, top to bottom? And an empty tree returns `[]` rather than `[[]]`?",
 "Within a level, must the order be strictly left to right? That determines that I need a FIFO queue rather than a stack.",
 "Should I output node values or node references? Values, I assume.",
 "Can the tree be very deep or very wide? That affects whether recursion is safe, and it decides the real space bound.",
],
"understand":
 "Given the root of a binary tree, return its node values level by level: the root's level "
 "first, then its children, and so on, with each level as its own list and each level ordered "
 "left to right.\n\n"
 "Visiting nodes in nondecreasing depth order is exactly what BFS does. The only extra "
 "requirement beyond ordinary BFS is knowing **where one level ends and the next begins**, so "
 "that the output can be grouped. That single requirement is the whole problem, and the "
 "technique that solves it &mdash; snapshotting the queue length before draining a level "
 "&mdash; is reused in Rotting Oranges, All Nodes Distance K, zigzag traversal, right-side "
 "view, and every other level-aware BFS.",
"brute_en":
 "Attack one level at a time, independently. First compute the height of the tree. Then, for "
 "each depth `d` from 0 up to height minus 1, traverse the **entire tree from the root** and "
 "collect the values of nodes that happen to sit at depth `d`, appending the resulting list to "
 "the output.\n\n"
 "It is correct because a DFS that carries a depth counter and appends only when the counter "
 "equals `d` visits the level's nodes left to right. But it re-walks the whole tree once per "
 "level.",
"brute_ds":
 "- The call stack, for the height computation and for one full traversal per level.\n"
 "- One list per level, plus the output list of lists.",
"brute_algo": [
 "Compute the height: an empty node has height 0, otherwise it is 1 plus the larger of the two children's heights.",
 "For `d` from 0 to `height - 1`, create an empty `level` list.",
 "Run a full DFS from the root carrying the current depth.",
 "If the current depth equals `d`, append this node's value to `level` and stop descending, since nothing below can be at depth `d`.",
 "Otherwise recurse left then right, in that order, so the level comes out left to right.",
 "Append `level` to the output.",
 "Return the output.",
],
"brute_cx":
 "**Time: O(n · h).** Each of the h levels triggers a traversal that can touch up to n "
 "nodes. For a balanced tree h is log n, giving O(n log n); for a degenerate list-shaped tree "
 "h is n, giving **O(n²)**.\n\n"
 "**Space: O(h)** for the recursion, plus O(n) for the output, which is required by the "
 "problem and is not really overhead.",
"brute_code":
'''def levelOrder_brute(root):
    """One full traversal per level. Correct, but re-walks the tree h times."""
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    def collect(node, depth, target, out):
        """Append values of nodes sitting exactly at depth == target."""
        if not node:
            return
        if depth == target:
            out.append(node.val)
            return                        # nothing deeper can be at `target`
        collect(node.left,  depth + 1, target, out)   # left first =>
        collect(node.right, depth + 1, target, out)   # left-to-right order

    result = []
    for d in range(height(root)):
        level = []
        collect(root, 0, d, level)        # re-walks from the root EVERY time
        result.append(level)
    return result''',
"brute_limit":
 "To reach level 5 the traversal must pass through levels 0 to 4 again, and it already did that "
 "on the previous five passes. All the upper levels are re-walked once for every level below "
 "them, which is where the O(n · h) comes from. On a skewed tree that degrades to "
 "quadratic.\n\n"
 "The fix is to keep the frontier instead of recomputing it. Once I have finished level `d`, "
 "the nodes of level `d + 1` are precisely the children I just saw &mdash; I should hold them "
 "in a queue rather than throw them away and rediscover them from the root.",
"opt_en":
 "Standard BFS with one addition. Put the root in a queue. Then, at the top of each outer "
 "iteration, **record the current queue length** &mdash; at that instant the queue holds "
 "exactly the nodes of one level and nothing else. Pop precisely that many nodes, collecting "
 "their values into a fresh `level` list and pushing their children to the back of the queue.\n\n"
 "When the snapshot count is exhausted, the level is complete, and everything now in the queue "
 "belongs to the next level. Append the `level` list to the output and repeat until the queue "
 "is empty. Because a node's children are always pushed behind every node of the current "
 "level, the FIFO ordering keeps each level in left-to-right order automatically.\n\n"
 "The reason for taking the snapshot **before** the inner loop is that the queue grows during "
 "the loop; testing against a live `len(q)` would spill the next level into the current one.",
"opt_ds":
 "- A **deque** used strictly as a FIFO queue. FIFO is what preserves left-to-right order "
 "within a level; a stack would reverse and interleave levels.\n"
 "- A **level-size integer snapshot** &mdash; the whole trick, and it needs no extra memory "
 "beyond one variable. The alternative of pushing `(node, depth)` pairs also works but stores "
 "an integer per node for no benefit.\n"
 "- The output list of lists.",
"opt_algo": [
 "If `root` is null, return an empty list.",
 "Initialise the queue with the root, and the output as an empty list.",
 "While the queue is non-empty: create an empty `level` list.",
 "Take `n = len(q)` **now**, before popping anything. Those n nodes are exactly the current level.",
 "Repeat n times: pop the front node, append its value to `level`, and push its left child then its right child, skipping nulls. Left before right is what preserves the required order.",
 "After the n pops, append `level` to the output. The queue now holds exactly the next level.",
 "When the queue empties, return the output.",
],
"opt_code":
'''from collections import deque

def levelOrder(root):
    """BFS. `for _ in range(len(q))` snapshots the level size and is the only
    idea in this problem -- every level-aware BFS reuses it."""
    if not root:
        return []

    out = []
    q = deque([root])

    while q:
        level = []
        # *** snapshot the size BEFORE popping: the queue grows inside this loop ***
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:                 # left pushed first ->
                q.append(node.left)
            if node.right:                # -> preserves left-to-right order
                q.append(node.right)
        out.append(level)                 # queue now holds exactly the next level

    return out''',
"opt_cx":
 "**Time: O(n).** Every node is enqueued once and dequeued once, doing O(1) work each time.\n\n"
 "**Space: O(w)** where w is the maximum width of the tree, since the queue never holds more "
 "than one level plus part of the next. For a complete binary tree the bottom level holds about "
 "n/2 nodes, so this is O(n) in the worst case. The output itself is a further O(n), but that "
 "is the required result rather than working space.\n\n"
 "**Say this out loud:** \"BFS, with the queue length snapshotted at the start of each "
 "iteration so I know exactly where the level boundary is. Each node enters and leaves the "
 "queue once, so O(n) time, and the queue is bounded by the widest level.\"\n\n"
 "**The variants this unlocks:** zigzag order (reverse alternate `level` lists, or use a "
 "deque and alternate the append end); right-side view (take the last value of each level); "
 "bottom-up order (reverse the output at the end); and average per level. All of them are the "
 "same loop with one line changed.",
},

{
"num": 417, "title": "Pacific Atlantic Water Flow", "stars": "★  (stretch)", "day": DAY,
"pattern": "Reverse multi-source DFS from the boundary",
"opt_cx_short": "O(m·n) time, O(m·n) space",
"clarify": [
 "Water flows from a cell to a neighbour whose height is **less than or equal to** the current cell &mdash; so equal heights do allow flow in both directions?",
 "The Pacific touches the top and left edges; the Atlantic touches the bottom and right edges. A corner cell such as `(0, 0)` therefore already touches the Pacific before moving at all.",
 "Should the output be a list of `[row, col]` pairs, in any order?",
 "Can the grid be 1 × 1, or a single row? In a single row, every cell touches both the top and bottom edges, so all of them qualify.",
],
"understand":
 "Each cell of the grid has a height. Water flows from a cell to any orthogonal neighbour of "
 "equal or lower height. The Pacific borders the top and left edges, the Atlantic the bottom "
 "and right edges. I must return every cell from which water can reach **both** oceans.\n\n"
 "Stated forwards, that is: for each cell, does some non-increasing path lead off the top or "
 "left edge, and does some non-increasing path lead off the bottom or right edge? The critical "
 "observation is that this is a reachability question, and reachability questions can be run "
 "**backwards**. Instead of asking which cells drain into an ocean, I ask which cells an ocean "
 "can climb up to, which turns thousands of single-source searches into two multi-source ones.",
"brute_en":
 "Take the definition literally. For every cell in the grid, run a fresh DFS that only ever "
 "steps to neighbours of equal or lower height, and record whether that search ever touches "
 "the top or left edge, and whether it ever touches the bottom or right edge. If both flags "
 "come back true, add the cell to the answer.\n\n"
 "Each search needs its own visited set, because a cell that was visited during the search "
 "starting at some other cell tells me nothing about this one &mdash; the searches are "
 "independent.",
"brute_ds":
 "- A fresh `visited` set for **each** of the m·n searches.\n"
 "- Two booleans per search, for Pacific and Atlantic contact.\n"
 "- The call stack for the DFS.",
"brute_algo": [
 "For each cell `(r, c)` of the grid, create an empty `visited` set and two flags set to False.",
 "Run a DFS from `(r, c)`. On entering a cell, if its row is 0 or its column is 0, set the Pacific flag; if its row is the last row or its column is the last column, set the Atlantic flag.",
 "Add the cell to `visited`, then for each of the four neighbours that is in bounds, unvisited, and of height less than or equal to the current cell, recurse into it.",
 "When the DFS finishes, if both flags are true, append `[r, c]` to the answer.",
 "Return the answer list.",
],
"brute_cx":
 "**Time: O((m·n)²).** There are m·n starting cells, and a single downhill DFS can "
 "in the worst case &mdash; a plateau where every height is identical &mdash; visit every one "
 "of the m·n cells.\n\n"
 "**Space: O(m·n)** for one search's visited set and recursion depth. The set is discarded "
 "and rebuilt for the next cell, which is precisely the waste.",
"brute_code":
'''def pacificAtlantic_brute(heights):
    """From every cell, flow downhill and see which oceans we reach. O((mn)^2)."""
    if not heights or not heights[0]:
        return []
    rows, cols = len(heights), len(heights[0])
    result = []

    for sr in range(rows):
        for sc in range(cols):
            visited = set()               # a FRESH set for every start cell
            flags = [False, False]        # [reached Pacific, reached Atlantic]

            def dfs(r, c):
                if (r, c) in visited:
                    return
                visited.add((r, c))
                if r == 0 or c == 0:
                    flags[0] = True       # top or left edge -> Pacific
                if r == rows - 1 or c == cols - 1:
                    flags[1] = True       # bottom or right edge -> Atlantic
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    # water only flows to an equal or LOWER neighbour
                    if (0 <= nr < rows and 0 <= nc < cols
                            and heights[nr][nc] <= heights[r][c]):
                        dfs(nr, nc)

            dfs(sr, sc)
            if flags[0] and flags[1]:
                result.append([sr, sc])
    return result''',
"brute_limit":
 "The m·n searches overlap almost completely: if cell A drains through cell B, then A's "
 "search re-walks the whole downstream region that B's search already covered, and neither can "
 "reuse the other's visited set because each search is anchored to a different origin.\n\n"
 "The inversion removes the redundancy entirely. \"Cell X can reach the Pacific\" is the same "
 "statement as \"the Pacific can reach cell X by walking uphill\". There are only two oceans, "
 "so instead of m·n forward searches I need exactly two reverse searches, each seeded from "
 "a whole border and each visiting any cell at most once.",
"opt_en":
 "Run two multi-source searches, one per ocean, in the reverse direction. For the Pacific, "
 "seed the search at every cell on the top row and every cell on the left column; for the "
 "Atlantic, seed at the bottom row and right column. From a seed, move to a neighbour only if "
 "that neighbour's height is **greater than or equal to** the current height &mdash; that is, "
 "walk uphill, which is exactly the reverse of the direction water flows.\n\n"
 "Each search marks every cell it can reach in its own set. A cell in the Pacific set is a "
 "cell from which water can flow down to the Pacific; likewise for the Atlantic. The answer is "
 "the **intersection** of the two sets.\n\n"
 "The reversal is the entire idea, and it is one of the most reusable tricks in grid problems. "
 "Number of Enclaves, Surrounded Regions and Walls and Gates all use the same move: when a "
 "property is defined by reaching a boundary, start at the boundary.",
"opt_ds":
 "- Two **hash sets** of `(r, c)` tuples, `pac` and `atl`, each doubling as that search's "
 "visited marker and as its result. Using the set for both jobs is what keeps each search "
 "linear.\n"
 "- The call stack for the DFS. BFS with a deque works identically and avoids deep recursion "
 "on a large grid.\n"
 "- Python's set intersection operator `&` for the final combine.",
"opt_algo": [
 "Create two empty sets, `pac` and `atl`.",
 "Write `dfs(r, c, seen, prev_height)`: return immediately if `(r, c)` is out of bounds or already in `seen`, or if `heights[r][c] < prev_height`, since water could not have flowed down from here to where we came from.",
 "Otherwise add `(r, c)` to `seen` and recurse into all four neighbours, passing this cell's height as the new `prev_height`.",
 "Seed the Pacific: for every column `c`, call `dfs(0, c, pac, 0)`. For every row `r`, call `dfs(r, 0, pac, 0)`. Passing 0 as the initial previous height means the seed cell always passes the height test.",
 "Seed the Atlantic: for every column `c`, call `dfs(rows - 1, c, atl, 0)`. For every row `r`, call `dfs(r, cols - 1, atl, 0)`.",
 "Return `[list(cell) for cell in pac & atl]`.",
],
"opt_code":
'''def pacificAtlantic(heights):
    """Invert the question: instead of flowing DOWN from every cell, climb UP
    from each ocean. Two multi-source searches instead of m*n single-source ones."""
    if not heights or not heights[0]:
        return []
    rows, cols = len(heights), len(heights[0])
    pac, atl = set(), set()               # each set is both 'visited' and 'result'

    def dfs(r, c, seen, prev_height):
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in seen:
            return
        if heights[r][c] < prev_height:   # cannot climb DOWN when running in reverse
            return
        seen.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc, seen, heights[r][c])

    for c in range(cols):
        dfs(0, c, pac, 0)                 # top row    -> Pacific
        dfs(rows - 1, c, atl, 0)          # bottom row -> Atlantic
    for r in range(rows):
        dfs(r, 0, pac, 0)                 # left col   -> Pacific
        dfs(r, cols - 1, atl, 0)          # right col  -> Atlantic

    # Cells that drain to BOTH oceans are exactly the intersection.
    return [list(cell) for cell in pac & atl]''',
"opt_cx":
 "**Time: O(m·n).** Each of the two searches adds a cell to its set the first time it "
 "reaches it and never revisits it, so each search is linear in the grid, and there are two "
 "searches. The final intersection is linear in the set sizes.\n\n"
 "**Space: O(m·n)** for the two sets and the recursion depth.\n\n"
 "**Say this out loud:** \"Rather than simulating flow from every cell, I invert it: a cell "
 "reaches an ocean exactly when the ocean reaches it walking uphill. That turns m·n "
 "searches into two multi-source searches, and the answer is the intersection of the two "
 "reachable sets. O(m·n) time and space.\"\n\n"
 "**The transferable pattern:** whenever a grid property is defined by \"can get to the "
 "border\", start the search at the border and reverse the movement rule.",
},

{
"num": 863, "title": "All Nodes Distance K in Binary Tree", "stars": "★  (stretch)", "day": DAY,
"pattern": "Tree → undirected graph, then BFS",
"opt_cx_short": "O(n) time, O(n) space",
"clarify": [
 "Distance means the number of edges on the path between two nodes, travelling either up or down the tree?",
 "If `k == 0`, the answer is just the target node itself?",
 "Are node values unique? The signature gives me the target as a node reference, so I will compare by identity, which is safe regardless.",
 "Should the output be values or nodes, and does the order matter? I will return values in any order.",
 "If fewer nodes exist at distance k than expected, I return whatever exists, possibly an empty list?",
],
"understand":
 "Given the root of a binary tree, a specific target node, and an integer k, I must return the "
 "values of all nodes exactly k edges away from the target &mdash; in **any** direction: "
 "below the target, above it, or across through a sibling subtree.\n\n"
 "The difficulty is entirely structural. A tree's pointers only run downward, so from the "
 "target I can descend but I cannot climb, and yet many of the answers are up and then back "
 "down. Once I add the ability to move from a node to its parent, the tree becomes an "
 "**undirected graph** with the same node set, and \"all nodes at distance exactly k\" is then "
 "the plainest possible BFS: expand k levels from the target and read off the frontier.\n\n"
 "\"Convert the tree into a graph by wiring parent pointers\" is one of the highest-value "
 "reusable tricks in tree interviews.",
"brute_en":
 "Compute the distance from the target to every node independently, using only downward "
 "traversals. For a pair of nodes, the distance is `depth(a) + depth(b) - 2 · "
 "depth(lca(a, b))`, which is the standard path-through-the-ancestor formula. So: walk the "
 "whole tree; for each node, find the LCA of it and the target, compute the three depths with "
 "further traversals, evaluate the formula, and keep the node if the result equals k.\n\n"
 "It is correct because it is the definition of tree distance, but every one of those helper "
 "calls is itself a full traversal.",
"brute_ds":
 "- The call stack for several nested recursions: the outer walk, an LCA search, and a depth "
 "lookup per node.\n"
 "- The output list.",
"brute_algo": [
 "Write `depth(root, node)` that returns the number of edges from the root down to `node`, or −1 if not found. This is O(n).",
 "Write `lca(root, a, b)`, the standard post-order LCA. This is also O(n).",
 "Walk every node `x` in the tree.",
 "For each `x`, compute `l = lca(root, x, target)`, then `d = depth(root, x) + depth(root, target) - 2 * depth(root, l)`.",
 "If `d == k`, append `x.val` to the output.",
 "Return the output.",
],
"brute_cx":
 "**Time: O(n²).** The outer walk visits n nodes and each iteration performs a constant "
 "number of O(n) traversals for the LCA and the depths.\n\n"
 "**Space: O(h)** for the recursion stack, plus the output.",
"brute_code":
'''def distanceK_brute(root, target, k):
    """distance(a, b) = depth(a) + depth(b) - 2 * depth(lca(a, b)).
    Correct, but every helper is a full O(n) traversal."""

    def depth(node, want, d=0):
        """Edges from `node` down to `want`, or -1 if `want` is not below `node`."""
        if not node:
            return -1
        if node is want:
            return d
        left = depth(node.left, want, d + 1)
        if left != -1:
            return left
        return depth(node.right, want, d + 1)

    def lca(node, a, b):
        if not node or node is a or node is b:
            return node
        L, R = lca(node.left, a, b), lca(node.right, a, b)
        return node if (L and R) else (L or R)

    out = []
    d_target = depth(root, target)

    def walk(node):
        if not node:
            return
        anc = lca(root, node, target)                 # O(n)
        d = depth(root, node) + d_target - 2 * depth(root, anc)   # two more O(n) calls
        if d == k:
            out.append(node.val)
        walk(node.left)
        walk(node.right)

    walk(root)
    return out''',
"brute_limit":
 "Every node triggers a fresh LCA search and fresh depth computations from the root, all of "
 "which re-traverse the same upper parts of the tree over and over. The formula is also doing "
 "far more than the question needs: I do not want the distance to *every* node, only the set "
 "of nodes at one specific distance, and BFS produces exactly that set as a by-product of "
 "expanding.\n\n"
 "The real obstacle is only that I cannot walk upward. Fixing that once, with a single "
 "traversal that records each node's parent, removes the need for all the LCA and depth "
 "machinery.",
"opt_en":
 "Two phases. **Phase one:** run one DFS over the tree recording, for every node, a pointer to "
 "its parent in a hash map. The tree now behaves as an undirected graph in which each node has "
 "up to three neighbours: `left`, `right`, and `parent`.\n\n"
 "**Phase two:** run a plain BFS starting from the target node, with a `seen` set to stop the "
 "search from bouncing back into the node it just came from. Process the queue one full level "
 "at a time, tracking the current distance. When the distance counter reaches k, everything "
 "currently in the queue is exactly k edges from the target, so return those values.\n\n"
 "If the queue drains before the distance reaches k, no node is that far away and the answer "
 "is an empty list.",
"opt_ds":
 "- A **hash map** from node to parent node, which is what makes movement bidirectional. This "
 "is the structure that turns an impossible traversal into a routine one.\n"
 "- A **deque** as the BFS queue, drained one level at a time with the `len(q)` snapshot from "
 "problem 102.\n"
 "- A **`seen` set** of nodes, essential here because the graph now contains cycles: a node "
 "and its parent point at each other.",
"opt_algo": [
 "Create an empty `parent` map. Run `wire(node, par)` from the root with `par = None`: record `parent[node] = par`, then recurse into `node.left` and `node.right` with `node` as the parent.",
 "Initialise `seen = {target}` and the queue holding just `target`, and set `dist = 0`.",
 "While the queue is non-empty: if `dist == k`, return the values of every node currently in the queue &mdash; they are all exactly k edges away.",
 "Otherwise snapshot `len(q)` and pop that many nodes, which is the current level.",
 "For each popped node, consider its three neighbours: `node.left`, `node.right`, and `parent[node]`. For each that is non-null and not in `seen`, add it to `seen` and push it.",
 "After the level completes, increment `dist` and loop.",
 "If the queue drains, return an empty list.",
],
"opt_code":
'''from collections import deque

def distanceK(root, target, k):
    """Give every node a parent pointer -> the tree becomes an undirected graph
    -> 'all nodes at distance k' is a plain BFS stopped after k levels."""

    parent = {}

    def wire(node, par):
        """One DFS to record each node's parent."""
        if not node:
            return
        parent[node] = par
        wire(node.left, node)
        wire(node.right, node)

    wire(root, None)

    seen = {target}                       # required: the graph now has cycles
    q = deque([target])
    dist = 0

    while q:
        if dist == k:
            # Everything still queued sits exactly k edges from the target.
            return [n.val for n in q]
        for _ in range(len(q)):           # drain exactly one level
            node = q.popleft()
            # three neighbours now, not two: left, right, and UP
            for nei in (node.left, node.right, parent[node]):
                if nei and nei not in seen:
                    seen.add(nei)         # mark on enqueue
                    q.append(nei)
        dist += 1

    return []                             # no node is that far from the target''',
"opt_cx":
 "**Time: O(n).** The wiring DFS visits each node once. The BFS enqueues each node at most "
 "once, and each dequeue inspects three neighbours, which is constant work.\n\n"
 "**Space: O(n)** for the parent map and the seen set, plus O(h) for the wiring recursion.\n\n"
 "**Say this out loud:** \"The obstacle is that tree edges only point downward, but the answer "
 "includes nodes above the target. So I spend one pass adding parent pointers, which converts "
 "the tree into an undirected graph, and then it is an ordinary BFS from the target stopped "
 "after k levels. O(n) time and space.\"\n\n"
 "**The gotcha:** the `seen` set is not optional here as it was in a pure downward traversal. "
 "Once parents are wired, every edge is bidirectional, so without `seen` the search immediately "
 "oscillates between a node and its parent forever.",
},

]
