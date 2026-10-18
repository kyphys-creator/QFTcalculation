# %% [markdown]
# # Step (10) of the CKM note: the two-loop Yukawa-matrix beta functions from the general formulas
#
# Research note models/sm_ckm, step (10).  The general two-loop formulas of Luo, Wang and Xiao (Phys. Rev. D 67 (2003)
# 065019; the corrected form of Machacek and Vaughn) with the semi-simple rules of their Sec. VI, as implemented in the SM
# note's models/sm/Src/rg_twoloop.py (checked there against Buttazzo et al. with y_t, y_b, y_tau only), evaluated with the
# explicit field content of step (4) (rg_ckm_general.py: 45 Weyl fermions, Phi as 4 real scalars) and complex 3 x 3
# Yukawa matrices Y_u, Y_d, Y_e.  The convention of the note: -Qbar Y_d Phi d_R - Qbar Y_u Phitilde u_R - Lbar Y_e Phi e_R,
# V = -mu^2 |Phi|^2 + lambda |Phi|^4, beta = d/d ln mu = beta^(1)/K + beta^(2)/K^2, K = (4 pi)^2.
#   (a) the general one-loop beta_Y against Eq. (betaY) at random complex points (as in step (4));
#   (b) the two-loop beta_{Y_f} (f = u, d, e), projected on the Dirac matrices, written as X_f Y_f with X_f in a basis of
#       matrix structures: H_u^2, H_u H_d, H_d H_u, H_d^2 (H_e^2 for f = e), H_f times {tr H_u, tr H_d, tr H_e, lambda,
#       g'^2, g^2, g_s^2} (also H_d, H_u for f = u, d), and the identity times every quartic invariant (traces of two H,
#       products of two traces, lambda^2, lambda x {traces, g^2}, {traces} x g^2, g^4).  The coefficients are fitted at
#       random complex points, rationalized, and checked at other points; the general beta^a must have no entries outside
#       the Yukawa structure;
#   (c) the two-loop gauge beta functions: the form of Buttazzo et al. (sm_rge.py) with y_t^2, y_b^2, y_tau^2 replaced by
#       tr H_u, tr H_d, tr H_e, against the general formula at random complex points (they do not depend on V);
#   (d) the limit Y_u = diag(0, 0, y_t), Y_d = Y_e = 0, g = g' = 0 against the SM note's two-loop gaugeless beta_yt, beta_gS
#       computed from its own FeynArts model (models/sm/Src/results/twoloop_sym_beta.csv).
# Output: results/rg2_ckm_coeffs.csv (the coefficients), results/rg2_ckm_general.csv.  Batch: python3 rg2_ckm_general.py

# %%
import csv
import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
RES.mkdir(exist_ok=True)
SMSRC = HERE.parent.parent / "sm" / "Src"
sys.path.insert(0, str(SMSRC))
import sm_rge  # noqa: E402

K = 16 * math.pi**2
KAPPA = 0.5
rng = np.random.default_rng(20261018)
dag = lambda m: m.conj().T

# %% [markdown]
# ## Group theory and the field content (as in rg_ckm_general.py and the SM note's rg_twoloop.py)

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
NS = 4
HYP = {"Q": 1 / 6, "uc": -2 / 3, "dc": 1 / 3, "L": -1 / 2, "ec": 1.0}


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


def groups_at(gs, g, gp):
    """per gauge group: the generators with the couplings included, on the fermions and the scalars"""
    groups = {}
    tf = []
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
    groups[3] = dict(tf=tf, ts=[np.zeros((NS, NS), dtype=complex) for _ in range(8)], g=gs, CG=3.0, dG=8, f=f3)
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
        ts.append(-1j * realify(g * T2[a]))
    groups[2] = dict(tf=tf, ts=ts, g=g, CG=2.0, dG=3, f=f2)
    t = np.zeros((NF, NF), dtype=complex)
    for key, j in idx.items():
        t[j, j] = gp * HYP[key[0]]
    groups[1] = dict(tf=[t], ts=[-1j * realify(gp * 0.5 * np.eye(2))], g=gp, CG=0.0, dG=1, f=None)
    for G in groups.values():
        G["S2F"] = np.trace(G["tf"][0] @ G["tf"][0]).real / G["g"] ** 2
        G["S2S"] = np.trace(G["ts"][0] @ G["ts"][0]).real / G["g"] ** 2
        G["C2F"] = sum(t @ t for t in G["tf"])
        G["C2S"] = sum(t @ t for t in G["ts"])
    TF = [t for k in (3, 2, 1) for t in groups[k]["tf"]]
    TS = [t for k in (3, 2, 1) for t in groups[k]["ts"]]
    return groups, TF, TS


dPhi = np.zeros((2, 4), dtype=complex)
for k in range(2):
    dPhi[k, 2 * k] = 1 / math.sqrt(2)
    dPhi[k, 2 * k + 1] = 1j / math.sqrt(2)
dPhic = np.conj(dPhi)


def weyl_yukawa(Yu, Yd, Ye):
    """Y^a_jk of -(1/2) Y^a_jk phi_a psi_j psi_k + h.c. for the Dirac matrices (as rg_ckm_general.py)"""
    Y = np.zeros((NS, NF, NF), dtype=complex)

    def add(a, j, k, val):
        Y[a, j, k] += val
        Y[a, k, j] += val
    for a in range(NS):
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


def dirac(B):
    """the Dirac matrices (beta_u, beta_d, beta_e) of a Weyl beta^a (the inverse of weyl_yukawa on its image)"""
    bu = np.array([[np.conj(B[2][idx[("Q", i, 0, 0)], idx[("uc", j, 0)]] / dPhi[1, 2]) for j in range(3)] for i in range(3)])
    bd = np.array([[np.conj(B[0][idx[("Q", i, 0, 0)], idx[("dc", j, 0)]] / dPhic[0, 0]) for j in range(3)] for i in range(3)])
    be = np.array([[np.conj(B[0][idx[("L", i, 0)], idx[("ec", j)]] / dPhic[0, 0]) for j in range(3)] for i in range(3)])
    return bu, bd, be


# %% [markdown]
# ## The general one- and two-loop formulas (Luo, Wang, Xiao; as the SM note's rg_twoloop.py, without the dummy scalar)

# %%
def general(Yu, Yd, Ye, gs, g, gp, lam):
    groups, TF, TS = groups_at(gs, g, gp)
    Y = weyl_yukawa(Yu, Yd, Ye)
    r = range(NS)
    Y2F = sum(dag(Y[b]) @ Y[b] for b in r)
    Y2S = np.array([[0.5 * np.trace(dag(Y[a]) @ Y[b] + dag(Y[b]) @ Y[a]) for b in r] for a in r])
    C2F = sum(t @ t for t in TF)
    C2S = sum(t @ t for t in TS)
    dl = np.eye(4)
    L4 = 2 * lam * (np.einsum("ab,cd->abcd", dl, dl) + np.einsum("ac,bd->abcd", dl, dl) + np.einsum("ad,bc->abcd", dl, dl))
    L2S = np.einsum("acde,bcde->ab", L4, L4) / 6
    YY = sum(Y[c] @ dag(Y[c]) for c in r)
    H2S = np.array([[0.5 * np.trace(Y[a] @ dag(Y[b]) @ YY + dag(Y[a]) @ Y[b] @ Y2F) for b in r] for a in r])
    H2bS = np.array([[0.5 * sum(np.trace(Y[a] @ dag(Y[c]) @ Y[b] @ dag(Y[c]) + dag(Y[a]) @ Y[c] @ dag(Y[b]) @ Y[c])
                                for c in r) for b in r] for a in r])
    Y2FS = np.array([[0.5 * np.trace(C2F @ (Y[a] @ dag(Y[b]) + Y[b] @ dag(Y[a]))) for b in r] for a in r])

    def weights(cG, cF, cS):
        wF = sum(G["g"] ** 2 * (cG * G["CG"] + cF * KAPPA * G["S2F"] + cS * G["S2S"]) * G["C2F"] for G in groups.values())
        wS = sum(G["g"] ** 2 * (cG * G["CG"] + cF * KAPPA * G["S2F"] + cS * G["S2S"]) * G["C2S"] for G in groups.values())
        return wF, wS

    def beta1_Y(a):
        out = 0.5 * (Y2F.T @ Y[a] + Y[a] @ Y2F)
        out += 2 * sum(Y[b] @ dag(Y[a]) @ Y[b] for b in r)
        out += 2 * KAPPA * sum(Y[b] * Y2S[b, a] for b in r)
        out -= 3 * (C2F.T @ Y[a] + Y[a] @ C2F)
        return out

    w1F, _ = weights(-97 / 6, 10 / 3, 11 / 12)
    _, w2S = weights(49 / 4, -2.0, -0.25)

    def beta2_Y(a):
        Ya, Yad = Y[a], dag(Y[a])
        o = np.zeros((NF, NF), dtype=complex)
        o += 2 * sum(Y[c] @ dag(Y[b]) @ Ya @ (dag(Y[c]) @ Y[b] - dag(Y[b]) @ Y[c]) for b in r for c in r)
        o -= sum(Y[b] @ (Y2F @ Yad + Yad @ Y2F.T) @ Y[b] for b in r)
        o -= sum(Y[b] @ Y2F @ dag(Y[b]) @ Ya + Ya @ dag(Y[b]) @ Y2F.T @ Y[b] for b in r) / 8
        o -= 4 * KAPPA * sum(Y2S[a, c] * Y[b] @ dag(Y[c]) @ Y[b] for b in r for c in r)
        o -= 2 * KAPPA * sum(Y[b] * H2bS[a, b] for b in r)
        o -= 1.5 * KAPPA * sum(Y2S[b, c] * (Y[b] @ dag(Y[c]) @ Ya + Ya @ dag(Y[c]) @ Y[b]) for b in r for c in r)
        o -= 3 * KAPPA * sum(Y[b] * H2S[a, b] for b in r)
        o -= 2 * sum(L4[a, b, c, d] * Y[b] @ dag(Y[c]) @ Y[d] for b in r for c in r for d in r)
        o += 0.5 * sum(L2S[a, b] * Y[b] for b in r)
        # g^2
        o += 3 * sum(C2F.T @ (Y[b] @ Yad @ Y[b]) + (Y[b] @ Yad @ Y[b]) @ C2F for b in r)
        o += 5 * sum(Y[b] @ (C2F @ Yad + Yad @ C2F.T) @ Y[b] for b in r)
        o -= 1.75 * (C2F.T @ Y2F.T @ Ya + Ya @ Y2F @ C2F)
        o -= 0.25 * sum(Y[b] @ C2F @ dag(Y[b]) @ Ya + Ya @ dag(Y[b]) @ C2F.T @ Y[b] for b in r)
        o += 6 * sum(np.conj(t) @ Ya @ dag(Y[b]) @ np.conj(t) @ Y[b] + Y[b] @ t @ dag(Y[b]) @ Ya @ t for t in TF for b in r)
        o += 10 * KAPPA * sum(Y[b] * Y2FS[a, b] for b in r)
        o += 6 * (sum(C2S[b, c] * Y[b] @ Yad @ Y[c] for b in r for c in r)
                  - 2 * sum(C2S[a, c] * Y[b] @ dag(Y[c]) @ Y[b] for b in r for c in r))
        o += 4.5 * sum(C2S[b, c] * (Y[b] @ dag(Y[c]) @ Ya + Ya @ dag(Y[c]) @ Y[b]) for b in r for c in r)
        # g^4
        o -= 1.5 * ((C2F @ C2F).T @ Ya + Ya @ (C2F @ C2F))
        o += 6 * sum(C2S[a, b] * (C2F.T @ Y[b] + Y[b] @ C2F) for b in r)
        o += w1F.T @ Ya + Ya @ w1F
        o -= 10.5 * sum((C2S @ C2S)[a, c] * Y[c] for c in r)
        o += sum(w2S[a, b] * Y[b] for b in r)
        return o

    def beta_gauge(k):
        G = groups[k]
        gk, CG, dG = G["g"], G["CG"], G["dG"]
        C2F_unc, C2S_unc = G["C2F"] / gk ** 2, G["C2S"] / gk ** 2
        cfsf = np.trace(C2F @ C2F_unc).real / dG
        cssf = np.trace(C2S @ C2S_unc).real / dG
        y4 = sum(np.trace(C2F_unc @ Y[a] @ dag(Y[a])).real for a in r) / dG
        one = gk ** 3 * (-11 / 3 * CG + 4 / 3 * KAPPA * G["S2F"] + 1 / 6 * G["S2S"])
        two = (-gk ** 5 * (34 / 3 * CG ** 2 - KAPPA * 20 / 3 * CG * G["S2F"] - 1 / 3 * CG * G["S2S"])
               + gk ** 3 * (KAPPA * 4 * cfsf + 2 * cssf) - 2 * KAPPA * gk ** 3 * y4)
        return one, two

    B1 = [beta1_Y(a) for a in r]
    B2 = [beta2_Y(a) for a in r]
    return {"Y": Y, "B1": B1, "B2": B2, "gauge": {k: beta_gauge(k) for k in (1, 2, 3)}}


# %% [markdown]
# ## Eq. (betaY) of the note and the basis of the two-loop structures

# %%
def note_beta1(Yu, Yd, Ye, gs, g, gp):
    Hu, Hd, He = Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye)
    T = np.trace(3 * Hu + 3 * Hd + He).real
    I3 = np.eye(3)
    bu = (1.5 * (Hu - Hd) + (T - 8 * gs**2 - 9 / 4 * g**2 - 17 / 12 * gp**2) * I3) @ Yu
    bd = (1.5 * (Hd - Hu) + (T - 8 * gs**2 - 9 / 4 * g**2 - 5 / 12 * gp**2) * I3) @ Yd
    be = (1.5 * He + (T - 9 / 4 * g**2 - 15 / 4 * gp**2) * I3) @ Ye
    return bu, bd, be


def structures(f, Yu, Yd, Ye, gs, g, gp, lam):
    """names and 3 x 3 matrices X_k (beta^(2)_{Y_f} = sum_k c_k X_k Y_f)"""
    Hu, Hd, He = Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye)
    tr = lambda m: np.trace(m).real
    T = {"Tu": tr(Hu), "Td": tr(Hd), "Te": tr(He)}
    G = {"gp2": gp**2, "g2": g**2, "gs2": gs**2}
    lin = {**T, "lam": lam, **G}
    quart = {"trHu2": tr(Hu @ Hu), "trHd2": tr(Hd @ Hd), "trHe2": tr(He @ He), "trHuHd": tr(Hu @ Hd)}
    for (a, x), (b, y) in itertools.combinations_with_replacement(T.items(), 2):
        quart[a + b] = x * y
    quart["lam2"] = lam**2
    for a, x in {**T, **G}.items():
        quart["lam" + a] = lam * x
    for a, x in T.items():
        for b, y in G.items():
            quart[a + b] = x * y
    for (a, x), (b, y) in itertools.combinations_with_replacement(G.items(), 2):
        quart[a + b] = x * y
    I3 = np.eye(3)
    mats = {}
    if f in ("u", "d"):
        mats.update({"HuHu": Hu @ Hu, "HuHd": Hu @ Hd, "HdHu": Hd @ Hu, "HdHd": Hd @ Hd})
        for a, x in lin.items():
            mats["Hu*" + a] = Hu * x
            mats["Hd*" + a] = Hd * x
    else:
        mats["HeHe"] = He @ He
        for a, x in lin.items():
            mats["He*" + a] = He * x
    for a, x in quart.items():
        mats["1*" + a] = I3 * x
    Yf = {"u": Yu, "d": Yd, "e": Ye}[f]
    return list(mats), [m @ Yf for m in mats.values()]


def random_point():
    cm = lambda s: s * (rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))
    return (cm(rng.uniform(0.2, 0.5)), cm(rng.uniform(0.1, 0.4)), cm(rng.uniform(0.05, 0.3)),
            rng.uniform(0.6, 1.3), rng.uniform(0.4, 0.9), rng.uniform(0.2, 0.6), rng.uniform(-0.2, 0.3))


def gauge_closed(Yu, Yd, Ye, gs, g, gp, lam):
    """K^2 beta^(2) of (g', g, g_s) from sm_rge.py (Buttazzo et al.) with y^2 -> traces; d g^2/d ln mu^2 = g beta_g"""
    Hu, Hd, He = Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye)
    t, b, tau = (np.trace(m).real for m in (Hu, Hd, He))
    _, two, _, _ = sm_rge.loops(5 / 3 * gp**2, g**2, gs**2, t, b, tau, lam)
    return {1: 3 / 5 * two["g1sq"] / gp, 2: two["g2sq"] / g, 3: two["g3sq"] / gs}



# %% [markdown]
# ## (a) one loop, (b) the two-loop fit, (c)-(e) checks (run as a script)

# %%
def main():
    rows = []
    # the identity structures differ only by their scalar factors, so the fit needs more points than structures
    fit_pts = [random_point() for _ in range(64)]
    chk_pts = [random_point() for _ in range(8)]
    evals = {}
    worst1, worst_out = 0.0, 0.0
    for tag, pts in (("fit", fit_pts), ("check", chk_pts)):
        evals[tag] = []
        for p in pts:
            res = general(*p)
            b1 = dirac(res["B1"])
            b2 = dirac(res["B2"])
            n1 = note_beta1(*p[:6])
            worst1 = max(worst1, max(np.max(np.abs(x - y)) / np.max(np.abs(y)) for x, y in zip(b1, n1)))
            # no entries outside the Yukawa structure: the Weyl image of the projected Dirac matrices is the whole beta^a
            img = weyl_yukawa(*b2)
            worst_out = max(worst_out, max(np.max(np.abs(res["B2"][a] - img[a])) for a in range(NS))
                            / max(np.max(np.abs(img[a])) for a in range(NS)))
            evals[tag].append((p, b2, res["gauge"]))
    print("(a) general one-loop beta_Y vs Eq. (betaY) at %d random complex points: max relative difference %.1e" %
          (len(fit_pts) + len(chk_pts), worst1))
    print("(b) two-loop: largest entry of beta^a outside the Yukawa structure, relative: %.1e" % worst_out)
    rows += [("one_loop_vs_note_rel", worst1), ("two_loop_outside_structure_rel", worst_out)]

    coeffs = {}
    for fi, f in enumerate("ude"):
        A, bvec = [], []
        for p, b2, _ in evals["fit"]:
            names, X = structures(f, *p)
            A.append(np.array([x.flatten() for x in X]).T)
            bvec.append(b2[fi].flatten())
        A = np.vstack(A)
        bvec = np.concatenate(bvec)
        Ar, br = np.vstack([A.real, A.imag]), np.concatenate([bvec.real, bvec.imag])
        c, *_ = np.linalg.lstsq(Ar, br, rcond=None)
        rank = np.linalg.matrix_rank(Ar)
        fr = [Fraction(x).limit_denominator(3000) for x in c]
        dev_rat = max(abs(float(q) - x) for q, x in zip(fr, c))
        # check at the other points with the rational coefficients
        dev = 0.0
        for p, b2, _ in evals["check"]:
            names, X = structures(f, *p)
            pred = sum(float(q) * x for q, x in zip(fr, X))
            dev = max(dev, np.max(np.abs(pred - b2[fi])) / np.max(np.abs(b2[fi])))
        coeffs[f] = list(zip(names, fr, c))
        nz = [(nm, q) for nm, q, _ in coeffs[f] if q != 0]
        print("(b) beta^(2)_{Y_%s}: %d structures (rank %d), %d non-zero; |fit - rational| max %.1e; check points: max relative "
              "difference %.1e" % (f, len(names), rank, len(nz), dev_rat, dev))
        print("      " + "  ".join("%s %s" % (nm, q) for nm, q in nz))
        rows += [("fit_rank_" + f, rank), ("fit_n_structures_" + f, len(names)), ("fit_minus_rational_" + f, dev_rat),
                 ("check_points_rel_" + f, dev)]

    # (c) the two-loop gauge beta functions with traces, (d) the SM note's gaugeless two-loop terms
    dev_g = 0.0
    for p, _, gauge in evals["fit"] + evals["check"]:
        cl = gauge_closed(*p)
        dev_g = max(dev_g, max(abs(gauge[k][1] - cl[k]) / abs(cl[k]) for k in (1, 2, 3)))
    print("(c) two-loop gauge beta functions, Buttazzo et al. with traces vs the general formula: max relative difference %.1e"
          % dev_g)
    rows.append(("gauge_two_loop_rel", dev_g))

    # the SM note's own two-loop gaugeless terms: K^2 beta_yt^(2), K^2 beta_gS^(2)
    expr = {r[0]: r[1] for r in csv.reader(open(SMSRC / "results" / "twoloop_sym_beta.csv"))}
    dev_d = 0.0
    for _ in range(4):
        yt, gS, la = rng.uniform(0.5, 1.2), rng.uniform(0.5, 1.3), rng.uniform(-0.2, 0.3)
        env = {"yt": yt, "gS": gS, "la": la}
        ref_y = eval(expr["K2_beta_yt_two_loop"].replace("^", "**"), {}, env)
        ref_g = eval(expr["K2_beta_gS_two_loop"].replace("^", "**"), {}, env)
        p = (np.diag([0, 0, yt]).astype(complex), np.zeros((3, 3), complex), np.zeros((3, 3), complex), gS, 0.0, 0.0, la)
        names, X = structures("u", *p)
        by = sum(float(q) * x for q, x in zip([q for _, q, _ in coeffs["u"]], X))[2, 2].real
        _, two, _, _ = sm_rge.loops(0.0, 0.0, gS**2, yt**2, 0.0, 0.0, la)
        bg = two["g3sq"] / gS
        dev_d = max(dev_d, abs(by - ref_y) / abs(ref_y), abs(bg - ref_g) / abs(ref_g))
    print("(d) the fitted beta^(2)_{Y_u} and the gauge formula at Y_u = diag(0, 0, y_t), g = g' = 0 against the SM note's "
          "two-loop gaugeless beta_yt, beta_gS from its model: max relative difference %.1e" % dev_d)
    rows.append(("sm_note_gaugeless_rel", dev_d))

    # (e) the diagonal limit (third generation only, all couplings) against Buttazzo et al. (sm_rge.py, a reference)
    dev_e = 0.0
    for _ in range(4):
        yt, yb, ytau = rng.uniform(0.5, 1.1), rng.uniform(0.1, 0.5), rng.uniform(0.05, 0.4)
        gs, g, gp, la = rng.uniform(0.6, 1.3), rng.uniform(0.4, 0.9), rng.uniform(0.2, 0.6), rng.uniform(-0.2, 0.3)
        p = tuple(np.diag([0, 0, y]).astype(complex) for y in (yt, yb, ytau)) + (gs, g, gp, la)
        _, two, _, _ = sm_rge.loops(5 / 3 * gp**2, g**2, gs**2, yt**2, yb**2, ytau**2, la)
        for f, y, key in (("u", yt, "ytsq"), ("d", yb, "ybsq"), ("e", ytau, "ytausq")):
            names, X = structures(f, *p)
            b = sum(float(q) * x for q, x in zip([q for _, q, _ in coeffs[f]], X))[2, 2].real
            dev_e = max(dev_e, abs(b - two[key] / y) / abs(two[key] / y))
    print("(e) the fitted beta^(2)_{Y_f} with the third generation only against Buttazzo et al. (y_t, y_b, y_tau): max relative "
          "difference %.1e" % dev_e)
    rows.append(("diagonal_vs_buttazzo_rel", dev_e))

    with open(RES / "rg2_ckm_coeffs.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["flavour", "structure", "numerator", "denominator", "fitted"])
        for f in "ude":
            for nm, q, x in coeffs[f]:
                w.writerow([f, nm, q.numerator, q.denominator, "%.15e" % x])
    with open(RES / "rg2_ckm_general.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "value"])
        for k, v in rows:
            w.writerow([k, v])
    print("wrote results/rg2_ckm_coeffs.csv, results/rg2_ckm_general.csv")


if __name__ == "__main__":
    main()
