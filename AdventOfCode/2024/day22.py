from libs import *

# Parse input

secrets = [int(d) for d in read_lines("example")]
secrets_p2 = [1, 2, 3, 2024] if secrets == [1, 10, 100, 2024] else secrets

modulus = 2**24 - 1

# Part 1


def next_secret(sec):
    sec ^= (sec << 6) & modulus
    sec ^= (sec >> 5) & modulus
    sec ^= (sec << 11) & modulus
    return sec


part_one(sum([compose([next_secret], s, repeat=2000) for s in secrets]))

# Part 2


def sequence_prices(secrets):
    seq = defaultdict(dict)
    for monkey, secret in enumerate(secrets):
        a = next_secret(secret)
        b = next_secret(a)
        last = c = next_secret(b)
        c = (c % 10) - (b % 10)
        b = (b % 10) - (a % 10)
        a = (a % 10) - (secret % 10)
        for _ in range(3, 2000):
            next = next_secret(last)
            d = (next % 10) - (last % 10)
            seq[(a, b, c, d)].setdefault(monkey, next % 10)
            a, b, c, last = b, c, d, next
    return seq


def best_price(seq_map):
    def total_price(monkey_prices):
        return sum(monkey_prices.values())

    return total_price(max(seq_map.values(), key=total_price))


part_two(best_price(sequence_prices(secrets_p2)))
