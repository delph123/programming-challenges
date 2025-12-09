from libs import *

# Parse input

red_tiles = [tuple(int(n) for n in l.split(",")) for l in read_lines("i")]

# Part 1


def largest_rectangle(corners):
    return max(
        (x - u + 1) * (y - v + 1)
        for i, (x, y) in enumerate(corners)
        for (u, v) in corners[i + 1 :]
    )


part_one(largest_rectangle(red_tiles))

# Part 2


part_two(0)
