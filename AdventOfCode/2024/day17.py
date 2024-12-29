from libs import *

# Parse input

file = "example"
registers, program = read(file).split("\n\n")
registers = [r.split("Register ")[1].split(": ") for r in registers.split("\n")]
registers = {r: int(v) for (r, v) in registers}
program = list(batched([int(d) for d in program.split("Program: ")[1].split(",")], 2))

# Part 1


def combo(registers, operand):
    if operand < 4:
        return operand
    elif operand == 7:
        print("reserved!")
        return -1
    else:
        return registers[chr(ord("A") + operand - 4)]


def run(registers, program):
    ip = 0
    output = []
    while ip < len(program):
        opcode, operand = program[ip]
        if opcode == 0:
            registers["A"] //= 2 ** combo(registers, operand)
        elif opcode == 1:
            registers["B"] ^= operand
        elif opcode == 2:
            registers["B"] = combo(registers, operand) % 8
        elif opcode == 3:
            if registers["A"] != 0:
                ip = operand
                continue
        elif opcode == 4:
            registers["B"] ^= registers["C"]
        elif opcode == 5:
            output.append(combo(registers, operand) % 8)
        elif opcode == 6:
            registers["B"] = registers["A"] // 2 ** combo(registers, operand)
        elif opcode == 7:
            registers["C"] = registers["A"] // 2 ** combo(registers, operand)
        else:
            print("unknown opcode!")
            return
        ip += 1
    return output


part_one(run(registers.copy(), program), sep=",")

# Part 2


# After some transformation, we can see that running the program with register A
# initialized to some value is equivalent to running the below program for some
# specific next() function.
def exec(a_register, next):
    a = a_register
    output = []
    while a > 0:
        output.append(next(a))
        a //= 8
    return output


# The next function is very simple to find for the example, while for
# my input it looks like this big expression below.
def next(a):
    if file.startswith("e"):
        return (a // 8) % 8
    else:
        return (((a % 8) ^ 5) ^ (a // 2 ** ((a % 8) ^ 5)) ^ 6) % 8


# We can know regenerate a value for register A, by running the program backward
# identifying the step by step the octal digit that can work for the provided
# output (which, in the case of the exercise must be equal to the program code).

if file.startswith("e"):
    reverse_program = list(reversed([0, 3, 5, 4, 3, 0]))
else:
    reverse_program = list(reversed(flatten(program)))


def find_register_value(i, num):
    if i == len(reverse_program):
        return num
    for n in range(8):
        if next(8 * num + n) == reverse_program[i]:
            m = find_register_value(i + 1, 8 * num + n)
            if m is not None:
                return m
    return None


part_two(find_register_value(0, 0))
