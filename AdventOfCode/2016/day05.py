from libs import *
from hashlib import md5

# Parse input

door_id = read("example")

# Part 1


def password(seed: str):
    pw = ""
    for i in range(100000000):
        if md5((seed + str(i)).encode()).hexdigest().startswith("00000"):
            pw += md5((seed + str(i)).encode()).hexdigest()[5]
            if len(pw) == 8:
                return pw


part_one(password(door_id))

# Part 2


def password_p2(seed: str):
    pw = ["", "", "", "", "", "", "", ""]
    for i in range(100000000):
        if md5((seed + str(i)).encode()).hexdigest().startswith("00000"):
            digest = md5((seed + str(i)).encode()).hexdigest()
            if "0" <= digest[5] <= "7" and pw[int(digest[5])] == "":
                pw[int(digest[5])] = digest[6]
            if all(l != "" for l in pw):
                return "".join(pw)


part_two(password_p2(door_id))
