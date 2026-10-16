# %% [markdown]
# # Appendix check: the C_F T_F n_f part of the two-loop gluon self-energy by hand
#
# Research note models/qcd, derivations of the appendices (sympy).  app:rg 「C_F T_F n_f の部分の手計算。」 (Z2): the hand derivation of
# diagram (c) (the quark loop crossed by a gluon) in the Landau gauge, step by step as in the text: the Feynman part of the trace through
# the two contraction identities, the scaleless terms, the G functions, the kite by the triangle rule, the k k part, the result
# b J_bub2 + s J_sun/(-q^2) exact in D, compared with the pipeline value of the same diagram (results/twoloop_diag4.txt from
# deriv_twoloop_export.wl: FeynArts + FeynCalc + Kira), the eps form of the table row and its poles 0, 0, -2 and finite part -55/3 + 16 zeta3;
# J(11111) = -6 zeta3.  The D-dimensional traces themselves are checked independently with FeynCalc in deriv_twoloop_trace.wl.
# Reads results/twoloop_diag4.txt.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_twoloop_cftf.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_twoloop_cftf.py   (about 1 minute)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import os
import sys
import sympy as sp

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
D, qq, ep = sp.symbols('D qq epsilon')
D1, D2, D3, D4, D5 = sp.symbols('D1:6')
CA, CF, TF, nf = sp.symbols('CA CF TF nf')
ok = True


def report(name, cond):
    global ok
    ok = ok and bool(cond)
    print(f"{name}: {bool(cond)}")


# %% [markdown]
# ## Scalar products in the family k2

# %%
# ---------- scalar products through the family k2 ----------
names = ['l1', 'l2', 'q']
gram = {('l1', 'l1'): D1, ('l2', 'l2'): D2, ('q', 'q'): qq,
        ('l1', 'q'): (D1 + qq - D3) / 2, ('l2', 'q'): (D2 + qq - D4) / 2, ('l1', 'l2'): (D1 + D2 - D5) / 2}


def dot(x, y):
    s = 0
    for i in range(3):
        for j in range(3):
            k = (names[i], names[j]) if (names[i], names[j]) in gram else (names[j], names[i])
            s += x[i] * y[j] * gram[k]
    return sp.expand(s)


def T4(w, x, y, z):  # tr(w x y z) with tr 1 = 4
    return 4 * (dot(w, x) * dot(y, z) - dot(w, y) * dot(x, z) + dot(w, z) * dot(x, y))


l1, l2, q = (1, 0, 0), (0, 1, 0), (0, 0, 1)
a = (1, 0, -1)   # l1 - q
b = (0, 1, -1)   # l2 - q


# %% [markdown]
# ## The Feynman part of the trace

# %%
# ---------- the Feynman part of the trace (two contraction identities) ----------
NF = sp.expand(-32 * dot(a, l2) * dot(b, l1) + 2 * (4 - D) * T4(b, a, l2, l1)
               + 16 * (4 - D) * dot(b, l2) * dot(a, l1) - (4 - D) ** 2 * T4(a, b, l2, l1))
NF_text = (D - 2) * (-4 * qq ** 2 + 2 * (D - 8) * qq * D5 - 4 * D5 ** 2 + 4 * (qq + D5) * (D1 + D2 + D3 + D4)
                     - 4 * (D1 + D4) * (D2 + D3) - 2 * (D - 4) * (D1 * D4 + D2 * D3))
report("g_ab N^ab in D_i equals the bracket of the text", sp.expand(NF - NF_text) == 0)

sp.factor(NF)          # inspect: g_ab N^ab in terms of D1..D5

# %% [markdown]
# ## The k_a k_b part

# %%
# ---------- the k_a k_b part ----------
NL = sp.expand(-4 * (D - 2) * (D1 * D3 * dot(b, l2) - D2 * D3 * dot(b, l1) - D1 * D4 * dot(a, l2) + D2 * D4 * dot(a, l1)))
# (the identity a k b = D3 b - D4 a, l2 k l1 = D1 l2 - D2 l1 and the trace are checked in deriv_twoloop_trace.wl)


# %% [markdown]
# ## G functions

# %%
# ---------- G functions ----------
def G(x, y, d=D):
    return sp.gamma(x + y - d / 2) * sp.gamma(d / 2 - x) * sp.gamma(d / 2 - y) / (sp.gamma(x) * sp.gamma(y) * sp.gamma(d - x - y))


e = (4 - D) / 2
r1 = sp.simplify(sp.gammasimp(G(1, 2) / G(1, 1)))
r2 = sp.simplify(sp.gammasimp(G(1, 1 + e) / G(1, e)))
r3 = sp.simplify(sp.gammasimp(G(2, 1 + e) / G(1, 1 + e)))
report("G(1,2) = -(D-3) G(1,1)", sp.simplify(r1 + (D - 3)) == 0)
report("G(1,1+eps) = (3D-8)/(D-4) G(1,eps)", sp.simplify(r2 - (3 * D - 8) / (D - 4)) == 0)
report("G(2,1+eps) = -(3D-10) G(1,1+eps)", sp.simplify(r3 + (3 * D - 10)) == 0)


# %% [markdown]
# ## The integrals

# %%
# ---------- the integrals, in units of q^2 J_bub2 (symbol Bq) and J_sun (symbol S) ----------
# J_bub2 = E^(2 eps gE) G(1,1)^2 (-q^2)^(-2eps);  J_sun = -E^(2 eps gE) G(1,1) G(eps,1) (-q^2)^(1-2eps)
# so G(1,1) G(1,eps) (-q^2)^(-2eps) = J_sun/q^2.
Bq, S = sp.symbols('Bq S')   # Bq = q^2 J_bub2, S = J_sun
qJ = {}
qJ['11110'] = Bq / qq                              # J[1/(D1 D2 D3 D4)]
qJ['1111m1'] = -qq / 2 * Bq / qq                   # J[D5/(D1 D2 D3 D4)] = -2 J[l1.l2/...] = -(q^2/2) J_bub2
qJ['01111'] = (3 * D - 8) / (D - 4) * S / qq       # G(1,1) G(1,1+eps) (-q^2)^(-2eps)
qJ['sun'] = S                                      # J[1/(D1 D4 D5)] = J[1/(D2 D3 D5)]
J21110 = -(D - 3) * Bq / qq ** 2                   # I(2,1) I(1,1) = -(D-3)/q^2 J_bub2
J20111 = -(3 * D - 10) * (3 * D - 8) / (D - 4) * S / qq ** 2   # -G(1,1) G(2,1+eps) (-q^2)^(-1-2eps)
kite = 2 / (D - 4) * (J21110 - J20111)            # triangle rule: (D-4) J(11111) = 2[J(21110) - J(20111)]
report("q^4 J(11111) = 2/(D-4)[-(D-3) q^2 J_bub2 + (3D-10)(3D-8)/(D-4) J_sun]",
       sp.simplify(qq ** 2 * kite - 2 / (D - 4) * (-(D - 3) * Bq + (3 * D - 10) * (3 * D - 8) / (D - 4) * S)) == 0)

# term by term (scaleless: D5*(D1+...+D4), (D1+D4)(D2+D3))
JF = (D - 2) * (-4 * qq ** 2 * kite + 2 * (D - 8) * qq * qJ['11110'] - 4 * qJ['1111m1']
                + 4 * qq * 4 * qJ['01111'] - 2 * (D - 4) * 2 * qJ['sun'])
JF_text = (D - 2) * (2 * (D ** 2 - 7 * D + 16) / (D - 4) * Bq - 4 * (D ** 3 - 6 * D ** 2 + 20 * D - 32) / (D - 4) ** 2 * S)
report("J[g N/(D1..D5)] = (D-2)[2(D^2-7D+16)/(D-4) q^2 J_bub2 - 4(D^3-6D^2+20D-32)/(D-4)^2 J_sun]", sp.simplify(JF - JF_text) == 0)

# check that the dropped terms of NF are exactly the scaleless ones, and the kept ones are as listed
P = sp.Poly(NF, D1, D2, D3, D4, D5, qq)
kept = {(0, 0, 0, 0, 0, 2), (0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 2, 0), (1, 0, 0, 0, 0, 1), (0, 1, 0, 0, 0, 1), (0, 0, 1, 0, 0, 1),
        (0, 0, 0, 1, 0, 1), (1, 0, 0, 1, 0, 0), (0, 1, 1, 0, 0, 0)}


def scaleless(mon):
    """denominator set after cancelling: index 1 - power; scaleless if l1 or l2 sits in a single propagator (or none) or q drops out"""
    idx = [1 - mon[i] for i in range(5)]
    lines = [i for i in range(5) if idx[i] > 0]
    l1lines = [i for i in lines if i in (0, 2, 4)]
    l2lines = [i for i in lines if i in (1, 3, 4)]
    if len(l1lines) <= 1 or len(l2lines) <= 1:
        return True
    if set(lines) <= {0, 1, 4} or set(lines) <= {2, 3, 4}:   # no q in the propagators
        return True
    return False


dropped = [m for m, c in P.terms() if m not in kept]
report("all other monomials of g N are scaleless", all(scaleless(m) for m in dropped))
report("the kept monomials are not scaleless", all(not scaleless(m) for m in kept))


# %% [markdown]
# ## The longitudinal part

# %%
# ---------- the longitudinal part ----------
# J[(l1-q).l2/(D2 D3 D5^2)]: l1 bubble with indices (1,2) and r = l2 - q, then the l2 integral
# l1 integral = (D-2)/2 G(1,1) (r.l2) (-D4)^(-1-eps);  r.l2 = (D2 + D4 - q^2)/2
# -> (D-2)/4 G(1,1) [G(1,eps) - G(1,1+eps)] (-q^2)^(1-2eps)
rl2 = sp.expand(dot(b, l2))
report("(l2-q).l2 = (D2 + D4 - q^2)/2", sp.expand(rl2 - (D2 + D4 - qq) / 2) == 0)
# X r^2 = (1/2)[r^2 I(1,2) - I(1,1)] with r^2 I(1,2) = -(D-3) I(1,1)  ->  -(D-2)/2 I(1,1)
report("r^2 I(1,2) - I(1,1) = -(D-2) I(1,1)", sp.simplify(-(D - 3) - 1 + (D - 2)) == 0)
JL1 = (D - 2) / 4 * (1 - (3 * D - 8) / (D - 4)) * (-S)  # G(1,1)G(1,eps)(-q^2)^(1-2eps) = -J_sun
report("J[(l1-q).l2/(D2 D3 D5^2)] = (D-2)^2/(2(D-4)) J_sun", sp.simplify(JL1 - (D - 2) ** 2 / (2 * (D - 4)) * S) == 0)
# NL/D5 over D1..D5: the D1 D3 and D2 D4 terms are scaleless; the other two are equal (l1 <-> l2)
PL = sp.Poly(NL, D1, D2, D3, D4, D5, qq)
JL = 8 * (D - 2) * JL1
report("k k N: only D2 D3 (b.l1) and D1 D4 (a.l2) survive, equal under l1<->l2",
       sp.expand(NL - (-4 * (D - 2)) * (D1 * D3 * dot(b, l2) + D2 * D4 * dot(a, l1)) - 4 * (D - 2) * (D2 * D3 * dot(b, l1) + D1 * D4 * dot(a, l2))) == 0)
report("J[k k N/(D1..D5 D5)] = 4(D-2)^3/(D-4) J_sun", sp.simplify(JL - 4 * (D - 2) ** 3 / (D - 4) * S) == 0)


# %% [markdown]
# ## The Landau projector

# %%
# ---------- Landau: P = g - k k/k^2 ----------
JP = sp.simplify(JF - JL)
JP_text = (D - 2) * (2 * (D ** 2 - 7 * D + 16) / (D - 4) * Bq - 8 * (D - 3) * (D ** 2 - 4 * D + 8) / (D - 4) ** 2 * S)
report("J[N P/(D1..D5)] = (D-2)[2(D^2-7D+16)/(D-4) q^2 J_bub2 - 8(D-3)(D^2-4D+8)/(D-4)^2 J_sun]", sp.simplify(JP - JP_text) == 0)
report("(D^3-6D^2+20D-32) + (D-2)^2(D-4) = 2(D-3)(D^2-4D+8)",
       sp.expand((D ** 3 - 6 * D ** 2 + 20 * D - 32) + (D - 2) ** 2 * (D - 4) - 2 * (D - 3) * (D ** 2 - 4 * D + 8)) == 0)

# (D-1) q^2 Pi_(c) = -(C_F - C_A/2) T_F n_f J[N P/...]  ->  Pi = b J_bub2 + s J_sun/(-q^2)
col = (CF - CA / 2) * TF * nf
Pi = -col * JP / ((D - 1) * qq)
bH = sp.simplify(sp.diff(Pi, Bq) * qq)      # coefficient of J_bub2  (Bq = q^2 J_bub2)
sH = sp.simplify(-sp.diff(Pi, S) * qq)      # coefficient of J_sun/(-q^2)
bT = col * (-2 * (D - 2) * (D ** 2 - 7 * D + 16) / ((D - 4) * (D - 1)))
sT = col * (-8 * (D - 2) * (D - 3) * (D ** 2 - 4 * D + 8) / ((D - 4) ** 2 * (D - 1)))
report("Pi_(c) = (C_F-C_A/2)T_F n_f [-2(D-2)(D^2-7D+16)/((D-4)(D-1)) J_bub2 - 8(D-2)(D-3)(D^2-4D+8)/((D-4)^2(D-1)) J_sun/(-q^2)]",
       sp.simplify(bH - bT) == 0 and sp.simplify(sH - sT) == 0)

bH, sH          # inspect: b and s of diagram (c) by hand, exact in D

# %% [markdown]
# ## Comparison with the pipeline (results/twoloop_diag4.txt)

# %%
# ---------- compare with the pipeline (FeynArts/FeynCalc/Kira) ----------
with open(os.path.join(HERE, 'results', 'twoloop_diag4.txt')) as f:
    lines = [l.strip() for l in f if l.strip()]
loc = {'CA': CA, 'CF': CF, 'TF': TF, 'nf': nf, 'D': D}
bP = sp.sympify(lines[0], locals=loc)
sP = sp.sympify(lines[1], locals=loc)
report("hand result = pipeline diagram 4 (b, exact in D)", sp.simplify(bH - bP) == 0)
report("hand result = pipeline diagram 4 (s, exact in D)", sp.simplify(sH - sP) == 0)


# %% [markdown]
# ## The eps form of the table row

# %%
# eps form used in the table
bE = sp.factor(sp.simplify((bT / col).subs(D, 4 - 2 * ep)))
sE = sp.factor(sp.simplify((sT / col).subs(D, 4 - 2 * ep)))
print("b/colour in eps:", bE, ";  s/colour in eps:", sE)
report("b = 4(1-e)(2-e+2e^2)/(e(3-2e))", sp.simplify(bE - 4 * (1 - ep) * (2 - ep + 2 * ep ** 2) / (ep * (3 - 2 * ep))) == 0)
report("s = -16(1-e)(1-2e)(2-2e+e^2)/(e^2(3-2e))", sp.simplify(sE - (-16) * (1 - ep) * (1 - 2 * ep) * (2 - 2 * ep + ep ** 2) / (ep ** 2 * (3 - 2 * ep))) == 0)
bs_ser = sp.series(bE, ep, 0, 2).removeO()
ss_ser = sp.series(sE, ep, 0, 1).removeO()
print("b =", sp.expand(bs_ser), ";  s =", sp.expand(ss_ser))
report("b = 8/(3e) - 20/9 + 68e/27 + ...", sp.expand(bs_ser - (sp.Rational(8, 3) / ep - sp.Rational(20, 9) + sp.Rational(68, 27) * ep)) == 0)
report("s = -32/(3e^2) + 320/(9e) - 944/27 + ...", sp.expand(ss_ser - (-sp.Rational(32, 3) / ep ** 2 + sp.Rational(320, 9) / ep - sp.Rational(944, 27))) == 0)

# expansion with the masters
d4 = 4 - 2 * ep
Jb = sp.exp(2 * ep * sp.EulerGamma) * G(1, 1, d4) ** 2
Js = -sp.exp(2 * ep * sp.EulerGamma) * G(1, 1, d4) * G(ep, 1, d4)
tot = sp.series(bE * Jb + sE * Js, ep, 0, 1).removeO()
coef = [sp.nsimplify(sp.simplify(tot.coeff(ep, k))) for k in (-3, -2, -1, 0)]
print("C_F T_F n_f part of Pi^(2): {1/eps^3, 1/eps^2, 1/eps, 1} =", coef)
report("poles 0, 0, -2", coef[0] == 0 and coef[1] == 0 and coef[2] == -2)
report("finite part -55/3 + 16 zeta3", sp.simplify(coef[3] - (-sp.Rational(55, 3) + 16 * sp.zeta(3))) == 0)
# pieces quoted in the text
bJ = sp.series(bE * Jb, ep, 0, 0).removeO(); sJ = sp.series(sE * Js, ep, 0, 0).removeO()
print("b J_bub2: 1/eps^3..1/eps:", [sp.nsimplify(sp.simplify(bJ.coeff(ep, k))) for k in (-3, -2, -1)])
print("s J_sun/(-q^2): 1/eps^3..1/eps:", [sp.nsimplify(sp.simplify(sJ.coeff(ep, k))) for k in (-3, -2, -1)])
report("b J_bub2 1/eps = 692/27 - 4pi^2/9, s J_sun 1/eps = -746/27 + 4pi^2/9",
       sp.simplify(bJ.coeff(ep, -1) - (sp.Rational(692, 27) - 4 * sp.pi ** 2 / 9)) == 0 and sp.simplify(sJ.coeff(ep, -1) - (-sp.Rational(746, 27) + 4 * sp.pi ** 2 / 9)) == 0)
report("1/eps^2: 76/9 and -76/9", sp.simplify(bJ.coeff(ep, -2) - sp.Rational(76, 9)) == 0 and sp.simplify(sJ.coeff(ep, -2) + sp.Rational(76, 9)) == 0)

coef          # inspect: the C_F T_F n_f part {1/eps^3, 1/eps^2, 1/eps, 1}

# %% [markdown]
# ## The kite

# %%
# the kite: J(11111) at -q^2 = 1 must be -6 zeta3 (Euclidean 6 zeta3/q_E^2 times (-1)^5)
kite_e = (2 / (d4 - 4) * ((d4 - 3) * Jb + (3 * d4 - 10) * (3 * d4 - 8) / (d4 - 4) * Js))
kser = sp.series(kite_e, ep, 0, 1).removeO()
kc = [sp.nsimplify(sp.simplify(kser.coeff(ep, k))) for k in (-3, -2, -1, 0)]
print("J(11111) at -q^2=1 from the triangle rule: {1/eps^3, 1/eps^2, 1/eps, 1} =", kc)
report("J(11111) = -6 zeta3 + O(eps) (known finite kite)", kc[0] == 0 and kc[1] == 0 and kc[2] == 0 and sp.simplify(kc[3] + 6 * sp.zeta(3)) == 0)

print("ALL OK" if ok else "SOME CHECK FAILED")
