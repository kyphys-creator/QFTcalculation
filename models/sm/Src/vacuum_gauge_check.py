# %% [markdown]
# # Step (10g): gauge independence of the vacuum-decay prefactor and the counting of the vector modes
#
# Research note models/sm, step (10).  The W/Z sector of the prefactor (vacuum_prefactor.py) is computed in the background
# Feynman gauge.  Here, for one real vector with its Goldstone and ghosts around the Fubini bounce (bounce_det.py):
#   1. the radial operators of the (S, L, G) block in background R_xi (F = d.A - xi e h G), derived symbolically from the
#      4d operator with an explicit harmonic, against the matrices M, C, D, E of bounce_det.ag_blocks_xi;
#   2. the MS-bar bubbles with the R_xi propagator in d dimensions (master integrals G(a, b)), against bounce_det.A2_ag_xi,
#      and the xi-independence of the total pole (= the note's beta_lambda term x^2 + 2x + 1/3 per vector);
#   3. the counting of the transverse modes: the 1/l coefficient of the weighted Born terms (the log divergence of the
#      mode sum) equals x^2 + 2x + 1/3 only with 2 l (l+2) transverse modes; with 2 (l+1)^2 it is x^2 + 1/3, the value in
#      the angular-momentum regularization of Chigusa-Moroi-Shoji (reference);
#   4. per level, -1/2 ln det(S, L, G) + ln det(ghost) does not depend on xi (and the general solver at xi = 1 equals the
#      Cartesian blocks of the Feynman gauge);
#   5. the Faddeev-Popov factor of the l = 0 threshold mode is sqrt(2 pi)/theta_inf(xi) for every xi (regulator eps M);
#   6. the renormalized sector (Born terms subtracted per level, the MS-bar second-order term restored) at several xi.
# Writes results/vacuum_gauge_check.csv.  Batch: python3 vacuum_gauge_check.py  (about 20 minutes)

# %%
import csv
import math
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import sympy as sp

from bounce_det import (A2_ag_xi, ag_blocks, ag_blocks_xi, ag_sector, ag_sector_xi, ghost_R0, green_inner_matrix,
                        gy_block, gy_block_general, gy_block_massive)
from sm_running import RES

XS = (2.0, 8.0)
XIS = (0.5, 1.0, 2.0, 3.0)


# ---- 1. radial operators ----
def derive_rows(l):
    """the S, L, G rows of the background R_xi operator acting on (a, b, g), on the ray x = r (1, 1, 1, 1)/2"""
    X = sp.symbols("x1:5", real=True)
    xi, e, lam = sp.symbols("xi e lambda", positive=True)
    rr = sp.Symbol("r", positive=True)
    a, b, g, hf = (sp.Function(n) for n in ("a", "b", "g", "h"))
    r = sp.sqrt(sum(v ** 2 for v in X))
    lap = lambda f: sum(sp.diff(f, v, 2) for v in X)
    Y = (X[0] + sp.I * X[1]) ** l / r ** l
    dY = [sp.diff(Y, v) for v in X]
    Lt = sp.sqrt(l * (l + 2))
    A = [a(r) * X[m] / r * Y + (b(r) * r * dY[m] / Lt if l > 0 else 0) for m in range(4)]
    G = g(r) * Y
    h = hf(r)
    dh = [sp.diff(h, v) for v in X]
    divA = sum(sp.diff(A[m], X[m]) for m in range(4))
    KA = [-lap(A[n]) + (1 - 1 / xi) * sp.diff(divA, X[n]) + e ** 2 * h ** 2 * A[n] + 2 * e * dh[n] * G for n in range(4)]
    KG = -lap(G) + (lam * h ** 2 + xi * e ** 2 * h ** 2) * G + 2 * e * sum(dh[m] * A[m] for m in range(4))
    sub = {X[m]: rr / 2 for m in range(4)}
    Yv = sp.simplify(Y.subs(sub))
    rows = [sp.simplify(sum(X[m] / r * KA[m] for m in range(4)).subs(sub) / Yv)]
    if l > 0:
        dYb = [sp.conjugate(v) for v in dY]
        num = sum(r * dYb[m] * KA[m] for m in range(4)).subs(sub)
        den = sum(r ** 2 * dYb[m] * dY[m] for m in range(4)).subs(sub)
        rows.append(sp.simplify(Lt * num / den))
    rows.append(sp.simplify(KG.subs(sub) / Yv))
    fields = [a(rr), b(rr), g(rr)] if l > 0 else [a(rr), g(rr)]
    return [sp.expand(v.doit()) for v in rows], fields, (xi, e, lam, rr, hf(rr))


def operator_check(l, xi_v=2.0, e_v=0.7, lam_v=-0.3):
    rows, fields, (xi, e, lam, rr, h) = derive_rows(l)
    n = len(fields)
    M, C, D = np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n))
    sval = {xi: xi_v, e: e_v, lam: lam_v}
    rv = sp.Rational(7, 5)
    for i, row in enumerate(rows):
        free = row.subs(h, 0).doit()
        for j, f in enumerate(fields):
            M[i, j] = -float(free.coeff(sp.Derivative(f, (rr, 2))).subs(sval))
            C[i, j] = -float((free.coeff(sp.Derivative(f, rr)) * rr).subs(sval).subs(rr, rv))
            rest = free.subs({sp.Derivative(f2, (rr, 2)): 0 for f2 in fields}).subs({sp.Derivative(f2, rr): 0 for f2 in fields})
            D[i, j] = float((rest.coeff(f) * rr ** 2).subs(sval).subs(rr, rv))
    Mb, Cb, Db, _, _ = ag_blocks_xi(1.0, l, xi_v)
    return max(np.max(np.abs(M - Mb)), np.max(np.abs(C - Cb)), np.max(np.abs(D - Db)))


# ---- 2. bubbles ----
def bubble_check():
    eps, P, a = sp.symbols("epsilon P a", positive=True)
    d = 4 - 2 * eps

    def G(al, be):
        return (sp.exp(sp.EulerGamma * eps) * P ** (d / 2 - al - be) * sp.gamma(al + be - d / 2) * sp.gamma(d / 2 - al)
                * sp.gamma(d / 2 - be) / (sp.gamma(al) * sp.gamma(be) * sp.gamma(d - al - be)))
    B, F, G22 = G(1, 1), G(2, 1), G(2, 2)
    IVV = (d - 2 * a) * B + a ** 2 * (P ** 2 * G22 + 2 * B - 4 * P * F) / 4
    Imix = P * B - a * (P ** 2 * F + 2 * P * B) / 4
    out = {}
    for name, expr, ref in (("vector-vector", IVV, 6 - 4 * a + a ** 2 / 2 - (4 - 2 * a + a ** 2) * sp.log(P)),
                            ("mixing", Imix, P * ((2 - a) - (1 - a / 4) * sp.log(P))),
                            ("scalar", B, 2 - sp.log(P))):
        ser = sp.series(expr, eps, 0, 1).removeO()
        out[name] = (sp.simplify(ser.coeff(eps, -1)), sp.simplify(sp.expand(ser.coeff(eps, 0) - ref)))
    # total pole of -1/2 ln det_AG + ln det_ghost per vector, in units of the Fubini integrals (x = e^2/|lambda|)
    x, xi = sp.symbols("x xi", positive=True)
    aa = 1 - xi
    pole_ag = 64 * x ** 2 * out["vector-vector"][0].subs(a, aa) + 64 * (xi * x - 1) ** 2 \
        + 512 * x * sp.simplify(out["mixing"][0] / P).subs(a, aa)
    total = sp.expand(sp.Rational(1, 4) * pole_ag - sp.Rational(1, 2) * 64 * xi ** 2 * x ** 2)
    return out, sp.factor(total)


# ---- 3. counting of the transverse modes ----
def log_coefficients(xV, ls=range(30, 161, 5)):
    rows = []
    UVm = lambda r: np.array([[8 * xV / (1 + r * r) ** 2]])
    for l in ls:
        blk = ag_blocks(xV, l)
        _, b1, b2 = gy_block(blk[0][1], blk[0][2])
        _, t1, t2 = gy_block(blk[1][1], blk[1][2])
        _, g1, g2 = gy_block([l], UVm)
        rows.append((l, b1 + b2, t1 + t2, g1 + g2))
    rows = np.array(rows)
    l, n = rows[:, 0], rows[:, 0] + 1
    out = []
    for nT in (2 * l * (l + 2), 2 * n ** 2):
        w = -0.5 * (n ** 2 * rows[:, 1] + nT * rows[:, 2]) + n ** 2 * rows[:, 3]
        Mfit = np.vstack([n, np.ones_like(n), 1 / n, 1 / n ** 2, 1 / n ** 3, 1 / n ** 4]).T
        out.append(np.linalg.lstsq(Mfit, w, rcond=None)[0][2])
    return out


# ---- 4. per level ----
def per_level(xV, l, xis=(1.0, 0.5, 2.0, 5.0)):
    out = []
    for xi in xis:
        ld, b1, b2, _ = gy_block_general(*ag_blocks_xi(xV, l, xi), rmax=4000.0 * (l + 3))
        lg = gy_block([l], lambda r: np.array([[8 * xi * xV / (1 + r * r) ** 2]]))[0]
        out.append(-0.5 * ld + lg)
    return out


# ---- 5. threshold mode ----
def threshold_xi(xV, xi, eps=1e-8):
    from scipy.integrate import solve_ivp, quad
    M, C, D, E, cols = ag_blocks_xi(xV, 0, xi)
    Minv = np.linalg.inv(M)
    e = math.sqrt(8 * xV)
    th = solve_ivp(lambda r, y: [y[1], -3 * y[1] / r + 8 * xi * xV / (1 + r * r) ** 2 * y[0]], (1e-6, 1e6), [1.0, 0.0],
                   method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)
    z = lambda r: (th.sol(r)[1] / e, th.sol(r)[0] / (1 + r * r))
    ld, sg = gy_block_massive([1, 0], E, eps, Minv=Minv)
    out = []
    for f in (lambda r: np.array([r * math.exp(-r * r), math.exp(-r * r)]),
              lambda r: np.array([0.3 * r ** 3 * math.exp(-r * r / 2), (1 - r * r) * math.exp(-r * r)])):
        fz = quad(lambda r: r ** 3 * (f(r)[0] * z(r)[0] + f(r)[1] * z(r)[1]), 0, 50, limit=400)[0]
        gi = green_inner_matrix([1, 0], E, f, eps, Minv=Minv)
        out.append(math.sqrt(2 * math.pi ** 2) * abs(fz) / math.sqrt(2 * math.pi) / math.sqrt(abs(sg * math.exp(ld) * gi)))
    return out


def task(t):
    warnings.simplefilter("ignore")
    kind, x, xi = t
    if kind == "xi":
        return t, ag_sector_xi(x, xi)
    if kind == "ref":
        return t, ag_sector(x, lmax=120)[0]
    raise ValueError(kind)


def main():
    warnings.simplefilter("ignore")
    t0 = time.time()
    tasks = [("xi", x, xi) for x in XS for xi in XIS] + [("ref", x, 1.0) for x in XS]
    ex = ProcessPoolExecutor(max_workers=len(tasks))
    fut = ex.map(task, sorted(tasks, key=lambda t: t[2]))

    for l in (0, 1, 2, 3):
        print("1. radial operator at l = %d: derived minus coded (M, C, D) max |diff| = %.1e" % (l, operator_check(l)), flush=True)
    bub, pole = bubble_check()
    for name, (pl, df) in bub.items():
        print("2. %-13s bubble: pole %s, derived finite part minus coded = %s" % (name, pl, df))
    print("   total pole of -1/2 ln det_AG + ln det_gh (per pi^2/6 of Fubini integrals): %s  (48 (x^2 + 2x + 1/3), no xi)"
          % pole)
    for x in (0.5, 2.0):
        c, cw = log_coefficients(x)
        print("3. x_V = %.1f: 1/l coefficient of the weighted Born terms with 2l(l+2) transverse modes %.6f, with 2(l+1)^2 "
              "%.6f; x^2 + 2x + 1/3 = %.6f, x^2 + 1/3 = %.6f" % (x, c, cw, x * x + 2 * x + 1 / 3, x * x + 1 / 3), flush=True)
    for l in (1, 2, 5, 20):
        v = per_level(2.0, l)
        blk = ag_blocks(2.0, l)[0]
        cart = gy_block(blk[1], blk[2])[0]
        gen = gy_block_general(*ag_blocks_xi(2.0, l, 1.0), rmax=4000.0 * (l + 3))[0]
        print("4. l = %2d, x_V = 2: -1/2 ln det(S,L,G) + ln det(gh) at xi = 1, 0.5, 2, 5: %s (spread %.1e); xi = 1 general "
              "solver minus Cartesian ln det %.1e" % (l, " ".join("%.9f" % u for u in v), max(v) - min(v), gen - cart),
              flush=True)
    for xi in (0.5, 1.0, 2.0, 5.0):
        print("5. xi = %.1f: Faddeev-Popov factor of the l = 0 threshold mode (theta(0) = 1) for two f: %s (sqrt(2 pi) = %.8f)"
              % (xi, " ".join("%.8f" % v for v in threshold_xi(2.0, xi)), math.sqrt(2 * math.pi)), flush=True)
    val = dict(fut)
    ex.shutdown()
    rows = []
    for x in XS:
        ref = val[("ref", x, 1.0)]
        print("6. x_V = %.1f: renormalized sector, Feynman gauge (ag_sector) %.8f; background R_xi: %s"
              % (x, ref, "  ".join("xi %.1f %.8f" % (xi, val[("xi", x, xi)]) for xi in XIS)))
        rows += [[x, "feynman_ag_sector", "%.10f" % ref]] + [[x, "%g" % xi, "%.10f" % val[("xi", x, xi)]] for xi in XIS]
    with open(RES / "vacuum_gauge_check.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["x_V", "gauge", "ln_factor_A1"])
        w.writerows(rows)
    print("wrote results/vacuum_gauge_check.csv (%.0f s)" % (time.time() - t0))


if __name__ == "__main__":
    main()
