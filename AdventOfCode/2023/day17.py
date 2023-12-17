from astar import AStar

# Parse file

heat_map = [
    [int(n) for n in l]
    for l in open("AdventOfCode/2023/examples/day17.in").read().strip().split("\n")
]

lava_pool = (0, 0)
machine_parts = ((len(heat_map) - 1) + (len(heat_map) - 1) * 1j, 0)

# Part 1


def get(map, coord):
    return map[int(coord.imag)][int(coord.real)]


class HeatMazeAStar(AStar):
    def __init__(self, maze) -> None:
        super().__init__()
        self.maze = maze

    def walk(self, n, d, to):
        s = int(abs(d.real + d.imag)) if d != 0 else 1
        # No half turn
        if to == -d / s:
            return None
        # No more than 3 steps in straight line
        if to == d / s and s >= 3:
            return None
        n2 = n + to
        # Not out-of-bounds
        if n2.real < 0 or n2.real >= len(self.maze[0]):
            return None
        if n2.imag < 0 or n2.imag >= len(self.maze):
            return None
        # If same direction, count steps
        if to == d / s:
            return (n2, d + to)
        else:
            return (n2, to)

    def neighbors(self, node):
        n, d = node
        ns = [
            self.walk(n, d, 1),
            self.walk(n, d, -1),
            self.walk(n, d, 1j),
            self.walk(n, d, -1j),
        ]
        return [m for m in ns if m is not None]

    def distance_between(self, node1, node2):
        return get(self.maze, node2[0])

    def heuristic_cost_estimate(self, current, goal):
        g = goal[0]
        c = current[0]
        return int(abs(g.real - c.real)) + int(abs(g.imag - c.imag))

    def is_goal_reached(self, current, goal):
        return current[0] == goal[0]


def heat(maze, path):
    h = [get(maze, p) for p, _ in path]
    return h[1:]


print(
    "Part 1:",
    sum(heat(heat_map, list(HeatMazeAStar(heat_map).astar(lava_pool, machine_parts)))),
)

# Part 2


class HeatMazeAStarP2(HeatMazeAStar):
    def walk(self, n, d, to):
        s = int(abs(d.real + d.imag)) if d != 0 else 1
        # No half turn
        if to == -d / s:
            return None
        # No more than 10 steps in straight line
        if to == d / s and s >= 10:
            return None
        # At least 4 steps before next turn
        if d != 0 and to != d / s and s < 4:
            return None
        n2 = n + to
        # Not out-of-bounds
        if n2.real < 0 or n2.real >= len(self.maze[0]):
            return None
        if n2.imag < 0 or n2.imag >= len(self.maze):
            return None
        # If same direction, count steps
        if to == d / s:
            return (n2, d + to)
        else:
            return (n2, to)

    def is_goal_reached(self, current, goal):
        # Goal can be reach after 4 straight steps minimum
        n, d = current
        s = int(abs(d.real + d.imag))
        return n == goal[0] and s >= 4


print(
    "Part 2:",
    sum(
        heat(heat_map, list(HeatMazeAStarP2(heat_map).astar(lava_pool, machine_parts)))
    ),
)
