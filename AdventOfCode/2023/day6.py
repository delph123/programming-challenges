# Part 1

with open("AdventOfCode/2023/examples/day6.in") as file:
    time = [int(a.strip()) for a in file.readline()[10:].strip().split()]
    dist = [int(a.strip()) for a in file.readline()[10:].strip().split()]

wins = 1

for (t, d) in zip(time, dist):
    w = 0
    for v in range(t):
        w += 1 if v * (t - v) > d else 0
    wins *= w

print("Part 1:", wins)

# Part 2

with open("AdventOfCode/2023/examples/day6.in") as file:
    time = int(file.readline()[10:].replace(" ", "").strip())
    dist = int(file.readline()[10:].replace(" ", "").strip())

# Even a few million loops are too quick to need optimizing,
# let's brute force this!
wins = 0
for v in range(time):
    wins += 1 if v * (time - v) > dist else 0

print("Part 2:", wins)
