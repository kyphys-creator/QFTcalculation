# %% [markdown]
# # Step (7): renormalization group from the mu-dependence of phi phi -> phi phi (phi^3 + phi^4)
#
# Renormalization group of the one-loop phi phi -> phi phi amplitude (research note models/phi34, step (7)).
#
# M1 (MS-bar, note Eq. (9) (eq:M1); m = g = lambda = 1) from FeynCalc + Package-X, FeynCalc + LoopTools
# (results/rg_feyncalc.csv), COLLIER (results/rg_collier*.csv) and MadLoop at the six points of step (4) for mu = 1, 1/2, 2.
# MadLoop: work/ml_MSbar (pole-only MS-bar counterterms; finite/M0 = Re M1 at the scale mu_R = mu) and work/ml_OS (NLOCT:
# field and mass on shell, couplings MS-bar; finite/M0 = Re of M1_phys - M0(m_p), Eq. (12)), both built by run_madloop_check.sh.
#
# The S-matrix element, written with a mass parameter m (MS-bar m(mu) or pole m_p) and the MS-bar couplings g(mu), lambda(mu),
#     M = M0(m, g, lambda) + Y(mu),   M0 = -g^2 B - lambda,
# must not depend on mu (note Eq. (17) (eq:rgfit), App. J).  With A = sum_x 1/(x - m^2)^2, B = sum_x 1/(x - m^2),
# dM0/dm^2 = -g^2 A, dM0/dg = -2 g B, dM0/dlambda = -1:
#     mu dY/dmu = g^2 A gamma + 2 g B beta_g + beta_lambda.
# The slope S = [Y(2) - Y(1/2)] / (2 ln 2) at the six points determines (gamma, beta_g, beta_lambda) by least squares.  Y:
#     MS-bar m:  Y = M1 + (R^2 - 1) M0 = M1 + g^2 B0'(m^2) (g^2 B + lambda)/(4pi)^2      (mu-independent residue term)
#                expected gamma = (g^2 + lambda m^2)/(4pi)^2, beta_g = 3 g lambda/(4pi)^2, beta_lambda = 3 lambda^2/(4pi)^2
#                (Eq. (7) (eq:rge));
#     pole m:    Y = M1_phys of Eq. (12) (MadLoop: ml_OS directly)                     expected gamma = 0, the same betas.
# Four-coefficient fit (COLLIER, MS-bar m): with M1 = g^4 P + g^2 lambda Q + lambda^2 R and
#     gamma = (c1 g^2 + c2 lambda m^2)/(4pi)^2,  beta_g = b_g g lambda/(4pi)^2,  beta_lambda = b_l lambda^2/(4pi)^2,
# the slopes of the three structures are c1 A, c2 m^2 A + 2 b_g B and b_l (times 1/(4pi)^2); expected c1 = c2 = 1, b_g = b_l = 3.
# The figure: the S-matrix element in MS-bar parameters at sqrt(s) = 5m, cos(theta) = 0.3 for mu = m/4 ... 4m, with m, g,
# lambda fixed and with the one-loop running (App. J):
#     lambda(mu) = lambda/(1 - 3 lambda t/(4pi)^2),  g(mu) = g lambda(mu)/lambda,
#     m^2(mu) = (m^2 - g^2/(2 lambda)) (lambda(mu)/lambda)^(1/3) + g^2 lambda(mu)/(2 lambda^2),   t = ln(mu/m);
# the remainder is (1/2) M0'' t^2 with (4pi)^4 M0'' = -54 B - 35 A - 8 C - 18 (m = g = lambda = 1, C = sum_x 1/(x - m^2)^3).
# Writes results/rg_comparison.csv and ../figs/rg_d4.pdf (the same layout as the phi^3 note's rg4_d4.pdf).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rg_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys
import re
import subprocess

import numpy as np

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K = (4 * math.pi) ** 2
B0PM = 2 * math.pi / (3 * math.sqrt(3)) - 1          # m^2 B0'(m^2), mu-independent
TOL = 1e-9     # Package-X's numerical D0 limits it to ~1e-11 where Re M1 is a cancellation of larger terms
MUS = (0.5, 1.0, 2.0)
POINTS = [(rs, ct) for rs in (2.5, 5.0, 10.0) for ct in (0.3, 0.9)]


# %% [markdown]
# ## Helper functions: tree, the sums A, B, C, conversions, MadLoop runs

# %%
def tree(s, t):
    u = 4 - s - t
    return -(1 / (s - 1) + 1 / (t - 1) + 1 / (u - 1)) - 1


def sums(s, t):
    xs = (s, t, 4 - s - t)
    return (sum(1 / (x - 1) ** 2 for x in xs), sum(1 / (x - 1) for x in xs), sum(1 / (x - 1) ** 3 for x in xs))


def b0m(mu):             # B0(m^2) at m = 1 (note, below Eq. (12))
    return 2 - math.pi / math.sqrt(3) + 2 * math.log(mu)


def a0m(mu):             # A0(m^2) = m^2 (1 - ln(m^2/mu^2)) at m = 1
    return 1 + 2 * math.log(mu)


def residue(s, t):       # (R^2 - 1) M0 = g^2 B0'(m^2) (g^2 B + lambda)/(4pi)^2
    return B0PM * (sums(s, t)[1] + 1) / K


def conversion(s, t, mu):   # Delta M of Eq. (12)
    a, b, _ = sums(s, t)
    return (2 * B0PM * b - (b0m(mu) + a0m(mu)) * a) / (2 * K) + B0PM / K


def read(path, cols):
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6), round(float(r["mu"]), 6))
            out[key] = dict(s=float(r["s"]), t=float(r["t"]),
                            **{c: complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols})
            for c in ("p", "q", "r"):
                if "re_" + c in r:
                    out[key][c] = float(r["re_" + c])
    return out


def momenta(rs, ct):
    e = rs / 2
    p = math.sqrt(e * e - 1)
    st = math.sqrt(1 - ct * ct)
    return [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * ct), (e, -p * st, 0, -p * ct)]


def run_madloop(scheme, rs, ct, mu):
    """MadLoop finite part M0 Re M1 (identical-particle factor 1/2 included); scheme MSbar or OS."""
    d = os.path.join(HERE, "work", f"ml_{scheme}", "SubProcesses", "P0_phiphi_phiphi")
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta(rs, ct))
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element finite\s*=\s*(\S+)", out).group(1))


# %% [markdown]
# ## The tools at mu = 1/2, 1, 2 (MadLoop included)

# %%
# ---------------- the tools at mu = 1/2, 1, 2 ----------------
fc = read(os.path.join(HERE, "results", "rg_feyncalc.csv"), ["packagex", "looptools"])
co = read(os.path.join(HERE, "results", "rg_collier.csv"), ["collier"])
data = {}
for rs, ct in POINTS:
    for mu in MUS:
        key = (rs, ct, mu)
        v = {**fc[key], **co[key]}
        m0 = tree(v["s"], v["t"])
        v["madloop"] = complex(run_madloop("MSbar", rs, ct, mu) / m0, float("nan"))
        v["madloop_os"] = run_madloop("OS", rs, ct, mu) / m0
        data[key] = v
tools = ("packagex", "looptools", "collier", "madloop")

rows = []
print(f"M1 (MS-bar) at mu = 1/2, 1, 2\n{'sqrt(s)':>7} {'cos':>4} {'mu':>4} {'Re M1 (COLLIER)':>22} {'Im M1 (COLLIER)':>22}"
      f" | Re: PX LT MadLoop | Im - Im(mu=1): PX LT COLLIER | MadLoop OS - Eq. (12)")
for key in sorted(data):
    rs, ct, mu = key
    v = data[key]
    re_ref = v["collier"].real
    dre = {k: abs(v[k].real - re_ref) / abs(re_ref) for k in tools}
    dim = {k: abs(v[k].imag - data[(rs, ct, 1.0)][k].imag) / abs(data[(rs, ct, 1.0)][k].imag) for k in tools[:3]}
    phys = re_ref + conversion(v["s"], v["t"], mu)
    dos = abs(v["madloop_os"] - phys) / abs(phys)
    bad = ([k for k in tools if dre[k] > TOL] + [k for k in tools[:3] if dim[k] > TOL]
           + (["madloop_os"] if dos > TOL else []))
    print(f"{rs:7.1f} {ct:4.1f} {mu:4.1f} {re_ref:+22.15e} {v['collier'].imag:+22.15e} | {dre['packagex']:7.1e} "
          f"{dre['looptools']:7.1e} {dre['madloop']:7.1e} | {dim['packagex']:7.1e} {dim['looptools']:7.1e} "
          f"{dim['collier']:7.1e} | {dos:7.1e}" + ("   <- disagrees: " + ",".join(bad) if bad else ""))
    rows.append([rs, ct, mu, v["s"], v["t"], tree(v["s"], v["t"]), re_ref, v["collier"].imag,
                 *(v[k].real for k in tools), v["madloop_os"], *(dre[k] for k in tools), dos])


# %% [markdown]
# ## Slopes in ln(mu) and the three-parameter fits (Eq. (17))

# %%
# ---------------- slopes and the three-parameter fits ----------------
def y_value(case, v, s, t, mu, k):
    if case == "MS-bar m":
        return v[k].real + residue(s, t)
    if k == "madloop":                     # pole m: the on-shell UFO gives M1_phys directly
        return v["madloop_os"]
    return v[k].real + conversion(s, t, mu)


CASES = [("MS-bar m", 2 / K, 3 / K, 3 / K), ("pole m", 0.0, 3 / K, 3 / K)]
slope_rows, fit_rows = [], []
for name, g_exp, bg_exp, bl_exp in CASES:
    print(f"\n{name}: expected gamma = {g_exp:+.10e}, beta_g = {bg_exp:+.10e}, beta_lambda = {bl_exp:+.10e}")
    for k in tools:
        eqs, lin = [], 0.0
        for rs, ct in POINTS:
            v1 = data[(rs, ct, 1.0)]
            s, t = v1["s"], v1["t"]
            y = {mu: y_value(name, data[(rs, ct, mu)], s, t, mu, k) for mu in MUS}
            slope = (y[2.0] - y[0.5]) / (2 * math.log(2))
            lin = max(lin, abs(y[1.0] - (y[2.0] + y[0.5]) / 2) / abs(y[1.0]))    # Y is linear in ln(mu)
            a, b, _ = sums(s, t)
            eqs.append((a, 2 * b, 1.0, slope))
            slope_rows.append([name, k, rs, ct, a, b, slope, a * g_exp + 2 * b * bg_exp + bl_exp])
        X = np.array([e[:3] for e in eqs])
        S = np.array([e[3] for e in eqs])
        norm = np.sqrt((X ** 2).sum(axis=1))               # a one-loop slope there is ~ norm/(4pi)^2
        (gam, bg, bl), *_ = np.linalg.lstsq(X / norm[:, None], S / norm, rcond=None)
        res = max(abs(X @ np.array([gam, bg, bl]) - S) / (norm / K))
        dg = abs(gam / g_exp - 1) if g_exp else abs(gam) * K        # zero expected: in units of the loop factor
        dbg, dbl = abs(bg / bg_exp - 1), abs(bl / bl_exp - 1)
        print(f"  {k:9}: gamma = {gam:+.10e} ({'rel. dev.' if g_exp else '|gamma| (4pi)^2'} {dg:.1e}),  "
              f"beta_g = {bg:+.10e} ({dbg:.1e}),  beta_lambda = {bl:+.10e} ({dbl:.1e}),  "
              f"residual {res:.0e},  linearity {lin:.0e}")
        fit_rows.append([name, k, gam, bg, bl, g_exp, bg_exp, bl_exp, dg, dbg, dbl, res, lin])
print(f"\ncondition number of the weighted design matrix: {np.linalg.cond(X / norm[:, None]):.1f}")


# %% [markdown]
# ## Four-coefficient fit from the COLLIER coupling structures

# %%
# ---------------- four coefficients c1, c2, b_g, b_l from the structures P, Q, R (COLLIER, MS-bar m) ----------------
sl = {c: [] for c in "pqr"}
ab = []
for rs, ct in POINTS:
    v1 = data[(rs, ct, 1.0)]
    for c in "pqr":
        sl[c].append((data[(rs, ct, 2.0)][c] - data[(rs, ct, 0.5)][c]) / (2 * math.log(2)) * K)
    ab.append(sums(v1["s"], v1["t"])[:2])
ab = np.array(ab)
c1 = np.linalg.lstsq(ab[:, :1], np.array(sl["p"]), rcond=None)[0][0]
c2, bg2 = np.linalg.lstsq(np.column_stack([ab[:, 0], 2 * ab[:, 1]]), np.array(sl["q"]), rcond=None)[0]
bl4 = float(np.mean(sl["r"]))
coef = dict(c1=c1, c2=c2, b_g=bg2, b_l=bl4)
spread_r = max(abs(np.array(sl["r"]) - bl4))
print("four-coefficient fit (COLLIER): " + ",  ".join(f"{n} = {v:.15f}" for n, v in coef.items())
      + f"   (expected 1, 1, 3, 3; spread of the lambda^2 slope over the points {spread_r:.0e})")
for n, v, e in (("c1", c1, 1), ("c2", c2, 1), ("b_g", bg2, 3), ("b_l", bl4, 3)):
    assert abs(v / e - 1) < 1e-12, n


# %%
with open(os.path.join(HERE, "results", "rg_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sqrts", "costheta", "mu", "s", "t", "tree", "re_ref_collier", "im_collier",
                *(f"re_{k}" for k in tools), "madloop_os_phys", *(f"reldev_re_{k}" for k in tools), "reldev_madloop_os"])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["case", "tool", "sqrts", "costheta", "A", "B", "slope_dY_dlnmu", "slope_expected"])
    w.writerows(slope_rows)
    w.writerow([])
    w.writerow(["case", "tool", "gamma_fit", "beta_g_fit", "beta_lambda_fit", "gamma_expected", "beta_g_expected",
                "beta_lambda_expected", "dev_gamma", "dev_beta_g", "dev_beta_lambda", "fit_residual", "linearity"])
    w.writerows(fit_rows)
    w.writerow([])
    w.writerow(["coefficient", "value", "expected"])
    w.writerows([[n, v, e] for (n, v), e in zip(coef.items(), (1, 1, 3, 3))])


# %% [markdown]
# ## Figure: the S-matrix element with m, g, lambda fixed and running

# %%
# ---------------- figure: the same layout as the phi^3 note's rg4_d4.pdf ----------------
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)

musc = read(os.path.join(HERE, "results", "rg_collier_muscan.csv"), ["collier"])
mus = np.array(sorted(k[2] for k in musc))
s0 = 25.0
t0 = musc[(5.0, 0.3, round(mus[0], 6))]["t"]
u0 = 4 - s0 - t0
y = np.array([musc[(5.0, 0.3, round(mu, 6))]["collier"].real for mu in mus]) + residue(s0, t0)


def tree_p(m2, g, lam):
    return -g * g * sum(1 / (x - m2) for x in (s0, t0, u0)) - lam


def running(t):
    """One-loop solution of Eq. (7) from m = g = lambda = 1 at mu = m (App. J)."""
    lam = 1 / (1 - 3 * t / K)
    return 0.5 * lam ** (1 / 3) + 0.5 * lam, lam, lam      # m^2, g, lambda


# the closed-form running satisfies Eq. (7) (central differences)
for tt in (-1.4, 0.0, 1.4):
    h = 1e-5
    (mp, gp, lp), (mm, gm, lm), (m2, g, lam) = running(tt + h), running(tt - h), running(tt)
    assert abs((lp - lm) / (2 * h) - 3 * lam ** 2 / K) < 1e-9 and abs((gp - gm) / (2 * h) - 3 * g * lam / K) < 1e-9
    assert abs((mp - mm) / (2 * h) - (g * g + lam * m2) / K) < 1e-9

ts = np.log(mus)
fixed = tree_p(1.0, 1.0, 1.0) + y
run = np.array([tree_p(*running(tt)) for tt in ts]) + y
i1 = int(np.argmin(abs(mus - 1)))
a0s, b0s, c0s = sums(s0, t0)
pred = 0.5 * (-54 * b0s - 35 * a0s - 8 * c0s - 18) / K ** 2 * ts ** 2 / run[i1]     # (1/2) M0'' t^2, relative
fig, ax = plt.subplots(figsize=(3.25, 2.2))
ax.plot(mus, 1e3 * (fixed / fixed[i1] - 1), color="#5d81b4", lw=0.9, ls="--", label=r"$m,g,\lambda$ fixed")
ax.plot(mus, 1e3 * (run / run[i1] - 1), color="k", lw=0.9, ls="-", label=r"running, Eq. (7)")
ax.set_xscale("log")
ax.set_xticks([0.25, 0.5, 1, 2, 4])
ax.set_xticklabels(["1/4", "1/2", "1", "2", "4"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel(r"$\mu/m$")
ax.set_ylabel(r"$10^3\,\Delta\mathcal{M}_{\rm phys}/\mathcal{M}_{\rm phys}$")
ax.set_title(r"$\sqrt{s}=5m$, $\cos\theta=0.3$", fontsize=8)
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "rg_d4.pdf"))
dev_run = run / run[i1] - 1
print(f"\nmu from 1/4 to 4 at sqrt(s) = 5m, cos = 0.3: largest deviation from mu = m with m, g, lambda fixed "
      f"{max(abs(fixed / fixed[i1] - 1)):.2e}, running {max(abs(dev_run)):.2e}; at mu = 4m running {dev_run[-1]:+.3e}, "
      f"(1/2) M0'' t^2 {pred[-1]:+.3e}; at mu = m/4 running {dev_run[0]:+.3e}, (1/2) M0'' t^2 {pred[0]:+.3e}")
print(f"A = {a0s:.6e}, B = {b0s:.6e}, C = {c0s:.6e}, M(mu = m) = {run[i1]:.10f}")
print("wrote results/rg_comparison.csv and figs/rg_d4.pdf")
