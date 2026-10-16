# %% [markdown]
# # Appendix check: one-loop IR poles of the renormalized amplitude
#
# Research note models/qcd, derivations of the appendices (mpmath, sympy).  app:ir 「軟らかい領域。」「3点関数の極。」「共線の領域と外線ごとの定数。」
# 「極の和。」 (I1): Eq. (irpole) from the soft (eikonal) integrals.
# (1) the one-parameter master formula of C0 against the standard two-parameter form (massless, massive and massive-massless pairs) and
#     the massless closed form; (2) the pole parts of 2 s_ij C0 (massive pair Euclidean and physical, massive-massless via 2F1);
# (3) gamma_q from the massless quark form factor of app:ee; (4) c_q, c_g of the splitting functions (number and momentum sum rules),
# gamma_i = -2 c_i; (5) <M0|Z^(1)|M0> of (A) and (B) against tab:scat (SU(3), g = 1, m = mu = 1, s = 10, t = -3, n_l = 5).
# Reads work/hq/born.m (the D-dimensional Born and colour correlations of hq_born.wl): run_hq_check.sh must have been run first
# (work/ is not in the repository).  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_ir_poles.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_ir_poles.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import os
import sys
import re, sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
ok_all = True
def report(name, val, ref, tol):
    global ok_all
    d = abs(val - ref)
    ok = d <= tol*max(1, abs(ref))
    ok_all &= ok
    print(f"  {name}: {mp.nstr(val, 15)}  vs  {mp.nstr(ref, 15)}   |diff| = {mp.nstr(d, 3)}  {'OK' if ok else 'FAIL'}")

# ---------------------------------------------------------------------------------------------

# %% [markdown]
# ## (1) The one-parameter master formula of C0

# %%
print("(1) master formula C0 = e^{eps gE} Gamma(1+eps)/(2 eps) int_0^1 dx (P_x^2)^(-1-eps)  vs the standard")
print("    two-parameter form  -e^{eps gE} Gamma(1+eps) int dx dy Delta^(-1-eps), Delta=(x p_i - y p_j)^2  (eps = -0.3, Euclidean)")
def master(mi2, mj2, pipj, eps):
    # x = X^k, k = -1/eps, removes the integrable x^(-1-eps) end-point behaviour (and likewise at x -> 1)
    k = -1/eps
    f = lambda x, xb: (x*x*mi2 + xb**2*mj2 - 2*x*xb*pipj)**(-1-eps)     # xb = 1 - x, passed exactly
    g = lambda X: k*X**(k-1)*(f(X**k/2, 1 - X**k/2) + f(1 - X**k/2, X**k/2))/2
    return mp.e**(eps*mp.euler)*mp.gamma(1+eps)/(2*eps)*mp.quad(g, [mp.mpf(10)**-60, 1])
def twopar(mi2, mj2, pipj, eps):
    k = -1/eps
    f = lambda x, y: (x*x*mi2 + y*y*mj2 - 2*x*y*pipj)**(-1-eps)
    def g(X):
        x = X**k; jx = k*X**(k-1)
        return jx*mp.quad(lambda Y: k*Y**(k-1)*(1-x)*f(x, (1-x)*Y**k), [mp.mpf(10)**-60, 1])
    return -mp.e**(eps*mp.euler)*mp.gamma(1+eps)*mp.quad(g, [mp.mpf(10)**-60, 1])
mp.mp.dps = 15
eps = mp.mpf('-0.3')
for name, args in [("massless pair, 2p_i.p_j=-3", (0, 0, mp.mpf(-1.5))),
                   ("massive pair, m=1, 2p_i.p_j=-5", (1, 1, mp.mpf(-2.5))),
                   ("massive-massless, m=1, 2p_I.p_j=-3", (1, 0, mp.mpf(-1.5)))]:
    report(name, master(*args, eps), twopar(*args, eps), 1e-8)
mp.mp.dps = 30
# massless closed form of the note (app:ee): C0 = -e^{eps gE} G(1+eps) G(1-eps)^2/(eps^2 G(1-2eps)) (-s)^(-1-eps)
s_ = mp.mpf(-3); eps = mp.mpf('-0.2')
cf = -mp.e**(eps*mp.euler)*mp.gamma(1+eps)*mp.gamma(1-eps)**2/(eps**2*mp.gamma(1-2*eps))*(-s_)**(-1-eps)
report("massless master vs closed form (s=-3, eps=-0.2)", master(0, 0, s_/2, eps), cf, 1e-20)

# ---------------------------------------------------------------------------------------------

# %% [markdown]
# ## (2) Pole parts of 2 s_ij C0

# %%
print("(2) pole parts of 2 s_ij C0 (mu = m = 1)")
# (b) massive pair: s_34 int_0^1 dx / P_x^2 = -2 b coth b, cosh b = -s_34/(2m^2); Euclidean and physical
for s34 in (mp.mpf(-5), mp.mpf(-3)):
    bb = mp.acosh(-s34/2)
    val = s34*mp.quad(lambda x: 1/(x*x + (1-x)**2 - x*(1-x)*s34), [0, 0.5, 1])
    report(f"massive pair, s34={s34}: s34 int dx/P_x^2 vs -2 b coth b", val, -2*bb*mp.coth(bb), 1e-25)
# physical s = 10 (tab:scat): s34 = s - 2m^2 = 8, P_x^2 - i0 = 1 - x(1-x) s - i0; compare with -2 beta34 coth beta34,
# beta34 = i pi - b, cosh b = (s-2)/2  (note: beta34 coth beta34 = (s-2)/(s beta) (b - i pi))
s = mp.mpf(10); beta = mp.sqrt(1 - 4/s)
x1, x2 = (1 - beta)/2, (1 + beta)/2           # zeros of 1 - x(1-x) s
delta = mp.mpf('1e-12')
f = lambda x: 1/(1 - x*(1-x)*s - 1j*delta)
val = (s - 2)*mp.quad(f, [0, x1 - mp.mpf('1e-3'), x1, x1 + mp.mpf('1e-3'), 0.5, x2 - mp.mpf('1e-3'), x2, x2 + mp.mpf('1e-3'), 1], maxdegree=12)
b = mp.log((1 + beta)/(1 - beta))
ref = -2*(s - 2)/(s*beta)*(b - 1j*mp.pi)
report("massive pair, s=10 (physical, -i0): s34 int dx/(P_x^2-i0) vs -2 beta34 coth beta34", val, ref, 1e-8)
report("  beta34 coth beta34 with beta34 = i pi - b, cosh b=(s-2)/2", (1j*mp.pi - mp.acosh((s-2)/2))*mp.coth(1j*mp.pi - mp.acosh((s-2)/2)), (s-2)/(s*beta)*(b - 1j*mp.pi), 1e-25)

# (c) massive-massless: P_x^2 = x [c (1-x) + x m^2], c = -s_Ij > 0;
#     int_0^1 dx x^(-1-eps) f(x) = -f(0)/eps + int_0^1 (f(x)-f(0))/x dx + O(eps),  int (f - f(0))/x = (1/c) ln(c/m^2)
x, c, m = sp.symbols('x c m', positive=True)
fx = 1/(c*(1-x) + x*m**2)
I = sp.integrate(sp.simplify((fx - 1/c)/x), (x, 0, 1))
print("  sympy: int_0^1 (f(x)-f(0))/x dx =", sp.simplify(I), "  [expect log(c/m^2)/c]:",
      sp.simplify(I - sp.log(c/m**2)/c) == 0 or sp.simplify(sp.expand_log(I - sp.log(c/m**2)/c, force=True)) == 0)
cv = mp.mpf(4)
# exact: x^(-1-eps) [c(1-x)+x]^(-1-eps) integrates to a 2F1; check the pole coefficients against the hypergeometric form
hyp = lambda eps: cv**(-1-eps)*mp.gamma(-eps)*mp.gamma(1)/mp.gamma(1-eps)*mp.hyp2f1(1+eps, -eps, 1-eps, 1 - 1/cv)
e1 = mp.mpf('-0.1'); k1 = -1/e1
report("  massive-massless: numeric J(eps=-0.1) vs 2F1 form", mp.quad(lambda X: k1*X**(k1-1)*(X**k1)**(-1-e1)*(cv*(1-X**k1)+X**k1)**(-1-e1), [0, 1]), hyp(e1), 1e-15)
# Laurent coefficients from the 2F1 form via mp.taylor of eps^2 * (-2c) * prefactor * J
F = lambda eps: eps**2*(-2*cv)*mp.e**(eps*mp.euler)*mp.gamma(1+eps)/(2*eps)*hyp(eps)
tc = mp.taylor(F, mp.mpf('1e-30'), 2)
report("  massive-massless: coefficient of 1/eps^2", tc[0], 1, 1e-15)
report("  massive-massless: coefficient of 1/eps  (2 ln(m mu/c))", tc[1], 2*mp.log(1/cv), 1e-15)

# ---------------------------------------------------------------------------------------------

# %% [markdown]
# ## (3) gamma_q from the massless quark form factor

# %%
print("(3) gamma_q from the massless quark form factor F1 = C_F a [(D-7) B0 - 2 s C0] (app:ee), mu^2 = -s")
ep = sp.symbols('epsilon')
D = 4 - 2*ep
B0 = sp.exp(ep*sp.EulerGamma)*sp.gamma(ep)*sp.gamma(1-ep)**2/sp.gamma(2-2*ep)     # (-s)^(-eps) = 1 at mu^2 = -s
sC0 = -(-1)*sp.exp(ep*sp.EulerGamma)*sp.gamma(1+ep)*sp.gamma(1-ep)**2/(ep**2*sp.gamma(1-2*ep))  # s C0 = -s(-s)^(-1-eps)... = +.../eps^2
# s*C0 = s * (-(...)/eps^2) (-s)^(-1-eps) = (...)/eps^2 at mu^2=-s  (since s*(-s)^(-1) = -1)
F1 = sp.series((D - 7)*B0 - 2*sC0, ep, 0, 1).removeO()
pair = sp.series(-2*sC0, ep, 0, 1).removeO()
print("  poles of (D-7)B0 - 2sC0      :", sp.simplify(F1.coeff(ep, -2)), "/eps^2 ,", sp.simplify(F1.coeff(ep, -1)), "/eps")
print("  of which T1.T2 * 2 s C0 (=-C_F 2sC0) gives:", sp.simplify(pair.coeff(ep, -2)), "/eps^2 ,", sp.simplify(pair.coeff(ep, -1)), "/eps")
print("  remainder (gamma_1+gamma_2)/(2 eps) with gamma_q = -3 C_F: -3/eps  ->",
      "OK" if sp.simplify(F1.coeff(ep, -1) - pair.coeff(ep, -1) + 3) == 0 else "FAIL")

# ---------------------------------------------------------------------------------------------
F1          # inspect: (D-7) B0 - 2 s C0 at mu^2 = -s, expanded in eps

# %% [markdown]
# ## (4) c_i of the splitting functions, gamma_i = -2 c_i

# %%
print("(4) delta(1-z) coefficients c_i of P_ii (number and momentum sum rules), gamma_i = -2 c_i")
z, CA, CF, TF, nl = sp.symbols('z C_A C_F T_F n_l', positive=True)
# quark number: int_0^1 P_qq = 0 with P_qq = C_F[2/(1-z)_+ - (1+z)] + c_q delta
cq = -sp.integrate(-CF*(1 + z), (z, 0, 1))
# momentum: int_0^1 z [P_gg + 2 n_l P_qg] = 0, P_gg = 2C_A[z/(1-z)_+ + (1-z)/z + z(1-z)] + c_g delta
plus = sp.integrate((z*z - 1)/(1 - z), (z, 0, 1))          # int z * z/(1-z)_+ = int (z^2 - 1)/(1-z)
cg = -(2*CA*(plus + sp.integrate(z*((1-z)/z + z*(1-z)), (z, 0, 1))) + 2*nl*TF*sp.integrate(z*(z**2 + (1-z)**2), (z, 0, 1)))
# check the quark momentum sum rule is consistent too: int z [P_qq + P_gq] = 0
mom_q = sp.simplify(sp.integrate(z*(-CF*(1+z)), (z, 0, 1)) + CF*sp.integrate(2*(z - 1)/(1 - z), (z, 0, 1)) + cq + sp.integrate(z*CF*(1 + (1-z)**2)/z, (z, 0, 1)))
print("  c_q =", cq, " c_g =", sp.simplify(cg), " (expect 3C_F/2, beta0^(nl)/2 = 11C_A/6 - 2T_F n_l/3);  quark momentum sum rule:", mom_q)
print("  gamma_q = -2c_q =", -2*cq, ", gamma_g = -2c_g =", sp.expand(-2*cg))
ok_all &= sp.simplify(cq - sp.Rational(3, 2)*CF) == 0 and sp.simplify(cg - (sp.Rational(11, 6)*CA - sp.Rational(2, 3)*TF*nl)) == 0 and mom_q == 0

# ---------------------------------------------------------------------------------------------

# %% [markdown]
# ## (5) <M0|Z^(1)|M0> against tab:scat (reads work/hq/born.m)

# %%
print("(5) <M0|Z^(1)|M0> against tab:scat (SU(3), g = 1, m = mu = 1, s = 10, t = -3; n_l = 5)")
txt = open(os.path.join(HERE, 'work', 'hq', 'born.m')).read()
from sympy.parsing.mathematica import parse_mathematica
def split_top(sx):
    out, depth, cur = [], 0, ''
    for ch in sx:
        if ch in '([{': depth += 1
        if ch in ')]}': depth -= 1
        if ch == ',' and depth == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur); return out
def proc(key):
    i0 = txt.index(f'"{key}" -> <|"born" -> ')
    j0 = i0 + len(f'"{key}" -> <|"born" -> ')
    j1 = txt.index('"cc" -> <|', j0)
    born = txt[j0:j1].strip().rstrip(',').strip()
    k1 = txt.index('|>', j1)
    ccs = {}
    for ent in split_top(txt[j1 + len('"cc" -> <|'):k1]):
        mm = re.match(r'\s*\{(\d), (\d)\} -> (.*)', ent, re.S)
        ccs[(int(mm.group(1)), int(mm.group(2)))] = parse_mathematica(' '.join(mm.group(3).split()))
    return parse_mathematica(' '.join(born.split())), ccs
Ds, ss, ts, CAs, CFs = sp.symbols('D s t CA CF')
vals = {CAs: 3, CFs: sp.Rational(4, 3), ss: 10, ts: -3}
u = 2 - 10 + 3
beta = mp.sqrt(1 - mp.mpf(4)/10); b = mp.log((1 + beta)/(1 - beta))
bcoth = (10 - 2)/(10*beta)*(b - 1j*mp.pi)                     # beta34 coth beta34
L12 = -mp.log(10) + 1j*mp.pi                                   # ln(mu^2/(-s - i0))
L13 = -mp.log(1 - (-3)); L14 = -mp.log(1 - u)                  # ln(m mu/(m^2 - t)), ln(m mu/(m^2 - u))
CFn, CAn, TFn, nln = mp.mpf(4)/3, mp.mpf(3), mp.mpf(1)/2, 5
b0nl = 11*CAn/3 - 4*TFn*nln/3
tab = {"A": (mp.mpf('-30.72'), mp.mpc('50.88989', '24.52307'), mp.mpf('11.52')),
       "B": (mp.mpf('-369.6356'), mp.mpc('1104.78228', '-834.72278'), mp.mpf('61.6059'))}
for key, Ci, gi in (("A", CFn, -3*CFn), ("B", CAn, -b0nl)):
    born, cc = proc(key)
    B4 = mp.mpf(sp.N(born.subs(vals).subs(Ds, 4), 30))
    dB = mp.mpf(sp.N(sp.diff(born, Ds).subs(vals).subs(Ds, 4), 30))
    c = {k: mp.mpf(sp.N(v.subs(vals).subs(Ds, 4), 30)) for k, v in cc.items()}
    # colour conservation check
    cons = [c[(1, 2)] + c[(1, 3)] + c[(1, 4)] + Ci*B4, c[(1, 3)] + c[(2, 3)] + c[(3, 4)] + CFn*B4]
    G0 = (4*c[(1, 2)]*L12 - 4*c[(3, 4)]*bcoth + 4*(c[(1, 3)]*L13 + c[(2, 4)]*L13 + c[(1, 4)]*L14 + c[(2, 3)]*L14)
          + (2*gi - 4*CFn)*B4)
    # K W = -(C_1+C_2)/eps^2 B(D) + Gamma0/(2 eps),  B(D) = B4 - 2 eps dB/dD + ...
    W2 = -2*Ci*B4
    W1 = -2*Ci*(-2*dB) + G0/2
    print(f"  ({key}) sum|M0|^2 (D=4) = {mp.nstr(B4, 12)} [tab {tab[key][2]}], colour conservation residues {[mp.nstr(x, 3) for x in cons]}")
    report(f"({key}) KW_-2", W2, tab[key][0], 5e-6)
    report(f"({key}) KW_-1", W1, tab[key][1], 5e-7)
    print(f"      split of KW_-1: Born O(eps) x double pole = {mp.nstr(4*Ci*dB, 12)}, <Gamma0>/2 = {mp.nstr(G0/2, 12)}, <Gamma0>/B(4) = {mp.nstr(G0/B4, 10)}, dB/dD = {mp.nstr(dB, 10)}")
print("ALL CHECKS PASSED" if ok_all else "SOME CHECK FAILED")
c          # inspect: the colour correlations <M0|T_i.T_j|M0> of (B) at D = 4 (i < j)
