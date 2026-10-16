# %% [markdown]
# # Appendix check: the colour algebra with explicit SU(N) matrices (N = 2, 3, 4)
#
# Research note models/qcd, derivations of the appendices (sympy, exact generalized Gell-Mann matrices, no floating point).
#   app:color (T1): tr(T^a T^b) = T_F delta, f^{abc} = -(i/T_F) tr([T^a,T^b]T^c), completeness, T^a T^a = C_F, T^c T^b T^c = -(T_F/N) T^b,
#       sum_d tr(X T^d) tr(Y T^d) = T_F tr(XY), f^{acd} f^{bcd} = C_A delta and the four traces, f^{abc} T^b T^c = (i/2) C_A T^a, the Jacobi
#       identity, the adjoint generators F^a (F^b F^a F^b = (C_A/2) F^a);
#   app:tree 「(C) gg -> gg。」 (T3): c_u = c_t - c_s and the colour matrix C_A^2 d_A [[1, 1/2], [1/2, 1]] in the basis (c_s, c_t).
# Conventions of the note: tr(T^a T^b) = T_F delta^{ab}, T_F = 1/2, [T^a,T^b] = i f^{abc} T^c, (F^a)_{bc} = -i f^{abc}.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_color.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_color.py   (about 5 s)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import itertools
import sympy as sp
INTERACTIVE = "ipykernel" in sys.modules


# %% [markdown]
# ## Generalized Gell-Mann matrices

# %%
def gell_mann(N):
    """generalized Gell-Mann matrices lambda^a, tr(lambda^a lambda^b) = 2 delta^{ab}; T^a = lambda^a/2"""
    mats = []
    for j in range(N):
        for k in range(j + 1, N):
            m = sp.zeros(N); m[j, k] = 1; m[k, j] = 1; mats.append(m)
            m = sp.zeros(N); m[j, k] = -sp.I; m[k, j] = sp.I; mats.append(m)
    for l in range(1, N):
        m = sp.zeros(N)
        for j in range(l):
            m[j, j] = 1
        m[l, l] = -l
        mats.append(m * sp.sqrt(sp.Rational(2, l * (l + 1))))
    return [m / 2 for m in mats]


gell_mann(3)[7]          # inspect: T^8 of SU(3)

# %% [markdown]
# ## All identities for one N

# %%
def check(N):
    T = gell_mann(N)
    dA = len(T)
    TF = sp.Rational(1, 2)
    CF = TF * (N ** 2 - 1) / sp.Integer(N)
    CA = 2 * TF * N
    tr = lambda M: sp.simplify(M.trace())
    ok = {}
    # normalization and f^{abc} = -(i/T_F) tr([T^a,T^b]T^c)
    ok["tr(TaTb) = TF delta"] = all(tr(T[a] * T[b]) == (TF if a == b else 0) for a in range(dA) for b in range(dA))
    f = [[[sp.simplify(-sp.I / TF * tr((T[a] * T[b] - T[b] * T[a]) * T[c])) for c in range(dA)] for b in range(dA)] for a in range(dA)]
    ok["f real"] = all(sp.im(f[a][b][c]) == 0 for a in range(dA) for b in range(dA) for c in range(dA))
    ok["[Ta,Tb] = i f T"] = all(sp.simplify(T[a] * T[b] - T[b] * T[a] - sp.I * sum((f[a][b][c] * T[c] for c in range(dA)), sp.zeros(N))) == sp.zeros(N)
                               for a in range(dA) for b in range(dA))
    # completeness (T^a)_{ij}(T^a)_{kl} = TF (delta_il delta_kj - delta_ij delta_kl / N)
    ok["completeness"] = all(sp.simplify(sum(T[a][i, j] * T[a][k, l] for a in range(dA))
                                         - TF * ((1 if (i == l and k == j) else 0) - sp.Rational(1, N) * (1 if (i == j and k == l) else 0))) == 0
                             for i, j, k, l in itertools.product(range(N), repeat=4))
    # T^a T^a = CF 1
    ok["TaTa = CF"] = sp.simplify(sum((T[a] * T[a] for a in range(dA)), sp.zeros(N)) - CF * sp.eye(N)) == sp.zeros(N)
    # T^c T^b T^c = -TF/N T^b = (CF - CA/2) T^b
    ok["TcTbTc = -TF/N Tb"] = all(sp.simplify(sum((T[c] * T[b] * T[c] for c in range(dA)), sp.zeros(N)) + TF / N * T[b]) == sp.zeros(N) for b in range(dA))
    ok["CF - CA/2 = -TF/N"] = sp.simplify(CF - CA / 2 + TF / N) == 0
    # sum_d tr(X T^d) tr(Y T^d) = TF tr(XY) for traceless X, Y (take X = [T^a,T^c], Y = [T^b,T^c] and random traceless)
    X = sp.Matrix(N, N, lambda i, j: sp.Rational((3 * i + 5 * j) % 7 - 3, 1 + i + j) + sp.I * ((i * j) % 3))
    X = X - X.trace() / N * sp.eye(N)
    Y = sp.Matrix(N, N, lambda i, j: sp.Rational((2 * i - j) % 5, 2 + i) - sp.I * ((i + 2 * j) % 4))
    Y = Y - Y.trace() / N * sp.eye(N)
    ok["sum_d tr(XT)tr(YT) = TF tr(XY)"] = sp.simplify(sum(tr(X * T[d]) * tr(Y * T[d]) for d in range(dA)) - TF * tr(X * Y)) == 0
    # f^{acd} f^{bcd} = -(1/TF) tr([T^a,T^c][T^b,T^c]) = 2 TF N delta^{ab}; and the four traces of the expanded product
    comm = lambda A, B: A * B - B * A
    good_ff, good_tr, good_4 = True, True, True
    for a in range(dA):
        for b in range(dA):
            ff = sum(f[a][c][d] * f[b][c][d] for c in range(dA) for d in range(dA))
            trcc = sum(tr(comm(T[a], T[c]) * comm(T[b], T[c])) for c in range(dA))
            dl = 1 if a == b else 0
            good_ff &= sp.simplify(ff - 2 * TF * N * dl) == 0
            good_tr &= sp.simplify(ff + trcc / TF) == 0
            t1 = sum(tr(T[a] * T[c] * T[b] * T[c]) for c in range(dA))
            t2 = sum(tr(T[a] * T[c] * T[c] * T[b]) for c in range(dA))
            t3 = sum(tr(T[c] * T[a] * T[b] * T[c]) for c in range(dA))
            t4 = sum(tr(T[c] * T[a] * T[c] * T[b]) for c in range(dA))
            good_4 &= all(sp.simplify(x) == 0 for x in (t1 + TF ** 2 / N * dl, t2 - CF * TF * dl, t3 - CF * TF * dl,
                                                        t4 + TF ** 2 / N * dl, t1 - t2 - t3 + t4 + 2 * TF ** 2 * N * dl))
    ok["f^{acd}f^{bcd} = 2 TF N delta"] = good_ff
    ok["f f = -(1/TF) tr([Ta,Tc][Tb,Tc])"] = good_tr
    ok["four traces -TF^2/N, CF TF, CF TF, -TF^2/N; sum -2 TF^2 N"] = good_4
    # f^{abc} T^b T^c = (i/2) CA T^a
    ok["f T T = i CA/2 T"] = all(sp.simplify(sum((f[a][b][c] * T[b] * T[c] for b in range(dA) for c in range(dA)), sp.zeros(N))
                                             - sp.I / 2 * CA * T[a]) == sp.zeros(N) for a in range(dA))
    # adjoint: (F^a)_{bc} = -i f^{abc}
    F = [sp.Matrix(dA, dA, lambda b, c: -sp.I * f[a][b][c]) for a in range(dA)]
    Z = sp.zeros(dA)
    ok["Jacobi f^{abc}f^{cde}+f^{bdc}f^{cae}+f^{dac}f^{cbe} = 0"] = all(
        sp.simplify(sum(f[a][b][c] * f[c][d][e] + f[b][d][c] * f[c][a][e] + f[d][a][c] * f[c][b][e] for c in range(dA))) == 0
        for a, b, d, e in itertools.product(range(dA), repeat=4))
    ok["(d,e) component: -f^{adg}f^{bge}+f^{bdg}f^{age} = f^{abc}f^{cde}"] = all(
        sp.simplify(sum(-f[a][d][g] * f[b][g][e] + f[b][d][g] * f[a][g][e] - f[a][b][g] * f[g][d][e] for g in range(dA))) == 0
        for a, b, d, e in itertools.product(range(dA), repeat=4))
    ok["[Fa,Fb] = i f F"] = all(sp.simplify(F[a] * F[b] - F[b] * F[a] - sp.I * sum((f[a][b][c] * F[c] for c in range(dA)), Z)) == Z
                                for a in range(dA) for b in range(dA))
    ok["FbFb = CA 1"] = sp.simplify(sum((F[b] * F[b] for b in range(dA)), Z) - CA * sp.eye(dA)) == Z
    ok["i f^{abc} F^b F^c = -CA/2 F^a"] = all(sp.simplify(sum((sp.I * f[a][b][c] * F[b] * F[c] for b in range(dA) for c in range(dA)), Z)
                                                          + CA / 2 * F[a]) == Z for a in range(dA))
    ok["FbFaFb = CA/2 Fa"] = all(sp.simplify(sum((F[b] * F[a] * F[b] for b in range(dA)), Z) - CA / 2 * F[a]) == Z for a in range(dA))
    # gg -> gg colour basis: c_s = f^{abe}f^{cde}, c_t = f^{ace}f^{bde}, c_u = f^{ade}f^{bce}
    cs = {}; ct = {}; cu = {}
    for a, b, c, d in itertools.product(range(dA), repeat=4):
        cs[a, b, c, d] = sum(f[a][b][e] * f[c][d][e] for e in range(dA))
        ct[a, b, c, d] = sum(f[a][c][e] * f[b][d][e] for e in range(dA))
        cu[a, b, c, d] = sum(f[a][d][e] * f[b][c][e] for e in range(dA))
    ok["c_u = c_t - c_s (Jacobi)"] = all(sp.simplify(cu[k] - ct[k] + cs[k]) == 0 for k in cs)
    g = lambda x, y: sp.simplify(sum(x[k] * y[k] for k in x))
    gram = sp.Matrix([[g(cs, cs), g(cs, ct)], [g(ct, cs), g(ct, ct)]])
    ok["colour matrix = CA^2 dA [[1,1/2],[1/2,1]]"] = sp.simplify(gram - CA ** 2 * dA * sp.Matrix([[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]])) == sp.zeros(2)
    ok["sum c_s c_t = tr(F^e F^g F^e F^g) = CA/2 tr(F^g F^g)"] = sp.simplify(g(cs, ct) - sum((F[e] * F[h] * F[e] * F[h]).trace() for e in range(dA) for h in range(dA))) == 0
    return ok


# %% [markdown]
# ## SU(2), SU(3), SU(4)

# %%
for N in (2, 3, 4):
    res = check(N)
    print(f"SU({N}):")
    for k, v in res.items():
        print(f"  {'OK  ' if v else 'FAIL'} {k}")
res          # inspect: the checks for SU(4)
