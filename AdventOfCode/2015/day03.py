# Parse input

moves = open("AdventOfCode/2015/examples/day03.in").read().strip()


# Part 1

DIRS = {">": 1, "<": -1, "^": -1j, "v": 1j}


def walk(moves):
    s = 0
    visited = set([s])
    for m in moves:
        s += DIRS[m]
        visited.add(s)
    return visited


print("Part 1:", len(walk(moves)))

# Part 2

print("Part 2:", len(walk(moves[::2]) | walk(moves[1::2])))
