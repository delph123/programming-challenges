from libs import *

# Parse input

distances = [
    (l.split(" = ")[0].split(" to "), int(l.split(" = ")[1]))
    for l in read("example").split("\n")
]

distances = {(a, b): d for [a, b], d in distances} | {
    (b, a): d for [a, b], d in distances
}


def graph():
    vertices = set(flatten([list(e) for e in distances.keys()]))
    return {
        n1: {n2: distances[(n1, n2)] for n2 in vertices if n2 != n1} for n1 in vertices
    }


G = graph()
MAX = len(G) * max(distances.values()) + 1


# Part 1


def shortest_dist(start, excl):
    dist = MAX
    for n, d in G[start].items():
        if n in excl:
            continue
        dist = min(dist, d + shortest_dist(n, excl | {n}))
    return dist if dist < MAX else 0


part_one(min(shortest_dist(city, {city}) for city in G.keys()))

# Part 2


def longest_dist(start, excl):
    dist = 0
    for n, d in G[start].items():
        if n in excl:
            continue
        dist = max(dist, d + longest_dist(n, excl | {n}))
    return dist


part_two(max(longest_dist(city, {city}) for city in G.keys()))
