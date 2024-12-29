from libs import *

# Parse input

messages = read_lines("example")

# Part 1


def pick(messages, col):
    return [row[col] for row in messages]


part_one(
    [Counter(pick(messages, i)).most_common()[0][0] for i in range(len(messages[0]))],
    sep="",
)

# Part 2

part_two(
    [Counter(pick(messages, i)).most_common()[-1][0] for i in range(len(messages[0]))],
    sep="",
)
