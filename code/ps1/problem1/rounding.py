# An example of finite precision errors and how they propagate
# during multiplication when the input numbers are truncated to
# a fixed number of digits and when products are rounded to a fixed
# number of digits.
import math
from functools import partial, reduce
from operator import mul

import numpy as np
import pandas as pd

__all__ = ['myround', 'truncate', 'rounded_mul', 'truncated_mul', 'rounded_accumulate',
           'truncated_accumulate']


def myround(x, ndigits):
    mantissa, exponent = math.frexp(x)
    return round(mantissa, ndigits) * 2 ** exponent


def truncate(x, ndigits):
    return int(x * 10 ** ndigits) * 10 ** (-ndigits)


def rounded_mul(x, y, ndigits):
    x, y = myround(x, ndigits), myround(y, ndigits)
    return x * y


def truncated_mul(x, y, ndigits):
    return x * truncate(y, ndigits)


def rounded_accumulate(ys, ndigits, initial):
    func = partial(rounded_mul, ndigits=ndigits)
    return reduce(func, ys, initial)


def truncated_accumulate(ys, ndigits, initial):
    func = partial(truncated_mul, ndigits=ndigits)
    return reduce(func, ys, truncate(initial, ndigits))


if __name__ == "__main__":
    ndigits = 6  # The number of digits we truncate the operand to
    x = np.random.rand()
    ys = np.random.rand(10000) + 0.542
    colnames = ['n', "datatype", "full", "rounded", "truncated"]
    df = pd.DataFrame(data=[[0, "value", x, myround(x, ndigits), truncate(x, ndigits)]],
                      columns=colnames)
    for n in (10, 100, 1000, 10000, 100000):
        a = reduce(mul, ys[:n], x)
        b = rounded_accumulate(ys[:n], ndigits, x)
        c = truncated_accumulate(ys[:n], ndigits, truncate(x, ndigits))
        diff = 1 - [a, b, c] / a
        new = pd.DataFrame(
            data=[[n, "value", a, b, c], [n, "frac diff", *diff]], columns=colnames)
        df = pd.concat([df, new])
    df = df.set_index(['n', "datatype"])
