from libs import *

# Parse input

number_of_elves = int(read("example"))

# Part 1


@dataclass
class Elf:
    num: int
    left: "Elf" = None


# Generate a linked list of elves and connect
# the last elf to the first to make a circle.
def gen_elves_circle(size):
    start = prev = Elf(1)
    for i in range(1, size):
        prev.left = Elf(i + 1)
        prev = prev.left
    prev.left = start
    return start


def steal(first_elf: Elf):
    elf = first_elf
    while elf.left != elf:
        elf.left = elf.left.left
        elf = elf.left
    return elf


part_one(steal(gen_elves_circle(number_of_elves)).num)

# Part 2


def steal_p2(size):
    # Generate a simple list containing all elves
    elves = list(range(1, size + 1))
    REMOVED = 0
    # Recursively run the stealing algorithm until there is only one elf,
    # the algorithm will remove half of the elves at each turn.
    while len(elves) > 1:
        current = 0
        size = len(elves)
        # Remove elves that are across the circle for half the elves (until
        # we meet the first removed elf - that was across elf at position 0)
        while elves[current] != REMOVED:
            # The elf across is positioned at index:
            #   across =
            #     current               (position of current elf)
            #     + current             (= number of elves removed until now)
            #     + current_size // 2   (= (size - current) // 2)
            #     modulo size
            elves[(2 * current + (size - current) // 2) % size] = REMOVED
            current += 1
        # After exhausting half the elves, we have lots of gaps all around,
        # we can re-index the list to remove gaps. Re-indexing will happen
        # only log2(initial size) times, which is acceptable.
        elves = list(
            elves[(current + i) % size]
            for i in range(len(elves))
            if elves[(current + i) % size] != REMOVED
        )
    return elves[0]


part_two(steal_p2(number_of_elves))
