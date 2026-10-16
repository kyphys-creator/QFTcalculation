# %% [markdown]
# # Appendix check: the [T^a,T^b] part of g g -> Q Qbar vanishes at threshold
#
# Research note models/qcd, derivations of the appendices (sympy, explicit Dirac matrices, exact, g = 1).
#   app:hq 「閾値の Coulomb の項。」 (T4): in Eq. (Mtree) (B) the coefficient of [T^a,T^b],
#     A_- = -g^2 ubar[(1/2)(X_t/(t-m^2) - X_u/(u-m^2)) + X_s/s] v,
#   (i) is antisymmetric under the exchange of the two gluons (the {T^a,T^b} coefficient is symmetric), (ii) at beta = 0 reduces to
#   (g^2 m/s) ubar[e1slash, e2slash] v, which vanishes for spinors at rest (gamma0 u = u, gamma0 v = -v), (iii) is O(beta) near threshold
#   (sum |A_-|^2/beta^2 tends to a constant: a p wave).
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_hq_pwave.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_hq_pwave.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import itertools
import sympy as sp
INTERACTIVE = "ipykernel" in sys.modules

I2 = sp.eye(2); Z2 = sp.zeros(2)
SIG = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
G = [sp.diag(1, 1, -1, -1)] + [sp.Matrix(sp.BlockMatrix([[Z2, s_], [-s_, Z2]])) for s_ in SIG]
gmet = sp.diag(1, -1, -1, -1)
sl = lambda p: sum((gmet[m, m] * p[m] * G[m] for m in range(4)), sp.zeros(4))
dot = lambda a, b: a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
one = sp.eye(4)


# %% [markdown]
# ## Spinors

# %%
def u_sp(p, m):
    E = p[0]; sp_ = sum((SIG[i] * p[i + 1] for i in range(3)), sp.zeros(2))
    return [sp.Matrix.vstack(sp.sqrt(E + m) * chi, sp_ * chi / sp.sqrt(E + m)) for chi in (sp.Matrix([1, 0]), sp.Matrix([0, 1]))]

def v_sp(p, m):
    E = p[0]; sp_ = sum((SIG[i] * p[i + 1] for i in range(3)), sp.zeros(2))
    return [sp.Matrix.vstack(sp_ * eta / sp.sqrt(E + m), sp.sqrt(E + m) * eta) for eta in (sp.Matrix([1, 0]), sp.Matrix([0, 1]))]

bar = lambda w: w.H * G[0]


# %% [markdown]
# ## The coefficients of [T^a,T^b] (A_-) and of {T^a,T^b}

# %%
def structures(p1, p2, k1, k2, e1, e2, m):
    s = dot(p1 + p2, p1 + p2); t = dot(p1 - k1, p1 - k1); u = dot(p1 - k2, p1 - k2)
    Xt = sl(e1) * (sl(k1 - p1) + m * one) * sl(e2)
    Xu = sl(e2) * (sl(k1 - p2) + m * one) * sl(e1)
    Xs = dot(e1, e2) * (sl(p1) - sl(p2)) + 2 * dot(e1, p2) * sl(e2) - 2 * dot(e2, p1) * sl(e1)
    return s, t, u, Xt, Xu, Xs

def coeff_minus(p1, p2, k1, k2, e1, e2, m):
    s, t, u, Xt, Xu, Xs = structures(p1, p2, k1, k2, e1, e2, m)
    return -(sp.Rational(1, 2) * (Xt / (t - m ** 2) - Xu / (u - m ** 2)) + Xs / s)

def coeff_plus(p1, p2, k1, k2, e1, e2, m):
    s, t, u, Xt, Xu, Xs = structures(p1, p2, k1, k2, e1, e2, m)
    return -(sp.Rational(1, 2) * (Xt / (t - m ** 2) + Xu / (u - m ** 2)))


# %% [markdown]
# ## (ii) At threshold

# %%
m = sp.Integer(1)
xh = sp.Matrix([0, 1, 0, 0]); yh = sp.Matrix([0, 0, 1, 0])
ok = True
# (ii) threshold: k1 = k2 = (m, 0), sqrt(s) = 2m
E = m
p1 = sp.Matrix([E, 0, 0, E]); p2 = sp.Matrix([E, 0, 0, -E]); K = sp.Matrix([E, 0, 0, 0])
for e1, e2 in itertools.product((xh, yh), repeat=2):
    s, t, u, Xt, Xu, Xs = structures(p1, p2, K, K, e1, e2, m)
    # matrix identities used in the text
    id1 = sp.simplify(Xt - Xu - (dot(e1, e2) * (sl(p1) - sl(p2)) + m * (sl(e1) * sl(e2) - sl(e2) * sl(e1))))
    id2 = sp.simplify(Xs - dot(e1, e2) * (sl(p1) - sl(p2)))
    Cm = coeff_minus(p1, p2, K, K, e1, e2, m)
    id3 = sp.simplify(Cm - m / s * (sl(e1) * sl(e2) - sl(e2) * sl(e1)))
    ok &= id1 == sp.zeros(4) and id2 == sp.zeros(4) and id3 == sp.zeros(4) and t - m ** 2 == -s / 2 and u - m ** 2 == -s / 2
    for uu, vv in itertools.product(u_sp(K, m), v_sp(K, m)):
        amp = sp.simplify((bar(uu) * Cm * vv)[0])
        comm = sp.simplify((bar(uu) * (sl(e1) * sl(e2) - sl(e2) * sl(e1)) * vv)[0])
        ok &= amp == 0 and comm == 0
    for uu in u_sp(K, m):
        ok &= sp.simplify(G[0] * uu - uu) == sp.zeros(4, 1)
    for vv in v_sp(K, m):
        ok &= sp.simplify(G[0] * vv + vv) == sp.zeros(4, 1)
    comm = sl(e1) * sl(e2) - sl(e2) * sl(e1)
    ok &= sp.simplify(G[0] * comm - comm * G[0]) == sp.zeros(4)
print("threshold: X_t - X_u = (e1.e2)(p1-p2) + m[e1,e2], X_s = (e1.e2)(p1-p2), coefficient = (m/s)[e1,e2],"
      " gamma0 u = u, gamma0 v = -v, [gamma0,[e1,e2]] = 0, ubar[e1,e2]v = 0 for all spins/polarizations:", ok)
# the {T^a,T^b} part does not vanish at threshold
nz = any(sp.simplify((bar(uu) * coeff_plus(p1, p2, K, K, e1, e2, m) * vv)[0]) != 0
         for e1, e2 in itertools.product((xh, yh), repeat=2) for uu, vv in itertools.product(u_sp(K, m), v_sp(K, m)))
print("the {T^a,T^b} coefficient is nonzero at threshold:", nz)

coeff_minus(p1, p2, K, K, xh, yh, m)          # inspect: the [T^a,T^b] coefficient at threshold for e1 = x, e2 = y: (m/s)[e1slash, e2slash]

# %% [markdown]
# ## (i) Exchange of the two gluons

# %%
# (i) antisymmetry under the exchange (p1, e1) <-> (p2, e2) at a generic point (exact numbers)
b, cth, sth = sp.Rational(3, 5), sp.Rational(5, 13), sp.Rational(12, 13)
E = 1 / sp.sqrt(1 - b ** 2) * m          # E = m/sqrt(1-beta^2)
pk = b * E
p1 = sp.Matrix([E, 0, 0, E]); p2 = sp.Matrix([E, 0, 0, -E])
k1 = sp.Matrix([E, pk * sth, 0, pk * cth]); k2 = sp.Matrix([E, -pk * sth, 0, -pk * cth])
anti = all(sp.simplify(coeff_minus(p1, p2, k1, k2, e1, e2, m) + coeff_minus(p2, p1, k1, k2, e2, e1, m)) == sp.zeros(4)
           for e1, e2 in itertools.product((xh, yh), repeat=2))
sym = all(sp.simplify(coeff_plus(p1, p2, k1, k2, e1, e2, m) - coeff_plus(p2, p1, k1, k2, e2, e1, m)) == sp.zeros(4)
          for e1, e2 in itertools.product((xh, yh), repeat=2))
print("[T^a,T^b] coefficient antisymmetric, {T^a,T^b} coefficient symmetric under gluon exchange:", anti, sym)


# %% [markdown]
# ## (iii) Near threshold: a p wave

# %%
# (iii) near threshold: sum over spins and polarizations of |A_-|^2 / beta^2 tends to a constant
import math
for bv in (sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)):
    E = 1 / sp.sqrt(1 - bv ** 2); pk = bv * E
    p1 = sp.Matrix([E, 0, 0, E]); p2 = sp.Matrix([E, 0, 0, -E])
    k1 = sp.Matrix([E, pk * sth, 0, pk * cth]); k2 = sp.Matrix([E, -pk * sth, 0, -pk * cth])
    tot = 0
    for e1, e2 in itertools.product((xh, yh), repeat=2):
        Cm = coeff_minus(p1, p2, k1, k2, e1, e2, m)
        for uu, vv in itertools.product(u_sp(k1, m), v_sp(k2, m)):
            a = (bar(uu) * Cm * vv)[0]
            tot += sp.Abs(a) ** 2
    print(f"beta = {bv}: sum |A_-|^2 / beta^2 = {float(sp.N(tot / bv ** 2, 20)):.10f}")
float(sp.N(tot / bv ** 2, 20))          # inspect: sum |A_-|^2/beta^2 at beta = 1/1000
