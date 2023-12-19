from collections import deque
from copy import deepcopy

# Parse file

rules, parts = open("AdventOfCode/2023/examples/day19.in").read().strip().split("\n\n")

rules = [(r.split("{")[0], r.split("{")[1][:-1].split(",")) for r in rules.split("\n")]
rules = [(n, [r.split(":") for r in rs]) for n, rs in rules]
rules = {
    n: [
        (
            (r[1] if len(r) == 2 else r[0]),
            ((r[0][0], r[0][1], int(r[0][2:])) if len(r) == 2 else None),
        )
        for r in rs
    ]
    for n, rs in rules
}

parts = [
    {h.split("=")[0]: int(h.split("=")[1]) for h in p[1:-1].split(",")}
    for p in parts.split("\n")
]

# Part 1


def accept_part(p):
    s = "in"
    while True:
        if s == "A":
            return True
        elif s == "R":
            return False
        for n, r in rules[s]:
            if r is None:
                s = n
                break
            (l, c, m) = r
            if c == "<":
                if p[l] < m:
                    s = n
                    break
            else:
                if p[l] > m:
                    s = n
                    break


print(
    "Part 1:", sum([p["x"] + p["m"] + p["a"] + p["s"] for p in parts if accept_part(p)])
)

# Part 2


def rep(part, label, value):
    p = deepcopy(part)
    p[label] = value
    return p


def parts_combinations():
    q = deque(
        [("in", {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)})]
    )
    comb = 0
    while q:
        s, p = q.popleft()
        if s == "A":
            comb += (
                (p["x"][1] - p["x"][0] + 1)
                * (p["m"][1] - p["m"][0] + 1)
                * (p["a"][1] - p["a"][0] + 1)
                * (p["s"][1] - p["s"][0] + 1)
            )
            continue
        elif s == "R":
            continue
        for n, r in rules[s]:
            if r is None:
                q.append((n, p))
                break
            (l, c, m) = r
            lmin, lmax = p[l]
            if c == "<":
                if lmax < m:
                    q.append((n, p))
                    break
                elif lmin < m:
                    q.append((n, rep(p, l, (lmin, m - 1))))
                    p = rep(p, l, (m, lmax))
            else:
                if lmin > m:
                    q.append((n, p))
                    break
                elif lmax > m:
                    q.append((n, rep(p, l, (m + 1, lmax))))
                    p = rep(p, l, (lmin, m))
    return comb


print("Part 2:", parts_combinations())
