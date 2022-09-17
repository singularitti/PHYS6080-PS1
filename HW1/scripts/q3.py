# Back recursion for modified Bessel functions
from src.bessel_functions import back_recursion
from src.plotting import plot_errors, plot_mat_errors, plot_raw


def main(x, max_order):
    plot_raw(x, max_order)
    plot_errors(x, max_order)
    plot_mat_errors(back_recursion)


if __name__ == "__main__":
    main(5, 10)
