from hashlib import md5
from libs import *

# Parse input

secret = read("example")

# Part 1


def find_hash(key, nb_zeros):
    start = "0" * nb_zeros
    for i in range(100000000):
        if md5((key + str(i)).encode()).hexdigest().startswith(start):
            return i


part_one(find_hash(secret, 5))

# Part 2

part_two(find_hash(secret, 6))
