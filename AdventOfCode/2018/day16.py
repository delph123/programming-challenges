from libs import *
from operator import and_

# Parse input (there is no example working for part 2)

samples, program_instructions = read("example").split("\n\n\n\n")


@dataclass
class Sample:
    before: list[int]
    instruction: list[int]
    after: list[int]


samples = [s.splitlines() for s in samples.split("\n\n")]
samples = [(b[9:-1].split(", "), i.split(), a[9:-1].split(", ")) for b, i, a in samples]
samples = [Sample(*(list(map(int, x)) for x in s)) for s in samples]

program_instructions = program_instructions.splitlines()
program_instructions = [[int(n) for n in l.split()] for l in program_instructions]

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


def exec(opcodes, initial_registers, instructions):
    registers = initial_registers[:]
    for opcode, lhs, rhs, tgt in instructions:
        registers[tgt] = opcodes[opcode](registers, lhs, rhs)
    return registers


def match_instr(sample: Sample):
    final_state = partial(
        exec, initial_registers=sample.before, instructions=[sample.instruction]
    )
    return set(
        opcode
        for opcode, operation in OPCODES.items()
        if final_state({sample.instruction[0]: operation}) == sample.after
    )


part_one(sum(len(match_instr(sample)) >= 3 for sample in samples))

# Part 2


def instruction_set(samples: list[Sample]):
    candidates = {i: set(OPCODES.keys()) for i in range(16)}
    for sample in samples:
        candidates[sample.instruction[0]] &= match_instr(sample)

    instructions = {}
    while candidates:
        instr = min(i for i, ops in candidates.items() if len(ops) == 1)
        opcode = list(candidates[instr])[0]
        instructions[instr] = OPCODES[opcode]
        del candidates[instr]
        for c in candidates:
            if opcode in candidates[c]:
                candidates[c].remove(opcode)

    return instructions


if not read.from_example:
    part_two(exec(instruction_set(samples), [0, 0, 0, 0], program_instructions)[0])
else:
    part_two("no example working for this part!")
