from libs import *

# Parse input

list_of_words = read("example").split("\n")

# Part 1

part_one(sum([len(l) - len(eval(l)) for l in list_of_words]))

# Part 2

part_two(sum([2 + l.count('"') + l.count("\\") for l in list_of_words]))
