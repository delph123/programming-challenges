from libs import *

# Parse input

instructions = [tuple(l.split()) for l in read_lines("i")]

# Part 1 & 2


def run(program, registers):
    pc = 0
    while pc < len(program):
        op = program[pc][0]
        if op == "cpy":
            v, r = program[pc][1:]
            if v in registers:
                registers[r] = registers[v]
            else:
                registers[r] = int(v)
        elif op == "inc":
            r = program[pc][1]
            registers[r] += 1
        elif op == "dec":
            r = program[pc][1]
            registers[r] -= 1
        elif op == "jnz":
            v, jmp = program[pc][1:]
            if (v in registers and registers[v] != 0) or (
                v not in registers and int(v) != 0
            ):
                pc += int(jmp)
                continue
        pc += 1
    return registers


part_one(run(instructions, {r: 0 for r in "abcd"})["a"])
part_two(run(instructions, {r: 0 for r in "abd"} | {"c": 1})["a"])

# Input program is actually equivalent to:

# def fib(n):
#     a, b = 1, 1
#     for _ in range(n):
#         a, b = a + b, a
#     return a

# part_one(fib(26) + 16 * 17)
# part_two(fib(26 + 7) + 16 * 17)
