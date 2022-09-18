# Back recursion for modified Bessel functions
from decimal import Decimal

import numpy as np
from scipy import special

__all__ = ['back_recursion', 'back_recursion_precise',
           'errors', 'max_errors', 'minimum_steps']


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


def back_recursion(x, last_order):
    orders = range(last_order + 1)
    I = np.empty(last_order + 1)  # Orders from 0 to `last_order`
    I[-2:] = 1, 0  # Set the last two values
    for n in np.flip(orders)[2:]:  # Orders from `last_order-2` to 0
        I[n] = I[n + 2] + 2 * (n + 1) / x * I[n + 1]
    return normalize(I)


def back_recursion_precise(x, last_order):
    orders = range(last_order + 1)
    I = np.fromiter(map(Decimal, orders), Decimal)
    I[-2:] = Decimal(1), Decimal(0)
    for n in np.flip(orders)[2:]:  # Orders from `last_order-2` to 0
        I[n] = I[n + 2] + 2 * (n + 1) / Decimal(x) * I[n + 1]
    return normalize(I)


def errors(x, last_order, method=back_recursion):
    I = method(x, last_order)
    I_exact = np.array([special.iv(order, x) for order in range(last_order + 1)])
    return abs(I - I_exact)


def max_errors(xrange, order_range, method):
    return np.array([[errors(x, last_order, method).max() for x in xrange] for last_order in order_range])


def minimum_steps(xrange, order_range, method):
    error_matrix = max_errors(xrange, order_range, method)
    for (i, row) in enumerate(error_matrix):
        if all(row < 1e-6):
            return order_range[i]
