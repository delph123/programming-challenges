from libs import *

# Parse input

pipes = [l.split(" <-> ") for l in read_lines("example")]

pipes_graph = Graph({int(a): set(int(d) for d in b.split(", ")) for a, b in pipes})

# Part 1

part_one(len(pipes_graph.accessible_from(0)))

# Part 2

part_two(len(pipes_graph.groups()))
