# %% [markdown]
# # Step (9) of the CKM note: MadLoop with the note's CKM NLO UFO against the note's own amplitudes
#
# Runs the MadLoop standalone programs built by run_madloop_check.sh (work/ml/<name>) with the UFO
# generated/SM_CKM_NLO_UFO (nlo_ckm_ufo.wl: NLOCT's R2 vertices; the MS-bar FJ counterterms, the CKM counterterm dV and
# NLOCT's on-shell field constants with the off-diagonal quark ones, as numbers at the point below; MU_R free).
#   (a) W+ -> u_i dbar_j, [virt=QED] (Born, UV counterterms): finite / born against 2 Re(M0^* M1)/|M0|^2 of
#       wud_madloop_ref.wl (step (5)'s amplitude, Feynman gauge, IR in dimensional regularization at mu_R), and the
#       single pole / born against its IR pole; mu_R = 91 and 500 GeV.
#   (b) loop-induced, [sqrvirt=QED] (no counterterm, no external self-energy): Z -> b sbar and b -> s gamma against the
#       1PI vertex of step (7) squared (fcnc_madloop_ref.wl, Feynman gauge), b sbar -> s bbar at small sqrt(s) against the
#       zero-momentum boxes of step (8).
# (a) with COLLIER alone (MLReductionLib = 7) and with MadLoop's default for processes with a Born (Ninja first, 6|7|1):
# with light quarks Ninja's loop differs from COLLIER's and CutTools' (double and quadruple precision) by up to 2e-8 of the
# Born.  (b) with the default for loop-induced processes (COLLIER first, 7|6|1).
# The point: step (5)'s benchmark with m_u, m_d ten times larger (MU = 0.0127, MD = 0.0271 GeV); for (b) the s quark
# (and for the boxes the b quark) massless, as in steps (7), (8).  Widths 0.
# Usage (from Src/): python3 ckm_madloop.py [--outputs | --card <param_card> <output>]

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
WIDTHS = (6, 23, 24, 25)
WUD = [("ud", "u d~"), ("us", "u s~"), ("ub", "u b~"), ("cd", "c d~"), ("cs", "c s~"), ("cb", "c b~")]
# the MadLoop outputs (one model loading each): the six W decays, the two loop-induced vertices, the boxes
# (the flavour-changing processes with the copy of the UFO whose CT parameters are those of m_s = 0, as steps (7), (8))
OUTPUTS = [("wud", "SM_CKM_NLO_UFO", ["w+ > %s [virt=QED]" % p for n, p in WUD]),
           ("fcnc", "SM_CKM_NLO_UFO_ms0", ["z > b s~ QED=3 [sqrvirt=QED]", "b > s a QED=3 [sqrvirt=QED]"]),
           ("bsbs", "SM_CKM_NLO_UFO_ms0", ["b s~ > s b~ QED=4 [sqrvirt=QED]"])]
SUB = {**{"wud_" + n: ("wud", "_wp_%sx" % n) for n, p in WUD}, "zbs": ("fcnc", "_z_bsx"), "bsg": ("fcnc", "_b_sa"),
       "bsbs": ("bsbs", "_bsx_sbx")}
MASS = {"u": "MU", "c": "MC", "d": "MD", "s": "MS", "b": "MB"}


def set_card(path, vals, widths=()):
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s\s*\n)" % k, lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1, (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(path, "w").write(s)


def two_body(m0, m1, m2):
    """a particle of mass m0 at rest into m1 (along +z) and m2"""
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
        out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    finally:
        open(card, "w").write(old)
    # a loop-induced process prints the finite part only
    return {k: float(m.group(1)) if (m := re.search(r"Matrix element %s\s*=\s*(\S+)" % k, out)) else 0.0
            for k in ("born", "finite", "1eps", "2eps")}


def ref(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


if len(sys.argv) > 1 and sys.argv[1] == "--outputs":
    for n, m, ps in OUTPUTS:
        print("%s|%s|%s" % (n, m, "|".join(ps)))
    sys.exit(0)
if len(sys.argv) > 2 and sys.argv[1] == "--card":
    # the param_card of one output: the point, widths 0; light quarks massless for the loop-induced processes
    path, name = sys.argv[2], sys.argv[3]
    vals = dict(POINT)
    if name in ("fcnc", "bsbs"):
        vals["MS"] = 0.0
    if name == "bsbs":
        vals["MB"] = 0.0
    set_card(path, vals, WIDTHS)
    sys.exit(0)

# %%
LIBS = (("7", "COLLIER"), (None, "default"))
rows = []
print("(a) W+ -> u_i dbar_j: MadLoop (the note's UFO) against this note's amplitude (wud_madloop_ref.wl)")
wref = {(r["channel"], float(r["mu"])): r for r in ref("wud_madloop_ref.csv")}
for lib, lname in LIBS:
    print(f"  reduction library: {lname}")
    for n, p in WUD:
        q, qb = p.split()
        pts = two_body(POINT["MW"], POINT[MASS[q]], POINT[MASS[qb[0]]])
        for mu in (91.0, 500.0):
            ml = run("wud_" + n, pts, mu, lib)
            r = wref[(n, mu)]
            fin, ir = float(r["delta_fin"]), float(r["delta_IRpole"])
            print(f"  {n}  mu = {mu:5.0f}: finite/born {ml['finite'] / ml['born']:.15e} vs {fin:.15e} (diff {ml['finite'] / ml['born'] - fin:+.1e});"
                  f"  1eps/born {ml['1eps'] / ml['born']:.12e} vs {ir:.12e} (diff {ml['1eps'] / ml['born'] - ir:+.1e});  2eps {ml['2eps']:.1e}")
            rows.append(["wud_" + n, mu, lname, ml["born"], ml["finite"] / ml["born"], fin, ml["1eps"] / ml["born"], ir, ml["2eps"]])

print("(b) loop-induced: MadLoop (loops, R2 and the field-constant vertices of the external legs) against this note's on-shell")
print("    amplitudes of step (7) (1PI + legs, Feynman gauge) and the zero-momentum boxes of step (8)")
fref = {r["quantity"]: complex(float(r["re"]), float(r["im"])) for r in ref("fcnc_madloop_ref.csv")}
c36 = fref["df2_colour_sum_over_36"].real
for name, pts in (("zbs", two_body(POINT["MZ"], POINT["MB"], 0.0)), ("bsg", two_body(POINT["MB"], 0.0, 0.0))):
    r = fref[name + "_finite"].real
    for mu in (91.0, 500.0):
        ml = run(name, pts, mu)
        print(f"  {name}  mu = {mu:5.0f}: |M|^2 {ml['finite']:.15e} vs {r:.15e} (rel {ml['finite'] / r - 1:+.1e})")
        rows.append([name, mu, "default", 0.0, ml["finite"], r, 0.0, 0.0, 0.0])
rel = {}
for rs in (2.0, 1.0, 0.5, 0.1):
    e, th = rs / 2, math.pi / 3
    pts = [(e, 0, 0, e), (e, 0, 0, -e), (e, e * math.sin(th), 0, e * math.cos(th)), (e, -e * math.sin(th), 0, -e * math.cos(th))]
    dot = lambda a, b: a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
    zero = c36 * 16 * dot(pts[0], pts[3]) * dot(pts[1], pts[2])
    ml = run("bsbs", pts, 91.0)
    print(f"  b sbar -> s bbar, sqrt(s) = {rs:4.1f} GeV: finite {ml['finite']:.15e} vs zero momentum {zero:.15e} (rel {ml['finite'] / zero - 1:+.2e});"
          f"  poles {ml['1eps']:.1e}, {ml['2eps']:.1e}")
    rows.append(["bsbs_sqrts" + str(rs), 91.0, "default", ml["born"], ml["finite"], zero, ml["1eps"], 0.0, ml["2eps"]])
    rel[rs**2] = ml["finite"] / zero - 1
# the deviation is linear in s (the external momenta against m_c, MW): a + b s from the two smallest sqrt(s)
(s1, r1), (s2, r2) = sorted(rel.items())[:2]
b = (r2 - r1) / (s2 - s1)
print(f"  b sbar -> s bbar: (MadLoop / zero momentum - 1) = a + b s with b = {b:.4e} GeV^-2, a = {r1 - b * s1:+.1e};"
      f"  at s = 1 GeV^2 MadLoop gives {rel[1.0]:.3e}, the linear term {r1 + b * (1.0 - s1):.3e} (the rest is of order s^2)")
rows.append(["bsbs_extrapolated_s0", 91.0, "default", 0.0, r1 - b * s1, 0.0, b, 0.0, 0.0])
with open(os.path.join(HERE, "results", "ckm_madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu", "library", "ml_born", "ml_value", "note_value", "ml_1eps", "note_1eps", "ml_2eps"])
    w.writerows(rows)
print("wrote results/ckm_madloop.csv")
