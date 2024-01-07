from libs import *

# Parse input

weights = [int(n) for n in read("example").split("\n")]

# Part 1


def pick(presents, weight, max):
    """
    Pick a combination of presents, totaling up to a given weight
    but only keep combinations of smallest size
    """
    if len(presents) == 0 or max == 0:
        return []
    if len(presents) == 1:
        if presents[0] == weight:
            return [presents]
        else:
            return []

    b1 = []
    if presents[0] < weight:
        b1 = pick(presents[1:], weight - presents[0], max - 1)
        for b in b1:
            b.append(presents[0])

    b2 = pick(presents[1:], weight, len(b1[0]) if b1 else max)
    if b2 and (not b1 or len(b2[0]) < len(b1[0])):
        return b2
    else:
        return b1 + b2


part_one(min([prod(qe) for qe in pick(weights, sum(weights) // 3, len(weights))]))

# Part 2

part_two(min([prod(qe) for qe in pick(weights, sum(weights) // 4, len(weights))]))
