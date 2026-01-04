from libs import *

# Parse input

facility_regex = read("example")

NSWE = {
    "N": Point.UDLR["^"],
    "S": Point.UDLR["v"],
    "W": Point.UDLR["<"],
    "E": Point.UDLR[">"],
}

# Part 1 & 2


def parse_regex(mode, facility_regex, index):
    r = []
    if mode == "(":
        r.append([])
        current = r[-1]
    else:
        current = r
    i = index
    while i < len(facility_regex):
        c = facility_regex[i]
        if c == "(":
            i, sub_regex = parse_regex(c, facility_regex, i + 1)
            current.append(sub_regex)
        elif c == ")":
            break
        elif c == "|":
            r.append([])
            current = r[-1]
        else:
            current.append(c)
        i += 1
    if mode == "(":
        return i, tuple(r)
    else:
        return i, r


def traverse(facility_path, edges: set, origins: set):
    current = origins
    for dir in facility_path:
        if isinstance(dir, str):
            edges |= set((c, c + NSWE[dir]) for c in current)
            current = set(c + NSWE[dir] for c in current)
        else:
            o = current
            current = set()
            for branch in dir:
                current |= traverse(branch, edges, o)
    return current


def facility_map(facility_regex):
    _, path = parse_regex(facility_regex[0], facility_regex[:-1], 1)
    edges = set()
    traverse(path, edges, {Point.ZERO})
    return Graph.from_edges(edges)


rooms_by_distance = facility_map(facility_regex).nodes_by_distance(Point.ZERO)
part_one(len(rooms_by_distance) - 1)
part_two(sum(len(rooms) for rooms in rooms_by_distance[1000:]))
