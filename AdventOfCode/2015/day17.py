from libs import *

# Parse input

containers = [int(n) for n in read("example").split("\n")]

# Part 1


def fill(volume, containers):
    return [c for c in powerset(containers) if sum(c) == volume]


combinations = fill(150 if len(containers) > 5 else 25, containers)

part_one(len(combinations))

# Part 2

comb_lengths = [len(c) for c in combinations]

part_two(comb_lengths.count(min(comb_lengths)))
