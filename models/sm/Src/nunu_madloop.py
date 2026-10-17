# %% [markdown]
# # Step (9a): MadLoop (loop_qcd_qed_sm, on-shell) against the note's MS-bar (FJ) nu_e nubar_e -> nu_mu nubar_mu
#
# Research note models/sm, step (9a).  Runs the MadLoop standalone program built by run_nunu_check.sh (work/ml_nunu, model
# loop_qcd_qed_sm-no_widths: on-shell MW, MZ, MH, MT, alpha(MZ) scheme, Feynman gauge, R2 and counterterms of MadGraph's
# EW NLO implementation) at the point of nunu_numeric.wl, with mu_R = MZ and 500 GeV, and compares:
#   born   = B4/4                       (spin average 1/4)
#   finite = Re W_OS/2,  W_OS = W(MS-bar, FJ) + B4 dln M0   (nunu_numeric.wl, FeynCalc, general R_xi)
#   1eps = 2eps = 0                     (UV renormalized; no photon couples to the external neutrinos)
# and shows FormCalc's W(MS-bar) (nunu_formcalc.wl, Feynman gauge) converted with the same dln M0.
# Inputs: 1/alpha(MZ) = 128, MZ = 91.1876, MW = 80.369, MH = 125.2, MT = ymt = 172.57 GeV; sqrt(s) = 500 GeV, theta = pi/3.
# (b) MadLoop with the note's own NLO UFO (generated/SM_NLO_FJ_UFO: NLOCT's R2 vertices and the FJ counterterms in
# counterterm form, nlo_ufo.wl), the same numbers read as the note's MS-bar parameters: finite = Re W(MS-bar)/2.
# Writes results/nunu_madloop.csv (the rows of (a), then of (b)).  Usage (from Src/): python3 nunu_madloop.py

# %%
import csv
import math
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT = {"aEWM1": 128.0, "MZ": 91.1876, "MW": 80.369, "MH": 125.2, "MT": 172.57, "ymt": 172.57}
SQRTS, THETA = 500.0, math.pi / 3
MUS = (91.1876, 500.0)
ML = os.path.join(HERE, "work", "ml_nunu")
ML_FJ = os.path.join(HERE, "work", "ml_nunu_fj")       # the note's UFO with the FJ counterterms (step (9b))
LIGHT = {"MD": 0, "MU": 0, "MS": 0, "MC": 0, "MB": 0, "Me": 0, "MMU": 0, "MTA": 0}


def set_card(ml, vals, widths=()):
    path = os.path.join(ml, "Cards", "param_card.dat")
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s\s*\n)" % k, lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(path, "w").write(s)


def run(mu, ml=ML):
    base = os.path.join(ml, "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    e = SQRTS / 2
    c, st = math.cos(THETA), math.sin(THETA)
    pts = [(e, 0, 0, e), (e, 0, 0, -e), (e, e * st, 0, e * c), (e, -e * st, 0, -e * c)]
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {k: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % k, out).group(1)) for k in ("born", "finite", "1eps", "2eps")}


def read(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


# %%
set_card(ML, INPUT)

fc = read("nunu_numeric.csv")          # FeynCalc, general R_xi, with the conversion
fo = {round(float(r["mu"]), 4): r for r in read("nunu_formcalc.csv")}     # FormCalc, Feynman gauge, MS-bar
rows = []
print("MadLoop (on-shell) against the note's MS-bar (FJ) amplitude converted to on-shell inputs")
for mu in MUS:
    ml = run(mu)
    for r in fc:
        if abs(float(r["mu"]) - mu) > 1e-6:
            continue
        born, fin = float(r["born_over_4"]), float(r["re_W_OS_over_2"])
        line = (f"  mu = {mu:8.4f}, (xiZ, xiW) = ({r['xiZ']}, {r['xiW']}): born {ml['born']:.15e} vs {born:.15e} "
                f"(rel {ml['born'] / born - 1:+.1e});  finite {ml['finite']:.15e} vs {fin:.15e} (rel {ml['finite'] / fin - 1:+.1e})")
        print(line)
        rows.append([mu, r["xiZ"], r["xiW"], ml["born"], born, ml["finite"], fin, ml["1eps"], ml["2eps"]])
    f = fo.get(round(mu, 4))
    if f:
        dln = float(next(r for r in fc if abs(float(r["mu"]) - mu) < 1e-6)["dlnM0_fin"])
        w_os = (float(f["re_W_MSbar"]) + float(f["B4"]) * dln) / 2
        print(f"  mu = {mu:8.4f}, FormCalc (Feynman gauge) W(MS-bar) {float(f['re_W_MSbar']):.15e}, converted: "
              f"finite {w_os:.15e} (rel to MadLoop {ml['finite'] / w_os - 1:+.1e});  MadLoop poles {ml['1eps']:.1e}, {ml['2eps']:.1e}")
# (b): MadLoop with the note's NLO UFO (NLOCT's R2, the FJ counterterms in counterterm form) against W(MS-bar) directly
# the same numbers read as MS-bar parameters (no ymt in the note's model), light masses and widths 0
set_card(ML_FJ, {**{k: v for k, v in INPUT.items() if k != "ymt"}, **LIGHT}, widths=(6, 23, 24, 25))
print("MadLoop with the note's UFO (FJ counterterms, MS-bar parameters) against Re W(MS-bar)/2")
for mu in MUS:
    ml = run(mu, ML_FJ)
    for r in fc:
        if abs(float(r["mu"]) - mu) > 1e-6:
            continue
        w = float(r["re_W_MSbar"]) / 2
        print(f"  mu = {mu:8.4f}, (xiZ, xiW) = ({r['xiZ']}, {r['xiW']}): finite {ml['finite']:.15e} vs {w:.15e} "
              f"(rel {ml['finite'] / w - 1:+.1e});  born rel {ml['born'] / float(r['born_over_4']) - 1:+.1e};  poles {ml['1eps']:.1e}, {ml['2eps']:.1e}")
        rows.append([mu, r["xiZ"], r["xiW"], ml["born"], float(r["born_over_4"]), ml["finite"], w, ml["1eps"], ml["2eps"]])
with open(os.path.join(HERE, "results", "nunu_madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["mu", "xiZ", "xiW", "ml_born", "note_born", "ml_finite", "note_finite", "ml_1eps", "ml_2eps"])
    w.writerows(rows)
