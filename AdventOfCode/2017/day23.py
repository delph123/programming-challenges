from libs import *
from lib.operations import iset, isub, imul, tryint, value

operations = {"set": iset, "sub": isub, "mul": imul}

# Parse input

instructions = [l.split(" ") for l in read_lines("example")]
instructions = [(l[0], tuple(tryint(n) for n in l[1:])) for l in instructions]

# Part 1


def exec(instructions):
    registers = defaultdict(int)
    cp = 0
    count_mul = 0
    while 0 <= cp < len(instructions):
        op, args = instructions[cp]
        if op == "jnz":
            if value(registers, args[0]) != 0:
                cp += value(registers, args[1])
                continue
        else:
            if op == "mul":
                count_mul += 1
            registers[args[0]] = operations[op](*(value(registers, a) for a in args))
        cp += 1
    return count_mul


part_one(exec(instructions))

# Part 2


def is_prime(n):
    if n > 2 and n % 2 == 0:
        return False
    return all(n % i != 0 for i in range(3, floor(sqrt(n)) + 1, 2))


# My instructions are equivalent to running following program:
def program():
    return sum(1 for i in range(1001) if not is_prime(109900 + 17 * i))


part_two(program())
