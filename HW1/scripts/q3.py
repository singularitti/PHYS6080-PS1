# Back recursion for modified Bessel functions
import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from src.bessel_functions import back_recursion
from src.plotting import figpath


def prepare_data(x, max_order):
    orders = range(1, max_order + 1)
    my = back_recursion(x, max_order, (1, 0))
    exact = np.array([special.iv(order - 1, x) for order in orders])
    return my, exact


def plot_raw(x, max_order):
    orders = range(1, max_order + 1)
    my, exact = prepare_data(x, max_order)
    plt.figure()
    plt.scatter(orders, my, label="A naïve algorithm")
    plt.scatter(orders, exact, label="Exact values by SciPy")
    plt.xlim((1, max_order))
    plt.xlabel(r"back recursion steps ($n$)")
    plt.ylabel(r"$I_{n}(x=5)$")
    plt.legend(loc="best")
    plt.savefig(figpath("q3_1.pdf"))


def plot_diff(x, max_order):
    orders = range(1, max_order + 1)
    my, exact = prepare_data(x, max_order)
    plt.figure()
    plt.scatter(orders, my - exact)
    plt.xlim((1, max_order))
    plt.xlabel(r"back recursion steps ($n$)")
    plt.ylabel(r"$\Delta = I_{n}(x=5) - I_{n,\textnormal{exact}}(x=5)$")
    plt.savefig(figpath("q3_2.pdf"))


def main(x, max_order):
    plot_raw(x, max_order)
    plot_diff(x, max_order)


if __name__ == "__main__":
    main(5, 10)
