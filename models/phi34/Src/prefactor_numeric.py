# %% [markdown]
# # Step (10): one-loop prefactor of the false-vacuum decay rate in d = 4 as a function of alpha
#
# Callan-Coleman (note, App. M; the phi^3 note, App. R):
#   Gamma/V = (S_B/2pi)^2 |det' M/det M_0|^{-1/2} e^{-S_B} = m^4 (S_B/2pi)^2 D^{-1/2} e^{-S_B},
#   M = -d^2 + V''(phi_B) = m^2 [-d_x^2 + 1 + U(x)],   U = f + alpha f^2/6,   S_B = (m^2/g^2) S_4(alpha),
# with x = m r and phi_B = (m^2/g) f the bounce of step (9).  M depends on alpha only, so the whole one-loop correction is
# one function ln D(alpha) (for given mu/m).
# Partial waves l (degeneracy (l+1)^2), Gel'fand-Yaglom: det M_l/det M_l^free = T_l(infinity),
#   T'' + [2 I_{l+2}(x)/I_{l+1}(x) + (2l+3)/x] T' = U T,   T(0) = 1, T'(0) = 0.
# l = 0: one negative mode.  l = 1: four zero modes, det' M_1/det M_1^free = S_4/(4 pi^2 f''(0) A) per mode,
#   f -> -A K_1(x)/x, f''(0) = v'(f(0))/4 (checked by shifting M -> M + lambda).
# Renormalization (MS-bar, tadpoles cancelled by Y): of the first-order term Tr[G0 U], the part f (linear in phi) is
# cancelled by Y; the part alpha f^2/6 (from lambda phi^2/2) leaves the MS-bar value
#   A_1(mu) = (alpha/48) (ln(m^2/mu^2) - 1) int x^3 f^2 dx;
# the second-order term in MS-bar from momentum space (U~ the 4d Fourier transform of U),
#   A_2(mu) = -1/2 int d^4p/(2pi)^4 |U~(p)|^2 B0_E(p)/(16 pi^2),   B0_E = 2 - b ln((b+1)/(b-1)) + ln(mu^2/m^2), b = sqrt(1+4/p^2);
# the third and higher orders from the partial waves with the first- and second-order Born terms h1, h2 subtracted:
#   ln D = sum_l (l+1)^2 [ln|T_l| - h1_l - h2_l + h1_l^2/2] + A_2(mu) + A_1(mu).
# Checks: S_4 against step (9); the tail amplitude A against the Green's-function integral A = int x^2 I_1 (f^2/2 +
# alpha f^3/18); int x^3 f^2 = (S_4 + alpha dS_4/dalpha)/pi^2; the zero mode by the lambda shift; one negative mode (Sturm);
# Parseval; the large-l coefficients of h1 and h2 - h1^2/2; the local formula of Dunne and Min (PRD 72, 125004 (2005),
# Eq. (4.12)) converted to our scheme, ln D = 2 Gamma_MS + 4 ln(S_4/(18 pi)) + (1/8) int x^3 f dx; mu-independence of the rate,
#   d(-S_B - ln D/2)/d ln mu = 0  <=>  [S_4 (3 - 5 alpha) + alpha W (3 - 2 alpha)]/(3 (4pi)^2) = (1/16) int x^3 [U^2 + alpha f^2/3],
#   W = dS_4/dalpha = 2 pi^2 int x^3 f^4/72;  the thin-wall limit (1 - alpha)^3 Gamma_MS -> (9/32)(1 - 2 pi/(9 sqrt 3)) = 0.16788888
#   (Konoplich-Rubin, as quoted by Dunne-Min, Eq. (4.21)).
# Then the cosmological condition S_B - 2 ln(S_B/2pi) + ln D/2 > 4 ln(m_h/H_0) in the (kappa_3, kappa_4) plane.
#
# Writes results/prefactor.csv and ../figs/prefactor_alpha.pdf, ../figs/stability.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python prefactor_numeric.py` (from Src/; about 20 minutes).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys
import time
from types import SimpleNamespace

import numpy as np
from scipy.integrate import simpson, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.special import ive, j1, kv, kve, zeta

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K16 = 16 * math.pi ** 2
MH, VEV, H0 = 125.25, 246.22, 1.44e-42
G_SM = 3 * MH / VEV
KR = 9 / 32 * (1 - 2 * math.pi / (9 * math.sqrt(3)))
ALPHAS = [float(sys.argv[1])] if len(sys.argv) > 1 and not INTERACTIVE else \
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.96, 0.97,
     0.98, 0.99]

STEP9 = {}
with open(os.path.join(HERE, "results", "bounce.csv")) as fh:
    for r in csv.reader(fh):
        if len(r) > 5 and r[0] == "4":
            STEP9[float(r[1])] = dict(S=float(r[3]), W=float(r[6]))


def pot(f, a):
    return f * f / 2 + f ** 3 / 6 + a * f ** 4 / 72


def dpot(f, a):
    return f + f * f / 2 + a * f ** 3 / 18


def f_true(a):
    return -9 / (2 * a) * (1 + math.sqrt(1 - 8 * a / 9))


def f_zero(a):
    return -3.0 if a == 0 else -6 * (1 - math.sqrt(1 - a)) / a


# %% [markdown]
# ## The bounce (d = 4): bisection as in step (9), then two-sided matching for the far tail
# Forward from x = 1e-5 (for alpha >= 0.5 in h = f - f_- until h = 0.1, then in f) to the wall centre XM, backward from
# XR = XM + 38 with the linear tail f = -A K_1(x)/x; Newton on (q0, A), q0 = ln h(0) or f(0), so that f, f' match at XM.

# %%
HSW = 0.1


def forward(a, q0, use_h, xend, rtol=1e-13, events=False, dense=False):
    """Forward integration (d = 4); returns (kind, pieces) with pieces = list of (solution, offset) in f."""
    def rhs_f(x, y):
        return [y[1], dpot(y[0], a) - 3 / x * y[1]]

    def cross(x, y):
        return y[0]
    cross.terminal, cross.direction = True, 1

    def turn(x, y):
        return y[1]
    turn.terminal, turn.direction = True, -1
    ev = (cross, turn) if events else None
    x0 = 1e-5
    pieces = []
    if use_h and math.exp(q0) < HSW:
        fm = f_true(a)
        c1, c2, c3 = 1 + fm + a * fm * fm / 6, (1 + a * fm / 3) / 2, a / 18
        h0 = math.exp(q0)

        def switch(x, y):
            return y[0] - HSW
        switch.terminal, switch.direction = True, 1
        acc = (c1 * h0 + c2 * h0 * h0 + c3 * h0 ** 3) / 8
        s1 = solve_ivp(lambda x, y: [y[1], c1 * y[0] + c2 * y[0] ** 2 + c3 * y[0] ** 3 - 3 / x * y[1]],
                       (x0, min(xend, 80.0 + max(0.0, -q0) / math.sqrt(c1))), [h0 + acc * x0 ** 2, 2 * acc * x0],
                       method="DOP853", rtol=rtol, atol=[1e-300, 1e-300], events=(switch,), dense_output=dense)
        pieces.append((s1, fm))
        if not s1.t_events[0].size:
            return "under", pieces
        xs, ys = s1.t[-1], [fm + s1.y[0, -1], s1.y[1, -1]]
    else:
        f0 = f_true(a) + math.exp(q0) if use_h else q0
        acc = dpot(f0, a) / 8
        xs, ys = x0, [f0 + acc * x0 ** 2, 2 * acc * x0]
    if xs < xend:
        s2 = solve_ivp(rhs_f, (xs, xend if not events else xs + 80.0), ys, method="DOP853", rtol=rtol, atol=1e-16,
                       events=ev, dense_output=dense)
        pieces.append((s2, 0.0))
        if events:
            return ("over" if s2.t_events[0].size else "under"), pieces
    return "end", pieces


def bisect_bounce(a):
    use_h = a >= 0.5
    if use_h:
        lo, hi = math.log(f_zero(a) - f_true(a)) - 1e-12, math.log(1e-280)
    elif a > 0:
        lo, hi = f_zero(a) - 1e-9, f_true(a) + 1e-9
    else:
        lo, hi = -3.0 - 1e-9, -40.0
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if forward(a, mid, use_h, 1e9, events=True)[0] == "over":
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) <= 4e-16 * max(abs(mid), 1.0):
            break
    return lo, use_h


def end_state(pieces):
    s, off = pieces[-1]
    return np.array([s.y[0, -1] + off, s.y[1, -1]])


def make_bounce(a):
    q0, use_h = bisect_bounce(a)
    # wall centre from the bisected trajectory: where f first rises above f(0)/2
    kind, pcs = forward(a, q0, use_h, 1e9, events=True, dense=True)
    t = np.concatenate([p[0].t for p in pcs])
    fv = np.concatenate([p[0].y[0] + p[1] for p in pcs])
    f0 = fv[0]
    XM = float(t[np.argmax(fv > f0 / 2)])
    XR = XM + 38.0

    def backward(A):
        return solve_ivp(lambda x, y: [y[1], dpot(y[0], a) - 3 / x * y[1]], (XR, XM),
                         [-A * kv(1, XR) / XR, A * kv(2, XR) / XR], method="DOP853", rtol=1e-13, atol=1e-30)

    def mismatch(q, A):
        return end_state(forward(a, q, use_h, XM)[1]) - backward(A).y[:, -1]
    i_tail = int(np.argmin(np.abs(fv - (-1e-4))))
    A = -fv[i_tail] * t[i_tail] / kv(1, t[i_tail])            # rough start from the bisected trajectory
    for _ in range(10):
        r = mismatch(q0, A)
        J = np.empty((2, 2))
        for j, (dq, dA) in enumerate(((1e-8 * max(abs(q0), 1.0), 0.0), (0.0, 1e-7 * A))):
            J[:, j] = (mismatch(q0 + dq, A + dA) - r) / (dq + dA)
        step = np.linalg.solve(J, -r)
        q0, A = q0 + step[0], A + step[1]
        if abs(step[0]) < 1e-15 * max(abs(q0), 1.0) and abs(step[1]) < 1e-13 * A:
            break
    kind, FW = forward(a, q0, use_h, XM, dense=True)
    BW = solve_ivp(lambda x, y: [y[1], dpot(y[0], a) - 3 / x * y[1]], (XR, XM), [-A * kv(1, XR) / XR, A * kv(2, XR) / XR],
                   method="DOP853", rtol=1e-13, atol=1e-30, dense_output=True)
    f0 = (f_true(a) + math.exp(q0)) if use_h else q0
    if use_h:          # v'(f(0)) from h(0) exactly: f(0) - f_- ~ e^{-R} is below the precision of f(0) near the thin wall
        fm, h0 = f_true(a), math.exp(q0)
        vp0 = (1 + fm + a * fm * fm / 6) * h0 + (1 + a * fm / 3) / 2 * h0 ** 2 + a / 18 * h0 ** 3
    else:
        vp0 = dpot(f0, a)
    return SimpleNamespace(a=a, f0=f0, vp0=vp0, A=A, XM=XM, XR=XR, FW=FW, BW=BW)


def fvec(b, x):
    """Bounce profile f(x) and f'(x) on an array x."""
    x = np.asarray(x, float)
    f, fp = np.empty_like(x), np.empty_like(x)
    lo = 0.0
    for s, off in b.FW:
        m = (x >= lo) & (x <= s.t[-1])
        if m.any():
            v = s.sol(np.clip(x[m], s.t[0], s.t[-1]))
            f[m], fp[m] = v[0] + off, v[1]
        lo = s.t[-1]
    m = (x > b.XM) & (x <= b.XR)
    if m.any():
        v = b.BW.sol(x[m])
        f[m], fp[m] = v[0], v[1]
    m = x > b.XR
    f[m] = -b.A * kv(1, x[m]) / x[m]
    fp[m] = b.A * kv(2, x[m]) / x[m]
    return f, fp


def fval(b, x):
    if x <= b.XM:
        for s, off in b.FW:
            if x <= s.t[-1]:
                return float(s.sol(max(x, s.t[0]))[0] + off)
    if x <= b.XR:
        return float(b.BW.sol(x)[0])
    return float(-b.A * kv(1, x) / x)


# %% [markdown]
# ## Partial waves with the potential U = f + alpha f^2/6

# %%
def rho_all(numax, z):
    """rho[nu] = I_{nu+1}(z)/I_nu(z) for nu = 0..numax, by the stable backward recurrence."""
    n = numax + 40 + int(2 * z)
    r = z / ((n + 1) + math.sqrt((n + 1) ** 2 + z * z))
    out = np.empty(numax + 1)
    for k in range(n - 1, -1, -1):
        r = z / (2 * (k + 1) + z * r)
        if k <= numax:
            out[k] = r
    return out


def radial(b, ls, kappa=1.0, born=True, rtol=1e-12, dense=False, xmax=None):
    a = b.a
    ls = np.asarray(ls)
    nl, x0 = len(ls), 1e-4
    u0 = b.f0 + a * b.f0 ** 2 / 6
    aa = u0 / (4 * (ls + 2))
    bb = u0 * u0 / (32 * (ls + 2) * (ls + 3))
    rows = [1 + aa * x0 ** 2, 2 * aa * x0]
    if born:
        rows += [aa * x0 ** 2, 2 * aa * x0, bb * x0 ** 4, 4 * bb * x0 ** 3]
    y0 = np.concatenate(rows)
    numax = int(ls.max()) + 1
    xmax = xmax or (b.XM + 34.0)

    def rhs(x, y):
        f = fval(b, x)
        u = f + a * f * f / 6
        c = 2 * kappa * rho_all(numax, kappa * x)[ls + 1] + (2 * ls + 3) / x
        Y = y.reshape(-1, nl)
        out = [Y[1], u * Y[0] - c * Y[1]]
        if born:
            out += [Y[3], u - c * Y[3], Y[5], u * Y[2] - c * Y[5]]
        return np.concatenate(out)
    return solve_ivp(rhs, (x0, xmax), y0, method="DOP853", rtol=rtol, atol=1e-16, dense_output=dense)


def tail_sum(w, lmax, lfit, ks=(3, 4, 5, 6)):
    l = np.arange(lfit[0], lfit[1] + 1)
    M = np.array([(l + 1.0) ** (-k) for k in ks]).T
    c = np.linalg.lstsq(M, w[l], rcond=None)[0]
    return float(np.sum(w[: lfit[1] + 1])) + sum(ck * zeta(k, lfit[1] + 2) for ck, k in zip(c, ks)), c


# %% [markdown]
# ## ln D(alpha)

# %%
def prefactor(a, verbose=True):
    t0 = time.time()
    b = make_bounce(a)
    R = b.XM
    xg = np.linspace(0.0, b.XR, int(b.XR * 8000) + 1)
    xg[0] = 1e-12
    fg, fpg = fvec(b, xg)
    ug = fg + a * fg ** 2 / 6
    S4 = 2 * math.pi ** 2 * simpson(xg ** 3 * (fpg ** 2 / 2 + pot(fg, a)), x=xg)
    Tk = 2 * math.pi ** 2 * simpson(xg ** 3 * fpg ** 2 / 2, x=xg)
    W = 2 * math.pi ** 2 * simpson(xg ** 3 * fg ** 4 / 72, x=xg)
    I3f2 = simpson(xg ** 3 * fg ** 2, x=xg)
    I3f = simpson(xg ** 3 * fg, x=xg)
    I1u = simpson(xg * ug, x=xg)
    I3u2 = simpson(xg ** 3 * ug ** 2, x=xg)
    I3uu2 = simpson(xg ** 3 * ug * (ug + 2), x=xg)
    A_green = simpson(xg ** 2 * ive(1, xg) * np.exp(xg) * (fg ** 2 / 2 + a * fg ** 3 / 18), x=xg)
    fpp0 = b.vp0 / 4                                         # f''(0) = v'(f(0))/4
    out = dict(alpha=a, f0=b.f0, A=b.A, A_green=A_green, R=R, S4=S4, derrick=(Tk + 2 * (S4 - Tk)) / Tk, W=W,
               I3f2=I3f2, I3f=I3f)
    # partial waves
    lmax = int(max(200, 12 * R))
    ls = np.arange(lmax + 1)
    sol = radial(b, ls)
    Y = sol.y[:, -1].reshape(6, -1)
    Tinf, h1, h2 = Y[0], Y[2], Y[4]
    c_zero = S4 / (4 * math.pi ** 2 * fpp0 * b.A)
    lnT = np.log(np.abs(Tinf))
    lnT[1] = math.log(c_zero)
    rl = lnT - h1 - h2 + h1 ** 2 / 2
    wl = (ls + 1.0) ** 2 * rl
    Sigma, cfit = tail_sum(wl, lmax, (lmax // 3, lmax))
    Sigma_b, _ = tail_sum(wl, lmax, (lmax // 2, lmax), ks=(3, 4, 5))
    # zero mode by the lambda shift, negative mode
    def dlam(lam):
        tp = radial(b, [1], kappa=math.sqrt(1 + lam), born=False).y[0, -1]
        tm = radial(b, [1], kappa=math.sqrt(1 - lam), born=False).y[0, -1]
        return (tp - tm) / (2 * lam)
    lam = 2e-3 / max(R, 1.0) ** 2
    c_lam = (4 * dlam(lam / 2) - dlam(lam)) / 3           # Richardson on the central difference
    T0lam = lambda la: radial(b, [0], kappa=math.sqrt(1 + la), born=False).y[0, -1]
    lam_neg = brentq(T0lam, 1e-9, 30.0, xtol=1e-14, rtol=1e-12)
    # second order in momentum space (Gauss-Legendre in p; the oscillation period in p is ~ 2 pi/R)
    PMAX = 40.0 if R < 20 else 20.0                       # U~ falls off on the scale of the wall thickness
    npn = int(max(400, 2 * PMAX * R))
    pn, pw = np.polynomial.legendre.leggauss(npn)
    P, PW = (pn + 1) * PMAX / 2, pw * PMAX / 2
    keep = xg <= b.XM + 34.0
    Xh, Uh = xg[keep][::4], ug[keep][::4]
    Ut = np.array([4 * math.pi ** 2 / p * simpson(Xh ** 2 * j1(p * Xh) * Uh, x=Xh) for p in P])
    beta = np.sqrt(1 + 4 / P ** 2)
    B0E = 2 - 2 * beta * np.arctanh(1 / beta)
    pars = np.sum(PW * P ** 3 * Ut ** 2) / (8 * math.pi ** 2)
    A2 = -0.5 * np.sum(PW * P ** 3 * Ut ** 2 * B0E) / (8 * math.pi ** 2) / K16
    A1 = -a / 48 * I3f2
    lnD = Sigma + A2 + A1
    # Dunne-Min local formula (their Eq. (4.12)) with V = U, converted to our scheme
    Phi_inf, Phi0 = b.A / 3, -b.f0 / 3
    Up0 = -b.vp0 / 3                                         # U'(Phi_0) = Phi0 - 3/2 Phi0^2 + alpha/2 Phi0^3 = -v'(f0)/3
    Iloc = simpson(xg[1:] ** 3 * ug[1:] * (ug[1:] + 2) * (0.5 - np.euler_gamma - np.log(xg[1:] / 2)), x=xg[1:])
    wdm = (ls + 1.0) ** 2 * (lnT - (I1u / 2) / (ls + 1.0) + (I3uu2 / 8) / (ls + 1.0) ** 3)
    wdm[:2] = 0.0
    Sdm, _ = tail_sum(wdm, lmax, (lmax // 3, lmax))
    Gamma_dm = 0.5 * lnT[0] - 2 * math.log(abs(math.pi / 2 * Phi_inf * Up0)) + 0.5 * Sdm - 0.75 * I1u + Iloc / 16
    lnD_dm = 2 * Gamma_dm + 4 * math.log(S4 / 9 / (2 * math.pi)) + I3f / 8
    Gamma_ms = 0.5 * (lnD - 4 * math.log(S4 / 9 / (2 * math.pi)) - I3f / 8)      # Dunne-Min's Gamma_MS from our ln D
    # mu-independence: dS_B/d ln mu (from the RG coefficients) against (1/16) int x^3 [U^2 + alpha f^2/3]
    rg_lhs = (S4 * (3 - 5 * a) + a * W * (3 - 2 * a)) / (3 * K16)
    rg_rhs = (I3u2 + a / 3 * I3f2) / 16
    out.update(lmax=lmax, T0=Tinf[0], T1=Tinf[1], e_neg=-lam_neg, c_zero=c_zero, c_lam=c_lam, Sigma=Sigma,
               Sigma_alt=Sigma_b, l0=wl[0], l1=wl[1], A2=A2, A1=A1, lnD=lnD, lnD_dm=lnD_dm, Gamma_ms=Gamma_ms,
               Gamma_dm=Gamma_dm, parseval=pars / (2 * math.pi ** 2 * I3u2) - 1, dA2=-0.5 * pars / K16,
               h1_large=h1[lmax] * (lmax + 1) / (I1u / 2) - 1,
               h2_large=(h2[lmax] - h1[lmax] ** 2 / 2) * (lmax + 1) ** 3 / (-I3u2 / 8) - 1,
               rg_lhs=rg_lhs, rg_rhs=rg_rhs, c3=cfit[0], steps=sol.t.size, secs=time.time() - t0)
    if verbose:
        s9 = STEP9.get(a)
        print(f"alpha = {a:5.3f}: R = {R:6.2f}, l_max = {lmax}, S_4 = {S4:.10f}"
              + (f" (step 9: rel. {S4 / s9['S'] - 1:.1e})" if s9 else "")
              + f", A = {b.A:.10f} (Green rel. {A_green / b.A - 1:.1e}), int x^3 f^2 vs (S_4 + alpha W)/pi^2: "
              f"{I3f2 / ((S4 + a * W) / math.pi ** 2) - 1:.1e}", flush=True)
        print(f"    T_0 = {Tinf[0]:.6e} (e_- = {-lam_neg:.6e}), zero mode {c_zero:.10e} vs lambda-shift rel. {c_lam / c_zero - 1:.1e}, "
              f"sum = {Sigma:.9f} (alt. fit {Sigma_b - Sigma:.1e}), A_2 = {A2:.9f}, A_1 = {A1:.9f}", flush=True)
        print(f"    ln D = {lnD:.9f}, Dunne-Min {lnD_dm:.9f} (diff. {lnD_dm - lnD:.1e}); Parseval {out['parseval']:.1e}; "
              f"large l: h1 {out['h1_large']:.1e}, h2 {out['h2_large']:.1e}; mu: {rg_lhs:.10f} vs {rg_rhs:.10f} "
              f"(rel. {rg_rhs / rg_lhs - 1:.1e}); Gamma_MS = {Gamma_ms:.6f}, (1-alpha)^3 Gamma_MS = {(1 - a) ** 3 * Gamma_ms:.6f}; "
              f"{out['secs']:.0f} s", flush=True)
    return out, b


results = {}
for a in ALPHAS:
    results[a], _ = prefactor(a)


# %% [markdown]
# ## Summary over alpha, the thin-wall limit, and the output

# %%
al = np.array(sorted(results))
get = lambda k: np.array([results[a][k] for a in al])
for k, lab in (("lnD_dm", "Dunne-Min - ours"),):
    print(f"{lab}: largest |difference| {np.max(np.abs(get(k) - get('lnD'))):.1e} "
          f"(relative to |ln D|: {np.max(np.abs(get(k) - get('lnD')) / np.abs(get('lnD'))):.1e})")
print(f"mu-independence identity: largest relative deviation {np.max(np.abs(get('rg_rhs') / get('rg_lhs') - 1)):.1e}")
print(f"zero mode, lambda shift: largest relative deviation {np.max(np.abs(get('c_lam') / get('c_zero') - 1)):.1e}")
twr = (1 - al) ** 3 * get("Gamma_ms")
sel = al >= 0.9
tw_fit = np.polyfit(1 - al[sel], twr[sel], 2)
print(f"(1 - alpha)^3 Gamma_MS extrapolated to alpha = 1 (quadratic, alpha >= 0.9): {tw_fit[-1]:.5f}  vs  KR {KR:.8f}  "
      f"(rel. {tw_fit[-1] / KR - 1:.1e})")
corr = 0.5 * get("lnD") / get("S4")                        # (ln D/2)/S_B = corr g^2/m^2
for a in (0.0, 0.5, 0.9, 0.97, 0.99):
    if a in results:
        print(f"alpha = {a}: (ln D/2)/S_4 = {0.5 * results[a]['lnD'] / results[a]['S4']:+.5f}  (one-loop correction to the exponent "
              f"in units of g^2/m^2);  R = {results[a]['R']:.1f}")

with open(os.path.join(HERE, "results", "prefactor.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    keys = ["alpha", "R", "lmax", "f0", "A", "A_green", "S4", "W", "T0", "e_neg", "c_zero", "c_lam", "Sigma", "Sigma_alt",
            "A2", "A1", "lnD", "lnD_dm", "Gamma_ms", "rg_lhs", "rg_rhs", "parseval"]
    w.writerow(keys)
    for a in al:
        w.writerow([results[a][k] for k in keys])


# %% [markdown]
# ## The cosmological condition in the (kappa_3, kappa_4) plane
# m = m_h, g = 1.5261 kappa_3 m_h, alpha = kappa_4/kappa_3^2 (MS-bar at mu = m); S_B = S_4(alpha)/(1.5261 kappa_3)^2.
# One loop: S_B - 2 ln(S_B/2pi) + ln D(alpha)/2 > 4 ln(m_h/H_0); tree estimate (A ~ m^4): S_B > 4 ln(m_h/H_0).

# %%
sb_cosmo = 4 * math.log(MH / H0)
lnS4 = CubicSpline(al, np.log(get("S4")))
rDs = CubicSpline(al, get("lnD") / get("S4"))     # ln D itself spans 1 ... -2e7: spline the smooth ratio ln D/S_4


def lnDs(a):
    return float(rDs(a)) * math.exp(lnS4(a))


def expo(k3, k4, loop=True):
    a = k4 / k3 ** 2
    sb = math.exp(lnS4(a)) / (G_SM * k3) ** 2
    return sb - 2 * math.log(sb / (2 * math.pi)) + 0.5 * float(lnDs(a)) if loop else sb


def k3_bound(k4, loop=True):
    """The kappa_3 where the condition is first violated coming from large kappa_3 (small alpha).  Closer to alpha = 1 the
    one-loop term grows like R g^2/m^2 and eventually exceeds S_B (perturbation theory fails there), so the scan stops at the
    first sign change."""
    k3s = np.geomspace(20.0, max(math.sqrt(k4 / al[-1]), 0.05), 2000)
    v = [expo(k3, k4, loop) - sb_cosmo for k3 in k3s]
    i = next(j for j in range(len(v)) if v[j] > 0)
    return brentq(lambda k3: expo(k3, k4, loop) - sb_cosmo, k3s[i], k3s[i - 1])


K4S = np.linspace(0, 8, 81)
bound_tree = np.array([k3_bound(k4, False) for k4 in K4S])
bound_loop = np.array([k3_bound(k4, True) for k4 in K4S])
for k4 in (0.0, 0.5, 1.0, 2.0, 5.0, 8.0):
    kt, kl = k3_bound(k4, False), k3_bound(k4, True)
    a = k4 / kl ** 2
    sb = math.exp(lnS4(a)) / (G_SM * kl) ** 2
    print(f"kappa_4 = {k4:3.1f}: kappa_3 < {kl:.4f} (one loop; alpha = {a:.3f}, S_B = {sb:.1f}, (ln D/2)/S_B = {0.5 * float(lnDs(a)) / sb:+.4f}, prefactor exp({-2 * math.log(sb / (2 * math.pi)) + 0.5 * float(lnDs(a)):+.2f}) "
          f"m^4 -> exp({2 * math.log(sb / (2 * math.pi)) - 0.5 * float(lnDs(a)):.2f}));  tree estimate {kt:.4f}")
with open(os.path.join(HERE, "results", "prefactor.csv"), "a", newline="") as fh:
    w = csv.writer(fh)
    w.writerow([])
    w.writerow(["kappa_4", "kappa_3_bound_one_loop", "kappa_3_bound_tree"])
    for k4, kl, kt in zip(K4S, bound_loop, bound_tree):
        w.writerow([k4, kl, kt])


# %% [markdown]
# ## Figures: Gamma_MS in Dunne-Min's normalization and the size of the one-loop correction; the stability bound

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1))
near = al >= 0.85
ax1.plot(al[near], twr[near], "o", ms=3.0, mfc="none", mec="k", label=r"this note")
xx = np.linspace(0, 0.1, 50)
ax1.plot(1 - xx, np.polyval(tw_fit, xx), color="0.55", lw=0.6, ls="-", label=r"quadratic fit ($\alpha\geq0.9$)")
ax1.plot([1.0], [KR], "*", ms=7, color="#eb6235", clip_on=False, zorder=6, label="thin wall (Konoplich-Rubin)")
ax1.set_xlim(0.85, 1.0)
ax1.set_xlabel(r"$\alpha$")
ax1.set_ylabel(r"$(1-\alpha)^3\,\Gamma_{\overline{\rm MS}}$")
ax1.legend(loc="lower left")
ax2.plot(al, corr, color="k", lw=0.9, marker="o", ms=2.5)
ax2.axhline(0, color="0.6", lw=0.5)
ax2.set_xlim(0, 1)
ax2.set_xlabel(r"$\alpha=3\lambda m^2/g^2$")
ax2.set_ylabel(r"$\ln\mathcal{D}/(2S_4)$")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "prefactor_alpha.pdf"))

fig, ax = plt.subplots(figsize=(3.25, 2.8))
kk = np.linspace(0, 3.5, 300)
ax.fill_betweenx(K4S, bound_loop, 3.5, color="#f2c9bb", lw=0)          # decays within the age of the universe
ax.plot(kk, kk ** 2, color="0.4", lw=0.7, ls=":", label=r"$\alpha=1$")
ax.plot(bound_tree, K4S, color="#5d81b4", lw=0.9, ls="--", label=r"$S_B=4\ln(m_h/H_0)$ ($A\sim m_h^4$)")
ax.plot(bound_loop, K4S, color="k", lw=0.9, ls="-", label="one-loop prefactor")
ax.plot([1.0], [1.0], "o", ms=3.5, color="#eb6235", zorder=6)
ax.text(0.25, 5.2, "stable\n" + r"($\alpha>1$)", fontsize=6.5, ha="left")
ax.text(2.45, 5.0, "metastable, long-lived", fontsize=6.0, ha="center", va="center", rotation=59)
ax.text(3.05, 1.6, "too\nshort-\nlived", fontsize=6.5, ha="center")
ax.set_xlim(0, 3.5)
ax.set_ylim(0, 8)
ax.set_xlabel(r"$\kappa_3$")
ax.set_ylabel(r"$\kappa_4$")
ax.legend(loc="upper left", fontsize=6.0, bbox_to_anchor=(0.0, 1.0))
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "stability.pdf"))
print("wrote results/prefactor.csv, figs/prefactor_alpha.pdf and figs/stability.pdf")
