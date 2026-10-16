# %% [markdown]
# # Appendix check: the FHSS heat-kernel coefficients O_2..O_6, validated on constant potentials and evaluated exactly on BPST
#
# Research note models/qcd, derivations of the appendices (numpy, exact rational arithmetic).  app:inst 「大きい質量の展開。」 and the
# step (10) checks (「文献との食い違い。」): A_2..A_6 of -D^2 in the BPST background (rho = 1) from the general formula of Fliegner, Haberl,
# Schmidt and Schubert (hep-th/9707189, minimal basis, tr a_n = (-1)^n O_n/n!), independently of the DeWitt recursion.
# (a) the LaTeX source of hep-th/9707189 (downloaded into work/arxiv/ when missing; data only) is parsed: O_1..O_6, the V-free terms
#     (V = E = 0 here), and a LaTeX round trip of every block;
# (b) the transcription against the exact heat kernel of random constant non-commuting potentials (N = 2..5, d = 4, 5, 6), n = 2..6;
# (c) rank tests: the values of the V-free basis invariants on random constant gl(N) potentials determine every coefficient when the rank is
#     full (O_5: rank 33 of 36 in d = 4, 36 in d = 5; O_6: 300 of 300 in d = 6), and least squares re-derives the FHSS coefficients;
# (d) exact BPST densities of every V-free invariant of O_2..O_6 at 14 rational radii, isospin 1/2 and 1 (covariant Taylor data of G_{mu nu},
#     exact contractions mod primes + CRT); SO(4) check (same radius, different direction);
# (e) each density is P(u)/(1+u)^(2n) exactly (u = r^2; interpolation on the first deg+1 radii, verified on the rest); exact integrals:
#     A_2..A_6 = -1/12, 1/75, 17/735, -116/2835, 25624/571725 (t = 1/2) and -1/3, 4/75, 208/735, -9248/19845, 245888/1715175 (t = 1);
# (f) the three combinations of O_5 invisible to the d = 4 constant-field test have nonzero BPST integrals (so d = 5 is needed).
# Reads the arXiv source (work/arxiv/hep-th_9707189/).  Writes nothing else; run_deriv_inst_a6_check.sh saves the printed output as
# results/deriv_inst_fhss.txt (timings go to stderr).
# Argument: norank6 = skip the O_6 rank test in d = 6 (it is also skipped cell by cell; set RANK6 = True to run it there).
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python -I deriv_inst_fhss.py   (about 90 minutes: the O_6 rank test in d = 6,
# 320 configurations at about a minute each, on 8 processes; about 2 minutes without it)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import math
import os
import sys
import time
from fractions import Fraction as Fr
from multiprocessing import Pool
import numpy as np
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
MAIN = __name__ == "__main__"          # False in the worker processes of multiprocessing (spawn), which import this file
sys.path.insert(0, HERE)
import deriv_inst_hk_lib as H
ARGS = sys.argv[1:] if not INTERACTIVE else []
NPROC = 8
RANK6 = not INTERACTIVE and "norank6" not in ARGS    # the O_6 rank test in d = 6 (about 90 minutes on 8 processes)

# %% [markdown]
# ## (a) The FHSS coefficients O_1..O_6 from the arXiv source

# %%
if MAIN:
    O, lines = H.load_fhss()
    print("(a) " + "\n    ".join(lines))
    terms = {n: [t for t in O[n] if all(f[0] == "F" for f in t["factors"])] for n in range(2, 7)}
O[4][:3] if MAIN else None          # inspect: the first terms of O_4 (F_{klm..} = D_k D_l .. F_{..}, index letters k l m n r s t)

# %% [markdown]
# ## (b) Constant non-commuting potentials: FHSS against the exact heat kernel

# %%
if MAIN:
    ev = {n: H.FHSSEval(O[n]) for n in range(2, 7)}
    maxrank = max(len(f[1]) for n in ev for t in ev[n].terms for f in t["factors"])
    print("(b) max rank of F tensors:", maxrank)
    rng = np.random.default_rng(1)
    worst = {n: 0 for n in range(2, 7)}
    for (N, herm, d) in [(2, True, 4), (3, True, 4), (3, False, 4), (4, True, 4), (5, False, 4), (3, False, 5), (3, True, 6)]:
        for rep in range(2):
            A = H.random_A(N, rng, herm=herm, scale=0.7, d=d)
            ex = H.exact_tr_a(A, 6)
            T = H.fhss_tensors(A, maxrank)
            line = []
            for n in range(2, 7):
                f = (-1) ** n / math.factorial(n) * ev[n].total(T)
                rd = abs(f - ex[n]) / abs(ex[n])
                worst[n] = max(worst[n], rd)
                line.append(f"n={n}: exact {ex[n].real:+.10e}{ex[n].imag:+.1e}i  FHSS {f.real:+.10e}{f.imag:+.1e}i  rel.diff {rd:.1e}")
            print(f"N={N} herm={herm} d={d} rep={rep}")
            print("   " + "\n   ".join(line), flush=True)
    print("worst relative differences:", {n: f"{v:.1e}" for n, v in worst.items()})

# %% [markdown]
# ## (c) Rank of the constant-field evaluation map; least-squares re-derivation of the coefficients

# %%
def rank_test(n, N, nconf, dim):
    t0 = time.time()
    os.environ["OPENBLAS_NUM_THREADS"] = "1"          # one BLAS thread per worker process (the values do not depend on it)
    with Pool(NPROC, initializer=H.rank_init, initargs=(O[n], n, N, dim)) as pool:
        res = pool.map(H.rank_work, [1000 * N + 17 * dim + c for c in range(nconf)], chunksize=1)
    print(f"    (rank test O_{n}, N = {N}, d = {dim}: {time.time() - t0:.0f} s)", file=sys.stderr, flush=True)
    M = np.array([r[0] for r in res])
    b = np.array([r[1] for r in res])
    ev = H.FHSSEval(O[n])
    sc = np.linalg.norm(M, axis=0)
    s = np.linalg.svd(M / sc, compute_uv=False)
    rank = int(np.sum(s > s[0] * 1e-9))
    print(f"O_{n}: {len(ev.terms)} V-free basis invariants, N = {N}, d = {dim}, {nconf} configurations")
    print("singular values: largest %.3e, smallest five %s" % (s[0], " ".join("%.2e" % x for x in s[-5:])))
    print("numerical rank (tol 1e-9):", rank)
    x, *_ = np.linalg.lstsq(M / sc, b, rcond=None)
    x = x / sc
    coef = np.array([complex(c) for c in ev.coef])
    print("max |least-squares coefficient - FHSS coefficient| = %.2e  (max |FHSS coefficient| = %.2e)"
          % (np.max(np.abs(x - coef)), np.max(np.abs(coef))))
    print("max residual of FHSS formula relative to |O_n|: %.2e" % np.max(np.abs(M @ coef - b) / np.abs(b)), flush=True)
    return M

if MAIN:
    print("(c) rank tests")
    M5d4 = rank_test(5, 8, 80, 4)
    rank_test(5, 8, 80, 5)
    if RANK6:
        rank_test(6, 6, 320, 6)
    else:
        print("O_6 in d = 6: skipped (RANK6 = False; cell by cell or with the argument norank6)")
M5d4.shape if MAIN else None          # inspect: (configurations, invariants) of O_5 in d = 4

# %% [markdown]
# ## (d) Exact BPST densities of the FHSS invariants at rational radii; SO(4) check

# %%
if MAIN:
    jmax = max(len(f[1]) for n in terms for t in terms[n] for f in t["factors"]) - 2
    radii = [Fr(0), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(4, 3), Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(4), Fr(5), Fr(7), Fr(9)]
    dens = {}
    t0 = time.time()
    for iso in ["1/2", "1"]:
        dens[iso] = {n: [] for n in range(2, 7)}
        for r in radii:
            Ex = H.ExactTerms(H.bpst_jets([r, 0, 0, 0], jmax), iso)
            for n in range(2, 7):
                dens[iso][n].append([Ex.value(t) for t in terms[n]])
        print(f"(d) iso {iso}: exact densities of {sum(len(terms[n]) for n in terms)} invariants at {len(radii)} radii", flush=True)
        print(f"    (iso {iso}: {time.time() - t0:.0f} s)", file=sys.stderr, flush=True)
    for xa, xb in [([Fr(3, 2), 0, 0, 0], [Fr(1, 2), Fr(1), Fr(1), 0]), ([Fr(1), 0, 0, 0], [Fr(1, 2)] * 4)]:
        Ra = H.ExactTerms(H.bpst_jets(xa, jmax), "1/2")
        Rb = H.ExactTerms(H.bpst_jets(xb, jmax), "1/2")
        nd = sum(1 for n in range(2, 7) for t in terms[n] if Ra.value(t) != Rb.value(t))
        print(f"    SO(4) check x0 = {[str(v) for v in xa]} vs {[str(v) for v in xb]}: {nd} of {sum(len(terms[n]) for n in terms)} invariant densities differ", flush=True)
[str(v) for v in dens["1/2"][2][0]] if MAIN else None          # inspect: the O_2 densities (tr F_kl F_lk) at r = 0, isospin 1/2

# %% [markdown]
# ## (e) Exact integrals: A_2..A_6 for isospin 1/2 and 1

# %%
if MAIN:
    Jint = {}
    for iso in ["1/2", "1"]:
        Jint[iso] = {}
        for n in range(2, 7):
            J = []
            dens_total = [Fr(0)] * len(radii)
            for i, t in enumerate(terms[n]):
                vals = [row[i] for row in dens[iso][n]]
                c, integ = H.fit_integrate(radii, vals, 2 * n)
                J.append(integ)
                for k in range(len(radii)):
                    dens_total[k] += Fr(t["num"], t["den"]) * vals[k]
            On = sum(Fr(t["num"], t["den"]) * j for t, j in zip(terms[n], J))   # int O_n d^4x / pi^2
            An = Fr((-1) ** n, math.factorial(n)) * On / 16
            ctot, itot = H.fit_integrate(radii, [Fr((-1) ** n, math.factorial(n)) * v for v in dens_total], 2 * n)
            assert itot / 16 == An
            Jint[iso][n] = J
            g = Fr(math.factorial(n - 3)) * An if n >= 3 else None
            print(f"(e) iso {iso}  n = {n}: A_n = {An} = {float(An):.12f}"
                  + (f";  m^-{2*n-4} coefficient -Gamma(n-2) A_n = {-g} = {float(-g):.10f}" if g is not None else "")
                  + f"\n      FHSS-form tr a_n density = P(u)/(1+u)^{2*n}, P = {[str(x) for x in ctot]}")

# %% [markdown]
# ## (f) The kernel of the d = 4 constant-field map of O_5 on BPST

# %%
if MAIN:
    sc = np.linalg.norm(M5d4, axis=0)
    U, S, Vt = np.linalg.svd(M5d4 / sc)
    rank = int((S > S[0] * 1e-9).sum())
    K = (Vt[rank:].conj() / sc).T
    print(f"(f) O_5: rank {rank} of {M5d4.shape[1]} in d = 4; kernel dim {K.shape[1]} (max |M K| relative {np.abs(M5d4 @ K).max() / np.abs(M5d4).max() / np.abs(K).max():.0e})")
    for iso in ["1/2", "1"]:
        J = np.array([float(x) for x in Jint[iso][5]])
        v = J @ K
        s = np.abs(K * J[:, None]).sum(axis=0)
        print(f"  iso {iso}: BPST integral of each kernel vector / sum of |terms|: {np.array2string(np.abs(v) / s, precision=2)}")
