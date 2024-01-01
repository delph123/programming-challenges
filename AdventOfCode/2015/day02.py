# Parse input

dimensions = [
    [int(d) for d in l.split("x")]
    for l in open("AdventOfCode/2015/examples/day02.in").read().strip().split("\n")
]

# Part 1


def wrap(a, b, c):
    ab = a * b
    bc = b * c
    ac = a * c
    return 2 * ab + 2 * bc + 2 * ac + min(ab, bc, ac)


print("Part 1:", sum([wrap(a, b, c) for (a, b, c) in dimensions]))

# Part 2


def ribbon(a, b, c):
    ab = a + b
    bc = b + c
    ac = a + c
    return a * b * c + 2 * min(ab, bc, ac)


print("Part 2:", sum([ribbon(a, b, c) for (a, b, c) in dimensions]))
