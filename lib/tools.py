from collections.abc import Sequence
from functools import reduce
from itertools import chain, combinations


def replace_all(old_words: list[str], new_words: str | list[str], source: str):
    """Returns a copy with all occurrences from old words replaced with
    new one in source string.
    """
    return reduce(
        lambda x, y: x.replace(y, new_words),
        old_words,
        source,
    )


def multi_replace(replacements: list[tuple[str, str]], source: str):
    """Apply multiple replacements sequentially and return the result"""
    return reduce(
        lambda x, rep: x.replace(rep[0], rep[1]),
        replacements,
        source,
    )


def flatten(list_of_lists, collect=list):
    return collect(chain.from_iterable(list_of_lists))


def reversed_mapping(mapping):
    return {v: k for k, v in mapping.items()}


def is_iterable(obj):
    try:
        return iter(obj) is not None
    except:
        return False


def cycle(iterable, times=None):
    if times is not None and times < 0:
        raise ValueError("times argument cannot be negative")
    if times == 0:
        return

    saved = []

    for element in iterable:
        yield element
        saved.append(element)

    if times is None:
        while saved:
            for element in saved:
                yield element
    else:
        for _ in range(1, times):
            for element in saved:
                yield element


def compose(functions, *initial_args, repeat=1):
    if len(initial_args) == 1:
        return reduce(lambda v, f: f(v), cycle(functions, repeat), initial_args[0])
    else:
        return reduce(lambda v, f: f(*v), cycle(functions, repeat), initial_args)


def powerset(sequence):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    return flatten(combinations(sequence, r) for r in range(len(sequence) + 1))


def transpose(grid):
    if len(grid) == 0:
        return []
    if isinstance(grid[0], str):
        return ["".join(r) for r in zip(*grid)]
    else:
        return list(zip(*grid))


def bisect(seq: Sequence, value, *, key=None, reverse=False, smallest=False):
    if not seq:
        return -1
    i = (len(seq) - 1) // 2
    v = seq[i]
    if key is not None:
        v = key(v)
    if not reverse and v < value or reverse and v > value:
        i2 = bisect(seq[i + 1 :], value, key=key, reverse=reverse, smallest=smallest)
        return i + 1 + i2 if i2 >= 0 else -1
    elif v == value and (not smallest or i == 0):
        return i
    elif v == value:
        return bisect(seq[: i + 1], value, key=key, reverse=reverse, smallest=smallest)
    else:
        return bisect(seq[:i], value, key=key, reverse=reverse, smallest=smallest)
