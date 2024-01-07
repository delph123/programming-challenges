from libs import *

# Parse input

instructions = {
    conn.split(" -> ")[1]: conn.split(" -> ")[0] for conn in read("example").split("\n")
}

# Part 1


def parse(conn: str, get_value):
    if " " not in conn:
        return get_value(conn, get_value)
    if conn.startswith("NOT "):
        return 65536 + ~int(get_value(conn[4:], get_value))
    a, op, b = conn.split(" ")
    va = get_value(a, get_value)
    vb = get_value(b, get_value)
    match op:
        case "AND":
            return va & vb
        case "OR":
            return va | vb
        case "LSHIFT":
            return va << vb
        case "RSHIFT":
            return va >> vb


@cache
def value(label: str, get_value):
    if label.isdecimal():
        return int(label)
    return parse(instructions[label], get_value)


part_one(value("a", value))

# Part 2


def value_p2(label: str, _):
    if label == "b":
        return value("a", value)
    return value(label, value_p2)


part_two(value_p2("a", value_p2))
