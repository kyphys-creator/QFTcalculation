# %% [markdown]
# # Step (4): the minimum value in the Fermi and background-field R_xi gauges (figure)
#
# Research note models/abelian_higgs_2loop, step (4).  Reads results/fermi_min.csv (fermi_v2.wl) and draws
# figs/fermi.pdf:
#   left:  V_min(xi) - V_min(hbar) at the benchmark (Q = 1), the fixed-order potential minimized numerically at one and
#          two loops in both gauges (V_min(hbar): the gauge-independent hbar expansion at the same loop order);
#   right: |V_min - V_min(hbar)| at two loops with the couplings scaled by s (lam -> s lam, e^2 -> s e^2): s^2 in the
#          background-field R_xi gauge, s in the Fermi gauge.
# Usage (from Src/, after fermi_v2.wl):  ~/miniforge3/envs/qft/bin/python fermi_plot.py

# %%
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()

with open(os.path.join(HERE, "results", "fermi_min.csv")) as fh:
    rows = list(csv.reader(fh))
split = [i for i, r in enumerate(rows) if r and r[0] == "gauge"]
scan = [r for r in rows[split[0] + 1:split[1]]]
scl = [r for r in rows[split[1] + 1:]]

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
style = {("R", "2"): ("C0", "-", r"background $R_\xi$, 2-loop"), ("F", "2"): ("C1", "-", "Fermi, 2-loop"),
         ("R", "1"): ("C0", "--", r"background $R_\xi$, 1-loop"), ("F", "1"): ("C1", "--", "Fermi, 1-loop")}
for (g, n), (col, ls, lab) in style.items():
    pts = sorted((float(r[2]), float(r[5])) for r in scan if r[0] == g and r[1] == n)
    ax1.semilogx([p[0] for p in pts], [1e3 * p[1] for p in pts], color=col, ls=ls, lw=1.3, marker="o", ms=3,
                 label=lab)
for r in scan:
    if r[0] == "L":
        ax1.axhline(1e3 * float(r[5]), color="0.55", lw=0.6, ls=":" if r[1] == "1" else "-.")
ax1.axhline(0, color="0.3", lw=0.5)
ax1.set_ylim(-12, 2)
ax1.set_xlabel(r"$\xi$")
ax1.set_ylabel(r"$10^3\,[V_{\min}-V_{\min}^{(\hbar)}]$")
ax1.legend(loc="lower left", fontsize=7)

for g, x, col, mk in (("R", "3.", "C0", "o"), ("F", "3.", "C1", "s"), ("F", "10.", "C1", "^"), ("R", "10.", "C0", "v")):
    pts = sorted((float(r[2]), abs(float(r[5]))) for r in scl if r[0] == g and r[1] == x)
    lab = (r"background $R_\xi$" if g == "R" else "Fermi") + r", $\xi=%s$" % x.rstrip(".")
    ax2.loglog([p[0] for p in pts], [p[1] for p in pts], color=col, ls="none", marker=mk, ms=4,
               mfc="none" if x == "10." else col, label=lab)
s = [2.0 ** -k for k in range(6)]
ax2.loglog(s, [6e-4 * t for t in s], color="0.5", lw=0.7, ls="--", label=r"$\propto s$")
ax2.loglog(s, [3e-4 * t * t for t in s], color="0.5", lw=0.7, ls=":", label=r"$\propto s^2$")
ax2.set_xlabel(r"$s$ (couplings $\lambda\to s\lambda$, $e^2\to se^2$)")
ax2.set_ylabel(r"$|V_{\min}-V_{\min}^{(\hbar)}|$, 2-loop")
ax2.legend(loc="lower right", fontsize=7)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "fermi.pdf"))
print("written figs/fermi.pdf")
