import os
from typing import List, Tuple

import matplotlib.pyplot as plt


def plot_ranges(*, x_coords: List[float], min_vals: List[float], mid_vals: List[float], max_vals: List[float], x_label: str, y_label: str, save_path: os.PathLike, show: bool = False):
    assert len(x_coords) == len(min_vals) == len(mid_vals) == len(max_vals)

    color = '#B22400'
    fontsize = 14
    fig, ax = plt.subplots(figsize=(4., 4.))
    ax.fill_between(x_coords, min_vals, max_vals, alpha=0.25, color=color, linewidth=0)
    ax.plot(x_coords, mid_vals, color=color)
    plt.xlabel(x_label, fontsize=fontsize)
    plt.ylabel(y_label, fontsize=fontsize)

    plt.tight_layout()
    plt.savefig(save_path)
    if show:
        plt.show()
