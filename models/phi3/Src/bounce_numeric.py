# %% [markdown]
# # Step (13): decay of the false vacuum phi = 0 (bounce action)
#
# The potential V(phi) = m^2 phi^2/2 + g phi^3/6 (note, Eq. (1)) is unbounded below for g phi < 0, so phi = 0 is a false
# vacuum.  Its decay rate per volume is Gamma/V = A exp(-S_B), with S_B the Euclidean action of the O(d)-symmetric bounce
#   phi'' + (d-1)/r phi' = V'(phi),   phi'(0) = 0,   phi(r -> infinity) = 0       (note, App. Q).
# With phi = (m^2/g) f, r = x/m:  f'' + (d-1)/x f' = f + f^2/2, and
#   S_B = Omega_{d-1} (m^{6-d}/g^2) int x^{d-1} dx [f'^2/2 + f^2/2 + f^3/6] = C_d m^{6-d}/g^2,
# Omega_{d-1} = 2 pi^{d/2}/Gamma(d/2).  C_d is found by shooting on f(0) (overshoot/undershoot bisection) for d = 3, 4.
# In d = 6 there is no bounce of finite size: the massless equation f'' + 5 f'/x = f^2/2 has the instantons
# f = -48 b/(1 + b x^2)^2 (b = 1/(m rho)^2, any size rho) with S_0 = (768 pi^3/5)/g^2 = 12/(5 alpha), and the mass term adds
# 192 pi^3 m^2 rho^2/g^2 > 0, so the action is lowest for rho -> 0 (shooting from f(0) -> -infinity never overshoots).
# The d = 6 rate needs the running coupling and the one-loop prefactor (not done); S_0 is checked numerically.
# Checks: Derrick's relation (d - 2) T + d U = 0 for the kinetic (T) and potential (U) parts; stability under the
# tolerance; d = 3 against Dine, Leigh, Huet, Linde, Linde (1992): S_3 = 4.85 M^3/E^2 for V = M^2 phi^2/2 - E phi^3,
# i.e. C_3 = 36 x 4.85 = 174.6 with E = g/6.
# Combined with step (12): S_B (d = 4) at the unitarity and perturbativity limits on g/m, and the g/m for which the
# false vacuum outlives the universe, Gamma V_H t_H < 1, i.e. S_B > 4 ln(m/H_0) up to the prefactor A ~ m^4.
#
# Writes results/bounce.csv and ../figs/bounce_d4.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python bounce_numeric.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
C3_LIT = 36 * 4.85                     # Dine et al. (1992), Eq. (26), converted to E = g/6
GSTEP12 = {"(A) tree unitarity": 9.81, "(B) perturbativity": 8.73, "(C) one-loop unitarity": 7.87}
MH, H0 = 125.25, 1.44e-42              # GeV; H_0 = 67.4 km/s/Mpc in GeV


def vprime(f):
    return f + f * f / 2


def omega(d):
    return 2 * math.pi ** (d / 2) / math.gamma(d / 2)


# %% [markdown]
# ## Shooting
# The particle analogy: x is time, f moves in the inverted potential -V(f) with friction (d-1)/x.  Starting at rest at
# f(0) = f0 < -3 (where V < 0), it must come to rest at the top f = 0 as x -> infinity.  Too far out it overshoots
# (crosses 0), too close to -3 it undershoots (turns back).  The integrals T and U are carried along as extra components.

# %%
def shoot(d, f0, rtol=1e-13, xmax=60.0):
    """Integrate from x0 with the regular series; returns ('over' | 'under', solution)."""
    x0 = 1e-5
    a = vprime(f0) / (2 * d)
    y0 = [f0 + a * x0 ** 2, 2 * a * x0, 0.0, 0.0]
    om = omega(d)

    def rhs(x, y):
        f, fp = y[0], y[1]
        return [fp, vprime(f) - (d - 1) / x * fp, om * x ** (d - 1) * fp * fp / 2, om * x ** (d - 1) * (f * f / 2 + f ** 3 / 6)]

    def cross(x, y):          # f reaches 0: overshoot
        return y[0]
    cross.terminal, cross.direction = True, 1

    def turn(x, y):           # f' changes sign below 0: undershoot
        return y[1]
    turn.terminal, turn.direction = True, -1
    sol = solve_ivp(rhs, (x0, xmax), y0, method="DOP853", rtol=rtol, atol=1e-16, events=(cross, turn), dense_output=False)
    if sol.t_events[0].size:
        return "over", sol
    return "under", sol


def bounce(d, rtol=1e-13):
    lo, hi = -3.0 - 1e-9, None                     # lo: undershoot side (close to -3); hi: overshoot side
    f = -4.0
    while True:                                    # bracket the bounce
        kind, _ = shoot(d, f, rtol)
        if kind == "over":
            hi = f
            break
        lo, f = f, 2 * f
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        kind, _ = shoot(d, mid, rtol)
        if kind == "over":
            hi = mid
        else:
            lo = mid
        if abs(hi - lo) < 4e-16 * abs(mid):
            break
    kind, sol = shoot(d, lo, rtol)                 # the undershooting trajectory follows the bounce longest
    i = int(np.argmin(np.abs(sol.y[0])))           # cut where |f| is smallest, before it turns back
    T, U = sol.y[2][i], sol.y[3][i]
    return dict(d=d, f0=lo, xcut=sol.t[i], fcut=sol.y[0][i], T=T, U=U, S=T + U, derrick=((d - 2) * T + d * U) / T, sol=sol, icut=i)


res = {d: bounce(d) for d in (3, 4)}
for d, r in res.items():
    r2 = bounce(d, rtol=1e-11)
    print(f"d = {d}: f(0) = {r['f0']:.12f},  C_{d} = S_B g^2/m^{6 - d} = {r['S']:.10f}   (2T/d = {2 * r['T'] / d:.10f}; "
          f"Derrick (d-2)T + dU = {r['derrick']:.1e} T; cut at x = {r['xcut']:.1f}, f = {r['fcut']:.1e}; "
          f"rtol 1e-11 -> {abs(r2['S'] / r['S'] - 1):.1e})")
print(f"d = 3 against Dine et al. (1992): C_3 = {res[3]['S']:.3f} vs 36 x 4.85 = {C3_LIT:.1f}  "
      f"(their 4.85 <-> {res[3]['S'] / 36:.4f})")
{d: round(r["S"], 6) for d, r in res.items()}          # inspect: the coefficients C_d

# %% [markdown]
# ## Independent check: the boundary-value problem solved by relaxation (scipy solve_bvp)
# From a rough Gaussian guess; f'(eps) from the regular series, and the decaying tail f' = -(1 + (d-1)/(2L)) f at x = L.

# %%
from scipy.integrate import solve_bvp

bvp = {}
for d, guess0 in ((3, -8.0), (4, -17.0)):
    eps, L = 1e-4, 28.0
    xg = np.linspace(eps, L, 4000)
    yg = np.vstack([guess0 * np.exp(-xg ** 2 / 3), guess0 * np.exp(-xg ** 2 / 3) * (-2 * xg / 3)])
    solb = solve_bvp(lambda x, y: np.vstack([y[1], vprime(y[0]) - (d - 1) / x * y[1]]),
                     lambda ya, yb: np.array([ya[1] - vprime(ya[0]) * eps / d, yb[1] + (1 + (d - 1) / (2 * L)) * yb[0]]),
                     xg, yg, tol=1e-10, max_nodes=200000)
    xs = np.linspace(eps, L, 400001)
    f, fp = solb.sol(xs)
    Tb = omega(d) * np.trapezoid(xs ** (d - 1) * fp ** 2 / 2, xs)
    Ub = omega(d) * np.trapezoid(xs ** (d - 1) * (f ** 2 / 2 + f ** 3 / 6), xs)
    bvp[d] = Tb + Ub
    print(f"d = {d}: relaxation (status {solb.status}): f(0) = {solb.sol(eps)[0]:.8f}, C_{d} = {Tb + Ub:.7f};  "
          f"shooting {res[d]['S']:.7f};  relative difference {abs((Tb + Ub) / res[d]['S'] - 1):.1e}")

# %% [markdown]
# ## d = 4: the bounce action against the unitarity limits of step (12)
# S_B = C_4 m^2/g^2.  For the false vacuum to survive the age of the universe in a Hubble volume, Gamma H_0^-4 < 1 with
# Gamma/V ~ m^4 exp(-S_B) (prefactor only estimated), i.e. S_B > 4 ln(m/H_0); for m = m_h this is about 405.

# %%
C4 = res[4]["S"]
sb_cosmo = 4 * math.log(MH / H0)
print(f"S_B = {C4:.4f} m^2/g^2 (d = 4)")
for name, g in GSTEP12.items():
    print(f"  at {name:24} g/m = {g:5.2f}:  S_B = {C4 / g ** 2:7.3f},  exp(-S_B) = {math.exp(-C4 / g ** 2):.2e}")
for sb in (1.0, 10.0, 100.0, sb_cosmo):
    print(f"  S_B = {sb:7.1f} at g/m = {math.sqrt(C4 / sb):.3f}" + ("   (Gamma H_0^-4 = 1 for m = m_h)" if sb == sb_cosmo else ""))
print(f"  as the Higgs trilinear alone (g/m_h = 3 m_h/v = 1.5261): S_B = {C4 / 1.5261 ** 2:.1f}  "
      "(the SM quartic removes the instability; illustration only)")
# d = 6: the massless instanton, its action against 768 pi^3/5 and the mass-term integral 192 pi^3/b (b = 1 here)
from scipy.integrate import quad as _quad
f6 = lambda x: -48 / (1 + x * x) ** 2
f6p = lambda x: 192 * x / (1 + x * x) ** 3
T6 = math.pi ** 3 * _quad(lambda x: x ** 5 * f6p(x) ** 2 / 2, 0, math.inf, epsabs=0, epsrel=1e-13)[0]
U6 = math.pi ** 3 * _quad(lambda x: x ** 5 * f6(x) ** 3 / 6, 0, math.inf, epsabs=0, epsrel=1e-13)[0]
M6 = math.pi ** 3 * _quad(lambda x: x ** 5 * f6(x) ** 2 / 2, 0, math.inf, epsabs=0, epsrel=1e-13)[0]
C6 = T6 + U6
print(f"d = 6: massless instanton S_0 g^2 = {C6:.9f} vs 768 pi^3/5 = {768 * math.pi ** 3 / 5:.9f};  Derrick 4T + 6U = {(4 * T6 + 6 * U6) / T6:.1e} T;  "
      f"mass term = {M6:.6f} vs 192 pi^3 = {192 * math.pi ** 3:.6f};  S_0 = {C6 / (4 * math.pi) ** 3:.6f}/alpha")

# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "bounce.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["d", "f0", "C_d", "T", "U", "derrick_residual", "xcut", "fcut"])
    for d, r in res.items():
        w.writerow([d, r["f0"], r["S"], r["T"], r["U"], r["derrick"], r["xcut"], r["fcut"]])
    w.writerow([])
    w.writerow(["criterion_step12", "g_over_m", "S_B_d4"])
    for name, g in GSTEP12.items():
        w.writerow([name, g, C4 / g ** 2])
    w.writerow(["S_B = 4 ln(m_h/H0)", math.sqrt(C4 / sb_cosmo), sb_cosmo])

# %% [markdown]
# ## Figure: bounce profiles, and S_B against g/m with the limits of step (12)

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1), gridspec_kw={"height_ratios": [1, 1.2]})
for d, color, ls in ((3, "#5d81b4", "--"), (4, "k", "-")):
    r = res[d]
    i = r["icut"]
    ax1.plot(r["sol"].t[:i], -r["sol"].y[0][:i], color=color, lw=0.9, ls=ls, label=f"$d={d}$")
ax1.axhline(3, color="0.7", lw=0.5, ls=":")
ax1.text(5.6, 3.7, r"$V=0$ at $-f=3$", fontsize=6.5)
ax1.set_xlim(0, 8)
ax1.set_xlabel(r"$x=mr$")
ax1.set_ylabel(r"$-f=-g\phi/m^2$")
ax1.legend(loc="upper right")
gg = np.geomspace(0.3, 20, 300)
ax2.plot(gg, C4 / gg ** 2, color="k", lw=0.9, ls="-")
for (name, g), color in zip(GSTEP12.items(), ("k", "#5d81b4", "#e09b24")):
    ax2.axvline(g, color=color, lw=0.6, ls=":")
ax2.text(7.3, 3.2e3, "step (12)\nlimits", fontsize=6.5, ha="right")
ax2.axhline(sb_cosmo, color="#eb6235", lw=0.7, ls="--")
ax2.text(1.8, sb_cosmo * 1.3, r"$S_B=4\ln(m_h/H_0)$", fontsize=6.5, color="#eb6235")
ax2.axhline(1, color="0.6", lw=0.5, ls="-")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel(r"$g/m$")
ax2.set_ylabel(r"$S_B$ ($d=4$)")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "bounce_d4.pdf"))
print("wrote results/bounce.csv and figs/bounce_d4.pdf")
