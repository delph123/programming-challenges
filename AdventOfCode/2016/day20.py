from libs import *

# Parse input

blocked_ip_ranges = [tuple(int(d) for d in l.split("-")) for l in read_lines("example")]

ip_range = (0, 9) if read.from_example else (0, 4294967295)


# Part 1


def min_authorized_ip(blocked_ranges):
    blocked_ranges = sorted(blocked_ranges)
    min_ip = 0
    for a, b in blocked_ranges:
        if min_ip < a:
            return min_ip
        else:
            min_ip = max(min_ip, b + 1)


part_one(min_authorized_ip(blocked_ip_ranges))

# Part 2


def count_allowed_ip_addresses(ip_range, blocked_ranges):
    min_ip, max_ip = ip_range
    blocked_ranges = sorted(blocked_ranges)
    allowed = 0
    current_ip = min_ip
    for a, b in blocked_ranges:
        if current_ip < a:
            allowed += a - current_ip
            current_ip = b + 1
        else:
            current_ip = max(current_ip, b + 1)
    if current_ip <= max_ip:
        allowed += max_ip - current_ip + 1
    return allowed


part_two(count_allowed_ip_addresses(ip_range, blocked_ip_ranges))
