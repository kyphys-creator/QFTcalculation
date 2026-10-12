# %% [markdown]
# # Step (11a, b): the general form of Dine et al. in PhaseTracer 2.2.2 and BSMPT 3.2.0
#
# Research note models/phi34_thermal, step (11).  Runs the two C++ programs of this folder (built by
# ../run_review_tools_check.sh into build/) for the SM-like coefficients and BP1-BP4, and compares with tptlib in each tool's
# own conventions:
#   PhaseTracer: T_n from S3/T = 140; alpha = Delta(V - T/4 dV/dT)/rho_rad (= alpha_theta); beta/H from 6 actions within
#                +-0.1 GeV; GW spectra at T_n with the sound-wave and turbulence formulas of the note (kappa_turb = 0.05
#                kappa_v set in the program).  The actions also at the note's T_n, against the shooting bounce of tptlib.
#   BSMPT:       T_c; T_n from S3/T = 140 and from Gamma = H^4 with H^2 = (rho_rad + Delta V)/(3 M_Pl^2), M_Pl = 2.4e18 GeV;
#                alpha and beta/H at that T_n.  (Its GW stage needs SM-like particle masses and is not used.)
# Writes ../results/review_tools_check.csv.  Batch (qft environment): `~/miniforge3/envs/qft/bin/python review_tools_check.py`.

# %%
import csv
import math
import os
import subprocess
import sys

import numpy as np
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
SRC = os.path.dirname(HERE)
sys.path.insert(0, SRC)
import tptlib as tl

with open(os.path.join(SRC, "results", "dine_form.csv")) as fh:
    step1 = {r[0]: float(r[1]) for r in csv.reader(fh) if r and r[0] in ("D", "E", "T0", "lambda_T_Tc")}
with open(os.path.join(SRC, "results", "strong_pt.csv")) as fh:
    rows = list(csv.reader(fh))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
points = [("SM-like", step1["E"], step1["lambda_T_Tc"])]
points += [(r[0], float(r[1 + keys.index("E")]), float(r[1 + keys.index("lam")])) for r in rows[ib + 1:] if r and r[0].startswith("BP")]
D, T0 = step1["D"], step1["T0"]
BUILD = os.path.join(HERE, "build")


def phi_minus(m, T):
    """The broken minimum of the general form at T."""
    return (3 * m.E * T + math.sqrt(9 * m.E ** 2 * T ** 2 - 8 * m.lam * m.D * (T * T - m.T0 ** 2))) / (2 * m.lam)


def s3T_direct(m, T):
    """S3/T from the shooting bounce of tptlib (not the interpolated S3(alpha))."""
    V = lambda p: m.V(p, T)
    dV = lambda p: 2 * m.D * (T * T - m.T0 ** 2) * p - 3 * m.E * T * p * p + m.lam * p ** 3
    return tl.bounce(V, dV, 0.0, phi_minus(m, T), d=3)["S"] / T


def T_at_s3T(m, target):
    return brentq(lambda T: m.s3T(T) - target, m.T_of_alpha(0.01), m.T_of_alpha(0.999999), xtol=1e-13 * m.T0)


def T_bsmpt(m):
    """Gamma = H^4 with BSMPT's H^2 = (rho_rad + Delta V)/(3 M_Pl^2), M_Pl = 2.4e18 GeV."""
    def f(T):
        dV = -m.V(phi_minus(m, T), T)
        H = math.sqrt((math.pi ** 2 / 30 * 106.75 * T ** 4 + dV) / 3) / 2.4e18
        s = m.s3T(T)
        return 4 * math.log(T) + 1.5 * math.log(s / (2 * math.pi)) - s - 4 * math.log(H)
    return brentq(f, m.T_of_alpha(0.01), m.T_of_alpha(0.999999), xtol=1e-13 * m.T0)


FGW = np.geomspace(1e-6, 10.0, 8001)                    # the frequency grid of phasetracer_dine.cpp


# %% [markdown]
# ## PhaseTracer

# %%
lines = []
refs = {}
for name, E, lam in points:
    m = tl.DineForm(D, E, T0, lam)
    Tn = m.nucleation()
    refs[name] = (m, Tn)
    tlow = T0 + 0.05 * (Tn - T0)
    for tight in (0, 1):
        lines.append(f"{name} {D!r} {E!r} {T0!r} {lam!r} {m.T_of_alpha(9 / 8)!r} {tlow!r} {tight} {Tn!r}")
res = subprocess.run([os.path.join(BUILD, "phasetracer_dine")], input="\n".join(lines) + "\n", capture_output=True, text=True)
out_pt = []
for ln in res.stdout.strip().splitlines():
    f = ln.split(",")
    name, tight = f[0], int(f[1])
    m, Tn = refs[name]
    TC, TN, s3tn, alpha, betaH, pamp, pfreq, s3_at_Tn = map(float, f[2:10])
    T140 = T_at_s3T(m, 140.0)
    s = m.summary(TN)
    g = tl.GWSource(s["alpha_theta"], s["betaH"], TN, 0.95)
    h2 = g.h2_total(FGW)
    k = int(np.argmax(h2))
    d = s3T_direct(m, Tn)
    r = dict(name=name, tight=tight, Tc_PT=TC, Tc_ref=m.T_of_alpha(1.0), TN_PT=TN, T140_ref=T140, S3T_TN_PT=s3tn,
             alpha_PT=alpha, alpha_ref_at_TN=s["alpha_theta"], betaH_PT=betaH, betaH_ref_at_TN=s["betaH"],
             peak_PT=pamp, peak_ref=h2[k], fpeak_PT=pfreq, fpeak_ref=FGW[k],
             S3T_at_Tn_PT=s3_at_Tn, S3T_at_Tn_direct=d, S3T_at_Tn_interp=m.s3T(Tn))
    out_pt.append(r)
    print(f"PT {name} tight={tight}: T_c {TC / r['Tc_ref'] - 1:+.1e};  T_n(140) {TN:.8g} vs {T140:.8g} ({TN / T140 - 1:+.1e});  "
          f"alpha {alpha / s['alpha_theta'] - 1:+.1e};  beta/H {betaH:.5g} vs {s['betaH']:.5g} ({betaH / s['betaH'] - 1:+.1e});  "
          f"GW peak {pamp:.4e} vs {h2[k]:.4e} ({pamp / h2[k] - 1:+.1e}) at {pfreq:.4e}/{FGW[k]:.4e} Hz;  S3/T at the note's T_n "
          f"{s3_at_Tn:.9g} vs direct {d:.9g} ({s3_at_Tn / d - 1:+.1e})")
if res.returncode != 0:
    print("phasetracer_dine stderr:", res.stderr[-2000:])


# %% [markdown]
# ## BSMPT

# %%
lines = []
for name, E, lam in points:
    m, Tn = refs[name]
    lines.append(f"{name} {D!r} {E!r} {T0!r} {lam!r} {T0 + 0.05 * (Tn - T0)!r} {1.05 * m.T_of_alpha(9 / 8)!r}")
res = subprocess.run([os.path.join(BUILD, "bsmpt_dine")], input="\n".join(lines) + "\n", capture_output=True, text=True)
out_bs = []
for ln in res.stdout.strip().splitlines():
    f = ln.split(",")
    name = f[0]
    if not name in refs:
        continue
    m, Tn = refs[name]
    if len(f) < 7:
        print(f"BSMPT {name}: {ln}")
        out_bs.append(dict(name=name, error=ln))
        continue
    Tc, Tn140, TnB, Tp, alpha, betaH = map(float, f[1:7])
    Tref = T_bsmpt(m)
    s = m.summary(TnB)
    r = dict(name=name, Tc_BS=Tc, Tc_ref=m.T_of_alpha(1.0), Tn140_BS=Tn140, T140_ref=T_at_s3T(m, 140.0), Tn_BS=TnB,
             Tn_ref_BSconv=Tref, Tn_ref_note=Tn, Tp_BS=Tp, alpha_BS=alpha, alpha_ref_at_TnBS=s["alpha_theta"], betaH_BS=betaH,
             betaH_ref_at_TnBS=s["betaH"])
    out_bs.append(r)
    print(f"BSMPT {name}: T_c {Tc / r['Tc_ref'] - 1:+.1e};  T_n(140) {Tn140 / r['T140_ref'] - 1:+.1e};  T_n(Gamma = H^4) {TnB:.8g} vs "
          f"{Tref:.8g} in BSMPT's H ({TnB / Tref - 1:+.1e}; note's T_n {Tn:.8g});  alpha {alpha / s['alpha_theta'] - 1:+.1e};  "
          f"beta/H {betaH:.5g} vs {s['betaH']:.5g} ({betaH / s['betaH'] - 1:+.1e});  T_p {Tp:.6g}")
if res.returncode != 0:
    print("bsmpt_dine stderr:", res.stderr[-2000:])


# %% [markdown]
# ## Output

# %%
with open(os.path.join(SRC, "results", "review_tools_check.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    for tag, rows_ in (("PhaseTracer", out_pt), ("BSMPT", out_bs)):
        cols = list(dict.fromkeys(k for r in rows_ for k in r))
        wr.writerow([tag] + cols)
        for r in rows_:
            wr.writerow([""] + [r.get(c, "") for c in cols])
        wr.writerow([])
print("wrote results/review_tools_check.csv")
