# %% [markdown]
# # Step (8): the two-loop beta functions of the SM from the general formulas, with explicit field content
#
# Research note models/sm, step (8).  The general two-loop formulas of Luo, Wang and Xiao (Phys. Rev. D 67 (2003)
# 065019, arXiv:hep-ph/0211440; the corrected form of Machacek and Vaughn) are evaluated with the explicit SM field
# content of rg_general.py (45 Weyl fermions, 4 real scalars, generators with the couplings included), extended to the
# semi-simple group SU(3) x SU(2) x U(1) with their substitution rules (Sec. VI): g^2 C2 -> sum_k g_k^2 C2^k (so the
# generators carry the couplings), g^4 C2(G) C2 -> sum_k g_k^4 C2(G_k) C2^k, g^6 [..] A -> sum_kl g_k^4 g_l^2 [..]_k
# (Lambda^k Lambda^l), A^g -> sum_k g_k^6 A^g(k).  The mass parameter mu^2 is obtained with a non-propagating dummy
# scalar d (lambda_{ab dd} = 2 m^2_ab, no gauge or Yukawa couplings; internal lambda-lambda sums exclude d).
# The results are compared, loop order by loop order, with the SM two-loop RGEs of Buttazzo et al. (JHEP 12 (2013) 089,
# appendix B; two independent derivations) at random couplings with y_t, y_b, y_tau only.
# Output: results/rg_twoloop.csv (point 1), rg_twoloop_point2.csv.  Batch: python3 rg_twoloop.py [1|2]

# %%
import csv
import itertools
import math
from pathlib import Path

import numpy as np

RES = Path(__file__).resolve().parent / "results"
RES.mkdir(exist_ok=True)
KAPPA = 0.5

# %% [markdown]
# ## Couplings (random, generic); only the third-generation Yukawa couplings, as in Buttazzo et al.

# %%
import sys
POINT = int(sys.argv[1]) if len(sys.argv) > 1 else 1
if POINT == 1:
    gs, g, gp = 1.13, 0.65, 0.36
    lam, mu2 = 0.13, 0.81
    yu = np.array([0.0, 0.0, 0.94])
    yd = np.array([0.0, 0.0, 0.12])
    ye = np.array([0.0, 0.0, 0.088])
else:          # a second, unrelated point (negative lambda, large y_b, y_tau)
    gs, g, gp = 0.71, 0.93, 0.52
    lam, mu2 = -0.07, 1.37
    yu = np.array([0.0, 0.0, 0.61])
    yd = np.array([0.0, 0.0, 0.44])
    ye = np.array([0.0, 0.0, 0.29])
print("coupling point", POINT)

# %% [markdown]
# ## Group theory (as in rg_general.py), now kept per gauge group

# %%
lam_gm = np.zeros((8, 3, 3), dtype=complex)
lam_gm[0][0, 1] = lam_gm[0][1, 0] = 1
lam_gm[1][0, 1], lam_gm[1][1, 0] = -1j, 1j
lam_gm[2][0, 0], lam_gm[2][1, 1] = 1, -1
lam_gm[3][0, 2] = lam_gm[3][2, 0] = 1
lam_gm[4][0, 2], lam_gm[4][2, 0] = -1j, 1j
lam_gm[5][1, 2] = lam_gm[5][2, 1] = 1
lam_gm[6][1, 2], lam_gm[6][2, 1] = -1j, 1j
lam_gm[7] = np.diag([1, 1, -2]) / math.sqrt(3)
T3c = lam_gm / 2
sig = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=complex)
T2 = sig / 2
# structure constants f^{ABC} = -2 i tr([T^A, T^B] T^C)
f3 = np.array([[[(-2j * np.trace((T3c[a] @ T3c[b] - T3c[b] @ T3c[a]) @ T3c[c])).real for c in range(8)]
                for b in range(8)] for a in range(8)])
f2 = np.array([[[(-2j * np.trace((T2[a] @ T2[b] - T2[b] @ T2[a]) @ T2[c])).real for c in range(3)]
                for b in range(3)] for a in range(3)])

idx = {}
n = 0
for gen in range(3):
    for c in range(3):
        for i in range(2):
            idx[("Q", gen, c, i)] = n; n += 1
    for c in range(3):
        idx[("uc", gen, c)] = n; n += 1
    for c in range(3):
        idx[("dc", gen, c)] = n; n += 1
    for i in range(2):
        idx[("L", gen, i)] = n; n += 1
    idx[("ec", gen)] = n; n += 1
NF = n
HYP = {"Q": 1 / 6, "uc": -2 / 3, "dc": 1 / 3, "L": -1 / 2, "ec": 1.0}
NS = 5            # 4 real Higgs components + dummy scalar (index 4)
DUM = 4
P = np.diag([1.0, 1.0, 1.0, 1.0, 0.0])   # internal scalar sums exclude the dummy


def realify(m):
    im = 1j * m
    r = np.zeros((4, 4))
    for p in range(2):
        for q in range(2):
            r[2 * p, 2 * q] = im[p, q].real
            r[2 * p, 2 * q + 1] = -im[p, q].imag
            r[2 * p + 1, 2 * q] = im[p, q].imag
            r[2 * p + 1, 2 * q + 1] = im[p, q].real
    return r


def pad(m4):
    out = np.zeros((NS, NS), dtype=complex)
    out[:4, :4] = m4
    return out


# per group: coupled generators on fermions and scalars, coupling, C2(G), d(G), structure constants
groups = {}
tf, ts = [], []
for a in range(8):
    t = np.zeros((NF, NF), dtype=complex)
    for gen in range(3):
        for i in range(2):
            for c1 in range(3):
                for c2 in range(3):
                    t[idx[("Q", gen, c1, i)], idx[("Q", gen, c2, i)]] = gs * T3c[a][c1, c2]
        for name in ("uc", "dc"):
            for c1 in range(3):
                for c2 in range(3):
                    t[idx[(name, gen, c1)], idx[(name, gen, c2)]] = -gs * np.conj(T3c[a][c1, c2])
    tf.append(t)
    ts.append(np.zeros((NS, NS), dtype=complex))
groups[3] = dict(tf=tf, ts=ts, g=gs, CG=3.0, dG=8, f=f3)
tf, ts = [], []
for a in range(3):
    t = np.zeros((NF, NF), dtype=complex)
    for gen in range(3):
        for c in range(3):
            for i1 in range(2):
                for i2 in range(2):
                    t[idx[("Q", gen, c, i1)], idx[("Q", gen, c, i2)]] = g * T2[a][i1, i2]
        for i1 in range(2):
            for i2 in range(2):
                t[idx[("L", gen, i1)], idx[("L", gen, i2)]] = g * T2[a][i1, i2]
    tf.append(t)
    ts.append(pad(-1j * realify(g * T2[a])))
groups[2] = dict(tf=tf, ts=ts, g=g, CG=2.0, dG=3, f=f2)
t = np.zeros((NF, NF), dtype=complex)
for key, j in idx.items():
    t[j, j] = gp * HYP[key[0]]
groups[1] = dict(tf=[t], ts=[pad(-1j * realify(gp * 0.5 * np.eye(2)))], g=gp, CG=0.0, dG=1, f=None)
TF = [t for k in (3, 2, 1) for t in groups[k]["tf"]]       # all coupled generators, aligned
TS = [t for k in (3, 2, 1) for t in groups[k]["ts"]]
for k, G in groups.items():
    G["S2F"] = np.trace(G["tf"][0] @ G["tf"][0]).real / G["g"] ** 2
    G["S2S"] = np.trace(G["ts"][0] @ G["ts"][0]).real / G["g"] ** 2
    G["C2F"] = sum(t @ t for t in G["tf"])                 # coupled: g_k^2 C2^k(F)
    G["C2S"] = sum(t @ t for t in G["ts"])

# %% [markdown]
# ## Yukawa matrices and quartic couplings (dummy scalar d: lambda_{ab dd} = 2 m^2_ab)

# %%
dPhi = np.zeros((2, 4), dtype=complex)
for k in range(2):
    dPhi[k, 2 * k] = 1 / math.sqrt(2)
    dPhi[k, 2 * k + 1] = 1j / math.sqrt(2)
dPhic = np.conj(dPhi)
Y = np.zeros((NS, NF, NF), dtype=complex)


def add(a, j, k, val):
    Y[a, j, k] += val
    Y[a, k, j] += val


for a in range(4):
    for gen in range(3):
        for c in range(3):
            for i in range(2):
                add(a, idx[("Q", gen, c, i)], idx[("dc", gen, c)], yd[gen] * dPhic[i, a])
            add(a, idx[("Q", gen, c, 0)], idx[("uc", gen, c)], yu[gen] * dPhi[1, a])
            add(a, idx[("Q", gen, c, 1)], idx[("uc", gen, c)], -yu[gen] * dPhi[0, a])
        for i in range(2):
            add(a, idx[("L", gen, i)], idx[("ec", gen)], ye[gen] * dPhic[i, a])

L4 = np.zeros((NS, NS, NS, NS))
dl = np.eye(4)
L4[:4, :4, :4, :4] = 2 * lam * (np.einsum("ab,cd->abcd", dl, dl) + np.einsum("ac,bd->abcd", dl, dl)
                                + np.einsum("ad,bc->abcd", dl, dl))
M2 = -mu2 * np.eye(4)
for a in range(4):
    for b in range(4):
        for p in set(itertools.permutations((a, b, DUM, DUM))):
            L4[p] = 2 * M2[a, b]

# %% [markdown]
# ## Invariants

# %%
dag = lambda m: m.conj().T
perms = list(itertools.permutations(range(4)))
Y2F = sum(dag(Y[b]) @ Y[b] for b in range(NS))
Y2S = np.array([[0.5 * np.trace(dag(Y[a]) @ Y[b] + dag(Y[b]) @ Y[a]) for b in range(NS)] for a in range(NS)])
C2F = sum(t @ t for t in TF)
C2S = sum(t @ t for t in TS)
print("C2(F) and Y2(F) diagonal (so complex conjugation on the left is immaterial):",
      np.allclose(C2F, np.diag(np.diag(C2F))), np.allclose(Y2F, np.diag(np.diag(Y2F))))
LP = np.einsum("abcd,ae,bf,cg,dh->efgh", L4, P, P, P, P)     # lambda with all legs internal (non-dummy)
L2S = np.einsum("acde,bcde->ab", np.einsum("acde,cf,dg,eh->afgh", L4, P, P, P), L4) / 6     # Lambda^2_ab(S)
H2S = np.array([[0.5 * np.trace(Y[a] @ dag(Y[b]) @ sum(Y[c] @ dag(Y[c]) for c in range(NS))
                                + dag(Y[a]) @ Y[b] @ sum(dag(Y[c]) @ Y[c] for c in range(NS)))
                 for b in range(NS)] for a in range(NS)])
H2bS = np.array([[0.5 * sum(np.trace(Y[a] @ dag(Y[c]) @ Y[b] @ dag(Y[c]) + dag(Y[a]) @ Y[c] @ dag(Y[b]) @ Y[c])
                            for c in range(NS)) for b in range(NS)] for a in range(NS)])
Y2FS = np.array([[0.5 * np.trace(C2F @ (Y[a] @ dag(Y[b]) + Y[b] @ dag(Y[a]))) for b in range(NS)]
                 for a in range(NS)])
anti = [[TS[A] @ TS[B] + TS[B] @ TS[A] for B in range(len(TS))] for A in range(len(TS))]


def leg_sum(mat, T):
    """sum over the four legs: sum_i mat_{leg i} T_{...i...} (the 'sum_i X(i) T_abcd' of Luo et al.)"""
    return (np.einsum("ai,ibcd->abcd", mat, T) + np.einsum("bi,aicd->abcd", mat, T)
            + np.einsum("ci,abid->abcd", mat, T) + np.einsum("di,abci->abcd", mat, T))


def tensor(fun):
    """full symmetric 4-index tensor from fun(a, b, c, d) (sum over permutations inside fun)"""
    T = np.zeros((NS, NS, NS, NS), dtype=complex)
    for a, b, c, d in itertools.combinations_with_replacement(range(NS), 4):
        v = fun(a, b, c, d)
        for p in set(itertools.permutations((a, b, c, d))):
            T[p] = v
    return T


def psum(fun, a, b, c, d):
    legs = (a, b, c, d)
    return sum(fun(*[legs[i] for i in p]) for p in perms)


# one-loop tensors
Ht = tensor(lambda a, b, c, d: psum(lambda p, q, r, s: np.trace(Y[p] @ dag(Y[q]) @ Y[r] @ dag(Y[s])), a, b, c, d) / 4)
At = tensor(lambda a, b, c, d: sum(psum(lambda p, q, r, s: anti[A][B][p, q] * anti[A][B][r, s], a, b, c, d)
                                     for A in range(len(TS)) for B in range(len(TS))) / 8)
# A in the Lambda_{ab,cd} = theta_ac theta_bd form (Luo et al. Sec. VI), with per-group weights for the g^6 term
Lam = {k: sum(np.einsum("ac,bd->abcd", t, t) for t in G["ts"]) for k, G in groups.items()}
LamT = sum(Lam.values())


def A_from_Lam(L1, L2):
    def f(a, b, c, d):
        return psum(lambda p, q, r, s: np.einsum("ef,ef->", L1[p, r], L2[:, :, q, s])
                    + np.einsum("ef,ef->", L1[p, :, :, s], L2[:, q, r, :].T), a, b, c, d) / 4
    return tensor(f)


At_L = A_from_Lam(LamT, LamT)
print("A_abcd: {theta,theta}{theta,theta} form vs Lambda form, max difference:", "%.1e" % np.max(np.abs(At - At_L)))

# %% [markdown]
# ## One-loop beta functions (as rg_general.py)

# %%
def beta1_L():
    # internal e, f exclude the dummy scalar
    lam2 = tensor(lambda a, b, c, d: psum(lambda p, q, r, s: np.einsum("ef,ef->", P @ L4[p, q] @ P, L4[:, :, r, s]),
                                          a, b, c, d) / 8)
    return lam2 - 8 * KAPPA * Ht + 3 * At + 2 * KAPPA * leg_sum(Y2S, L4) - 3 * leg_sum(C2S, L4)


def beta1_Y(a):
    out = 0.5 * (Y2F.T @ Y[a] + Y[a] @ Y2F)
    out += 2 * sum(Y[b] @ dag(Y[a]) @ Y[b] for b in range(NS))
    out += 2 * KAPPA * sum(Y[b] * Y2S[b, a] for b in range(NS))
    out -= 3 * (C2F.T @ Y[a] + Y[a] @ C2F)
    return out


# %% [markdown]
# ## Two-loop beta functions (Luo, Wang, Xiao, Eqs. for beta^a_II and beta^II_abcd, Sec. VI rules)

# %%
def weights(cG, cF, cS):
    """sum_k g_k^2 [cG C2(G_k) + cF kappa S2^k(F) + cS S2^k(S)] x (coupled C2^k), on fermions and on scalars"""
    wF = sum(G["g"] ** 2 * (cG * G["CG"] + cF * KAPPA * G["S2F"] + cS * G["S2S"]) * G["C2F"] for G in groups.values())
    wS = sum(G["g"] ** 2 * (cG * G["CG"] + cF * KAPPA * G["S2F"] + cS * G["S2S"]) * G["C2S"] for G in groups.values())
    return wF, wS


def beta2_Y(a):
    Ya, Yad = Y[a], dag(Y[a])
    o = np.zeros((NF, NF), dtype=complex)
    r = range(NS)
    o += 2 * sum(Y[c] @ dag(Y[b]) @ Ya @ (dag(Y[c]) @ Y[b] - dag(Y[b]) @ Y[c]) for b in r for c in r)
    o -= sum(Y[b] @ (Y2F @ Yad + Yad @ Y2F.T) @ Y[b] for b in r)
    o -= sum(Y[b] @ Y2F @ dag(Y[b]) @ Ya + Ya @ dag(Y[b]) @ Y2F.T @ Y[b] for b in r) / 8
    o -= 4 * KAPPA * sum(Y2S[a, c] * Y[b] @ dag(Y[c]) @ Y[b] for b in r for c in r)
    o -= 2 * KAPPA * sum(Y[b] * H2bS[a, b] for b in r)
    o -= 1.5 * KAPPA * sum(Y2S[b, c] * (Y[b] @ dag(Y[c]) @ Ya + Ya @ dag(Y[c]) @ Y[b]) for b in r for c in r)
    o -= 3 * KAPPA * sum(Y[b] * H2S[a, b] for b in r)
    o -= 2 * sum(L4[a, b, c, d] * Y[b] @ dag(Y[c]) @ Y[d] for b in range(4) for c in range(4) for d in range(4))
    o += 0.5 * sum(L2S[a, b] * Y[b] for b in r)
    # g^2
    o += 3 * sum(C2F.T @ (Y[b] @ Yad @ Y[b]) + (Y[b] @ Yad @ Y[b]) @ C2F for b in r)
    o += 5 * sum(Y[b] @ (C2F @ Yad + Yad @ C2F.T) @ Y[b] for b in r)
    o -= 1.75 * (C2F.T @ Y2F.T @ Ya + Ya @ Y2F @ C2F)
    o -= 0.25 * sum(Y[b] @ C2F @ dag(Y[b]) @ Ya + Ya @ dag(Y[b]) @ C2F.T @ Y[b] for b in r)
    H2t = sum(np.conj(t) @ Ya @ dag(Y[b]) @ np.conj(t) @ Y[b] + Y[b] @ t @ dag(Y[b]) @ Ya @ t for t in TF for b in r)
    o += 6 * H2t
    o += 10 * KAPPA * sum(Y[b] * Y2FS[a, b] for b in r)
    o += 6 * (sum(C2S[b, c] * Y[b] @ Yad @ Y[c] for b in r for c in r)
              - 2 * sum(C2S[a, c] * Y[b] @ dag(Y[c]) @ Y[b] for b in r for c in r))
    o += 4.5 * sum(C2S[b, c] * (Y[b] @ dag(Y[c]) @ Ya + Ya @ dag(Y[c]) @ Y[b]) for b in r for c in r)
    # g^4
    o -= 1.5 * ((C2F @ C2F).T @ Ya + Ya @ (C2F @ C2F))
    o += 6 * sum(C2S[a, b] * (C2F.T @ Y[b] + Y[b] @ C2F) for b in r)
    wF, _ = weights(-97 / 6, 10 / 3, 11 / 12)
    o += wF.T @ Ya + Ya @ wF
    o -= 10.5 * sum((C2S @ C2S)[a, c] * Y[c] for c in r)
    _, wS = weights(49 / 4, -2.0, -0.25)
    o += sum(wS[a, b] * Y[b] for b in r)
    return o


def beta2_L(a, b, c, d):
    """beta^II_abcd for one index set (external indices may be the dummy)"""
    legs = (a, b, c, d)
    nA = len(TS)
    tr = np.trace

    def ps(fun):
        return sum(fun(*[legs[i] for i in p]) for p in perms)

    def lamP(p, q):        # lambda_{pq ef} with e, f internal
        return P @ L4[p, q] @ P
    out = 0.0
    out += 0.5 * leg_sum(L2S, L4)[legs]
    out -= ps(lambda p, q, r, s: np.einsum("ef,egh,fgh->", lamP(p, q), np.einsum("egh,gi,hj->eij", L4[r], P, P), L4[s]))/4
    out -= 4 * KAPPA * ps(lambda p, q, r, s: np.einsum("fg,ef,eg->", Y2S, lamP(p, q), L4[r, s])) / 8
    Hbl = ps(lambda p, q, r, s: sum(L4[p, q, e, f] * tr(Y[r] @ dag(Y[e]) @ Y[s] @ dag(Y[f])
                                                         + dag(Y[r]) @ Y[e] @ dag(Y[s]) @ Y[f])
                                     for e in range(4) for f in range(4))) / 8
    out += KAPPA * (8 * Hbl - leg_sum(3 * H2S + 2 * H2bS, L4)[legs])
    HY = ps(lambda p, q, r, s: tr(Y2F @ dag(Y[p]) @ Y[q] @ dag(Y[r]) @ Y[s]))
    HbY = ps(lambda p, q, r, s: sum(tr(Y[e] @ dag(Y[p]) @ Y[e] @ dag(Y[q]) @ Y[r] @ dag(Y[s])
                                       + dag(Y[e]) @ Y[p] @ dag(Y[e]) @ Y[q] @ dag(Y[r]) @ Y[s]) for e in range(4))) / 2
    H3 = ps(lambda p, q, r, s: sum(tr(Y[p] @ dag(Y[q]) @ Y[e] @ dag(Y[r]) @ Y[s] @ dag(Y[e])) for e in range(4))) / 2
    out += 4 * KAPPA * (HY + 2 * HbY + 2 * H3)
    # g^2
    L2Sb = ps(lambda p, q, r, s: np.einsum("fg,ef,eg->", C2S, lamP(p, q), L4[r, s])) / 8
    L2g = ps(lambda p, q, r, s: sum(np.einsum("ef,gh,eg,fh->", L4[p, q], L4[r, s], t, t) for t in TS)) / 8
    HS = leg_sum(C2S, Ht)[legs]
    HF = ps(lambda p, q, r, s: tr((C2F.T @ Y[p] + Y[p] @ C2F) @ dag(Y[q]) @ Y[r] @ dag(Y[s])))
    out += 2 * L2Sb - 6 * L2g + 4 * KAPPA * (HS - HF) + 10 * KAPPA * leg_sum(Y2FS, L4)[legs]
    # g^4
    _, w35 = weights(35 / 3, -10 / 3, -11 / 12)
    LSw = leg_sum(w35, L4)[legs]
    LSS = leg_sum(C2S @ C2S, L4)[legs]
    Al = ps(lambda p, q, r, s: sum(np.einsum("ef,ef->", L4[p, q], anti[A][B]) * anti[A][B][r, s]
                                   for A in range(nA) for B in range(nA))) / 4
    Alb = ps(lambda p, q, r, s: sum(np.einsum("ef,e,f->", L4[p, q], anti[A][B][r], anti[A][B][s])
                                    for A in range(nA) for B in range(nA))) / 4
    BY = ps(lambda p, q, r, s: sum(anti[A][B][p, q] * tr(np.conj(TF[A]) @ np.conj(TF[B]) @ Y[r] @ dag(Y[s])
                                                         + Y[r] @ TF[A] @ TF[B] @ dag(Y[s]))
                                   for A in range(nA) for B in range(nA))) / 4
    BbY = ps(lambda p, q, r, s: sum(anti[A][B][p, q] * tr(np.conj(TF[A]) @ Y[r] @ TF[B] @ dag(Y[s]))
                                    for A in range(nA) for B in range(nA))) / 4
    out -= LSw - 1.5 * LSS - 2.5 * Al - 0.5 * Alb + 4 * KAPPA * (BY - 10 * BbY)
    # g^6
    Aw = 0.0
    for k, G in groups.items():
        wk = G["g"] ** 2 * (161 / 6 * G["CG"] - 32 / 3 * KAPPA * G["S2F"] - 7 / 3 * G["S2S"])
        Aw += wk * Ak_l[k][legs]
    AS = leg_sum(C2S, At)[legs]
    Ag = 0.0
    for k, G in groups.items():
        if G["f"] is None:
            continue
        ts_k, fk = G["ts"], G["f"]
        nk = len(ts_k)
        ac = [[ts_k[A] @ ts_k[B] + ts_k[B] @ ts_k[A] for B in range(nk)] for A in range(nk)]
        ff = np.einsum("ace,bde->abcd", fk, fk)
        Ag += G["g"] ** 2 * ps(lambda p, q, r, s: sum(ff[A, B, C, D] * ac[A][B][p, q] * ac[C][D][r, s]
                                                     for A in range(nk) for B in range(nk) for C in range(nk)
                                                     for D in range(nk) if ff[A, B, C, D] != 0)) / 8
    out += Aw - 7.5 * AS + 27 * Ag
    return out


# A with one Lambda from group k and one from the full gauge group (for the g^6 [..]_k A term)
Ak_l = {k: A_from_Lam(Lam[k], LamT) for k in groups}

# %% [markdown]
# ## Two-loop gauge beta functions (Eq. (gague2) with the Sec. VI rules)

# %%
def beta2_gauge(k):
    G = groups[k]
    gk, CG, dG = G["g"], G["CG"], G["dG"]
    C2F_unc = G["C2F"] / gk ** 2
    C2S_unc = G["C2S"] / gk ** 2
    # sum_l g_l^2 C2^l(R) S2^k(R) = (1/d(G_k)) tr[C2_total C2^k_unc]
    cfsf = np.trace(C2F @ C2F_unc).real / dG
    cssf = np.trace(C2S @ C2S_unc).real / dG
    y4 = sum(np.trace(C2F_unc @ Y[a] @ dag(Y[a])).real for a in range(NS)) / dG
    return (-gk ** 5 * (34 / 3 * CG ** 2 - KAPPA * 20 / 3 * CG * G["S2F"] - 1 / 3 * CG * G["S2S"])
            + gk ** 3 * (KAPPA * 4 * cfsf + 2 * cssf) - 2 * KAPPA * gk ** 3 * y4)


def beta1_gauge(k):
    G = groups[k]
    return G["g"] ** 3 * (-11 / 3 * G["CG"] + 4 / 3 * KAPPA * G["S2F"] + 1 / 6 * G["S2S"])

# %% [markdown]
# ## Buttazzo et al. appendix B (one- and two-loop parts, transcribed in sm_rge.py), d/d ln mu^2, g1^2 = 5 gY^2/3

# %%
import sm_rge


def buttazzo(g1, g2, g3, yt, yb, ytau, la):
    one, two, _, _ = sm_rge.loops(g1 ** 2, g2 ** 2, g3 ** 2, yt ** 2, yb ** 2, ytau ** 2, la)
    return one, two

# %% [markdown]
# ## Comparison

# %%
# general formulas, converted to Buttazzo's quantities: d(g^2)/d ln mu^2 = g beta_g, d lambda/d ln mu^2 = beta_lambda/2,
# d y^2/d ln mu^2 = y beta_y, d ln m^2/d ln mu^2 = (beta_mu2/mu2)/2; g1^2 = 5 gp^2/3
Lb1 = beta1_L()
mine = {1: {}, 2: {}}
gk = {3: gs, 2: g, 1: gp}
for lo, fun in ((1, beta1_gauge), (2, beta2_gauge)):
    mine[lo]["g3sq"] = gs * fun(3)
    mine[lo]["g2sq"] = g * fun(2)
    mine[lo]["g1sq"] = 5 / 3 * gp * fun(1)
# lambda_0000 = 6 lam; m^2: lambda_{00dd} = 2 m^2_00 = -2 mu^2
b2_0000 = beta2_L(0, 0, 0, 0).real
b1_0000 = Lb1[0, 0, 0, 0].real
mine[1]["lam"] = b1_0000 / 6 / 2
mine[2]["lam"] = b2_0000 / 6 / 2
mine[1]["m2rel"] = (Lb1[0, 0, DUM, DUM] / L4[0, 0, DUM, DUM]).real / 2
mine[2]["m2rel"] = (beta2_L(0, 0, DUM, DUM) / L4[0, 0, DUM, DUM]).real / 2
# Yukawa: entries that define y_t, y_b, y_tau (third generation), via phi_3
a = 2
by1, by2 = beta1_Y(a), beta2_Y(a)
for name, (j, k), y in (("ytsq", (idx[("Q", 2, 0, 0)], idx[("uc", 2, 0)]), yu[2]),
                        ("ybsq", (idx[("Q", 2, 0, 1)], idx[("dc", 2, 0)]), yd[2]),
                        ("ytausq", (idx[("L", 2, 1)], idx[("ec", 2)]), ye[2])):
    mine[1][name] = (by1[j, k] / Y[a, j, k]).real * y ** 2
    mine[2][name] = (by2[j, k] / Y[a, j, k]).real * y ** 2
# no new structures in the two-loop Yukawa beta functions
resid = 0.0
for aa in range(4):
    b2 = beta2_Y(aa)
    mask = np.abs(Y[aa]) < 1e-14
    resid = max(resid, np.max(np.abs(b2[mask])))
# lambda_{0011} = 2 lam must give the same beta (one quartic coupling)
lam_alt = beta2_L(0, 0, 1, 1).real / 2 / 2

one, two = buttazzo(math.sqrt(5 / 3) * gp, g, gs, yu[2], yd[2], ye[2], lam)
rows = []
worst = 0.0
for lo, ref in ((1, one), (2, two)):
    for key in ("g1sq", "g2sq", "g3sq", "lam", "m2rel", "ytsq", "ybsq", "ytausq"):
        m, r = mine[lo][key], ref[key]
        rel = abs(m - r) / abs(r)
        worst = max(worst, rel)
        rows.append((lo, key, m, r, rel))
        print("%d-loop %-7s general formula %+.15e   Buttazzo %+.15e   rel. diff %.1e" % (lo, key, m, r, rel))
print("two-loop beta_lambda from lambda_0011 vs lambda_0000: rel. diff %.1e" % (abs(lam_alt - mine[2]["lam"]) / abs(mine[2]["lam"])))
print("two-loop Yukawa beta functions, largest entry outside the Yukawa structure: %.1e" % resid)
print("largest relative difference:", "%.1e" % worst)
with open(RES / ("rg_twoloop.csv" if POINT == 1 else "rg_twoloop_point%d.csv" % POINT), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["loop", "quantity", "general_formula", "buttazzo_appendix_B", "rel_diff"])
    for lo, key, m, r, rel in rows:
        w.writerow([lo, key, "%.15e" % m, "%.15e" % r, "%.2e" % rel])
