# %% [markdown]
# # Step (4): the thermal potential of the phi^3 + phi^4 model from its own loops, and its phase history
#
# Research note models/phi34_thermal, step (4).  One loop at finite temperature (MS-bar at mu = m with the
# tadpole-cancelling linear term of the zero-temperature note):
#   V = V_tree + t phi + V_CW(M^2) + (T^4/2 pi^2) J_B(M^2/T^2),  M^2(phi) = V''(phi) = m^2 + g phi + lambda phi^2/2,
# and its high-temperature expansion with the daisy-resummed zero mode (Pi = lambda T^2/24),
#   V_ht = V_tree + t phi + (T^2/24) M^2 - (T/12 pi) (M^2 + Pi)^(3/2) + (M^4/64 pi^2) [ln(T^2/mu^2) + 2 ln 4 pi - 2 gamma_E].
# Around the inflection point phi_i = -g/lambda, chi = phi - phi_i: M^2 = M^2(phi_i) + lambda chi^2/2 is even in chi and the
# tree potential has no chi^3 term, so V(chi) = h chi + (even in chi) (note, Sec. 3, App. E).  Units: chi in m^2/g
# (chi = f + 3/alpha), tau = g T/m^2, V in m^6/g^2; kappa_4 = 1, g/m = 1.5261 kappa_3 = 1.5261 (kappa_4/alpha)^(1/2).
# Checks: J_B and its high-T expansion (the y^3 coefficient zeta(3)/(384 pi^2) derived in App. E); the odd part of V in the
# phi variables; the leading-order spinodal in closed form; the high-T minimum; high-T expansion vs full one loop.
# Writes results/thermal_single.csv and ../figs/thermal_single.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python thermal_single.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import tptlib as tl

GM1 = 1.5261                                       # g/m at kappa_3 = 1 (zero-temperature note, App. L)
gm_of = lambda al, k4=1.0: GM1 * math.sqrt(k4 / al)
chk = []


# %% [markdown]
# ## (a) J_B and its high-temperature expansion

# %%
print(f"J_B(0) = {tl.jb_quad(0.0):.15f} vs -pi^4/45 = {-math.pi ** 4 / 45:.15f}")
c3 = tl.ZETA3 / (384 * math.pi ** 2)
for y in (0.4, 0.1, 0.025):
    r = (tl.jb_quad(y) - (tl.jb_hight(y) - c3 * y ** 3)) / y ** 3
    print(f"y = {y}: [J_B - (expansion through y^2 ln y)]/y^3 = {r:.6e} vs zeta(3)/(384 pi^2) = {c3:.6e} (rel. {r / c3 - 1:+.1e})")
    chk.append((f"jb_y3_coefficient_y{y}", r, c3))
# Re J_B for y < 0 is the continuation of the analytic part: J_B - (non-analytic) = -pi^4/45 + pi^2 y/12 + (ln a_b/32) y^2 + O(y^3)
for y in (-0.05, -0.01, 0.01, 0.05):
    S = tl.jb_quad(y) - float(tl.jb_nonanalytic(y))
    T2 = -math.pi ** 4 / 45 + math.pi ** 2 * y / 12 + tl.LN_AB / 32 * y * y
    print(f"y = {y:+.2f}: analytic part {S:.12f}, Taylor through y^2 {T2:.12f}, diff/y^3 = {(S - T2) / y ** 3:+.4e}")
print(f"spline vs quadrature: {max(abs(float(tl.jb(y)) - tl.jb_quad(y)) for y in (-25.3, -7.7, -1.3, 0.37, 4.1, 57.1)):.1e}")


# %% [markdown]
# ## (b) The odd part of the one-loop potential, in the original phi variables (m = 1, g = 1.6)

# %%
m, g, al = 1.0, 1.6, 0.9
lam = al * g * g / (3 * m * m)                    # alpha = 3 lambda m^2/g^2
t_lin = m * m * g / (32 * math.pi ** 2)
def V_phi(phi, T):
    M2 = m * m + g * phi + lam * phi * phi / 2
    tree = m * m * phi ** 2 / 2 + g * phi ** 3 / 6 + lam * phi ** 4 / 24 + t_lin * phi
    cw = M2 * M2 / (64 * math.pi ** 2) * (np.log(np.abs(M2) / m ** 2) - 1.5)
    th = T ** 4 / (2 * math.pi ** 2) * tl.jb(M2 / T ** 2)
    Pi = lam * T * T / 24
    dz = -T / (12 * math.pi) * (np.maximum(M2 + Pi, 0) ** 1.5 - np.maximum(M2, 0) ** 1.5)
    return tree + cw + th + dz
phi_i = -g / lam
h_phys = tl.SingleField(al, g / m).h * m ** 4 / g          # h in m^6/g^2 per (m^2/g)
xs = np.linspace(0.05, 4, 9) * m * m / g
for T in (0.5, 2.0, 6.0):
    odd = (V_phi(phi_i + xs, T) - V_phi(phi_i - xs, T)) / 2
    print(f"T = {T} m: max |[V(phi_i + chi) - V(phi_i - chi)]/2 - h chi| / |h chi| = {np.max(np.abs(odd / (h_phys * xs) - 1)):.1e}")
chk.append(("odd_part_rel", float(np.max(np.abs(odd / (h_phys * xs) - 1))), 0.0))


# %% [markdown]
# ## (c) Leading order (tree + T^2 term): the spinodal in closed form; (d) the high-temperature minimum

# %%
print(f"alpha = 9/8: tau_sp closed = {tl.SingleField(9 / 8, gm_of(9 / 8), tadpole=False).tau_spinodal_lo_closed():.1e} "
      f"(the second minimum appears only at T = 0)")
for al_, tad in ((1.0, False), (1.12, False), (0.9, True), (0.5, True)):
    sf = tl.SingleField(al_, gm_of(al_), tadpole=tad)
    tc = sf.tau_spinodal_lo_closed()
    tn = sf.tau_spinodal("lo")
    print(f"alpha = {al_:.4f} (tadpole {tad}): tau_sp closed {tc:.8f}, from the minima {tn:.8f}")
    chk.append((f"lo_spinodal_alpha{al_:.3f}", tn, tc))
sf = tl.SingleField(0.9, gm_of(0.9))
for tau in (25.0, 50.0, 100.0):
    x = sf.minima(tau, "ht")[0][0]
    d = 1e-3
    curv = float(sf.v_ht(d, tau) + sf.v_ht(-d, tau) - 2 * sf.v_ht(0.0, tau)) / d ** 2     # V'' of the even part at chi = 0
    print(f"tau = {tau}: high-T minimum chi = {x:.6e} (f = {x - 3 / 0.9:.6f}), linear response -h/V''_even(0) = {-sf.h / curv:.6e} "
          f"(rel. {x / (-sf.h / curv) - 1:+.1e}), leading order -h/(A0 + alpha tau^2/72) = {-sf.h / (sf.A0 + sf.Pi(tau)):.6e}")


# %% [markdown]
# ## (e) Spinodal temperature: leading order, high-T + daisy, full one loop (kappa_4 = 1)

# %%
alphas = [0.3, 0.4, 0.459, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99, 0.995, 1.0, 1.005, 1.01, 1.02, 1.03, 1.05, 1.08, 1.1, 1.12]
sp = []
for al_ in alphas:
    sf = tl.SingleField(al_, gm_of(al_))
    r = dict(alpha=al_, gm=sf.gm, h=sf.h, lo=sf.tau_spinodal_lo_closed(), ht=sf.tau_spinodal("ht"), full=sf.tau_spinodal("full"))
    x_meta = sorted(sf.minima(r["ht"] * 0.999, "ht"), key=lambda p: p[1])[-1][0]
    r["y_meta"] = sf.gm ** 2 * sf.M2(x_meta) / (0.999 * r["ht"]) ** 2
    r["T_over_m"] = r["ht"] / sf.gm
    sp.append(r)
    print(f"alpha = {al_:.3f} (g/m = {sf.gm:.4f}): tau_sp LO {r['lo']:.5f}, high-T+daisy {r['ht']:.5f}, full {r['full']:.5f} "
          f"(rel. {r['full'] / r['ht'] - 1:+.1e});  T_sp = {r['T_over_m']:.4f} m;  M^2/T^2 at the new minimum {r['y_meta']:.3f}")


# %% [markdown]
# ## Phase history at alpha = 0.9 and 1.05: the global and the metastable minimum while cooling

# %%
taus = np.linspace(12, 0.6, 2281)
traj = {}
for al_ in (0.9, 1.05):
    sf = tl.SingleField(al_, gm_of(al_))
    rows = []
    for tau in taus:
        mins = sf.minima(tau, "ht", n=2001)
        rows.append((tau, mins[0][0], mins[1][0] if len(mins) > 1 else float("nan")))
    rows = np.array(rows)
    jump = np.max(np.abs(np.diff(rows[:, 1])))
    side = -np.sign(sf.h)
    print(f"alpha = {al_}: h = {sf.h:+.5f}; global minimum on the side sign(chi) = {side:+.0f} at every tau: "
          f"{bool(np.all(side * rows[:, 1] > 0))};  largest step of the global minimum {jump:.4f} (d tau = {taus[0] - taus[1]:.4f})")
    traj[al_] = rows


# %% [markdown]
# ## A first-order step only next to exact degeneracy (h = 0): the window in alpha and the step (kappa_4 = 1)

# %%
hfun = lambda al_: tl.SingleField(al_, gm_of(al_)).h
a_deg = brentq(hfun, 0.95, 1.05, xtol=1e-15)
sf0 = tl.SingleField(a_deg, gm_of(a_deg))
Ep = lambda x, tau: sf0.dv_ht(x, tau) - sf0.h               # E'(chi), E = even part of v_ht
curv0 = lambda tau: float(sf0.v_ht(1e-3, tau) + sf0.v_ht(-1e-3, tau) - 2 * sf0.v_ht(0.0, tau)) / 1e-6
tau0 = brentq(curv0, 5.5, 7.0, xtol=1e-13)                 # V''(0) = 0: the symmetric minimum disappears below tau0
xs = np.concatenate([np.geomspace(1e-8, 1e-2, 4000, endpoint=False), np.linspace(1e-2, 1.5, 20000)])


def eprime_extrema(tau):
    """(local max, local min) of E' on chi > 0, if E' rises, falls and rises again (V''(0) > 0)."""
    e = Ep(xs, tau)
    de = np.diff(e)
    imax = [i for i in range(1, len(de)) if de[i - 1] > 0 >= de[i]]
    imin = [i for i in range(1, len(de)) if de[i - 1] < 0 <= de[i]]
    return (e[imax[0]], e[imin[0]]) if imax and imin and imax[0] < imin[0] else None


ext = [(t,) + eprime_extrema(t) for t in np.linspace(tau0, tau0 + 2e-3, 2001) if eprime_extrema(t) is not None]
h_max = max(e[1] for e in ext)                             # two minima on the favoured side iff |h| < E'_max at some tau


def chi_b(tau):
    e = Ep(xs, tau)
    idx = [i for i in range(1, len(e)) if e[i - 1] < 0 <= e[i]]
    x = xs[idx[-1]]
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda y: float(sf0.v_ht(y, tau)), bounds=(x - 0.01, x + 0.01), method="bounded", options={"xatol": 1e-12})
    return r.x, float(r.fun - sf0.v_ht(0.0, tau))


tau_b = max(t for t, emax, emin in ext if emin < 0)        # the broken minimum chi_b exists below tau_b
tau_c = brentq(lambda t: chi_b(t)[1], tau0 + 1e-9, tau_b, xtol=1e-13)
xb = chi_b(tau_c)[0]
dh = (hfun(a_deg + 1e-6) - hfun(a_deg - 1e-6)) / 2e-6
print(f"alpha_deg = {a_deg:.8f} (h = 0; alpha - 1 = {a_deg - 1:.3e} from the tadpole term);  tau_0 = {tau0:.6f} (V''(0) = 0), "
      f"tau_c = {tau_c:.6f}, tau_b = {tau_b:.6f};  step chi_b/tau_c = phi/T = {xb / tau_c:.4f}")
print(f"two minima on the favoured side only for |h| < {h_max:.3e}, i.e. |alpha - alpha_deg| < {h_max / abs(dh):.2e} "
      f"(dh/dalpha = {dh:.4f});  tau range of the structure {ext[0][0]:.6f}-{ext[-1][0]:.6f}")
chk += [("alpha_deg", a_deg, 1.0), ("tau0_deg", tau0, ""), ("tau_c_deg", tau_c, ""), ("tau_b_deg", tau_b, ""), ("step_phi_over_T_deg", xb / tau_c, ""),
        ("h_max", h_max, ""), ("alpha_window", h_max / abs(dh), "")]


# %% [markdown]
# ## Output and figure

# %%
with open(os.path.join(HERE, "results", "thermal_single.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    keys = list(sp[0].keys())
    wr.writerow(keys)
    for r in sp:
        wr.writerow([r[k] for k in keys])
    wr.writerow([])
    wr.writerow(["check", "value", "reference"])
    wr.writerows(chk)

import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax3, ax2) = plt.subplots(3, 1, figsize=(3.25, 5.4), gridspec_kw=dict(height_ratios=[1, 1, 1.3]))
for ax, al_, col in ((ax1, 0.9, "#5d81b4"), (ax3, 1.05, "#eb6235")):
    rows = traj[al_]
    off = 3 / al_                                       # f = chi - 3/alpha
    sfa = tl.SingleField(al_, gm_of(al_))
    ax.plot(rows[:, 0], rows[:, 1] - off, color=col, ls="-", lw=1.0, label="global minimum")
    ax.plot(rows[:, 0], rows[:, 2] - off, color=col, ls="--", lw=0.9, label="metastable minimum")
    ax.axhline(-off, color="0.6", ls=":", lw=0.7)
    above = al_ < 1                                     # the global minimum approaches -3/alpha from below (alpha < 1)
    ax.text(11.8, -off + (0.25 if above else -0.25), r"$f=-3/\alpha$", ha="right", va="bottom" if above else "top",
            fontsize=6, color="0.4")
    ax.set_xlim(0, 12)
    ax.set_ylim(sfa.fminus - 0.8, 0.8)
    ax.set_ylabel(r"$f=g\phi/m^2$")
    ax.text(0.97, 0.06 if al_ < 1 else 0.88, rf"$\alpha={al_}$ ($\kappa_4=1$)", transform=ax.transAxes, ha="right",
            va="bottom" if al_ < 1 else "top", fontsize=7)
ax1.legend(loc="upper right", fontsize=6)
ax3.set_xlabel(r"$\tau=gT/m^2$")
A = np.linspace(0.3, 1.125, 300)
ax2.plot(A, [tl.SingleField(a, gm_of(a), tadpole=False).tau_spinodal_lo_closed() for a in A], color="k", ls="-", lw=0.9,
         label="leading order")
ax2.plot([r["alpha"] for r in sp], [r["ht"] for r in sp], color="#5d81b4", ls="--", lw=0.9, label=r"high $T$ + daisy ($\kappa_4=1$)")
ax2.plot([r["alpha"] for r in sp], [r["full"] for r in sp], "o", ms=3, mfc="none", mec="#5d81b4", label=r"full one loop ($\kappa_4=1$)")
ax2.axvline(1.0, color="0.6", ls=":", lw=0.7)
ax2.axvline(9 / 8, color="0.6", ls=":", lw=0.7)
ax2.text(0.55, 1.5, "two minima", fontsize=6)
ax2.text(0.75, 7.0, "one minimum", fontsize=6)
ax2.set_xlim(0.3, 1.15)
ax2.set_ylim(0, 8)
ax2.set_xlabel(r"$\alpha$")
ax2.set_ylabel(r"$\tau_{\mathrm{sp}}$")
ax2.legend(loc="upper left", fontsize=6)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "thermal_single.pdf"))
print("wrote results/thermal_single.csv and figs/thermal_single.pdf")
