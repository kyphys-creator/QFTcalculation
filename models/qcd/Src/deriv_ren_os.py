# %% [markdown]
# # Appendix check: the quark loop (a4), the quark self-energy (c) and the on-shell quantities
#
# Research note models/qcd, derivations of the appendices (sympy, mpmath).  Checks every nontrivial equality of
#   app:ren 「クォークのループ (a4)。」 and 「極と有限部分。」 (R1): the traces g_{mu nu} tr, k_mu k_nu tr in terms of D1, D2; the T_F part of
#       Eq. (V) and its form with (D-2) A0 = 2 m^2 B0(0) (exact in D); the pole -4/3 and the quark bracket of Eq. (VR); the massless quark;
#   app:ren 「クォークの自己エネルギー (c)。」 (R2): the Dirac identities for P = pslash - m, the integration-by-parts and reduction identities
#       (numerically, Feynman parameters, 30 digits, two (D, p^2, m^2) points), Sigma_V = xi (D-2) B1, Sigma_S = (D-1+xi) B0, delta_2, delta_m;
#   app:os 「重いクォーク。」「on-shell の質量の対抗項。」「重いクォークの留数。」 (R3): B0, B1 and their derivatives at p^2 = m^2 exactly in D,
#       delta m (Eq. (os)), the xi independence, the residue R_Q - 1 = -[(3-xi) DIR + 4 + 3L] and the O(eps) x IR-pole terms;
#   app:os 「質量のないクォークとグルーオンの留数。」 (R4): the C_A and quark coefficients, R_G - 1 = Pi^R(0) of Eq. (os).
# Each line prints OK or FAIL; the last line is ALL OK.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_ren_os.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_ren_os.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import sympy as sp
import mpmath as mp
INTERACTIVE = "ipykernel" in sys.modules

eps, D, k2, m2, p2, xi = sp.symbols('epsilon D k2 m2 p2 xi')
A0, B0, B00, B1, J, U, I12 = sp.symbols('A0 B0 B00 B1 J U I12')
L = sp.symbols('L')
eta = 1 - xi
ok = []


def check(name, expr):
    if isinstance(expr, sp.MatrixBase):
        z = expr.applyfunc(sp.simplify)
        good = z.is_zero_matrix
    else:
        z = sp.simplify(expr)
        good = (z == 0)
    ok.append(good)
    print(f"{'OK ' if good else 'FAIL'} {name}" + ('' if good else f"   residual = {z}"))


# %% [markdown]
# ## R1: the quark loop (a4) (app:ren)

# %%
print("=== R1: quark loop (a4) ===")
D1, D2 = sp.symbols('D1 D2')  # D1 = l^2 - m^2, D2 = (l+k)^2 - m^2
ldotlp = (D1 + D2 + 2*m2 - k2)/2           # l.(l+k)
gtrace = 4*((2 - D)*ldotlp + D*m2)          # g_{mu nu} tr[g^mu (l+m) g^nu (l'+m)]
check("g_{mu nu} tr = 2(2-D)(D1+D2) + 2[4m^2+(D-2)k^2]", gtrace - (2*(2 - D)*(D1 + D2) + 2*(4*m2 + (D - 2)*k2)))
# k_mu k_nu tr = 4[2(k.l)(k.l') - k^2(l.l' - m^2)],  k.l = (D2-D1-k^2)/2, k.l' = (D2-D1+k^2)/2
kl, klp = (D2 - D1 - k2)/2, (D2 - D1 + k2)/2
ktrace = 4*(2*kl*klp - k2*(ldotlp - m2))
check("k_mu k_nu tr = 2[(D2-D1)^2 - k^2(D1+D2)]", ktrace - 2*((D2 - D1)**2 - k2*(D1 + D2)))
# divided by D1 D2: D2/D1 - 2 + D1/D2 - k^2/D2 - k^2/D1; int D2/D1 = int D1/D2 = k^2 A0, int 1 = 0 -> sum 0
check("k_mu k_nu part integrates to 0", k2*A0 + k2*A0 - k2*A0 - k2*A0)
# i (D-1) k^2 Pi = -g^2 T_F (i/K) {4(2-D) A0 + 2[4m^2+(D-2)k^2] B0}
Pi_T = -(4*(2 - D)*A0 + 2*(4*m2 + (D - 2)*k2)*B0)/((D - 1)*k2)
Pi_eqV = 2/((D - 1)*k2)*(2*(D - 2)*A0 - (4*m2 + (D - 2)*k2)*B0)
check("T_F part = eq:V first line", Pi_T - Pi_eqV)
Pi_new = -2/(D - 1)*((D - 2)*B0 + 4*m2/k2*(B0 - B00))
check("with 2(D-2)A0 = 4m^2 B0(0): -2/(D-1)[(D-2)B0 + 4m^2/k^2 (B0 - B0(0))]",
      Pi_eqV.subs(A0, 2*m2*B00/(D - 2)) - Pi_new)
# exact D-dim relation (D-2)A0 = 2 m^2 B0(0;m^2,m^2): A0 = m^2 G(1+e) X^e/(e(1-e)), B0(0) = G(e) X^e
X = sp.symbols('X', positive=True)
A0ex = m2*sp.gamma(1 + eps)*X**eps/(eps*(1 - eps))
B00ex = sp.gamma(eps)*X**eps
check("(D-2) A0 = 2 m^2 B0(0;m,m) exactly", sp.gammasimp(((D - 2)*A0ex - 2*m2*B00ex).subs(D, 4 - 2*eps)))
ser = sp.series((2*(D - 2)/(D - 1)).subs(D, 4 - 2*eps), eps, 0, 2).removeO()
check("2(D-2)/(D-1) = 4/3 - 4 eps/9 + O(eps^2)", ser - (sp.Rational(4, 3) - sp.Rational(4, 9)*eps))
b, b0 = sp.symbols('b b0')  # MS-bar finite parts of B0(k^2), B0(0)
expr = sp.series((Pi_new.subs({B0: 1/eps + b, B00: 1/eps + b0})).subs(D, 4 - 2*eps), eps, 0, 1).removeO()
VR = -sp.Rational(4, 3)*((1 + 2*m2/k2)*b - 2*m2/k2*b0 - sp.Rational(1, 3))
check("pole -4/3 and finite part = eq:VR quark bracket", sp.expand(expr - (-sp.Rational(4, 3)/eps + VR)))
# massless quark: -2 T_F (D-2)/(D-1) B0
check("massless quark: -2(D-2)/(D-1) B0", Pi_eqV.subs({m2: 0, A0: 0}) + 2*(D - 2)/(D - 1)*B0)

Pi_new, VR          # inspect: Pi_T in the B0(0) form and the quark bracket of Eq. (VR)

# %% [markdown]
# ## R2: the quark self-energy (c) (app:ren)

# %%
print("=== R2: quark self-energy (c) ===")
# Dirac identity P q P with P = pslash - m: verified with explicit gamma matrices below (4-dim, algebraic identity)
g0 = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
gam = [g0] + [sp.Matrix(sp.BlockMatrix([[sp.zeros(2), s], [-s, sp.zeros(2)]])) for s in sig]
metric = sp.diag(1, -1, -1, -1)
pv = sp.symbols('p0:4'); qv = sp.symbols('q0:4'); m = sp.symbols('m')
def slash(v):
    return sum((metric[i, i]*v[i]*gam[i] for i in range(4)), sp.zeros(4))
def dot(a, c):
    return sum(metric[i, i]*a[i]*c[i] for i in range(4))
P = slash(pv) - m*sp.eye(4)
lhs = P*(slash(qv) + slash(pv) + m*sp.eye(4))*P
rhs = 2*dot(pv, qv)*P - (dot(pv, pv) - m**2)*slash(qv) + (dot(pv, pv) - m**2)*P
check("P(qslash+pslash+m)P = 2(p.q)P - (p^2-m^2) qslash + (p^2-m^2) P", (lhs - rhs).applyfunc(sp.expand))
# l (k+m) l = P(k+m)P - 2 D(k) P + D(k)(k - m), with l = p - k  (QED-note form, also used for the scaleless terms)
kv = sp.symbols('k0:4')
lv = [pv[i] - kv[i] for i in range(4)]
Dk = dot(kv, kv) - m**2
lhs2 = slash(lv)*(slash(kv) + m*sp.eye(4))*slash(lv)
rhs2 = P*(slash(kv) + m*sp.eye(4))*P - 2*Dk*P + Dk*(slash(kv) - m*sp.eye(4))
check("lslash(kslash+m)lslash = P(k+m)P - 2D(k)P + D(k)(kslash-m)", (lhs2 - rhs2).applyfunc(sp.expand))
check("gamma^rho (k+m) gamma_rho = -(D-2)k + D m  [4-dim check: -2k+4m]",
      (sum((metric[i, i]*gam[i]*(slash(kv) + m*sp.eye(4))*gam[i] for i in range(4)), sp.zeros(4))
       - (-2*slash(kv) + 4*m*sp.eye(4))).applyfunc(sp.expand))


# %% [markdown]
# ### The integration-by-parts and reduction identities, numerically (30 digits)

# %%
# integrals with Feynman parameters (Minkowski, measure d^Dq/(i pi^{D/2}); common factor irrelevant):
# I(a,b) = int 1/[(q^2)^a ((q+p)^2-m^2)^b]
mp.mp.dps = 30
def I_ab(a, b, Dn, P2, M2):
    if a == 0:
        return (-1)**b*mp.gamma(b - Dn/2)/mp.gamma(b)*M2**(Dn/2 - b)
    if b == 0:
        return mp.mpf(0)
    # x^{a-1}(1-x)^{b-1} Delta^{D/2-a-b}, Delta = (1-x)(M2 - x P2) = x^{a-1}(1-x)^{D/2-a-1}(M2-xP2)^{D/2-a-b};
    # substitute t = (1-x)^s, s = D/2 - a, to remove the integrable endpoint singularity at x = 1
    s = Dn/2 - a
    f = lambda t: (1 - t**(1/s))**(a - 1)*(M2 - (1 - t**(1/s))*P2)**(Dn/2 - a - b)/s
    return (-1)**(a + b)*mp.gamma(a + b - Dn/2)/(mp.gamma(a)*mp.gamma(b))*mp.quad(f, [0, 1])
def B1_num(Dn, P2, M2):   # int k^mu/[(k^2-m^2)(k-p)^2] = -p^mu B1(p^2;m^2,0)
    f = lambda x: x*((1 - x)*M2 - x*(1 - x)*P2)**(Dn/2 - 2)
    return -mp.gamma(2 - Dn/2)*mp.quad(f, [0, 1])
def U_num(Dn, P2, M2):    # int q^mu/[(q^2)^2 ((q+p)^2-m^2)] = p^mu U
    f = lambda x: x*(1 - x)*((1 - x)*M2 - x*(1 - x)*P2)**(Dn/2 - 3)
    return mp.gamma(3 - Dn/2)*mp.quad(f, [0, 0.5, 1])
for (Dn, P2, M2) in [(mp.mpf('4.37'), mp.mpf('-0.7'), mp.mpf(1)), (mp.mpf('4.61'), mp.mpf('0.3'), mp.mpf('1.3'))]:
    I = lambda a, b: I_ab(a, b, Dn, P2, M2)
    r1 = (Dn - 3)*I(1, 1) - I(0, 2) - (M2 - P2)*I(1, 2)
    r2 = (Dn - 3)*I(1, 1) - I(2, 0) - (M2 - P2)*I(2, 1) - 2*M2*I(1, 2)
    r3 = I(0, 2) - (Dn - 2)/(2*M2)*I(0, 1)
    Jf = ((Dn - 2)*I(0, 1) - (Dn - 3)*(M2 + P2)*I(1, 1))/(M2 - P2)**2
    b1 = B1_num(Dn, P2, M2)
    r4 = P2*b1 - (I(0, 1) - (P2 + M2)*I(1, 1))/2
    r5 = 2*P2*U_num(Dn, P2, M2) - (-I(1, 1) - (P2 - M2)*I(2, 1))
    for nm, r in [("IBP v=q, a=b=1", r1), ("IBP v=q+p, a=b=1", r2), ("I(0,2) = (D-2)A0/(2m^2)", r3),
                  ("I(2,1) closed form", I(2, 1) - Jf), ("p^2 B1 = [A0-(p^2+m^2)B0]/2", r4), ("2p^2 U = -B0-(p^2-m^2)I(2,1)", r5)]:
        good = abs(r) < mp.mpf(10)**(-20)
        ok.append(good)
        print(f"{'OK ' if good else 'FAIL'} [D={Dn}, p2={P2}, m2={M2}] {nm}: residual {mp.nstr(r, 3)}")

# %% [markdown]
# ### Sigma_V, Sigma_S and the counterterms

# %%
# symbolic: the pslash coefficient of P(pslash U + ...)P combination is (D-2) B1, the m coefficient B0
Jsym = ((D - 2)*A0 - (D - 3)*(m2 + p2)*B0)/(m2 - p2)**2
Usym = (-B0 - (p2 - m2)*Jsym)/(2*p2)
B1sym = (A0 - (p2 + m2)*B0)/(2*p2)
# (K/i) int P(k+m)P/(D(k) q^4) = [-B0 - (p^2-m^2)J] P - (p^2-m^2) pslash U + (p^2-m^2) J P
pcoef = (-B0 - (p2 - m2)*Jsym) - (p2 - m2)*Usym + (p2 - m2)*Jsym
mcoef = -((-B0 - (p2 - m2)*Jsym) + (p2 - m2)*Jsym)
check("gauge part: pslash coefficient = (D-2) B1", pcoef - (D - 2)*B1sym)
check("gauge part: m coefficient = B0", mcoef - B0)
check("B0 + (p^2-m^2) J = [(D-2)(A0 - m^2 B0) - (D-4) p^2 B0]/(p^2-m^2)",
      B0 + (p2 - m2)*Jsym - ((D - 2)*(A0 - m2*B0) - (D - 4)*p2*B0)/(p2 - m2))
# total: Feynman part (D-2) pslash B1 + D m B0, gauge part -eta[(D-2) pslash B1 + m B0]
SV = (D - 2)*B1 - eta*(D - 2)*B1
SS = D*B0 - eta*B0
check("Sigma_V = xi (D-2) B1", SV - xi*(D - 2)*B1)
check("Sigma_S = (D-1+xi) B0", SS - (D - 1 + xi)*B0)
b1f, b0f = sp.symbols('b1f b0f')
sv = sp.series((xi*(D - 2)*(-1/(2*eps) + b1f)).subs(D, 4 - 2*eps), eps, 0, 1).removeO()
ss = sp.series(((D - 1 + xi)*(1/eps + b0f)).subs(D, 4 - 2*eps), eps, 0, 1).removeO()
check("xi(D-2)B1 = -xi/eps + xi(1 + 2 B1^f)", sp.expand(sv - (-xi/eps + xi*(1 + 2*b1f))))
check("(D-1+xi)B0 = (3+xi)/eps + (3+xi)B0^f - 2", sp.expand(ss - ((3 + xi)/eps + (3 + xi)*b0f - 2)))
check("B1 pole = -1/2: [A0 - (p^2+m^2)B0]/(2p^2) with A0 -> m^2/eps, B0 -> 1/eps",
      ((m2 - (p2 + m2))/(2*p2)) + sp.Rational(1, 2))
# counterterms: delta2 pslash - (delta2+delta_m) m = pole of Sigma = [-xi pslash + (3+xi) m]/eps
d2_, dm_ = sp.symbols('d2 dm')
sol = sp.solve([d2_ + xi, -(d2_ + dm_) - (3 + xi)], [d2_, dm_])
check("delta2 = -xi C_F, delta_m = -3 C_F", (sol[d2_] + xi) + (sol[dm_] + 3))

sol, sp.expand(sv), sp.expand(ss)          # inspect: delta_2, delta_m (units C_F) and the expanded Sigma_V, Sigma_S

# %% [markdown]
# ## R3: the heavy quark on shell (app:os)

# %%
print("=== R3: heavy quark on shell ===")
N = sp.symbols('N')  # N = Gamma(1+eps)(4 pi mu^2/m^2)^eps
x = sp.symbols('x', positive=True)
A0os = m2*N/(eps*(1 - eps))
en = sp.symbols('en', negative=True)
check("int_0^1 x^{-2eps} dx = 1/(1-2eps)", sp.integrate(x**(-2*en), (x, 0, 1)) - 1/(1 - 2*en))
check("int_0^1 (1-x) x^{-1-2eps} dx = -1/(2eps) - 1/(1-2eps)  (eps<0)",
      sp.integrate((1 - x)*x**(-1 - 2*en), (x, 0, 1)) - (-1/(2*en) - 1/(1 - 2*en)))
B0os = N/(eps*(1 - 2*eps))     # B0(m^2;m^2,0) = N/eps int x^{-2eps}
check("B0(m^2;m^2,0) = (D-2)A0/(2(D-3)m^2) exactly", (B0os - ((D - 2)*A0os/(2*(D - 3)*m2)).subs(D, 4 - 2*eps)))
B1os = A0os/(2*m2) - B0os
check("B1(m^2;m^2,0) = -A0/(2(D-3)m^2) exactly", (B1os + (A0os/(2*(D - 3)*m2)).subs(D, 4 - 2*eps)))
# B0'(m^2;m^2,0): d/dp^2 of N/eps int dx [x m^2 - x(1-x) p^2]^{-eps} (m^2)^eps at p^2 = m^2
# = N/m^2 int (1-x) x^{-1-2eps} dx  (eps < 0)
B0pos = N/m2*(sp.Rational(-1, 2)/eps - 1/(1 - 2*eps))
check("B0'(m^2;m^2,0) = -N/(2 eps (1-2eps) m^2)", B0pos + N/(2*eps*(1 - 2*eps)*m2))
check("B0' = -(D-2)A0/(4(D-3)m^4) exactly", (B0pos + ((D - 2)*A0os/(4*(D - 3)*m2**2)).subs(D, 4 - 2*eps)))
B1pos = -A0os/(2*m2**2) + B0os/(2*m2) - B0pos
check("B1' = A0/(2(D-3)m^4) exactly", (B1pos - (A0os/(2*(D - 3)*m2**2)).subs(D, 4 - 2*eps)))
msb = lambda e: sp.expand(sp.series(e.subs(N, 1 + eps*L), eps, 0, 1).removeO())
check("A0^f = m^2(1+L)", msb(A0os) - (m2/eps + m2*(1 + L)))
check("B0^f(m^2;m^2,0) = 2+L", msb(B0os) - (1/eps + 2 + L))
check("B1^f(m^2;m^2,0) = -3/2 - L/2", msb(B1os) - (-1/(2*eps) - sp.Rational(3, 2) - L/2))
check("B0'(m^2;m^2,0) = -(1/eps_IR + 2 + L)/(2m^2)", msb(B0pos) - (-(1/eps + 2 + L)/(2*m2)))
# pole mass from eq:VR
SVR = xi*(1 + 2*(-sp.Rational(3, 2) - L/2))
SSR = (3 + xi)*(2 + L) - 2
check("Sigma_V^R + Sigma_S^R on shell = 4 + 3L (xi cancels)", sp.expand(SVR + SSR - (4 + 3*L)))
# bare on-shell sum and delta m
SVb = (xi*(D - 2)*B1os).subs(D, 4 - 2*eps)
SSb = ((D - 1 + xi)*B0os).subs(D, 4 - 2*eps)
check("Sigma_V + Sigma_S (bare, on shell) = (D-1)(D-2)A0/(2(D-3)m^2)",
      sp.simplify(SVb + SSb - ((D - 1)*(D - 2)*A0os/(2*(D - 3)*m2)).subs(D, 4 - 2*eps)))
check("(D-1)(D-2)/(2(D-3)) = 3 + eps + O(eps^2)",
      sp.series(((D - 1)*(D - 2)/(2*(D - 3))).subs(D, 4 - 2*eps), eps, 0, 2).removeO() - (3 + eps))
check("delta m/m = -C_F a (3/eps + 4 + 3L)", msb(-((D - 1)*(D - 2)*A0os/(2*(D - 3)*m2)).subs(D, 4 - 2*eps)) + (3/eps + 4 + 3*L))
# residue: R - 1 = Sigma_V - delta2 + 2m^2(Sigma_V' + Sigma_S'), with the exact D-dim expressions
SVp = (xi*(D - 2)*B1pos).subs(D, 4 - 2*eps)
SSp = ((D - 1 + xi)*B0pos).subs(D, 4 - 2*eps)
bare = SVb + 2*m2*(SVp + SSp)
check("Sigma_V + 2m^2(Sigma_V'+Sigma_S') = -(D-1)(D-2)A0/(2(D-3)m^2): xi cancels exactly",
      sp.simplify(bare + ((D - 1)*(D - 2)*A0os/(2*(D - 3)*m2)).subs(D, 4 - 2*eps)))
# UV/IR split: UV pole of bare is that of Sigma_V (derivatives UV finite): -xi/eps_UV; the rest IR
eU, eI = sp.symbols('eUV eIR')
bare = sp.cancel(sp.together(bare))
tot_pole = msb(bare).coeff(eps, -1)
check("total 1/eps coefficient of the bracket = -3", tot_pole + 3)
RQ = xi/eU - xi/eU - (3 - xi)/eI + (msb(bare) - msb(bare).coeff(eps, -1)/eps)
check("R_Q - 1 = -[(3-xi)DIR + 4 + 3L]", sp.expand(RQ - (-(3 - xi)/eI - 4 - 3*L)))
# the 4-dim-coefficient route: xi(1+2B1) + 4m^2 xi B1' + 2m^2(3+xi)B0' + 2(1-xi)
B1p_f = msb(B1pos)    # = (1/eps_IR + 3 + L)/(2m^2)
check("B1'(m^2;m^2,0) = (1/eps_IR + 3 + L)/(2m^2)", B1p_f - (1/eps + 3 + L)/(2*m2))
check("(D-2)B1' = 2B1' - 1/m^2 + O(eps)", msb(((D - 2)*B1pos).subs(D, 4 - 2*eps)) - (2*B1p_f - 1/m2))
check("(D-1+xi)B0' = (3+xi)B0' + 1/m^2 + O(eps)", msb(((D - 1 + xi)*B0pos).subs(D, 4 - 2*eps)) - ((3 + xi)*msb(B0pos) + 1/m2))
route = SVR + 4*m2*xi*B1p_f + 2*m2*(3 + xi)*msb(B0pos) + 2*(1 - xi)
check("xi(1+2B1)+4m^2 xi B1'+2m^2(3+xi)B0'+2(1-xi) = -(3-xi)/eps_IR - 4 - 3L", sp.expand(route - (-(3 - xi)/eps - 4 - 3*L)))
route_wrong = SVR + 4*m2*xi*B1p_f + 2*m2*(3 + xi)*msb(B0pos)
print("     (dropping the O(eps) x IR-pole terms would give ", sp.expand(route_wrong), ")")

msb(bare)          # inspect: the bracket of R_Q - 1 (MS-bar; 1/eps = DIR after the UV/IR split)

# %% [markdown]
# ## R4: the massless residues (app:os)

# %%
print("=== R4: massless residues ===")
cA = sp.Rational(1, 2)*((3*D - 2)/(D - 1) + (2*D - 7)*eta - (D - 4)/4*eta**2)
cq = -2*(D - 2)/(D - 1)
check("C_A coefficient at D=4 = 13/6 - xi/2", sp.expand(cA.subs(D, 4) - (sp.Rational(13, 6) - xi/2)))
check("massless-quark coefficient at D=4 = -4/3", cq.subs(D, 4) + sp.Rational(4, 3))
c1 = sp.series(cA.subs(D, 4 - 2*eps), eps, 0, 2).removeO().coeff(eps, 1)
check("O(eps) part of the C_A coefficient = 1/9 - 2 eta + eta^2/4", sp.expand(c1 - (sp.Rational(1, 9) - 2*eta + eta**2/4)))
# c(D) * (1/eps_UV - 1/eps_IR) = c(4)(1/eps_UV - 1/eps_IR) + c1 eps (1/eps_UV - 1/eps_IR) with eps_UV = eps_IR = eps
check("eps (1/eps_UV - 1/eps_IR) = 0 for eps_UV = eps_IR", (eps*(1/eU - 1/eI)).subs({eU: eps, eI: eps}))
# heavy quark at k^2 = 0: B0(k^2;m,m) = G(eps) X^eps int [1 - x(1-x)k^2/m^2]^{-eps}
kk = sp.symbols('kk')
B0k = sp.gamma(eps)*X**eps*sp.Integral((1 - x*(1 - x)*kk/m2)**(-eps), (x, 0, 1))
B0p0 = sp.simplify(sp.diff(B0k, kk).subs(kk, 0).doit())
check("B0'(0;m^2,m^2) = Gamma(1+eps) X^eps/(6 m^2) exactly", sp.gammasimp(B0p0 - sp.gamma(1 + eps)*X**eps/(6*m2)))
PiQ0 = (-2/(D - 1)*((D - 2)*B00ex + 4*m2*sp.gamma(1 + eps)*X**eps/(6*m2))).subs(D, 4 - 2*eps)
check("Pi_Q(0) = -(4/3) T_F B0(0;m^2,m^2) exactly in D dims", sp.gammasimp(PiQ0 + sp.Rational(4, 3)*B00ex))
check("eq:VR quark bracket at k^2 -> 0: B0(0) + 2m^2 B0'(0) - 1/3 = B0(0)",
      sp.Rational(1, 3) - sp.Rational(1, 3))   # 2 m^2 * 1/(6 m^2) = 1/3
# R_G
CA, TF, nl = sp.symbols('C_A T_F n_l')
PiR0 = -(cA.subs(D, 4)*CA + cq.subs(D, 4)*TF*nl)/eI - sp.Rational(4, 3)*TF*L
RG = -((sp.Rational(13, 6) - xi/2)*CA - sp.Rational(4, 3)*TF*nl)/eI - sp.Rational(4, 3)*TF*L
check("Pi^R(0) = eq:os R_G - 1", sp.expand(PiR0 - RG))
# massless quark residue
check("Sigma_V(p^2;0,0) = -xi(1-eps)B0: xi(D-2)(-B0/2)", sp.expand((xi*(D - 2)*(-sp.Rational(1, 2))).subs(D, 4 - 2*eps) + xi*(1 - eps)))

RG          # inspect: R_G - 1 of Eq. (os)

# %%
print()
print("ALL OK" if all(ok) else f"FAILURES: {ok.count(False)}")
