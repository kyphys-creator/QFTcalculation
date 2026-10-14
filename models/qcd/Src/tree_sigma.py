# %% [markdown]
# # Step (2): tree-level spin/colour sums and cross sections with explicit matrices (QCD)
#
# Research note models/qcd, step (2).  Independent numerical checks of Eq. (12) (eq:Mtree), Eq. (13) (eq:sumtree),
# Eq. (14) (eq:ghostsum) and Eq. (15) (eq:sigtree), with explicit Dirac matrices, spinors, Gell-Mann matrices and real
# transverse polarization vectors, before any trace or colour identity:
#
# 1. Spin, polarization and colour sums of the Feynman-rule amplitudes against the closed forms of the note, at many
#    phase-space points:
#    - (A) u ubar -> t tbar, (B) g g -> t tbar, (C) g g -> g g with the gluon propagator in a general covariant gauge
#      -i [g - (1 - xi) q q/q^2]/q^2: the amplitudes must not depend on xi;
#    - (B): the physical polarization sum, the -g sum (four basis vectors weighted by -g_{ll}) and the ghost pairs
#      c cbar -> t tbar, cbar c -> t tbar (Eq. (14)); the Ward residual p1_mu M^{mu nu} = (g^2/s) p2^nu ubar[T^a,T^b]p1slash v
#      for every component nu, spin and colour;
#    - (C): Ward identity (eps(p1) -> p1 with the other gluons physical);
#    - (D) e- e+ -> u ubar g: the sum over spins, polarizations and colours averaged over the lepton directions (six
#      directions +-x, +-y, +-z integrate a quadratic polynomial of the direction exactly) against the three-jet formula.
# 2. Cross sections: Eq. (15) against the numerical integral of Eq. (13), and against MadGraph (tree_mg5.mg5):
#    (A), (B) at sqrt(s) = 3, 5, 10;  (C) with |cos theta| < C0 (MadGraph: |eta_j| < atanh(C0)) at 5, 10, 20;
#    (D) with all pair invariants s_ij > Y s (MadGraph: mmjj = sqrt(Y s)) at 5, 10, 20.
#
# Parameters: m = 1, g = 1 (alpha_s = 1/4pi), e = 1 (GeV units in MadGraph; MadGraph runs alpha_s from its param_card
# value at M_Z, so tree_mg5.mg5 fixes the renormalization scale at 91.188).
# Batch:  `python3 tree_sigma.py [mg5_log]`.  With an MG5 log the "Cross-section" lines are compared in the order of
# tree_mg5.mg5: (A) x 3, (B) x 3, (C) x 3, (D) x 3.  Interactive (VS Code, "Run Cell"): the log defaults to work/tree_mg5.log.

# %%
import itertools
import math
import os
import re
import sys

import numpy as np
from scipy.integrate import quad, dblquad
from scipy.special import spence

INTERACTIVE = "ipykernel" in sys.modules
GEV2_TO_PB = 0.3893794e9
MT, GS, EE = 1.0, 1.0, 1.0
ALS = GS ** 2 / (4 * math.pi)
ALPHA = EE ** 2 / (4 * math.pi)
NC, CF, CA, TF, DA = 3, 4.0 / 3.0, 3.0, 0.5, 8
QU = 2.0 / 3.0
SQRTS = {"A": (3.0, 5.0, 10.0), "B": (3.0, 5.0, 10.0), "C": (5.0, 10.0, 20.0), "D": (5.0, 10.0, 20.0)}
C0 = 0.8          # (C): |cos theta| < C0
Y = 0.1           # (D): s_ij > Y s for all three pairs

# %% [markdown]
# ## Dirac and colour matrices, spinors, polarization vectors
#
# Dirac representation, u(p, chi) = (sqrt(E+m) chi, (s.p) chi/sqrt(E+m)), v(p, eta) = ((s.p) eta/sqrt(E+m), sqrt(E+m) eta)
# (sum u ubar = pslash + m, sum v vbar = pslash - m).  T^a = lambda^a/2, f^{abc} = -2i tr([T^a,T^b]T^c).
# Gluon polarizations: real transverse unit vectors orthogonal to the direction of motion.

# %%
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
G0 = np.block([[I2, Z2], [Z2, -I2]])
GAM = [G0] + [np.block([[Z2, s], [-s, Z2]]) for s in SIG]
METRIC = np.diag([1.0, -1.0, -1.0, -1.0])


def slash(p):
    return GAM[0] * p[0] - GAM[1] * p[1] - GAM[2] * p[2] - GAM[3] * p[3]


def dot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def lower(v):
    return METRIC @ v


def u_spinors(p, m):
    E = p[0]
    sp = sum(SIG[i] * p[i + 1] for i in range(3))
    out = []
    for chi in (np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)):
        out.append(np.concatenate([math.sqrt(E + m) * chi, sp @ chi / math.sqrt(E + m)]))
    return out


def v_spinors(p, m):
    E = p[0]
    sp = sum(SIG[i] * p[i + 1] for i in range(3))
    out = []
    for eta in (np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)):
        out.append(np.concatenate([sp @ eta / math.sqrt(E + m), math.sqrt(E + m) * eta]))
    return out


def bar(sp):
    return sp.conj() @ G0


def pols(k):
    n = k[1:] / np.linalg.norm(k[1:])
    a = np.array([0.0, 1.0, 0.0]) if abs(n[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = a - np.dot(a, n) * n
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    return [np.concatenate([[0.0], e1]), np.concatenate([[0.0], e2])]


LAM = np.zeros((8, 3, 3), dtype=complex)
LAM[0][0, 1] = LAM[0][1, 0] = 1
LAM[1][0, 1], LAM[1][1, 0] = -1j, 1j
LAM[2][0, 0], LAM[2][1, 1] = 1, -1
LAM[3][0, 2] = LAM[3][2, 0] = 1
LAM[4][0, 2], LAM[4][2, 0] = -1j, 1j
LAM[5][1, 2] = LAM[5][2, 1] = 1
LAM[6][1, 2], LAM[6][2, 1] = -1j, 1j
LAM[7] = np.diag([1, 1, -2]) / math.sqrt(3)
T = LAM / 2
FABC = np.zeros((8, 8, 8))
for a, b, c in itertools.product(range(8), repeat=3):
    FABC[a, b, c] = (-2j * np.trace((T[a] @ T[b] - T[b] @ T[a]) @ T[c])).real

# %% [markdown]
# ## Kinematics: 2 -> 2 in the CM frame
#
# p1 along +z, p2 along -z; k1 at polar angle theta and azimuth phi; t = (p1 - k1)^2, u = (p1 - k2)^2.

# %%
def kin22(sqrts, m_in, m_out, cth, phi=0.3):
    s = sqrts ** 2
    E = sqrts / 2
    pin = math.sqrt(E * E - m_in ** 2)
    pout = math.sqrt(E * E - m_out ** 2)
    sth = math.sqrt(1 - cth * cth)
    p1 = np.array([E, 0, 0, pin])
    p2 = np.array([E, 0, 0, -pin])
    n = np.array([sth * math.cos(phi), sth * math.sin(phi), cth])
    k1 = np.concatenate([[E], pout * n])
    k2 = np.concatenate([[E], -pout * n])
    return s, p1, p2, k1, k2


def prop_tensor(q, xi):
    """numerator of -i[g - (1-xi) q q/q^2]/q^2 without the -i/q^2, with upper indices"""
    q2 = dot(q, q)
    return METRIC - (1 - xi) * np.outer(q, q) / q2

# %% [markdown]
# ## (A) u ubar -> t tbar

# %%
def sumA(sqrts, cth, xi=1.0):
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, MT, cth)
    P = p1 + p2
    N = prop_tensor(P, xi)
    tot = 0.0
    for uu in u_spinors(p1, 0.0):
        for vv in v_spinors(p2, 0.0):
            Jin = np.array([bar(vv) @ GAM[mu] @ uu for mu in range(4)])
            for ut in u_spinors(k1, MT):
                for vt in v_spinors(k2, MT):
                    Jout = np.array([bar(ut) @ GAM[mu] @ vt for mu in range(4)])
                    lor = (lower(Jin) @ N @ lower(Jout)) * GS ** 2 / s
                    # colour: sum_{ijkl} |T^a_{ji} T^a_{kl}|^2 computed explicitly
                    col = np.einsum("aji,akl->ijkl", T, T)
                    tot += np.sum(np.abs(lor * col) ** 2)
    return tot


def sumA_note(sqrts, cth):
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, MT, cth)
    t, u = dot(p1 - k1, p1 - k1), dot(p1 - k2, p1 - k2)
    return 8 * GS ** 4 * TF ** 2 * DA * ((t - MT ** 2) ** 2 + (u - MT ** 2) ** 2 + 2 * MT ** 2 * s) / s ** 2

# %% [markdown]
# ## (B) g g -> t tbar, -g sum, ghosts and the Ward residual
#
# M = -g^2 ubar [T^aT^b e1 (k1-p1+m) e2/(t-m^2) + T^bT^a e2 (k1-p2+m) e1/(u-m^2) + [T^a,T^b] V/s] v with the s-channel
# gluon propagator in a general gauge: V = (gluon vertex contracted with e1, e2) . N(P) . gamma (note Eq. (12)).

# %%
def three_gluon(k, p, q):
    """V^{mu nu rho}(k, p, q), upper indices, all momenta incoming"""
    return (np.einsum("mn,r->mnr", METRIC, k - p) + np.einsum("nr,m->mnr", METRIC, p - q)
            + np.einsum("rm,n->mnr", METRIC, q - k))


def ampB_lorentz(p1, p2, k1, k2, e1, e2, ut, vt, xi):
    """the three Lorentz structures (t, u, s) of M_B for given spinors and polarizations (upper-index vectors)"""
    s = dot(p1 + p2, p1 + p2)
    t = dot(p1 - k1, p1 - k1)
    u = dot(p1 - k2, p1 - k2)
    At = bar(ut) @ slash(e1) @ (slash(k1 - p1) + MT * np.eye(4)) @ slash(e2) @ vt / (t - MT ** 2)
    Au = bar(ut) @ slash(e2) @ (slash(k1 - p2) + MT * np.eye(4)) @ slash(e1) @ vt / (u - MT ** 2)
    P = p1 + p2
    V = np.einsum("m,n,mna->a", lower(e1), lower(e2), three_gluon(p1, p2, -P))
    V = prop_tensor(P, xi) @ lower(V)        # upper index after contraction with N^{ab} g_{b.}
    J = np.array([bar(ut) @ GAM[mu] @ vt for mu in range(4)])
    As = dot(V, J) / s                        # M_s = -g^2 [T^a,T^b] (J.N.V)/s since -i f^{abc} T^c = -[T^a,T^b] (App. I)
    return At, Au, As


def sumB(sqrts, cth, xi=1.0, mode="phys"):
    """mode: phys (two transverse polarizations per gluon) or minusg (basis vectors weighted by -g_ll)"""
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, MT, cth)
    if mode == "phys":
        P1 = [(1.0, e) for e in pols(p1)]
        P2 = [(1.0, e) for e in pols(p2)]
    else:
        basis = [np.eye(4)[l] for l in range(4)]
        P1 = [(-METRIC[l, l], basis[l]) for l in range(4)]
        P2 = P1
    TaTb = np.einsum("aij,bjk->abik", T, T)
    TbTa = np.einsum("bij,ajk->abik", T, T)
    tot = 0.0
    for (w1, e1), (w2, e2) in itertools.product(P1, P2):
        for ut in u_spinors(k1, MT):
            for vt in v_spinors(k2, MT):
                At, Au, As = ampB_lorentz(p1, p2, k1, k2, e1, e2, ut, vt, xi)
                M = -GS ** 2 * (TaTb * At + TbTa * Au + (TaTb - TbTa) * As)
                tot += w1 * w2 * np.sum(np.abs(M) ** 2)
    return tot


def sumB_note(sqrts, cth):
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, MT, cth)
    t, u = dot(p1 - k1, p1 - k1), dot(p1 - k2, p1 - k2)
    t1, t2, rho = (MT ** 2 - t) / s, (MT ** 2 - u) / s, 4 * MT ** 2 / s
    return 8 * GS ** 4 * CA * CF * (CF / (t1 * t2) - CA) * (t1 ** 2 + t2 ** 2 + rho - rho ** 2 / (4 * t1 * t2))


def ghostB(sqrts, cth):
    """sum |M(c cbar -> t tbar)|^2 with M = -(g^2/s) ubar [T^a,T^b] p2slash v (note App. I)"""
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, MT, cth)
    comm = np.einsum("aij,bjk->abik", T, T) - np.einsum("bij,ajk->abik", T, T)
    tot = 0.0
    for ut in u_spinors(k1, MT):
        for vt in v_spinors(k2, MT):
            M = -GS ** 2 / s * comm * (bar(ut) @ slash(p2) @ vt)
            tot += np.sum(np.abs(M) ** 2)
    return tot


def wardB(sqrts, cth):
    """max over nu, spins, colours of |p1_mu M^{mu nu} - (g^2/s) p2^nu ubar[T^a,T^b]p1slash v| / max|M|"""
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, MT, cth)
    TaTb = np.einsum("aij,bjk->abik", T, T)
    TbTa = np.einsum("bij,ajk->abik", T, T)
    worst, scale = 0.0, 0.0
    for nu in range(4):
        e2 = np.eye(4)[nu]          # upper-index basis vector: picks M^{. nu} g_{nu nu}
        for ut in u_spinors(k1, MT):
            for vt in v_spinors(k2, MT):
                At, Au, As = ampB_lorentz(p1, p2, k1, k2, p1, e2, ut, vt, 1.0)
                M = -GS ** 2 * (TaTb * At + TbTa * Au + (TaTb - TbTa) * As)
                W = GS ** 2 / s * (TaTb - TbTa) * (bar(ut) @ slash(p1) @ vt) * dot(p2, e2)
                worst = max(worst, np.max(np.abs(M - W)))
                scale = max(scale, np.max(np.abs(W)))
    return worst / scale

# %% [markdown]
# ## (C) g g -> g g (Feynman rules of note Fig. 1, general gauge for the internal gluon)

# %%
FS = np.einsum("abe,ecd->abcd", FABC, FABC)
FT = np.einsum("ace,ebd->abcd", FABC, FABC)
FU = np.einsum("ade,ebc->abcd", FABC, FABC)
F1 = np.einsum("abe,cde->abcd", FABC, FABC)
F2 = np.einsum("ace,bde->abcd", FABC, FABC)
F3 = np.einsum("ade,bce->abcd", FABC, FABC)


def ampC(p1, p2, k1, k2, e1, e2, e3, e4, xi):
    s, t, u = dot(p1 + p2, p1 + p2), dot(p1 - k1, p1 - k1), dot(p1 - k2, p1 - k2)
    L1, L2, L3, L4 = lower(e1), lower(e2), lower(e3), lower(e4)
    J1 = np.einsum("m,n,mna->a", L1, L2, three_gluon(p1, p2, -(p1 + p2)))
    J2 = np.einsum("r,s,brs->b", L3, L4, three_gluon(p1 + p2, -k1, -k2))
    Ls = -(GS ** 2 / s) * (lower(J1) @ prop_tensor(p1 + p2, xi) @ lower(J2))
    J1 = np.einsum("m,r,mra->a", L1, L3, three_gluon(p1, -k1, k1 - p1))
    J2 = np.einsum("n,s,bns->b", L2, L4, three_gluon(p1 - k1, p2, -k2))
    Lt = -(GS ** 2 / t) * (lower(J1) @ prop_tensor(p1 - k1, xi) @ lower(J2))
    J1 = np.einsum("m,s,msa->a", L1, L4, three_gluon(p1, -k2, k2 - p1))
    J2 = np.einsum("n,r,bnr->b", L2, L3, three_gluon(p1 - k2, p2, -k1))
    Lu = -(GS ** 2 / u) * (lower(J1) @ prop_tensor(p1 - k2, xi) @ lower(J2))
    c1 = dot(e1, e3) * dot(e2, e4) - dot(e1, e4) * dot(e2, e3)
    c2 = dot(e1, e2) * dot(e3, e4) - dot(e1, e4) * dot(e2, e3)
    c3 = dot(e1, e2) * dot(e3, e4) - dot(e1, e3) * dot(e2, e4)
    return Ls * FS + Lt * FT + Lu * FU - GS ** 2 * (F1 * c1 + F2 * c2 + F3 * c3)


def sumC(sqrts, cth, xi=1.0):
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, 0.0, cth)
    tot = 0.0
    for e1, e2, e3, e4 in itertools.product(pols(p1), pols(p2), pols(k1), pols(k2)):
        tot += np.sum(np.abs(ampC(p1, p2, k1, k2, e1, e2, e3, e4, xi)) ** 2)
    return tot


def sumC_note(sqrts, cth):
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, 0.0, cth)
    t, u = dot(p1 - k1, p1 - k1), dot(p1 - k2, p1 - k2)
    return 16 * GS ** 4 * CA ** 2 * DA * (3 - t * u / s ** 2 - s * u / t ** 2 - s * t / u ** 2)


def wardC(sqrts, cth):
    s, p1, p2, k1, k2 = kin22(sqrts, 0.0, 0.0, cth)
    worst, scale = 0.0, 0.0
    for e2, e3, e4 in itertools.product(pols(p2), pols(k1), pols(k2)):
        worst = max(worst, np.max(np.abs(ampC(p1, p2, k1, k2, p1, e2, e3, e4, 1.0))))
        scale = max(scale, np.max(np.abs(ampC(p1, p2, k1, k2, pols(p1)[0], e2, e3, e4, 1.0))))
    return worst / scale

# %% [markdown]
# ## (D) e- e+ -> u ubar g, averaged over the lepton directions
#
# Hadron momenta in the CM frame from (x1, x2): the quark along +z, the antiquark and the gluon in the xz plane.
# M = e^2 Q_u g/s [vbar(p2) g_nu u(p1)] ubar(k1) T^a [e*(k1+k3) g^nu/(2k1.k3) - g^nu (k2+k3) e*/(2k2.k3)] v(k2)
# (overall sign irrelevant).  The six lepton directions +-x, +-y, +-z average the quadratic dependence exactly.

# %%
def hadrons(sqrts, x1, x2):
    E = sqrts / 2
    x3 = 2 - x1 - x2
    E1, E2, E3 = x1 * E, x2 * E, x3 * E
    # angle between quark and antiquark: |k1 + k2| = E3
    c12 = (E3 ** 2 - E1 ** 2 - E2 ** 2) / (2 * E1 * E2)
    s12 = math.sqrt(max(0.0, 1 - c12 ** 2))
    k1 = np.array([E1, 0, 0, E1])
    k2 = np.array([E2, E2 * s12, 0, E2 * c12])
    k3 = np.array([sqrts, 0, 0, 0]) - k1 - k2
    return k1, k2, k3


def sumD(sqrts, x1, x2):
    s = sqrts ** 2
    k1, k2, k3 = hadrons(sqrts, x1, x2)
    E = sqrts / 2
    tot = 0.0
    dirs = [np.array(d, dtype=float) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    for n in dirs:
        p1 = np.concatenate([[E], E * n])
        p2 = np.concatenate([[E], -E * n])
        for ue in u_spinors(p1, 0.0):
            for ve in v_spinors(p2, 0.0):
                L = np.array([bar(ve) @ GAM[mu] @ ue for mu in range(4)])
                for eps in pols(k3):
                    for uq in u_spinors(k1, 0.0):
                        for vq in v_spinors(k2, 0.0):
                            H = np.array([bar(uq) @ (slash(eps) @ slash(k1 + k3) @ GAM[nu] / (2 * dot(k1, k3))
                                                     - GAM[nu] @ slash(k2 + k3) @ slash(eps) / (2 * dot(k2, k3))) @ vq
                                          for nu in range(4)])
                            lor = EE ** 2 * QU * GS / s * dot(L, H)
                            tot += abs(lor) ** 2 * np.sum(np.abs(T) ** 2) / len(dirs)
    return tot


def sumD0(sqrts):
    """Born e- e+ -> u ubar averaged over the lepton directions"""
    s = sqrts ** 2
    E = sqrts / 2
    k1 = np.array([E, 0, 0, E])
    k2 = np.array([E, 0, 0, -E])
    tot = 0.0
    dirs = [np.array(d, dtype=float) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    for n in dirs:
        p1 = np.concatenate([[E], E * n])
        p2 = np.concatenate([[E], -E * n])
        for ue in u_spinors(p1, 0.0):
            for ve in v_spinors(p2, 0.0):
                L = np.array([bar(ve) @ GAM[mu] @ ue for mu in range(4)])
                for uq in u_spinors(k1, 0.0):
                    for vq in v_spinors(k2, 0.0):
                        H = np.array([bar(uq) @ GAM[nu] @ vq for nu in range(4)])
                        tot += abs(EE ** 2 * QU / s * dot(L, H)) ** 2 * NC / len(dirs)
    return tot


def threejet_note(x1, x2):
    return CF * ALS / (2 * math.pi) * (x1 ** 2 + x2 ** 2) / ((1 - x1) * (1 - x2))

# %% [markdown]
# ## 1. Spin/colour sums against the closed forms

# %%
def check_sums():
    rows = []
    for sq in (3.0, 5.0, 10.0):
        for c in (-0.9, -0.3, 0.3, 0.7, 0.95):
            rows.append(("A", sq, c, sumA(sq, c) / sumA_note(sq, c) - 1, abs(sumA(sq, c, 0.0) / sumA(sq, c, 3.0) - 1)))
            phys = sumB(sq, c)
            rows.append(("B", sq, c, phys / sumB_note(sq, c) - 1, abs(sumB(sq, c, 0.0) / sumB(sq, c, 3.0) - 1)))
            _, q1, q2, r1, r2 = kin22(sq, 0.0, MT, c)
            tau12 = (MT ** 2 - dot(q1 - r1, q1 - r1)) * (MT ** 2 - dot(q1 - r2, q1 - r2)) / sq ** 4
            gh = ghostB(sq, c)
            rows.append(("B ghost", sq, c, (sumB(sq, c, mode="minusg") - phys) / (2 * gh) - 1,
                         abs(gh / (GS ** 4 * CA * DA * tau12) - 1)))
            rows.append(("B Ward", sq, c, wardB(sq, c), 0.0))
            rows.append(("C", sq, c, sumC(sq, c) / sumC_note(sq, c) - 1, abs(sumC(sq, c, 0.0) / sumC(sq, c, 3.0) - 1)))
            rows.append(("C Ward", sq, c, wardC(sq, c), 0.0))
    for sq in (5.0, 20.0):
        for x1, x2 in ((0.6, 0.7), (0.9, 0.5), (0.75, 0.95), (0.98, 0.98)):
            ratio = (sumD(sq, x1, x2) * sq ** 2 / (128 * math.pi ** 3)) / (sumD0(sq) / (8 * math.pi))
            rows.append(("D", sq, x1 * 10 + x2, ratio / threejet_note(x1, x2) - 1, 0.0))
    return rows


rows = check_sums()
print("process  sqrt(s)  point   rel. dev. from the note   |xi=0 / xi=3 - 1|")
for r in rows:
    print(f"{r[0]:8s} {r[1]:6.1f} {r[2]:7.2f}   {r[3]: .2e}   {r[4]:.2e}")
for proc in ("A", "B", "B ghost", "B Ward", "C", "C Ward", "D"):
    dev = max(abs(r[3]) for r in rows if r[0] == proc)
    xi = max(r[4] for r in rows if r[0] == proc)
    print(f"max |dev| {proc:8s}: {dev:.2e}    max xi dependence: {xi:.2e}")
print("check point sqrt(s) = 5, cos = 0.3 (tree_feyncalc.wl prints the same): "
      f"(A) {sumA(5.0, 0.3):.16g}  (B) {sumB(5.0, 0.3):.16g}  (C) {sumC(5.0, 0.3):.16g}")

# %% [markdown]
# ## 2. Cross sections: Eq. (15) and numerical integrals of Eq. (13)
#
# sigma = (1/2s) (1/(spin x colour average)) int sum|M|^2 dPhi_2,  dPhi_2 = beta/(16 pi) dcos  (identical gluons in
# (C): extra 1/2);  sigma_D = sigma_0 C_F alpha_s/2pi F(Y), sigma_0 = N_c Q_u^2 4 pi alpha^2/(3s).

# %%
def sigA_note(sq):
    s = sq * sq
    rho = 4 * MT ** 2 / s
    beta = math.sqrt(1 - rho)
    return GS ** 4 * TF ** 2 * DA * beta * (1 + rho / 2) / (12 * math.pi * s * NC ** 2)


def sigB_note(sq):
    s = sq * sq
    rho = 4 * MT ** 2 / s
    beta = math.sqrt(1 - rho)
    L = math.log((1 + beta) / (1 - beta))
    I0 = CF * ((4 + 4 * rho - 2 * rho ** 2) * L / beta - 4 * (1 + rho)) - CA * (4 / 3 + 5 * rho / 3 - rho ** 2 * L / beta)
    return GS ** 4 * CA * CF * beta * I0 / (16 * math.pi * s * DA ** 2)


def sigC_note(sq):
    s = sq * sq
    c = C0
    J = 16 * c / (1 - c * c) + 5.5 * c + c ** 3 / 6 - 4 * math.log((1 + c) / (1 - c))
    return math.pi * ALS ** 2 * CA ** 2 * J / (s * DA)


def F3jet(y):
    """int over s_ij > y s of (x1^2 + x2^2)/((1-x1)(1-x2)) dx1 dx2 (note Eq. (15))"""
    li2 = lambda z: spence(1 - z)       # scipy's spence(x) = Li2(1 - x)
    return ((3 - 6 * y) * math.log(y / (1 - 2 * y)) + 2 * math.log(y / (1 - y)) ** 2 + 2.5 - 6 * y - 4.5 * y * y
            + 4 * li2(y / (1 - y)) - math.pi ** 2 / 3)


def sig0(sq):
    return NC * QU ** 2 * 4 * math.pi * ALPHA ** 2 / (3 * sq * sq)


def sigD_note(sq):
    return sig0(sq) * CF * ALS / (2 * math.pi) * F3jet(Y)


def sig_numeric(proc, sq):
    s = sq * sq
    if proc == "A":
        beta = math.sqrt(1 - 4 * MT ** 2 / s)
        val, _ = quad(lambda c: sumA_note(sq, c), -1, 1, epsabs=0, epsrel=1e-13)
        return val * beta / (16 * math.pi) / (2 * s) / (4 * NC ** 2)
    if proc == "B":
        beta = math.sqrt(1 - 4 * MT ** 2 / s)
        val, _ = quad(lambda c: sumB_note(sq, c), -1, 1, epsabs=0, epsrel=1e-13)
        return val * beta / (16 * math.pi) / (2 * s) / (4 * DA ** 2)
    if proc == "C":
        val, _ = quad(lambda c: sumC_note(sq, c), -C0, C0, epsabs=0, epsrel=1e-13)
        return 0.5 * val / (16 * math.pi) / (2 * s) / (4 * DA ** 2)
    if proc == "D":
        f = lambda x2, x1: (x1 ** 2 + x2 ** 2) / ((1 - x1) * (1 - x2))
        val, _ = dblquad(f, 2 * Y, 1 - Y, lambda x1: 1 + Y - x1, lambda x1: 1 - Y, epsabs=0, epsrel=1e-12)
        return sig0(sq) * CF * ALS / (2 * math.pi) * val


NOTE = {"A": sigA_note, "B": sigB_note, "C": sigC_note, "D": sigD_note}
print("\nCross sections in pb (GeV units): Eq. (15) vs numerical integral of Eq. (13)")
for proc in "ABCD":
    for sq in SQRTS[proc]:
        a, b = NOTE[proc](sq), sig_numeric(proc, sq)
        print(f"({proc}) sqrt(s) = {sq:5.1f}: Eq. (15) {a * GEV2_TO_PB:.10e}   numerical {b * GEV2_TO_PB:.10e}   rel {a / b - 1: .1e}")

# %% [markdown]
# ## 3. MadGraph

# %%
def read_mg5(path):
    """cross sections in the order of tree_mg5.mg5.  The log prints 4 digits; the run pages
    work/mg5_tree<X>/HTML/run_0<n>/results.html print 5 ("s= 2.3236e+05 &#177 42") and are used when present."""
    base = os.path.dirname(path) or "."
    vals = []
    for proc in "ABCD":
        for n in range(1, len(SQRTS[proc]) + 1):
            html = os.path.join(base, f"mg5_tree{proc}", "HTML", f"run_{n:02d}", "results.html")
            if not os.path.exists(html):
                vals = []
                break
            with open(html) as fh:
                m = re.search(r"s= ([0-9.eE+-]+) &#177 ([0-9.eE+-]+)", fh.read())
            vals.append((float(m.group(1)), float(m.group(2))))
        else:
            continue
        break
    if vals:
        return vals, "results.html (5 digits)"
    with open(path) as fh:
        for line in fh:
            m = re.search(r"Cross-section :\s+([0-9.eE+-]+)\s+\+-\s+([0-9.eE+-]+)\s+pb", line)
            if m:
                vals.append((float(m.group(1)), float(m.group(2))))
    return vals, "log (4 digits)"


log = sys.argv[1] if len(sys.argv) > 1 and not INTERACTIVE else "work/tree_mg5.log"
if os.path.exists(log):
    vals, src = read_mg5(log)
    order = [(p, sq) for p in "ABCD" for sq in SQRTS[p]]
    print(f"\nMadGraph ({log}, values from {src}): {len(vals)} cross sections")
    print("proc sqrt(s)   MadGraph [pb]              Eq. (15) [pb]        pull")
    for (proc, sq), (v, e) in zip(order, vals):
        ref = NOTE[proc](sq) * GEV2_TO_PB
        print(f"({proc}) {sq:6.1f}   {v:.5e} +- {e:.2e}   {ref:.6e}   {(v - ref) / e: .2f}")
else:
    print(f"\n(no MadGraph log at {log})")
