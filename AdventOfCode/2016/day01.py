from libs import *

# Parse input

instructions = [(d[0], int(d[1:])) for d in read("example").split(", ")]

# Part 1


def walk(start: Point, direction: Point):
    for turn, dist in instructions:
        direction = direction.rotate(90 if turn == "R" else -90)
        start += dist * direction
    return start.manhattan()


part_one(walk(Point.ZERO, Point.UDLR["^"]))

# Part 2


def walk_p2(start: Point, direction: Point):
    visited = set()
    for turn, dist in instructions:
        direction = direction.rotate(90 if turn == "R" else -90)
        for _ in range(dist):
            start += direction
            if start in visited:
                return start.manhattan()
            visited.add(start)


part_two(walk_p2(Point.ZERO, Point.UDLR["^"]))
