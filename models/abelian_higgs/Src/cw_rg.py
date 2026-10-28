# %% [markdown]
# # Step (8): the Coleman-Weinberg minimum with CosmoTransitions and with the renormalization group
#
# Research note models/abelian_higgs, step (8).  m^2 = 0, K = (4 pi)^2, one-loop Landau-gauge potential
#     V = lam phi^4/4 + (1/(4K)) sum_i n_i m_i^4 (ln(m_i^2/mu^2) - c_i),  m_i^2 = k_i phi^2,
#     (k, n, c) = (3 lam, 1, 3/2), (lam, 1, 3/2), (e^2, 3, 5/6),
# which is exactly (phi^4/4)[Lambda + beta ln phi^2] with beta = sum n k^2/K, Lambda = lam + sum n k^2 (ln(k/mu^2) - c)/K,
# minimum ln v^2 = -Lambda/beta - 1/2 and MH^2/MA^2 = 2 beta/e^2.
# (a) CosmoTransitions 2.0.7 (generic_potential.V1, MS-bar) with the field-dependent masses of this note (Landau and
#     background R_xi, e = 1/2, lam = e^4/K, mu = 1) against results/cw_points.csv (cw.wl) and the minimum of cw.wl;
# (b) renormalization-group improvement: (e0 = 1/2, lam0) at mu0 = 1, tau0 = K lam0/(6 e0^4) = 0 ... 12.  Fixed order:
#     the one-loop potential at mu0 (leading order: ln(e0 v) = 1/6 - tau0).  RG-improved: e^2, lam, the field (Landau
#     gamma = -3 e^2/K) run with the one-loop RGEs to the scale mu* = e(mu*) v(mu*) where the one-loop potential is
#     minimized (no large logarithm), v converted back to the mu0 normalization; also mu = 2 mu*, mu*/2;
# (c) figure ../figs/cw.pdf: left, the one-loop MH^2/MA^2 against 3 e^2/(8 pi^2) in five gauges (results/cw_ratio.csv);
#     right, ln(e0 v) against tau0, fixed order and RG-improved.
# Writes results/cw_rg.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python cw_rg.py

# %%
import csv
import math
import os
import sys
import warnings

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

np.product = np.prod                               # numpy 2: removed alias used by cosmoTransitions.helper_functions
warnings.filterwarnings("ignore")
INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
from importlib.metadata import version
import cosmoTransitions
from cosmoTransitions import generic_potential

K = (4 * math.pi) ** 2
E0 = 0.5
print(f"CosmoTransitions {version('cosmoTransitions')} at {os.path.dirname(cosmoTransitions.__file__)}")


# %% [markdown]
# ## (a) CosmoTransitions

# %%
class CWModel(generic_potential.generic_potential):
    """m^2 = 0 abelian Higgs model; xi = None: Landau gauge, otherwise background R_xi."""

    def init(self, e, lam, xi=None, mu=1.0):
        self.Ndim = 1
        self.renormScaleSq = mu ** 2
        self.e, self.lam, self.xi = e, lam, xi

    def V0(self, X):
        phi = np.asanyarray(X)[..., 0]
        return self.lam * phi ** 4 / 4

    def boson_massSq(self, X, T):
        phi2 = np.asanyarray(X)[..., 0] ** 2
        e2, lam = self.e ** 2, self.lam
        if self.xi is None:
            m2 = np.stack([3 * lam * phi2, lam * phi2, e2 * phi2], axis=-1)
            return m2, np.array([1, 1, 3]), np.array([1.5, 1.5, 5 / 6])
        x = self.xi * e2 * phi2
        m2 = np.stack([3 * lam * phi2, lam * phi2 + x, x, e2 * phi2], axis=-1)
        return m2, np.array([1, 1, -1, 3]), np.array([1.5, 1.5, 1.5, 5 / 6])

    def fermion_massSq(self, X):
        phi = np.asanyarray(X)[..., 0]
        return np.zeros(phi.shape + (0,)), np.zeros(0)

    def V(self, phi):
        X = np.array([phi], dtype=float)
        return float(self.V0(X) + self.V1(self.boson_massSq(X, 0.0), self.fermion_massSq(X)))


lam_b = E0 ** 4 / K
models = {("Landau", 0): CWModel(E0, lam_b), ("background R_xi", 1): CWModel(E0, lam_b, xi=1.0)}
with open(os.path.join(HERE, "results", "cw_points.csv")) as fh:
    pts = list(csv.reader(fh))[1:]
dmax = 0.0
for g, xv, phi, val in pts:
    if g == "min":
        continue
    key = (g, int(float(xv)))
    if key not in models:
        continue
    d = abs(models[key].V(float(phi)) - float(val)) / abs(float(val))
    dmax = max(dmax, d)
print("(a) CosmoTransitions V0 + V1 against cw.wl at 7 points (Landau, background R_xi xi = 1): max relative difference %.1e"
      % dmax)
vmin_wl, curv_wl = [float(r[2]) for r in pts if r[0] == "min"][0], [float(r[3]) for r in pts if r[0] == "min"][0]
m = models[("Landau", 0)]
res = minimize_scalar(m.V, bracket=(1.0, 2.0, 3.0), tol=1e-12)
h = 1e-4
curv_ct = (m.V(res.x + h) - 2 * m.V(res.x) + m.V(res.x - h)) / h ** 2
print("(a) minimum (Landau, e = 1/2): CosmoTransitions potential %.10f, cw.wl %.10f;  V'' %.8f vs %.8f"
      % (res.x, vmin_wl, curv_ct, curv_wl))


# %% [markdown]
# ## (b) Renormalization-group improvement

# %%
def lam_beta(e2, lam, mu):
    """Lambda and beta of the exact log form of the Landau one-loop potential at scale mu."""
    ks = np.array([3 * lam, lam, e2]); ns = np.array([1, 1, 3]); cs = np.array([1.5, 1.5, 5 / 6])
    beta = np.sum(ns * ks ** 2) / K
    nz = ks != 0                                                         # k^2 ln k -> 0 for lam = 0
    Lam = lam + np.sum(ns[nz] * ks[nz] ** 2 * (np.log(np.abs(ks[nz]) / mu ** 2) - cs[nz])) / K
    return Lam, beta


def vmin(e2, lam, mu):
    Lam, beta = lam_beta(e2, lam, mu)
    return math.exp(0.5 * (-Lam / beta - 0.5)), 2 * beta / e2          # v, MH^2/MA^2


def rhs(t, y):
    e2, lam, lz = y
    return [2 * e2 ** 2 / (3 * K), (20 * lam ** 2 - 12 * e2 * lam + 6 * e2 ** 2) / K, 3 * e2 / K]


def rg_improved(lam0, shift=0.0):
    """run to mu* with ln(e^2 v^2/mu*^2) = 2 shift (shift = 0: mu* = MA); returns ln(e0 v) in the mu0 normalization,
    MH^2/MA^2 and t*."""
    y3 = solve_ivp(rhs, (0, 3), [E0 ** 2, lam0, 0.0], rtol=1e-12, atol=1e-15).y[:, -1]     # the inputs are at t = 0
    sol = solve_ivp(rhs, (3, -40), y3, rtol=1e-12, atol=1e-15, dense_output=True)

    def g(t):
        e2, lam, lz = sol.sol(t)
        v, _ = vmin(e2, lam, math.exp(t))
        return math.log(e2 * v ** 2) - 2 * t - 2 * shift
    ts = np.linspace(2.5, -39.5, 421)
    gs = [g(t) for t in ts]
    i = next(i for i in range(len(ts) - 1) if gs[i] * gs[i + 1] < 0)
    tstar = brentq(g, ts[i + 1], ts[i], xtol=1e-14)
    e2, lam, lz = sol.sol(tstar)
    v, ratio = vmin(e2, lam, math.exp(tstar))
    return math.log(E0 * v) - lz, ratio, tstar, e2, lam


rows = []
for tau0 in np.arange(0, 12.01, 0.5):
    lam0 = 6 * E0 ** 4 * tau0 / K
    v_fo, r_fo = vmin(E0 ** 2, lam0, 1.0)
    lv_rg, r_rg, tstar, e2s, lams = rg_improved(lam0)
    lv_up = rg_improved(lam0, shift=-math.log(2))[0]          # mu = 2 MA
    lv_dn = rg_improved(lam0, shift=math.log(2))[0]           # mu = MA/2
    exact = 6 * e2s / K * (1 + 10 * lams ** 2 / (3 * e2s ** 2))   # Eq. (cwratio) with the couplings at mu*
    rows.append([tau0, lam0, 1 / 6 - tau0, math.log(E0 * v_fo), lv_rg, lv_up, lv_dn, r_fo, r_rg, tstar, e2s / E0 ** 2,
                 r_rg / exact - 1, lams * K / e2s ** 2])
for r in rows[::4]:
    print("(b) tau0 = %4.1f: ln(e0 v) leading order %8.4f, fixed order %8.4f, RG-improved %8.4f (mu = 2 MA, MA/2: %+.1e, %+.1e);"
          "  MH^2/MA^2 x 8 pi^2/(3 e0^2) fixed %.6f, RG %.6f;  t* = %.3f, e(mu*)^2/e0^2 = %.6f, K lam(mu*)/e^4 = %.6f,"
          " RG ratio against Eq. (cwratio) at mu*: %.1e" % (
              r[0], r[2], r[3], r[4], r[5] - r[4], r[6] - r[4], r[7] / (6 * E0 ** 2 / K), r[8] / (6 * E0 ** 2 / K),
              r[9], r[10], r[12], r[11]))
with open(os.path.join(HERE, "results", "cw_rg.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["tau0", "lam0", "lnev_LO", "lnev_fixed", "lnev_RG", "lnev_RG_2MA", "lnev_RG_halfMA", "ratio_fixed",
                "ratio_RG", "tstar", "e2star_over_e02", "ratio_RG_minus_formula", "K_lamstar_over_e4"])
    for r in rows:
        w.writerow(["%.12g" % x for x in r])


# %% [markdown]
# ## (c) Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
with open(os.path.join(HERE, "results", "cw_ratio.csv")) as fh:
    rr = list(csv.DictReader(fh))
styles = {("Landau", "0"): ("k", "o", "Landau"), ("background R_xi", "1."): ("C0", "s", None),
          ("background R_xi", "3."): ("C0", "D", None), ("Fermi", "1."): ("C1", "s", None), ("Fermi", "3."): ("C1", "D", None)}
es = np.logspace(math.log10(1 / 40), math.log10(0.6), 100)
for (g, xv), (col, mk, _) in styles.items():
    sel = [r for r in rr if r["gauge"] == g and r["xi"] == xv]
    x = [float(r["e"]) for r in sel]
    y = [float(r["dev_K_over_e2"]) for r in sel]
    ax1.semilogx(x, y, mk, color=col, ls="none", ms=4, mfc="none" if mk == "D" else col)
    s = {"Landau": 0, "background R_xi": 1, "Fermi": -1}[g]
    xi = float(xv)
    lam = es ** 4 / K
    ax1.semilogx(es, (10 * lam ** 2 + 2 * s * xi * es ** 2 * lam) / (3 * es ** 4) * K / es ** 2, color=col, ls="-", lw=0.8)
ax1.axhline(0, color="0.55", lw=0.6)
ax1.set_xlabel(r"$e$")
ax1.set_xticks([1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2])
ax1.set_xticklabels([r"$\frac{1}{32}$", r"$\frac{1}{16}$", r"$\frac{1}{8}$", r"$\frac{1}{4}$", r"$\frac{1}{2}$"])
ax1.xaxis.set_minor_formatter(plt.NullFormatter())
ax1.set_ylabel(r"$(K/e^2)\,[(M_h^2/M_A^2)/(3e^2/8\pi^2)-1]$")
ax1.set_ylim(-2.4, 2.4)
ax1.text(0.033, 2.12, r"background $R_\xi$, $\xi=3$", fontsize=8)
ax1.text(0.033, 0.79, r"background $R_\xi$, $\xi=1$", fontsize=8)
ax1.text(0.033, 0.12, "Landau", fontsize=8)
ax1.text(0.033, -0.55, r"Fermi, $\xi=1$", fontsize=8)
ax1.text(0.033, -1.88, r"Fermi, $\xi=3$", fontsize=8)

a = np.array(rows)
ax2.plot(a[:, 0], a[:, 4], color="C0", lw=1.5, ls="-", label=r"RG-improved ($\mu=M_A$)")
ax2.plot(a[:, 0], a[:, 3], color="C1", lw=1.5, ls="--", label=r"fixed order ($\mu=\mu_0$)")
ax2.plot(a[:, 0], a[:, 2], color="0.4", lw=1.0, ls=":", label=r"leading order, $1/6-\tau_0$")
ax2.legend(loc="lower left", fontsize=8)
ax2.set_xlabel(r"$\tau_0=K\lambda_0/(6e_0^4)$")
ax2.set_ylabel(r"$\ln(e_0v)$")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "cw.pdf"))
print("written ../figs/cw.pdf, results/cw_rg.csv")
