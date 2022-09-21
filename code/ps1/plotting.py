import os
from os.path import abspath, dirname, exists, join

import matplotlib.pyplot as plt

__all__ = ['plotsdir', 'figpath']

params = {
    "figure.figsize": (8, 5),
    "figure.autolayout": True,
    "figure.dpi": 300,
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "x-large",
    "ytick.labelsize": "x-large",
    "legend.fontsize": "x-large",
    "text.usetex": True,
}
plt.rcParams.update(params)


def plotsdir():
    path = abspath(join(dirname(__file__), "..", "..", "tex", "ps1", "plots"))
    if not exists(path):
        os.makedirs(path)
    return path


def figpath(figname):
    return join(plotsdir(), figname)
