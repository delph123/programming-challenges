from collections.abc import Sequence
from functools import reduce
from itertools import chain, combinations
from copy import deepcopy
import cmath
from sys import float_info


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


def reversed_mapping(mapping):
    return {v: k for k, v in mapping.items()}


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


def compose(functions, initial, repeat=1):
    return reduce(lambda v, f: f(v), cycle(functions, repeat), initial)


def powerset(sequence):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
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

    def __rmul__(self, left):
        return Point(complex(left) * complex(self))

    def __mul__(self, right):
        return Point(complex(self) * complex(right))

    def __rtruediv__(self, left):
        return Point(complex(left) / complex(self))

    def __truediv__(self, right):
        return Point(complex(self) / complex(right))

    def __floordiv__(self, right):
        return Point(self.x // right, self.y // right)

    def __mod__(self, right):
        return Point(self.x % right, self.y % right)

    def __hash__(self):
        return complex(self).__hash__()

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __abs__(self):
        return abs(complex(self))

    def __complex__(self):
        return self.x + 1j * self.y

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def rotate(self, angle):
        """Rotate the vector by angle in degree"""
        # we need to add epsilon to avoid rounding issues with integer coordinates
        return self * cmath.rect(1 + float_info.epsilon, angle * cmath.pi / 180)

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


Point.ZERO = Point(0, 0)
Point.UDLR = {"^": Point(0, -1), "v": Point(0, 1), "<": Point(-1, 0), ">": Point(1, 0)}
Point.DIAGONALS = {
    "↖": Point(-1, -1),
    "↗": Point(1, -1),
    "↘": Point(1, 1),
    "↙": Point(-1, 1),
}
Point.DIRS = Point.UDLR | Point.DIAGONALS


class Grid:

    def __init__(self, content):
        self.content = content

    def __len__(self):
        return len(self.content) * len(self.content[0])

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return f"Grid({self})"

    def __eq__(self, other):
        return self.content == other.content

    def __ne__(self, other):
        return self.content != other.content

    def copy(self):
        return Grid(deepcopy(self.content))

    def __getitem__(self, p: Point):
        return self.content[p.y][p.x]

    def __setitem__(self, p: Point, val):
        self.content[p.y][p.x] = val

    def __contains__(self, p: Point):
        return p.is_within(self.content)

    def get(self, p: Point, default=None):
        return self[p] if p in self else default

    def at(self, index: int | complex | Point):
        """
        A more generic version of __getitem__ that can handle integer, complex or point.

        When the index is an integer, the returned item is equivalent to getting the nth
        value from iterator. Index can be negative to search from the end.
        When index is a Point or a complex, the returned item is equivalent to getting the
        item from __getitem__ with possibly a complex conversion to Point.
        """
        if isinstance(index, Point):
            return self[index]
        elif isinstance(index, complex):
            return self[Point(index)]
        else:
            return self[self.index_at(index)]

    def keys(self):
        for j in range(len(self.content)):
            for i in range(len(self.content[j])):
                yield Point(i, j)

    __iter__ = keys

    def values(self):
        for row in self.content:
            for v in row:
                yield v

    def items(self):
        for y, row in enumerate(self.content):
            for x, v in enumerate(row):
                yield (Point(x, y), v)

    def rows(self):
        return self.content

    def index_at(self, index: int):
        """The index (Point) in the grid at the index position in the iterator."""
        x = (index % len(self)) % len(self.content[0])
        y = (index % len(self)) // len(self.content[0])
        return Point(x, y)

    def index(self, val):
        for y, row in enumerate(self.content):
            for x, v in enumerate(row):
                if v == val:
                    return Point(x, y)

    def count(self, val):
        return sum(sum(1 for v in row if v == val) for row in self.content)

    def find_all(self, val):
        return set(p for (p, v) in self.items() if v == val)
