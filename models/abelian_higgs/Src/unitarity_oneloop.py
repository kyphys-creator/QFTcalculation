# %% [markdown]
# # Step (9): one-loop s-wave partial waves of the scalar sector at high energy
#
# Research note models/abelian_higgs, step (9).  For s much larger than all masses and lam >> e^2 the scattering of
# A_L A_L, h h, A_L h is that of the two real components phi_1 = h, phi_2 = G (equivalence theorem) of
#     V = lam |Phi|^4 = (lam/4)(phi_1^2 + phi_2^2)^2,  lam_abcd = d^4 V/dphi_a dphi_b dphi_c dphi_d  (built by
# differentiation, as in rg_general.py).  Tree and one-loop MS-bar amplitudes (massless):
#     M0_abcd = -lam_abcd,
#     M1_abcd = (1/(2K)) sum_ef [lam_abef lam_efcd B(s) + lam_acef lam_efbd B(t) + lam_adef lam_efbc B(u)],
#     B(x) = 2 - ln(-x/mu^2 - i0),
# and the s wave a = N_i N_j (1/(32 pi)) Integral dc M over the symmetric two-particle states hh, GG (N = 1/sqrt 2) and
# hG (N = 1).  With L = ln(s/mu^2) the angular averages are <B(s)> = 2 - L + i pi, <B(t)> = <B(u)> = 3 - L.
#   (a) the tree matrix and its eigenvalues -lam/(4 pi) (charge 0), -lam/(8 pi) (charge 2, twice);
#   (b) checks of the one-loop matrix: Im A1 = A0 A0 (elastic unitarity, all channels open), A0 and A1 commute
#       (U(1)), and mu independence d(A0 + A1)/d ln mu = 0 with beta_lam = 20 lam^2/K (Eq. (rge) at e = 0);
#   (c) the eigenvalues at mu^2 = s, a1 = a0^2 (r + i), and where perturbation theory fails, |a1| = |a0|; Re(a0 + a1)
#       stays above -1/2 (its minimum is -pi/(4 r)), so |Re(a0 + a1)| = 1/2 is reached only after a0 + Re a1 has
#       changed sign;
# writes results/unitarity_oneloop.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python unitarity_oneloop.py

# %%
import csv
import itertools
import math
import os

import sympy as sp
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
lam, L, c = sp.symbols("lam L c", real=True)
K = 16 * sp.pi ** 2
phi = sp.symbols("phi1:3", real=True)
V = lam / 4 * (phi[0] ** 2 + phi[1] ** 2) ** 2
R = range(2)
l4 = {k: sp.diff(V, *[phi[i] for i in k]) for k in itertools.product(R, repeat=4)}
states = [((0, 0), 1 / sp.sqrt(2)), ((1, 1), 1 / sp.sqrt(2)), ((0, 1), sp.Integer(1))]   # hh, GG, hG

Bs = 2 - L + sp.I * sp.pi
Bt_avg = 3 - L          # <2 - ln(-t/mu^2)> with -t = s(1 - c)/2
assert sp.simplify(sp.integrate(sp.log((1 - c) / 2), (c, -1, 1)) / 2 + 1) == 0     # <ln(-t/s)> = -1


def tensor_sum(a, b, cc, d):
    return sum(l4[(a, b, e, f)] * l4[(e, f, cc, d)] for e in R for f in R)


A0 = sp.zeros(3, 3)
A1 = sp.zeros(3, 3)
for i, ((a, b), na) in enumerate(states):
    for j, ((cc, d), nb) in enumerate(states):
        A0[i, j] = sp.simplify(na * nb / (16 * sp.pi) * (-l4[(a, b, cc, d)]))
        m1 = (tensor_sum(a, b, cc, d) * Bs + tensor_sum(a, cc, b, d) * Bt_avg + tensor_sum(a, d, b, cc) * Bt_avg) / (2 * K)
        A1[i, j] = sp.simplify(na * nb / (16 * sp.pi) * m1)

# %% [markdown]
# ## (a) tree

# %%
print("(a) tree s-wave matrix (hh, GG, hG) x 16 pi/lam:", (A0 * 16 * sp.pi / lam).applyfunc(sp.simplify).tolist())
ev0 = A0.eigenvals()
print("(a) tree eigenvalues:", {sp.simplify(k): v for k, v in ev0.items()})

# %% [markdown]
# ## (b) checks

# %%
print("(b) Im A1 - A0 A0 (expect 0):", sp.simplify(A1.applyfunc(sp.im) - A0 * A0).tolist())
print("(b) [A0, A1] (expect 0):", sp.simplify(A0 * A1 - A1 * A0).tolist())
beta_lam = 20 * lam ** 2 / K            # Eq. (rge) at e = 0
# d/d ln mu^2: A0 through lam (d lam/d ln mu^2 = beta/2), A1 through L = ln s - ln mu^2
rg = sp.simplify(A0.diff(lam) * beta_lam / 2 - A1.diff(L))
print("(b) d(A0 + A1)/d ln mu^2 (expect 0):", rg.tolist())

# %% [markdown]
# ## (c) eigenvalues at mu^2 = s and the bounds

# %%
# eigenvectors of A0 diagonalize A1: charge 0 (hh + GG)/sqrt 2, charge 2: (hh - GG)/sqrt 2 and hG
vecs = {"charge 0": sp.Matrix([1, 1, 0]) / sp.sqrt(2), "charge 2 (hh - GG)": sp.Matrix([1, -1, 0]) / sp.sqrt(2),
        "charge 2 (hG)": sp.Matrix([0, 0, 1])}
eig = {}
for name, v in vecs.items():
    a0 = sp.simplify((v.T * A0 * v)[0])
    a1 = sp.simplify((v.T * A1 * v)[0].subs(L, 0))
    assert sp.simplify(A0 * v - a0 * v) == sp.zeros(3, 1) and sp.simplify(A1.subs(L, 0) * v - a1 * v) == sp.zeros(3, 1)
    eig[name] = (a0, a1)
    print("(c) %-18s a0 = %s,  a1(mu^2 = s) = %s  =  a0^2 (%s)" % (
        name, a0, sp.simplify(a1), sp.simplify(sp.expand(a1 / a0 ** 2))))

rows = []
for name, (a0, a1) in eig.items():
    re_tot = sp.lambdify(lam, sp.re(a0 + a1))
    ratio = sp.lambdify(lam, sp.Abs(a1) / sp.Abs(a0))
    lam_tree = float(sp.solve(sp.Eq(a0, -sp.Rational(1, 2)), lam)[0])     # a0 < 0
    # |Re(a0 + a1)| = 1/2 (the smallest lam), and |a1| = |a0|
    grid = [0.01 * k for k in range(1, 4001)]
    def first_cross(f, target):
        prev = None
        for x in grid:
            y = f(x) - target
            if prev is not None and prev * y < 0:
                return brentq(lambda z: f(z) - target, x - 0.01, x)
            prev = y
        return math.nan
    lam_nlo = first_cross(lambda x: abs(re_tot(x)), 0.5)
    lam_ratio = first_cross(ratio, 1.0)
    rows.append([name, lam_tree, lam_nlo, lam_ratio])
    print("(c) %-18s |a0| = 1/2 at lam = %.6f;  |a1| = |a0| at lam = %.6f (|a1/a0| at lam = 2 pi: %.4f);"
          "  min Re(a0 + a1) = %.6f;  |Re(a0 + a1)| = 1/2 at lam = %.6f" % (
              name, lam_tree, lam_ratio, ratio(2 * math.pi), min(re_tot(x) for x in grid), lam_nlo))
with open(os.path.join(HERE, "results", "unitarity_oneloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["channel", "a0", "a1_at_mu2_eq_s", "lam_tree_bound", "lam_ReNLO_bound", "lam_ratio_bound"])
    for (name, (a0, a1)), r in zip(eig.items(), rows):
        w.writerow([name, str(a0), str(sp.simplify(a1)), "%.10g" % r[1], "%.10g" % r[2], "%.10g" % r[3]])
print("written results/unitarity_oneloop.csv")
