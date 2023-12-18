# Parse file

dig_plan = [
    l.split(" ")
    for l in open("AdventOfCode/2023/examples/day18.in").read().strip().split("\n")
]

dig_plan = [(a, int(b), c[2 : len(c) - 1]) for (a, b, c) in dig_plan]

# Part 1

turn = {"R": 1, "L": -1, "D": 1j, "U": -1j}
trans = {"#.#.": "F", "##..": "-", "#..#": "L", ".##.": "7", ".#.#": "J", "..##": "|"}

wall = {
    ".": 8,
    "7": 0.5,
    "-": 0,
    "F": -0.5,
    "J": -0.5,
    "|": 1,
    "L": 0.5,
}


def set(map, coord, val):
    map[int(coord.imag)][int(coord.real)] = val


def get(map, coord):
    return map[int(coord.imag)][int(coord.real)]


def scope(start, map):
    p = start
    imin = 0
    imax = 0
    jmin = 0
    jmax = 0
    for d, s, _ in map:
        p += s * turn[d]
        imin = min(imin, p.real)
        imax = max(imax, p.real)
        jmin = min(jmin, p.imag)
        jmax = max(jmax, p.imag)
    return (-imin - jmin * 1j, (imax - imin) + (jmax - jmin) * 1j)


def trench(map):
    a, b = scope(0, map)

    # Draw the digger
    grid = [["." for _ in range(int(b.real) + 3)] for _ in range(int(b.imag) + 3)]
    a = a + 1 + 1j
    for d, s, _ in map:
        for x in range(s):
            set(grid, a + x * turn[d], "#")
        a += s * turn[d]

    # Convert digger in a path formatted as day 10 :)
    grid2 = [r[:] for r in grid]
    for i in range(int(b.imag) + 1):
        for j in range(int(b.real) + 1):
            w = "".join(get(grid, j + 1 + (i + 1) * 1j + t) for t in turn.values())
            if get(grid, j + 1 + (i + 1) * 1j) == "#":
                set(
                    grid2,
                    j + 1 + (i + 1) * 1j,
                    trans[w],
                )

    return grid2


# Count same as day 10
def count(map):
    c = 0
    for l in map:
        out = True
        part = 0
        for x in l:
            v = wall[x]
            if v == 8:
                if not out:
                    c += 1
                continue
            c += 1
            if v == 1:
                out = not out
            elif abs(v) > 0.1 and abs(v) < 0.9:
                part += v
                if abs(part) == 1:
                    out = not out
                    part = 0
    return c


print("Part 1:", count(trench(dig_plan)))

# Part 2

turn_p2 = {"0": "R", "1": "D", "2": "L", "3": "U"}

dig_plan_p2 = [(turn_p2[c[5]], int(c[:5], 16), "") for (_, _, c) in dig_plan]


def scope_p2(start, map):
    p = start
    iset = {0}
    jset = {0}
    for d, s, _ in map:
        p += s * turn[d]
        iset.add(int(p.imag))
        jset.add(int(p.real))
    return sorted(iset), sorted(jset)


def trench_p2(map):
    iset, jset = scope_p2(0, map)

    # Draw the digger (only vertical lines)
    grid = [["." for _ in range(len(jset))] for _ in range(len(iset))]
    a = 0
    ai = iset.index(0)
    aj = jset.index(0)
    for d, s, _ in map:
        a += s * turn[d]
        bi = iset.index(int(a.imag))
        bj = jset.index(int(a.real))
        if abs(ai - bi) > 0:
            for x in range(min(ai, bi), max(ai, bi)):
                grid[x][aj] = "|"
        ai = bi
        aj = bj

    return grid, iset, jset


def measure(map, iset, jset):
    pick = [[False for _ in range(len(jset))] for _ in range(len(iset) - 1)]

    for i in range(len(iset) - 1):
        inside = False
        for j in range(len(jset)):
            if map[i][j] == "|":
                inside = not inside
            pick[i][j] = inside

    m = 0
    for i in range(len(iset) - 1):
        for j in range(len(jset) - 1):
            if pick[i][j]:
                # Add inside of square
                m += (jset[j + 1] - jset[j]) * (iset[i + 1] - iset[i])
                # Add vertical bar
                if not pick[i][j + 1]:
                    m += iset[i + 1] - iset[i]
                # Add horizontal bar
                if i + 1 >= len(pick) or not pick[i + 1][j]:
                    m += jset[j + 1] - jset[j]
                # Remove beginning of horizontal bar
                if i + 1 < len(pick) and not pick[i + 1][j] and pick[i + 1][j - 1]:
                    m -= 1
                # Add end of horizontal bar
                if not pick[i][j + 1] and (
                    i + 1 >= len(pick) or not pick[i + 1][j] and not pick[i + 1][j + 1]
                ):
                    m += 1

    return m


t, iset, jset = trench_p2(dig_plan_p2)
print("Part 2:", measure(t, iset, jset))
