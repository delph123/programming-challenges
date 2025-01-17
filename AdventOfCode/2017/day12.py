from libs import *

# Parse input

pipes = [l.split(" <-> ") for l in read_lines("example")]
pipes = {int(a): set(int(d) for d in b.split(", ")) for a, b in pipes}

pipe_graph = Graph((a, b) for a, n in pipes.items() for b in n)

# Part 1

part_one(len(pipe_graph.accessible_from(0)))

# Part 2

part_two(len(pipe_graph.groups()))
