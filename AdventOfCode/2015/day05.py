from libs import *

# Parse input

strings = read("example").split("\n")

# Part 1


def nice(string):
    return (
        sum([string.count(vowel) for vowel in "aeiou"]) >= 3
        and any(string[i] == string[i + 1] for i in range(len(string) - 1))
        and not any(gr in string for gr in ["ab", "cd", "pq", "xy"])
    )


part_one(sum(1 for s in strings if nice(s)))

# Part 2


def nice_p2(string):
    return any(
        string[i : i + 2] in string[i + 2 :] for i in range(len(string) - 3)
    ) and any(string[i] == string[i + 2] for i in range(len(string) - 2))


part_two(sum(1 for s in strings if nice_p2(s)))
