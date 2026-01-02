from libs import *

# Parse input

matcher = create_matcher([("{str}={int}, {str}={int}..{int}", [(0, 1), (2, 3, 4)])])

clay_veins = [matcher(l) for l in read_lines("example")]

SAND = "."
DRY = "|"
WET = "~"
CLAY = "#"

DOWN = Point.UDLR["v"]
LEFT, RIGHT = Point.UDLR["<"], Point.UDLR[">"]
UP = Point.UDLR["^"]

# Part 1 & 2


@dataclass
class Water:
    fronts: list[list[Point]]
    parent: Water


def clip(segments):
    x_y_segments = [sorted(segment) for segment in segments]
    x_min = min([x[1] for x, _ in x_y_segments]) - 1
    y_min = min([y[1] for _, y in x_y_segments])
    x_max = max([x[-1] for x, _ in x_y_segments]) + 1
    y_max = max([y[-1] for _, y in x_y_segments])
    return (Point(x_min, y_min), Point(x_max - x_min + 1, y_max - y_min + 1))


def ground_map(origin, size, segments):
    ground = Grid.of_size(size.x, size.y).fill(SAND)
    for (x, a), (y, b, c) in segments:
        for i in range(b, c + 1):
            ground[Point(a if x == "x" else i, i if y == "y" else a) - origin] = "#"
    return ground


def flow(source, segments):
    origin, size = clip(segments)
    ground = ground_map(origin, size, segments)
    inner_source = Point(source.x - origin.x, 0)

    ground[inner_source] = "+" if origin.y == source.y else DRY
    water = Water([[inner_source]], None)
    while water:
        if len(water.fronts) == 0:
            water = water.parent
            continue

        current = water.fronts[0]
        if current[0].y + 1 == size.y:
            water.fronts.pop(0)
            continue

        # Explore down
        d = {w + DOWN for w in current if ground.get(w + DOWN) in [SAND, DRY]}
        if d:
            if all(ground[w] == DRY for w in d):
                water.fronts.pop(0)
                continue
            water = Water([[w] for w in d if ground[w] == SAND], water)
            for w in d:
                ground[w] = DRY
            continue

        # Explore left
        w = current[0]
        while (
            w + LEFT in ground
            and ground[w + LEFT] in [SAND, DRY]
            and ground[w + DOWN] in [CLAY, WET]
        ):
            w += LEFT
            current.insert(0, w)
            ground[w] = DRY

        # Explore right
        w = current[-1]
        while (
            w + RIGHT in ground
            and ground[w + RIGHT] in [SAND, DRY]
            and ground[w + DOWN] in [CLAY, WET]
        ):
            w += RIGHT
            current.append(w)
            ground[w] = DRY

        # Check water is at rest
        if ground.get(current[0] + LEFT, SAND) in [CLAY, WET] and ground.get(
            current[-1] + RIGHT, SAND
        ) in [CLAY, WET]:
            for w in current:
                ground[w] = WET
            water.fronts.pop(0)
            continue
    return ground


ground = flow(Point(500, 0), clay_veins)
part_one(sum(ground.count(k) for k in ["+", WET, DRY]))
part_two(ground.count(WET))
