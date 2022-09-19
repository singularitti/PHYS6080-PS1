import os
from os.path import abspath, dirname, exists, join

import imageio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from scipy import special

from .bessel_functions import back_recursion, errors, max_errors

__all__ = ["plot_exact", "plot_raw", "plot_errors", "save_plots_gif", "plot_mat_errors"]

params = {
    "figure.figsize": (8, 5),
    "figure.autolayout": True,
    "figure.dpi": 300,
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "x-large",
    "ytick.labelsize": "x-large",
    "legend.fontsize": "x-large",
    "text.usetex": True,
}
plt.rcParams.update(params)


def plotsdir():
    path = abspath(join(dirname(__file__), "..", "..", "tex", "ps1", "plots"))
    if not exists(path):
        os.makedirs(path)
    return path


def figpath(figname):
    return join(plotsdir(), figname)


def prepare_data(x, last_order):
    orders = range(last_order + 1)
    my = back_recursion(x, last_order)
    exact = np.array([special.iv(order, x) for order in orders])
    return my, exact


def plot_exact(last_order):
    orders = range(last_order + 1)
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


def plot_raw(x, last_order):
    my, exact = prepare_data(x, last_order)
    fig, ax = plt.subplots()
    ax.scatter(range(len(my)), my, label="A naïve algorithm")
    ax.scatter(range(len(exact)), exact, label="Exact values by SciPy")
    ax.set_xlim(0, last_order)
    ax.set_xlabel("Order of the modified Bessel function ($n$)")
    ax.set_ylabel(f"$I_{{n}}(x={x})$")
    ax.legend(loc="best")
    fig.savefig(figpath("q3_1.pdf"))
    return fig, ax


def plot_errors(x, last_order, figname="p3_2.pdf"):
    fig, ax = plt.subplots()
    ax.scatter(range(last_order + 1), errors(x, last_order, back_recursion))
    ax.set_xlim(0, last_order)
    # See https://stackoverflow.com/a/34880501/3260253
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Order of the modified Bessel function ($n$)")
    ax.set_ylabel(f"$\Delta = I_{{n}}(x={x}) - I_{{n,\\textnormal{{exact}}}}(x={x})$")
    fig.savefig(figpath(figname))
    return fig, ax


def save_plots_gif(x, ys, figname="errors.gif"):
    filenames = []
    for y in ys:
        filename = f"p3_{x}_{y}.png"
        filenames.append(filename)
        plot_errors(x, y, filename)
    with imageio.get_writer(figpath(figname), mode="I", fps=5) as writer:
        for filename in filenames:
            image = imageio.imread(figpath(filename))
            writer.append_data(image)


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
