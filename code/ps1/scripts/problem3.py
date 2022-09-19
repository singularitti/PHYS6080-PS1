# Back recursion for modified Bessel functions
from ps1.bessel_functions import back_recursion
from ps1.plotting import plot_exact, plot_errors, save_plots_gif, plot_mat_errors, plot_raw


def main(x, max_order):
    # plot_raw(x, max_order)
    plot_errors(x, max_order)
    # plot_mat_errors(back_recursion)


if __name__ == "__main__":
    pass
    # for y in range(10, 40):
    #     main(10, y)
