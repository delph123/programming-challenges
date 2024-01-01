# Parse input

directions = open("AdventOfCode/2015/examples/day01.in").read().strip()

# Part 1

print("Part 1:", directions.count("(") - directions.count(")"))

# Part 2

floor = 0
for i in range(len(directions)):
    floor += 1 if directions[i] == "(" else -1
    if floor == -1:
        print("Part 2:", i + 1)
        break
