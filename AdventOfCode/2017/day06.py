from libs import *

# Parse input

memory_banks = [int(n) for n in read("example").split()]

# Part 1


def redistribute(mem):
    m = max(range(len(mem)), key=lambda x: mem[x])
    blocks = mem[m]
    mem[m] = 0
    for n in range(len(mem)):
        r = (n - m) % len(mem)
        r = len(mem) if r == 0 else r
        mem[n] += ceil(max(0, blocks - r + 1) / len(mem))
    return mem


def detect_cycle(mem):
    seen = set()
    tmem = tuple(mem)
    while tmem not in seen:
        seen.add(tmem)
        mem = redistribute(mem)
        tmem = tuple(mem)
    return len(seen)


# Detect cycle from 0
part_one(detect_cycle(memory_banks))

# Now that memory_bank contains the first element
# of the cycle, detect the cycle period.
part_two(detect_cycle(memory_banks))
