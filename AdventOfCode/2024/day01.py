from libs import *

# Parse input

two_lists = [tuple(int(n) for n in l.split("   ")) for l in read_lines("example")]
l1, l2 = tuple(zip(*two_lists))

# Part 1


def distance(l, r):
    return [abs(a - b) for (a, b) in zip(sorted(l), sorted(r))]


part_one(sum(distance(l1, l2)))

# Part 2


def similarity(l, r):
    count = Counter(r)
    return [a * count[a] for a in l]


part_two(sum(similarity(l1, l2)))
