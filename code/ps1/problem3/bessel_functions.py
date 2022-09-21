# Back recursion for modified Bessel functions
from decimal import Decimal

import numpy as np
from scipy import special

__all__ = ['back_recursion', 'back_recursion_precise',
           'errors', 'max_errors', 'find_minimum_order']


def coeff(order):
    if order == 0:
        return 1
    elif order % 4 == 0:
        return 2
    elif order % 2 == 0:
        return -2
    else:  # Odd orders
        return 0


def normalize(bessel_functions):
    coeffs = np.vectorize(coeff)(range(len(bessel_functions)))
    # Calculate $s = \sum_i \bm{c}_i \bm{I}_i(x)$
    scaling_factor = np.dot(coeffs, bessel_functions)
    return bessel_functions / scaling_factor  # Divide all values in $\bm{I}$ by $s$


def back_recursion(x, starting_order):
    orders = range(starting_order + 1)
    I = np.empty(starting_order + 1)  # Orders from 0 to `starting_order`
    I[-2:] = 1, 0  # Set the last two values
    for n in reversed(orders[:-2]):  # Orders from `starting_order-2` to 0
        I[n] = I[n + 2] + 2 * (n + 1) / x * I[n + 1]
    return normalize(I)


def back_recursion_precise(x, starting_order):
    orders = range(starting_order + 1)
    I = np.fromiter(map(Decimal, orders), Decimal)
    I[-2:] = Decimal(1), Decimal(0)
    for n in reversed(orders[:-2]):  # Orders from `starting_order-2` to 0
        I[n] = I[n + 2] + Decimal(2) * (n + 1) / Decimal(x) * I[n + 1]
    return normalize(I)


def errors(x, starting_order):
    I = back_recursion(x, starting_order)
    I_exact = np.array([special.iv(order, x) for order in range(starting_order + 1)])
    return abs(I - I_exact)


def max_errors(xs, ns):
    return np.array([[errors(x, n).max() for x in xs] for n in ns])


def find_minimum_order(xs, ns):
    error_matrix = max_errors(xs, ns)
    for (i, row) in enumerate(error_matrix):
        if all(row < 1e-6):
            return ns[i]


if __name__ == '__main__':
    n = find_minimum_order(range(1, 11), range(3, 40))
