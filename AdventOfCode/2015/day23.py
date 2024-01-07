from libs import *

# Parse input

instructions = [
    ([l[0:3]] + (l[4:].split(", ") if "," in l else [l[4:], ""]))
    for l in read("example").split("\n")
]


# Part 1


def run(instructions, start):
    registers = {"a": start[0], "b": start[1]}
    pc = 0
    while 0 <= pc < len(instructions):
        inst, reg, offset = instructions[pc]
        match inst:
            case "hlf":
                registers[reg] //= 2
                pc += 1
            case "tpl":
                registers[reg] *= 3
                pc += 1
            case "inc":
                registers[reg] += 1
                pc += 1
            case "jmp":
                pc += int(reg[1:]) if reg[0] == "+" else -int(reg[1:])
            case "jie":
                if registers[reg] % 2 == 0:
                    pc += int(offset[1:]) if offset[0] == "+" else -int(offset[1:])
                else:
                    pc += 1
            case "jio":
                if registers[reg] == 1:
                    pc += int(offset[1:]) if offset[0] == "+" else -int(offset[1:])
                else:
                    pc += 1

    return registers


part_one(run(instructions, (0, 0))["b"])

# Part 2

part_two(run(instructions, (1, 0))["b"])
