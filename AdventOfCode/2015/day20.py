from libs import *
from itertools import dropwhile, count

# Parse input

minimum_presents = int(read("example"))

# Part 1


def house_presents(n):
    return 10 * sum(divisors(n))


part_one(next(dropwhile(lambda n: house_presents(n) < minimum_presents, count())))

# Part 2


def house_presents_p2(n):
    return 11 * sum([m for m in divisors(n) if n <= 50 * m])


part_two(next(dropwhile(lambda n: house_presents_p2(n) < minimum_presents, count())))
