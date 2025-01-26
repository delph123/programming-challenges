from libs import *

# Parse input

components_ports = [tuple(int(n) for n in r.split("/")) for r in read_lines("example")]

# Part 1


def strongest(components, start):
    max_strength = 0
    for i, (a, b) in enumerate(components):
        if a == start:
            strength = strongest(components[:i] + components[i + 1 :], b)
            max_strength = max(max_strength, a + b + strength)
        if b == start and b != a:
            strength = strongest(components[:i] + components[i + 1 :], a)
            max_strength = max(max_strength, a + b + strength)
    return max_strength


part_one(strongest(components_ports, 0))

# Part 2


def strongest_p2(components, start):
    max_strength = (0, 0)
    for i, (a, b) in enumerate(components):
        if a == start:
            (size, strength) = strongest_p2(components[:i] + components[i + 1 :], b)
            max_strength = max(max_strength, (size + 1, strength + a + b))
        if b == start and b != a:
            (size, strength) = strongest_p2(components[:i] + components[i + 1 :], a)
            max_strength = max(max_strength, (size + 1, strength + a + b))
    return max_strength


part_two(strongest_p2(components_ports, 0)[1])
