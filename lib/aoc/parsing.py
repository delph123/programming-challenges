import sys
import inspect
from pathlib import Path
from ..tools import replace_all, multi_replace
from ..grid import Grid


def sanitized(
    text: str, replace: list[str] | None = None, ignore: list[str] | None = None
):
    text = text.rstrip()
    if ignore is not None:
        text = replace_all(ignore, "", text)
    if replace is not None:
        text = multi_replace(replace, text)
    return text


def read(version, replace: list[str] | None = None, ignore: list[str] | None = None):
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

    return sanitized(open(input_file).read(), replace=replace, ignore=ignore)


def read_lines(
    version, replace: list[str] | None = None, ignore: list[str] | None = None
):
    return read(version, replace=replace, ignore=ignore).splitlines()


def read_grid(version, cell_format=str):
    return Grid([[cell_format(c) for c in row] for row in read_lines(version)])
