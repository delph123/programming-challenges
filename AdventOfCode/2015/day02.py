from libs import *

# Parse input

dimensions = [[int(d) for d in l.split("x")] for l in read("example").split("\n")]

# Part 1


def wrap(a, b, c):
    ab = a * b
    bc = b * c
    ac = a * c
    return 2 * ab + 2 * bc + 2 * ac + min(ab, bc, ac)


part_one(sum([wrap(a, b, c) for (a, b, c) in dimensions]))

# Part 2


def ribbon(a, b, c):
    ab = a + b
    bc = b + c
    ac = a + c
    return a * b * c + 2 * min(ab, bc, ac)


part_two(sum([ribbon(a, b, c) for (a, b, c) in dimensions]))
