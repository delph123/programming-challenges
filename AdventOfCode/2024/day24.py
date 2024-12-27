from libs import *
from operator import xor, and_, or_

# Parse input

inputs, gates = read("example").split("\n\n")
inputs = {i.split(": ")[0]: int(i.split(": ")[1]) for i in inputs.split("\n")}
gates = [g.split(" -> ") for g in gates.split("\n")]
gates = {b: tuple(a.split(" ")) for (a, b) in gates}

# Part 1

operators = {"XOR": xor, "OR": or_, "AND": and_}


def eval(gates, inputs, gate):
    if gate in inputs:
        return inputs[gate]
    a, op, b = gates[gate]
    return operators[op](eval(gates, inputs, a), eval(gates, inputs, b))


def eval_number(gates, inputs, n):
    variables = sorted(list(gates.keys()) + list(inputs.keys()), reverse=True)
    number = [eval(gates, inputs, v) for v in variables if v.startswith(n)]
    return int("".join([str(n) for n in number]), 2)


part_one(eval_number(gates, inputs, "z"))

# Part 2


def swaps(gates, sw_pairs):
    g2 = gates.copy()
    for a, b in sw_pairs:
        g2[a], g2[b] = g2[b], g2[a]
    return g2


def decompose(v, n, l):
    return {f"{v}{i:02}": int(d) for i, d in enumerate(reversed(format(n, f"0{l}b")))}


def add(gates, x, y):
    l = len([v for v in gates.keys() if v.startswith("z")]) - 1
    return eval_number(gates, decompose("x", x, l) | decompose("y", y, l), "z")


def output(gates, instr):
    return next(a for (a, b) in gates.items() if sorted(b) == sorted(instr))


def find_output(gates, fa, fop):
    return next(
        c for (c, (a, op, b)) in gates.items() if fop == op and fa == a or fa == b
    )


# Input file should look like:
#
# x00 ^ y00 = ^00 = z00 -> 1 op
# x00 & y00 = &00 = r00 -> 1 op
# ...
# x21 ^ y21 = ^21
# ^21 ^ r20 = z21       -> (4 * 21 - 1) op
# x21 & y21 = &21
# ^21 & r20 = i21       -> (4 * 21 - 1) op
# i21 | &21 = r21       -> (4 * 21 + 1) op
# ...
# x44 ^ y44 = ^44
# ^44 ^ r43 = z44       -> 175 op
# x44 & y44 = &44
# ^44 & r43 = i44       -> 175 op
# i44 | &44 = z45 = r44 -> 177 op
#
# But 4 pairs of lines have been swapped.


# This is based on some heuristics to find the bad wiring.
# It may or may not work, depending on your data 🤷
# It did work for mine 😁
def identify_bad_wires(gates, i):
    if i == 0:
        # We have:
        #   z(0)    = x(0) ^ y(0)
        # If z(0) is incorrect, we can swap it with x(0) ^ y(0)
        return (f"z{i:02}", output(gates, ("x00", "XOR", "y00")))
    elif i == len([v for v in gates.keys() if v.startswith("z")]) - 1:
        # We have:
        #   z(45)   = r(45)
        #           = and(44) | i(44)
        #   and(44) = x(44) & y(44)
        #   i(44)   = xor(44) & r(43)
        # And we know that xor(44) and r(43) are valid, since z(44) is valid:
        #   z(44)   = xor(44) ^ r(43)
        # And we know and(44) should be ok or it would result in a cycle.
        # Therefore, the only possible swaps are:
        #   z(45) with and(44) -> would result in a cycle
        #   z(45) with i(44) -> would also result in a cycle
        #   and(44) with i(44) -> turns out to be invisible w.r.t. z(45)
        print(f"Impossible swap for z{i}!")
    else:
        # We have:
        #   z(n)     = xor(n) ^ r(n-1)
        #   xor(n)   = x(n) ^ y(n)
        #   r(n-1)   = and(n-1) | i(n-1)
        #   and(n-1) = x(n-1) & y(n-1)
        #   i(n-1)   = xor(n-1) & r(n-2)
        # And we know that xor(n-1), r(n-2) are ok.

        # With np = n-1:
        xor_n = output(gates, (f"x{i:02}", "XOR", f"y{i:02}"))
        and_np = output(gates, (f"x{i-1:02}", "AND", f"y{i-1:02}"))

        # We can assume xor(n) = x(n) ^ y(n) was not swapped with z(n)
        # or it would result in a cycle in the circuit. Same goes for
        # and(n-1) = x(n-1) & y(n-1).

        try:
            z_n = find_output(gates, xor_n, "XOR")
            if z_n == f"z{i:02}":
                try:
                    r_np = find_output(gates, and_np, "OR")
                    if r_np == gates[z_n][0] or r_np == gates[z_n][1]:
                        xor_np = output(gates, (f"x{i-1:02}", "XOR", f"y{i-1:02}"))
                        i_np = find_output(gates, xor_np, "AND")
                        if gates[r_np][0] == and_np:
                            return (i_np, gates[r_np][1])
                        else:
                            return (i_np, gates[r_np][0])
                    else:
                        if gates[z_n][0] == xor_n:
                            return (r_np, gates[z_n][1])
                        else:
                            return (r_np, gates[z_n][0])
                except:
                    # and(n-1) is incorrectly wired, find the correct wire from r(n-1)
                    xor_np = output(gates, (f"x{i-1:02}", "XOR", f"y{i-1:02}"))
                    i_np = find_output(gates, xor_np, "AND")
                    r_np = find_output(gates, i_np, "OR")
                    if gates[r_np][0] == i_np:
                        return (and_np, gates[r_np][1])
                    else:
                        return (and_np, gates[r_np][0])
            else:
                # z(n) is incorrectly wired:
                return (f"z{i:02}", z_n)
        except:
            # xor(n) is incorrectly wired, find the correct wire from z(n)
            a, o, b = gates[f"z{i:02}"]
            if gates[a][1] == "OR":
                return (xor_n, b)
            elif gates[b][1] == "OR":
                return (xor_n, a)
            else:
                print("wired!")


# The idea here is to find the first bit that doesn't work by computing
# 2 ** x + 0 and check that it is actually equal to 2 ** x.
def incorrectly_wired(gates):
    l = len([v for v in gates.keys() if v.startswith("z")]) - 1
    swap_pairs = []
    invalid = True
    while invalid:
        invalid = False
        g2 = swaps(gates, swap_pairs)
        for i in range(l):
            if add(g2, 1 << i, 0) != 1 << i:
                invalid = True
                swap_pairs.append(identify_bad_wires(gates, i))
                break
    return swap_pairs


try:
    part_two(",".join(sorted(flatten(incorrectly_wired(gates)))))
except:
    part_two("Cannot run part two on example data!")
