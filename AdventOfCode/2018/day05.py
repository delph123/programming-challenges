from libs import *
import sys

# Parse input

polymer = read("example")

# Part 1


def react(polymer: str):
    # For efficiently processing the polymer we only need an array to collect the units
    # which did not react (or not yet at least), the "reaction", and a pointer to where
    # we are in the polymer string. This is inspired from the zipper data structure.
    reaction = []
    index = 0
    while index < len(polymer):
        if len(reaction) == 0:
            reaction.append(polymer[index])
            index += 1
        else:
            a = reaction[-1]
            b = polymer[index]
            if a != b and a.upper() == b.upper():
                reaction.pop()
            else:
                reaction.append(polymer[index])
            index += 1
    return reaction


part_one(len(react(polymer)))

# Part 2


def improve(polymer: str):
    units = set([u.lower() for u in polymer])
    return min(len(react(replace_all([u, u.upper()], "", polymer))) for u in units)


part_two(improve(polymer))
