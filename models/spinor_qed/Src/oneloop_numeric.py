# %% [markdown]
# # Step (3): one-loop 1PI functions of spinor QED -- Package-X, LoopTools and COLLIER against the note
#
# Research note models/spinor_qed, Eqs. (5), (7), (10), at e = 1, m_e = mu = 1, m_mu = 1.7.  All brackets are K/e^2
# times the note's quantity (K = (4 pi)^2), split into the 1/eps coefficient ("pole") and the MS-bar finite part:
# - Pi_e, Pi_mu (q^2): the renormalized vacuum polarization of one flavour, Eq. (7);
# - SigV, SigS (p^2, xi) for e and mu: Sigma_V^R, Sigma_S^R of Eq. (7), xi = 0, 1, 3;
# - F1 (q^2): F1^Lambda on shell with its total pole (UV and IR together), F2 (q^2);
# - R_e, R_mu (xi): R - 1 of Eq. (10), its IR pole and finite part.
#
# Package-X and LoopTools evaluate the FeynCalc amplitudes (oneloop_feyncalc.wl: the FeynArts diagrams reduced by TID);
# COLLIER evaluates the note's PaVe forms (oneloop_collier.f90).  The references, independent of the three tools, are
# mpmath integrals (30 digits) of the note's formulas:
#   B0^ab(p^2) = -int_0^1 dx ln(Delta_x - i0),  B1^ab(p^2) = int_0^1 dx x ln(Delta_x - i0),  A0 = m^2 (1 - ln m^2),
#   Delta_x = x m_b^2 + (1-x) m_a^2 - x(1-x) p^2;
#   F1^Lambda = pole [1 + (2m^2 - q^2) I0] + finite [-2 - I_L - (2m^2 - q^2) I_LH + 2 (3m^2 - q^2) I0],
#   F2 = 2 m^2 I0,  I0 = int dw/h, I_L = int dw ln h, I_LH = int dw ln(h)/h,  h = m^2 - q^2 w (1-w)
#   (the z integration of Eq. (5) done, App. D; for q^2 < 4 m^2 only, where h > 0; above threshold COLLIER is the reference);
#   R - 1: pole -(3 - xi), finite -4 + 3 ln m^2 (Eq. (10)).
# Missing values: LoopTools and COLLIER fail for the IR-divergent C0(m^2, 0, m^2; 0, m^2, m^2) at q^2 = 0 (F1 at q^2 = 0 is
# Package-X only); Package-X does not evaluate DB0, DB1 (R is LoopTools and COLLIER only).
# Reads results/oneloop_mathematica.csv and results/oneloop_collier.csv, writes results/oneloop_comparison.csv.
# Batch: `~/miniforge3/envs/qft/bin/python oneloop_numeric.py` (from Src/).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import sys

import mpmath as mp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
MASS = {"e": mp.mpf(1), "mu": mp.mpf("1.7")}


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
    return mp.quad(lambda x: x ** power * log_m_i0(delta(x)) if delta(x) != 0 else 0, pts)


def a0(m2):
    m2 = mp.mpf(m2)
    return m2 * (1 - mp.log(m2))


def b0(p2, ma2, mb2):
    return -feynman_b(p2, ma2, mb2, 0)


def b1(p2, ma2, mb2):
    return feynman_b(p2, ma2, mb2, 1)


def pi_f(q2, m):
    m2 = m * m
    q2 = mp.mpf(q2)
    return -mp.mpf(4) / 3 * ((1 + 2 * m2 / q2) * b0(q2, m2, m2) - 2 * m2 / q2 * b0(0, m2, m2) - mp.mpf(1) / 3)


def vertex(q2, m):
    """(pole, finite) of K F1^Lambda / e^2 and K F2 / e^2 from the w integrals; q2 < 4 m^2"""
    m2, q2 = m * m, mp.mpf(q2)
    h = lambda w: m2 - q2 * w * (1 - w)
    i0 = mp.quad(lambda w: 1 / h(w), [0, 0.5, 1])
    il = mp.quad(lambda w: mp.log(h(w)), [0, 0.5, 1])
    ilh = mp.quad(lambda w: mp.log(h(w)) / h(w), [0, 0.5, 1])
    return (1 + (2 * m2 - q2) * i0, -2 - il - (2 * m2 - q2) * ilh + 2 * (3 * m2 - q2) * i0), 2 * m2 * i0


def reference(func, arg, xi):
    """(pole, finite) from the note's formulas with mpmath; None where COLLIER is the reference"""
    fam, _, fl = func.partition("_")
    if fam == "Pi":
        return 0, complex(pi_f(arg, MASS[fl]))
    if fam in ("SigV", "SigS"):
        m2 = MASS[fl] ** 2
        if fam == "SigV":
            return 0, complex(xi * (1 + 2 * b1(arg, m2, 0)))
        return 0, complex((3 + xi) * b0(arg, m2, 0) - 2)
    if fam in ("F1", "F2"):
        if arg >= 4:
            return None
        (pole, fin), f2 = vertex(arg, MASS["e"])
        return (complex(pole), complex(fin)) if fam == "F1" else (0, complex(f2))
    if fam == "R":
        return -(3 - xi), complex(-4 + 3 * mp.log(MASS[fl] ** 2))
    return None


def read(name, cols):
    out = []
    with open(os.path.join(HERE, "results", name)) as fh:
        for r in csv.DictReader(fh):
            vals = []
            for c in cols:
                pole = complex(float(r["re_pole_" + c]), float(r["im_pole_" + c]))
                fin = complex(float(r["re_" + c]), float(r["im_" + c]))
                vals.append((pole, fin))
            out.append((r["func"], float(r["arg"]), float(r["xi"]), vals))
    return out


def read_collier():
    with open(os.path.join(HERE, "results", "oneloop_collier.csv")) as fh:
        return {(r["func"], round(float(r["arg"]), 10), round(float(r["xi"]), 10)):
                (complex(float(r["re_pole"]), float(r["im_pole"])), complex(float(r["re_fin"]), float(r["im_fin"])))
                for r in csv.DictReader(fh)}


mma = read("oneloop_mathematica.csv", ("px", "lt"))
col = read_collier()
mma[:3]          # inspect

# %% [markdown]
# ## Comparison
#
# Finite parts: relative deviation from the reference (absolute where |ref| < 1e-3, e.g. Sigma_V at xi = 0, which is 0).
# Poles: absolute deviation of the 1/eps coefficient.  nan marks a value the tool cannot give.

# %%
def dev(x, ref):
    if x is None or any(math.isnan(v) for v in (x.real, x.imag)):
        return float("nan")
    return abs(x - ref) / max(abs(ref), 1e-3)


rows, worst = [], {}
for func, arg, xi, ((ppx, fpx), (plt, flt)) in mma:
    key = (func, round(arg, 10), round(xi, 10))
    pcl, fcl = col[key]
    ref = reference(func, arg, xi)
    src = "mpmath/note"
    if ref is None:
        ref, src = (pcl, fcl), "COLLIER"
    pref, fref = complex(ref[0]), complex(ref[1])
    d = {"Package-X": (dev(fpx, fref), abs(ppx - pref)), "LoopTools": (dev(flt, fref), abs(plt - pref)),
         "COLLIER": (dev(fcl, fref), abs(pcl - pref))}
    fam = func.split("_")[0]
    for tool, (df, dp) in d.items():
        if src == "COLLIER" and tool == "COLLIER":
            continue
        for kind, v in (("finite", df), ("pole", dp)):
            if not math.isnan(v):
                worst[(fam, tool, kind)] = max(worst.get((fam, tool, kind), 0.0), v)
    rows.append((func, arg, xi, src, pref.real, fref.real, fref.imag, *[x for t in d.values() for x in t]))
    print(f"{func:7s} {arg:6.2f} xi={xi:3.1f}  ref({src:11s}) pole {pref.real:+.6f}  finite {fref.real:+.12f} {fref.imag:+.12f}i  "
          + "  ".join(f"{t[:2]} {v[0]:.1e}/{v[1]:.0e}" for t, v in d.items()))
print("max deviation (finite: relative, pole: absolute) by function and tool:")
for (fam, tool, kind), v in sorted(worst.items()):
    print(f"  {fam:5s} {tool:10s} {kind:6s} {v:.1e}")

with open(os.path.join(HERE, "results", "oneloop_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg", "xi", "reference", "pole_ref", "re_ref", "im_ref", "dev_px", "dpole_px", "dev_lt", "dpole_lt",
                "dev_collier", "dpole_collier"])
    w.writerows(rows)
print("wrote results/oneloop_comparison.csv")
