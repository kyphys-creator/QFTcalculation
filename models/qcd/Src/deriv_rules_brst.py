# %% [markdown]
# # Appendix check: gluon propagator, counterterm two-point rules, BRST nilpotency
#
# Research note models/qcd, derivations of the appendices (sympy).
#   app:rules 「伝播関数。」「対抗項の頂点。」 (R5): K^{mu nu} = -k^2 g + (1 - 1/xi) k k from -F^2/4 - (dG)^2/(2 xi) and its inverse (the
#       propagator); the counterterm vertex i delta_3 (-k^2 g + k k).
#   app:st 「BRST 変換。」「s^2=0 の確認。」 (R6): explicit Grassmann algebra for SU(3) (generators c^a, d_mu c^a, psi_i; G^a_mu, g even):
#       s^2 G = s^2 c = s^2 psi = s^2 (d c) = 0 component by component, the Jacobi identity in the form of the text, the intermediate formulas
#       s^2 c^a = -g f^{abc} (s c^b) c^c and c^a c^b T^a T^b = (i/2) f^{abc} c^a c^b T^c, and a negative control (wrong sign of s c).
# Each line prints OK or FAIL; the last line is ALL OK.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_rules_brst.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_rules_brst.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import itertools
import sympy as sp
INTERACTIVE = "ipykernel" in sys.modules

ok = []
def report(name, good, extra=''):
    ok.append(good)
    print(f"{'OK ' if good else 'FAIL'} {name} {extra}")


# %% [markdown]
# ## R5: the gluon propagator and the counterterm two-point rule (app:rules)

# %%
# ---------------- R5 ----------------
print("=== R5: gluon propagator and counterterm insertions ===")
k = sp.symbols('k0:4'); xi = sp.symbols('xi')
g = sp.diag(1, -1, -1, -1)            # g_{mu nu} = g^{mu nu}
kup = sp.Matrix(k)                     # k^mu
klo = g*kup                            # k_mu
k2 = (kup.T*g*kup)[0]
Kup = -k2*g + (1 - 1/xi)*kup*kup.T     # K^{mu nu}
Kinv_lo = -(g - (1 - xi)*klo*klo.T/k2)/k2   # (K^{-1})_{nu rho}
report("K^{mu nu} (K^{-1})_{nu rho} = delta^mu_rho", (Kup*Kinv_lo).applyfunc(sp.simplify) == sp.eye(4))
# quadratic form from -1/4 F^2 - 1/(2 xi)(dG)^2 with a = G(-k) (d -> +ik), b = G(k) (d -> -ik)
a = sp.symbols('a0:4'); b = sp.symbols('b0:4')
aup, bup = sp.Matrix(a), sp.Matrix(b)
I = sp.I
def F(vec, sgn):   # F_{mu nu} lower indices for plane wave: (d_mu G_nu - d_nu G_mu) with d_mu -> sgn*i*k_mu
    vlo = g*vec
    return sp.Matrix(4, 4, lambda m, n: sgn*I*klo[m]*vlo[n] - sgn*I*klo[n]*vlo[m])
Fa, Fb = F(aup, +1), F(bup, -1)
FF = sum(Fa[m, n]*Fb[r, s]*g[m, r]*g[n, s] for m in range(4) for n in range(4) for r in range(4) for s in range(4))
divA = I*(klo.T*aup)[0]; divB = -I*(klo.T*bup)[0]
# G = a e^{ikx} + b e^{-ikx}: the x-independent a-b cross term of -1/4 F^2 is -1/4 * 2 F(a).F(b), that of
# -(dG)^2/(2 xi) is -(1/xi)(ik.a)(-ik.b); (1/2) G(-k) K G(k) + (k -> -k) gives the cross term a.K.b
lag = -sp.Rational(1, 2)*FF - divA*divB/xi
quad = (aup.T*g*Kup*g*bup)[0]     # a_mu K^{mu nu} b_nu
report("-1/4F^2 - (dG)^2/(2xi) -> (1/2) G(-k) K G(k), K = -k^2 g + (1-1/xi) k k  [a-b cross term = a.K.b]",
       sp.simplify(sp.expand(lag - quad)) == 0)
d3 = sp.symbols('delta3')
ct = (-sp.Rational(1, 2)*FF)*d3          # cross term of -delta3/4 F^2
report("counterterm: -delta3/4 F^2 cross term = a.[delta3(-k^2 g + k k)].b, vertex i*delta3(-k^2 g + kk)",
       sp.simplify(sp.expand(ct - (aup.T*g*(d3*(-k2*g + kup*kup.T))*g*bup)[0])) == 0)

Kup, Kinv_lo          # inspect: K^{mu nu} and the propagator (K^{-1})_{nu rho}

# %% [markdown]
# ## R6: BRST nilpotency for SU(3) (app:st)

# %%
# ---------------- R6 ----------------
print("=== R6: BRST nilpotency, SU(3) ===")
# Gell-Mann matrices
l = [None]*9
l[1] = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
l[2] = sp.Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]])
l[3] = sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
l[4] = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
l[5] = sp.Matrix([[0, 0, -I], [0, 0, 0], [I, 0, 0]])
l[6] = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
l[7] = sp.Matrix([[0, 0, 0], [0, 0, -I], [0, I, 0]])
l[8] = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 0, -2]])/sp.sqrt(3)
T = [l[i]/2 for i in range(1, 9)]
NA = 8
f = [[[sp.nsimplify(sp.simplify(-2*I*((T[x]*T[y] - T[y]*T[x])*T[z]).trace())) for z in range(NA)] for y in range(NA)] for x in range(NA)]
# check [T^a,T^b] = i f^{abc} T^c
good = all(((T[x]*T[y] - T[y]*T[x]) - I*sum((f[x][y][z]*T[z] for z in range(NA)), sp.zeros(3))).applyfunc(sp.simplify).is_zero_matrix
           for x in range(NA) for y in range(NA))
report("[T^a,T^b] = i f^{abc} T^c with tr(T^a T^b) = delta/2", good)
# Jacobi in the form of the text: f^{abc} f^{bde} + f^{abd} f^{bec} + f^{abe} f^{bcd} = 0
good = True
for A_, C_, D_, E_ in itertools.product(range(NA), repeat=4):
    v = sum(f[A_][B_][C_]*f[B_][D_][E_] + f[A_][B_][D_]*f[B_][E_][C_] + f[A_][B_][E_]*f[B_][C_][D_] for B_ in range(NA))
    if sp.simplify(v) != 0:
        good = False; break
report("Jacobi: f^{abc}f^{bde} + f^{abd}f^{bec} + f^{abe}f^{bcd} = 0 (all a,c,d,e)", good)

[(a_ + 1, b_ + 1, c_ + 1, f[a_][b_][c_]) for a_ in range(NA) for b_ in range(a_ + 1, NA) for c_ in range(b_ + 1, NA) if f[a_][b_][c_] != 0]          # inspect: the nonzero f^{abc}, a < b < c

# %% [markdown]
# ### The Grassmann algebra

# %%
# Grassmann algebra: element = dict {tuple(sorted generator ids): coefficient}
NMU = 4
def gid_c(a_): return ('c', a_)
def gid_dc(a_, m_): return ('dc', a_, m_)
def gid_psi(i_): return ('psi', i_)
order = [gid_c(x) for x in range(NA)] + [gid_dc(x, m_) for x in range(NA) for m_ in range(NMU)] + [gid_psi(i_) for i_ in range(3)]
rank = {gname: n for n, gname in enumerate(order)}
G = [[sp.Symbol(f'G{x}_{m_}') for m_ in range(NMU)] for x in range(NA)]
gc = sp.Symbol('g')

def canon(gens):
    """sort generators, return (sign, tuple) or (0, None) if a generator repeats"""
    gl = list(gens)
    if len(set(gl)) < len(gl):
        return 0, None
    sign = 1
    arr = [rank[x] for x in gl]
    for i_ in range(len(arr)):          # bubble sort counting transpositions
        for j_ in range(len(arr) - 1 - i_):
            if arr[j_] > arr[j_ + 1]:
                arr[j_], arr[j_ + 1] = arr[j_ + 1], arr[j_]
                sign = -sign
    return sign, tuple(order[x] for x in arr)

def add(e1, e2, c2=1):
    r = dict(e1)
    for key, v in e2.items():
        r[key] = r.get(key, 0) + c2*v
    return r

def mul(e1, e2):
    r = {}
    for k1, v1 in e1.items():
        for k2_, v2 in e2.items():
            sgn, key = canon(k1 + k2_)
            if sgn == 0:
                continue
            r[key] = r.get(key, 0) + sgn*v1*v2
    return r

def gen(gname, coef=1):
    return {(gname,): coef}

def scal(coef):
    return {(): coef}


# %% [markdown]
# ### s on the generators and on G

# %%
# s on the generators and on G
sG = {}
for x in range(NA):
    for m_ in range(NMU):
        e = gen(gid_dc(x, m_))
        for y in range(NA):
            for z in range(NA):
                if f[x][y][z] != 0:
                    e = add(e, gen(gid_c(z), gc*f[x][y][z]*G[y][m_]))
        sG[(x, m_)] = e
s_gen = {}
for x in range(NA):
    e = {}
    for y in range(NA):
        for z in range(NA):
            if f[x][y][z] != 0:
                e = add(e, mul(gen(gid_c(y)), gen(gid_c(z))), -gc/2*f[x][y][z])
    s_gen[gid_c(x)] = e
    for m_ in range(NMU):
        e = {}
        for y in range(NA):
            for z in range(NA):
                if f[x][y][z] != 0:
                    e = add(e, mul(gen(gid_dc(y, m_)), gen(gid_c(z))), -gc/2*f[x][y][z])
                    e = add(e, mul(gen(gid_c(y)), gen(gid_dc(z, m_))), -gc/2*f[x][y][z])
        s_gen[gid_dc(x, m_)] = e
for i_ in range(3):
    e = {}
    for x in range(NA):
        for j_ in range(3):
            if T[x][i_, j_] != 0:
                e = add(e, mul(gen(gid_c(x)), gen(gid_psi(j_))), I*gc*T[x][i_, j_])
    s_gen[gid_psi(i_)] = e

def s(elem):
    """odd derivation: s(F theta_1...theta_k) = (sF) theta... + F sum_j (-1)^{j-1} theta_1..(s theta_j)..theta_k"""
    r = {}
    for key, coef in elem.items():
        # sF: coefficient depends on G
        for x in range(NA):
            for m_ in range(NMU):
                dF = sp.diff(coef, G[x][m_])
                if dF != 0:
                    r = add(r, mul(sG[(x, m_)], {key: dF}))
        for j_, th in enumerate(key):
            left = {key[:j_]: 1}
            right = {key[j_ + 1:]: 1}
            term = mul(mul(left, s_gen[th]), right)
            r = add(r, term, coef*(-1)**j_)
    return {kk: sp.expand(v) for kk, v in r.items() if sp.expand(v) != 0}

def is_zero(e):
    return all(sp.simplify(v) == 0 for v in e.values())

s_gen[gid_c(0)]          # inspect: s c^1 = -(g/2) f^{1bc} c^b c^c as {Grassmann monomial: coefficient}

# %% [markdown]
# ### The checks

# %%
# s^2 c^a
good = all(is_zero(s(s_gen[gid_c(x)])) for x in range(NA))
report("s^2 c^a = 0 for all a", good)
# s^2 psi_i
good = all(is_zero(s(s_gen[gid_psi(i_)])) for i_ in range(3))
report("s^2 psi_i = 0 for all colours i", good)
# s^2 G^a_mu
good = all(is_zero(s(sG[(x, m_)])) for x in range(NA) for m_ in range(NMU))
report("s^2 G^a_mu = 0 for all a, mu", good)
# s^2 (d_mu c^a) = d_mu s^2 c^a = 0 (consistency of the derivation on the derivative generators)
good = all(is_zero(s(s_gen[gid_dc(x, m_)])) for x in range(NA) for m_ in range(NMU))
report("s^2 (d_mu c^a) = 0", good)
# intermediate formulas of the text:
# s^2 c^a = -g f^{abc} (s c^b) c^c
good = True
for x in range(NA):
    lhs = s(s_gen[gid_c(x)])
    rhs = {}
    for y in range(NA):
        for z in range(NA):
            if f[x][y][z] != 0:
                rhs = add(rhs, mul(s_gen[gid_c(y)], gen(gid_c(z))), -gc*f[x][y][z])
    rhs2 = s(s_gen[gid_c(x)])
    if not is_zero(add(lhs, rhs, -1)):
        good = False
report("s^2 c^a = -g f^{abc}(s c^b) c^c (before Jacobi)", good)
# c^a c^b T^a T^b = (i/2) f^{abc} c^a c^b T^c (matrix element by element)
good = True
for i_ in range(3):
    for j_ in range(3):
        lhs = {}
        rhs = {}
        for x in range(NA):
            for y in range(NA):
                cf = (T[x]*T[y])[i_, j_]
                if cf != 0:
                    lhs = add(lhs, mul(gen(gid_c(x)), gen(gid_c(y))), cf)
                for z in range(NA):
                    if f[x][y][z] != 0 and T[z][i_, j_] != 0:
                        rhs = add(rhs, mul(gen(gid_c(x)), gen(gid_c(y))), I/2*f[x][y][z]*T[z][i_, j_])
        if not is_zero(add(lhs, rhs, -1)):
            good = False
report("c^a c^b T^a T^b = (i/2) f^{abc} c^a c^b T^c", good)
# negative control: with the wrong sign of s c the nilpotency on G must fail
for x in range(NA):
    for key in list(s_gen[gid_c(x)].keys()):
        s_gen[gid_c(x)][key] = -s_gen[gid_c(x)][key]
bad = not all(is_zero(s(sG[(x, m_)])) for x in range(NA) for m_ in range(NMU))
report("negative control: s c^a -> +(g/2) f c c spoils s^2 G = 0", bad)
nterms = len(s(sG[(0, 0)]))
print(f"     (with the wrong sign, s^2 G^1_0 has {nterms} nonzero Grassmann monomials)")

# %%
print()
print("ALL OK" if all(ok) else f"FAILURES: {ok.count(False)}")
