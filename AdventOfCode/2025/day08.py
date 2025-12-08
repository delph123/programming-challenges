from libs import *

# Parse input

box_positions = [tuple(int(n) for n in b.split(",")) for b in read_lines("i")]

times_p1 = 10 if read.from_example else 1000
times_p2 = -1

# Part 1


def squared_distance(edge):
    (x, y, z), (t, u, v) = edge
    return (t - x) ** 2 + (u - y) ** 2 + (v - z) ** 2


def edges(nodes):
    return [(p, q) for i, p in enumerate(nodes) for q in nodes[i + 1 :]]


def connect_short_distance(box_positions, times):
    boxes = {b: {b} for b in box_positions}
    for t, (s, e) in enumerate(sorted(edges(box_positions), key=squared_distance)):
        if t == times:
            # For part 1, stop when we explored the required number of connections
            break
        if boxes[s] != boxes[e]:
            bt = boxes[s] | boxes[e]
            for b in bt:
                boxes[b] = bt
        if times == times_p2 and len(boxes[s]) == len(box_positions):
            # For part 2, stop when we have connected all boxes (and return last connection)
            return (s, e)
    return {tuple(s) for s in boxes.values()}


circuits = connect_short_distance(box_positions, times_p1)
part_one(prod(sorted(len(b) for b in circuits)[-3:]))

# Part 2

last_connection = connect_short_distance(box_positions, times_p2)
part_two(last_connection[0][0] * last_connection[1][0])
