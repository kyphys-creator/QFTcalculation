# %% [markdown]
# # Appendix check: exact A_2..A_9 of the BPST instanton by the plane-wave (symbol) expansion modulo primes
#
# Research note models/qcd, derivations of the appendices (numpy, modular arithmetic).  app:inst 「大きい質量の展開。」 and the step (10)
# checks (「文献との食い違い。」): a third, independent route to the heat-kernel coefficients of -D^2 in the BPST background (isospin 1/2,
# rho = 1): no Fock-Schwinger gauge, no DeWitt recursion, no invariant basis.  tr a_n(x,x) = sum_k (-1)^k/k! sum_{|alpha| = 2(k-n)}
# (-1)^{k-n} w(alpha) tr[(Y^k)_alpha 1](x), Y = 2 p.D - D^2 (plane waves e^{ipx}, Gaussian moments w(alpha) of p), with D = d + calA as
# Taylor polynomials in y = x - x0, exactly modulo primes p < 2^30 (real 4x4 representation of the quaternion units, tr_2 = tr_4/2).
# (a) the floating-point version against the exact heat kernel of random constant potentials (N = 2, 3);
# (b) tr a_n(x0) mod p, n <= NMAX, at NMAX + 3 rational radii x0 = (r,0,0,0), two primes;
# (c) per n and prime: tr a_n = P_n(u)/(1+u)^(2n) (u = r^2) interpolated mod p on deg+1 radii and verified on the rest; A_n = (1/16)
#     sum_j p_j B(j+2, 2n-j-2) mod p, compared with the candidates: A_2..A_5 (exact), A_6 = 25624/571725 (FHSS = recursion) against the
#     literature 3958/444675, A_7, A_8 (recursion, deriv_inst_dewitt_modp.py 8) and A_9 = 40094573632/586396035225 (deriv_inst_dewitt_modp.py
#     9); also P_n against the recursion's pointwise polynomials (n <= 8).  Two primes ~2^30 identify the rationals beyond doubt.
# Argument: NMAX (default 6, also when run cell by cell; run_deriv_inst_a6_check.sh passes 9, about 17 minutes on 8 processes;
# the time grows steeply with NMAX).
# Writes work/inst_planewave/tr_a_mod_NMAX<NMAX>.json (the values mod p); run_deriv_inst_a6_check.sh saves the printed output as
# results/deriv_inst_planewave.txt (timings go to stderr).
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_planewave.py 9
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import json
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
NMAX = int(ARGS[0]) if ARGS else 6
NPRIMES, NPROC = 2, 8
PW_PRIMES = []
c = (1 << 30) - 1
while len(PW_PRIMES) < NPRIMES:
    if all(c % q for q in range(3, int(c ** 0.5) + 1, 2)):
        PW_PRIMES.append(c)
    c -= 2
radii = [Fr(0), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(4), Fr(1, 4), Fr(5, 4)][:NMAX + 3]
NMAX, PW_PRIMES, [str(r) for r in radii]          # inspect

# %% [markdown]
# ## (a) The floating-point plane-wave method against the exact heat kernel of constant potentials

# %%
if MAIN:
    nmax_c = 6
    yp = H.YPoly(2 * nmax_c)
    rng = np.random.default_rng(3)
    for N in [2, 3]:
        A = H.random_A(N, rng, herm=True, scale=0.6)
        Ac = []
        for mu in range(4):
            cc = np.zeros((yp.count[2 * nmax_c], N, N), dtype=complex)
            cc[0] = -1j * A[mu]
            Ac.append(cc)
        pw = H.heat_coeffs(Ac, N, nmax_c, yp)
        ex = H.exact_tr_a(A, nmax_c)
        print(f"(a) N = {N}:", "  ".join(f"n={n}: {abs(pw[n]-ex[n])/abs(ex[n]):.1e}" for n in range(1, nmax_c + 1) if abs(ex[n]) > 1e-12),
              f"(|a_1| = {abs(pw[1]):.1e})", flush=True)

# %% [markdown]
# ## (b) BPST, isospin 1/2: tr a_n(x0) mod p at rational radii (NMAX + 3 radii, two primes)

# %%
if MAIN:
    tasks = [(p, r, NMAX) for p in PW_PRIMES for r in radii]
    t0 = time.time()
    with Pool(NPROC) as pool:
        results = pool.map(H.pw_task, tasks, chunksize=1)
    print(f"(b) {len(tasks)} runs (NMAX = {NMAX}, {len(radii)} radii, primes {PW_PRIMES})", flush=True)
    print(f"    ({len(tasks)} runs in {time.time() - t0:.0f} s)", file=sys.stderr, flush=True)
    vals = {(p, r): v for p, r, v in results}
    os.makedirs(os.path.join(HERE, "work", "inst_planewave"), exist_ok=True)
    with open(os.path.join(HERE, "work", "inst_planewave", f"tr_a_mod_NMAX{NMAX}.json"), "w") as fh:     # tr_2 a_n mod p, per "p|r"
        json.dump({"primes": PW_PRIMES, "radii": [str(r) for r in radii], "tr_a_mod": {f"{p}|{r}": v for (p, r), v in vals.items()}}, fh)
vals[(PW_PRIMES[0], "0")] if MAIN else None          # inspect: tr a_0..a_NMAX mod p at r = 0

# %% [markdown]
# ## (c) P_n(u) mod p, A_n mod p, and the candidate rationals

# %%
DEW = {2: ["-8"], 3: ["192/5", "-256/5"], 4: ["-1248/7", "5120/7", "-2304/7"],
       5: ["6656/7", "-2430976/315", "650240/63", "-16384/7"],
       6: ["-327424/55", "38797312/495", "-305211392/1485", "1497088/11", "-204800/11"],
       7: ["30898176/715", "-2486411264/3003", "964026368/273", "-9779838976/2145", "1288404992/715", "-23592960/143"],
       8: ["-1789542912/5005", "2100563050496/225225", "-39334443999232/675675", "1270742024192/10395",
           "-335516418048/3575", "88120229888/3575", "-231211008/143"]}
CAND = {2: {"exact": Fr(-1, 12)}, 3: {"exact": Fr(1, 75)}, 4: {"exact": Fr(17, 735)}, 5: {"exact": Fr(-116, 2835)},
        6: {"FHSS = recursion": Fr(25624, 571725), "KLM/DHLM": Fr(3958, 444675)},
        7: {"recursion": Fr(-3267232, 96621525), "GY c10 = 0.87": None},
        8: {"recursion": Fr(132784, 131756625), "GY c12 = -2.2": None},
        9: {"recursion (NMAX = 9)": Fr(40094573632, 586396035225)}}


def interp_mod(us, vs, p):
    """polynomial coefficients through (us, vs) mod p (Lagrange)."""
    n = len(us)
    co = [0] * n
    for i in range(n):
        basis = [1]
        den = 1
        for j in range(n):
            if j == i:
                continue
            basis = [0] + basis
            for k in range(len(basis) - 1):
                basis[k] = (basis[k] - us[j] * basis[k + 1]) % p
            den = den * (us[i] - us[j]) % p
        f = vs[i] * H.modinv(den, p) % p
        for k in range(n):
            co[k] = (co[k] + f * basis[k]) % p
    return co


if MAIN:
    B = lambda a, b: Fr(math.factorial(a - 1) * math.factorial(b - 1), math.factorial(a + b - 1))
    for n in range(2, NMAX + 1):
        lines = []
        for p in PW_PRIMES:
            us = [H.frac_mod(r * r, p) for r in radii]
            ws = [vals[(p, str(r))][n] * pow((1 + u) % p, 2 * n, p) % p for r, u in zip(radii, us)]
            ok = None
            for deg in range(0, len(radii) - 2):
                co = interp_mod(us[:deg + 1], ws[:deg + 1], p)
                if all(sum(c_ * pow(u, j, p) for j, c_ in enumerate(co)) % p == w_ for u, w_ in zip(us, ws)):
                    ok = (deg, co)
                    break
            if ok is None:
                lines.append(f"  p = {p}: no polynomial of degree <= {len(radii) - 3} fits all {len(radii)} radii")
                continue
            deg, co = ok
            An = sum(c_ * H.frac_mod(B(j + 2, 2 * n - j - 2), p) for j, c_ in enumerate(co)) * H.modinv(16, p) % p
            msg = f"  p = {p}: P_n of degree {deg} (fitted on {deg + 1} radii, verified on {len(radii) - deg - 1} more)"
            if n in DEW:
                same = deg == len(DEW[n]) - 1 and all(H.frac_mod(Fr(c_), p) == co[j] for j, c_ in enumerate(DEW[n]))
                msg += f"; P_n == DeWitt-recursion polynomial mod p: {same}"
            for name, val in CAND.get(n, {}).items():
                if val is not None:
                    msg += f"; A_n == {name} {val}: {H.frac_mod(val, p) == An}"
            lines.append(msg)
        print(f"(c) n = {n}:\n" + "\n".join(lines), flush=True)
