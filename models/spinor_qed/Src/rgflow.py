# %% [markdown]
# # Step (7): the one-loop RG flow of spinor QED (alpha, the masses, the gauge parameter)
#
# Research note models/spinor_qed, step (7), Eqs. (rge), (run), App. rg.  With t = ln(mu/m_e), g = e^2, K = (4 pi)^2, N_f = 2
# (MS-bar is mass independent: both flavours count at every scale), the coefficients of Eq. (rge) as determined in
# rg_numeric.py give
#     dg/dt = b g^2,                b = 8 N_f/(3K)        (2 e beta_e),
#     d ln m_f/dt = -6 g/K          (gamma_m^f/m_f),
#     d ln xi/dt = -b g             (-2 gamma_A),
# with the closed forms  g(t) = g0/(1 - b g0 t),  m_f = m_f0 (g/g0)^(-9/(4 N_f)),  xi g = xi0 g0.  The coupling has a Landau pole at
# t_L = 1/(b g0); there the masses and xi go to 0 (the Landau gauge xi = 0 is a fixed point of the flow).  The benchmark
# e(m_e) = 1 (alpha = 1/(4 pi)) has t_L = 3 pi^2; the physical alpha(m_e) ~ 1/137.036 has t_L ~ 323.
# Checks the closed forms against a numerical integration of the four equations (g, m_e, m_mu, xi) and draws ../figs/rgflow.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rgflow.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

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
NF = 2
B = 8 * NF / (3 * K)                     # dg/dt = B g^2
GM = -6 / K                              # d ln m/dt = GM g
ME, MMU = 1.0, 1.7
G_BENCH = 1.0                            # e(m_e) = 1
G_PHYS = 4 * math.pi / 137.035999084     # alpha(m_e) ~ alpha(0)


def g_cf(t, g0):
    return g0 / (1 - B * g0 * t)


def t_landau(g0):
    return 1 / (B * g0)


def m_cf(t, g0, m0):
    return m0 * (g_cf(t, g0) / g0) ** (GM / B)


def xi_cf(t, g0, xi0):
    return xi0 * g0 / g_cf(t, g0)


print(f"Landau pole: benchmark t_L = {t_landau(G_BENCH):.6f} (3 pi^2 = {3 * math.pi ** 2:.6f}), mu_L/m_e = {math.exp(t_landau(G_BENCH)):.4e};  "
      f"physical alpha: t_L = {t_landau(G_PHYS):.3f}, log10(mu_L/m_e) = {t_landau(G_PHYS) / math.log(10):.1f}")
print(f"mass exponent d ln m/d ln g = gamma_m/(beta_e-part) = {GM / B:.6f} (-9/(4 N_f) = {-9 / (4 * NF):.6f})")

# %% [markdown]
# ## The closed forms against a numerical integration (benchmark, xi(m_e) = 1)

# %%
def rhs(t, y):
    g, me, mmu, xi = y
    return [B * g * g, GM * g * me, GM * g * mmu, -B * g * xi]


T_END = 0.98 * t_landau(G_BENCH)
sol = solve_ivp(rhs, [0, T_END], [G_BENCH, ME, MMU, 1.0], rtol=1e-12, atol=1e-14, dense_output=True)
ts = np.linspace(0, T_END, 50)
num = sol.sol(ts)
cf = np.array([g_cf(ts, G_BENCH), m_cf(ts, G_BENCH, ME), m_cf(ts, G_BENCH, MMU), xi_cf(ts, G_BENCH, 1.0)])
dev = np.max(np.abs(num / cf - 1), axis=1)
print("max relative deviation, numerical integration against the closed forms up to t = 0.98 t_L "
      f"(g = {num[0, -1]:.2f} there): g {dev[0]:.1e}, m_e {dev[1]:.1e}, m_mu {dev[2]:.1e}, xi {dev[3]:.1e}")
print(f"invariants along the numerical solution: max |xi g - 1| = {np.max(np.abs(num[3] * num[0] - 1)):.1e}, "
      f"max |m_mu/m_e - 1.7| = {np.max(np.abs(num[2] / num[1] - MMU)):.1e}")
for tq in (5.0, 10.0, 20.0, 29.0):
    print(f"t = {tq:5.1f} (mu/m_e = {math.exp(tq):.2e}): alpha = {g_cf(tq, G_BENCH) / (4 * math.pi):.5f}, "
          f"m_e = {m_cf(tq, G_BENCH, ME):.5f}, xi/xi0 = {xi_cf(tq, G_BENCH, 1.0):.5f}")

# %% [markdown]
# ## Figure: alpha(mu), the masses and xi, and the flow in the (alpha, xi) plane

# %%
COLORS = {"bench": "#2a78d6", "phys": "#eb6834", "xi": "#1baf7a"}     # validated categorical slots 1-3 (dataviz palette)
fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.5))
tl = t_landau(G_BENCH)
tt = np.linspace(0, tl * (1 - 1e-4), 400)
mus = np.exp(tt)

ax = axes[0]
ax.plot(mus, g_cf(tt, G_BENCH) / (4 * math.pi), color=COLORS["bench"], lw=2, label=r"$e(m_e)=1$")
tp = np.linspace(0, tl, 400)
ax.plot(np.exp(tp), g_cf(tp, G_PHYS) / (4 * math.pi), color=COLORS["phys"], lw=2, ls="--", label=r"$\alpha(m_e)=1/137$")
ax.plot(np.exp(ts[::4]), num[0, ::4] / (4 * math.pi), ls="none", marker="o", ms=4, color=COLORS["bench"], label="numerical")
ax.axvline(math.exp(tl), color="0.5", lw=1, ls=":")
ax.text(math.exp(tl) * 0.6, 3e-3, "Landau pole", rotation=90, ha="right", va="bottom", fontsize=8, color="0.35")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(2e-3, 10)
ax.set_xlabel(r"$\mu/m_e$")
ax.set_ylabel(r"$\alpha(\mu)$")
ax.legend(frameon=False, fontsize=8, loc="upper left")

ax = axes[1]
ax.plot(mus, m_cf(tt, G_BENCH, 1.0), color=COLORS["bench"], lw=2, label=r"$m_f(\mu)/m_f(m_e)$")
ax.plot(mus, xi_cf(tt, G_BENCH, 1.0), color=COLORS["xi"], lw=2, ls="--", label=r"$\xi(\mu)/\xi(m_e)$")
ax.plot(np.exp(ts[::4]), num[1, ::4] / ME, ls="none", marker="o", ms=4, color=COLORS["bench"])
ax.plot(np.exp(ts[::4]), num[3, ::4], ls="none", marker="s", ms=4, color=COLORS["xi"])
ax.axvline(math.exp(tl), color="0.5", lw=1, ls=":")
ax.set_xscale("log")
ax.set_ylim(0, 1.08)
ax.set_xlabel(r"$\mu/m_e$")
ax.set_ylabel(r"ratio to the value at $\mu=m_e$")
ax.set_title(r"$e(m_e)=1$ (marks: numerical)", fontsize=9)
ax.legend(frameon=False, fontsize=8, loc="lower left")

ax = axes[2]
al = np.linspace(0.02, 1.0, 300)
a0 = G_BENCH / (4 * math.pi)
for xi0 in (0.5, 1.0, 2.0, 3.0, 4.0):
    xs = a0 * xi0 / al                                  # xi alpha = const
    ax.plot(al, xs, color="0.55", lw=1)
    i0 = np.searchsorted(al, 0.3)
    ax.annotate("", xy=(al[i0 + 8], xs[i0 + 8]), xytext=(al[i0], xs[i0]),
                arrowprops=dict(arrowstyle="-|>", color="0.35", lw=1))
ax.plot([a0] * 5, [0.5, 1.0, 2.0, 3.0, 4.0], ls="none", marker="o", ms=6, color=COLORS["bench"], label=r"$e(m_e)=1$")
ax.axhline(0, color=COLORS["xi"], lw=2)
ax.text(0.98, -0.12, r"Landau gauge $\xi=0$ (fixed)", ha="right", va="top", fontsize=8, color="0.25")
ax.text(0.55, 2.2, r"$\xi\,\alpha=$ const" + "\n" + r"(arrows: $\mu\to\infty$)", fontsize=8, color="0.25")
ax.set_xlim(0, 1.0)
ax.set_ylim(-0.5, 4.3)
ax.set_xlabel(r"$\alpha(\mu)$")
ax.set_ylabel(r"$\xi(\mu)$")
ax.legend(frameon=False, fontsize=8, loc="upper right")
for ax in axes:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(alpha=0.3, lw=0.5)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "rgflow.pdf"))
print("wrote ../figs/rgflow.pdf")
if INTERACTIVE:
    plt.show()
