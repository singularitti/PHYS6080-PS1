import os

import matplotlib.pyplot as plt

__all__ = ['figpath']

params = {
    "legend.fontsize": "x-large",
    "figure.figsize": (8, 5),
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "x-large",
    "ytick.labelsize": "x-large",
    "figure.autolayout": True,
    "text.usetex": True,
}
plt.rcParams.update(params)


def plotsdir():
    return os.path.abspath("../images")


def figpath(figname):
    return os.path.join(plotsdir(), figname)
