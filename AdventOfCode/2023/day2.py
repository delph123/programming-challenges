# Parse input

games = []

with open("AdventOfCode/2023/examples/day2.in") as file:
    for line in file:
        line = line.replace(" ", "").replace("\n", "")
        game, sets = line.split(":")
        game = int(game[4:])
        sets = sets.split(";")
        sets = [s.split(",") for s in sets]
        parsed_sets = []
        for set in sets:
            r, g, b = 0, 0, 0
            for el in set:
                if el.endswith("red"):
                    r = int(el[0:-3])
                if el.endswith("green"):
                    g = int(el[0:-5])
                if el.endswith("blue"):
                    b = int(el[0:-4])
            parsed_sets.append((r, g, b))
        games.append(parsed_sets)

# Part 1

rl, gl, bl = (12, 13, 14)

excludes = []

for i, game in enumerate(games):
    for r, g, b in game:
        if r > rl or g > gl or b > bl:
            excludes.append(i + 1)
            break

print("Part 1:", int(len(games) * (len(games) + 1) / 2 - sum(excludes)))

# Part 2

powers = []

for game in games:
    rm, gm, bm = (0, 0, 0)
    for r, g, b in game:
        rm = max(rm, r)
        gm = max(gm, g)
        bm = max(bm, b)
    powers.append(rm * gm * bm)

print("Part 2:", sum(powers))
