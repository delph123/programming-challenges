import inspect
from pathlib import Path


def read(version):
    # Read file name from calling file (using the caller's stack frame)
    calling_path = Path(inspect.currentframe().f_back.f_locals["__file__"])
    year = int(calling_path.parts[-2])
    day = int(calling_path.stem[3:])

    print(f"\x1b[30;33m--- Advent of Code {year} - Day {day} ---\x1b[0m")

    if (
        version == "e"
        or version == "ex"
        or version == "example"
        or version == "examples"
    ):
        print("\x1b[30;41m /!\ \x1b[0m Reading from example")
        directory = "examples"
    elif version == "i" or version == "in" or version == "input" or version == "inputs":
        directory = "inputs"
    else:
        print("/!\ Wrong file version specified, reading from input")
        directory = "inputs"

    return (
        open(calling_path.parent / directory / calling_path.with_suffix(".in").name)
        .read()
        .strip()
    )
