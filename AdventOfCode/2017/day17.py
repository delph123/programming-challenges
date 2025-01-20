from libs import *

# Parse input

steps = int(read("example"))

# Part 1


def spinlock(n):
    buffer = [0]
    offset = 0
    for i in range(1, n + 1):
        if i % 100000 == 0:
            print(i)
        offset = (offset + steps) % len(buffer) + 1
        buffer.insert(offset, i)
    return buffer


def succeeds(buffer, n):
    offset = buffer.index(n)
    return buffer[offset + 1]


part_one(succeeds(spinlock(2017), 2017))

# Part 2


def spinlock_p2(n):
    # Since 0 is the first value, and all other values are inserted right after it,
    # there is no need to track the entire buffer, only the element that succeeds 0.
    succeeds_0 = None
    offset = 0
    for i in range(1, n + 1):
        offset = (offset + steps) % i + 1
        if offset == 1:
            succeeds_0 = i
    return succeeds_0


# An even quicker version of spinlock_p2 which computes directly the next offset after
# the spinlock algorithm has cycled once the buffer as well as the number of items added
# during the cycle. When the size of the list becomes big, this will provide a great
# speedup in comparison with jumping of steps multiple times until we've reached a full
# cycle
def quick_spinlock_p2(n):
    # For values of n that are less than steps, the computations are not working well,
    # so we simply generate the values from spinlock_p2
    if n <= steps:
        return spinlock_p2(n)
    # Otherwise, we'll generate the first steps of values with spinlock algorithm to
    # initiate the algorithm at a point where it works well
    buffer = spinlock(steps)
    succeeds_0 = buffer[1]
    offset = buffer.index(steps)
    # The size of the buffer (also the next value to insert)
    size = steps + 1
    while size <= n:
        # length of buffer from offset to the end
        l = size - offset
        # new offset after stepping the full size of the buffer
        offset = (steps - (l % steps)) % steps + 1
        # number of elements added during the stepping process
        size += (l - 1) // steps + 1
        # if offset is 1 and we didn't overshoot, we can memorize
        if offset == 1 and size - 1 <= n:
            succeeds_0 = size - 1
    return succeeds_0


part_two(quick_spinlock_p2(50_000_000))
