from copy import deepcopy

# Parse file

bricks = [
    (
        [int(n) for n in b.split("~")[0].split(",")],
        [int(n) for n in b.split("~")[1].split(",")],
    )
    for b in open("AdventOfCode/2023/examples/day22.in").read().strip().split("\n")
]

bricks = [
    [(a, b, c), (d, e, f), 0 if a != d else (1 if b != e else 2)]
    for [(a, b, c), (d, e, f)] in bricks
]


# Part 1


def min_max():
    mm = [[(min(a[i], b[i]), max(a[i], b[i])) for i in range(3)] for a, b, _ in bricks]
    return [(min([a[i][0] for a in mm]), max([a[i][1] for a in mm])) for i in range(3)]


def space():
    [(xl, xh), (yl, yh), (zl, zh)] = min_max()
    return [[[-1 for x in range(xh + 1)] for y in range(yh + 1)] for z in range(zh + 1)]


def write(brick, num, sp, hi, zd):
    [(a, b, c), (d, e, f), g] = brick
    c -= zd
    f -= zd
    if g == 0:
        for x in range(a, d + 1):
            sp[c][b][x] = num
    if g == 1:
        for y in range(b, e + 1):
            sp[c][y][a] = num
    if g == 2:
        for z in range(c, f + 1):
            sp[z][b][a] = num
    if hi is not None:
        hi[min(c, f)].add(num)


def accept(brick, nums, sp, zd):
    [(a, b, c), (d, e, f), g] = brick
    c -= zd
    f -= zd
    if min(c, f) < 1:
        return False
    if g == 0:
        return all(sp[c][b][x] in nums for x in range(a, d + 1))
    if g == 1:
        return all(sp[c][y][a] in nums for y in range(b, e + 1))
    if g == 2:
        return all(sp[z][b][a] in nums for z in range(c, f + 1))


def fall():
    sp = space()
    hi = [set() for z in range(len(sp))]
    zd = [0 for _ in bricks]
    for b, brick in enumerate(bricks):
        write(brick, b, sp, hi, 0)

    for z in range(len(hi)):
        for b in list(hi[z]):
            brick = bricks[b]
            i = 1
            while accept(brick, [-1, b], sp, i):
                i = i + 1
            if i > 1:
                hi[z].remove(b)
                write(brick, -1, sp, None, 0)
                zd[b] = i - 1
                write(brick, b, sp, hi, zd[b])

    return sp, hi, zd


def disintegrate():
    sp, hi, zd = fall()
    c = []
    for z in range(len(hi)):
        for b in list(hi[z]):
            h = abs(bricks[b][0][2] - bricks[b][1][2]) + 1
            if not any(
                accept(bricks[b1], [-1, b, b1], sp, zd[b1] + 1) for b1 in hi[z + h]
            ):
                c.append(b)
    return c


print("Part 1:", len(disintegrate()))

# Part 2


def fall_p2(sp, hi, zd, be):
    c = 0
    for z in range(len(hi)):
        for b in list(hi[z]):
            if b == be:
                continue
            brick = bricks[b]
            i = 1
            while accept(brick, [-1, b], sp, i + zd[b]):
                i = i + 1
            if i > 1:
                c += 1
                write(brick, -1, sp, None, zd[b])
                write(brick, b, sp, None, zd[b] + i - 1)
    return c


def disintegrate_p2():
    sp, hi, zd = fall()
    c = []
    for b in range(len(bricks)):
        sp0 = deepcopy(sp)
        write(bricks[b], -1, sp0, None, zd[b])
        c.append(fall_p2(sp0, hi, zd, b))
    return c


print("Part 2:", sum(disintegrate_p2()))
