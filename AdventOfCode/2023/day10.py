# Parse file

tiles = [
    [t for t in l.strip()]
    for l in open("AdventOfCode/2023/examples/day10.in").read().strip().split("\n")
]

# Part 1

dir = {
    "7": [(0, -1), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "F": [(0, 1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "|": [(-1, 0), (1, 0)],
    "L": [(0, 1), (-1, 0)],
}


def start():
    for i, l in enumerate(tiles):
        for j, t in enumerate(l):
            if t == "S":
                return (i, j)


def starting_tile(sp):
    neighbors = []
    for h in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        (i, j) = (sp[0] + h[0]), (sp[1] + h[1])
        if i >= 0 and i < len(tiles) and j >= 0 and j < len(tiles[i]):
            if tiles[i][j] == ".":
                continue
            a, b = dir[tiles[i][j]]
            (ai, aj) = (i + a[0]), (j + a[1])
            if (ai, aj) == sp:
                neighbors.append(h)
            (bi, bj) = (i + b[0]), (j + b[1])
            if (bi, bj) == sp:
                neighbors.append(h)
    if len(neighbors) == 2:
        for t, d in dir.items():
            if (d[0] == neighbors[0] and d[1] == neighbors[1]) or (
                d[1] == neighbors[0] and d[0] == neighbors[1]
            ):
                return t


def move(sp, d):
    (ei, ej) = (sp[0] + d[0]), (sp[1] + d[1])
    et = tiles[ei][ej]
    a, b = dir[et]
    (ai, aj) = (ei + a[0]), (ej + a[1])
    if (ai, aj) != sp:
        return (ei, ej), a
    (bi, bj) = (ei + b[0]), (ej + b[1])
    if (bi, bj) != sp:
        return (ei, ej), b


def walk(sp, st):
    x, a = move(sp, dir[st][0])
    y, b = move(sp, dir[st][1])
    i = 1
    while x != y:
        x, a = move(x, a)
        y, b = move(y, b)
        i += 1
    return i


print("Part 1:", walk(start(), starting_tile(start())))

# Part 2

wall = {
    "7": 0.5,
    "-": 0,
    "F": -0.5,
    "J": -0.5,
    "|": 1,
    "L": 0.5,
}

path = [[8 for _ in range(len(tiles[0]))] for _ in range(len(tiles))]


def mark(p):
    global path
    path[p[0]][p[1]] = wall[tiles[p[0]][p[1]]]


# Prepare a secondary sketch containing only the connected pipes
def walk_p2(sp, st):
    global path
    path[sp[0]][sp[1]] = wall[st]
    x, a = move(sp, dir[st][0])
    mark(x)
    y, b = move(sp, dir[st][1])
    mark(y)
    while x != y:
        x, a = move(x, a)
        mark(x)
        y, b = move(y, b)
        mark(y)


# To count the inside tiles, we use a kind of 'ray-tracing' algorithm.
# We draw an horizontal line: when this line crosses the path of the pipes,
# the in/out state is changed (if we were outside, we are now inside and the
# contrary). There is only a small additional thing to account for: some
# pipes are parallel to the line we draw so we need to only account for a
# state change when we actually cross two half vertical pipes or a full
# vertical pipe (that's what the wall dict is for).
def count():
    c = 0
    for l in path:
        out = True
        part = 0
        for v in l:
            if v == 8:
                if not out:
                    c += 1
            elif v == 1:
                out = not out
            elif abs(v) > 0.1 and abs(v) < 0.9:
                part += v
                if abs(part) == 1:
                    out = not out
                    part = 0
    return c


walk_p2(start(), starting_tile(start()))
print("Part 2:", count())
