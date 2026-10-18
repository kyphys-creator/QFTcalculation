# %% [markdown]
# # Step (9) of the CKM note: the extended UFO (all field constants, four-point R2) with MadLoop
#
# The field constants of the bosons (Z, photon-Z mixing, H: this note's, checked against NLOCT), the leptons and
# neutrinos (NLOCT's of the SM note) and the four-point R2 vertices (NLOCT's, as numbers at the point) were added to
# generated/SM_CKM_NLO_UFO.  Two checks:
#   (a) processes with a Born whose external legs need those constants, [virt=QED]: W+ -> tau+ nu_tau, W+ -> mu+ nu_mu,
#       Z -> nu_tau nubar_tau, Z -> tau- tau+, Z -> b bbar; finite / born and the single pole / born against FeynArts'
#       SM.mod + FormCalc with its own on-shell field constants and MS-bar couplings (ext_formcalc.wl), mu_R = 91, 500 GeV;
#       with COLLIER alone (MLReductionLib = 7) and with MadLoop's default for processes with a Born (Ninja first, 6|7|1): with
#       the light muon Ninja's loop differs from COLLIER's and CutTools' (double and quadruple precision) by ~1e-7 of the
#       Born;
#   (b) the loop-induced gamma gamma -> Z Z (four-point R2 vertex A A Z Z; UV finite, independent of V): against MadGraph's
#       loop_qcd_qed_sm-full with the same masses (the R2 vertices of Shao et al.).
#       Both with the default for loop-induced processes (COLLIER first, 7|6|1).
# Writes results/ckm_madloop_ext.csv.  Usage (from Src/): python3 ckm_madloop_ext.py [--outputs | --card <param_card> <output>]

# %%
import csv
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work", "ml")
POINT = {"aEWM1": 128.0, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
         "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MMU": 0.1027, "Me": 0.000487,
         "s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "dCKM": 1.147}
MG5 = {"aEWM1": 128.0, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
       "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MM": 0.1027, "Me": 0.000487}
YUK = {"ymt": "MT", "ymb": "MB", "ymc": "MC", "yms": "MS", "ymdo": "MD", "ymup": "MU", "ymtau": "MTA", "ymm": "MM", "yme": "Me"}
PROCS = [("w_taunu", "w+ > ta+ vt", "_wp_tapvt"), ("w_munu", "w+ > mu+ vm", "_wp_mupvm"), ("z_nunu", "z > vt vt~", "_z_vtvtx"),
         ("z_tautau", "z > ta- ta+", "_z_tamtap"), ("z_bb", "z > b b~", "_z_bbx")]
OUTPUTS = [("ext", "SM_CKM_NLO_UFO", ["%s [virt=QED]" % p for n, p, t in PROCS]),
           ("aazz", "SM_CKM_NLO_UFO", ["a a > z z QED=4 [sqrvirt=QED]"]),
           ("mg5_aazz", "loop_qcd_qed_sm-full", ["a a > z z QED=4 [sqrvirt=QED]"])]
SUB = {**{n: ("ext", t) for n, p, t in PROCS}, "aazz": ("aazz", "_aa_zz"), "mg5_aazz": ("mg5_aazz", "_aa_zz")}


def set_card(path, vals, widths=(6, 23, 24, 25)):
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s\s*\n)" % k, lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(path, "w").write(s)


def two_body(m0, m1, m2):
    p = math.sqrt((m0**2 - (m1 + m2)**2) * (m0**2 - (m1 - m2)**2)) / (2 * m0)
    return [(m0, 0, 0, 0), (math.sqrt(m1**2 + p**2), 0, 0, p), (math.sqrt(m2**2 + p**2), 0, 0, -p)]


def run(name, pts, mu, lib=None):
    """lib: MLReductionLib for this run (the output's Cards/MadLoopParams.dat, restored afterwards)"""
    out, tag = SUB[name]
    base = os.path.join(WORK, out, "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P") and x.endswith(tag)))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    card = os.path.join(WORK, out, "Cards", "MadLoopParams.dat")
    old = open(card).read()
    try:
        if lib is not None:
            new, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + lib, old)
            assert n == 1
            open(card, "w").write(new)
        o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    finally:
        open(card, "w").write(old)
    return {k: float(m.group(1)) if (m := re.search(r"Matrix element %s\s*=\s*(\S+)" % k, o)) else 0.0
            for k in ("born", "finite", "1eps", "2eps")}


if len(sys.argv) > 1 and sys.argv[1] == "--outputs":
    for n, m, ps in OUTPUTS:
        print("%s|%s|%s" % (n, m, "|".join(ps)))
    sys.exit(0)
if len(sys.argv) > 3 and sys.argv[1] == "--card":
    if sys.argv[3].startswith("mg5"):
        vals = dict(MG5)
        vals.update({y: vals[m] for y, m in YUK.items()})
    else:
        vals = dict(POINT)
    set_card(sys.argv[2], vals)
    sys.exit(0)

# %%
rows = []
ref = {(r["process"], float(r["mu"])): r for r in csv.DictReader(open(os.path.join(HERE, "results", "ext_formcalc.csv")))}
M = {"w_taunu": (POINT["MW"], POINT["MTA"], 0.0), "w_munu": (POINT["MW"], POINT["MMU"], 0.0), "z_nunu": (POINT["MZ"], 0.0, 0.0),
     "z_tautau": (POINT["MZ"], POINT["MTA"], POINT["MTA"]), "z_bb": (POINT["MZ"], POINT["MB"], POINT["MB"])}
print("(a) the note's UFO against SM.mod + FormCalc (on-shell field constants, MS-bar couplings)")
LIBS = (("7", "COLLIER"), (None, "default"))
for lib, lname in LIBS:
    print(f"  reduction library: {lname}")
    for n, p, t in PROCS:
        pts = two_body(*M[n])
        for mu in (91.0, 500.0):
            ml = run(n, pts, mu, lib)
            r = ref[(n, mu)]
            fin, ir = float(r["delta_fin"]), float(r["delta_IRpole"])
            print(f"  {n:9s} mu = {mu:5.0f}: finite/born {ml['finite'] / ml['born']:.13e} vs {fin:.13e} (diff {ml['finite'] / ml['born'] - fin:+.1e});"
                  f"  1eps/born {ml['1eps'] / ml['born']:.10e} vs {ir:.10e} (diff {ml['1eps'] / ml['born'] - ir:+.1e})")
            rows.append([n, mu, lname, ml["finite"] / ml["born"], fin, ml["1eps"] / ml["born"], ir])
print("(b) gamma gamma -> Z Z, loop-induced: the note's UFO (four-point R2 with internal parameters) against loop_qcd_qed_sm")
e, th, mz = 250.0, math.pi / 3, POINT["MZ"]
pz = math.sqrt(e**2 - mz**2)
pts = [(e, 0, 0, e), (e, 0, 0, -e), (e, pz * math.sin(th), 0, pz * math.cos(th)), (e, -pz * math.sin(th), 0, -pz * math.cos(th))]
for mu in (91.0, 500.0):
    a, b = run("aazz", pts, mu)["finite"], run("mg5_aazz", pts, mu)["finite"]
    print(f"  mu = {mu:5.0f}: note's UFO {a:.15e}, loop_qcd_qed_sm {b:.15e} (rel {a / b - 1:+.1e})")
    rows.append(["aazz", mu, "default", a, b, 0.0, 0.0])
with open(os.path.join(HERE, "results", "ckm_madloop_ext.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu", "library", "madloop", "reference", "madloop_1eps", "reference_1eps"])
    w.writerows(rows)
print("wrote results/ckm_madloop_ext.csv")
