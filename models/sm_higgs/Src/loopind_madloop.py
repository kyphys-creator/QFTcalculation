"""Step (2) of the Higgs note: MadLoop's loop-induced H -> gamma gamma, Z gamma, g g against FeynCalc and Package-X.

The CKM note's NLO UFO (models/sm_ckm/Src/generated/SM_CKM_NLO_UFO: the tree couplings of the note's model, NLOCT's R2, the
field constants of the bosons including the photon-Z mixing) with [sqrvirt=QED] (gamma gamma, Z gamma) and [sqrvirt=QCD]
(g g), Feynman gauge, COLLIER (MLReductionLib = 7), check_sa.f patched to read the point and MU_R (models/sm/Src/
patch_check_sa.py), mu_R = M_H and 1000 GeV.  The values of the H card (work/card_H.dat; 14 digits, as MadGraph reads them).
MadLoop's "finite" of a loop-induced process is sum|M|^2 over the final helicities and colours divided by MadGraph's IDEN, which
includes 2 for the identical photons and gluons; times that 2, against sum|M|^2 = 2 |Fg|^2 (gamma gamma, Z gamma), 16 |Fg|^2 (g g) of
loopind.wl at mu = M_H, xi = 1 (work/loopind_me.txt).  At the H card and at the point of the CKM note's MadLoop checks: the UFO's
field constants (the photon-Z mixing of the H Z gamma UV vertex among them) are numbers at that point only, so H -> Z gamma, whose
UV counterterm vertex enters, can be compared there only; H -> gamma gamma and g g have no counterterm.
Usage (from Src/): python3 loopind_madloop.py --prepare   (copies the UFO and writes work/ml_loopind/run.mg5; run mg5_aMC there)
                   python3 loopind_madloop.py             (card, patch, compile, run; writes results/loopind_madloop.csv)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "ml_loopind"
UFO = HERE.parent.parent / "sm_ckm" / "Src" / "generated" / "SM_CKM_NLO_UFO"
PATCH = HERE.parent.parent / "sm" / "Src" / "patch_check_sa.py"
# name (loopind_me.txt), process, folder tag, mass of particle 1
# the point of the CKM note's NLO UFO (its field constants are numbers there: models/sm_ckm/Src/ckm_madloop_ext.py), alpha_s 0.118
CKMPT = {"aEWM1": 128.0, "aS": 0.118, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
         "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MMU": 0.1027, "Me": 0.000487, "s12": 0.22501, "s23": 0.04183, "s13": 0.003732,
         "dCKM": 1.147}
PROCS = [("aa", "h > a a QED=3 [sqrvirt=QED]", "_h_aa", None), ("za", "h > z a QED=3 [sqrvirt=QED]", "_h_za", "MZ"),
         ("gg", "h > g g QED=1 QCD=2 [sqrvirt=QCD]", "_h_gg", None)]


def card():
    vals = {}
    for line in open(HERE / "work" / "card_H.dat"):
        m = re.match(r"\s+\d+\s+(\S+)\s+#\s+(\S+)", line)
        if m:
            vals[m.group(2)] = float(m.group(1))
    return vals


def set_card(path, vals, widths=(6, 23, 24, 25)):
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s(?:\s[^\n]*)?\n)" % k, lambda m: m.group(1) + "%.13e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(path, "w").write(s)


def two_body(m0, m1):
    p = (m0**2 - m1**2) / (2 * m0)
    return [(m0, 0, 0, 0), (math.sqrt(m1**2 + p**2), 0, 0, p), (p, 0, 0, -p)]


def run(d, pts, mu):
    with open(d / "PS.input", "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(d / "MU_R.input", "w") as fh:
        fh.write("%.17e\n" % mu)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {k: float(m.group(1)) if (m := re.search(r"Matrix element %s\s*=\s*(\S+)" % k, o)) else 0.0
            for k in ("born", "finite", "1eps", "2eps")}


if len(sys.argv) > 1 and sys.argv[1] == "--prepare":
    WORK.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(WORK / "SM_CKM_NLO_UFO", ignore_errors=True)
    shutil.rmtree(WORK / "out", ignore_errors=True)
    shutil.copytree(UFO, WORK / "SM_CKM_NLO_UFO")
    with open(WORK / "run.mg5", "w") as fh:
        fh.write("import model ./SM_CKM_NLO_UFO\n")
        fh.write("generate %s\n" % PROCS[0][1])
        for p in PROCS[1:]:
            fh.write("add process %s\n" % p[1])
        fh.write("output standalone ./out\n")
    print("copied the CKM note's NLO UFO and wrote work/ml_loopind/run.mg5")
    sys.exit(0)

out = WORK / "out"
mlp = out / "Cards" / "MadLoopParams.dat"
s, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + "7", open(mlp).read())
assert n == 1
open(mlp, "w").write(s)
mine = {l.split()[0]: float(l.split()[1].replace("*^", "e")) for l in open(HERE / "work" / "loopind_me.txt") if l.strip()}
rows, worst = [], {}
base = out / "SubProcesses"
dirs = {}
for name, proc, tag, mk in PROCS:
    d = base / next(x for x in sorted(p.name for p in base.iterdir()) if x.startswith("P") and x.endswith(tag))
    if "MU_R.input" not in open(d / "check_sa.f").read():
        subprocess.run([sys.executable, str(PATCH), str(d / "check_sa.f")], check=True)
    (d / "check").unlink(missing_ok=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    dirs[name] = d
for label, vals, suffix in (("the H card", card(), ""), ("the CKM note's point", CKMPT, "_ckm")):
    set_card(out / "Cards" / "param_card.dat", vals)   # read by ./check at run time
    print("at %s:" % label)
    for name, proc, tag, mk in PROCS:
        pts = two_body(vals["MH"], vals[mk] if mk else 0.0)
        ref = mine[name + suffix]
        # MadGraph's matrix element includes 1/2 for identical bosons in the final state
        iden = 2 if name in ("aa", "gg") else 1
        for mu in (vals["MH"], 1000.0):
            r = run(dirs[name], pts, mu)
            rel = iden * r["finite"] / ref - 1
            worst[(label, name)] = max(worst.get((label, name), 0.0), abs(rel))
            print("  H -> %s  mu_R = %7.2f: MadLoop sum|M|^2 x %d = %.13e, FeynCalc + Package-X %.13e (rel %+.1e)"
                  % (name, mu, iden, iden * r["finite"], ref, rel))
            rows.append([label, name, mu, "%.15e" % (iden * r["finite"]), "%.15e" % ref, "%.3e" % rel])
for k, v in worst.items():
    print("  largest |rel| %s, H -> %s: %.1e" % (k[0], k[1], v))
with open(HERE / "results" / "loopind_madloop.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["point", "process", "mu_R", "madloop_times_iden", "feyncalc_packagex", "rel"])
    w.writerows(rows)
print("wrote results/loopind_madloop.csv")
