# %% [markdown]
# # Step (10): one-loop decay rate around the lambda < 0 bounce, with the fermion determinant (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (10), Eq. (rate), App. prefactor.  Scale-invariant (Fubini) bounce; masses neglected
# (M R, m R << 1); the pseudoscalar coupling is rotated to a scalar one (exact for M = 0).  Following Andreassen, Frost and
# Schwartz (AFS, Phys. Rev. D 97 (2018) 056006), with lambda_A = lambda/6, y_A = sqrt(2) y (their V = lambda_A phi^4/4 and
# Yukawa (y_A/sqrt 2) phi psibar psi), the rate is
#   Gamma/V = int dR/R^5 exp E(R; mu),
#   E = -S + (5/2) ln(S/pi) - 5/4 + 6 zeta'(-1) + 3 ln(R mu/2) + (1/2) S_fin^psi(w) + w (13/18 + 2 gamma_E/3 + (2/3) ln(R mu/2))
#       - w^2 (5/18 + gamma_E/3 + (1/3) ln(R mu/2)),     S = 16 pi^2/|lambda(mu)|,  w = 12 y^2(mu)/lambda(mu)  (= y_A^2/lambda_A),
# i.e. the zero-mode Jacobians (6S/5 pi)^(5/2), the scalar determinant (5/6)^(5/2) exp(...) (AFS (3.31), (5.9)) and the fermion
# determinant (AFS (5.111), with the partial waves (5.98) squared).  The explicit mu-dependence 3 + (2/3) w - (1/3) w^2 equals
# (4 pi)^2 beta_lambda/lambda^2, so E is mu-independent at one loop.
# Checks (independent of AFS):
#   1. scalar partial waves: Gel'fand-Yaglom (radial ODE) against R_l(x) = Gamma(1+l)Gamma(2+l)/(Gamma(3/2+l-k/2)Gamma(3/2+l+k/2)),
#      k = sqrt(1 - 24 x) (AFS (4.27)), for x = -0.9, -0.5, 0.3, 2 and l = 0..6;
#   2. fermion partial waves: Gel'fand-Yaglom for the 2x2 radial system (AFS (5.97)) against [Gamma(a)^2/(Gamma(a+z)Gamma(a-z))]^2,
#      a = j + 1/2, z^2 = w;
#   3. the scalar finite sum (AFS (5.5)) against the direct sum over the exact spectrum lambda_n = (n+1)(n+2)/6 + x;
#   4. the MS-bar loop terms (AFS (4.16), (4.17), (5.110)) by momentum integrals with FT(phi_b^2) ~ K0(qR), FT(phi_b) ~ K1(qR)/q;
#   5. S_fin^psi(w) as the subtracted partial-wave sum (AFS (5.100)-(5.102)), convergence in j_max.
# Results: E(R) at the stationary scale mu* (minimum of E over mu), the band mu*/2 ... 2 mu*, the tree estimate -16 pi^2/|lambda(1/R)|;
# the largest cutoff Lambda_max with Gamma/V < H0^4 for a Higgs-like reading m = m_h (4 ln(m_h/H0) = 404.7, as in the phi^3 + phi^4
# note), Gamma/V = int_{1/Lambda} dR R^-5 e^E.
# Writes results/prefactor.csv and ../figs/prefactor_d4.pdf.  Usage (from Src/): ~/miniforge3/envs/qft/bin/python prefactor_numeric.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import csv
import math
import os
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar
from scipy.special import k0, k1

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
mp.mp.dps = 30
K = (4 * math.pi) ** 2
GE = float(mp.euler)
ZP = float(mp.zeta(-1, derivative=1))
HALF = mp.mpf(1) / 2
COSMO = 404.7              # 4 ln(m_h/H0)

# %% [markdown]
# ## Check 1: scalar partial waves (Gel'fand-Yaglom) against AFS (4.27)

# %%
def tail_fit(sol, rmax, comp):
    """value at r -> infinity from f = A + (c + d ln r)/r^2 at three radii"""
    rs = np.array([rmax / 4, rmax / 2, rmax])
    A = np.array([[1, 1 / r ** 2, math.log(r) / r ** 2] for r in rs])
    return np.linalg.solve(A, np.array([comp(sol.sol(r)) for r in rs]))[0]


def gy_scalar(l, x, rmax=4000.0):
    """psi = r^l f, f'' + (2l+3) f'/r = U f, U = 24 x/(1+r^2)^2 (R = 1): R_l = f(infinity)"""
    a = 24 * x / (4 * (l + 2))
    r0 = 1e-6
    sol = solve_ivp(lambda r, v: [v[1], -(2 * l + 3) / r * v[1] + 24 * x / (1 + r * r) ** 2 * v[0]], [r0, rmax],
                    [1 + a * r0 ** 2, 2 * a * r0], rtol=1e-12, atol=1e-14, method="DOP853", dense_output=True)
    return tail_fit(sol, rmax, lambda v: v[0])


def R_scalar(l, x):
    k = mp.sqrt(1 - 24 * x)
    return mp.re(mp.gamma(1 + l) * mp.gamma(2 + l) / (mp.gamma(3 * HALF + l - k / 2) * mp.gamma(3 * HALF + l + k / 2)))


dev1 = max(abs(gy_scalar(l, x) / float(R_scalar(l, x)) - 1) for x in (-0.9, -0.5, 0.3, 2.0) for l in range(7))
print(f"check 1: scalar partial waves, Gel'fand-Yaglom vs AFS (4.27) (4 x, l = 0..6): max rel. dev. {dev1:.1e}")

# %% [markdown]
# ## Check 2: fermion partial waves (Gel'fand-Yaglom for the 2x2 radial system) against AFS (5.98), squared

# %%
def gy_fermion(j, zabs, rmax=4000.0):
    """u'' = (j(j-1)/r^2 + W^2) u + W' v, v'' = (j(j+1)/r^2 + W^2) v + W' u, W = 2|z|/(1+r^2); u = r^j a, v = r^(j+1) b"""
    W = lambda r: 2 * zabs / (1 + r * r)
    Wp = lambda r: -4 * zabs * r / (1 + r * r) ** 2
    rhs = lambda r, s: [s[1], -2 * j * s[1] / r + W(r) ** 2 * s[0] + Wp(r) * r * s[2],
                        s[3], -2 * (j + 1) * s[3] / r + W(r) ** 2 * s[2] + Wp(r) * s[0] / r]
    sols = [solve_ivp(rhs, [1e-5, rmax], init, rtol=1e-12, atol=1e-14, method="DOP853", dense_output=True)
            for init in ([1.0, 0, 0, 0], [0, 0, 1.0, 0])]
    rs = (rmax / 2, rmax)
    dets = [sols[0].sol(r)[0] * sols[1].sol(r)[2] - sols[1].sol(r)[0] * sols[0].sol(r)[2] for r in rs]
    return (dets[1] * rs[1] ** 2 - dets[0] * rs[0] ** 2) / (rs[1] ** 2 - rs[0] ** 2)


def lnR_j(j, z):
    a = j + HALF
    return 2 * (2 * mp.loggamma(a) - mp.loggamma(a + z) - mp.loggamma(a - z))


dev2 = max(abs(gy_fermion(j, za) / float(mp.re(mp.exp(lnR_j(mp.mpf(j), 1j * za)))) - 1) for za in (0.3, 1.0, 3.0)
           for j in (1.5, 2.5, 3.5, 5.5))
print(f"check 2: fermion partial waves, Gel'fand-Yaglom vs AFS (5.98) squared (|z| = 0.3, 1, 3; j = 3/2..11/2): max rel. dev. {dev2:.1e}")

# %% [markdown]
# ## Check 3: the scalar finite sum (AFS (5.5)); check 4: the MS-bar loop terms (AFS (4.16), (4.17), (5.110))

# %%
def sfin_phi(nmax):
    x, tot = mp.mpf(-1), mp.mpc(0)
    for n in range(nmax):
        d, l0 = mp.mpf((n + 1) * (n + 2) * (2 * n + 3)) / 6, mp.mpf((n + 1) * (n + 2)) / 6
        sub = (2 * n + 3) * x - (6 * n + 9) * x ** 2 / ((n + 1) * (n + 2))
        tot += -sub if n == 1 else d * mp.log((l0 + x) / l0) - sub        # the five zero modes (n = 1) removed
    return tot


cf = mp.mpf(15) / 2 + 6 * mp.euler - 12 * mp.zeta(-1, derivative=1) + mp.log(mp.mpf(7776) / 3125)
s1, s2 = sfin_phi(2000), sfin_phi(20000)
print(f"check 3: Re S_fin^phi: sum to n = 2e3, 2e4: {float(mp.re(s1)):.9f}, {float(mp.re(s2)):.9f} (~1/n); AFS (5.5): {float(cf):.9f};"
      f" Im = {float(mp.im(s2)) / math.pi:+.0f} pi (negative mode)")
F2 = lambda q: 16 * math.pi ** 2 * k0(q)                    # FT(phi_b^2) at lambda_A = -1, R = 1
F1 = lambda q: math.sqrt(8) * 4 * math.pi ** 2 * k1(q) / q  # FT(phi_b)
B0 = lambda q, mu: (2 - math.log(q * q / mu ** 2)) / K      # MS-bar finite part
d4 = lambda f: quad(lambda q: q ** 3 * f(q), 1e-14, 60, limit=500)[0] / (8 * math.pi ** 2)
dev4 = []
dev4.append(abs(d4(lambda q: F2(q) ** 2) / (32 * math.pi ** 2 / 3) - 1))
dev4.append(abs(d4(lambda q: F2(q) ** 2 * math.log(q * q)) / (32 * math.pi ** 2 / 9 * (1 - 6 * GE - 6 * math.log(0.5))) - 1))
for mu in (1.0, 3.0):
    L = math.log(mu / 2)
    dev4.append(abs(-d4(lambda q: F2(q) ** 2 * B0(q, mu)) / 4 / (-(5 / 18 + GE / 3 + L / 3)) - 1))
    dev4.append(abs(-d4(lambda q: q * q * F1(q) ** 2 * B0(q, mu)) / 2 / (-(13 / 18 + 2 * GE / 3 + 2 * L / 3)) - 1))
print(f"check 4: MS-bar loop terms by momentum integrals against AFS (4.16), (4.17), (5.110) (mu R = 1, 3): max rel. dev. {max(dev4):.1e}")

# %% [markdown]
# ## Check 5 and the table of S_fin^psi(w): the subtracted fermion partial-wave sum

# %%
def sub_terms(j):
    c2 = -2 * mp.psi(1, j + HALF)
    lnRs = lambda s, x: mp.loggamma(1 + s) + mp.loggamma(2 + s) - mp.loggamma(3 * HALF + s - mp.sqrt(1 - 24 * x) / 2) \
        - mp.loggamma(3 * HALF + s + mp.sqrt(1 - 24 * x) / 2)
    d4_ = mp.re(mp.diff(lambda w: lnRs(j - 3 * HALF, -w / 6) + lnRs(j - HALF, -w / 6), 0, 2)) / 2
    return c2, d4_


SUB = [sub_terms(3 * HALF + n) for n in range(400)]


def sfin_psi(w, jmax=300):
    z, tot, last = mp.sqrt(w), mp.mpf(0), None
    for n in range(jmax):
        j = 3 * HALF + n
        c2, d4_ = SUB[n]
        last = 2 * (j * j - HALF / 2) * (mp.re(lnR_j(j, z)) - c2 * w - d4_ * w * w)
        tot += last
    jl = 3 * HALF + jmax - 1
    return float(tot + last * jl ** 3 * mp.zeta(3, jl + 1))


conv5 = [abs(sfin_psi(w, 150) - sfin_psi(w, 300)) / abs(sfin_psi(w, 300)) for w in (-1.0, -10.0, -40.0)]
print(f"check 5: S_fin^psi, j_max = 150 vs 300 (w = -1, -10, -40): max rel. dev. {max(conv5):.1e};  S_fin^psi(-1, -10, -40) ="
      f" {sfin_psi(-1.0):.6f}, {sfin_psi(-10.0):.4f}, {sfin_psi(-40.0):.3f}")
U_GRID = np.linspace(math.log(0.05), math.log(2000.0), 141)                 # u = ln(-w)
S_TAB = CubicSpline(U_GRID, [sfin_psi(-math.exp(u)) for u in U_GRID])
spl_dev = max(abs(S_TAB(math.log(-w)) / sfin_psi(w) - 1) for w in (-0.3, -3.3, -33.0, -333.0))
print(f"   spline of S_fin^psi(w) in ln(-w): max rel. dev. at test points {spl_dev:.1e}")

# %% [markdown]
# ## The one-loop exponent with running couplings

# %%
def make_run(y0, lam0):
    rge = lambda t, v: [10 * v[0] ** 2 / K, (3 * v[1] ** 2 + 8 * v[1] * v[0] - 48 * v[0] ** 2) / K]
    t_end = 0.95 * K / (10 * y0 ** 2)
    return solve_ivp(rge, [0, t_end], [y0 ** 2, lam0], rtol=1e-11, atol=1e-13, dense_output=True), t_end


def exponent(run, R, mu):
    """E(R; mu) and its parts; -inf where lambda(mu) >= 0 (no bounce)"""
    y2, lam = run.sol(math.log(mu))
    if lam >= 0:
        return -math.inf, math.inf, 0.0, 0.0, 0.0
    S = 16 * math.pi ** 2 / abs(lam)
    w = 12 * y2 / lam
    L = math.log(R * mu / 2)
    scal = 2.5 * math.log(S / math.pi) - 1.25 + 6 * ZP + 3 * L
    ferm = 0.5 * float(S_TAB(math.log(-w))) + w * (13 / 18 + 2 * GE / 3 + 2 * L / 3) - w * w * (5 / 18 + GE / 3 + L / 3)
    return -S + scal + ferm, S, scal, ferm, w


def mu_zero(run, t_end):
    """the scale where lambda(mu) = 0"""
    return math.exp(brentq(lambda t: run.sol(t)[1], 1e-6, t_end))


def E_star(run, t_end, R, mu0):
    """E at the stationary scale mu* (minimum over mu in [max(0.5/R, mu0), 60/R], lambda(mu) < 0) and mu* R; also E at mu*/2, 2 mu*
    (-inf where mu*/2 < mu0)"""
    lo = max(math.log(0.5), math.log(1.0001 * mu0 * R))
    hi = min(math.log(60), t_end - math.log(1 / R) - 0.01)
    if lo >= hi:
        return -math.inf, math.nan, -math.inf, -math.inf
    f = lambda lk: exponent(run, R, math.exp(lk) / R)[0]
    res = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-7})
    k = math.exp(res.x)
    return res.fun, k, (f(math.log(k / 2)) if math.log(k / 2) > lo else -math.inf), f(min(math.log(2 * k), hi))


RUN, TEND = make_run(1.0, 1.0)
MU0 = mu_zero(RUN, TEND)
# the one-loop RG identity: explicit d E/d ln mu = 3 + (2/3) w - (1/3) w^2 = (4 pi)^2 beta_lambda/lambda^2
idev = 0.0
for t in (3.5, 6.0, 9.0):
    y2, lam = RUN.sol(t)
    w = 12 * y2 / lam
    idev = max(idev, abs((3 + 2 * w / 3 - w * w / 3) / ((3 * lam ** 2 + 8 * lam * y2 - 48 * y2 ** 2) / lam ** 2) - 1))
print(f"explicit mu-dependence of the one-loop terms = (4 pi)^2 beta_lambda/lambda^2: max rel. dev. {idev:.1e}")
rows = []
print("benchmark (y = lambda = 1 at mu = m):")
for inv_R in (40.0, 60.0, 100.0, 300.0, 1e3, 1e4):
    e, k, eh, e2 = E_star(RUN, TEND, 1 / inv_R, MU0)
    _, S, sc, fe, w = exponent(RUN, 1 / inv_R, k * inv_R)
    tree = -16 * math.pi ** 2 / abs(RUN.sol(math.log(inv_R))[1])
    print(f"  1/R = {inv_R:8.0f} m: mu* R = {k:5.3f}, E(mu*) = {e:8.2f} [mu*/2: {eh:8.2f}, 2 mu*: {e2:8.2f}];  S(mu*) = {S:7.2f},"
          f" scalar {sc:6.2f}, fermion {fe:7.2f}, w = {w:7.2f};  tree -S(1/R) = {tree:8.2f}")
    rows.append([inv_R, k, e, eh, e2, S, sc, fe, w, tree])

# %% [markdown]
# ## Where the one-loop exponent is reliable, and the cutoff bound (tree level, with |w| at the bound)

# %%
# the band width relative to |E| along the benchmark: the one-loop exponent is reliable where it is small
for r in rows:
    band = max(r[3], r[4]) - r[2]
    print(f"  1/R = {r[0]:8.0f} m: band/|E(mu*)| = {band / abs(r[2]):.3f};  (E(mu*) - E_tree)/|E_tree| = {(r[2] - r[9]) / abs(r[9]):+.3f}")


def ln_rate_tree(run, mu0, Lam):
    """ln(Gamma/(V m^4)) with the tree estimate E = -16 pi^2/|lambda(1/R)|, Gamma/V = int_{1/Lambda} dR R^-5 e^E"""
    ts = np.linspace(math.log(mu0) + 1e-4, math.log(Lam), 400)
    vals = np.array([4 * t - 16 * math.pi ** 2 / abs(run.sol(t)[1]) for t in ts])
    top = np.max(vals)
    return top + math.log(np.trapezoid(np.exp(vals - top), ts))


def lambda_max_tree(y0, lam0):
    run, t_end = make_run(y0, lam0)
    if run.sol(t_end)[1] > 0:                  # lambda/y^2 > r_+: lambda never turns negative (it diverges first)
        return math.inf, math.inf, math.nan, math.nan
    mu0 = mu_zero(run, t_end)
    g = lambda lnL: ln_rate_tree(run, mu0, math.exp(lnL)) + COSMO
    lnL = brentq(g, math.log(mu0) + 1e-3, min(math.log(mu0) + 8, t_end - 0.5), xtol=1e-8)
    y2, lam = run.sol(lnL)
    return math.exp(lnL), mu0, 12 * y2 / lam, 16 * math.pi ** 2 / abs(lam)


Lb, mu0b, wb, Sb = lambda_max_tree(1.0, 1.0)
print(f"benchmark: lambda(mu) = 0 at mu0 = {mu0b:.2f} m; tree-level Lambda_max (Gamma/V < H0^4, m = m_h) = {Lb:.2f} m = {Lb / mu0b:.3f} mu0;"
      f" there S = {Sb:.1f} and w = 12 y^2/lambda = {wb:.1f}")
scan = []
for lam0 in (0.25, 0.5, 1.0, 2.0, 3.0):
    for y0 in (0.7, 1.0, 1.4):
        Lm, mu0, wL, SL = lambda_max_tree(y0, lam0)
        if not math.isfinite(mu0):
            print(f"  y = {y0:3.1f}, lambda = {lam0:4.2f}: lambda/y^2 = {lam0 / y0 ** 2:.2f} > r_+ = 4.35, lambda stays positive (no instability)")
            continue
        scan.append([y0, lam0, mu0, Lm, wL, SL])
        print(f"  y = {y0:3.1f}, lambda = {lam0:4.2f}: mu0 = {mu0:10.4g} m, Lambda_max = {Lm:10.4g} m = {Lm / mu0:6.3f} mu0;"
              f" w at Lambda_max = {wL:7.2f}")

with open(os.path.join(HERE, "results", "prefactor.csv"), "w", newline="") as fh:
    w_ = csv.writer(fh)
    w_.writerow(["inv_R_over_m", "mustar_R", "E_star", "E_half", "E_two", "S_mustar", "scalar", "fermion", "w", "E_tree"])
    w_.writerows(rows)
    w_.writerow([])
    w_.writerow(["y_m", "lambda_m", "mu0_over_m", "Lmax_tree_over_m", "w_at_Lmax", "S_at_Lmax"])
    w_.writerows(scan)
print("wrote results/prefactor.csv")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))
invs = np.geomspace(60.0, 2e4, 120)
Es = [E_star(RUN, TEND, 1 / x, MU0) for x in invs]
tree = np.array([16 * math.pi ** 2 / abs(RUN.sol(math.log(x))[1]) for x in np.geomspace(MU0 * 1.02, 2e4, 200)])
ax.plot(np.geomspace(MU0 * 1.02, 2e4, 200), tree, color="k", ls="--", lw=1.0, label=r"tree, $16\pi^2/|\lambda(1/R)|$")
ax.plot(invs, [-e[0] for e in Es], color="C1", ls="-", label=r"one loop, $\mu=\mu^*$")
ax.fill_between(invs, [-max(e[2], e[3], e[0]) for e in Es], [-e[0] for e in Es], color="C1", alpha=0.25, lw=0,
                label=r"$\mu=\mu^*/2,\ 2\mu^*$")
xx = np.geomspace(MU0 * 1.02, 2e4, 200)
ax.plot(xx, COSMO + 4 * np.log(xx), color="0.5", ls=":", lw=1.0, label=r"$404.7+4\ln(1/mR)$")
ax.axvline(Lb, color="0.6", lw=0.5, zorder=0)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(10, 3e3)
ax.set_xlabel(r"$1/(mR)$")
ax.set_ylabel(r"$-E(R)$")
ax.legend(fontsize=6.5)
for y0, st in ((0.7, ":"), (1.0, "-"), (1.4, "--")):
    sel = [r for r in scan if r[0] == y0]
    ax2.plot([r[1] for r in sel], [r[3] / r[2] for r in sel], color="C0", ls=st, marker="o", ms=3, label=fr"$y(m)={y0}$")
ax2.set_xlabel(r"$\lambda(m)$")
ax2.set_yscale("log")
ax2.set_ylabel(r"$\Lambda_{\max}/\mu_0$ (tree)")
ax2.legend(fontsize=7)
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "prefactor_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
