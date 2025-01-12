from libs import *

# Parse input

sequence = read("example")

# Part 1


def say(seq):
    prev = ""
    times = 0
    res = []
    for s in seq:
        if s != prev:
            if times > 0:
                res.append(str(times) + prev)
            prev = s
            times = 1
        else:
            times += 1
    if times > 0:
        res.append(str(times) + prev)
    return "".join(res)


part_one(len(compose(40 * [say], sequence)))

# Part 2

part_two(len(compose(50 * [say], sequence)))
