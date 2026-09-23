"""
Shared chart styling for all notebooks — static matplotlib/seaborn PNGs, not interactive web
charts, so this applies only the parts of the dataviz skill's method that carry over: a fixed
categorical hue order (never cycled/reordered by value), one hue for sequential/magnitude,
blue<->red for diverging, reserved status colors for good/bad outcome states, thin marks, a
legend whenever there are 2+ series. No dark mode / hover — not applicable to static PNGs.
Palette values are the skill's validated default reference instance, used unchanged.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Fixed categorical order — never reorder by value, never cycle past what's needed.
CATEGORICAL = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

# Reserved for state, never reused as a categorical series color.
STATUS = {
    "good": "#0ca30c",
    "warning": "#fab219",
    "serious": "#ec835a",
    "critical": "#d03b3b",
}

SEQUENTIAL_BLUE = "Blues"  # one hue, light->dark; use for heatmaps / magnitude ramps
DIVERGING = "vlag"  # blue<->red with a neutral midpoint; use for signed lift/deltas

# Ordinal ramp — discrete ordered stages (funnel steps, tiers), one hue light->dark, from the
# skill's validated blue ramp (steps 250/350/450/550/700). Starts no lighter than step 250, the
# documented 2:1-contrast floor for ordinal use. Needed as explicit hex (not a colormap name)
# for non-matplotlib renderers, e.g. the Plotly funnel chart in notebook 03.
SEQUENTIAL_BLUE_ORDINAL = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]

INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

# The four OULAD outcome states, in a fixed reading order (best -> left the course), mapped to
# status colors so a "did this go well" read is consistent across every chart that uses it.
RESULT_ORDER = ["Distinction", "Pass", "Fail", "Withdrawn"]
RESULT_COLORS = {
    "Distinction": STATUS["good"],
    "Pass": CATEGORICAL[0],
    "Fail": STATUS["serious"],
    "Withdrawn": STATUS["critical"],
}
SUCCESS_COLOR = STATUS["good"]
NOT_SUCCESS_COLOR = STATUS["critical"]


def set_style():
    """Call once per notebook, in the imports cell."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "axes.edgecolor": BASELINE,
            "axes.labelcolor": INK_SECONDARY,
            "text.color": INK_PRIMARY,
            "xtick.color": INK_MUTED,
            "ytick.color": INK_MUTED,
            "grid.color": GRIDLINE,
            "axes.grid.axis": "y",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.family": "sans-serif",
        }
    )


def savefig(name: str, fig=None):
    """Save a chart to images/<name>.png at 150 dpi with a tight bbox — the project convention."""
    (fig or plt).savefig(f"images/{name}.png", dpi=150, bbox_inches="tight")
