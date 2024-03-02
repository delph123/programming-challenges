from libs import *

# Parse input

rooms = [
    (
        room.split("-")[:-1],
        int(room.split("-")[-1].split("[")[0]),
        room.split("-")[-1].split("[")[1][:-1],
    )
    for room in read_lines("e")
]

# Part 1


def checksum(name_parts: list[str]):
    name = "".join(name_parts)
    most_common = Counter(sorted(name)).most_common()[:5]
    return "".join([letter for (letter, _) in most_common])


part_one(
    sum(
        [
            sector
            for (name, sector, control_sum) in rooms
            if checksum(name) == control_sum
        ]
    )
)

# Part 2


def decrypt(name_parts, turns):
    parts = []
    for name in name_parts:
        part = [chr((ord(l) - ord("a") + (turns % 26)) % 26 + ord("a")) for l in name]
        parts.append("".join(part))
    return " ".join(parts)


def find(decrypted_name):
    decrypted_room_names = [
        decrypt(name, sector) if checksum("".join(name)) == control_sum else ""
        for (name, sector, control_sum) in rooms
    ]
    return decrypted_room_names.index(decrypted_name)


part_two(rooms[find("northpole object storage")][1])
