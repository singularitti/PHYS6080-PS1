# Back recursion for modified Bessel functions
from problem3.bessel_functions import back_recursion
from problem3.plotting import (plot_errors, plot_exact, plot_mat_errors,
                               plot_raw, save_plots_gif)


def main(x, max_order):
    # plot_raw(x, max_order)
    plot_errors(x, max_order)
    # plot_mat_errors(back_recursion)


if __name__ == "__main__":
    pass
    # for y in range(10, 40):
    #     main(10, y)
