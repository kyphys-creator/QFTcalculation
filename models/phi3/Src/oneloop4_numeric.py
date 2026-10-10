# %% [markdown]
# # Step (3): d = 4 one-loop finite parts against closed forms and the optical theorem
#
# d = 4 one-loop check, finite parts (research note, step (3)).
#
# Reference values: MS-bar finite parts at m = mu = 1 (DeltaUV = 1/eps - gamma_E + ln 4 pi subtracted;
# the same as LoopTools' Delta = 0 and COLLIER's Delta_UV = 0):
#   A0 = m^2 (1 - ln m^2/mu^2) = 1
#   B0(p^2) closed form (Appendix G of the note), cross-checked by the Feynman-parameter integral
#       B0 = - int_0^1 dx ln(m^2 - x(1-x) p^2 - i0)
#   C0 below threshold: C0 = - int dF 1/Delta,  Delta = m^2 - x1 x2 p1^2 - x2 x3 p2^2 - x1 x3 p3^2
#   (above threshold only the tools are compared with each other).
# Optical theorem: Im B0 = pi beta for p^2 > 4 m^2, beta = sqrt(1 - 4 m^2/p^2).
#
# Reads results/oneloop4_mathematica.csv (Package-X, LoopTools) and results/oneloop4_collier.csv,
# writes results/oneloop4_comparison.csv and ../figs/b0_d4.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python oneloop4_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import os
import sys

import mpmath as mp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
TOL = 1e-10          # relative agreement required (double-precision tools)


# %% [markdown]
# ## Reference values: closed forms and Feynman-parameter integrals

# %%
def b0_closed(p2, m2=1, mu2=1):
    p2, m2, mu2 = mp.mpf(p2), mp.mpf(m2), mp.mpf(mu2)
    base = 2 - mp.log(m2 / mu2)
    if p2 < 0:
        beta = mp.sqrt(1 - 4 * m2 / p2)
        return base + beta * mp.log((beta - 1) / (beta + 1))
    if p2 == 0:
        return -mp.log(m2 / mu2)
    if p2 < 4 * m2:
        bt = mp.sqrt(4 * m2 / p2 - 1)
        return base - 2 * bt * mp.atan(1 / bt)
    if p2 == 4 * m2:
        return base
    beta = mp.sqrt(1 - 4 * m2 / p2)
    return base + beta * mp.log((1 - beta) / (1 + beta)) + 1j * mp.pi * beta


def b0_feynman(p2, m2=1, mu2=1):
    p2, m2, mu2 = mp.mpf(p2), mp.mpf(m2), mp.mpf(mu2)
    a = lambda x: m2 - x * (1 - x) * p2
    pts = [0, mp.mpf(1) / 2, 1]          # x = 1/2 is the log singularity at p^2 = 4 m^2
    if p2 > 4 * m2:
        beta = mp.sqrt(1 - 4 * m2 / p2)
        pts = [0, (1 - beta) / 2, mp.mpf(1) / 2, (1 + beta) / 2, 1]
    # a(x) = 0 only at isolated points (integrable log singularity); give them weight 0
    re = -mp.quad(lambda x: mp.log(abs(a(x)) / mu2) if a(x) != 0 else 0, pts)
    # ln(a - i0) = ln|a| - i pi for a < 0, so -int ln(...) has imaginary part +pi * (length where a < 0)
    im = mp.quad(lambda x: mp.pi if a(x) < 0 else 0, pts)
    return mp.mpc(re, im)


def c0_feynman(p1, p2, p3, m2=1):
    p1, p2, p3, m2 = map(mp.mpf, (p1, p2, p3, m2))
    f = lambda x1, x2: -1 / (m2 - x1 * x2 * p1 - x2 * (1 - x1 - x2) * p2 - x1 * (1 - x1 - x2) * p3)
    return mp.quad(lambda x1: mp.quad(lambda x2: f(x1, x2), [0, 1 - x1]), [0, 1])


def below_threshold(p1, p2, p3, m2=1):
    return max(p1, p2, p3) < 4 * m2


def read(path, cols):
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (r["func"], round(float(r["arg1"]), 6), round(float(r["arg2"]), 6), round(float(r["arg3"]), 6))
            out[key] = {c: complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols}
    return out


# %% [markdown]
# ## The tool values
# Package-X and LoopTools through FeynCalc (oneloop4_feyncalc.wl), COLLIER (oneloop4_collier.f90).

# %%
mma = read(os.path.join(HERE, "results", "oneloop4_mathematica.csv"), ["packagex", "looptools"])
col = read(os.path.join(HERE, "results", "oneloop4_collier.csv"), ["collier"])


# %% [markdown]
# ## Comparison with the reference values
# Relative deviations; LoopTools' C0 below threshold is wrong (step (3)).

# %%
rows = []
closed_vs_feyn = []
print(f"{'func':4} {'args':>18} {'reference':>34} {'src':>9} | rel. deviation  PX  LT  COLLIER")
for key in mma:
    func, a1, a2, a3 = key
    vals = dict(mma[key], **col[key])
    if func == "A0":
        ref, src = mp.mpc(1), "exact"
    elif func == "B0":
        ref, src = b0_closed(a1), "closed"
        feyn = b0_feynman(a1)
        # closed form vs Feynman-parameter integral (30-digit quadrature; ~1e-17 at the threshold,
        # where the log singularity sits inside the interval)
        closed_vs_feyn.append(float(abs(feyn - ref) / max(1, abs(ref))))
        assert closed_vs_feyn[-1] < 1e-15, (a1, feyn, ref)
    elif below_threshold(a1, a2, a3):
        ref, src = mp.mpc(c0_feynman(a1, a2, a3)), "Feynman"
    else:
        ref, src = mp.mpc(vals["packagex"]), "PX"
    dev = {k: float(abs(mp.mpc(v) - ref) / max(abs(ref), mp.mpf("1e-300"))) for k, v in vals.items()}
    # COLLIER returns the sentinel 1e50 for C0 at exactly zero external momenta
    # (ErrOut: 'C0reg_coli: case not implemented'); such entries are reported, not judged.
    na = {k for k, v in vals.items() if abs(v) >= 1e49}
    ok = {k: (d < TOL) for k, d in dev.items() if k not in na}
    refc = complex(ref)
    print(f"{func:4} {str((a1, a2, a3)):>18} {refc.real:+.15f}{refc.imag:+.15f}i {src:>9} | "
          f"{dev['packagex']:9.1e} {dev['looptools']:9.1e} {dev['collier']:9.1e}"
          + ("" if all(ok.values()) else "   <- disagrees: " + ",".join(k for k, v in ok.items() if not v))
          + ("   (" + ",".join(sorted(na)) + ": not implemented, sentinel 1e50)" if na else ""))
    rows.append([func, a1, a2, a3, src, refc.real, refc.imag,
                 *(x for k in ("packagex", "looptools", "collier") for x in (vals[k].real, vals[k].imag, dev[k]))])

print(f"\nB0 closed form vs Feynman-parameter integral: max rel. difference {max(closed_vs_feyn):.1e}")

# %% [markdown]
# ## Optical theorem: Im B0 = pi beta above threshold

# %%
# optical theorem: Im B0 = pi beta above threshold
print("\noptical theorem, p^2 > 4 m^2:  Im B0 / (pi beta) for Package-X, LoopTools, COLLIER")
for key in mma:
    func, a1 = key[0], key[1]
    if func == "B0" and a1 > 4:
        pib = float(mp.pi * mp.sqrt(1 - 4 / mp.mpf(a1)))
        v = dict(mma[key], **col[key])
        print(f"  p^2 = {a1:5}: {v['packagex'].imag / pib:.15f} {v['looptools'].imag / pib:.15f} {v['collier'].imag / pib:.15f}")


# %%
with open(os.path.join(HERE, "results", "oneloop4_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg1", "arg2", "arg3", "reference_source", "re_ref", "im_ref",
                "re_packagex", "im_packagex", "reldev_packagex", "re_looptools", "im_looptools", "reldev_looptools",
                "re_collier", "im_collier", "reldev_collier"])
    w.writerows(rows)


# %% [markdown]
# ## Figure: Re and Im of B0(p^2; m, m)

# %%
# ---------------- figure: Re and Im of B0(p^2; m, m) ----------------
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
x = np.concatenate([np.linspace(-10, 3.999, 400), np.linspace(4.0, 30, 400)])
b0 = np.array([complex(b0_closed(v)) for v in x])
pts = sorted(k for k in mma if k[0] == "B0")
px = np.array([k[1] for k in pts])
get = lambda src, d: np.array([d[k][src] for k in pts])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 3.6), sharex=True)
for ax, part in ((ax1, np.real), (ax2, np.imag)):
    ax.plot(x, part(b0), color="k", lw=0.9, ls="-", label="closed form")
    ax.plot(px, part(get("packagex", mma)), "o", ms=4.5, mfc="none", mec="#5d81b4", label="Package-X")
    ax.plot(px, part(get("looptools", mma)), "x", ms=4, color="#e09b24", label="LoopTools")
    ax.plot(px, part(get("collier", col)), "+", ms=6, color="#8eb031", label="COLLIER")
    ax.axvline(4, color="0.6", lw=0.5, ls=":")
pib, = ax2.plot(x[x >= 4], np.pi * np.sqrt(1 - 4 / x[x >= 4]), color="#eb6235", lw=0.8, ls="--", label=r"$\pi\beta$")
ax1.set_ylabel(r"$\mathrm{Re}\,B_0(p^2;m,m)$")
ax2.set_ylabel(r"$\mathrm{Im}\,B_0(p^2;m,m)$")
ax2.set_xlabel(r"$p^2/m^2$")
ax1.legend(loc="upper right")
ax2.legend(handles=[pib], loc="lower right")
ax2.text(5.0, 0.3, r"$p^2=4m^2$", fontsize=7)
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)
fig.savefig(os.path.join(figdir, "b0_d4.pdf"))
print("\nwrote results/oneloop4_comparison.csv and figs/b0_d4.pdf")
