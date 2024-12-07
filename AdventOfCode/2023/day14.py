from libs import *

# Parse file

rocks = [list(m) for m in read_lines("example")]

# Part 1


def template(map):
    return [
        ["#" if map[i][j] == "#" else "." for j in range(len(map[i]))]
        for i in range(len(map))
    ]


def segments(map):
    segs = []

    for i in range(len(map)):
        s = None
        a = []
        for j in range(len(map[i])):
            if map[i][j] == "#":
                if s is not None:
                    a.append((s, j))
                    s = None
            else:
                if s is None:
                    s = j
        if s is not None:
            a.append((s, len(map[i])))
        segs.append(a)

    return segs


rows = segments(rocks)
cols = segments(transpose(rocks))

map_template = template(rocks)
rmap_template = template(transpose(rocks))


def tilt(map, rot, beg):
    rmap = transpose(map) if rot else map
    template = rmap_template if rot else map_template
    t = [template[i][:] for i in range(len(template))]
    segs = cols if rot else rows
    for i, rsegs in enumerate(segs):
        for a, b in rsegs:
            c = sum(1 if x == "O" else 0 for x in rmap[i][a:b])
            if beg:
                t[i][a : a + c] = "O" * c
            else:
                t[i][b - c : b] = "O" * c

    return transpose(t) if rot else t


def load(map):
    l = 0
    for i, row in enumerate(map):
        l += (len(map) - i) * sum(1 if x == "O" else 0 for x in row)
    return l


part_one(load(tilt(rocks, True, True)))

# Part 2


def cycle(map, n, cache):
    m = map
    for i in range(n):
        k = "".join(["".join(row) for row in m])
        if k in cache:
            lp = i - cache[k]
            r = (n - cache[k]) % lp
            return cycle(map, r + cache[k], dict())
        else:
            cache[k] = i
        m = tilt(m, True, True)
        m = tilt(m, False, True)
        m = tilt(m, True, False)
        m = tilt(m, False, False)
    return m


part_two(load(cycle(rocks, 1000000000, dict())))
