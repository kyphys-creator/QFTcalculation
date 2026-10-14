# %% [markdown]
# # Step (9): RG flow of the dimensionless parameters in d = 4 and d = 6
#
# RG flow of the dimensionless parameters in d = 4 and d = 6 (research note, step (9), figs/rgflow.pdf).
#
# With t = ln(mu), the loop-expansion parameter a and y = m^2/mu^2 (m: MS-bar mass, g: MS-bar coupling) obey
#     d = 4:  a = g^2/((4pi)^2 mu^2):  da/dt = -2 a,       dy/dt = c4 a - 2 y,        c4 = (4pi)^2 gamma/g^2
#     d = 6:  a = g^2/(4pi)^3:         da/dt = b6 a^2,     dy/dt = (c6 a - 2) y,      b6 = 2 (4pi)^3 beta/g^3,
#                                                                                     c6 = (4pi)^3 gamma/(g^2 m^2)
# (note, App. M), gamma = mu dm^2/dmu and beta = mu dg/dmu.  The coefficients are built from the COLLIER fits of
# step (9) (results/rg4_comparison.csv, rg4_numeric.py) and compared with the note's c4 = 1, b6 = -3/2, c6 = -5/6.
# Exact trajectories (checked against the flow equations below):
#     d = 4:  a = a0 e^{-2t},              y = e^{-2t} (y0 + c4 a0 t)
#     d = 6:  a = a0 / (1 - b6 a0 t),      y = y0 e^{-2t} (1 - b6 a0 t)^{-c6/b6}
# Arrows point toward the infrared (decreasing mu).  The star is the reference point of the note (m = g = 1 at mu = m).
# Writes ../figs/rgflow.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rgflow.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K4 = (4 * math.pi) ** 2
K6 = (4 * math.pi) ** 3


# %% [markdown]
# ## The flow coefficients from the step (9) fits

# %%
# the coefficients from the step (9) fits (COLLIER, m = g = 1)
fits = {}
with open(os.path.join(HERE, "results", "rg4_comparison.csv")) as fh:
    rows = list(csv.reader(fh))
start = next(i for i, r in enumerate(rows) if r[:2] == ["case", "tool"] and "gamma_fit" in r)
for r in rows[start + 1:]:
    if len(r) > 3 and r[1] == "collier":
        fits[r[0]] = (float(r[2]), float(r[3]))
c4 = K4 * fits["d=4, MS-bar m"][0]
b6 = 2 * K6 * fits["d=6, MS-bar m"][1]
c6 = K6 * fits["d=6, MS-bar m"][0]
for name, val, ref in (("c4", c4, 1.0), ("b6", b6, -1.5), ("c6", c6, -5 / 6)):
    print(f"{name} from the step (9) fit = {val:+.15f}  (note: {ref:+.15f}, rel. dev. {abs(val / ref - 1):.1e})")
    assert abs(val / ref - 1) < 1e-13


# %% [markdown]
# ## Flow equations and exact trajectories

# %%
def flow4(a, y):
    return -2 * a, c4 * a - 2 * y


def flow6(a, y):
    return b6 * a * a, (c6 * a - 2) * y


def traj4(a0, y0, t):
    return a0 * np.exp(-2 * t), np.exp(-2 * t) * (y0 + c4 * a0 * t)


def traj6(a0, y0, t):
    return a0 / (1 - b6 * a0 * t), y0 * np.exp(-2 * t) * (1 - b6 * a0 * t) ** (-c6 / b6)


# %%
# the exact trajectories satisfy the flow equations (central differences)
for traj, flow in ((traj4, flow4), (traj6, flow6)):
    for a0, y0 in ((0.3, 0.5), (0.7, -0.4), (1 / K4, 1.0)):
        for t in (-0.3, 0.0, 0.8):
            h = 1e-5
            (ap, yp), (am, ym) = traj(a0, y0, t + h), traj(a0, y0, t - h)
            fa, fy = flow(*traj(a0, y0, t))
            assert abs((ap - am) / (2 * h) - fa) < 1e-8 and abs((yp - ym) / (2 * h) - fy) < 1e-8
print("exact trajectories satisfy the flow equations: ok")


# %% [markdown]
# ## Figure

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)



def window_path(traj, a0, y0):
    """The trajectory through the boundary point (a0, y0), followed toward the ultraviolet down to the origin."""
    t = np.concatenate([[0], np.geomspace(1e-4, 2e3, 4000)])
    a, y = traj(a0, y0, t)
    keep = (a <= 1 + 1e-12) & (abs(y) <= 1 + 1e-12)
    return a[keep], y[keep]


def ir_arrow(ax, a, y, frac, color):
    """An arrowhead pointing toward the infrared (back along the ultraviolet-ordered path) at arc length frac."""
    seg = np.hypot(np.diff(a), np.diff(y) / 2)
    arc = np.concatenate([[0], np.cumsum(seg)])
    i = int(np.searchsorted(arc, frac))
    ax.annotate("", xy=(a[i - 3], y[i - 3]), xytext=(a[i], y[i]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.6, mutation_scale=7, shrinkA=0, shrinkB=0))


GRAY = "0.45"
seeds = ([(1.0, y0) for y0 in np.linspace(-0.9, 0.9, 7)]
         + [(a0, sgn) for sgn in (1.0, -1.0) for a0 in (0.08, 0.25, 0.5, 0.75)])
fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.9), sharey=True)
panels = ((axes[0], traj4, 1 / K4, r"$d=4$", r"$\hat\alpha=g^2/((4\pi)^2\mu^2)$", False),
          (axes[1], traj6, 1 / K6, r"$d=6$", r"$\hat\alpha=g^2/(4\pi)^3$", True))
for ax, traj, aref, title, xlabel, massless in panels:
    for a0, y0 in seeds:
        if massless and y0 == 0:
            continue                                  # on the invariant line y = 0, drawn below
        a, y = window_path(traj, a0, y0)
        ax.plot(a, y, color=GRAY, lw=0.6, ls="-")
        ir_arrow(ax, a, y, 0.22, GRAY)
    # invariant lines: the free theory (a = 0) and, in d = 6 only, the massless theory (y = 0)
    for sgn in (1, -1):
        ax.plot([0, 0], [0, sgn], color="k", lw=0.9, ls="-")
        ir_arrow(ax, np.zeros(200), np.linspace(sgn, 0, 200), 0.2, "k")
    if massless:
        ax.plot([0, 1], [0, 0], color="k", lw=0.9, ls="-")
        ir_arrow(ax, np.linspace(1, 0, 200), np.zeros(200), 0.45, "k")
    ax.plot([aref], [1.0], "*", ms=8, color="#eb6235", zorder=6, clip_on=False)
    ax.plot([0], [0], "o", ms=4, color="k", zorder=6, clip_on=False)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, 1)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontsize=8)
axes[0].set_ylabel(r"$\hat m^2=m^2/\mu^2$")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "rgflow.pdf"))
print("wrote figs/rgflow.pdf")
