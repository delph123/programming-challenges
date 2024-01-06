from math import sqrt, floor


def divisors(n):
    divs = [i for i in range(1, floor(sqrt(n)) + 1) if n % i == 0]
    divs.extend(reversed([n // i for i in divs if i * i != n]))
    return divs
