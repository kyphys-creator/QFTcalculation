# %% [markdown]
# # Step (3): the Goldstone boson at small G, numerically (TSIL)
#
# Research note models/abelian_higgs_2loop, step (3).  Landau gauge, K = 16 pi^2, G = -m2 + lam phi^2.
#   (a) Martin's formulas used in goldstone_ir.wl (arXiv:1406.2355): the derivative dI/dx (Eq. (A.23)) against central
#       differences, and the small-G expansions of I(G,G,x), I(G,x,y) (Eqs. (A.27), (A.28)) against TSIL;
#   (b) near the tree minimum (Q = 1): K (1/phi) d(V - V0)/dphi (analytic, from goldstone_ir.wl) for the one-loop,
#       the two-loop, and the resummed two-loop potential
#           Vh = V + [f(G + Delta1/K) - f(G)]/K - Delta1 A(G)/(2 K^2),  Delta1 = 3 lam A(H) + e^2 [3 A(xa) + 2 xa],
#       as G -> 0 (figs/goldstone.pdf);
#   (c) at Q = 2, where G > 0 at the minimum: the minimum of Vh and of the two-loop V found numerically, against the
#       G-free condition and the hbar expansion of goldstone_ir.wl (results/goldstone_min.csv), with the couplings
#       scaled by s (lam -> s lam, e^2 -> s e^2 at fixed m2).
# Writes results/goldstone_numeric.csv and figs/goldstone.pdf.  Usage (from Src/, after goldstone_ir.wl):
#     ~/miniforge3/envs/qft/bin/python goldstone_numeric.py

# %%
import csv
import math
import os
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
K = 16 * math.pi ** 2
E0, LAM0, M20 = 0.5, 25 / 32, 25 / 8


def tsil(triples, qq=1.0):
    inp = "".join("%.17g,%.17g,%.17g,%.17g\n" % (tuple(t) + (qq,)) for t in triples)
    out = subprocess.run([os.path.join(HERE, "work", "v2_tsil")], input=inp, capture_output=True, text=True,
                         check=True).stdout
    return [float(r["I"]) for r in csv.DictReader(out.splitlines())]


def Af(x, qq=1.0):
    return 0.0 if x == 0 else x * (math.log(x / qq) - 1)


# %% [markdown]
# ## (a) Martin's formulas against TSIL

# %%
def dI_formula(x, y, z, Ixyz):
    A = Af
    lk = x * x + y * y + z * z - 2 * x * y - 2 * x * z - 2 * y * z
    return ((x - y - z) * Ixyz - 2 * A(y) * A(z) + (x - y + z) * A(x) * A(y) / x + (x + y - z) * A(x) * A(z) / x
            + (y + z - x) * (A(x) + A(y) + A(z)) + x * x - (y + z) ** 2) / lk


worst = 0.0
for x, y, z in ((6.25, 0.3, 1.0), (6.25, 6.25, 6.25), (1.0, 1.0, 6.25), (0.3, 0.0, 6.25), (2.0, 0.0, 0.0)):
    h = 1e-4 * x
    Ip, Im, I0 = tsil([(x + h, y, z), (x - h, y, z), (x, y, z)])
    fd, fo = (Ip - Im) / (2 * h), dI_formula(x, y, z, I0)
    worst = max(worst, abs(fd / fo - 1))
    print("(a) dI/dx at (%g, %g, %g): central difference %.10f, Eq. (A.23) %.10f" % (x, y, z, fd, fo))
print("(a) largest relative difference: %.1e (central differences, step 1e-4 x)" % worst)
H0, XA0 = 6.25, 1.0
for G in (1e-3, 1e-4, 1e-5):
    lG = math.log(G)
    Igg, Iga, Ig0, I00, I0a = tsil([(G, G, H0), (G, H0, XA0), (G, 0.0, H0), (0.0, 0.0, H0), (0.0, H0, XA0)])
    e27 = I00 + 2 * G * (-H0 - I00 + 3 * Af(H0) - Af(H0) * lG) / H0

    def e28(x, y, I0xy):
        return I0xy + G * (-(x + y) * I0xy - 2 * Af(x) * Af(y) + 3 * x * Af(x) + 3 * y * Af(y) - y * Af(x)
                           - x * Af(y) - (x + y) ** 2 + (x - y) * (Af(y) - Af(x)) * lG) / (x - y) ** 2
    print("(a) G = %.0e: TSIL - expansion for I(G,G,h) %.2e, I(G,h,xa) %.2e, I(G,0,h) %.2e  (G^2 ln^2 G = %.1e)"
          % (G, Igg - e27, Iga - e28(H0, XA0, I0a), Ig0 - e28(0.0, H0, I00), G * G * lG * lG))


# %% [markdown]
# ## The potentials

# %%
def pot(lam, e, m2, phi, qq, mode):
    """V - V0 (Lam = 0): mode 1 = one loop, 2 = two loops, 'r' = resummed two loops."""
    xh, xg, xa = -m2 + 3 * lam * phi ** 2, -m2 + lam * phi ** 2, e ** 2 * phi ** 2
    A = lambda x: Af(x, qq)
    f = lambda x: x * x * (math.log(x / qq) - 1.5) / 4
    v = (f(xh) + f(xg) + 3 * xa * xa * (math.log(xa / qq) - 5 / 6) / 4) / K
    if mode == 1:
        return v
    Ihhh, Ihgg, Ihga, I0hg, Iaah, I0ah, I00h = tsil(
        [(xh, xh, xh), (xh, xg, xg), (xh, xg, xa), (0.0, xh, xg), (xa, xa, xh), (0.0, xa, xh), (0.0, 0.0, xh)], qq)
    lk = -xh * xh - xg * xg - xa * xa + 2 * xh * xg + 2 * xh * xa + 2 * xg * xa
    fssv = ((lk * Ihga + (xh - xg) ** 2 * I0hg + (xg - xh - xa) * A(xh) * A(xa) + (xh - xg - xa) * A(xg) * A(xa)
             + xa * A(xh) * A(xg)) / xa + 2 * (xh + xg - xa / 3) * A(xa))
    fvs = lambda x, y: 3 * A(x) * A(y) + 2 * x * A(y)
    c = -12 * xa * xa - xh * xh + 4 * xa * xh
    fvvs = ((c * Iaah + 2 * (xa - xh) ** 2 * I0ah - xh * xh * I00h + (xh - 2 * xa) * A(xa) ** 2
             + 2 * xa * A(xa) * A(xh)) / (4 * xa * xa) + A(xa) + 2 * A(xh) - 2 * xa - xh)
    v2 = (-3 * lam ** 2 * phi ** 2 * Ihhh - lam ** 2 * phi ** 2 * Ihgg + 0.75 * lam * (A(xh) ** 2 + A(xg) ** 2)
          + 0.5 * lam * A(xh) * A(xg) + e ** 2 / 2 * fssv + e ** 2 / 2 * (fvs(xa, xh) + fvs(xa, xg))
          + e ** 4 * phi ** 2 * fvvs)
    v += v2 / K ** 2
    if mode == "r":
        # G + Delta1/K is O(1/K^2) at the minimum; when it is negative, the real part (the imaginary part is O(1/K^5))
        fr = lambda x: 0.0 if x == 0 else x * x * (math.log(abs(x) / qq) - 1.5) / 4
        d1 = 3 * lam * A(xh) + e ** 2 * (3 * A(xa) + 2 * xa)
        v += (fr(xg + d1 / K) - f(xg)) / K - d1 * A(xg) / (2 * K ** 2)
    return v


def dpot(lam, e, m2, phi, qq, mode, h):
    """d(V - V0)/dphi, five-point central difference."""
    p = [pot(lam, e, m2, phi + k * h, qq, mode) for k in (-2, -1, 1, 2)]
    return (p[0] - 8 * p[1] + 8 * p[2] - p[3]) / (12 * h)


# %% [markdown]
# ## (b) The minimization condition near G = 0 (Q = 1)

# %%
# The derivatives are analytic (goldstone_ir.wl, section (g)): TSIL's I(G,G,h) in double precision is off by ~1e-6 at
# G/h ~ 1e-9, too much for finite differences with steps ~ G.
with open(os.path.join(HERE, "results", "goldstone_curve.csv")) as fh:
    cur = [[float(x) for x in (r["G"], r["one_loop"], r["two_loops"], r["resummed"])] for r in csv.DictReader(fh)]
gs = [c[0] for c in cur]
phi0 = math.sqrt(M20 / LAM0)
d1_0 = 3 * LAM0 * Af(2 * LAM0 * phi0 ** 2) + E0 ** 2 * (3 * Af(E0 ** 2 * phi0 ** 2) + 2 * E0 ** 2 * phi0 ** 2)
slope = (cur[0][2] - cur[16][2]) / math.log(gs[0] / gs[16])
print("(b) two loops: slope in ln G between G = 1e-10 and 1e-6: %.7f;  lam Dh1/K = %.7f" % (slope, LAM0 * d1_0 / K))
print("(b) resummed: change between G = 1e-10 and 1e-6: %.1e" % (cur[0][3] - cur[16][3]))

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, ax = plt.subplots(figsize=(4.6, 3.0))
sel = [c for c in cur if c[0] <= 1.001e-2]
ax.semilogx([c[0] for c in sel], [c[3] for c in sel], color="C0", lw=1.5, ls="-", label="two loops, resummed")
ax.semilogx([c[0] for c in sel], [c[2] for c in sel], color="C1", lw=1.5, ls="--", label="two loops")
ax.semilogx([c[0] for c in sel], [c[1] for c in sel], color="0.4", lw=1.0, ls=":", label="one loop")
ax.set_ylim(9.0, 12.4)
ax.set_xlabel(r"$G=x_G$ (tree-level Goldstone mass$^2$, $Q=1$)")
ax.set_ylabel(r"$K\,\phi^{-1}\,\partial(V-V_0)/\partial\phi$")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "goldstone.pdf"))
print("(b) written figs/goldstone.pdf")


# %% [markdown]
# ## (c) The minimum at Q = 2

# %%
with open(os.path.join(HERE, "results", "goldstone_min.csv")) as fh:
    ref = [r for r in csv.DictReader(fh) if float(r["Q"]) == 2.0]
rows = []
for r in ref:
    s = float(r["s"])
    lam, e = s * LAM0, math.sqrt(s) * E0
    g_est = -float(r["Dh1"]) / K
    vmin = {}
    for mode in ("r", 2):
        def dv(phi):
            return phi * (-M20 + lam * phi ** 2) + dpot(lam, e, M20, phi, 4.0, mode, 1e-6 * phi)
        lo, hi = math.sqrt((M20 + 0.3 * g_est) / lam), math.sqrt((M20 + 3 * g_est) / lam)
        vm = brentq(dv, lo, hi, xtol=1e-14, rtol=1e-15)
        vmin[mode] = (vm, -M20 * vm ** 2 / 2 + lam * vm ** 4 / 4 + pot(lam, e, M20, vm, 4.0, mode))
    vg, vh = float(r["v_Gfree"]), float(r["v_hbar"])
    rows.append([s, vmin["r"][0], vg, vh, vmin[2][0], vmin["r"][1], float(r["Vhat_min"]), float(r["Vmin_hbar"]),
                 vmin[2][1]])
    print("(c) s = %-5g v: resummed (numerical) %.12f, G-free %.12f, hbar %.12f, two loops (numerical) %.12f"
          % (s, vmin["r"][0], vg, vh, vmin[2][0]))
    print("(c)           V_min: resummed (numerical) %.12f, formula %.12f, hbar %.12f, two loops (numerical) %.12f"
          % (vmin["r"][1], float(r["Vhat_min"]), float(r["Vmin_hbar"]), vmin[2][1]))
for a, b in zip(rows, rows[1:]):
    print("(c) ratio s = %g / s = %g: v (resummed - G-free) %.3f, (resummed - hbar) %.3f, (two loops - resummed) %.3f;"
          "  V_min (resummed - hbar) %.3f  (expect 2^2.5 = 5.66, 5.66, 2^1.5 = 2.83; 4)"
          % (a[0], b[0], (a[1] - a[2]) / (b[1] - b[2]), (a[1] - a[3]) / (b[1] - b[3]), (a[4] - a[1]) / (b[4] - b[1]),
             (a[5] - a[7]) / (b[5] - b[7])))
with open(os.path.join(HERE, "results", "goldstone_numeric.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["s", "v_resummed_num", "v_Gfree", "v_hbar", "v_2loop_num", "Vmin_resummed_num", "Vhat_min_formula",
                "Vmin_hbar", "Vmin_2loop_num"])
    for r in rows:
        w.writerow(["%.17g" % x for x in r])
print("written results/goldstone_numeric.csv")
