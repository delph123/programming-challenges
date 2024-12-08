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


def flatten(list_of_lists, collect=list):
    return collect(chain.from_iterable(list_of_lists))


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


class Point:
    def __init__(self, x, y=None):
        if isinstance(x, complex) and y is None:
            self.x = int(x.real)
            self.y = int(x.imag)
        elif y is not None:
            self.x = int(x)
            self.y = int(y)
        else:
            raise ValueError(
                "Point takes two integer parameters or one complex parameter"
            )

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return complex(self).__hash__()

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __abs__(self):
        return abs(complex(self))

    def __complex__(self):
        return self.x + 1j * self.y

    def is_within(self, grid):
        return 0 <= self.y < len(grid) and 0 <= self.x < len(grid[self.y])

    def is_within_bounds(self, horizontal_len, vertical_len):
        return 0 <= self.x < horizontal_len and 0 <= self.y < vertical_len

    def manhattan(self, other=None):
        if other is None:
            return abs(self.x) + abs(self.y)
        else:
            return abs(self.x - other.x) + abs(self.y - other.y)

    def get(self, grid):
        return grid[self.y][self.x]

    def set(self, grid, val):
        grid[self.y][self.x] = val
