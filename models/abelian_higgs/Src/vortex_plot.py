# %% [markdown]
# # Step (11): figure of the ANO vortex
#
# Research note models/abelian_higgs, step (11).  Reads results/vortex_profiles.csv and results/vortex.csv (vortex.py) and
# draws ../figs/vortex.pdf:
#   left : the n = 1 profiles f (solid) and a (dashed) against rho = MA r for beta = MH^2/MA^2 = 0.2, 1, 5;
#   right: T(n)/(n pi v^2) against beta for n = 1, 2, 3: equal to 1 at the BPS point beta = 1, higher n lower for
#          beta < 1 (type I, vortices attract) and higher for beta > 1 (type II, repel).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python vortex_plot.py

# %%
import csv
import os
import sys

import numpy as np

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
with open(os.path.join(HERE, "results", "vortex_profiles.csv")) as fh:
    rows = list(csv.reader(fh))
hp, pr = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
with open(os.path.join(HERE, "results", "vortex.csv")) as fh:
    tr = list(csv.DictReader(fh))

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))

cols = {"0.2": "C1", "1": "k", "5": "C0"}
for b, col in cols.items():
    ax1.plot(pr[:, 0], pr[:, hp.index("f_b" + b)], color=col, ls="-", lw=1.5, label=r"$\beta=%s$" % b)
    ax1.plot(pr[:, 0], pr[:, hp.index("a_b" + b)], color=col, ls="--", lw=1.5)
ax1.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.12))
ax1.set_xlim(0, 8)
ax1.set_ylim(0, 1.05)
ax1.set_xlabel(r"$\rho=M_Ar$")
ax1.set_ylabel(r"$f$ (solid), $a$ (dashed)")
ax1.text(4.7, 0.05, r"$n=1$, $\beta=M_h^2/M_A^2$", color="0.3", fontsize=8)

for n, col, ls, mk in ((1, "k", "-", "o"), (2, "C0", "--", "s"), (3, "C1", "-.", "^")):
    pts = sorted((float(r["beta"]), float(r["T_over_piv2"]) / n) for r in tr if int(r["n"]) == n and float(r["beta"]) <= 50)
    x, y = np.array(pts).T
    ax2.semilogx(x, y, color=col, ls=ls, marker=mk, ms=3.5, lw=1.3, label=r"$n=%d$" % n)
ax2.axvline(1, color="0.55", lw=0.8, ls=":")
ax2.set_xlabel(r"$\beta=M_h^2/M_A^2=2\lambda/e^2$")
ax2.set_ylabel(r"$T/(n\,\pi v^2)$")
ax2.legend(loc="upper left", fontsize=8)
ax2.text(0.06, 1.45, "type I", fontsize=8, color="0.3")
ax2.text(4.0, 0.75, "type II", fontsize=8, color="0.3")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "vortex.pdf"))
print("written ../figs/vortex.pdf")
