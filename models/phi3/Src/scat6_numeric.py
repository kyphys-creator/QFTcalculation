# %% [markdown]
# # Step (8): d = 6 one-loop phi phi -> phi phi: comparison, unitarity and the beta function
#
# One-loop phi phi -> phi phi in d = 6: comparison, unitarity and beta function (research note, step (8)).
#
# M1 (MS-bar, note Eq. (22) (eq:M6); m = g = 1) from FeynCalc + Package-X, FeynCalc + LoopTools (results/scat6_feyncalc.csv)
# and COLLIER (results/scat6_collier*.csv) at the six points of step (5) for mu = 1, 1/2, 2.
#   Re M1: COLLIER is the reference.
#   Im M1: s-channel unitarity with the d = 6 two-body phase space (note, App. L),
#       Im M1(s, t) = (1/4) (2 pi)^-4 p^3/(4 sqrt(s)) * 4 pi int_0^pi sin^3(a) da int_0^pi sin^2(b) db M0(s, t1) M0(s, t2),
#       t1 = -2 p^2 (1 - cos a),  t2 = -2 p^2 (1 - cos(theta) cos a - sin(theta) sin a cos b).
#   beta function: the S-matrix element in terms of the pole mass m_p and the MS-bar coupling g(mu),
#       M_phys = M0 + M1_phys,  M1_phys = M1 + 1/(2(4pi)^3) sum_x [2 B0^(6)'(m^2)/(x - m^2) - B0^(6)(m^2)/(x - m^2)^2],
#       with B0^(6)(m^2) = m^2 (-17/9 + pi/(2 sqrt 3) + (5/6) L) and B0^(6)'(m^2) = 17/18 - pi/(2 sqrt 3) - L/6,
#       L = ln(m^2/mu^2) (from Eq. (13)), must not depend on mu:  beta = (d M1_phys/d ln mu) / (2 g sum_x 1/(x - m^2)),
#       to be compared with Eq. (14), beta = -3 g^3/(4 (4 pi)^3).
# Writes results/scat6_comparison.csv, ../figs/scat6_d6.pdf (same layout as scat4_d4.pdf) and
# ../figs/scat6_rg_d6.pdf (mu-dependence of the S-matrix element).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python scat6_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import mpmath as mp

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K6 = (4 * math.pi) ** 3
BETA = -3 / (4 * K6)
TOL = 1e-9     # Package-X's numerical D0 limits it to ~1e-10 where Re M1 is a cancellation of larger terms


# %% [markdown]
# ## Tree amplitude, the S-matrix conversion (Eq. (23)) and closed forms

# %%
def tree(s, t):
    u = 4 - s - t
    return -(1 / (s - 1) + 1 / (t - 1) + 1 / (u - 1))


def b06m(mu):
    L = -2 * math.log(mu)
    return -17 / 9 + math.pi / (2 * math.sqrt(3)) + 5 / 6 * L


def b06p(mu):
    L = -2 * math.log(mu)
    return 17 / 18 - math.pi / (2 * math.sqrt(3)) - L / 6


def conversion6(s, t, mu):
    u = 4 - s - t
    return sum(2 * b06p(mu) / (x - 1) - b06m(mu) / (x - 1) ** 2 for x in (s, t, u)) / (2 * K6)


def b0_closed(p2, mu2=1):
    """d = 4 MS-bar B0(p^2; 1, 1), App. G (below threshold suffices here)."""
    p2 = mp.mpf(p2)
    if p2 == 0:
        return -mp.log(1 / mp.mpf(mu2))
    bt = mp.sqrt(4 / p2 - 1)
    return 2 - mp.log(1 / mp.mpf(mu2)) - 2 * bt * mp.atan(1 / bt)


def b06_closed(p2, mu2=1):
    """Eq. (13) with m = 1."""
    p2 = mp.mpf(p2)
    return -1 + p2 / 9 + mp.log(1 / mp.mpf(mu2)) / 3 - mp.mpf(2) / 3 * (1 - p2 / 4) * b0_closed(p2, mu2)


# %%
# the closed forms used in the conversion, against Eq. (13)
with mp.workdps(30):
    for mu in (0.5, 1.0, 2.0):
        assert abs(b06_closed(1, mu * mu) - b06m(mu)) < 1e-14
        assert abs(mp.diff(lambda q: b06_closed(q, mu * mu), 1) - b06p(mu)) < 1e-14
print("B0^(6)(m^2) and B0^(6)'(m^2) used in the conversion agree with Eq. (13): ok")


# %% [markdown]
# ## The d = 6 unitarity integral and the optical theorem

# %%
def im_unitarity(s, cth, dps=20):
    with mp.workdps(dps):
        s, cth = mp.mpf(s), mp.mpf(cth)
        p2 = s / 4 - 1
        p = mp.sqrt(p2)
        sth = mp.sqrt(1 - cth ** 2)

        def f(a, b):
            ca, sa = mp.cos(a), mp.sin(a)
            t1 = -2 * p2 * (1 - ca)
            t2 = -2 * p2 * (1 - cth * ca - sth * sa * mp.cos(b))
            return sa ** 3 * mp.sin(b) ** 2 * tree(s, t1) * tree(s, t2)

        integral = mp.quad(f, [0, mp.pi], [0, mp.pi])
        return float(mp.mpf(1) / 4 * (2 * mp.pi) ** -4 * p ** 3 / (4 * mp.sqrt(s)) * 4 * mp.pi * integral)


def sigma_tree6(s, dps=20):
    """d = 6 tree cross section: (1/(4 p sqrt s)) (1/2) int dPhi_2 |M0|^2, dPhi_2 = (2pi)^-4 p^3 dOmega_4/(4 sqrt s);
    the integrand depends only on the polar angle a, and int dOmega_4 = 2 pi^2 int_0^pi sin^3(a) da (2 pi^2 = |S^3|)."""
    with mp.workdps(dps):
        s = mp.mpf(s)
        p2 = s / 4 - 1
        p = mp.sqrt(p2)
        integral = mp.quad(lambda a: mp.sin(a) ** 3 * tree(s, -2 * p2 * (1 - mp.cos(a))) ** 2, [0, mp.pi])
        return (2 * mp.pi) ** -4 * p ** 3 / (4 * mp.sqrt(s)) * 2 * mp.pi ** 2 * integral / 2 / (4 * p * mp.sqrt(s))


# the unitarity integral reproduces the optical theorem in the forward direction (checks the d = 6 angular measure)
for rs_ in (2.5, 5.0, 10.0):
    lhs = im_unitarity(rs_ ** 2, 1.0)
    rhs = float(2 * mp.sqrt(rs_ ** 2 / 4 - 1) * rs_ * sigma_tree6(rs_ ** 2))
    assert abs(lhs / rhs - 1) < 1e-14, (rs_, lhs, rhs)
print("d = 6 unitarity integral at cos(theta) = 1 equals 2 p sqrt(s) sigma_tree (optical theorem): ok")


def read(path, cols):
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6), round(float(r["mu"]), 6))
            out[key] = dict(s=float(r["s"]), t=float(r["t"]),
                            **{c: complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols})
    return out


# %% [markdown]
# ## The tool values

# %%
fc = read(os.path.join(HERE, "results", "scat6_feyncalc.csv"), ["packagex", "looptools"])
co = read(os.path.join(HERE, "results", "scat6_collier.csv"), ["collier"])
tools = ("packagex", "looptools", "collier")


# %% [markdown]
# ## Comparison at the six points

# %%
rows = []
print(f"\n{'sqrt(s)':>7} {'cos':>4} {'mu':>4} {'Re M1 (COLLIER)':>22} {'Im M1 (unitarity)':>22} | Re: PX LT | Im: PX LT COLLIER")
imref = {}
for key in sorted(fc):
    rs, cth, mu = key
    v = {**fc[key], **co[key]}
    if (rs, cth) not in imref:
        imref[(rs, cth)] = im_unitarity(v["s"], cth)
    re_ref, im_ref = v["collier"].real, imref[(rs, cth)]
    dre = {k: abs(v[k].real - re_ref) / abs(re_ref) for k in tools}
    dim = {k: abs(v[k].imag - im_ref) / abs(im_ref) for k in tools}
    bad = [k for k in tools if dre[k] > TOL or dim[k] > TOL]
    print(f"{rs:7.1f} {cth:4.1f} {mu:4.1f} {re_ref:+22.15e} {im_ref:+22.15e} | {dre['packagex']:7.1e} {dre['looptools']:7.1e} | "
          f"{dim['packagex']:7.1e} {dim['looptools']:7.1e} {dim['collier']:7.1e}" + ("   <- disagrees: " + ",".join(bad) if bad else ""))
    rows.append([rs, cth, mu, v["s"], v["t"], tree(v["s"], v["t"]), re_ref, im_ref,
                 *(x for k in tools for x in (v[k].real, v[k].imag, dre[k], dim[k]))])


# %% [markdown]
# ## beta from the mu-dependence of the S-matrix element

# %%
print("\nbeta function from the mu-dependence of M1_phys (mu = 1/2 and 2), expected beta = -3/(4 (4 pi)^3) = %.10e:" % BETA)
betas = []
for rs in (2.5, 5.0, 10.0):
    for cth in (0.3, 0.9):
        s = rs * rs
        t = co[(rs, cth, 1.0)]["t"]
        u = 4 - s - t
        den = 2 * sum(1 / (x - 1) for x in (s, t, u))
        line = []
        for k in tools:
            src = co if k == "collier" else fc
            ph = {mu: src[(rs, cth, mu)][k].real + conversion6(s, t, mu) for mu in (0.5, 1.0, 2.0)}
            slope = (ph[2.0] - ph[0.5]) / (2 * math.log(2))
            lin = abs(ph[1.0] - (ph[2.0] + ph[0.5]) / 2) / abs(ph[1.0])   # M1_phys is linear in ln(mu)
            b = slope / den
            betas.append((rs, cth, k, b))
            line.append(f"{k} {b:+.10e} (rel. dev. {abs(b / BETA - 1):.1e}, linearity {lin:.0e})")
        print(f"  sqrt(s) = {rs:4.1f}, cos = {cth:.1f}: " + ";  ".join(line))
maxdev = max(abs(b / BETA - 1) for *_, b in betas)
print(f"  max relative deviation from Eq. (14): {maxdev:.1e}")


# %%
with open(os.path.join(HERE, "results", "scat6_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sqrts", "costheta", "mu", "s", "t", "tree", "re_ref_collier", "im_ref_unitarity",
                *(f"{c}_{k}" for k in tools for c in ("re", "im", "reldev_re", "reldev_im"))])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["sqrts", "costheta", "tool", "beta_from_amplitude", "beta_eq14"])
    for rs, cth, k, b in betas:
        w.writerow([rs, cth, k, b, BETA])


# %% [markdown]
# ## Figures

# %%
# ---------------- figures ----------------
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)

# (1) Re and Im of the MS-bar M1 at sqrt(s) = 5, mu = m, versus cos(theta): the same layout as figs/scat4_d4.pdf
scan = read(os.path.join(HERE, "results", "scat6_collier_scan.csv"), ["collier"])
cs = np.array(sorted(k[1] for k in scan))
col = np.array([scan[(5.0, round(c, 6), 1.0)]["collier"] for c in cs])
cu = np.linspace(0, 1, 21)
imu = np.array([im_unitarity(25, c, dps=15) for c in cu])
sig = 2 * math.sqrt(25 / 4 - 1) * 5 * float(sigma_tree6(25))
pts = [(5.0, c, 1.0) for c in (0.3, 0.9)]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 3.6), sharex=True)
ax1.plot(cs, 1e4 * col.real, color="k", lw=0.9, label="COLLIER")
ax2.plot(cs, 1e4 * col.imag, color="k", lw=0.9, label="COLLIER")
ax2.plot(cu, 1e4 * imu, color="#eb6235", lw=0.8, ls="--", label="unitarity")
ax2.plot([1], [1e4 * sig], "*", ms=7, color="#eb6235", label=r"$2p\sqrt{s}\,\sigma_{\rm tree}$")
for ax, part in ((ax1, np.real), (ax2, np.imag)):
    ax.plot([k[1] for k in pts], [1e4 * part(fc[k]["packagex"]) for k in pts], "o", ms=4.5, mfc="none",
            mec="#5d81b4", label="Package-X")
    ax.plot([k[1] for k in pts], [1e4 * part(fc[k]["looptools"]) for k in pts], "x", ms=4, color="#e09b24",
            label="LoopTools")
ax1.set_ylabel(r"$10^4\,\mathrm{Re}\,\mathcal{M}^{(1)}$")
ax2.set_ylabel(r"$10^4\,\mathrm{Im}\,\mathcal{M}^{(1)}$")
ax2.set_xlabel(r"$\cos\theta$")
ax1.legend(loc="lower left")
ax2.legend(loc="upper left", ncol=2)
ax1.set_title(r"$d=6$, $\sqrt{s}=5m$, $\mu=m$", fontsize=8)
fig.savefig(os.path.join(figdir, "scat6_d6.pdf"))


# %%
# (2) mu-dependence of the S-matrix element at sqrt(s) = 5, cos(theta) = 0.3
musc = read(os.path.join(HERE, "results", "scat6_collier_muscan.csv"), ["collier"])
mus = np.array(sorted(k[2] for k in musc))
t03 = musc[(5.0, 0.3, round(mus[0], 6))]["t"]
m0 = tree(25.0, t03)
ph = np.array([musc[(5.0, 0.3, round(mu, 6))]["collier"].real + conversion6(25.0, t03, mu) for mu in mus])
g2 = 1 / (1 - 2 * BETA * np.log(mus))            # one-loop running from g(m) = 1
fixed = m0 + ph
running = g2 * m0 + g2 ** 2 * ph
i1 = int(np.argmin(abs(mus - 1)))
fig, ax = plt.subplots(figsize=(3.25, 2.2))
ax.plot(mus, 1e3 * (fixed / fixed[i1] - 1), color="#5d81b4", lw=0.9, ls="--", label=r"$g$ fixed")
ax.plot(mus, 1e3 * (running / running[i1] - 1), color="k", lw=0.9, ls="-", label=r"$g(\mu)$, Eq. (14)")
ax.set_xscale("log")
ax.set_xticks([0.25, 0.5, 1, 2, 4])
ax.set_xticklabels(["1/4", "1/2", "1", "2", "4"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlabel(r"$\mu/m$")
ax.set_ylabel(r"$10^3\,\Delta\mathcal{M}_{\rm phys}/\mathcal{M}_{\rm phys}$")
ax.set_title(r"$d=6$, $\sqrt{s}=5m$, $\cos\theta=0.3$", fontsize=8)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "scat6_rg_d6.pdf"))
print(f"\nmu from 1/4 to 4 at sqrt(s) = 5m, cos = 0.3: relative change with g fixed {abs(fixed[-1] / fixed[0] - 1):.2e}, "
      f"with g(mu) {abs(running[-1] / running[0] - 1):.2e}")
print("wrote results/scat6_comparison.csv, figs/scat6_d6.pdf and figs/scat6_rg_d6.pdf")
