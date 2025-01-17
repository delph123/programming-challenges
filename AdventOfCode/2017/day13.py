from libs import *

# Parse input

firewall = [l.split(": ") for l in read_lines("example")]
firewall = {int(a): int(b) for a, b in firewall}

# Part 1


def caught(d, r):
    return d % (2 * (r - 1)) == 0


def severity(firewall):
    return sum(d * r for d, r in firewall.items() if caught(d, r))


part_one(severity(firewall))

# Part 2


# Brute-force, no smart computation this time
def delay(firewall):
    return next(
        n for n in count() if all(not caught(d + n, r) for d, r in firewall.items())
    )


part_two(delay(firewall))
