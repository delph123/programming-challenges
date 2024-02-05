from libs import *
from itertools import batched

# Parse input

triangles = [[int(n) for n in l.split()] for l in read_lines("example")]


# Part 1


def is_valid(a, b, c):
    return a + b > c


def valid_triangles(triangles):
    return len([l for l in triangles if is_valid(*sorted(l))])


part_one(valid_triangles(triangles))


# Part 2


def pick(triangle, col):
    return [row[col] for row in triangle]


part_two(
    valid_triangles(batched(pick(triangles, 0), n=3))
    + valid_triangles(batched(pick(triangles, 1), n=3))
    + valid_triangles(batched(pick(triangles, 2), n=3))
)
