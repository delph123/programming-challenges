from libs import *

# Parse input

rotations = read_lines("example")

# Part 1


def rotate(instructions):
    dial = 50
    password = 0
    for instr in instructions:
        dial = (dial + (-1 if instr[0] == "L" else 1) * int(instr[1:])) % 100
        if dial == 0:
            password += 1
    return password


part_one(rotate(rotations))

# Part 2


def rotate_p2(instructions):
    dial = 50
    password = 0
    for instr in instructions:
        if instr[0] == "R":
            password += (dial + int(instr[1:])) // 100
        else:
            password += abs((dial - int(instr[1:]) - 1) // 100)
            password -= 1 if dial == 0 else 0
        dial = (dial + (-1 if instr[0] == "L" else 1) * int(instr[1:])) % 100
    return password


part_two(rotate_p2(rotations))
