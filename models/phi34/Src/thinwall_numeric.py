# %% [markdown]
# # Step (11): the thin-wall growth of the one-loop correction, and the scheme without tadpole cancellation
#
# In the note's scheme (MS-bar m, g, lambda; the linear term Y phi cancels the tadpole so that phi = 0 is the exact false
# vacuum) the one-loop correction to the decay exponent grows like the bubble radius R_b (step (10)).  Here (note, App. N):
#  (a) ln D = ln D_N + (1/8) int x^3 f dx, where (1/16) int x^3 f = -V_CW'(0) int phi_B d^4x is the Y counterterm on the bounce
#      and ln D_N is the determinant of the scheme without tadpole cancellation ("N scheme", Dunne-Min's); thin wall:
#      (1 - alpha) ln D/(2 S_4) -> -1/(32 pi^2) (the true vacuum is lowered by 3 m^4/(4pi)^2), while ln D_N/(2 S_4) stays finite.
#  (b) N-scheme parameters: m~^2 = m^2 - g c, g~ = g - lambda c, lambda~ = lambda, c = -V_CW'(0)/m^2 = g/(2 (4pi)^2) at mu = m.
#      The two one-loop rates agree at one loop: S~_B - S_B = -V_CW'(0) int phi_B by the integrated equation of motion
#      int x^3 (f + f^2/2 + alpha f^3/18) = 0; numerically ln Gamma_N - ln Gamma = O(g^2/m^2) at fixed alpha.
#  (c) The one-loop degenerate point of the note's scheme is alpha_deg = 1 + g^2/(6 (4pi)^2 m^2) (alpha~ = 1); checked against
#      the minima of the one-loop effective potential V + V_CW - V_CW(0) - V_CW'(0) phi.
#  (d) The cosmological condition evaluated in the N scheme (parameters converted from the note's), as a scheme uncertainty.
# Input: results/prefactor.csv (step (10)).  Writes results/thinwall.csv and ../figs/thinwall.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python thinwall_numeric.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.interpolate import CubicHermiteSpline, CubicSpline
from scipy.optimize import brentq, minimize_scalar

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K = 16 * math.pi ** 2
MH, VEV, H0 = 125.25, 246.22, 1.44e-42
G_SM, L_SM = 3 * MH / VEV, 3 * MH ** 2 / VEV ** 2

rows = list(csv.reader(open(os.path.join(HERE, "results", "prefactor.csv"))))
hdr = rows[0]
data = [dict(zip(hdr, map(float, r))) for r in rows[1:] if len(r) == len(hdr)]
al = np.array([d["alpha"] for d in data])
col = lambda k: np.array([d[k] for d in data])
S4, W, lnD, I3f, Gms, Rb = col("S4"), col("W"), col("lnD"), col("I3f"), col("Gamma_ms"), col("R")
lnDN = lnD - I3f / 8                                   # determinant of the N scheme (first-order term included)


# %% [markdown]
# ## (a) Decomposition and the thin-wall coefficients

# %%
chk = np.max(np.abs(0.5 * lnDN - (Gms + 2 * np.log(S4 / (18 * math.pi)))))
print(f"(1/2) ln D_N = Gamma_MS + 2 ln(S_4/(18 pi)) (Dunne-Min's quantity): largest difference {chk:.1e}")
rO = 0.5 * lnD / S4                                    # one-loop correction / S_B per unit g^2/m^2, note's scheme
rN = 0.5 * lnDN / S4                                   # the same in the N scheme
sel = al >= 0.9
fitO = np.polyfit(1 - al[sel], (1 - al[sel]) * rO[sel], 2)
fitN = np.polyfit(1 - al[sel], rN[sel], 2)
fitT = np.polyfit(1 - al[sel], (1 - al[sel]) * (I3f[sel] / 16) / S4[sel], 2)
print(f"(1 - alpha) ln D/(2 S_4) -> {fitO[-1]:.6f} at alpha = 1   (prediction -1/(32 pi^2) = {-1 / (32 * math.pi ** 2):.6f})")
print(f"(1 - alpha) (int x^3 f/16)/S_4 -> {fitT[-1]:.6f} at alpha = 1   (thin wall: -(3/2)/16/(3 pi^2) = {-1 / (32 * math.pi ** 2):.6f})")
print(f"ln D_N/(2 S_4) -> {fitN[-1]:.6f} at alpha = 1   (Dunne-Min/Konoplich-Rubin: 0.1678875/(3 pi^2) = {0.1678875 / (3 * math.pi ** 2):.6f})")
for a in (0.0, 0.5, 0.9, 0.97, 0.99):
    i = int(np.argmin(abs(al - a)))
    print(f"  alpha = {al[i]:.2f}: ln D/(2S_4) = {rO[i]:+.5f},  ln D_N/(2S_4) = {rN[i]:+.5f},  R_b = {Rb[i]:.1f}")


# %% [markdown]
# ## (c) The one-loop degenerate point from the effective potential
# In units of m (mu = m), w = V''/m^2 = 1 + f + alpha f^2/6, V_CW = m^4 w^2 (ln|w| - 3/2)/(64 pi^2) (real part).
# Note's scheme: V_eff/(m^6/g^2) = v(f) + (g^2/m^2)/(64 pi^2) [w^2 (ln|w| - 3/2) + 3/2 + 2 f]   (V_CW(0), V_CW'(0) subtracted);
# N scheme (no linear subtraction), in its own parameters: v(f; alpha~) + (g~^2/m~^2)/(64 pi^2) [w^2 (ln|w| - 3/2) + 3/2].

# %%
def veff(f, a, gh2, linear=True):
    w = 1 + f + a * f * f / 6
    v = f * f / 2 + f ** 3 / 6 + a * f ** 4 / 72
    return v + gh2 / (64 * math.pi ** 2) * (w * w * (math.log(abs(w)) - 1.5) + 1.5 + (2 * f if linear else 0.0))


def depth(a, gh2, linear=True):
    """V_eff(second minimum) - V_eff(false minimum), the false minimum found near f = 0."""
    fm = -9 / (2 * a) * (1 + math.sqrt(max(1 - 8 * a / 9, 0.0)))
    r1 = minimize_scalar(lambda f: veff(f, a, gh2, linear), bounds=(fm - 2, fm + 2), method="bounded", options={"xatol": 1e-12})
    r0 = minimize_scalar(lambda f: veff(f, a, gh2, linear), bounds=(-0.5, 0.5), method="bounded", options={"xatol": 1e-12})
    return r1.fun - r0.fun


deg_rows = []
for gh2 in (0.1, 0.5, 1.0, 2.0, 4.0):
    a_deg = brentq(lambda a: depth(a, gh2), 0.98, 1.0 + 0.05 * gh2, xtol=1e-14)
    a_degN = brentq(lambda a: depth(a, gh2, linear=False), 0.98, 1.02, xtol=1e-14)
    pred = 1 + gh2 / (6 * K)
    deg_rows.append((gh2, a_deg, pred, a_degN))
    print(f"g^2/m^2 = {gh2:3.1f}: alpha_deg (note's scheme, from V_eff) = {a_deg:.10f}, 1 + g^2/(6(4pi)^2 m^2) = {pred:.10f} "
          f"(diff {a_deg - pred:+.1e});  N scheme: alpha~_deg - 1 = {a_degN - 1:+.1e}")


# %% [markdown]
# ## (b) The two one-loop rates: agreement at one loop
# For the note's (m = 1, g = gh, lambda = alpha gh^2/3): ln(Gamma/V) = 4 ln m - [S_B - 2 ln(S_B/2pi) + ln D(alpha)/2], S_B = S_4/gh^2.
# N scheme: m~^2 = 1 - gh^2/(2K), g~ = gh (1 - lambda/(2K)), alpha~ = 3 lambda m~^2/g~^2, S~_B = (m~^2/g~^2) S_4(alpha~),
# ln(Gamma/V) = 2 ln m~^2 - [S~_B - 2 ln(S~_B/2pi) + ln D_N(alpha~)/2].
# S_4(alpha) is interpolated with its exact derivative W (Hermite), ln D_N/S_4 with a cubic spline (it is smooth and bounded).

# %%
lnS4h = CubicHermiteSpline(al, np.log(S4), W / S4)
rNs = CubicSpline(al, rN)
rOs = CubicSpline(al, rO)


def lnrate(a, gh, scheme):
    lam = a * gh * gh / 3
    if scheme == "note":
        sb = math.exp(lnS4h(a)) / gh ** 2
        return -(sb - 2 * math.log(sb / (2 * math.pi)) + float(rOs(a)) * math.exp(lnS4h(a)))
    m2 = 1 - gh * gh / (2 * K)
    gt = gh * (1 - lam / (2 * K))
    at = 3 * lam * m2 / gt ** 2
    sb = m2 / gt ** 2 * math.exp(lnS4h(at))
    return 2 * math.log(m2) - (sb - 2 * math.log(sb / (2 * math.pi)) + float(rNs(at)) * math.exp(lnS4h(at)))


eq_rows = []
print(f"{'alpha':>6} " + " ".join(f"{'D/gh^2 (gh=' + str(g) + ')':>18}" for g in (0.05, 0.1, 0.2)))
for a in (0.0, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95):
    vals = [(lnrate(a, g, "N") - lnrate(a, g, "note")) / g ** 2 for g in (0.05, 0.1, 0.2)]
    eq_rows.append((a, *vals))
    print(f"{a:6.2f} " + " ".join(f"{v:18.6f}" for v in vals))
print("ln Gamma_N - ln Gamma_note divided by g^2/m^2 tends to a constant as g -> 0: the two agree at one loop; the constant")
print("(a two-loop-order scheme difference) grows steeply towards the thin wall.")


# %% [markdown]
# ## (d) The cosmological condition in the N scheme (parameters converted from the note's)

# %%
sb_cosmo_note = 4 * math.log(MH / H0)


def cond(k3, k4, scheme):
    """-ln(Gamma/(V H_0^4)): positive when the false vacuum outlives the universe (m = m_h; in the N scheme the prefactor
    m~^4 = m_h^4 (1 - g^2/(2K m^2))^2 is inside lnrate)."""
    return -lnrate(k4 / k3 ** 2, G_SM * k3, scheme) - sb_cosmo_note


def k3_bound(k4, scheme):
    k3s = np.geomspace(8.0, max(math.sqrt(k4 / 0.985), 0.05), 3000)      # g/m < 12.2 keeps m~^2 > 0
    v = [cond(k, k4, scheme) for k in k3s]
    i = next(j for j in range(len(v)) if v[j] > 0)
    return brentq(lambda k: cond(k, k4, scheme), k3s[i], k3s[i - 1])


st_rows = []
for k4 in (0.0, 0.5, 1.0, 2.0, 5.0, 8.0):
    kn, kN = k3_bound(k4, "note"), k3_bound(k4, "N")
    a = k4 / kN ** 2
    st_rows.append((k4, kn, kN))
    print(f"kappa_4 = {k4:3.1f}: kappa_3 < {kn:.4f} (note's scheme), {kN:.4f} (N scheme); relative difference {kN / kn - 1:+.1e}; "
          f"N-scheme one-loop/S_B at the bound {float(rNs(a)) * G_SM ** 2 * kN ** 2:+.4f}")


# %% [markdown]
# ## Output and figure

# %%
with open(os.path.join(HERE, "results", "thinwall.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["alpha", "R_b", "lnD_over_2S4", "lnDN_over_2S4", "I3f_over_16S4"])
    for i in range(len(al)):
        wr.writerow([al[i], Rb[i], rO[i], rN[i], I3f[i] / 16 / S4[i]])
    wr.writerow([])
    wr.writerow(["thin_wall_limit", "value", "prediction"])
    wr.writerow(["(1-alpha) lnD/(2S4)", fitO[-1], -1 / (32 * math.pi ** 2)])
    wr.writerow(["lnD_N/(2S4)", fitN[-1], 0.1678875 / (3 * math.pi ** 2)])
    wr.writerow([])
    wr.writerow(["g2_over_m2", "alpha_deg_Veff", "alpha_deg_formula", "alphatilde_deg_N"])
    wr.writerows(deg_rows)
    wr.writerow([])
    wr.writerow(["alpha", "dlnGamma_over_g2_gh0.05", "gh0.1", "gh0.2"])
    wr.writerows(eq_rows)
    wr.writerow([])
    wr.writerow(["kappa_4", "kappa_3_bound_note", "kappa_3_bound_N"])
    wr.writerows(st_rows)

import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1))
ax1.plot(al, (1 - al) * rO, "o-", ms=2.5, lw=0.8, color="k", label=r"$(1-\alpha)\ln\mathcal{D}/(2S_4)$")
ax1.plot(al, (1 - al) * rN, "s-", ms=2.5, lw=0.8, color="#5d81b4", label=r"$(1-\alpha)\ln\mathcal{D}_N/(2S_4)$")
ax1.plot([1.0], [-1 / (32 * math.pi ** 2)], "*", ms=7, color="#eb6235", clip_on=False, zorder=6, label=r"$-1/(32\pi^2)$")
ax1.axhline(0, color="0.6", lw=0.5)
ax1.set_xlim(0, 1)
ax1.set_xlabel(r"$\alpha$")
ax1.legend(loc="lower left", fontsize=6.5)
ea = np.array([r[0] for r in eq_rows])
for j, (g, mk) in enumerate(((0.05, "o"), (0.1, "s"), (0.2, "^"))):
    ax2.plot(ea, np.abs([r[1 + j] for r in eq_rows]), mk, ms=3.0, mfc="none", lw=0.7, ls="-",
             label=rf"$g/m={g}$")
ax2.set_yscale("log")
ax2.set_xlim(0, 1)
ax2.set_xlabel(r"$\alpha$")
ax2.set_ylabel(r"$|\ln\Gamma_N-\ln\Gamma|/(g^2/m^2)$")
ax2.legend(loc="upper left", fontsize=6.5)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "thinwall.pdf"))
print("wrote results/thinwall.csv and figs/thinwall.pdf")
