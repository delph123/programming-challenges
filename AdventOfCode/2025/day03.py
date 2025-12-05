from libs import *

# Parse input

banks = [[int(n) for n in r] for r in read_lines("example")]

# Part 1


def largest_joltage(row, digits):
    if digits == 1:
        return max(row)
    else:
        d = digits - 1
        m = max(row[:-d])
        return m * (10**d) + largest_joltage(row[row.index(m) + 1 :], d)


part_one(sum([largest_joltage(b, 2) for b in banks]))

# Part 2


part_two(sum([largest_joltage(b, 12) for b in banks]))
