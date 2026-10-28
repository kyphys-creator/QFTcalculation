# %% [markdown]
# # Step (11): the Abrikosov-Nielsen-Olesen vortex of the abelian Higgs model
#
# Research note models/abelian_higgs, step (11).  Static string along z with winding n,
#     Phi = (v/sqrt 2) f(rho) e^{i n theta},   A_theta = (n/(e r)) a(rho),   rho = MA r = e v r,
# V = lam (|Phi|^2 - v^2/2)^2 and beta = MH^2/MA^2 = 2 lam/e^2.  The tension (energy per unit length) is
#     T = 2 pi v^2 I,  I = Integral rho drho [ n^2 a'^2/(2 rho^2) + f'^2/2 + n^2 f^2 (1 - a)^2/(2 rho^2) + (beta/8)(1 - f^2)^2 ],
# with the Euler-Lagrange equations
#     f'' + f'/rho - n^2 f (1 - a)^2/rho^2 + (beta/2) f (1 - f^2) = 0,   a'' - a'/rho + f^2 (1 - a) = 0,
# f(0) = a(0) = 0, f(inf) = a(inf) = 1.  Bogomolny: I = n/2 + (1/2) Integral rho [(n a'/rho - (1 - f^2)/2)^2 + (f' - n f (1 - a)/rho)^2]
# at beta = 1, so T >= pi v^2 |n| with equality on the first-order equations.
#   (a) solve_bvp (collocation) for n = 1, 2, 3 and beta = 0.05 ... 50: T/(pi v^2);
#   (b) checks: the BPS value T = pi v^2 n at beta = 1 and the residual of the first-order equations; the virial identity
#       (Derrick scaling in two dimensions) Integral B^2/2 = Integral V; the flux 2 pi n/e; the asymptotic decay 1 - a ~ rho K1(rho),
#       1 - f ~ K0(sqrt(beta) rho) (beta < 4); the large-beta slope dT/d ln beta -> n^2/2 (pi v^2);
#   (c) type I / II: T(n)/n against T(1): attraction (T(2) < 2 T(1)) for beta < 1, repulsion for beta > 1;
#   writes results/vortex.csv, results/vortex_profiles.csv.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python vortex.py

# %%
import csv
import math
import os

import numpy as np
from scipy.integrate import solve_bvp, quad
from scipy.special import k0, k1

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
RHO0 = 1e-3


def rhs(n, beta):
    def f(rho, y):
        F, dF, A, dA = y
        return np.vstack([dF, -dF / rho + n * n * F * (1 - A) ** 2 / rho ** 2 - beta / 2 * F * (1 - F * F),
                          dA, dA / rho - F * F * (1 - A)])
    return f


def bc(n):
    # regular at the origin: f ~ rho^n, a ~ rho^2;  f = a = 1 at the outer boundary
    def g(ya, yb):
        return np.array([ya[0] - RHO0 * ya[1] / n, ya[2] - RHO0 * ya[3] / 2, yb[0] - 1, yb[2] - 1])
    return g


def solve(n, beta, guess=None):
    R = max(30.0, 30.0 / math.sqrt(min(beta, 1.0)))
    x = np.concatenate([np.geomspace(RHO0, 0.1, 150), np.linspace(0.1, 2, 200)[1:], np.linspace(2, R, 1200)[1:]])
    if guess is None:
        y = np.vstack([np.tanh(x / 1.5) ** n, n * (1 - np.tanh(x / 1.5) ** 2) * np.tanh(x / 1.5) ** (n - 1) / 1.5,
                       np.tanh(x / 2.0) ** 2, (1 - np.tanh(x / 2.0) ** 2) * np.tanh(x / 2.0)])
    else:
        y = guess.sol(x)
    s = solve_bvp(rhs(n, beta), bc(n), x, y, tol=1e-8, max_nodes=400000)
    if not s.success:
        raise RuntimeError("solve_bvp: n = %d, beta = %g: %s" % (n, beta, s.message))
    return s, R


def parts(s, R, n, beta):
    """(magnetic, gradient, potential) parts of I, by quadrature of the collocation solution"""
    def dens(rho):
        F, dF, A, dA = s.sol(rho)
        return np.array([n * n * dA ** 2 / (2 * rho), rho * dF ** 2 / 2 + n * n * F ** 2 * (1 - A) ** 2 / (2 * rho),
                         rho * beta / 8 * (1 - F * F) ** 2])
    # [0, RHO0] with f = F0 (rho/RHO0)^n, a = A0 (rho/RHO0)^2: n^2 A0^2/RHO0^2, n F0^2/4 + n F0^2/4, beta RHO0^2/16
    F0, dF0, A0, dA0 = s.sol(RHO0)
    out = np.array([n * n * A0 ** 2 / RHO0 ** 2, n * F0 ** 2 / 2, beta * RHO0 ** 2 / 16])
    edges = [RHO0, 0.05, 0.5, 2, 5, 10, 20] + [r for r in (40, 80, 160, 320) if r < R] + [R]
    for a_, b_ in zip(edges[:-1], edges[1:]):
        for k in range(3):
            out[k] += quad(lambda r: dens(r)[k], a_, b_, epsabs=1e-14, epsrel=1e-12, limit=400)[0]
    return out


# %% [markdown]
# ## (a) the tension

# %%
betas = sorted(set([0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 200.0, 1000.0, 3000.0, 10000.0]))
rows, sols = [], {}
for n in (1, 2, 3):
    prev = None
    for beta in [1.0] + [b for b in betas if b > 1] :
        s, R = solve(n, beta, prev)
        prev = s
        sols[(n, beta)] = (s, R)
    prev = sols[(n, 1.0)][0]
    for beta in sorted([b for b in betas if b < 1], reverse=True):
        s, R = solve(n, beta, prev)
        prev = s
        sols[(n, beta)] = (s, R)
for n in (1, 2, 3):
    for beta in betas:
        s, R = sols[(n, beta)]
        p = parts(s, R, n, beta)
        rows.append([n, beta, 2 * p.sum(), p[0], p[1], p[2], p[0] / p[2] - 1, len(s.x), R])
for r in rows:
    if r[1] in (0.1, 0.5, 1.0, 2.0, 10.0, 50.0):
        print("(a) n = %d, beta = %5.2f: T/(pi v^2) = %.10f;  virial Integral B^2/2 / Integral V - 1 = %.1e  (%d nodes, R = %g)"
              % (r[0], r[1], r[2], r[6], r[7], r[8]))

# %% [markdown]
# ## (b) checks

# %%
for n in (1, 2, 3):
    s, R = sols[(n, 1.0)]
    T = [r[2] for r in rows if r[0] == n and r[1] == 1.0][0]
    xs = np.linspace(0.01, 15, 2000)
    F, dF, A, dA = s.sol(xs)
    res1 = np.max(np.abs(n * dA / xs - (1 - F * F) / 2))
    res2 = np.max(np.abs(dF - n * F * (1 - A) / xs))
    print("(b) beta = 1, n = %d: T/(pi v^2) - n = %.1e;  first-order equations max residual %.1e, %.1e" % (n, T - n, res1, res2))
print("(b) virial: max |Integral B^2/2 / Integral V - 1| over n = 1..3 and all beta = %.1e" % max(abs(r[6]) for r in rows))
# asymptotic decay (n = 1): 1 - a against rho K1(rho), 1 - f against K0(sqrt(beta) rho)
for beta in (0.5, 1.0, 2.0):
    s, R = sols[(1, beta)]
    r1, r2 = 8.0, 12.0
    ca = [(1 - s.sol(r)[2]) / (r * k1(r)) for r in (r1, r2)]
    cf = [(1 - s.sol(r)[0]) / k0(math.sqrt(beta) * r) for r in (r1, r2)]
    print("(b) beta = %.1f, n = 1: (1 - a)/(rho K1(rho)) at rho = 8, 12: %.6f, %.6f;  (1 - f)/K0(sqrt(beta) rho): %.6f, %.6f"
          % (beta, ca[0], ca[1], cf[0], cf[1]))
for n in (1, 2, 3):
    sl = []
    for b1, b2 in ((20.0, 50.0), (200.0, 1000.0), (1000.0, 10000.0)):
        t1 = [r[2] for r in rows if r[0] == n and r[1] == b1][0]
        t2 = [r[2] for r in rows if r[0] == n and r[1] == b2][0]
        sl.append((t2 - t1) / math.log(b2 / b1))
    print("(b) n = %d: d(T/pi v^2)/d ln beta for beta = 20-50, 200-1000, 1000-10^4: %.4f, %.4f, %.4f  (-> n^2/2 = %.1f)"
          % (n, sl[0], sl[1], sl[2], n * n / 2))

# %% [markdown]
# ## (c) type I / type II

# %%
for beta in betas:
    t = {n: [r[2] for r in rows if r[0] == n and r[1] == beta][0] for n in (1, 2, 3)}
    print("(c) beta = %5.2f: T(1) = %.8f, T(2)/2 - T(1) = %+.3e, T(3)/3 - T(1) = %+.3e  (%s)" % (
        beta, t[1], t[2] / 2 - t[1], t[3] / 3 - t[1], "attract, type I" if t[2] / 2 < t[1] - 1e-9 else
        ("repel, type II" if t[2] / 2 > t[1] + 1e-9 else "BPS")))
with open(os.path.join(HERE, "results", "vortex.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["n", "beta", "T_over_piv2", "I_magnetic", "I_gradient", "I_potential", "virial_minus_1", "nodes", "R"])
    for r in rows:
        w.writerow([r[0], "%.6g" % r[1]] + ["%.14g" % x for x in r[2:7]] + [r[7], "%.6g" % r[8]])
with open(os.path.join(HERE, "results", "vortex_profiles.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    hdr = ["rho"]
    for beta in (0.2, 1.0, 5.0):
        hdr += ["f_b%g" % beta, "a_b%g" % beta, "B_b%g" % beta]
    w.writerow(hdr)
    for x in np.linspace(0.0, 8.0, 401):
        row = [x]
        for beta in (0.2, 1.0, 5.0):
            s, R = sols[(1, beta)]
            xx = max(x, RHO0)
            F, dF, A, dA = s.sol(xx)
            row += [F, A, dA / xx]              # B / (e v^2) = n a'/rho in units of MA^2/e  (n = 1)
        w.writerow(["%.10g" % v for v in row])
print("written results/vortex.csv, results/vortex_profiles.csv")
