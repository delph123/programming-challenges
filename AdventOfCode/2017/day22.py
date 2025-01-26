from libs import *

# Parse input

cluster_nodes = read_grid("example")

# Part 1


def virus_positions(g):
    return set(p for p, v in g.items() if v == "#")


def infect(g, bursts):
    current = Point(len(cluster_nodes.rows()) // 2, len(cluster_nodes.rows()[0]) // 2)
    direction = Point.UDLR["^"]
    viruses = virus_positions(g)
    infections = 0
    for _ in range(bursts):
        if current in viruses:
            direction = direction.rotate(90)
            viruses.remove(current)
            current += direction
        else:
            direction = direction.rotate(-90)
            viruses.add(current)
            current += direction
            infections += 1
    return infections


part_one(infect(cluster_nodes, 10000))

# Part 2


def infect_p2(g, bursts):
    current = Point(len(cluster_nodes.rows()) // 2, len(cluster_nodes.rows()[0]) // 2)
    direction = Point.UDLR["^"]
    viruses = {p: "#" for p in virus_positions(g)}
    infections = 0
    for _ in range(bursts):
        if current not in viruses:
            direction = direction.rotate(-90)
            viruses[current] = "W"
            current += direction
        elif viruses[current] == "#":
            direction = direction.rotate(90)
            viruses[current] = "F"
            current += direction
        elif viruses[current] == "F":
            direction = direction.rotate(180)
            del viruses[current]
            current += direction
        elif viruses[current] == "W":
            viruses[current] = "#"
            current += direction
            infections += 1
    return infections


part_two(infect_p2(cluster_nodes, 10000000))
