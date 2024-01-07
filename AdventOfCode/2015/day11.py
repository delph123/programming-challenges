from libs import *

# Parse input

password = read("example")

# Part 1


def acceptable(pw):
    return (
        any(
            pw[i + 1] == pw[i] + 1 and pw[i + 2] == pw[i] + 2
            for i in range(len(pw) - 2)
        )
        and all(ord(l) - ord("a") not in pw for l in "iol")
        and any(
            pw[i + 1] == pw[i]
            and any(
                pw[j + 1] == pw[j] and pw[j] != pw[i] for j in range(i + 2, len(pw) - 1)
            )
            for i in range(len(pw) - 1)
        )
    )


def conv(pw):
    return [ord(l) - ord("a") for l in pw]


def inc(pw):
    i = len(pw) - 1
    while i >= 0:
        pw[i] += 1
        if pw[i] == 26:
            pw[i] = 0
            i -= 1
        else:
            return pw


def next(pw):
    pw = inc(conv(pw))
    while not acceptable(pw):
        pw = inc(pw)
    return "".join([chr(l + ord("a")) for l in pw])


part_one(next(password))

# Part 2

part_two(next(next(password)))
