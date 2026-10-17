# %% [markdown]
# # Step (4) of the CKM note: the Yukawa-matrix beta functions from the general formulas, and the running of m, V, J
#
# Research note models/sm_ckm, step (4).  Independent of the note's model files.
# (a) The general one-loop formulas (Machacek-Vaughn; Luo-Wang-Xiao), implemented with the explicit SM field content
#     as in the SM note's models/sm/Src/rg_general.py (45 Weyl fermions, Phi as 4 real scalars), now with complex
#     3 x 3 Yukawa matrices Y_u, Y_d (and diagonal Y_e).  The Dirac term -Qbar Y_d Phi d_R - Qbar Y_u Phitilde u_R + h.c.
#     is the Weyl term -conj(Y_d)_ij Phi_k^* Q_ik dc_j - conj(Y_u)_ij (Phi_2 Q_i1 - Phi_1 Q_i2) uc_j (+ h.c.).
#     The general beta_Y^a is compared with the Weyl image of Eq. (betaY) of the note for every scalar component and
#     every fermion pair, at a generic point (random complex Y_u, Y_d, not in a mass basis) and at the benchmark
#     (Y_u = yhat_u, Y_d = V yhat_d).  beta_lambda, gamma_mu2 and the gauge coefficients are checked to be the same as
#     for the singular values alone (no V at one loop).
# (b) Eq. (yrun) and Eq. (Vrun): the full one-loop matrix RGEs (Eq. (betaY) with the gauge and trace terms) are
#     integrated by RK4 over +-h and +-h/2, diagonalized (SVD) and Richardson-extrapolated; the derivatives of the singular values, |V_ij| and J are compared with
#     the closed forms at the benchmark and at a point with enlarged Yukawas.  The closed form of Eq. (Vrun) is evaluated
#     also with a rephased V (random phases): d|V_ij|/dln mu and dJ/dln mu must not change.
# Output: results/rg_ckm_general.csv.   Batch: python3 rg_ckm_general.py

# %%
import csv
import itertools
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
RES.mkdir(exist_ok=True)
K = 16 * math.pi**2
KAPPA = 0.5
rng = np.random.default_rng(20261017)
dag = lambda m: m.conj().T

# %% [markdown]
# ## Group theory and the field content (as in the SM note's rg_general.py)

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
T2 = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=complex) / 2

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


def generators(gs, g, gp):
    gf = []
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
        gf.append(t)
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
        gf.append(t)
    t = np.zeros((NF, NF), dtype=complex)
    for key, j in idx.items():
        t[j, j] = gp * HYP[key[0]]
    gf.append(t)

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
    gsc = [np.zeros((4, 4), dtype=complex) for _ in range(8)]
    gsc += [-1j * realify(g * T2[a]) for a in range(3)]
    gsc += [-1j * realify(gp * 0.5 * np.eye(2))]
    return gf, gsc


dPhi = np.zeros((2, 4), dtype=complex)
for k in range(2):
    dPhi[k, 2 * k] = 1 / math.sqrt(2)
    dPhi[k, 2 * k + 1] = 1j / math.sqrt(2)
dPhic = np.conj(dPhi)


def weyl_yukawa(Yu, Yd, Ye):
    """Y^a_jk of -(1/2) Y^a_jk phi_a psi_j psi_k + h.c. for the Dirac matrices Yu, Yd, Ye (generation indices)."""
    Y = np.zeros((4, NF, NF), dtype=complex)

    def add(a, j, k, val):
        Y[a, j, k] += val
        Y[a, k, j] += val
    for a in range(4):
        for g1 in range(3):
            for g2 in range(3):
                for c in range(3):
                    for i in range(2):
                        add(a, idx[("Q", g1, c, i)], idx[("dc", g2, c)], np.conj(Yd[g1, g2]) * dPhic[i, a])
                    add(a, idx[("Q", g1, c, 0)], idx[("uc", g2, c)], np.conj(Yu[g1, g2]) * dPhi[1, a])
                    add(a, idx[("Q", g1, c, 1)], idx[("uc", g2, c)], -np.conj(Yu[g1, g2]) * dPhi[0, a])
                for i in range(2):
                    add(a, idx[("L", g1, i)], idx[("ec", g2)], np.conj(Ye[g1, g2]) * dPhic[i, a])
    return Y


# %% [markdown]
# ## General one-loop formulas

# %%
def general(Yu, Yd, Ye, gs, g, gp, lam, mu2):
    gf, gsc = generators(gs, g, gp)
    Y = weyl_yukawa(Yu, Yd, Ye)
    Y2F = sum(dag(Y[b]) @ Y[b] for b in range(4))
    Y2S = np.array([[0.5 * np.trace(dag(Y[a]) @ Y[b] + dag(Y[b]) @ Y[a]) for b in range(4)] for a in range(4)])
    C2F = sum(t @ t for t in gf)
    C2S = sum(t @ t for t in gsc)
    bY = []
    for a in range(4):
        out = 0.5 * (Y2F.T @ Y[a] + Y[a] @ Y2F)
        out += 2 * sum(Y[b] @ dag(Y[a]) @ Y[b] for b in range(4))
        out += 2 * KAPPA * sum(Y[b] * Y2S[b, a] for b in range(4))
        out -= 3 * (C2F.T @ Y[a] + Y[a] @ C2F)
        bY.append(out)
    dl = np.eye(4)
    L4 = 2 * lam * (np.einsum("ab,cd->abcd", dl, dl) + np.einsum("ac,bd->abcd", dl, dl) + np.einsum("ad,bc->abcd", dl, dl))

    def sym_sum(f, a, b, c, d):
        return sum(f(*p) for p in itertools.permutations((a, b, c, d)))

    def beta_L(a, b, c, d):
        lam2 = sym_sum(lambda p, q, r, s: np.einsum("ef,ef->", L4[p, q], L4[:, :, r, s]), a, b, c, d) / 8
        H = sym_sum(lambda p, q, r, s: np.trace(Y[p] @ dag(Y[q]) @ Y[r] @ dag(Y[s])), a, b, c, d) / 4
        A = 0.0
        for tA in gsc:
            for tB in gsc:
                ac = tA @ tB + tB @ tA
                A += sym_sum(lambda p, q, r, s: ac[p, q] * ac[r, s], a, b, c, d) / 8
        legs = (a, b, c, d)

        def leg_sum(mat):
            tot = 0.0
            for pos in range(4):
                for i in range(4):
                    lg = list(legs)
                    lg[pos] = i
                    tot += mat[legs[pos], i] * L4[tuple(lg)]
            return tot
        return lam2 - 8 * KAPPA * H + 3 * A + 2 * KAPPA * leg_sum(Y2S) - 3 * leg_sum(C2S)
    M2 = -mu2 * np.eye(4)
    bM2 = np.einsum("ef,abef->ab", M2, L4).astype(complex) + 2 * KAPPA * (Y2S @ M2 + M2 @ Y2S) - 3 * (C2S @ M2 + M2 @ C2S)
    return {"Y": Y, "bY": bY, "bl1111": beta_L(0, 0, 0, 0).real / 6, "bl1122": beta_L(0, 0, 1, 1).real / 2,
            "gmu2": -bM2[0, 0].real}


# %% [markdown]
# ## Eq. (betaY) of the note (K beta)

# %%
def note_beta(Yu, Yd, Ye, gs, g, gp):
    Hu, Hd, He = Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye)
    T = np.trace(3 * Hu + 3 * Hd + He).real
    I3 = np.eye(3)
    bu = (1.5 * (Hu - Hd) + (T - 8 * gs**2 - 9 / 4 * g**2 - 17 / 12 * gp**2) * I3) @ Yu
    bd = (1.5 * (Hd - Hu) + (T - 8 * gs**2 - 9 / 4 * g**2 - 5 / 12 * gp**2) * I3) @ Yd
    be = (1.5 * He + (T - 9 / 4 * g**2 - 15 / 4 * gp**2) * I3) @ Ye
    return bu, bd, be


def compare_point(label, Yu, Yd, Ye, gs, g, gp, lam, mu2):
    gen = general(Yu, Yd, Ye, gs, g, gp, lam, mu2)
    bu, bd, be = note_beta(Yu, Yd, Ye, gs, g, gp)
    Ynote = weyl_yukawa(bu, bd, be)          # Weyl image of Eq. (betaY) (linear in the conjugate matrices)
    dev = max(np.max(np.abs(gen["bY"][a] - Ynote[a])) for a in range(4))
    scale = max(np.max(np.abs(Ynote[a])) for a in range(4))
    # beta_lambda and gamma_mu2 with the same singular values but V = 1
    su, sd, se = (np.linalg.svd(m, compute_uv=False) for m in (Yu, Yd, Ye))
    gen1 = general(np.diag(su), np.diag(sd), np.diag(se), gs, g, gp, lam, mu2)
    d_l = abs(gen["bl1111"] - gen1["bl1111"]) / abs(gen1["bl1111"])
    d_m = abs(gen["gmu2"] - gen1["gmu2"]) / abs(gen1["gmu2"])
    print("(a) %-28s general beta_Y^a vs Eq. (betaY), all entries: max |diff| = %.1e (max |entry| %.1e); "
          "beta_lambda, gamma_mu2 vs V = 1: %.1e, %.1e" % (label, dev, scale, d_l, d_m))
    return dev / scale, d_l, d_m


# %% [markdown]
# ## (a) the general formulas

# %%
def ckm(s12, s23, s13, dl):
    c12, c23, c13 = (math.sqrt(1 - x**2) for x in (s12, s23, s13))
    e = np.exp(1j * dl)
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


ee, sw = math.sqrt(4 * math.pi / 128), math.sqrt(1881 / 8281)
MW = 80.0
vev = 2 * MW * sw / ee
gB, gpB, gsB = ee / sw, ee / math.sqrt(1 - sw**2), math.sqrt(4 * math.pi * 0.118)
lamB, mu2B = 125.0**2 / (2 * vev**2), 125.0**2 / 2
Vb = ckm(0.22501, 0.04183, 0.003732, 1.147)
yuB = math.sqrt(2) * np.array([0.00127, 0.619, 165.0]) / vev
ydB = math.sqrt(2) * np.array([0.00271, 0.0546, 2.86]) / vev
yeB = math.sqrt(2) * np.array([0.000487, 0.1027, 1.746]) / vev
rows = []
r1 = compare_point("generic complex matrices", 0.4 * (rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))),
                   0.3 * (rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))), np.diag([0.01, 0.05, 0.2]),
                   1.13, 0.65, 0.36, 0.13, 0.81)
r2 = compare_point("benchmark (Yu diag, Yd = V yd)", np.diag(yuB).astype(complex), Vb @ np.diag(ydB), np.diag(yeB),
                   gsB, gB, gpB, lamB, mu2B)
rows += [("general_vs_note_betaY_generic_rel", r1[0]), ("general_vs_note_betaY_bench_rel", r2[0]),
         ("beta_lambda_vs_V1_generic_rel", r1[1]), ("gamma_mu2_vs_V1_generic_rel", r1[2])]

# %% [markdown]
# ## (b) the running of the masses, V and J

# %%
def rk4(Yu, Yd, Ye, h, gs, g, gp):
    def f(y):
        b = note_beta(*y, gs, g, gp)
        return tuple(x / K for x in b)
    y0 = (Yu, Yd, Ye)
    k1 = f(y0)
    k2 = f(tuple(a + h / 2 * b for a, b in zip(y0, k1)))
    k3 = f(tuple(a + h / 2 * b for a, b in zip(y0, k2)))
    k4 = f(tuple(a + h * b for a, b in zip(y0, k3)))
    return tuple(a + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(y0, k1, k2, k3, k4))


def observables(Yu, Yd):
    """singular values (ascending), |V| and J from the left singular vectors (more accurate than eigh of Y Y^dagger
    for the light generations)."""
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    Uu, su, Ud, sd = Uu[:, ::-1], su[::-1], Ud[:, ::-1], sd[::-1]
    W = dag(Uu) @ Ud
    J = np.imag(W[0, 1] * W[1, 2] * np.conj(W[0, 2]) * np.conj(W[1, 1]))
    return su, sd, np.abs(W), J


def closed_forms(V, yu, yd, ye, gs, g, gp):
    """K dln y/dln mu of Eq. (yrun) and K dV/dln mu of Eq. (Vrun)."""
    T = 3 * np.sum(yu**2) + 3 * np.sum(yd**2) + np.sum(ye**2)
    a2 = np.abs(V)**2
    dlnyu = 1.5 * yu**2 - 1.5 * a2 @ yd**2 + T - 8 * gs**2 - 9 / 4 * g**2 - 17 / 12 * gp**2
    dlnyd = 1.5 * yd**2 - 1.5 * a2.T @ yu**2 + T - 8 * gs**2 - 9 / 4 * g**2 - 5 / 12 * gp**2
    Du, Dd = np.diag(yu**2), np.diag(yd**2)
    Hd_u, Hu_d = V @ Dd @ dag(V), dag(V) @ Du @ V
    KAu, KAd = np.zeros((3, 3), complex), np.zeros((3, 3), complex)
    for i in range(3):
        for k in range(3):
            if i != k:
                KAu[i, k] = -1.5 * (yu[i]**2 + yu[k]**2) / (yu[k]**2 - yu[i]**2) * Hd_u[i, k]
                KAd[i, k] = -1.5 * (yd[i]**2 + yd[k]**2) / (yd[k]**2 - yd[i]**2) * Hu_d[i, k]
    return dlnyu, dlnyd, -KAu @ V + V @ KAd


def dabs_dJ(V, dV):
    dabs = np.real(np.conj(V) * dV) / np.abs(V)
    dJ = np.imag(dV[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]) + V[0, 1] * dV[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])
                 + V[0, 1] * V[1, 2] * np.conj(dV[0, 2]) * np.conj(V[1, 1]) + V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(dV[1, 1]))
    return dabs, dJ


def check_running(label, V, yu, yd, ye, gs, g, gp, h):
    Yu, Yd, Ye = np.diag(yu).astype(complex), V @ np.diag(yd), np.diag(ye).astype(complex)
    def central(hh):
        p, m = rk4(Yu, Yd, Ye, hh, gs, g, gp), rk4(Yu, Yd, Ye, -hh, gs, g, gp)
        op, om = observables(p[0], p[1]), observables(m[0], m[1])
        return [(a - b) / (2 * hh) for a, b in zip(op, om)]
    # Richardson extrapolation of the central differences (removes the h^2 error)
    c1, c2 = central(h), central(h / 2)
    num = [(4 * b - a) / 3 for a, b in zip(c1, c2)]
    numJ = num[3]
    dlnyu, dlnyd, dV = closed_forms(V, yu, yd, ye, gs, g, gp)
    dabs, dJ = dabs_dJ(V, dV)
    e_yu = np.max(np.abs(num[0] / yu * K - dlnyu) / np.abs(dlnyu))
    e_yd = np.max(np.abs(num[1] / yd * K - dlnyd) / np.abs(dlnyd))
    e_v = np.max(np.abs(num[2] * K - dabs) / np.abs(dabs))
    e_j = abs(numJ * K - dJ) / abs(dJ)
    # rephasing: V -> P V Q with random phases; |V| and J and their closed-form derivatives are unchanged
    P = np.diag(np.exp(1j * rng.uniform(0, 2 * np.pi, 3))); Q = np.diag(np.exp(1j * rng.uniform(0, 2 * np.pi, 3)))
    V2 = P @ V @ Q
    dabs2, dJ2 = dabs_dJ(V2, closed_forms(V2, yu, yd, ye, gs, g, gp)[2])
    J1 = np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]))
    J2 = np.imag(V2[0, 1] * V2[1, 2] * np.conj(V2[0, 2]) * np.conj(V2[1, 1]))
    e_re = max(np.max(np.abs(dabs2 - dabs) / np.abs(dabs)), abs(dJ2 / J2 - dJ / J1) / abs(dJ / J1))
    print("(b) %-24s Eq. (yrun) up %.1e, down %.1e;  Eq. (Vrun) |V| %.1e, J %.1e;  rephasing %.1e  (Richardson, h = %g, h/2)"
          % (label, e_yu, e_yd, e_v, e_j, e_re, h))
    return e_yu, e_yd, e_v, e_j, e_re, dabs / np.abs(V), dJ / J1


bench = check_running("benchmark", Vb, yuB, ydB, yeB, gsB, gB, gpB, 2e-2)
big = check_running("enlarged Yukawas", Vb, math.sqrt(2) * np.array([0.05, 20.0, 165.0]) / 246.0,
                    math.sqrt(2) * np.array([0.3, 5.0, 60.0]) / 246.0, yeB, gsB, gB, gpB, 2e-2)


# %% [markdown]
# ## (b') Eq. (Vrun) at the benchmark in 50-digit arithmetic
# In double precision, d|V_cd|/dln mu (the smallest derivative, K dln|V_cd|/dln mu = -7.4e-5) differs from Eq. (Vrun) by
# a constant 7.7e-7 relative for every step h: LAPACK's SVD of the light-quark singular vectors has an error proportional
# to the off-diagonal entries of Y (which grow like h), so the error does not average out of the difference quotient.
# The same Richardson-extrapolated difference with mpmath (50 digits) agrees with Eq. (Vrun) for all nine |V_ij|.

# %%
def mp_check():
    import mpmath as mp
    mp.mp.dps = 50
    Km = 16 * mp.pi**2
    s12, s23, s13, dl = mp.mpf("0.22501"), mp.mpf("0.04183"), mp.mpf("0.003732"), mp.mpf("1.147")
    c12, c23, c13 = [mp.sqrt(1 - x**2) for x in (s12, s23, s13)]
    e = mp.expj(dl)
    Vm = mp.matrix([[c12 * c13, s12 * c13, s13 / e],
                    [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                    [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])
    vm = 2 * 80 * mp.sqrt(mp.mpf(1881) / 8281) / mp.sqrt(4 * mp.pi / 128)
    yu = [mp.sqrt(2) * mp.mpf(m) / vm for m in ("0.00127", "0.619", "165")]
    yd = [mp.sqrt(2) * mp.mpf(m) / vm for m in ("0.00271", "0.0546", "2.86")]
    dg = lambda M: M.transpose_conj()

    def beta(Yu, Yd):           # the part of Eq. (betaY) that rotates V
        Hu, Hd = Yu * dg(Yu), Yd * dg(Yd)
        return (mp.mpf(3) / 2 * (Hu - Hd) * Yu) / Km, (mp.mpf(3) / 2 * (Hd - Hu) * Yd) / Km

    def step(Yu, Yd, h):
        k1 = beta(Yu, Yd); k2 = beta(Yu + h / 2 * k1[0], Yd + h / 2 * k1[1])
        k3 = beta(Yu + h / 2 * k2[0], Yd + h / 2 * k2[1]); k4 = beta(Yu + h * k3[0], Yd + h * k3[1])
        return (Yu + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), Yd + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))

    P = mp.matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

    def absv(Yu, Yd):
        Uu = mp.svd_c(Yu)[0] * P
        Ud = mp.svd_c(Yd)[0] * P
        W = dg(Uu) * Ud
        return [[abs(W[i, j]) for j in range(3)] for i in range(3)]
    Yu0, Yd0 = mp.diag(yu), Vm * mp.diag(yd)

    def central(h):
        a, b = absv(*step(Yu0, Yd0, h)), absv(*step(Yu0, Yd0, -h))
        return [[(a[i][j] - b[i][j]) / (2 * h) for j in range(3)] for i in range(3)]
    c1, c2 = central(mp.mpf("0.02")), central(mp.mpf("0.01"))
    Du, Dd = mp.diag([y**2 for y in yu]), mp.diag([y**2 for y in yd])
    Hd_u, Hu_d = Vm * Dd * dg(Vm), dg(Vm) * Du * Vm
    Au, Ad = mp.matrix(3, 3), mp.matrix(3, 3)
    for i in range(3):
        for k in range(3):
            if i != k:
                Au[i, k] = -mp.mpf(3) / (2 * Km) * (yu[i]**2 + yu[k]**2) / (yu[k]**2 - yu[i]**2) * Hd_u[i, k]
                Ad[i, k] = -mp.mpf(3) / (2 * Km) * (yd[i]**2 + yd[k]**2) / (yd[k]**2 - yd[i]**2) * Hu_d[i, k]
    dV = -Au * Vm + Vm * Ad
    worst = mp.mpf(0)
    for i in range(3):
        for j in range(3):
            num = (4 * c2[i][j] - c1[i][j]) / 3
            cf = mp.re(mp.conj(Vm[i, j]) * dV[i, j]) / abs(Vm[i, j])
            worst = max(worst, abs((num - cf) / cf))
    return float(worst)


mpdev = mp_check()
print("(b') benchmark, 50 digits: Eq. (Vrun) vs the matrix RGE for all |V_ij|: max relative difference %.1e" % mpdev)
rows.append(("Vrun_abs_rel_bench_50digits", mpdev))
print("(b) benchmark: K dln|V|/dln mu =\n", np.array2string(bench[5], precision=5), "\n    K dlnJ/dln mu = %.5f" % bench[6])
rows += [("yrun_up_rel_bench", bench[0]), ("yrun_down_rel_bench", bench[1]), ("Vrun_abs_rel_bench", bench[2]),
         ("Vrun_J_rel_bench", bench[3]), ("rephasing_rel_bench", bench[4]),
         ("yrun_up_rel_big", big[0]), ("yrun_down_rel_big", big[1]), ("Vrun_abs_rel_big", big[2]),
         ("Vrun_J_rel_big", big[3]), ("rephasing_rel_big", big[4]), ("KdlnJ_bench", bench[6])]
with open(RES / "rg_ckm_general.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value"])
    for name, val in rows:
        w.writerow([name, "%.6e" % val])
print("largest relative difference (a), (b) in double precision, (b') in 50 digits:", "%.1e" % max(r1[0], r2[0], r1[1], r1[2]),
      "%.1e" % max(bench[:5] + big[:5]), "%.1e" % mpdev)
