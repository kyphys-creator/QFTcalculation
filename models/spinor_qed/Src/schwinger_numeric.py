# %% [markdown]
# # Step (11): Schwinger pair production -- constant field, worldline instantons, Sauter potential
#
# Research note models/spinor_qed, step (11), Eqs. (eq:schw), (eq:wli), (eq:sauter), App. schw.  Units m = 1, F = eE/m^2.
# - Constant field: the proper-time integral of Eq. (schw) along tau = t e^{i phi} (above the poles; Feynman's m^2 - i0)
#   against Im L = (F^2/8 pi^3) sum n^-2 e^{-n pi/F}, the real part against the twice-subtracted dispersion integral over
#   eps = F^2, the weak-field coefficients against the dispersion (Borel) integrals; physical rates.
# - Sauter potential eA0 = lam tanh(k x3), E = E sech^2(k x3), lam = eE/k, gt = m k/(eE): the transmission of the reduced
#   Dirac equation (u' = i[(w - V)u - mt v], v' = -i[(w - V)v - mt u]) against Nikishov's nbar (Eq. (sauter)), R + T = 1;
#   the WKB exponent W(w, mt) and its derivatives against the closed forms; the worldline instanton (curvature eE(x3)/m)
#   integrated numerically against S0 of Eq. (wli); Im Gamma/(A T) = -int dw d^2p/(2pi)^3 ln(1 - nbar) against the
#   semiclassical prefactor formula and the locally constant field (LCF) value; the mean number against Kim and Page's
#   x, y double integral.
# - Gaussian field E exp(-(k x3)^2) (no closed form): instanton action against the WKB integral, Im Gamma from the Dirac
#   equation mode by mode against the semiclassical formula with numerical derivatives of W.
# Compares with schwinger_exact.wl (Mathematica) through results/schwinger_mathematica.csv; writes results/schwinger.csv
# and ../figs/schwinger.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python schwinger_numeric.py --points` writes work/schw_points.txt (run first), then
# without arguments after schwinger_exact.wl (run_schwinger_check.sh).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import sys
import time

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf

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
F_CONST = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0]                       # eE/m^2, constant field
MODES = [(0.0, 1.0, 2.0, 1.0), (0.3, 1.2, 2.0, 1.0), (-0.5, 1.0, 3.0, 0.7), (0.2, 1.1, 4.0, 0.5),
         (0.0, 1.0, 6.0, 0.4), (1.5, 1.3, 5.0, 2.0)]           # (omega, m_perp, lambda, k), Sauter, m = 1
GT_LOOP = [0.2, 0.5, 0.8, 0.95]                                # gt for the instanton loops (F = 1/2)
GRID = [(inv, gt) for inv in (1, 2, 5, 10, 20) for gt in (0.2, 0.5, 0.8)]   # (m^2/eE, gt), Sauter totals
GAUSS = [(2, 0.3), (4, 0.3), (8, 0.3), (4, 0.6)]               # (m^2/eE, gt), Gaussian field
GT_FIG = np.linspace(0.02, 0.98, 25)
INV_FIG = [2, 5, 10]

if "--points" in sys.argv:
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    with open(os.path.join(HERE, "work", "schw_points.txt"), "w") as fh:
        fh.writelines(f"const {f!r}\n" for f in F_CONST)
        fh.writelines(f"mode {w!r} {mt!r} {lam!r} {k!r}\n" for w, mt, lam, k in MODES)
        fh.writelines(f"loop {gt!r}\n" for gt in GT_LOOP)
        fh.writelines(f"total {inv} {gt!r}\n" for inv, gt in GRID)
        fh.writelines(f"gauss {inv} {gt!r}\n" for inv, gt in GAUSS)
    print("wrote work/schw_points.txt")
    sys.exit(0)

rows = []


def read_mathematica():
    out = {}
    with open(os.path.join(HERE, "results", "schwinger_mathematica.csv")) as fh:
        for r in csv.reader(fh):
            if r and r[0] != "kind":
                out.setdefault(r[0], []).append([float(x) for x in r[1:]])
    return out


MA = read_mathematica()

# %% [markdown]
# ## Constant field

# %%
def bracket(z):
    """z cot z - 1 + z^2/3 (series near 0)"""
    if abs(z) < mp.mpf("1e-3"):
        return -z ** 4 / 45 - 2 * z ** 6 / 945
    return z * mp.cot(z) - 1 + z ** 2 / 3


def L_const(F, phi=mp.mpf("0.4")):
    """L/m^4 along tau = t e^{i phi}: the path passes above the poles tau_n = n pi/F (Feynman's m^2 - i0); 40 digits,
    since Im L is a small fraction of the integral at weak fields"""
    with mp.workdps(40):
        return _L_const(mp.mpf(F), mp.mpf(phi))


def _L_const(F, phi):
    ph = mp.exp(1j * phi)
    # the integrand is below e^(-t cos phi) < e^(-180) beyond t = 200 (and cot of huge complex arguments overflows gmp)
    return -mp.quad(lambda t: ph * mp.exp(-t * ph) * bracket(F * t * ph) / (t * ph) ** 3, [0, 1, 5, 20, 60, 200]) / (8 * mp.pi ** 2)


def im_const(F):
    """(F^2/8 pi^3) sum_n n^-2 exp(-n pi/F)"""
    F = mp.mpf(F)
    return F ** 2 / (8 * mp.pi ** 3) * mp.nsum(lambda n: mp.exp(-n * mp.pi / F) / n ** 2, [1, mp.inf])


def re_disp(F):
    """twice-subtracted dispersion relation in eps = F^2: Re L = (eps^2/pi) PV int de Im L(e)/(e^2 (e - eps))"""
    eps = mp.mpf(F) ** 2
    g = lambda e: im_const(mp.sqrt(e)) / e ** 2
    c = 2 * eps
    pv = mp.quad(lambda e: (g(e) - g(eps)) / (e - eps), [0, eps, c]) + mp.quad(lambda e: g(e) / (e - eps), [c, 10 * c, mp.inf])
    return eps ** 2 / mp.pi * pv


def coef_series(n):
    """weak-field coefficient of eps^n: zeta(2n) Gamma(2n-2)/(4 pi^(2n+2))"""
    return mp.zeta(2 * n) * mp.gamma(2 * n - 2) / (4 * mp.pi ** (2 * n + 2))


def coef_disp(n):
    return mp.quad(lambda e: im_const(mp.sqrt(e)) / e ** (n + 1), [0, mp.mpf("0.05"), mp.mpf("0.5"), 5, mp.inf]) / mp.pi


print(f"{'eE/m^2':>7} {'Re L/m^4 (contour)':>22} {'Im L (contour)':>18} {'Im series dev':>13} {'Re disp dev':>12} {'phi-dev':>8} {'Re/EH':>8}")
CONST = {}
for F in F_CONST:
    v, v2 = L_const(mp.mpf(F)), L_const(mp.mpf(F), mp.mpf("0.9"))
    im_s, re_d = im_const(F), re_disp(F)
    eh = mp.mpf(F) ** 4 / (360 * mp.pi ** 2)
    di, dr = abs(v.imag / im_s - 1), abs(v.real / re_d - 1)
    CONST[F] = (v, im_s, re_d)
    print(f"{F:7.2f} {mp.nstr(v.real, 15):>22} {mp.nstr(v.imag, 12):>18} {float(di):13.1e} {float(dr):12.1e} {float(abs(v - v2)):8.1e} {float(v.real / eh):8.4f}")
    rows.append(["const", F, float(v.real), float(v.imag), float(di), float(dr), float(v.real / eh)])
print(f"{'n':>3} {'zeta Gamma/(4 pi^(2n+2))':>26} {'dispersion integral':>22} {'rel.dev':>8}  (coefficients of eps^n)")
for n in (2, 3, 4, 6, 8):
    a, b = coef_series(n), coef_disp(n)
    print(f"{n:3d} {mp.nstr(a, 16):>26} {mp.nstr(b, 16):>22} {float(abs(b / a - 1)):8.1e}")
    rows.append(["coef", n, float(a), float(b), float(abs(b / a - 1))])
# Mathematica: the contour integrals at the same F
md = max(abs(complex(r[1], r[2]) - complex(CONST[r[0]][0])) / abs(CONST[r[0]][0]) for r in MA["const"])
print(f"Mathematica NIntegrate vs mpmath (constant field): max rel. dev {md:.1e}")
# physical: E_c = m^2 c^3/(e hbar)
EC = 1.32328585e18      # V/m
ME_EV, HBAR_EVS, HBARC_EVM = 0.51099895e6, 6.582119569e-16, 1.973269804e-7
m4_per_m3s = (ME_EV / HBARC_EVM) ** 3 * (ME_EV / HBAR_EVS)          # m^4 in 1/(m^3 s) (natural units)
for x in (0.05, 0.1, 0.2, 1.0):
    rate = 2 * float(im_const(x)) * m4_per_m3s
    pairs = float(mp.mpf(x) ** 2 / (4 * mp.pi ** 3) * mp.exp(-mp.pi / x)) * m4_per_m3s
    print(f"E = {x} E_c = {x * EC:.3e} V/m: vacuum decay 2 Im L = {rate:.3e} /(m^3 s), pairs (n = 1) {pairs:.3e} /(m^3 s)")
    rows.append(["physical", x, x * EC, rate, pairs])

# %% [markdown]
# ## Sauter potential: Dirac equation mode by mode, WKB exponent, worldline instanton

# %%
def profile(name, lam, k):
    if name == "sech":
        return (lambda x: lam * np.tanh(k * x)), lam, 22.0 / k
    return (lambda x: lam * math.sqrt(math.pi) / 2 * erf(k * x)), lam * math.sqrt(math.pi) / 2, 7.0 / k


def transmission(w, mt, lam, k, name="sech"):
    """T and R of the reduced Dirac equation; the transmitted wave (momentum -p2 on the right) integrated to the left"""
    V, vmax, X = profile(name, lam, k)

    def f(x, y):
        u, v = y[0] + 1j * y[1], y[2] + 1j * y[3]
        e = w - V(x)
        du, dv = 1j * (e * u - mt * v), -1j * (e * v - mt * u)
        return [du.real, du.imag, dv.real, dv.imag]
    ER, EL = w - V(X), w - V(-X)
    pR, pL = math.sqrt(ER ** 2 - mt ** 2), math.sqrt(EL ** 2 - mt ** 2)
    u0 = np.exp(-1j * pR * X)
    v0 = (ER + pR) / mt * u0
    sol = solve_ivp(f, [X, -X], [u0.real, u0.imag, v0.real, v0.imag], method="DOP853", rtol=1e-12, atol=1e-30)
    u, v = sol.y[0, -1] + 1j * sol.y[1, -1], sol.y[2, -1] + 1j * sol.y[3, -1]
    ci, cr = (EL - pL) / mt, (EL + pL) / mt
    M = np.array([[np.exp(-1j * pL * X), np.exp(1j * pL * X)], [ci * np.exp(-1j * pL * X), cr * np.exp(1j * pL * X)]])
    A, B = np.linalg.solve(M, [u, v])
    ji = abs(A) ** 2 * (1 - ci ** 2)
    return (1 - ((ER + pR) / mt) ** 2) / ji, abs(B) ** 2 * (cr ** 2 - 1) / ji


def nbar_exact(w, mt2, lam, k):
    """Nikishov, written with exponentials: e^(a+b-c)(1-e^-2a)(1-e^-2b)/(1 + e^-2c - e^(d-c)(1 + e^-2d))"""
    w, mt2, lam, k = (mp.mpf(x) for x in (w, mt2, lam, k))
    p1, p2 = mp.sqrt((lam + w) ** 2 - mt2), mp.sqrt((lam - w) ** 2 - mt2)
    a, b, c, d = mp.pi * p1 / k, mp.pi * p2 / k, 2 * mp.pi * lam / k, abs(mp.pi * (p1 - p2) / k)
    return mp.exp(a + b - c) * (-mp.expm1(-2 * a)) * (-mp.expm1(-2 * b)) / (1 + mp.exp(-2 * c) - mp.exp(d - c) * (1 + mp.exp(-2 * d)))


print(f"{'omega':>6} {'m_perp':>6} {'lambda':>6} {'k':>4} {'T (Dirac eq.)':>22} {'nbar (Nikishov)':>22} {'rel.dev':>8} {'R+T-1':>8} {'Mathematica':>8}")
md = {tuple(r[:4]): r[4] for r in MA["mode"]}
for w, mt, lam, k in MODES:
    T, R = transmission(w, mt, lam, k)
    ne = float(nbar_exact(w, mt * mt, lam, k))
    dm = abs(md[(w, mt, lam, k)] / ne - 1)
    print(f"{w:6.2f} {mt:6.2f} {lam:6.2f} {k:4.1f} {T:22.15e} {ne:22.15e} {abs(T / ne - 1):8.1e} {abs(R + T - 1):8.1e} {dm:8.1e}")
    rows.append(["mode", w, mt, lam, k, T, ne, abs(T / ne - 1), abs(R + T - 1), dm])


def W_quad(w, mt2, F, k, name):
    """WKB exponent 2 int sqrt(mt^2 - (w - V)^2) dx3 between the turning points"""
    lam = mp.mpf(F) / k
    V = (lambda x: lam * mp.tanh(k * x)) if name == "sech" else (lambda x: lam * mp.sqrt(mp.pi) / 2 * mp.erf(k * x))
    mt = mp.sqrt(mt2)
    xa = mp.findroot(lambda x: w - V(x) - mt, 0)
    xb = mp.findroot(lambda x: w - V(x) + mt, 0)
    return 2 * mp.quad(lambda x: mp.sqrt(max(mt2 - (w - V(x)) ** 2, 0)), [xa, xb])


def W_derivs(F, k, name, h=mp.mpf("1e-5")):
    W0 = W_quad(0, 1, F, k, name)
    Wm = (W_quad(0, 1 + h, F, k, name) - W_quad(0, 1 - h, F, k, name)) / (2 * h)
    Ww = (W_quad(h, 1, F, k, name) - 2 * W0 + W_quad(-h, 1, F, k, name)) / h ** 2
    return W0, Wm, Ww


def S0_closed(F, gt):
    return math.pi / F * 2 / (1 + math.sqrt(1 - gt ** 2))


def instanton(F, gt, name="sech", npts=400):
    """worldline instanton: theta' = F h(k x3), x3' = cos, x4' = sin (m = 1), from the left turning point f(kc) = gt;
    returns the action m l - e Phi, the closure |x(end) - x(start)|, the total turning angle and the path"""
    k = gt * F
    h = (lambda x: 1 / math.cosh(k * x) ** 2) if name == "sech" else (lambda x: math.exp(-(k * x) ** 2))
    f = (lambda x: math.tanh(k * x)) if name == "sech" else (lambda x: math.sqrt(math.pi) / 2 * erf(k * x))
    c = brentq(lambda x: f(x) - gt, 0, 60 / k)

    def rhs(s, y):
        x3, x4, th, flux = y
        return [math.cos(th), math.sin(th), F * h(x3), F / k * f(x3) * math.sin(th)]
    ev = lambda s, y: y[2] - 1.5 * math.pi
    ev.terminal = True
    sol = solve_ivp(rhs, [0, 1e4], [-c, 0, -math.pi / 2, 0], events=ev, rtol=1e-12, atol=1e-14, dense_output=True)
    ell = sol.t_events[0][0]
    end = sol.y_events[0][0]
    path = sol.sol(np.linspace(0, ell, npts))
    return ell - end[3], math.hypot(end[0] + c, end[1]), end[2] + math.pi / 2, path


print(f"{'gt':>5} {'S0 (instanton loop)':>22} {'closed form':>22} {'rel.dev':>8} {'closure':>8} {'turn/2pi':>9} {'W(0,m) dev':>10} {'Mathematica':>8}")
LOOPS = {}
F = 0.5
for gt in GT_LOOP:
    S, clos, turn, path = instanton(F, gt)
    LOOPS[gt] = path
    Wq = float(W_quad(0, 1, F, gt * F, "sech"))
    sc = S0_closed(F, gt)
    ma = [r for r in MA["loop"] if abs(r[0] - gt) < 1e-12][0][1]
    print(f"{gt:5.2f} {S:22.15f} {sc:22.15f} {abs(S / sc - 1):8.1e} {clos:8.1e} {turn / (2 * math.pi):9.6f} {abs(Wq / sc - 1):10.1e} {abs(ma / sc - 1):8.1e}")
    rows.append(["loop", gt, S, sc, abs(S / sc - 1), clos, turn / (2 * math.pi), abs(Wq / sc - 1), abs(ma / sc - 1)])
for inv, gt in ((3, 0.3), (6, 0.3)):
    F, k = 1 / inv, 0.3 / inv
    W0, Wm, Ww = W_derivs(F, k, "sech")
    cW0, cWm, cWw = S0_closed(F, gt), math.pi / (F * math.sqrt(1 - gt ** 2)), 2 * math.pi * k ** 2 / (F ** 3 * (1 - gt ** 2) ** 1.5)
    print(f"m^2/eE = {inv}, gt = {gt}: W0, dW/dm^2, d^2W/dw^2 numerical/closed - 1 = {float(W0 / cW0 - 1):.1e}, "
          f"{float(Wm / cWm - 1):.1e}, {float(Ww / cWw - 1):.1e}")

# %% [markdown]
# ## Sauter potential: Im Gamma from Nikishov's nbar against the semiclassical formula and LCF

# %%
def im_gamma_sauter(F, gt, mean=False):
    """Im Gamma/(A T) = -(1/8 pi^2) int dw d(mt^2) ln(1 - nbar); mean=True: the mean number int nbar.  Scaled variables
    w = sw u (sw: Gaussian width of nbar in omega) and mt^2 = 1 + sm y (sm: decay scale in mt^2), with break points at
    1, 2, 4, 8, ... in u and 1, 3, 10, 30, ... in y (a plain break-point split in w, mt^2 lost 1e-7 at m^2/eE = 20)"""
    F, gt = mp.mpf(F), mp.mpf(gt)
    k = gt * F
    lam = F / k
    sw = 1 / mp.sqrt(2 * mp.pi * k ** 2 / (F ** 3 * (1 - gt ** 2) ** mp.mpf(1.5)))
    sm = F * mp.sqrt(1 - gt ** 2) / mp.pi
    umax = (lam - 1) / sw

    def inner(u):
        w = sw * u
        ymax = ((lam - w) ** 2 - 1) / sm
        g = (lambda y: nbar_exact(w, 1 + sm * y, lam, k)) if mean else (lambda y: -mp.log1p(-nbar_exact(w, 1 + sm * y, lam, k)))
        return mp.quad(g, [0] + [y for y in (1, 3, 10, 30, 100, 300) if y < ymax] + [ymax])
    total = mp.quad(inner, [0] + [u for u in (1, 2, 4, 8, 16, 32) if u < umax] + [umax])
    return mp.re(2 * sw * sm * total) / (8 * mp.pi ** 2)


def semiclassical(F, gt):
    return F ** 2.5 * (1 - gt ** 2) ** 1.25 / (8 * math.pi ** 3 * gt * F) * math.exp(-S0_closed(F, gt))


def lcf(F, gt):
    """locally constant field: int dx3 Im L(E(x3)) with all n (per unit area and time)"""
    k = gt * F
    X = mp.acosh(mp.sqrt(1 + 700 * F / mp.pi)) / k      # beyond X the exponent exceeds pi m^2/eE by 700
    return float(mp.quad(lambda x: im_const(F / mp.cosh(k * x) ** 2), [0, X / 4, X / 2, X])) * 2


def kim_page_mean(F, gt):
    """Kim and Page (2006), Eq. (62): pairs per area and time (two spin states) = 2 (lam k... )"""
    F, gt = mp.mpf(F), mp.mpf(gt)
    k = gt * F
    L = 1 / k
    Z, eps = 2 * mp.pi * F * L ** 2, 1 / (F * L)          # Z = 2 pi qE L^2, eps = m/(qEL)

    def inner(y):
        xm = mp.sqrt(max(0, 1 - eps ** 2 / (1 - y ** 2)))
        if xm <= 0:
            return 0
        g = lambda x: (mp.cosh(Z * y) - mp.cosh(Z * x)) / (mp.cosh(Z) - mp.cosh(Z * x)) * (y ** 2 - x ** 2)
        return mp.quad(g, [-min(xm, y), 0, min(xm, y)])
    ymax = mp.sqrt(1 - eps ** 2)
    return 2 * (F * L) ** 3 / (2 * mp.pi) ** 2 * mp.quad(inner, [0, ymax]) / 2     # per spin state: /2


print(f"{'m^2/eE':>6} {'gt':>4} {'Im Gamma/(A T) exact':>22} {'semiclassical':>14} {'exact/semi':>10} {'exact/LCF':>10} {'(1-g^2)^5/4 e^-dS':>17} {'Mathematica':>8} {'mean: KP dev':>12}")
TOT = {}
ma_tot = {(r[0], r[1]): r[2] for r in MA["total"]}
for inv, gt in GRID:
    F = 1 / inv
    ex = float(im_gamma_sauter(F, gt))
    sc = semiclassical(F, gt)
    lc = lcf(F, gt)
    rat_lcf_semi = (1 - gt ** 2) ** 1.25 * math.exp(-(S0_closed(F, gt) - math.pi / F))
    dm = abs(ma_tot[(inv, gt)] / ex - 1)
    dkp = ""
    if inv in (1, 5):
        mn = im_gamma_sauter(F, gt, mean=True)
        kp = kim_page_mean(F, gt)
        dkp = f"{float(abs(kp / mn - 1)):12.1e}"
    TOT[(inv, gt)] = (ex, sc, lc)
    print(f"{inv:6d} {gt:4.1f} {ex:22.12e} {sc:14.6e} {ex / sc:10.6f} {ex / lc:10.6f} {rat_lcf_semi:17.6f} {dm:8.1e} {dkp:>12}")
    rows.append(["total", inv, gt, ex, sc, ex / sc, lc, ex / lc, rat_lcf_semi, dm])

# %% [markdown]
# ## Gaussian field: instanton and Dirac equation mode by mode

# %%
def im_gamma_ode(F, gt, name, nw=24, nm=24):
    """-(1/8 pi^2) int dw d(mt^2) ln(1 - T) with T from the Dirac equation (omega >= 0 doubled: V odd)"""
    k = gt * F
    lam = F / k
    W0, Wm, Ww = W_derivs(F, k, name)
    sw, sm = float(1 / mp.sqrt(Ww)), float(1 / Wm)
    vmax = profile(name, lam, k)[1]
    wmax = min(vmax - 1 - 1e-9, 8 * sw)
    xw, aw = np.polynomial.legendre.leggauss(nw)
    xm, am = np.polynomial.legendre.leggauss(nm)
    tot = 0.0
    for wv, wa in zip((xw + 1) / 2 * wmax, aw / 2 * wmax):
        top = min((vmax - wv) ** 2, 1 + 40 * sm)
        for m2, ma in zip(1 + (xm + 1) / 2 * (top - 1), am / 2 * (top - 1)):
            T, _ = transmission(wv, math.sqrt(m2), lam, k, name)
            tot += 2 * wa * ma * (-math.log1p(-T))
    semi = float(mp.exp(-W0) / (8 * mp.pi ** 2) / Wm * mp.sqrt(2 * mp.pi / Ww))
    return tot / (8 * math.pi ** 2), semi, float(W0)


print(f"{'m^2/eE':>6} {'gt':>4} {'S0 (loop)':>18} {'W(0,m) (WKB)':>18} {'rel.dev':>8} {'Im Gamma (Dirac eq.)':>20} {'semiclassical':>14} {'ratio':>8} {'loop Math.':>10}")
GA = {}
for inv, gt in GAUSS:
    F = 1 / inv
    t0 = time.time()
    S, clos, turn, path = instanton(F, gt, "gauss")
    ex, sc, W0 = im_gamma_ode(F, gt, "gauss")
    ma = [r for r in MA["gauss"] if r[0] == inv and abs(r[1] - gt) < 1e-12][0][2]
    GA[(inv, gt)] = (ex, sc, path)
    print(f"{inv:6d} {gt:4.1f} {S:18.12f} {W0:18.12f} {abs(S / W0 - 1):8.1e} {ex:20.10e} {sc:14.6e} {ex / sc:8.5f} {abs(ma / S - 1):10.1e}  ({time.time() - t0:.0f} s)")
    rows.append(["gauss", inv, gt, S, W0, abs(S / W0 - 1), ex, sc, ex / sc, abs(ma / S - 1)])
# the mode integral of the Dirac equation for the Sauter potential reproduces the Nikishov integral
F, gt = 1 / 3, 0.3
ex_ode, _, _ = im_gamma_ode(F, gt, "sech")
print(f"Sauter, m^2/eE = 3, gt = 0.3: Im Gamma from the Dirac equation {ex_ode:.10e}, from nbar {TOT.get((3, 0.3), (float(im_gamma_sauter(F, gt)),))[0]:.10e}")

with open(os.path.join(HERE, "results", "schwinger.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["kind", "x1", "x2", "..."])
    wr.writerows(rows)
print("wrote results/schwinger.csv")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
COLORS = ["C0", "C1", "C2", "0.35"]     # colors of physrev.mplstyle
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.6))
ax = axes[0]
Fs = np.geomspace(0.05, 10, 60)
eh = lambda x: x ** 4 / (360 * math.pi ** 2)
reL = np.array([float(L_const(mp.mpf(x)).real) / eh(x) for x in Fs])
imL = [float(im_const(x)) / eh(x) for x in Fs]
pos = reL > 0
ax.plot(Fs[pos], reL[pos], color=COLORS[0], lw=1, ls="-", label=r"Re $\mathcal{L}$ / Euler-Heisenberg")
ax.plot(Fs[~pos], -reL[~pos], color=COLORS[0], lw=1, ls="--", label=r"$-$Re $\mathcal{L}$ (sign change)")
ax.plot(Fs, imL, color=COLORS[1], lw=1, ls="-", label=r"Im $\mathcal{L}$ / Euler-Heisenberg")
ax.plot(F_CONST, [abs(float(CONST[x][2])) / eh(x) for x in F_CONST], ls="none", marker="o", ms=2.4,
        color="0.3", label=r"dispersion ($|\mathrm{Re}|$)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1e-6, 30)
ax.set_xlabel(r"$eE/m^2$ (constant field)")
ax.set_ylabel(r"$\mathcal{L}\,/\,[(eE)^4/(360\pi^2m^4)]$")
ax.legend(frameon=False, fontsize=6, loc="lower right")
ax = axes[1]
for gt, col in zip(GT_LOOP, COLORS):
    p = LOOPS[gt]          # F = 1/2: unit m/(eE) = 2; the loop starts at the left turning point, x4 is centred here
    ax.plot(p[0] * 0.5, (p[1] - (p[1].max() + p[1].min()) / 2) * 0.5, color=col, lw=0.9, ls="-", label=rf"$\tilde\gamma={gt}$")
    th = np.linspace(0, 2 * np.pi, 200)
    a = 1 / math.sqrt(1 - gt ** 2)
    x3 = np.arcsinh(gt * a * np.sin(th)) / gt
    x4 = a * np.arcsin(gt * np.cos(th)) / gt
    ax.plot(x3 * 1, x4 * 1, color="k", lw=0.6, ls=":")
pg = GA[(4, 0.3)][2]
ax.plot(pg[0] * 0.25, (pg[1] - (pg[1].max() + pg[1].min()) / 2) * 0.25, color="0.65", lw=0.7, ls="--",
        label=r"Gaussian, $\tilde\gamma=0.3$")
ax.plot([], [], color="k", lw=0.6, ls=":", label="closed form")
ax.set_aspect("equal")
ax.set_xlim(-7.2, 2.2)
ax.set_xlabel(r"$x_3\ [m/(eE)]$")
ax.set_ylabel(r"$x_4\ [m/(eE)]$")
ax.legend(frameon=False, fontsize=6, loc="upper left")
ax = axes[2]
for inv, col in zip(INV_FIG, COLORS):
    F = 1 / inv
    ex = [float(im_gamma_sauter(F, g)) / lcf(F, g) for g in GT_FIG]
    ax.plot(GT_FIG, ex, color=col, lw=1, ls="-", label=rf"exact, $m^2/eE={inv}$")
    ax.plot(GT_FIG, [semiclassical(F, g) / lcf(F, g) for g in GT_FIG], color=col, lw=0.5, ls="--")
ax.plot([], [], color="0.4", lw=0.5, ls="--", label="semiclassical")
ax.set_yscale("log")
ax.set_ylim(1e-6, 2)
ax.set_xlim(0, 1)
ax.set_xlabel(r"$\tilde\gamma=mk/(eE)$")
ax.set_ylabel(r"Im $\Gamma$ / locally constant field")
ax.legend(frameon=False, fontsize=6.5, loc="lower left")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "schwinger.pdf"))
print("wrote ../figs/schwinger.pdf")
if INTERACTIVE:
    plt.show()
