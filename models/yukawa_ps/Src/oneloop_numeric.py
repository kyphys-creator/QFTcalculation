# %% [markdown]
# # Step (3): one-loop 1PI functions of the pseudoscalar Yukawa + phi^4 model -- Package-X, LoopTools and COLLIER compared
#
# Research note models/yukawa_ps, Eqs. (6), (7), at m = mu = 1, M = 0.7, y = lambda = 1.  The brackets
# - b_phi = (4 pi)^2 V_phi / i = 2 y^2 (p^2 B0^MM(p^2) - 2 A0(M^2)) + lambda/2 A0(m^2),
# - b_psi^V = -y^2 B1^Mm(p^2),  b_psi^S = -y^2 M B0^Mm(p^2),
# - b_y = -y^3 (B0^Mm(p'^2) + k^2 C1), -y^3 M C0, 0, y^3 C2  (structures gamma5, kslash gamma5, pslash gamma5, kslash pslash gamma5),
# - b_4 = lambda^2/2 sum B0^mm - 2 y^4 sum F  (Eq. (7)).
#
# Package-X and LoopTools evaluate the FeynCalc amplitudes (oneloop_feyncalc.wl, the FeynArts diagrams reduced by TID);
# COLLIER evaluates the note's formulas (oneloop_collier.f90).  The two-point brackets (b_phi, b_psi) are also computed
# here from the Feynman-parameter integrals of A0, B0, B1 with mpmath (30 digits), independently of all three tools:
#   B0^ab(p^2) = -int_0^1 dx ln(Delta_x - i0),  B1^ab(p^2) = int_0^1 dx x ln(Delta_x - i0),
#   Delta_x = x m_b^2 + (1-x) m_a^2 - x(1-x) p^2,  A0(m^2) = m^2 (1 - ln m^2)   (mu = 1).
# LoopTools fails at one V_y point, (p^2, k^2, p'^2) = (M^2, m^2, M^2): its C0 there is wrong (it prints "Discrepancy in C0";
# the internal version 'a' is right but the returned value is not, whatever the version key; ~/hep/README.md, Known problems).
# Reads results/oneloop_mathematica.csv and results/oneloop_collier.csv, writes results/oneloop_comparison.csv.
# Batch: `~/miniforge3/envs/qft/bin/python oneloop_numeric.py` (from Src/).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import os
import sys

import mpmath as mp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
MPHI, MPSI, Y, LAM = mp.mpf(1), mp.mpf("0.7"), mp.mpf(1), mp.mpf(1)


def log_m_i0(x):
    """ln(x - i0) for real x."""
    return mp.log(x) if x > 0 else mp.log(-x) - 1j * mp.pi


def feynman_b(p2, ma2, mb2, power):
    """int_0^1 dx x^power ln(Delta_x - i0); the zeros of Delta_x in (0, 1) are passed to quad as break points."""
    p2, ma2, mb2 = mp.mpf(p2), mp.mpf(ma2), mp.mpf(mb2)
    delta = lambda x: x * mb2 + (1 - x) * ma2 - x * (1 - x) * p2
    pts = [mp.mpf(0)]
    if p2 != 0:   # p2 x^2 + (mb2 - ma2 - p2) x + ma2 = 0
        a, b, c = p2, mb2 - ma2 - p2, ma2
        disc = b * b - 4 * a * c
        if disc > 0:
            pts += sorted(r for r in ((-b - mp.sqrt(disc)) / (2 * a), (-b + mp.sqrt(disc)) / (2 * a)) if 0 < r < 1)
    pts.append(mp.mpf(1))
    return mp.quad(lambda x: x ** power * log_m_i0(delta(x)), pts)


def a0(m2):
    m2 = mp.mpf(m2)
    return m2 * (1 - mp.log(m2))


def b0(p2, ma2, mb2):
    return -feynman_b(p2, ma2, mb2, 0)


def b1(p2, ma2, mb2):
    return feynman_b(p2, ma2, mb2, 1)


def reference(func, a1):
    """two-point brackets from the Feynman-parameter integrals; None for the other functions."""
    m2, bm2 = MPHI ** 2, MPSI ** 2
    if func == "Vphi":
        return complex(2 * Y ** 2 * (a1 * b0(a1, bm2, bm2) - 2 * a0(bm2)) + LAM / 2 * a0(m2))
    if func == "Vpsi_V":
        return complex(-Y ** 2 * b1(a1, bm2, m2))
    if func == "Vpsi_S":
        return complex(-Y ** 2 * MPSI * b0(a1, bm2, m2))
    return None


def read(name, cols):
    with open(os.path.join(HERE, "results", name)) as fh:
        return [(r["func"], float(r["arg1"]), float(r["arg2"]), float(r["arg3"]),
                 [complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols])
                for r in csv.DictReader(fh)]


mma = read("oneloop_mathematica.csv", ("packagex", "looptools"))
col = read("oneloop_collier.csv", ("collier",))
assert len(mma) == len(col) and all(a[0] == b[0] and all(abs(x - z) < 1e-12 * (1 + abs(x)) for x, z in zip(a[1:4], b[1:4]))
                                    for a, b in zip(mma, col))
mma[:3]          # inspect

# %% [markdown]
# ## Comparison
#
# Reference: the mpmath integrals for the two-point brackets, COLLIER for V_y and V_4.  The deviation is relative to the
# largest bracket at the same point (so that a structure that is exactly 0, V_y's pslash gamma5, compares absolutely).

# %%
LT_BAD = ("Vy", 0.49, 1.0, 0.49)   # LoopTools returns a wrong C0 here (prints "Discrepancy in C0"), see the docstring
rows, worst, points, lt_bad = [], {}, {}, []
for (f, a1, a2, a3, (px, lt)), (_, _, _, _, (cl,)) in zip(mma, col):
    points.setdefault((f.split("_")[0], a1, a2, a3), []).append((f, px, lt, cl))
for (fam, a1, a2, a3), entries in points.items():
    refs = [reference(f, mp.mpf(a1)) or cl for f, px, lt, cl in entries]
    scale = max(abs(r) for r in refs)
    for (f, px, lt, cl), ref in zip(entries, refs):
        dpx, dlt, dcl = (abs(z - ref) / scale for z in (px, lt, cl))
        rows.append((f, a1, a2, a3, ref.real, ref.imag, dpx, dlt, dcl))
        tag = f"{f:7s} ({a1:6.2f}, {a2:6.2f}, {a3:6.2f})"
        extra = f"  COLLIER {dcl:.1e}" if fam in ("Vphi", "Vpsi") else ""
        print(f"{tag}: b = {ref.real:+.12f} {ref.imag:+.12f} i   rel. dev.  Package-X {dpx:.1e}  LoopTools {dlt:.1e}{extra}")
        bad = all(abs(x - z) < 1e-12 for x, z in zip((a1, a2, a3), LT_BAD[1:])) and fam == LT_BAD[0]
        if bad:
            lt_bad.append(dlt)
        for name, d in (("Package-X", dpx), ("LoopTools", dlt), ("COLLIER", dcl)):
            if not (fam not in ("Vphi", "Vpsi") and name == "COLLIER") and not (bad and name == "LoopTools"):
                worst[(fam, name)] = max(worst.get((fam, name), 0.0), d)
print("max deviation by function and tool (COLLIER is the reference for V_y and V_4; LoopTools at the bad V_y point excluded):")
for (fam, name), d in sorted(worst.items()):
    print(f"  {fam:5s} {name:10s} {d:.1e}")
print(f"LoopTools at the V_y point (p^2, k^2, p'^2) = (M^2, m^2, M^2) = (0.49, 1, 0.49): deviation up to {max(lt_bad):.1e};")
print("  its C0(m^2, M^2, M^2; M^2, M^2, m^2) = -21.747 + 9.691 i (FF: lambda < 0, 'Discrepancy in C0'), Package-X and COLLIER -1.10566")

with open(os.path.join(HERE, "results", "oneloop_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg1", "arg2", "arg3", "re_ref", "im_ref", "dev_packagex", "dev_looptools", "dev_collier"])
    w.writerows(rows)
print("wrote results/oneloop_comparison.csv")
