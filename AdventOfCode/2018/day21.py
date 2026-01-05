from libs import *
from lib.operations import tryint

# Parse input

program_instructions = read_lines("example")

ip_pragma = int(program_instructions.pop(0).split()[1])
program_instructions = [[tryint(n) for n in l.split()] for l in program_instructions]


OPCODES = {
    "addr": lambda r, a, b: r[a] + r[b],
    "addi": lambda r, a, b: r[a] + b,
    "mulr": lambda r, a, b: r[a] * r[b],
    "muli": lambda r, a, b: r[a] * b,
    "banr": lambda r, a, b: r[a] & r[b],
    "bani": lambda r, a, b: r[a] & b,
    "borr": lambda r, a, b: r[a] | r[b],
    "bori": lambda r, a, b: r[a] | b,
    "setr": lambda r, a, b: r[a],
    "seti": lambda r, a, b: a,
    "gtir": lambda r, a, b: 1 if a > r[b] else 0,
    "gtri": lambda r, a, b: 1 if r[a] > b else 0,
    "gtrr": lambda r, a, b: 1 if r[a] > r[b] else 0,
    "eqir": lambda r, a, b: 1 if a == r[b] else 0,
    "eqri": lambda r, a, b: 1 if r[a] == b else 0,
    "eqrr": lambda r, a, b: 1 if r[a] == r[b] else 0,
}

# Part 1


def find_min_reg0_halting(instructions, registers, ip):
    while 0 <= registers[ip] < len(instructions):
        opcode, lhs, rhs, tgt = instructions[registers[ip]]
        # We can see from input that it's the comparison to register 0 that
        # ultimately causes the system to halt.
        if opcode[:2] in ["gt", "eq"] and (
            (opcode[2] == "r" and lhs == 0) or (opcode[3] == "r" and rhs == 0)
        ):
            if opcode[2] == "r" and lhs == 0:
                if opcode[:2] == "eq":
                    if opcode[3] == "i":
                        return rhs
                    else:
                        return registers[rhs]
                else:
                    if opcode[3] == "i":
                        return rhs + 1
                    else:
                        return registers[rhs] + 1
            else:
                if opcode[:2] == "eq":
                    if opcode[2] == "i":
                        return lhs
                    else:
                        return registers[lhs]
                else:
                    if opcode[2] == "i":
                        return 0
                    else:
                        return 0
        registers[tgt] = OPCODES[opcode](registers, lhs, rhs)
        registers[ip] += 1


part_one(find_min_reg0_halting(program_instructions, [0] * 6, ip_pragma))

# Part 2


# Except from 'prev' & 'visited', the function below is the equivalent python
# program from my specific input.
# In the function, variables 'b' and 'e' correspond to registers 1 and 5.
def find_max_reg0_halting():
    prev = None
    visited = set()
    b, e = 0, 0
    while b not in visited:
        prev = b
        visited.add(b)
        e = b | 65536  # 2**16
        b = 8586263  # 7 * 1226609
        b += e & 255  # 2**8-1
        b &= 16777215  # 2**24-1
        b *= 65899
        b &= 16777215
        while e >= 256:
            e //= 256
            b += e & 255  # 2**8-1
            b &= 16777215  # 2**24-1
            b *= 65899
            b &= 16777215
    return prev


part_two(find_max_reg0_halting())
