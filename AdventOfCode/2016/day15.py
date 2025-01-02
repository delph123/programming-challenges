from libs import *

# Parse input

disks = [
    tuple(int(d) for d in l.split(" ")[1:])
    for l in read_lines(
        "example",
        ignore=["positions; at time=0, it is at position ", "Disc #", "has ", "."],
    )
]

# Part 1 (Brute force minimum time to pass through disks)


def pass_through(disks, time):
    return all((time + i + 1 + pos) % size == 0 for i, (size, pos) in enumerate(disks))


part_one(next(t for t in count() if pass_through(disks, t)))


# Part 2 (Smart way: compute period of composition of all disks)


def period(disks):
    a, b = 0, 1
    for i, (size, pos) in enumerate(disks):
        u = (size - pos - (i + 1)) % size
        a = next(u + k * size for k in count() if (u + k * size) % b == a)
        b = size * b // gcd(b, size)
    return (a, b)


part_two(period(disks + [(11, 0)])[0])
