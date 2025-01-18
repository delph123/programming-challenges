from libs import *

# Parse input

garden = read_grid("example")

# Part 1


def regions(grid: Grid):
    def neighbors(p):
        return [p + d for d in Point.UDLR.values() if grid.get(p + d) == grid[p]]

    return group_adjacent(grid, neighbors)


def perimeter(region):
    c = 0
    for p in region:
        c += sum(1 for d in Point.UDLR.values() if p + d not in region)
    return c


part_one(sum([len(r) * perimeter(r) for r in regions(garden)]))

# Part 2

u = Point.UDLR["^"]
d = Point.UDLR["v"]
l = Point.UDLR["<"]
r = Point.UDLR[">"]


def sides(region):
    c = 0
    for p in region:
        if (p + u) not in region and ((p + l) not in region or (p + l + u) in region):
            c += 1
        if (p + r) not in region and ((p + u) not in region or (p + u + r) in region):
            c += 1
        if (p + d) not in region and ((p + l) not in region or (p + l + d) in region):
            c += 1
        if (p + l) not in region and ((p + u) not in region or (p + u + l) in region):
            c += 1
    return c


part_two(sum([len(r) * sides(r) for r in regions(garden)]))
