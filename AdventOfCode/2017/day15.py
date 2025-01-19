from libs import *

# Parse input

matcher = create_matcher([("Generator {str} starts with {int}", (0, 1))])

generators_seed = [matcher(r) for r in read_lines("example")]
generators_seed = {g: s for g, s in generators_seed}

factors = {"A": 16807, "B": 48271}
remainders = {"A": 4, "B": 8}

judge_remainder = 2**16

# Part 1


def generator(name):
    a = generators_seed[name]
    f = factors[name]
    while True:
        a = (a * f) % 2147483647
        yield a


def matching_judge(gen, number_of_pairs):
    return sum(
        1
        for a, b in islice(zip(gen("A"), gen("B")), number_of_pairs)
        if a % judge_remainder == b % judge_remainder
    )


part_one(matching_judge(generator, 40_000_000))

# Part 2


def generator_p2(name):
    a = generators_seed[name]
    f = factors[name]
    r = remainders[name]
    while True:
        a = (a * f) % 2147483647
        if a % r == 0:
            yield a


part_two(matching_judge(generator_p2, 5_000_000))
