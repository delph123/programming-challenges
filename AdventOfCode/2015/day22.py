from libs import *
from itertools import product

# Parse input

boss = {l.split(": ")[0]: int(l.split(": ")[1]) for l in read("example").split("\n")}


# Part 1


def wins(config):
    (m, d, s, p, r) = config
    turns = m + d + s + p + r
    return (
        50 - (turns - 1) * boss["Damage"] + 21 * s + 2 * d > 0
        and boss["Hit Points"] - 4 * m - 2 * d - 3 * min(6 * p, 2 * turns) <= 0
        and 53 * m + 73 * d + 113 * s + 173 * p + 229 * r - 5 * r * 101 <= 500
    )


def mana(config):
    (m, d, s, p, r) = config
    return 53 * m + 73 * d + 113 * s + 173 * p + 229 * r


# Given how small the inputs are, choosing between 0 and 10 spells should be enough
part_one(min([mana(config) for config in product(range(11), repeat=5) if wins(config)]))

# Part 2


def wins_p2(config):
    (m, d, s, p, r) = config
    turns = m + d + s + p + r
    return (
        50 - (turns - 1) * boss["Damage"] - turns + 21 * s + 2 * d > 0
        and boss["Hit Points"] - 4 * m - 2 * d - 3 * min(6 * p, 2 * turns) <= 0
        and 53 * m + 73 * d + 113 * s + 173 * p + 229 * r - 5 * r * 101 <= 500
    )


part_two(
    min([mana(config) for config in product(range(11), repeat=5) if wins_p2(config)])
)
