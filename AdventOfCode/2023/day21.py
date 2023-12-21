# Parse file

map = open("AdventOfCode/2023/examples/day21.in").read().strip().split("\n")

# Part 1


def start():
    for x, row in enumerate(map):
        for y, v in enumerate(row):
            if v == "S":
                return y + x * 1j


def accept(coord):
    x = int(coord.imag)
    y = int(coord.real)
    return 0 <= x < len(map) and 0 <= y < len(map[x]) and map[x][y] != "#"


def walk(steps):
    n1 = set([start()])
    for _ in range(steps):
        n2 = set()
        for n in n1:
            for d in [1, -1, 1j, -1j]:
                if accept(n + d):
                    n2.add(n + d)
        n1 = n2
    return len(n1)


print("Part 1:", walk(64))

# Part 2


def accept_p2(coord):
    x = int(coord.imag) % len(map)
    y = int(coord.real) % len(map[x])
    if map[x][y] != "#":
        return (
            (y + x * 1j),
            ((int(coord.real) // len(map[x])) + (int(coord.imag) // len(map)) * 1j),
        )
    else:
        return None, 0


# Due to the nature of the input, the walk will cycle after 131 steps.
# What's more, the middle of the map is located exactly 65 steps from
# the border.
# Interestingly, the number of steps to reach can be expressed:
#   26501365 = 202300 * 131 + 65
def walk_p2():
    n1 = set([start()])
    cache = [set(), set()]
    # Let's compute 3 factors (each every 131 steps)
    factors = []
    for s in range(2 * 131 + 65):
        n2 = set()
        for n in n1:
            for d in [1, -1, 1j, -1j]:
                u, k = accept_p2(n + d)
                if u is not None:
                    n2.add(n + d)
        n1 = n2 - cache[s % 2]
        cache[s % 2] = n2 | cache[s % 2]
        if (s + 1) % 131 == 65:
            factors.append(len(cache[s % 2]))
    # After having computing 3 factors, we can use a polynomial
    # regression of second degree to compute the result of the problem
    a, b, c = factors
    n = 26501365 // 131
    return a + (b - a) * n + (a + c - 2 * b) * (n * (n - 1) // 2)


# Note: it won't work on the example though
print("Part 2:", walk_p2())
