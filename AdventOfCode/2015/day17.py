# Parse input

containers = [
    int(n)
    for n in open("AdventOfCode/2015/examples/day17.in").read().strip().split("\n")
]

# Part 1


def fill(volume, containers):
    if volume == 0:
        return [[]]
    if len(containers) == 1:
        return [list(containers)] if volume == containers[0] else []
    combinations = []
    if volume >= containers[0]:
        combs = fill(volume - containers[0], containers[1:])
        combinations.extend([containers[0]] + c for c in combs)
    combinations.extend(fill(volume, containers[1:]))
    return combinations


combinations = fill(150 if len(containers) > 5 else 25, containers)

print("Part 1:", len(combinations))

# Part 2

comb_lengths = [len(c) for c in combinations]

print("Part 2:", comb_lengths.count(min(comb_lengths)))
