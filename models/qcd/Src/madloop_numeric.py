# %% [markdown]
# # Step (5): MadLoop against the one-loop u ubar -> t tbar and g g -> t tbar interferences
#
# Research note models/qcd, step (5).  Runs the MadLoop standalone programs built by run_madloop_check.sh
# (work/ml_A, work/ml_B; NLO UFO with NLOCT's counterterms: top mass and fields on shell, aS = alpha_s^(n_l))
# at the point of step (4), sqrt(s) = sqrt(10), t = -3, m_t = 1, g = 1 (aS = 1/(4 pi)), with mu_R = m, 2m, m/2,
# and compares with madloop_predict.wl (results/madloop_pred.csv: step (4) converted to alpha_s^(n_l), four-dimensional
# spin sums and mu_R).
#
# MadLoop averages over the initial spins and colours (A: 1/36, B: 1/256) and returns, with W = sum M0^* M1:
#   born = B4/avg,   finite = 2 Re W_fin/avg,   1eps, 2eps = 2 Re (pole coefficients)/avg,
# with its poles normalized by (4 pi)^eps/Gamma(1 - eps) (c_Gamma agrees to O(eps^2)), i.e.
#   e^(-eps gamma_E) (1 - pi^2 eps^2/12): its finite part = ours (MS-bar, e^(-eps gamma_E)) + (pi^2/12) x double pole.
# Writes results/madloop.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python madloop_numeric.py
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

# %%
import csv
import math
import os
import re
import subprocess
import sys

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
KK = (4 * math.pi) ** 2
AVG = {"A": 36, "B": 256}
TOL = 1e-12
pred = {(r["process"], float(r["lambda"])): {k: float(v) for k, v in r.items() if k != "process"}
        for r in csv.DictReader(open(os.path.join(HERE, "results", "madloop_pred.csv")))}
pred[("A", 1.0)]                       # inspect

# %% [markdown]
# ## Kinematics and the MadLoop standalone runs

# %%
def momenta():
    e = math.sqrt(10) / 2
    k = math.sqrt(e * e - 1)
    c = (e - 2 / e) / k                # t = m^2 - 2 E (E - k c) = -3
    st = math.sqrt(1 - c * c)
    return [(e, 0, 0, e), (e, 0, 0, -e), (e, k * st, 0, k * c), (e, -k * st, 0, -k * c)]


def run_madloop(proc, mu):
    base = os.path.join(HERE, "work", f"ml_{proc}", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta())
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps", "2eps")}


run_madloop("A", 1.0)                  # inspect

# %% [markdown]
# ## Comparison

# %%
rows, worst = [], 0.0
for proc in ("A", "B"):
    for lam in (1.0, 2.0, 0.5):
        v = run_madloop(proc, lam)
        p = pred[(proc, lam)]
        a = AVG[proc]
        expect = {"born": p["born4"] / a,
                  "finite": 2 * (p["re_KW4_fin"] + math.pi ** 2 / 12 * p["re_KW4_m2"]) / KK / a,
                  "1eps": 2 * p["re_KW4_m1"] / KK / a,
                  "2eps": 2 * p["re_KW4_m2"] / KK / a}
        dev = {k: abs(v[k] - expect[k]) / abs(expect[k]) for k in expect}
        worst = max(worst, *dev.values())
        print(f"({proc}) mu_R = {lam} m:  MadLoop born {v['born']:.15e} finite {v['finite']:+.15e} 1eps {v['1eps']:+.15e} 2eps {v['2eps']:+.15e}")
        print("      relative deviation from step (4): " + "  ".join(f"{k} {dev[k]:.1e}" for k in dev)
              + ("" if max(dev.values()) < TOL else "   <- FAIL"))
        rows.append([proc, lam, v["born"], v["finite"], v["1eps"], v["2eps"], expect["born"], expect["finite"], expect["1eps"],
                     expect["2eps"], max(dev.values())])
print(f"max relative deviation (Born, finite part, 1/eps, 1/eps^2; both processes, mu_R = m, 2m, m/2): {worst:.1e}  (expect < {TOL})")
with open(os.path.join(HERE, "results", "madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu_over_m", "ml_born", "ml_finite", "ml_1eps", "ml_2eps", "pred_born", "pred_finite", "pred_1eps",
                "pred_2eps", "max_rel_dev"])
    w.writerows(rows)
print("wrote results/madloop.csv")
