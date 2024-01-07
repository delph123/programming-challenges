from libs import *

# Parse input

instructions = [
    (
        l.replace("turn ", "turn_").split(" ")[0],
        tuple(int(n) for n in l.replace("turn ", "turn_").split(" ")[1].split(",")),
        tuple(int(n) for n in l.split(" through ")[1].split(",")),
    )
    for l in read("example").split("\n")
]

# Part 1


def lit():
    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    for instruction, (a, b), (c, d) in instructions:
        assert a <= c and b <= d
        for i in range(a, c + 1):
            for j in range(b, d + 1):
                lights[i][j] = (
                    1
                    if instruction == "turn_on"
                    else (0 if instruction == "turn_off" else 1 - lights[i][j])
                )
    return lights


part_one(sum([sum(l) for l in lit()]))

# Part 2


def lit_p2():
    lights = [[0 for _ in range(1000)] for _ in range(1000)]
    for instruction, (a, b), (c, d) in instructions:
        assert a <= c and b <= d
        for i in range(a, c + 1):
            for j in range(b, d + 1):
                lights[i][j] += (
                    1
                    if instruction == "turn_on"
                    else (
                        2
                        if instruction == "toggle"
                        else (-1 if lights[i][j] >= 1 else 0)
                    )
                )
    return lights


part_two(sum([sum(l) for l in lit_p2()]))
