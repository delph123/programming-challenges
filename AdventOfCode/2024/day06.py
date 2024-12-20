from libs import *

# Parse input

lab = read_grid("i")

# Part 1


def patrol(grid: Grid):
    p = grid.index("^")
    d = Point(0, -1)
    grid[p] = "X"
    while (p + d) in grid:
        if grid[p + d] == "#":
            # turn 90°
            d = d.rotate(90)
        else:
            p += d
            grid[p] = "X"
    return grid


part_one(patrol(lab.copy()).count("X"))

# Part 2

lab2 = Grid([["#" if c == "#" else 0 for c in row] for row in lab.content])


def is_looping(grid: Grid, p: Point):
    d = Point(0, -1)
    grid[p] += 1
    while (p + d) in grid:
        if grid[p + d] == "#":
            # turn 90°
            d = d.rotate(90)
        else:
            p += d
        if grid[p] == 4:
            return True
        else:
            grid[p] += 1
    return False


def obstructions(grid: Grid):
    p0 = lab.index("^")
    path = patrol(lab.copy())
    path[p0] = "."

    for p, c in path.items():
        if c == "X":
            g = grid.copy()
            g[p] = "#"
            if is_looping(g, p0):
                path[p] = "O"

    return path


part_two(obstructions(lab2).count("O"))
