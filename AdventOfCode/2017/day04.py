from libs import *

# Parse input

passphrases = read_lines("example")

cut = passphrases.index("") if read.from_example else len(passphrases)
cut_p2 = cut + 1 if read.from_example else 0

# Part 1


def valid(passphrase):
    words = passphrase.split(" ")
    return len(words) == len(set(words))


part_one(sum([valid(phrase) for phrase in passphrases[:cut]]))

# Part 2


def valid_p2(passphrase):
    words = ["".join(sorted(word)) for word in passphrase.split(" ")]
    return len(words) == len(set(words))


part_two(sum([valid_p2(phrase) for phrase in passphrases[cut_p2:]]))
