from functools import reduce
from itertools import chain, combinations


def replace_all(old_words: list[str], new_word: str, source: str):
    """Returns a copy with all occurrences from old words replaced with
    new one in source string.
    """
    return reduce(
        lambda x, y: x.replace(y, new_word),
        old_words,
        source,
    )


def flatten(list_of_lists):
    return list(chain.from_iterable(list_of_lists))


def compose(functions, initial):
    return reduce(lambda v, f: f(v), functions, initial)


def powerset(sequence):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    return flatten(combinations(sequence, r) for r in range(len(sequence) + 1))


def transpose(grid):
    if len(grid) == 0:
        return []
    if isinstance(grid[0], str):
        return [
            "".join([grid[i][j] for i in range(len(grid))]) for j in range(len(grid[0]))
        ]
    else:
        return [[grid[i][j] for i in range(len(grid))] for j in range(len(grid[0]))]
