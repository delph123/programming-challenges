from libs import *

# Parse input

grid = [list(l) for l in read("example").split("\n")]

# Part 1

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def light_is_on(grid, i, j):
    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[i]):
        return False
    return grid[i][j] == "#"


def next(grid):
    g2 = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            l = sum([1 for a, b in DIRS if light_is_on(grid, i + a, j + b)])
            if grid[i][j] == "#" and (l < 2 or l > 3):
                g2[i][j] = "."
            elif grid[i][j] == "." and l == 3:
                g2[i][j] = "#"
    return g2


def simulate(times):
    return compose(times * [next], grid)


part_one(len([1 for x in flatten(simulate(100)) if x == "#"]))

# Part 2


def next_p2(grid):
    g2 = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i == 0 or i == len(grid) - 1) and (j == 0 or j == len(grid[i]) - 1):
                # keep corner lights on
                continue
            l = sum([1 for a, b in DIRS if light_is_on(grid, i + a, j + b)])
            if grid[i][j] == "#" and (l < 2 or l > 3):
                g2[i][j] = "."
            elif grid[i][j] == "." and l == 3:
                g2[i][j] = "#"
    return g2


def simulate_p2(times):
    g = grid
    g[0][0] = "#"
    g[0][-1] = "#"
    g[-1][0] = "#"
    g[-1][-1] = "#"
    return compose(times * [next_p2], grid)


part_two(len([1 for x in flatten(simulate_p2(100)) if x == "#"]))
