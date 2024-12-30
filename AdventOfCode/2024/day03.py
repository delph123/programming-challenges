from libs import *

# Parse input

instruction = read("example", ignore=["\n"])  # Concatenate multi-line input

# Part 1


def exec(instruction):
    return [
        (int(a) * int(b)) for (a, b) in re.findall(r"mul\((\d+),(\d+)\)", instruction)
    ]


part_one(sum(exec(instruction)))

# Part 2


def active(instruction):
    return [
        x
        for x in flatten(
            re.findall(
                r"(?:(.*?)don't\(\).*?do\(\))|(?:(.*?)don't\(\).*)|(.*)", instruction
            )
        )
        if x
    ]


part_two(sum([sum(exec(x)) for x in active(instruction)]))
