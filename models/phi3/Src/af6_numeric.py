# %% [markdown]
# # Step (11): asymptotic freedom in d = 6 phi phi -> phi phi scattering
#
# Asymptotic freedom in d = 6 phi phi -> phi phi scattering (research note, step (11)).
#
# 90-degree scattering, pole mass m = 1.  M1 (MS-bar, note Eq. (22) (eq:M6), g = 1) at mu = m and mu = sqrt(s):
# Package-X with analytic C0, D0 at 30 digits (reference) and LoopTools (results/af6_feyncalc.csv), COLLIER with its two
# branches COLI and DD (results/af6_collier.csv).
# S-matrix element in terms of the pole mass and the MS-bar coupling g(mu) (note, App. L):
#     M_phys = g^2 M0h + g^4 M1h_phys(mu),   M0h = -sum_x 1/(x - 1),   M1h_phys = M1 + conversion (Eq. (23)),
# and the effective coupling measured in 90-degree scattering  alpha_eff(s) = Re M_phys / ((4pi)^3 M0h)  (= alpha at tree
# level).  With alpha = g^2/K, K = (4pi)^3, and the one-loop coefficient  c(s; mu) = K Re M1h_phys / M0h:
#     fixed order:              alpha_FO  = alpha_m + alpha_m^2 c(s; m)
#     RG, coupling only:        alpha_RG1 = alpha(sqrt s) + alpha(sqrt s)^2 c(s; sqrt s)
#     RG, coupling and legs:    alpha_RG2 = [1 - alpha_m B0'(m)] (alpha(sqrt s)/alpha_m)^(2/9) [alpha(sqrt s) + alpha(sqrt s)^2 c_G(s; sqrt s)]
# where alpha(mu) = alpha_m/(1 + (3/2) alpha_m ln(mu/m)) (Eq. (14)), c = c_G + c_R splits off the residue of the external
# legs, c_R(mu) = -B0^(6)'(m^2; mu), whose ln(mu) evolves with 4 gamma_phi (step (10)); 2/9 = 4 (1/12)/(3/2) (note, App. O).
# Checks: c(s; sqrt s) - c(s; m) = (3/2) ln(sqrt s/m) (Eq. (24)); the large-s slope dc(s; m)/d ln sqrt(s) -> -3/2 - 1/3 = -11/6;
# c_G(s; sqrt s) -> constant (no other logarithm of s/m^2).
# Writes results/af6_comparison.csv and ../figs/af6_d6.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python af6_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K = (4 * math.pi) ** 3
ALPHA_M = 0.1                   # alpha(m) = g(m)^2/(4pi)^3 used for the effective couplings


# %% [markdown]
# ## Conversion, tree amplitude and the running coupling

# %%
def b06m(mu):                   # Eq. (23) at m = 1: B0^(6)(m^2) and B0^(6)'(m^2)
    return -17 / 9 + math.pi / (2 * math.sqrt(3)) - 5 / 3 * math.log(mu)


def b06p(mu):
    return 17 / 18 - math.pi / (2 * math.sqrt(3)) + math.log(mu) / 3


def channels(s, t):
    return (s, t, 4 - s - t)


def m0h(s, t):
    return -sum(1 / (x - 1) for x in channels(s, t))


def conversion6(s, t, mu):
    xs = channels(s, t)
    return sum(2 * b06p(mu) / (x - 1) - b06m(mu) / (x - 1) ** 2 for x in xs) / (2 * K)


def alpha_run(mu):
    return ALPHA_M / (1 + 1.5 * ALPHA_M * math.log(mu))


# %% [markdown]
# ## The values (Package-X at 30 digits, LoopTools, COLLIER COLI and DD)

# %%
# ---------------- read ----------------
px, lt = {}, {}
with open(os.path.join(HERE, "results", "af6_feyncalc.csv")) as fh:
    for r in csv.DictReader(fh):
        k, mu_is_1 = int(r["k"]), abs(float(r["mu"]) - 1) < 1e-12
        key = (k, "m" if mu_is_1 else "rs")
        px[key] = (float(r["sqrts"]), float(r["costheta"]), complex(float(r["re_packagex"]), float(r["im_packagex"])))
        if r["re_looptools"] != "nan":
            lt[key] = complex(float(r["re_looptools"]), float(r["im_looptools"]))
co = {1: {}, 2: {}}
with open(os.path.join(HERE, "results", "af6_collier.csv")) as fh:
    for r in csv.DictReader(fh):
        rs, ct = float(r["sqrts"]), float(r["costheta"])
        k = round(40 * math.log(rs / 2.5) / math.log(4000)) if ct == 0 else -1
        key = (k, "m" if abs(float(r["mu"]) - 1) < 1e-12 else "rs")
        co[int(r["mode"])][key] = complex(float(r["re_collier"]), float(r["im_collier"]))


# %% [markdown]
# ## Tools against Package-X

# %%
# ---------------- tools against Package-X (30 digits) ----------------
print("one-loop amplitude against Package-X (analytic C0, D0, 30 digits): relative deviation of Re and Im, max over mu = m, sqrt(s)")
print(f"{'sqrt(s)/m':>11} | {'LoopTools Re':>12} {'Im':>8} | {'COLI Re':>9} {'Im':>8} | {'DD Re':>8} {'Im':>8}")
tool_rows = []
for k in [-1] + list(range(0, 41)):
    rs = px[(k, "m")][0]
    devs = {}
    for name, src in (("lt", lt), ("coli", co[1]), ("dd", co[2])):
        dre = max(abs(src[(k, w)].real - px[(k, w)][2].real) / abs(px[(k, w)][2].real) for w in (("m",) if k == -1 else ("m", "rs")))
        dim = max(abs(src[(k, w)].imag - px[(k, w)][2].imag) / abs(px[(k, w)][2].imag) for w in (("m",) if k == -1 else ("m", "rs")))
        devs[name] = (dre, dim)
    tool_rows.append([k, rs, *devs["lt"], *devs["coli"], *devs["dd"]])
    if k == -1 or k % 4 == 0 or k in (30, 31, 33):
        print(f"{rs:11.4g} | {devs['lt'][0]:12.1e} {devs['lt'][1]:8.1e} | {devs['coli'][0]:9.1e} {devs['coli'][1]:8.1e} | "
              f"{devs['dd'][0]:8.1e} {devs['dd'][1]:8.1e}" + ("   (step (8) point, cos = 0.3)" if k == -1 else ""))
lt_max = max(max(r[2], r[3]) for r in tool_rows)
print(f"LoopTools: largest deviation {lt_max:.1e}")
for name, i in (("COLI", 4), ("DD", 6)):
    bad = [r[1] for r in tool_rows if r[0] >= 0 and max(r[i], r[i + 1]) > 1e-8]
    print(f"COLLIER {name}: deviation > 1e-8 from sqrt(s) = {min(bad):.4g} m on; largest {max(max(r[i], r[i + 1]) for r in tool_rows):.1e}")


# %% [markdown]
# ## One-loop coefficients and their logarithms

# %%
# ---------------- one-loop coefficients (Package-X) ----------------
ks = list(range(0, 65))
rs_arr, c_m, c_rs, cG_rs, cR_rs = [], [], [], [], []
shift_dev, im_dev = 0.0, 0.0
for k in ks:
    rs, ct, m1_m = px[(k, "m")]
    _, _, m1_rs = px[(k, "rs")]
    s = rs * rs
    t = -2 * (s / 4 - 1) * (1 - ct)
    mh = m0h(s, t)
    cm = K * (m1_m.real + conversion6(s, t, 1.0)) / mh
    crs = K * (m1_rs.real + conversion6(s, t, rs)) / mh
    shift_dev = max(shift_dev, abs((crs - cm) - 1.5 * math.log(rs)) / (1.5 * math.log(rs)) if k > 0 else 0.0)
    im_dev = max(im_dev, abs(m1_rs.imag - m1_m.imag) / abs(m1_m.imag))
    rs_arr.append(rs)
    c_m.append(cm)
    c_rs.append(crs)
    cR_rs.append(-b06p(rs))
    cG_rs.append(crs + b06p(rs))
rs_arr, c_m, c_rs, cG_rs, cR_rs = map(np.array, (rs_arr, c_m, c_rs, cG_rs, cR_rs))
lnrs = np.log(rs_arr)
print(f"\nc(s; sqrt s) - c(s; m) = (3/2) ln(sqrt(s)/m) (Eq. (24)): largest relative deviation {shift_dev:.1e};  "
      f"Im M1 independent of mu to {im_dev:.1e}")
slope_m = np.gradient(c_m, lnrs)
slope_G = np.gradient(cG_rs, lnrs)
print("local slopes d c/d ln(sqrt s):  c(s; m) -> -11/6 = -1.8333,   c_G(s; sqrt s) -> 0")
for k in (0, 8, 16, 24, 32, 40, 48, 56, 64):
    print(f"  sqrt(s) = {rs_arr[k]:10.4g} m:  c(s; m) = {c_m[k]:+9.5f}, slope {slope_m[k]:+8.5f};   "
          f"c_G(s; sqrt s) = {cG_rs[k]:+9.5f}, slope {slope_G[k]:+.1e};   c_R(sqrt s) = {cR_rs[k]:+8.5f}")
# the approach to the limit: power corrections in m^2/s
print(f"  c_G(s; sqrt s) at the three largest sqrt(s): {cG_rs[-3]:.10f}, {cG_rs[-2]:.10f}, {cG_rs[-1]:.10f}")


# %% [markdown]
# ## Effective couplings: fixed order and RG-improved (Eq. (30))

# %%
# ---------------- effective couplings ----------------
a_rs = np.array([alpha_run(r) for r in rs_arr])
a_fo = ALPHA_M + ALPHA_M ** 2 * c_m
a_rg1 = a_rs + a_rs ** 2 * c_rs
a_rg2 = (1 - ALPHA_M * b06p(1.0)) * (a_rs / ALPHA_M) ** (2 / 9) * (a_rs + a_rs ** 2 * cG_rs)
zero = None
for i in range(1, len(a_fo)):
    if a_fo[i - 1] > 0 >= a_fo[i]:
        zero = math.exp(np.interp(0, [a_fo[i], a_fo[i - 1]], [lnrs[i], lnrs[i - 1]]))
print(f"\neffective coupling from 90-degree scattering, alpha(m) = {ALPHA_M}:")
for k in (0, 8, 16, 24, 32, 40, 48, 56, 64):
    print(f"  sqrt(s) = {rs_arr[k]:10.4g} m:  alpha_FO/alpha_m = {a_fo[k] / ALPHA_M:+.4f},  alpha_RG1 = {a_rg1[k] / ALPHA_M:.4f},  "
          f"alpha_RG2 = {a_rg2[k] / ALPHA_M:.4f},  alpha(sqrt s) = {a_rs[k] / ALPHA_M:.4f}")
print(f"  the fixed-order alpha_eff vanishes at sqrt(s) = {zero:.3g} m")
# the three agree to O(alpha^2) near threshold; their difference starts at O(alpha^3 ln^2)
print(f"  at sqrt(s) = 2.5 m: |RG2 - FO|/alpha_m = {abs(a_rg2[0] - a_fo[0]) / ALPHA_M:.1e}, |RG1 - FO|/alpha_m = "
      f"{abs(a_rg1[0] - a_fo[0]) / ALPHA_M:.1e}")


# %%
with open(os.path.join(HERE, "results", "af6_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["k", "sqrts", "reldev_re_looptools", "reldev_im_looptools", "reldev_re_coli", "reldev_im_coli",
                "reldev_re_dd", "reldev_im_dd"])
    w.writerows(tool_rows)
    w.writerow([])
    w.writerow(["k", "sqrts", "c_mu_m", "c_mu_sqrts", "cG_mu_sqrts", "cR_mu_sqrts", "alpha_FO", "alpha_RG1", "alpha_RG2",
                "alpha_run", "alpha_m"])
    for k in ks:
        w.writerow([k, rs_arr[k], c_m[k], c_rs[k], cG_rs[k], cR_rs[k], a_fo[k], a_rg1[k], a_rg2[k], a_rs[k], ALPHA_M])


# %% [markdown]
# ## Figure

# %%
# ---------------- figure ----------------
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.3), sharex=True, gridspec_kw={"height_ratios": [1, 1.35]})
asym = cG_rs[-1] + b06p(1.0) - (11 / 6) * lnrs          # c(s; m) -> c_G(inf) - B0'(m) - (11/6) ln sqrt(s)
ax1.plot(rs_arr, c_m, color="k", lw=0.9, ls="-", label=r"$c(s;\mu=m)$")
ax1.plot(rs_arr, asym, color="0.6", lw=0.7, ls=":", label=r"slope $-\frac{11}{6}$")
ax1.plot(rs_arr, cG_rs, color="#5d81b4", lw=0.9, ls="--", label=r"$c_G(s;\mu=\sqrt{s})$")
ax1.set_ylabel(r"one-loop coefficient")
ax1.legend(loc="lower left")
ax2.plot(rs_arr, a_fo / ALPHA_M, color="#5d81b4", lw=0.9, ls="--", label="fixed order")
ax2.plot(rs_arr, a_rg1 / ALPHA_M, color="#e09b24", lw=0.9, ls="-.", label=r"RG, $g$")
ax2.plot(rs_arr, a_rg2 / ALPHA_M, color="k", lw=0.9, ls="-", label=r"RG, $g$ and legs")
ax2.plot(rs_arr, a_rs / ALPHA_M, color="0.6", lw=0.7, ls=":", label=r"$\alpha(\sqrt{s})$")
ax2.axhline(0, color="0.8", lw=0.5, ls="-")
ax2.set_ylabel(r"$\alpha_{\rm eff}/\alpha(m)$")
ax2.set_xlabel(r"$\sqrt{s}/m$")
ax2.set_xscale("log")
ax2.set_ylim(-1.25, 1.25)
ax2.legend(loc="lower left", fontsize=6.5, title=r"$\alpha(m)=%g$" % ALPHA_M, title_fontsize=6.5)
ax1.set_title(r"$d=6$, $\theta=90^\circ$", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(figdir, "af6_d6.pdf"))
print("\nwrote results/af6_comparison.csv and figs/af6_d6.pdf")
