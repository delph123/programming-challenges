from libs import *

# Parse input

keys_locks = read("example").split("\n\n")
keys_locks = [Grid(kl.split("\n")) for kl in keys_locks]
locks = [g for g in keys_locks if g.at(0) == "#"]
keys = [g for g in keys_locks if g.at(-1) == "#"]

# Part 1


def heights(grid: Grid, is_key):
    return [
        6 - r.index("#") if is_key else r.index(".") - 1
        for r in grid.transpose().rows()
    ]


def fit(key, lock):
    return all(a + b < 6 for (a, b) in zip(key, lock))


def compatibles():
    key_heights = [heights(key, is_key=True) for key in keys]
    lock_heights = [heights(lock, is_key=False) for lock in locks]
    return [
        (key, lock)
        for key, lock in product(key_heights, lock_heights)
        if fit(key, lock)
    ]


part_one(len(compatibles()))
