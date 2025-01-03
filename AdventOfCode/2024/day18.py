from libs import *

# Parse input

coordinates = [
    Point(int(l.split(",")[0]), int(l.split(",")[1])) for l in read_lines("example")
]

memory_space_size = 7 if read.from_example else 71
corrupted_memory_size = 12 if read.from_example else 1024

# Part 1

start = Point(0, 0)
end = Point(memory_space_size - 1, memory_space_size - 1)


class MemoryAStar(AStar):
    def __init__(self, corrupted_memory_size) -> None:
        super().__init__()
        self.corrupted_memory = set(coordinates[:corrupted_memory_size])

    def neighbors(self, node: Point):
        return (
            node + d
            for d in Point.UDLR.values()
            if (node + d).is_within_bounds(memory_space_size, memory_space_size)
            and (node + d) not in self.corrupted_memory
        )

    def cost_between(self, node1, node2):
        return 1

    def heuristic_cost_estimate(self, current, cost, goal):
        return cost + current.manhattan(goal)


part_one(MemoryAStar(corrupted_memory_size).solve(start, end).cost())

# Part 2


# Bisect coordinates set to find first coordinates that prevents reaching end
def bad_coordinates(min, max):
    def blocked(x):
        return MemoryAStar(x).solve(start, end) is None

    return bisect(range(min, max), True, key=blocked, smallest=True) + min - 1


c = bad_coordinates(12 if read.from_example else 1024, len(coordinates))
part_two(str(coordinates[c].x) + "," + str(coordinates[c].y))
