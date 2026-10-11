# %% [markdown]
# # Step (3): one-loop 1PI functions of phi^3 + phi^4 -- Package-X, LoopTools and COLLIER compared
#
# The brackets b_n = (4 pi)^2 V_n^R / i of Eq. (6) of the note (models/phi34) at m = mu = g = lambda = 1:
#   b2 = [B0(p^2) + A0]/2,  b3 = C0 + sum B0/2,  b4 = sum_x B0(x)/2 + 2 sum_x C0(m^2, m^2, x) + sum D0.
# Package-X and LoopTools evaluate the FeynCalc amplitudes (oneloop_feyncalc.wl); COLLIER evaluates the note's formula
# (oneloop_collier.f90).  b2 also against the closed form of B0 (phi^3 note, App. G) with A0 = 1.
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


def b0_closed(p2):
    """MS-bar B0(p^2; 1, 1) at mu = 1 (phi^3 note, App. G)."""
    p2 = mp.mpf(p2)
    if p2 < 0:
        beta = mp.sqrt(1 - 4 / p2)
        return 2 + beta * mp.log((beta - 1) / (beta + 1))
    if p2 == 0:
        return mp.mpf(0)
    if p2 < 4:
        bt = mp.sqrt(4 / p2 - 1)
        return 2 - 2 * bt * mp.atan(1 / bt)
    beta = mp.sqrt(1 - 4 / p2)
    return 2 + beta * mp.log((1 - beta) / (1 + beta)) + 1j * mp.pi * beta


def read(name, cols):
    with open(os.path.join(HERE, "results", name)) as fh:
        return [(r["func"], float(r["arg1"]), float(r["arg2"]), float(r["arg3"]),
                 complex(float(r["re_" + cols[0]]), float(r["im_" + cols[0]])),
                 complex(float(r["re_" + cols[1]]), float(r["im_" + cols[1]])) if len(cols) > 1 else None)
                for r in csv.DictReader(fh)]


mma = read("oneloop_mathematica.csv", ("packagex", "looptools"))
col = read("oneloop_collier.csv", ("collier",))
assert len(mma) == len(col)
mma[:3]          # inspect

# %% [markdown]
# ## Comparison (relative to COLLIER; b2 also to the closed form)

# %%
rows, worst = [], {}
for (f, a1, a2, a3, px, lt), (_, _, _, _, cl, _) in zip(mma, col):
    ref = complex(b0_closed(a1) + 1) / 2 if f == "V2" else cl
    dpx, dlt, dcl = (abs(z - ref) / abs(ref) for z in (px, lt, cl))
    rows.append((f, a1, a2, a3, ref.real, ref.imag, dpx, dlt, dcl))
    print(f"{f} ({a1:7.3f}, {a2:7.3f}, {a3:5.1f}):  b = {ref.real:+.12f} {ref.imag:+.12f} i   "
          f"rel. dev.  Package-X {dpx:.1e}  LoopTools {dlt:.1e}" + (f"  COLLIER {dcl:.1e}" if f == "V2" else ""))
    for name, d in (("Package-X", dpx), ("LoopTools", dlt), ("COLLIER", dcl)):
        if not (f == "V3" and a1 < 0 and name == "LoopTools"):
            worst[(f, name)] = max(worst.get((f, name), 0.0), d)
print("max relative deviation by function and tool (LoopTools at the Euclidean V3 point excluded):")
for (f, name), d in sorted(worst.items()):
    if not (f != "V2" and name == "COLLIER"):
        print(f"  {f} {name:10s} {d:.1e}")
lt_eu = [r for r in rows if r[0] == "V3" and r[1] < 0][0]
print(f"LoopTools at the Euclidean V3 point (k1^2, k2^2, p^2) = (-1, -2, -3): relative deviation {lt_eu[7]:.1e} "
      "(FF error 'eta is not defined'; Package-X and COLLIER agree)")

with open(os.path.join(HERE, "results", "oneloop_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg1", "arg2", "arg3", "re_ref", "im_ref", "reldev_packagex", "reldev_looptools", "reldev_collier"])
    w.writerows(rows)
print("wrote results/oneloop_comparison.csv")
