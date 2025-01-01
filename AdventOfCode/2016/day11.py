from libs import *

# Parse input

FLOORS = ["fourth", "third", "second", "first"]

floors_content = read_lines(
    "i",
    ignore=["The ", "a ", "floor contains ", "and ", ",", ".", " nothing relevant"],
    replace=[(" generator", "-gen"), ("-compatible microchip", "-chip")],
)

floors_content = sorted(
    [c.split(" ") for c in floors_content], key=lambda f: FLOORS.index(f[0])
)
floors_content = tuple(
    tuple(sorted(tuple(reversed(el.split("-"))) for el in elements[1:]))
    for elements in floors_content
)

elevator_floor = FLOORS.index("first")
target_floor = FLOORS.index("fourth")

# Part 1


def print_floors(e, floors):
    inc = int(copysign(1, elevator_floor - target_floor))
    n = len(FLOORS)
    for i in range(target_floor, elevator_floor + inc, inc):
        print(f"F{n}", "E" if e == i else " ", end=" ")
        print(*sorted(f"{b}-{a}" for a, b in floors[i]), sep=" ")
        n -= 1
    print()


def valid_floor(content):
    floor_content = {
        t: set(x for (_, x) in c) for t, c in groupby(content, key=itemgetter(0))
    }
    gens = floor_content.get("gen", set())
    chips = floor_content.get("chip", set())
    return len(chips - gens) == 0 or len(gens) == 0


def is_valid(floors):
    return all(valid_floor(f) for f in floors)


class FloorAStar(AStar):
    def __init__(self):
        super().__init__(visit_closed=False)

    def heuristic_cost_estimate(self, current, cost=0, goal=None):
        e, floors = current
        h = cost
        nb = 0
        malus = False
        inc = int(copysign(1, target_floor - elevator_floor))
        for i in range(elevator_floor, target_floor, inc):
            nb += len(floors[i])
            if not malus and nb > 0:
                malus = True
                h += abs(e - i)
                if abs(target_floor - e) < abs(target_floor - i):
                    h += 1
            h += 1 if nb <= 2 else nb
        return h

    def neighbors(self, current):
        e, floors = current
        if e + 1 < len(floors):
            for swaps in chain(combinations(floors[e], 2), combinations(floors[e], 1)):
                np = self.position(floors, e, swaps, e + 1)
                if is_valid(np):
                    yield ((e + 1), np)
        if e > 0:
            for swaps in chain(combinations(floors[e], 2), combinations(floors[e], 1)):
                np = self.position(floors, e, swaps, e - 1)
                if is_valid(np):
                    yield ((e - 1), np)

    def is_goal_reached(self, current, goal=None):
        return all(i == target_floor or len(c) == 0 for i, c in enumerate(current[1]))

    def position(self, floors, level, swaps, next_level):
        return tuple(
            (
                elements
                if i not in (level, next_level)
                else (
                    tuple(sorted(set(elements) - set(swaps)))
                    if i == level
                    else tuple(sorted(set(elements) | set(swaps)))
                )
            )
            for i, elements in enumerate(floors)
        )


sol_p1 = FloorAStar().solve((elevator_floor, floors_content))

# for e, f in sol_p1.path():
#     print_floors(e, f)

part_one(sol_p1.cost())

# Part 2

new_elements = product(["gen", "chip"], ["elerium", "dilithium"])
floors_content_p2 = tuple(
    (
        tuple(sorted(set(elements) | set(new_elements)))
        if i == elevator_floor
        else elements
    )
    for i, elements in enumerate(floors_content)
)

# Part 2 takes very long to compute but eventually finishes.

sol_p2 = FloorAStar().solve((elevator_floor, floors_content_p2))

# for e, f in sol_p2.path():
#     print_floors(e, f)

part_two(sol_p2.cost())
