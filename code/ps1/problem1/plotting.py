import matplotlib.pyplot as plt
import numpy as np

from plotconfig import figpath
from problem1.rounding import averages, sampling


def prepare_averages(data):
    times = data.index.levels[0][1:]  # Ignore where `n` == 0
    rounded, truncated = np.empty(len(times)), np.empty(len(times))
    for i, n in enumerate(times):
        columns = data.xs((n, "frac diff"))
        rounded[i] = columns["rounded"]
        truncated[i] = columns["truncated"]
    return times, rounded, truncated


def plot_averages(data):
    times, rounded, truncated = prepare_averages(data)
    fig, ax = plt.subplots()
    ax.scatter(times, rounded, label="rounded")
    ax.scatter(times, truncated, label="truncated")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(min(times), max(times))
    ax.set_xlabel("numbers of multiplications")
    ax.set_ylabel("average difference for the rounding and truncation cases")
    ax.legend(loc="best")
    return fig, ax


def plot_averages_diff(data):
    times, rounded, truncated = prepare_averages(data)
    fig, ax = plt.subplots()
    ax.scatter(times, truncated - rounded)
    ax.set_xscale("log")
    ax.set_xlim(min(times), max(times))
    ax.set_xlabel("numbers of multiplications")
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
