from libs import *

# Parse input

instructions = read_lines("example")

width, height = (7, 3) if read.from_example else (50, 6)

# Part 1


def parse(instruction):
    if instruction.startswith("rect"):
        return ("rect", tuple(int(d) for d in instruction[5:].split("x")))
    elif instruction.startswith("rotate row"):
        return ("rotr", tuple(int(d) for d in instruction[13:].split(" by ")))
    elif instruction.startswith("rotate column"):
        return ("rotc", tuple(int(d) for d in instruction[16:].split(" by ")))


def display(instructions, width, height):
    screen = Grid.of_size(width, height).fill(".")
    for instruction in instructions:
        (op, (a, b)) = parse(instruction)
        if op == "rect":
            for x in range(a):
                for y in range(b):
                    screen[Point(x, y)] = "#"
        elif op == "rotc":
            col = [screen[Point(a, y)] for y in range(height)]
            for y in range(height):
                screen[Point(a, y)] = col[(y - b) % height]
        elif op == "rotr":
            row = [screen[Point(x, a)] for x in range(width)]
            for x in range(width):
                screen[Point(x, a)] = row[(x - b) % width]
    return screen


screen = display(instructions, width, height)

part_one(screen.count("#"))

# Part 2

part_two(screen)
