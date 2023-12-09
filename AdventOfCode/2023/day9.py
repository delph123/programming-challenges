report = [
    [int(n) for n in l.strip().split()]
    for l in open("AdventOfCode/2023/examples/day9.in").read().strip().split("\n")
]

# Compute diffs


def rec_diffs(history):
    diffs = [history]
    d = history
    while any(d):
        d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
        diffs.append(d)
    return diffs


hist_differences = [rec_diffs(h) for h in report]


# Part 1


def predict_future(diffs):
    n = 0
    for l in reversed(diffs):
        l.append(l[-1] + n)
        n = l[-1]

    return diffs[0][-1]


print("Part 1:", sum([predict_future(h) for h in hist_differences]))

# Part 2


def predict_past(diffs):
    n = 0
    for l in reversed(diffs):
        l.insert(0, l[0] - n)
        n = l[0]

    return diffs[0][0]


print("Part 2:", sum([predict_past(h) for h in hist_differences]))
