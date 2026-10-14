# %% [markdown]
# # Step (7): the RG coefficients from the mu-dependence of the 1PI functions, the pole masses and the S-matrix element
#
# Research note models/spinor_qed, step (7), Eqs. (rge), (run), (os), App. rg.  e = 1, m_e = 1, m_mu = 1.7 at mu = 1.
# At fixed parameters an MS-bar quantity is linear in ln mu^2 at one loop; its slope mu d/dmu is fixed by the RG equation
# of the quantity (K = (4 pi)^2, e^2/K units, N_f = 2):
#   1PI (two-point functions):  K Pi_f^R: -8/3 per flavour (-2 gamma_A summed);  K Sigma_V^R: -2 xi (-2 gamma_psi);
#                               K Sigma_S^R: 2 (3 + xi) (2 gamma_psi - gamma_m/m);
#   pole mass:                  K (Sigma_V + Sigma_S)(m^2): 6 for every xi (-gamma_m/m: m_pole = m(mu)[1 + Sigma_V + Sigma_S]
#                               does not run);
#   residue:                    K (R_f - 1): -6 for every xi, with the IR pole -(3 - xi): slope - 2 x IR pole = -2 xi = -2 gamma_psi;
#   S-matrix element:           K W of e+ e- -> mu+ mu- (MS-bar charge, pole masses): d(K W)/d ln mu^2 = P - (8/3) B(4), P the IR
#                               pole (every pole carries mu^(2 eps)); with beta_e = (8/3) e^3/K:  beta_e = (e^3/K)(Re P - slope)/B(4).
#                               With the charge alpha(0) (MadLoop a0, Eq. (Wos)) the UV part is absent: slope = Re P.
# Slopes from mu = 1/2 and 2: [X(2) - X(1/2)]/(2 ln 2) per ln mu (1PI) and /(2 ln 4) per ln mu^2 (K W); X(1) must be the mean.
# Tools: Package-X and LoopTools (rg_feyncalc.wl -> results/rg_feyncalc_onepi.csv, results/rg_feyncalc.csv), COLLIER
# (work/rg_collier -> results/rg_collier_onepi.csv, results/rg_collier_amp.csv), MadLoop (work/ml_MS, work/ml_a0 of step (5),
# mu_R = mu).  Figure: at sqrt(s) = 6, t = -8 the IR-finite combination K W - P ln mu^2 (the virtual part with the soft factor's
# mu-dependence, i.e. the IR log removed) relative to the Born, sigma-like quantity Y = e^4 [1 + e^2 2 Re(K W - P ln mu^2)/(K B)],
# for mu = 1/4 ... 4 with e = 1 fixed and with e(mu) of Eq. (run); and the electron pole mass with m fixed and with m(mu).
# Writes results/rg_comparison.csv and ../figs/rg_running.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python rg_numeric.py` (from Src/; run_rg_check.sh builds the helpers).
# Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import re
import subprocess
import sys

import numpy as np

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
ME, MMU, NF = 1.0, 1.7, 2
KK = (4 * math.pi) ** 2
MUS = (0.5, 1.0, 2.0)
POINTS = [(16.0, -6.0), (16.0, -3.0), (16.0, -1.0), (36.0, -20.0), (36.0, -8.0), (36.0, -1.0),
          (100.0, -70.0), (100.0, -30.0), (100.0, -5.0)]                 # the nine points of step (4)
FIG_PT = (36.0, -8.0)
FIG_MUS = np.geomspace(0.25, 4.0, 33)
BETA_E = 4 * NF / 3 / KK                 # beta_e/e^3
GAMMA_A = 4 * NF / 3                     # e^2/K units
GAMMA_M = -6.0                           # gamma_m/m in e^2/K units


def born4(s, t):
    u = 2 * ME ** 2 + 2 * MMU ** 2 - s - t
    sig = ME ** 2 + MMU ** 2
    return 8 / s ** 2 * ((t - sig) ** 2 + (u - sig) ** 2 + 2 * s * sig)


# %% [markdown]
# ## COLLIER: the 1PI brackets and K W at the nine points (and the figure's scan)

# %%
with open(os.path.join(HERE, "work", "rg_points.txt"), "w") as fh:
    for s, t in POINTS:
        for mu in MUS:
            fh.write(f"{s:.17g} {t:.17g} {mu:.17g}\n")
    for mu in FIG_MUS:
        fh.write(f"{FIG_PT[0]:.17g} {FIG_PT[1]:.17g} {mu:.17g}\n")
subprocess.run(["./rg_collier", "../results/rg_collier_onepi.csv", "rg_points.txt", "../results/rg_collier_amp.csv"],
               cwd=os.path.join(HERE, "work"), check=True, capture_output=True)


def read_csv(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


def cz(r, k):
    return complex(float(r["re_" + k]), float(r["im_" + k]))


# 1PI: {(func, arg, xi, tool): {mu: (pole, fin)}}
ONEPI = {}
for r in read_csv("rg_collier_onepi.csv"):
    key = (r["func"], round(float(r["arg"]), 6), round(float(r["xi"]), 6), "COLLIER")
    ONEPI.setdefault(key, {})[round(float(r["mu"]), 6)] = (cz(r, "pole"), cz(r, "fin"))
for r in read_csv("rg_feyncalc_onepi.csv"):
    for tool, tag in (("Package-X", "px"), ("LoopTools", "lt")):
        key = (r["func"], round(float(r["arg"]), 6), round(float(r["xi"]), 6), tool)
        ONEPI.setdefault(key, {})[round(float(r["mu"]), 6)] = (cz(r, "pole_" + tag), cz(r, "fin_" + tag))
# K W: {(s, t, tool): {mu: (born4, pole, fin)}}
AMP = {}
for r in read_csv("rg_collier_amp.csv"):
    AMP.setdefault((float(r["s"]), float(r["t"]), "COLLIER"), {})[float(r["mu"])] = (float(r["born4"]), cz(r, "pole"), cz(r, "fin"))
for r in read_csv("rg_feyncalc.csv"):
    AMP.setdefault((float(r["s"]), float(r["t"]), "LoopTools"), {})[float(r["mu"])] = (float(r["born4"]), cz(r, "pole"), cz(r, "fin"))
len(ONEPI), len(AMP)                     # inspect


# %% [markdown]
# ## MadLoop (step (5) programs, mu_R = mu): finite = Re W/2, 1eps = Re P/(2K) (four-dimensional spin sums; Eq. (17), eq:scheme is a
# ## mu-independent shift, so the slopes are those of CDR)

# %%
def momenta(s, t):
    e = math.sqrt(s) / 2
    p, k = math.sqrt(e * e - ME ** 2), math.sqrt(e * e - MMU ** 2)
    c = (t - ME ** 2 - MMU ** 2 + 2 * e * e) / (2 * p * k)
    st = math.sqrt(1 - c * c)
    return [(e, 0, 0, p), (e, 0, 0, -p), (e, k * st, 0, k * c), (e, -k * st, 0, -k * c)]


def run_madloop(scheme, s, t, mu):
    base = os.path.join(HERE, "work", f"ml_{scheme}", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta(s, t))
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps")}


for scheme, tool in (("MS", "MadLoop"), ("a0", "MadLoop alpha(0)")):
    pts = [(s, t, mu) for s, t in POINTS for mu in MUS] + ([(FIG_PT[0], FIG_PT[1], mu) for mu in (0.25, 4.0)] if scheme == "a0" else [])
    for s, t, mu in pts:
        v = run_madloop(scheme, s, t, mu)
        AMP.setdefault((s, t, tool), {})[mu] = (4 * v["born"], complex(2 * KK * v["1eps"]), complex(2 * KK * v["finite"]))
AMP[(36.0, -8.0, "MadLoop")]             # inspect


# %% [markdown]
# ## 1PI slopes, pole masses, residues

# %%
EXPECT = {"Pi_e": lambda xi: -8 / 3, "Pi_mu": lambda xi: -8 / 3, "SigV_e": lambda xi: -2 * xi, "SigV_mu": lambda xi: -2 * xi,
          "SigS_e": lambda xi: 2 * (3 + xi), "SigS_mu": lambda xi: 2 * (3 + xi), "Mpole_e": lambda xi: 6.0,
          "Mpole_mu": lambda xi: 6.0, "R_e": lambda xi: -6.0, "R_mu": lambda xi: -6.0}


def slope_lnmu(vals):
    """mu d/dmu from mu = 1/2 and 2, and the deviation of mu = 1 from the mean (linearity)"""
    a, b, c = vals[0.5][1], vals[1.0][1], vals[2.0][1]
    return (c - a) / (2 * math.log(2)), abs(b - (a + c) / 2)


rows = []
worst = {}
for (func, arg, xi, tool), vals in sorted(ONEPI.items()):
    sl, lin = slope_lnmu(vals)
    ex = EXPECT[func](xi)
    dev = abs(sl - ex)
    pole_spread = max(abs(vals[m][0] - vals[1.0][0]) for m in MUS)
    worst[(func.split("_")[0], tool)] = max(worst.get((func.split("_")[0], tool), 0.0), dev, lin, pole_spread)
    rows.append(["1PI", func, arg, xi, tool, sl.real, sl.imag, ex, dev, lin, vals[1.0][0].real])
print(f"{'function':8} {'tool':10} {'max |slope - expected|, |X(1) - mean|, pole spread':>50}")
for (f, tool), x in sorted(worst.items()):
    print(f"{f:8} {tool:10} {x:50.1e}")
# the RG coefficients (e^2/K units) read from the slopes, at one point each, COLLIER
c1 = lambda f, arg, xi: slope_lnmu(ONEPI[(f, arg, xi, "COLLIER")])[0].real
for xi in (0.0, 1.0, 3.0):
    g_psi = -c1("SigV_e", 2.0, xi) / 2
    g_m = 2 * g_psi - c1("SigS_e", 2.0, xi)
    print(f"xi = {xi:.0f}: gamma_psi = {g_psi:+.12f} (xi), gamma_m/m from Sigma = {g_m:+.12f}, from the pole mass = "
          f"{-c1('Mpole_e', 1.0, xi):+.12f} (-6);  residue: slope - 2 x IR pole = "
          f"{c1('R_e', 1.0, xi) - 2 * ONEPI[('R_e', 1.0, xi, 'COLLIER')][1.0][0].real:+.12f} (-2 xi)")
g_a = -(c1("Pi_e", 2.0, 0.0) + c1("Pi_mu", 2.0, 0.0)) / 2
print(f"gamma_A = {g_a:.12f} (expected {GAMMA_A:.12f}),  beta_e/e^3 = gamma_A/K = {g_a / KK:.12e} (expected {BETA_E:.12e})")

# %% [markdown]
# ## The S-matrix element: beta_e from the slope of K W

# %%
print(f"{'tool':17} {'sqrt(s)':>7} {'t':>6} {'K W(1)':>22} {'slope/ln mu^2':>14} {'Re P - (8/3)B':>14} {'beta_e K/e^3':>13} {'lin':>8} {'Im':>8}")
beta_dev = {}
for (s, t, tool), vals in sorted(AMP.items(), key=lambda x: (x[0][2], x[0][0], x[0][1])):
    if not all(m in vals for m in MUS):
        continue
    b4, pole, _ = vals[1.0]
    fa, fb, fc = vals[0.5][2], vals[1.0][2], vals[2.0][2]
    sl = (fc - fa) / (2 * math.log(4))
    lin = abs(fb - (fa + fc) / 2) / abs(fb)
    alpha0 = tool.endswith("alpha(0)")
    pred = pole.real - (0 if alpha0 else 8 / 3 * b4)
    bfit = (pole.real - sl.real) / b4                  # (K/e^3) beta_e
    dim = abs(sl.imag - pole.imag)                     # the imaginary part runs only with the IR pole
    beta_dev[tool] = max(beta_dev.get(tool, 0.0), abs(bfit - (0 if alpha0 else 8 / 3)) / (8 / 3))
    print(f"{tool:17} {math.sqrt(s):7.1f} {t:6.1f} {fb.real:+22.15e} {sl.real:+14.8f} {pred:+14.8f} {bfit:13.10f} {lin:8.1e} {dim:8.1e}")
    rows.append(["K W", f"{s:g},{t:g}", "", 1.0, tool, sl.real, sl.imag, pred, abs(sl.real - pred), lin, pole.real])
print("max |beta_e fit - expected|/(8/3):", {k: f"{v:.1e}" for k, v in beta_dev.items()})
# tool against tool at mu = 1/2, 2: K W relative to COLLIER
for tool in ("LoopTools", "MadLoop"):
    d = 0.0
    for s, t in POINTS:
        for mu in MUS:
            ref = AMP[(s, t, "COLLIER")][mu][2]
            x = AMP[(s, t, tool)][mu][2]
            if tool == "MadLoop":        # four-dimensional spin sums: the mu-independent shift of Eq. (17), eq:scheme, from mu = 1
                x = x - (AMP[(s, t, tool)][1.0][2] - AMP[(s, t, "COLLIER")][1.0][2])
            d = max(d, abs(x.real - ref.real) / abs(ref.real))
    note = " (shifted by its mu = 1 difference, the mu-independent Eq. (17), eq:scheme)" if tool == "MadLoop" else ""
    print(f"{tool} against COLLIER{note}: max relative deviation {d:.1e}")

with open(os.path.join(HERE, "results", "rg_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["kind", "quantity", "arg", "xi", "tool", "re_slope", "im_slope", "expected", "abs_dev", "linearity", "re_pole"])
    w.writerows(rows)
print("wrote results/rg_comparison.csv")

# %% [markdown]
# ## Figure: fixed parameters against the one-loop running of Eq. (run)

# %%
def e2_run(mu):          # 1/e^2(mu) = 1/e^2(1) - (8 N_f/(3K)) ln mu
    return 1 / (1 - 8 * NF / (3 * KK) * math.log(mu))


def m_run(mu, m1=ME):    # m(mu) = m(1) [alpha(mu)/alpha(1)]^(-9/(4 N_f))
    return m1 * e2_run(mu) ** (-9 / (4 * NF))


scan = AMP[(FIG_PT[0], FIG_PT[1], "COLLIER")]
near = lambda d, m: d[min(d, key=lambda k: abs(k - m))]                                  # the scan's mu as written to file
mus = FIG_MUS
b4 = scan[1.0][0]
wt = np.array([(near(scan, m)[2] - near(scan, m)[1] * math.log(m * m)).real for m in mus])   # K W - P ln mu^2
w1 = scan[1.0][2].real
y_fix = (1 + 2 * wt / (KK * b4)) / (1 + 2 * w1 / (KK * b4))
y_run = np.array([e2_run(m) ** 2 * (1 + e2_run(m) * 2 * x / (KK * b4)) for m, x in zip(mus, wt)]) / (1 + 2 * w1 / (KK * b4))
a0 = AMP[(FIG_PT[0], FIG_PT[1], "MadLoop alpha(0)")]
mu_a0 = np.array(sorted(a0))
y_a0 = np.array([1 + 2 * (a0[m][2] - a0[m][1] * math.log(m * m)).real / (KK * b4) for m in mu_a0])
y_a0 = y_a0 / y_a0[list(mu_a0).index(1.0)]
mp_fix = np.array([ME * (1 + (4 + 3 * math.log(m * m / ME ** 2)) / KK) for m in mus])
mp_run = np.array([m_run(m) * (1 + e2_run(m) * (4 + 3 * math.log(m * m / m_run(m) ** 2)) / KK) for m in mus])
mp_col = {m: ME * (1 + ONEPI[("Mpole_e", 1.0, 1.0, "COLLIER")][m][1].real / KK) for m in MUS}
print(f"Y(mu)/Y(1) at mu = 1/4, 4: fixed e {y_fix[0]:.6f}, {y_fix[-1]:.6f};  running e {y_run[0]:.6f}, {y_run[-1]:.6f};  "
      f"alpha(0) (MadLoop) {y_a0[0]:.6f}, {y_a0[-1]:.6f};  fixed-e slope per ln mu {(y_fix[-1] - y_fix[0]) / math.log(16):+.6f} "
      f"(expected -2 (16/3)/K / (1 + 2 K W(1)/(K B)) = {-2 * 16 / 3 / KK / (1 + 2 * w1 / (KK * b4)):+.6f})")
print(f"m_e,pole at mu = 1/4, 4: fixed m {mp_fix[0]:.6f}, {mp_fix[-1]:.6f};  running m {mp_run[0]:.6f}, {mp_run[-1]:.6f}")
# with e(mu) the one-loop logarithm cancels; what remains is of order e^4: with c = 2 Re(K W - P ln mu^2)/(K B) = c1 - 2 b' ln mu
# (b' = 16/(3K) = 2 beta_e/e^3) and e^2(mu) = 1/(1 - b' ln mu), d ln Y/d ln mu at mu = 1 is 3 b' c1/(1 + c1)
c1, bp = 2 * w1 / (KK * b4), 2 * BETA_E
print(f"running e: d ln Y/d ln mu at mu = 1 (finite difference) {(y_run[17] - y_run[15]) / (2 * math.log(FIG_MUS[17])):+.6f}, "
      f"next order 3 b' c1/(1 + c1) = {3 * bp * c1 / (1 + c1):+.6f}  (c1 = {c1:.6f}; fixed e: -2 b'/(1 + c1) = {-2 * bp / (1 + c1):+.6f})")

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
COLORS = {"fix": "C0", "run": "C1", "a0": "C2"}     # colors of physrev.mplstyle
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
ax = axes[0]
ax.plot(mus, y_fix, color=COLORS["fix"], lw=1, ls="-", label=r"$e=1$ fixed ($\overline{\rm MS}$)")
ax.plot(mus, y_run, color=COLORS["run"], lw=1, ls="--", label=r"$e(\mu)$ running")
ax.plot(mu_a0, y_a0, ls="none", marker="o", ms=4.8, color=COLORS["a0"], label=r"$\alpha(0)$ (MadLoop)")
ax.set_xscale("log")
ax.set_xlabel(r"$\mu/m_e$")
ax.set_ylabel(r"$Y(\mu)/Y(m_e)$")
ax.set_title(r"$e^+e^-\to\mu^+\mu^-$, $\sqrt{s}=6$, $t=-8$", fontsize=8)
ax.legend(frameon=False, fontsize=6.5)
ax = axes[1]
ax.plot(mus, mp_fix, color=COLORS["fix"], lw=1, ls="-", label=r"$m_e=1$ fixed")
ax.plot(mus, mp_run, color=COLORS["run"], lw=1, ls="--", label=r"$m_e(\mu)$, $e(\mu)$ running")
ax.plot(list(mp_col), list(mp_col.values()), ls="none", marker="s", ms=4.2, color=COLORS["fix"], label="COLLIER")
ax.set_xscale("log")
ax.set_xlabel(r"$\mu/m_e$")
ax.set_ylabel(r"$m_{e,\mathrm{p}}$")
ax.set_title("electron pole mass", fontsize=8)
ax.legend(frameon=False, fontsize=6.5)
for ax in axes:
    ax.set_xticks([0.25, 0.5, 1, 2, 4], ["1/4", "1/2", "1", "2", "4"])
    ax.minorticks_off()
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "rg_running.pdf"))
print("wrote ../figs/rg_running.pdf")
if INTERACTIVE:
    plt.show()
