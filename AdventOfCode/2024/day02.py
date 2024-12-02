from libs import *

# Parse input

reports = [[int(d) for d in l.split(" ")] for l in read_lines("example")]

# Part 1


def ordered(r):
    return r == sorted(r) or list(reversed(r)) == sorted(r)


def safe(r):
    return ordered(r) and all(
        abs(a - b) < 4 and abs(a - b) > 0 for (a, b) in zip(r, r[1:])
    )


part_one(sum([int(safe(r)) for r in reports]))

# Part 2


def tolerable(r):
    return any(safe(r[:i] + r[i + 1 :]) for i in range(len(r)))


part_two(sum([int(safe(r) or tolerable(r)) for r in reports]))
