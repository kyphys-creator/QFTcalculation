# %% [markdown]
# # Step (9): where the general form reaches LISA, scanning D and T0
#
# Research note models/phi34_thermal, step (9).  Steps (2), (3) scanned E and lambda_T with D and T0 fixed at their SM-like
# values; here D and T0 move as well.  At fixed (E, lambda_T) the nucleation value alpha_n = alpha(T_n) depends on D and
# T0 only through the logarithm in Gamma = H^4, while
#   alpha_theta = (15/(9 pi^2 g*)) (E^4/lambda_T^3) alpha_n^2 f_-(alpha_n)^2 (R - alpha_n),
#   beta/H      = (S3/T) [3/(2 alpha_n) + W/S3] 2 (R - alpha_n),       R = lambda_T D/E^2 > 9/8,
# so D sets the strength and the speed together, and T0 (with T_n^2 = T0^2/(1 - alpha_n/R)) sets the frequency.  A larger
# D also allows a larger E (R > 9/8), i.e. more supercooling (smaller alpha_n, larger phi_n/T_n).
# Checks: the scalings above against tptlib.DineForm.  Scan A: (D, T0) for the (E, lambda_T) of BP1-BP4.  Scan B: (E, D)
# for lambda_T = 0.02, 0.05, 0.1146 (SM), with T0 chosen to maximise the SNR.  SNR for LISA with v_w = 0.95 and 0.44
# (sound waves + turbulence, step (3)).  g* = 106.75 throughout (note, premise 2).
# Writes results/lisa_scan.csv and ../figs/lisa_scan.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python lisa_scan.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

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

step1 = {r[0]: float(r[1]) for r in csv.reader(open(os.path.join(HERE, "results", "dine_form.csv"))) if r and r[0] != "quantity"
         and r[0] in ("D", "T0")}
D_SM, T0_SM = step1["D"], step1["T0"]
rows = list(csv.reader(open(os.path.join(HERE, "results", "strong_pt.csv"))))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
bench = [dict(name=r[0], **dict(zip(keys, map(float, r[1:])))) for r in rows[ib + 1:] if r and r[0].startswith("BP")]
print("D_SM =", D_SM, " T0_SM =", T0_SM, " benchmarks:", [(b["name"], b["lam"], round(b["E"], 6)) for b in bench])


def point(E, lam, D, T0, vw=0.95):
    """Nucleation, strength, speed, peak frequency and LISA SNR of the general form; None if there is no nucleation."""
    m = tl.DineForm(D, E, T0, lam)
    Tn = m.nucleation()
    if Tn is None:
        return None
    s = m.summary(Tn)
    g = tl.GWSource(s["alpha_theta"], s["betaH"], Tn, vw)
    s.update(D=D, T0=T0, R=m.R, fp=g.fp, snr=tl.snr(g.h2_total), K=g.K)
    return s


# %% [markdown]
# ## Checks: regression against BP4 of step (2), and the scalings in D at fixed (E, lambda_T)

# %%
b4 = bench[-1]
s = point(b4["E"], b4["lam"], D_SM, T0_SM)
print(f"BP4 regression: alpha_theta {s['alpha_theta']:.10g} vs {b4['alpha_theta']:.10g}, beta/H {s['betaH']:.10g} vs "
      f"{b4['betaH']:.10g}, SNR {s['snr']:.6g} (step (3): 0.0140)")
ref = s
for fac in (3.0, 30.0):
    t = point(b4["E"], b4["lam"], fac * D_SM, T0_SM)
    sc = (t["R"] - t["alpha_n"]) / (ref["R"] - ref["alpha_n"])
    pred_a = ref["alpha_theta"] * sc * (t["alpha_n"] * tl.fminus(t["alpha_n"]) / (ref["alpha_n"] * tl.fminus(ref["alpha_n"]))) ** 2
    pred_b = (t["S3T"] * (1.5 / t["alpha_n"] + tl.w3(t["alpha_n"]) / tl.s3(t["alpha_n"])) * 2 * (t["R"] - t["alpha_n"]))
    print(f"D = {fac:g} D_SM: alpha_n {t['alpha_n']:.6f} (BP4 {ref['alpha_n']:.6f});  alpha_theta {t['alpha_theta']:.6e} vs scaling "
          f"{pred_a:.6e} (rel. {t['alpha_theta'] / pred_a - 1:.1e});  beta/H {t['betaH']:.6e} vs formula {pred_b:.6e};  "
          f"T_n/T0 {t['Tn'] / T0_SM:.6f} vs (1 - alpha_n/R)^(-1/2) {1 / math.sqrt(1 - t['alpha_n'] / t['R']):.6f}")


# %% [markdown]
# ## Scan in (D, T0) for the (E, lambda_T) of BP1-BP4

# %%
NG = 61
T0S = np.geomspace(0.3, 3e4, NG)
grids, out = {}, []
for b in bench:
    Dmin = 1.0005 * 9 / 8 * b["E"] ** 2 / b["lam"]                  # R > 9/8
    DS = np.geomspace(Dmin, 300 * D_SM, NG)
    for vw in (0.95, 0.44):
        Z = np.full((NG, NG), np.nan)
        for i, T0 in enumerate(T0S):
            for j, D in enumerate(DS):
                p = point(b["E"], b["lam"], D, T0, vw)
                if p is not None:
                    Z[i, j] = p["snr"]
        grids[(b["name"], vw)] = (DS, Z)
        # smallest D with SNR = 10 at each T0, and the overall smallest
        best = None
        for i, T0 in enumerate(T0S):
            k = np.where(Z[i] >= 10)[0]
            if len(k) and (best is None or DS[k[0]] < best[0]):
                best = (DS[k[0]], T0)
        if best is None:
            out.append(dict(name=b["name"], vw=vw, D10=float("nan")))
            print(f"{b['name']} v_w = {vw}: SNR < 10 in the whole scan (max {np.nanmax(Z):.3g})")
            continue
        D10 = brentq(lambda D: math.log(point(b["E"], b["lam"], D, best[1], vw)["snr"] / 10), Dmin, best[0] * 1.2)
        p = point(b["E"], b["lam"], D10, best[1], vw)
        p.update(name=b["name"], vw=vw, D10=D10, D10_over_DSM=D10 / D_SM)
        out.append(p)
        print(f"{b['name']} v_w = {vw}: SNR = 10 first at D = {D10:.4g} ({D10 / D_SM:.3g} D_SM), T0 = {best[1]:.3g} GeV: "
              f"alpha_theta {p['alpha_theta']:.3g}, beta/H {p['betaH']:.3g}, T_n {p['Tn']:.3g} GeV, f_p {p['fp'] * 1e3:.3g} mHz;  "
              f"max SNR in the scan {np.nanmax(Z):.3g}")


# %% [markdown]
# ## Scan B: (E, D) at fixed lambda_T, T0 chosen for the largest SNR

# %%
from scipy.optimize import minimize_scalar
E_SM = float([r for r in csv.reader(open(os.path.join(HERE, "results", "dine_form.csv"))) if r and r[0] == "E"][0][1])
LAMS = (0.02, 0.05, 0.11457239619981101)


def best_T0(E, lam, D, vw=0.95):
    """The point with the T0 (0.1 GeV - 100 TeV) that maximises the SNR."""
    def f(lt):
        p = point(E, lam, D, math.exp(lt), vw)
        return 700.0 if p is None else -math.log(max(p["snr"], 1e-300))
    r = minimize_scalar(f, bounds=(math.log(0.1), math.log(1e5)), method="bounded", options={"xatol": 1e-3})
    return point(E, lam, D, math.exp(r.x), vw)


NB = 49
ES = np.geomspace(1.0, 60.0, NB) * E_SM
DB = np.geomspace(0.1, 300.0, NB) * D_SM
gridsB, outB = {}, []
for lam in LAMS:
    for vw in (0.95, 0.44):
        Z = np.full((NB, NB), np.nan)
        for i, D in enumerate(DB):
            for j, E in enumerate(ES):
                if lam * D / E ** 2 > 1.0005 * 9 / 8:
                    p = best_T0(E, lam, D, vw)
                    if p is not None:
                        Z[i, j] = p["snr"]
        gridsB[(lam, vw)] = Z
        # along R = 9/8 (the smallest D for each E, where the SNR is largest): the smallest E with SNR = 10
        g = lambda E: math.log(best_T0(E, lam, 1.0005 * 9 / 8 * E * E / lam, vw)["snr"] / 10)
        Eg = [E for E in ES if best_T0(E, lam, 1.0005 * 9 / 8 * E * E / lam, vw) is not None]
        k = next((n for n in range(1, len(Eg)) if g(Eg[n - 1]) < 0 <= g(Eg[n])), None)
        if k is None:
            print(f"lambda_T = {lam:.4f}, v_w = {vw}: no SNR = 10 along R = 9/8")
            continue
        E10 = brentq(g, Eg[k - 1], Eg[k], xtol=1e-10)
        p = best_T0(E10, lam, 1.0005 * 9 / 8 * E10 * E10 / lam, vw)
        p.update(name=f"R=9/8, lambda_T={lam:.4g}", vw=vw, E=E10, E_over_ESM=E10 / E_SM, D10=p["D"], D10_over_DSM=p["D"] / D_SM)
        outB.append(p)
        print(f"lambda_T = {lam:.4f}, v_w = {vw}: SNR = 10 from E = {E10:.4g} ({E10 / E_SM:.3g} E_SM), D = {p['D']:.3g} "
              f"({p['D'] / D_SM:.3g} D_SM), best T0 = {p['T0']:.3g} GeV (T_n {p['Tn']:.3g}):  alpha_n {p['alpha_n']:.3f}, "
              f"phi_n/T_n {p['phin_Tn']:.3g}, alpha_theta {p['alpha_theta']:.3g}, beta/H {p['betaH']:.4g}, f_p {p['fp'] * 1e3:.3g} mHz;  "
              f"max SNR in the plane {np.nanmax(Z):.3g}")


# %% [markdown]
# ## Inspect: the BP4 plane (v_w = 0.95)

# %%
DS, Z = grids[("BP4", 0.95)]
i0 = int(np.argmin(abs(np.log(T0S / T0_SM))))
print("SNR along D at T0 = T0_SM:", [f"{D / D_SM:.3g}:{z:.2g}" for D, z in zip(DS[::10], Z[i0, ::10])])
i1 = int(np.argmin(abs(np.log(T0S / 3.0))))
print("SNR along D at T0 = 3 GeV:", [f"{D / D_SM:.3g}:{z:.2g}" for D, z in zip(DS[::10], Z[i1, ::10])])


# %% [markdown]
# ## Output and figure

# %%
cols = ["name", "vw", "D10", "D10_over_DSM", "T0", "Tn", "R", "alpha_n", "alpha_theta", "alpha_e", "betaH", "phin_Tn", "K", "fp",
        "snr"]
with open(os.path.join(HERE, "results", "lisa_scan.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(cols)
    for r in out:
        wr.writerow([r.get(c, "") for c in cols])
    wr.writerow([])
    colsB = ["name", "vw", "E", "E_over_ESM", "D10", "D10_over_DSM", "T0", "Tn", "R", "alpha_n", "alpha_theta", "alpha_e", "betaH",
             "phin_Tn", "K", "fp", "snr"]
    wr.writerow(colsB)
    for r in outB:
        wr.writerow([r.get(c, "") for c in colsB])
    wr.writerow([])
    wr.writerow(["check", "value", "reference"])
    wr.writerow(["BP4_snr_regression", ref["snr"], 0.0140])
    wr.writerow(["D_SM", D_SM, ""])
    wr.writerow(["T0_SM", T0_SM, ""])

import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.55))
ax = axs[0]
DS, Z = grids[("BP4", 0.95)]
cs = ax.contour(DS / D_SM, T0S, np.log10(Z), levels=[-6, -4, -2, -1], colors="k", linewidths=0.7, linestyles="solid")
ax.clabel(cs, fmt=lambda v: rf"$10^{{{int(v)}}}$", fontsize=6, inline_spacing=2)
im, jm = np.unravel_index(np.nanargmax(Z), Z.shape)
ax.plot([DS[jm] / D_SM], [T0S[im]], marker="x", ms=4, color="k")
ax.annotate(f"max {np.nanmax(Z):.2f}", (DS[jm] / D_SM, T0S[im]), xytext=(4, -8), textcoords="offset points", fontsize=6)
ax.plot([1], [T0_SM], marker="o", ms=3, color="#eb6235")
ax.annotate("BP4", (1, T0_SM), xytext=(4, 3), textcoords="offset points", fontsize=6, color="#eb6235")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$D/D_{\mathrm{SM}}$")
ax.set_ylabel(r"$T_0$ [GeV]")
ax.set_title(r"(a) SNR, $(E,\lambda_T)$ of BP4", fontsize=7)
ax = axs[1]
lam = 0.05
Z = gridsB[(lam, 0.95)]
cs = ax.contour(ES / E_SM, DB / D_SM, np.log10(Z), levels=[-8, -4, -2, 0, 1, 2], colors="k", linewidths=0.7, linestyles="solid")
ax.clabel(cs, fmt=lambda v: rf"$10^{{{int(v)}}}$", fontsize=6, inline_spacing=2)
ax.fill_between(ES / E_SM, DB[0] / D_SM, np.clip(9 / 8 * ES ** 2 / lam / D_SM, DB[0] / D_SM, DB[-1] / D_SM), color="0.85", lw=0)
ax.text(30, 0.4, r"$R<9/8$", fontsize=6, ha="center", color="0.35")
ax.axhline(1.0, color="#5d81b4", ls=":", lw=0.9)
for bb, col in zip(bench[:3], ("#5d81b4", "#e09b24", "#8eb031")):
    ax.plot([bb["E"] / E_SM], [1.0], marker="o", ms=2.5, color=col)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$E/E_{\mathrm{SM}}$")
ax.set_ylabel(r"$D/D_{\mathrm{SM}}$")
ax.set_ylim(DB[0] / D_SM, DB[-1] / D_SM)
ax.set_title(r"(b) largest SNR over $T_0$, $\lambda_T=0.05$", fontsize=7)
ax = axs[2]
for lam, col in zip(LAMS, ("#eb6235", "#5d81b4", "k")):
    for vw, ls in ((0.95, "-"), (0.44, "--")):
        Z = gridsB[(lam, vw)]
        if np.nanmax(Z) >= 10:
            ax.contour(ES / E_SM, DB / D_SM, np.log10(Z), levels=[1], colors=[col], linewidths=1.0, linestyles=[ls])
    ax.plot(ES / E_SM, 9 / 8 * ES ** 2 / lam / D_SM, color=col, ls=":", lw=0.7)
    ax.plot([], [], color=col, ls="-", lw=1.0, label=rf"$\lambda_T={lam:.3g}$")
ax.plot([], [], color="0.4", ls="--", lw=1.0, label=r"$v_w=0.44$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(ES[0] / E_SM, ES[-1] / E_SM)
ax.set_ylim(DB[0] / D_SM, DB[-1] / D_SM)
ax.set_xlabel(r"$E/E_{\mathrm{SM}}$")
ax.set_ylabel(r"$D/D_{\mathrm{SM}}$")
ax.set_title("(c) SNR = 10; dotted: $R=9/8$", fontsize=7)
ax.legend(loc="lower right", fontsize=6, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "lisa_scan.pdf"))
print("wrote results/lisa_scan.csv and figs/lisa_scan.pdf")
