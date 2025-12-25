from libs import *

# Parse input

claims = [r.split() for r in read_lines("example")]
claims = [
    (
        int(i[1:]),
        Point(*(int(n) for n in r[:-1].split(","))),
        Point(*(int(n) for n in s.split("x"))),
    )
    for i, _, r, s in claims
]

p_max = Point(
    max((r + s).x for _, r, s in claims), max((r + s).y for _, r, s in claims)
)

# Part 1


def overlapping(claims):
    g = Grid.of_size(p_max.x + 1, p_max.y + 1).fill(".")
    for _, r, s in claims:
        for i in range(r.x, r.x + s.x):
            for j in range(r.y, r.y + s.y):
                if g[Point(i, j)] == ".":
                    g[Point(i, j)] = "#"
                else:
                    g[Point(i, j)] = "O"
    return g.count("O")


part_one(overlapping(claims))

# Part 2


def overlaps(r0, s0, r1, s1):
    overlap_x = r0.x <= r1.x + s1.x - 1 and r1.x <= r0.x + s0.x - 1
    overlap_y = r0.y <= r1.y + s1.y - 1 and r1.y <= r0.y + s0.y - 1
    return overlap_x and overlap_y


def ideal(claims):
    for id, r0, s0 in claims:
        if not any(overlaps(r0, s0, r1, s1) for id1, r1, s1 in claims if id != id1):
            return id


part_two(ideal(claims))
