# %% [markdown]
# # Appendix check: g g -> g g, colour decomposition and linear-polarization amplitudes
#
# Research note models/qcd, derivations of the appendices (sympy, numpy).
#   app:tree 「(C) gg -> gg。」 (T3): M = -g^2 (c_s X + c_t Y) with linear polarizations in the CM frame:
#   1. sympy, symbolic in c = cos(theta): the kinematic invariants, J(i,j), L_S, L_T, L_U, the contact terms C_s, C_t, C_u, X and Y for all
#      16 configurations (table of the text), the per-class X^2 + Y^2 + XY and the polarization sum 16 (3 - tu/s^2 - su/t^2 - st/u^2)
#      (the third line of Eq. (sumtree));
#   2. numerical cross-check against the explicit-matrix amplitude ampC of tree_sigma.py (SU(3) f^{abc}, Feynman rules of the note,
#      xi = 1 and 3), reused by executing its definitions.
# Reads tree_sigma.py.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_tree_C.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_tree_C.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import itertools
import os
import sys
import sympy as sp
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules

E, c = sp.symbols('E c', positive=True)
sn = sp.sqrt(1 - c ** 2)
dot = lambda a, b: a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
V = lambda *x: sp.Matrix(x)
p1 = V(E, 0, 0, E); p2 = V(E, 0, 0, -E); k1 = V(E, E * sn, 0, E * c); k2 = V(E, -E * sn, 0, -E * c)
q = [p1, p2, -k1, -k2]                                       # all incoming
s = sp.simplify(dot(p1 + p2, p1 + p2)); t = sp.simplify(dot(p1 - k1, p1 - k1)); u = sp.simplify(dot(p1 - k2, p1 - k2))
xh = V(0, 1, 0, 0); yh = V(0, 0, 1, 0); th = V(0, c, 0, -sn)  # x^, y^, theta^ = (0, cos, 0, -sin)
pol = [{'x': xh, 'y': yh}, {'x': xh, 'y': yh}, {'x': th, 'y': yh}, {'x': th, 'y': yh}]
sig = E * sn                                                  # sigma = E sin(theta), sigma^2 = tu/s
S = lambda z: sp.simplify(sp.factor(sp.simplify(z)))
report = []
def chk(label, expr):
    z = S(expr)
    report.append(("OK  " if z == 0 else "FAIL") + " " + label + ("" if z == 0 else f"   residual {z}"))

# kinematic invariants used in the text
chk("s = 4E^2", s - 4 * E ** 2); chk("t = -s(1-c)/2", t + s * (1 - c) / 2); chk("u = -s(1+c)/2", u + s * (1 + c) / 2)
chk("sigma^2 = tu/s", sig ** 2 - t * u / s)
chk("q1.q2 = q3.q4 = s/2", dot(q[0], q[1]) - s / 2); chk("q3.q4", dot(q[2], q[3]) - s / 2)
chk("q1.q3 = q2.q4 = t/2", dot(q[0], q[2]) - t / 2); chk("q2.q4", dot(q[1], q[3]) - t / 2)
chk("q1.q4 = q2.q3 = u/2", dot(q[0], q[3]) - u / 2); chk("q2.q3", dot(q[1], q[2]) - u / 2)
chk("x.q3 = sigma", dot(xh, q[2]) - sig); chk("x.q4 = -sigma", dot(xh, q[3]) + sig)
chk("x.q1 = x.q2 = 0", dot(xh, q[0]) ** 2 + dot(xh, q[1]) ** 2)
chk("th.q1 = sigma", dot(th, q[0]) - sig); chk("th.q2 = -sigma", dot(th, q[1]) + sig)
chk("th.q3 = th.q4 = 0", dot(th, q[2]) ** 2 + dot(th, q[3]) ** 2)
chk("x.x = th.th = y.y = -1", (dot(xh, xh) + 1) ** 2 + (dot(th, th) + 1) ** 2 + (dot(yh, yh) + 1) ** 2)
chk("x.th = -c", dot(xh, th) + c)
chk("(q1-q2).(q3-q4) = t-u", dot(q[0] - q[1], q[2] - q[3]) - (t - u))
chk("(q1-q3).(q2-q4) = s-u", dot(q[0] - q[2], q[1] - q[3]) - (s - u))
chk("(q1-q4).(q2-q3) = s-t", dot(q[0] - q[3], q[1] - q[2]) - (s - t))
chk("t - u = s c", t - u - s * c)


# %% [markdown]
# ## J(i, j), L_S, L_T, L_U, the contact terms, X and Y

# %%
def J(i, j, e):
    """e_i^mu e_j^nu V_{mu nu alpha}(q_i, q_j, -q_i-q_j) with e_i.q_i = 0"""
    return dot(e[i], e[j]) * (q[i] - q[j]) + 2 * dot(e[i], q[j]) * e[j] - 2 * dot(e[j], q[i]) * e[i]

def XY(cfg):
    e = [pol[i][cfg[i]] for i in range(4)]
    for i in range(4):
        assert S(dot(e[i], q[i])) == 0
    LS = dot(J(0, 1, e), J(2, 3, e)); LT = dot(J(0, 2, e), J(1, 3, e)); LU = dot(J(0, 3, e), J(1, 2, e))
    ee = lambda i, j: dot(e[i], e[j])
    Cs = ee(0, 2) * ee(1, 3) - ee(0, 3) * ee(1, 2)
    Ct = ee(0, 1) * ee(2, 3) - ee(0, 3) * ee(1, 2)
    Cu = ee(0, 1) * ee(2, 3) - ee(0, 2) * ee(1, 3)
    X = LS / s - LU / u + Cs - Cu
    Y = LT / t + LU / u + Ct + Cu
    return [S(z) for z in (LS, LT, LU, Cs, Ct, Cu, X, Y)], e


# %% [markdown]
# ## The 16 polarization configurations

# %%
Ssum = (s ** 2 + t ** 2 + u ** 2)
expected = {  # (X, Y) for the four classes, in c and in Mandelstam variables
    'xxxx': ((3 + c ** 2) / (1 + c), -2 * (3 + c ** 2) / (1 - c ** 2), -Ssum / (s * u), -Ssum / (t * u)),
    'yyyy': ((3 + c ** 2) / (1 + c), -2 * (3 + c ** 2) / (1 - c ** 2), -Ssum / (s * u), -Ssum / (t * u)),
    'xxyy': (1 - c, -2, -2 * t / s, -2), 'yyxx': (1 - c, -2, -2 * t / s, -2),
    'xyxy': (2, -4 / (1 - c), 2, 2 * s / t), 'yxyx': (2, -4 / (1 - c), 2, 2 * s / t),
    'xyyx': (-2 * (1 - c) / (1 + c), 4 / (1 + c), -2 * t / u, -2 * s / u), 'yxxy': (-2 * (1 - c) / (1 + c), 4 / (1 + c), -2 * t / u, -2 * s / u),
}
total = 0
table = {}
for cfg in itertools.product('xy', repeat=4):
    name = ''.join(cfg)
    vals, e = XY(name)
    LS, LT, LU, Cs, Ct, Cu, X, Y = vals
    table[name] = vals
    if name.count('y') % 2 == 1:
        chk(f"{name}: odd number of y -> X = Y = 0", X ** 2 + Y ** 2)
    else:
        ex = expected[name]
        chk(f"{name}: X = {ex[0]}", X - ex[0]); chk(f"{name}: Y = {ex[1]}", Y - ex[1])
        chk(f"{name}: X (Mandelstam)", X - ex[2]); chk(f"{name}: Y (Mandelstam)", Y - ex[3])
    total += X ** 2 + Y ** 2 + X * Y

{k: (v[6], v[7]) for k, v in table.items() if k.count('y') % 2 == 0}          # inspect: (X, Y) for an even number of y

# %% [markdown]
# ## Intermediate values quoted in the text

# %%
# intermediate values quoted in the text
LS, LT, LU, Cs, Ct, Cu, X, Y = table['yyyy']
chk("yyyy: L_S = t-u, L_T = s-u, L_U = s-t, C = 0", (LS - (t - u)) ** 2 + (LT - (s - u)) ** 2 + (LU - (s - t)) ** 2 + Cs ** 2 + Ct ** 2 + Cu ** 2)
LS, LT, LU, Cs, Ct, Cu, X, Y = table['xxxx']
chk("xxxx: L_S = t-u", LS - (t - u))
chk("xxxx: L_T = c^2 (s-u) + 8 sigma^2", LT - (c ** 2 * (s - u) + 8 * sig ** 2))
chk("xxxx: L_U = c^2 (s-t) + 8 sigma^2", LU - (c ** 2 * (s - t) + 8 * sig ** 2))
chk("xxxx: C_s = 0, C_t = C_u = 1-c^2", Cs ** 2 + (Ct - (1 - c ** 2)) ** 2 + (Cu - (1 - c ** 2)) ** 2)
LS, LT, LU, Cs, Ct, Cu, X, Y = table['xxyy']
chk("xxyy: L_S = t-u, L_T = L_U = 4 sigma^2, C_s = 0, C_t = C_u = 1",
    (LS - (t - u)) ** 2 + (LT - 4 * sig ** 2) ** 2 + (LU - 4 * sig ** 2) ** 2 + Cs ** 2 + (Ct - 1) ** 2 + (Cu - 1) ** 2)
LS, LT, LU, Cs, Ct, Cu, X, Y = table['yyxx']
chk("yyxx: same L and C as xxyy",
    (LS - (t - u)) ** 2 + (LT - 4 * sig ** 2) ** 2 + (LU - 4 * sig ** 2) ** 2 + Cs ** 2 + (Ct - 1) ** 2 + (Cu - 1) ** 2)
LS, LT, LU, Cs, Ct, Cu, X, Y = table['xyxy']
chk("xyxy: L_S = 0, L_T = c(s-u) + 4 sigma^2, L_U = 4 sigma^2, (C_s, C_t, C_u) = (c, 0, -c)",
    LS ** 2 + (LT - (c * (s - u) + 4 * sig ** 2)) ** 2 + (LU - 4 * sig ** 2) ** 2 + (Cs - c) ** 2 + Ct ** 2 + (Cu + c) ** 2)
LS, LT, LU, Cs, Ct, Cu, X, Y = table['xyyx']
chk("xyyx: L_S = 0, L_T = -4 sigma^2, L_U = c(s-t) - 4 sigma^2, (C_s, C_t, C_u) = (-c, -c, 0)",
    LS ** 2 + (LT + 4 * sig ** 2) ** 2 + (LU - (c * (s - t) - 4 * sig ** 2)) ** 2 + (Cs + c) ** 2 + (Ct + c) ** 2 + Cu ** 2)
# the J vectors quoted in the text for xxxx: J(1,3) = -c(q1-q3) + 2 sigma (th - x), J(2,4) = -c(q2-q4) - 2 sigma (th - x), ...
e = [xh, xh, th, th]
chk("xxxx: J(1,2) = q2 - q1", sum((J(0, 1, e) - (q[1] - q[0])).applyfunc(lambda z: S(z) ** 2)))
chk("xxxx: J(1,3) = -c(q1-q3) + 2 sigma (th - x)", sum((J(0, 2, e) - (-c * (q[0] - q[2]) + 2 * sig * (th - xh))).applyfunc(lambda z: S(z) ** 2)))
chk("xxxx: J(2,4) = -c(q2-q4) - 2 sigma (th - x)", sum((J(1, 3, e) - (-c * (q[1] - q[3]) - 2 * sig * (th - xh))).applyfunc(lambda z: S(z) ** 2)))
chk("xxxx: J(1,4) = -c(q1-q4) - 2 sigma (th + x)", sum((J(0, 3, e) - (-c * (q[0] - q[3]) - 2 * sig * (th + xh))).applyfunc(lambda z: S(z) ** 2)))
chk("xxxx: J(2,3) = -c(q2-q3) + 2 sigma (th + x)", sum((J(1, 2, e) - (-c * (q[1] - q[2]) + 2 * sig * (th + xh))).applyfunc(lambda z: S(z) ** 2)))
chk("(th - x)^2 = -2(1-c), (th + x)^2 = -2(1+c)", (dot(th - xh, th - xh) + 2 * (1 - c)) ** 2 + (dot(th + xh, th + xh) + 2 * (1 + c)) ** 2)
chk("(q1-q3).(th-x) = 2 sigma, (q2-q4).(th-x) = -2 sigma", (dot(q[0] - q[2], th - xh) - 2 * sig) ** 2 + (dot(q[1] - q[3], th - xh) + 2 * sig) ** 2)
chk("(q1-q4).(th+x) = 2 sigma, (q2-q3).(th+x) = -2 sigma", (dot(q[0] - q[3], th + xh) - 2 * sig) ** 2 + (dot(q[1] - q[2], th + xh) + 2 * sig) ** 2)
# per-class X^2 + Y^2 + XY
f3 = lambda name: S(table[name][6] ** 2 + table[name][7] ** 2 + table[name][6] * table[name][7])
chk("xxxx: X^2+Y^2+XY = (3+c^2)^3/(1-c^2)^2", f3('xxxx') - (3 + c ** 2) ** 3 / (1 - c ** 2) ** 2)
chk("xxyy: X^2+Y^2+XY = 3+c^2", f3('xxyy') - (3 + c ** 2))
chk("xyxy: X^2+Y^2+XY = 4(3+c^2)/(1-c)^2", f3('xyxy') - 4 * (3 + c ** 2) / (1 - c) ** 2)
chk("xyyx: X^2+Y^2+XY = 4(3+c^2)/(1+c)^2", f3('xyyx') - 4 * (3 + c ** 2) / (1 + c) ** 2)
chk("1 + 4/(1-c)^2 + 4/(1+c)^2 = (3+c^2)^2/(1-c^2)^2", 1 + 4 / (1 - c) ** 2 + 4 / (1 + c) ** 2 - (3 + c ** 2) ** 2 / (1 - c ** 2) ** 2)
total = S(total)
chk("sum over 16 polarizations of X^2+Y^2+XY = 4(3+c^2)^3/(1-c^2)^2", total - 4 * (3 + c ** 2) ** 3 / (1 - c ** 2) ** 2)
chk("= 16(3 - tu/s^2 - su/t^2 - st/u^2)", total - 16 * (3 - t * u / s ** 2 - s * u / t ** 2 - s * t / u ** 2))
chk("= 2(s^2+t^2+u^2)^3/(s^2 t^2 u^2)", total - 2 * Ssum ** 3 / (s ** 2 * t ** 2 * u ** 2))
chk("s^2+t^2+u^2 = s^2(3+c^2)/2", Ssum - s ** 2 * (3 + c ** 2) / 2)
# the Mandelstam identity 8[3 s^2t^2u^2 - (s^3t^3 + t^3u^3 + u^3s^3)] = (s^2+t^2+u^2)^3 for s+t+u = 0
a_, b_ = sp.symbols('a b')
chk("8[3 s^2t^2u^2 - sum (st)^3] = (s^2+t^2+u^2)^3 at u = -s-t",
    (8 * (3 * a_ ** 2 * b_ ** 2 * (a_ + b_) ** 2 - (a_ ** 3 * b_ ** 3 + b_ ** 3 * (-(a_ + b_)) ** 3 + (-(a_ + b_)) ** 3 * a_ ** 3))
     - (a_ ** 2 + b_ ** 2 + (a_ + b_) ** 2) ** 3).expand())
chk("(C) cross-section integrand of app:tree: tu/s^2 = (1-c^2)/4", t * u / s ** 2 - (1 - c ** 2) / 4)

total          # inspect: the sum over the 16 configurations of X^2 + Y^2 + XY

# %% [markdown]
# ## Report

# %%
for line in report:
    print(line)
print("all symbolic checks passed:", all(l.startswith("OK") for l in report))


# %% [markdown]
# ## Numerical cross-check with ampC of tree_sigma.py

# %%
# --- 2. numerical cross-check with Src/tree_sigma.py (definitions only) ---
import numpy as np
src_path = os.path.join(HERE, "tree_sigma.py")
src = open(src_path).read()
cut = src.index("# ## 1. Spin/colour sums against the closed forms")
ns = {"__name__": "tree_sigma_defs"}
exec(compile(src[:cut], src_path, "exec"), ns)
ampC, kin22, FABC, ns_pols, sumC = ns["ampC"], ns["kin22"], ns["FABC"], ns["pols"], ns["sumC"]
CS = np.einsum("abe,cde->abcd", FABC, FABC); CT = np.einsum("ace,bde->abcd", FABC, FABC)
worst = 0.0
for cv in (-0.83, -0.2, 0.37, 0.91):
    for sq in (5.0, 17.0):
        s_, P1, P2, K1, K2 = kin22(sq, 0.0, 0.0, cv, phi=0.0)
        snv = np.sqrt(1 - cv * cv)
        xv = np.array([0, 1.0, 0, 0]); yv = np.array([0, 0, 1.0, 0]); tv = np.array([0, cv, 0, -snv])
        pv = [{'x': xv, 'y': yv}, {'x': xv, 'y': yv}, {'x': tv, 'y': yv}, {'x': tv, 'y': yv}]
        tot = 0.0
        for cfg in itertools.product('xy', repeat=4):
            M = ampC(P1, P2, K1, K2, *[pv[i][cfg[i]] for i in range(4)], 1.0)       # g = 1, Feynman gauge
            M3 = ampC(P1, P2, K1, K2, *[pv[i][cfg[i]] for i in range(4)], 3.0)      # xi = 3
            # project on c_s, c_t: M = -(c_s X + c_t Y)
            A = np.stack([CS.ravel(), CT.ravel()], axis=1)
            coef, *_ = np.linalg.lstsq(A, -M.ravel(), rcond=None)
            resid = np.max(np.abs(A @ coef + M.ravel()))
            Xs = float(table[''.join(cfg)][6].subs(c, cv)); Ys = float(table[''.join(cfg)][7].subs(c, cv))
            worst = max(worst, resid, abs(coef[0] - Xs), abs(coef[1] - Ys), np.max(np.abs(M - M3)))
            tot += np.sum(np.abs(M) ** 2)
        ref = 9 * 8 * float(total.subs(c, cv))              # C_A^2 d_A sum(X^2+Y^2+XY), SU(3): 72
        worst = max(worst, abs(tot / ref - 1), abs(sumC(sq, cv) / ref - 1))
print(f"tree_sigma.ampC (SU(3), xi = 1 and 3) vs the table of X, Y and the sum: max deviation {worst:.2e}")
worst          # inspect: the largest deviation
