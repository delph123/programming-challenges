from libs import *

# Parse input

fresh_ingredient_ranges, ingredients = read("example").split("\n\n")

fresh_ingredient_ranges = [
    tuple(int(n) for n in r.split("-")) for r in fresh_ingredient_ranges.splitlines()
]
ingredients = [int(n) for n in ingredients.splitlines()]

# Part 1


def is_fresh(i):
    for s, e in fresh_ingredient_ranges:
        if s <= i <= e:
            return True
    return False


part_one(sum([is_fresh(i) for i in ingredients]))

# Part 2


def intersects(ranges, r):
    (a, b) = r
    return [(s, e) for s, e in ranges if a <= e and b >= s]


def canonical_ranges(ranges):
    cr = set()
    for s, e in ranges:
        intersections = intersects(cr, (s, e))
        for i in intersections:
            cr.remove(i)
        intersections.append((s, e))
        cr.add((min(l for (l, _) in intersections), max(h for (_, h) in intersections)))
    return cr


part_two(sum(h - l + 1 for (l, h) in canonical_ranges(fresh_ingredient_ranges)))
