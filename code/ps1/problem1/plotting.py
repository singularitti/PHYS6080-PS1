import matplotlib.pyplot as plt
import numpy as np

from plotconfig import figpath
from problem1.rounding import averages, deviations, sampling


def prepare_averages(data):
    times = data.index.levels[0][1:]  # Ignore where `n` == 0
    rounded, truncated = np.empty(len(times)), np.empty(len(times))
    for i, n in enumerate(times):
        columns = data.xs((n, "frac diff"))
        rounded[i] = columns["rounded"]
        truncated[i] = columns["truncated"]
    return times, rounded, truncated


def plot_histogram(data):
    df = deviations(data)
    rounded, truncated = df["rounded"], df["truncated"]
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.hist(rounded, 50, label="deviations for rounded")
    ax2.hist(truncated, 50, label="deviations for truncated", color="orange")
    ax1.set_xlim(min(rounded), max(rounded))
    ax1.set_xlabel(r"$\Delta = \frac{ x' - x }{ x }$")
    ax2.set_xlabel(r"$\Delta = \frac{ x' - x }{ x }$")
    ax1.set_ylabel("count")
    ax2.set_xlim(min(truncated), max(truncated))
    fig.savefig(figpath("p1_q1_1.pdf"))
    return fig, (ax1, ax2)


def plot_averages(data):
    times, rounded, truncated = prepare_averages(data)
    fig, ax = plt.subplots()
    ax.scatter(times, rounded, label="rounded")
    ax.scatter(times, truncated, label="truncated")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(min(times), max(times))
    ax.set_xlabel("Numbers of multiplications ($n$)")
    ax.set_ylabel("Average fractional differences")
    ax.legend(loc="best")
    fig.savefig(figpath("p1_q1.pdf"))
    return fig, ax


def plot_averages_diff(data):
    times, rounded, truncated = prepare_averages(data)
    fig, ax = plt.subplots()
    y = truncated - rounded
    ax.scatter(times, y, color="k")
    ax.set_xscale("log")
    ax.set_xlim(min(times), max(times))
    ax.set_ylim(min(y), max(y))
    ax.set_xlabel("Numbers of multiplications ($n$)")
    ax.set_ylabel("Differences between rounding and truncation")
    fig.savefig(figpath("p1_q2.pdf"))
    return fig, ax


if __name__ == "__main__":
    ndigits = 6  # The number of digits we truncate the operand to
    sampling_at = np.append(
        np.linspace(10, 1000, dtype=int), np.linspace(1000, 10000, num=10, dtype=int)
    )
    raw_data = sampling(100)(ndigits, at=sampling_at)
    times, rounded, truncated = prepare_averages(averages(raw_data))
    plot_averages(averages(raw_data))
    plot_averages_diff(averages(raw_data))
