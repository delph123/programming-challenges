from libs import *

# Parse input

matcher = create_matcher([(r"{str} \({int}\)(?: -> {str*})?", (0, 1, 2))])

programs = [matcher(l) for l in read_lines("example")]
programs = {p: (w, l.split(", ") if l else []) for p, w, l in programs}

# Part 1


def bottom(program):
    for p, (_, standing) in programs.items():
        if program in standing:
            return bottom(p)
    return program


part_one(bottom(next(iter(programs.keys()))))

# Part 2


def balance(tree):
    w, standing = programs[tree]
    weights = []
    corrections = []
    for t in standing:
        wt, tcorr = balance(t)
        weights.append(wt)
        corrections.extend(tcorr)
    if weights and not all(w == weights[0] for w in weights):
        if len(weights) < 3 or weights[0] == weights[1] or weights[0] == weights[2]:
            w0 = weights[0]
        else:
            w0 = weights[1]
        n = next(i for i in range(len(weights)) if weights[i] != w0)
        return w + len(weights) * w0, corrections + [
            (standing[n], programs[standing[n]][0] - weights[n] + w0)
        ]
    return w + sum(weights), corrections


part_two(balance(bottom(next(iter(programs.keys()))))[1][0][1])
