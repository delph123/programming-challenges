from libs import *

# Parse input

spreadsheet = [tuple(int(d) for d in l.split()) for l in read_lines("example")]

sheet1 = spreadsheet[: len(spreadsheet) // 2] if read.from_example else spreadsheet
sheet2 = spreadsheet[-(len(spreadsheet) // 2) :] if read.from_example else spreadsheet

# Part 1


def checksum(spreadsheet):
    return sum(max(l) - min(l) for l in spreadsheet)


part_one(checksum(sheet1))

# Part 2


def multiples(line):
    for a, b in combinations(line, 2):
        if max(a, b) % min(a, b) == 0:
            return max(a, b) // min(a, b)


part_two(sum(multiples(l) for l in sheet2))
