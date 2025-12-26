from libs import *

# Parse input

points_of_light = read_lines("example", ignore=["position=<", "velocity=<", ">", ","])
points_of_light = [[int(n) for n in l.split()] for l in points_of_light]
points_of_light = [(Point(a, b), Point(c, d)) for a, b, c, d in points_of_light]

# Part 1


def move(points, times):
    return [p + times * v for p, v in points]


def clip(points):
    p_min = Point(min(p.x for p in points), min(p.y for p in points))
    p_max = Point(max(p.x for p in points), max(p.y for p in points))
    return (p_min, p_max, (p_max - p_min).x * (p_max - p_min).y)


def smallest_clip(points):
    _, _, current_size = clip(move(points, 0))
    for t in range(100000):
        _, _, size = clip(move(points, t))
        if size > current_size:
            return t - 1
        current_size = size


def draw(points):
    p_min, p_max, _ = clip(points)
    g = Grid.of_size(p_max.x - p_min.x + 1, p_max.y - p_min.y + 1).fill(" ")
    for c in points:
        g[c - p_min] = "#"
    return g


part_one(draw(move(points_of_light, smallest_clip(points_of_light))))

# Part 2

part_two(smallest_clip(points_of_light))
