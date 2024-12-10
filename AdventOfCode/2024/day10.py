from libs import *

# Parse input

topographic_map = read_grid("example", cell_format=int)

# Part 1


def score(p0):
    points = set([p0])
    for i in range(1, 10):
        next_points = set()
        for p, d in product(points, Point.UDLR.values()):
            if (p + d) in topographic_map and topographic_map[p + d] == i:
                next_points.add(p + d)
        points = next_points
    return len(points)


part_one(sum([score(p) for p in topographic_map.find_all(0)]))

# Part 2


def ratings(p, i):
    return sum(
        ratings(p + d, i + 1) if i < 8 else 1
        for d in Point.UDLR.values()
        if topographic_map.get(p + d) == i + 1
    )


part_one(sum([ratings(p, 0) for p in topographic_map.find_all(0)]))
