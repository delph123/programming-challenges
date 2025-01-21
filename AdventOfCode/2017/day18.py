from libs import *
from lib.operations import iset, iadd, imul, imod, tryint, value

operations = {"set": iset, "add": iadd, "mul": imul, "mod": imod}

# Parse input

instructions = [l.split(" ") for l in read_lines("example")]
instructions = [(l[0], tuple(tryint(n) for n in l[1:])) for l in instructions]

if read.from_example:
    instructions_p2 = instructions[instructions.index(("", ())) + 2 :]
    instructions = instructions[1 : instructions.index(("", ()))]
else:
    instructions_p2 = instructions

# Part 1


def exec(instructions):
    registers = defaultdict(int)
    cp = 0
    while 0 <= cp < len(instructions):
        op, args = instructions[cp]
        if op == "snd":
            sound = registers[args[0]]
        elif op == "rcv":
            return sound
        elif op == "jgz":
            if value(registers, args[0]) > 0:
                cp += value(registers, args[1])
                continue
        else:
            registers[args[0]] = operations[op](*(value(registers, a) for a in args))
        cp += 1


part_one(exec(instructions))

# Part 2


def coroutine(instructions, id):
    registers = defaultdict(int)
    registers["p"] = id
    queue_out = []
    queue_in = []
    cp = 0
    while 0 <= cp < len(instructions):
        op, args = instructions[cp]
        if op == "snd":
            queue_out.append(value(registers, args[0]))
        elif op == "rcv":
            if not queue_in:
                q = queue_out[:]
                queue_out.clear()
                queue_in = yield q
            registers[args[0]] = queue_in.pop()
        elif op == "jgz":
            if value(registers, args[0]) > 0:
                cp += value(registers, args[1])
                continue
        else:
            registers[args[0]] = operations[op](*(value(registers, a) for a in args))
        cp += 1


def exec_p2(instructions):
    total = ([], [])
    c0 = coroutine(instructions, 0)
    c1 = coroutine(instructions, 1)
    q1 = next(c0)
    q0 = next(c1)
    while q0 or q1:
        if q0:
            total[1].extend(q0)
            q1.extend(c0.send(list(reversed(q0))))
            q0.clear()
        if q1:
            total[0].extend(q1)
            q0.extend(c1.send(list(reversed(q1))))
            q1.clear()
    return total


part_two(len(exec_p2(instructions_p2)[1]))
