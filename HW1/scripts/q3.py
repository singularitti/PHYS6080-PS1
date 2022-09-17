# Back recursion for modified Bessel functions
import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from src.bessel_functions import back_recursion, errors, max_errors
from src.plotting import figpath


def prepare_data(x, max_order):
    orders = range(1, max_order + 1)
    my = back_recursion(x, max_order)
    exact = np.array([special.iv(order - 1, x) for order in orders])
    return my, exact


def plot_raw(x, max_order):
    orders = range(1, max_order + 1)
    my, exact = prepare_data(x, max_order)
    fig, ax = plt.subplots()
    ax.scatter(orders, my, label="A naïve algorithm")
    ax.scatter(orders, exact, label="Exact values by SciPy")
    ax.set_xlim((1, max_order))
    ax.set_xlabel(r"back recursion steps ($n$)")
    ax.set_ylabel(r"$I_{n}(x=5)$")
    ax.legend(loc="best")
    fig.savefig(figpath("q3_1.pdf"))
    return fig, ax


def plot_errors(x, max_order):
    orders = range(1, max_order + 1)
    fig, ax = plt.subplots()
    ax.scatter(orders, errors(x, max_order, back_recursion))
    ax.set_xlim((1, max_order))
    ax.set_xlabel(r"back recursion steps ($n$)")
    ax.set_ylabel(r"$\Delta = I_{n}(x=5) - I_{n,\textnormal{exact}}(x=5)$")
    fig.savefig(figpath("q3_2.pdf"))
    return fig, ax


def plot_mat_errors(method):
    xmin, xmax, ymin, ymax = 1, 11, 3, 20
    xrange, yrange = list(range(xmin, xmax)), list(range(ymin, ymax))
    mat_errors = max_errors(xrange, yrange, method)
    mat_errors[mat_errors > 1] = 0
    fig, ax = plt.subplots()
    ax.imshow(mat_errors, aspect="equal", origin="lower", extent=[xmin, xmax, ymin, ymax])
    ax.set_xticks(xrange)
    ax.set_yticks(yrange)
    plt.colorbar()
    plt.savefig(figpath("q3_3.pdf"))
    return fig, ax


def main(x, max_order):
    plot_raw(x, max_order)
    plot_errors(x, max_order)
    plot_mat_errors(back_recursion)


if __name__ == "__main__":
    main(5, 10)
