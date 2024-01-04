# Parse input

detected = """
    children: 3
    cats: 7
    samoyeds: 2
    pomeranians: 3
    akitas: 0
    vizslas: 0
    goldfish: 5
    trees: 3
    cars: 2
    perfumes: 1
"""

detected = {
    l.strip().split(": ")[0]: int(l.strip().split(": ")[1])
    for l in detected.strip().split("\n")
}

sues = [
    l.strip().replace(": ", "|", 1).split("|")
    for l in open("AdventOfCode/2015/examples/day16.in").read().strip().split("\n")
]

sues = {
    s[4:]: {
        l.strip().split(": ")[0]: int(l.strip().split(": ")[1])
        for l in p.strip().split(", ")
    }
    for s, p in sues
}

# Part 1


def match(sue):
    return all(detected[c] == v for c, v in sue.items())


print("Part 1:", list({sue for sue, caracs in sues.items() if match(caracs)})[0])

# Part 2


def match_p2(sue):
    def matcher(c, v, d):
        if c in ["cats", "trees"]:
            return v > d
        if c in ["pomeranians", "goldfish"]:
            return v < d
        return v == d

    return all(matcher(c, v, detected[c]) for c, v in sue.items())


print("Part 2:", list({sue for sue, caracs in sues.items() if match_p2(caracs)})[0])
