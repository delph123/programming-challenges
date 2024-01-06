def preview(result):
    if isinstance(result, (list, set)):
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
    elif isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}:", value)
    else:
        print(result)


def print_result(result, part: int):
    if isinstance(result, (str, int)):
        print(f"\x1b[30;{36 if part == 1 else 32}mPart {part}:\x1b[0m", result)
    else:
        print(f"\x1b[30;{36 if part == 1 else 32}mPart {part}:\x1b[0m")
        preview(result)


def part_one(result):
    print_result(result, part=1)


def part_two(result):
    print_result(result, part=2)
