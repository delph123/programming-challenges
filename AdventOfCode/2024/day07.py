from libs import *

# Parse input

equations = [
    (int(eq.split(": ")[0]), [int(d) for d in eq.split(": ")[1].split(" ")])
    for eq in read_lines("example")
]

# Part 1


def eval(equation, operations):
    r = equation[0]
    for v, o in zip(equation[1:], operations):
        if o == "+":
            r += v
        elif o == "*":
            r *= v
        else:
            r = int(str(r) + str(v))
    return r


def test_true(equation, value):
    return any(
        eval(equation, operations) == value
        for operations in product(["+", "*"], repeat=len(equation) - 1)
    )


part_one(sum([a for (a, b) in equations if test_true(b, a)]))

# Part 2


def test_true_v2(equation, value):
    return any(
        eval(equation, operations) == value
        for operations in product(["+", "*", "||"], repeat=len(equation) - 1)
    )


part_one(sum([a for (a, b) in equations if test_true_v2(b, a)]))
