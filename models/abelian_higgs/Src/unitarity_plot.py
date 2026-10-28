# %% [markdown]
# # Step (9): figure of the s-wave unitarity of the coupled channels
#
# Research note models/abelian_higgs, step (9).  Reads results/unitarity_curves.csv (unitarity_numeric.wl) and draws
# ../figs/unitarity.pdf:
#   left : the tree s wave against sqrt(s) for e = 1/10, MH = 32.5 MA (lam = 5.28): the C-even combinations (a11 + a22)/2 -+ a12 of
#          A_L A_L, h h (charge 0 and 2 at high energy, where they are the eigenvalues) and A_L h, with the lam limits
#          -lam/(4 pi), -lam/(8 pi); the departure from them is the e^2 ln s of the vector exchange;
#   right: high energy, scalar sector: |a0| and |a1| (mu^2 = s) of the charge-0 and charge-2 channels against lam,
#          a1 = a0^2 (r + i), r = 13/(2 pi) (charge 0), 14/pi (charge 2) (unitarity_oneloop.py).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python unitarity_plot.py

# %%
import csv
import math
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
with open(os.path.join(HERE, "results", "unitarity_curves.csv")) as fh:
    rows = list(csv.reader(fh))
hdr, a = rows[0], np.array([[float(x) for x in r] for r in rows[1:]])
lam_b = 0.01 * 32.5 ** 2 / 2

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))

i11, i12, i22 = hdr.index("a11"), hdr.index("a12"), hdr.index("a22")
ax1.semilogx(a[:, 0], (a[:, i11] + a[:, i22]) / 2 - a[:, i12], color="C0", ls="-", lw=1.5)
ax1.semilogx(a[:, 0], (a[:, i11] + a[:, i22]) / 2 + a[:, i12], color="C1", ls="-", lw=1.5)
ax1.semilogx(a[:, 0], a[:, hdr.index("a_Lh")], color="C1", ls="--", lw=1.5)
ax1.axhline(-lam_b / (4 * math.pi), color="C0", lw=0.7, ls=":")
ax1.axhline(-lam_b / (8 * math.pi), color="C1", lw=0.7, ls=":")
ax1.axhline(-0.5, color="0.4", lw=0.8)
ax1.set_xlim(1100, 1e6)
ax1.set_ylim(-0.55, 0)
ax1.set_xlabel(r"$\sqrt{s}/M_A$")
ax1.set_ylabel(r"$a_0$ (tree)")
ax1.text(1.3e3, -0.48, r"$-1/2$", color="0.3", fontsize=8)
ax1.text(2.5e5, -0.405, r"$-\lambda/4\pi$", color="k", fontsize=8)
ax1.text(2.5e5, -0.198, r"$-\lambda/8\pi$", color="k", fontsize=8)
ax1.text(1.3e3, -0.385, "charge 0", color="k", fontsize=8)
ax1.text(1.3e3, -0.25, r"charge 2: $A_LA_L,hh$; $A_Lh$ (dashed)", color="k", fontsize=8)

lam = np.linspace(0, 8, 400)
for col, den, r, lab in (("C0", 4, 13 / (2 * math.pi), "charge 0"), ("C1", 8, 14 / math.pi, "charge 2")):
    a0 = lam / (den * math.pi)
    a1 = a0 ** 2 * math.hypot(r, 1)
    ax2.plot(lam, a0, color=col, ls="-", lw=1.5)
    ax2.plot(lam, a1, color=col, ls="--", lw=1.5)
ax2.axhline(0.5, color="0.4", lw=0.8)
ax2.axvline(2 * math.pi, color="0.55", lw=0.8, ls=":")
ax2.set_xlim(0, 8)
ax2.set_ylim(0, 1.0)
ax2.set_xlabel(r"$\lambda$")
ax2.set_ylabel(r"$|a_0|$ (solid), $|a_1|$ (dashed)")
ax2.text(0.3, 0.53, r"$1/2$", color="0.3", fontsize=8)
ax2.text(6.4, 0.06, r"$2\pi$", color="0.3", fontsize=8)
ax2.text(3.0, 0.20, "charge 0", color="k", fontsize=8)
ax2.text(4.2, 0.07, "charge 2", color="k", fontsize=8)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "unitarity.pdf"))
print("written ../figs/unitarity.pdf")
