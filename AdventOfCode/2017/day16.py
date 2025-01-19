from libs import *

# Parse input

dance_moves = [(l[0], tuple(l[1:].split("/"))) for l in read("example").split(",")]
dance_moves = [
    (op, params if op == "p" else tuple(int(n) for n in params))
    for op, params in dance_moves
]

programs = "abcde" if read.from_example else "abcdefghijklmnop"

# Part 1


def dance(moves, programs):
    for op, params in moves:
        match op:
            case "s":
                (x,) = params
                programs = programs[-x:] + programs[:-x]
            case "x":
                (a, b) = params
                programs[a], programs[b] = programs[b], programs[a]
            case "p":
                (x, y) = params
                a, b = programs.index(x), programs.index(y)
                programs[a], programs[b] = programs[b], programs[a]
    return programs


part_one(dance(dance_moves, list(programs)), sep="")

# Part 2


def compose_dance(dance_moves, programs, times):
    # Eventually, the dance positions should cycle, let's compute the
    # period of this cycle and register all possible dance positions
    positions = {}
    t = 0
    program_key = "".join(programs)
    while program_key not in positions:
        positions[program_key] = t
        programs = dance(dance_moves, programs)
        t += 1
        program_key = "".join(programs)
    # Now we can compute the position after times dances
    return reversed_mapping(positions)[times % len(positions)]


part_two(compose_dance(dance_moves, list(programs), 1_000_000_000))
