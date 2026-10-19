"""Step (4c) of the NLO note: MadLoop's electroweak virtual correction of t -> b W+ against the note's (tweak.wl).

As wweak_madloop.py: the CKM note's NLO UFO with [virt=QED] for t -> b W+ at the point of the CKM note's MadLoop check, COLLIER,
check_sa.f patched, mu_R = 91, 500 GeV, against the electroweak virtual correction of tweak.wl at the same point
(results/tweak_ml.csv: its single infrared pole and its finite part, MadLoop's normalization).
Usage (from Src/): python3 tweak_madloop.py --prepare   (copies the UFO and writes work/ml_tweak/run.mg5; run mg5_aMC there)
                   python3 tweak_madloop.py             (card, patch, compile, run; writes results/tweak_madloop.csv)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "ml_tweak"
UFO = HERE.parent.parent / "sm_ckm" / "Src" / "generated" / "SM_CKM_NLO_UFO"
PATCH = HERE.parent.parent / "sm" / "Src" / "patch_check_sa.py"
ALPHA = 1 / 128.0
POINT = {"aEWM1": 128.0, "aS": 0.118, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
         "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MMU": 0.1027, "Me": 0.000487,
         "s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "dCKM": 1.147}
# name, process, folder tag, masses (t, b, W), tweak name
PROCS = [("t_bW", "t > b w+ [virt=QED]", "_t_bwp", ("MT", "MB", "MW"), "tbW")]


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
    print("copied the CKM note's NLO UFO and wrote work/ml_tweak/run.mg5")
    sys.exit(0)

out = WORK / "out"
set_card(out / "Cards" / "param_card.dat", POINT)
card = out / "Cards" / "MadLoopParams.dat"
s, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + "7", open(card).read())
assert n == 1
open(card, "w").write(s)
note = {(r["channel"], float(r["mu_R"])): (float(r["pole"]), float(r["finite"])) for r in csv.DictReader(open(HERE / "results" / "tweak_ml.csv"))}
rows, worst = [], 0.0
base = out / "SubProcesses"
for name, proc, tag, mk, wname in PROCS:
    d = base / next(x for x in sorted(p.name for p in base.iterdir()) if x.startswith("P") and x.endswith(tag))
    if "MU_R.input" not in open(d / "check_sa.f").read():
        subprocess.run([sys.executable, str(PATCH), str(d / "check_sa.f")], check=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    pts = two_body(*(POINT[k] if k else 0.0 for k in mk))
    for mu in (91.0, 500.0):
        r = run(d, pts, mu)
        note_p, note_f = note[(wname, mu)]
        fp, ep = r["finite"] / r["born"], r["1eps"] / r["born"]
        df = fp / note_f - 1
        worst = max(worst, abs(df))
        print("  %-8s mu_R = %5.0f: finite/born %.12e vs %.12e (%+.1e);  1eps/born %.10e vs %.10e (diff %+.1e);  2eps %.1e"
              % (name, mu, fp, note_f, df, ep, note_p, ep - note_p, r["2eps"]))
        rows.append([name, mu, "%.15e" % fp, "%.15e" % note_f, "%.15e" % ep, "%.15e" % note_p])
print("largest relative difference of finite/born: %.1e" % worst)
with open(HERE / "results" / "tweak_madloop.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu_R", "madloop_finite_born", "note_finite_born", "madloop_1eps_born", "note_1eps_born"])
    w.writerows(rows)
print("wrote results/tweak_madloop.csv")
