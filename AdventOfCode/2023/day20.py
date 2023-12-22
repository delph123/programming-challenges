from collections import deque

# Parse file

config = [
    (m.strip().split(" -> ")[0], m.strip().split(" -> ")[1].split(", "))
    for m in open("AdventOfCode/2023/inputs/day20.in").read().strip().split("\n")
]

config = {
    (name[1:] if name != "broadcaster" else "broadcaster"): (
        (name[0] if name != "broadcaster" else "b"),
        dest,
    )
    for (name, dest) in config
}

# Part 1


def setup_mod():
    modules = {
        mod: False if typ == "%" else dict() for (mod, (typ, _)) in config.items()
    }
    for mod, (_, destinations) in config.items():
        for d in destinations:
            if config.get(d, ("", []))[0] == "&":
                modules[d][mod] = 0
    return modules


def broadcast(modules):
    q = deque([("button", "broadcaster", 0)])
    low, high = 0, 0
    while q:
        orig, mod, s = q.popleft()
        if s == 0:
            low += 1
        else:
            high += 1
        (t, destinations) = config.get(mod, ("", []))
        if t == "b":
            for d in destinations:
                q.append((mod, d, s))
        elif t == "%" and s == 0:
            modules[mod] = not modules[mod]
            for d in destinations:
                q.append((mod, d, 1 if modules[mod] else 0))
        elif t == "&":
            modules[mod][orig] = s
            sd = 0 if all(v == 1 for v in modules[mod].values()) else 1
            for d in destinations:
                q.append((mod, d, sd))
    return low, high


def cycle(n):
    modules_setup = setup_mod()
    low, high = 0, 0
    for _ in range(n):
        l, h = broadcast(modules_setup)
        low += l
        high += h

    return low * high


print("Part 1:", cycle(1000))

# Part 2


def broadcast_p2(modules, name):
    q = deque([("button", "broadcaster", 0)])
    while q:
        orig, mod, s = q.popleft()
        if mod == name and s == 0:
            return False
        (t, destinations) = config.get(mod, ("", []))
        if t == "b":
            for d in destinations:
                q.append((mod, d, s))
        elif t == "%" and s == 0:
            modules[mod] = not modules[mod]
            for d in destinations:
                q.append((mod, d, 1 if modules[mod] else 0))
        elif t == "&":
            modules[mod][orig] = s
            sd = 0 if all(v == 1 for v in modules[mod].values()) else 1
            for d in destinations:
                q.append((mod, d, sd))
    return True


def cycle_p2(name):
    modules_setup = setup_mod()
    p = 1
    while broadcast_p2(modules_setup, name):
        p += 1
    return p


# Observation: we are searching the moment when all four input modules of dh (that is tr, xm, dr & nh)
# all receive simultaneously a low signal.
# Second observation: all input modules cycles with a period of a prime number, so we can simply multiply
# them together to find the smallest number that will send a high signal to dh (and a low signal to rx)
print("Part 2:", cycle_p2("tr") * cycle_p2("xm") * cycle_p2("dr") * cycle_p2("nh"))
