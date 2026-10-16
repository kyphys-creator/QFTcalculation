# %% [markdown]
# # Step (10): figure figs/inst.pdf
#
# Research note models/qcd, step (10).  (a) Gamma~(m rho) of the isospin-1/2 scalar (Gel'fand-Yaglom, results/inst_gy.csv) with the small- and
# large-mass expansions; (b) lattice BPST: S_W/(8 pi^2) and the clover charge minus the continuum sums, against (a/rho)^2, with -(1/5)(a/rho)^2 and
# -(4/5)(a/rho)^2 (results/inst_lattice.csv); (c) the SU(3) instanton density d(rho) and chi(rho_c)^(1/4) (results/inst_density.csv).
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python inst_plot.py

# %%
import csv, os, sys
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
sys.path.insert(0, HERE)
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
def load(name):
    rows = list(csv.DictReader(open(os.path.join(HERE, "results", name))))
    return {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}
from inst_gy import small_m, large_m
g = load("inst_gy.csv"); lat = load("inst_lattice.csv"); de = load("inst_density.csv")

fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.5))
ax = axs[0]
mm = np.geomspace(0.02, 10, 300)
ax.plot(mm[mm < 1.2], small_m(mm[mm < 1.2]), "--", color="C2", lw=1, label="small $m\\rho$")
ax.plot(mm[mm > 1.0], large_m(mm[mm > 1.0]), ":", color="C3", lw=1.2, label="large $m\\rho$")
ax.plot(g["m_rho"], g["Gamma_tilde"], "o", ms=3, color="C0", label="Gel'fand--Yaglom")
ax.set_xscale("log"); ax.set_xlabel(r"$m\rho$"); ax.set_ylabel(r"$\tilde\Gamma^S(m\rho)$"); ax.legend(fontsize=6.5, loc="lower left")
ax = axs[1]
a2 = lat["a_over_rho"]**2; x = np.linspace(0, 0.27, 50)
ax.plot(a2, lat["S_W_over_8pi2"] - lat["S_continuum_same_plaquettes"], "o", ms=3, color="C0", label=r"$S_W/8\pi^2$")
ax.plot(x, -x/5, "-", color="C0", lw=0.8)
ax.plot(a2, lat["Q_clover"] - lat["Q_continuum_same_sites"], "s", ms=3, color="C1", label=r"$Q_{\rm clover}$")
ax.plot(x, -4*x/5, "-", color="C1", lw=0.8)
ax.axhline(0, color="k", lw=0.4)
ax.set_xlabel(r"$(a/\rho)^2$"); ax.set_ylabel("lattice $-$ continuum"); ax.legend(fontsize=6.5, loc="lower left")
ax = axs[2]
ax.semilogy(de["rho_fm"], de["d_fm-5"], "-", color="C0", label=r"$d(\rho)$ [fm$^{-5}$]")
ax.set_xlabel(r"$\rho$ [fm]"); ax.set_ylabel(r"$d(\rho)$ [fm$^{-5}$]")
ax2 = ax.twinx(); ax2.plot(de["rho_fm"], de["chi_quarter_MeV"], "--", color="C1")
ax2.axhline(191, color="C1", lw=0.5, ls=":"); ax2.set_ylabel(r"$\chi(\rho_c)^{1/4}$ [MeV]", color="C1")
ax2.spines["right"].set_visible(True); ax2.tick_params(axis="y", colors="C1")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "inst.pdf"))
print("wrote ../figs/inst.pdf")
