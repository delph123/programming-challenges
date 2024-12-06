from libs import *

# Parse input

lab = [list(r) for r in read_lines("example")]

# Part 1


def guard(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "^":
                return x + y * 1j


def patrol(grid):
    p = guard(grid)
    d = -1j
    grid[int(p.imag)][int(p.real)] = "X"
    while (
        p.real + d.real >= 0
        and p.real + d.real < len(grid[0])
        and p.imag + d.imag >= 0
        and p.imag + d.imag < len(grid)
    ):
        if grid[int(p.imag + d.imag)][int(p.real + d.real)] == "#":
            # turn
            d = -d.imag + d.real * 1j
        else:
            p += d
            grid[int(p.imag)][int(p.real)] = "X"
    return grid


def count(grid, letter):
    return sum(sum(1 for c in row if c == letter) for row in grid)


part_one(count(patrol(deepcopy(lab)), "X"))

# Part 2

lab2 = [["#" if c == "#" else 0 for c in row] for row in lab]


def is_looping(grid, p):
    d = -1j
    grid[int(p.imag)][int(p.real)] += 1
    while (
        p.real + d.real >= 0
        and p.real + d.real < len(grid[0])
        and p.imag + d.imag >= 0
        and p.imag + d.imag < len(grid)
    ):
        if grid[int(p.imag + d.imag)][int(p.real + d.real)] == "#":
            # turn
            d = -d.imag + d.real * 1j
        else:
            p += d
        if grid[int(p.imag)][int(p.real)] == 4:
            return True
        else:
            grid[int(p.imag)][int(p.real)] += 1
    return False


def obstructions(grid):
    p = guard(lab)
    path = patrol(deepcopy(lab))
    path[int(p.imag)][int(p.real)] = "."

    for y, row in enumerate(path):
        for x, c in enumerate(row):
            if c == "X":
                g = deepcopy(grid)
                g[y][x] = "#"
                if is_looping(g, p):
                    path[y][x] = "O"

    return path


part_two(count(obstructions(lab2), "O"))
