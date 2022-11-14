import matplotlib.pyplot as plt
import numpy as np

from plotconfig import figpath
from problem2.timing import time_mul


def plot():
    standard, rounded, truncated = [], [], []
    N = np.linspace(10, 1000, dtype=int)
    for n in N:
        t1, t2, t3 = time_mul(n, 1000)
        standard.append(t1 / 1000)
        rounded.append(t2 / 1000)
        truncated.append(t3 / 1000)
    fig, ax = plt.subplots()
    ax.scatter(N, standard, label="standard")
    ax.scatter(N, rounded, label="rounded")
    ax.scatter(N, truncated, label="truncated")
    ax.set_xlim(min(N), max(N))
    ax.set_ylim(0)
    ax.set_xlabel("Numbers of multiplications ($n$)")
    ax.set_ylabel("Time per loop ($t$)")
    ax.legend(loc="best")
    fig.savefig(figpath("p2_q3.pdf"))
    return fig, ax


if __name__ == '__main__':
    plot()
