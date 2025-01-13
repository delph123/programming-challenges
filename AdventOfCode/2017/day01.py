from libs import *

# Parse input

digits_sequences = [[int(n) for n in l] for l in read_lines("example")]

# Part 1


def captcha(seq):
    return sum([p for (p, q) in pairwise(seq + [seq[0]]) if p == q])


part_one([captcha(d) for d in digits_sequences[:4]])

# Part 2


def captcha_p2(seq):
    l = len(seq)
    return sum([d for i, d in enumerate(seq) if d == seq[(i + l // 2) % l]])


part_two([captcha_p2(d) for d in digits_sequences[-5:]])
