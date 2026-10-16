# %% [markdown]
# # Appendix check: the vector fluctuation operator of the instanton in the 2x2 (quaternion) form
#
# Research note models/qcd, derivations of the appendices (sympy).  app:inst 「集団座標と1ループの積分。」 (N1): BPST background (regular
# gauge, rho = 1, g = 1), adjoint representation, D_mu = d_mu - i A_mu, (D_mu v)^b = d_mu v^b + eps_{bcd} A^c_mu v^d.
# (a) the spinor identities s_mu sbar_nu = delta + i eta_a sigma^a, sbar_mu s_nu = delta + i etabar_a sigma^a, i sigma^a s_nu = eta_{a mu nu} s_mu,
#     etabar.eta = 0, eta_{a al mu} eta_{b al nu} = delta delta + eps eta, tr(eta_a eta_b eta_c eta_d);
# (b) the sign of M_A: the translation zero mode a_mu = G_{nu mu} is annihilated by -D^2 delta + 2i ad G (True) and not by -D^2 delta - 2i ad G
#     (False, expected);
# (c) s_mu (M_A a)_mu = D D^+ (s.a) and D^+ D = -D^2 1_2 for a generic polynomial a, D = s_mu D_mu, D^+ = -sbar_mu D_mu;
#     D^+(s.a) = -D.a - (i/2) etabar sigma (D_mu a_nu - D_nu a_mu): det' M_A = det(-D^2)^4.
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_spinor.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_spinor.py   (about 1 minute)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import itertools
import sympy as sp
INTERACTIVE = "ipykernel" in sys.modules

# %% [markdown]
# ## (a) Spinor identities

# %%
x = sp.symbols('x1:5', real=True)
I = sp.I
eps3 = lambda a, b, c: sp.LeviCivita(a, b, c)
def eta(a, m, n):
    if m < 3 and n < 3: return eps3(a, m, n)
    if n == 3 and m < 3: return 1 if a == m else 0
    if m == 3 and n < 3: return -1 if a == n else 0
    return 0
def etab(a, m, n):
    if m < 3 and n < 3: return eps3(a, m, n)
    if n == 3 and m < 3: return -1 if a == m else 0
    if m == 3 and n < 3: return 1 if a == n else 0
    return 0
sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -I], [I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
one = sp.eye(2)
s = [I*sig[0], I*sig[1], I*sig[2], one]
sb = [-I*sig[0], -I*sig[1], -I*sig[2], one]
R4, R3 = range(4), range(3)
ok = all((s[m]*sb[n] - (sp.KroneckerDelta(m, n)*one + I*sum((eta(a, m, n)*sig[a] for a in R3), sp.zeros(2)))) == sp.zeros(2) for m in R4 for n in R4)
ok2 = all((sb[m]*s[n] - (sp.KroneckerDelta(m, n)*one + I*sum((etab(a, m, n)*sig[a] for a in R3), sp.zeros(2)))) == sp.zeros(2) for m in R4 for n in R4)
ok3 = all((I*sig[a]*s[n] - sum((eta(a, m, n)*s[m] for m in R4), sp.zeros(2))) == sp.zeros(2) for a in R3 for n in R4)
ok4 = all(sum(etab(a, m, n)*eta(b, m, n) for m in R4 for n in R4) == 0 for a in R3 for b in R3)
ok5 = all(sum(eta(a, l, m)*eta(b, l, n) for l in R4) == sp.KroneckerDelta(a, b)*sp.KroneckerDelta(m, n) + sum(eps3(a, b, c)*eta(c, m, n) for c in R3)
          for a in R3 for b in R3 for m in R4 for n in R4)
E = [sp.Matrix(4, 4, lambda m, n: eta(a, m, n)) for a in R3]
ok6 = all((E[a]*E[b]*E[c]*E[d]).trace() == 4*(sp.KroneckerDelta(a, b)*sp.KroneckerDelta(c, d) - sp.KroneckerDelta(a, c)*sp.KroneckerDelta(b, d)
          + sp.KroneckerDelta(a, d)*sp.KroneckerDelta(b, c)) for a in R3 for b in R3 for c in R3 for d in R3)
print(f"(a) s sbar = 1 + i eta.sigma: {ok};  sbar s = 1 + i etabar.sigma: {ok2};  i sigma^a s_nu = eta_(a mu nu) s_mu: {ok3};  etabar.eta = 0: {ok4};"
      f"  eta_(a al mu) eta_(b al nu) = dd + eps eta: {ok5};  tr(eta_a eta_b eta_c eta_d) = 4(dd - dd + dd): {ok6}")
s, sb          # inspect: s_mu = (i sigma, 1), sbar_mu = (-i sigma, 1)

# %% [markdown]
# ## BPST and the operator M_A

# %%
# BPST regular gauge
x2 = sum(xi**2 for xi in x)
f = 1/(x2 + 1)
A = [[2*sum(eta(a, m, n)*x[n] for n in R4)*f for a in R3] for m in R4]          # A[mu][a]
G = [[[sp.simplify(sp.diff(A[n][a], x[m]) - sp.diff(A[m][a], x[n]) + sum(eps3(a, b, c)*A[m][b]*A[n][c] for b in R3 for c in R3)) for a in R3] for n in R4] for m in R4]
print("    G^a_mn = -4 eta f^2:", all(sp.simplify(G[m][n][a] + 4*eta(a, m, n)*f**2) == 0 for m in R4 for n in R4 for a in R3))
def Dv(m, v):          # adjoint covariant derivative of a 3-vector of functions
    return [sp.diff(v[b], x[m]) + sum(eps3(b, c, d)*A[m][c]*v[d] for c in R3 for d in R3) for b in R3]
def adG(m, n, v):      # (ad G_mn v)^b = [G, v]^b = i eps_{cdb} G^c v^d
    return [I*sum(eps3(c, d, b)*G[m][n][c]*v[d] for c in R3 for d in R3) for b in R3]
def Mop(a, sgn):       # (M a)_mu = -D^2 a_mu + sgn 2i ad(G_mu nu) a_nu
    out = []
    for m in R4:
        lap = [0, 0, 0]
        for k in R4:
            t = Dv(k, Dv(k, a[m])); lap = [lap[b] + t[b] for b in R3]
        sp_ = [0, 0, 0]
        for n in R4:
            t = adG(m, n, a[n]); sp_ = [sp_[b] + 2*I*sgn*t[b] for b in R3]
        out.append([-lap[b] + sp_[b] for b in R3])
    return out
sp.Matrix(4, 4, lambda m, n: sp.factor(G[m][n][0]))          # inspect: G^1_{mu nu} = -4 eta_{1 mu nu} f^2

# %% [markdown]
# ## (b) The sign of M_A: the translation zero mode

# %%
for nu in (0, 3):
    a = [[G[nu][m][b] for b in R3] for m in R4]
    for sgn in (+1, -1):
        res = Mop(a, sgn)
        z = all(sp.simplify(res[m][b]) == 0 for m in R4 for b in R3)
        print(f"(b) translation mode a_mu = G_({nu+1} mu): (-D^2 + {'+' if sgn > 0 else '-'}2i ad G) a = 0: {z}")

# %% [markdown]
# ## (c) M_A in the 2x2 form for a generic fluctuation

# %%
# (c) generic polynomial fluctuation
import random
random.seed(3)
def rpoly():
    return sum(random.randint(-3, 3)*x[i]*x[j] for i in R4 for j in R4 if i <= j) + sum(random.randint(-3, 3)*x[i] for i in R4) + random.randint(-3, 3)
a = [[rpoly() for b in R3] for m in R4]
Ma = Mop(a, +1)
# 2x2 matrices with adjoint-vector entries: represent as dict (alpha, beta) -> 3-vector
def smul(M, V):        # M (2x2 numbers) times matrix-of-vectors V
    return {(i, j): [sum(M[i, k]*V[(k, j)][b] for k in range(2)) for b in R3] for i in range(2) for j in range(2)}
def add(*Vs):
    return {key: [sum(V[key][b] for V in Vs) for b in R3] for key in Vs[0]}
def scal(c, V):
    return {key: [c*V[key][b] for b in R3] for key in V}
def Dmat(m, V):
    return {key: Dv(m, V[key]) for key in V}
def svec(a):           # s.a
    return {(i, j): [sum(s[m][i, j]*a[m][b] for m in R4) for b in R3] for i in range(2) for j in range(2)}
def Dslash(V):         # s_mu D_mu
    return add(*[smul(s[m], Dmat(m, V)) for m in R4])
def Dslashdag(V):      # -sbar_mu D_mu
    return scal(-1, add(*[smul(sb[m], Dmat(m, V)) for m in R4]))
lhs = svec(Ma)
rhs = Dslash(Dslashdag(svec(a)))
print("(c) s_mu (M_A a)_mu = D D^+ (s.a) [M_A with +2i ad G]:", all(sp.simplify(lhs[k][b] - rhs[k][b]) == 0 for k in lhs for b in R3))
lapA = [[0, 0, 0] for _ in R4]
V = svec(a)
DdD = Dslashdag(Dslash(V))
lap = add(*[Dmat(m, Dmat(m, V)) for m in R4])
print("    D^+ D = -D^2 1_2 on s.a:", all(sp.simplify(DdD[k][b] + lap[k][b]) == 0 for k in V for b in R3))
# D^+(s.a) = -D.a - (i/2) etabar_{b mu nu} sigma^b (D_mu a_nu - D_nu a_mu)
Dd = Dslashdag(V)
divA = [sum(Dv(m, a[m])[b] for m in R4) for b in R3]
rhs2 = {}
for (i, j) in V:
    vec = [-(divA[b] if i == j else 0) for b in R3]
    for c in R3:
        for m in R4:
            for n in R4:
                if etab(c, m, n) == 0: continue
                Fmn = [Dv(m, a[n])[b] - Dv(n, a[m])[b] for b in R3]
                vec = [vec[b] - I/2*etab(c, m, n)*sig[c][i, j]*Fmn[b] for b in R3]
    rhs2[(i, j)] = vec
print("    D^+(s.a) = -D.a - (i/2) etabar sigma (D a - D a):", all(sp.simplify(Dd[k][b] - rhs2[k][b]) == 0 for k in V for b in R3))
