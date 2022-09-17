# Back recursion for modified Bessel functions
from decimal import Decimal

import numpy as np

__all__ = ['back_recursion', 'back_recursion_precise']


def normalization_coeff(order):
    if order == 0:
        return 1
    elif order % 4 == 0:
        return 2
    elif order % 2 == 0:
        return -2
    else:  # Odd orders
        return 0


def normalize(bessel_functions):
    coeffs = np.vectorize(normalization_coeff)(range(len(bessel_functions)))
    scaling_factor = np.dot(coeffs, bessel_functions)
    return bessel_functions / scaling_factor


def orders(max_order):
    return range(1, max_order + 1)


def back_recursion(x, max_order):
    I = np.empty(max_order)  # Initialize a vector of size `max_order`
    I[-2:] = 1, 0  # Set the last two values to `init`
    for n in np.flip(orders(max_order))[2:]:  # Orders from `max_order-2` to 1
        I[n - 1] = I[n + 1] + 2 * n / x * I[n]
    return normalize(I)


def back_recursion_precise(x, max_order):
    I = np.array(list(map(Decimal, orders(max_order))))
    I[-2:] = Decimal(1.0), Decimal(0.0)
    for n in np.flip(orders(max_order))[2:]:  # Orders from `max_order-2` to 1
        I[n - 1] = I[n + 1] + 2 * n / Decimal(x) * I[n]
    return normalize(I)
