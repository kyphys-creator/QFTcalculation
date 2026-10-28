# %% [markdown]
# # Step (2): renormalization-group invariance of the Landau-gauge effective potential, numerically (TSIL)
#
# Research note models/abelian_higgs_2loop, step (2).  Along the RG flow (couplings, m2, the vacuum energy Lam and the
# background field phi run with the RG functions of rg2_mv.wl, results/rg2_beta.csv), the effective potential
# V = V0 + V1/K + V2/K^2 (Landau gauge, K = 16 pi^2) changes only at the first order left out.  From Q = 1 to Q = 2:
#   (a) V0 + V1/K with one-loop running: the change is O(1/K^2);
#   (b) V0 + V1/K + V2/K^2 with one-loop running: still O(1/K^2) (the two-loop RG functions are missing);
#   (c) V0 + V1/K + V2/K^2 with two-loop running: O(1/K^3).
# To see the orders, the couplings are scaled as lam -> s lam, e^2 -> s e^2, phi -> phi/sqrt(s) at fixed m2: the masses
# do not change, V0 ~ 1/s, V1 ~ 1, V2 ~ s, so the changes (a), (b) go as s and (c) as s^2.
# Start: e = 1/2, lam = 25/32, m2 = 25/8, phi = 3, Lam = 0 at Q = 1.  I(x,y,z) at Q^2 != 1 from TSIL 1.46
# (work/v2_tsil).  Writes results/rg2_numeric.csv.  Usage (from Src/, after rg2_mv.wl and building work/v2_tsil):
#     ~/miniforge3/envs/qft/bin/python rg2_numeric.py

# %%
import csv
import math
import os
import subprocess
from fractions import Fraction

from scipy.integrate import solve_ivp

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
K = 16 * math.pi ** 2
E0, LAM0, M20, PHI0 = 0.5, 25 / 32, 25 / 8, 3.0

# the RG functions: coefficient of lam^i e^j m2^k at each loop order
RG = {}
with open(os.path.join(HERE, "results", "rg2_beta.csv")) as fh:
    for r in csv.DictReader(fh):
        RG.setdefault((r["function"], int(r["loops"])), []).append(
            (int(r["power_lam"]), int(r["power_e"]), int(r["power_m2"]), float(Fraction(r["coefficient"]))))


def rgf(name, loops, lam, e, m2):
    return sum(c * lam ** i * e ** j * m2 ** k for i, j, k, c in RG.get((name, loops), []))


def flow(t, y, nloop):
    lam, e, m2, lv, phi = y
    out = [sum(rgf(n, L, lam, e, m2) / K ** L for L in range(1, nloop + 1)) for n in ("lam", "el", "m2", "Lam")]
    return out + [-phi * sum(rgf("gamma", L, lam, e, m2) / K ** L for L in range(1, nloop + 1))]


# %% [markdown]
# ## V0, V1 and V2 at the scale Q

# %%
def tsil(triples, qq):
    inp = "".join("%.17g,%.17g,%.17g,%.17g\n" % (t + (qq,)) for t in triples)
    out = subprocess.run([os.path.join(HERE, "work", "v2_tsil")], input=inp, capture_output=True, text=True,
                         check=True).stdout
    return [float(r["I"]) for r in csv.DictReader(out.splitlines())]


def potential(y, qq, nv):
    lam, e, m2, lv, phi = y
    xh, xg, xa = -m2 + 3 * lam * phi ** 2, -m2 + lam * phi ** 2, e ** 2 * phi ** 2
    A = lambda x: 0.0 if x == 0 else x * (math.log(x / qq) - 1)
    v = lv - m2 * phi ** 2 / 2 + lam * phi ** 4 / 4
    if nv >= 1:
        f = lambda x, c: x * x * (math.log(x / qq) - c)
        v += (f(xh, 1.5) + f(xg, 1.5) + 3 * f(xa, 5 / 6)) / 4 / K
    if nv >= 2:
        trip = [(xh, xh, xh), (xh, xg, xg), (xh, xg, xa), (0.0, xh, xg), (xa, xa, xh), (0.0, xa, xh), (0.0, 0.0, xh)]
        Ihhh, Ihgg, Ihga, I0hg, Iaah, I0ah, I00h = tsil(trip, qq)
        lk = -xh * xh - xg * xg - xa * xa + 2 * xh * xg + 2 * xh * xa + 2 * xg * xa
        fssv = ((lk * Ihga + (xh - xg) ** 2 * I0hg + (xg - xh - xa) * A(xh) * A(xa) + (xh - xg - xa) * A(xg) * A(xa)
                 + xa * A(xh) * A(xg)) / xa + 2 * (xh + xg - xa / 3) * A(xa))
        fvs = lambda x, y_: 3 * A(x) * A(y_) + 2 * x * A(y_)
        c = -xa * xa - xa * xa - xh * xh - 10 * xa * xa + 2 * xa * xh + 2 * xa * xh
        fvvs = ((c * Iaah + 2 * (xa - xh) ** 2 * I0ah - xh * xh * I00h + (xh - 2 * xa) * A(xa) ** 2
                 + 2 * xa * A(xa) * A(xh)) / (4 * xa * xa) + A(xa) + 2 * A(xh) - 2 * xa - xh)
        v2 = (-3 * lam ** 2 * phi ** 2 * Ihhh - lam ** 2 * phi ** 2 * Ihgg + 0.75 * lam * (A(xh) ** 2 + A(xg) ** 2)
              + 0.5 * lam * A(xh) * A(xg) + e ** 2 / 2 * fssv + e ** 2 / 2 * (fvs(xa, xh) + fvs(xa, xg))
              + e ** 4 * phi ** 2 * fvvs)
        v += v2 / K ** 2
    return v


# %% [markdown]
# ## The change of V from Q = 1 to Q = 2 along the flow

# %%
rows = []
cases = (("a", 1, 1), ("b", 2, 1), ("c", 2, 2))     # (label, loops in V, loops in the running)
for s in (1.0, 0.5, 0.25, 0.125):
    y0 = [s * LAM0, math.sqrt(s) * E0, M20, 0.0, PHI0 / math.sqrt(s)]
    d = {}
    for lab, nv, nrg in cases:
        sol = solve_ivp(flow, (0.0, math.log(2.0)), y0, args=(nrg,), method="DOP853", rtol=1e-13, atol=1e-15)
        y1 = sol.y[:, -1]
        d[lab] = potential(y1, 4.0, nv) - potential(y0, 1.0, nv)
    v = potential(y0, 1.0, 2)
    print("(%s) s = %-5g V = %.10f;  V(Q=2) - V(Q=1): (a) %.6e  (b) %.6e  (c) %.6e"
          % ("abc", s, v, d["a"], d["b"], d["c"]))
    rows.append([s, v, d["a"], d["b"], d["c"]])
for r0, r1 in zip(rows, rows[1:]):
    print("(abc) ratio s = %g / s = %g: (a) %.4f  (b) %.4f  (c) %.4f  (expect 2, 2, 4)"
          % (r0[0], r1[0], r0[2] / r1[2], r0[3] / r1[3], r0[4] / r1[4]))
with open(os.path.join(HERE, "results", "rg2_numeric.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["s", "V_Q1", "dV_a_V1_RG1", "dV_b_V2_RG1", "dV_c_V2_RG2"])
    for r in rows:
        w.writerow(["%.17g" % x for x in r])
print("written results/rg2_numeric.csv")
