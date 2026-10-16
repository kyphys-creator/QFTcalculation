# %% [markdown]
# # Appendix check: Gamma~''(u) and Gamma~'''(u) of the isospin-1/2 scalar by a high-precision Gel'fand-Yaglom calculation
#
# Research note models/qcd, derivations of the appendices (C, numpy, mpmath).  app:inst 「大きい質量の展開。」 and the step (10) checks
# (「文献との食い違い。」): the large-mass expansion Gamma~ = -(1/12) ln u + sum_k c_2k u^-k (u = (m rho)^2, rho = 1, c_2k = -Gamma(k) A_{k+2})
# has c8 = -51248/190575 by the heat-kernel recursion and -7916/148225 in the literature.  To decide numerically, this script computes the
# u-derivatives G_j = d^j Gamma~/du^j (j = 0..3) directly: per partial wave the mass correction of inst_gylib.py is integrated together with
# its first three u-derivatives (sensitivity equations, C code deriv_inst_gy_hp.c, fixed-step 8th-order Runge-Kutta), summed over l <= L with
# a fitted large-l tail.  G2 and G3 do not depend on the counterterms or on alpha(1/2) and are smooth in 1/u: the fits for c8, c10, ... are
# in deriv_inst_gy_hp_fit.py.  Error of each G_j: the spread over tail-fit variants, plus |base - chk| where the chk set exists.
# Sets: base (17 masses m rho = 2.5..10, L = 1500); chk (6 masses, L = 1000, other integration parameters K = 32, Z0 = 480, hfac = 0.5,
# hmax = 0.01, r0fac = 1e-5); small (6 masses m rho = 0.02..2, L = 1000).
# (a) sanity: group values at m = 4; the sensitivity equations against 5-point finite differences in u (error ~ h^4).
# (b) production; (c) G_0..G_3 with errors -> results/inst_gy_hp.csv; (d) Gamma~ = G_0 against results/inst_gy.csv (inst_gy.py) and the
# small-mass expansion (Hur-Lee-Min, through the u^2 ln^2 u terms) for G_0, G_1, G_2.
# Reads results/inst_gy.csv.  Writes work/inst_gy_hp/ (dop853coef.h, libgyd.dylib, data/*.npy) and results/inst_gy_hp.csv (columns m,
# G0..G3, dG0..dG3, chk = 1 where the chk set enters the error; rows m <= 2 from the small set, m >= 2.5 from the base set);
# run_deriv_inst_a6_check.sh saves the printed output as results/deriv_inst_gy_hp.txt (timings go to stderr).
# Argument: reuse = take the existing work/inst_gy_hp/data/*.npy instead of recomputing (cell by cell this is the default).
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_gy_hp.py   (about 20 minutes on 8 processes)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import os
import sys
import time
from multiprocessing import Pool
import numpy as np
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import deriv_inst_gy_hp_lib as G
MAIN = __name__ == "__main__"          # False in the worker processes of multiprocessing (spawn), which import this file
ARGS = sys.argv[1:] if not INTERACTIVE else []
REUSE = INTERACTIVE or "reuse" in ARGS
T = 0.5
NPROC = 8
CHK = {"K": 32, "Z0": 480, "hfac": 0.5, "hmax": 0.01, "r0fac": 1e-5}
SETS = [("base", 1500, [2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5, 5.5, 6, 6.5, 7, 8, 10], {}),
        ("chk", 1000, [2.5, 3, 4, 5, 6, 8], CHK),
        ("small", 1000, [0.02, 0.1, 0.5, 1, 1.5, 2], {})]

# %% [markdown]
# ## Build the C library (work/inst_gy_hp/)

# %%
if MAIN:
    print("build:", G.build())

# %% [markdown]
# ## (a) Sanity: group values at m = 4; sensitivity equations against finite differences in u

# %%
if MAIN:
    with np.printoptions(linewidth=200, precision=10):
        for n in (0, 1, 2, 3, 6):
            print(f"(a) n={n} m=4: {G.group(0.5, n, 4.0)[0]}")
        t, n, m = 0.5, 7, 4.0; u = m*m
        for hr in (1e-2, 5e-3, 2.5e-3):
            h = hr*u
            f = {k: G.group(t, n, np.sqrt(u + k*h))[0] for k in (-2, -1, 0, 1, 2)}
            fd = (f[-2] - 8*f[-1] + 8*f[1] - f[2])/(12*h)
            print(f"    FD h/u={hr}: rel diff d^(j+1) vs FD of d^(j): {(fd[:3]-f[0][1:])/np.abs(f[0][1:])}")
G.waves(0.5, 6)          # inspect: the two waves (degeneracy, type, l, k, c, t, A, B, C) of the group l = 3

# %% [markdown]
# ## (b) Production: the group values d_l^(j)(u), l = n/2 <= L, for the three sets (work/inst_gy_hp/data/)

# %%
if MAIN:
    os.makedirs(os.path.join(G.WORK, "data"), exist_ok=True)
    pool = None
    for tag, L, ms, kw in SETS:
        for m in ms:
            fn = G.datafile(T, float(m), L, tag)
            if REUSE and os.path.exists(fn):
                print(f"(b) t={T} m={float(m)} L={L} {tag} {kw}: reused {os.path.basename(fn)}", flush=True)
                continue
            if pool is None:
                pool = Pool(NPROC)
            t0 = time.time()
            d = G.compute(T, float(m), L, kw, pool)
            np.save(fn, d)
            print(f"(b) t={T} m={float(m)} L={L} {tag} {kw}: -> {os.path.basename(fn)}", flush=True)
            print(f"    ({tag} m = {m}: {time.time() - t0:.1f} s)", file=sys.stderr, flush=True)
    if pool is not None:
        pool.close(); pool.join()
np.load(G.datafile(T, 4.0, 1500, "base"))[:4] if MAIN else None          # inspect: m = 4, the groups l = 0, 1/2, 1, 3/2 (columns j = 0..3)

# %% [markdown]
# ## (c) G_j = d^j Gamma~/du^j with error estimates -> results/inst_gy_hp.csv

# %%
if MAIN:
    rows = []
    for tag, L in (("small", 1000), ("base", 1500)):
        ms = sorted(float(m) for s, LL, mm, kw in SETS if s == tag for m in mm)
        for m in ms:
            d = np.load(G.datafile(T, m, L, tag))
            g, e = G.analyse(d, T, m, L)
            chk = 0
            fc = G.datafile(T, m, 1000, "chk")
            if tag == "base" and os.path.exists(fc):
                dc = np.load(fc); Lc = (len(dc) - 1)//2
                gc, _ = G.analyse(dc, T, m, min(L, Lc))
                gb, _ = G.analyse(d, T, m, min(L, Lc))
                e = e + np.abs(gc - gb); chk = 1
            rows.append(f"{m:.6g}," + ",".join(f"{x:.16e}" for x in g) + "," + ",".join(f"{x:.3e}" for x in e) + f",{chk}")
            print(f"(c) {tag:5s} m={m:6.3f}: G = {g}  err = {e}  chk={chk}", flush=True)
    with open(os.path.join(HERE, "results", "inst_gy_hp.csv"), "w") as fh:
        fh.write("m,G0,G1,G2,G3,dG0,dG1,dG2,dG3,chk\n")
        fh.write("\n".join(rows) + "\n")
    print("    -> results/inst_gy_hp.csv")
rows[:3] if MAIN else None          # inspect: the first rows of the CSV

# %% [markdown]
# ## (d) Cross-checks: Gamma~ against inst_gy.csv; the small-mass expansion

# %%
if MAIN:
    EG = np.euler_gamma; AL = G.ALPHA[0.5]; C4 = -0.382727; a = 0.5 - EG + np.log(2)
    def small(u):
        lu = np.log(u)
        G0 = AL + u/2*(lu/2 - np.log(2) + EG + 0.5) + u*u*(-lu*lu/16 + a/4*lu + C4)
        G1 = 0.5*(lu/2 - np.log(2) + EG + 1) + u*(-lu*lu/8 + a/2*lu + 2*C4 - lu/8 + a/4)
        G2 = 1/(4*u) - lu*lu/8 + (a/2 - 3/8)*lu + 2*C4 + 0.75*a - 1/8
        return np.array([G0, G1, G2])
    rows = {float(r["m"]): r for r in csv.DictReader(open(os.path.join(HERE, "results", "inst_gy_hp.csv")))}
    old = {float(r["m_rho"]): r for r in csv.DictReader(open(os.path.join(HERE, "results", "inst_gy.csv")))}
    print("(d) (i) Gamma~ (this method, j = 0) vs inst_gy.csv")
    for m in sorted(rows):
        if m in old:
            g = float(rows[m]["G0"]); e = float(rows[m]["dG0"]); go = float(old[m]["Gamma_tilde"]); eo = float(old[m]["L_dependence"])
            print(f"  m={m:5.2f}: new {g:+.12f} (+- {e:.1e})  old {go:+.10f} (L-dep {eo:.1e})  diff {g-go:+.2e}")
    print("    (ii) small-mass expansion: G_j(num) - G_j(expansion)")
    for m in sorted(rows):
        if m <= 0.5:
            u = m*m; s = small(u)
            g = np.array([float(rows[m][k]) for k in ("G0", "G1", "G2")])
            print(f"  m={m:5.2f}: G0..2 = {g},  diff {g - s}")
