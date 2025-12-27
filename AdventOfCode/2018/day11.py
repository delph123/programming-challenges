from libs import *

# Parse input

serial_number = int(read("example"))

# Part 1


def power_levels(serial_number):
    levels_grid = Grid.of_size(300, 300)
    for p in levels_grid:
        rack_id = p.x + 11
        power = (rack_id * (p.y + 1) + serial_number) * rack_id
        levels_grid[p] = (power // 100) % 10 - 5
    return levels_grid


def sum_square(table: Grid, size: int, p: Point):
    return sum(table[p + Point(i, j)] for i in range(size) for j in range(size))


def largest_3x3_sum(table: Grid):
    width, height = table.size()
    sum_3x3_area = partial(sum_square, table, 3)
    return max(
        (Point(i, j) for i in range(width - 2) for j in range(height - 2)),
        key=sum_3x3_area,
    )


part_one(largest_3x3_sum(power_levels(serial_number)).coordinates(origin=1), sep=",")

# Part 2


def largest_summed_square(values: Grid):
    sum_rect = values.summed_area_calculator()
    sum_sq = lambda p, s: sum_rect(p, Point(s, s))

    p_max = Point.ZERO
    size = 1
    highest_power = sum_rect(p_max, Point(size, size))

    for j in range(300):
        for i in range(300):
            p = Point(i, j)
            l, s = max((sum_sq(p, s), s) for s in range(1, 301 - max(p.x, p.y)))
            if l > highest_power:
                p_max, size, highest_power = p, s, l

    return (p_max.x + 1, p_max.y + 1, size)


part_two(largest_summed_square(power_levels(serial_number)), sep=",")
