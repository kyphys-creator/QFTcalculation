# %% [markdown]
# # Step (6): the one-loop RG flow of the abelian Higgs model (e, lambda), Landau poles and the triviality bound
#
# Research note models/abelian_higgs, step (6), Eqs. (rge), (runsol).  With t = ln(mu/MA) (mu = MA = 1 at the benchmark),
# K = (4 pi)^2 and the one-loop equations
#     de^2/dt = 2 e^4/(3K),   dlam/dt = (20 lam^2 - 12 e^2 lam + 6 e^4)/K,   dm^2/dt = m^2 (8 lam - 6 e^2)/K,
# the closed forms are
#     e^2(t) = e0^2/(1 - 2 e0^2 t/(3K))                                        (Landau pole t_e = 3K/(2 e0^2)),
#     (40 lam - 12 e^2)/Delta = tan(Delta t/(2K) + arctan((40 lam0 - 12 e^2)/Delta)),  Delta = sqrt(336) e^2   (e frozen),
# so lam has a Landau pole at t_lam = (2K/Delta)[pi/2 - arctan((40 lam0 - 12 e^2)/Delta)] and, since 20 lam^2 - 12 e^2 lam
# + 6 e^4 > 0 for every lam, never decreases with t; it vanishes only far below the masses, at
# t_0 = (2K/Delta)[arctan(-12 e^2/Delta) - arctan((40 lam0 - 12 e^2)/Delta)].
# The triviality bound: the largest lam(MA), i.e. MH/MA = sqrt(2 lam)/e, for which lam stays finite (or below the
# tree-level unitarity limit 2 pi, step (9)) up to the cutoff Lambda.
# Checks the closed forms against a numerical integration (with e running) and draws ../figs/rgflow.pdf.
# Writes results/rgflow.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rgflow.py

# %%
import csv
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
except NameError:
    HERE = os.getcwd()
K = (4 * math.pi) ** 2
E0, LAM0, M20 = 0.5, 25 / 32, 25 / 8          # benchmark at mu = MA = 1
LAM_U = 2 * math.pi                            # tree-level unitarity limit of lambda (step (9))


def rhs(t, y):
    e2, lam, m2 = y
    return [2 * e2 ** 2 / (3 * K), (20 * lam ** 2 - 12 * e2 * lam + 6 * e2 ** 2) / K, m2 * (8 * lam - 6 * e2) / K]


def delta(e2):
    return math.sqrt(336) * e2


def lam_closed(t, lam0=LAM0, e2=E0 ** 2):
    d = delta(e2)
    return (d * math.tan(d * t / (2 * K) + math.atan((40 * lam0 - 12 * e2) / d)) + 12 * e2) / 40


def t_pole(lam0=LAM0, e2=E0 ** 2, lam_end=math.inf):
    d = delta(e2)
    end = math.pi / 2 if lam_end == math.inf else math.atan((40 * lam_end - 12 * e2) / d)
    return 2 * K / d * (end - math.atan((40 * lam0 - 12 * e2) / d))


# %% [markdown]
# ## Closed forms against the numerical integration

# %%
t_e = 3 * K / (2 * E0 ** 2)
t_lam = t_pole()
t_unit = t_pole(lam_end=LAM_U)
t_zero = 2 * K / delta(E0 ** 2) * (math.atan(-12 * E0 ** 2 / delta(E0 ** 2)) - math.atan((40 * LAM0 - 12 * E0 ** 2) / delta(E0 ** 2)))
print("Landau pole of e: t_e = 3K/(2 e0^2) = %.6f" % t_e)
print("closed form (e frozen): t_lam = %.10f, lam = 2 pi at t = %.10f, lam = 0 at t = %.4f" % (t_lam, t_unit, t_zero))

# numerical integration with e running: stop when lam reaches 2 pi and when it exceeds 1e6
ev_u = lambda t, y: y[1] - LAM_U
ev_u.terminal = False
ev_big = lambda t, y: y[1] - 1e6
ev_big.terminal = True
sol = solve_ivp(rhs, (0, 40), [E0 ** 2, LAM0, M20], rtol=1e-12, atol=1e-14, events=[ev_u, ev_big], dense_output=True)
t_unit_num, t_big = sol.t_events[0][0], sol.t_events[1][0]
print("numerical (e running): lam = 2 pi at t = %.10f (closed form %.10f, diff %.1e); lam = 1e6 at t = %.6f (pole %.6f)"
      % (t_unit_num, t_unit, t_unit_num - t_unit, t_big, t_lam))
down = solve_ivp(rhs, (0, -200), [E0 ** 2, LAM0, M20], rtol=1e-12, atol=1e-14, events=[lambda t, y: y[1]], dense_output=True)
print("numerical (e running): lam = 0 at t = %.4f (closed form %.4f)" % (down.t_events[0][0], t_zero))
for t in (-5.0, 2.0, 8.0):
    y = (sol if t > 0 else down).sol(t)
    print("t = %5.1f: lam numerical %.12f, closed form %.12f, e^2 %.8f (closed %.8f)" % (
        t, y[1], lam_closed(t), y[0], E0 ** 2 / (1 - 2 * E0 ** 2 * t / (3 * K))))

# %% [markdown]
# ## Triviality bound: the largest MH/MA = sqrt(2 lam(MA))/e for which lam stays below lam_end up to Lambda

# %%
def t_reach(l0, lam_end):
    """t at which lam (starting at lam0 = l0 at t = 0, e running) reaches lam_end; lam_end = inf: lam = 1e6 (the pole
    is 2K/(40 lam) ~ 4e-7 further)."""
    target = 1e6 if lam_end == math.inf else lam_end
    ev = lambda t, y: y[1] - target
    ev.terminal = True
    s = solve_ivp(rhs, (0, 1e4), [E0 ** 2, l0, M20], rtol=1e-11, atol=1e-13, events=[ev])
    return s.t_events[0][0]


def mh_max(t_cut, lam_end):
    """largest lam0 with lam(t_cut) = lam_end (numerical, e running); returns MH/MA and lam0."""
    l0 = brentq(lambda l: t_reach(l, lam_end) - t_cut, 1e-3, 0.999 * (LAM_U if lam_end != math.inf else 1e5), xtol=1e-12)
    return math.sqrt(2 * l0) / E0, l0


log_cut = np.linspace(0.25, 8, 32)
bound_pole = [mh_max(lc * math.log(10), math.inf)[0] for lc in log_cut]
bound_unit = [mh_max(lc * math.log(10), LAM_U)[0] for lc in log_cut]
for lc in (1, 2, 4, 8):
    print("Lambda = 10^%d MA: MH/MA < %.4f (lam finite), < %.4f (lam < 2 pi)" % (
        lc, mh_max(lc * math.log(10), math.inf)[0], mh_max(lc * math.log(10), LAM_U)[0]))
with open(os.path.join(HERE, "results", "rgflow.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value"])
    for k, v in (("t_e", t_e), ("t_lam_closed", t_lam), ("t_unit_closed", t_unit), ("t_unit_numerical", t_unit_num),
                 ("t_zero_closed", t_zero), ("t_zero_numerical", down.t_events[0][0])):
        w.writerow([k, "%.12g" % v])
    for lc, a, b in zip(log_cut, bound_pole, bound_unit):
        w.writerow(["MHmax_over_MA_log10Lambda_%.4g_pole_unit" % lc, "%.10g %.10g" % (a, b)])

# %% [markdown]
# ## Figure: lambda and e^2 against t (left), the triviality bound (right)

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
C_LAM, C_E = "C0", "C1"
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))

ts = np.concatenate([np.linspace(-6, 0, 200), np.linspace(0, min(t_big, t_lam) - 1e-3, 400)])
ys = np.array([(sol if t >= 0 else down).sol(t) for t in ts])
ax1.plot(ts, ys[:, 1], color=C_LAM, ls="-", lw=1.5)
ax1.plot(ts, ys[:, 0], color=C_E, ls="--", lw=1.5)
ax1.axhline(LAM_U, color="0.55", lw=0.8, ls=":")
ax1.axvline(t_lam, color="0.55", lw=0.8, ls=":")
ax1.set_ylim(0, 8)
ax1.set_xlim(-6, 13)
ax1.set_xlabel(r"$t=\ln(\mu/M_A)$")
ax1.set_ylabel("coupling")
ax1.text(3.0, 1.55, r"$\lambda(\mu)$", color="k", fontsize=9)
ax1.text(3.0, 0.5, r"$e^2(\mu)$", color="k", fontsize=9)
ax1.text(-5.6, LAM_U + 0.2, r"$\lambda=2\pi$", color="0.35", fontsize=8)
ax1.text(t_lam + 0.3, 7.2, "Landau\npole", color="0.35", fontsize=8, ha="left")
ax1.plot([0], [LAM0], "o", color=C_LAM, ms=4)

ax2.plot(log_cut, bound_pole, color=C_LAM, ls="-", lw=1.5)
ax2.plot(log_cut, bound_unit, color=C_E, ls="--", lw=1.5)
ax2.plot([t_unit / math.log(10)], [math.sqrt(2 * LAM0) / E0], "o", color="k", ms=4)
ax2.set_xlabel(r"$\log_{10}(\Lambda/M_A)$")
ax2.set_ylabel(r"largest $M_h/M_A$")
ax2.set_xlim(0, 8)
ax2.set_ylim(0, 12)
ax2.text(0.85, 7.6, r"$\lambda(\Lambda)<\infty$", color="k", fontsize=9)
ax2.text(0.35, 2.7, r"$\lambda(\Lambda)<2\pi$", color="k", fontsize=9)
ax2.text(t_unit / math.log(10) + 0.2, math.sqrt(2 * LAM0) / E0 - 1.1, "benchmark", color="0.35", fontsize=8)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "rgflow.pdf"))
print("written ../figs/rgflow.pdf, results/rgflow.csv")
