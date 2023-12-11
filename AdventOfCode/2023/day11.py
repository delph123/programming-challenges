# Parse map

map = [list(l) for l in open("AdventOfCode/2023/examples/day11.in").read().strip().split("\n")]

# Compute empty lines
rows = []
cols = []

for i in range(len(map)):
    if all(map[i][j] == '.' for j in range(len(map[i]))):
        rows.append(i)
for j in range(len(map[0])):
    if all(map[i][j] == '.' for i in range(len(map))):
        cols.append(j)

# Part 1 & 2

def sum_short_path(m, i, j, size):
    s = 0
    for a in range(i, len(m)):
        t = j if a == i else 0
        for b in range(t, len(m[a])):
            if m[a][b] == '#':
                if a < i:
                    x = sum([1 if a<r<i else 0 for r in rows])
                else:
                    x = sum([1 if i<r<a else 0 for r in rows])
                if b < j:
                    y = sum([1 if b<c<j else 0 for c in cols])
                else:
                    y = sum([1 if j<c<b else 0 for c in cols])
                s += abs(a - i) + abs(b - j) + (x + y) * size
    return s

def short_path(m, size):
    s = 0
    for i, l in enumerate(m):
        for j, g in enumerate(l):
            if g == '#':
                s += sum_short_path(m, i, j, size)
    return s

print("Part 1:", short_path(map, 1))
print("Part 2:", short_path(map, 1000000-1))