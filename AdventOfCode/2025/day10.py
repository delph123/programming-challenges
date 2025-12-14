from libs import *
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, value, PULP_CBC_CMD

# Parse input

matcher = create_matcher([(r"\[{str}\] {str*} \{{str}\}", (0, 1, 2))])

specifications = [matcher(l) for l in read_lines("example")]
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


def add(source, toggles):
    j = list(source)
    for t in toggles:
        j[t] += 1
    return tuple(j)


def initialize_joltage(buttons, requirements):
    # Use a Mixed-Integer Linear Programming Solver to solve the problem.

    # This is a diophantine system of equations where we want to minimize the sum of all
    # variables.
    #
    # Say we have:
    #   - requirement = {22,169,31,198}
    #   - buttons = (1,3) (0,2) (1,2,3) (0,3) (3)
    #
    # We can express the solution of the problem as:
    #   - solution = min( sum(a, b, c, d, e) )
    #   - where a, b, c, d, e are positive integers
    #   - and a * (0,1,0,1) + b * (1,0,1,0) + ... + e * (0,0,0,1) = (22,169,31,198)
    #
    # Or in other words:
    #   - b + d = 22
    #   - a + c = 169
    #   - b + c = 31
    #   - a + c + d + e = 198
    #
    # Note: in the sample, there are some problems where the number of variables is equal
    # to the number of equations but also some where it is bigger (underdetermined) and
    # some where it is smaller (overdetermined, and in this case we can trust the author
    # of the problem made sure that a solution exists). Anyway, with the minimization of
    # the sum, we always have a unique solution.

    problem = LpProblem("diophantine_system", LpMinimize)

    variables = [
        LpVariable("x" + str(i), lowBound=0, cat="Integer") for i in range(len(buttons))
    ]

    problem += sum(variables), "minimize_number_of_presses"

    for i in range(len(requirements)):
        eq = sum(variables[j] for j, toggles in enumerate(buttons) if i in toggles)
        problem += eq == requirements[i], "equation_for_joltage_req_" + str(i)

    problem.solve(PULP_CBC_CMD(msg=False))  # msg=False is to silence solver logging

    # print("Solution:", [value(x) for x in variables], f"({LpStatus[model.status]})")

    return int(value(problem.objective))


part_two(sum(initialize_joltage(b, j) for (_, b, j) in specifications))
