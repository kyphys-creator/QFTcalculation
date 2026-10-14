# %% [markdown]
# # Step (6): the one-loop RG flow of QCD (alpha_s, the heavy-quark mass, the gauge parameter) and Lambda_QCD
#
# Research note models/qcd, step (6), Eqs. (rge), (run), (xirun), App. rg.  With t = ln(mu/m), G = g^2, K = (4 pi)^2, n_f = 6
# (MS-bar is mass independent: the top counts at every scale), the coefficients of Eq. (rge) as read in rg_numeric.py give
#     dG/dt = -2 beta0 G^2/K,            beta0 = 11 - 2 n_f/3 = 7 (SU(3)),
#     d ln m/dt = -6 C_F G/K,            (gamma_m/m)
#     dxi/dt = (C_A G/K) xi (xi_* - xi),  xi_* = 13/3 - 8 T_F n_f/(3 C_A) = 5/3   (-2 gamma_A xi),
# with the closed forms  G = G0/(1 + 2 beta0 G0 t/K),  m = m0 (G/G0)^(3 C_F/beta0),  xi/(xi_* - xi) = [xi0/(xi_* - xi0)] (G/G0)^(-C_A xi_*/(2 beta0)).
# The coupling diverges at Lambda = m exp(-K/(2 beta0 G0)) (1.26e-5 m for the benchmark g(m) = 1); xi = 0 and xi = xi_* are fixed points.
# Physical scales: alpha_s^(5)(M_Z) = 0.118 runs with n_l = 5 (beta0 = 23/3) as alpha_s^(n_l) of Eq. (11) (MadGraph's convention);
# above m_t = 172.5 GeV the MS-bar alpha_s^(6) (equal to alpha_s^(5) at mu = m_t at one loop) runs with beta0 = 7.  MadGraph's
# ALPHAS(Q) (Template/LO/Source/alfas_functions.f, nloop = 1; work/alfas_mg5, built by run_rg_check.sh) is compared for Q >= 5 GeV
# (below m_b = 4.7 GeV MadGraph switches to n_f = 4).
# Checks the closed forms against a numerical integration and draws ../figs/rgflow.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rgflow.py
# Interactive: "Run Cell" (# %%) in VS Code.

# %%
import math
import os
import subprocess
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
CA, CF, TF = 3.0, 4.0 / 3.0, 0.5
NF, NL = 6, 5
B0 = 11 * CA / 3 - 4 * TF * NF / 3          # 7
B0L = 11 * CA / 3 - 4 * TF * NL / 3         # 23/3
XIS = 13 / 3 - 8 * TF * NF / (3 * CA)       # 5/3
G_BENCH = 1.0                               # g(m) = 1, alpha_s = 1/(4 pi)
MZ, MT, ASMZ = 91.188, 172.5, 0.118         # MadGraph's Z mass in alfas_functions.f


def g_cf(t, g0=G_BENCH):
    return g0 / (1 + 2 * B0 * g0 * t / K)


def m_cf(t, g0=G_BENCH, m0=1.0):
    return m0 * (g_cf(t, g0) / g0) ** (3 * CF / B0)


def xi_cf(t, xi0, g0=G_BENCH):
    r = xi0 / (XIS - xi0) * (g_cf(t, g0) / g0) ** (-CA * XIS / (2 * B0))
    return XIS * r / (1 + r)


T_LAMBDA = -K / (2 * B0 * G_BENCH)
print(f"benchmark: Lambda/m = exp({T_LAMBDA:.6f}) = {math.exp(T_LAMBDA):.6e} (exp(-8 pi^2/7) = {math.exp(-8 * math.pi ** 2 / 7):.6e});  "
      f"mass exponent 3 C_F/beta0 = {3 * CF / B0:.6f} (4/7);  xi_* = {XIS:.6f},  xi exponent C_A xi_*/(2 beta0) = {CA * XIS / (2 * B0):.6f} (5/14)")

# %% [markdown]
# ## The closed forms against a numerical integration (benchmark), towards the infrared and the ultraviolet

# %%
def rhs(t, y):
    g, lm, xa, xb, xc = y
    f = lambda x: CA * g / K * x * (XIS - x)
    return [-2 * B0 * g * g / K, -6 * CF * g / K, f(xa), f(xb), f(xc)]


XI0 = (1.0, 3.0, -0.5)
devs = []
for t_end in (0.98 * T_LAMBDA, 40.0):
    if t_end > 0:
        t_lim = t_end
    else:                                     # xi0 = 3 blows up before Lambda: stop at 0.98 of its pole
        tb = next(t for t in np.linspace(0, t_end, 200001) if not (xi_cf(t, 3.0) > 0 and np.isfinite(xi_cf(t, 3.0))))
        t_lim = max(t_end, 0.98 * tb)
    sol = solve_ivp(rhs, [0, t_lim], [G_BENCH, 0.0, *XI0], rtol=1e-12, atol=1e-14, dense_output=True, method="DOP853")
    ts = np.linspace(0, t_lim, 60)
    num = sol.sol(ts)
    cf = np.array([g_cf(ts), np.log(m_cf(ts)), *[xi_cf(ts, x) for x in XI0]])
    d = [np.max(np.abs(num[0] / cf[0] - 1)), np.max(np.abs(np.exp(num[1] - cf[1]) - 1))] + \
        [np.max(np.abs(num[2 + i] / cf[2 + i] - 1)) for i in range(3)]
    devs.append(max(d))
    print(f"t from 0 to {t_lim:+.4f} (mu/m = {math.exp(t_lim):.3e}, alpha_s = {g_cf(t_lim) / (4 * math.pi):.4f}): max relative deviation "
          f"g^2 {d[0]:.1e}, m {d[1]:.1e}, xi(0) = 1, 3, -0.5: {d[2]:.1e}, {d[3]:.1e}, {d[4]:.1e}")
tb3 = math.log(abs(3.0 / (XIS - 3.0))) * (2 * B0) / (CA * XIS)      # (G/G0) at which xi(0) = 3 blows up: r = -1
print(f"xi(m) = 3 > xi_*: xi -> infinity where (g/g0)^2 = {math.exp(tb3):.4f}, i.e. alpha_s = {G_BENCH * math.exp(tb3) / (4 * math.pi):.4f}; "
      f"xi(m) = -0.5 < 0: xi -> -infinity towards the UV where (g/g0)^2 = {abs(-0.5 / (XIS + 0.5)) ** (2 * B0 / (CA * XIS)):.4f}")

# %% [markdown]
# ## Physical alpha_s: n_l = 5 below m_t (MadGraph), n_f = 6 above; Lambda

# %%
def a5(q):
    return ASMZ / (1 + B0L / (2 * math.pi) * ASMZ * math.log(q / MZ))


def a6(q):
    return 1 / (1 / a5(MT) + B0 / (2 * math.pi) * math.log(q / MT))


L5 = MZ * math.exp(-2 * math.pi / (B0L * ASMZ))
L6 = MT * math.exp(-2 * math.pi / (B0 * a5(MT)))
print(f"alpha_s^(5)(m_t) = {a5(MT):.6f};  one-loop Lambda^(5) = {1e3 * L5:.3f} MeV,  Lambda^(6) = {1e3 * L6:.3f} MeV,  "
      f"m_t (Lambda^(5)/m_t)^(beta0^(5)/beta0^(6)) = {1e3 * MT * (L5 / MT) ** (B0L / B0):.3f} MeV")
mt_ms = MT / (1 + 4 * a5(MT) / (3 * math.pi))
print(f"MS-bar m_t(m_t) from the pole mass {MT} GeV (Eq. (11) at mu = m): {mt_ms:.3f} GeV;  m_t(1 TeV) = "
      f"{mt_ms * (a6(1000.0) / a5(MT)) ** (3 * CF / B0):.3f} GeV")
qs = np.geomspace(5.0, 1000.0, 41)
exe = os.path.join(HERE, "work", "alfas_mg5")
mg = None
if os.path.exists(exe):
    out = subprocess.run([exe], input="".join(f"{q:.17e}\n" for q in qs), capture_output=True, text=True, check=True).stdout
    mg = np.array([[float(x) for x in line.split()] for line in out.split("\n") if line.strip()])
    dev = np.max(np.abs(mg[:, 1] / np.array([a5(q) for q in mg[:, 0]]) - 1))
    print(f"MadGraph ALPHAS (nloop = 1) against alpha_s^(5) of Eq. (run), {len(mg)} scales 5 GeV - 1 TeV: max relative deviation {dev:.1e}")
else:
    print("work/alfas_mg5 not built (run_rg_check.sh builds it)")

# %% [markdown]
# ## Figure: physical alpha_s; the benchmark alpha_s, m and xi; the flow in the (alpha_s, xi) plane

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))

ax = axes[0]
q5 = np.geomspace(1.0, MT, 200)
q6 = np.geomspace(MT, 1e4, 200)
ax.plot(q5, [a5(q) for q in q5], color="C0", lw=1, ls="-", label=r"$\alpha_s^{(5)}$")
ax.plot(q6, [a5(q) for q in q6], color="C0", lw=0.8, ls=":")
ax.plot(q6, [a6(q) for q in q6], color="C1", lw=1, ls="--", label=r"$\alpha_s^{(6)}$ ($\overline{\rm MS}$)")
if mg is not None:
    ax.plot(mg[::5, 0], mg[::5, 1], ls="none", marker="o", ms=2.6, color="C0", label="MadGraph")
ax.axvline(MT, color="0.5", lw=0.5, ls=":")
ax.text(MT * 1.15, 0.065, r"$m_t$", fontsize=7, color="0.35")
ax.set_xscale("log")
ax.set_ylim(0.06, 0.32)
ax.set_xlabel(r"$\mu$ [GeV]")
ax.set_ylabel(r"$\alpha_s(\mu)$")
ax.set_title(r"$\alpha_s^{(5)}(M_Z)=0.118$, one loop", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper right")

ax = axes[1]
tt = np.linspace(0.995 * T_LAMBDA, 20, 600)
mus = np.exp(tt)
ax.plot(mus, g_cf(tt) / (4 * math.pi), color="C0", lw=1, ls="-", label=r"$\alpha_s(\mu)$")
ax.plot(mus, m_cf(tt), color="C1", lw=1, ls="--", label=r"$m(\mu)/m$")
ax.plot(mus, xi_cf(tt, 1.0), color="C2", lw=1, ls="-.", label=r"$\xi(\mu)$, $\xi(m)=1$")
ax.axvline(math.exp(T_LAMBDA), color="0.5", lw=0.5, ls=":")
ax.text(math.exp(T_LAMBDA) * 1.6, 1.75, r"$\Lambda$", fontsize=7, color="0.35")
ax.axhline(XIS, color="C2", lw=0.5, ls=":")
ax.text(1e7, XIS + 0.05, r"$\xi_*$", fontsize=7, color="0.35")
ax.set_xscale("log")
ax.set_ylim(0, 2.0)
ax.set_xlabel(r"$\mu/m$")
ax.set_title(r"benchmark $g(m)=1$, $n_f=6$", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper right")

ax = axes[2]
a0 = G_BENCH / (4 * math.pi)
for xi0 in (-0.5, 0.5, 1.0, 2.5, 3.0):
    al = np.linspace(0.005, 1.0, 600)
    gg = al / a0
    r = xi0 / (XIS - xi0) * gg ** (-CA * XIS / (2 * B0))
    xs = np.where(np.abs(1 + r) > 1e-3, XIS * r / (1 + r), np.nan)
    ok = (np.sign(xs) == np.sign(xi0)) & (np.abs(xs) < 6)
    ax.plot(al[ok], xs[ok], color="0.55", lw=0.6)
    i0 = int(np.argmin(np.abs(al - 0.06)))
    if ok[i0] and ok[i0 - 20]:
        ax.annotate("", xy=(al[i0 - 20], xs[i0 - 20]), xytext=(al[i0], xs[i0]), arrowprops=dict(arrowstyle="-|>", color="0.35", lw=0.5))
ax.plot([a0] * 5, [-0.5, 0.5, 1.0, 2.5, 3.0], ls="none", marker="o", ms=3.2, color="C0", label=r"$\mu=m$")
ax.axhline(0, color="C2", lw=1)
ax.axhline(XIS, color="C1", lw=1, ls="--")
ax.text(0.006, 0.08, r"Landau gauge $\xi=0$", ha="left", va="bottom", fontsize=7, color="0.25")
ax.text(0.98, XIS + 0.08, r"$\xi_*=5/3$", ha="right", va="bottom", fontsize=7, color="0.25")
ax.set_xscale("log")
ax.set_xlim(0.005, 1.0)
ax.set_ylim(-2.0, 4.5)
ax.set_xlabel(r"$\alpha_s(\mu)$")
ax.set_ylabel(r"$\xi(\mu)$")
ax.set_title(r"arrows: $\mu\to\infty$", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper left")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "rgflow.pdf"))
print("wrote ../figs/rgflow.pdf")
if INTERACTIVE:
    plt.show()
