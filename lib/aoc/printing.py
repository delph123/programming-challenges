from itertools import islice, tee
from ..tools import is_iterable
from ..grid import Grid, Point


def preview(result):
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}:", value)
    elif isinstance(result, Grid):
        preview(result.content)
    elif is_iterable(result):
        for line in result:
            if isinstance(line, (list, set)):
                if (
                    len(line) > 10
                    or len(line) > 5
                    and isinstance(next(iter(line)), str)
                    and all(len(c) == 1 for c in line)
                ):
                    print("".join([str(l) for l in line]))
                else:
                    print(line)
            else:
                print(line)
    else:
        print(result)


def print_error(text):
    print("\x1b[1;31m" + text + "\x1b[0m")


def print_result(result, part: int, sep=None):
    print(f"\x1b[30;{36 if part == 1 else 32}mPart {part}:\x1b[0m ", end="")
    if sep is not None:
        print(*result, sep=sep)
    elif isinstance(result, (bool, str, int, float, complex, Point)):
        print(result)
    elif is_iterable(result):
        l = list(islice(result, 6))
        if len(l) == 1:
            print(l[0])
        elif len(l) < 6:
            print(result)
        else:
            print("")
            preview(result)
    else:
        print(result)


def part_one(result, sep=None):
    print_result(result, part=1, sep=sep)


def part_two(result, sep=None):
    print_result(result, part=2, sep=sep)
