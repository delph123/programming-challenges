from libs import *

# Parse input

initial_state, disk_length = read_lines("example")
disk_length = int(disk_length)

# Part 1


def dragon_curve(state: str, size):
    while len(state) < size:
        b = int("".join(reversed(state)), 2)
        b ^= 2 ** len(state) - 1
        state += "0" + format(b, f"0{len(state)}b")
    return state[:size]


def checksum(data):
    cs = "".join([str(int(a == b)) for a, b in batched(data, 2)])
    if len(cs) % 2 == 0:
        return checksum(cs)
    else:
        return cs


part_one(checksum(dragon_curve(initial_state, disk_length)))

# Part 2

part_two(checksum(dragon_curve(initial_state, 35651584)))
