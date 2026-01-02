from libs import *

# Parse input

lumber_collection_area = read_grid("example")

OPEN = "."
TREES = "|"
LUMBERYARD = "#"

# Part 1


def count_adjacent(area, p, kind):
    return sum(area.get(p + d) == kind for d in Point.DIRS.values())


def transform(area: Grid):
    next_area = area.copy()
    for p in next_area:
        if area[p] == OPEN and count_adjacent(area, p, TREES) >= 3:
            next_area[p] = TREES
        if area[p] == TREES and count_adjacent(area, p, LUMBERYARD) >= 3:
            next_area[p] = LUMBERYARD
        if area[p] == LUMBERYARD and (
            count_adjacent(area, p, LUMBERYARD) == 0
            or count_adjacent(area, p, TREES) == 0
        ):
            next_area[p] = OPEN
    return next_area


def resource_value(area: Grid):
    # preview(area)
    return area.count(TREES) * area.count(LUMBERYARD)


part_one(resource_value(compose(10 * [transform], lumber_collection_area)))

# Part 2


def resource_value_p2(area, time):
    rv_by_val = defaultdict(list)
    rv_by_turn = []
    for t in range(time):
        rv = resource_value(area)
        rv_by_turn.append(rv)
        rv_by_val[rv].append(t)
        if len(rv_by_val[rv]) >= 2:
            prev = rv_by_val[rv][-2]
            l = t - prev
            if rv_by_turn[prev + 1 :] == rv_by_turn[prev + 1 - l : prev + 1]:
                return rv_by_turn[prev + (time - t) % l]
        area = transform(area)


part_two(resource_value_p2(lumber_collection_area, 1000000000))
