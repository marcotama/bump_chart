import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from collections import defaultdict, OrderedDict
from scipy import interpolate
import pandas as pd


def plot_bump_chart(
    data: pd.DataFrame,
    colors=None,
    title='',
    font_family='GillSans',
    font_size=12,
    width=12,
    height=8,
    savename=None,
    dpi=150
):
    """
    Creates a bump chart.

    :param data: (pandas.DataFrame) index indicate the categories, columns indicate time / period
    :param font_family: (str) font family name installed on your system
    :param font_size: (int, default 12) set the font size in case your data have more lines than you can have text lines
     of text in your figure height, data will be binned to fit
    :param height: (float, default 12) Figure height in inches
    :param width: (float, default 8) Figure width in inches
    :param savename: (str or Iterable[str]) File path to save your graph
    :param colors: (Dict[str, str], like: {label: color}) Colors to be used
    :param title: (str) A title at the bottom of the graph
    :param dpi: (int) DPI resolution for saving to file
    :returns: (matplotlib.figure.Figure) Plot slope plot Tufte Style
    """

    RECTANGLES_WIDTH = .1
    RECTANGLES_HEIGHT = .1
    ALPHA_SPLINE = .4
    ALPHA_RECTANGLE = .4
    ALPHA_LEGEND = ALPHA_SPLINE * (1 - ALPHA_RECTANGLE) + ALPHA_RECTANGLE

    font = FontProperties(font_family)
    font.set_size(font_size)
    fig = plt.figure(figsize=(width, height), dpi=30, facecolor="w")
    ax = fig.gca()

    df = data.copy()  # type: pd.DataFrame

    X = []
    Y = defaultdict(list)
    x_ticks = []
    # prepare xs and ys that trick spline interpolation in being horizontal where knot points are
    for i, label in enumerate(df.columns.values):
        X += [i, i + 0.01, i + RECTANGLES_WIDTH - 0.01, i + RECTANGLES_WIDTH]
        for index, row in df.iterrows():
            Y[index] += [row[label]] * 4
        x_ticks.append(label)
    X = np.array(X)
    for k, v in Y.items():
        Y[k] = np.array(v)

    X_int = np.arange(0, len(df.columns) - 1 + RECTANGLES_WIDTH, 0.001)

    for index, row in df.iterrows():
        # spline interpolation
        tck = interpolate.splrep(X, Y[index], s=0)
        Y_int = interpolate.splev(X_int, tck, der=0)

        color = 'blue' if colors is None else colors[index]

        plt.fill_between(
            X_int,
            Y_int * (1-RECTANGLES_HEIGHT/2),
            Y_int * (1+RECTANGLES_HEIGHT/2),
            color=color,
            alpha=ALPHA_SPLINE
        )

        for i in range(len(df.columns)):
            y = df.ix[index, i]
            plt.fill_between(
                [i, i+RECTANGLES_WIDTH],
                [y*(1-RECTANGLES_HEIGHT/2), y*(1-RECTANGLES_HEIGHT/2)],
                [y*(1+RECTANGLES_HEIGHT/2), y*(1+RECTANGLES_HEIGHT/2)],
                color=color,
                alpha=ALPHA_RECTANGLE
            )

    # legend for fill_between is a bit tricky
    legend_proxies = OrderedDict()
    for label, color in colors.items():
        legend_proxies[label] = plt.Rectangle((0, 0), 1, 1, fc=color, alpha=ALPHA_LEGEND)
    plt.sca(ax)
    # ax.set_position([box.x0, box.y0, box.width, box.height])
    lgd = plt.legend(
        legend_proxies.values(),
        legend_proxies.keys(),
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0.0
    )

    plt.title(title)
    plt.xticks([f+RECTANGLES_WIDTH/2 for f in range(len(df.columns))], x_ticks)
    plt.yticks([])
    ax.set_xlim(-0.1, X.max() + 0.1)
    ax.set_ylim(
        min(y.min() for y in Y.values()),
        max(y.max() for y in Y.values()) * (1 + RECTANGLES_HEIGHT)
    )
    plt.tight_layout()

    if savename:
        if isinstance(savename, str):
            plt.gcf().savefig(savename, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
        if hasattr(savename, '__iter__'):
            for savename_ in savename:
                plt.gcf().savefig(savename_, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
