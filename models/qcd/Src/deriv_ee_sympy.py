# %% [markdown]
# # Appendix check: e+e- -> hadrons at NLO: reduction, Dirichlet integrals, phase space
#
# Research note models/qcd, derivations of the appendices (sympy, mpmath).
#   app:ee 「仮想の補正。」 (E2): T from the pieces of the text, the reduction rules <1>, <K>, <x>, <y>, <xy> (also numerically at Euclidean
#       kinematics, Feynman parameters), F^(1)/(C_F a) = (D-7) B0 - 2 s C0, C0 from Feynman parameters, C0/B0 = (1-2eps)/(eps s),
#       F^(1) of Eq. (rr), r_V = -4/eps^2 - 6/eps - 16 + 7 pi^2/3;
#   app:ee 「実の補正。」 (E1): the Dirichlet integrals of -g H_3 term by term (also numerically at eps = -0.4), their sum and r_R of Eq. (rr),
#       r_V + r_R = 3;
#   app:ee 「D 次元の位相空間。」: Phi_2, Phi_3 by recursion, the MS-bar factors;
#   app:tree 「(D) e+e- -> q qbar g。」 (E4): the normalization of the fourth line of Eq. (sumtree) at D = 4.
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_ee_sympy.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_ee_sympy.py   (about 2 minutes)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import sympy as sp
import mpmath as mp
INTERACTIVE = "ipykernel" in sys.modules

ep, s, D = sp.symbols('epsilon s D')
x, y, K = sp.symbols('x y K')  # x = k.p1, y = k.p2, K = k^2
G = sp.gamma
EG = sp.EulerGamma


def ok(name, expr):
    e = sp.simplify(expr)
    print(f"{name}: {'OK (0)' if e == 0 else e}")


# %% [markdown]
# ## E2: reduction of the vertex trace

# %%
print("==== E2: reduction of the vertex trace ====")
# hand form of T = tr[N^mu p2 g_mu p1]
T = (-8*s**2 - 16*s*x + 16*s*y + 32*x*y
     + (4-D)*(4*s**2 + 8*s*(x-y) - 4*s*K - 16*x*y) + 2*(4-D)**2*s*K)
# build T from the pieces stated in the text
a_p2 = s/2 - y; b_p1 = s/2 + x; b_p2 = y; a_p1 = -x
tr_bp1 = 4*b_p1; tr_ap1 = 4*a_p1
tr_ba_p2p1 = 2*s**2 + 4*s*(x-y) - 2*s*K
tr_ab_p2p1 = -2*s*K
T_pieces = (-8*a_p2*tr_bp1 + 2*(4-D)*tr_ba_p2p1 + 4*(4-D)*b_p2*tr_ap1 - (4-D)**2*tr_ab_p2p1)
ok("T from the pieces = hand T", sp.expand(T_pieces - T))
# check tr[b a p2 p1] and tr[a b p2 p1] from the 4-trace formula with a = p1-k, b = p2+k
ab = s/2 - y + x - K   # a.b = (p1-k).(p2+k)
p1p2 = s/2


def tr4(ab_, cd, ac, bd, ad, bc):
    return 4*(ab_*cd - ac*bd + ad*bc)


# tr[b a p2 p1]: (b.a)(p2.p1) - (b.p2)(a.p1) + (b.p1)(a.p2)
ok("tr[b a p2 p1]", sp.expand(tr4(ab, p1p2, b_p2, a_p1, b_p1, a_p2) - tr_ba_p2p1))
# tr[a b p2 p1]: (a.b)(p2.p1) - (a.p2)(b.p1) + (a.p1)(b.p2)
ok("tr[a b p2 p1]", sp.expand(tr4(ab, p1p2, a_p2, b_p1, a_p1, b_p2) - tr_ab_p2p1))
# reduction rules: <1>=C0, <K>=B0, <x>=B0/2, <y>=-B0/2, <xy>=s B0/8
B0, C0 = sp.symbols('B0 C0')
Tpoly = sp.Poly(sp.expand(T), x, y, K)
rule = {(0, 0, 0): C0, (0, 0, 1): B0, (1, 0, 0): B0/2, (0, 1, 0): -B0/2, (1, 1, 0): s*B0/8}
red = 0
for mon, c in Tpoly.terms():
    if mon not in rule:
        raise SystemExit(f"unexpected monomial {mon}")
    red += c*rule[mon]
red = sp.expand(red)
ok("<T/(D1D2D3)> = 2(D-2)s[(D-7)B0 - 2s C0]", sp.expand(red - 2*(D-2)*s*((D-7)*B0 - 2*s*C0)))
print("   coefficient of s^2 C0:", sp.factor(red.coeff(C0)/s**2), "; of s B0:", sp.factor(red.coeff(B0)/s))
F1 = sp.simplify(-red/(-2*(D-2)*s))   # F/(C_F a) = -<T>/tr_Born, tr_Born = -2(D-2)s
ok("F^(1)/(C_F a) = (D-7)B0 - 2 s C0", sp.expand(F1 - ((D-7)*B0 - 2*s*C0)))

red          # inspect: <T/(D1 D2 D3)> in B0, C0

# %% [markdown]
# ### The reduction rules, numerically (Euclidean s = -1, eps = -0.3)

# %%
# the reduction rules themselves, checked numerically: massless one-loop integrals in the
# Feynman-parameter representation at Euclidean kinematics s = -1 and eps = -0.3 (finite there)
print("-- numerical check of <x>, <y>, <K>, <xy> rules (Euclidean s=-1, eps=-0.3, Feynman parameters) --")
mp.mp.dps = 30
epsn = mp.mpf('-0.3'); sn = mp.mpf(-1)
# generic one-loop triangle with numerator: use the representation
# <N(k)/(D1D2D3)>, D1=k^2, D2=(k-p1)^2, D3=(k+p2)^2; shift k = l + x2 p1 - x3 p2:
# <1/(D1D2D3)> = -Gamma(1+eps) int (Delta)^(-1-eps), Delta = -x2 x3 s
# numerators: k.p1 = l.p1 - x3 p1.p2 (only), k.p2 = l.p2 + x2 p1.p2, k^2 = l^2 + (x2 p1 - x3 p2)^2
# l^2 terms: <l^2/(-l^2+Delta)^3> etc. are handled with the standard formulas:
#   int d^Dl/(i pi^{D/2}) 1/(-l^2+Delta)^3 = Gamma(1+eps)/2 Delta^(-1-eps)
#   int d^Dl/(i pi^{D/2}) (-l^2)/(-l^2+Delta)^3 = (D/2) Gamma(eps)/2 Delta^(-eps)
#   int d^Dl/(i pi^{D/2}) l^mu l^nu/(-l^2+Delta)^3 = -g^{mu nu}/2 Gamma(eps)/2 Delta^(-eps)
Dn = 4 - 2*epsn


def tri(fun):
    # 2 * int over simplex of fun(x2, x3)   (Feynman parameter measure for three propagators)
    return 2*mp.quad(lambda x2: mp.quad(lambda x3: fun(x2, x3), [0, 1-x2]), [0, 1])


def Dl(x2, x3):
    return -x2*x3*sn


I3 = lambda x2, x3: mp.gamma(1+epsn)/2*Dl(x2, x3)**(-1-epsn)
I3l2 = lambda x2, x3: (Dn/2)*mp.gamma(epsn)/2*Dl(x2, x3)**(-epsn)   # with (-l^2) numerator
# signs: 1/(D1D2D3) = -1/((-D1)(-D2)(-D3))
C0n = -tri(I3)
# <k.p1> : k.p1 -> -x3 s/2 (the l.p1 term integrates to zero)
kp1 = -tri(lambda a, b: (-b*sn/2)*I3(a, b))
kp2 = -tri(lambda a, b: (a*sn/2)*I3(a, b))
# <k^2>: k^2 = l^2 + (x2 p1 - x3 p2)^2 = l^2 - x2 x3 s ; l^2 = -(-l^2)
kk = -tri(lambda a, b: (-a*b*sn)*I3(a, b) - I3l2(a, b))
# <(k.p1)(k.p2)> : (l.p1 - x3 s/2)(l.p2 + x2 s/2) -> l.p1 l.p2 - x2 x3 s^2/4 ; <l.p1 l.p2> = -(p1.p2)/2 Gamma(eps)/2 Delta^-eps
kp1kp2 = -tri(lambda a, b: (-a*b*sn**2/4)*I3(a, b) + (-(sn/2)/2)*mp.gamma(epsn)/2*Dl(a, b)**(-epsn))
B0n = mp.gamma(epsn)*mp.gamma(1-epsn)**2/mp.gamma(2-2*epsn)*(-sn)**(-epsn)
C0closed = -mp.gamma(1+epsn)*mp.gamma(1-epsn)**2/(epsn**2*mp.gamma(1-2*epsn))*(-sn)**(-1-epsn)
print("   C0 numeric vs closed (no e^{eps gE}):", mp.nstr(C0n, 15), mp.nstr(C0closed, 15))
print("   <x>/(B0/2) =", mp.nstr(kp1/(B0n/2), 15), " <y>/(-B0/2) =", mp.nstr(kp2/(-B0n/2), 15),
      " <K>/B0 =", mp.nstr(kk/B0n, 15), " <xy>/(s B0/8) =", mp.nstr(kp1kp2/(sn*B0n/8), 15))


# %% [markdown]
# ## E2: C0 from Feynman parameters, C0/B0, F^(1), r_V

# %%
print("==== E2: C0 from Feynman parameters, ratio, F^(1), r_V ====")
x2, x3 = sp.symbols('x2 x3', positive=True)
k = sp.symbols('k')
# combined denominator: x1 k^2 + x2 (k-p1)^2 + x3 (k+p2)^2 = (k - x2 p1 + x3 p2)^2 + x2 x3 s  (x1+x2+x3=1)
# check with a 2d toy representation: treat k.p1 = kp1, k.p2 = kp2, k^2 = kk, p1.p2 = s/2
kp1s, kp2s, kks, x1 = sp.symbols('kp1 kp2 kk x1')
lhs = x1*kks + x2*(kks - 2*kp1s) + x3*(kks + 2*kp2s)
l2 = kks - 2*x2*kp1s + 2*x3*kp2s + (-2*x2*x3*(s/2))   # (k - x2 p1 + x3 p2)^2
ok("Feynman combination = l^2 - x2 x3 s ... (with x1 = 1-x2-x3)", sp.expand((lhs - (l2 + x2*x3*s)).subs(x1, 1-x2-x3)))
dirichlet = lambda a, b, c: G(a)*G(b)*G(c)/G(a+b+c)
C0_fp = -sp.exp(ep*EG)*G(1+ep)*dirichlet(-ep, -ep, 1)          # times (-s)^(-1-eps)
C0_note = -sp.exp(ep*EG)*G(1+ep)*G(1-ep)**2/(ep**2*G(1-2*ep))
ok("C0 Feynman-parameter form = note's form", sp.gammasimp(C0_fp - C0_note))
B0_note = sp.exp(ep*EG)*G(ep)*G(1-ep)**2/G(2-2*ep)                # times (-s)^(-eps)
ratio = sp.gammasimp(C0_note/B0_note)                             # times (-s)^(-1)
print("   C0/B0 * (-s) =", sp.simplify(ratio), " => C0/B0 =", sp.simplify(-ratio/s))
ok("C0/B0 = +(1-2eps)/(eps s)", sp.simplify(-ratio/s - (1-2*ep)/(ep*s)))
ok("C0/B0 = -2(D-3)/((D-4)s)", sp.simplify(-ratio/s - (-2*(D-3)/((D-4)*s))).subs(D, 4-2*ep))
ok("(D-7) + 4(D-3)/(D-4) = (D^2-7D+16)/(D-4)", sp.simplify((D-7) + 4*(D-3)/(D-4) - (D**2-7*D+16)/(D-4)))
ok("(D^2-7D+16)/(D-4) = -(2-eps+2eps^2)/eps", sp.simplify(((D**2-7*D+16)/(D-4)).subs(D, 4-2*ep) + (2-ep+2*ep**2)/ep))
F1_closed = -(2-ep+2*ep**2)/ep*B0_note
F1_rr = -(2-ep+2*ep**2)/(ep**2*(1-2*ep))*sp.exp(ep*EG)*G(1+ep)*G(1-ep)**2/G(1-2*ep)
ok("F^(1) closed = eq:rr form", sp.gammasimp(F1_closed - F1_rr))
GV = sp.exp(ep*EG)*G(1+ep)*G(1-ep)**2/G(1-2*ep)
print("   e^{eps gE}Gamma(1+eps)Gamma(1-eps)^2/Gamma(1-2eps) =", sp.series(GV, ep, 0, 3).removeO())
print("   (2-eps+2eps^2)/(1-2eps) =", sp.series((2-ep+2*ep**2)/(1-2*ep), ep, 0, 3).removeO())
print("   cos(pi eps) =", sp.series(sp.cos(sp.pi*ep), ep, 0, 3).removeO())
print("   lnGamma(1-eps) =", sp.series(sp.loggamma(1-ep), ep, 0, 3).removeO(),
      "; lnGamma(1+eps) =", sp.series(sp.loggamma(1+ep), ep, 0, 3).removeO())
rV = sp.series(2*F1_rr*sp.cos(sp.pi*ep), ep, 0, 1).removeO()
rV_note = -4/ep**2 - 6/ep - 16 + 7*sp.pi**2/3
ok("r_V/(C_F a) = -4/eps^2 - 6/eps - 16 + 7pi^2/3", sp.simplify(sp.expand(rV) - rV_note))
# pi^2 bookkeeping: cos part and Gamma part
print("   pi^2 from cos: ", sp.expand(-2*2*(-sp.pi**2/2)), "; from Gamma's:", sp.expand(-2*2*(-sp.pi**2/12)))
print("   -2 x 8 =", -2*8)

rV          # inspect: r_V/(C_F a) to eps^0

# %% [markdown]
# ## E1: the Dirichlet integrals for r_R

# %%
print("==== E1: Dirichlet integrals for r_R ====")
d = D
br = 4 + (d-2)*(sp.Symbol('y13')**2 + sp.Symbol('y23')**2) + 2*(d-4)*sp.Symbol('y13')*sp.Symbol('y23') - 4*(sp.Symbol('y13') + sp.Symbol('y23'))
y13, y23 = sp.symbols('y13 y23')
integrand = sp.expand(br/(y13*y23))
print("   integrand terms:", integrand)
# Dirichlet: int y13^{a-1} y23^{b-1} y12^{c-1}, with (y12 y13 y23)^(-eps)
terms = []
total = 0
for term in sp.Add.make_args(integrand):
    c, rest = term.as_independent(y13, y23)
    pd = rest.as_powers_dict()
    # Dirichlet exponents: y13^(alpha-1) with alpha = (power of y13) + 1 - eps, etc.
    a_ = pd.get(y13, 0) + 1 - ep; b_ = pd.get(y23, 0) + 1 - ep; c_ = 1 - ep
    val = c*dirichlet(a_, b_, c_)
    terms.append((term, (a_, b_, c_), val))
    total += val
for t in terms:
    print("   term", t[0], " exponents (y13,y23,y12):", t[1])
four = [4*G(-ep)**2*G(1-ep)/G(1-3*ep),
        2*(d-2)*G(2-ep)*G(-ep)*G(1-ep)/G(3-3*ep),
        2*(d-4)*G(1-ep)**3/G(3-3*ep),
        -8*G(1-ep)**2*G(-ep)/G(2-3*ep)]
four = [f.subs(D, 4-2*ep) for f in four]
total = total.subs(D, 4-2*ep)
ok("sum of Dirichlet terms = sum of the four listed integrals", sp.gammasimp(total - sum(four)))
F0 = G(1-ep)*G(-ep)**2/G(3-3*ep)
pieces = [sp.simplify(sp.gammasimp(f/F0)) for f in four]
print("   each / [Gamma(1-eps)Gamma(-eps)^2/Gamma(3-3eps)]:", [sp.factor(p) for p in pieces])
ok("pieces = 4(2-3e)(1-3e), -4e(1-e)^2, -4e^3, 8e(2-3e)",
   sp.expand(sum(pieces) - (4*(2-3*ep)*(1-3*ep) - 4*ep*(1-ep)**2 - 4*ep**3 + 8*ep*(2-3*ep))))
ok("sum of pieces = 4(2-6e+5e^2-2e^3) = 4(1-2e)(2-2e+e^2)", sp.expand(sum(pieces) - 4*(1-2*ep)*(2-2*ep+ep**2)))
Iclosed = 4*G(1-ep)*(1-2*ep)*(2-2*ep+ep**2)*G(-ep)**2/G(3-3*ep)
ok("I = 4 Gamma(1-e)(1-2e)(2-2e+e^2)Gamma(-e)^2/Gamma(3-3e)", sp.gammasimp(sum(four) - Iclosed))
rR = sp.exp(ep*EG)/G(1-ep)*Iclosed
rR_note = 4*sp.exp(ep*EG)*(1-2*ep)*(2-2*ep+ep**2)*G(-ep)**2/G(3-3*ep)
ok("e^{eps gE}/Gamma(1-eps) * I = eq:rr closed form", sp.gammasimp(rR - rR_note))
rat = (1-2*ep)*(2-2*ep+ep**2)/((2-3*ep)*(1-3*ep))
print("   (1-2e)(2-2e+e^2)/((2-3e)(1-3e)) =", sp.series(rat, ep, 0, 3).removeO())
GR = sp.exp(ep*EG)*G(1-ep)**2/G(1-3*ep)
print("   e^{eps gE}Gamma(1-eps)^2/Gamma(1-3eps) =", sp.series(GR, ep, 0, 3).removeO())
ok("rR closed = (4/eps^2) rat GR", sp.gammasimp(rR_note - 4/ep**2*rat*GR))
rRser = sp.expand(sp.series(rR_note, ep, 0, 1).removeO())
ok("r_R/(C_F a) = 4/eps^2 + 6/eps + 19 - 7pi^2/3", sp.simplify(rRser - (4/ep**2 + 6/ep + 19 - 7*sp.pi**2/3)))
print("   bare Dirichlet sum I (no e^{eps gE}/Gamma(1-eps)) expands to:",
      sp.simplify(sp.expand(sp.series(Iclosed, ep, 0, 1).removeO())))
print("   r_V + r_R =", sp.simplify(rV_note + rRser))

four          # inspect: the four Dirichlet integrals of the text

# %% [markdown]
# ### The Dirichlet formula, numerically (eps = -0.4)

# %%
# numerical check of the Dirichlet formula for each term at eps = -0.4 (convergent)
print("-- numerical Dirichlet check at eps=-0.4 --")
en = mp.mpf('-0.4')
for t in terms:
    f = sp.lambdify((y13, y23), (t[0]*(1-y13-y23)**(-ep)*y13**(-ep)*y23**(-ep)).subs({D: 4-2*ep}).subs(ep, sp.Rational(-2, 5)), 'mpmath')
    num = mp.quad(lambda u: mp.quad(lambda v: f(u, v), [0, 1-u]), [0, 1])
    ex = sp.N(t[2].subs(D, 4-2*ep).subs(ep, sp.Rational(-2, 5)), 20)
    print("   ", t[0], ": numeric", mp.nstr(num, 12), " Dirichlet", sp.N(ex, 12))


# %% [markdown]
# ## E1: the phase space and the MS-bar factor

# %%
print("==== E1: phase space and MS-bar factor ====")
# Phi_2 in D dims, and Phi_3 total by recursion Phi_3 = int ds'/(2pi) Phi_2(s; s', 0) Phi_2(s')
Phi2 = 1/(8*sp.pi)*(4*sp.pi/s)**ep*G(1-ep)/G(2-2*ep)
sp_ = sp.symbols('sp', positive=True)
# two-body with one mass^2 = s' : (1/8pi)(4pi/s)^eps Gamma(1-eps)/Gamma(2-2eps) (1-s'/s)^(1-2eps)
# total: Beta integral int_0^s ds' s'^(-eps) (1-s'/s)^(1-2eps) = s^(1-eps) B(1-eps, 2-2eps)
Phi3_rec = (1/(2*sp.pi))*(1/(8*sp.pi))**2*(4*sp.pi)**(2*ep)*G(1-ep)**2/G(2-2*ep)**2*s**(-ep)*s**(1-ep)*G(1-ep)*G(2-2*ep)/G(3-3*ep)
Phi3_note = Phi2*s/(16*sp.pi**2)*(4*sp.pi/s)**ep/G(1-ep)*G(1-ep)**3/G(3-3*ep)
ok("total Phi_3 (recursion) = Phi_2 * s/(16pi^2)(4pi/s)^eps/Gamma(1-eps) * Dirichlet(1-e,1-e,1-e)",
   sp.simplify(sp.gammasimp(sp.powsimp(sp.expand_power_base(Phi3_rec/Phi3_note, force=True), force=True)) - 1))
# Phi_2 itself from Omega_{D-1}(sqrt s/2)^{D-4}/(8 (2pi)^{D-2})
Om = 2*sp.pi**((3-2*ep)/2)/G((3-2*ep)/2)
Phi2_direct = Om*(s/4)**(-ep)/(8*(2*sp.pi)**(2-2*ep))
print("   Phi_2 direct / note (numeric at eps=0.17, s=2.3):",
      sp.N((Phi2_direct/Phi2).subs({ep: sp.Rational(17, 100), s: sp.Rational(23, 10)}), 20))
# MS-bar: g0^2 (4pi/s)^eps/(16 pi^2) = a e^{eps gE} (mu^2/s)^eps
g, mu = sp.symbols('g mu', positive=True)
g02 = g**2*mu**(2*ep)*(sp.exp(EG)/(4*sp.pi))**ep
print("   g0^2/(16pi^2) (4pi/s)^eps / [a e^{eps gE}(mu^2/s)^eps] (numeric) =",
      sp.N((g02/(16*sp.pi**2)*(4*sp.pi/s)**ep/(g**2/(16*sp.pi**2)*sp.exp(ep*EG)*(mu**2/s)**ep)).subs({ep: sp.Rational(3, 10), s: 3, mu: 2, g: 1}), 20))
# measure: g0^2 int d^Dk/(2pi)^D X = i a <X> with <X> = e^{eps gE} mu^{2eps} int d^Dk/(i pi^{D/2}) X
print("   g0^2 * i pi^{D/2}/(2pi)^D / (i a e^{eps gE} mu^{2eps}) (numeric) =",
      sp.N((g02*sp.pi**(2-ep)/(2*sp.pi)**(4-2*ep)/(g**2/(16*sp.pi**2)*sp.exp(ep*EG)*mu**(2*ep))).subs({ep: sp.Rational(3, 10), mu: 2, g: 1}), 20))


# %% [markdown]
# ## E4: the normalization of Eq. (sumtree) (D) at D = 4

# %%
print("==== E4: normalization of eq:sumtree (D) at D = 4 ====")
gg, CF, dF, f = sp.symbols('g C_F d_F f', positive=True)
H2 = (2*(D-2)*dF*s).subs(D, 4)
print("   -g H2 at D=4 =", H2)
print("   Phi2 at D=4 =", sp.limit(Phi2, ep, 0), "; |k|/(16 pi^2 sqrt s) * 4 pi with |k| = sqrt(s)/2:", sp.simplify(sp.sqrt(s)/2/(16*sp.pi**2*sp.sqrt(s))*4*sp.pi))
dPhi3 = s/(128*sp.pi**3)
print("   dPhi_3 at D=4: Phi2 * s/(16 pi^2) =", sp.simplify(sp.limit(Phi2, ep, 0)*s/(16*sp.pi**2)),
      "; 8 pi^2/(8 (2pi)^5) * (s/4) =", sp.simplify(8*sp.pi**2/(8*(2*sp.pi)**5)*s/4))
R = sp.simplify(dPhi3*8*gg**2*CF*dF*f/(H2*sp.limit(Phi2, ep, 0)))
alphas = gg**2/(4*sp.pi)
ok("ratio = C_F alpha_s/(2 pi) f", sp.simplify(R - CF*alphas/(2*sp.pi)*f))
print("   ratio =", R)
# lepton average <p1^mu p2^nu> = Q^mu Q^nu/6 + s g^{mu nu}/12 (CM frame check)
nvec = sp.symbols('n1 n2 n3')
print("   (lepton average checked in text already; not part of E4)")
R          # inspect: the ratio to the two-body tree (C_F alpha_s/(2 pi) f)
