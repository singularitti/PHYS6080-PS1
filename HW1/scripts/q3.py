# Back recursion for modified Bessel fucntions
from decimal import Decimal, getcontext

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

params = {
    "legend.fontsize": "x-large",
    "figure.figsize": (8, 5),
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "x-large",
    "ytick.labelsize": "x-large",
    "figure.autolayout": True,
    "text.usetex": True,
}
plt.rcParams.update(params)

getcontext().prec = 50

max_order = 30
orders = range(1, max_order + 1)
x = 5


def coeff(i):
    if i == 0:
        return 1
    elif i % 4 == 0:
        return 2
    elif i % 2 == 0:
        return -2
    else:
        return 0


def normalize(I):
    coeffs = np.vectorize(coeff)(range(len(I)))
    scaling_factor = np.dot(coeffs, I)
    return I / scaling_factor


def back_recursion(x, max_order, init=(1, 0)):
    I = np.empty(max_order)  # Initialize a vector of size `max_order`
    I[-2:] = init  # Set the last two values to `init`
    for v in np.flip(orders)[2:]:  # Orders from `max_order-2` to 1
        I[v - 1] = I[v + 1] + 2 * v / x * I[v]
    return normalize(I)


def back_recursion_precise(x, max_order, init=(Decimal(1.0), Decimal(0.0))):
    orders = range(1, max_order + 1)
    I = np.array(list(map(Decimal, orders)))
    I[-2:] = map(Decimal, init)
    for v in np.flip(orders)[2:]:  # Orders 28-1
        I[v - 1] = I[v + 1] + 2 * v / Decimal(x) * I[v]
    return normalize(I)


I = back_recursion(x, max_order, (1, 0))
I_dec = back_recursion(x, max_order, (Decimal(1.0), Decimal(0.0)))
I_exact = np.array([special.iv(order - 1, x) for order in orders])

plt.plot(orders, I, label="My rough algorithm")
plt.plot(orders, I_dec, label="My rough algorithm with higher precision")
plt.plot(orders, I_exact, label="Exact values")
plt.xlim((1, max_order))
plt.legend(loc="best")

plt.figure()
plt.plot(orders, np.divide(I, I_exact), label="My rough algorithm")
plt.plot(orders, np.divide(I_dec, I_exact),
         label="My rough algorithm with higher precision")
plt.xlim((1, max_order))
plt.legend(loc="best")
# plt.show()
