# %% [markdown]
# # Step (7): figure of the gauge dependence of the one-loop effective potential
#
# Research note models/abelian_higgs, step (7).  Reads results/effpot_curves.csv and results/effpot_hbar.csv (from
# effpot.wl) and draws ../figs/effpot.pdf:
#   left : V1(xi; phi) - V1(Landau; phi) against phi/v for background R_xi and Fermi gauges (xi = 1, 3).  By the Nielsen
#          identity the difference is proportional to dV0/dphi and vanishes at the tree minimum phi = v;
#   right: (phi_min - v)/hbar of V0 + hbar V1 against hbar.  Background R_xi and Landau tend to T/MH^2 (the beta_t
#          shift of the vev, gauge dependent); Fermi gauge drifts like ln hbar, with the leading-order solution.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python effpot_plot.py

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


def read(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        rows = list(csv.reader(fh))
    return rows[0], np.array([[float(x) for x in r] for r in rows[1:]])


hc, curves = read("effpot_curves.csv")
hh, hbar = read("effpot_hbar.csv")
with open(os.path.join(HERE, "results", "effpot.csv")) as fh:
    tab = list(csv.reader(fh))
t_over_mh2 = {float(r[0]): float(r[2]) for r in tab[1:5]}          # Delta v = T/MH^2 for xi = 1/2, 1, 3, 10
t_landau = hbar[-1, hh.index("dphi_over_hbar_Landau")]               # hbar -> 0 value, Landau

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
C_B, C_F, C_L = "C0", "C1", "k"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))

x = curves[:, 0]
scale = 1e3
ax1.plot(x, scale * curves[:, hc.index("dV_bRxi_xi1")], color=C_B, ls="-", lw=1.5)
ax1.plot(x, scale * curves[:, hc.index("dV_bRxi_xi3")], color=C_B, ls="--", lw=1.5)
ax1.plot(x, scale * curves[:, hc.index("dV_Fermi_xi1")], color=C_F, ls="-", lw=1.5)
ax1.plot(x, scale * curves[:, hc.index("dV_Fermi_xi3")], color=C_F, ls="--", lw=1.5)
ax1.axhline(0, color="0.55", lw=0.6)
ax1.axvline(1, color="0.55", lw=0.8, ls=":")
ax1.set_xlim(0.85, 1.15)
ax1.set_ylim(-6.5, 10.5)
ax1.set_xlabel(r"$\phi/v$")
ax1.set_ylabel(r"$10^3\,[V_1(\xi)-V_1(\mathrm{Landau})]$")
ax1.text(0.858, 5.0, r"background $R_\xi$", color="k", fontsize=8)
ax1.text(0.858, -6.0, "Fermi", color="k", fontsize=8)
ax1.text(1.035, -5.6, r"solid $\xi=1$, dashed $\xi=3$", color="0.35", fontsize=8)

h = hbar[:, 0]
ax2.semilogx(h, hbar[:, hh.index("dphi_over_hbar_bRxi1")], "o-", color=C_B, ms=4, lw=1.2)
ax2.semilogx(h, hbar[:, hh.index("dphi_over_hbar_Fermi1")], "s-", color=C_F, ms=4, lw=1.2)
ax2.semilogx(h, hbar[:, hh.index("dphi_over_hbar_Fermi1_leading")], color=C_F, ls=":", lw=1.0)
ax2.semilogx(h, hbar[:, hh.index("dphi_over_hbar_Landau")], "^-", color=C_L, ms=4, lw=1.0)
ax2.axhline(t_over_mh2[1.0], color=C_B, lw=0.6, ls=":")
ax2.axhline(t_landau, color="0.45", lw=0.6, ls=":")
ax2.set_xlim(1.5e-4, 1.5)
ax2.invert_xaxis()
ax2.set_xlabel(r"$\hbar$")
ax2.set_ylabel(r"$(\phi_{\min}-v)/\hbar$")
ax2.text(1.0, -0.0218, r"background $R_\xi$, $\xi=1$", color="k", fontsize=8)
ax2.text(1.0, -0.0251, "Landau", color="k", fontsize=8)
ax2.text(2.5e-2, -0.0328, r"Fermi, $\xi=1$", color="k", fontsize=8)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "effpot.pdf"))
print("written ../figs/effpot.pdf")
