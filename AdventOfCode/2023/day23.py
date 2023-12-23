from collections import deque
from copy import copy

# Parse file

trails_map = [
    list(l)
    for l in open("AdventOfCode/2023/examples/day23.in").read().strip().split("\n")
]

start = 1
end = (len(trails_map[-1]) - 2) + (len(trails_map) - 1) * 1j

# Part 1


def walk(n, prev, to, ignore_hill):
    n2 = n + to
    # Not out-of-bounds
    if n2.real < 0 or n2.real >= len(trails_map[0]):
        return None
    if n2.imag < 0 or n2.imag >= len(trails_map):
        return None
    x = int(n2.imag)
    y = int(n2.real)
    # Not in the forrest
    if trails_map[x][y] == "#":
        return None
    # Always downhill
    if not ignore_hill:
        if trails_map[x][y] == ">" and to != 1:
            return None
        if trails_map[x][y] == "<" and to != -1:
            return None
        if trails_map[x][y] == "^" and to != -1j:
            return None
        if trails_map[x][y] == "v" and to != 1j:
            return None
    # Never onto previous tile
    if "/" + str(x) + "," + str(y) + "/" in prev:
        return None
    return (n2, ("/" + str(x) + "," + str(y) + prev))


def neighbors(node, ignore_hill=False):
    n, prev = node
    ns = [
        walk(n, prev, 1, ignore_hill),
        walk(n, prev, -1, ignore_hill),
        walk(n, prev, 1j, ignore_hill),
        walk(n, prev, -1j, ignore_hill),
    ]
    return [m for m in ns if m is not None]


def longest_path():
    q = deque([(start, "/0,1/")])
    p = 0
    while q:
        curr = q.popleft()
        if curr[0] == end:
            p = max(p, curr[1].count("/") - 2)
            continue
        ns = neighbors(curr)
        for n in ns:
            q.append(n)
    return p


print("Part 1:", longest_path())

# Part 2


def graph():
    q = deque([(start, (start, "/0,1/"))])
    cache = set([start])
    g = dict()
    while q:
        init, curr = q.popleft()

        d = 0 if init == curr[0] else 1
        ns = [curr]
        while len(ns) == 1 and ns[0][0] != end:
            c = ns[0]
            ns = neighbors(c, True)
            d += 1

        if len(ns) == 0:
            continue

        if init not in g:
            g[init] = dict()

        if len(ns) == 1:
            if ns[0][0] == end:
                g[init][end] = d
                if end not in g:
                    g[end] = dict()
                g[end][init] = d
            continue

        g[init][c[0]] = d - 1
        if c[0] not in g:
            g[c[0]] = dict()
        g[c[0]][init] = d - 1

        if c[0] not in cache:
            cache.add(c[0])
            for n in ns:
                q.append((c[0], n))

    return g


def longest_path_p2():
    trail_graph = graph()

    q = deque([(start, {start}, 0)])
    p = 0
    while q:
        curr, excl, dist = q.popleft()
        if curr == end:
            p = max(p, dist)
            continue
        for neigh, d in trail_graph[curr].items():
            if neigh not in excl:
                q.append((neigh, excl | {neigh}, dist + d))

    return p


print("Part 2:", longest_path_p2())
