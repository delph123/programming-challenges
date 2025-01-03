from libs import *

# Parse input

tiles = read("example")

grid_rows = 10 if read.from_example else 40

# Part 1


def next_row(row):
    next = []
    row = "." + row + "."
    for i in range(1, len(row) - 1):
        next.append("^" if row[i - 1 : i + 2 : 2] in ["^.", ".^"] else ".")
    return "".join(next)


part_one(
    Grid(
        reduce(lambda a, _: a + [next_row(a[-1])], range(1, grid_rows), [tiles])
    ).count(".")
)

# Part 2


def count_tiles(t, row, size):
    c = 0
    for _ in range(size):
        c += row.count(t)
        row = next_row(row)
    return c


part_two(count_tiles(".", tiles, 400000))
