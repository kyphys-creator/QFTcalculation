"""Step (2) of the NLO note: MadGraph's tree |M|^2 of Z -> mu- mu+ gamma and Z -> u ubar g against the d = 4 form.

The real-emission matrix element of ir_massless_feyncalc.wl at eps = 0 (massless f; checked there against the FeynArts model):
  (1/3) sum|M_R|^2 = (1/3) N_c C c^2 (g_Z/2)^2 (v^2 + a^2) 4 r,   r = 2 (x1^2 + x2^2)/((1 - x1)(1 - x2)),
with v = T3 - 2 Q s^2, a = T3, x_i = 2 E_i/M_Z, and (c, C) = (e Q, 1) for the photon, (g_s, C_F) for the gluon; 1/3 is
MadGraph's average over the Z helicities.  The couplings are MadGraph's own from the card (e from aEWM1, c_W = M_W/M_Z,
g_s from aS): the values of the Z card of step (1) (work/card_Z.dat of lo_widths.py --cards) with m_mu = 0, written into
MadGraph's default card.  MadGraph's standalone output is evaluated at Dalitz points from the centre to near the soft and
collinear edges, each turned by a fixed rotation.
Usage (from Src/): python3 ir_mg5.py --prepare   (writes work/mg5run/ir_mg5.mg5; run mg5_aMC on it in work/mg5run)
                   python3 ir_mg5.py             (compiles and runs the standalone check; writes results/ir_mg5.csv)
"""
import csv
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
OUT = WORK / "me_ir"
# name, MadGraph process, subprocess folder, N_c, C, T3, Q, coupling of the radiated boson
PROCS = [("Z_mumugamma", "z > mu- mu+ a", "P1_z_mummupa", 1, 1.0, -0.5, -1.0, "e"),
         ("Z_uubarg", "z > u u~ g", "P2_z_uuxg", 3, 4.0 / 3.0, 0.5, 2.0 / 3.0, "gs")]
# (y13, y23): y_ij = (p_i + p_j)^2/M_Z^2, 1 = mu- or u, 2 = mu+ or ubar, 3 = the photon or the gluon
POINTS = [(1 / 3, 1 / 3), (0.2, 0.5), (0.45, 0.05), (1e-3, 0.3), (0.3, 1e-4), (1e-3, 2e-3), (0.6, 0.39)]


def card():
    vals = {}
    for line in open(WORK / "card_Z.dat"):
        m = re.match(r"\s+\d+\s+(\S+)\s+#\s+(\S+)", line)
        if m:
            vals[m.group(2)] = float("%.13e" % float(m.group(1)))   # what set_card writes
    vals["MMU"] = 0.0
    assert vals["MU"] == 0.0
    return vals


def set_card(src, dst, vals, widths=(6, 23, 24, 25)):
    """the values with 14 digits: MadGraph's Fortran reader (Source/MODEL/lha_read.f) keeps 20 characters of each"""
    s = open(src).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s(?:\s[^\n]*)?\n)" % k, lambda m: m.group(1) + "%.13e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(dst, "w").write(s)


def momenta(MZ, y13, y23, rot):
    y12 = 1 - y13 - y23
    x1, x2 = 1 - y23, 1 - y13
    x3 = 2 - x1 - x2
    E1, E2, E3 = MZ * x1 / 2, MZ * x2 / 2, MZ * x3 / 2
    c13 = 1 - MZ**2 * y13 / (2 * E1 * E3)
    p1 = np.array([0.0, 0.0, E1])
    p3 = E3 * np.array([math.sqrt(max(0.0, 1 - c13**2)), 0.0, c13])
    p2 = -p1 - p3
    assert abs(np.linalg.norm(p2) - E2) < 1e-12 * MZ and abs(y12 - (E1 * E2 - p1 @ p2) * 2 / MZ**2) < 1e-12
    return [(MZ, 0.0, 0.0, 0.0)] + [(E, *(rot @ p)) for E, p in ((E1, p1), (E2, p2), (E3, p3))]


def rotation(seed):
    rng = np.random.default_rng(seed)
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q @ np.diag(np.sign(np.diag(r)))
    return q if np.linalg.det(q) > 0 else -q


def hand(vals, proc, y13, y23):
    _, _, _, nc, C, t3, q, cpl = proc
    ee = math.sqrt(4 * math.pi / vals["aEWM1"])
    cw = vals["MW"] / vals["MZ"]
    s2 = 1 - cw**2
    gZ = ee / math.sqrt(s2 * cw**2)
    c = ee * q if cpl == "e" else math.sqrt(4 * math.pi * vals["aS"])
    x1, x2 = 1 - y23, 1 - y13
    r = 2 * (x1**2 + x2**2) / ((1 - x1) * (1 - x2))
    return nc * C * c**2 * (gZ / 2)**2 * ((t3 - 2 * q * s2)**2 + t3**2) * 4 * r / 3


def run_check(d, pts):
    with open(d / "PS.input", "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element =\s*(\S+)", o).group(1))


if len(sys.argv) > 1 and sys.argv[1] == "--prepare":
    # run from work/mg5run: the standalone output leaves nsqso_born.inc in the folder and its parent
    (WORK / "mg5run").mkdir(parents=True, exist_ok=True)
    with open(WORK / "mg5run" / "ir_mg5.mg5", "w") as fh:
        fh.write("import model ../SM_CKM_UFO\n")
        fh.write("generate %s\n" % PROCS[0][1])
        for p in PROCS[1:]:
            fh.write("add process %s\n" % p[1])
        fh.write("output standalone ../me_ir -f\n")
    print("wrote work/mg5run/ir_mg5.mg5")
    sys.exit(0)

vals = card()
set_card(OUT / "Cards" / "param_card_default.dat", OUT / "Cards" / "param_card.dat", vals)
rows = []
worst = 0.0
for proc in PROCS:
    d = OUT / "SubProcesses" / proc[2]
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    for i, (y13, y23) in enumerate(POINTS):
        mg = run_check(d, momenta(vals["MZ"], y13, y23, rotation(i)))
        hd = hand(vals, proc, y13, y23)
        rel = mg / hd - 1
        worst = max(worst, abs(rel))
        print("  %-12s y13 = %.4g, y23 = %.4g: MadGraph %.15e, hand %.15e, ratio - 1 = %+.2e" % (proc[0], y13, y23, mg, hd, rel))
        rows.append([proc[0], y13, y23, "%.16e" % mg, "%.16e" % hd, "%.3e" % rel])
print("largest |MadGraph/hand - 1| over %d points: %.1e" % (len(rows), worst))
with open(HERE / "results" / "ir_mg5.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "y13", "y23", "madgraph", "hand", "ratio_minus_1"])
    w.writerows(rows)
print("wrote results/ir_mg5.csv")
