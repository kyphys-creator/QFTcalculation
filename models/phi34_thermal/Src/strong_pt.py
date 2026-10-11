# %% [markdown]
# # Step (2): strength and speed of the transition in the high-temperature potential of Dine et al.
#
# Research note models/phi34_thermal, step (2).  Strength alpha_theta = 4 Delta theta(T_n)/(3 w_+(T_n)) with
# theta = (e - 3p)/4 (Caprini et al. 2020, Eq. (12)); for a radiation bath 3 w_+/4 = rho_rad = pi^2 g* T^4/30, and
#   Delta theta = Delta V - (T/4) d(Delta V)/dT,   Delta V = V(0, T) - V(phi_-, T)
#   => Delta theta = D T0^2 phi_-^2/2,  alpha_theta = (15 D/(pi^2 g*)) (T0/T_n)^2 (phi_n/T_n)^2
#   (note, App. C: only the explicit scale T0 breaks the T^4 scaling, and a T^4 term has no trace).
# Also alpha_e = Delta e/rho_rad with Delta e = Delta V - T d(Delta V)/dT = 4 Delta theta - 3 Delta V (Caprini et al., Eq. (13)),
#   Delta V = (E^4 T^4/lambda_T^3) h(alpha), h = -(2 alpha^3/9) v(f_-).
# Checks: tptlib reproduces step (1); the closed forms of Delta V, Delta theta, Delta e against the numerical minima and a
# numerical T-derivative.  Scan: D and T0 SM-like, lambda_T = 0.02, 0.05, 0.1146 (SM), E from E_SM up to the largest value
# with R = lambda_T D/E^2 > 9/8 (a single minimum at high temperature).  Benchmarks for step (3).
# Writes results/strong_pt.csv and ../figs/strong_pt.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python strong_pt.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize_scalar

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
from tptlib import DineForm, fminus

step1 = {r[0]: float(r[1]) for r in csv.reader(open(os.path.join(HERE, "results", "dine_form.csv"))) if r[0] != "quantity"}
D, E_SM, T0, LT_SM = step1["D"], step1["E"], step1["T0"], step1["lambda_T_Tc"]


# %% [markdown]
# ## Regression against step (1), and the closed form of Delta theta against numerical minima

# %%
sm = DineForm(D, E_SM, T0, LT_SM)
r = sm.summary(sm.nucleation())
for k, k1 in (("Tn", "Tn"), ("alpha_n", "alpha_n"), ("S3T", "S3_over_T_n"), ("betaH", "beta_over_H"), ("phin_Tn", "phin_over_Tn")):
    print(f"{k:8}: tptlib {r[k]:.12g}, step (1) {step1[k1]:.12g}, rel. {r[k] / step1[k1] - 1:.1e}")


def dV_numerical(model, T):
    """V(0,T) - min over phi > 0 of V(phi, T), from the numerical minimum."""
    a = model.alpha(T)
    guess = (model.D * 2 * (T * T - model.T0 ** 2)) / (-6 * model.E * T) * fminus(a)      # (m^2/g) f_-
    res = minimize_scalar(lambda p: model.V(p, T), bounds=(0.5 * guess, 1.5 * guess), method="bounded",
                          options={"xatol": 1e-15 * guess})
    return -res.fun


def dtheta_numerical(model, T):
    """Delta theta and Delta e from Delta V of the numerical minima and its central difference (Richardson)."""
    cd = lambda hh: T * (dV_numerical(model, T + hh) - dV_numerical(model, T - hh)) / (2 * hh)
    hh = 1e-5 * (T - model.T0)
    TdV = (4 * cd(hh / 2) - cd(hh)) / 3
    dV = dV_numerical(model, T)
    return dV - TdV / 4, dV - TdV


chk = []
for name, model in (("SM-like", sm), ("lambda_T = 0.05, E = 0.04", DineForm(D, 0.04, T0, 0.05))):
    Tn = model.nucleation()
    s = model.summary(Tn)
    rho = math.pi ** 2 * model.gstar * Tn ** 4 / 30
    dth_num, de_num = dtheta_numerical(model, Tn)
    at_num, ae_num = dth_num / rho, de_num / rho
    dv_num = dV_numerical(model, Tn)
    chk.append((name, s["alpha_theta"], at_num, s["alpha_e"], ae_num))
    print(f"{name}: Delta V closed {s['dV']:.10e} vs numerical {dv_num:.10e} (rel. {dv_num / s['dV'] - 1:.1e});  "
          f"alpha_theta closed {s['alpha_theta']:.10e} vs numerical {at_num:.10e} (rel. {at_num / s['alpha_theta'] - 1:.1e});  "
          f"alpha_e closed {s['alpha_e']:.10e} vs numerical {ae_num:.10e} (rel. {ae_num / s['alpha_e'] - 1:.1e});  "
          f"alpha_e/alpha_theta = {s['alpha_e'] / s['alpha_theta']:.4f}")


# %% [markdown]
# ## Scan in E at fixed lambda_T

# %%
scan = []
for lam in (0.02, 0.05, LT_SM):
    Emax = math.sqrt(lam * D / 1.125)
    for E in np.geomspace(E_SM if E_SM < Emax else 0.5 * Emax, 0.995 * Emax, 60):
        model = DineForm(D, E, T0, lam)
        Tn = model.nucleation()
        if Tn is None:
            scan.append(dict(lam=lam, E=E, R=model.R, Tn=float("nan")))
            continue
        s = model.summary(Tn)
        s.update(lam=lam, E=E, R=model.R)
        scan.append(s)
for lam in (0.02, 0.05, LT_SM):
    sub = [s for s in scan if s["lam"] == lam and not math.isnan(s["Tn"])]
    nn = sum(1 for s in scan if s["lam"] == lam and math.isnan(s["Tn"]))
    print(f"lambda_T = {lam:.4f}: E = {sub[0]['E']:.4f} ... {sub[-1]['E']:.4f};  phi_n/T_n {sub[0]['phin_Tn']:.3f} ... "
          f"{sub[-1]['phin_Tn']:.3f};  alpha_theta {sub[0]['alpha_theta']:.2e} ... {sub[-1]['alpha_theta']:.2e};  "
          f"beta/H {sub[0]['betaH']:.2e} ... {sub[-1]['betaH']:.2e};  T_n/T_c {sub[-1]['Tn'] / sub[-1]['Tc']:.4f} at the largest E;  "
          f"no nucleation at {nn} points")


# %% [markdown]
# ## Benchmarks for step (3): phi_n/T_n = 1, 2, 3 at lambda_T = 0.05 (E from a root in phi_n/T_n)

# %%
from scipy.optimize import brentq

bench = []
lam = 0.05
for target in (1.0, 2.0, 3.0):
    def g(E):
        m = DineForm(D, E, T0, lam)
        tn = m.nucleation()
        return (m.summary(tn)["phin_Tn"] if tn else 1e3) - target
    Eb = brentq(g, 0.005, 0.999 * math.sqrt(lam * D / 1.125), xtol=1e-12)
    m = DineForm(D, Eb, T0, lam)
    s = m.summary(m.nucleation())
    s.update(lam=lam, E=Eb, R=m.R, name=f"BP{len(bench) + 1}")
    bench.append(s)
    print(f"BP{len(bench)}: E = {Eb:.6f}, R = {m.R:.4f}, T_c = {s['Tc']:.3f}, T_n = {s['Tn']:.3f} GeV, alpha(T_n) = {s['alpha_n']:.4f}, "
          f"phi_n/T_n = {s['phin_Tn']:.3f}, alpha_theta = {s['alpha_theta']:.4e}, alpha_e = {s['alpha_e']:.4e}, beta/H = {s['betaH']:.4e}")
# BP4: the strongest transition of the scan (lambda_T = 0.02, E = 0.995 of the largest value with R > 9/8)
Eb = 0.995 * math.sqrt(0.02 * D / 1.125)
m = DineForm(D, Eb, T0, 0.02)
s = m.summary(m.nucleation())
s.update(lam=0.02, E=Eb, R=m.R, name="BP4")
bench.append(s)
print(f"BP4: E = {Eb:.6f}, R = {m.R:.4f}, T_c = {s['Tc']:.3f}, T_n = {s['Tn']:.3f} GeV, alpha(T_n) = {s['alpha_n']:.4f}, "
      f"phi_n/T_n = {s['phin_Tn']:.3f}, alpha_theta = {s['alpha_theta']:.4e}, alpha_e = {s['alpha_e']:.4e}, beta/H = {s['betaH']:.4e}")


# %% [markdown]
# ## Output and figure

# %%
keys = ["lam", "E", "R", "Tc", "Tn", "alpha_n", "S3T", "phin_Tn", "alpha_theta", "alpha_e", "betaH"]
with open(os.path.join(HERE, "results", "strong_pt.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(keys)
    for s in scan:
        wr.writerow([s.get(k, float("nan")) for k in keys])
    wr.writerow([])
    wr.writerow(["benchmark"] + keys)
    for s in bench:
        wr.writerow([s["name"]] + [s[k] for k in keys])
    wr.writerow([])
    wr.writerow(["check", "alpha_theta_closed", "alpha_theta_numerical", "alpha_e_closed", "alpha_e_numerical"])
    wr.writerows(chk)

import matplotlib
import matplotlib.ticker
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1), sharex=True)
for lam, col, ls in ((0.02, "#eb6235", "-"), (0.05, "#5d81b4", "--"), (LT_SM, "k", "-.")):
    sub = [s for s in scan if s["lam"] == lam and not math.isnan(s["Tn"])]
    x = [s["phin_Tn"] for s in sub]
    lab = rf"$\lambda_T={lam:.3g}$" + (" (SM)" if lam == LT_SM else "")
    ax1.plot(x, [s["alpha_theta"] for s in sub], color=col, ls=ls, lw=0.9, label=lab)
    ax2.plot(x, [s["betaH"] for s in sub], color=col, ls=ls, lw=0.9)
xs = np.geomspace(0.17, 8, 50)
ax1.plot(xs, 15 * D / (math.pi ** 2 * 106.75) * xs ** 2, color="0.6", ls=":", lw=0.9, label=r"$T_n\to T_0$")
for s in bench:
    col = "#eb6235" if s["lam"] == 0.02 else "#5d81b4"
    ax1.plot(s["phin_Tn"], s["alpha_theta"], "o", ms=3.5, mfc="none", mec=col)
    ax2.plot(s["phin_Tn"], s["betaH"], "o", ms=3.5, mfc="none", mec=col)
    ax1.annotate(s["name"], (s["phin_Tn"], s["alpha_theta"]), textcoords="offset points",
                 xytext=(4, -3) if s["name"] == "BP4" else (-16, 4), fontsize=6)
ax1.set_yscale("log")
ax2.set_yscale("log")
ax1.set_xscale("log")
ax1.set_ylim(top=0.3)
ax1.set_xlim(0.15, 11)
ax2.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([0.2, 0.5, 1, 2, 5]))
ax2.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(["0.2", "0.5", "1", "2", "5"]))
ax2.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax1.set_ylabel(r"$\alpha_\theta$")
ax2.set_ylabel(r"$\beta/H$")
ax2.set_xlabel(r"$\phi_n/T_n$")
ax1.legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "strong_pt.pdf"))
print("wrote results/strong_pt.csv and figs/strong_pt.pdf")
