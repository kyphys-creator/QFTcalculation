# %% [markdown]
# # Step (9) of the CKM note: MadGraph's electroweak NLO model loop_qcd_qed_sm against this note's loop amplitudes
#
# MadGraph's model (Shao et al., hand-written R2 and on-shell UV counterterms; the CKM matrix in the Wolfenstein form to
# O(lambda^3), not unitary) has no flavour-changing counterterm: its UV vertices Z sbar b, A sbar b, ... are 0.  The two
# comparisons that do not depend on that:
#   (a) the loop-induced Z -> b sbar and b -> s gamma, [sqrvirt=QED]: the model has no R2 vertex Z sbar b, A sbar b (nor
#       a counterterm), so MadLoop gives the 1PI loops alone in Feynman gauge, UV divergent; against the 1PI form factors of
#       step (7) with the same CKM matrix minus NLOCT's R2 vertices of this note's model (fcnc_madloop_ref.wl mg5).
#       MadLoop prints one number, |A_0(mu_R)|^2 for A = A_{-1}/eps + A_0: it is fitted as a + b L + c L^2 in
#       L = ln(mu_R^2/91^2) and compared with |A_0|^2, 2 Re(A_0 A_{-1}^*), |A_{-1}|^2 (also with the R2 vertex kept);
#   (b) b sbar -> s bbar at small sqrt(s) against the zero-momentum boxes of step (8) with that CKM matrix (Feynman gauge:
#       with a non-unitary V the boxes depend on the gauge).
# The full model (loop_qcd_qed_sm-full) with the masses of the note's point, the Yukawa couplings of the YUKAWA block equal
# to the masses (y = sqrt(2) m/v as in the note's model), widths 0, alpha(MZ) = 1/128, MW = 80, MZ = 91 GeV; the
# Wolfenstein parameters of the model.  Writes results/ckm_madloop_mg5.csv.
# Usage (from Src/): python3 ckm_madloop_mg5.py [--outputs | --card <param_card> <output>]

# %%
import csv
import math
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work", "ml")
MASSES = {"MW": 80.0, "MZ": 91.0, "MH": 125.0, "MT": 165.0, "MB": 2.86, "MC": 0.619, "MS": 0.0, "MD": 0.0271, "MU": 0.0127,
          "MTA": 1.746, "MM": 0.1027, "Me": 0.000487}
YUK = {"ymt": "MT", "ymb": "MB", "ymc": "MC", "yms": "MS", "ymdo": "MD", "ymup": "MU", "ymtau": "MTA", "ymm": "MM", "yme": "Me"}
OUTPUTS = [("mg5_fcnc", "loop_qcd_qed_sm-full", ["z > b s~ QED=3 [sqrvirt=QED]", "b > s a QED=3 [sqrvirt=QED]"]),
           ("mg5_bsbs", "loop_qcd_qed_sm-full", ["b s~ > s b~ QED=4 [sqrvirt=QED]"])]
SUB = {"zbs": ("mg5_fcnc", "_z_bsx"), "bsg": ("mg5_fcnc", "_b_sa"), "bsbs": ("mg5_bsbs", "_bsx_sbx")}


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


def run(name, pts, mu):
    out, tag = SUB[name]
    base = os.path.join(WORK, out, "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P") and x.endswith(tag)))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element finite\s*=\s*(\S+)", o).group(1))


if len(sys.argv) > 1 and sys.argv[1] == "--outputs":
    for n, m, ps in OUTPUTS:
        print("%s|%s|%s" % (n, m, "|".join(ps)))
    sys.exit(0)
if len(sys.argv) > 3 and sys.argv[1] == "--card":
    vals = dict(MASSES)
    if sys.argv[3] == "mg5_bsbs":
        vals["MB"] = 0.0
    vals.update({y: vals[m] for y, m in YUK.items()})
    vals["aEWM1"] = 128.0
    set_card(sys.argv[2], vals)
    sys.exit(0)

# %%
ref = {r["quantity"]: complex(float(r["re"]), float(r["im"])) for r in csv.DictReader(open(os.path.join(HERE, "results", "fcnc_madloop_ref_mg5.csv")))}
rows = []
print("(a) loop_qcd_qed_sm, loop-induced (Feynman gauge) against this note's 1PI vertices with the same CKM matrix, minus the R2 vertex")
mus = [30.0, 91.0, 200.0, 500.0, 1000.0]
for name, pts in (("zbs", two_body(MASSES["MZ"], MASSES["MB"], 0.0)), ("bsg", two_body(MASSES["MB"], 0.0, 0.0))):
    L = [math.log(m**2 / 91.0**2) for m in mus]
    f = [run(name, pts, m) for m in mus]
    c2, c1, c0 = np.polyfit(L, f, 2)
    resid = max(abs(np.polyval([c2, c1, c0], L) - np.array(f))) / abs(c0)
    r0, r1, r2 = (ref[name + "_1PImR2_" + k].real for k in ("finite", "1eps", "2eps"))
    w0, w1 = (ref[name + "_1PI_" + k].real for k in ("finite", "1eps"))
    print(f"  {name}: MadLoop at mu_R = 91 GeV {f[1]:.12e} vs |A_0|^2 {r0:.12e} (rel {f[1] / r0 - 1:+.1e});"
          f"  fit in ln mu_R^2 (residual {resid:.0e}): linear {c1:.10e} vs 2 Re(A_0 A_-1^*) {r1:.10e} (rel {c1 / r1 - 1:+.1e}),"
          f" quadratic {c2:.10e} vs |A_-1|^2 {r2:.10e} (rel {c2 / r2 - 1:+.1e})")
    print(f"        with the R2 vertex kept: |A_0|^2 {w0:.6e} (MadLoop rel {f[1] / w0 - 1:+.2f}), 2 Re(A_0 A_-1^*) {w1:.6e}")
    rows += [[name, "finite_mu91", f[1], r0], [name, "lnmu2_coefficient", c1, r1], [name, "lnmu2_squared_coefficient", c2, r2],
             [name, "finite_mu91_with_R2", f[1], w0]]
print("(b) loop_qcd_qed_sm, b sbar -> s bbar against this note's zero-momentum boxes with the same CKM matrix (Feynman gauge)")
c36 = ref["df2_colour_sum_over_36"].real
rel = {}
for rs in (2.0, 1.0, 0.5, 0.1):
    e, th = rs / 2, math.pi / 3
    pts = [(e, 0, 0, e), (e, 0, 0, -e), (e, e * math.sin(th), 0, e * math.cos(th)), (e, -e * math.sin(th), 0, -e * math.cos(th))]
    dot = lambda a, b: a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
    zero = c36 * 16 * dot(pts[0], pts[3]) * dot(pts[1], pts[2])
    ml = run("bsbs", pts, 91.0)
    rel[rs**2] = ml / zero - 1
    print(f"  sqrt(s) = {rs:4.1f} GeV: {ml:.15e} vs zero momentum {zero:.15e} (rel {ml / zero - 1:+.2e})")
    rows.append(["bsbs", "sqrts" + str(rs), ml, zero])
(s1, r1), (s2, r2) = sorted(rel.items())[:2]
b = (r2 - r1) / (s2 - s1)
print(f"  (MadLoop / zero momentum - 1) = a + b s: b = {b:.4e} GeV^-2, a = {r1 - b * s1:+.1e}")
rows.append(["bsbs", "extrapolated_s0", r1 - b * s1, 0.0])
with open(os.path.join(HERE, "results", "ckm_madloop_mg5.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "quantity", "madloop", "note"])
    w.writerows(rows)
print("wrote results/ckm_madloop_mg5.csv")
