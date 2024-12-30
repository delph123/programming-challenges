from libs import *

# Parse input

compressed = read_lines("example", ignore=[" "])

# Part 1


def decompressed(seq):
    pattern = re.compile(r"\((\d+)x(\d+)\)")
    out = ""
    n = 0
    m = pattern.search(seq, n)
    while m is not None:
        length, times = (int(m.group(1)), int(m.group(2)))
        out += seq[n : m.start()] + seq[m.end() : m.end() + length] * times
        n = m.end() + length
        m = pattern.search(seq, n)
    out += seq[n:]
    return out


part_one([len(decompressed(l)) for l in compressed])

# Part 2


def len_decompressed(seq):
    pattern = re.compile(r"\((\d+)x(\d+)\)")
    total_length = 0
    n = 0
    m = pattern.search(seq, n)
    while m is not None:
        length, times = (int(m.group(1)), int(m.group(2)))
        total_length += m.start() - n
        total_length += times * len_decompressed(seq[m.end() : m.end() + length])
        n = m.end() + length
        m = pattern.search(seq, n)
    total_length += len(seq) - n
    return total_length


part_two([len_decompressed(l) for l in compressed])
