# Parse file

cards = [
    line.split(": ")[1].strip().split(" | ")
    for line in open("AdventOfCode/2023/examples/day4.in").read().strip().split("\n")
]
cards = [([int(n) for n in a.split()], [int(n) for n in b.split()]) for (a, b) in cards]

# Part 1

points = []

for winning, own in cards:
    x = len(set(winning) & set(own))
    if x:
        points.append(pow(2, x - 1))

print("Part 1:", sum(points))

# Part 2

deck = [1 for _ in range(len(cards))]

for i, (winning, own) in enumerate(cards):
    matchs = len(set(winning) & set(own))
    for j in range(matchs):
        deck[i + j + 1] += deck[i]

print("Part 2:", sum(deck))
