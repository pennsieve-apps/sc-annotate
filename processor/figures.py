"""
PNG figures (150 dpi): UMAP by cell type, cell types by sample (stacked bar) and the
cell_type_score histogram. One colour system: a fixed, ordered
categorical list (identity follows the label, never its rank; a legend is
always drawn), a single-hue sequential ramp for magnitude, 'Unassigned' in a
neutral grey, muted inks for chrome.
"""
from __future__ import annotations

from pathlib import Path

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
NEUTRAL = "#bdbcb5"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948",
          "#184f95", "#9a3d12", "#0f6e4c", "#8a5c00", "#a63d6a", "#5c8a3a", "#3b2f8f", "#8f2727",
          "#7fb3ee", "#f3a07a", "#7fd3b2", "#f5cb5c", "#f3b5cc", "#7fc07f", "#aa9ee8", "#f09a9a"]
SEQUENTIAL = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
DPI = 150


def _plt():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID, "axes.labelcolor": INK_2, "xtick.color": MUTED, "ytick.color": MUTED,
        "text.color": INK, "font.size": 9, "axes.titlesize": 11, "axes.titleweight": "bold",
        "legend.frameon": False, "legend.fontsize": 8,
    })
    return plt


def colour_map(labels: list[str]) -> dict[str, str]:
    """A fixed colour per label in the given order; 'Unassigned' is always neutral grey."""
    out, i = {}, 0
    for lab in labels:
        if lab == "Unassigned":
            out[lab] = NEUTRAL
        else:
            out[lab] = SERIES[i % len(SERIES)]
            i += 1
    return out


def _legend(ax, labels, colours, counts=None, ncol=1, title=None):
    from matplotlib.lines import Line2D

    handles = [Line2D([0], [0], marker="o", linestyle="", markersize=6, markerfacecolor=colours[lab],
                      markeredgecolor=SURFACE, markeredgewidth=0.5,
                      label=f"{lab} ({counts[lab]:,})" if counts else lab) for lab in labels]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.01, 0.5), ncol=ncol, title=title,
              handletextpad=0.3, borderaxespad=0.0, labelspacing=0.3, markerscale=1.0)


def _point_size(n: int) -> float:
    return 6.0 if n < 5000 else 2.5 if n < 50000 else 1.0


def scatter_categorical(coords, labels, order, title: str, path: Path) -> Path:
    """Points coloured by a categorical label, largest categories drawn first (small ones on top)."""
    import numpy as np

    plt = _plt()
    colours = colour_map(order)
    labels = np.asarray(labels, dtype=object)
    n = len(labels)
    size = _point_size(n)
    ncol = 1 if len(order) <= 24 else 2
    fig, ax = plt.subplots(figsize=(7.5 + 1.6 * ncol, 6.4))
    sizes = {lab: int((labels == lab).sum()) for lab in order}
    for lab in sorted(order, key=lambda l: -sizes[l]):
        m = labels == lab
        if not m.any():
            continue
        ax.scatter(coords[m, 0], coords[m, 1], s=size, c=colours[lab], linewidths=0, rasterized=True, alpha=0.9)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(title)
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.tick_params(length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    _legend(ax, [l for l in order if sizes[l] > 0], colours, counts=sizes, ncol=ncol)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def stacked_bar(table, samples: list[str], order: list[str], title: str, path: Path) -> Path:
    """table: dict sample -> dict cell_type -> fraction. One bar per sample, segments in the fixed
    colour order with a 2 px surface gap between them."""
    import numpy as np

    plt = _plt()
    colours = colour_map(order)
    fig, ax = plt.subplots(figsize=(max(5.5, 0.6 * len(samples) + 4.0), 5.0))
    bottoms = np.zeros(len(samples))
    for lab in order:
        vals = np.array([table.get(s, {}).get(lab, 0.0) for s in samples])
        if not vals.any():
            continue
        ax.bar(range(len(samples)), vals, bottom=bottoms, color=colours[lab], width=0.62, edgecolor=SURFACE,
               linewidth=1.5, label=lab)
        for i, v in enumerate(vals):
            if v >= 0.08:
                ax.text(i, bottoms[i] + v / 2, f"{100 * v:.0f} %", ha="center", va="center", fontsize=7,
                        color=INK if lab != "Unassigned" else INK_2)
        bottoms += vals
    ax.set_xticks(range(len(samples)))
    ax.set_xticklabels(samples, rotation=30 if len(samples) > 4 else 0, ha="right" if len(samples) > 4 else "center")
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "25 %", "50 %", "75 %", "100 %"])
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_title(title)
    ax.set_ylabel("fraction of observations")
    _legend(ax, [l for l in order if any(table.get(s, {}).get(l, 0) > 0 for s in samples)], colours)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def score_histogram(scores, min_score: float, title: str, path: Path, xlabel: str) -> Path:
    """Histogram of cell_type_score (0-1) with the MIN_SCORE threshold (reference mode) as a dashed line."""
    import numpy as np

    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    bins = np.linspace(0, 1, 41)
    ax.hist(np.asarray(scores, dtype=float), bins=bins, color=SERIES[0], edgecolor=SURFACE, linewidth=0.6)
    if min_score is not None:
        ax.axvline(min_score, color=INK_2, linestyle="--", linewidth=1)
        ax.text(min_score, ax.get_ylim()[1] * 0.97, f"  MIN_SCORE {min_score:g}", color=INK_2, va="top", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("cells")
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path
