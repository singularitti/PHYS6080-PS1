# An example of finite precision errors and how they propagate
# during multiplication when the input numbers are truncated to
# a fixed number of digits and when products are rounded to a fixed
# number of digits.
import math


__all__ = ['myround', 'truncate', 'rounded_mul', 'truncated_mul']


def myround(x, ndigits):
    mantissa, exponent = math.frexp(x)
    return round(mantissa, ndigits) * 2**exponent


def truncate(x, ndigits):
    return int(x * 10**ndigits) * 10**(-ndigits)


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
