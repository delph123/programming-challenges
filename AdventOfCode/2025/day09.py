from libs import *

# Parse input

red_tiles = [Point(*(int(n) for n in l.split(","))) for l in read_lines("example")]

# Part 1


def area(c0, c1):
    return (abs(c0.x - c1.x) + 1) * (abs(c0.y - c1.y) + 1)


def largest_rectangle(corners):
    return max(area(c0, c1) for i, c0 in enumerate(corners) for c1 in corners[i + 1 :])


part_one(largest_rectangle(red_tiles))

# Part 2


def distinct(iterable, *, key=None):
    return {key(x) if key else x for x in iterable}


def is_free(p: Point, g: Grid):
    return p.x == 0 or p.y == 0 or p.x == g.index_at(-1).x or p.y == g.index_at(-1).y


def is_tiled(c0: Point, c1: Point, grid: Grid):
    x_min, x_max = min(c0.x, c1.x), max(c0.x, c1.x)
    y_min, y_max = min(c0.y, c1.y), max(c0.y, c1.y)
    # We can check only the perimeter of the rectangle since if there are some non-tiled
    # (= free tiles), they must come from the exterior and therefore cross the perimeter
    for x in [x_min, x_max]:
        for y in range(y_min + 1, y_max):
            if grid[Point(x, y)] == ".":
                return False
    for y in [y_min, y_max]:
        for x in range(x_min + 1, x_max):
            if grid[Point(x, y)] == ".":
                return False
    return True


def largest_red_green_rectangle(nodes):
    # Build a collapsed view of the area
    x_coord = sorted(distinct(nodes, key=attrgetter("x")))
    y_coord = sorted(distinct(nodes, key=attrgetter("y")))
    collapsed = [Point(x_coord.index(p.x), y_coord.index(p.y)) for p in nodes]

    grid = Grid.of_size(len(x_coord), len(y_coord)).fill(".")

    # Corners
    for p in collapsed:
        grid[p] = "+"

    # Boundaries
    for p0, p1 in pairwise(collapsed + collapsed[:1]):
        if p0.x == p1.x:
            for y in range(min(p0.y, p1.y) + 1, max(p0.y, p1.y)):
                grid[Point(p0.x, y)] = "|"
        else:
            for x in range(min(p0.x, p1.x) + 1, max(p0.x, p1.x)):
                grid[Point(x, p0.y)] = "-"

    # Interior
    groups = group_adjacent(
        (p for p in grid if grid[p] == "."),
        lambda p: [p + d for d in Point.DIRS.values() if grid.get(p + d) == "."],
    )

    for g in groups:
        if not any(is_free(p, grid) for p in g):
            for p in g:
                grid[p] = "#"

    rectangles = sorted(
        ((c0, c1) for i, c0 in enumerate(nodes) for c1 in nodes[i + 1 :]),
        reverse=True,
        key=lambda x: area(x[0], x[1]),
    )

    # Check biggest rectangles until we find one which is tiled completely
    for c0, c1 in rectangles:
        cc0 = Point(x_coord.index(c0.x), y_coord.index(c0.y))
        cc1 = Point(x_coord.index(c1.x), y_coord.index(c1.y))
        if is_tiled(cc0, cc1, grid):
            return area(c0, c1)


part_two(largest_red_green_rectangle(red_tiles))
