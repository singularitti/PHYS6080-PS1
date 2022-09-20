# An example of finite precision errors and how they propagate
# during multiplication when the input numbers are truncated to
# a fixed number of digits and when products are rounded to a fixed
# number of digits.
import math
from functools import reduce
from operator import mul

import numpy as np
import pandas as pd

__all__ = ["myround", "truncate", "rounded_mul", "truncated_mul", "rounded_accumulate",
           "truncated_accumulate", "sampling", "averages"]


def myround(x, ndigits):
    mantissa, exponent = math.frexp(x)
    return round(mantissa, ndigits) * 2 ** exponent


def truncate(x, ndigits):
    return int(x * 10 ** ndigits) * 10 ** (-ndigits)


def rounded_mul(ndigits):
    return lambda x, y: myround(x, ndigits) * myround(y, ndigits)


def truncated_mul(ndigits):
    return lambda x, y: x * truncate(y, ndigits)


def rounded_accumulate(ndigits):
    func = rounded_mul(ndigits)
    return lambda ys, initial: reduce(func, ys, initial)


def truncated_accumulate(ndigits):
    func = truncated_mul(ndigits)
    return lambda ys, initial: reduce(func, ys, truncate(initial, ndigits))


def sampling(times):
    colnames = ["n", "type", "full", "rounded", "truncated", "times"]
    df = pd.DataFrame(columns=colnames)

    def sampler(ndigits):
        for time in range(1, times + 1):
            x = np.random.rand()
            ys = np.random.rand(10000) + 0.542
            new1 = pd.DataFrame(
                data=[[0, "value", x, myround(x, ndigits), truncate(x, ndigits), time]],
                columns=colnames,
            )
            df = pd.concat([df, new1], ignore_index=True)
            for n in (10, 100, 1000, 10000):
                a = reduce(mul, ys[:n], x)
                b = rounded_accumulate(ndigits)(ys[:n], x)
                c = truncated_accumulate(ndigits)(ys[:n], truncate(x, ndigits))
                diff = 1 - [a, b, c] / a
                new = pd.DataFrame(
                    data=[[n, "value", a, b, c, time], [n, "frac diff", *diff, time]],
                    columns=colnames,
                )
                df = pd.concat([df, new], ignore_index=True)
        df = df.set_index(["n", "type"])
        return df

    return sampler


def averages(data):
    colnames = ["n", "type", "rounded", "truncated"]
    df = pd.DataFrame(columns=colnames)
    for n, group in data.groupby('n'):
        for t, g in group.groupby('type'):
            new = pd.DataFrame(
                [n, t, g["rounded"].mean(), g["truncated"].mean()],
                columns=colnames
            )
            pd.concat([df, new])
    return df


if __name__ == "__main__":
    ndigits = 6  # The number of digits we truncate the operand to
    sampling(10)(ndigits)
