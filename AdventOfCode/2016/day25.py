from libs import *

# Parse input

instructions = [l.split() for l in read_lines("example")]

# Part 1


def run(program, registers, size_to_validate):
    target_pc = len(program)
    out_seq_size = 0
    pc = 0
    while pc < len(program):
        op = program[pc][0]
        if pc == target_pc:
            preview(registers)
        match op:
            case "out":
                r = program[pc][1]
                v = registers[r] if r in registers else int(r)
                if v != out_seq_size % 2:
                    return False
                else:
                    out_seq_size += 1
                    if out_seq_size == size_to_validate:
                        return True
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
    return False


# Brute-force all integers starting from 0 and stopping when we have found a number
# producing at least 1000 alternating zeros and ones.
part_one(
    next(
        i for i in count() if run(instructions, {r: 0 for r in "bcd"} | {"a": i}, 1000)
    )
)

####### ANALYSIS #######

# # The provided instructions are equivalent to:
# def clock(a):
#     d = a + 7 * 362  # 7 * 362 = 2534
#     while True:
#         a = d
#         while a > 0:
#             a, b = (a // 2, a % 2)
#             print(b)


# # Therefore, the value of 'a' will be:
# #   a = d - 7 * 362
# # Where d is the smallest integer whose binary representation
# # is 10..1010 and is bigger than 7 * 362
# def find_a(boundary):
#     d = "10"
#     while int(d, 2) < boundary:
#         d = "10" + d
#     return int(d, 2) - boundary


# part_one(find_a(7 * 362))
