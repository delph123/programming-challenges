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


def exec(instructions, registers, ip):
    while 0 <= registers[ip] < len(instructions):
        opcode, lhs, rhs, tgt = instructions[registers[ip]]
        registers[tgt] = OPCODES[opcode](registers, lhs, rhs)
        registers[ip] += 1
    return registers


part_one(exec(program_instructions, [0] * 6, ip_pragma)[0])

# Part 2


# With registers denoted as
#   [a, b, c, d, ip, e]
#
# Here is the program that was running for my input:
def background_program(a):
    c = 898
    if a == 1:
        c = 10551298
        a = 0
    b = 1
    while b <= c:
        d = 1
        while d <= c:
            e = b * d
            if e == c:
                a += b
            d += 1
        b += 1
    return a


# Therefore, for a = 1, the program is computing the sum of divisor of 10551298.
# Note that on the example input, the program was just looping indefinitely.
part_two(sum(divisors(10551298)) if not read.from_example else "process never halts!")
