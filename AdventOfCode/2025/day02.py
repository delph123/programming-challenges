from libs import *

# Parse input

product_ranges = [[int(n) for n in r.split("-")] for r in read("example").split(",")]

# Part 1


def invalid_ids(start, end):
    ids = []
    for i in range(start, end + 1):
        l = str(i)
        if len(l) % 2 == 0:
            if l[: len(l) // 2] == l[len(l) // 2 :]:
                ids.append(int(l))
    return ids


part_one(sum([sum(invalid_ids(s, e)) for s, e in product_ranges]))

# Part 2


def invalid_ids_p2(start, end):
    ids = []
    for i in range(start, end + 1):
        l = str(i)
        for s in range(1, len(l) // 2 + 1):
            if len(l) % s == 0:
                if l == l[:s] * (len(l) // s):
                    ids.append(int(l))
                    break
    return ids


part_two(sum([sum(invalid_ids_p2(s, e)) for s, e in product_ranges]))
