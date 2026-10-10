# %% [markdown]
# # Step (6): MadLoop against the S-matrix element (on-shell) and the MS-bar amplitude
#
# MadLoop check of the one-loop phi phi -> phi phi amplitude (research note, step (6)).
#
# Runs the MadLoop standalone programs built by run_madloop_check.sh (work/ml_OS, work/ml_MSbar) at the
# six points of step (5) with mu_R = m, and at sqrt(s) = 5m, cos(theta) = 0.3 with mu_R = m/2, 2m, 5m.
# MadLoop returns, with the identical-particle factor 1/2 of the final state,
#     born = |M0|^2 / 2,   finite = 2 Re(M0* M1) / 2 = M0 Re M1   (M0 real),   and the 1/eps, 1/eps^2 parts.
# Predictions (m = g = 1; M1 = Re M1(mu = m) of step (5), results/scat4_comparison.csv):
#     MSbar counterterms (deltaZ = deltag = 0, pole-only deltam): M1(mu) = M1(m) + ln(mu^2/m^2)/(2(4pi)^2) sum_x 1/(x-m^2)^2,
#         i.e. the note's Eq. (17) at scale mu (B0 depends on mu only through + ln mu^2);
#     OS counterterms (NLOCT): Eq. (20), M1_phys = M1(m) + 1/(2(4pi)^2) sum_x [2 B0'(m^2)/(x-m^2) - B0(m^2)/(x-m^2)^2]
#         with B0(m^2) = 2 - pi/sqrt(3), m^2 B0'(m^2) = 2 pi/(3 sqrt(3)) - 1 at mu = m; independent of mu.
# Writes results/madloop.csv.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python madloop_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys
import re
import subprocess

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K = 16 * math.pi ** 2
B0M = 2 - math.pi / math.sqrt(3)
B0PM = 2 * math.pi / (3 * math.sqrt(3)) - 1
TOL = 1e-10


# %% [markdown]
# ## Kinematics and the MadLoop standalone runs

# %%
def kinematics(rs, ct):
    s = rs * rs
    p2 = s / 4 - 1
    return s, -2 * p2 * (1 - ct), -2 * p2 * (1 + ct)


def momenta(rs, ct):
    e = rs / 2
    p = math.sqrt(e * e - 1)
    st = math.sqrt(1 - ct * ct)
    return [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * ct), (e, -p * st, 0, -p * ct)]


def run_madloop(scheme, rs, ct, mu):
    d = os.path.join(HERE, "work", f"ml_{scheme}", "SubProcesses", "P0_phiphi_phiphi")
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta(rs, ct))
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    val = {}
    for key in ("born", "finite", "1eps", "2eps"):
        val[key] = float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1))
    return val


# %% [markdown]
# ## Predictions from step (5) (Eqs. (17) and (20))

# %%
ref = {}
with open(os.path.join(HERE, "results", "scat4_comparison.csv")) as fh:
    for r in csv.DictReader(fh):
        ref[(round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6))] = (float(r["tree"]), float(r["re_ref_collier"]))


def predictions(rs, ct, mu):
    s, t, u = kinematics(rs, ct)
    m0, m1 = ref[(rs, ct)]
    xs = (s, t, u)
    m1_ms = m1 + math.log(mu * mu) / (2 * K) * sum(1 / (x - 1) ** 2 for x in xs)
    m1_os = m1 + sum(2 * B0PM / (x - 1) - B0M / (x - 1) ** 2 for x in xs) / (2 * K)
    return {"born": m0 * m0 / 2, "MSbar": m0 * m1_ms, "OS": m0 * m1_os, "M0": m0, "M1_MSbar_mu_m": m1, "M1_phys": m1_os}


# %% [markdown]
# ## MadLoop at the six points and at several mu_R

# %%
runs = [(rs, ct, 1.0) for rs in (2.5, 5.0, 10.0) for ct in (0.3, 0.9)] + [(5.0, 0.3, mu) for mu in (0.5, 2.0, 5.0)]
rows = []
print(f"{'scheme':6} {'sqrt(s)':>7} {'cos':>4} {'mu_R':>5} {'finite (MadLoop)':>22} {'prediction':>22} {'rel.dev':>8} "
      f"{'born dev':>8} {'1/eps':>9}")
for scheme in ("OS", "MSbar"):
    for rs, ct, mu in runs:
        v = run_madloop(scheme, rs, ct, mu)
        pr = predictions(rs, ct, mu)
        dfin = abs(v["finite"] - pr[scheme]) / abs(pr[scheme])
        dborn = abs(v["born"] - pr["born"]) / pr["born"]
        flag = "" if (dfin < TOL and dborn < TOL and abs(v["1eps"]) < 1e-15 and v["2eps"] == 0) else "   <- disagrees"
        print(f"{scheme:6} {rs:7.1f} {ct:4.1f} {mu:5.1f} {v['finite']:+22.15e} {pr[scheme]:+22.15e} {dfin:8.1e} "
              f"{dborn:8.1e} {v['1eps']:+9.1e}{flag}")
        rows.append([scheme, rs, ct, mu, v["born"], v["finite"], v["1eps"], v["2eps"], pr["born"], pr[scheme], dborn, dfin,
                     pr["M0"], pr["M1_MSbar_mu_m"], pr["M1_phys"]])


# %%
with open(os.path.join(HERE, "results", "madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["scheme", "sqrts", "costheta", "mu_R", "born_madloop", "finite_madloop", "eps1_madloop", "eps2_madloop",
                "born_pred", "finite_pred", "reldev_born", "reldev_finite", "M0", "ReM1_MSbar_mu_m", "ReM1_phys"])
    w.writerows(rows)
print("\nwrote results/madloop.csv")
