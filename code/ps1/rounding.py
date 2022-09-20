# An example of finite precision errors and how they propagate
# during multiplication when the input numbers are truncated to
# a fixed number of digits and when products are rounded to a fixed
# number of digits.
import math


__all__ = ['myround', 'truncate', 'rounded_multiply', 'truncated_multiply']


def myround(x, ndigits):
    mantissa, exponent = math.frexp(x)
    return round(mantissa, ndigits) * 2**exponent


def truncate(x, ndigits):
    return int(x * 10**ndigits) * 10**(-ndigits)


def rounded_multiply(x, y, ndigits):
    x, y = myround(x, ndigits), myround(y, ndigits)
    z = x * y
    return myround(z, ndigits)


def truncated_multiply(x, y, ndigits):
    x, y = truncate(x, ndigits), truncate(y, ndigits)
    return x * y
