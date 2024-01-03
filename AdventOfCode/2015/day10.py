# Parse input

sequence = open("AdventOfCode/2015/examples/day10.in").read().strip()

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


def repeat(seq, times):
    for _ in range(times):
        seq = say(seq)
    return seq


print("Part 1:", len(repeat(sequence, 40)))

# Part 2

print("Part 2:", len(repeat(sequence, 50)))
