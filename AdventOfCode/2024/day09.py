from libs import *

# Parse input

disk_map = [int(d) for d in read("i")]

# Part 1


def memorymap():
    return [
        [[i] * a, [-1] * b]
        for (i, (a, b)) in enumerate(
            zip_longest(disk_map[::2], disk_map[1::2], fillvalue=0)
        )
    ]


def compact(mm: list[list[list[int]]]):
    (x, y) = (0, 0)
    while len(mm) - 1 > x:
        v = mm[-1][0].pop()
        mm[x][1][y] = v
        y += 1
        while y >= len(mm[x][1]):
            x += 1
            y = 0
        while len(mm[-1][0]) == 0:
            mm.pop()
    return mm


def checksum(mm):
    inline_mm = flatten(flatten([[l[0], l[-1]] for l in mm]))
    return sum([i * v if v >= 0 else 0 for i, v in enumerate(inline_mm)])


part_one(checksum(compact(memorymap())))

# Part 2


def memorymap_v2():
    return [
        [[i] * a, [i] * a, [-1] * b]
        for (i, (a, b)) in enumerate(
            zip_longest(disk_map[::2], disk_map[1::2], fillvalue=0)
        )
    ]


def compact_v2(mm: list[list[list[int]]]):
    for l0, f, _ in reversed(mm):
        try:
            (l, _, b) = next(filter(lambda x: len(x[2]) >= len(f), mm[: f[0]]))
            l.extend(f)
            for i in range(len(f)):
                b.pop()
                l0[i] = -1
        except:
            pass
    return mm


part_two(checksum(compact_v2(memorymap_v2())))
