# %% [markdown]
# # Step (7): RG flow of the shape of the potential, (lambda, alpha)
#
# RG flow of lambda and alpha = 3 lambda m^2/g^2 (research note models/phi34, step (7), figs/rgflow.pdf).
#
# With t = ln(mu), gamma = (c1 g^2 + c2 lambda m^2)/(4pi)^2, beta_g = b_g g lambda/(4pi)^2, beta_lambda = b_l lambda^2/(4pi)^2
# (MS-bar, Y scheme; note Eq. (7), App. J),
#     d lambda/dt = b_l lambda^2/(4pi)^2,
#     d alpha/dt  = alpha (beta_lambda/lambda + gamma/m^2 - 2 beta_g/g) = lambda [3 c1 - k alpha]/(4pi)^2,  k = 2 b_g - b_l - c2,
# a closed two-dimensional flow (g^2/m^2 = 3 lambda/alpha).  With the note's c1 = c2 = 1, b_g = b_l = 3: k = 2,
# d alpha/dt = lambda (3 - 2 alpha)/(4pi)^2.  Exact trajectories (checked against the flow equations below):
#     lambda = lambda0/(1 - b_l lambda0 t/(4pi)^2),   alpha = alpha* + (alpha0 - alpha*) (lambda/lambda0)^(-k/b_l),
#     alpha* = 3 c1/k (= 3/2).
# The coefficients come from the four-coefficient COLLIER fit of rg_numeric.py (results/rg_comparison.csv).  Arrows point
# toward the infrared (decreasing mu).  The star is the reference point of the note (m = g = lambda = 1 at mu = m, alpha = 3).
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
K = (4 * math.pi) ** 2


# %% [markdown]
# ## The flow coefficients from the step (7) fit

# %%
with open(os.path.join(HERE, "results", "rg_comparison.csv")) as fh:
    rows = list(csv.reader(fh))
start = next(i for i, r in enumerate(rows) if r[:1] == ["coefficient"])
coef = {r[0]: float(r[1]) for r in rows[start + 1:] if len(r) == 3}
c1, c2, bg, bl = coef["c1"], coef["c2"], coef["b_g"], coef["b_l"]
kk = 2 * bg - bl - c2
astar = 3 * c1 / kk
for name, val, ref in (("k", kk, 2.0), ("alpha*", astar, 1.5), ("b_g - b_l", bg - bl, 0.0)):
    print(f"{name} from the step (7) fit = {val:+.15f}  (note: {ref:+.15f})")
    assert abs(val - ref) < 1e-13


# %% [markdown]
# ## Flow equations and exact trajectories

# %%
def flow(lam, alpha):
    return bl * lam * lam / K, lam * (3 * c1 - kk * alpha) / K


def traj(lam0, alpha0, t):
    lam = lam0 / (1 - bl * lam0 * t / K)
    return lam, astar + (alpha0 - astar) * (lam / lam0) ** (-kk / bl)


# %%
# the exact trajectories satisfy the flow equations (central differences)
for lam0, alpha0 in ((1.0, 3.0), (0.3, 0.5), (5.0, -0.4)):
    for t in (-30.0, 0.0, 8.0):
        h = 1e-4
        (lp, ap), (lm, am) = traj(lam0, alpha0, t + h), traj(lam0, alpha0, t - h)
        fl, fa = flow(*traj(lam0, alpha0, t))
        assert abs((lp - lm) / (2 * h) / fl - 1) < 1e-7 and abs((ap - am) / (2 * h) / fa - 1) < 1e-7
print("exact trajectories satisfy the flow equations: ok")


# %% [markdown]
# ## Figure

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)

LMIN, LMAX, AMIN, AMAX = 1e-2, 1e2, -0.6, 3.6
GRAY = "0.45"


def path(cc):
    """The trajectory alpha = alpha* + cc lambda^(-k/b_l), ordered toward the ultraviolet (increasing lambda)."""
    lam = np.geomspace(LMIN, LMAX, 2000)
    alpha = astar + cc * lam ** (-kk / bl)
    keep = (alpha >= AMIN) & (alpha <= AMAX)
    return lam[keep], alpha[keep]


def ir_arrow(ax, lam, alpha, frac, color):
    """An arrowhead pointing toward the infrared (decreasing lambda) at the fraction frac of the drawn path."""
    x = np.log10(lam)
    arc = np.concatenate([[0], np.cumsum(np.hypot(np.diff(x) / 4, np.diff(alpha) / (AMAX - AMIN)))])
    i = max(int(np.searchsorted(arc, frac * arc[-1])), 4)
    ax.annotate("", xy=(lam[i - 4], alpha[i - 4]), xytext=(lam[i], alpha[i]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.6, mutation_scale=7, shrinkA=0, shrinkB=0))


fig, ax = plt.subplots(figsize=(3.25, 2.6))
ax.axhspan(AMIN, 0, color="0.92", lw=0)
ax.text(27, -0.35, r"$m^2<0$", fontsize=7, color="0.35")      # in a gap between the trajectories
for aline in (1.0, 9 / 8):                      # alpha = 1 (degenerate minima) and 9/8 (second minimum appears)
    ax.axhline(aline, color="#5d81b4", lw=0.7, ls=":")
for cc, frac in ((0.04, 0.25), (0.15, 0.6), (0.5, 0.35), (1.5, 0.55), (4.0, 0.4), (12.0, 0.6)):
    for sgn in (1, -1):
        lam, alpha = path(sgn * cc)
        if len(lam) < 10:
            continue
        ax.plot(lam, alpha, color=GRAY, lw=0.6, ls="-")
        ir_arrow(ax, lam, alpha, frac, GRAY)
lam_ref, alpha_ref = path(3.0 - astar)          # through the reference point (1, 3)
ax.plot(lam_ref, alpha_ref, color="#eb6235", lw=0.9, ls="-")
ax.plot([LMIN, LMAX], [astar, astar], color="k", lw=0.9, ls="-")
ir_arrow(ax, np.geomspace(LMIN, LMAX, 200), np.full(200, astar), 0.12, "k")
ax.plot([1.0], [3.0], "*", ms=8, color="#eb6235", zorder=6)
ax.set_xscale("log")
ax.set_xlim(LMIN, LMAX)
ax.set_ylim(AMIN, AMAX)
ax.set_xlabel(r"$\lambda$")
ax.set_ylabel(r"$\alpha=3\lambda m^2/g^2$")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "rgflow.pdf"))
print("wrote figs/rgflow.pdf")


# %% [markdown]
# ## Numbers quoted in the note

# %%
# change of alpha along the reference trajectory for mu = m/4 ... 4m, and lambda at the ends
for t in (math.log(0.25), math.log(4.0)):
    lam, alpha = traj(1.0, 3.0, t)
    print(f"mu = {math.exp(t):5.2f} m: lambda = {lam:.6f}, alpha = {alpha:.6f}")
print(f"Landau pole of the reference trajectory: ln(mu/m) = (4pi)^2/3 = {K / 3:.2f}")
# a trajectory with alpha = 1 at mu = m and lambda = 1: alpha at mu = 4m and mu = m/4
for t in (math.log(0.25), math.log(4.0)):
    print(f"alpha0 = 1: mu = {math.exp(t):5.2f} m, alpha = {traj(1.0, 1.0, t)[1]:.6f}")
