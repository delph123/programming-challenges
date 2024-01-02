from hashlib import md5

# Parse input

secret = open("AdventOfCode/2015/examples/day04.in").read().strip()

# Part 1


def find_hash(key, nb_zeros):
    start = "0" * nb_zeros
    for i in range(100000000):
        if md5((key + str(i)).encode()).hexdigest().startswith(start):
            return i


print("Part 1:", find_hash(secret, 5))

# Part 2

print("Part 2:", find_hash(secret, 6))
