# Back recursion for modified Bessel fucntions
from decimal import Decimal

import numpy as np


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


def back_recursion(x, max_order, init=(1, 0)):
    I = np.empty(max_order)  # Initialize a vector of size `max_order`
    I[-2:] = init  # Set the last two values to `init`
    for n in np.flip(orders(max_order))[2:]:  # Orders from `max_order-2` to 1
        I[n - 1] = I[n + 1] + 2 * n / x * I[n]
    return normalize(I)


def back_recursion_precise(x, max_order, init=(Decimal(1.0), Decimal(0.0))):
    I = np.array(list(map(Decimal, orders)))
    I[-2:] = map(Decimal, init)
    for n in np.flip(orders(max_order))[2:]:  # Orders 28-1
        I[n - 1] = I[n + 1] + 2 * n / Decimal(x) * I[n]
    return normalize(I)
