from libs import *
from operator import lt, gt, le, ge, eq, ne

# Parse input

instructions = [l.split() for l in read_lines("e")]
instructions = [(a, b, int(c), d, e, int(f)) for (a, b, c, _, d, e, f) in instructions]

operations = {"<": lt, "<=": le, ">": gt, ">=": ge, "==": eq, "!=": ne}

# Part 1


def run(instructions):
    registers = defaultdict(int)
    for r, op, v, cr, cop, cv in instructions:
        if operations[cop](registers[cr], cv):
            registers[r] += v if op == "inc" else -v
    return registers


part_one(max(run(instructions).values()))

# Part 2


def run_p2(instructions):
    registers = defaultdict(int)
    highest = 0
    for r, op, v, cr, cop, cv in instructions:
        if operations[cop](registers[cr], cv):
            registers[r] += v if op == "inc" else -v
            highest = max(registers[r], highest)
    return highest


part_two(run_p2(instructions))
