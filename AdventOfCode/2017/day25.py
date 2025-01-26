from libs import *

# Parse input

HEADER = """
Begin in state {str}.
Perform a diagnostic checksum after {int} steps.
"""

STATE = """
In state {str}:
  If the current value is {int}:
    - Write the value {int}.
    - Move one slot to the {str}.
    - Continue with state {str}.
  If the current value is {int}:
    - Write the value {int}.
    - Move one slot to the {str}.
    - Continue with state {str}.
"""

matcher = create_matcher(
    [
        (HEADER.strip().replace("\n", "/"), (0, 1)),
        (STATE.strip().replace("\n", "/"), (0, [(1, (2, 3, 4)), (5, (6, 7, 8))])),
    ]
)

blueprint = [matcher(l.replace("\n", "/")) for l in read("example").split("\n\n")]

starting_state, diagnostic_steps = blueprint[0]
states = {
    s: {v: (v0, 1 if d0 == "right" else -1, s0) for (v, (v0, d0, s0)) in cond}
    for s, cond in blueprint[1:]
}

# Part 1


def run_turing_machine(tape_size):
    tape = [0] * tape_size
    cursor = len(tape) // 2
    state = starting_state
    for _ in range(diagnostic_steps):
        if cursor == 0:
            cursor += len(tape)
            tape = [0] * len(tape) + tape
        if cursor == len(tape) - 1:
            tape.extend([0] * len(tape))
        (v, d, s) = states[state][tape[cursor]]
        tape[cursor] = v
        cursor += d
        state = s
    return tape.count(1)


part_one(run_turing_machine(1000))
