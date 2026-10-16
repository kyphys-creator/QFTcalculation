# %% [markdown]
# # Step (9): the partonic functions f0, f1, fbar1 against eta_s = s/4m^2 - 1 (figs/hq_f.pdf)
#
# Research note models/qcd, step (9).  f1: this work (results/hq_f1_<chan>.csv, points) and the exact result of Czakon-Mitov at the
# nodes of hq_hadronic.py (results/hq_cm_nodes.csv of hq_cm.wl, line); f0, fbar1 (Eq. (hqfbar)), threshold expansions (Eq. (hqthr))
# and the high-energy limits of f1_gg, f1_qg (Czakon-Mitov) from hq_lib.py.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python hq_plot.py

# %%
import os, sys, csv, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fractions import Fraction
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
sys.path.insert(0, HERE)
import hq_lib as H
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
chans = ("qq", "gg", "qg")
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6))
eta = np.logspace(-3, 3.2, 300); rho = 1/(1 + eta)
for ax, c, title in zip(axs, ("qq", "gg", "qg"), (r"$q\bar q$", r"$gg$", r"$qg$")):
    f0 = {"qq": H.f0_qq, "gg": H.f0_gg}.get(c)
    fb = {"qq": H.fbar_qq, "gg": H.fbar_gg, "qg": H.fbar_qg}[c]
    if f0: ax.plot(eta, [float(f0(r)) for r in rho], "-", color="C0", label=r"$f^{(0)}$")
    ax.plot(eta, [float(fb(r)) for r in rho], "--", color="C2", label=r"$\bar f^{(1)}$")
    thr = {"qq": H.thr_qq, "gg": H.thr_gg}.get(c)
    if thr:
        e2 = eta[eta < 0.3]; ax.plot(e2, [float(thr(np.sqrt(1 - 1/(1 + e)))) for e in e2], ":", color="C3", label="threshold")
    if c in chans:
        pts = []
        for r in csv.DictReader(open(os.path.join(HERE, "results", f"hq_f1_{c}.csv"))):
            s = float(Fraction(r["s"])); pts.append((s/4 - 1, float(r["f1"])))
        pts.sort(); ax.plot([p[0] for p in pts], [p[1] for p in pts], "o", ms=2.5, color="C1", label=r"$f^{(1)}$")
        cmf = os.path.join(HERE, "results", "hq_cm_nodes.csv")
        if os.path.exists(cmf):
            ex = sorted((1/float(r["rho"]) - 1, float(r["f1_cm"])) for r in csv.DictReader(open(cmf)) if r["chan"] == c)
            ax.plot([p[0] for p in ex], [p[1] for p in ex], "-", lw=0.7, color="C1", label=r"$f^{(1)}$ (CM)")
    if c in ("gg", "qg"):
        ax.axhline(float(H.he_gg() if c == "gg" else H.he_gq()), color="C1", lw=0.6, ls=(0, (1, 2)))
        ax.set_ylim(top=1.08*float(H.he_gg() if c == "gg" else H.he_gq()))
    ax.set_xscale("log"); ax.set_xlabel(r"$\eta_s=s/4m^2-1$"); ax.set_title(title, fontsize=9); ax.axhline(0, color="k", lw=0.4)
axs[0].legend(fontsize=6.5, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "hq_f.pdf"))
print("wrote ../figs/hq_f.pdf")
