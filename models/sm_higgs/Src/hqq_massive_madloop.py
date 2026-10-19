"""Step (4) of the Higgs note: MadLoop's QCD virtual correction of H -> b bbar against hqq_massive_virtual.wl.

The CKM note's NLO UFO (models/sm_ckm/Src/generated/SM_CKM_NLO_UFO: NLOCT's R2 vertices and the note's counterterms; the UV vertex
H b bbar of QCD is -i (y_b/sqrt2) [dZ_L/2 + dZ_R/2 + dm_b/m_b] with the on-shell QCD field constants and the MS-bar mass, so the
MS-bar Yukawa coupling of the note) with [virt=QCD], at the point of the CKM note's MadLoop checks (its field constants are numbers
there: alpha_s = 0.118, M_H = 125, m_b = 2.86 GeV, ...), COLLIER (MLReductionLib = 7), check_sa.f patched to read the point and
MU_R (models/sm/Src/patch_check_sa.py).
  1eps/born   against (alpha_s C_F/pi) K_V|pole
  finite/born against (alpha_s C_F/pi) K_V|finite (MadLoop's normalization: (4 pi)^eps/Gamma(1 - eps) and mu_R^(2 eps) out)
with the MS-bar K_V of hqq_massive_virtual.wl (results/hqq_massive_virtual_ml.csv), at mu_R = 125 and 500 GeV.
Usage (from Src/): python3 hqq_massive_madloop.py --prepare   (copies the UFO and writes work/ml_hqq/run.mg5; run mg5_aMC there)
                   python3 hqq_massive_madloop.py             (card, patch, compile, run; writes results/hqq_massive_madloop.csv)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "ml_hqq"
UFO = HERE.parent.parent / "sm_ckm" / "Src" / "generated" / "SM_CKM_NLO_UFO"
PATCH = HERE.parent.parent / "sm" / "Src" / "patch_check_sa.py"
AS = 0.118
POINT = {"aEWM1": 128.0, "aS": AS, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
         "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MMU": 0.1027, "Me": 0.000487,
         "s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "dCKM": 1.147}
PROCS = [("h_bb", "h > b b~ [virt=QCD]", "_h_bbx", ("MH", "MB", "MB"))]


def set_card(path, vals, widths=(6, 23, 24, 25)):
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s(?:\s[^\n]*)?\n)" % k, lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(path, "w").write(s)


def two_body(m0, m1, m2):
    p = math.sqrt((m0**2 - (m1 + m2)**2) * (m0**2 - (m1 - m2)**2)) / (2 * m0)
    return [(m0, 0, 0, 0), (math.sqrt(m1**2 + p**2), 0, 0, p), (math.sqrt(m2**2 + p**2), 0, 0, -p)]


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
    print("copied the CKM note's NLO UFO and wrote work/ml_hqq/run.mg5")
    sys.exit(0)

out = WORK / "out"
set_card(out / "Cards" / "param_card.dat", POINT)
card = out / "Cards" / "MadLoopParams.dat"
s, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + "7", open(card).read())
assert n == 1
open(card, "w").write(s)
ref = {(r["process"], float(r["mu_R"])): (float(r["KV_pole"]), float(r["KV_finite"]))
       for r in csv.DictReader(open(HERE / "results" / "hqq_massive_virtual_ml.csv"))}
pref = AS * 4 / 3 / math.pi
rows, worst = [], 0.0
base = out / "SubProcesses"
for name, proc, tag, ms in PROCS:
    d = base / next(x for x in sorted(p.name for p in base.iterdir()) if x.startswith("P") and x.endswith(tag))
    if "MU_R.input" not in open(d / "check_sa.f").read():
        subprocess.run([sys.executable, str(PATCH), str(d / "check_sa.f")], check=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    pts = two_body(*(POINT[k] for k in ms))
    for mu in (125.0, 500.0):
        r = run(d, pts, mu)
        kp, kf = ref[(name, mu)]
        ep, fp = r["1eps"] / r["born"], r["finite"] / r["born"]
        dp, df = ep / (pref * kp) - 1, fp / (pref * kf) - 1
        worst = max(worst, abs(dp), abs(df))
        print("  %-5s mu_R = %5.0f: 1eps/born %.12e vs %.12e (%+.1e);  finite/born %.12e vs %.12e (%+.1e);  2eps %.1e"
              % (name, mu, ep, pref * kp, dp, fp, pref * kf, df, r["2eps"]))
        rows.append([name, mu, "%.15e" % ep, "%.15e" % (pref * kp), "%.15e" % fp, "%.15e" % (pref * kf)])
print("largest relative difference: %.1e" % worst)
with open(HERE / "results" / "hqq_massive_madloop.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu_R", "madloop_1eps_born", "note_1eps_born", "madloop_finite_born", "note_finite_born"])
    w.writerows(rows)
print("wrote results/hqq_massive_madloop.csv")
