from libs import *

# Parse input

players, marbles = [
    int(n)
    for n in read("e", ignore=["players; last marble is worth", "points"]).split()
]

# Part 1


def scores(players, marbles):
    if marbles < 23:
        return 0
    lhs, rhs = [0, 2], [1]
    scores = [0] * players
    for m in range(3, marbles + 1):
        if m % 23 != 0:
            if len(rhs) == 0:
                lhs, rhs = [], list(reversed(lhs))
            lhs.append(rhs.pop())
            lhs.append(m)
        else:
            for _ in range(8):
                if len(lhs) == 0:
                    lhs, rhs = list(reversed(rhs)), []
                rhs.append(lhs.pop())
            scores[(m - 1) % players] += m + rhs.pop()
            if len(rhs) == 0:
                lhs, rhs = [], list(reversed(lhs))
            lhs.append(rhs.pop())
    return scores


part_one(max(scores(players, marbles)))

# Part 2

part_two(max(scores(players, 100 * marbles)))
