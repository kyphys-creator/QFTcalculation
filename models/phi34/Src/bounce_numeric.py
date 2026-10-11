# %% [markdown]
# # Step (9): bounce action of the false vacuum phi = 0 as a function of alpha, in d = 4 and d = 3
#
# With phi = (m^2/g) f and r = x/m, the potential of the note's Eq. (13) is V = (m^6/g^2) v(f),
#   v(f) = f^2/2 + f^3/6 + alpha f^4/72,   alpha = 3 lambda m^2/g^2,
# and for alpha < 1 the false vacuum f = 0 decays through the O(d)-symmetric bounce (note, App. L)
#   f'' + (d-1)/x f' = v'(f) = f + f^2/2 + alpha f^3/18,   f'(0) = 0,   f(infinity) = 0,
#   S_B = (m^{6-d}/g^2) S(alpha),   S(alpha) = Omega_{d-1} int x^{d-1} dx [f'^2/2 + v(f)].
# True vacuum f_- = -(9/(2 alpha))(1 + sqrt(1 - 8 alpha/9)); v = 0 again at f_z = -6 (1 - sqrt(1 - alpha))/alpha.
# Shooting on f(0) between f_z (undershoot) and f_- (overshoot).  Near the thin-wall limit f(0) - f_- ~ e^{-R} is below
# double precision, so for alpha >= 0.5 the deviation h = f - f_- is integrated with the exact polynomial
# v'(f_- + h) = v''(f_-) h + v'''(f_-) h^2/2 + v''''(f_-) h^3/6 (v'(f_-) = 0 dropped) and the bisection is on ln h(0).
# Checks: Derrick's relation (d-2) T + d U = 0; dS/dalpha = Omega_{d-1} int x^{d-1} f^4/72 (the bounce is stationary, so only
# the explicit alpha-dependence of the action contributes); relaxation (scipy solve_bvp) from a thin-wall guess;
# alpha = 0 against the phi^3 note (C_3 = 174.6409, C_4 = 817.7138); the thin-wall limits S -> 3 pi^2/(1 - alpha)^3 (d = 4)
# and (32 pi/9)/(1 - alpha)^2 (d = 3) (App. L); d = 3 against Dine, Leigh, Huet, Linde, Linde (1992), Eqs. (26), (27):
#   S_3/T = 4.85 M^3/(E^2 T^3) f(alpha),  f(alpha) = 1 + (alpha/4)[1 + 2.4/(1 - alpha) + 0.26/(1 - alpha)^2]
#   (about 1% for 0 <= alpha <= 0.95), i.e. S(alpha) = 36 x 4.85 f(alpha) in d = 3 (M = m, E T = -g/6, their alpha = ours).
# Higgs reading (illustration, no prefactor): S_B (d = 4) = S(kappa_4/kappa_3^2)/(1.5261 kappa_3)^2 against 4 ln(m_h/H_0).
#
# Writes results/bounce.csv and ../figs/bounce_alpha.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python bounce_numeric.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

from types import SimpleNamespace

import numpy as np
from scipy.integrate import solve_bvp, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
C_PHI3 = {3: 174.64094686498785, 4: 817.7137733676353}     # phi^3 note, results/bounce.csv
DINE = 36 * 4.85
MH, VEV, H0 = 125.25, 246.22, 1.44e-42                     # GeV; H_0 = 67.4 km/s/Mpc
G_SM, L_SM = 3 * MH / VEV, 3 * MH ** 2 / VEV ** 2
ALPHAS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.825, 0.85, 0.875,
          0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.985, 0.99]


def omega(d):
    return 2 * math.pi ** (d / 2) / math.gamma(d / 2)


def pot(f, a):
    return f * f / 2 + f ** 3 / 6 + a * f ** 4 / 72


def dpot(f, a):
    return f + f * f / 2 + a * f ** 3 / 18


def f_true(a):
    return -9 / (2 * a) * (1 + math.sqrt(1 - 8 * a / 9))


def f_zero(a):
    return -3.0 if a == 0 else -6 * (1 - math.sqrt(1 - a)) / a


def dine(a):
    return DINE * (1 + a / 4 * (1 + 2.4 / (1 - a) + 0.26 / (1 - a) ** 2))


# %% [markdown]
# ## Shooting
# The particle analogy: f moves in -v(f) with friction (d-1)/x, starting at rest at f(0) and ending at rest at the top f = 0.
# Too close to f_z it turns back (undershoot); too close to the hilltop f_- of -v it stays long and then crosses 0 (overshoot).
# T, U and W = Omega int x^{d-1} f^4/72 are carried along.

# %%
HSW = 0.1      # h = f - f_- at which the h-variable integration hands over to the f-variable one


def shoot(d, a, q0, use_h, rtol=1e-13):
    """Integrate from x0 with the regular series; q0 = f(0) - f_- (use_h) or f(0).  Returns ('over' | 'under', sol), with
    sol.t and sol.y = (f, f', T, U, W) of both phases joined."""
    om = omega(d)

    def rhs_f(x, y):
        f, fp = y[0], y[1]
        return [fp, dpot(f, a) - (d - 1) / x * fp, om * x ** (d - 1) * fp * fp / 2, om * x ** (d - 1) * pot(f, a),
                om * x ** (d - 1) * f ** 4 / 72]

    def cross(x, y):                    # f reaches 0: overshoot
        return y[0]
    cross.terminal, cross.direction = True, 1

    def turn(x, y):                     # f' changes sign below 0: undershoot
        return y[1]
    turn.terminal, turn.direction = True, -1
    x0 = 1e-5
    ts, ys, nfev = [], [], 0
    if use_h and q0 < HSW:
        # phase 1: h = f - f_- with v'(f_- + h) as an exact polynomial in h, while h is small
        fm = f_true(a)
        c1, c2, c3 = 1 + fm + a * fm * fm / 6, (1 + a * fm / 3) / 2, a / 18

        def rhs_h(x, y):
            h, hp = y[0], y[1]
            f = fm + h
            return [hp, c1 * h + c2 * h * h + c3 * h ** 3 - (d - 1) / x * hp, om * x ** (d - 1) * hp * hp / 2,
                    om * x ** (d - 1) * pot(f, a), om * x ** (d - 1) * f ** 4 / 72]

        def switch(x, y):
            return y[0] - HSW
        switch.terminal, switch.direction = True, 1
        acc = (c1 * q0 + c2 * q0 * q0 + c3 * q0 ** 3) / (2 * d)
        y0 = [q0 + acc * x0 ** 2, 2 * acc * x0, 0.0, 0.0, 0.0]
        # long enough to roll off the hilltop f_- of -v (h grows like e^{sqrt(v''(f_-)) x})
        xmax = 80.0 + max(0.0, -math.log(q0)) / math.sqrt(c1)
        s1 = solve_ivp(rhs_h, (x0, xmax), y0, method="DOP853", rtol=rtol, atol=[1e-300, 1e-300, 1e-16, 1e-16, 1e-16],
                       events=(switch, turn))
        nfev += s1.nfev
        y1 = s1.y.copy()
        y1[0] += fm
        ts.append(s1.t)
        ys.append(y1)
        if not s1.t_events[0].size:     # turned back (or never left the hilltop) before h = HSW
            return "under", SimpleNamespace(t=np.concatenate(ts), y=np.hstack(ys), nfev=nfev)
        xs, ystart = s1.t[-1], y1[:, -1]
    else:
        f0 = f_true(a) + q0 if use_h else q0
        acc = dpot(f0, a) / (2 * d)
        xs, ystart = x0, np.array([f0 + acc * x0 ** 2, 2 * acc * x0, 0.0, 0.0, 0.0])
    # phase 2: f itself (no cancellation near f = 0)
    s2 = solve_ivp(rhs_f, (xs, xs + 80.0), ystart, method="DOP853", rtol=rtol, atol=1e-16, events=(cross, turn))
    nfev += s2.nfev
    ts.append(s2.t)
    ys.append(s2.y)
    return ("over" if s2.t_events[0].size else "under"), SimpleNamespace(t=np.concatenate(ts), y=np.hstack(ys), nfev=nfev)


def bounce(d, a, rtol=1e-13):
    use_h = a >= 0.5
    if use_h:                           # bisection on ln h(0), h(0) in (tiny, f_z - f_-)
        lo, hi = math.log(f_zero(a) - f_true(a)) - 1e-12, math.log(1e-280)    # lo: undershoot, hi: overshoot
        val = lambda q: math.exp(q)
    elif a > 0:
        lo, hi = f_zero(a) - 1e-9, f_true(a) + 1e-9
        val = lambda q: q
    else:
        lo, hi, val = -3.0 - 1e-9, None, (lambda q: q)
        q = -4.0
        while True:
            if shoot(d, a, q, False, rtol)[0] == "over":
                hi = q
                break
            lo, q = q, 2 * q
    assert shoot(d, a, val(lo), use_h, rtol)[0] == "under" and shoot(d, a, val(hi), use_h, rtol)[0] == "over"
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if shoot(d, a, val(mid), use_h, rtol)[0] == "over":
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) <= 4e-16 * max(abs(mid), 1.0):
            break
    kind, sol = shoot(d, a, val(lo), use_h, rtol)      # the undershooting trajectory follows the bounce longest
    fm = 0.0                                          # sol.y[0] is f
    i = int(np.argmin(np.abs(sol.y[0])))              # cut where |f| is smallest, before it turns back
    T, U, W = sol.y[2][i], sol.y[3][i], sol.y[4][i]
    return dict(d=d, a=a, f0=(f_true(a) if use_h else 0.0) + val(lo), h0=val(lo) if use_h else float("nan"), T=T, U=U, W=W, S=T + U, S_T=2 * T / d,
                derrick=((d - 2) * T + d * U) / T, xcut=sol.t[i], fcut=fm + sol.y[0][i], sol=sol, icut=i, use_h=use_h, fm=fm)


res = {(d, a): bounce(d, a) for d in (3, 4) for a in ALPHAS}
print(f"{'d':>2} {'alpha':>6} {'f(0)':>12} {'S(alpha)':>16} {'2T/d':>16} {'Derrick':>9} {'x_cut':>6}")
for (d, a), r in res.items():
    print(f"{d:2d} {a:6.3f} {r['f0']:12.8f} {r['S']:16.8f} {r['S_T']:16.8f} {r['derrick']:9.1e} {r['xcut']:6.1f}")


# %% [markdown]
# ## Checks: alpha = 0, the two shooting variables, tolerance, dS/dalpha, and relaxation

# %%
for d in (3, 4):
    print(f"d = {d}, alpha = 0: S = {res[(d, 0.0)]['S']:.10f} vs phi^3 note {C_PHI3[d]:.10f} "
          f"(rel. {abs(res[(d, 0.0)]['S'] / C_PHI3[d] - 1):.1e})")
# the h-variable shooting against the plain one where both work, and the tolerance
for d in (3, 4):
    for a in (0.5, 0.7, 0.9):
        r_h = res[(d, a)]
        r_f = None
        lo, hi = f_zero(a) - 1e-9, f_true(a) + 1e-9
        for _ in range(300):
            mid = 0.5 * (lo + hi)
            if shoot(d, a, mid, False)[0] == "over":
                hi = mid
            else:
                lo = mid
            if abs(hi - lo) <= 4e-16 * abs(mid):
                break
        kind, sol = shoot(d, a, lo, False)
        i = int(np.argmin(np.abs(sol.y[0])))
        s_f = sol.y[2][i] + sol.y[3][i]
        r_loose = bounce(d, a, rtol=1e-11)
        print(f"d = {d}, alpha = {a}: h-shooting {r_h['S']:.10f}, f-shooting {s_f:.10f} (rel. {abs(s_f / r_h['S'] - 1):.1e}); "
              f"rtol 1e-11 -> {abs(r_loose['S'] / r_h['S'] - 1):.1e}")
dmax = max(abs(r["derrick"]) for r in res.values())
print(f"Derrick's relation: largest |(d-2)T + dU|/T = {dmax:.1e}")


# %%
# dS/dalpha: a cubic spline through S(alpha) against W(alpha) = Omega int x^{d-1} f^4/72
dsda = {}
for d in (3, 4):
    a_arr = np.array(ALPHAS)
    s_arr = np.array([res[(d, a)]["S"] for a in ALPHAS])
    w_arr = np.array([res[(d, a)]["W"] for a in ALPHAS])
    spl = CubicSpline(a_arr, np.log(s_arr))
    deriv = spl(a_arr, 1) * s_arr
    inner = (a_arr >= 0.1) & (a_arr <= 0.95)
    dsda[d] = max(abs(deriv[inner] / w_arr[inner] - 1))
    print(f"d = {d}: dS/dalpha (spline of ln S) vs W = Omega int x^{d - 1} f^4/72: largest relative deviation {dsda[d]:.1e} "
          f"(0.1 <= alpha <= 0.95);  at alpha = 0: W = {w_arr[0]:.4f}")
print(f"d = 3 at alpha = 0: dS/dalpha = W = {res[(3, 0.0)]['W']:.3f};  Dine's fit: 36 x 4.85 x f'(0) = {DINE * (1 + 2.4 + 0.26) / 4:.3f}")


# %%
# relaxation (solve_bvp) from the guess f = f_-/(1 + e^{x - R}) (R = (d-1) sigma/epsilon, sigma = 6, epsilon = -v(f_-)).
# It converges for alpha <= 0.6; closer to the thin-wall limit it falls onto the trivial solution f = 0 (also when continued
# in alpha), so there the checks are the two shooting variables, Derrick's relation, dS/dalpha and the thin-wall limit.
bvp = {}
RELAX = (0.3, 0.6)
for d in (3, 4):
    eps, L = 1e-4, 70.0
    xg = np.linspace(eps, L, 8000)
    for a in RELAX:
        fm = f_true(a)
        R = max((d - 1) * 6 / (-pot(fm, a)), 2.0)
        yg = np.vstack([fm / (1 + np.exp(xg - R)), -fm * np.exp(xg - R) / (1 + np.exp(xg - R)) ** 2])
        solb = solve_bvp(lambda x, y: np.vstack([y[1], dpot(y[0], a) - (d - 1) / x * y[1]]),
                         lambda ya, yb: np.array([ya[1] - dpot(ya[0], a) * eps / d, yb[1] + (1 + (d - 1) / (2 * L)) * yb[0]]),
                         xg, yg, tol=1e-10, max_nodes=1000000)
        xs = np.linspace(eps, L, 1400001)
        f, fp = solb.sol(xs)
        Tb = omega(d) * np.trapezoid(xs ** (d - 1) * fp ** 2 / 2, xs)
        Ub = omega(d) * np.trapezoid(xs ** (d - 1) * pot(f, a), xs)
        bvp[(d, a)] = Tb + Ub
        print(f"d = {d}, alpha = {a}: relaxation (status {solb.status}) S = {Tb + Ub:.8f}, shooting {res[(d, a)]['S']:.8f}, "
                  f"rel. {abs((Tb + Ub) / res[(d, a)]['S'] - 1):.1e}")


# %%
# dS/dalpha by central differences of the shooting (step 1e-4) against W = Omega int x^{d-1} f^4/72
dsda_cd = {}
for d in (3, 4):
    for a in (0.3, 0.9):
        dl = 1e-4
        cd = (bounce(d, a + dl)["S"] - bounce(d, a - dl)["S"]) / (2 * dl)
        dsda_cd[(d, a)] = abs(cd / res[(d, a)]["W"] - 1)
        print(f"d = {d}, alpha = {a}: [S(alpha + 1e-4) - S(alpha - 1e-4)]/2e-4 = {cd:.8f}, W = {res[(d, a)]['W']:.8f}, "
              f"rel. {dsda_cd[(d, a)]:.1e}")


# %% [markdown]
# ## Thin-wall limits and Dine et al.

# %%
tw = {4: 3 * math.pi ** 2, 3: 32 * math.pi / 9}
print(f"{'alpha':>6} {'(1-a)^3 S4/(3pi^2)':>19} {'(1-a)^2 S3/(32pi/9)':>20} {'S3/Dine - 1':>12}")
for a in ALPHAS:
    print(f"{a:6.3f} {(1 - a) ** 3 * res[(4, a)]['S'] / tw[4]:19.6f} {(1 - a) ** 2 * res[(3, a)]['S'] / tw[3]:20.6f} "
          f"{res[(3, a)]['S'] / dine(a) - 1:+12.4f}")
dev_dine = max(abs(res[(3, a)]["S"] / dine(a) - 1) for a in ALPHAS if a <= 0.95)
# extrapolate (1 - alpha)^{d-1} S/S_tw = 1 + c1 (1 - alpha) + c2 (1 - alpha)^2 + ... to alpha = 1 (quadratic fit, 0.94 <= alpha <= 0.99)
tw_fit = {}
for d in (3, 4):
    aa_ = np.array([a for a in ALPHAS if a >= 0.94])
    rr_ = np.array([(1 - a) ** (d - 1) * res[(d, a)]["S"] / tw[d] for a in aa_])
    tw_fit[d] = np.polyfit(1 - aa_, rr_, 2)
    print(f"d = {d}: (1 - alpha)^{d - 1} S/S_thin-wall extrapolated to alpha = 1: {tw_fit[d][-1]:.4f} "
          f"(slope {tw_fit[d][-2]:.2f} in 1 - alpha)")
print(f"d = 3: largest |S/(36 x 4.85 f(alpha)) - 1| for alpha <= 0.95: {dev_dine:.4f}")


# %% [markdown]
# ## Higgs reading (illustration, no prefactor): S_B (d = 4) against 4 ln(m_h/H_0)

# %%
sb_cosmo = 4 * math.log(MH / H0)
a_arr = np.array(ALPHAS)
lnS4 = CubicSpline(a_arr, np.log([res[(4, a)]["S"] for a in ALPHAS]))


def s4(a):
    if a < 0.99:
        return float(np.exp(lnS4(a)))
    return tw[4] / (1 - a) ** 3 * (res[(4, 0.99)]["S"] * (1 - 0.99) ** 3 / tw[4])   # thin-wall extrapolation beyond 0.99


def sb_higgs(k3, k4):
    a = k4 / k3 ** 2
    return math.inf if a >= 1 else s4(a) / (G_SM * k3) ** 2


def k3_limit(k4):
    """kappa_3 at which S_B = 4 ln(m_h/H_0); the vacuum is metastable for kappa_3 > sqrt(kappa_4)."""
    lo = math.sqrt(k4) * (1 + 1e-9)
    return brentq(lambda k3: sb_higgs(k3, k4) - sb_cosmo, lo * (1 + 1e-6), 50.0)


print(f"4 ln(m_h/H_0) = {sb_cosmo:.1f}")
for k4 in (0.0, 0.5, 1.0, 2.0, 5.0):
    if k4 == 0:
        k3 = math.sqrt(C_PHI3[4] / sb_cosmo) / G_SM
        print(f"kappa_4 = 0 (phi^3): S_B = 405 at kappa_3 = {k3:.3f} (g/m = {k3 * G_SM:.3f})")
        continue
    k3 = k3_limit(k4)
    print(f"kappa_4 = {k4}: S_B = 4 ln(m_h/H_0) at kappa_3 = {k3:.3f} (alpha = {k4 / k3 ** 2:.3f}); metastable above kappa_3 = {math.sqrt(k4):.3f}")


# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "bounce.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["d", "alpha", "f0", "S", "T", "U", "W_dS_dalpha", "derrick_residual", "xcut", "fcut", "thinwall_ratio", "dine_ratio"])
    for (d, a), r in res.items():
        w.writerow([d, a, r["f0"], r["S"], r["T"], r["U"], r["W"], r["derrick"], r["xcut"], r["fcut"],
                    (1 - a) ** (d - 1) * r["S"] / tw[d], r["S"] / dine(a) if d == 3 else ""])
    w.writerow([])
    w.writerow(["kappa_4", "kappa_3_at_SB_cosmo", "SB_cosmo"])
    for k4 in (0.5, 1.0, 2.0, 5.0):
        w.writerow([k4, k3_limit(k4), sb_cosmo])


# %% [markdown]
# ## Figure: bounce profiles (d = 4), and S(alpha) with the thin-wall limits and Dine et al.

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1), gridspec_kw={"height_ratios": [1, 1.2]})
for a, color, ls in ((0.0, "k", "-"), (0.5, "#5d81b4", "--"), (0.8, "#e09b24", "-."), (0.95, "#eb6235", ":")):
    r = res[(4, a)]
    i = r["icut"]
    ax1.plot(r["sol"].t[:i], -(r["fm"] + r["sol"].y[0][:i]), color=color, lw=0.9, ls=ls, label=rf"$\alpha={a}$")
ax1.set_xlim(0, 40)
ax1.set_ylim(0, 19)
ax1.set_xlabel(r"$x=mr$")
ax1.set_ylabel(r"$-f=-g\phi/m^2$  ($d=4$)")
ax1.legend(loc="upper right")
aa = np.linspace(0, 0.99, 400)
ax2.plot(a_arr, [res[(4, a)]["S"] for a in ALPHAS], color="k", lw=0.9, ls="-", label=r"$d=4$")
ax2.plot(a_arr, [res[(3, a)]["S"] for a in ALPHAS], color="#5d81b4", lw=0.9, ls="--", label=r"$d=3$")
ax2.plot(aa[aa <= 0.95][::16], [dine(a) for a in aa[aa <= 0.95][::16]], "o", ms=3.0, mfc="none", mec="#eb6235",
         label=r"Dine et al., $d=3$")
ax2.plot(aa[aa > 0.5], tw[4] / (1 - aa[aa > 0.5]) ** 3, color="0.55", lw=0.7, ls=":", label="thin wall")
ax2.plot(aa[aa > 0.5], tw[3] / (1 - aa[aa > 0.5]) ** 2, color="0.55", lw=0.7, ls=":")
ax2.set_yscale("log")
ax2.set_xlim(0, 1)
ax2.set_xlabel(r"$\alpha=3\lambda m^2/g^2$")
ax2.set_ylabel(r"$S(\alpha)=S_B\,g^2/m^{6-d}$")
ax2.legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "bounce_alpha.pdf"))
print("wrote results/bounce.csv and figs/bounce_alpha.pdf")
