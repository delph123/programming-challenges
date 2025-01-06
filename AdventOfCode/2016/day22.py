from libs import *

# Parse input

matcher = create_matcher(
    [
        (
            "/dev/grid/node-x{int}-y{int} +{int}T +{int}T +{int}T +{int}%",
            [(0, 1), 3, 4],
        )
    ]
)

df = [matcher(r) for r in read_lines("example")[2:]]

# Part 1


def viable_pairs(df):
    node_by_available = sorted(a for _, _, a in df)

    def accepts(size):
        b = bisect(
            node_by_available,
            size,
            key=lambda x: min(size, x),
            smallest=True,
        )
        return len(node_by_available) - b if b >= 0 else 0

    return sum(accepts(u) - int(a > u) for _, u, a in df if u > 0)


part_one(viable_pairs(df))

# Part 2


class GridAStar(AStar):
    def __init__(self, df):
        super().__init__()
        empty_pos, empty_space = next((p, a) for p, u, a in df if u == 0)
        width = max(n for (n, _), _, _ in df) + 1
        height = max(n for (_, n), _, _ in df) + 1
        self.grid = Grid.of_size(width, height).fill(".")
        self.grid[Point(*empty_pos)] = "_"
        self.grid[Point(width - 1, 0)] = "G"
        for p, u, _ in df:
            if u > empty_space:
                self.grid[Point(*p)] = "#"

    def neighbors(self, node):
        for d in Point.UDLR.values():
            if self.grid.get(node + d, "#") not in "#G":
                yield node + d

    def steps_to_move_data(self):
        goal = self.grid.index("G")
        empty = self.grid.index("_")
        left = Point.UDLR["<"]

        cost = 0
        while goal != Point.ZERO:
            # move to the left of goal then swap empty with goal
            cost += self.solve(empty, goal + left).cost() + 1
            self.grid[goal] = "."
            self.grid[goal + left] = "G"
            empty = goal
            goal = goal + left

        return cost


part_two(GridAStar(df).steps_to_move_data())
