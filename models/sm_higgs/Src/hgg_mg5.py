"""Step (6) of the Higgs note: MadGraph's tree |M|^2 of H -> g g g and H -> g u ubar of the heavy-top operator against FeynCalc.

The note's UFO with the operator -(1/4) cHgg (H/vev) G G (generated/SM_CKM_HEFT_UFO, generate_HggEFT.wl) at the H card of step (1)
(work/card_H.dat) and cHgg = -alpha_s/(3 pi); FeynCalc's 4-dimensional sum|M_R|^2 from the same model (work/me_hgg.txt,
hgg_eft_feyncalc.wl; C_A = 3, C_F = 4/3).  MadGraph's matrix element is divided by 3! for the three gluons.  The Dalitz points of
the NLO note's ir_massive_mg5.py with massless particles.
Usage (from Src/): python3 hgg_mg5.py --prepare   (writes work/mg5run_hgg/hgg_mg5.mg5; run mg5_aMC there)
                   python3 hgg_mg5.py             (compiles and runs the standalone check; writes results/hgg_mg5.csv)
"""
import csv
import math
import re
import subprocess
import sys
from pathlib import Path

import mpmath
import numpy as np

mpmath.mp.dps = 40

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
RUN = WORK / "mg5run_hgg"
OUT = WORK / "me_hggtree"
# name, MadGraph process, subprocess folder, parent mass key, (m1, m2) keys
PROCS = [("GGG", "h > g g g", "P1_h_ggg", "MH", (None, None), 6), ("GQQ", "h > g u u~", "P2_h_guux", "MH", (None, None), 1)]
# (x/x_max, f): x = M^2 - s12 = 2 M E_3, and 2 p1.p3 = w_lo + f (w_hi - w_lo) at that x
POINTS = [(0.5, 0.5), (0.2, 0.1), (0.9, 0.7), (1e-4, 0.5), (0.3, 1e-4), (0.3, 1 - 1e-4), (0.999, 0.3)]


def card():
    vals = {}
    for line in open(WORK / "card_H.dat"):
        m = re.match(r"\s+\d+\s+(\S+)\s+#\s+(\S+)", line)
        if m:
            vals[m.group(2)] = float("%.13e" % float(m.group(1)))   # what set_card writes
    return vals


def set_card(src, dst, vals, widths=(6, 23, 24, 25)):
    s = open(src).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s(?:\s[^\n]*)?\n)" % k, lambda m: m.group(1) + "%.13e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(dst, "w").write(s)


def rotation(seed):
    rng = np.random.default_rng(seed)
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q @ np.diag(np.sign(np.diag(r)))
    return q if np.linalg.det(q) > 0 else -q


def dalitz(M, m1, m2, xi, f):
    """s12, s13 at x = xi x_max and 2 p1.p3 = w_lo + f (w_hi - w_lo) (12 rest frame, massless particle 3)"""
    xhi = M**2 - (m1 + m2)**2
    x = xi * xhi
    s = M**2 - x
    e1 = (s + m1**2 - m2**2) / (2 * math.sqrt(s))
    p1 = math.sqrt((xhi - x) * (s - (m1 - m2)**2)) / (2 * math.sqrt(s))
    e3 = x / (2 * math.sqrt(s))
    wlo, whi = 2 * e3 * m1**2 / (e1 + p1), 2 * e3 * (e1 + p1)
    return s, m1**2 + wlo + f * (whi - wlo)


def momenta(M, m1, m2, s12, s13, rot):
    s23 = M**2 + m1**2 + m2**2 - s12 - s13
    E1, E2, E3 = (M**2 + m1**2 - s23) / (2 * M), (M**2 + m2**2 - s13) / (2 * M), (M**2 - s12) / (2 * M)
    a1 = math.sqrt(E1**2 - m1**2)
    c13 = (2 * E1 * E3 - (s13 - m1**2)) / (2 * a1 * E3)
    p1 = np.array([0.0, 0.0, a1])
    p3 = E3 * np.array([math.sqrt(max(0.0, 1 - c13**2)), 0.0, c13])
    p2 = -p1 - p3
    assert abs(math.sqrt(p2 @ p2 + m2**2) - E2) < 1e-10 * M
    return [(M, 0.0, 0.0, 0.0)] + [(E, *(rot @ p)) for E, p in ((E1, p1), (E2, p2), (E3, p3))]


def hand_me():
    ns = {"Power": lambda a, b: a**b, "Sqrt": mpmath.sqrt}
    exprs = dict(line.strip().split("|", 1) for line in open(WORK / "me_hgg.txt") if "|" in line)
    return {k: compile(v, k, "eval") for k, v in exprs.items()}, ns


def hand(vals, name, s12, s13, me, ns):
    v = {k: mpmath.mpf(repr(x)) for k, x in vals.items()}
    loc = {"ee": mpmath.sqrt(4 * mpmath.pi / v["aEWM1"]), "gS": mpmath.sqrt(4 * mpmath.pi * v["aS"]), "MW": v["MW"],
           "sw": mpmath.sqrt(1 - (v["MW"] / v["MZ"])**2), "cHgg": v["cHgg"], "CA": mpmath.mpf(3), "CF": mpmath.mpf(4) / 3,
           "MM": v["MH"]**2, "s12": s12, "s13": s13}
    return eval(me[name], ns, loc)


def run_check(d, pts):
    lines = ["%.17e %.17e %.17e %.17e" % p for p in pts]
    with open(d / "PS.input", "w") as fh:
        fh.writelines(l + "\n" for l in lines)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    mom = [[mpmath.mpf(x) for x in l.split()] for l in lines]
    dot = lambda a, b: a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
    add = lambda a, b: [x + y for x, y in zip(a, b)]
    s12, s13 = dot(add(mom[1], mom[2]), add(mom[1], mom[2])), dot(add(mom[1], mom[3]), add(mom[1], mom[3]))
    return float(re.search(r"Matrix element =\s*(\S+)", o).group(1)), s12, s13


if len(sys.argv) > 1 and sys.argv[1] == "--prepare":
    RUN.mkdir(parents=True, exist_ok=True)   # the standalone output leaves nsqso_born.inc in the folder and its parent
    with open(RUN / "hgg_mg5.mg5", "w") as fh:
        fh.write("import model ../SM_CKM_HEFT_UFO\n")
        fh.write("generate %s\n" % PROCS[0][1])
        for p in PROCS[1:]:
            fh.write("add process %s\n" % p[1])
        fh.write("output standalone ../me_hggtree -f\n")
    print("wrote work/mg5run_hgg/hgg_mg5.mg5")
    sys.exit(0)

vals = card()
vals["cHgg"] = float("%.13e" % (-vals["aS"] / (3 * math.pi)))
set_card(OUT / "Cards" / "param_card_default.dat", OUT / "Cards" / "param_card.dat", vals)
me, ns = hand_me()
rows, worst = [], 0.0
for name, proc, sub, mk, (k1, k2), iden in PROCS:
    d = OUT / "SubProcesses" / sub
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    M, m1, m2 = vals[mk], 0.0, 0.0
    for i, (xi, f) in enumerate(POINTS):
        s12, s13 = dalitz(M, m1, m2, xi, f)
        mg, s12x, s13x = run_check(d, momenta(M, m1, m2, s12, s13, rotation(i)))
        hd = float(hand(vals, name, s12x, s13x, me, ns)) / iden
        rel = mg / hd - 1
        worst = max(worst, abs(rel))
        print("  %-14s x/x_max = %-6g f = %-7g: MadGraph %.15e, hand %.15e, ratio - 1 = %+.2e" % (name, xi, f, mg, hd, rel))
        rows.append([name, xi, f, "%.16e" % mg, "%.16e" % hd, "%.3e" % rel])
print("largest |MadGraph/hand - 1| over %d points: %.1e" % (len(rows), worst))
with open(HERE / "results" / "hgg_mg5.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "x_over_xmax", "f", "madgraph", "hand", "ratio_minus_1"])
    w.writerows(rows)
print("wrote results/hgg_mg5.csv")
