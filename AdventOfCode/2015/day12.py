import json
from functools import singledispatch
from libs import *

# Parse input

books = json.loads(read("example"))

# Part 1


@singledispatch
def parse(books, excl=None):
    return 0


@parse.register(int)
def parse_int(books, excl=None):
    return books


@parse.register(list)
def parse_list(books, excl=None):
    s = 0
    for v in books:
        s += parse(v, excl)
    return s


@parse.register(dict)
def parse_dict(books, excl=None):
    if excl is not None and excl in books.values():
        return 0
    s = 0
    for k, v in books.items():
        s += parse(k, excl) + parse(v, excl)
    return s


part_one(parse(books))

# Part 2

part_two(parse(books, "red"))
