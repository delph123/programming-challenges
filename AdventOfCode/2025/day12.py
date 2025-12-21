from libs import *

# Parse input

shapes = read("example").split("\n\n")

regions = [l.split(": ") for l in shapes[-1].splitlines()]
regions = [
    (Point(*(int(i) for i in s.split("x"))), [int(j) for j in n.split()])
    for s, n in regions
]


def rotated_and_flipped(g: Grid):
    rfg = []
    for g1 in [g, g.hflip()]:
        for i in range(0, 4):
            g2 = g1.rotate(i)
            if all(g2.content != g0.content for g0 in rfg):
                rfg.append(g2)
    return rfg


shapes = [(Grid(l.splitlines()[1:]), l.count("#")) for l in shapes[:-1]]
shapes = [(rotated_and_flipped(g), c) for g, c in shapes]

# Part 1


def fit_grid(g: Grid, shapes_req):
    if len(shapes_req) == 0:
        return True

    for j in range(len(g.content) - 2):
        for i in range(len(g.content[j]) - 2):
            for shape in shapes[shapes_req[0]][0]:
                p0 = Point(i, j)
                if all(g[p0 + p] == "." for p in shape if shape[p] == "#"):
                    if len(shapes_req) == 1:
                        return True
                    g2 = g.copy()
                    for p in shape:
                        if shape[p] == "#":
                            g2[p0 + p] = "#"
                    if fit_grid(g2, shapes_req[1:]):
                        return True
    return False


def fit(size, requirements):
    if sum(requirements) <= (size.x // 3) * (size.y // 3):
        return True  # All required shapes fits in their own 3x3 square
    elif size.x * size.y < sum(shapes[i][1] * r for i, r in enumerate(requirements)):
        return False  # the total size of the requirements is above the actual size of the region
    else:
        # Search all possible arrangements of pieces (very slow, especially on ex. 3)
        # Real input will never go there since it's designed to be trivial :)
        shapes_req = flatten([[i] * r for i, r in enumerate(requirements)])
        return fit_grid(Grid.of_size(size.x, size.y).fill("."), shapes_req)


part_one(sum(fit(s, r) for s, r in regions))
