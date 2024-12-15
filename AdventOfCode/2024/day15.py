from libs import *

# Parse input

warehouse, moves = read("example").split("\n\n")
moves = moves.replace("\n", "")
warehouse = Grid([list(row) for row in warehouse.split("\n")])

# Part 1


def move_robot():
    wh = warehouse.copy()
    r = wh.index("@")
    for m in moves:
        d = Point.UDLR[m]
        b = 1
        while wh[r + b * d] == "O":
            b += 1
        if wh[r + b * d] == "#":
            continue
        if b > 1:
            wh[r + b * d] = "O"
        wh[r + d] = "@"
        wh[r] = "."
        r += d
    return wh


def gps_coordinates(b):
    return b.x + 100 * b.y


part_one(sum([gps_coordinates(b) for b in move_robot().find_all("O")]))

# Part 2

left = Point.UDLR["<"]
right = Point.UDLR[">"]


def second_warehouse():
    def widen(t):
        if t == "#":
            return "##"
        if t == "O":
            return "[]"
        if t == ".":
            return ".."
        if t == "@":
            return "@."

    return Grid([flatten([widen(t) for t in row]) for row in warehouse.rows()])


def stones_to_move(grid, start, dir):
    # Find stones to move
    found = [{start}]
    while found[-1]:
        next = set()
        for p in found[-1]:
            if grid[p + dir] == "#":
                # We can't move
                return None
            elif grid[p + dir] == "[":
                next.add(p + dir)
                next.add(p + dir + right)
            elif grid[p + dir] == "]":
                next.add(p + dir)
                next.add(p + dir + left)
        found.append(next)
    return found


def move_robot_v2():
    wh = second_warehouse()
    r = wh.index("@")
    for m in moves:
        d = Point.UDLR[m]
        if m in "<>":
            b = 1
            while wh[r + b * d] in "[]":
                b += 1
            if wh[r + b * d] == "#":
                continue
            for i in range(b, 0, -1):
                wh[r + i * d] = wh[r + (i - 1) * d]
            wh[r] = "."
        else:
            stones_row = stones_to_move(wh, r, d)
            if stones_row is None:
                continue
            for points in reversed(stones_row):
                for p in points:
                    (wh[p + d], wh[p]) = (wh[p], wh[p + d])
        r += d
    return wh


part_two(sum([gps_coordinates(b) for b in move_robot_v2().find_all("[")]))
