from math import sqrt, floor


def divisors(n):
    divs = [i for i in range(1, floor(sqrt(n)) + 1) if n % i == 0]
    divs.extend(reversed([n // i for i in divs if i * i != n]))
    return divs


def solve_integer_linear_eq(a, b):
    """
    Solve a linear equation with coefficients and solutions all
    being integer values.

    The equation has the form: ax + b = 0

    The solution is returned as a list with 0 or 1 value.
    None is returned when a = b = 0
    """

    if a == 0 and b == 0:
        # any x is a solution, return None as special value
        return None
    elif a == 0:
        # b = 0 has no solution for b != 0
        return []

    # Check that the solution is an integer
    if b % a == 0:
        return [-b // a]
    else:
        return []


def solve_integer_quadratic_eq(a, b, c):
    """
    Solve a quadratic equation with coefficients and solutions all
    being integer values.

    The equation has the form: ax² + bx + c = 0

    The solutions are returned as a list with 0, 1 or 2 value(s).
    None is returned when a = b = c = 0
    """

    # The solutions for a general quadratic equation are:
    #   s = ( -b ± sqrt(delta) ) / 2a
    # Where the discriminant is defined as:
    #   delta = b^2 - 4ac
    #
    # To be acceptable, following conditions must hold true:
    #   delta >= 0
    #   s is an integer

    if a == 0:
        return solve_integer_linear_eq(b, c)

    delta = b**2 - 4 * a * c

    if delta == 0 and b % (2 * a) == 0:
        return [-b // (2 * a)]

    if delta <= 0 or int(sqrt(delta)) ** 2 != delta:
        return []

    sqrt_delta = int(sqrt(delta))
    solutions = []
    if (b + sqrt_delta) % (2 * a) == 0:
        solutions.append((-b - sqrt_delta) // (2 * a))
    if (b - sqrt_delta) % (2 * a) == 0:
        solutions.append((-b + sqrt_delta) // (2 * a))
    return solutions
