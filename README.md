# PHYS6080

This repository stores the homework I did when I was taking this class
in the fall semester of 2022 at Columbia University.

## How to run the code

For example, go to directory `code/ps1`, and run `python`
or `ipython` from that directory. Import functions and other modules just as I did
in `problem1/plotting.py`:

```python
from problem1.rounding import averages, deviations, sampling

if __name__ == "__main__":
    ndigits = 6
    sampling_at = np.append(
        np.linspace(10, 1000, dtype=int), np.linspace(1000, 10000, num=10, dtype=int)
    )
    raw_data = sampling(100)(ndigits, at=sampling_at)
```

Have fun!
