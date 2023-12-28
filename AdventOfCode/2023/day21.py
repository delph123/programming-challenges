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


# Due to the nature of the input, the walk will cycle after 262 steps
# (since the map size is 131, which is odd, we need to multiply the
# number of steps by two to 262 to cycle - or the points we reach after
# only 131 steps will alternate).
# What's more, the middle of the map is located exactly 65 steps from
# the border.
# Interestingly, the number of steps to reach can be expressed:
#   26501365 = 101150 * 262 + 65
def walk_p2():
    n1 = set([start()])
    cache = [set(), set()]
    # Let's compute 3 factors (each every 262 steps)
    factors = []
    for s in range(2 * 262 + 65):
        n2 = set()
        for n in n1:
            for d in [1, -1, 1j, -1j]:
                u, k = accept_p2(n + d)
                if u is not None:
                    n2.add(n + d)
        n1 = n2 - cache[s % 2]
        cache[s % 2] = n2 | cache[s % 2]
        if (s + 1) % 262 == 65:
            factors.append(len(cache[s % 2]))
    # After having computing 3 factors, we can compute the diff between them
    # and use the fact that we have 8 odd diamonds followed by 16 even diamonds
    # after one cycle (first diff) and 24 odd diamonds followed by 32 even after
    # second cycle (second diff).
    # Therefore:
    #     - 8 * odd + 16 * even = f[1] - f[0]
    #     - 24 * odd + 32 * even = f[2] - f[1]
    # And:
    #     - 8 * odd = (f[2] - f[1]) - 2 * (f[1] - f[0])
    #     - 8 * even = (f[1] - f[0] - odd) / 2
    odd = factors[2] - 3 * factors[1] + 2 * factors[0]
    even = (factors[1] - factors[0] - odd) // 2
    # The formula to compute is the following:
    # f[0] + 8 * odd + 2 * 8 * even + 3 * 8 * odd + 4 * 8 * even + ... + 8 * (2 * n - 1) * odd + 8 * 2 * n * even
    n = 26501365 // 262
    return factors[0] + n * n * odd + n * (n + 1) * even


# Note: it won't work on the example though
print("Part 2:", walk_p2())
