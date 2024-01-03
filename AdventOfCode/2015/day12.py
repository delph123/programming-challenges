import json

# Parse input

books = json.load(open("AdventOfCode/2015/examples/day12.in"))

# Part 1


def parse(books, excl=None):
    if isinstance(books, dict):
        if excl is not None and excl in books.values():
            return 0
        s = 0
        for k, v in books.items():
            s += parse(k, excl) + parse(v, excl)
        return s
    if isinstance(books, list):
        s = 0
        for v in books:
            s += parse(v, excl)
        return s
    if isinstance(books, int):
        return books
    return 0


print("Part 1:", parse(books))

# Part 2

print("Part 2:", parse(books, "red"))
