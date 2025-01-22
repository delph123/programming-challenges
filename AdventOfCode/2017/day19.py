from libs import *

# Parse input

routing_diagram = read_grid("example")

# Part 1


def path(g: Grid):
    s = Point(g.rows()[0].index("|"), 0)
    p = [s]
    d = Point.UDLR["v"]
    while True:
        # Advance to the '+'
        while g.get(s + d, " ") not in "+ ":
            s += d
            p.append(s)
        if g.get(s + d, " ") != " ":
            s += d
            p.append(s)
        else:
            break
        # Turn if possible
        if g.get(s + d.rotate(90), " ") != " ":
            d = d.rotate(90)
        elif g.get(s + d.rotate(-90), " ") != " ":
            d = d.rotate(-90)
        else:
            break
        s += d
        p.append(s)
    return p


part_one(
    [
        routing_diagram[p]
        for p in path(routing_diagram)
        if routing_diagram[p] not in "+|-"
    ],
    sep="",
)

# Part 2

part_two(len(path(routing_diagram)))
