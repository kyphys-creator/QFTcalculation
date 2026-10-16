# %% [markdown]
# # Step (4): the one-loop beta functions of the SM from the general formulas, with explicit field content
#
# Research note models/sm, step (4).  Independent check of Eq. (beta) of the note: the general one-loop formulas for a
# gauge theory with real scalars phi_a and two-component (Weyl) fermions psi_j (Machacek and Vaughn, Nucl. Phys. B 222
# (1983) 83, B 236 (1984) 221, B 249 (1985) 70; Luo, Wang and Xiao, Phys. Rev. D 67 (2003) 065019), in the convention
#     L = ... - (1/2)(Y^a_jk phi_a psi_j psi_k + h.c.) - (1/2) m2_ab phi_a phi_b - (1/4!) lambda_abcd phi^4,
#     D_mu phi = (d_mu - i g_A theta^A A^A_mu) phi (theta imaginary antisymmetric), D_mu psi = (d_mu - i g_A t^A A^A_mu) psi,
# kappa = 1/2, and (times (4 pi)^2):
#     beta_g / g^3 = -(11/3) C2(G) + (4/3) kappa S2(F) + (1/6) S2(S)
#     beta_Y^a = (1/2)(Y2F^T Y^a + Y^a Y2F) + 2 Y^b Y^a+ Y^b + 2 kappa Y^b Y2S_ba - 3 (C2F^T Y^a + Y^a C2F)
#     beta_lambda_abcd = Lambda2 - 8 kappa H + 3 A + 2 kappa LambdaY - 3 LambdaS
#     beta_m2_ab = m2_ef lambda_abef + 2 kappa (Y2S_ae m2_eb + m2_ae Y2S_eb) - 3 (C2S_ae m2_eb + m2_ae C2S_eb)
# with Y2F = Y^b+ Y^b, Y2S_ab = (1/2) tr(Y^a+ Y^b + Y^b+ Y^a), C2F = g_A^2 t^A t^A, C2S = g_A^2 theta^A theta^A,
# Lambda2 = (1/8) sum_perm lambda_abef lambda_efcd, H = (1/4) sum_perm tr(Y^a Y^b+ Y^c Y^d+),
# A = (1/8) sum_perm {Theta^A, Theta^B}_ab {Theta^A, Theta^B}_cd (Theta = g theta), LambdaY = sum over the 4 legs of
# Y2S_ai lambda_ibcd, LambdaS = sum over the 4 legs of C2S_ai lambda_ibcd.
# The SM is built explicitly: 45 Weyl fermions (Q, u^c, d^c, L, e^c per generation, colour and isospin components),
# Phi = ((phi1 + i phi2), (phi3 + i phi4))/sqrt 2, the Yukawa terms -y_d Phi^* Q d^c - y_u (Phi_2 Q_1 - Phi_1 Q_2) u^c
# - y_e Phi^* L e^c (+ h.c.), V = -mu^2 |Phi|^2 + lam |Phi|^4.  The numbers are compared with Eq. (beta) at random
# couplings (all 9 Yukawa couplings different).  Output: results/rg_general.csv.
# Batch: python3 rg_general.py

# %%
import csv
import itertools
import math
from pathlib import Path

import numpy as np

RES = Path(__file__).resolve().parent / "results"
RES.mkdir(exist_ok=True)
KAPPA = 0.5
rng = np.random.default_rng(20261016)

# %% [markdown]
# ## Couplings (random, generic)

# %%
gs, g, gp = 1.13, 0.65, 0.36
lam, mu2 = 0.13, 0.81
yu = np.array([0.011, 0.31, 0.94])
yd = np.array([0.023, 0.057, 0.12])
ye = np.array([0.0071, 0.043, 0.088])

# %% [markdown]
# ## Group theory: generators on the Weyl fermions and on the real scalars

# %%
lam_gm = np.zeros((8, 3, 3), dtype=complex)  # Gell-Mann
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

# fermion index map: per generation Q[c, i] (6), uc[c] (3), dc[c] (3), L[i] (2), ec (1)
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

# generators t^A (including the coupling) on the fermions: 8 gluons, 3 W, 1 B
gens_f = []
for a in range(8):
    t = np.zeros((NF, NF), dtype=complex)
    for gen in range(3):
        for i in range(2):
            for c1 in range(3):
                for c2 in range(3):
                    t[idx[("Q", gen, c1, i)], idx[("Q", gen, c2, i)]] = gs * T3c[a][c1, c2]
        for name in ("uc", "dc"):            # antitriplets: -T^*
            for c1 in range(3):
                for c2 in range(3):
                    t[idx[(name, gen, c1)], idx[(name, gen, c2)]] = -gs * np.conj(T3c[a][c1, c2])
    gens_f.append(t)
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
    gens_f.append(t)
t = np.zeros((NF, NF), dtype=complex)
for key, j in idx.items():
    t[j, j] = gp * HYP[key[0]]
gens_f.append(t)


def realify(m):
    """complex 2x2 generator -> 4x4 action on (Re z1, Im z1, Re z2, Im z2) of i m (a real antisymmetric matrix)."""
    im = 1j * m
    r = np.zeros((4, 4))
    for p in range(2):
        for q in range(2):
            r[2 * p, 2 * q] = im[p, q].real
            r[2 * p, 2 * q + 1] = -im[p, q].imag
            r[2 * p + 1, 2 * q] = im[p, q].imag
            r[2 * p + 1, 2 * q + 1] = im[p, q].real
    return r


# theta^A = -i R (Hermitian, imaginary antisymmetric), including the couplings; gluons do not act on Phi
gens_s = [np.zeros((4, 4), dtype=complex) for _ in range(8)]
gens_s += [-1j * realify(g * T2[a]) for a in range(3)]
gens_s += [-1j * realify(gp * 0.5 * np.eye(2))]

# %% [markdown]
# ## Yukawa matrices Y^a (symmetric in the fermion indices) and the quartic coupling

# %%
# Phi_k = (phi_{2k} + i phi_{2k+1})/sqrt 2: d Phi_k / d phi_a and d Phi_k^* / d phi_a
dPhi = np.zeros((2, 4), dtype=complex)
for k in range(2):
    dPhi[k, 2 * k] = 1 / math.sqrt(2)
    dPhi[k, 2 * k + 1] = 1j / math.sqrt(2)
dPhic = np.conj(dPhi)

Y = np.zeros((4, NF, NF), dtype=complex)


def add(a, j, k, val):
    """-(1/2)(Y^a_jk + Y^a_kj) phi_a psi_j psi_k: a term -val phi_a psi_j psi_k gives Y_jk = Y_kj = val."""
    Y[a, j, k] += val
    Y[a, k, j] += val


for a in range(4):
    for gen in range(3):
        for c in range(3):
            for i in range(2):
                # -y_d Phi_i^* Q_i dc
                add(a, idx[("Q", gen, c, i)], idx[("dc", gen, c)], yd[gen] * dPhic[i, a])
            # -y_u (Phi_2 Q_1 - Phi_1 Q_2) uc
            add(a, idx[("Q", gen, c, 0)], idx[("uc", gen, c)], yu[gen] * dPhi[1, a])
            add(a, idx[("Q", gen, c, 1)], idx[("uc", gen, c)], -yu[gen] * dPhi[0, a])
        for i in range(2):
            add(a, idx[("L", gen, i)], idx[("ec", gen)], ye[gen] * dPhic[i, a])

# V = lam |Phi|^4 with |Phi|^2 = (1/2) sum phi^2: lambda_abcd = 2 lam (d_ab d_cd + d_ac d_bd + d_ad d_bc)
dl = np.eye(4)
L4 = 2 * lam * (np.einsum("ab,cd->abcd", dl, dl) + np.einsum("ac,bd->abcd", dl, dl) + np.einsum("ad,bc->abcd", dl, dl))
M2 = -mu2 * np.eye(4)          # (1/2) m2_ab phi_a phi_b = -mu^2 |Phi|^2

# %% [markdown]
# ## General one-loop formulas

# %%
dag = lambda m: m.conj().T
Y2F = sum(dag(Y[b]) @ Y[b] for b in range(4))
Y2S = np.array([[0.5 * np.trace(dag(Y[a]) @ Y[b] + dag(Y[b]) @ Y[a]) for b in range(4)] for a in range(4)])
C2F = sum(t @ t for t in gens_f)
C2S = sum(t @ t for t in gens_s)


def beta_Y(a):
    out = 0.5 * (Y2F.T @ Y[a] + Y[a] @ Y2F)
    out += 2 * sum(Y[b] @ dag(Y[a]) @ Y[b] for b in range(4))
    out += 2 * KAPPA * sum(Y[b] * Y2S[b, a] for b in range(4))
    out -= 3 * (C2F.T @ Y[a] + Y[a] @ C2F)
    return out


def sym_sum(f, a, b, c, d):
    return sum(f(*p) for p in itertools.permutations((a, b, c, d)))


def beta_L(a, b, c, d):
    lam2 = sym_sum(lambda p, q, r, s: np.einsum("ef,ef->", L4[p, q], L4[:, :, r, s]), a, b, c, d) / 8
    H = sym_sum(lambda p, q, r, s: np.trace(Y[p] @ dag(Y[q]) @ Y[r] @ dag(Y[s])), a, b, c, d) / 4
    A = 0.0
    for tA in gens_s:
        for tB in gens_s:
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


def beta_M2():
    out = np.einsum("ef,abef->ab", M2, L4).astype(complex)
    out += 2 * KAPPA * (Y2S @ M2 + M2 @ Y2S)
    out -= 3 * (C2S @ M2 + M2 @ C2S)
    return out


def group_b(tlist_f, tlist_s, gauge_index, ca, coupling):
    """one-loop gauge coefficient b (beta_g = b g^3/K) from the explicit generators of one gauge boson."""
    s2f = np.trace(tlist_f[gauge_index] @ tlist_f[gauge_index]).real / coupling**2
    s2s = np.trace(tlist_s[gauge_index] @ tlist_s[gauge_index]).real / coupling**2
    return -11 / 3 * ca + 4 / 3 * KAPPA * s2f + 1 / 6 * s2s


# %% [markdown]
# ## Comparison with Eq. (beta) of the note

# %%
rows = []
b3 = group_b(gens_f, gens_s, 0, 3, gs)
b2 = group_b(gens_f, gens_s, 8, 2, g)
b1 = group_b(gens_f, gens_s, 11, 0, gp)
rows += [("b_gs", b3, -7.0), ("b_g", b2, -19 / 6), ("b_gp", b1, 41 / 6)]

TT = np.sum(3 * yu**2 + 3 * yd**2 + ye**2)
NY4 = np.sum(3 * yu**4 + 3 * yd**4 + ye**4)


def note_beta_yu(i):
    return yu[i] * (1.5 * (yu[i]**2 - yd[i]**2) + TT - 8 * gs**2 - 9 / 4 * g**2 - 17 / 12 * gp**2)


def note_beta_yd(i):
    return yd[i] * (1.5 * (yd[i]**2 - yu[i]**2) + TT - 8 * gs**2 - 9 / 4 * g**2 - 5 / 12 * gp**2)


def note_beta_ye(i):
    return ye[i] * (1.5 * ye[i]**2 + TT - 9 / 4 * g**2 - 15 / 4 * gp**2)


# read the Yukawa beta functions off the same entries that define the couplings
for gen in range(3):
    j, k = idx[("Q", gen, 0, 0)], idx[("uc", gen, 0)]
    a = 2      # phi_3: d Phi_2 / d phi_3 = 1/sqrt 2, entry Y^3_{Q1 uc} = y_u/sqrt 2
    rows.append(("beta_yu%d" % (gen + 1), (beta_Y(a)[j, k] / Y[a, j, k] * yu[gen]).real, note_beta_yu(gen)))
    j, k = idx[("Q", gen, 0, 1)], idx[("dc", gen, 0)]
    rows.append(("beta_yd%d" % (gen + 1), (beta_Y(a)[j, k] / Y[a, j, k] * yd[gen]).real, note_beta_yd(gen)))
    j, k = idx[("L", gen, 1)], idx[("ec", gen)]
    rows.append(("beta_ye%d" % (gen + 1), (beta_Y(a)[j, k] / Y[a, j, k] * ye[gen]).real, note_beta_ye(gen)))
# check that beta_Y^a is proportional to Y^a entry by entry (no new structures)
resid = 0.0
for a in range(4):
    bY = beta_Y(a)
    for (j, k) in zip(*np.nonzero(np.abs(bY) > 1e-14)):
        if abs(Y[a, j, k]) < 1e-14:
            resid = max(resid, abs(bY[j, k]))
rows.append(("beta_Y_new_entries_max", resid, 0.0))

# lambda: lambda_1111 = 6 lam; also lambda_1122 = 2 lam
bl = beta_L(0, 0, 0, 0).real / 6
bl2 = beta_L(0, 0, 1, 1).real / 2
note_bl = 24 * lam**2 + 4 * lam * TT - 2 * NY4 - 3 * lam * (3 * g**2 + gp**2) + 3 / 8 * (2 * g**4 + (g**2 + gp**2)**2)
rows += [("beta_lambda_1111", bl, note_bl), ("beta_lambda_1122", bl2, note_bl)]
# mu^2: m2 = -mu^2, so beta(m2_11) = -gamma_mu2
gm = -beta_M2()[0, 0].real
note_gm = mu2 * (12 * lam + 2 * TT - 9 / 2 * g**2 - 3 / 2 * gp**2)
rows.append(("gamma_mu2", gm, note_gm))
# scalar anomalous dimension in Landau gauge (Yukawa part 2 kappa Y2S, gauge part -3 C2S): note's gamma_Phi^L
gphi = (2 * KAPPA * Y2S[0, 0] - 3 * C2S[0, 0]).real
rows.append(("gamma_Phi_Landau", gphi, TT - 9 / 4 * g**2 - 3 / 4 * gp**2))

worst = 0.0
for name, mine, note in rows:
    rel = abs(mine - note) / max(abs(note), 1e-30) if note != 0 else abs(mine)
    worst = max(worst, rel)
    print("%-22s general formula %+.15e   note %+.15e   rel. diff %.1e" % (name, mine, note, rel))
print("largest relative difference:", "%.1e" % worst)
with open(RES / "rg_general.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "general_formula_times_K", "note_times_K"])
    for name, mine, note in rows:
        w.writerow([name, "%.15e" % mine, "%.15e" % note])
