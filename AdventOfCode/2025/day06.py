from libs import *

# Parse input

worksheet = read_lines("example")

# Fix because the last spaces could get lost!
line_size = max(len(l) for l in worksheet)
worksheet = [row + " " * (line_size - len(row)) for row in worksheet]

# Part 1


def transpose_p1(worksheet):
    problems = transpose([l.split() for l in worksheet])
    return [(p[-1], [int(n) for n in p[:-1]]) for p in problems]


def compute(op, numbers):
    if op == "+":
        return sum(numbers)
    else:
        return prod(numbers)


part_one(sum(compute(op, n) for op, n in transpose_p1(worksheet)))

# Part 2


def transpose_p2(worksheet):
    problems = [[None, []]]
    for n, op in [
        (row[:-1].strip(), row[-1]) for row in reversed(transpose(worksheet))
    ]:
        if n:
            if op != " ":
                problems[-1][0] = op
            problems[-1][1].append(int(n))
        else:
            problems.append([None, []])
    return problems


part_two(sum(compute(op, n) for op, n in transpose_p2(worksheet)))
