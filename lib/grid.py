import cmath
from sys import float_info
from copy import deepcopy
from .tools import (
    transpose as transpose_matrix,
    rotate as rotate_matrix,
    horizontal_flip,
    vertical_flip,
)


class Point:

    ZERO: "Point"
    UDLR: dict[str, "Point"]
    DIAGONALS: dict[str, "Point"]
    DIRS: dict[str, "Point"]

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
        """Rotate clockwise the vector by angle in degree"""
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


if __name__ == "__main__":
    print(Point.ZERO)


class Grid:

    def __init__(self, content):
        self.content = content

    @classmethod
    def of_size(cls, width, height):
        return cls([list(range(width * j, width * (j + 1))) for j in range(height)])

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

    def fill(self, val):
        for p in self.keys():
            self[p] = val
        return self

    def count(self, val):
        return sum(sum(1 for v in row if v == val) for row in self.content)

    def find_all(self, val):
        return set(p for (p, v) in self.items() if v == val)

    def hflip(self):
        return Grid(horizontal_flip(self.content))

    def vflip(self):
        return Grid(vertical_flip(self.content))

    def transpose(self):
        return Grid(transpose_matrix(self.content))

    def rotate(self, i):
        return Grid(rotate_matrix(self.content, i))
