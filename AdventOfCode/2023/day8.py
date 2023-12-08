from math import sqrt, prod

# Parse file

path, graph =  open("AdventOfCode/2023/examples/day8.in").read().split("\n\n")
path = [p for p in path.strip()]
graph = [line.split(" = ") for line in graph.strip().split("\n")]
graph = { f: tuple(lr.strip("()").split(", ")) for [f, lr] in graph }

# Part 1

turn = { 'L': 0, 'R': 1 }

def walk(start, end):
    curr = start
    i = 0
    while curr != end:
        curr = graph[curr][turn[path[i % len(path)]]]
        i += 1

    return i

print("Part 1:", walk('AAA', 'ZZZ'))

# Part 2

def walk_p2(starts, ends):
    curr = starts
    i = 0
    while (curr & ends) != curr:
        curr = set([graph[c][turn[path[i % len(path)]]] for c in curr])
        i += 1

    # The number of steps necessary to reach an end is the same as the number
    # of steps necessary to loop from end to next end. Return the smallest
    # number of steps for one loop
    return i

def nodes_flt(end):
    n = [k for k in graph.keys() if k.endswith(end)]
    return set(n)

starts = nodes_flt("A")
ends = nodes_flt("Z")

# Compute number of steps from each starts separately (because the number of steps
# from all starts at once will be too big!)
steps = [walk_p2({s}, ends) for s in starts]

def factors(n):
    j = 2
    while n > 1:
        for i in range(j, int(sqrt(n+0.05)) + 1):
            if n % i == 0:
                n //= i
                j = i
                yield i
                break
        else:
            if n > 1:
                yield n
                break

# The we basically decompose in prime factors & multiply factors for find the smallest
# number that can be divided by all the numbers in the steps list
print("Part 2:", prod(set(m for n in steps for m in factors(n))))
