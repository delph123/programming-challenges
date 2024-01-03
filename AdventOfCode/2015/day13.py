# Parse input

potentials = [
    l.replace(".", "")
    .replace("would ", "")
    .replace("happiness units by sitting next to ", "")
    .split(" ")
    for l in open("AdventOfCode/2015/inputs/day13.in").read().strip().split("\n")
]

potentials = {
    (p1, p2): int(units) if outcome == "gain" else -int(units)
    for p1, outcome, units, p2 in potentials
}

attendees = list(set([a for a, _ in potentials.keys()]))


# Part 1


def happiness(arr):
    h = 0
    for i, attendee in enumerate(arr):
        h += potentials.get((attendee, arr[i - 1]), 0)
        if i == len(arr) - 1:
            h += potentials.get((attendee, arr[0]), 0)
        else:
            h += potentials.get((attendee, arr[i + 1]), 0)
    return h


def best_arrangement(attendees, arr, i):
    if i == len(arr):
        return happiness(arr)
    ba = 0
    for attendee in attendees:
        if attendee in arr[:i]:
            continue
        arr[i] = attendee
        ba = max(ba, best_arrangement(attendees, arr, i + 1))
    arr[i] = None
    return ba


print(
    "Part 1:",
    best_arrangement(attendees, attendees[0:1] + [None] * (len(attendees) - 1), 1),
)

# Part 2

print(
    "Part 2:",
    best_arrangement(["myself"] + attendees, ["myself"] + [None] * len(attendees), 1),
)
