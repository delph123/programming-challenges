from libs import *

# Parse input

changes = [int(n) for n in read_lines("example")]

# Part 1

part_one(sum(changes))

# Part 2


def repeated_frequency(start):
    frequencies = {start}
    f = start
    while True:
        for c in changes:
            f += c
            if f in frequencies:
                return f
            frequencies.add(f)


part_two(repeated_frequency(0))
