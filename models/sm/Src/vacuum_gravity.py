# %% [markdown]
# # Step (10e): the leading gravitational correction to the Fubini bounce
#
# Research note models/sm, step (10).  Euclidean O(4) metric ds^2 = dxi^2 + rho(xi)^2 dOmega_3^2, action
#   S = int sqrt(g) [-(Mbar^2/2) R + (1/2)(dh)^2 + V(h)],  Mbar = (8 pi G)^(-1/2) the reduced Planck mass,
# false vacuum h = 0 with V = 0 (flat space).  To first order in 1/Mbar^2, rho = xi + u/Mbar^2:
#   - the Hamiltonian constraint rho'^2 = 1 + rho^2 (h'^2/2 - V)/(3 Mbar^2) gives u' = xi^2 (h'^2/2 - V)/6;
#   - the action, expanded to this order around the flat bounce (whose own first-order change does not contribute),
#     is S0 + (6 pi^2/Mbar^2) int [xi^2 u (h'^2/2 + V) - xi u'^2] dxi, and with the u equation (xi u')' = -xi^2 (h'^2/2 + V)/2
#     (consistent with the constraint by the flat bounce equation) dS = (6 pi^2/Mbar^2) int xi u'^2 dxi > 0.
# For the Fubini bounce h = A R/(xi^2 + R^2), A^2 = 8/|lambda|:  dS = 32 pi^2/(45 lambda^2 (R Mbar)^2)  (symbolic, below).
# Independent check: graviton exchange in de Donder gauge, dS = -(1/(2 Mbar^2)) int int [T_mn T_mn - T^2/2] Delta(x - y),
# Delta = 1/(4 pi^2 |x - y|^2), T_mn = d_m h d_n h - delta_mn (dh^2/2 + V), with the S^3 angular averages
# <1/|x-y|^2> = 1/r_>^2 and <(x.y)^2/(r^2 s^2 |x-y|^2)> = (1 + (r_</r_>)^2)/(4 r_>^2) (Chebyshev U_l orthogonality), numerically.
# Then S(R) = 8 pi^2/(3 |lambda(1/R)|) + dS(R) with the note's running MS-bar lambda at mu = 1/R, minimized over R (the R
# integral with the one-loop prefactor is in vacuum_prefactor.py).
# Writes results/vacuum_gravity.csv.  Batch: python3 vacuum_gravity.py

# %%
import csv
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad, dblquad
from scipy.optimize import minimize_scalar

from sm_running import MPL, RES, run, starts

MBAR = MPL / math.sqrt(8 * math.pi)        # reduced Planck mass

# %% [markdown]
# ## The O(4) first-order correction, symbolically

# %%
xi, R, A = sp.symbols("xi R A", positive=True)
h = A * R / (xi ** 2 + R ** 2)
lam = -8 / A ** 2
V = lam * h ** 4 / 4
hp = sp.diff(h, xi)
print("flat bounce equation h'' + 3h'/xi - V'(h):", sp.simplify(sp.diff(h, xi, 2) + 3 * hp / xi - lam * h ** 3))
up = xi ** 2 * (hp ** 2 / 2 - V) / 6
L = hp ** 2 / 2 + V
print("u equation (xi u')' + xi^2 L/2:", sp.simplify(sp.diff(xi * up, xi) + xi ** 2 * L / 2))
dS = sp.simplify(6 * sp.pi ** 2 * sp.integrate(sp.simplify(xi * up ** 2), (xi, 0, sp.oo)))
lam_s, M = sp.symbols("lambda Mbar", positive=True)
dS_formula = sp.simplify(dS.subs(A, sp.sqrt(8 / lam_s)))          # lam_s = |lambda|
print("dS * Mbar^2 =", dS_formula, " (with |lambda| = lambda):  32 pi^2/(45 lambda^2 R^2) ->",
      sp.simplify(dS_formula - 32 * sp.pi ** 2 / (45 * lam_s ** 2 * R ** 2)))
# the same through the matter + gravity form with u itself (u(0) = 0)
u = sp.integrate(up, (xi, 0, xi))
dS2 = 6 * sp.pi ** 2 * (sp.integrate(sp.simplify(xi ** 2 * u * L), (xi, 0, sp.oo)) - sp.integrate(sp.simplify(xi * up ** 2), (xi, 0, sp.oo)))
print("matter + gravity form minus the reduced form:", sp.simplify(dS2 - dS))

# %% [markdown]
# ## Independent check: graviton exchange (numerically, R = 1, A = 1)

# %%
def fub(r):
    return 1 / (1 + r * r)


def dfub(r):
    return -2 * r / (1 + r * r) ** 2


lam1 = -8.0                                   # A = 1, R = 1
Lag = lambda r: 0.5 * dfub(r) ** 2 + lam1 * fub(r) ** 4 / 4
# T_mn T_mn(x, y) - T(x) T(y)/2 with T_mn = h'^2 xhat_m xhat_n - delta_mn L:
#   T.T = h'(r)^2 h'(s)^2 c^2 - h'(r)^2 L(s) - h'(s)^2 L(r) + 4 L(r) L(s),  T = h'^2 - 4 L
def kernel_avg(r, s):
    rg, rl = max(r, s), min(r, s)
    k0 = 1 / rg ** 2                                  # <1/|x-y|^2>
    k2 = (1 + (rl / rg) ** 2) / (4 * rg ** 2)        # <c^2/|x-y|^2>
    a, b = dfub(r) ** 2, dfub(s) ** 2
    Lr, Ls = Lag(r), Lag(s)
    tt = a * b * k2 - (a * Ls + b * Lr - 4 * Lr * Ls) * k0
    tr = (a - 4 * Lr) * (b - 4 * Ls) * k0
    return (tt - tr / 2) / (4 * math.pi ** 2)


inner = lambda s: (quad(lambda r: r ** 3 * s ** 3 * kernel_avg(r, s), 0, s, limit=400, epsabs=1e-14, epsrel=1e-12)[0]
                   + quad(lambda r: r ** 3 * s ** 3 * kernel_avg(r, s), s, np.inf, limit=400, epsabs=1e-14, epsrel=1e-12)[0])
total = (2 * math.pi ** 2) ** 2 * quad(inner, 0, np.inf, limit=400, epsabs=1e-14, epsrel=1e-11)[0]
dS_exchange = -total / 2                      # times 1/Mbar^2
dS_o4 = float(dS.subs({A: 1, R: 1}))
print("graviton exchange: dS Mbar^2 = %.12f;  O(4) metric: %.12f  (rel. %.1e)" % (dS_exchange, dS_o4, dS_exchange / dS_o4 - 1))

# %% [markdown]
# ## S(R) with the note's running lambda

# %%
s0, mu0 = starts["B_note_PDG_yt_QCD3"]
sol = run(s0, mu0, 10 * MPL, ("note", 2))
lam_of = lambda mu: sol.sol(math.log(mu))[6]


def S_of(lnmu, grav=True):
    mu = math.exp(lnmu)
    l = lam_of(mu)
    if l >= 0:
        return float("inf")
    s = 8 * math.pi ** 2 / (3 * abs(l))
    if grav:
        s += 32 * math.pi ** 2 / (45 * l ** 2) * (mu / MBAR) ** 2
    return s


rows = []
for grav in (False, True):
    r = minimize_scalar(lambda x: S_of(x, grav), bounds=(math.log(1e12), math.log(MPL)), method="bounded",
                        options={"xatol": 1e-10})
    mu = math.exp(r.x)
    print("%s: min over R of S = %.2f at 1/R = 10^%.3f GeV (lambda(1/R) = %+.6f; gravity part %.2f)"
          % ("with gravity" if grav else "flat", r.fun, math.log10(mu), lam_of(mu),
             r.fun - 8 * math.pi ** 2 / (3 * abs(lam_of(mu)))))
    rows.append(["with_gravity" if grav else "flat", "%.6g" % r.fun, "%.6g" % math.log10(mu), "%.6g" % lam_of(mu)])
with open(RES / "vacuum_gravity.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["case", "S_min", "log10_invR_GeV", "lambda_MSbar_at_invR"])
    w.writerows(rows)
    w.writerow(["dS_Mbar2_R2_lambda2", "%.12g" % (dS_o4 * 64), "", ""])
print("wrote results/vacuum_gravity.csv")
