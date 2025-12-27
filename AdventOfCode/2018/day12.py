from libs import *

# Parse input

initial_state, spread_rules = read("example").split("\n\n")

initial_state = initial_state[15:]

spread_rules = [l.split(" => ") for l in spread_rules.splitlines()]
spread_rules = defaultdict(lambda: ".", spread_rules)

# Part 1


def spread(current):
    state, offset = current
    # Extend (because we need 5 pots for spread computation)
    state = "...." + state + "...."
    # Spread according to rules
    s = "".join(spread_rules[state[i - 2 : i + 3]] for i in range(2, len(state) - 2))
    # Return a canonical version (between first & last #)
    return (s[s.index("#") : len(s) - s[::-1].index("#")], offset + s.index("#") - 2)


def pots(current):
    state, offset = current
    return [i for i, s in enumerate(state, offset) if s == "#"]


part_one(sum(pots(compose(20 * [spread], (initial_state, 0)))))

# Part 2


def generation(initial, gen):
    state, offset = initial, 0
    visited = {}

    for g in range(1, gen + 1):
        state, offset = spread((state, offset))

        if state in visited and (gen - g) % (g - visited[state][0]) == 0:
            visited_gen, visited_offset = visited[state]
            offset_diff = offset - visited_offset
            final_offset = offset + offset_diff * ((gen - g) // (g - visited_gen))
            return (state, final_offset)

        visited[state] = (g, offset)

    return (state, offset)


part_two(sum(pots(generation(initial_state, 50000000000))))
