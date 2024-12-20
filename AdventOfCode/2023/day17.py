from libs import *

# Parse file

heat_map = read_grid("example", int)

lava_pool = (heat_map.index_at(0), Point.ZERO)
machine_parts = (heat_map.index_at(-1), Point.ZERO)

# Part 1


class HeatMazeAStar(AStar):
    def __init__(self, maze) -> None:
        super().__init__()
        self.maze = maze

    def walk(self, n: Point, d: Point, to: Point):
        s = d.manhattan() if d != Point.ZERO else 1
        # No half turn
        if to == -d // s:
            return None
        # No more than 3 steps in straight line
        if to == d // s and s >= 3:
            return None
        n2 = n + to
        # Not out-of-bounds
        if n2 not in self.maze:
            return None
        # If same direction, count steps
        if to == d // s:
            return (n2, d + to)
        else:
            return (n2, to)

    def neighbors(self, node):
        n, d = node
        ns = [self.walk(n, d, to) for to in Point.UDLR.values()]
        return [m for m in ns if m is not None]

    def cost_between(self, node1, node2):
        return self.maze[node2[0]]

    def heuristic_cost_estimate(self, current, cost, goal):
        return cost + goal[0].manhattan(current[0])

    def is_goal_reached(self, current, goal):
        return current[0] == goal[0]


def heat(maze, path):
    h = [maze[p] for p, _ in path]
    return h[1:]


part_one(
    sum(heat(heat_map, HeatMazeAStar(heat_map).solve(lava_pool, machine_parts).path()))
)

# Part 2


class HeatMazeAStarP2(HeatMazeAStar):
    def walk(self, n, d, to):
        s = d.manhattan() if d != Point.ZERO else 1
        # No half turn
        if to == -d // s:
            return None
        # No more than 10 steps in straight line
        if to == d // s and s >= 10:
            return None
        # At least 4 steps before next turn
        if d != Point.ZERO and to != d // s and s < 4:
            return None
        n2 = n + to
        # Not out-of-bounds
        if n2 not in self.maze:
            return None
        # If same direction, count steps
        if to == d // s:
            return (n2, d + to)
        else:
            return (n2, to)

    def is_goal_reached(self, current, goal):
        # Goal can be reach after 4 straight steps minimum
        return current[0] == goal[0] and current[1].manhattan() >= 4


part_two(
    sum(
        heat(heat_map, HeatMazeAStarP2(heat_map).solve(lava_pool, machine_parts).path())
    ),
)
