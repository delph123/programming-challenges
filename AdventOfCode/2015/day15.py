from libs import *

# Parse input

properties = [
    l.split(":")
    for l in read_lines(
        "example",
        ignore=[" capacity ", " durability ", " flavor ", " texture ", " calories "],
    )
]

properties = {
    ingredient: [int(n) for n in props.split(",")] for ingredient, props in properties
}

# Part 1


def score(take):
    capacity, durability, flavor, texture = 0, 0, 0, 0
    for ingredient, amount in take.items():
        c, d, f, t, _ = properties[ingredient]
        capacity += amount * c
        durability += amount * d
        flavor += amount * f
        texture += amount * t
    return max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(texture, 0)


def best_take(take, score):
    remaining = [p for p in properties.keys() if p not in take.keys()]

    if len(remaining) == 1:
        return score({**take, **{remaining[0]: 100 - sum(take.values())}})

    bt = 0
    for i in range(100 - sum(take.values()) + 1):
        bt = max(bt, best_take({**take, **{remaining[0]: i}}, score))
    return bt


part_one(best_take({}, score))

# Part 2


def score_p2(take):
    capacity, durability, flavor, texture, calories = 0, 0, 0, 0, 0
    for ingredient, amount in take.items():
        c, d, f, t, w = properties[ingredient]
        capacity += amount * c
        durability += amount * d
        flavor += amount * f
        texture += amount * t
        calories += amount * w
    if calories == 500:
        return max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(texture, 0)
    else:
        return 0


part_two(best_take({}, score_p2))
