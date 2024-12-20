from libs import *

# Parse input

file = "example"
coordinates = [
    Point(int(l.split(",")[0]), int(l.split(",")[1])) for l in read_lines(file)
]

# Part 1

size = 71 if file.startswith("i") else 7
start = Point(0, 0)
end = Point(size - 1, size - 1)


class MemoryAStar(AStar):
    def __init__(self, corrupted_memory_size) -> None:
        super().__init__()
        self.corrupted_memory = set(coordinates[:corrupted_memory_size])

    def neighbors(self, node: Point):
        return (
            node + d
            for d in Point.UDLR.values()
            if (node + d).is_within_bounds(size, size)
            and (node + d) not in self.corrupted_memory
        )

    def cost_between(self, node1, node2):
        return 1

    def heuristic_cost_estimate(self, current, cost, goal):
        return cost + current.manhattan(goal)


part_one(MemoryAStar(1024 if file.startswith("i") else 12).solve(start, end).cost())

# Part 2


# Bisect coordinates set to find first coordinates that prevents reaching end
def bad_coordinates(min, max):
    def blocked(x):
        return MemoryAStar(x).solve(start, end) is None

    return bisect(range(min, max), True, key=blocked, smallest=True) + min - 1


c = bad_coordinates(1024 if file.startswith("i") else 12, len(coordinates))
part_two(str(coordinates[c].x) + "," + str(coordinates[c].y))
