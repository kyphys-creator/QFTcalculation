# %% [markdown]
# # Appendix check: exact heat-kernel coefficients A_n of the BPST instanton in modular arithmetic
#
# Research note models/qcd, derivations of the appendices (numpy, sympy).  app:inst 「大きい質量の展開。」 (N2b, N2c): EXACT heat-kernel
# coefficients A_n (n <= NMAX) of -D^2 in the BPST background (isospin 1/2, rho = 1) by the same Fock-Schwinger-gauge DeWitt recursion as
# deriv_inst_dewitt_num.py, done in modular arithmetic (F_p with p = 1 mod 4, i = sqrt(-1) mod p) at the integer points r = 0..NMAX;
# tr a_n(0) (1+r^2)^(2n) = P_n(r^2) with deg P_n <= n-2 is interpolated mod p (the extra points check the degree),
# A_n = (1/16) sum_k c_k (k+1)! (2n-3-k)!/(2n-1)!, and the rational number is recovered by CRT + rational reconstruction (four primes;
# three primes give the same).  Result: A_2..A_5 = -1/12, 1/75, 17/735, -116/2835 (literature), A_6 = 25624/571725 (the literature
# m^-8 coefficient -7916/148225 of inst_gy.py corresponds to A_6 = 3958/444675), A_7, A_8.
# Argument: NMAX (default 6, also when run cell by cell; run_deriv_check.sh passes 8, whose output contains those of 6 and 7).
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_dewitt_modp.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_dewitt_modp.py 8   (about 4 minutes with 8)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import itertools, math
import sys
import numpy as np
from sympy import nextprime, sqrt_mod
from sympy.ntheory.modular import crt
from fractions import Fraction
INTERACTIVE = "ipykernel" in sys.modules
ARGS = sys.argv[1:] if "ipykernel" not in sys.modules else []      # cell by cell (IPython kernel): the default NMAX
NMAX = int(ARGS[0]) if ARGS else 6
K = 2*NMAX

# %% [markdown]
# ## Monomials of degree <= 2 NMAX and the product table

# %%
MON = sorted({e for d in range(K + 1) for e in itertools.product(range(d + 1), repeat=4) if sum(e) == d}, key=lambda e: (sum(e), e))
IDX = {e: i for i, e in enumerate(MON)}; M = len(MON); DEG = np.array([sum(e) for e in MON])
pi_, pj_, pk_ = [], [], []
for i, a in enumerate(MON):
    for j, b in enumerate(MON):
        if DEG[i] + DEG[j] <= K:
            pi_.append(i); pj_.append(j); pk_.append(IDX[tuple(x + y for x, y in zip(a, b))])
PI, PJ, PK = np.array(pi_), np.array(pj_), np.array(pk_)
DER = []
for mu in range(4):
    src, dst, fac = [], [], []
    for i, e in enumerate(MON):
        if e[mu] > 0:
            f = list(e); f[mu] -= 1; src.append(i); dst.append(IDX[tuple(f)]); fac.append(e[mu])
    DER.append((np.array(src), np.array(dst), np.array(fac, dtype=np.int64)))
NMAX, M, len(PI)          # inspect: NMAX, the number of monomials and of products

# %% [markdown]
# ## The DeWitt recursion modulo p

# %%
def run(p):
    ii = int(sqrt_mod(p - 1, p))
    inv = lambda a: pow(int(a) % p, p - 2, p)
    def pmul(a, b):
        d = a.shape[0]; out = np.zeros((d, d, M), dtype=np.int64)
        for i in range(d):
            for j in range(d):
                acc = np.zeros(M, dtype=np.int64)
                for m in range(d):
                    if not (a[i, m].any() and b[m, j].any()): continue
                    prod = (a[i, m][PI]*b[m, j][PJ]) % p
                    np.add.at(acc, PK, prod)
                out[i, j] = acc % p
        return out
    def pder(P, mu):
        src, dst, fac = DER[mu]; out = np.zeros_like(P); out[:, :, dst] = (P[:, :, src]*fac) % p; return out
    def trunc(P, k):
        return P*(DEG <= k)
    def const(Mat):
        d = Mat.shape[0]; P = np.zeros((d, d, M), dtype=np.int64); P[:, :, 0] = np.array(Mat, dtype=np.int64) % p; return P
    def mono(mu, d):
        P = np.zeros((d, d, M), dtype=np.int64); e = [0]*4; e[mu] = 1; P[:, :, IDX[tuple(e)]] = np.eye(d, dtype=np.int64); return P
    def smul(c, P):
        return (P*(int(c) % p)) % p
    eps3 = np.zeros((3, 3, 3), dtype=np.int64); eps3[0, 1, 2] = eps3[1, 2, 0] = eps3[2, 0, 1] = 1; eps3[0, 2, 1] = eps3[2, 1, 0] = eps3[1, 0, 2] = -1
    eta = np.zeros((3, 4, 4), dtype=np.int64)
    for a in range(3):
        eta[a, :3, :3] = eps3[a]; eta[a, a, 3] = 1; eta[a, 3, a] = -1
    h = inv(2)
    T = [np.array([[0, h], [h, 0]]), np.array([[0, (-ii*h) % p], [(ii*h) % p, 0]]), np.array([[h, 0], [0, (-h) % p]])]
    Id = np.eye(2, dtype=np.int64)
    def tr_an(r):
        w = (smul(2*r, mono(0, 1)) + sum(pmul(mono(m, 1), mono(m, 1)) for m in range(4))) % p
        ic = inv(r*r + 1)
        f = const(np.array([[ic]])); term = f.copy()
        for k in range(1, K + 1):
            term = pmul(term, smul(-ic, w)); f = (f + term) % p
        X = [(const(np.array([[r]])) + mono(0, 1)) % p if m == 0 else mono(m, 1) for m in range(4)]
        A = []
        for mu in range(4):
            s = np.zeros((2, 2, M), dtype=np.int64)
            for a in range(3):
                for nu in range(4):
                    if eta[a, mu, nu] == 0: continue
                    xf = pmul(X[nu], f)[0, 0]
                    s = (s + (2*int(eta[a, mu, nu]) % p)*((T[a][:, :, None]*xf[None, None]) % p)) % p
            A.append(s)
        yA = sum(pmul(mono(m, 2), A[m]) for m in range(4)) % p
        parts = [yA*(DEG == j) for j in range(K + 1)]
        Phi_k = [const(Id)]
        for k in range(1, K + 1):
            Phi_k.append(smul(ii*inv(k), sum(pmul(parts[j], Phi_k[k - j]) for j in range(1, k + 1)) % p))
        Phi = sum(Phi_k) % p
        Inv_k = [const(Id)]
        for k in range(1, K + 1):
            Inv_k.append(smul(-1, sum(pmul(Inv_k[j], Phi_k[k - j]) for j in range(0, k)) % p))
        Phinv = sum(Inv_k) % p
        Ap = [trunc((pmul(Phinv, pmul(A[m], Phi)) + smul(ii, pmul(Phinv, pder(Phi, m)))) % p, K - 1) for m in range(4)]
        chk = int(np.max(trunc(sum(pmul(mono(m, 2), Ap[m]) for m in range(4)) % p, K - 1)))
        divA = sum(pder(Ap[m], m) for m in range(4)) % p
        AA = sum(pmul(Ap[m], Ap[m]) for m in range(4)) % p
        a_prev = const(Id); res = []
        for n in range(1, NMAX + 1):
            Kn = 2*(NMAX - n)
            Dsq = (sum(pder(pder(a_prev, m), m) for m in range(4)) + smul(-ii, pmul(divA, a_prev))
                   + smul(-2*ii, sum(pmul(Ap[m], pder(a_prev, m)) for m in range(4)) % p) + smul(-1, pmul(AA, a_prev))) % p
            Dsq = trunc(Dsq, Kn)
            invs = np.array([inv(n + dg) for dg in DEG], dtype=np.int64)
            a_new = (Dsq*invs[None, None]) % p
            res.append(int((a_new[0, 0, 0] + a_new[1, 1, 0]) % p))
            a_prev = a_new
        return res, chk
    pts = list(range(0, NMAX + 1))
    vals = {r: tr_an(r) for r in pts}
    out = {}
    for n in range(2, NMAX + 1):
        us = [r*r for r in pts]
        ys = [vals[r][0][n - 1]*pow(1 + r*r, 2*n, p) % p for r in pts]
        npar = n - 1
        # Lagrange interpolation mod p on the first npar points, check on the rest
        def lag(u, U, Yv):
            tot = 0
            for j in range(len(U)):
                num, den = 1, 1
                for k in range(len(U)):
                    if k != j: num = num*(u - U[k]) % p; den = den*(U[j] - U[k]) % p
                tot = (tot + Yv[j]*num*inv(den)) % p
            return tot
        check = all(lag(us[q], us[:npar], ys[:npar]) == ys[q] for q in range(npar, len(us)))
        # coefficients of P: solve Vandermonde mod p
        import sympy
        V = sympy.Matrix([[pow(u, k, p) for k in range(npar)] for u in us[:npar]])
        c = (V.inv_mod(p)*sympy.Matrix(ys[:npar])).applyfunc(lambda z: z % p)
        N2 = 2*n
        In = 0
        for k in range(npar):
            In = (In + int(c[k])*math.factorial(k + 1)*math.factorial(N2 - k - 3) % p*inv(math.factorial(N2 - 1))) % p
        In = In*inv(16) % p
        out[n] = (In, check, [int(z) for z in c])
    return out, max(vals[r][1] for r in pts)

# %% [markdown]
# ## Rational reconstruction

# %%
def ratrec(a, m):
    # rational reconstruction: find x/y = a mod m with |x|, y < sqrt(m/2)
    import math as _m
    bound = _m.isqrt(m//2)
    r0, r1, s0, s1 = m, a % m, 0, 1
    while r1 > bound:
        q = r0//r1; r0, r1 = r1, r0 - q*r1; s0, s1 = s1, s0 - q*s1
    if s1 == 0 or abs(s1) > bound: return None
    return Fraction(r1, s1) if s1 > 0 else Fraction(-r1, -s1)

# %% [markdown]
# ## Four primes, CRT, A_n

# %%
if __name__ == "__main__":
    primes = []; q = 2**30
    while len(primes) < 4:
        q = nextprime(q)
        if q % 4 == 1: primes.append(q)
    results = [run(p) for p in primes]
    for n in range(2, NMAX + 1):
        res = [results[k][0][n][0] for k in range(len(primes))]
        chks = [results[k][0][n][1] for k in range(len(primes))]
        mod = 1
        for p in primes: mod *= p
        a = int(crt(primes, res)[0])
        fr = ratrec(a, mod)
        a3 = int(crt(primes[:3], res[:3])[0]); fr3 = ratrec(a3, primes[0]*primes[1]*primes[2])
        # coefficients of P_n
        cs = []
        for k in range(n - 1):
            ck = [results[j][0][n][2][k] for j in range(len(primes))]
            cs.append(ratrec(int(crt(primes, ck)[0]), mod))
        g = math.factorial(n - 3) if n > 2 else None
        print(f"n = {n}: degree check {all(chks)};  P_n(u) coefficients {[str(c) for c in cs]};  A_n = {fr} (3 primes: {fr3})"
              + (f";  Gamma(n-2) A_n = {fr*g} = {float(fr*g):.12f}" if g else ""))
    print("FS gauge check (max residue of y.A' mod p, should be 0):", max(r[1] for r in results))
    print("literature (as used in inst_gy.py): -A_3 = -1/75, -A_4 = -17/735, -2 A_5 = 232/2835, -6 A_6 = -7916/148225 =", -7916/148225)
fr          # inspect: A_NMAX
