from libs import *

# Parse input

depth, target = read_lines("example")
depth = int(depth[7:])
target = Point(*(int(n) for n in target[8:].split(",")))

# Part 1


def cave(depth, target, size):
    g = Grid.of_size(size.x, size.y)
    g[Point.ZERO] = depth % 20183
    for j in range(size.y):
        for i in range(size.x):
            if j == 0:
                geologic_index = i * 16807
            elif i == 0:
                geologic_index = j * 48271
            else:
                geologic_index = g[Point(i - 1, j)] * g[Point(i, j - 1)]
            erosion_level = (geologic_index + depth) % 20183
            g[Point(i, j)] = erosion_level
    for p in g:
        erosion_level = g[p]
        g[p] = erosion_level % 3
    g[target] = 0  # The target is always on rocky ground
    return g


part_one(sum(cave(depth, target, target + Point(1, 1)).values()))

# Part 2

# Each tool's number corresponds to the region's type on which it is NOT allowed!
TOOLS = {"none": 0, "torch": 1, "climbing gear": 2}


class CaveAStar(AStar[tuple[Point, int]]):
    def __init__(self, depth, target):
        super().__init__(visit_closed=False)
        # Prepare a large-enough map
        size = 2 * max(target.x, target.y)
        self.cave = cave(depth, target, Point(size, size))

    def neighbors(self, node):
        p, tool = node
        for d in Point.UDLR.values():
            if self.cave.get(p + d, tool) != tool:
                yield (p + d, tool)
        yield (p, 3 - tool - self.cave[p])

    def cost_between(self, n1, n2):
        return 7 if n1[1] != n2[1] else 1

    def heuristic_cost_estimate(self, current, cost, goal):
        # Use manhattan estimate as lower bound of cost to avoid exploring too many paths
        return cost + current[0].manhattan(goal[0])


start = (Point.ZERO, TOOLS["torch"])
goal = (target, TOOLS["torch"])
part_two(CaveAStar(depth, target).solve(start, goal).cost())
