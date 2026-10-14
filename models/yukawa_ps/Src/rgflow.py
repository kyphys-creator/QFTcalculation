# %% [markdown]
# # Step (7): the one-loop RG flow of (y^2, lambda) (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (7), Eq. (9) (eq:rflow), App. rg.  With t = ln mu,
#     d y^2/dt = 10 y^4/(4pi)^2,   d lambda/dt = (3 lambda^2 + 8 lambda y^2 - 48 y^4)/(4pi)^2,
# the coefficients of Eq. (8) as determined in rg_numeric.py.  r = lambda/y^2 obeys dr/dt = y^2 (3r^2 - 2r - 48)/(4pi)^2, so the
# rays lambda = r_pm y^2, r_pm = (1 pm sqrt(145))/3, are flow lines; every other trajectory is
#     r = (r_+ - C Z r_-)/(1 - C Z),   Z = y^(2 sqrt(145)/5)   (one constant C per trajectory):
# towards the infrared (y^2 -> 0) r -> r_+; towards the ultraviolet r -> r_- (C < 0, lambda turns negative) or r -> infinity at
# Z = 1/C (C > 0, a Landau pole of lambda before that of y).  The benchmark y = lambda = 1 at mu = m has C = (1 - r_+)/(1 - r_-).
# Checks the closed form against a numerical integration of the two equations, finds the scale where lambda = 0 and the Landau
# pole of y, and draws ../figs/rgflow.pdf.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rgflow.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
K = (4 * math.pi) ** 2
BY, B3, B8, B48 = 10.0, 3.0, 8.0, -48.0       # d y^2/dt = BY y^4/K, d lambda/dt = (B3 lambda^2 + B8 lambda y^2 + B48 y^4)/K
R_PLUS, R_MINUS = (1 + math.sqrt(145)) / 3, (1 - math.sqrt(145)) / 3
EXP = math.sqrt(145) / 5
R_PLUS, R_MINUS

# %% [markdown]
# ## The benchmark trajectory: closed form against numerical integration, lambda = 0 and the Landau pole

# %%
def closed_form(y2, c):
    z = y2 ** EXP
    return (R_PLUS - c * z * R_MINUS) / (1 - c * z) * y2


def rhs(t, v):
    y2, lam = v
    return [BY * y2 ** 2 / K, (B3 * lam ** 2 + B8 * lam * y2 + B48 * y2 ** 2) / K]


C_BENCH = (1 - R_PLUS) / (1 - R_MINUS)
sol = solve_ivp(rhs, [0, 12], [1.0, 1.0], rtol=1e-12, atol=1e-14, dense_output=True)
ts = np.linspace(0, 12, 25)
dev = max(abs(sol.sol(t)[1] - closed_form(sol.sol(t)[0], C_BENCH)) for t in ts)
t0 = brentq(lambda t: sol.sol(t)[1], 0.1, 12, xtol=1e-14)
t_landau = K / BY
print(f"closed form vs numerical integration along the benchmark (t = 0 ... 12): max |d lambda| = {dev:.1e}")
print(f"benchmark: lambda = 0 at mu = {math.exp(t0):.4f} m (y^2 = {sol.sol(t0)[0]:.4f}); Landau pole of y at mu = {math.exp(t_landau):.3e} m")
# a first estimate of the size of the instability (note Sec. rg, App. rgfit): the action 16 pi^2/|lambda| of the bounce of the
# massless theory with V = lambda phi^4/4!, lambda < 0, evaluated with the running lambda(mu); the real decay rate is step (9), (10)
for mu in (30.0, 100.0, 1000.0):
    y2_mu, lam_mu = sol.sol(math.log(mu))
    print(f"mu = {mu:6.0f} m: y^2 = {y2_mu:.3f}, lambda = {lam_mu:+.3f}, 16 pi^2/|lambda| = {K / abs(lam_mu):.0f}")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, ax = plt.subplots(figsize=(3.4, 2.9))
y2 = np.linspace(1e-4, 4.0, 800)
for c in (-40, -8, -2, -0.3, 0.05, 0.15, 0.4, 1.2):
    lam = closed_form(y2, c)
    ok = (1 - c * y2 ** EXP) > 0.02
    ax.plot(y2[ok], lam[ok], color="0.7", lw=0.6, ls="-")
    i = int(0.55 * np.count_nonzero(ok))                                # an arrow towards the ultraviolet
    if 5 < i < np.count_nonzero(ok) - 5:
        xs, ys = y2[ok], lam[ok]
        ax.annotate("", xy=(xs[i + 3], ys[i + 3]), xytext=(xs[i], ys[i]),
                    arrowprops=dict(arrowstyle="->", color="0.5", lw=0.6))
ax.plot(y2, R_PLUS * y2, color="k", lw=1.0, ls="-", label=r"$\lambda=r_+y^2$")
ax.plot(y2, R_MINUS * y2, color="k", lw=1.0, ls="--", label=r"$\lambda=r_-y^2$")
lam_b = closed_form(y2, C_BENCH)
ax.plot(y2[y2 >= 1], lam_b[y2 >= 1], color="C1", lw=1.4, label=r"benchmark, $\mu\geq m$")
ax.plot(y2[y2 < 1], lam_b[y2 < 1], color="C1", lw=1.4, ls=":")
ax.plot([1.0], [1.0], marker="*", color="C1", ms=8, ls="none")
ax.plot([sol.sol(t0)[0]], [0.0], marker="o", color="C1", ms=4, ls="none")
ax.axhline(0, color="0.6", lw=0.5, zorder=0)
ax.set_xlim(0, 4)
ax.set_ylim(-10, 14)
ax.set_xlabel(r"$y^2$")
ax.set_ylabel(r"$\lambda$")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "rgflow.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
