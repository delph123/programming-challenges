from libs import *

# Parse input

ip_addresses = read_lines("example")

# Part 1


def parse_ip_address(addr):
    parts = re.findall(r"([^\[\]]+)(?:\[([^\[\]]+)\])?", addr)
    supernet, hypernet = transpose(parts)
    return (supernet, hypernet[:-1])


def has_abba(addr):
    return any(
        addr[n] == addr[n + 3] and addr[n + 1] == addr[n + 2] and addr[n] != addr[n + 1]
        for n in range(len(addr) - 3)
    )


def supports_tls(addr):
    supernet, hypernet = parse_ip_address(addr)
    return any(has_abba(i) for i in supernet) and all(not has_abba(o) for o in hypernet)


part_one(len([addr for addr in ip_addresses if supports_tls(addr)]))

# Part 2


def aba_sequences(addr_parts):
    return set(
        flatten(
            [
                addr[i : i + 3]
                for i in range(len(addr) - 2)
                if addr[i] == addr[i + 2] and addr[i] != addr[i + 1]
            ]
            for addr in addr_parts
        )
    )


def contains_bab(addr_parts, aba_seq):
    bab_seq = aba_seq[1:] + aba_seq[1]
    return any(bab_seq in addr for addr in addr_parts)


def supports_ssl(addr):
    supernet, hypernet = parse_ip_address(addr)
    abas = aba_sequences(supernet)
    return any(contains_bab(hypernet, aba) for aba in abas)


part_two(len([addr for addr in ip_addresses if supports_ssl(addr)]))
