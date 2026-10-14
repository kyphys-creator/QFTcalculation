# %% [markdown]
# # Step (5): a generic bounce solver, and the thermal stability of the false vacuum phi = 0 of the single-field model
#
# Research note models/phi34_thermal, step (5).  tptlib.bounce solves the O(d) bounce of any potential by overshoot/
# undershoot (start from the linearised solution near the true minimum; bisection in ln(phi(0) - phi_t)).
# Checks: the zero-temperature note's S_3(alpha), S_4(alpha) (results/bounce.csv of models/phi34); Derrick's relation
# (d - 2) T + d U = 0; step (1) and the benchmarks of step (2) (S_3/T from the Hermite interpolation of S_3(alpha)).
# Physics: for alpha < 1 the present vacuum phi = 0 is false.  Below T_sp (step (4)) it is a local minimum of the thermal
# potential, and it decays thermally with Gamma = T^4 (S_3/2 pi T)^(3/2) e^(-S_3/T).  S_3/T falls to 0 at T_sp and grows
# as T decreases, so phi = 0 survives a radiation era only if the highest temperature lies below T_dec, Gamma(T_dec) = H^4.
# Units of step (4): chi in m^2/g, tau = g T/m^2, S_3/T = S_hat/((g/m) tau); m = m_h = 125.25 GeV, g* = 106.75;
# g/m = 1.5261 kappa_3, alpha = kappa_4/kappa_3^2.  Main potential: high T + daisy (Eq. (13)); checked by the full one loop.
# Writes results/stability_single.csv and ../figs/stability_single.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python stability_single.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import tptlib as tl

GM1, MH = 1.5261, 125.25
gm_of = lambda al, k4=1.0: GM1 * math.sqrt(k4 / al)
chk = []
ZT = os.path.join(HERE, "..", "..", "phi34", "Src", "results")


# %% [markdown]
# ## (a) The generic solver against the zero-temperature note (tree potential v = f^2/2 + f^3/6 + alpha f^4/72)

# %%
with open(os.path.join(ZT, "bounce.csv")) as fh:
    zt = {(int(r[0]), float(r[1])): float(r[3]) for r in csv.reader(fh) if r and r[0] in ("3", "4")}
for d in (3, 4):
    for a in (0.5, 0.8, 0.9, 0.95):
        V = lambda f, a=a: f * f / 2 + f ** 3 / 6 + a * f ** 4 / 72
        dV = lambda f, a=a: f + f * f / 2 + a * f ** 3 / 18
        b = tl.bounce(V, dV, 0.0, -9 / (2 * a) * (1 + math.sqrt(1 - 8 * a / 9)), d=d)
        print(f"d = {d}, alpha = {a}: S = {b['S']:.10f} vs zero-T note {zt[(d, a)]:.10f} (rel. {b['S'] / zt[(d, a)] - 1:+.1e}); "
              f"Derrick (2T/d)/S - 1 = {b['S_derrick'] / b['S'] - 1:+.1e}")
        chk.append((f"zeroT_S{d}_alpha{a}", b["S"], zt[(d, a)]))


# %% [markdown]
# ## (b) Step (1) and the benchmarks of step (2): S_3/T of the Dine form at T_n, directly

# %%
with open(os.path.join(HERE, "results", "dine_form.csv")) as fh:
    step1 = {r[0]: float(r[1]) for r in csv.reader(fh) if r[0] != "quantity"}
with open(os.path.join(HERE, "results", "strong_pt.csv")) as fh:
    rows = list(csv.reader(fh))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
pts = [("SM-like", step1["lambda_T_Tc"], step1["E"], step1["Tn"], step1["S3_over_T_n"])]
pts += [(r[0],) + tuple(float(r[1 + keys.index(k)]) for k in ("lam", "E", "Tn", "S3T")) for r in rows[ib + 1:ib + 5]]
for name, lam, E, Tn, s3t in pts:
    dm = tl.DineForm(step1["D"], E, step1["T0"], lam)
    V = lambda p: dm.V(p, Tn)
    dV = lambda p: 2 * dm.D * (Tn * Tn - dm.T0 ** 2) * p - 3 * dm.E * Tn * p * p + dm.lam * p ** 3
    a = dm.alpha(Tn)
    b = tl.bounce(V, dV, 0.0, -(a * dm.E * Tn / (3 * dm.lam)) * tl.fminus(a), d=3)
    print(f"{name}: alpha(T_n) = {a:.4f}, S_3/T generic {b['S'] / Tn:.6f}, interpolated S_3(alpha) {s3t:.6f} "
          f"(rel. {s3t / (b['S'] / Tn) - 1:+.1e}), Derrick {b['S_derrick'] / b['S'] - 1:+.1e}")
    chk.append((f"S3T_{name}", b["S"] / Tn, s3t))


# %% [markdown]
# ## (c) S_3/T of the thermal decay of phi = 0 (kappa_4 = 1), high T + daisy and full one loop

# %%
curves = {}
for al in (0.5, 0.7, 0.9):
    sf = tl.SingleField(al, gm_of(al))
    tsp = sf.tau_spinodal("ht")
    taus = np.concatenate([np.linspace(0.6, 0.9 * tsp, 22), np.linspace(0.9 * tsp, 0.985 * tsp, 6)[1:]])
    curves[al] = (tsp, [(t, sf.s3T(t, "ht")[0]) for t in taus])
    for t in (0.8, 0.5 * tsp, 0.9 * tsp):
        h_, f_ = sf.s3T(t, "ht")[0], sf.s3T(t, "full")[0]
        print(f"alpha = {al}: tau = {t:.4f} (T = {t / sf.gm:.4f} m): S_3/T high T + daisy {h_:.6f}, full one loop {f_:.6f} "
              f"(rel. {h_ / f_ - 1:+.1e})")
        chk.append((f"s3T_ht_vs_full_alpha{al}_tau{t:.3f}", h_, f_))


# %% [markdown]
# ## (d) T_dec and T_sp along kappa_3 at kappa_4 = 0.5, 1, 2, 4 (up to the zero-temperature bound of the zero-T note)

# %%
with open(os.path.join(ZT, "prefactor.csv")) as fh:
    pr = list(csv.reader(fh))
ik = [k for k, r in enumerate(pr) if r and r[0] == "kappa_4"][0]
k3max = {round(float(r[0]), 3): float(r[1]) for r in pr[ik + 1:] if r}
scan = []
for k4 in (0.5, 1.0, 2.0, 4.0):
    k3s = np.linspace(math.sqrt(k4) * 1.005, k3max[k4], 9)
    for k3 in k3s:
        al = k4 / k3 ** 2
        sf = tl.SingleField(al, GM1 * k3)
        td, tsp = sf.tau_decay("ht")
        r = dict(kappa4=k4, kappa3=k3, alpha=al, gm=sf.gm, tau_dec=td, tau_sp=tsp, T_dec=td / sf.gm * MH, T_sp=tsp / sf.gm * MH)
        scan.append(r)
        print(f"kappa_4 = {k4}, kappa_3 = {k3:.4f} (alpha = {al:.4f}): T_dec = {r['T_dec']:.2f} GeV ({td / sf.gm:.4f} m), "
              f"T_sp = {r['T_sp']:.2f} GeV, T_dec/T_sp = {td / tsp:.4f}", flush=True)
# the full one loop at three points of kappa_4 = 1
for r in [s for s in scan if s["kappa4"] == 1.0][::4]:
    sf = tl.SingleField(r["alpha"], r["gm"])
    tdf = sf.tau_decay("full")[0]
    r["T_dec_full"] = tdf / sf.gm * MH
    print(f"kappa_3 = {r['kappa3']:.4f}: T_dec high T + daisy {r['T_dec']:.4f} GeV, full one loop {r['T_dec_full']:.4f} GeV "
          f"(rel. {r['T_dec'] / r['T_dec_full'] - 1:+.1e})")
    chk.append((f"T_dec_ht_vs_full_k3_{r['kappa3']:.3f}", r["T_dec"], r["T_dec_full"]))


# %% [markdown]
# ## Output and figure

# %%
keys = ["kappa4", "kappa3", "alpha", "gm", "tau_dec", "tau_sp", "T_dec", "T_sp", "T_dec_full"]
with open(os.path.join(HERE, "results", "stability_single.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(keys)
    for r in scan:
        wr.writerow([r.get(k, "") for k in keys])
    wr.writerow([])
    wr.writerow(["curve_alpha", "tau", "S3_over_T"])
    for al, (tsp, cv) in curves.items():
        for t, s in cv:
            wr.writerow([al, t, s])
    wr.writerow([])
    wr.writerow(["check", "value", "reference"])
    wr.writerows(chk)

import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1))
cols = {0.5: "#5d81b4", 0.7: "#e09b24", 0.9: "#eb6235"}
for al, (tsp, cv) in curves.items():
    gm = gm_of(al)
    ax1.plot([t / gm for t, _ in cv], [s for _, s in cv], color=cols[al], ls="-", lw=1.0, label=rf"$\alpha={al}$")
    ax1.axvline(tsp / gm, color=cols[al], ls=":", lw=0.7)
Ts = np.linspace(0.3, 4.0, 200)
thr = [brentq(lambda S: S - 1.5 * math.log(S / (2 * math.pi)) - 4 * math.log(tl.MPL / (1.66 * math.sqrt(106.75) * T * MH)), 50, 400)
       for T in Ts]
ax1.plot(Ts, thr, color="0.5", ls="--", lw=0.9, label=r"$\Gamma=H^4$")
ax1.set_yscale("log")
ax1.set_xlim(0.3, 4.6)
ax1.set_ylim(3, 3e3)
ax1.set_xlabel(r"$T/m$")
ax1.set_ylabel(r"$S_3/T$")
ax1.legend(loc="upper right", fontsize=6)
for k4, col in zip((0.5, 1.0, 2.0, 4.0), ("#5d81b4", "#e09b24", "#8eb031", "#eb6235")):
    sub = [r for r in scan if r["kappa4"] == k4]
    ax2.plot([r["kappa3"] for r in sub], [r["T_dec"] for r in sub], color=col, ls="-", lw=1.0, label=rf"$\kappa_4={k4:g}$")
    ax2.plot([r["kappa3"] for r in sub], [r["T_sp"] for r in sub], color=col, ls="--", lw=0.9)
ax2.set_xlabel(r"$\kappa_3$")
ax2.set_ylabel(r"$T$ [GeV]")
ax2.set_ylim(0, 720)
ax2.legend(loc="upper right", fontsize=6)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "stability_single.pdf"))
print("wrote results/stability_single.csv and figs/stability_single.pdf")
