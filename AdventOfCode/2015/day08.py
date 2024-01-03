# Parse input

list = open("AdventOfCode/2015/inputs/day08.in").read().strip().split("\n")

# Part 1

print("Part 1:", sum([len(l) - len(eval(l)) for l in list]))

# Part 2

print("Part 2:", sum([2 + l.count('"') + l.count("\\") for l in list]))
