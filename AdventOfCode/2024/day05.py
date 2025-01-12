from libs import *

# Parse input

ordering, production = read("example").split("\n\n")

ordering = [(int(l.split("|")[0]), int(l.split("|")[1])) for l in ordering.split("\n")]
production = [[int(p) for p in l.split(",")] for l in production.split("\n")]


# Part 1


def right_order(update):
    for n, page in enumerate(update):
        if any(b in update[:n] for (a, b) in ordering if a == page):
            return False
    return True


part_one(sum([p[int(len(p) / 2)] for p in production if right_order(p)]))

# Part 2


def cmp_pages(a, b):
    if (a, b) in ordering:
        return -1
    if (b, a) in ordering:
        return 1
    return 0


def reorder(update):
    return sorted(update, key=cmp_to_key(cmp_pages))


part_two(sum([reorder(p)[int(len(p) / 2)] for p in production if not right_order(p)]))
