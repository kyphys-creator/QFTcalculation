# %% [markdown]
# # Step (3): finite parts of the one-loop self-energies -- LoopTools, Package-X, COLLIER and mpmath (Standard Model)
#
# Research note models/sm, step (3), section (e) of oneloop_feyncalc.wl.  The note's formulas Eqs. (T), (SAA)-(SWW),
# (SH) (K Sigma, K = (4 pi)^2, all three generations) at a numerical point are written by oneloop_feyncalc.wl as
# a constant plus a linear combination of B0 functions (results/oneloop_coeffs.csv); the B0 values come from LoopTools
# and Package-X (results/oneloop_b0.csv) and COLLIER (results/oneloop_collier.csv, oneloop_collier.f90), all with
# Delta = 0 and mu = MZ.  The reference, independent of the three tools, is the Feynman-parameter integral (mpmath,
# 30 digits)
#   B0(p^2; m1^2, m2^2) = -int_0^1 dx ln[(x m2^2 + (1-x) m1^2 - x(1-x) p^2 - i0)/mu^2].
# Optical theorem: Im Sigma_T^V(M_V^2)/M_V and Im Sigma^H(M_H^2)/M_H against the sums of the tree-level fermion-pair
# widths (massive formulas of App. B; the bosonic thresholds are closed at this point).
# Writes results/oneloop_comparison.csv.
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
RES = os.path.join(HERE, "results")
MU2 = mp.mpf("91.1880") ** 2


def log_m_i0(x):
    """ln(x - i0) for real x."""
    return mp.log(x) if x > 0 else mp.log(-x) - 1j * mp.pi


def b0_ref(p2, m1, m2):
    """-int_0^1 dx ln(Delta_x - i0)/mu^2; the zeros of Delta_x in (0, 1) are passed to quad as break points."""
    p2, m1, m2 = mp.mpf(p2), mp.mpf(m1), mp.mpf(m2)
    delta = lambda x: x * m2 + (1 - x) * m1 - x * (1 - x) * p2
    pts = [mp.mpf(0)]
    if p2 != 0:
        a, b, c = p2, m2 - m1 - p2, m1
        disc = b * b - 4 * a * c
        if disc > 0:
            pts += sorted(r for r in ((-b - mp.sqrt(disc)) / (2 * a), (-b + mp.sqrt(disc)) / (2 * a)) if 0 < r < 1)
    pts.append(mp.mpf(1))
    return -mp.quad(lambda x: log_m_i0(delta(x) / MU2) if delta(x) != 0 else 0, pts)


# %% [markdown]
# ## The B0 functions

# %%
with open(os.path.join(RES, "oneloop_b0.csv")) as f:
    b0rows = list(csv.DictReader(f))
with open(os.path.join(RES, "oneloop_collier.csv")) as f:
    coll = {int(r["index"]): complex(float(r["re_collier"]), float(r["im_collier"])) for r in csv.DictReader(f)}
B0 = {}
for r in b0rows:
    i = int(r["index"])
    ref = b0_ref(r["p2"], r["m1sq"], r["m2sq"])
    B0[i] = {"lt": complex(float(r["re_lt"]), float(r["im_lt"])), "px": complex(float(r["re_px"]), float(r["im_px"])),
             "collier": coll[i], "mpmath": complex(ref)}
worst = {t: max(abs(B0[i][t] - B0[i]["mpmath"]) / max(abs(B0[i]["mpmath"]), 1e-300) for i in B0) for t in ("lt", "px", "collier")}
print(f"{len(B0)} B0 functions; max relative deviation from the mpmath integral: LoopTools {worst['lt']:.1e}, "
      f"Package-X {worst['px']:.1e}, COLLIER {worst['collier']:.1e}")

# %% [markdown]
# ## The self-energies

# %%
with open(os.path.join(RES, "oneloop_coeffs.csv")) as f:
    crows = list(csv.DictReader(f))
points = []
for r in crows:
    key = (r["key"], float(r["kk"]))
    if key not in points:
        points.append(key)
out = []
print(f"{'quantity':5s} {'k^2 (GeV^2)':>13s}  {'mpmath (re, im)':>42s}   rel. dev.: LoopTools, Package-X, COLLIER")
maxdev = {"lt": 0.0, "px": 0.0, "collier": 0.0}
for key in points:
    rows = [r for r in crows if (r["key"], float(r["kk"])) == key]
    val = {}
    for t in ("lt", "px", "collier", "mpmath"):
        v = 0j
        for r in rows:
            c = float(r["coefficient"])
            v += c if r["index"] == "0" else c * B0[int(r["index"])][t]
        val[t] = v
    dev = {t: abs(val[t] - val["mpmath"]) / abs(val["mpmath"]) for t in ("lt", "px", "collier")}
    for t in dev:
        maxdev[t] = max(maxdev[t], dev[t])
    print(f"{key[0]:5s} {key[1]:13.4f}  {val['mpmath'].real:+.14e} {val['mpmath'].imag:+.6e}   "
          f"{dev['lt']:.1e}, {dev['px']:.1e}, {dev['collier']:.1e}")
    out.append([key[0], key[1], val["mpmath"].real, val["mpmath"].imag] + [x for t in ("lt", "px", "collier") for x in (val[t].real, val[t].imag)])
print(f"max relative deviation of the self-energies from the mpmath values: LoopTools {maxdev['lt']:.1e}, "
      f"Package-X {maxdev['px']:.1e}, COLLIER {maxdev['collier']:.1e}")

# %% [markdown]
# ## Optical theorem: Im Sigma_T^V(M_V^2) = M_V sum_f Gamma(V -> f fbar'),  Im Sigma^H(M_H^2) = M_H sum_f Gamma(H -> f fbar)
#
# At this point the bosonic thresholds are closed (2 M_W > M_Z, M_H; M_Z + M_H > M_W, M_Z; the W-photon threshold of
# Sigma^W sits exactly at k^2 = M_W^2 and gives no imaginary part), so only the open fermion channels contribute.  The
# widths are the massive tree-level formulas of App. B (step (2)) with the parameters of this point (alpha(0), CKM = 1).

# %%
ALPHA = mp.mpf(1) / mp.mpf("137.035999177")
MWv, MZv, MHv = mp.mpf("80.3692"), mp.mpf("91.1880"), mp.mpf("125.20")
CW2 = MWv ** 2 / MZv ** 2
SW2 = 1 - CW2
EE2 = 4 * mp.pi * ALPHA
GENS = [(mp.mpf("0.000510998950"), mp.mpf("0.00216"), mp.mpf("0.00470")), (mp.mpf("0.1056583755"), mp.mpf("1.2730"), mp.mpf("0.0935")),
        (mp.mpf("1.77686"), mp.mpf("172.57"), mp.mpf("4.183"))]


def pcm(M, m1, m2):
    """momentum of the decay products; None below threshold"""
    if M <= m1 + m2:
        return None
    return mp.sqrt((M ** 2 - (m1 + m2) ** 2) * (M ** 2 - (m1 - m2) ** 2)) / (2 * M)


def gam_v(M, m1, m2, v, a, nc):
    """V -> f1 fbar2, vertex i gamma (v - a gamma5), averaged over the three polarizations"""
    p = pcm(M, m1, m2)
    if p is None:
        return mp.mpf(0)
    return nc * p / (6 * mp.pi * M ** 2) * ((v * v + a * a) * (M ** 2 - (m1 ** 2 + m2 ** 2) / 2 - (m1 ** 2 - m2 ** 2) ** 2 / (2 * M ** 2))
                                           + 3 * (v * v - a * a) * m1 * m2)


def gam_h(m, nc):
    if 2 * m >= MHv:
        return mp.mpf(0)
    return nc * ALPHA * MHv * m ** 2 / (8 * SW2 * MWv ** 2) * (1 - 4 * m ** 2 / MHv ** 2) ** mp.mpf(1.5)


ee, s, c = mp.sqrt(EE2), mp.sqrt(SW2), mp.sqrt(CW2)
gw = ee / (2 * mp.sqrt(2) * s)
gamW = sum(gam_v(MWv, ml, 0, gw, gw, 1) + gam_v(MWv, mu, md, gw, gw, 3) for ml, mu, md in GENS)
gamZ = mp.mpf(0)
for ml, mu, md in GENS:
    for (m, Q, T3, nc) in ((0, 0, mp.mpf(1) / 2, 1), (ml, -1, -mp.mpf(1) / 2, 1), (mu, mp.mpf(2) / 3, mp.mpf(1) / 2, 3), (md, -mp.mpf(1) / 3, -mp.mpf(1) / 2, 3)):
        gamZ += gam_v(MZv, m, m, ee * (T3 - 2 * Q * SW2) / (2 * s * c), ee * T3 / (2 * s * c), nc)
gamH = sum(gam_h(ml, 1) + gam_h(mu, 3) + gam_h(md, 3) for ml, mu, md in GENS)
K = (4 * mp.pi) ** 2
for key, M, G in (("WW", MWv, gamW), ("ZZ", MZv, gamZ), ("HH", MHv, gamH)):
    row = [o for o in out if o[0] == key and abs(o[1] - float(M ** 2)) < 1e-6][0]
    im = mp.mpf(row[3]) / K
    print(f"optical theorem {key}: Im Sigma(M^2)/M = {mp.nstr(im / M, 15)} GeV,  sum of tree widths = {mp.nstr(G, 15)} GeV,"
          f"  rel. diff. {mp.nstr(abs(im / M / G - 1), 2)}")

with open(os.path.join(RES, "oneloop_comparison.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["key", "kk", "re_mpmath", "im_mpmath", "re_lt", "im_lt", "re_px", "im_px", "re_collier", "im_collier"])
    for row in out:
        wr.writerow([row[0], repr(row[1])] + [f"{x:.16e}" for x in row[2:]])
print("wrote results/oneloop_comparison.csv")
