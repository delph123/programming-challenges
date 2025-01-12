from libs import *

# Parse input

stones = [int(d) for d in read("example").split(" ")]

# Part 1


def blink(stones, times):
    for _ in range(times):
        next_stones = list()
        for s in stones:
            if s == 0:
                next_stones.append(1)
                continue
            s_digits = str(s)
            if len(s_digits) % 2 == 0:
                next_stones.append(int(s_digits[: int(len(s_digits) / 2)]))
                next_stones.append(int(s_digits[int(len(s_digits) / 2) :]))
                continue
            next_stones.append(2024 * s)
        stones = next_stones
    return stones


part_one(len(blink(stones, 25)))

# Part 2


@cache
def blink_stone(s, times):
    if times == 0:
        return 1
    if s == 0:
        return blink_stone(1, times - 1)
    s_digits = str(s)
    if len(s_digits) % 2 == 0:
        a = blink_stone(int(s_digits[: int(len(s_digits) / 2)]), times - 1)
        b = blink_stone(int(s_digits[int(len(s_digits) / 2) :]), times - 1)
        return a + b
    return blink_stone(2024 * s, times - 1)


part_two(sum([blink_stone(s, 75) for s in stones]))
