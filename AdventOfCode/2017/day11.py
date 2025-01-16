from libs import *

# Parse input

hex_directions = {
    "n": Point(0, 2),
    "ne": Point(1, 1),
    "se": Point(1, -1),
    "s": Point(0, -2),
    "sw": Point(-1, -1),
    "nw": Point(-1, 1),
}

path = read("example").split(",")

# Part 1


def arrival(start, path):
    for d in path:
        start += hex_directions[d]
    return start


def hex_manhattan_distance(a, b):
    dist = b - a
    return abs(dist.x) + max(abs(dist.y) - abs(dist.x), 0) // 2


part_one(hex_manhattan_distance(Point.ZERO, arrival(Point.ZERO, path)))

# Part 2


def furthest_distance(start, path):
    pos = start
    max_dist = 0
    for d in path:
        pos += hex_directions[d]
        max_dist = max(max_dist, hex_manhattan_distance(start, pos))
    return max_dist


part_two(furthest_distance(Point.ZERO, path))
