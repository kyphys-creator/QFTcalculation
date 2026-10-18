# %% [markdown]
# # Step (9) of the CKM note: the QCD part of the CKM NLO UFO with MadLoop
#
# The diagonal quark field constants of generated/SM_CKM_NLO_UFO have a QCD part (nlo_ckm_dz.wl: on-shell, Feynman gauge,
# -(alpha_s C_F/(4 pi)) (3/eps + 4 + 3 ln(mu^2/m^2)), alpha_s = 0.118; checked there against NLOCT's of the SM note).  The
# one-loop QCD corrections to colour-singlet decays into quarks, [virt=QCD], need only that constant and the gluon exchange:
#   W+ -> c bbar, W+ -> u dbar, Z -> b bbar, Z -> c cbar;  finite / born and the single pole / born at mu_R = 91, 500 GeV,
#   (a) the single pole against the soft pole of two massive emitters (Catani-Dittmaier-Trocsanyi),
#       (alpha_s C_F/pi) [-1 - ln((1 - v)/(1 + v))/(2 v)],  v = sqrt(1 - m1^2 m2^2/(p1.p2)^2)  (the QED form, checked on
#       Z -> tau- tau+ of ckm_madloop_ext.py, with alpha C_F -> alpha);
#   (b) finite / born against MadGraph's loop_qcd_qed_sm-full with the same masses and alpha_s (a reference: its own R2 and
#       counterterms).  Its quark field constants are on-shell for b and t; for c (whatever MC) and u, d, s it uses the
#       massless one (qWcft_UV, UV - IR pole), so only Z -> b bbar compares: for the others its single pole exceeds the
#       massive one by 3 alpha_s C_F/(4 pi) per c, u, d leg (printed);
#   (c) the mu_R dependence: finite(500) - finite(91) = (single pole) ln(500^2/91^2) (no alpha_s in the Born).
# COLLIER for the reduction (MLReductionLib = 7).  Writes results/ckm_madloop_qcd.csv.
# Usage (from Src/): python3 ckm_madloop_qcd.py [--outputs | --card <param_card> <output>]

# %%
import csv
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work", "ml")
AS = 0.118
POINT = {"aEWM1": 128.0, "aS": AS, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
         "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MMU": 0.1027, "Me": 0.000487,
         "s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "dCKM": 1.147}
MG5 = {"aEWM1": 128.0, "aS": AS, "MZ": 91.0, "MW": 80.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0546,
       "MD": 0.0271, "MU": 0.0127, "MTA": 1.746, "MM": 0.1027, "Me": 0.000487}
YUK = {"ymt": "MT", "ymb": "MB", "ymc": "MC", "yms": "MS", "ymdo": "MD", "ymup": "MU", "ymtau": "MTA", "ymm": "MM", "yme": "Me"}
PROCS = [("w_cb", "w+ > c b~", "_wp_cbx", ("MW", "MC", "MB")), ("w_ud", "w+ > u d~", "_wp_udx", ("MW", "MU", "MD")),
         ("z_bb", "z > b b~", "_z_bbx", ("MZ", "MB", "MB")), ("z_cc", "z > c c~", "_z_ccx", ("MZ", "MC", "MC"))]
OUTPUTS = [("qcd", "SM_CKM_NLO_UFO", ["%s [virt=QCD]" % p for n, p, t, m in PROCS]),
           ("mg5_qcd", "loop_qcd_qed_sm-full", ["%s [virt=QCD]" % p for n, p, t, m in PROCS])]
# the legs on which loop_qcd_qed_sm uses the massless field constant
MASSLESS_IN_MG5 = {"w_cb": ("MC",), "w_ud": ("MU", "MD"), "z_bb": (), "z_cc": ("MC", "MC")}
SUB = {**{n: ("qcd", t) for n, p, t, m in PROCS}, **{"mg5_" + n: ("mg5_qcd", t) for n, p, t, m in PROCS}}


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


def run(name, pts, mu, lib="7"):
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
        new, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + lib, old)
        assert n == 1
        open(card, "w").write(new)
        o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    finally:
        open(card, "w").write(old)
    return {k: float(m.group(1)) if (m := re.search(r"Matrix element %s\s*=\s*(\S+)" % k, o)) else 0.0
            for k in ("born", "finite", "1eps", "2eps")}


def soft_pole(m0, m1, m2):
    """(alpha_s C_F/pi) [-1 - ln((1 - v)/(1 + v))/(2 v)] for the pair q(m1) qbar(m2) from a colour singlet of mass m0"""
    pp = (m0**2 - m1**2 - m2**2) / 2
    x = (m1 * m2 / pp)**2
    v = math.sqrt(1 - x)
    one_minus_v = x / (1 + v)                  # without the cancellation of 1 - v for light quarks
    return AS * 4 / 3 / math.pi * (-1 - math.log(one_minus_v / (1 + v)) / (2 * v))


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
L = math.log(500.0**2 / 91.0**2)
print("[virt=QCD], COLLIER: the note's UFO against the soft pole and against loop_qcd_qed_sm (reference)")
for n, p, t, ms in PROCS:
    m0, m1, m2 = (POINT[k] for k in ms)
    pts = two_body(m0, m1, m2)
    ip = soft_pole(m0, m1, m2)
    res = {}
    for mu in (91.0, 500.0):
        a, b = run(n, pts, mu), run("mg5_" + n, pts, mu)
        fa, fb = a["finite"] / a["born"], b["finite"] / b["born"]
        ea, eb = a["1eps"] / a["born"], b["1eps"] / b["born"]
        res[mu] = (fa, ea)
        # this note minus loop_qcd_qed_sm = the massive on-shell dZ_q (finite part at mu) on those legs
        aq = AS * 4 / 3 / (4 * math.pi)
        expect = sum(-aq * (4 + 3 * math.log(mu**2 / POINT[k]**2)) for k in MASSLESS_IN_MG5[n])
        print(f"  {n:5s} mu = {mu:5.0f}: finite/born {fa:.13e} vs loop_qcd_qed_sm {fb:.13e} (diff {fa - fb:+.1e});"
              f"  1eps/born {ea:.10e} vs soft pole {ip:.10e} (diff {ea - ip:+.1e}), loop_qcd_qed_sm {eb:.10e};"
              f"  2eps {a['2eps']:.1e}")
        print(f"        finite/born minus loop_qcd_qed_sm minus the massive dZ_q of its massless legs: {fa - fb - expect:+.1e}")
        rows.append([n, mu, fa, fb, ea, ip, eb])
    dmu = (res[500.0][0] - res[91.0][0]) - res[91.0][1] * L
    legs = (eb - ip) / (3 * AS * 4 / 3 / (4 * math.pi))
    print(f"        finite(500) - finite(91) - (1eps) ln(500^2/91^2) = {dmu:+.1e};  loop_qcd_qed_sm single pole minus the "
          f"massive soft pole = {legs:.8f} x 3 alpha_s C_F/(4 pi)")
    rows.append([n, "mu_dependence", dmu, 0.0, 0.0, 0.0, 0.0])
with open(os.path.join(HERE, "results", "ckm_madloop_qcd.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "mu", "finite_born", "loop_qcd_qed_sm_finite_born", "eps1_born", "soft_pole", "loop_qcd_qed_sm_eps1_born"])
    w.writerows(rows)
print("wrote results/ckm_madloop_qcd.csv")
