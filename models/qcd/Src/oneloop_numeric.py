# %% [markdown]
# # Step (3): renormalized one-loop two-point functions of QCD -- Package-X, LoopTools and COLLIER against the note
#
# Research note models/qcd, Eq. (8) (eq:VR), at g = 1, m = mu = 1, C_A = 3, C_F = 4/3, T_F = 1/2.  All brackets are K/g^2
# times the note's quantity (K = (4 pi)^2), split into the 1/eps coefficient minus the counterterm ("pole", must be 0)
# and the MS-bar finite part:
# - PiYM (k^2, xi): the gluon + ghost loops of the gluon self-energy;  PiQ0, PiT (k^2): one massless and the t quark loop;
# - Ghost (p^2, xi): the ghost self-energy;  SigV_t, SigS_t (p^2, xi): Sigma_V^R, Sigma_S^R of t;  SigV_u (p^2, xi).
# Package-X and LoopTools evaluate the FeynCalc amplitudes (oneloop_feyncalc.wl: the FeynArts diagrams reduced by TID and
# the IBP relations); COLLIER evaluates the note's Eq. (8) (oneloop_collier.f90).  The references, independent of the
# three tools, are mpmath integrals (30 digits) of Eq. (8):
#   B0^ab(p^2) = -int_0^1 dx ln(Delta_x - i0),  B1^ab(p^2) = int_0^1 dx x ln(Delta_x - i0),
#   Delta_x = x m_b^2 + (1-x) m_a^2 - x(1-x) p^2   (mu = 1).
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
CA, CF, TF, M = mp.mpf(3), mp.mpf(4) / 3, mp.mpf(1) / 2, mp.mpf(1)


def log_m_i0(x):
    """ln(x - i0) for real x."""
    return mp.log(x) if x > 0 else mp.log(-x) - 1j * mp.pi


def feynman_b(p2, ma2, mb2, power):
    """int_0^1 dx x^power ln(Delta_x - i0); the zeros of Delta_x in (0, 1) are passed to quad as break points."""
    p2, ma2, mb2 = mp.mpf(p2), mp.mpf(ma2), mp.mpf(mb2)
    delta = lambda x: x * mb2 + (1 - x) * ma2 - x * (1 - x) * p2
    pts = [mp.mpf(0)]
    if p2 != 0:
        a, b, c = p2, mb2 - ma2 - p2, ma2
        disc = b * b - 4 * a * c
        if disc > 0:
            pts += sorted(r for r in ((-b - mp.sqrt(disc)) / (2 * a), (-b + mp.sqrt(disc)) / (2 * a)) if 0 < r < 1)
    pts.append(mp.mpf(1))
    return mp.quad(lambda x: x ** power * log_m_i0(delta(x)) if delta(x) != 0 else 0, pts)


def b0(p2, ma2, mb2):
    return -feynman_b(p2, ma2, mb2, 0)


def b1(p2, ma2, mb2):
    return feynman_b(p2, ma2, mb2, 1)


def reference(func, arg, xi):
    """MS-bar finite part of K/g^2 times Eq. (8)"""
    xi = mp.mpf(xi)
    eta = 1 - xi
    m2 = M * M
    if func == "PiYM":
        return CA * ((mp.mpf(5) / 3 + eta / 2) * b0(arg, 0, 0) + mp.mpf(1) / 9 - 2 * eta + eta ** 2 / 4)
    if func == "PiQ0":
        return -mp.mpf(4) / 3 * TF * (b0(arg, 0, 0) - mp.mpf(1) / 3)
    if func == "PiT":
        k2 = mp.mpf(arg)
        return -mp.mpf(4) / 3 * TF * ((1 + 2 * m2 / k2) * b0(k2, m2, m2) - 2 * m2 / k2 * b0(0, m2, m2) - mp.mpf(1) / 3)
    if func == "Ghost":
        return -CA * ((3 - xi) / 4 * b0(arg, 0, 0) - (1 - xi) / 2)
    if func == "SigV_t":
        return xi * CF * (1 + 2 * b1(arg, m2, 0))
    if func == "SigS_t":
        return CF * ((3 + xi) * b0(arg, m2, 0) - 2)
    if func == "SigV_u":
        return xi * CF * (1 + 2 * b1(arg, 0, 0))
    raise ValueError(func)


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
# Finite parts: relative deviation from the mpmath reference (absolute where |ref| < 1e-3, e.g. Sigma_V at xi = 0).
# Poles: absolute value of (1/eps coefficient - counterterm), which must vanish.

# %%
def dev(x, ref):
    if x is None or any(math.isnan(v) for v in (x.real, x.imag)):
        return float("nan")
    return abs(x - ref) / max(abs(ref), 1e-3)


rows, worst = [], {}
for func, arg, xi, ((ppx, fpx), (plt, flt)) in mma:
    pcl, fcl = col[(func, round(arg, 10), round(xi, 10))]
    fref = complex(reference(func, mp.mpf(arg), xi))
    d = {"Package-X": (dev(fpx, fref), abs(ppx)), "LoopTools": (dev(flt, fref), abs(plt)), "COLLIER": (dev(fcl, fref), abs(pcl))}
    for tool, (df, dp) in d.items():
        for kind, v in (("finite", df), ("pole", dp)):
            if not math.isnan(v):
                worst[(func, tool, kind)] = max(worst.get((func, tool, kind), 0.0), v)
    rows.append((func, arg, xi, fref.real, fref.imag, *[x for t in d.values() for x in t]))
    print(f"{func:7s} {arg:6.2f} xi={xi:3.1f}  ref {fref.real:+.12f} {fref.imag:+.12f}i  "
          + "  ".join(f"{t[:2]} {v[0]:.1e}/{v[1]:.0e}" for t, v in d.items()))
print("max deviation (finite: relative, pole - counterterm: absolute) by function and tool:")
for (func, tool, kind), v in sorted(worst.items()):
    print(f"  {func:7s} {tool:10s} {kind:6s} {v:.1e}")

with open(os.path.join(HERE, "results", "oneloop_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg", "xi", "re_ref", "im_ref", "dev_px", "dpole_px", "dev_lt", "dpole_lt", "dev_collier", "dpole_collier"])
    w.writerows(rows)
print("wrote results/oneloop_comparison.csv")
