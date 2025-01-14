from libs import *

# Parse input

value = int(read("example"))

# Part 1


def spiral_size(n):
    return ceil((sqrt(n) - 1) / 2) * 2 + 1


def steps_from_center(n):
    if n == 1:
        return 0
    inner_spiral_size = spiral_size(n) - 2
    radius = (inner_spiral_size + 1) // 2
    r = (n - (inner_spiral_size**2)) % (2 * radius)
    return radius + abs(radius - r)


part_one(steps_from_center(value))


# Part 2


def spiral(center):
    p = center
    yield p
    r = 0
    for d in cycle(
        [Point.UDLR["^"], Point.UDLR["<"], Point.UDLR["v"], Point.UDLR[">"]]
    ):
        if d == Point.UDLR["^"]:
            p += Point.UDLR[">"] + Point.UDLR["v"]
            r += 2
        for _ in range(r):
            p += d
            yield p


def fibonacci_spiral(n):
    size = spiral_size(n)
    center = Point(size // 2, size // 2)
    g = Grid.of_size(size, size).fill(0)
    if n > 0:
        g[center] = 1
        yield g[center]
    for p in islice(spiral(center), 1, n):
        for d in Point.DIRS.values():
            g[p] += g.get(p + d, 0)
        yield g[p]


part_two(next(f for f in fibonacci_spiral(value) if f > value))
