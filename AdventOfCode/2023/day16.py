from collections import deque

# Parse file

layout = open("AdventOfCode/2023/examples/day16.in").read().strip().split("\n")

# Part 1

def get(map, coord):
    return map[int(coord.imag)][int(coord.real)]

def empty_map(map):
    return [[[False,False,False,False] for _ in range(len(map[i]))] for i in range(len(map))]

def beams(map, start):
    q = deque([start])
    b4 = empty_map(map)
    while q:
        t, d = q.popleft()
        if t.real < 0 or t.real >= len(map[0]):
            continue
        if t.imag < 0 or t.imag >= len(map):
            continue
        v = get(map, t)
        x = int((d.real+1) // 2 + abs(d.imag) * (2 + ((d.imag+1) // 2)))
        if get(b4, t)[x]:
             continue
        get(b4, t)[x] = True
        if v == '.' or (v == '|' and d.real == 0) or (v == '-' and d.imag == 0):
            q.append(((t+d), d))
        elif v == '|':
            q.append((t-1j, -1j))
            q.append((t+1j, 1j))
        elif v == '-':
            q.append((t-1, -1))
            q.append((t+1, 1))
        elif v == '/':
            if d.real == 1:
                q.append((t-1j, -1j))
            elif d.real == -1:
                q.append((t+1j, 1j))
            elif d.imag == 1:
                q.append((t-1, -1))
            elif d.imag == -1:
                q.append((t+1, 1))
        elif v == '\\':
            if d.real == 1:
                q.append((t+1j, 1j))
            elif d.real == -1:
                q.append((t-1j, -1j))
            elif d.imag == 1:
                q.append((t+1, 1))
            elif d.imag == -1:
                q.append((t-1, -1))
    return b4

def countb(map):
    c = 0
    for row in map:
        for val in row:
            c += 1 if any(val) else 0
    return c

print("Part 1:", countb(beams(layout, (0, 1))))

# Part 2

m = 0

for i in range(len(layout)):
    m = max(m, countb(beams(layout, (i * 1j, 1))))
    m = max(m, countb(beams(layout, (len(layout[i]) - 1 + i * 1j, -1))))

for i in range(len(layout[0])):
    m = max(m, countb(beams(layout, (i, 1j))))
    m = max(m, countb(beams(layout, ((len(layout) - 1) * 1j + i, -1j))))

print("Part 2:", m)