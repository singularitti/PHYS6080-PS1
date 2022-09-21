import matplotlib.pyplot as plt
import numpy as np

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
    ax.set_yscale('log')
    ax.legend(loc="best")
    ax.set_xlabel("numbers of multiplications")
    ax.set_ylabel("average difference for the rounding and truncation cases")
    return fig, ax


if __name__ == '__main__':
    ndigits = 6  # The number of digits we truncate the operand to
    raw_data = sampling(10)(ndigits)
    times, rounded, truncated = prepare_averages(averages(raw_data))
    plot_averages(averages(raw_data))
