from libs import *

# Parse input

directions = read("example")

# Part 1

part_one(directions.count("(") - directions.count(")"))

# Part 2

floor = 0
for i in range(len(directions)):
    floor += 1 if directions[i] == "(" else -1
    if floor == -1:
        part_two(i + 1)
        break
