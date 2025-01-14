from libs import *

# Parse input

jumps_maze = [int(j) for j in read_lines("example")]

# Part 1


def escape(maze):
    pc = 0
    steps = 0
    while 0 <= pc < len(maze):
        maze[pc], pc = (maze[pc] + 1, pc + maze[pc])
        steps += 1
    return steps


part_one(escape(deepcopy(jumps_maze)))

# Part 2


def escape_p2(maze):
    pc = 0
    steps = 0
    while 0 <= pc < len(maze):
        maze[pc], pc = (maze[pc] + (-1 if maze[pc] >= 3 else 1), pc + maze[pc])
        steps += 1
    return steps


part_two(escape_p2(deepcopy(jumps_maze)))
