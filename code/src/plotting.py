import os
from os.path import abspath, join, dirname, exists

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from .bessel_functions import back_recursion, errors, max_errors

__all__ = ["plot_exact", "plot_raw", "plot_errors", "plot_mat_errors"]

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


def plotsdir():
    path = abspath(join(dirname(__file__), "../plots"))
    if not exists(path):
        os.makedirs(path)
    return path


def figpath(figname):
    return join(plotsdir(), figname)


def prepare_data(x, max_order):
    orders = range(1, max_order + 1)
    my = back_recursion(x, max_order)
    exact = np.array([special.iv(order - 1, x) for order in orders])
    return my, exact


def plot_exact(max_order):
    orders = range(1, max_order + 1)
    fig, ax = plt.subplots()
    x = np.linspace(1, 10, 100)
    for order in orders:
        ax.plot(x, [special.iv(order, y) for y in x], label=f"$I_{{{order}}}(x)$")
    ax.set_xlim(1, 10)
    ax.set_ylim(0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$I_n(x)$")
    ax.legend(loc="best")
    fig.savefig(figpath("q3_0.pdf"))
    return fig, ax


def plot_raw(x, max_order):
    orders = range(1, max_order + 1)
    my, exact = prepare_data(x, max_order)
    fig, ax = plt.subplots()
    ax.scatter(orders, my, label="A naïve algorithm")
    ax.scatter(orders, exact, label="Exact values by SciPy")
    ax.set_xlim((1, max_order))
    ax.set_xlabel(r"back recursion steps ($n$)")
    ax.set_ylabel(f"$I_{{n}}(x={x})$")
    ax.legend(loc="best")
    fig.savefig(figpath("q3_1.pdf"))
    return fig, ax


def plot_errors(x, max_order):
    orders = range(1, max_order + 1)
    fig, ax = plt.subplots()
    ax.scatter(orders, errors(x, max_order, back_recursion))
    ax.set_xlim(1, max_order)
    ax.set_xticks(orders)
    ax.set_xlabel(r"back recursion steps ($n$)")
    ax.set_ylabel(f"$\Delta = I_{{n}}(x={x}) - I_{{n,\textnormal{{exact}}}}(x={x})$")
    plt.show()
    # fig.savefig(figpath("q3_2.pdf"))
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
