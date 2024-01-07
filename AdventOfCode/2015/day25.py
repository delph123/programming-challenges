from libs import *

# Parse input

row, column = (
    int(n) for n in re.match(".* row (\d*), column (\d*)\.", read("example")).groups()
)

# Part 1


def code_number(row, column):
    n = row + column - 1
    return (n - 1) * n // 2 + column


def next_code(cd):
    return (252533 * cd) % 33554393


def code(row, column):
    n = code_number(row, column)
    return compose((n - 1) * [next_code], 20151125)


part_one(code(row, column))
