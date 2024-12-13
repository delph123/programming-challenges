from libs import *

# Parse input

machine_specs = [m.split("\n") for m in read("example").split("\n\n")]
machine_specs = [
    (
        tuple(int(d) for d in a.split("Button A: X+")[1].split(", Y+")),
        tuple(int(d) for d in b.split("Button B: X+")[1].split(", Y+")),
        tuple(int(d) for d in p.split("Prize: X=")[1].split(", Y=")),
    )
    for (a, b, p) in machine_specs
]


# Part 1


def price_to_win(machine, offset=0):
    ((ax, ay), (bx, by), (px, py)) = machine
    px += offset
    py += offset
    # a * ax + b * bx = px => a = (px - b * bx) / ax
    # a * ay + b * by = py => ay * px - b * ay * bx + b * ax * by = py * ax
    b = int((py * ax - ay * px) / (ax * by - ay * bx))
    a = int((px - b * bx) / ax)
    if a * ax + b * bx == px and a * ay + b * by == py:
        return 3 * a + b
    else:
        return 0


part_one(sum([price_to_win(m) for m in machine_specs]))

# Part 2

part_two(sum([price_to_win(m, 10000000000000) for m in machine_specs]))
