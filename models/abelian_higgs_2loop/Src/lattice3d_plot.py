# %% [markdown]
# # Step (7): the 3D U(1)+Higgs transition against the lattice (figure)
#
# Research note models/abelian_higgs_2loop, step (7).  Reads results/lattice3d.csv and results/lattice3d_bench.csv
# (lattice3d.wl) and draws figs/lattice3d.pdf, scaled with the leading x -> 0 behaviour as in Kajantie et al.
# (hep-lat/9711048, Figs. 2, 3):
#   left:  x y_c(x);   right: x^2 Delta l3(x);
# LO and NLO of the strict (gauge-invariant) expansion, the Landau-gauge one- and two-loop potentials (mu3 = e3^2;
# the two-loop curve is dotted where V''(0) < 0 at y_c, i.e. the symmetric phase is no longer a local minimum),
# the continuum lattice point at x = 0.0463, and the step (6) benchmark MH = 1/2 at its ultrasoft x.
# Usage (from Src/, after lattice3d.wl):  ~/miniforge3/envs/qft/bin/python lattice3d_plot.py

# %%
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()


def num(s):
    return float("nan") if s == "nan" else float(s)


with open(os.path.join(HERE, "results", "lattice3d.csv")) as fh:
    rows = [r for r in csv.DictReader(fh)]
rows = sorted(({k: num(v) for k, v in r.items()} for r in rows), key=lambda r: r["x"])
with open(os.path.join(HERE, "results", "lattice3d_bench.csv")) as fh:
    bench = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(fh)]

XLAT, YC, DYC, DL, DDL = 0.0463, 0.1038, 0.0014, 1.64, 0.12      # Kajantie et al., Secs. 6.2.1, 6.3 (continuum)
XMAX = 0.3

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
curves = (("NLO", "C0", "-", "strict NLO"), ("2L", "C1", "-", "Landau 2-loop"), ("1L", "C1", "--", "Landau 1-loop"))
for ax, q, p in ((ax1, "yc", 1), (ax2, "dl3", 2)):
    lo = 1 / (18 * math.pi ** 2)
    ax.axhline(lo, color="0.55", lw=0.8, ls=":", label=r"LO $1/(18\pi^2)$")
    for key, col, ls, lab in curves:
        pts = [(r["x"], r["x"] ** p * r[f"{q}_{key}"], r.get(f"curv0_{key}", 1.0)) for r in rows
               if r["x"] <= XMAX and not math.isnan(r[f"{q}_{key}"])]
        good = [t for t in pts if not t[2] <= 0]
        ax.plot([t[0] for t in good], [t[1] for t in good], color=col, ls=ls, lw=1.3, label=lab)
        bad = [t for t in pts if t[2] <= 0]
        if bad:      # the origin is no longer a local minimum at y_c (V''(0) < 0): drawn dotted from the last good point
            seg = good[-1:] + bad
            ax.plot([t[0] for t in seg], [t[1] for t in seg], color=col, ls=":", lw=1.0)
    val, err = (YC, DYC) if q == "yc" else (DL, DDL)
    ax.errorbar([XLAT], [XLAT ** p * val], yerr=[XLAT ** p * err], color="k", marker="o", ms=4, capsize=2, lw=1,
                ls="none", label="lattice (continuum)")
    for b in bench:
        if b["x_US"] <= XMAX:
            ax.axvline(b["x_US"], color="0.7", lw=0.6, ls="-.")
            ax.text(b["x_US"] + 0.004, 0.0003 if q == "dl3" else 0.0012, r"$M_h=1/2$", fontsize=7, color="0.4")
    ax.set_xlim(0, XMAX)
    ax.set_xlabel(r"$x=\lambda_3/e_3^2$")
ax1.set_ylim(0, 0.012)
ax2.set_ylim(-0.002, 0.008)
ax2.axhline(0, color="0.3", lw=0.5)
ax1.set_ylabel(r"$x\,y_c$")
ax2.set_ylabel(r"$x^2\Delta\ell_3$")
ax1.legend(loc="upper left", fontsize=7)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "lattice3d.pdf"))
print("written figs/lattice3d.pdf")
