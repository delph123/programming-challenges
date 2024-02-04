from libs import *

# Parse input

instructions = read_lines("example")
square_keypad = ["123", "456", "789"]
diamond_keypad = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]
DIRS = {"U": -1j, "D": 1j, "L": -1, "R": 1}

# Part 1


def decode(start, keypad):
    code = []
    for inst in instructions:
        for t in inst:
            s = start + DIRS[t]
            if (
                s.imag >= 0
                and s.imag < len(keypad)
                and s.real >= 0
                and s.real < len(keypad)
                and keypad[int(s.imag)][int(s.real)] != " "
            ):
                start = s
        code.append(keypad[int(start.imag)][int(start.real)])
    return "".join(code)


part_one(decode(1 + 1j, square_keypad))

# Part 2

part_two(decode(0 + 2j, diamond_keypad))
