from libs import *

# Parse input

coordinates = [Point(*(int(n) for n in r.split(", "))) for r in read_lines("i")]

p_min = Point(min(c.x for c in coordinates), min(c.y for c in coordinates))
p_max = Point(max(c.x for c in coordinates), max(c.y for c in coordinates))

# Part 1


def safest_area():
    # Outside of this grid, coordinates with smallest distance does not change
    # because of the manhattan distance, all points outside the box, say at a
    # distance of n, are at the same distance of border + n.
    g = Grid.of_size(p_max.x + 1, p_max.y + 1).fill(-1)
    for p in g:
        i_min = None
        d_min = None
        for i, c in enumerate(coordinates):
            if i_min == None:
                i_min = i
                d_min = p.manhattan(c)
            else:
                d = p.manhattan(c)
                if d == d_min:
                    i_min = -1
                elif d < d_min:
                    i_min = i
                    d_min = d
        g[p] = i_min
    # All coordinates in the border are considered to be part of
    # an infinite area
    borders = (
        set(g.content[0])
        | set(g.content[-1])
        | set(g.transpose().content[0])
        | set(g.transpose().content[-1])
    )
    areas = [0] * len(coordinates)
    for v in g.values():
        if v >= 0 and v not in borders:
            areas[v] += 1
    return max(areas)


part_one(safest_area())

# Part 2


def closest_area(max_distance):
    # We could compute the area more efficiently but the coordinates are far enough
    # that all points outside this region are well above the max distance already.
    g = Grid.of_size(p_max.x + 10, p_max.y + 10).fill(-1)
    for p in g:
        g[p] = sum(p.manhattan(c) for c in coordinates)
    return sum(v < max_distance for v in g.values())


part_two(closest_area(32 if read.from_example else 10000))
