"""Step (4b) of the NLO note: MadGraph's tree |M|^2 of W+ -> f fbar' gamma against the hand form of wreal.wl.

R = sum|M_R|^2/(e^2 sum|M_0|^2) and the Born sum sum|M_0|^2 at |V| = 1 and one colour (work/me_wreal.txt, CForm in
s12 = (p1 + p2)^2, s13 = (p1 + p3)^2, written by wreal.wl from the note's FeynArts model in Feynman gauge, the Goldstone diagram
included), so that MadGraph's average (1/3 over the W helicities; unitary gauge) is
  (1/3) N_c |V|^2 e^2 R sum|M_0|^2,   e from aEWM1, s_W^2 = 1 - M_W^2/M_Z^2,
for W+ -> nu_e e+ a, nu_tau tau+ a, u dbar a, c bbar a with the W card of step (1) (work/card_W.dat: u, d massless) in
MadGraph's default card (14 digits, as ir_massive_mg5.py).  The Dalitz points of ir_massive_mg5.py and two closer to the edge
along the charged particle 2 (the photon collinear to the lepton or the antiquark); the hand form with mpmath at the invariants
of the momenta as written to PS.input.
MadGraph writes the UFO's photon coupling of the down quarks, -0.3333333333333333*ee, as -3.333333D-01*ee in its Fortran
(Source/MODEL/couplings1.f; the only inexact number there): a relative 1e-7 in Q_d, 2e-7 in |M|^2 where the photon is along the
dbar or bbar.  The quark channels are run twice: as generated, and with that literal replaced by 1/3 and the model library
rebuilt.
Usage (from Src/): python3 wreal_mg5.py --prepare   (writes work/mg5run_wreal/wreal_mg5.mg5; run mg5_aMC on it there)
                   python3 wreal_mg5.py             (compiles and runs the standalone check; writes results/wreal_mg5.csv)
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
RUN = WORK / "mg5run_wreal"
OUT = WORK / "me_wreal"
# name (wreal.wl), MadGraph process, (m1, m2) keys, colours, |V|^2 from the card
PROCS = [("lnu1", "w+ > ve e+ a", (None, "Me"), 1, lambda v: 1),
         ("lnu3", "w+ > vt ta+ a", (None, "MTA"), 1, lambda v: 1),
         ("ud", "w+ > u d~ a", ("MU", "MD"), 3, lambda v: (1 - v["s12"]**2) * (1 - v["s13"]**2)),
         ("cb", "w+ > c b~ a", ("MC", "MB"), 3, lambda v: v["s23"]**2 * (1 - v["s13"]**2))]
# (x/x_max, f): x = M^2 - s12 = 2 M E_3, and 2 p1.p3 = w_lo + f (w_hi - w_lo) at that x (f -> 1: the photon along particle 2)
POINTS = [(0.5, 0.5), (0.2, 0.1), (0.9, 0.7), (1e-4, 0.5), (0.3, 1e-4), (0.3, 1 - 1e-4), (0.999, 0.3), (0.05, 1 - 1e-6),
          (0.7, 1 - 1e-6)]


def card():
    vals = {}
    for line in open(WORK / "card_W.dat"):
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
    exprs = dict(line.strip().split("|", 1) for line in open(WORK / "me_wreal.txt") if "|" in line)
    return {k: compile(v, k, "eval") for k, v in exprs.items()}


def hand(v, name, ncol, absv2, s12, s13, me):
    ns = {"Power": lambda a, b: a**b, "Sqrt": mpmath.sqrt}
    loc = {k: v[k] for k in ("MW", "Me", "MTA", "MU", "MD", "MC", "MB")}
    loc.update({"ee": mpmath.sqrt(4 * mpmath.pi / v["aEWM1"]), "sw": mpmath.sqrt(1 - v["MW"]**2 / v["MZ"]**2), "s12": s12, "s13": s13})
    r, b0 = eval(me[name], ns, loc), eval(me[name + "_B"], ns, loc)
    return ncol * absv2 * loc["ee"]**2 * r * b0 / 3


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
    with open(RUN / "wreal_mg5.mg5", "w") as fh:
        fh.write("import model ../SM_CKM_UFO\n")
        fh.write("generate %s\n" % PROCS[0][1])
        for p in PROCS[1:]:
            fh.write("add process %s\n" % p[1])
        fh.write("output standalone ../me_wreal -f\n")
    print("wrote work/mg5run_wreal/wreal_mg5.mg5")
    sys.exit(0)

vals = card()
set_card(OUT / "Cards" / "param_card_default.dat", OUT / "Cards" / "param_card.dat", vals)
v = {k: mpmath.mpf(repr(x)) for k, x in vals.items()}
me = hand_me()
subs = sorted(p.name for p in (OUT / "SubProcesses").iterdir() if p.is_dir() and p.name.startswith("P"))
cpl = OUT / "Source" / "MODEL" / "couplings1.f"
orig = cpl.with_name("couplings1.f.as_generated")
if not orig.exists():
    orig.write_text(cpl.read_text())
LIT = "-3.333333D-01*"


def build_model(exact):
    s = orig.read_text()
    assert s.count(LIT) == 1
    cpl.write_text(s.replace(LIT, "-(1.0D0/3.0D0)*") if exact else s)
    cpl.with_suffix(".o").unlink(missing_ok=True)   # make compares whole seconds: rebuild and relink unconditionally
    subprocess.run(["make"], cwd=OUT / "Source" / "MODEL", capture_output=True, text=True, check=True)


rows, worst = [], {False: 0.0, True: 0.0}
for exact in (False, True):
    build_model(exact)
    for i, (name, proc, (k1, k2), ncol, vf) in enumerate(PROCS):
        if exact and k1 is None:
            continue   # no down quark in the lepton channels
        d = OUT / "SubProcesses" / next(s for s in subs if s.startswith("P%d_" % (i + 1)))
        (d / "check").unlink(missing_ok=True)
        subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
        M, m1, m2 = vals["MW"], vals[k1] if k1 else 0.0, vals[k2]
        for j, (xi, f) in enumerate(POINTS):
            s12, s13 = dalitz(M, m1, m2, xi, f)
            mg, s12x, s13x = run_check(d, momenta(M, m1, m2, s12, s13, rotation(j)))
            hd = float(hand(v, name, ncol, vf(v), s12x, s13x, me))
            rel = mg / hd - 1
            worst[exact] = max(worst[exact], abs(rel))
            tag = "Q_d = 1/3" if exact else "as generated"
            print("  %-5s %-12s %-12s x/x_max = %-6g f = %-9g: MadGraph %.15e, hand %.15e, ratio - 1 = %+.2e"
                  % (name, d.name, tag, xi, f, mg, hd, rel))
            rows.append([name, "exact" if exact else "generated", xi, f, "%.16e" % mg, "%.16e" % hd, "%.3e" % rel])
build_model(False)
print("largest |MadGraph/hand - 1|: as generated %.1e (all channels);  with Q_d = 1/3 in MadGraph's Fortran %.1e (quarks)"
      % (worst[False], worst[True]))
with open(HERE / "results" / "wreal_mg5.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["channel", "madgraph_Qd", "x_over_xmax", "f", "madgraph", "hand", "ratio_minus_1"])
    w.writerows(rows)
print("wrote results/wreal_mg5.csv")
