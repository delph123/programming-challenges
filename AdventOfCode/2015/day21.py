from libs import *

# Parse input


def scores(items):
    items = items.strip().split("\n")
    items = [
        re.match(r"(.*) {2,10}(\d+) +(\d+) +(\d+)", item).groups() for item in items
    ]
    return [
        (name.strip(), int(cost), int(damage), int(armor))
        for name, cost, damage, armor in items
    ]


weapons = scores(
    """
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0
    """
)

armors = scores(
    """
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5
    """
)

rings = scores(
    """
    Damage +1    25     1       0
    Damage +2    50     2       0
    Damage +3   100     3       0
    Defense +1   20     0       1
    Defense +2   40     0       2
    Defense +3   80     0       3
    """
)

boss = {l.split(": ")[0]: int(l.split(": ")[1]) for l in read("input").split("\n")}

# Part 1


def best_price(caracs_comb, picker):
    # Pick any combination of at most two rings
    rings_comb = flatten(combinations(rings, r) for r in range(3))
    # Allow choosing no armor
    armors_or_none = [("", 0, 0, 0)] + armors

    price = None
    for md, ma in caracs_comb:
        for _, wp, wd, _ in weapons:
            for _, ap, _, aa in armors_or_none:
                for rc in rings_comb:
                    td = wd + sum(rd for (_, _, rd, _) in rc)
                    ta = aa + sum(ra for (_, _, _, ra) in rc)
                    if md == td and ma == ta:
                        if price is None:
                            price = wp + ap + sum(rp for (_, rp, _, _) in rc)
                        price = picker(price, wp + ap + sum(rp for (_, rp, _, _) in rc))

    return price


def min_price_to_win(my_health):
    caracs_comb = []
    for a in range(0, 11):
        # Number of turns the boss needs to kill myself
        t = ceil(my_health / max(boss["Damage"] - a, 1))
        # Damage necessary to kill boss before
        d = ceil((boss["Hit Points"] + t * boss["Armor"]) / t)
        if d <= 13 and a <= 5 or d <= 11 and a <= 8 or d <= 8:
            caracs_comb.append((d if d >= 4 else 4, a))

    return best_price(caracs_comb, min)


part_one(min_price_to_win(8 if boss["Hit Points"] == 12 else 100))

# Part 2


def max_price_to_loose(my_health):
    caracs_comb = []
    for a in range(0, 11):
        # Number of turns the boss needs to kill myself
        t = ceil(my_health / max(boss["Damage"] - a, 1))
        # Max damage not killing the boss before
        d = ceil((boss["Hit Points"] + t * boss["Armor"]) / t) - 1
        if d > 4 and (d <= 13 and a <= 5 or d <= 11 and a <= 8 or d <= 8):
            caracs_comb.append((d, a))

    return best_price(caracs_comb, max)


part_two(max_price_to_loose(8 if boss["Hit Points"] == 12 else 100))
