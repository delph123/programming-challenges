from collections import deque

# Parse file

conditions = [
    (line.split(" ")[0], [int(n) for n in line.split(" ")[1].split(",")])
    for line in open("AdventOfCode/2023/examples/day12.in").read().strip().split("\n")
]

# Part 1 & 2


def count_arrangements(rec, groups_in, start, n, cache):
    groups = groups_in[n:]
    q = deque([rec[start:]])
    arr = 0
    while q:
        r = q.popleft()
        i = 0
        burst = 0
        g = []
        while i < len(r) and r[i] != "?":
            if r[i] == "." and burst != 0:
                g.append(burst)
                burst = 0
            elif r[i] == "#":
                burst += 1
            i += 1

        if i == len(r):
            if burst:
                g.append(burst)
            if g == groups:
                arr += 1
            continue

        if g != groups[0 : len(g)]:
            continue

        if len(g) == len(groups):
            if burst:
                continue
            else:
                if "#" not in r[i:]:
                    arr += 1
                continue

        if len(g) == len(groups) - 1:
            if burst:
                if burst > groups[len(g)]:
                    continue
                if (
                    len(r) >= i + groups[len(g)] - burst
                    and "." not in r[i : i + groups[len(g)] - burst]
                    and "#" not in r[i + groups[len(g)] - burst :]
                ):
                    arr += 1
                continue

        if len(r) - i < sum(groups[len(g) :]) + len(groups) - len(g) - 1 - burst:
            continue

        if burst == 0:
            if (start + i, n + len(g)) in cache:
                arr += cache[(start + i, n + len(g))]
            elif i == 0:
                q.append(r[0:i] + "." + r[i + 1 :])
                if (
                    len(r) >= i + groups[len(g)]
                    and "." not in r[i : i + groups[len(g)]]
                ):
                    q.append(r[0:i] + "#" * groups[len(g)] + r[i + groups[len(g)] :])
            else:
                x = count_arrangements(rec, groups_in, start + i, n + len(g), cache)
                cache[(start + i, n + len(g))] = x
                arr += x
        elif len(groups) > len(g) and burst == groups[len(g)]:
            q.append(r[0:i] + "." + r[i + 1 :])
        elif len(groups) > len(g) and burst < groups[len(g)]:
            if (
                len(r) >= i + groups[len(g)] - burst
                and "." not in r[i : i + groups[len(g)] - burst]
            ):
                q.append(
                    r[0:i]
                    + "#" * (groups[len(g)] - burst)
                    + r[i + groups[len(g)] - burst :]
                )

    return arr


print(
    "Part 1:", sum([count_arrangements(c[0], c[1], 0, 0, dict()) for c in conditions])
)

print(
    "Part 2:",
    sum(
        [
            count_arrangements("?".join([c[0]] * 5), c[1] * 5, 0, 0, dict())
            for c in conditions
        ]
    ),
)
