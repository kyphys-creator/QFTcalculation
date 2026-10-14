# %% [markdown]
# # Step (9): RG-improved effective potential and the lambda < 0 bounce (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (9), Eqs. (vrg), (bounce), App. bounce.  m = 1, M = 0.7, y = lambda = 1 (MS-bar at mu = m).
# 1. One-loop running of (y^2, lambda, m^2, M) (Eq. (8)), checked against the closed forms y^2(t), r(t) (Eq. (9)), M ~ y^(-1/5) and
#    the field rescaling xi(t) = exp(-int gamma_phi dt) = (y^2(t)/y^2(0))^(-1/5).
# 2. RG-improved effective potential: the solution of [mu d_mu + beta d_g - gamma_phi phi d_phi] V = 0 is
#        V(phi; g, m) = V_CW(xi(t) phi; g(t), m e^t),
#    with V_CW the one-loop potential Eq. (10) (eq:cw).  Delta V(phi) = V(phi) - V(0) at the same t (the vacuum energy and the
#    constants cancel).  Scale choices: m e^t = kappa phi (kappa = 1/2, 1, 2) and m e^t = M_psi(phi) = (M^2 + y^2 xi^2 phi^2)^(1/2)
#    at the running couplings.  lambda_eff(phi) = 24 Delta V/phi^4; the field phi_I where Delta V turns negative, against the scale
#    mu_0 = 19.49 m where lambda(mu) = 0.  Fixed order (t = 0) for comparison.
# 3. Bounce: for constant lambda < 0 and m = 0 the O(4) solution phi = sqrt(48/|lambda|) R/(r^2 + R^2) with S = 16 pi^2/|lambda|
#    for every R (App. rgfit), checked by integrating the radial equation from r = 0 and the action numerically.  With m^2 > 0 there
#    is no stationary bounce in d = 4 (Derrick's scaling: S = T/2 and V2 = 0 would be needed); the Fubini profile then costs
#    delta S = (m^2/2) int phi_R^2 = (24 pi^2 m^2 R^2/|lambda|)[ln(L^2/R^2) - 1 + ...] with the tail cut at L ~ 1/m.
#    RG improvement: S(R) = 16 pi^2/|lambda(kappa/R)|, kappa = 1/2 ... 2.  S decreases monotonically towards small R up to the
#    Landau pole of y, so there is no minimum: the decay is dominated by the shortest scale where the theory is used.
# Writes results/bounce.csv and ../figs/bounce_d4.pdf.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python bounce_numeric.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.integrate import quad, solve_ivp
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
Y0, LAM0, M2PHI0, MPSI0 = 1.0, 1.0, 1.0, 0.7
R_PLUS, R_MINUS = (1 + math.sqrt(145)) / 3, (1 - math.sqrt(145)) / 3
T_LANDAU = K / (10 * Y0 ** 2)

# %% [markdown]
# ## One-loop running and the closed forms

# %%
def rge(t, v):
    y2, lam, m2, M = v
    return [10 * y2 ** 2 / K, (3 * lam ** 2 + 8 * lam * y2 - 48 * y2 ** 2) / K,
            (lam * m2 + 4 * y2 * m2 - 8 * y2 * M ** 2) / K, -y2 * M / K]


T_MAX = 0.98 * T_LANDAU
run = solve_ivp(rge, [0, T_MAX], [Y0 ** 2, LAM0, M2PHI0, MPSI0], rtol=1e-12, atol=1e-14, dense_output=True)


def couplings(t):
    y2, lam, m2, M = run.sol(t)
    xi = (y2 / Y0 ** 2) ** (-0.2)                    # exp(-int_0^t gamma_phi), gamma_phi = 2 y^2/(4 pi)^2
    return y2, lam, m2, M, xi


def closed(t):
    z = 1 / (1 - 10 * Y0 ** 2 * t / K)
    c = (LAM0 / Y0 ** 2 - R_PLUS) / (LAM0 / Y0 ** 2 - R_MINUS)
    zz = c * z ** (math.sqrt(145) / 5)
    return Y0 ** 2 * z, (R_PLUS - zz * R_MINUS) / (1 - zz) * Y0 ** 2 * z, MPSI0 * z ** (-0.1)


dev_run = max(max(abs(a - b) / abs(b) for a, b in zip(run.sol(t)[[0, 1, 3]], closed(t)) if abs(b) > 1e-3)
              for t in np.linspace(0, 12, 49) if abs(closed(t)[1]) > 1e-3)
gam_check = []
for t in (1.0, 5.0, 10.0):                           # xi(t) against the numerical integral of gamma_phi
    integ = quad(lambda s: 2 * run.sol(s)[0] / K, 0, t, epsabs=1e-14, epsrel=1e-13)[0]
    gam_check.append(abs(math.exp(-integ) - couplings(t)[4]))
t0 = brentq(lambda t: run.sol(t)[1], 0.1, 10, xtol=1e-14)
print(f"running vs closed forms (y^2, lambda, M; t <= 12): max rel. dev. {dev_run:.1e};  xi = (y^2/y0^2)^(-1/5) vs exp(-int gamma_phi):"
      f" {max(gam_check):.1e};  lambda(mu) = 0 at mu = {math.exp(t0):.4f} m, Landau pole of y at {math.exp(T_LANDAU):.3e} m")

# %% [markdown]
# ## The RG-improved effective potential

# %%
def v_cw(phi, y2, lam, m2, M, mu2):
    """Eq. (10) without the vacuum energy; Re of the logarithm for m_phi^2 < 0"""
    mp2, Mp2 = m2 + lam * phi ** 2 / 2, M ** 2 + y2 * phi ** 2
    f = lambda x: 0.0 if x == 0 else x * x * (math.log(abs(x) / mu2) - 1.5)
    return m2 * phi ** 2 / 2 + lam * phi ** 4 / 24 + (f(mp2) - 4 * f(Mp2)) / (64 * math.pi ** 2)


def delta_v(phi, choice, kappa=1.0):
    """V(phi) - V(0) in the RG-improved form; choice 'phi' (mu = kappa phi), 'Mpsi' (mu = M_psi(phi)), 'fixed' (mu = m)"""
    if choice == "fixed":
        t = 0.0
    elif choice == "phi":
        t = math.log(kappa * phi) if kappa * phi > 1 else 0.0
    else:                                             # mu = M_psi(xi phi) at the running couplings: solve for t
        g = lambda t: t - 0.5 * math.log(couplings(t)[3] ** 2 + couplings(t)[0] * (couplings(t)[4] * phi) ** 2)
        t = brentq(g, -5, T_MAX) if g(0) < 0 else 0.0
        t = max(t, 0.0)
    y2, lam, m2, M, xi = couplings(t)
    mu2 = math.exp(2 * t)
    return v_cw(xi * phi, y2, lam, m2, M, mu2) - v_cw(0.0, y2, lam, m2, M, mu2)


PHIS = np.geomspace(1.0, 1e5, 401)
CHOICES = [("phi", 0.5), ("phi", 1.0), ("phi", 2.0), ("Mpsi", 1.0)]
lam_eff = {c: np.array([24 * delta_v(p, *c) / p ** 4 for p in PHIS]) for c in CHOICES}
lam_eff[("fixed", 1.0)] = np.array([24 * delta_v(p, "fixed") / p ** 4 for p in PHIS])
phi_I = {}
for c in CHOICES:
    i = np.argmax(lam_eff[c] < 0)
    phi_I[c] = brentq(lambda p: delta_v(p, *c), PHIS[i - 1], PHIS[i], xtol=1e-12)
print("field where the RG-improved Delta V turns negative (lambda(mu) = 0 at mu = 19.49 m):",
      {f"{c[0]}{'' if c[0] == 'Mpsi' else ', kappa=' + str(c[1])}": round(v, 2) for c, v in phi_I.items()})
lam_eff[("phi", 1.0)][::80]          # inspect

# %%
# RG invariance: the potential does not depend on the choice of t up to higher orders; the spread of lambda_eff between the
# choices against the size of the one-loop term, and the fixed-order potential against the RG-improved one at large phi
for p in (5.0, 30.0, 300.0, 3000.0):
    j = int(np.argmin(abs(PHIS - p)))
    vals = [lam_eff[c][j] for c in CHOICES]
    y2 = couplings(math.log(p))[0]
    print(f"phi = {PHIS[j]:8.1f} m: lambda_eff = {lam_eff[('phi', 1.0)][j]:+.4f} (mu = phi), spread over the choices {max(vals) - min(vals):.3f},"
          f" one-loop size 24*4 y^4/(64 pi^2) = {24 * 4 * y2 ** 2 / (64 * math.pi ** 2):.3f};  fixed order (mu = m): {lam_eff[('fixed', 1.0)][j]:+.3f}")

# %% [markdown]
# ## The bounce: Fubini solution (constant lambda < 0, m = 0), the mass term, and S(R) with the running lambda

# %%
def radial(lam_abs, m2, phi0, r_max):
    """integrate phi'' + 3 phi'/r = V'(phi) = m^2 phi - (|lambda|/6) phi^3 from r = 0 (series start)"""
    r0 = 1e-6 / phi0
    a2 = (m2 * phi0 - lam_abs / 6 * phi0 ** 3) / 8          # phi = phi0 + a2 r^2 + ...
    f = lambda r, v: [v[1], m2 * v[0] - lam_abs / 6 * v[0] ** 3 - 3 * v[1] / r]
    return solve_ivp(f, [r0, r_max], [phi0 + a2 * r0 ** 2, 2 * a2 * r0], rtol=1e-12, atol=1e-14, dense_output=True)


dev_fub = 0.0
for lam_abs, R in ((1.0, 1.0), (0.3, 0.01), (5.0, 3.0)):
    phi0 = math.sqrt(48 / lam_abs) / R
    sol = radial(lam_abs, 0.0, phi0, 50 * R)
    for r in np.linspace(0.1 * R, 40 * R, 9):
        dev_fub = max(dev_fub, abs(sol.sol(r)[0] / (math.sqrt(48 / lam_abs) * R / (r * r + R * R)) - 1))
action_fub = []
for lam_abs, R in ((1.0, 1.0), (0.3, 0.01), (5.0, 3.0)):
    A = math.sqrt(48 / lam_abs)
    phi = lambda r: A * R / (r * r + R * R)
    dphi = lambda r: -2 * A * R * r / (r * r + R * R) ** 2
    S = 2 * math.pi ** 2 * quad(lambda r: r ** 3 * (0.5 * dphi(r) ** 2 - lam_abs / 24 * phi(r) ** 4), 0, np.inf, epsabs=0, epsrel=1e-13, limit=400)[0]
    action_fub.append(abs(S * lam_abs / (16 * math.pi ** 2) - 1))
print(f"Fubini: radial equation from r = 0 against the closed form {dev_fub:.1e}; action against 16 pi^2/|lambda| {max(action_fub):.1e}")

# the mass term on the Fubini profile: delta S(L) = (m^2/2) int_0^L phi_R^2 against the closed form, for m R << 1
lam_abs, R, m2 = 1.0, 1e-2, 1.0
A = math.sqrt(48 / lam_abs)
for L in (1.0, 3.0):
    num = 0.5 * m2 * 2 * math.pi ** 2 * quad(lambda r: r ** 3 * (A * R / (r * r + R * R)) ** 2, 0, L, epsrel=1e-13)[0]
    cf = 24 * math.pi ** 2 * m2 * R ** 2 / lam_abs * (math.log((L * L + R * R) / (R * R)) + R * R / (L * L + R * R) - 1)
    print(f"mass term on the Fubini profile, m R = {R}, tail cut at L = {L}/m: delta S = {num:.6e} (closed form {cf:.6e}),"
          f" relative to 16 pi^2/|lambda|: {num / (16 * math.pi ** 2 / lam_abs):.2e}")

# %%
def s_of_R(inv_R, kappa):
    t = math.log(kappa * inv_R)
    lam = couplings(t)[1]
    return 16 * math.pi ** 2 / abs(lam) if lam < 0 else math.inf


INV_R = np.geomspace(25.0, math.exp(T_MAX) / 2, 300)
S_band = {k: np.array([s_of_R(x, k) for x in INV_R]) for k in (0.5, 1.0, 2.0)}
print("S(R) = 16 pi^2/|lambda(kappa/R)| (kappa = 1/2, 1, 2):")
rows = []
for x in (30.0, 100.0, 1e3, 1e4, 1e5, 1e6):
    vals = [s_of_R(x, k) for k in (0.5, 1.0, 2.0)]
    y2, lam = couplings(math.log(x))[:2]
    print(f"  1/R = {x:8.0e} m: S = {vals[1]:8.1f}  (kappa band {min(vals):.1f} - {max(vals):.1f});  lambda = {lam:+.3f}, y^2/(4pi)^2 = {y2 / K:.4f},"
          f" |lambda|/(4pi)^2 = {abs(lam) / K:.4f}, m^2 R^2 = {1 / x ** 2:.1e}")
    rows.append([x, lam, y2, vals[1], min(vals), max(vals)])
mono = all(np.diff(S_band[1.0][np.isfinite(S_band[1.0])]) < 0)
print(f"S(R) decreases monotonically towards small R over 1/R = 25 m ... {INV_R[-1]:.2e} m: {mono}")

with open(os.path.join(HERE, "results", "bounce.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["inv_R_over_m", "lambda", "y2", "S_kappa1", "S_min_band", "S_max_band"])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["choice", "kappa", "phi_I_over_m"])
    for c, v in phi_I.items():
        w.writerow([c[0], c[1], v])
print("wrote results/bounce.csv")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.9))
mus = np.geomspace(1.0, 1e5, 400)
ax.plot(mus, [couplings(math.log(x))[1] for x in mus], color="k", ls="-", lw=1.0, label=r"$\lambda(\mu)$")
styles = {("phi", 0.5): ("C0", ":"), ("phi", 1.0): ("C0", "-"), ("phi", 2.0): ("C0", "--"), ("Mpsi", 1.0): ("C1", "-.")}
labels = {("phi", 0.5): r"$\lambda_{\rm eff}$, $\mu=\phi/2$", ("phi", 1.0): r"$\lambda_{\rm eff}$, $\mu=\phi$",
          ("phi", 2.0): r"$\lambda_{\rm eff}$, $\mu=2\phi$", ("Mpsi", 1.0): r"$\lambda_{\rm eff}$, $\mu=M_\psi(\phi)$"}
for c in CHOICES:
    ax.plot(PHIS, lam_eff[c], color=styles[c][0], ls=styles[c][1], lw=1.0, label=labels[c])
ax.plot(PHIS, lam_eff[("fixed", 1.0)], color="0.5", ls="-", lw=0.6, label=r"fixed order, $\mu=m$")
ax.axhline(0, color="0.6", lw=0.5, zorder=0)
ax.set_xscale("log")
ax.set_ylim(-8, 3)
ax.set_xlabel(r"$\phi/m$ or $\mu/m$")
ax.set_ylabel(r"$\lambda$, $\lambda_{\rm eff}=24\,\Delta V/\phi^4$")
ax.legend(fontsize=6.5, loc="lower left")
ax2.fill_between(INV_R, np.minimum(S_band[0.5], S_band[2.0]), np.maximum(S_band[0.5], S_band[2.0]), color="C1", alpha=0.25, lw=0)
ax2.plot(INV_R, S_band[1.0], color="C1", ls="-", label=r"$16\pi^2/|\lambda(1/R)|$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel(r"$1/(mR)$")
ax2.set_ylabel(r"$S$")
ax2.legend(fontsize=7)
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "bounce_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
