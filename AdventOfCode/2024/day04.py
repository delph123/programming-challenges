from libs import *

# Parse input

xmas_grid = read_lines("example")

# Part 1


def count_xmas(grid):
    forward = sum([len(re.findall(r"XMAS", row)) for row in grid])
    backward = sum([len(re.findall(r"XMAS", "".join(reversed(row)))) for row in grid])
    return forward + backward


def rotate45(map):
    return [
        "".join(
            [
                map[i][n - i]
                for i in range(n + 1)
                if i < len(map) and n - i < len(map[0])
            ]
        )
        for n in range(len(map) + len(map[0]) - 1)
    ]


def rotate135(map):
    return [
        "".join(
            [
                map[n - len(map) + 1 + i][i]
                for i in range(len(map))
                if i < len(map)
                and n - len(map) + 1 + i < len(map)
                and n - len(map) + 1 + i >= 0
            ]
        )
        for n in range(len(map) + len(map[0]) - 1)
    ]


def all_directions(grid):
    horizontal = count_xmas(grid)
    vertical = count_xmas(transpose(grid))
    diagonal1 = count_xmas(rotate45(grid))
    diagonal2 = count_xmas(rotate135(grid))
    return [horizontal, vertical, diagonal1, diagonal2]


part_one(sum(all_directions(xmas_grid)))

# Part 2


def count_cross_mas(grid):
    c = 0
    for i in range(len(grid[0]) - 2):
        for j in range(len(grid) - 2):
            if grid[j + 1][i + 1] == "A":
                if (
                    grid[j][i] == "M"
                    and grid[j + 2][i + 2] == "S"
                    or grid[j][i] == "S"
                    and grid[j + 2][i + 2] == "M"
                ) and (
                    grid[j][i + 2] == "M"
                    and grid[j + 2][i] == "S"
                    or grid[j][i + 2] == "S"
                    and grid[j + 2][i] == "M"
                ):
                    c += 1
    return c


part_two(count_cross_mas(xmas_grid))
