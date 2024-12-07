from libs import *

# Parse file

maps = [m.strip().split("\n") for m in read("example").split("\n\n")]

# Part 1


def reflect(map):
    for i in range(len(map) - 1):
        max = min(i + 1, len(map) - 1 - i)
        if all(map[i - h] == map[i + 1 + h] for h in range(max)):
            return i


rows = [reflect(m) for m in maps]
cols = [reflect(transpose(m)) for m in maps]
part_one(
    sum([100 * (r + 1) for r in rows if r is not None])
    + sum([c + 1 for c in cols if c is not None]),
)

# Part 2


def reflect_smudge(map):
    for i in range(len(map) - 1):
        max = min(i + 1, len(map) - 1 - i)
        corr = 0
        for h in range(max):
            for j in range(len(map[i - h])):
                if map[i - h][j] != map[i + 1 + h][j]:
                    corr += 1
                if corr >= 2:
                    break
            if corr >= 2:
                break
        if corr == 1:
            return i


rows_smudge = [reflect_smudge(m) for m in maps]
cols_smudge = [reflect_smudge(transpose(m)) for m in maps]
part_two(
    sum([100 * (r + 1) for r in rows_smudge if r is not None])
    + sum([c + 1 for c in cols_smudge if c is not None]),
)
