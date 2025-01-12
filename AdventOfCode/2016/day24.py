from libs import *

# Parse input

hvac_map = read_grid("example")

# Part 1


class HvacAStar(AStar):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.poi = self._poi()
        self.costs = self._cost_shortest_paths(product(self.poi, repeat=2))

    def neighbors(self, node):
        for d in Point.UDLR.values():
            if self.grid[node + d] != "#":
                yield node + d

    def heuristic_cost_estimate(self, current, cost, goal):
        return cost + current.manhattan(goal)

    def _poi(self):
        points = []
        i = 0
        p = self.grid.index(str(i))
        while p:
            points.append(p)
            i += 1
            p = self.grid.index(str(i))
        return points

    def _cost_shortest_paths(self, routes):
        return {(p0, p1): self.solve(p0, p1).cost() for p0, p1 in routes}

    def min_steps_to_visit_all_poi(self, returning=False):
        min_steps = float("inf")
        for path in permutations(self.poi[1:], len(self.poi) - 1):
            steps = 0
            p0 = self.poi[0]
            for p in path:
                steps += self.costs[(p0, p)]
                p0 = p
            if returning:
                steps += self.costs[(p0, self.poi[0])]
            min_steps = min(min_steps, steps)
        return min_steps


hvac_shortest_path = HvacAStar(hvac_map)

part_one(hvac_shortest_path.min_steps_to_visit_all_poi())

# Part 2

part_two(hvac_shortest_path.min_steps_to_visit_all_poi(returning=True))
