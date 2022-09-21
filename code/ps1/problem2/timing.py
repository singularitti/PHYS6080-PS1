import math
import timeit

import numpy as np


def time1():
    setup = "import math"
    n = 10000000
    s = timeit.timeit(stmt='8967.4*15.4328', setup=setup, number=n)
    print('Time per multiplication call is ', float(s) / n)
    s = timeit.timeit(stmt='8967.4*15.4328+3567.2', setup=setup, number=n)
    print('Time per multiplication plus add call is ', float(s) / n)
    s = timeit.timeit(stmt='8967.4/15432.8', setup=setup, number=n)
    print('Time per division call is ', float(s) / n)
    s = timeit.timeit(stmt='math.cos(10)', setup=setup, number=n)
    print('Time per cos call is ', float(s) / n)
    s = timeit.timeit(stmt='math.log(10)', setup=setup, number=n)
    print('Time per log call is ', float(s) / n)


def time2():
    n = 1000000
    a = np.random.rand(n)
    b = np.random.rand(n)
    starttime = timeit.default_timer()
    print("The start time is :", starttime)
    a * np.log(b)
    dt = timeit.default_timer() - starttime
    print("The time difference is :", dt)
    print("The time per operation is :", dt / n)


def time3():
    n = 1000
    a = np.random.rand(n)
    b = np.random.rand(n)
    a = a.tolist()
    b = b.tolist()
    starttime = timeit.default_timer()
    print("The start time is :", starttime)
    for i, j in zip(a, b):
        i * math.log(j)
    dt = timeit.default_timer() - starttime
    print("The time difference is :", dt)
    print("The time per operation is :", dt / n)


if __name__ == '__main__':
    time1()
    time2()
    time3()
