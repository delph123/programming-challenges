from libs import *

# Parse input

instructions = [l.split() for l in read_lines("example")]


# Part 1


def run(program, registers):
    target_pc = len(program)
    pc = 0
    while pc < len(program):
        op = program[pc][0]
        if pc == target_pc:
            preview(registers)
        match op:
            case "tgl":
                r = program[pc][1]
                v = registers[r] if r in registers else int(r)
                if pc + v < 0 or pc + v >= len(program):
                    pass
                elif len(program[pc + v]) == 2:
                    if program[pc + v][1] not in registers:
                        program[pc + v][0] = "pass"
                    elif program[pc + v][0] == "inc":
                        program[pc + v][0] = "dec"
                    else:
                        program[pc + v][0] = "inc"
                else:
                    if program[pc + v][0] == "jnz":
                        if program[pc + v][2] in registers:
                            program[pc + v][0] = "cpy"
                        else:
                            program[pc + v][0] = "pass"
                    else:
                        program[pc + v][0] = "jnz"
            case "cpy":
                v, r = program[pc][1:]
                if v in registers:
                    registers[r] = registers[v]
                else:
                    registers[r] = int(v)
            case "inc":
                r = program[pc][1]
                registers[r] += 1
            case "dec":
                r = program[pc][1]
                registers[r] -= 1
            case "jnz":
                v, jmp = program[pc][1:]
                if (v in registers and registers[v] != 0) or (
                    v not in registers and int(v) != 0
                ):
                    pc += registers[jmp] if jmp in registers else int(jmp)
                    continue
        pc += 1
    return registers


part_one(run(deepcopy(instructions), {r: 0 for r in "bcd"} | {"a": 7})["a"])

# Part 2


def modified_factorial(a):
    # Lines 1 - 19 of input instructions are actually equivalent to:
    b = a - 1
    while b > 1:  # While True, toggled into 'c = 1' when b == 1
        a *= b
        b -= 1
        # toggle line (17 + 2 * b)
    # After toggling, remaining instructions are equivalent to:
    a += 89 * 90
    return a


part_two(modified_factorial(12))
