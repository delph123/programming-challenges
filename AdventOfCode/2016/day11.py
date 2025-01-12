from libs import *
from collections import namedtuple

Parts = namedtuple("Floor", ["rtgs", "chips"])


# Parse input

FLOORS = ["fourth", "third", "second", "first"]

floors_content = read_lines(
    "example",
    ignore=["The ", "a ", "floor contains ", "and ", ",", ".", " nothing relevant"],
    replace=[(" generator", "-rtg"), ("-compatible microchip", "-chip")],
)

floors_content = sorted(
    [c.split(" ") for c in floors_content], key=lambda f: FLOORS.index(f[0])
)
floors_content = tuple(
    Parts(
        frozenset(el.split("-")[0] for el in elements[1:] if el.split("-")[1] == "rtg"),
        frozenset(
            el.split("-")[0] for el in elements[1:] if el.split("-")[1] == "chip"
        ),
    )
    for elements in floors_content
)

elevator_floor = FLOORS.index("first")
target_floor = FLOORS.index("fourth")

# Part 1


def print_floors(e, floors):
    n, inc = len(floors), int(copysign(1, elevator_floor - target_floor))
    for i in range(target_floor, elevator_floor + inc, inc):
        connected = floors[i].rtgs & floors[i].chips
        rtgs = floors[i].rtgs - floors[i].chips
        chips = floors[i].chips - floors[i].rtgs
        print(f"\x1b[33m{n}\x1b[0m", "\x1b[1;35mE\x1b[0m" if e == i else " ", end=" ")
        if connected:
            print("\x1b[1;31mConnected = \x1b[0m", end="")
            print(*sorted(e for e in connected), sep=", ", end=" ")
        if rtgs:
            print("\x1b[1;32mRTGs = \x1b[0m", end="")
            print(*sorted(e for e in rtgs), sep=", ", end=" ")
        if chips:
            print("\x1b[1;34mChips = \x1b[0m", end="")
            print(*sorted(e for e in chips), sep=", ", end="")
        print()
        n -= 1
    print()


class FloorAStar(AStar):
    def __init__(self):
        super().__init__(visit_closed=False)

    def heuristic_cost_estimate(self, current, cost=0, goal=None):
        e, floors = current
        h = cost
        nb = 0
        inc = int(copysign(1, target_floor - elevator_floor))
        for i in range(elevator_floor, target_floor, inc):
            nb += len(floors[i].rtgs) + len(floors[i].chips)
            h += 1 if nb <= 2 else nb
        l = self.min_filled_floor(floors)
        if l != e:
            h += abs(e - l) + 1
        return h

    def neighbors(self, current):
        e, floors = current
        parts = self.expand(floors[e])
        for swaps in chain(combinations(parts, 2), combinations(parts, 1)):
            for d in (d for d in [-1, 1] if 0 <= e + d < len(floors)):
                np = self.position(floors, e, swaps, e + d)
                if self.is_valid(np):
                    yield ((e + d), np)

    def key(self, current):
        e, floors = current
        elements = defaultdict(int)
        for i, floor in enumerate(floors):
            for n in floor.rtgs:
                elements[n] += 10 * (i + 1)
            for n in floor.chips:
                elements[n] += i + 1
        return (e, tuple(sorted(elements.values())))

    def is_goal_reached(self, current, goal=None):
        return self.min_filled_floor(current[1]) == target_floor

    def min_filled_floor(self, floors):
        inc = int(copysign(1, target_floor - elevator_floor))
        for i in range(elevator_floor, target_floor + inc, inc):
            if floors[i].rtgs or floors[i].chips:
                return i

    def is_valid(self, floors):
        return all(not f.rtgs or f.chips <= f.rtgs for f in floors)

    def expand(self, floor_content):
        candidates = [("rtg", n) for n in floor_content.rtgs]
        candidates.extend([("chip", n) for n in floor_content.chips])
        return candidates

    def position(self, floors, level, swaps, next_level):
        rswap = frozenset(n for (k, n) in swaps if k == "rtg")
        cswap = frozenset(n for (k, n) in swaps if k == "chip")
        return tuple(
            (
                Parts(f.rtgs - rswap, f.chips - cswap)
                if i == level
                else (Parts(f.rtgs | rswap, f.chips | cswap) if i == next_level else f)
            )
            for i, f in enumerate(floors)
        )


sol_p1 = FloorAStar().solve((elevator_floor, floors_content))

# for e, f in sol_p1.path():
#     print_floors(e, f)

part_one(sol_p1.cost())

# Part 2

new_elements = {"elerium", "dilithium"}
to_floor = 1 if read.from_example else elevator_floor
floors_content_p2 = tuple(
    (Parts(f.rtgs | new_elements, f.chips | new_elements) if i == to_floor else f)
    for i, f in enumerate(floors_content)
)

sol_p2 = FloorAStar().solve((elevator_floor, floors_content_p2))

# for e, f in sol_p2.path():
#     print_floors(e, f)

part_two(sol_p2.cost())
