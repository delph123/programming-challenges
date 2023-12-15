import re

# Parse file

strings = [
    s for s in open("AdventOfCode/2023/examples/day15.in").read().strip().split(",")
]

# Part 1


def hash(string):
    h = 0
    for c in string:
        h += ord(c)
        h *= 17
        h %= 256
    return h


print("Part 1:", sum([hash(s) for s in strings]))

# Part 2


def label(string):
    return re.sub(r"(-|=)\d*$", "", string)


def lens(s, a):
    l = label(s)
    b = hash(l)
    ol = a[b]
    x = s[len(l)]
    if x == "-":
        try:
            i = [a for (a, _) in ol].index(l)
            ol.pop(i)
        except ValueError:
            pass
    else:
        y = int(s[len(l) + 1 :])
        try:
            i = [a for (a, _) in ol].index(l)
            ol[i] = (l, y)
        except ValueError:
            ol.append((l, y))


def power(boxes):
    p = 0
    for i, lenses in enumerate(boxes):
        for j, (_, f) in enumerate(lenses):
            p += (i + 1) * (j + 1) * f
    return p


a = [[] for _ in range(256)]
for s in strings:
    lens(s, a)

print("Part 2:", power(a))
