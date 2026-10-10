# %% [markdown]
# # Step (9): renormalization group from the mu-dependence of phi phi -> phi phi (d = 4 and d = 6)
#
# Renormalization group of the one-loop phi phi -> phi phi amplitude in d = 4 and d = 6 (research note, step (9)).
#
# d = 4: M1 (MS-bar, note Eq. (17) (eq:M1); m = g = 1) from FeynCalc + Package-X, FeynCalc + LoopTools (results/rg4_feyncalc.csv),
# COLLIER (results/rg4_collier*.csv) and MadLoop with the pole-only MS-bar counterterms (work/ml_MSbar, built by
# run_madloop_check.sh; M1 = finite/M0) at the six points of step (5) for mu = 1, 1/2, 2.
# d = 6: M1 (Eq. (22) (eq:M6)) from results/scat6_feyncalc.csv and results/scat6_collier.csv (step (8)).
#
# The S-matrix element, written with a mass parameter m (MS-bar m(mu) or pole m_p) and the MS-bar coupling g(mu),
#     M = M0(m, g) + Y(mu),   Y = M1 + (conversion to the S-matrix element, note Eq. (20) (eq:Mphys), Apps. J, L),
# must not depend on mu (note Eq. (27) (eq:rgfit), App. M).  With A = sum_x 1/(x - m^2)^2, B = sum_x 1/(x - m^2),
# dM0/dm^2 = -g^2 A and dM0/dg = -2 g B,
#     mu dY/dmu = g^2 A gamma + 2 g B beta,   gamma = mu dm^2/dmu,   beta = mu dg/dmu.
# The slope S = [Y(2) - Y(1/2)] / (2 ln 2) at the six points determines (gamma, beta) by least squares.  Y:
#     d = 4, MS-bar m:  Y = M1 + (1/(4pi)^2) sum_x B0'(m^2)/(x - m^2)          (the residue; mu-independent)
#                       expected gamma = g^2/(4pi)^2 (Eq. (15)), beta = 0;
#     d = 4, pole m:    Y = M1_phys of Eq. (20)                                 expected gamma = beta = 0;
#     d = 6, pole m:    Y = M1_phys (App. L)                                    expected gamma = 0, beta = -3 g^3/(4 (4pi)^3) (Eq. (14));
#     d = 6, MS-bar m:  Y = M1 + (1/(4pi)^3) sum_x B0^(6)'(m^2)/(x - m^2)
#                       expected gamma = -5 g^2 m^2/(6 (4pi)^3) (App. D), beta = -3 g^3/(4 (4pi)^3).
# Writes results/rg4_comparison.csv and ../figs/rg4_d4.pdf (the same layout as figs/scat6_rg_d6.pdf).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rg4_numeric.py
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
K4 = (4 * math.pi) ** 2
K6 = (4 * math.pi) ** 3
B0PM = 2 * math.pi / (3 * math.sqrt(3)) - 1          # m^2 B0'(m^2), mu-independent
TOL = 1e-9     # Package-X's numerical D0 limits it to ~1e-10 where Re M1 is a cancellation of larger terms
MUS = (0.5, 1.0, 2.0)
POINTS = [(rs, ct) for rs in (2.5, 5.0, 10.0) for ct in (0.3, 0.9)]


# %% [markdown]
# ## Helper functions: tree, the sums A and B, conversions, MadLoop runs

# %%
def tree(s, t):
    u = 4 - s - t
    return -(1 / (s - 1) + 1 / (t - 1) + 1 / (u - 1))


def sums(s, t):
    xs = (s, t, 4 - s - t)
    return sum(1 / (x - 1) ** 2 for x in xs), sum(1 / (x - 1) for x in xs)


def b04m(mu):            # B0(m^2) at m = 1, App. J
    return 2 - math.pi / math.sqrt(3) + 2 * math.log(mu)


def b06m(mu):            # Eq. (23) (eq:B06m) at m = 1
    return -17 / 9 + math.pi / (2 * math.sqrt(3)) - 5 / 3 * math.log(mu)


def b06p(mu):
    return 17 / 18 - math.pi / (2 * math.sqrt(3)) + math.log(mu) / 3


def residue4(s, t):
    return B0PM * sums(s, t)[1] / K4


def conversion4(s, t, mu):
    a, b = sums(s, t)
    return (2 * B0PM * b - b04m(mu) * a) / (2 * K4)


def residue6(s, t, mu):
    return b06p(mu) * sums(s, t)[1] / K6


def conversion6(s, t, mu):
    a, b = sums(s, t)
    return (2 * b06p(mu) * b - b06m(mu) * a) / (2 * K6)


def read(path, cols):
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6), round(float(r["mu"]), 6))
            out[key] = dict(s=float(r["s"]), t=float(r["t"]),
                            **{c: complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols})
    return out


def momenta(rs, ct):
    e = rs / 2
    p = math.sqrt(e * e - 1)
    st = math.sqrt(1 - ct * ct)
    return [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * ct), (e, -p * st, 0, -p * ct)]


def run_madloop(rs, ct, mu):
    """MadLoop with the pole-only MS-bar counterterms: finite = M0 Re M1 (identical-particle factor 1/2 included)."""
    d = os.path.join(HERE, "work", "ml_MSbar", "SubProcesses", "P0_phiphi_phiphi")
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta(rs, ct))
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element finite\s*=\s*(\S+)", out).group(1))


# %% [markdown]
# ## d = 4: the tools at mu = 1/2, 1, 2 (MadLoop included)

# %%
# ---------------- d = 4: the tools at mu = 1/2, 1, 2 ----------------
fc = read(os.path.join(HERE, "results", "rg4_feyncalc.csv"), ["packagex", "looptools"])
co = read(os.path.join(HERE, "results", "rg4_collier.csv"), ["collier"])
d4 = {}
for rs, ct in POINTS:
    for mu in MUS:
        key = (rs, ct, mu)
        v = {**fc[key], **co[key]}
        v["madloop"] = complex(run_madloop(rs, ct, mu) / tree(v["s"], v["t"]), float("nan"))
        d4[key] = v
tools4 = ("packagex", "looptools", "collier", "madloop")

rows = []
print(f"d = 4, M1 (MS-bar) at mu = 1/2, 1, 2\n{'sqrt(s)':>7} {'cos':>4} {'mu':>4} {'Re M1 (COLLIER)':>22} {'Im M1 (COLLIER)':>22}"
      f" | Re: PX LT MadLoop | Im - Im(mu=1): PX LT COLLIER")
for key in sorted(d4):
    rs, ct, mu = key
    v = d4[key]
    re_ref = v["collier"].real
    dre = {k: abs(v[k].real - re_ref) / abs(re_ref) for k in tools4}
    dim = {k: abs(v[k].imag - d4[(rs, ct, 1.0)][k].imag) / abs(d4[(rs, ct, 1.0)][k].imag) for k in tools4[:3]}
    bad = [k for k in tools4 if dre[k] > TOL] + [k for k in tools4[:3] if dim[k] > TOL]
    print(f"{rs:7.1f} {ct:4.1f} {mu:4.1f} {re_ref:+22.15e} {v['collier'].imag:+22.15e} | {dre['packagex']:7.1e} "
          f"{dre['looptools']:7.1e} {dre['madloop']:7.1e} | {dim['packagex']:7.1e} {dim['looptools']:7.1e} "
          f"{dim['collier']:7.1e}" + ("   <- disagrees: " + ",".join(bad) if bad else ""))
    rows.append([rs, ct, mu, v["s"], v["t"], tree(v["s"], v["t"]), re_ref, v["collier"].imag,
                 *(v[k].real for k in tools4), *(dre[k] for k in tools4)])


# %% [markdown]
# ## d = 6: the values of step (8)

# %%
# ---------------- d = 6: step (8) ----------------
fc6 = read(os.path.join(HERE, "results", "scat6_feyncalc.csv"), ["packagex", "looptools"])
co6 = read(os.path.join(HERE, "results", "scat6_collier.csv"), ["collier"])
d6 = {key: {**fc6[key], **co6[key]} for key in fc6}
tools6 = ("packagex", "looptools", "collier")


# %% [markdown]
# ## Slopes in ln(mu) and the two-parameter fits (Eq. (27))

# %%
# ---------------- slopes and the two-parameter fits ----------------
CASES = [
    # name, data, tools, Y(v, s, t, mu, tool), expected gamma, expected beta
    ("d=4, MS-bar m", d4, tools4, lambda v, s, t, mu, k: v[k].real + residue4(s, t), 1 / K4, 0.0),
    ("d=4, pole m", d4, tools4, lambda v, s, t, mu, k: v[k].real + conversion4(s, t, mu), 0.0, 0.0),
    ("d=6, pole m", d6, tools6, lambda v, s, t, mu, k: v[k].real + conversion6(s, t, mu), 0.0, -3 / (4 * K6)),
    ("d=6, MS-bar m", d6, tools6, lambda v, s, t, mu, k: v[k].real + residue6(s, t, mu), -5 / (6 * K6), -3 / (4 * K6)),
]
slope_rows, fit_rows = [], []
for name, data, tools, yfun, g_exp, b_exp in CASES:
    print(f"\n{name}: expected gamma = mu dm^2/dmu = {g_exp:+.10e}, beta = {b_exp:+.10e}")
    for k in tools:
        eqs, lin = [], 0.0
        for rs, ct in POINTS:
            v1 = data[(rs, ct, 1.0)]
            s, t = v1["s"], v1["t"]
            y = {mu: yfun(data[(rs, ct, mu)], s, t, mu, k) for mu in MUS}
            slope = (y[2.0] - y[0.5]) / (2 * math.log(2))
            lin = max(lin, abs(y[1.0] - (y[2.0] + y[0.5]) / 2) / abs(y[1.0]))    # Y is linear in ln(mu)
            a, b = sums(s, t)
            eqs.append((a, 2 * b, slope))
            slope_rows.append([name, k, rs, ct, a, b, slope, a * g_exp + 2 * b * b_exp])
        X = np.array([e[:2] for e in eqs])
        S = np.array([e[2] for e in eqs])
        w = 1 / np.hypot(X[:, 0], X[:, 1])                    # each point with the same weight
        (gam, bet), *_ = np.linalg.lstsq(X * w[:, None], S * w, rcond=None)
        scale = np.hypot(X[:, 0], X[:, 1]) / (K4 if name.startswith("d=4") else K6)   # a one-loop slope there
        res = max(abs(X @ np.array([gam, bet]) - S) / scale)
        kd, nd = (K4, "(4pi)^2") if name.startswith("d=4") else (K6, "(4pi)^3")
        dg = abs(gam / g_exp - 1) if g_exp else abs(gam) * kd        # zero expected: in units of the loop factor
        db = abs(bet / b_exp - 1) if b_exp else abs(bet) * kd
        print(f"  {k:9}: gamma = {gam:+.10e} ({'rel. dev.' if g_exp else '|gamma| ' + nd} {dg:.1e}),  "
              f"beta = {bet:+.10e} ({'rel. dev.' if b_exp else '|beta| ' + nd} {db:.1e}),  "
              f"fit residual {res:.0e},  linearity in ln mu {lin:.0e}")
        fit_rows.append([name, k, gam, bet, g_exp, b_exp, dg, db, res, lin])


# %%
with open(os.path.join(HERE, "results", "rg4_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sqrts", "costheta", "mu", "s", "t", "tree", "re_ref_collier", "im_collier",
                *(f"re_{k}" for k in tools4), *(f"reldev_re_{k}" for k in tools4)])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["case", "tool", "sqrts", "costheta", "A", "B", "slope_dY_dlnmu", "slope_expected"])
    w.writerows(slope_rows)
    w.writerow([])
    w.writerow(["case", "tool", "gamma_fit", "beta_fit", "gamma_expected", "beta_expected", "dev_gamma", "dev_beta",
                "fit_residual", "linearity"])
    w.writerows(fit_rows)


# %% [markdown]
# ## Figure: the S-matrix element with m fixed and with m(mu) running

# %%
# ---------------- figure: the same layout as figs/scat6_rg_d6.pdf ----------------
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)

musc = read(os.path.join(HERE, "results", "rg4_collier_muscan.csv"), ["collier"])
mus = np.array(sorted(k[2] for k in musc))
s0 = 25.0
t0 = musc[(5.0, 0.3, round(mus[0], 6))]["t"]
u0 = 4 - s0 - t0
y = np.array([musc[(5.0, 0.3, round(mu, 6))]["collier"].real for mu in mus]) + residue4(s0, t0)


def tree_m2(m2):
    return -sum(1 / (x - m2) for x in (s0, t0, u0))


m2run = 1 + np.log(mus) / K4                     # Eq. (mrun4) from m(m) = 1 (g does not run)
fixed = tree_m2(1.0) + y
running = np.array([tree_m2(m2) for m2 in m2run]) + y
i1 = int(np.argmin(abs(mus - 1)))
fig, ax = plt.subplots(figsize=(3.25, 2.2))
ax.plot(mus, 1e3 * (fixed / fixed[i1] - 1), color="#5d81b4", lw=0.9, ls="--", label=r"$m$ fixed")
ax.plot(mus, 1e3 * (running / running[i1] - 1), color="k", lw=0.9, ls="-", label=r"$m(\mu)$, Eq. (15)")
ax.set_xscale("log")
ax.set_xticks([0.25, 0.5, 1, 2, 4])
ax.set_xticklabels(["1/4", "1/2", "1", "2", "4"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel(r"$\mu/m$")
ax.set_ylabel(r"$10^3\,\Delta\mathcal{M}_{\rm phys}/\mathcal{M}_{\rm phys}$")
ax.set_title(r"$d=4$, $\sqrt{s}=5m$, $\cos\theta=0.3$", fontsize=8)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "rg4_d4.pdf"))
print(f"\nmu from 1/4 to 4 at sqrt(s) = 5m, cos = 0.3: relative change between the ends with m fixed "
      f"{abs(fixed[-1] / fixed[0] - 1):.2e}, with m(mu) {abs(running[-1] / running[0] - 1):.2e}; largest deviation from "
      f"mu = m with m fixed {max(abs(fixed / fixed[i1] - 1)):.2e}, with m(mu) {max(abs(running / running[i1] - 1)):.2e}")
print("wrote results/rg4_comparison.csv and figs/rg4_d4.pdf")
