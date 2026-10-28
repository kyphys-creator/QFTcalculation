# %% [markdown]
# # Step (5): MadLoop's virtual correction to h -> A A against the note's NLO width
#
# Research note models/abelian_higgs, step (5).  Runs the MadLoop standalone program built by run_width_check.sh
# (work/ml_haa: NLOCT's counterterms, on-shell masses and fields, MS-bar e, no tadpole diagrams) at the decay point
# h(MH) -> A A in the h rest frame, for mu_R = 0.5, 1, 2, 5.  MadLoop returns, with the identical-particle factor 1/2,
#     born = sum|M0|^2 / 2,   finite = 2 Re sum(M0* M1) / 2,   and the 1/eps, 1/eps^2 parts,
# so finite/born = delta_OS of the note (Eq. (nlowidth)): e MS-bar at mu_R, MA and MH the pole masses.
# Prediction: delta_OS(mu) from nlo_width_numeric.wl (results/nlo_width.csv, mu = 1, 2) and, at one loop,
# delta_OS(mu) = delta_OS(1) - (2 e^2/(3 K)) ln mu  (the running of e^2 in Gamma_0).
# Writes results/madloop.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python madloop_numeric.py

# %%
import csv
import math
import os
import re
import subprocess

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
K = 16 * math.pi ** 2
EE, MA, MH = 0.5, 1.0, 2.5
P = os.path.join(HERE, "work", "ml_haa", "SubProcesses", "P0_h_zpzp")


def run_madloop(mu):
    q = math.sqrt(MH ** 2 / 4 - MA ** 2)
    with open(os.path.join(P, "PS.input"), "w") as fh:
        fh.write("%.17e 0 0 0\n%.17e 0 0 %.17e\n%.17e 0 0 %.17e\n" % (MH, MH / 2, q, MH / 2, -q))
    with open(os.path.join(P, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=P, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps", "2eps")}


# %%
ref = {}
with open(os.path.join(HERE, "results", "nlo_width.csv")) as fh:
    for r in csv.DictReader(fh):
        if r["mu"] and r["xi"] in ("1", "1."):
            ref[float(r["mu"])] = float(r["delta_OS"])
slope = -2 * EE ** 2 / (3 * K)
born_note = 4 * EE ** 2 * MA ** 2 * (3 - MH ** 2 / MA ** 2 + MH ** 4 / (4 * MA ** 4)) / 2
rows = []
for mu in (0.5, 1.0, 2.0, 5.0):
    v = run_madloop(mu)
    d_ml = v["finite"] / v["born"]
    d_note = ref.get(mu, ref[1.0] + slope * math.log(mu))
    src = "nlo_width_numeric.wl" if mu in ref else "delta(1) - (2e^2/3K) ln mu"
    rows.append([mu, v["born"], v["finite"], v["1eps"], v["2eps"], d_ml, d_note, d_ml / d_note - 1])
    print("mu_R = %4g: born %.16e (note %.16e), finite/born %.16e, note %.16e (%s), rel. diff %+.1e, poles %.1e %.1e"
          % (mu, v["born"], born_note, d_ml, d_note, src, d_ml / d_note - 1, v["1eps"], v["2eps"]))
with open(os.path.join(HERE, "results", "madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["mu_R", "born", "finite", "pole1", "pole2", "delta_madloop", "delta_note", "rel_diff"])
    for r in rows:
        w.writerow([r[0]] + ["%.17e" % x for x in r[1:]])
print("written results/madloop.csv")
