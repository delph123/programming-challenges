from libs import *

# Parse input

matcher = create_matcher([(r"\[{str}\] {str*} \{{str}\}", (0, 1, 2))])

specifications = [matcher(l) for l in read_lines("i")]
specifications = [
    (
        l,
        [tuple(int(n) for n in r[1:-1].split(",")) for r in w.split(" ")],
        tuple(int(n) for n in j.split(",")),
    )
    for (l, w, j) in specifications
]

# Part 1


class InitializeLightsAStar(AStar):
    def __init__(self, buttons):
        super().__init__()
        self.buttons = buttons

    def neighbors(self, lights):
        for toggles in self.buttons:
            l = list(lights)
            for t in toggles:
                l[t] = "." if l[t] == "#" else "#"
            yield "".join(l)


part_one(
    sum(
        InitializeLightsAStar(b).solve("." * len(l), l).cost()
        for (l, b, _) in specifications
    )
)

# Part 2


class InitializeJoltageAStar(AStar):
    def __init__(self, buttons, target):
        super().__init__()
        self.buttons = buttons
        self.target = target

    def neighbors(self, levels):
        for toggles in self.buttons:
            j = list(levels)
            for t in toggles:
                j[t] += 1
            if all(j[i] <= v for i, v in enumerate(self.target)):
                yield tuple(j)


# part_two(
#     sum(
#         InitializeJoltageAStar(b, j).solve(tuple([0] * len(j)), j).cost()
#         for (_, b, j) in specifications
#     )
# )

s = 0
for _, b, j in specifications:
    s += InitializeJoltageAStar(b, j).solve(tuple([0] * len(j)), j).cost()
    print(s)
part_two(s)
