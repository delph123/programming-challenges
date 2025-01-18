from libs import *
from day10 import knot_hash

# Parse input

key = read("example")

# Part 1


def grid_row(key, row):
    h = knot_hash(key + "-" + str(row))
    return format(int(h, 16), "0128b")


def create_grid(key):
    return Grid([grid_row(key, r) for r in range(128)])


part_one(create_grid(key).count("1"))

# Part 2


def regions(grid):
    def neighbors(p):
        return [p + d for d in Point.UDLR.values() if grid.get(p + d) == "1"]

    return list(group_adjacent((p for p, v in grid.items() if v == "1"), neighbors))


part_two(len(regions(create_grid(key))))
