# Parse input


def replacement_dict():
    rp = {f: [] for f in set(f for f, _ in replacements)}
    for f, t in replacements:
        rp[f].append(t)
    return rp


replacements, medicine = (
    open("AdventOfCode/2015/examples/day19.in").read().strip().split("\n\n")
)

replacements = [l.split(" => ") for l in replacements.strip().split("\n")]
replacements = replacement_dict()


# Part 1


def replace(mol):
    i = 0
    molecules = []
    while i < len(mol):
        j = 0
        if mol[i : i + 1] in replacements:
            j = 1
        elif mol[i : i + 2] in replacements:
            j = 2
        if j > 0:
            for r in replacements[mol[i : i + j]]:
                mm = list(mol)
                mm[i : i + j] = r
                molecules.append("".join(mm))
        i += j if j > 0 else 1
    return set(molecules)


print("Part 1:", len(replace(medicine)))

# Part 2


# Greedily destructuring  the molecule seems to work - most of the times.
# When it doesn't it will print an error and stop.
def destructure(molecule):
    s = 0
    while molecule != "e":
        p = s
        for reactant, products in replacements.items():
            if any(m for m in products if m in molecule):
                m = next(m for m in products if m in molecule)
                molecule = molecule.replace(m, reactant, 1)
                s += 1
        if p == s:
            print("error - try again")
            return 0
    return s


# print("Part 2:", destructure(medicine))


def template(mol):
    i = 0
    before = ""
    token = []
    while i < len(mol):
        j = 0
        if mol[i : i + 1] in replacements:
            j = 1
        elif mol[i : i + 2] in replacements:
            j = 2
        if j > 0:
            if i == 0 or len(before) > 0:
                token.append(before)
            before = ""
            i += j
        else:
            before += mol[i]
            i += 1
    return token[0], token[1:], before


TEMPLATE = template(medicine)


def match(mol):
    b0, t0, a0 = template(mol)
    b1, t1, a1 = TEMPLATE
    if b0 != "" and b0 != b1:
        return False
    if a0 != "" and a0 != a1:
        return False
    i1 = 0
    for t in t0:
        try:
            i1 = t1.index(t, i1) + 1
        except ValueError:
            return False
    return True


def tokenize(mol):
    i = 0
    before = ""
    token = []
    while i < len(mol):
        j = 0
        if mol[i : i + 1] in replacements:
            j = 1
        elif mol[i : i + 2] in replacements:
            j = 2
        if j > 0:
            token.append((before, mol[i : i + j]))
            before = ""
            i += j
        else:
            before += mol[i]
            i += 1
    return token, before


# The input is created in such a way that each replacement is actually
# replacing one token by two tokens (a token being a molecule that is
# part of the replacement map). There are some molecules that are also
# introduced by the process (like Y, Ar, Rn) that are not token since
# they are not part of the replacement map (they can't be replaced).
# One exception to the above rule is the replacements containing a Y,
# which actually introduce one more token per Y in the string. Another
# exception is the replacements with CRn in them, but there is only one
# such replacement in the whole medicine, and it is cancelled out by
# by the initial token. Therefore, the number of replacements to build
# the medicine must be the number of tokens minus number of 'Y'.
if len(medicine) > 10:
    print("Part 2:", len(tokenize(medicine)[0]) - medicine.count("Y"))


# This won't work for actual input since it generates too many
# replacements to be able to finish in a timely fashion
def fabricate(start, mol):
    molecules = {start}
    visited = {start}
    s = 0
    while mol not in molecules:
        next_molecules = set()
        for m in molecules:
            next_molecules |= replace(m)
        molecules = next_molecules - visited
        molecules = set([m for m in molecules if match(m)])
        visited |= next_molecules
        s += 1
    return s


if len(medicine) < 10:
    print("Part 2:", fabricate("e", medicine))
