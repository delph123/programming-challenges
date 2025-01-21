from operator import *


def tryint(n):
    try:
        return int(n)
    except:
        return n


def value(registers, v):
    if isinstance(v, str):
        return registers[v]
    else:
        return v


def iset(_, b):
    return b
