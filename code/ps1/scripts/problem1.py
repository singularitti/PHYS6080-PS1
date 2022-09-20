# An example of finite precision errors and how they propagate
# during multiplication when the input numbers are truncated to
# a fixed number of digits and when products are rounded to a fixed
# number of digits.
from functools import partial, reduce
from operator import mul

import numpy as np
import pandas as pd
from ps1.rounding import myround, rounded_mul, truncate, truncated_mul

if __name__ == "__main__":
    ndigits = 6  # The number of digits we truncate the operand to
    x = np.random.rand()
    ys = np.random.rand(10000) + 0.542
    colnames = ['n', "datatype", "full", "rounded", "truncated"]
    df = pd.DataFrame(data=[[0, "value", x, myround(x, ndigits), truncate(x, ndigits)]],
                      columns=colnames)
    for n in (10, 100, 1000, 10000, 100000):
        a = reduce(mul, ys[:n], x)
        b = reduce(partial(rounded_mul, ndigits=ndigits), ys[:n], x)
        c = reduce(partial(truncated_mul, ndigits=ndigits), ys[:n], truncate(x, ndigits))
        diff = 1 - [a, b, c] / a
        new = pd.DataFrame(
            data=[[n, "value", a, b, c], [n, "frac diff", *diff]], columns=colnames)
        df = pd.concat([df, new])
    df = df.set_index(['n', "datatype"])
