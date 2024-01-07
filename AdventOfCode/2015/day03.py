from libs import *

# Parse input

moves = read("example")


# Part 1

DIRS = {">": 1, "<": -1, "^": -1j, "v": 1j}


def walk(moves):
    s = 0
    visited = {0}
    for m in moves:
        s += DIRS[m]
        visited.add(s)
    return visited


part_one(len(walk(moves)))

# Part 2

part_two(len(walk(moves[::2]) | walk(moves[1::2])))
