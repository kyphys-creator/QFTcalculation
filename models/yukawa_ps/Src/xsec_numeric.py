# %% [markdown]
# # Step (6): total cross section of phi phi scattering to next-to-leading order (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, Eq. (sigmatot) of step (6).  With lambda ~ y^2, the total cross section of phi phi -> X
# to O(y^6) (m = mu = 1, M = 0.7, y = lambda = 1; masses on shell, couplings MS-bar at mu = m) is
#     sigma_tot = sigma_A0 + sigma_Bbar0           (tree level, O(y^4): phi phi -> phi phi, phi phi -> psi psibar)
#               + sigma_A1 + sigma_Bbar1           (one-loop interference with the S-matrix elements, O(y^6))
#               + sigma_3                          (phi phi -> phi psi psibar, O(y^6); phi phi -> phi phi phi vanishes by parity)
# - sigma_A0 = lambda^2/(32 pi s);  sigma_A1 = (1/2) 1/(64 pi^2 s) int dOmega 2 (-lambda) Re M1_phys,A,
#   (4 pi)^2 M1_phys,A = (4 pi)^2 M1_A + 4 lambda y^2 [B0^MM + m^2 B0^MM'](m^2)            (Eqs. (13), (16));
# - phi phi -> psi psibar: by time reversal the spin-summed |M|^2 at given (s, t, u) equals that of psi psibar -> phi phi
#   (t = (p_psi - k_phi)^2), so sum|M0|^2 is Eq. (11) and sum 2 Re(M0* M1) = 2 b0/(4 pi)^2 [2 M (t - u) Re a_phys
#   + 2 ((t-M^2)(u-M^2) - m^4) Re b_phys] with a_phys, b_phys of Eq. (20); sigma = 1/(64 pi^2 s) (p_psi/k_phi) int dOmega;
#   the time-reversal step is checked with MadLoop for phi phi -> psi psibar directly (work/ml_OS_Bbar);
# - sigma_3: tree amplitude M = ubar(q1) G v(q2), G = i [y^3 sum_(6 orderings) g5 (q1 + a1 + M) g5 (q1 + a1 + a2 + M) g5 / (D1 D2)
#   - lambda y g5/((q1 + q2)^2 - m^2)], a_i in {k, -p1, -p2} the outgoing momenta of the phi's along the line,
#   D1 = (q1 + a1)^2 - M^2, D2 = (q1 + a1 + a2)^2 - M^2; sum|M|^2 = tr[(q1 + M) G (q2 - M) Gbar]; Gauss-Legendre quadrature over
#   three-body phase space (two channels split by the collinear fermion propagators; cross-checked with a
#   single-grid quadrature and an independent Monte Carlo).
# The one-loop pieces are also computed from MadLoop at the same nodes (work/ml_OS_A, work/ml_OS_Bbar), the 2 -> 3 spin sum
# is compared with MadGraph's standalone matrix element at nodes of the grid (work/sa_xsec3), and the tree-level
# phi phi -> psi psibar and phi phi -> phi psi psibar cross sections are compared with MadGraph (work/xsec_mg5.log).
# Writes results/xsec.csv and ../figs/xsec_d4.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python xsec_numeric.py` (from Src/; run_xsec_check.sh builds the helpers).
# Interactive: "Run Cell" in VS Code.

# %%
import csv
import itertools
import math
import os
import re
import subprocess
import sys

import mpmath as mp
import numpy as np
from scipy.spatial.transform import Rotation

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
MPHI, MPSI, Y, LAM = 1.0, 0.7, 1.0, 1.0
m2, bm2 = MPHI ** 2, MPSI ** 2
K16 = (4 * math.pi) ** 2
GEV2_TO_PB = 0.3893794e9
mp.mp.dps = 30
SQRTS_TABLE = (2.5, 3.0, 5.0, 10.0, 20.0)
SQRTS_SCAN = (2.02, 2.05, 2.1, 2.15, 2.2, 2.3, 2.35, 2.42, 2.45, 2.5, 2.6, 2.75, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.5, 10.0, 12.0,
              14.0, 17.0, 20.0)
NGL = 24                                    # Gauss-Legendre nodes on each half of cos(theta) for the 2 -> 2 integrals

# %% [markdown]
# ## Two-point functions at the special points (as in madloop_numeric.py)

# %%
def dx(x, p2, ma2, mb2):
    return x * mb2 + (1 - x) * ma2 - x * (1 - x) * p2


def b0(p2, ma2, mb2):
    return float(-mp.quad(lambda x: mp.log(dx(x, p2, ma2, mb2)), [0, 1]))


def b1(p2, ma2, mb2):
    return float(mp.quad(lambda x: x * mp.log(dx(x, p2, ma2, mb2)), [0, 1]))


def b0p(p2, ma2, mb2):
    return float(mp.quad(lambda x: x * (1 - x) / dx(x, p2, ma2, mb2), [0, 1]))


def b1p(p2, ma2, mb2):
    return float(-mp.quad(lambda x: x * x * (1 - x) / dx(x, p2, ma2, mb2), [0, 1]))


dRpsi = Y ** 2 * (b1(bm2, bm2, m2) + 2 * bm2 * (b0p(bm2, bm2, m2) + b1p(bm2, bm2, m2)))   # (4 pi)^2 (R_psi - 1)
dRphi = -2 * Y ** 2 * (b0(m2, bm2, bm2) + m2 * b0p(m2, bm2, bm2))                         # (4 pi)^2 (R_phi - 1)
dMpsi = Y ** 2 * (b0(bm2, bm2, m2) + b1(bm2, bm2, m2))                                    # (4 pi)^2 (M_p - M)/M
dRpsi, dRphi, dMpsi                                                                         # inspect

# %% [markdown]
# ## One-loop amplitudes at the Gauss-Legendre nodes (COLLIER), and the 2 -> 2 cross sections

# %%
def nodes_2to2(rs, n):
    """cos(theta) nodes and weights for phi phi -> psi psibar at sqrt(s) = rs: on each half [0, 1], [-1, 0], c = +-(A - e^u)
    with n Gauss-Legendre nodes in u, A = (2 E^2 - m^2)/(2 p k), so that the t- and u-channel propagators
    1/|t - M^2| = 1/(2 p k (A - c)), 1/|u - M^2| = 1/(2 p k (A + c)) are flat (E = sqrt(s)/2, p = |p_psi|, k = |k_phi|)."""
    e = rs / 2
    p, k = math.sqrt(e * e - bm2), math.sqrt(e * e - m2)
    a = (2 * e * e - m2) / (2 * p * k)
    xg, wg = np.polynomial.legendre.leggauss(n)
    ua, ub = math.log(a - 1), math.log(a)
    u = ua + (ub - ua) * (xg + 1) / 2
    c, w = a - np.exp(u), np.exp(u) * (ub - ua) / 2 * wg
    return np.concatenate([c, -c]), np.concatenate([w, w])


def amplitudes_at_nodes(sqrts_list, n):
    nodes = os.path.join(HERE, "work", "xsec_nodes.txt")
    outp = os.path.join(HERE, "work", "xsec_amp_nodes.csv")
    with open(nodes, "w") as fh:
        for rs in sqrts_list:
            for c in nodes_2to2(rs, n)[0]:
                fh.write("%.17e %.17e\n" % (rs, c))
    subprocess.run([os.path.join(HERE, "work", "xsec_collier"), nodes, outp], cwd=os.path.join(HERE, "work"),
                   check=True, capture_output=True)
    table = {}
    with open(outp) as fh:
        for r in csv.DictReader(fh):
            table.setdefault(round(float(r["sqrts"]), 9), []).append(
                {k: float(r[k]) for k in ("costheta", "s", "t_B", "t_A", "re_a", "re_b", "re_mA")})
    return table


def kin_B(s, c):
    e = math.sqrt(s) / 2
    p, k = math.sqrt(e * e - bm2), math.sqrt(e * e - m2)
    t = bm2 + m2 - 2 * (e * e - p * k * c)
    return p, k, t, 2 * bm2 + 2 * m2 - s - t


def sum_tree_B(t, u):
    X, W = t - bm2, u - bm2
    return 2 * Y ** 4 * (X * W - m2 ** 2) * (t - u) ** 2 / (X * X * W * W)


def interference_B(t, u, a, b):
    """sum_spins 2 Re(M0* M1) with (4 pi)^2 M1 = a vbar u + b vbar k1 u (a, b real parts)."""
    X, W = t - bm2, u - bm2
    b0t = Y ** 2 * (1 / X - 1 / W)
    return 2 * b0t / K16 * (2 * MPSI * (t - u) * a + 2 * (X * W - m2 ** 2) * b)


def phys_B(t, u, a, b):
    """a_phys, b_phys of Eq. (20) at mu = m."""
    X, W = t - bm2, u - bm2
    b0t = Y ** 2 * (1 / X - 1 / W)
    return (a - Y ** 2 * MPSI * dMpsi * (1 / X + 1 / W),
            b + (dRpsi + dRphi) * b0t - 2 * bm2 * Y ** 2 * dMpsi * (1 / X ** 2 - 1 / W ** 2))


B0PHI_COMB = b0(m2, bm2, bm2) + m2 * b0p(m2, bm2, bm2)       # [B0^MM + m^2 B0^MM'](m^2), the residue of phi


def sigma_2to2(rs, rows):
    s = rs * rs
    p, k, _, _ = kin_B(s, 0.0)
    pA = math.sqrt(s / 4 - m2)
    sA0 = LAM ** 2 / (32 * math.pi * s)
    tree_B, loop_B, loop_A = 0.0, 0.0, 0.0
    for w, r in zip(nodes_2to2(rs, NGL)[1], rows):
        _, _, t, u = kin_B(s, r["costheta"])
        tree_B += w * sum_tree_B(t, u)
        ap, bp = phys_B(t, u, r["re_a"], r["re_b"])
        loop_B += w * interference_B(t, u, ap, bp)
        loop_A += w * (r["re_mA"] + 4 * LAM * Y ** 2 * B0PHI_COMB) / K16
    f_B = 2 * math.pi * p / (64 * math.pi ** 2 * s * k)            # phi phi -> psi psibar: p_psi / k_phi (here p = |p_psi|, k = |k_phi|)
    sB0 = f_B * tree_B
    sB1 = f_B * loop_B
    sA1 = 0.5 * 2 * math.pi / (64 * math.pi ** 2 * s) * 2 * (-LAM) * loop_A
    return sA0, sB0, sA1, sB1


amp_tab = amplitudes_at_nodes(sorted(set(SQRTS_TABLE) | set(SQRTS_SCAN)), NGL)
two2two = {rs: sigma_2to2(rs, amp_tab[round(rs, 9)]) for rs in sorted(set(SQRTS_TABLE) | set(SQRTS_SCAN))}
amp_chk = amplitudes_at_nodes(SQRTS_TABLE, 2 * NGL)       # convergence: twice the nodes
NGL *= 2
dev = max(abs(a - b) / abs(b) for rs in SQRTS_TABLE for a, b in zip(two2two[rs], sigma_2to2(rs, amp_chk[round(rs, 9)])))
NGL //= 2
amplitudes_at_nodes(sorted(set(SQRTS_TABLE) | set(SQRTS_SCAN)), NGL)
print(f"2 -> 2 cross sections, {2 * NGL} vs {4 * NGL} nodes in cos(theta): max rel. dev. {dev:.1e}")
two2two[5.0]          # inspect: (sigma_A0, sigma_Bbar0, sigma_A1, sigma_Bbar1) in GeV^-2 at sqrt(s) = 5

# %% [markdown]
# ## The one-loop pieces from MadLoop at the same nodes (OS counterterms, mu_R = m)
#
# MadLoop's finite part: phi phi -> phi phi: (1/2) 2 Re(M0* M1) (identical final particles); phi phi -> psi psibar:
# sum_spins 2 Re(M0* M1) (no initial spin, distinct final particles).  So sigma_A1 = 1/(64 pi^2 s) int dOmega finite and
# sigma_Bbar1 = 1/(64 pi^2 s) (p_psi/k_phi) int dOmega finite.  Checks the time-reversal step and the integration.

# %%
def show_ps(paths):
    """show MadGraph's PostScript diagrams (interactive only): Ghostscript -> PNG -> IPython.display."""
    import shutil
    import tempfile
    from IPython.display import Image, display
    gs = shutil.which("gs") or "/opt/homebrew/bin/gs"
    tmp = tempfile.mkdtemp()
    for i, ps in enumerate(paths):
        subprocess.run([gs, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                        "-sOutputFile=" + os.path.join(tmp, f"d{i}_%02d.png"), ps], check=True)
    for png in sorted(os.listdir(tmp)):
        display(Image(filename=os.path.join(tmp, png)))


if INTERACTIVE:          # the diagrams of phi phi -> psi psibar that MadLoop computes, before the first run
    with open(os.path.join(HERE, "work", "ml_OS_Bbar.log")) as fh:
        print("ml_OS_Bbar:", next(line.strip() for line in fh if "Contributing diagrams" in line))
    base = os.path.join(HERE, "work", "ml_OS_Bbar", "SubProcesses")
    dML = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    show_ps([os.path.join(dML, "born_matrix.ps"), os.path.join(dML, "loop_matrix.ps")])

# %%
def madloop_dir(name):
    base = os.path.join(HERE, "work", name, "SubProcesses")
    return os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))


def madloop_finite(name, mom):
    d = madloop_dir(name)
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % tuple(m) for m in mom)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("1.0\n")
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element finite\s*=\s*(\S+)", out).group(1)), \
        float(re.search(r"Matrix element born\s*=\s*(\S+)", out).group(1))


def sigma_loop_madloop(rs):
    s = rs * rs
    e = rs / 2
    pA = math.sqrt(e * e - m2)
    ppsi = math.sqrt(e * e - bm2)
    accA = accB = accBorn = 0.0
    for c, w in zip(*nodes_2to2(rs, NGL)):
        st = math.sqrt(1 - c * c)
        momA = [(e, 0, 0, pA), (e, 0, 0, -pA), (e, pA * st, 0, pA * c), (e, -pA * st, 0, -pA * c)]
        momB = [(e, 0, 0, pA), (e, 0, 0, -pA), (e, ppsi * st, 0, ppsi * c), (e, -ppsi * st, 0, -ppsi * c)]
        fA, _ = madloop_finite("ml_OS_A", momA)
        fB, bB = madloop_finite("ml_OS_Bbar", momB)
        accA += w * fA
        accB += w * fB
        accBorn += w * bB
    sA1 = 2 * math.pi / (64 * math.pi ** 2 * s) * accA
    f_B = 2 * math.pi * ppsi / (64 * math.pi ** 2 * s * pA)
    return sA1, f_B * accB, f_B * accBorn


ml_loops = {rs: sigma_loop_madloop(rs) for rs in SQRTS_TABLE}
for rs in SQRTS_TABLE:
    sA0, sB0, sA1, sB1 = two2two[rs]
    mA1, mB1, mB0 = ml_loops[rs]
    print(f"sqrt(s) = {rs:5.2f}:  sigma_A1 rel. dev. (MadLoop vs note) {abs(mA1 - sA1) / abs(sA1):.1e},  sigma_Bbar1 {abs(mB1 - sB1) / abs(sB1):.1e},"
          f"  sigma_Bbar0 {abs(mB0 - sB0) / sB0:.1e}")

# %% [markdown]
# ## phi phi -> phi psi psibar: amplitude, spin sum and three-body phase space

# %%
if INTERACTIVE:          # the seven tree diagrams of phi phi -> phi psi psibar (MadGraph standalone output), before the evaluation
    base = os.path.join(HERE, "work", "sa_xsec3", "SubProcesses")
    show_ps([os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P1_")), "matrix.ps")])

# %%
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
G0 = np.block([[I2, Z2], [Z2, -I2]])
GI = [np.block([[Z2, s_], [-s_, Z2]]) for s_ in SIG]
G5 = 1j * G0 @ GI[0] @ GI[1] @ GI[2]
ONE = np.eye(4, dtype=complex)
GAM = np.array([G0, -GI[0], -GI[1], -GI[2]])          # gamma_mu with lower index: slash(p) = p^mu gamma_mu


def vslash(q):
    return np.einsum("nm,mij->nij", q, GAM)


def vmdot(a, b):
    return a[..., 0] * b[..., 0] - a[..., 1] * b[..., 1] - a[..., 2] * b[..., 2] - a[..., 3] * b[..., 3]


def sum_m2_23(p1, p2, k, q1, q2, terms=("y3", "lam")):
    """sum over the psi, psibar spins of |M(phi(p1) phi(p2) -> phi(k) psi(q1) psibar(q2))|^2 on arrays of momenta (N, 4);
    terms selects the six y^3 diagrams ("y3") and/or the lambda y diagram ("lam")."""
    n = len(k)
    one = np.broadcast_to(ONE, (n, 4, 4))
    g5 = np.broadcast_to(G5, (n, 4, 4))
    gam = np.zeros((n, 4, 4), dtype=complex)
    outs = (k, -np.broadcast_to(p1, k.shape), -np.broadcast_to(p2, k.shape))
    sq1 = vslash(q1)
    for a1, a2, _ in itertools.permutations(outs) if "y3" in terms else ():
        r1, r2 = q1 + a1, q1 + a1 + a2
        d1, d2 = vmdot(r1, r1) - bm2, vmdot(r2, r2) - bm2
        num = g5 @ (vslash(r1) + MPSI * one) @ g5 @ (vslash(r2) + MPSI * one) @ g5
        gam += Y ** 3 * num / (d1 * d2)[:, None, None]
    if "lam" in terms:
        pp = q1 + q2
        gam -= LAM * Y * g5 / (vmdot(pp, pp) - m2)[:, None, None]
    gam = 1j * gam
    gbar = np.conj(np.transpose(gam, (0, 2, 1)))
    gbar = G0[None] @ gbar @ G0[None]
    mat = (sq1 + MPSI * one) @ gam @ (vslash(q2) - MPSI * one) @ gbar
    return np.real(np.trace(mat, axis1=1, axis2=2))


def madgraph_me(mom):
    """sum |M|^2 of MadGraph's standalone tree output (work/sa_xsec3) at one phase-space point."""
    base = os.path.join(HERE, "work", "sa_xsec3", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P1_")))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % tuple(m) for m in mom)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element =\s*(\S+)", out).group(1))


def boost(v, beta):
    """boost four-vectors v (N, 4) by velocities beta (N, 3)."""
    b2 = np.sum(beta ** 2, axis=1)
    g = 1 / np.sqrt(1 - b2)
    bp = np.sum(beta * v[:, 1:], axis=1)
    g2 = np.where(b2 > 0, (g - 1) / np.where(b2 > 0, b2, 1), 0.0)
    e = g * (v[:, 0] + bp)
    vec = v[:, 1:] + (g2 * bp)[:, None] * beta + (g * v[:, 0])[:, None] * beta
    return np.concatenate([e[:, None], vec], axis=1)


def two_body(msq_parent, ma, mb):
    return np.sqrt(np.maximum((msq_parent - (ma + mb) ** 2) * (msq_parent - (ma - mb) ** 2), 0)) / (2 * np.sqrt(msq_parent))


def grid_2to3(rs, n, single):
    """Gauss-Legendre nodes of the three-body phase space and their weights, flux included, so that
    sigma = sum_i weight_i sum|M|^2(p1, p2, k_i, q1_i, q2_i).  single = "phi", "psi" or "psibar" is the particle whose
    direction is a variable; the other two form the pair.  Variables: pair mass^2 msq = a + (b - a)(1 - cos v)/2 (v in
    [0, pi], which removes the square-root endpoints), cos(theta) of the single particle, cos(theta*) and phi* of the pair's
    decay in its rest frame (axes parallel to the CM axes; phi* evenly spaced).  The azimuth of the single particle is
    integrated analytically.  dPhi_3 = [p dOmega/(16 pi^2 sqrt(s))] [dmsq/(2 pi)] [p* dOmega*/(16 pi^2 sqrt(msq))].
    For a single fermion, cos(theta) on each half [0, 1], [-1, 0] is mapped by c = +-(A - e^u), A = (2 E E_q - m^2)/(2 p q),
    with n nodes in u: this makes the propagator 1/|(q - p_1)^2 - M^2| = 1/(2 p q (A - c)) flat (backward: p_2)."""
    s = rs * rs
    e = rs / 2
    pA = math.sqrt(e * e - m2)
    p1, p2 = np.array([e, 0, 0, pA]), np.array([e, 0, 0, -pA])
    m_single, ma, mb = (MPHI, MPSI, MPSI) if single == "phi" else (MPSI, MPHI, MPSI)
    lo, hi = (ma + mb) ** 2, (rs - m_single) ** 2
    xg, wg = np.polynomial.legendre.leggauss(n)
    v, wv = (xg + 1) * math.pi / 2, wg * math.pi / 2
    msq1 = lo + (hi - lo) * (1 - np.cos(v)) / 2
    es1 = (s + m_single ** 2 - msq1) / (2 * rs)
    ps1 = np.sqrt(np.maximum(es1 ** 2 - m_single ** 2, 0))
    if single == "phi":                                    # plain Gauss-Legendre in cos(theta)
        CT1 = np.broadcast_to(xg, (n, n))
        WC1 = np.broadcast_to(wg, (n, n))
    else:
        A = (2 * e * es1 - m2) / (2 * pA * ps1)            # > 1
        ua, ub = np.log(A - 1), np.log(A)
        u = ua[:, None] + (ub - ua)[:, None] * (xg[None, :] + 1) / 2
        c = A[:, None] - np.exp(u)
        wc = np.exp(u) * (ub - ua)[:, None] / 2 * wg[None, :]
        CT1, WC1 = np.concatenate([c, -c], axis=1), np.concatenate([wc, wc], axis=1)
    nc = CT1.shape[1]
    phis = 2 * math.pi * (np.arange(n) + 0.5) / n
    iv, ic, ics, iph = (z.reshape(-1) for z in np.meshgrid(np.arange(n), np.arange(nc), np.arange(n), np.arange(n), indexing="ij"))
    CT, CS, PH = CT1[iv, ic], xg[ics], phis[iph]
    W = wv[iv] * WC1[iv, ic] * wg[ics] * (2 * math.pi / n)
    msq, es, ps = msq1[iv], es1[iv], ps1[iv]
    jac = (hi - lo) / 2 * np.sin(v[iv])
    st = np.sqrt(np.maximum(1 - CT ** 2, 0))
    single_p = np.stack([es, ps * st, 0 * ps, ps * CT], axis=1)
    pair = np.stack([rs - es, -ps * st, 0 * ps, -ps * CT], axis=1)
    pst = two_body(msq, ma, mb)
    ea, eb = np.sqrt(pst ** 2 + ma ** 2), np.sqrt(pst ** 2 + mb ** 2)
    ss = np.sqrt(1 - CS ** 2)
    nvec = np.stack([ss * np.cos(PH), ss * np.sin(PH), CS], axis=1)
    beta = pair[:, 1:] / pair[:, :1]
    a_cm = boost(np.concatenate([ea[:, None], pst[:, None] * nvec], axis=1), beta)
    b_cm = boost(np.concatenate([eb[:, None], -pst[:, None] * nvec], axis=1), beta)
    if single == "phi":
        k, q1, q2 = single_p, a_cm, b_cm
    elif single == "psibar":
        q2, k, q1 = single_p, a_cm, b_cm
    else:
        q1, k, q2 = single_p, a_cm, b_cm
    # (2 pi from the azimuth of the single particle) x dmsq/(2 pi): the 2 pi's cancel; flux 4 |p| sqrt(s)
    weight = W * jac * ps / (16 * math.pi ** 2 * rs) * pst / (16 * math.pi ** 2 * np.sqrt(msq)) / (4 * pA * rs)
    return p1, p2, k, q1, q2, weight


def collinear(p1, p2, q):
    """1/|(q - p_1)^2 - M^2| + 1/|(q - p_2)^2 - M^2|: the fermion propagators that peak when q is along a beam."""
    return 1 / np.abs(vmdot(q - p1, q - p1) - bm2) + 1 / np.abs(vmdot(q - p2, q - p2) - bm2)


def sigma_2to3(rs, n, method="channels", terms=("y3", "lam")):
    """method = "channels": sum|M|^2 split by g_psi/(g_psi + g_psibar) (g = collinear(q)), each part on the grid whose single
    particle is that fermion;  "phi": single grid with the phi as the single particle, plain Gauss-Legendre in cos(theta)."""
    total = 0.0
    for single in (("psi", "psibar") if method == "channels" else ("phi",)):
        p1, p2, k, q1, q2, weight = grid_2to3(rs, n, single)
        for i0 in range(0, len(weight), 40000):
            sl = slice(i0, i0 + 40000)
            f = sum_m2_23(p1, p2, k[sl], q1[sl], q2[sl], terms)
            if method == "channels":
                g1, g2 = collinear(p1, p2, q1[sl]), collinear(p1, p2, q2[sl])
                f = f * (g1 if single == "psi" else g2) / (g1 + g2)
            total += np.sum(weight[sl] * f)
    return total


def sigma_2to3_mc(rs, npts, seed=1, chunk=200000, terms=("y3", "lam"), bins=None):
    """independent Monte Carlo check: Dalitz variables m12^2 = (q1 + q2)^2, m23^2 = (q2 + k)^2 uniform, the orientation of the
    final triangle uniform (random rotation), dPhi_3 = dm12^2 dm23^2/(128 pi^3 s) dR/(8 pi^2).  Returns (sigma, error), and
    with bins also the cross section and its error in bins of cos(theta) of the psi."""
    rng = np.random.default_rng(seed)
    s = rs * rs
    e = rs / 2
    pA = math.sqrt(e * e - m2)
    p1, p2 = np.array([e, 0, 0, pA]), np.array([e, 0, 0, -pA])
    a12, b12 = (2 * MPSI) ** 2, (rs - MPHI) ** 2
    a23, b23 = (MPSI + MPHI) ** 2, (rs - MPSI) ** 2
    vals, cth = [], []
    for _ in range(npts // chunk):
        x, y = rng.uniform(a12, b12, chunk), rng.uniform(a23, b23, chunk)
        ek, e1 = (s + m2 - x) / (2 * rs), (s + bm2 - y) / (2 * rs)
        e2 = rs - ek - e1
        pk, pq1, pq2 = (np.sqrt(np.maximum(z, 0)) for z in (ek ** 2 - m2, e1 ** 2 - bm2, e2 ** 2 - bm2))
        c = (pq2 ** 2 - pk ** 2 - pq1 ** 2) / np.maximum(2 * pk * pq1, 1e-300)
        ok = (ek > MPHI) & (e1 > MPSI) & (e2 > MPSI) & (np.abs(c) <= 1)
        c = np.clip(c, -1, 1)
        zero = np.zeros(chunk)
        kv = np.stack([zero, zero, pk], axis=1)
        q1v = np.stack([pq1 * np.sqrt(1 - c * c), zero, pq1 * c], axis=1)
        rot = Rotation.random(chunk, random_state=rng).as_matrix()
        kv, q1v = np.einsum("nij,nj->ni", rot, kv), np.einsum("nij,nj->ni", rot, q1v)
        k = np.concatenate([ek[:, None], kv], axis=1)
        q1 = np.concatenate([e1[:, None], q1v], axis=1)
        q2 = np.concatenate([e2[:, None], -kv - q1v], axis=1)
        f = np.zeros(chunk)
        f[ok] = sum_m2_23(p1, p2, k[ok], q1[ok], q2[ok], terms)
        vals.append(f)
        cth.append(q1v[:, 2] / np.maximum(pq1, 1e-300))
    f = np.concatenate(vals) * (b12 - a12) * (b23 - a23) / (128 * math.pi ** 3 * s) / (4 * pA * rs)
    if bins is None:
        return f.mean(), f.std() / math.sqrt(len(f))
    idx = np.digitize(np.concatenate(cth), bins) - 1
    fb = np.array([np.where(idx == i, f, 0.0) for i in range(len(bins) - 1)])
    return f.mean(), f.std() / math.sqrt(len(f)), fb.mean(axis=1), fb.std(axis=1) / math.sqrt(len(f))


# the spin sum against MadGraph at nodes of the quadrature grids (every 997th node of n = 8)
worst, npts = 0.0, 0
for rs in (2.5, 5.0, 20.0):
    for single in ("phi", "psi", "psibar"):
        p1, p2, k, q1, q2, _ = grid_2to3(rs, 8, single)
        idx = np.arange(0, len(k), 997)
        ours = sum_m2_23(p1, p2, k[idx], q1[idx], q2[idx])
        for j, i in enumerate(idx):
            mg_me = madgraph_me([p1, p2, k[i], q1[i], q2[i]])
            worst, npts = max(worst, abs(ours[j] - mg_me) / abs(mg_me)), npts + 1
print(f"sum|M|^2 of phi phi -> phi psi psibar vs MadGraph standalone ({npts} points): max rel. dev. {worst:.1e}")

sig3 = {}
for rs in SQRTS_TABLE:
    c32, c24 = sigma_2to3(rs, 32), sigma_2to3(rs, 24)
    f24 = sigma_2to3(rs, 24, "phi")
    mc, mce = sigma_2to3_mc(rs, 2000000)
    sig3[rs] = (c32, c24, f24, mc, mce)
    print(f"sigma_3 at sqrt(s) = {rs:5.2f}: {c32 * GEV2_TO_PB:.10e} pb (two channels, n = 32);  n = 24: rel. {abs(c24 - c32) / c32:.1e};"
          f"  single phi grid, n = 24: rel. {abs(f24 - c32) / c32:.1e};  Monte Carlo: (MC - GL)/err = {(mc - c32) / mce:+.2f}"
          f" (err {mce / mc:.1e})")

# %% [markdown]
# ## Comparison with MadGraph (tree level) and the table of cross sections

# %%
mg = []
logf = os.path.join(HERE, "work", "xsec_mg5.log")
if os.path.exists(logf):
    mg = [(float(x), float(e)) for x, e in re.findall(r"Cross-section :\s+([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb", open(logf).read())]
mg_points = [("Bbar", 3.0), ("Bbar", 5.0), ("Bbar", 10.0), ("3", 3.0), ("3", 5.0), ("3", 10.0), ("3lam", 10.0), ("3y", 10.0)]
for (proc, rs), (x, e) in zip(mg_points, mg):
    if proc == "Bbar":
        ref = two2two[rs][1]
    elif proc == "3":
        ref = sig3[rs][0]
    else:
        ref = sigma_2to3(rs, 32, terms=("lam",) if proc == "3lam" else ("y3",))
    ref *= GEV2_TO_PB
    half_ulp = 0.5 * 10 ** (math.floor(math.log10(abs(x))) - 3)
    print(f"MadGraph {proc:4s} sqrt(s) = {rs:5.1f}: {x:.4e} +- {e:.1e} pb vs {ref:.6e} pb ({(x - ref) / ref:+.2%}),"
          f"  (MG - note)/err_eff = {(x - ref) / max(e, half_ulp):+.2f}")

# where MadGraph's phi phi -> phi psi psibar falls short: the six y^3 diagrams at sqrt(s) = 10, in bins of cos(theta_psi)
lhe = os.path.join(HERE, "work", "mg5_xsec3y", "Events", "run_01", "unweighted_events.lhe.gz")
if len(mg) == len(mg_points) and os.path.exists(lhe):
    import gzip
    bins = np.array([-1, -0.999, -0.99, -0.95, -0.8, -0.5, 0, 0.5, 0.8, 0.95, 0.99, 0.999, 1])
    cpsi = []
    with gzip.open(lhe, "rt") as fh:
        for blk in fh.read().split("<event>")[1:]:
            lines = blk.split("</event>")[0].strip().split("\n")
            for line in lines[1:1 + int(lines[0].split()[0])]:
                f = line.split()
                if f[0] == "9000002" and f[1] == "1":
                    px, py, pz = map(float, f[6:9])
                    cpsi.append(pz / math.sqrt(px * px + py * py + pz * pz))
    hmg = np.histogram(cpsi, bins)[0]
    _, _, hb, hbe = sigma_2to3_mc(10.0, 6000000, seed=3, terms=("y3",), bins=bins)
    print(f"y^3 diagrams, sqrt(s) = 10, {len(cpsi)} MadGraph events: d sigma in bins of cos(theta_psi) [pb]")
    for i in range(len(bins) - 1):
        x, e = mg[-1][0] * hmg[i] / len(cpsi), mg[-1][0] * math.sqrt(hmg[i]) / len(cpsi)
        print(f"  [{bins[i]:+.3f}, {bins[i + 1]:+.3f}]  MadGraph {x:9.1f} +- {e:5.1f}   Monte Carlo {hb[i] * GEV2_TO_PB:9.1f} +- "
              f"{hbe[i] * GEV2_TO_PB:5.1f}   ({(x - hb[i] * GEV2_TO_PB) / math.hypot(e, hbe[i] * GEV2_TO_PB):+.1f} sigma)")

rows = []
print(f"{'sqrt(s)':>7} {'sA0':>11} {'sBbar0':>11} {'sA1':>11} {'sBbar1':>11} {'s3':>11} {'s_tot LO':>11} {'s_tot NLO':>11} {'NLO/LO-1':>9}  [pb]")
for rs in sorted(set(SQRTS_TABLE) | set(SQRTS_SCAN)):
    sA0, sB0, sA1, sB1 = two2two[rs]
    s3 = sig3[rs][0] if rs in sig3 else sigma_2to3(rs, 16) if rs > MPHI + 2 * MPSI else 0.0
    lo = sA0 + sB0
    nlo = lo + sA1 + sB1 + s3
    rows.append([rs, sA0, sB0, sA1, sB1, s3, lo, nlo])
    if rs in SQRTS_TABLE:
        print(f"{rs:7.2f} " + " ".join(f"{x * GEV2_TO_PB:11.4e}" for x in (sA0, sB0, sA1, sB1, s3, lo, nlo)) + f" {nlo / lo - 1:+9.4f}")

with open(os.path.join(HERE, "results", "xsec.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sqrts", "sigma_A0_pb", "sigma_Bbar0_pb", "sigma_A1_pb", "sigma_Bbar1_pb", "sigma_3_pb", "sigma_tot_LO_pb", "sigma_tot_NLO_pb"])
    for r in rows:
        w.writerow([r[0]] + [x * GEV2_TO_PB for x in r[1:]])
print("wrote results/xsec.csv")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
from matplotlib.ticker import FixedLocator, NullFormatter, NullLocator
arr = np.array(rows)
rs = arr[:, 0]
tab = np.array(SQRTS_TABLE)
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
ax = axes[0]
ax.plot(rs, arr[:, 6] * GEV2_TO_PB, color="C0", ls="--", label=r"$\sigma_{\rm tot}$, tree")
ax.plot(rs, arr[:, 7] * GEV2_TO_PB, color="C0", ls="-", label=r"$\sigma_{\rm tot}$, NLO")
ax.plot(rs, arr[:, 1] * GEV2_TO_PB, color="C1", ls=":", label=r"$\phi\phi\to\phi\phi$, tree")
ax.plot(rs, arr[:, 2] * GEV2_TO_PB, color="C2", ls=":", label=r"$\phi\phi\to\psi\bar\psi$, tree")
open3 = arr[:, 5] > 0                       # phi phi -> phi psi psibar opens at sqrt(s) = m + 2M
ax.plot(rs[open3], arr[open3, 5] * GEV2_TO_PB, color="C3", ls="-.", label=r"$\phi\phi\to\phi\psi\bar\psi$")
ax.set_yscale("log")
ax.set_ylim(5e3, 8e6)
ax.set_ylabel(r"$\sigma$ [pb]")
ax.legend(fontsize=7, loc="lower left", bbox_to_anchor=(0.18, 0.0))
ax = axes[1]
lo_tab = np.array([two2two[r][0] + two2two[r][1] for r in tab])
ax.plot(rs, arr[:, 3] / arr[:, 6], color="C1", ls="-", label=r"$\sigma^{(1)}_{\phi\phi\to\phi\phi}$")
ax.plot(rs, arr[:, 4] / arr[:, 6], color="C2", ls="-", label=r"$\sigma^{(1)}_{\phi\phi\to\psi\bar\psi}$")
ax.plot(rs, arr[:, 5] / arr[:, 6], color="C3", ls="-.", label=r"$\sigma_{\phi\phi\to\phi\psi\bar\psi}$")
ax.plot(rs, (arr[:, 7] - arr[:, 6]) / arr[:, 6], color="C0", ls="-", lw=1.5, label="sum")
ax.plot(tab, [ml_loops[r][0] for r in tab] / lo_tab, ls="none", marker="o", mfc="none", color="C1", ms=4, label="MadLoop")
ax.plot(tab, [ml_loops[r][1] for r in tab] / lo_tab, ls="none", marker="o", mfc="none", color="C2", ms=4)
mg3 = [(rs_, x / GEV2_TO_PB) for (proc, rs_), (x, e) in zip(mg_points, mg) if proc == "3"]
if mg3:
    ax.plot([r for r, _ in mg3], [x / (two2two[r][0] + two2two[r][1]) for r, x in mg3], ls="none", marker="x", color="C3", ms=4,
            label="MadGraph")
ax.axhline(0, color="0.6", lw=0.5)
ax.set_ylabel(r"ratio to $\sigma_{\rm tot}$ (tree)")
ax.legend(fontsize=7)
for ax in axes:
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator([2, 3, 5, 10, 20]))
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:g}")
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(2, 21)
    ax.set_xlabel(r"$\sqrt{s}/m$")
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "xsec_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
