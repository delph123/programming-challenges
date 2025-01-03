from libs import *
import time

# Parse input

robots = [r.split("p=")[1].split(" v=") for r in read_lines("example")]
robots = [
    (
        Point(int(a.split(",")[0]), int(a.split(",")[1])),
        Point(int(b.split(",")[0]), int(b.split(",")[1])),
    )
    for (a, b) in robots
]

space = Point(11, 7) if read.from_example else Point(101, 103)

# Part 1


def move(p, v, times=1):
    r = p + times * v + times * space
    return Point(r.x % space.x, r.y % space.y)


def area(p: Point):
    a = 0
    if p.x < (space.x - 1) / 2:
        a += 1
    elif p.x > (space.x - 1) / 2:
        a += 2
    else:
        return 0
    if p.y < (space.y - 1) / 2:
        a += 1
    elif p.y > (space.y - 1) / 2:
        a += 3
    else:
        return 0
    return a - 1


def safety_factor(points):
    c = Counter(points)
    return c.get(1, 0) * c.get(2, 0) * c.get(3, 0) * c.get(4, 0)


part_one(safety_factor([area(move(p, v, 100)) for p, v in robots]))

# Part 2


def next(robots):
    return [(move(p, v), v) for (p, v) in robots]


def draw(robots):
    g = Grid([[" " for _ in range(space.x)] for _ in range(space.y)])
    for p, _ in robots:
        g[p] = "X"
    preview(g.content)


def count(robots):
    rows = [0] * space.y
    for p, _ in robots:
        rows[p.y] += 1
    return len(Counter(rows))


def shape(robots):
    rows = [[1000, -1] for _ in range(space.y)]
    for p, _ in robots:
        rows[p.y][0] = min(rows[p.y][0], p.x)
        rows[p.y][1] = max(rows[p.y][1], p.x)
    (x0, y0) = (None, None)
    (xi, yi) = (0, 0)
    for x, y in filter(lambda x: x[1] >= 0, rows):
        if x0 == None:
            (x0, y0) = (x, y)
            continue
        if x > x0:
            xi += 1
        if y < y0:
            yi += 1
        (x0, y0) = (x, y)
    return (xi, yi)


def biggest_group(robots):
    positions = {p: False for (p, _) in robots}
    max_size = 0
    for p, _ in robots:
        if positions[p]:
            continue
        explore = {p}
        size = 0
        while explore:
            p2 = explore.pop()
            if positions[p2]:
                continue
            positions[p2] = True
            size += 1
            for d in Point.DIRS.values():
                if positions.get(p2 + d) == False:
                    explore.add(p2 + d)
        max_size = max(max_size, size)
    return max_size


def time_to_display_easter(robots):
    # We'll assume that when the robots are arranged into a picture of a Christmas
    # tree, the robots that are part of the tree form a group of size more than 50
    # We use 8 for the example since the example never really arrange in a tree.
    EASTER_GROUP_SIZE = 8 if read.from_example else 50

    for i in range(100000):
        b = biggest_group(robots)
        if b > EASTER_GROUP_SIZE:
            # draw(robots)
            # print("Found group with size:", b)
            return i
        robots = next(robots)


part_two(time_to_display_easter(robots))
