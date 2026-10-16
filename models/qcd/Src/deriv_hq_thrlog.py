# %% [markdown]
# # Appendix check: threshold logarithms of the heavy-quark f^(1)
#
# Research note models/qcd, derivations of the appendices (sympy, mpmath).  app:hq 「閾値の対数。」 (I2): the threshold logarithms of
# Eq. (hqthr) from the soft real emission + the MS-bar collinear counterterm + the virtual poles of Eq. (irpole).
# (1) symbolic: R + C + V at threshold; the poles cancel iff gamma_i = -2 c_i; the finite ln(8 beta^2) terms 2 C_i and -(8 C_i + w8 C_A);
# (2) the elementary integrals, the eikonal colour algebra at threshold, the prefactor, w8;
# (3) the leading-power predictions against the pieces K sigma_V, K sigma_C, K sigma_R of hq_assemble.wl (work/hq/assemble_*.log);
# (4) the exact f^(1) (results/hq_f1_*.csv) against Eq. (hqthr) with the constants a_ij of Czakon-Mitov (hq_lib.py): the residual / beta.
# Reads work/hq/born.m, work/hq/assemble_qq.log, work/hq/assemble_gg.log (run_hq_check.sh must have been run first; work/ is not in the
# repository), results/hq_f1_qq.csv, results/hq_f1_gg.csv, hq_lib.py.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_hq_thrlog.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_hq_thrlog.py   (about 10 s)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import os
import sys
import re, csv, sys
import sympy as sp
import mpmath as mp
mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
SRC = HERE
ok_all = True

# ---------------------------------------------------------------------------------------------------------------

# %% [markdown]
# ## (1) R + C + V at threshold

# %%
print("(1) symbolic: R + C + V at threshold (units a = g^2/K, ratio to the D-dim Born sigma0_D(s)), mu = m = 1")
ep = sp.symbols('epsilon')
Ci, Tw, gi, ci, lb = sp.symbols('C_i T_H2 gamma_i c_i ell')   # Tw = <T_H^2>/B = w8 C_A ; ell = ln beta ; omega_max = beta^2
EG = sp.EulerGamma
Neps = 2**(1 - 2*ep)*sp.gamma(1 - ep)**2/sp.gamma(2 - 2*ep)
# real emission (soft, heavy pair at rest):
#   2 a e^{eps gE}/Gamma(1-eps) (mu/omega_max)^{2eps} Gamma(3/2-eps)/Gamma(3/2-3eps) [ (2C_i/eps^2) 4^-eps Gamma(1-eps)^2 - T_H^2 N_eps Gamma(-2eps) ]
Rhat = 2*sp.exp(ep*EG)/sp.gamma(1 - ep)*sp.exp(-2*ep*2*lb)*sp.gamma(sp.Rational(3, 2) - ep)/sp.gamma(sp.Rational(3, 2) - 3*ep) * \
       (2*Ci/ep**2*4**(-ep)*sp.gamma(1 - ep)**2 - Tw*Neps*sp.gamma(-2*ep))
# collinear counterterm (two legs, P_ii -> 2C_i/(1-z)_+ + c_i delta(1-z)):  (4/eps)[2C_i(ln beta^2 - psi(3/2-eps) - gE) + c_i]
Chat = 4/ep*(2*Ci*(2*lb - sp.polygamma(0, sp.Rational(3, 2) - ep) - EG) + ci)
# virtual poles at threshold from eq:irpole (real part):  -4C_i/eps^2 + (8 C_i ln2 - 2 T_H^2 + 2 gamma_i)/eps
Vhat = -4*Ci/ep**2 + (8*Ci*sp.log(2) - 2*Tw + 2*gi)/ep
def ser(e, n=0):
    return sp.expand(sp.series(e, ep, 0, n + 1).removeO())
Rs, Cs = ser(Rhat), ser(Chat)
tot = sp.expand(Rs + Cs + Vhat)
p2 = sp.simplify(tot.coeff(ep, -2)); p1 = sp.simplify(sp.expand_func(tot.coeff(ep, -1)))
print("  R poles   :", sp.simplify(Rs.coeff(ep, -2)), "/eps^2 ,", sp.nsimplify(sp.simplify(sp.expand_func(Rs.coeff(ep, -1)))), "/eps")
print("  C poles   :", sp.simplify(sp.expand_func(Cs.coeff(ep, -1))), "/eps")
print("  sum of 1/eps^2:", p2, ";  sum of 1/eps:", sp.simplify(p1), "  -> poles cancel iff gamma_i = -2 c_i")
ok_all &= p2 == 0 and sp.simplify(p1 - (2*gi + 4*ci)) == 0
# finite ln(beta) dependence (V has none): from R only (C has ln beta only in its pole)
fin = sp.expand(sp.expand_func(Rs.coeff(ep, 0) + Cs.coeff(ep, 0)))
finC = sp.expand(sp.expand_func(Cs.coeff(ep, 0)))
print("  ln(beta) in C finite part:", sp.Poly(finC, lb).degree() if finC.has(lb) else 0, "(none)")
Lam = sp.symbols('Lambda')                          # Lambda = ln(8 beta^2) = 2 ell + 3 ln2
finL = sp.expand(fin.subs(lb, (Lam - 3*sp.log(2))/2))
c2 = sp.simplify(finL.coeff(Lam, 2)); c1 = sp.simplify(sp.expand_log(finL.coeff(Lam, 1), force=True))
c0 = sp.simplify(finL.coeff(Lam, 0))
print("  finite part of R + C in units a:  Lambda^2 coeff =", c2, ";  Lambda coeff =", c1)
print("  in units alpha_s/pi = 4a:  ", sp.simplify(c2/4), "Lambda^2 +", sp.simplify(c1/4), "Lambda   [eq:hqthr: 2C_i, -(8C_i + w8 C_A)]")
ok_all &= sp.simplify(c2/4 - 2*Ci) == 0 and sp.simplify(c1/4 + 8*Ci + Tw) == 0
c0n = sp.nsimplify(sp.simplify(c0/4))
print("  (constant of R + C, units alpha_s/pi; part of a_ij together with the virtual constant):", sp.simplify(c0/4))

# ---------------------------------------------------------------------------------------------------------------
sp.collect(finL, Lam)          # inspect: the finite part of R + C in Lambda = ln(8 beta^2) (units a)

# %% [markdown]
# ## (2) The elementary integrals

# %%
print("(2) the elementary integrals")
c, w, u = sp.symbols('c omega u', positive=True)
a_ = sp.symbols('alpha', positive=True)
print("  int_{-1}^1 (1-c^2)^(a-1) dc = 2^(2a-1) Gamma(a)^2/Gamma(2a):",
      [mp.nstr(mp.quad(lambda x: (1 - x*x)**(av - 1), [-1, 0, 1]) - 2**(2*av - 1)*mp.gamma(av)**2/mp.gamma(2*av), 3) for av in (mp.mpf('0.3'), mp.mpf('1.2'))])
print("  int_0^1 [(1-u)^(1/2-eps) - 1]/u du = -(psi(3/2-eps) + gE):",
      [mp.nstr(mp.quad(lambda x: ((1 - x)**(mp.mpf(1)/2 - e) - 1)/x, [0, 1]) + mp.digamma(mp.mpf(3)/2 - e) + mp.euler, 3) for e in (mp.mpf(0), mp.mpf('-0.2'))])
print("  int_0^1 dw w^(-1-2eps) (1-w)^(1/2-eps) = Gamma(-2eps)Gamma(3/2-eps)/Gamma(3/2-3eps) (eps=-0.2):",
      mp.nstr(mp.quad(lambda x: x**(-1 + mp.mpf('0.4'))*(1 - x)**(mp.mpf('0.7')), [0, 1]) - mp.gamma(mp.mpf('0.4'))*mp.gamma(mp.mpf('1.7'))/mp.gamma(mp.mpf('2.1')), 3))
# eikonal colour algebra at threshold: T1.T2 = (T_H^2 - 2C_i)/2, T1.T_H = T2.T_H = -T_H^2/2  => -J^2 omega^2 = 4C_i/(1-c^2) - T_H^2
cc = sp.symbols('cth')
TH2 = sp.symbols('T_H2')
mJ2 = -(2*(TH2/2 - Ci)*2/(1 - cc**2) + 2*(-TH2/2)*(1/(1 - cc) + 1/(1 + cc)) + TH2)
print("  -J^2 omega^2 =", sp.simplify(mJ2), "  [expect 4C_i/(1-c^2) - T_H^2]:", sp.simplify(mJ2 - (4*Ci/(1 - cc**2) - TH2)) == 0)
ok_all &= sp.simplify(mJ2 - (4*Ci/(1 - cc**2) - TH2)) == 0
# prefactor g0^2 Omega_{2-2eps} / (2 (2 pi)^{3-2eps}) = 2 a e^{eps gE}/Gamma(1-eps)  (a = g^2/(16 pi^2), g0^2 = g^2 e^{eps gE}(4 pi)^-eps)
g = sp.symbols('g', positive=True)
pref = g**2*sp.exp(ep*EG)*(4*sp.pi)**(-ep)*2*sp.pi**(1 - ep)/sp.gamma(1 - ep)/(2*(2*sp.pi)**(3 - 2*ep))
print("  prefactor / (2 a e^{eps gE}/Gamma(1-eps)) =", sp.simplify(sp.powsimp(pref/(2*g**2/(16*sp.pi**2)*sp.exp(ep*EG)/sp.gamma(1 - ep)), force=True)))
# w8 for g g: singlet and octet weights of {T^a,T^b} at threshold
N = sp.symbols('N', positive=True)
w1 = (N**2 - 1)/N; w8 = (N**2 - 4)*(N**2 - 1)/(2*N)
print("  gg octet fraction w8 =", sp.factor(w8/(w1 + w8)), " (SU(3):", (w8/(w1 + w8)).subs(N, 3), ")")

# ---------------------------------------------------------------------------------------------------------------

# %% [markdown]
# ## (3) Leading power against the pieces of hq_assemble.wl (reads work/hq)

# %%
print("(3) leading-power predictions vs the pieces K sigma_V, K sigma_C, K sigma_R of hq_assemble.wl (work/hq/assemble_*.log)")
# D-dimensional Born ratio F_D(eps) = sigma0(s;eps)/sigma0(s;0) from the note's definitions (hq_assemble.wl)
from sympy.parsing.mathematica import parse_mathematica
txt = open(SRC + '/work/hq/born.m').read()
def born_expr(key):
    i0 = txt.index(f'"{key}" -> <|"born" -> ') + len(f'"{key}" -> <|"born" -> ')
    i1 = txt.index('"cc" -> <|', i0)
    return parse_mathematica(' '.join(txt[i0:i1].strip().rstrip(',').split()))
Ds, ss, ts, CAs, CFs = sp.symbols('D s t CA CF')
CAn, CFn, TFn, nln = 3, sp.Rational(4, 3), sp.Rational(1, 2), 5
b0nl = sp.Rational(11, 3)*CAn - sp.Rational(4, 3)*TFn*nln
def FD_series(key, sv):
    """Taylor coefficients (1, F1, F2) of sigma0(s; eps)/sigma0(s; 0), with the definitions of hq_assemble.wl"""
    sv_ = sp.nsimplify(sv)
    bD = born_expr(key).subs({CAs: CAn, CFs: CFn, ss: sv_})
    # born is a polynomial (degree <= 2) in D: b(4 - 2 eps) = b(4) - 2 eps b'(4) + 2 eps^2 b''(4)
    bk = [sp.lambdify(ts, e, 'mpmath') for e in (bD.subs(Ds, 4), -2*sp.diff(bD, Ds).subs(Ds, 4), 2*sp.diff(bD, Ds, 2).subs(Ds, 4))]
    beta = mp.sqrt(1 - 4/mp.mpf(sv_))
    tof = lambda x: 1 - mp.mpf(sv_)/2*(1 - beta*x)
    l = lambda x: mp.log(1 - x*x)
    I0 = mp.quad(lambda x: bk[0](tof(x)), [-1, 0, 1])
    I1 = mp.quad(lambda x: bk[1](tof(x)) - l(x)*bk[0](tof(x)), [-1, 0, 1])
    I2 = mp.quad(lambda x: bk[2](tof(x)) - l(x)*bk[1](tof(x)) + l(x)**2/2*bk[0](tof(x)), [-1, 0, 1])
    svm = mp.mpf(sv_)
    def other(e):
        avg = 4*CAn**2 if key == "A" else 4*(1 - e)**2*(CAn**2 - 1)**2
        phi2 = 2*mp.pi**((3 - 2*e)/2)/mp.gamma((3 - 2*e)/2)*(beta*mp.sqrt(svm)/2)**(1 - 2*e)/(4*(2*mp.pi)**(2 - 2*e)*mp.sqrt(svm))
        neps = 2**(1 - 2*e)*mp.gamma(1 - e)**2/mp.gamma(2 - 2*e)
        return mp.e**(2*e*mp.euler)*(4*mp.pi)**(-2*e)*phi2/avg/neps
    o = mp.taylor(other, 0, 2); o = [x/o[0] for x in o]
    Fa = [1, I1/I0, I2/I0]
    return [mp.mpf(1), o[1] + Fa[1], o[2] + o[1]*Fa[1] + Fa[2]]
def laurent(expr, lo=-2, hi=0):
    se = sp.series(expr, ep, 0, hi + 1).removeO()
    return {k: complex(sp.N(se.coeff(ep, k), 30)) for k in range(lo, hi + 1)}
def parse_log(chan):
    out = {}
    lines = open(SRC + f'/work/hq/assemble_{chan}.log').read().split('\n')
    for i, ln in enumerate(lines):
        mm = re.match(rf'{chan} s = (\S+) \(beta = ([\d.]+)', ln)
        if not mm: continue
        sv = sp.nsimplify(mm.group(1)); b = float(mm.group(2))
        blob = ln + ' ' + lines[i + 1]
        def grab(tag):
            src = ln if (tag + ' = ') in ln else lines[i + 1]
            seg = src.split(tag + ' = ')[1].split(';')[0]
            seg = re.sub(r'`+[\d.]*', '', seg).replace('*^', 'e').replace('^', '**')
            e = sp.sympify(seg, locals={'ep': ep, 'I': sp.I})
            return {k: complex(sp.expand(e).coeff(ep, k)) for k in (-2, -1, 0)}
        f0 = float(re.sub(r'`.*', '', blob.split('f0 = ')[1].split(';')[0]))
        out[b] = dict(s=sv, f0=f0, V=grab('K sigma_V'), C=grab('K sigma_C'), R=grab('K sigma_R'))
    return out
K = 16*mp.pi**2
setup = {"qq": ("A", CFn, 1, -3*CFn, sp.Rational(3, 2)*CFn), "gg": ("B", CAn, sp.Rational(5, 7), -b0nl, b0nl/2)}
for chan in ("qq", "gg"):
    key, Cv, w8v, gv, cv = setup[chan]
    data = parse_log(chan)
    print(f"  channel {chan}: C_i = {Cv}, w8 = {w8v}, gamma_i = {gv}, c_i = {cv}")
    for b in (0.02, 0.05, 0.1):
        d = data[b]; sv = d['s']
        F = FD_series(key, sv)
        bet = mp.sqrt(1 - 4/mp.mpf(sv)); wmax = (mp.mpf(sv) - 4)/(2*mp.sqrt(mp.mpf(sv)))
        subs = {Ci: Cv, Tw: w8v*CAn, gi: gv, ci: cv}
        lr = {k: mp.mpf(sp.N(sp.expand_func(Rs.coeff(ep, k)).subs(subs).subs(lb, sp.log(sp.Float(str(wmax), 40))/2), 40)) for k in (-2, -1, 0)}
        lc = {k: mp.mpf(sp.N(sp.expand_func(Cs.coeff(ep, k)).subs(subs).subs(lb, sp.log(sp.Float(str(bet), 40))), 40)) for k in (-2, -1, 0)}
        lv = {k: mp.mpf(sp.N(Vhat.subs(subs).coeff(ep, k), 40)) for k in (-2, -1)}; lv[0] = mp.mpf(0)
        pref_ = d['f0']/K
        def times_F(lc_):
            return {-2: pref_*lc_[-2], -1: pref_*(lc_[-1] + F[1]*lc_[-2]), 0: pref_*(lc_[0] + F[1]*lc_[-1] + F[2]*lc_[-2])}
        pr = {"R": times_F(lr), "C": times_F(lc), "V": times_F(lv)}
        print(f"    beta = {b}:")
        for X in ("V", "C", "R"):
            row = []
            for k in (-2, -1, 0):
                if X == "V" and k == 0: continue
                lgv, pv = d[X][k].real, float(pr[X][k])
                if abs(lgv) < 1e-30 and abs(pv) < 1e-30: continue
                row.append(f"eps^{k}: log {lgv:+.8e} pred {pv:+.8e} rel {abs(lgv - pv)/max(abs(lgv), 1e-300):.1e}")
            print(f"      K sigma_{X}  " + ";  ".join(row))
        # genuine finite part of 2 Re W / B in units a: v0 = K*(K sigma_V)_fin/f0 - [cross terms F_D x poles]
        v0 = float(K)*d['V'][0].real/d['f0'] - float(F[2]*lv[-2] + F[1]*lv[-1])
        Ccoul = float(CFn - w8v*CAn/2)
        print(f"      virtual finite part (units a) minus Coulomb 4 C^Coul pi^2/(2 beta): {v0 - 4*Ccoul*float(sp.pi)**2/(2*b):+.6f}"
              "   (tends to a constant: no ln beta in the virtual correction)")

# ---------------------------------------------------------------------------------------------------------------
data[0.02]          # inspect: the pieces of hq_assemble.wl at beta = 0.02 (g g)

# %% [markdown]
# ## (4) The exact f^(1) against Eq. (hqthr)

# %%
print("(4) exact f^(1) (this work = Czakon-Mitov to 2e-8, results/hq_f1_*.csv) against eq:hqthr with the constants a_ij of")
print("    Czakon-Mitov Eqs. (26), (27) (hq_lib.py); the residual divided by f0/(4 pi^2) must vanish as beta -> 0")
sys.path.insert(0, SRC)
import hq_lib as H
for chan, thr, f0f in (("qq", H.thr_qq, H.f0_qq), ("gg", H.thr_gg, H.f0_gg)):
    rows = sorted(((float(r['beta']), float(r['f1'])) for r in csv.DictReader(open(SRC + f'/results/hq_f1_{chan}.csv'))))
    for b, f1 in rows[:5]:
        rho = 1 - b*b
        res = (f1 - float(thr(b)))/float(f0f(rho)/(4*mp.pi**2))
        print(f"  {chan}  beta = {b:5.2f}:  f1 = {f1:.12f}  eq:hqthr = {float(thr(b)):.12f}  residual/(f0/4pi^2) = {res:+.5f}"
              f"  (residual/beta = {res/b:+.3f};  ln(8 beta^2) = {float(mp.log(8*b*b)):+.3f})")
print("ALL SYMBOLIC CHECKS PASSED" if ok_all else "SOME SYMBOLIC CHECK FAILED")
