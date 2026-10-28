# %% [markdown]
# # Step (10): figure of the finite-temperature transition
#
# Research note models/abelian_higgs, step (10).  Reads results/thermal_curves.csv and results/thermal_gauge.csv
# (thermal.wl) and draws ../figs/thermal.pdf:
#   left : V(phi, T_c) - V(0, T_c) over T_c^4 for MH = 0.5 MA (e = 1/2): the one-loop high-T potential (Landau gauge),
#          with the daisy resummation, and with the exact J_B, each at its own T_c;
#   right: |phi_c/T_c in background R_xi and Fermi gauges relative to Landau gauge - 1| against e (lam = e^3/4, all with
#          the same resummation): it falls like e^2 (background R_xi) and e^(3/4) (Fermi, non-analytic m+-); log-log.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python thermal_plot.py

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
with open(os.path.join(HERE, "results", "thermal_curves.csv")) as fh:
    rows = list(csv.reader(fh))
hc, cv = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
with open(os.path.join(HERE, "results", "thermal_gauge.csv")) as fh:
    gr = list(csv.DictReader(fh))

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))

scale = 1e5
ax1.plot(cv[:, 0], scale * cv[:, hc.index("highT_Landau")], color="C1", ls="--", lw=1.5, label="high-$T$ one loop")
ax1.plot(cv[:, 0], scale * cv[:, hc.index("exactJB_Landau")], color="0.3", ls=":", lw=1.5, label=r"exact $J_B$")
ax1.plot(cv[:, 0], scale * cv[:, hc.index("daisy_Landau")], color="C0", ls="-", lw=1.5, label="with daisy")
ax1.axhline(0, color="0.55", lw=0.6)
ax1.set_xlim(0, 0.75)
ax1.set_ylim(-1.5, 9)
ax1.set_xlabel(r"$\phi/T_c$")
ax1.set_ylabel(r"$10^5\,[V(\phi,T_c)-V(0,T_c)]/T_c^4$")
ax1.legend(loc="upper left", fontsize=8)

es = sorted({float(r["e"]) for r in gr})
land = {float(r["e"]): float(r["phic_Tc"]) for r in gr if r["gauge"] == "Landau"}
for g, xi, col, mk, ls in (("background R_xi", "1.", "C0", "s", "-"), ("background R_xi", "3.", "C0", "D", "--"),
                           ("Fermi", "1.", "C1", "s", "-"), ("Fermi", "3.", "C1", "D", "--")):
    # rows with a deeper xi-induced minimum at small phi are left out (e = 1/2, xi = 3)
    pts = sorted((float(r["e"]), abs(float(r["phic_Tc"]) / land[float(r["e"])] - 1)) for r in gr
                 if r["gauge"] == g and r["xi"] == xi and float(r["deeper_min_phi_over_Tc"]) == 0)
    x, y = np.array(pts).T
    ax2.loglog(x, y, marker=mk, color=col, ls=ls, lw=1.2, ms=4, mfc="none" if mk == "D" else col)
xx = np.array([1 / 32, 1 / 2])
ax2.loglog(xx, 0.11 * (xx / 0.5) ** 2, color="0.55", lw=0.7, ls=":")
ax2.loglog(xx, 0.09 * (xx / 0.5) ** 0.75, color="0.55", lw=0.7, ls=":")
ax2.set_xlim(0.025, 0.6)
ax2.set_ylim(1e-5, 0.3)
ax2.set_xticks([1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2])
ax2.set_xticklabels([r"$\frac{1}{32}$", r"$\frac{1}{16}$", r"$\frac{1}{8}$", r"$\frac{1}{4}$", r"$\frac{1}{2}$"])
ax2.xaxis.set_minor_formatter(plt.NullFormatter())
ax2.set_xlabel(r"$e$ ($\lambda=e^3/4$)")
ax2.set_ylabel(r"$|(\phi_c/T_c)/(\phi_c/T_c)_{\mathrm{Landau}}-1|$")
ax2.text(0.028, 0.06, r"Fermi: $\propto e^{3/4}$", fontsize=8)
ax2.text(0.045, 1.4e-5, r"background $R_\xi$: $\propto e^2$", fontsize=8)
ax2.text(0.20, 2.0e-4, r"solid $\xi=1$" + "\n" + r"dashed $\xi=3$", fontsize=8)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "thermal.pdf"))
print("written ../figs/thermal.pdf")
