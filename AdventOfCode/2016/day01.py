from libs import *

# Parse input

instructions = [(d[0], int(d[1:])) for d in read("example").split(", ")]

DIRS = [-1j, 1, 1j, -1]

# Part 1


def walk(start, direction):
    for turn, dist in instructions:
        direction = (direction + (1 if turn == "R" else 3)) % 4
        start += dist * DIRS[direction]
    return abs(int(start.real)) + abs(int(start.imag))


part_one(walk(0, 0))

# Part 2


def walk_p2(start, direction):
    visited = set()
    for turn, dist in instructions:
        direction = (direction + (1 if turn == "R" else 3)) % 4
        for _ in range(dist):
            start += DIRS[direction]
            if start in visited:
                return abs(int(start.real)) + abs(int(start.imag))
            visited.add(start)


part_two(walk_p2(0, 0))
