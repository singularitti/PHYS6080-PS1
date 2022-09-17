# Back recursion for modified Bessel fucntions
from decimal import getcontext

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from src.back_recursion import back_recursion

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


if __name__ == "__main__":
    max_order = 30
    orders = range(1, max_order + 1)
    x = 5

    I = back_recursion(x, max_order, (1, 0))
    I_exact = np.array([special.iv(order - 1, x) for order in orders])

    plt.scatter(orders, I, label="A naïve algorithm")
    plt.scatter(orders, I_exact, label="Exact values by SciPy")
    plt.xlim((1, max_order))
    plt.xlabel(r"back recursion steps ($n$)")
    plt.ylabel(r"$I_{n}(x=5)$")
    plt.legend(loc="best")
    plt.savefig("../images/q3_1.pdf")

    plt.figure()
    plt.scatter(orders, I - I_exact)
    plt.xlim((1, max_order))
    plt.xlabel(r"back recursion steps ($n$)")
    plt.ylabel(r"$\Delta = I_{n}(x=5) - I_{n,\textnormal{exact}}(x=5)$")
    plt.savefig("../images/q3_2.pdf")
