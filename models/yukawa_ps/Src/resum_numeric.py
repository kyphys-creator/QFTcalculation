# %% [markdown]
# # Step (11): resummation of the fermion terms y^4/lambda^2 near lambda = 0 (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (11), Eqs. (lo), (nlo), App. resum.  Near lambda(mu) = 0 the one-loop exponent of step (10)
# contains terms ~ w^2 = (12 y^2/lambda)^2 as large as S = 16 pi^2/|lambda|.  Counting lambda ~ y^4/(4 pi)^2, they are leading order.
# 1. Derivative expansion: at large |w| the fermion determinant around the Fubini bounce is the local Coleman-Weinberg potential
#    V_psi = -(y^4 phi^4/(4pi)^2)(ln(y^2 phi^2/mu^2) - 3/2) plus the gradient term Z_psi = -(2 y^2/(4pi)^2)(ln(y^2 phi^2/mu^2) + 2/3),
#    i.e. (1/2) S_fin^psi(w) = (w^2/6) ln|w| + (gamma_E/3 - 1/4) w^2 - (w/3) ln|w| + (5/18 - 2 gamma_E/3) w + O(ln|w|).
# 2. Leading order: the bounce in V_0 = lambda phi^4/4! + V_psi.  On S^4 (phi = Omega chi, Omega = 2R/(r^2+R^2), t = cos theta)
#    S = 2 pi^2 int dt (1-t^2)[(1/2)(1-t^2) chi_t^2 + chi^2 + (chi^4/24) lambda_eff(Omega chi)], with the dilatation (n = 1 Gegenbauer)
#    component of chi removed (the constraint that fixes the size R).  Then S_LO = 16 pi^2 f(eps)/|lambda(mu_R)|,
#    mu_R R = 4 sqrt(3) e^(-19/12) y(mu_R)/sqrt|lambda(mu_R)|, eps = 24 y^4/((4pi)^2 |lambda(mu_R)|), f = 1 + (13/90) eps^2 + O(eps^3).
# 3. Next-to-leading order: E = -S_LO + (5/2) ln(S_LO/pi) - 5/4 + 6 zeta'(-1) + 3 ln(R mu/2) + Delta_psi(w_R, R mu), where Delta_psi is the
#    one-loop fermion part of step (10) minus its local-potential part (O(ln|w|) by item 1).  E is mu-independent at this order.
# Checks: the large-|w| expansion of S_fin^psi against item 1 (|w| up to 1000); the S^4 functional at eps = 0 (Fubini, the spectrum
# n(n+3) - 4); the source integrals I_n = 4(-1)^(n+1)/(n(n+3)); f''(0)/2 = 13/90 against the nonlinear solution; convergence in the basis
# and quadrature; one negative mode along the branch; the leading-log running of y inside the bounce (RG-improved lambda_eff with
# mu = kappa y phi; the kappa-dependence ~ ln kappa (ln kappa + 3/2) is stationary at kappa_c = e^(-3/4); band kappa_c/2 ... 2 kappa_c).  Results: E(R) along the benchmark, Lambda_max (Gamma/V < H0^4, m = m_h, as in step (10)) and the scan.
# Writes results/resum.csv and ../figs/resum_d4.pdf.  Usage (from Src/): ~/miniforge3/envs/qft/bin/python resum_numeric.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import csv
import math
import os
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar
from scipy.special import eval_gegenbauer, roots_jacobi

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
CR = 4 * math.sqrt(3) * math.exp(-19 / 12)      # mu_R R = CR y/sqrt|lambda|
KC = math.exp(-0.75)                             # kappa where the kappa-dependence of the RG-improved lambda_eff is stationary

# %% [markdown]
# ## Check A: the fermion finite sum S_fin^psi(w) at large |w| against the derivative expansion (CW potential + Z term)

# %%
def lnR_j(j, z):
    a = j + HALF
    return 2 * (2 * mp.loggamma(a) - mp.loggamma(a + z) - mp.loggamma(a - z))


def lnR_s(s, x):
    k = mp.sqrt(1 - 24 * x)
    return mp.loggamma(1 + s) + mp.loggamma(2 + s) - mp.loggamma(3 * HALF + s - k / 2) - mp.loggamma(3 * HALF + s + k / 2)


JMAX = 3000
SUB = [(-2 * mp.psi(1, 2 + n), mp.re(mp.diff(lambda w: lnR_s(n, -w / 6) + lnR_s(n + 1, -w / 6), 0, 2)) / 2) for n in range(JMAX)]


def sfin_psi(w, jmax=600):
    """subtracted fermion partial-wave sum (as in step (10)), j = 3/2 + n, tail ~ j^-3"""
    z, tot, last = mp.sqrt(w), mp.mpf(0), None
    for n in range(jmax):
        j = 3 * HALF + n
        c2, d4 = SUB[n]
        last = 2 * (j * j - HALF / 2) * (mp.re(lnR_j(j, z)) - c2 * w - d4 * w * w)
        tot += last
    jl = 3 * HALF + jmax - 1
    return float(tot + last * jl ** 3 * mp.zeta(3, jl + 1))


def half_sfin_asym(w):
    """derivative expansion: -int V_psi - int Z_psi (d phi)^2/2 on the Fubini bounce, minus the MS-bar terms of Eq. (rate)"""
    L = math.log(-w)
    return (w * w / 6) * L + (GE / 3 - 0.25) * w * w - (w / 3) * L + (5 / 18 - 2 * GE / 3) * w


print("check A: (1/2) S_fin^psi(w) against the derivative expansion")
for w in (-10.0, -30.0, -100.0, -300.0, -1000.0):
    s1, s2 = sfin_psi(w, 1500), sfin_psi(w, 3000)
    d = 0.5 * s2 - half_sfin_asym(w)
    print(f"  w = {w:7.0f}: (1/2) S_fin = {0.5 * s2:13.6f} (j_max 1500 vs 3000: {abs(s1 / s2 - 1):.0e}); expansion {half_sfin_asym(w):13.6f};"
          f" remainder {d:7.4f} = {d / math.log(-w):6.4f} ln|w|, w^2-coefficient {w * w:.0e}")
# weighted averages over the Fubini bounce: <ln(1+u)> with phi^4 (u/(1+u)^4) and (d phi)^2 (u^2/(1+u)^4) weights, u = r^2/R^2
av4 = mp.quad(lambda u: u * mp.log(1 + u) / (1 + u) ** 4, [0, mp.inf]) / mp.quad(lambda u: u / (1 + u) ** 4, [0, mp.inf])
avT = mp.quad(lambda u: u ** 2 * mp.log(1 + u) / (1 + u) ** 4, [0, mp.inf]) / mp.quad(lambda u: u ** 2 / (1 + u) ** 4, [0, mp.inf])
print(f"  <ln(1+u)>: phi^4 weight {float(av4):.12f} (5/6), (d phi)^2 weight {float(avT):.12f} (11/6)")
UG = np.linspace(math.log(0.05), math.log(5000.0), 91)                       # u = ln(-w)
S_TAB = CubicSpline(UG, [sfin_psi(-math.exp(u)) for u in UG])
spl = max(abs(S_TAB(math.log(-w)) / sfin_psi(w) - 1) for w in (-0.3, -3.3, -33.0, -333.0, -3333.0))
print(f"  spline of S_fin^psi in ln(-w): max rel. dev. at test points {spl:.1e}")


def delta_psi(w, L):
    """one-loop fermion part of Eq. (rate) minus its local-potential part -int V_psi; L = ln(R mu/2)"""
    return 0.5 * float(S_TAB(math.log(-w))) - (w * w / 6) * math.log(-w) - (GE / 3 - 0.25) * w * w \
        + w * (13 / 18 + 2 * GE / 3 + 2 * L / 3)

# %% [markdown]
# ## Check B: the constrained bounce on S^4 (Gegenbauer basis without n = 1), the Fubini limit, and f''(0)/2 = 13/90

# %%
def basis(N, NQ):
    t, wq = roots_jacobi(NQ, 1, 1)               # weight (1 - t^2) = sin^3(theta) d theta / d t
    C = np.array([eval_gegenbauer(n, 1.5, t) for n in range(N + 1)])
    h = np.array([(n + 1) * (n + 2) / (n + 1.5) for n in range(N + 1)])       # int (1-t^2) C_n^2
    k = np.array([n * (n + 3) + 2 for n in range(N + 1)], float)              # -Laplacian on S^4 + 2 (conformal mass)
    return t, wq, C, h, k


B40 = basis(40, 800)


def solve_s4(ell_fun, a0=None, B=B40):
    """g = chi/sqrt(12/|lam_N|) = sum_{n != 1} a_n C_n(t);  F = int (1-t^2)[(1/2)(1-t^2) g_t^2 + g^2 + (g^4/2) ell],  S = (24 pi^2/|lam_N|) F,
    ell = lambda_eff/|lam_N| as a function of g and t (ell_fun returns ell, d ell/d ln phi, d^2 ell/d ln phi^2).  Damped Newton.
    Returns F, a, the number of negative modes of the constrained Hessian, |grad|."""
    t, wq, C, h, k = B
    N = len(h) - 1
    idx = [n for n in range(N + 1) if n != 1]
    a = np.zeros(N + 1)
    a[0] = 1.0
    if a0 is not None:
        m = min(len(a0), N + 1)
        a[:m] = a0[:m]
        a[1] = 0.0
    for _ in range(80):
        g = a @ C
        l, l1, l2 = ell_fun(g, t)
        Ug = 2 * g ** 3 * l + 0.5 * g ** 3 * l1
        Ugg = 6 * g ** 2 * l + 3.5 * g ** 2 * l1 + 0.5 * g ** 2 * l2
        grad = (a * h * k + C @ (wq * Ug))[idx]
        H = (np.diag(h * k) + (C * (wq * Ugg)) @ C.T)[np.ix_(idx, idx)]
        da = np.linalg.solve(H, -grad)
        s = 1.0
        while not np.all((a + s * np.insert(da, 1, 0.0)) @ C > 0):
            s *= 0.5
        a = a + s * np.insert(da, 1, 0.0)
        if s == 1.0 and np.max(np.abs(da)) < 1e-12:
            break
    g = a @ C
    l, _, _ = ell_fun(g, t)
    F = 0.5 * np.sum(a ** 2 * h * k) + np.sum(wq * g ** 4 / 2 * l)
    return F, a, int(np.sum(np.linalg.eigvalsh(H) < 0)), float(np.linalg.norm(grad))


L0 = lambda t: 2 * np.log1p(t) - 2 * math.log(2) + 5 / 3          # ln(phi_F^2/phi_R^2) on S^4, zero average


def ell_cw(eps):
    """fixed-scale CW potential: lambda_eff/|lambda_R| = -1 - eps ln(phi^2/phi_R^2), phi_R where the first-order term vanishes"""
    return lambda g, t: (-1 - eps * (np.log(g ** 2) + L0(t)), -2 * eps + 0 * t, 0 * t)


t_, wq_, C_, h_, k_ = basis(60, 2000)
F0, a0_, neg0, _ = solve_s4(ell_cw(0.0))
H0 = np.diag(h_ * k_) + (C_ * (wq_ * (-6.0))) @ C_.T                       # Hessian at the Fubini point, eps = 0
spec = np.linalg.eigvalsh(np.diag(1 / np.sqrt(h_)) @ H0 @ np.diag(1 / np.sqrt(h_)))
print(f"check B: eps = 0: F = {F0:.15f} (2/3: S = 16 pi^2/|lambda|); spectrum {np.round(spec[:5], 9)} (n(n+3) - 4 = -4, 0, 6, 14, 24)")
J = C_ @ (wq_ * (-(2 * L0(t_) + 1)))                                       # source d(Delta U)/dg at g = 1, per eps
In = [float(mp.quad(lambda x: (1 - x * x) * mp.log(1 + x) * mp.gegenbauer(n, 1.5, x), [-1, 0, 1])) for n in (1, 2, 3, 6)]
print("  I_n = int (1-t^2) ln(1+t) C_n dt:", [f"{v:.12f}" for v in In], " vs 4(-1)^(n+1)/(n(n+3)):",
      [f"{4 * (-1) ** (n + 1) / (n * (n + 3)):.12f}" for n in (1, 2, 3, 6)])
f2 = -0.5 * sum(J[n] ** 2 / (h_[n] * (n * (n + 3) - 4)) for n in range(61) if n != 1) / (2 / 3)
s19 = mp.nsum(lambda n: 256 * (n + 1.5) / (n ** 2 * (n + 3) ** 2 * (n + 1) * (n + 2) * (n - 1) * (n + 4)), [2, mp.inf])
print(f"  second order: f2 = {f2:.12f}; analytic 1/4 - (3/4) sum_n>=2 = 1/4 - (3/4)({mp.identify(s19)}) = {float(0.25 - 0.75 * s19):.12f}"
      f" = 13/90 = {13 / 90:.12f}")
# the branch: continuation in eps from the Fubini point (a fresh Newton start at eps ~ 1 converges to a saddle with two negative modes)
EPS = np.linspace(0.0, 4.0, 81)
FE, AE, a = [], [], None
for e in EPS:
    F, a, neg, gn = solve_s4(ell_cw(e), a)
    assert neg == 1 and gn < 1e-9, (e, neg, gn)
    FE.append(F / (2 / 3))
    AE.append(a.copy())
F_SPL = CubicSpline(EPS, FE)
for e in (0.05, 0.1, 0.2):
    print(f"  eps = {e}: (f - 1)/eps^2 = {(F_SPL(e) - 1) / e ** 2:.6f}, (f - 1 - 13 eps^2/90)/eps^3 = {(F_SPL(e) - 1 - 13 * e * e / 90) / e ** 3:.4f}")
conv = []
for e in (1.0, 2.0, 3.0, 4.0):
    i = int(round(e / 0.05))
    Fb, _, negb, _ = solve_s4(ell_cw(e), AE[i], basis(60, 2000))
    conv.append(abs(Fb / (2 / 3) / FE[i] - 1))
print(f"  basis/quadrature N = 40, 800 vs 60, 2000 at eps = 1, 2, 3, 4: max rel. dev. {max(conv):.1e}; one negative mode along eps in [0, 4]")
print("  f(eps) at eps = 0.5, 1, 2, 3, 4:", [round(float(F_SPL(e)), 6) for e in (0.5, 1, 2, 3, 4)])

# %% [markdown]
# ## The resummed exponent along the benchmark (y = lambda = 1 at mu = m)

# %%
def make_run(y0, lam0):
    rge = lambda t, v: [10 * v[0] ** 2 / K, (3 * v[1] ** 2 + 8 * v[1] * v[0] - 48 * v[0] ** 2) / K]
    t_end = 0.95 * K / (10 * y0 ** 2)
    return solve_ivp(rge, [0, t_end], [y0 ** 2, lam0], rtol=1e-11, atol=1e-13, dense_output=True), t_end


def lam_R_at(run, R, mu):
    """lambda_eff at the typical field of the bounce for the fixed-scale CW potential at mu (first-order term zero):
    lam_R = lambda(mu) - b [ln(48 y^2/(|lam_R| R^2 mu^2)) - 19/6], b = 24 y^4/(4pi)^2 (monotonic in lam_R, one root)"""
    y2, lam = run.sol(math.log(mu))
    b = 24 * y2 ** 2 / K
    c = lam - b * (math.log(48 * y2 / (R * R * mu * mu)) - 19 / 6)
    return brentq(lambda lr: lr - c - b * math.log(-lr), -100.0, -1e-12, xtol=1e-14), y2, b


def mu_R_of(run, R, t_end):
    """mu_R with mu_R R = CR y(mu_R)/sqrt|lambda(mu_R)| (where lam_R = lambda(mu_R))"""
    f = lambda t: math.exp(t) * R - CR * math.sqrt(run.sol(t)[0] / max(-run.sol(t)[1], 1e-300)) if run.sol(t)[1] < 0 else -1.0
    lo = brentq(lambda t: run.sol(t)[1], 1e-6, t_end) + 1e-9
    return math.exp(brentq(f, lo, t_end - 1e-3, xtol=1e-13))


def E_resum(run, t_end, R, ratio=1.0):
    """E_LO, E_NLO and parts at mu_ref = ratio * mu_R"""
    mu = ratio * mu_R_of(run, R, t_end)
    lamR, y2, b = lam_R_at(run, R, mu)
    eps = b / abs(lamR)
    S = 16 * math.pi ** 2 / abs(lamR) * float(F_SPL(eps))
    w = 12 * y2 / lamR
    L = math.log(R * mu / 2)
    scal = 2.5 * math.log(S / math.pi) - 1.25 + 6 * ZP + 3 * L
    ferm = delta_psi(w, L)
    return -S, -S + scal + ferm, dict(mu=mu, lamR=lamR, eps=eps, S=S, w=w, scal=scal, ferm=ferm)


def E_step10(run, R, mu):
    """the one-loop exponent of step (10), Eq. (rate)"""
    y2, lam = run.sol(math.log(mu))
    if lam >= 0:
        return math.inf
    S, w, L = 16 * math.pi ** 2 / abs(lam), 12 * y2 / lam, math.log(R * mu / 2)
    return -S + 2.5 * math.log(S / math.pi) - 1.25 + 6 * ZP + 3 * L + 0.5 * float(S_TAB(math.log(-w))) \
        + w * (13 / 18 + 2 * GE / 3 + 2 * L / 3) - w * w * (5 / 18 + GE / 3 + L / 3)


def E10_star(run, t_end, R, mu0):
    """step (10): E at the stationary scale mu*, mu* R, and the band mu*/2, 2 mu* (as in Fig. prefactor)"""
    lo, hi = max(math.log(0.5), math.log(1.0001 * mu0 * R)), min(math.log(60), t_end - math.log(1 / R) - 0.01)
    if lo >= hi:
        return math.nan, math.nan, math.nan
    f = lambda lk: E_step10(run, R, math.exp(lk) / R)
    res = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-7})
    band = [f(res.x + s) for s in (-math.log(2), math.log(2)) if lo < res.x + s < hi]
    return res.fun, math.exp(res.x), max(band + [res.fun])


RUN, TEND = make_run(1.0, 1.0)
MU0 = math.exp(brentq(lambda t: RUN.sol(t)[1], 1e-6, TEND))
rows = []
print(f"benchmark: mu0 = {MU0:.3f} m")
for inv_R in (12.0, 15.0, 20.0, 30.0, 40.0, 60.0, 100.0, 300.0, 1e3, 1e4):
    R = 1 / inv_R
    lo, nlo, p = E_resum(RUN, TEND, R)
    band = [E_resum(RUN, TEND, R, r)[1] for r in (0.5, 2.0)]
    e10, k10, _ = E10_star(RUN, TEND, R, MU0)
    tree = -16 * math.pi ** 2 / abs(RUN.sol(math.log(inv_R))[1]) if inv_R > MU0 else math.nan
    print(f"  1/R = {inv_R:7.0f} m: mu_R R = {p['mu'] * R:5.3f}, lam_R = {p['lamR']:7.4f}, eps = {p['eps']:5.3f}, f = {F_SPL(p['eps']):6.4f};"
          f" E_LO = {lo:8.2f}, E_NLO = {nlo:8.2f} [mu_R/2: {band[0]:8.2f}, 2 mu_R: {band[1]:8.2f}] (scalar {p['scal']:5.2f}, Delta_psi"
          f" {p['ferm']:5.2f}, w_R = {p['w']:6.2f});  step (10) E(mu*) = {e10:8.2f};  tree {tree:9.2f}")
    rows.append([inv_R, p["mu"] * R, p["lamR"], p["eps"], float(F_SPL(p["eps"])), lo, nlo, band[0], band[1], p["scal"], p["ferm"], p["w"],
                 e10, tree])
# mu_ref-independence at one loop: d E_NLO/d ln mu_ref at mu_R against the size of its parts (3 + (2/3) w_R per e-fold)
d = (E_resum(RUN, TEND, 1 / 40.0, math.exp(0.01))[1] - E_resum(RUN, TEND, 1 / 40.0, math.exp(-0.01))[1]) / 0.02
lo_d = (E_resum(RUN, TEND, 1 / 40.0, math.exp(0.01))[0] - E_resum(RUN, TEND, 1 / 40.0, math.exp(-0.01))[0]) / 0.02
print(f"  1/R = 40 m: d E_LO/d ln mu_ref = {lo_d:7.3f}, d E_NLO/d ln mu_ref = {d:7.3f} (residual, two-loop order)")

# %% [markdown]
# ## Check C: leading-log running of y inside the bounce (RG-improved lambda_eff) and the scale choice kappa

# %%
def ell_rg(run, R, mu_ref, lamN, kappa):
    """lambda_eff(phi) = lam~(t) + (24 y~^4/(4pi)^2)(3/2 + 2 ln kappa), m e^t = kappa y~(t) phi, field normalized at mu_ref:
    y~ = y^(3/5) y_ref^(2/5), d lam~/dt = -48 y~^4/(4pi)^2  =>  lam~ = lambda(mu_ref) - 24 y_ref^(8/5)(y(t)^(2/5) - y_ref^(2/5))"""
    tr = math.log(mu_ref)
    y2r, lamr = run.sol(tr)
    yr = math.sqrt(y2r)

    def lam_eff(lnphi):
        t = lnphi + math.log(kappa) + math.log(yr)
        for _ in range(30):
            y = 1 / np.sqrt(1 / y2r - 10 * (t - tr) / K)
            t = lnphi + math.log(kappa) + np.log(y ** 0.6 * yr ** 0.4)
        y = 1 / np.sqrt(1 / y2r - 10 * (t - tr) / K)
        yt = y ** 0.6 * yr ** 0.4
        return lamr - 24 * yr ** 1.6 * (y ** 0.4 - yr ** 0.4) + 24 * yt ** 4 / K * (1.5 + 2 * math.log(kappa))

    def ell(g, t):
        lnphi = np.log((1 + t) * math.sqrt(12 / abs(lamN)) * g / R)
        hh = 1e-3
        f0, fp, fm = lam_eff(lnphi), lam_eff(lnphi + hh), lam_eff(lnphi - hh)
        return f0 / abs(lamN), (fp - fm) / (2 * hh) / abs(lamN), (fp - 2 * f0 + fm) / hh ** 2 / abs(lamN)
    return ell


def S_rg(run, t_end, R, kappa=1.0):
    mu = mu_R_of(run, R, t_end)
    lamR, y2, b = lam_R_at(run, R, mu)
    eps = b / abs(lamR)
    F, _, neg, gn = solve_s4(ell_rg(run, R, mu, lamR, kappa), AE[min(int(round(eps / 0.05)), len(AE) - 1)])
    assert neg == 1 and gn < 1e-8
    return 24 * math.pi ** 2 / abs(lamR) * F, 16 * math.pi ** 2 / abs(lamR) * float(F_SPL(eps))


for inv_R in (15.0, 40.0, 300.0):
    vals = [S_rg(RUN, TEND, 1 / inv_R, kp) for kp in (KC / 2, KC, 2 * KC, 1.0, 2.0)]
    print(f"check C: 1/R = {inv_R:5.0f} m: S_LO fixed-scale CW = {vals[1][1]:8.3f}; RG-improved kappa = kappa_c/2, kappa_c, 2 kappa_c:"
          f" {vals[0][0]:8.3f}, {vals[1][0]:8.3f}, {vals[2][0]:8.3f} (kappa = 1: {vals[3][0]:8.3f}, kappa = 2: {vals[4][0]:8.3f})")

# %% [markdown]
# ## The cutoff bound: Gamma/V = int_{1/Lambda} dR R^-5 e^E < H0^4 (m = m_h), resummed, against the tree estimate of step (10)

# %%
def ln_rate(run, t_end, Lam, ratio=1.0, order=1):
    """ln(Gamma/(V m^4)) = ln int_{t <= ln Lambda} dt e^(4t + E), t = ln(1/mR); the integrand falls by e^O(100) per e-fold"""
    ts = np.linspace(math.log(Lam) - 0.6, math.log(Lam), 61)
    vals = np.array([4 * t + E_resum(run, t_end, math.exp(-t), ratio)[order] for t in ts])
    top = np.max(vals)
    return top + math.log(np.trapezoid(np.exp(vals - top), ts))


def ln_rate_tree(run, mu0, Lam):
    ts = np.linspace(math.log(mu0) + 1e-4, math.log(Lam), 400)
    vals = np.array([4 * t - 16 * math.pi ** 2 / abs(run.sol(t)[1]) for t in ts])
    top = np.max(vals)
    return top + math.log(np.trapezoid(np.exp(vals - top), ts))


def bounds(y0, lam0):
    """Lambda_max: tree (step (10)), resummed LO, NLO and its band (mu_ref = mu_R/2, 2 mu_R); mu_R and eps at the NLO bound"""
    run, t_end = make_run(y0, lam0)
    if run.sol(t_end)[1] > 0:
        return None
    mu0 = math.exp(brentq(lambda t: run.sol(t)[1], 1e-6, t_end))
    tree = math.exp(brentq(lambda x: ln_rate_tree(run, mu0, math.exp(x)) + COSMO, math.log(mu0) + 1e-3,
                           min(math.log(mu0) + 8, t_end - 0.5), xtol=1e-9))
    out = {"mu0": mu0, "tree": tree}
    lo_x, hi_x = math.log(mu0) - 1.5, math.log(tree) + 0.5
    for key, ratio, order in (("lo", 1.0, 0), ("nlo", 1.0, 1), ("nlo_half", 0.5, 1), ("nlo_two", 2.0, 1)):
        out[key] = math.exp(brentq(lambda x: ln_rate(run, t_end, math.exp(x), ratio, order) + COSMO, lo_x, hi_x, xtol=1e-9))
    _, _, p = E_resum(run, t_end, 1 / out["nlo"])
    out.update(muR=p["mu"], eps=p["eps"], lamR=p["lamR"], w=p["w"], S=p["S"])
    Srg = [S_rg(run, t_end, 1 / out["nlo"], kp)[0] for kp in (KC / 2, KC, 2 * KC)]
    dEdt = (E_resum(run, t_end, 1 / (out["nlo"] * 1.001))[1] - E_resum(run, t_end, 1 / (out["nlo"] / 1.001))[1]) / (2 * math.log(1.001))
    # Delta S at fixed R moves ln Lambda_max by Delta S/(dE/d ln(1/R) + 4); kappa = kappa_c/2, kappa_c, 2 kappa_c
    out["rg"] = [(s - p["S"]) / (dEdt + 4) for s in Srg]
    out["dEdt"] = dEdt
    return out


bm = bounds(1.0, 1.0)
print(f"benchmark: tree Lambda_max = {bm['tree']:.2f} m = {bm['tree'] / bm['mu0']:.3f} mu0 (step (10));"
      f" resummed LO {bm['lo']:.2f} m, NLO {bm['nlo']:.3f} m = {bm['nlo'] / bm['mu0']:.4f} mu0 [mu_ref = mu_R/2: {bm['nlo_half']:.3f},"
      f" 2 mu_R: {bm['nlo_two']:.3f}]; there mu_R = {bm['muR']:.2f} m = {bm['muR'] / bm['mu0']:.3f} mu0, lambda(mu_R) = {bm['lamR']:.4f},"
      f" S_LO = {bm['S']:.1f}, eps = {bm['eps']:.3f}, w_R = {bm['w']:.1f}; d E/d ln(1/R) = {bm['dEdt']:.0f};"
      f" RG-improved LO with kappa = kappa_c/2, kappa_c, 2 kappa_c shifts ln Lambda_max by {bm['rg'][0]:+.3f}, {bm['rg'][1]:+.3f}, {bm['rg'][2]:+.3f}")
scan = []
for lam0 in (0.25, 0.5, 1.0, 2.0, 3.0):
    for y0 in (0.7, 1.0, 1.4):
        o = bm if (y0, lam0) == (1.0, 1.0) else bounds(y0, lam0)
        if o is None:
            print(f"  y = {y0:3.1f}, lambda = {lam0:4.2f}: lambda/y^2 > r_+, lambda stays positive (no instability)")
            continue
        scan.append([y0, lam0, o["mu0"], o["tree"], o["lo"], o["nlo"], o["nlo_half"], o["nlo_two"], o["muR"], o["eps"], o["lamR"], o["w"],
                     min(o["rg"]), max(o["rg"])])
        print(f"  y = {y0:3.1f}, lambda = {lam0:4.2f}: mu0 = {o['mu0']:10.4g} m; Lambda_max/mu0: tree {o['tree'] / o['mu0']:6.3f},"
              f" LO {o['lo'] / o['mu0']:6.3f}, NLO {o['nlo'] / o['mu0']:6.4f} [{o['nlo_half'] / o['mu0']:6.4f}, {o['nlo_two'] / o['mu0']:6.4f}];"
              f" mu_R/mu0 = {o['muR'] / o['mu0']:6.3f}, lambda(mu_R) = {o['lamR']:6.3f}, eps = {o['eps']:5.3f}, w_R = {o['w']:6.1f},"
              f" kappa band: d ln Lambda_max = {min(o['rg']):+.3f} ... {max(o['rg']):+.3f}")

with open(os.path.join(HERE, "results", "resum.csv"), "w", newline="") as fh:
    w_ = csv.writer(fh)
    w_.writerow(["inv_R_over_m", "muR_R", "lam_R", "eps", "f", "E_LO", "E_NLO", "E_NLO_half", "E_NLO_two", "scalar", "Delta_psi", "w_R",
                 "E_step10_mustar", "E_tree"])
    w_.writerows(rows)
    w_.writerow([])
    w_.writerow(["y_m", "lambda_m", "mu0_over_m", "Lmax_tree", "Lmax_LO", "Lmax_NLO", "Lmax_NLO_half", "Lmax_NLO_two", "muR_at_Lmax",
                 "eps_at_Lmax", "lam_muR", "w_R", "dlnL_kappa_min", "dlnL_kappa_max"])
    w_.writerows(scan)
print("wrote results/resum.csv")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))
xs = np.geomspace(11.0, 2e4, 90)
res = [[E_resum(RUN, TEND, 1 / x, r)[1] for r in (1.0, 0.5, 2.0)] for x in xs]
xt = np.geomspace(MU0 * 1.02, 2e4, 200)
ax.plot(xt, [16 * math.pi ** 2 / abs(RUN.sol(math.log(x))[1]) for x in xt], color="k", ls="--", lw=1.0, label=r"tree, $16\pi^2/|\lambda(1/R)|$")
x10 = np.geomspace(25.0, 2e4, 70)
e10 = [E10_star(RUN, TEND, 1 / x, MU0) for x in x10]
ax.fill_between(x10, [-e[2] for e in e10], [-e[0] for e in e10], color="C1", alpha=0.25, lw=0, label=r"one loop (step 10), $\mu^*\ldots\mu^*/2,\,2\mu^*$")
ax.plot(xs, [-r[0] for r in res], color="C0", label=r"resummed, NLO")
ax.fill_between(xs, [-max(r) for r in res], [-min(r) for r in res], color="C0", alpha=0.3, lw=0, label=r"$\mu_R/2,\ 2\mu_R$")
ax.plot(xs, [-E_resum(RUN, TEND, 1 / x)[0] for x in xs], color="C0", ls="--", lw=0.8, label="resummed, LO")
ax.plot(xs, COSMO + 4 * np.log(xs), color="0.5", ls="-.", lw=0.8, label=r"$404.7+4\ln(1/mR)$")
ax.axvline(MU0, color="0.6", lw=0.5, zorder=0)
ax.axvline(bm["nlo"], color="C0", lw=0.5, ls=":", zorder=0)
ax.text(MU0 * 1.08, 1.3e3, r"$\mu_0$", fontsize=7, color="0.4")
ax.text(bm["nlo"] * 0.93, 1.3e3, r"$\Lambda_{\max}$", fontsize=7, color="C0", ha="right")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(10, 2e4)
ax.set_xlabel(r"$1/(mR)$")
ax.set_ylabel(r"$-E(R)$")
ax.legend(fontsize=6, loc="upper right")
for y0, st in ((0.7, ":"), (1.0, "-"), (1.4, "--")):
    sel = [r for r in scan if r[0] == y0]
    lam_ = [r[1] for r in sel]
    ax2.fill_between(lam_, [r[5] * math.exp(min(0, r[12], r[13])) / r[2] for r in sel],
                     [max(r[5] * math.exp(max(r[12], r[13])), r[6], r[7]) / r[2] for r in sel], color="C0", alpha=0.2, lw=0)
    ax2.plot(lam_, [r[5] / r[2] for r in sel], color="C0", ls=st, marker="o", ms=3, label=fr"$y(m)={y0}$")
    ax2.plot(lam_, [r[3] / r[2] for r in sel], color="0.5", ls=st, marker="o", ms=2.5, mfc="none", lw=0.7)
ax2.axhline(1.0, color="0.6", lw=0.5, zorder=0)
ax2.set_xlabel(r"$\lambda(m)$")
ax2.set_yscale("log")
ax2.set_ylim(0.2, 300)
ax2.set_ylabel(r"$\Lambda_{\max}/\mu_0$")
from matplotlib.lines import Line2D
h1 = ax2.legend(fontsize=6, loc="upper right", title=None)
ax2.add_artist(h1)
ax2.legend(handles=[Line2D([], [], color="C0", marker="o", ms=3, label="resummed (NLO)"),
                    Line2D([], [], color="0.5", marker="o", ms=2.5, mfc="none", lw=0.7, label="tree (step 10)")],
           fontsize=6, loc="upper center")
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "resum_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
