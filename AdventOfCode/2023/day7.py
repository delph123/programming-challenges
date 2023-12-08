from functools import cmp_to_key
from collections import Counter

# Part 1

conv = { 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14 }

hands = []

with open("AdventOfCode/2023/examples/day7.in") as file:
    for line in file:
        cards, bid = line.split(" ")
        bid = int(bid.strip())
        cards = [int(c) if c.isdigit() else conv[c] for c in cards]
        hands.append((cards, bid))

def cmp_hands(left, right):
    lc = left[0]
    rc = right[0]

    lcnt = tuple(b for (_,b) in Counter(lc).most_common())
    rcnt = tuple(b for (_,b) in Counter(rc).most_common())

    if rcnt != lcnt:
        return 1 if rcnt > lcnt else -1

    i = 0
    while lc[i] == rc[i] and i < len(lc):
        i += 1

    return rc[i] - lc[i]

print("Part 1:", sum([(i+1) * b for (i, (_, b)) in enumerate(reversed(sorted(hands, key=cmp_to_key(cmp_hands))))]))

# Part 2

conv = { 'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14 }

hands_p2 = []

with open("AdventOfCode/2023/examples/day7.in") as file:
    for line in file:
        cards, bid = line.split(" ")
        bid = int(bid.strip())
        cards = [int(c) if c.isdigit() else conv[c] for c in cards]
        hands_p2.append((cards, bid))

def cmp_hands_p2(left, right):
    lc = left[0]
    rc = right[0]

    lc2 = [c for c in left[0] if c > 1]
    lcnt = [b for (_,b) in Counter(lc2).most_common()]
    if len(lcnt) == 0:
        lcnt.append(0)
    lcnt[0] += 5 - len(lc2)
    lcnt = tuple(lcnt)

    rc2 = [c for c in right[0] if c > 1]
    rcnt = [b for (_,b) in Counter(rc2).most_common()]
    if len(rcnt) == 0:
        rcnt.append(0)
    rcnt[0] += 5 - len(rc2)
    rcnt = tuple(rcnt)

    if rcnt != lcnt:
        return 1 if rcnt > lcnt else -1

    i = 0
    while lc[i] == rc[i] and i < len(lc):
        i += 1

    return rc[i] - lc[i]

print("Part 2:", sum([(i+1) * b for (i, (_, b)) in enumerate(reversed(sorted(hands_p2, key=cmp_to_key(cmp_hands_p2))))]))
