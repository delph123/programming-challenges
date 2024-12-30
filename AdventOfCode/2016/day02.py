from libs import *

# Parse input

# Read and normalize directions from file to ^ v < > notation
instructions = read_lines("example", replace=zip("UDLR", "^v<>"))

square_keypad = Grid(["123", "456", "789"])
diamond_keypad = Grid(["  1  ", " 234 ", "56789", " ABC ", "  D  "])

# Part 1


def decode(keypad):
    start = keypad.index("5")
    code = []
    for inst in instructions:
        for t in inst:
            if keypad.get(start + Point.UDLR[t], " ") != " ":
                start += Point.UDLR[t]
        code.append(keypad[start])
    return "".join(code)


part_one(decode(square_keypad))

# Part 2

part_two(decode(diamond_keypad))
