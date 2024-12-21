from libs import *

# Parse input

codes = read_lines("i")

UDLR = reversed_mapping(Point.UDLR)

numeric_keypad = Grid(["789", "456", "123", "*0A"])
numeric_start = numeric_keypad.index("A")
directional_keypad = Grid(["*^A", "<v>"])
directional_start = directional_keypad.index("A")

# Part 1


class KeypadAStar(AStar):
    def __init__(self, keypad) -> None:
        super().__init__()
        self.keypad = keypad

    def neighbors(self, node: Point):
        return (
            node + d
            for d in Point.UDLR.values()
            if self.keypad.get(node + d, "*") != "*"
        )


def directions(path):
    for a, b in pairwise(path):
        yield UDLR[b - a]
    yield "A"


def sequences_between(shortest_path, keypad, beg, end):
    start, goal = keypad.index(beg), keypad.index(end)
    paths = shortest_path.solve(start, goal).all_paths()
    return ["".join(directions(p)) for p in paths]


def shortest_seq_for_code(shortest_seq_between, code, *args):
    seq = []
    for start, stop in pairwise("A" + code):
        seq.extend(shortest_seq_between(start, stop, *args))
    return seq


numeric_shortest_path = KeypadAStar(numeric_keypad)
directional_shortest_path = KeypadAStar(directional_keypad)

numerical_sequences_between = partial(
    sequences_between, numeric_shortest_path, numeric_keypad
)
directional_sequences_between = partial(
    sequences_between, directional_shortest_path, directional_keypad
)


def shortest_directional_seq_between(start, stop, times):
    dir_sequences = directional_sequences_between(start, stop)
    if times == 1:
        return min(dir_sequences, key=len)
    else:
        return min(
            [
                shortest_seq_for_code(shortest_directional_seq_between, seq, times - 1)
                for seq in dir_sequences
            ],
            key=len,
        )


def shortest_numeric_seq_between(start, stop, times):
    num_sequences = numerical_sequences_between(start, stop)
    return min(
        [
            shortest_seq_for_code(shortest_directional_seq_between, seq, times)
            for seq in num_sequences
        ],
        key=len,
    )


part_one(
    sum(
        [
            int(code[:-1])
            * len(shortest_seq_for_code(shortest_numeric_seq_between, code, 2))
            for code in codes
        ]
    )
)

# Part 2


def len_shortest_seq_for_code(len_shortest_seq_between, code, *args):
    l = 0
    for start, stop in pairwise("A" + code):
        l += len_shortest_seq_between(start, stop, *args)
    return l


@cache
def len_shortest_directional_seq_between(start, stop, times):
    dir_sequences = directional_sequences_between(start, stop)
    if times == 1:
        return min(len(s) for s in dir_sequences)
    else:
        return min(
            len_shortest_seq_for_code(
                len_shortest_directional_seq_between, seq, times - 1
            )
            for seq in dir_sequences
        )


@cache
def len_shortest_numeric_seq_between(start, stop, times):
    num_sequences = numerical_sequences_between(start, stop)
    return min(
        len_shortest_seq_for_code(len_shortest_directional_seq_between, seq, times)
        for seq in num_sequences
    )


part_two(
    sum(
        [
            int(code[:-1])
            * len_shortest_seq_for_code(len_shortest_numeric_seq_between, code, 25)
            for code in codes
        ]
    )
)
