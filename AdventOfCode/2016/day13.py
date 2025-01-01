from libs import *

# Parse input

favorite_number, coordinates = read_lines("example")
favorite_number = int(favorite_number)
coordinates = Point(*(int(d) for d in coordinates.split(",")))

# Part 1


def is_open(p):
    n = p.x * p.x + 3 * p.x + 2 * p.x * p.y + p.y + p.y * p.y
    n += favorite_number
    return n.bit_count() % 2 == 0


class MazeAStar(AStar):
    def neighbors(self, node):
        for d in Point.UDLR.values():
            if (node + d).x >= 0 and (node + d).y >= 0 and is_open(node + d):
                yield node + d


maze_shortest_path = MazeAStar()
part_one(maze_shortest_path.solve(Point(1, 1), coordinates).cost())

# Part 2


def reachable_locations(starting_points, n):
    if n <= 0:
        return starting_points

    reachable = set(starting_points)
    for p in starting_points:
        for p2 in maze_shortest_path.neighbors(p):
            reachable.add(p2)
    return reachable_locations(reachable, n - 1)


part_two(len(reachable_locations({Point(1, 1)}, 50)))
