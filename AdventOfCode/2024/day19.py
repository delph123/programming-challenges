from libs import *

# Parse input

towels, designs = read("example").split("\n\n")
towels = towels.split(", ")
designs = designs.split("\n")

# Part 1


def is_valid(design):
    for towel in towels:
        if towel == design:
            return True
        if design.startswith(towel) and is_valid(design[len(towel) :]):
            return True
    return False


part_one(sum([int(is_valid(design)) for design in designs]))

# Part 2


@cache
def arrangements(design):
    a = 0
    for towel in towels:
        if towel == design:
            a += 1
        elif design.startswith(towel):
            a += arrangements(design[len(towel) :])
    return a


part_two(sum([arrangements(design) for design in designs]))
