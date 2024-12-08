from libs import *

# Parse input

city_map = read_lines("example")

# Part 1


def antenna_locations():
    locations = {}
    for j, r in enumerate(city_map):
        for i, c in enumerate(r):
            if c != ".":
                locations.setdefault(c, []).append(Point(i, j))
    return locations


def antinodes(locations: list[Point]):
    nodes = set()
    for i, l1 in enumerate(locations):
        for l2 in locations[i + 1 :]:
            if (l1 + l1 - l2).is_within(city_map):
                nodes.add(l1 + l1 - l2)
            if (l2 + l2 - l1).is_within(city_map):
                nodes.add(l2 + l2 - l1)
    return nodes


part_one(
    len(
        flatten(
            (antinodes(l) for (_, l) in antenna_locations().items()),
            collect=set,
        )
    )
)

# Part 2


def antinodes_v2(locations: list[Point]):
    nodes = set(locations)
    for i, l1 in enumerate(locations):
        for l2 in locations[i + 1 :]:
            a = l1 - l2
            while (l1 + a).is_within(city_map):
                nodes.add(l1 + a)
                a += l1 - l2
            a = l1 - l2
            while (l2 - a).is_within(city_map):
                nodes.add(l2 - a)
                a += l1 - l2
    return nodes


part_one(
    len(
        flatten(
            (antinodes_v2(l) for (_, l) in antenna_locations().items()),
            collect=set,
        )
    )
)
