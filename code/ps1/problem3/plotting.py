import imageio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from scipy import special

from plotconfig import figpath
from problem3.bessel_functions import back_recursion, errors, max_errors

__all__ = ["plot_exact", "plot_raw", "plot_errors", "save_plots_gif", "plot_errors_x"]


def prepare_data(x, starting_order):
    orders = range(starting_order + 1)
    my = back_recursion(x, starting_order)
    exact = np.array([special.iv(order, x) for order in orders])
    return my, exact


def plot_exact(starting_order):
    orders = range(starting_order + 1)
    fig, ax = plt.subplots()
    x = np.linspace(1, 10, 100)
    for order in orders:
        ax.plot(x, [special.iv(order, y) for y in x], label=f"$I_{{{order}}}(x)$")
    ax.set_xlim(1, 10)
    ax.set_ylim(0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$I_n(x)$")
    ax.legend(loc="best", ncol=2)
    fig.savefig(figpath("p3_q1_1.pdf"))
    return fig, ax


def plot_raw(x, starting_order):
    my, exact = prepare_data(x, starting_order)
    fig, ax = plt.subplots()
    ax.scatter(range(len(my)), my, label="A naïve algorithm")
    ax.scatter(range(len(exact)), exact, label="Exact values by SciPy")
    ax.set_xlim(0, starting_order)
    ax.set_xlabel("Order of the modified Bessel function ($n$)")
    ax.set_ylabel(f"$I_{{n}}(x={x})$")
    ax.legend(loc="best")
    fig.savefig(figpath("q3_1.pdf"))
    return fig, ax


def plot_errors(x, starting_order, figname="p3_q1_2.pdf"):
    fig, ax = plt.subplots()
    ax.scatter(range(starting_order + 1), errors(x, starting_order))
    ax.set_xlim(0, starting_order)
    # See https://stackoverflow.com/a/34880501/3260253
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Order of the modified Bessel function ($n$)")
    ax.set_ylabel(f"$\Delta = I_{{n}}(x={x}) - I_{{n,\\textnormal{{exact}}}}(x={x})$")
    fig.savefig(figpath(figname))
    return fig, ax


def plot_errors_x(x, starting_order, figname="p3_q1_3.pdf"):
    fig, ax = plt.subplots()
    hsv = plt.get_cmap('hsv')
    for order in range(starting_order, 5, -1):
        ax.scatter(
            range(order + 1), errors(x, order),
            color=hsv(order / starting_order),
            label=f"$N={order}$"
        )
    ax.set_xlim(0, starting_order)
    # See https://stackoverflow.com/a/34880501/3260253
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Order of the modified Bessel function ($n$)")
    ax.set_ylabel(f"$\Delta = I_{{n}}(x={x}) - I_{{n,\\textnormal{{exact}}}}(x={x})$")
    ax.legend(loc="upper right", ncol=4, fontsize=9)
    fig.savefig(figpath(figname))
    return fig, ax


def save_plots_gif(x, ns, figname="errors.gif"):
    filenames = []
    for n in ns:
        filename = f"p3_{x}_{n}.png"
        filenames.append(filename)
        plot_errors(x, n, filename)
    with imageio.get_writer(figpath(figname), mode="I", fps=5) as writer:
        for filename in filenames:
            image = imageio.imread(figpath(filename))
            writer.append_data(image)


def plot_mat_errors():
    xmin, xmax, nmin, nmax = 1, 11, 3, 20
    xs, ns = list(range(xmin, xmax)), list(range(nmin, nmax))
    mat_errors = max_errors(xs, ns)
    mat_errors[mat_errors > 1] = 0
    fig, ax = plt.subplots()
    ax.imshow(mat_errors, aspect="equal", origin="lower", extent=[xmin, xmax, nmin, nmax])
    ax.set_xticks(xs)
    ax.set_yticks(ns)
    plt.savefig(figpath("q3_3.pdf"))
    return fig, ax


if __name__ == '__main__':
    for x in range(1, 11):
        save_plots_gif(x, range(5, 35), figname=f"errors_{x}.gif")
