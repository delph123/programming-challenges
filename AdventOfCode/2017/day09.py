from libs import *

# Parse input

streams = read_lines("example")

# Part 1


def score(stream):
    opened = 0
    s = 0
    garbage = False
    ignore = False
    for c in stream:
        if ignore:
            ignore = False
        elif c == "!":
            ignore = True
        elif garbage and c == ">":
            garbage = False
        elif not garbage and c == "{":
            opened += 1
            s += opened
        elif not garbage and c == "}":
            opened -= 1
        elif c == "<":
            garbage = True
    return s


part_one([score(stream) for stream in streams[:8]], sep=", ")

# Part 2


def garbage(stream):
    s = 0
    garbage = False
    ignore = False
    for c in stream:
        if ignore:
            ignore = False
        elif c == "!":
            ignore = True
        elif garbage and c == ">":
            garbage = False
        elif not garbage and c == "<":
            garbage = True
        elif garbage:
            s += 1
    return s


part_two([garbage(stream) for stream in streams[-7:]], sep=", ")
