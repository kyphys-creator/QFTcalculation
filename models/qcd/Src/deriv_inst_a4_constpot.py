# %% [markdown]
# # Appendix check: the heat-kernel coefficients b_2, b_3, b_4 for constant non-abelian potentials
#
# Research note models/qcd, derivations of the appendices (numpy).  app:inst 「大きい質量の展開。」 (N2b): the integrated heat-kernel
# coefficients b_2, b_3, b_4 of -D^2 (flat, E = 0) for constant non-abelian potentials A_mu (random Hermitian N x N, N = 2, 3, 4),
# D_mu = d_mu - i A_mu (g = 1).  For constant A every total derivative vanishes, so the diagonal heat kernel equals the integrated density:
#   K(x,x;s) = int d^4k/(2pi)^4 exp(-s (k - A)^2) = (4 pi s)^-2 sum_n s^n b_n,  (k - A)^2 = k^2 + X,  X = -2 k.A + A.A.
# Compared with the minimal basis O_n of Fliegner, Haberl, Schmidt and Schubert (hep-th/9707189), b_n = (-1)^n O_n/n!, translated to the
# note's conventions (F_{kl} = -i Omega_{kl}, Omega_{mn} = [D_m, D_n] = -[A_m, A_n], D_k X = -i [A_k, X]), with the seven terms T1..T7 of O_4
# written with Omega as in the text, and with Vassilevich's a_4, a_6.
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_a4_constpot.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_a4_constpot.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import itertools, math
import numpy as np
INTERACTIVE = "ipykernel" in sys.modules
rng = np.random.default_rng(12345)


# %% [markdown]
# ## The plane-wave expansion of the heat kernel

# %%
def pairings(lst):
    if not lst:
        yield []
        return
    a = lst[0]
    for i in range(1, len(lst)):
        b = lst[i]; rest = lst[1:i] + lst[i+1:]
        for p in pairings(rest):
            yield [(a, b)] + p

def b_coeff(A, order):
    """tr b_order from the plane-wave expansion"""
    N = A[0].shape[0]
    B = sum(A[m] @ A[m] for m in range(4))
    tot = 0.0
    for n in range(order, 2*order + 1):
        nk = 2*(n - order)
        coef = (-1)**n/math.factorial(n)*(-2.0)**nk*(0.5)**(nk//2)
        for kpos in itertools.combinations(range(n), nk):
            for pr in pairings(list(kpos)):
                for idx in itertools.product(range(4), repeat=len(pr)):
                    lab = {}
                    for (p, q), mu in zip(pr, idx):
                        lab[p] = mu; lab[q] = mu
                    M = np.eye(N, dtype=complex)
                    for pos in range(n):
                        M = M @ (A[lab[pos]] if pos in lab else B)
                    tot += coef*np.trace(M)
    return tot


# %% [markdown]
# ## Random Hermitian potentials and the invariants

# %%
def herm(N):
    X = rng.normal(size=(N, N)) + 1j*rng.normal(size=(N, N))
    return (X + X.conj().T)/2

def invariants(A):
    N = A[0].shape[0]
    com = lambda X, Y: X @ Y - Y @ X
    Om = [[-com(A[m], A[n]) for n in range(4)] for m in range(4)]
    D = lambda k, X: -1j*com(A[k], X)
    DOm = [[[D(k, Om[m][n]) for n in range(4)] for m in range(4)] for k in range(4)]
    DDOm = [[[[D(k, DOm[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)] for k in range(4)]
    F = lambda k, l: -1j*Om[k][l]
    F3 = lambda k, l, m: -1j*DOm[k][l][m]
    F4 = lambda k, l, m, n: -1j*DDOm[k][l][m][n]
    tr = np.trace
    R4 = range(4)
    O2 = sum(tr(F(k, l) @ F(l, k)) for k in R4 for l in R4)/6
    O3 = (sum(tr(F3(k, l, m) @ F3(k, m, l)) for k in R4 for l in R4 for m in R4)/20
          - 2j/15*sum(tr(F(k, l) @ F(l, m) @ F(m, k)) for k in R4 for l in R4 for m in R4))
    t = {}
    t['FFFF chain (-1/21)'] = -1/21*sum(tr(F(k, l) @ F(l, m) @ F(m, n) @ F(n, k)) for k in R4 for l in R4 for m in R4 for n in R4)
    t['F_klmn F_lknm (1/70)'] = 1/70*sum(tr(F4(k, l, m, n) @ F4(l, k, n, m)) for k in R4 for l in R4 for m in R4 for n in R4)
    t['F_kl F_lk F_mn F_nm (2/35)'] = 2/35*sum(tr(F(k, l) @ F(l, k) @ F(m, n) @ F(n, m)) for k in R4 for l in R4 for m in R4 for n in R4)
    t['F_kl F_lm F_kn F_nm (4/35)'] = 4/35*sum(tr(F(k, l) @ F(l, m) @ F(k, n) @ F(n, m)) for k in R4 for l in R4 for m in R4 for n in R4)
    t['-6/35 i F_kl F_mln F_mnk'] = -6j/35*sum(tr(F(k, l) @ F3(m, l, n) @ F3(m, n, k)) for k in R4 for l in R4 for m in R4 for n in R4)
    t['-8/105 i F_kl F_lmn F_knm'] = -8j/105*sum(tr(F(k, l) @ F3(l, m, n) @ F3(k, n, m)) for k in R4 for l in R4 for m in R4 for n in R4)
    t['F_kl F_mn F_lk F_nm (11/420)'] = 11/420*sum(tr(F(k, l) @ F(m, n) @ F(l, k) @ F(n, m)) for k in R4 for l in R4 for m in R4 for n in R4)
    O4 = sum(t.values())
    # the same seven terms written with Omega (note's conventions), as in the snippet
    s = {}
    s['T1'] = -1/21*sum(tr(Om[k][l] @ Om[l][m] @ Om[m][n] @ Om[n][k]) for k in R4 for l in R4 for m in R4 for n in R4)
    s['T2'] = 1/70*sum(tr(DDOm[k][l][m][n] @ DDOm[l][k][m][n]) for k in R4 for l in R4 for m in R4 for n in R4)
    s['T3'] = 2/35*sum(tr(Om[k][l] @ Om[l][k] @ Om[m][n] @ Om[n][m]) for k in R4 for l in R4 for m in R4 for n in R4)
    s['T4'] = 4/35*sum(tr(Om[k][l] @ Om[l][m] @ Om[k][n] @ Om[n][m]) for k in R4 for l in R4 for m in R4 for n in R4)
    s['T5'] = 6/35*sum(tr(Om[k][l] @ DOm[m][l][n] @ DOm[m][n][k]) for k in R4 for l in R4 for m in R4 for n in R4)
    s['T6'] = 8/105*sum(tr(Om[k][l] @ DOm[l][m][n] @ DOm[k][n][m]) for k in R4 for l in R4 for m in R4 for n in R4)
    s['T7'] = 11/420*sum(tr(Om[k][l] @ Om[m][n] @ Om[l][k] @ Om[n][m]) for k in R4 for l in R4 for m in R4 for n in R4)
    O4om = sum(s.values())
    # Vassilevich a_6 (Omega part, f = 1): (1/360) tr(8 Om_{ij;k}^2 + 2 Om_{ij;j} Om_{ik;k} + 12 Om_{ij;kk} Om_{ij} - 12 Om_ij Om_jk Om_ki)
    a6v = (8*sum(tr(DOm[k][i][j] @ DOm[k][i][j]) for i in R4 for j in R4 for k in R4)
           + 2*sum(tr(DOm[j][i][j] @ DOm[k][i][k]) for i in R4 for j in R4 for k in R4)
           + 12*sum(tr(DDOm[k][k][i][j] @ Om[i][j]) for i in R4 for j in R4 for k in R4)
           - 12*sum(tr(Om[i][j] @ Om[j][k] @ Om[k][i]) for i in R4 for j in R4 for k in R4))/360
    a4v = sum(tr(Om[i][j] @ Om[i][j]) for i in R4 for j in R4)/12
    return O2, O3, O4, O4om, a4v, a6v


# %% [markdown]
# ## N = 2, 3, 4

# %%
if __name__ == "__main__":
    for N, trial in ((2, 0), (3, 1), (3, 2), (4, 3)):
        A = [herm(N) for _ in range(4)]
        b2, b3, b4 = (b_coeff(A, o) for o in (2, 3, 4))
        O2, O3, O4, O4om, a4v, a6v = invariants(A)
        print(f"N = {N} (trial {trial}):")
        print(f"   b_2 = {b2:.12g}   O_2/2 = {O2/2:.12g}   (1/12) tr Om^2 = {a4v:.12g}")
        print(f"   b_3 = {b3:.12g}  -O_3/6 = {-O3/6:.12g}   Vassilevich a_6/(4pi)^-2 = {a6v:.12g}")
        print(f"   b_4 = {b4:.12g}  O_4/24 = {O4/24:.12g}   (Omega form) {O4om/24:.12g}   rel.diff {abs(b4 - O4/24)/abs(b4):.1e}, {abs(O4 - O4om)/abs(O4):.1e}")
b2, b3, b4          # inspect: b_2, b_3, b_4 of the last trial (N = 4)
