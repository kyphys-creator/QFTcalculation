# %% [markdown]
# # Step (2): tree-level amplitudes, widths and cross sections with explicit matrices (Standard Model)
#
# Research note models/sm, step (2).  Independent numerical checks of the tree-level results of the note with explicit
# Dirac matrices, helicity spinors and polarization vectors, before any trace or spin-sum identity:
#
# 1. e+ e- -> mu+ mu- (photon and Z with the Breit-Wigner width): the sum over helicities of the Feynman-rule amplitudes
#    against Eq. (11) (eq:eeff) at many angles; the cross section and A_FB.
# 2. e+ e- -> W+ W- (t-channel nu_e, s-channel photon and Z): the polarization sum against the explicit -g + k k/M^2;
#    the growth ~ s/M_W^2 of each diagram for longitudinal W pairs and its cancellation in the sum (gauge cancellation);
#    the sum over spins and polarizations against FeynCalc's traces (results/tree_feyncalc_ww.csv, Gamma_Z = 0);
#    the cross section by numerical integration over cos(theta).
# 3. The two-body widths (Eqs. (9), (10) and their massive forms) and the muon width (Eq. (8)) by numerical integration
#    of the Fermi matrix element over the Dalitz plot.
# 4. With MadGraph logs (tree_mg5.mg5): the widths of compute_widths, the muon width and the cross sections (all digits
#    from the run banners in work/mg5_*/Events; the log prints four).
#
# Parameters: those of the UFO's default parameter card (SM.fr 1.4.7): alpha(M_Z)^-1 = 127.9, G_F = 1.16637e-5,
# M_Z = 91.1876, M_W = sqrt(M_Z^2/2 + sqrt(M_Z^4/4 - pi alpha M_Z^2/(sqrt2 G_F))) = 79.82, s_W^2 = 1 - M_W^2/M_Z^2,
# Gamma_Z = 2.4952, the masses of the card, and the Cabibbo angle 0.227736 for the widths (CKM = 1 for scattering).
# Batch:  `python3 tree_numeric.py [work/tree_mg5.log]`.  Interactive (VS Code, "Run Cell"): the log defaults to work/tree_mg5.log.

# %%
import csv
import math
import os
import re
import sys

import numpy as np
from scipy.integrate import quad

INTERACTIVE = "ipykernel" in sys.modules
GEV2_TO_PB = 0.3893794e9

# parameters of the UFO card (SM.fr defaults)
AEW = 1 / 127.9
GF = 1.16637e-5
MZ = 91.1876
MW = math.sqrt(MZ ** 2 / 2 + math.sqrt(MZ ** 4 / 4 - math.pi / math.sqrt(2) * AEW / GF * MZ ** 2))
SW2 = 1 - MW ** 2 / MZ ** 2
SW, CW = math.sqrt(SW2), MW / MZ
EE = math.sqrt(4 * math.pi * AEW)
WZ = 2.4952
MASS = {"e": 0.000511, "mu": 0.10566, "ta": 1.777, "u": 0.00255, "c": 1.27, "t": 172.0, "d": 0.00504, "s": 0.101,
        "b": 4.7, "ve": 0.0, "vm": 0.0, "vt": 0.0}
MH = 125.0
CABI = 0.227736
print(f"parameters: M_W = {MW:.10f}, s_W^2 = {SW2:.10f}, e = {EE:.10f}")

# %% [markdown]
# ## Dirac matrices, helicity spinors, polarization vectors
#
# Dirac representation.  u(p, h) = (sqrt(E+m) chi_h, 2h sqrt(E-m) chi_h), v(p, h) = (-2h sqrt(E-m) chi_-h, sqrt(E+m) chi_-h)
# with chi_h the helicity eigenstates along p (sum u ubar = pslash + m, sum v vbar = pslash - m, checked below).
# Massive vector: eps(k, +-1) = (-+ e1 - i e2)/sqrt2, eps(k, 0) = (|k|, E khat)/M with e1, e2 transverse; the sum over
# the three is -g + k k/M^2 (checked).

# %%
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
GAM = [np.block([[I2, Z2], [Z2, -I2]])] + [np.block([[Z2, s], [-s, Z2]]) for s in SIG]
G5 = np.block([[Z2, I2], [I2, Z2]])
PL, PR = (np.eye(4) - G5) / 2, (np.eye(4) + G5) / 2
METRIC = np.diag([1.0, -1.0, -1.0, -1.0])


def dot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def slash(p):
    return sum(METRIC[m, m] * p[m] * GAM[m] for m in range(4))


def chi(theta, phi, h):
    if h > 0:
        return np.array([math.cos(theta / 2), np.exp(1j * phi) * math.sin(theta / 2)], dtype=complex)
    return np.array([-np.exp(-1j * phi) * math.sin(theta / 2), math.cos(theta / 2)], dtype=complex)


def four(E, m, theta, phi):
    p = math.sqrt(max(E * E - m * m, 0.0))
    return np.array([E, p * math.sin(theta) * math.cos(phi), p * math.sin(theta) * math.sin(phi), p * math.cos(theta)])


def u_sp(E, m, theta, phi, h):
    c = chi(theta, phi, h)
    return np.concatenate([math.sqrt(E + m) * c, 2 * h * math.sqrt(max(E - m, 0.0)) * c])


def v_sp(E, m, theta, phi, h):
    c = chi(theta, phi, -h)
    return np.concatenate([-2 * h * math.sqrt(max(E - m, 0.0)) * c, math.sqrt(E + m) * c])


def bar(sp):
    return sp.conj() @ GAM[0]


def eps(E, M, theta, phi, lam):
    k = math.sqrt(E * E - M * M)
    e1 = np.array([0, math.cos(theta) * math.cos(phi), math.cos(theta) * math.sin(phi), -math.sin(theta)], dtype=complex)
    e2 = np.array([0, -math.sin(phi), math.cos(phi), 0], dtype=complex)
    if lam == 0:
        return np.array([k, E * math.sin(theta) * math.cos(phi), E * math.sin(theta) * math.sin(phi), E * math.cos(theta)],
                        dtype=complex) / M
    return (-lam * e1 - 1j * e2) / math.sqrt(2)


# checks of the spin and polarization sums
E0, m0, th0, ph0 = 3.0, 1.3, 0.7, 0.4
pp = four(E0, m0, th0, ph0)
su = sum(np.outer(u_sp(E0, m0, th0, ph0, h), bar(u_sp(E0, m0, th0, ph0, h))) for h in (0.5, -0.5))
sv = sum(np.outer(v_sp(E0, m0, th0, ph0, h), bar(v_sp(E0, m0, th0, ph0, h))) for h in (0.5, -0.5))
dev_u = np.abs(su - (slash(pp) + m0 * np.eye(4))).max()
dev_v = np.abs(sv - (slash(pp) - m0 * np.eye(4))).max()
kk = four(E0, m0, th0, ph0)
spol = sum(np.outer(eps(E0, m0, th0, ph0, l), eps(E0, m0, th0, ph0, l).conj()) for l in (1, 0, -1))
want = -np.linalg.inv(METRIC) + np.outer(kk, kk) / m0 ** 2       # upper indices: -g^{mu nu} + k^mu k^nu/M^2
dev_e = np.abs(spol - want).max()
trans = max(abs(dot(kk, eps(E0, m0, th0, ph0, l))) for l in (1, 0, -1))
print(f"(0) spin sums: |sum u ubar - (pslash+m)| = {dev_u:.1e}, |sum v vbar - (pslash-m)| = {dev_v:.1e};  "
      f"polarization sum - (-g + kk/M^2) = {dev_e:.1e}, max |k.eps| = {trans:.1e}")

# %% [markdown]
# ## e+ e- -> mu+ mu-
#
# i M = sum_V [vbar(p2) G_V u(p1)] (-i/(s - M_V^2 + i M_V Gamma_V)) [ubar(k1) G_V v(k2)] with G_A = i e Q gamma,
# G_Z = i e gamma (gL PL + gR PR), gL = (T3 - Q s^2)/(s c), gR = -Q s/c (Table 2 of the note).  Leptons massless.
# Eq. (11): dsigma/dcos = (pi alpha^2 Nc/(8 s)) [(|A_LL|^2+|A_RR|^2)(1+c)^2 + (|A_LR|^2+|A_RL|^2)(1-c)^2],
# A_ij = Qe Qf + g_i^e g_j^f chi(s).

# %%
def gLR(Q, T3):
    return (T3 - Q * SW2) / (SW * CW), -Q * SW / CW


def chi_z(s):
    return s / (s - MZ ** 2 + 1j * MZ * WZ)


def vertex_ff(kind, Q, T3):
    if kind == "A":
        return 1j * EE * Q * np.eye(4)
    gl, gr = gLR(Q, T3)
    return 1j * EE * (gl * PL + gr * PR)


def amp_eemumu(rs, theta, he, hp, hm, hpp, Qf=-1.0, T3f=-0.5):
    E = rs / 2
    p1, p2 = (E, 0.0, 0.0), (E, math.pi, 0.0)          # e- along +z, e+ along -z
    k1, k2 = (E, theta, 0.0), (E, math.pi - theta, math.pi)
    s = rs * rs
    ve = bar(v_sp(E, 0.0, p2[1], p2[2], hp))
    ue = u_sp(E, 0.0, p1[1], p1[2], he)
    um = bar(u_sp(E, 0.0, k1[1], k1[2], hm))
    vm = v_sp(E, 0.0, k2[1], k2[2], hpp)
    tot = 0j
    for V, den in (("A", s), ("Z", s - MZ ** 2 + 1j * MZ * WZ)):
        ge, gf = vertex_ff(V, -1.0, -0.5), vertex_ff(V, Qf, T3f)
        Je = np.array([ve @ GAM[m] @ ge @ ue for m in range(4)]) if V == "A" else \
            np.array([ve @ (GAM[m] @ (gLR(-1.0, -0.5)[0] * PL + gLR(-1.0, -0.5)[1] * PR)) @ ue for m in range(4)]) * 1j * EE
        Jf = np.array([um @ GAM[m] @ gf @ vm for m in range(4)]) if V == "A" else \
            np.array([um @ (GAM[m] @ (gLR(Qf, T3f)[0] * PL + gLR(Qf, T3f)[1] * PR)) @ vm for m in range(4)]) * 1j * EE
        tot += dot(Je, Jf) * (-1j / den)
    return tot          # = i M


def note_eemumu(rs, c, Qf=-1.0, T3f=-0.5, Nc=1):
    s = rs * rs
    ch = chi_z(s)
    A = {(i, j): (-1.0) * Qf + gLR(-1.0, -0.5)[i] * gLR(Qf, T3f)[j] * ch for i in (0, 1) for j in (0, 1)}
    same = abs(A[0, 0]) ** 2 + abs(A[1, 1]) ** 2
    opp = abs(A[0, 1]) ** 2 + abs(A[1, 0]) ** 2
    return math.pi * AEW ** 2 * Nc / (8 * s) * (same * (1 + c) ** 2 + opp * (1 - c) ** 2)


def num_eemumu(rs, c):
    th = math.acos(c)
    tot = sum(abs(amp_eemumu(rs, th, a, b, x, y)) ** 2 for a in (0.5, -0.5) for b in (0.5, -0.5)
              for x in (0.5, -0.5) for y in (0.5, -0.5))
    return tot / 4 / (32 * math.pi * rs * rs)          # dsigma/dcos(theta), massless


devs = []
for rs in (30.0, 91.1876, 200.0):
    for c in np.linspace(-0.95, 0.95, 9):
        devs.append(abs(num_eemumu(rs, c) / note_eemumu(rs, c) - 1))
print(f"(1) e+e- -> mu+mu-: explicit helicity sum vs Eq. (11), 27 points (sqrt s = 30, MZ, 200): max rel. dev. {max(devs):.1e}")
SIG_MUMU = {}
for rs in (30.0, 91.1876, 200.0):
    sig = quad(lambda c: note_eemumu(rs, c), -1, 1, epsabs=0, epsrel=1e-12)[0] * GEV2_TO_PB
    s = rs * rs
    A = {(i, j): (-1.0) * (-1.0) + gLR(-1.0, -0.5)[i] * gLR(-1.0, -0.5)[j] * chi_z(s) for i in (0, 1) for j in (0, 1)}
    tot = sum(abs(a) ** 2 for a in A.values())
    sig_cl = math.pi * AEW ** 2 / (3 * s) * tot * GEV2_TO_PB
    afb = 0.75 * (abs(A[0, 0]) ** 2 + abs(A[1, 1]) ** 2 - abs(A[0, 1]) ** 2 - abs(A[1, 0]) ** 2) / tot
    fwd = quad(lambda c: note_eemumu(rs, c), 0, 1, epsrel=1e-12)[0]
    bwd = quad(lambda c: note_eemumu(rs, c), -1, 0, epsrel=1e-12)[0]
    SIG_MUMU[rs] = sig_cl
    print(f"    sqrt s = {rs:8.4f}: sigma = {sig_cl:.8e} pb (integral of Eq. (11): rel. {sig / sig_cl - 1:.1e}), "
          f"A_FB = {afb:+.6f} (integral: {(fwd - bwd) / (fwd + bwd) - afb:.1e})")

# %% [markdown]
# ## e+ e- -> W+ W-
#
# W- (k1) and W+ (k2) outgoing; the field W creates W- (leg "W" of the vertices), Wbar creates W+.
# t channel: vbar(p2) [i C gamma^nu PL] i(p1slash - k1slash)/t [i C gamma^mu PL] u(p1) eps*_mu(k1) eps*_nu(k2), C = e/(sqrt2 s).
# s channel: J_rho = vbar(p2) G_V u(p1), propagator -i/(s - M_V^2 + i M_V Gamma_V), vertex A W Wbar: -i e Gamma^{rho mu nu}(q, -k1, -k2),
# W Wbar Z: -i e (c/s) Gamma^{mu nu rho}(-k1, -k2, q) (the same cyclic structure).

# %%
def gamma3(a, b, c, pa, pb, pc):
    """a_mu1 b_mu2 c_mu3 Gamma^{mu1 mu2 mu3}(pa, pb, pc) for vectors with upper indices."""
    return dot(a, b) * dot(pa - pb, c) + dot(b, c) * dot(pb - pc, a) + dot(c, a) * dot(pc - pa, b)


def amps_eeww(rs, theta, he, hp, l1, l2, wz=WZ):
    """i M of the three diagrams (t, photon, Z); wz: the Z width in the propagator."""
    E = rs / 2
    s = rs * rs
    p1v, p2v = four(E, 0.0, 0.0, 0.0), four(E, 0.0, math.pi, 0.0)
    k1v, k2v = four(E, MW, theta, 0.0), four(E, MW, math.pi - theta, math.pi)
    ue = u_sp(E, 0.0, 0.0, 0.0, he)
    ve = bar(v_sp(E, 0.0, math.pi, 0.0, hp))
    e1 = eps(E, MW, theta, 0.0, l1).conj()
    e2 = eps(E, MW, math.pi - theta, math.pi, l2).conj()
    C = EE / (math.sqrt(2) * SW)
    q = p1v - k1v
    prop = 1j * slash(q) / dot(q, q)
    m1 = slash(e1)
    m2 = slash(e2)
    Mt = ve @ (1j * C * m2 @ PL) @ prop @ (1j * C * m1 @ PL) @ ue
    qs = p1v + p2v
    JA = np.array([ve @ GAM[m] @ ue for m in range(4)]) * 1j * EE * (-1.0)
    gl, gr = gLR(-1.0, -0.5)
    JZ = np.array([ve @ GAM[m] @ (gl * PL + gr * PR) @ ue for m in range(4)]) * 1j * EE
    MA = (-1j / s) * (-1j * EE) * gamma3(JA, e1, e2, qs, -k1v, -k2v)
    MZz = (-1j / (s - MZ ** 2 + 1j * MZ * wz)) * (-1j * EE * CW / SW) * gamma3(e1, e2, JZ, -k1v, -k2v, qs)
    return Mt, MA, MZz


def sum_m2_eeww(rs, c, wz=WZ):
    """sum over the electron helicities and the W polarizations of |M|^2."""
    th = math.acos(c)
    tot = 0.0
    for he in (0.5, -0.5):
        for hp in (0.5, -0.5):
            for l1 in (1, 0, -1):
                for l2 in (1, 0, -1):
                    tot += abs(sum(amps_eeww(rs, th, he, hp, l1, l2, wz))) ** 2
    return tot


def dsig_eeww(rs, c):
    beta = math.sqrt(1 - 4 * MW ** 2 / (rs * rs))
    return beta / (32 * math.pi * rs * rs) * sum_m2_eeww(rs, c) / 4


# gauge cancellation: e-_L e+_R -> W-_0 W+_0 at cos(theta) = 0.3; each diagram / (s/(2 M_W^2))
print("(2) e+e- -> W+W-: longitudinal W pair, e- helicity -1/2, e+ +1/2, cos(theta) = 0.3; i M / (s/(2 M_W^2)):")
print("    sqrt s     t-channel nu        photon             Z                  sum              |sum|")
CANCEL = []
for rs in (200.0, 500.0, 1000.0, 3000.0, 10000.0, 30000.0):
    th = math.acos(0.3)
    Mt, MA, MZz = amps_eeww(rs, th, -0.5, 0.5, 0, 0)
    f = rs * rs / (2 * MW ** 2)
    CANCEL.append((rs, Mt / f, MA / f, MZz / f, (Mt + MA + MZz)))
    print(f"    {rs:7.0f}  {Mt / f:+.6f}  {MA / f:+.6f}  {MZz / f:+.6f}  {(Mt + MA + MZz) / f:+.2e}  {abs(Mt + MA + MZz):.6f}")
print("    e- helicity +1/2 (no nu exchange):")
for rs in (1000.0, 30000.0):
    th = math.acos(0.3)
    Mt, MA, MZz = amps_eeww(rs, th, 0.5, -0.5, 0, 0)
    f = rs * rs / (2 * MW ** 2)
    print(f"    {rs:7.0f}  {Mt / f:+.6f}  {MA / f:+.6f}  {MZz / f:+.6f}  {(Mt + MA + MZz) / f:+.2e}  {abs(Mt + MA + MZz):.6f}")
# the predicted leading coefficients (see the note): with i M_V ~ -i e^2 x_V (s/(2MW^2)) sin(theta) for the three diagrams
gl, gr = gLR(-1.0, -0.5)
pred = {"t": 1 / (2 * SW2), "A": -1.0, "Z": gl * CW / SW}
print(f"    hand: t : photon : Z = 1/(2 s^2) : Q_e : g_L c/s = {pred['t']:+.6f} : {pred['A']:+.6f} : {pred['Z']:+.6f} "
      f"(sum {sum(pred.values()):+.1e});  e- R: Q_e + g_R c/s = {-1.0 + gr * CW / SW:+.1e}")
rs, Mt, MA, MZz, _ = CANCEL[-1]
ratio = [x / MA * pred["A"] for x in (Mt, MA, MZz)]
print(f"    numerical ratios at sqrt s = 30 TeV, normalized to the photon: {ratio[0].real:+.6f} : {ratio[1].real:+.6f} : {ratio[2].real:+.6f}")

# FeynCalc (tree_feyncalc.wl, section (e)): the traces with -g + k k/M_W^2, Gamma_Z = 0
fcfile = os.path.join(os.path.dirname(os.path.abspath(__file__)) if not INTERACTIVE else ".", "results", "tree_feyncalc_ww.csv")
if os.path.exists(fcfile):
    rows = [list(map(float, r)) for r in list(csv.reader(open(fcfile)))[1:] if r]
    devs = [abs(sum_m2_eeww(rs, c, 0.0) / m2 - 1) for rs, c, m2 in rows]
    print(f"    FeynCalc traces vs explicit helicity sum (Gamma_Z = 0), {len(rows)} points: max rel. dev. {max(devs):.1e}")
    for (rs, c, m2), d in zip(rows, devs):
        print(f"      sqrt s = {rs:6.0f}, cos = {c:+.1f}: sum|M|^2 FeynCalc {m2:.12e}, here {sum_m2_eeww(rs, c, 0.0):.12e}")
else:
    print(f"    no FeynCalc results at {fcfile}")

SIG_WW = {}
for rs in (200.0, 500.0, 1000.0):
    sig = quad(lambda c: dsig_eeww(rs, c), -1, 1, epsabs=0, epsrel=1e-10, limit=200)[0] * GEV2_TO_PB
    SIG_WW[rs] = sig
    print(f"    sigma(e+e- -> W+W-) at sqrt s = {rs:6.0f}: {sig:.8e} pb")

# %% [markdown]
# ## Two-body widths and the muon width
#
# V -> f1 fbar2 (vertex i gamma (v - a gamma5)): Gamma = Nc |p| /(6 pi M^2) [ (v^2+a^2)(M^2 - (m1^2+m2^2)/2 - (m1^2-m2^2)^2/(2M^2))
#   + 3 (v^2 - a^2) m1 m2 ],  which gives Eq. (9) for m1 = m2 and the W forms; H -> f fbar and t -> b W as in Eq. (10)
#   and its massive-b form Gamma = (G_F m_t^3/(8 sqrt2 pi)) lambda^{1/2}(1, rb, rw) [(1-rb)^2 + rw (1+rb) - 2 rw^2].

# %%
def pcm(M, m1, m2):
    return math.sqrt(max((M * M - (m1 + m2) ** 2) * (M * M - (m1 - m2) ** 2), 0.0)) / (2 * M)


def gam_v(M, m1, m2, v, a, Nc):
    p = pcm(M, m1, m2)
    return Nc * p / (6 * math.pi * M * M) * ((v * v + a * a) * (M * M - (m1 * m1 + m2 * m2) / 2 - (m1 * m1 - m2 * m2) ** 2 / (2 * M * M))
                                             + 3 * (v * v - a * a) * m1 * m2)


def gam_z(f, Q, T3, Nc):
    m = MASS[f]
    beta = math.sqrt(1 - 4 * m * m / MZ ** 2)
    gv, ga = (T3 - 2 * Q * SW2) / (2 * SW * CW), T3 / (2 * SW * CW)
    mu = m * m / MZ ** 2
    return Nc * AEW * MZ / 3 * beta * (gv * gv * (1 + 2 * mu) + ga * ga * beta * beta)


def gam_w(f1, f2, Nc, V2=1.0):
    C = EE / (2 * math.sqrt(2) * SW)
    return V2 * gam_v(MW, MASS[f1], MASS[f2], C, C, Nc)


def gam_h(f, Nc):
    m = MASS[f]
    return Nc * AEW * MH * m * m / (8 * SW2 * MW ** 2) * (1 - 4 * m * m / MH ** 2) ** 1.5


def gam_t():
    mt, mb = MASS["t"], MASS["b"]
    rb, rw = (mb / mt) ** 2, (MW / mt) ** 2
    lam = (1 - rb - rw) ** 2 - 4 * rb * rw
    gfm = math.pi * AEW / (math.sqrt(2) * SW2 * MW ** 2)          # = G_F of the model
    return gfm * mt ** 3 / (8 * math.sqrt(2) * math.pi) * math.sqrt(lam) * ((1 - rb) ** 2 + rw * (1 + rb) - 2 * rw * rw)


ZCH = {"ve": (0, 0.5, 1), "vm": (0, 0.5, 1), "vt": (0, 0.5, 1), "e": (-1, -0.5, 1), "mu": (-1, -0.5, 1), "ta": (-1, -0.5, 1),
       "u": (2 / 3, 0.5, 3), "c": (2 / 3, 0.5, 3), "d": (-1 / 3, -0.5, 3), "s": (-1 / 3, -0.5, 3), "b": (-1 / 3, -0.5, 3)}
WIDTHS = {}
for f, (Q, T3, Nc) in ZCH.items():
    WIDTHS[("Z", f)] = gam_z(f, Q, T3, Nc)
    m = MASS[f]
    v, a = EE * (T3 - 2 * Q * SW2) / (2 * SW * CW), EE * T3 / (2 * SW * CW)
    assert abs(gam_v(MZ, m, m, v, a, Nc) / WIDTHS[("Z", f)] - 1) < 1e-12
c2, s2 = math.cos(CABI) ** 2, math.sin(CABI) ** 2
for (f1, f2, Nc, V2) in (("ve", "e", 1, 1), ("vm", "mu", 1, 1), ("vt", "ta", 1, 1), ("u", "d", 3, c2), ("u", "s", 3, s2),
                         ("c", "d", 3, s2), ("c", "s", 3, c2)):
    WIDTHS[("W", f1 + f2)] = gam_w(f1, f2, Nc, V2)
for f in ("b", "ta", "c", "mu", "s", "e", "d", "u"):
    WIDTHS[("H", f)] = gam_h(f, 3 if f in ("b", "c", "s", "d", "u") else 1)
WIDTHS[("t", "bW")] = gam_t()
print(f"(3) widths (GeV): Z -> nu nubar {WIDTHS[('Z', 've')]:.8e} (= G_F MZ^3/(12 sqrt2 pi) with the model's G_F: "
      f"{(math.pi * AEW / (math.sqrt(2) * SW2 * MW ** 2)) * MZ ** 3 / (12 * math.sqrt(2) * math.pi) / WIDTHS[('Z', 've')] - 1:+.1e}), "
      f"W -> e nu {WIDTHS[('W', 've' + 'e')]:.8e}, H -> b bbar {WIDTHS[('H', 'b')]:.8e}, t -> b W {WIDTHS[('t', 'bW')]:.8e}")
print(f"    totals: Gamma_Z = {sum(v for k, v in WIDTHS.items() if k[0] == 'Z'):.8e}, Gamma_W = {sum(v for k, v in WIDTHS.items() if k[0] == 'W'):.8e}")

# muon width: Gamma = 16 G_F^2/(256 pi^3 m^3) int ds (m^2 - s)^2 (s - me^2)^2/s  (Dalitz plot, Fermi limit)
mmu, me = MASS["mu"], MASS["e"]
gfm = math.pi * AEW / (math.sqrt(2) * SW2 * MW ** 2)
gmu_num = 16 * gfm ** 2 / (256 * math.pi ** 3 * mmu ** 3) * quad(lambda s: (mmu ** 2 - s) ** 2 * (s - me ** 2) ** 2 / s,
                                                                 me ** 2, mmu ** 2, epsrel=1e-13)[0]
x = (me / mmu) ** 2
gmu_x = gfm ** 2 * mmu ** 5 / (192 * math.pi ** 3) * (1 - 8 * x + 8 * x ** 3 - x ** 4 - 12 * x * x * math.log(x))
gmu0 = gfm ** 2 * mmu ** 5 / (192 * math.pi ** 3)
print(f"    muon: Dalitz integral {gmu_num:.10e} GeV, closed form with m_e {gmu_x:.10e} (rel. {gmu_num / gmu_x - 1:.1e}), "
      f"Eq. (8) (m_e = 0) {gmu0:.10e};  with the W propagator x (1 + 3 m_mu^2/(5 M_W^2)): {gmu_x * (1 + 0.6 * mmu ** 2 / MW ** 2):.10e}")

# %% [markdown]
# ## Comparison with MadGraph (tree_mg5.mg5)

# %%
logfile = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)) if not INTERACTIVE else ".",
                                                              "work", "tree_mg5.log")
def banner_xs(rundir, n):
    """the cross section with all digits from the run banner (the log prints four digits)"""
    f = os.path.join(os.path.dirname(logfile), rundir, "Events", f"run_{n:02d}", f"run_{n:02d}_tag_1_banner.txt")
    m = re.search(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)", open(f).read()) if os.path.exists(f) else None
    return float(m.group(1)) if m else None


if os.path.exists(logfile):
    text = open(logfile).read()
    xs = [float(a) for a in re.findall(r"Cross-section :\s+([0-9.eE+-]+)", text)]
    er = [float(a) for a in re.findall(r"Cross-section :\s+[0-9.eE+-]+ \+- ([0-9.eE+-]+)", text)]
    print(f"(4) MadGraph cross sections ({len(xs)} found; values from the run banners, errors from the log)")
    labels = [("mumu", 30.0, 1), ("mumu", 91.1876, 2), ("mumu", 200.0, 3), ("ww", 200.0, 1), ("ww", 500.0, 2), ("ww", 1000.0, 3)]
    for (lab, rs, n), x0, e0 in zip(labels, xs, er):
        x0 = banner_xs("mg5_eemumu" if lab == "mumu" else "mg5_eeww", n) or x0
        ref = SIG_MUMU[rs] if lab == "mumu" else SIG_WW[rs]
        print(f"    {lab:5s} sqrt s = {rs:8.4f}: MadGraph {x0:.7e} +- {e0:.1e} pb, here {ref:.6e} pb, (MG - here)/err = {(x0 - ref) / e0:+.2f}")
    wfile = os.path.join(os.path.dirname(logfile), "widths_card.dat")
    if os.path.exists(wfile):
        card = open(wfile).read()
        print("    MadGraph compute_widths (FeynRules formulas; partial widths from the comments of widths_card.dat):")
        pdg = {"ve": 12, "vm": 14, "vt": 16, "e": 11, "mu": 13, "ta": 15, "u": 2, "c": 4, "d": 1, "s": 3, "b": 5, "t": 6}
        blocks = re.findall(r"DECAY\s+(-?\d+)\s+([0-9.eE+-]+)(.*?)(?=DECAY|\Z)", card, re.S)
        part = {int(p): [(tuple(sorted(abs(int(i)) for i in ids.split())), float(w)) for ids, w in
                         re.findall(r"^\s*[0-9.eE+-]+\s+2\s+([-\d ]+?)\s*#\s*([0-9.eE+-]+)\s*$", body, re.M)]
                for p, _, body in blocks}
        worst = 0.0
        for (P, f), val in sorted(WIDTHS.items()):
            pid = {"Z": 23, "W": 24, "H": 25, "t": 6}[P]
            if P == "W":
                a, b = (f[:2], f[2:]) if f[:2] in pdg else (f[0], f[1:])
                ids = tuple(sorted((pdg[a], pdg[b])))
            elif P == "t":
                ids = (5, 24)
            else:
                ids = (pdg[f], pdg[f])
            mg = [w for i, w in part.get(pid, []) if i == ids]
            if mg:
                worst = max(worst, abs(mg[0] / val - 1))
                print(f"      {P} -> {f:5s}: MadGraph {mg[0]:.12e}  here {val:.12e}  rel. {mg[0] / val - 1:+.1e}")
        print(f"    largest relative difference of the partial widths: {worst:.1e}")
    mu = re.findall(r"Width :\s+([0-9.eE+-]+)\s+\+-\s+([0-9.eE+-]+)\s+GeV", text)
    if mu:
        w, e = banner_xs("mg5_mudecay", 1) or float(mu[-1][0]), float(mu[-1][1])
        ref = gmu_x * (1 + 0.6 * mmu ** 2 / MW ** 2)
        print(f"    muon width: MadGraph {w:.6e} +- {e:.1e} GeV, here {ref:.6e} GeV, (MG - here)/err = {(w - ref) / e:+.2f}")
else:
    print(f"(4) no MadGraph log at {logfile}")
