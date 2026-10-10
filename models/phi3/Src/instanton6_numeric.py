# %% [markdown]
# # Step (15): decay of the false vacuum in d = 6 (instanton-size integral)
#
# In d = 6 there is no bounce of finite size (step (13)).  The massless equation has the instantons
#   phi_I = -(48/g) rho^2/(rho^2 + r^2)^2,   S_0 = 768 pi^3/(5 g^2) = 12/(5 alpha),   alpha = g^2/(4 pi)^3,
# for every size rho, and the mass term adds (1/2) m^2 int phi_I^2 = 3 m^2 rho^2/alpha.  The rate is an integral over rho
# of the one-instanton density (note, App. S)
#   Gamma/V = int_0^infinity d rho n(rho),
#   n(rho) = 2 D6^{-1/2} (S_0/2pi)^{7/2} rho^-7 exp[-12/(5 alpha(1/rho)) - 3 m^2 rho^2/alpha] [1 + O(alpha, m^2 rho^2)],
# with 7 zero modes (6 translations, norm^2 = S_0 each; 1 dilatation, norm^2 = 4 S_0), one negative mode, and the
# one-loop constant D6 (renormalized det' ratio in MS-bar at mu = 1/rho; not computed here).  Asymptotic freedom,
# 1/alpha(mu) = 1/alpha(m) + (3/2) ln(mu/m), gives exp[-12/(5 alpha(1/rho))] ~ rho^(18/5), which cannot beat rho^-7:
# the integral diverges at small rho like Lambda^(12/5) (cutoff rho > 1/Lambda).  The divergent pieces are polynomial in
# m^2 (Lambda^6 and m^2 Lambda^4 times e^{-12/(5 alpha(Lambda))}); the universal (non-analytic, m^(12/5)) part is finite.
# Checks: the spectrum via the map to S^6 (weighted eigenvalues (L-1)(L+6)/rho^2: one negative mode, seven zero modes),
# the closed form T_l(infinity) = (l-1) l (l+1)/((l+3)(l+4)(l+5)) of the Gel'fand-Yaglom ratios and h1 = -12/(l+2)
# against numerical integration; the zero-mode norms; the counterterms of the note on the instanton
# (S_ct = (9/5) Delta_UV, i.e. the running exponent 18/5); the decomposition of the rho integral.
#
# Writes results/instanton6.csv and ../figs/instanton6_d6.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python instanton6_numeric.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import gamma as Gamma

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
S0G2 = 768 * math.pi ** 3 / 5          # S_0 g^2
K3 = (4 * math.pi) ** 3


def T_closed(l):
    return (l - 1) * l * (l + 1) / ((l + 3) * (l + 4) * (l + 5))


def psi_closed(l, x):
    """Regular zero-energy solution of the l-th radial operator (rho = 1), normalized to x^l at the origin."""
    b = 3 * (l - 1) / (l + 3)
    c = 3 * (l - 1) * l / ((l + 3) * (l + 4))
    return x ** l * (1 + b * x ** 2 + c * x ** 4 + T_closed(l) * x ** 6) / (1 + x ** 2) ** 3


# %% [markdown]
# ## Partial waves of the fluctuation operator around the instanton (rho = 1)
# M = -d^2 + g phi_I = -d^2 - 48/(1 + x^2)^2.  Radial operator in d = 6: -d^2/dx^2 - (5/x) d/dx + l(l+4)/x^2 + V(x);
# the free regular solution is x^l, so T_l = psi_l/x^l obeys T'' + (2l+5)/x T' = V T, T(0) = 1 (integrated in s = ln x
# up to x = 1e5).  Weighted problem: M psi = lambda (4/(1+x^2)^2) psi has zero modes where the potential
# -(48 + 4 lambda)/(1 + x^2)^2 does; on S^6 the eigenvalues are (L-1)(L+6), so c = 48 + 4 lambda = 24, 48, 80 for
# L = 0, 1, 2: at c = 24 the l = 0 wave, at c = 48 the l = 0, 1 waves, at c = 80 the l = 0, 1, 2 waves have T(inf) = 0.

# %%
def gy(l, c=48.0, born=False, xmax=1e5):
    """Gel'fand-Yaglom ratio T_l(infinity) (and the first Born term h1) for V = -c/(1+x^2)^2."""
    V = lambda x: -c / (1 + x * x) ** 2
    x0 = 1e-4
    a = V(0.0) / (4 * (l + 3))
    y0 = [1 + a * x0 ** 2, 2 * a * x0 ** 2]                       # T and dT/ds (s = ln x)
    if born:
        y0 += [a * x0 ** 2, 2 * a * x0 ** 2]

    def rhs(s, y):
        x = math.exp(s)
        out = [y[1], x * x * V(x) * y[0] - (2 * l + 4) * y[1]]
        if born:
            out += [y[3], x * x * V(x) - (2 * l + 4) * y[3]]
        return out
    sol = solve_ivp(rhs, (math.log(x0), math.log(xmax)), y0, method="DOP853", rtol=1e-13, atol=1e-16)
    return sol.y[:, -1]


dT = max(abs(gy(l)[0] - T_closed(l)) for l in range(0, 13))
dh = max(abs(gy(l, born=True)[2] - (-12 / (l + 2))) for l in range(0, 13))
print(f"T_l(inf): numerical vs (l-1)l(l+1)/((l+3)(l+4)(l+5)), l = 0..12: max abs. difference {dT:.1e}")
print(f"h1_l(inf): numerical vs -12/(l+2), l = 0..12: max abs. difference {dh:.1e}")
for c, L in ((24.0, 0), (48.0, 1), (80.0, 2)):
    print(f"  weighted eigenvalue (L-1)(L+6) = {(L - 1) * (L + 6):3d} (c = {c:.0f}): T_l(inf) for l = 0..3 = "
          + ", ".join(f"{gy(l, c)[0]:.2e}" for l in range(4)))
xs = np.linspace(1e-3, 30, 30001)
nodes = [int(np.sum(np.diff(np.sign(psi_closed(l, xs))) != 0)) for l in range(6)]
print(f"zeros of psi_l on (0, 30] for l = 0..5: {nodes}  -> one negative mode (l = 0); psi_0 = (1-x^2)/(1+x^2)^3, "
      f"psi_1 = x/(1+x^2)^3 are the dilatation and translation zero modes")
{l: T_closed(l) for l in range(6)}          # inspect

# %% [markdown]
# ## Zero modes and the counterterms on the instanton
# Translations: ||d_mu phi_I||^2 = (1/6) int (d phi_I)^2 = T/3 = S_0 (Derrick in d = 6: 4T + 6U = 0, S_0 = T/3).
# Dilatation: ||d_rho phi_I||^2 = 4 S_0.  Counterterms of the note (d = 6): delta_Z = -alpha Delta/12,
# delta_g/g = -alpha Delta/2 -> S_ct = delta_Z T + (delta_g/g) U = (3/4) alpha S_0 Delta = (9/5) Delta, so the one-loop
# determinant carries -(18/5) ln(mu rho), and S_0(alpha(mu)) - (18/5) ln(mu rho) = S_0(alpha(1/rho)).
# Mass term: (1/2) m^2 int phi_I^2 = 192 pi^3 m^2 rho^2/g^2 = 3 m^2 rho^2/alpha.

# %%
om6 = math.pi ** 3
phi = lambda r: -48 / (1 + r * r) ** 2                       # g = rho = 1
dphi = lambda r: 192 * r / (1 + r * r) ** 3
drho = lambda r: -48 * 2 * (r * r - 1) / (1 + r * r) ** 3     # d/d rho of -48 rho^2/(rho^2 + r^2)^2 at rho = 1
q = lambda f: quad(f, 0, np.inf, epsabs=0, epsrel=1e-13, limit=200)[0]
T = om6 * q(lambda r: r ** 5 * dphi(r) ** 2 / 2)
U = om6 * q(lambda r: r ** 5 * phi(r) ** 3 / 6)
n_tr = om6 * q(lambda r: r ** 5 * dphi(r) ** 2) / 6
n_dil = om6 * q(lambda r: r ** 5 * drho(r) ** 2)
mass = om6 * q(lambda r: r ** 5 * phi(r) ** 2 / 2)
S0 = T + U
print(f"S_0 g^2 = {S0:.9f} (768 pi^3/5 = {S0G2:.9f});  T = {T / S0:.12f} S_0, U = {U / S0:.12f} S_0")
print(f"zero-mode norms: translations {n_tr / S0:.12f} S_0, dilatation {n_dil / S0:.12f} S_0")
alpha_ = 1.0 / K3                                             # alpha for g = 1
S_ct = (-alpha_ / 12) * T + (-alpha_ / 2) * U
print(f"counterterms on the instanton: S_ct/Delta = {S_ct:.12f} (9/5);  running exponent 2 x 9/5 = 18/5;  "
      f"mass term g^2/(m^2 rho^2) = {mass:.6f} (192 pi^3 = {192 * math.pi ** 3:.6f}) -> 3 m^2 rho^2/alpha")

# %% [markdown]
# ## The instanton-size integral
# With x = m rho and a = alpha(m):  1/alpha(1/rho) = 1/a - (3/2) ln x, so
#   Gamma/V = K m^6 e^{-12/(5a)} int dx x^(-17/5) (alpha(1/rho))^(-7/2) exp(-3x^2/a),   K = 2 D6^{-1/2} (6/(5 pi))^(7/2).
# Fixed alpha (the factor alpha^-7/2 frozen) shows the structure exactly: with b = 3/a,
#   int_{x0}^inf x^(-17/5) e^{-b x^2} dx = (5/12) x0^(-12/5) - (5/2) b x0^(-2/5) + (1/2) Gamma(-6/5) b^(6/5) + O(x0^(8/5)),
# the first two terms polynomial in b ~ m^2/alpha (cutoff Lambda = m/x0), the last the universal part.
# With the running alpha^-7/2 the UV part becomes (5/12) Lambda^6 alpha(Lambda)^(-7/2) e^{-12/(5 alpha(Lambda))}
# x [1 - (35/16) alpha(Lambda) + O(alpha^2)] (one integration by parts).

# %%
mp.mp.dps = 30


def I_fixed(x0, b):
    """int_{x0}^inf x^(-17/5) e^{-b x^2} dx in t = ln x (30 digits), and the same from the incomplete gamma function."""
    t0 = mp.log(x0)
    quad_ = mp.quad(lambda t: mp.exp(-mp.mpf(12) / 5 * t - b * mp.exp(2 * t)), [t0, t0 / 2, 0, mp.log(10 / mp.sqrt(b)) + 1])
    exact = mp.mpf(b) ** (mp.mpf(6) / 5) / 2 * mp.gammainc(-mp.mpf(6) / 5, b * mp.mpf(x0) ** 2)
    return quad_, exact


rows = []
for a in (0.05, 0.1, 0.2):
    b = 3 / a
    univ = 0.5 * Gamma(-6 / 5) * b ** (6 / 5)
    for x0 in (1e-2, 1e-3, 1e-4):
        Iq, Ie = I_fixed(x0, b)
        rest = float(Iq - mp.mpf(5) / 12 * mp.mpf(x0) ** (-mp.mpf(12) / 5) + mp.mpf(5) / 2 * b * mp.mpf(x0) ** (-mp.mpf(2) / 5))
        rows.append((a, x0, float(Iq), rest, univ))
        print(f"a = {a:4.2f}, m rho > {x0:.0e}: integral = {float(Iq):.6e} (incomplete gamma: rel. {float(Iq / Ie - 1):.0e}); "
              f"minus the two cutoff terms = {rest:.6f} vs (1/2) Gamma(-6/5) b^(6/5) = {univ:.6f};  "
              f"cutoff/universal = {(float(Iq) - rest) / univ:.1e}")


def I_run(x0, a):
    """Integral with the running alpha(1/rho)^(-7/2), normalized to a^(-7/2), from x0 to 1 (alpha stays below its pole)."""
    f = lambda t: mp.exp(-mp.mpf(12) / 5 * t) * ((1 / mp.mpf(a) - mp.mpf(3) / 2 * t) * a) ** mp.mpf(3.5) * mp.exp(-3 * mp.exp(2 * t) / a)
    t0 = mp.log(x0)
    return float(mp.quad(f, [t0, t0 / 2, 0]))


print("running coupling: integral x0^(12/5)/[(5/12) (alpha(m/x0)/a)^(-7/2)] -> 1 as x0 -> 0:")
for a in (0.05, 0.1, 0.2):
    vals = []
    for x0 in (1e-3, 1e-5, 1e-7):
        aL_ = 1 / (1 / a - 1.5 * math.log(x0))
        lead = (5 / 12) * x0 ** (-12 / 5) * (aL_ / a) ** -3.5
        vals.append(f"{I_run(x0, a) / lead:.4f} (1 - 35/16 alpha(Lambda) = {1 - 35 / 16 * aL_:.4f})")
    print(f"  a = {a:4.2f}: " + ", ".join(vals) + "   (x0 = 1e-3, 1e-5, 1e-7)")
a, Lam = 0.1, 1e3
aL = 1 / (1 / a + 1.5 * math.log(Lam))
print(f"example a = alpha(m) = {a}, Lambda = {Lam:.0e} m: alpha(Lambda) = {aL:.4f};  UV part / universal part = "
      f"{(5 / 12) * Lam ** 2.4 * (aL / a) ** -3.5 / (0.5 * Gamma(-6 / 5) * (3 / a) ** 1.2):.2e}")

# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "instanton6.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value"])
    for k, v in (("S0_g2", S0), ("T_over_S0", T / S0), ("U_over_S0", U / S0), ("norm_translation_over_S0", n_tr / S0),
                 ("norm_dilatation_over_S0", n_dil / S0), ("S_ct_over_Delta", S_ct), ("max_dT_closed", dT), ("max_dh1", dh)):
        w.writerow([k, v])
    w.writerow([])
    w.writerow(["l", "T_inf_closed", "h1_closed"])
    for l in range(13):
        w.writerow([l, T_closed(l), -12 / (l + 2)])
    w.writerow([])
    w.writerow(["a", "x0", "integral_fixed_alpha", "minus_cutoff_terms", "universal"])
    for r in rows:
        w.writerow(r)

# %% [markdown]
# ## Figure: Gel'fand-Yaglom ratios around the instanton, and the instanton-size distribution

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1), gridspec_kw={"height_ratios": [1, 1.2]})
xx = np.linspace(1e-4, 6.0, 600)
for l, color, ls_ in ((0, "#eb6235", "-"), (1, "k", "--"), (2, "#5d81b4", "-."), (3, "#8cc2a3", ":")):
    ax1.plot(xx, psi_closed(l, xx) / xx ** l, color=color, lw=0.9, ls=ls_, label=f"$l={l}$")
ax1.axhline(0, color="0.6", lw=0.5)
ax1.set_xlim(0, 6)
ax1.set_xlabel(r"$r/\rho$")
ax1.set_ylabel(r"$T_l$")
ax1.legend(loc="upper right", ncol=2)
xr = np.geomspace(1e-4, 1.0, 400)
for a, color, ls_ in ((0.05, "#5d81b4", "-."), (0.1, "k", "-"), (0.2, "#eb6235", "--")):
    y = xr ** (-12 / 5) * ((1 / a - 1.5 * np.log(xr)) * a) ** 3.5 * np.exp(-3 * xr ** 2 / a)
    ax2.plot(xr, y, color=color, lw=0.9, ls=ls_, label=rf"$\alpha(m)={a}$")
ax2.plot(xr[xr < 0.03], 0.3 * xr[xr < 0.03] ** (-12 / 5), color="0.5", lw=0.6, ls=":", label=r"$\propto(m\rho)^{-12/5}$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_ylim(1e-2, 1e11)
ax2.set_xlabel(r"$m\rho$")
ax2.set_ylabel(r"$\rho\,n(\rho)$ (rel.)")
ax2.legend(loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "instanton6_d6.pdf"))
print("wrote results/instanton6.csv and figs/instanton6_d6.pdf")
