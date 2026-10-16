# %% [markdown]
# # Appendix check: heat-kernel coefficients of the BPST instanton in floating point (t = 1/2 and 1)
#
# Research note models/qcd, derivations of the appendices (numpy, scipy).  app:inst 「大きい質量の展開。」 (N2b): floating-point version of
# deriv_inst_dewitt.wl, used for t = 1 and for the higher coefficients A_5, A_6, A_7 (t = 1/2): DeWitt recursion in the Fock-Schwinger gauge
# at x' = (r,0,0,0), BPST regular gauge, rho = 1, g = 1, with sparse truncated polynomials in y (monomials of total degree <= 2 NMAX,
# products by a precomputed index table).  tr a_n(0) at 12 points is fitted to P(r^2)/(1+r^2)^(2n), deg P <= n-2 (fit residual printed),
# and A_n = (1/8) int_0^inf r^3 tr a_n dr.  Large-m expansion of ln det: -A_3/m^2 - A_4/m^4 - 2 A_5/m^6 - 6 A_6/m^8 (Gamma(n-2) A_n/m^(2n-4)).
# Arguments: NMAX [both] (default 6, t = 1/2 only; cell by cell the defaults are used); run_deriv_check.sh runs "4 both" (t = 1/2 and 1:
# A_4 = 8 T (7C-1)/735 for t = 1) and "7" (t = 1/2 to A_7; its lines up to n = 6 are those of NMAX = 6).  Writes nothing;
# run_deriv_check.sh saves the printed output as results/deriv_inst_dewitt_num_4both.txt and results/deriv_inst_dewitt_num_7.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_dewitt_num.py 4 both;  ... deriv_inst_dewitt_num.py 7   (4 both: a few seconds; 7: about 1 minute)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import math, itertools
import sys
import numpy as np
from scipy.integrate import quad
INTERACTIVE = "ipykernel" in sys.modules
ARGS = sys.argv[1:] if "ipykernel" not in sys.modules else []      # cell by cell (IPython kernel): the defaults
NMAX = int(ARGS[0]) if ARGS else 6
K = 2*NMAX

# %% [markdown]
# ## Monomials and the product table

# %%
MON = [e for d in range(K + 1) for e in itertools.product(range(d + 1), repeat=4) if sum(e) == d]
MON = sorted(set(MON), key=lambda e: (sum(e), e))
IDX = {e: i for i, e in enumerate(MON)}
M = len(MON)
DEG = np.array([sum(e) for e in MON])
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
            f = list(e); f[mu] -= 1
            src.append(i); dst.append(IDX[tuple(f)]); fac.append(e[mu])
    DER.append((np.array(src), np.array(dst), np.array(fac, float)))
NMAX, M          # inspect: NMAX and the number of monomials

# %% [markdown]
# ## Polynomial algebra

# %%
def pmul(a, b):                 # a, b: (d, d, M) complex
    d = a.shape[0]
    out = np.zeros((d, d, M), complex)
    for i in range(d):
        for j in range(d):
            for m in range(d):
                prod = a[i, m][PI]*b[m, j][PJ]
                out[i, j] += np.bincount(PK, weights=prod.real, minlength=M) + 1j*np.bincount(PK, weights=prod.imag, minlength=M)
    return out
def pder(P, mu):
    src, dst, fac = DER[mu]
    out = np.zeros_like(P)
    out[:, :, dst] = P[:, :, src]*fac
    return out
def trunc(P, k):
    return P*(DEG <= k)
def const(Mat):
    d = Mat.shape[0]; P = np.zeros((d, d, M), complex); P[:, :, 0] = Mat; return P
def mono(mu, d):
    P = np.zeros((d, d, M), complex); e = [0]*4; e[mu] = 1; P[:, :, IDX[tuple(e)]] = np.eye(d); return P
eps3 = np.zeros((3, 3, 3)); eps3[0, 1, 2] = eps3[1, 2, 0] = eps3[2, 0, 1] = 1; eps3[0, 2, 1] = eps3[2, 1, 0] = eps3[1, 0, 2] = -1
eta = np.zeros((3, 4, 4))
for a in range(3):
    eta[a, :3, :3] = eps3[a]; eta[a, a, 3] = 1; eta[a, 3, a] = -1
sig = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]

# %% [markdown]
# ## The DeWitt recursion at x' = (r,0,0,0)

# %%
def coeffs(t, r):
    T = [s/2 for s in sig] if t == 0.5 else [-1j*eps3[a] for a in range(3)]
    d = T[0].shape[0]; Id = np.eye(d)
    w = 2*r*mono(0, 1) + sum(pmul(mono(m, 1), mono(m, 1)) for m in range(4))
    c = r*r + 1
    f = const(np.eye(1)/c); term = const(np.eye(1)/c)
    for k in range(1, K + 1):
        term = pmul(term, -w/c); f = f + term
    X = [r*const(np.eye(1)) + mono(0, 1) if m == 0 else mono(m, 1) for m in range(4)]
    A = []
    for mu in range(4):
        s = np.zeros((d, d, M), complex)
        for a in range(3):
            for nu in range(4):
                if eta[a, mu, nu] == 0: continue
                xf = pmul(X[nu], f)[0, 0]
                s += 2*eta[a, mu, nu]*T[a][:, :, None]*xf[None, None]
        A.append(s)
    yA = sum(pmul(mono(m, d), A[m]) for m in range(4))
    parts = [yA*(DEG == j) for j in range(K + 1)]
    Phi_k = [const(Id)]
    for k in range(1, K + 1):
        Phi_k.append(sum(1j/k*pmul(parts[j], Phi_k[k - j]) for j in range(1, k + 1)))
    Phi = sum(Phi_k)
    Inv_k = [const(Id)]
    for k in range(1, K + 1):
        Inv_k.append(-sum(pmul(Inv_k[j], Phi_k[k - j]) for j in range(0, k)))
    Phinv = sum(Inv_k)
    Ap = [trunc(pmul(Phinv, pmul(A[m], Phi)) + 1j*pmul(Phinv, pder(Phi, m)), K - 1) for m in range(4)]
    chk = np.max(np.abs(trunc(sum(pmul(mono(m, d), Ap[m]) for m in range(4)), K - 1)))
    divA = sum(pder(Ap[m], m) for m in range(4))
    AA = sum(pmul(Ap[m], Ap[m]) for m in range(4))
    a_prev = const(Id); res = []
    for n in range(1, NMAX + 1):
        Kn = 2*(NMAX - n)
        Dsq = (sum(pder(pder(a_prev, m), m) for m in range(4)) - 1j*pmul(divA, a_prev) - 2j*sum(pmul(Ap[m], pder(a_prev, m)) for m in range(4))
               - pmul(AA, a_prev))
        a_new = trunc(Dsq, Kn)/(n + DEG)[None, None]
        res.append(np.trace(a_new[:, :, 0]).real)
        a_prev = a_new
    return np.array(res), chk

# %% [markdown]
# ## Fit and integrate

# %%
if __name__ == "__main__":
    pts = np.array([0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.5, 1.8, 2.2, 2.6, 3])
    for t in ((0.5,) if len(ARGS) < 2 else (0.5, 1.0)):
        vals = []; chks = []
        for r in pts:
            v, ch = coeffs(t, r); vals.append(v); chks.append(ch)
        vals = np.array(vals)
        print(f"t = {t} (NMAX = {NMAX}, {M} monomials): FS-gauge check max|y.A'| = {max(chks):.1e};  max|tr a_1(0)| = {np.max(np.abs(vals[:, 0])):.1e}")
        for n in range(2, NMAX + 1):
            u = pts**2
            yv = vals[:, n - 1]*(1 + u)**(2*n)
            V = np.vander(u, n - 1, increasing=True)
            cf, *_ = np.linalg.lstsq(V, yv, rcond=None)
            resid = np.max(np.abs(V @ cf - yv)/np.maximum(1, np.abs(yv)))
            An = quad(lambda rr: rr**3*np.polyval(cf[::-1], rr*rr)/(1 + rr*rr)**(2*n), 0, np.inf, epsabs=0, epsrel=1e-13)[0]/8
            g = math.gamma(n - 2)*An if n > 2 else float("nan")
            print(f"   n = {n}: P(u) = {np.round(cf, 8)} (fit residual {resid:.1e});  A_n = {An:.12f};  Gamma(n-2) A_n = {g:.12f}")
        if t == 0.5:
            print(f"   compare: A_2 = -1/12; A_3 = 1/75 = {1/75:.12f}; A_4 = 17/735 = {17/735:.12f}; 2 A_5 = -232/2835 = {-232/2835:.12f}; 6 A_6 = 7916/148225 = {7916/148225:.12f}")
        else:
            print(f"   compare: A_2 = -1/3; A_3 = 4/75 = {4/75:.12f}; A_4 = 8 T (7C-1)/735 = 208/735 = {208/735:.12f}")
vals[:, :4]          # inspect: tr a_n(0), n = 1..4, at the 12 points (the last t)
