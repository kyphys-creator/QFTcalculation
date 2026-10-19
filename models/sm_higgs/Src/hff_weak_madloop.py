"""Step (5) of the Higgs note: MadLoop's electroweak virtual correction of H -> f fbar against the note's weak and photonic parts.

The CKM note's NLO UFO (models/sm_ckm/Src/generated/SM_CKM_NLO_UFO: MS-bar couplings with FJ tadpoles, on-shell field constants,
NLOCT's R2; its field constants are numbers at the point of the CKM note's MadLoop checks) with [virt=QED] for H -> tau- tau+,
mu- mu+, b bbar at that point (1/alpha = 128, M_Z = 91, M_W = 80, M_H = 125, m_t = 165, m_b = 2.86, m_tau = 1.746 GeV, ...),
COLLIER (MLReductionLib = 7), check_sa.f patched to read the point and MU_R (models/sm/Src/patch_check_sa.py), mu_R = 125, 500 GeV.
The electroweak virtual correction is the weak part plus the photonic part:
  finite/born = delta_weak (hff_weak.wl, results/hff_weak_ml.csv) + (alpha Q^2/pi) K_V|finite (hqq_massive_virtual.wl,
                results/hqq_massive_virtual_ml.csv: the photon exchange with the photonic field constants and the QED part of the
                MS-bar counterterm, MadLoop's normalization)
  1eps/born   = (alpha Q^2/pi) K_V|pole
Usage (from Src/): python3 hff_weak_madloop.py --prepare   (copies the UFO and writes work/ml_hffweak/run.mg5; run mg5_aMC there)
                   python3 hff_weak_madloop.py             (card, patch, compile, run; writes results/hff_weak_madloop.csv)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "ml_hffweak"
UFO = HERE.parent.parent / "sm_ckm" / "Src" / "generated" / "SM_CKM_NLO_UFO"
PATCH = HERE.parent.parent / "sm" / "Src" / "patch_check_sa.py"
ALPHA = 1 / 128.0
POINT = {"aEWM1": 128.0, "aS": 0.118, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
         "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MMU": 0.1027, "Me": 0.000487,
         "s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "dCKM": 1.147}
# name, process, folder tag, mass key, hff_weak name, photonic K row, Q
PROCS = [("h_tautau", "h > ta- ta+ [virt=QED]", "_h_tamtap", "MTA", "l3", "h_tata", -1.0),
         ("h_mumu", "h > mu- mu+ [virt=QED]", "_h_mummup", "MMU", "l2", "h_mumu", -1.0),
         ("h_bb", "h > b b~ [virt=QED]", "_h_bbx", "MB", "d3", "h_bb", -1 / 3)]


def set_card(path, vals, widths=(6, 23, 24, 25)):
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s(?:\s[^\n]*)?\n)" % k, lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(path, "w").write(s)


def two_body(m0, m1):
    p = math.sqrt(m0**2 / 4 - m1**2)
    return [(m0, 0, 0, 0), (math.sqrt(m1**2 + p**2), 0, 0, p), (math.sqrt(m1**2 + p**2), 0, 0, -p)]


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
    print("copied the CKM note's NLO UFO and wrote work/ml_hffweak/run.mg5")
    sys.exit(0)

out = WORK / "out"
set_card(out / "Cards" / "param_card.dat", POINT)
card = out / "Cards" / "MadLoopParams.dat"
s, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + "7", open(card).read())
assert n == 1
open(card, "w").write(s)
dweak = {(r["fermion"], float(r["mu_R"])): float(r["delta_weak"]) for r in csv.DictReader(open(HERE / "results" / "hff_weak_ml.csv"))}
kph = {(r["process"], float(r["mu_R"])): (float(r["KV_pole"]), float(r["KV_finite"]))
       for r in csv.DictReader(open(HERE / "results" / "hqq_massive_virtual_ml.csv"))}
rows, worst = [], 0.0
base = out / "SubProcesses"
for name, proc, tag, mk, wname, krow, q in PROCS:
    d = base / next(x for x in sorted(p.name for p in base.iterdir()) if x.startswith("P") and x.endswith(tag))
    if "MU_R.input" not in open(d / "check_sa.f").read():
        subprocess.run([sys.executable, str(PATCH), str(d / "check_sa.f")], check=True)
    (d / "check").unlink(missing_ok=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    pts = two_body(POINT["MH"], POINT[mk])
    for mu in (125.0, 500.0):
        r = run(d, pts, mu)
        kp, kf = kph[(krow, mu)]
        c = ALPHA * q**2 / math.pi
        note_f, note_p = dweak[(wname, mu)] + c * kf, c * kp
        fp, ep = r["finite"] / r["born"], r["1eps"] / r["born"]
        df = fp / note_f - 1
        worst = max(worst, abs(df))
        print("  %-8s mu_R = %5.0f: finite/born %.12e vs %.12e (%+.1e);  1eps/born %.10e vs %.10e (diff %+.1e);  2eps %.1e"
              % (name, mu, fp, note_f, df, ep, note_p, ep - note_p, r["2eps"]))
        print("            of which delta_weak %.10e and the photonic part %.10e" % (dweak[(wname, mu)], c * kf))
        rows.append([name, mu, "%.15e" % fp, "%.15e" % note_f, "%.15e" % ep, "%.15e" % note_p])
print("largest relative difference of finite/born: %.1e" % worst)
with open(HERE / "results" / "hff_weak_madloop.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu_R", "madloop_finite_born", "note_finite_born", "madloop_1eps_born", "note_1eps_born"])
    w.writerows(rows)
print("wrote results/hff_weak_madloop.csv")
