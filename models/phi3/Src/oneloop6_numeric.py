# %% [markdown]
# # Step (4): d = 6 one-loop finite parts against closed forms and the optical theorem
#
# d = 6 one-loop check, finite parts (research note, step (4)).
#
# MS-bar finite parts X_N of the D = 6 - 2 eps scalar integrals,
#     mu^(2 eps) I_N = i/(4 pi)^3 [c_N DeltaUV + X_N],   DeltaUV = 1/eps - gamma_E + ln 4 pi,
# at m = mu = 1 (note, App. H):
#   A0^(6) = -(m^4/2) (3/2 - ln m^2/mu^2) = -3/4
#   B0^(6)(p^2) = -(m^2 - p^2/6) + int_0^1 dx Delta ln(Delta - i0)/mu^2,   Delta = m^2 - x(1-x) p^2
#               = -m^2 + p^2/9 + (m^2/3) ln(m^2/mu^2) - (2/3)(m^2 - p^2/4) B0(p^2)   (closed form,
#                 with the d = 4 MS-bar B0 of App. G)
#   C0^(6) = int dF ln(Delta/mu^2)  (below threshold; above threshold only the tools are compared).
# Optical theorem: Im B0^(6) = pi p^2 beta^3 / 6 for p^2 > 4 m^2.
#
# Reads results/oneloop6_mathematica.csv (Package-X, LoopTools via the dimension shift) and
# results/oneloop6_collier.csv, writes results/oneloop6_comparison.csv and ../figs/b0_d6.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python oneloop6_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import mpmath as mp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
TOL = 1e-10          # agreement required (double-precision tools)


# %% [markdown]
# ## Reference values: closed forms (App. H) and Feynman-parameter integrals

# %%
def b0_closed(p2, m2=1, mu2=1):
    """d = 4 MS-bar B0(p^2; m, m) (App. G of the note; same as in oneloop4_numeric.py)."""
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


def b06_closed(p2, m2=1, mu2=1):
    p2, m2, mu2 = mp.mpf(p2), mp.mpf(m2), mp.mpf(mu2)
    return -m2 + p2 / 9 + m2 / 3 * mp.log(m2 / mu2) - mp.mpf(2) / 3 * (m2 - p2 / 4) * b0_closed(p2, m2, mu2)


def b06_feynman(p2, m2=1, mu2=1):
    p2, m2, mu2 = mp.mpf(p2), mp.mpf(m2), mp.mpf(mu2)
    a = lambda x: m2 - x * (1 - x) * p2
    pts = [0, mp.mpf(1) / 2, 1]
    if p2 > 4 * m2:
        beta = mp.sqrt(1 - 4 * m2 / p2)
        pts = [0, (1 - beta) / 2, mp.mpf(1) / 2, (1 + beta) / 2, 1]
    # Delta ln|Delta| -> 0 where Delta = 0; ln(Delta - i0) = ln|Delta| - i pi for Delta < 0
    re = mp.quad(lambda x: a(x) * mp.log(abs(a(x)) / mu2) if a(x) != 0 else 0, pts)
    im = mp.quad(lambda x: -mp.pi * a(x) if a(x) < 0 else 0, pts)
    return mp.mpc(-(m2 - p2 / 6) + re, im)


def c06_feynman(p1, p2, p3, m2=1, mu2=1):
    p1, p2, p3, m2, mu2 = map(mp.mpf, (p1, p2, p3, m2, mu2))
    f = lambda x1, x2: mp.log((m2 - x1 * x2 * p1 - x2 * (1 - x1 - x2) * p2 - x1 * (1 - x1 - x2) * p3) / mu2)
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
# Package-X and LoopTools through the dimension shift (oneloop6_feyncalc.wl), COLLIER (oneloop6_collier.f90).

# %%
mma = read(os.path.join(HERE, "results", "oneloop6_mathematica.csv"), ["packagex", "looptools"])
col = read(os.path.join(HERE, "results", "oneloop6_collier.csv"), ["collier"])


# %% [markdown]
# ## Comparison with the reference values

# %%
rows = []
closed_vs_feyn = []
print(f"{'func':4} {'args':>18} {'reference':>34} {'src':>9} | deviation  PX  LT  COLLIER")
for key in mma:
    func, a1, a2, a3 = key
    vals = dict(mma[key], **col[key])
    if func == "A06":
        ref, src = mp.mpc(mp.mpf(-3) / 4), "exact"
    elif func == "B06":
        ref, src = b06_closed(a1), "closed"
        feyn = b06_feynman(a1)
        closed_vs_feyn.append(float(abs(feyn - ref) / max(1, abs(ref))))
        assert closed_vs_feyn[-1] < 1e-15, (a1, feyn, ref)
    elif below_threshold(a1, a2, a3):
        ref, src = mp.mpc(c06_feynman(a1, a2, a3)), "Feynman"
    else:
        ref, src = mp.mpc(vals["packagex"]), "PX"
    # relative deviation; absolute where the reference vanishes (C0^(6)(0,0,0) = ln(m^2/mu^2)/2 = 0)
    scale = abs(ref) if abs(ref) > 0 else mp.mpf(1)
    dev = {k: (float(abs(mp.mpc(v) - ref) / scale) if not math.isnan(v.real) else float("nan"))
           for k, v in vals.items()}
    ok = {k: (d < TOL) for k, d in dev.items() if not math.isnan(d)}
    na = sorted(k for k, d in dev.items() if math.isnan(d))
    refc = complex(ref)
    print(f"{func:4} {str((a1, a2, a3)):>18} {refc.real:+.15f}{refc.imag:+.15f}i {src:>9} | "
          f"{dev['packagex']:9.1e} {dev['looptools']:9.1e} {dev['collier']:9.1e}"
          + ("" if all(ok.values()) else "   <- disagrees: " + ",".join(k for k, v in ok.items() if not v))
          + ("   (" + ",".join(na) + ": no value)" if na else ""))
    rows.append([func, a1, a2, a3, src, refc.real, refc.imag,
                 *(x for k in ("packagex", "looptools", "collier") for x in (vals[k].real, vals[k].imag, dev[k]))])

print(f"\nB0^(6) closed form vs Feynman-parameter integral: max rel. difference {max(closed_vs_feyn):.1e}")

# %% [markdown]
# ## Optical theorem: Im B0^(6) = pi p^2 beta^3 / 6 above threshold

# %%
print("\noptical theorem, p^2 > 4 m^2:  Im B0^(6) / (pi p^2 beta^3 / 6) for Package-X, LoopTools, COLLIER")
for key in mma:
    func, a1 = key[0], key[1]
    if func == "B06" and a1 > 4:
        expect = float(mp.pi * a1 * mp.sqrt(1 - 4 / mp.mpf(a1)) ** 3 / 6)
        v = dict(mma[key], **col[key])
        print(f"  p^2 = {a1:5}: {v['packagex'].imag / expect:.15f} {v['looptools'].imag / expect:.15f} "
              f"{v['collier'].imag / expect:.15f}")


# %%
with open(os.path.join(HERE, "results", "oneloop6_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg1", "arg2", "arg3", "reference_source", "re_ref", "im_ref",
                "re_packagex", "im_packagex", "dev_packagex", "re_looptools", "im_looptools", "dev_looptools",
                "re_collier", "im_collier", "dev_collier"])
    w.writerows(rows)


# %% [markdown]
# ## Figure: Re and Im of B0^(6)(p^2; m, m)

# %%
# ---------------- figure: Re and Im of B0^(6)(p^2; m, m) ----------------
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
x = np.concatenate([np.linspace(-10, 3.999, 400), np.linspace(4.0, 30, 400)])
b6 = np.array([complex(b06_closed(v)) for v in x])
pts = sorted(k for k in mma if k[0] == "B06")
px = np.array([k[1] for k in pts])
get = lambda src, d: np.array([d[k][src] for k in pts])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 3.6), sharex=True)
for ax, part in ((ax1, np.real), (ax2, np.imag)):
    ax.plot(x, part(b6), color="k", lw=0.9, ls="-", label="closed form")
    ax.plot(px, part(get("packagex", mma)), "o", ms=4.5, mfc="none", mec="#5d81b4", label="Package-X")
    ax.plot(px, part(get("looptools", mma)), "x", ms=4, color="#e09b24", label="LoopTools")
    ax.plot(px, part(get("collier", col)), "+", ms=6, color="#8eb031", label="COLLIER")
    ax.axvline(4, color="0.6", lw=0.5, ls=":")
xo = x[x >= 4]
opt, = ax2.plot(xo, np.pi * xo * np.sqrt(1 - 4 / xo) ** 3 / 6, color="#eb6235", lw=0.8, ls="--",
                label=r"$\pi p^2\beta^3/6$")
ax1.set_ylabel(r"$\mathrm{Re}\,B_0^{(6)}(p^2;m,m)$")
ax2.set_ylabel(r"$\mathrm{Im}\,B_0^{(6)}(p^2;m,m)$")
ax2.set_xlabel(r"$p^2/m^2$")
ax2.legend(loc="upper left")      # all symbols; the upper panel has no free corner
ax2.text(4.6, 5.0, r"$p^2=4m^2$", fontsize=7)
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)
fig.savefig(os.path.join(figdir, "b0_d6.pdf"))
print("\nwrote results/oneloop6_comparison.csv and figs/b0_d6.pdf")
