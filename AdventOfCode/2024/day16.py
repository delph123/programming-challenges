from libs import *

# Parse input

reindeer_maze = read_grid("example")

start = (reindeer_maze.index("S"), Point.UDLR[">"])
end = reindeer_maze.index("E")

# Part 1


class ReindeerMazeAStar(AStar):
    def __init__(self, maze) -> None:
        super().__init__()
        self.maze = maze

    def neighbors(self, node):
        n0, d0 = node
        return [
            (n0 + d, d)
            for d in Point.UDLR.values()
            if self.maze[n0 + d] in ".E" and d != -d0
        ]

    def cost_between(self, node1, node2):
        if node1[1] == node2[1]:
            turn = 0
        elif node1[1] == -node2[1]:
            turn = 2
        else:
            turn = 1
        return node1[0].manhattan(node2[0]) + turn * 1000

    def heuristic_cost_estimate(self, current, cost, goal):
        dist = goal - current[0]
        p = dist.dot(current[1])
        if p * current[1] == dist:
            turn = 0
        elif p >= 0:
            turn = 1
        else:
            turn = 2
        return cost + dist.manhattan() + turn * 1000

    def is_goal_reached(self, current, goal):
        return current[0] == goal


best_path = ReindeerMazeAStar(reindeer_maze).solve(start, end)

part_one(best_path.cost())

# Part 2


def tiles(maze_solution):
    tiles = set()
    nodes = [maze_solution.goal]
    while nodes:
        predecessors = []
        for node in nodes:
            tiles.add(node.node[0])
            predecessors.extend(node.predecessors)
        nodes = predecessors
    return tiles


part_two(len(tiles(best_path)))
