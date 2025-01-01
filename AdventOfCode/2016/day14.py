from libs import *
from hashlib import md5

# Parse input

salt = read("example")

# Part 1


def is_key(k, next_hashes):
    for i in range(len(k) - 2):
        if k[i] == k[i + 1] and k[i] == k[i + 2]:
            return any((k[i] * 5) in h for h in next_hashes)
    return False


def key(gen_key, n):
    keys = {}
    hashes = [gen_key(i) for i in range(1000)]
    i = 0
    while len(keys) < n:
        hashes.append(gen_key(len(hashes)))
        if is_key(hashes[i], hashes[i + 1 :]):
            keys[i] = hashes[i]
        i += 1
    return keys


def gen_key(i):
    return md5((salt + str(i)).encode()).hexdigest()


part_one(max(key(gen_key, 64).keys()))

# Part 2


def gen_key_p2(i):
    return compose(
        [md5, lambda x: x.hexdigest().encode()], (salt + str(i)).encode(), repeat=2017
    ).decode()


part_two(max(key(gen_key_p2, 64).keys()))
