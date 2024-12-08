import sys
import inspect
from pathlib import Path
from ..tools import Grid


def read(version):
    # Read file name from calling file (using the caller's stack frame)
    frame = inspect.currentframe().f_back
    while "__file__" not in frame.f_locals:
        frame = frame.f_back
    calling_path = Path(frame.f_locals["__file__"])

    # Parse file path to detect day & year
    year = int(calling_path.parts[-2])
    day = int(calling_path.stem[3:])

    print(f"\x1b[30;33m--- Advent of Code {year} - Day {day} ---\x1b[0m")

    if len(sys.argv) >= 2 and sys.argv[1]:
        print("\x1b[30;43m INFO \x1b[0m Reading from", sys.argv[1])
        input_file = sys.argv[1]
    elif version.startswith("e"):
        print("\x1b[30;41m /!\\ \x1b[0m Reading from example")
        input_file = (
            calling_path.parent / "examples" / calling_path.with_suffix(".in").name
        )
    else:
        input_file = (
            calling_path.parent / "inputs" / calling_path.with_suffix(".in").name
        )

    return open(input_file).read().rstrip()


def read_lines(version):
    return read(version).split("\n")


def read_grid(version):
    return Grid([list(r) for r in read_lines(version)])
