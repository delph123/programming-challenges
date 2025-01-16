from libs import *
from operator import xor

# Parse input

seq = read_lines("example")
lengths = [int(d) for d in seq[0].split(",")]
numbers = list(range(5 if read.from_example else 256))

# Part 1


def hash(lengths, marks, pos, skip):
    for length in lengths:
        if pos + length > len(marks):
            l0 = (pos + length) % len(marks)
            r = list(reversed(marks[pos:] + marks[:l0]))
            marks[pos:] = r[: len(marks) - pos]
            marks[:l0] = r[len(marks) - pos :]
        else:
            marks[pos : pos + length] = list(reversed(marks[pos : pos + length]))
        pos = (pos + length + skip) % len(marks)
        skip += 1
    return lengths, marks, pos, skip


part_one(prod(hash(lengths, numbers, 0, 0)[1][:2]))

# Part 2


def hash_p2(seq):
    # convert sequence to ascii
    lengths = [ord(s) for s in seq]
    # extend it
    lengths.extend([17, 31, 73, 47, 23])
    # run hash 64 times
    sparse_hash = compose(64 * [hash], lengths, list(range(256)), 0, 0)[1]
    # XOR by groups of 16 blocks
    dense_hash = [reduce(xor, b) for b in batched(sparse_hash, 16)]
    # convert to hexadecimal notation
    return "".join([format(h, "02x") for h in dense_hash])


part_two([hash_p2(s) for s in seq[-4:]])
