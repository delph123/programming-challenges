from libs import *

# Parse input

rolls_grid = read_grid("example")

# Part 1


def neighboring_rolls(g: Grid, p: Point):
    return sum(1 for d in Point.DIRS.values() if g.get(p + d) == "@")


def mark_accessible(g: Grid, mark):
    g2 = g.copy()
    for p in g:
        if g[p] == "@" and neighboring_rolls(g, p) < 4:
            g2[p] = mark
    return g2


part_one(mark_accessible(rolls_grid, "x").count("x"))

# Part 2


def mark_removable(g: Grid, mark):
    g1, g2 = Grid([]), g
    while g1 != g2:
        g1, g2 = g2, mark_accessible(g2, mark)
    return g2


part_two(mark_removable(rolls_grid, "+").count("+"))
