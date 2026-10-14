# %% [markdown]
# # Step (6): e+ e- -> mu+ mu- (gamma) to order alpha^3 -- virtual, soft and hard photons, IR cancellation, A_FB
#
# Research note models/spinor_qed, step (6), Eqs. (19)-(21).  e = 1 (MS-bar e(mu) at mu = 1), m_e = 1, m_mu = 1.7 (pole
# masses), sqrt(s) = 4, 6, 10.  The order-alpha^3 cross section is split at the photon energy DeltaE (CM frame):
#     Delta sigma = sigma_V + sigma_S(DeltaE) + sigma_H(DeltaE),
# - sigma_V: the interference 2 Re W of step (4) (K W from the note's formulas with COLLIER, xsec_collier.f90, at Gauss-Legendre
#   nodes in cos(theta)), in CDR and with four-dimensional spin sums (Eq. (17));
# - sigma_S: the Born times the soft factor S(DeltaE) of Eq. (19), S = (2 e^2/K) sum_{i,j} c_i c_j [P_ij DeltaIR + J_ij],
#   P_ij = p_i.p_j int dx/p_x^2, J_ij = p_i.p_j int dx [ln(mu^2/DeltaE^2) - A(p_x)]/p_x^2,
#   A(p) = (p^2/2) int_{-1}^{1} dc ln(1 - c^2)/(p^0 - |p| c)^2 (the O(eps) part of the (D-1)-dimensional angular integral);
#   in CDR the Born is B(D) = B(4) - 8 eps e^4, which adds -8 e^4 S_pole;  checked against the photon-mass formula
#   ('t Hooft-Veltman) with ln(lambda^2) -> DeltaIR + ln(mu^2);
# - sigma_H: the 2 -> 3 cross section with E_gamma > DeltaE, |M|^2 of real_feyncalc.wl (generated/msq_eemumua.py), integrated
#   with nested Gauss-Legendre quadrature in photon-first variables (photon energy log-mapped and smoothed at the muon-pair
#   threshold, photon polar angle and the mu- polar angle in the pair rest frame tanh-mapped to flatten the collinear
#   peaks, the mu- azimuth split where mu- changes hemisphere), checked with an independent Monte Carlo in Dalitz variables.
# Checks: the IR pole of 2 Re W plus the Born times S_pole vanishes at every node; sigma_S + sigma_H does not depend on DeltaE
# as DeltaE -> 0; the total is the same in CDR and with four-dimensional spin sums; |M|^2 against explicit spinors and MadGraph's
# standalone matrix element, its soft limit against the eikonal factor; sigma_H and the hard-photon forward-backward asymmetry
# against MadGraph (work/xsec_mg5.log, LHE files); MadGraph's deficit binned in y = min(2 p_1.k, 2 p_2.k)/m_e^2, the distance to the
# electron pole, with MadGraph's original grid and with the grid of mg5_tpole.py (work/xsec_mg5_tpole.log); the same grid for
# the tree-level processes of step (2) is in tree_sigma.py.  A_FB = (sigma_F - sigma_B)/(sigma_F + sigma_B), forward = mu- along e-.
# Writes results/xsec.csv and ../figs/xsec_softhard.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python xsec_numeric.py` (from Src/; run_xsec_check.sh builds the helpers).
# Interactive: "Run Cell" in VS Code.

# %%
import csv
import gzip
import itertools
import math
import os
import re
import subprocess
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import quad

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
sys.path.insert(0, os.path.join(HERE, "generated"))
from msq_eemumua import msq   # noqa: E402  (written by real_feyncalc.wl)

ME, MMU, EL = 1.0, 1.7, 1.0
KK = (4 * math.pi) ** 2
PB = 0.3893794e9                       # GeV^-2 -> pb
SQRTS = (4.0, 6.0, 10.0)
DES = (0.1, 0.03, 0.01, 0.003, 0.001)  # the soft-hard boundary DeltaE
DE_MG = 0.1                            # the cut of xsec_mg5.mg5
NGL = 24                               # Gauss-Legendre nodes on each half of cos(theta)
GRID, GRID_COARSE = (32, 64, 64, 16), (24, 48, 48, 12)
mp.mp.dps = 20


def dot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def gl(n, a=0.0, b=1.0):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def kin22(rs, c):
    e = rs / 2
    p, k = math.sqrt(e * e - ME ** 2), math.sqrt(e * e - MMU ** 2)
    st = math.sqrt(1 - c * c)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    k1, k2 = np.array([e, k * st, 0, k * c]), np.array([e, -k * st, 0, -k * c])
    return p1, p2, k1, k2


def born4(s, t):
    u = 2 * ME ** 2 + 2 * MMU ** 2 - s - t
    sig = ME ** 2 + MMU ** 2
    return 8 / s ** 2 * ((t - sig) ** 2 + (u - sig) ** 2 + 2 * s * sig)


cnodes, cweights = zip(*[gl(NGL, -1, 0), gl(NGL, 0, 1)])
CN, CW = np.concatenate(cnodes), np.concatenate(cweights)
CN[:3], CW[:3]       # inspect

# %% [markdown]
# ## Virtual: K W at the nodes (COLLIER, CDR) and Eq. (17)

# %%
def f_ir(s, m):
    s, m = mp.mpf(s), mp.mpf(m)
    b = mp.sqrt(1 - 4 * m * m / s)
    return (s - 2 * m * m) / (s * b) * (mp.log((1 + b) / (1 - b)) - 1j * mp.pi) - 1


def g_ir(x):
    m2, mm2, x = mp.mpf(ME) ** 2, mp.mpf(MMU) ** 2, mp.mpf(x)
    return (m2 + mm2 - x) * mp.quad(lambda w: 1 / (w * m2 + (1 - w) * mm2 - x * w * (1 - w)), [0, 1])


with open(os.path.join(HERE, "work", "xsec_nodes.txt"), "w") as fh:
    fh.writelines("%.17e %.17e\n" % (rs, c) for rs in SQRTS for c in CN)
subprocess.run(["./xsec_collier", "xsec_nodes.txt", "xsec_virt.csv"], cwd=os.path.join(HERE, "work"), check=True,
               capture_output=True)
VIRT = {}
with open(os.path.join(HERE, "work", "xsec_virt.csv")) as fh:
    for r in csv.DictReader(fh):
        z = lambda k: complex(float(r["re_" + k]), float(r["im_" + k]))
        VIRT[(round(float(r["sqrts"]), 6), round(float(r["costheta"]), 12))] = {"uv": z("uv"), "ir": z("ir"), "fin": z("fin"),
                                                                                "s": float(r["s"]), "t": float(r["t"])}
for key, v in VIRT.items():
    u = 2 * ME ** 2 + 2 * MMU ** 2 - v["s"] - v["t"]
    v["fin4"] = v["fin"] + 16 * complex(f_ir(v["s"], ME) + f_ir(v["s"], MMU) + g_ir(v["t"]) - g_ir(u))   # Eq. (17)
print("max |UV pole| of K W at the nodes:", max(abs(v["uv"]) for v in VIRT.values()))

# %% [markdown]
# ## Soft photons: the pair integrals of Eq. (19) and the photon-mass formula

# %%
def a_fn(p):
    e, pa, p2 = p[0], math.sqrt(p[1] ** 2 + p[2] ** 2 + p[3] ** 2), dot(p, p)
    f = lambda c: math.log(1 - c * c) / (e - pa * c) ** 2
    return p2 / 2 * (quad(f, -1, 0, limit=200, epsabs=0, epsrel=1e-13)[0] + quad(f, 0, 1, limit=200, epsabs=0, epsrel=1e-13)[0])


def pair(pi, pj):
    """P_ij = p_i.p_j int dx/p_x^2 and Atil_ij = p_i.p_j int dx A(p_x)/p_x^2, p_x = x p_i + (1-x) p_j:
    J_ij(DeltaE) = P_ij ln(mu^2/DeltaE^2) - Atil_ij"""
    pp = dot(pi, pj)
    px = lambda x: x * pi + (1 - x) * pj
    P = pp * quad(lambda x: 1 / dot(px(x), px(x)), 0, 1, epsabs=0, epsrel=1e-13)[0]
    At = pp * quad(lambda x: a_fn(px(x)) / dot(px(x), px(x)), 0, 1, epsabs=0, epsrel=1e-12)[0]
    return P, At


def i_mass(pi, pj, de, lnlam2):
    """int_{|k|<DeltaE} d^3k/(2 omega) p_i.p_j/((p_i.k)(p_j.k)) with a photon mass ('t Hooft-Veltman)"""
    if np.allclose(pi, pj):
        e, pa = pi[0], math.sqrt(pi[1] ** 2 + pi[2] ** 2 + pi[3] ** 2)
        return math.pi * (math.log(4 * de ** 2) - lnlam2 + e / pa * math.log((e - pa) / (e + pa)))
    pp, mi2, mj2 = dot(pi, pj), dot(pi, pi), dot(pj, pj)
    al = next(a for a in ((pp + sg * math.sqrt(pp * pp - mi2 * mj2)) / mi2 for sg in (1, -1)) if a * pi[0] - pj[0] > 0)
    v = (al * al * mi2 - mj2) / (2 * (al * pi[0] - pj[0]))

    def f(u):
        u0, ua = u[0], math.sqrt(u[1] ** 2 + u[2] ** 2 + u[3] ** 2)
        return (0.25 * math.log((u0 - ua) / (u0 + ua)) ** 2 + float(mp.polylog(2, 1 - (u0 + ua) / v))
                + float(mp.polylog(2, 1 - (u0 - ua) / v)))
    return 2 * math.pi * al * pp / (al * al * mi2 - mj2) * (0.5 * math.log(al * al * mi2 / mj2) * (math.log(4 * de ** 2) - lnlam2)
                                                           + f(al * pi) - f(pj))


SOFT, mass_dev = {}, 0.0
for rs in SQRTS:
    p1, p2, k1, k2 = kin22(rs, 0.3)
    const = {"11": pair(p1, p1), "33": pair(k1, k1), "12": pair(p1, p2), "34": pair(k1, k2)}
    for c in CN:
        p1, p2, k1, k2 = kin22(rs, c)
        d = dict(const, **{"13": pair(p1, k1), "14": pair(p1, k2)})
        # S = (4 e^2/K) [J11 + J33 - J12 - J34 - 2 J13 + 2 J14] (J22 = J11, J44 = J33, J24 = J13, J23 = J14 by symmetry)
        coef = {"11": 1, "33": 1, "12": -1, "34": -1, "13": -2, "14": 2}
        SOFT[(rs, round(c, 12))] = {"pole": 4 / KK * sum(coef[k] * d[k][0] for k in coef),
                                    "atil": 4 / KK * sum(coef[k] * d[k][1] for k in coef)}
        if abs(c) > 0.9 or abs(c - CN[NGL]) < 1e-12:          # the photon-mass formula at a few nodes, DeltaE = 0.1, mu = 1
            for (a, b), kk in zip(((p1, p1), (k1, k1), (p1, p2), (k1, k2), (p1, k1), (p1, k2)), ("11", "33", "12", "34", "13", "14")):
                jd = d[kk][0] * math.log(1 / 0.1 ** 2) - d[kk][1]
                mass_dev = max(mass_dev, abs(-math.pi * jd - i_mass(a, b, 0.1, 0.0)) / abs(i_mass(a, b, 0.1, 0.0)))
print(f"soft pair integrals: D-dimensional representation against the photon-mass formula, max rel. dev. {mass_dev:.1e}")


def s_fin(rs, c, de):
    """finite part of S at mu = 1: S_pole ln(1/DeltaE^2) - Atil"""
    v = SOFT[(rs, round(c, 12))]
    return v["pole"] * math.log(1 / de ** 2) - v["atil"]

# %% [markdown]
# ## IR poles: 2 Re W + B(4) S_pole = 0 at every node (Bloch-Nordsieck)

# %%
pole_dev = 0.0
for rs in SQRTS:
    for c in CN:
        v = VIRT[(rs, round(c, 12))]
        b4 = born4(v["s"], v["t"])
        lhs = 2 * v["ir"].real / KK + b4 * SOFT[(rs, round(c, 12))]["pole"]
        pole_dev = max(pole_dev, abs(lhs) / (2 * abs(v["ir"].real) / KK))
print(f"IR poles: max |2 Re W_pole + B(4) S_pole| / |2 Re W_pole| over the nodes = {pole_dev:.1e}")

# %% [markdown]
# ## Hard photons: |M|^2 checks and the 2 -> 3 integral

# %%
def kin3(rs, w, cg, cst, phs):
    """photon (w, polar cos cg, azimuth 0); mu- in the mu-pair rest frame: polar cos cst w.r.t. the photon direction, azimuth phs"""
    e = rs / 2
    p = math.sqrt(e * e - ME ** 2)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    sg = math.sqrt(1 - cg * cg)
    k3 = w * np.array([1, sg, 0, cg])
    q = p1 + p2 - k3
    qm = math.sqrt(dot(q, q))
    kst = math.sqrt(qm * qm / 4 - MMU ** 2)
    z, x, y = k3[1:] / w, np.array([cg, 0, -sg]), np.array([0.0, 1.0, 0.0])
    d = cst * z + math.sqrt(1 - cst * cst) * (math.cos(phs) * x + math.sin(phs) * y)
    bv = q[1:] / q[0]
    g = 1 / math.sqrt(1 - bv @ bv)

    def boost(e0, vec):
        bp = bv @ vec
        return np.concatenate([[g * (e0 + bp)], vec + ((g - 1) * bp / (bv @ bv) + g * e0) * bv])
    return p1, p2, boost(qm / 2, kst * d), boost(qm / 2, -kst * d), k3


def msq_pt(p1, p2, k1, k2, k3):
    return msq(dot(p1, p2), dot(p1, k1), dot(p1, k2), dot(p1, k3), dot(p2, k1), dot(p2, k2), dot(p2, k3), dot(k1, k2),
               dot(k1, k3), dot(k2, k3), ME, MMU, EL)


# explicit spinors and real transverse polarization vectors (as tree_sigma.py), the four diagrams of Fig. 5 (viii)
I2, Z2 = np.eye(2, dtype=complex), np.zeros((2, 2), dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
G0 = np.block([[I2, Z2], [Z2, -I2]])
GAM = [G0] + [np.block([[Z2, s], [-s, Z2]]) for s in SIG]
METRIC = np.array([1.0, -1.0, -1.0, -1.0])
ONE, CHI = np.eye(4, dtype=complex), [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]
slash = lambda p: sum(METRIC[n] * p[n] * GAM[n] for n in range(4))


def u_sp(p, m, c):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + m)
    return np.concatenate([n * c, sp @ c / n])


def v_sp(p, m, c):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + m)
    return np.concatenate([sp @ c / n, n * c])


bar = lambda w: w.conj() @ G0


def pols(k):
    kv = k[1:] / np.linalg.norm(k[1:])
    th, ph = math.acos(max(-1.0, min(1.0, kv[2]))), math.atan2(kv[1], kv[0])
    return [np.array([0, math.cos(th) * math.cos(ph), math.cos(th) * math.sin(ph), -math.sin(th)]),
            np.array([0, -math.sin(ph), math.cos(ph), 0.0])]


def msq_explicit(p1, p2, k1, k2, k3):
    s, q2 = dot(p1 + p2, p1 + p2), dot(k1 + k2, k1 + k2)
    tot = 0.0
    for a, b, c, d in itertools.product(CHI, CHI, CHI, CHI):
        u1, v2, u3, v4 = u_sp(p1, ME, a), v_sp(p2, ME, b), u_sp(k1, MMU, c), v_sp(k2, MMU, d)
        for eps in pols(k3):
            es = slash(eps)
            je = [bar(v2) @ GAM[n] @ u1 for n in range(4)]
            jm = [bar(u3) @ GAM[n] @ v4 for n in range(4)]
            le = [bar(v2) @ (GAM[n] @ (slash(p1 - k3) + ME * ONE) @ es / (dot(p1 - k3, p1 - k3) - ME ** 2)
                             + es @ (slash(k3 - p2) + ME * ONE) @ GAM[n] / (dot(p2 - k3, p2 - k3) - ME ** 2)) @ u1 for n in range(4)]
            lm = [bar(u3) @ (es @ (slash(k1 + k3) + MMU * ONE) @ GAM[n] / (dot(k1 + k3, k1 + k3) - MMU ** 2)
                             + GAM[n] @ (slash(-k2 - k3) + MMU * ONE) @ es / (dot(k2 + k3, k2 + k3) - MMU ** 2)) @ v4 for n in range(4)]
            m = EL ** 3 * (sum(METRIC[n] * le[n] * jm[n] for n in range(4)) / q2 + sum(METRIC[n] * je[n] * lm[n] for n in range(4)) / s)
            tot += abs(m) ** 2
    return tot


CHECK_PTS = [(4.0, 0.2, 0.3, 0.4, 1.0), (10.0, 2.0, -0.9, 0.7, 2.5), (6.0, 0.01, 0.99, -0.95, 0.3), (10.0, 0.5, 0.999, 0.2, 0.1),
             (6.0, 1.5, -0.2, 0.98, 4.0)]
me_dir = os.path.join(HERE, "work", "sa_xsec3", "SubProcesses", "P1_emep_mummupa")
mg_in = "\n".join(" ".join("%.17e" % x for vec in kin3(*a) for x in vec) for a in CHECK_PTS) + "\n"
mg_me = [float(x) for x in subprocess.run(["./me_points"], cwd=me_dir, input=mg_in, capture_output=True, text=True,
                                            check=True).stdout.split()]
dev_sp = dev_mg = 0.0
for a, mgv in zip(CHECK_PTS, mg_me):
    f = msq_pt(*kin3(*a))
    dev_sp = max(dev_sp, abs(f - msq_explicit(*kin3(*a))) / f)
    dev_mg = max(dev_mg, abs(f / 4 - mgv) / (f / 4))          # MadGraph averages over the initial helicities
print(f"|M|^2 at {len(CHECK_PTS)} points: against explicit spinors {dev_sp:.1e}, against MadGraph's standalone {dev_mg:.1e}")

# soft limit: omega^2 |M|^2 -> -e^2 sum c_i c_j (p_i.p_j)/((p_i.n)(p_j.n)) B(4), n = k3/omega
for w in (1e-2, 1e-4, 1e-6):
    p1, p2, k1, k2, k3 = kin3(6.0, w, 0.3, 0.4, 1.0)
    n = k3 / w
    moms, cs = (p1, p2, k1, k2), (1, -1, -1, 1)
    eik = -EL ** 2 * sum(cs[i] * cs[j] * dot(moms[i], moms[j]) / (dot(moms[i], n) * dot(moms[j], n)) for i in range(4) for j in range(4))
    s_, t_ = dot(p1 + p2, p1 + p2), dot(p1 - k1, p1 - k1)
    print(f"soft limit, omega = {w:.0e}: omega^2 |M|^2 / (eikonal x B(4)) - 1 = {w ** 2 * msq_pt(p1, p2, k1, k2, k3) / (eik * born4(s_, t_)) - 1:+.1e}")

# %%
def hard(rs, de, nu, neta, nst, nph, cmax=1.0, ycut=0.0):
    """sigma_H(E_gamma > DeltaE) and its forward part (mu- with p_z > 0), GeV^-2; |cos theta_gamma| < cmax and
    y = min(2 p_1.k, 2 p_2.k)/m_e^2 > ycut (the distance to the electron pole of the initial-state radiation)"""
    s, e = rs * rs, rs / 2
    p = math.sqrt(e * e - ME ** 2)
    be = p / e
    wmax = (s - 4 * MMU ** 2) / (2 * rs)
    lg = math.log(wmax / de)
    vv, wv = gl(nu)
    uu = 1 - (1 - vv) ** 2                           # sqrt(omega_max - omega) at the pair threshold made smooth
    w = de * np.exp(lg * uu)
    jw = w * lg * 2 * (1 - vv) * wv
    et, wet = gl(neta, -math.atanh(be * cmax), math.atanh(be * cmax))
    cg = np.tanh(et) / be
    jg = (1 - be * be * cg * cg) / be * wet
    tq, wtq = gl(nph)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    P1, P2 = p1[:, None, None, None], p2[:, None, None, None]
    tot = fwd = 0.0
    for iw in range(nu):
        om = w[iw]
        if ycut > 0:       # min(2 p_1.k, 2 p_2.k) = 2 omega (E - |p| |cos theta_gamma|) > ycut m_e^2
            ce = min(cmax, (e - ycut * ME ** 2 / (2 * om)) / p)
            if ce <= 0:
                continue
            et, wet = gl(neta, -math.atanh(be * ce), math.atanh(be * ce))
            cg = np.tanh(et) / be
            jg = (1 - be * be * cg * cg) / be * wet
        q2 = s - 2 * rs * om
        qm = math.sqrt(q2)
        bs = math.sqrt(1 - 4 * MMU ** 2 / q2)
        kst, est = qm / 2 * bs, qm / 2
        es, wes = gl(nst, -math.atanh(bs), math.atanh(bs))
        cs = np.tanh(es) / bs
        js = (1 - bs * bs * cs * cs) / bs * wes
        CG, CS = np.meshgrid(cg, cs, indexing="ij")
        SG, SS = np.sqrt(1 - CG * CG), np.sqrt(1 - CS * CS)
        bmag = om / (rs - om)
        gam = 1 / math.sqrt(1 - bmag * bmag)
        gp = (gam - 1) / bmag ** 2
        # p_z of mu- = A + B cos(phi): the azimuth is split at the zero, phi in [0, pi] times 2 (reflection symmetry)
        A = -gam * est * bmag * CG + CS * kst * (CG + gp * bmag * bmag * CG)
        B = -SS * kst * SG
        ph0 = np.arccos(np.clip(-A / np.where(B == 0, -1e-300, B), -1, 1))
        PH = np.concatenate([ph0[..., None] * tq, ph0[..., None] + (math.pi - ph0[..., None]) * tq], axis=-1)
        WPH = 2 * np.concatenate([ph0[..., None] * wtq, (math.pi - ph0[..., None]) * wtq], axis=-1)
        CGg, CSg, SGg, SSg = (X[..., None] for X in (CG, CS, SG, SS))
        z, x = np.stack([SGg, 0 * SGg, CGg]), np.stack([CGg, 0 * CGg, -SGg])
        y = np.stack([0 * SGg, 1 + 0 * SGg, 0 * SGg])
        d = CSg * z + SSg * (np.cos(PH) * x + np.sin(PH) * y)
        k3 = om * np.stack([np.ones(PH.shape), SGg + 0 * PH, np.zeros(PH.shape), CGg + 0 * PH])
        bvec = -bmag * z

        def boost(e0, vec):
            bp = (bvec * vec).sum(0)
            return np.concatenate([[gam * (e0 + bp)], vec + (gp * bp + gam * e0) * bvec])
        k1, k2 = boost(est, kst * d), boost(est, -kst * d)
        m2 = msq(dot(p1, p2), dot(P1, k1), dot(P1, k2), dot(P1, k3), dot(P2, k1), dot(P2, k2), dot(P2, k3), dot(k1, k2),
                 dot(k1, k3), dot(k2, k3), ME, MMU, EL)
        # d sigma = |M|^2/4 dPhi_3/(4 |p| sqrt s),  dPhi_3 = omega d omega dOmega_gamma |k*| dOmega*/(256 pi^5 sqrt(Q^2))
        wt = jw[iw] * om * (2 * math.pi * jg)[:, None, None] * (kst * js)[None, :, None] * WPH / (256 * math.pi ** 5 * qm)
        f = m2 / 4 * wt / (4 * p * rs)
        tot += f.sum()
        fwd += f[k1[3] > 0].sum()
    return tot, fwd


def hard_mc(rs, de, n=2_000_000, reps=10, seed=12345):
    """independent Monte Carlo in Dalitz variables: dPhi_3 = dE1 d omega dcos1 dphi1 dchi/(8 (2 pi)^5)"""
    rng = np.random.default_rng(seed)
    s, e = rs * rs, rs / 2
    p = math.sqrt(e * e - ME ** 2)
    wmax = (s - 4 * MMU ** 2) / (2 * rs)
    vol = (rs / 2 - MMU) * (wmax - de) * 2 * (2 * math.pi) ** 2
    p1, p2 = np.array([e, 0, 0, p])[:, None], np.array([e, 0, 0, -p])[:, None]
    res = []
    for _ in range(reps):
        e1, om = rng.uniform(MMU, rs / 2, n), rng.uniform(de, wmax, n)
        c1, chi = rng.uniform(-1, 1, n), rng.uniform(0, 2 * math.pi, n)
        e2 = rs - e1 - om
        k1a = np.sqrt(e1 * e1 - MMU ** 2)
        c1k = (e2 * e2 - MMU ** 2 - k1a ** 2 - om ** 2) / (2 * k1a * om)
        ok = (e2 > MMU) & (np.abs(c1k) <= 1)
        c1k = np.clip(c1k, -1, 1)
        s1, s1k = np.sqrt(1 - c1 * c1), np.sqrt(1 - c1k * c1k)
        n1, e1v, e2v = np.stack([s1, 0 * s1, c1]), np.stack([c1, 0 * c1, -s1]), np.stack([0 * s1, 1 + 0 * s1, 0 * s1])
        nk = c1k * n1 + s1k * (np.cos(chi) * e1v + np.sin(chi) * e2v)
        k1, k3 = np.concatenate([[e1], k1a * n1]), np.concatenate([[om], om * nk])
        k2 = np.concatenate([[e2], -k1[1:] - k3[1:]])
        m2 = msq(dot(p1, p2)[0], dot(p1, k1), dot(p1, k2), dot(p1, k3), dot(p2, k1), dot(p2, k2), dot(p2, k3), dot(k1, k2),
                 dot(k1, k3), dot(k2, k3), ME, MMU, EL)
        f = np.where(ok, m2 / 4 / (8 * (2 * math.pi) ** 5) / (4 * p * rs) * vol, 0.0)
        res.append([f.mean(), (f * (k1[3] > 0)).mean()])
    r = np.array(res)
    return r.mean(0), r.std(0) / math.sqrt(reps)


HARD = {}
for rs in SQRTS:
    for de in DES:
        HARD[(rs, de)] = hard(rs, de, *GRID)
        coarse = hard(rs, de, *GRID_COARSE)
        HARD[(rs, de, "err")] = (abs(coarse[0] - HARD[(rs, de)][0]), abs(coarse[1] - HARD[(rs, de)][1]))
mcv = {rs: hard_mc(rs, DE_MG) for rs in SQRTS}
for rs in SQRTS:
    (m, mf), (e, ef) = mcv[rs]
    h = HARD[(rs, DE_MG)]
    print(f"sqrt(s) = {rs:4.1f}, DeltaE = {DE_MG}: sigma_H quadrature {h[0] * PB:.6e} pb (grid change {HARD[(rs, DE_MG, 'err')][0] / h[0]:.0e}), "
          f"Monte Carlo {m * PB:.5e} +- {e * PB:.1e} pb ({(h[0] - m) / e:+.1f} sigma)")

# %% [markdown]
# ## MadGraph: sigma_H and the hard forward-backward asymmetry at DeltaE = 0.1

# %%
mg_log = open(os.path.join(HERE, "work", "xsec_mg5.log")).read()
mg_sig = [(float(a), float(b)) for a, b in re.findall(r"Cross-section :\s+(\S+)\s+\+-\s+(\S+)\s+pb", mg_log)]


def lhe_afb(path):
    nf = nb = 0
    with gzip.open(path, "rt") as fh:
        block = False
        for line in fh:
            if line.startswith("<event>"):
                block = True
                continue
            if line.startswith("</event>"):
                block = False
                continue
            if block:
                f = line.split()
                if len(f) > 9 and f[0] == "13" and f[1] == "1":
                    if float(f[8]) > 0:
                        nf += 1
                    else:
                        nb += 1
    n = nf + nb
    a = (nf - nb) / n
    return a, math.sqrt((1 - a * a) / n), n


MG = {}
for i, rs in enumerate(SQRTS):
    a, da, n = lhe_afb(os.path.join(HERE, "work", "mg5_xsec3", "Events", f"run_{i + 1:02d}", "unweighted_events.lhe.gz"))
    MG[rs] = {"sigma": mg_sig[i][0], "err": mg_sig[i][1], "afb": a, "afb_err": da, "n": n}
    h = HARD[(rs, DE_MG)]
    print(f"sqrt(s) = {rs:4.1f}: sigma_H MadGraph {mg_sig[i][0]:.4e} +- {mg_sig[i][1]:.1e} pb, quadrature {h[0] * PB:.4e} pb "
          f"({(mg_sig[i][0] - h[0] * PB) / mg_sig[i][1]:+.1f} sigma, {mg_sig[i][0] / (h[0] * PB) - 1:+.2%});  "
          f"A_FB(hard) MadGraph {a:+.4f} +- {da:.4f}, quadrature {(2 * h[1] - h[0]) / h[0]:+.5f}")

# diagnostic runs: |cos theta_gamma| < 0.9 at sqrt(s) = 6, 10 and sde_strategy 2 at sqrt(s) = 6; the photon-energy bins of the
# LHE files of the main runs against the quadrature
for (rs, cmax, label), (sg, er) in zip(((6.0, 0.9, "|cos g| < 0.9"), (10.0, 0.9, "|cos g| < 0.9"), (6.0, 1.0, "sde_strategy 2")), mg_sig[3:6]):
    q = hard(rs, DE_MG, *GRID, cmax=cmax)[0] * PB
    print(f"sqrt(s) = {rs:4.1f}, {label}: MadGraph {sg:.4e} +- {er:.1e} pb, quadrature {q:.4e} pb ({sg / q - 1:+.1%}, {(sg - q) / er:+.1f} sigma)")


def lhe_omega(path):
    om = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            f = line.split()
            if len(f) > 9 and f[0] == "22" and f[1] == "1":
                om.append(float(f[9]))
    return np.array(om)


MG_BINS = []
for i, rs in enumerate(SQRTS):
    om = lhe_omega(os.path.join(HERE, "work", "mg5_xsec3", "Events", f"run_{i + 1:02d}", "unweighted_events.lhe.gz"))
    wmax = (rs * rs - 4 * MMU ** 2) / (2 * rs)
    edges = [x for x in (DE_MG, 0.3, 1.0) if x < wmax] + [wmax]
    cum = [hard(rs, x, *GRID)[0] * PB for x in edges[:-1]] + [0.0]
    for (a, b_), ca, cb in zip(zip(edges[:-1], edges[1:]), cum[:-1], cum[1:]):
        nmg = ((om >= a) & (om < b_)).sum() / len(om) * MG[rs]["sigma"]
        MG_BINS.append((rs, a, b_, nmg, ca - cb))
        print(f"sqrt(s) = {rs:4.1f}, omega in [{a:.2f}, {b_:.2f}): MadGraph {nmg:.4e} pb, quadrature {ca - cb:.4e} pb, ratio {nmg / (ca - cb):.3f}")

# %% [markdown]
# ## MadGraph's deficit: the VEGAS grid of the massive t-channel invariant
#
# MadEvent samples the t-channel invariant of the two initial-state-radiation channels as x = -t/s (t = (p_1 - k)^2 and
# (p_1 - k_1 - k_2)^2) on a VEGAS grid started logarithmic above x_o = 0.1^2/s, the grid of a massless propagator
# (SubProcesses/myamp.f, setgrid itype 1 of Source/dsample.f, which ignores the pole offset -m_e^2/s).  The electron pole is
# at x = -m_e^2/s, so the photons with y = min(2 p_1.k, 2 p_2.k)/m_e^2 < 1 (x < 0) start in one grid bin.  The LHE files of the
# main runs and of the same runs with the grid of mg5_tpole.py (logarithmic in x + m_e^2/s) are binned in y against the
# quadrature with the cut y > y_c.  The same grid for the tree-level processes of step (2), Compton scattering among them
# (backward u-channel pole at u = m_e^2): tree_sigma.py.

# %%
tp_log = open(os.path.join(HERE, "work", "xsec_mg5_tpole.log")).read()
tp_err = [float(b) for b in re.findall(r"Cross-section :\s+\S+\s+\+-\s+(\S+)\s+pb", tp_log)]


def banner_sigma(d, run):
    """the integrated weight of a MadEvent run (pb), to more digits than the log"""
    path = os.path.join(HERE, "work", d, "Events", run, f"{run}_tag_1_banner.txt")
    return float(re.search(r"Integrated weight \(pb\)\s*:\s*(\S+)", open(path).read()).group(1))


tp_sig = [(banner_sigma("mg5_xsec3_tpole", f"run_{i:02d}"), tp_err[i - 1]) for i in (1, 2, 3)]


def lhe_y(path, rs):
    """y = min(2 p_1.k, 2 p_2.k)/m_e^2 = 2 (E omega - |p| |k_z|)/m_e^2 of the photons of an LHE file"""
    e = rs / 2
    p = math.sqrt(e * e - ME ** 2)
    ys = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            f = line.split()
            if len(f) > 9 and f[0] == "22" and f[1] == "1":
                ys.append(2 * (e * float(f[9]) - p * abs(float(f[8]))) / ME ** 2)
    return np.array(ys)


Y_EDGES = (0.0, 0.1, 0.3, 1.0, 3.0, 10.0, math.inf)
TPOLE = {}
for i, rs in enumerate(SQRTS):
    cum = [HARD[(rs, DE_MG)][0] * PB] + [hard(rs, DE_MG, *GRID, ycut=y)[0] * PB for y in Y_EDGES[1:-1]] + [0.0]
    ours = np.array(cum[:-1]) - np.array(cum[1:])
    sg, er = tp_sig[i]
    a, da, _ = lhe_afb(os.path.join(HERE, "work", "mg5_xsec3_tpole", "Events", f"run_{i + 1:02d}", "unweighted_events.lhe.gz"))
    TPOLE[rs] = {"sigma": sg, "err": er, "afb": a, "afb_err": da, "share": ours / cum[0]}
    print(f"sqrt(s) = {rs:4.1f}: sigma_H MadGraph with the t-pole grid {sg:.4e} +- {er:.1e} pb, quadrature {cum[0]:.4e} pb "
          f"({sg / cum[0] - 1:+.2%}, {(sg - cum[0]) / er:+.1f} sigma);  A_FB(hard) {a:+.4f} +- {da:.4f}")
    print("    y bins            " + "  ".join(f"[{lo:g},{hi:g})" for lo, hi in zip(Y_EDGES[:-1], Y_EDGES[1:])))
    print("    share of sigma_H  " + "  ".join(f"{x:.3f}" for x in TPOLE[rs]["share"]))
    for tag, d, sm in (("original", "mg5_xsec3", MG[rs]["sigma"]), ("t-pole", "mg5_xsec3_tpole", sg)):
        y = lhe_y(os.path.join(HERE, "work", d, "Events", f"run_{i + 1:02d}", "unweighted_events.lhe.gz"), rs)
        cnt = np.array([((y >= lo) & (y < hi)).sum() for lo, hi in zip(Y_EDGES[:-1], Y_EDGES[1:])])
        with np.errstate(divide="ignore", invalid="ignore"):          # empty bins (y >= 3 at sqrt(s) = 4) give nan
            TPOLE[rs][tag] = (cnt / len(y) * sm / ours, np.sqrt(np.maximum(cnt, 1)) / len(y) * sm / ours)
        print(f"    MadGraph/ours, {tag:8s} grid: " + "  ".join(f"{r:.3f}+-{dr:.3f}" for r, dr in zip(*TPOLE[rs][tag])))


def grid_y1(d, g, rs):
    """y of the first edge x_1 of the t-channel grid (index 2) of channel g after the survey (G*/ftn26): the first bin is [-1, x_1]"""
    v = open(os.path.join(HERE, "work", d, "SubProcesses", "P1_emep_mummupa", g, "ftn26")).read().split()
    return (float(v[96]) * rs * rs + ME ** 2) / ME ** 2


# the grid after the last run of each directory (G3, G4: the two initial-state-radiation channels); the part of the phase
# space between the kinematic end and x_1 lies in the wide first bin and is rarely sampled
for d, rs, label in (("mg5_xsec3", 6.0, "original grid (last run sqrt(s) = 6, sde_strategy 2)"),
                     ("mg5_xsec3_tpole", 10.0, "t-pole grid (last run sqrt(s) = 10)")):
    e = rs / 2
    ymin = 2 * DE_MG * (e - math.sqrt(e * e - ME ** 2)) / ME ** 2
    y1 = min(grid_y1(d, g, rs) for g in ("G3", "G4"))
    share = 1 - hard(rs, DE_MG, *GRID, ycut=y1)[0] / HARD[(rs, DE_MG)][0]
    print(f"{label}: first grid edge y_1 = {y1:.3f} (smaller of G3, G4), kinematic end y = {ymin:.4f} (omega = DeltaE); "
          f"share of sigma_H with y < y_1: {share:.3f}")


# %% [markdown]
# ## The order-alpha^3 cross section and A_FB

# %%
rows = []
for rs in SQRTS:
    # forward (cos > 0) and backward sums: Born, 2 Re W (CDR, four-dimensional), Born x S_pole, Born x Atil, -8 S_pole (CDR)
    acc = {k: np.zeros(2) for k in ("born", "vcdr", "v4", "spole", "satil", "cdrb")}
    for c, wgt in zip(CN, CW):
        v, so = VIRT[(rs, round(c, 12))], SOFT[(rs, round(c, 12))]
        e = rs / 2
        pre = wgt * 2 * math.pi / (64 * math.pi ** 2 * v["s"]) * math.sqrt(e * e - MMU ** 2) / math.sqrt(e * e - ME ** 2) / 4
        b4 = born4(v["s"], v["t"])
        h = 0 if c > 0 else 1
        acc["born"][h] += pre * b4
        acc["vcdr"][h] += pre * 2 * v["fin"].real / KK
        acc["v4"][h] += pre * 2 * v["fin4"].real / KK
        acc["spole"][h] += pre * b4 * so["pole"]
        acc["satil"][h] += pre * b4 * so["atil"]
        acc["cdrb"][h] += pre * (-8 * so["pole"])        # B(D) S = (B(4) - 8 eps) (S_pole/eps + ...): -8 e^4 S_pole
    sb = acc["born"].sum()
    for de in DES:
        h, hf = HARD[(rs, de)]
        hfb = np.array([hf, h - hf])
        s4 = acc["spole"] * math.log(1 / de ** 2) - acc["satil"]       # sigma_S (F, B), four-dimensional spin sums
        sc = s4 + acc["cdrb"]                                           # sigma_S in CDR
        t4, tc = acc["v4"] + s4 + hfb, acc["vcdr"] + sc + hfb
        rows.append({"sqrts": rs, "DeltaE": de, "sigma_B": sb, "sigma_V4": acc["v4"].sum(), "sigma_Vcdr": acc["vcdr"].sum(),
                     "sigma_S4": s4.sum(), "sigma_Scdr": sc.sum(), "sigma_H": h, "sigma_H_err": HARD[(rs, de, "err")][0],
                     "delta4": t4.sum() / sb, "delta_cdr": tc.sum() / sb, "afb4": (t4[0] - t4[1]) / sb, "afb_cdr": (tc[0] - tc[1]) / sb,
                     "afb_V": (acc["v4"][0] - acc["v4"][1]) / sb, "afb_S": (s4[0] - s4[1]) / sb, "afb_H": (hfb[0] - hfb[1]) / sb})
print(f"{'sqrt s':>6} {'DeltaE':>7} {'sigma_B (pb)':>13} {'delta_V':>9} {'delta_S':>9} {'delta_H':>9} {'delta (4-dim)':>14} {'delta (CDR)':>13} {'A_FB':>9}")
for r in rows:
    print(f"{r['sqrts']:6.1f} {r['DeltaE']:7.3f} {r['sigma_B'] * PB:13.6e} {r['sigma_V4'] / r['sigma_B']:+9.5f} {r['sigma_S4'] / r['sigma_B']:+9.5f} "
          f"{r['sigma_H'] / r['sigma_B']:+9.5f} {r['delta4']:+14.8f} {r['delta_cdr']:+13.8f} {r['afb4']:+9.6f}")
kpi = {rs: 4 / 3 * (math.log(1 / ME ** 2) + math.log(1 / MMU ** 2)) for rs in SQRTS}   # -K Pi^R(0) at mu = 1
for rs in SQRTS:
    r = [x for x in rows if x["sqrts"] == rs]
    # the soft approximation leaves O(DeltaE): with DeltaE = 0.003, 0.001 (ratio 3) the linear extrapolation to DeltaE = 0 is
    # x(0) = x(0.001) - [x(0.003) - x(0.001)]/2
    d0 = r[-1]["delta4"] - (r[-2]["delta4"] - r[-1]["delta4"]) / 2
    a0 = r[-1]["afb4"] - (r[-2]["afb4"] - r[-1]["afb4"]) / 2
    for x in r:
        x["delta0"], x["afb0"] = d0, a0
    print(f"sqrt(s) = {rs:4.1f}: delta(DeltaE -> 0) = {d0:+.6f} (MS-bar e(1)), {d0 + 2 * kpi[rs] / KK:+.6f} (alpha(0));  "
          f"A_FB(DeltaE -> 0) = {a0:+.6f};  delta(0.001) - delta(0) = {r[-1]['delta4'] - d0:.1e};  "
          f"CDR - 4-dim: {max(abs(x['delta4'] - x['delta_cdr']) for x in r):.1e}")

# %%
with open(os.path.join(HERE, "results", "xsec.csv"), "w", newline="") as fh:
    keys = list(rows[0].keys())
    w = csv.writer(fh)
    w.writerow(keys)
    w.writerows([[r[k] for k in keys] for r in rows])
print("wrote results/xsec.csv")

# %% [markdown]
# ## Figure: soft and hard photons against DeltaE

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
COLORS = {"S": "C0", "H": "C1", "SH": "C2"}     # colors of physrev.mplstyle
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.4), sharey=False)
for ax, rs in zip(axes, SQRTS):
    r = [x for x in rows if x["sqrts"] == rs]
    de = np.array([x["DeltaE"] for x in r])
    ds, dh = np.array([x["sigma_S4"] / x["sigma_B"] for x in r]), np.array([x["sigma_H"] / x["sigma_B"] for x in r])
    ax.plot(de, ds, color=COLORS["S"], lw=0.75, ls="--", marker="o", ms=2.4, label="soft")
    ax.plot(de, dh, color=COLORS["H"], lw=0.75, ls=":", marker="s", ms=2.4, label="hard")
    ax.plot(de, ds + dh, color=COLORS["SH"], lw=1, ls="-", marker="D", ms=2.4, label="soft + hard")
    ax.set_xscale("log")
    ax.set_xlabel(r"$\Delta E$")
    ax.set_title(rf"$\sqrt{{s}}={rs:g}$", fontsize=8)
    ax.annotate("soft + hard", (de[-1], (ds + dh)[-1]), textcoords="offset points", xytext=(4, 6), fontsize=7, color="0.25")
axes[0].set_ylabel(r"$\sigma/\sigma_B$ (four-dimensional spin sums)")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", bbox_to_anchor=(0.5, 0.93), ncol=3,
           frameon=False, fontsize=6.5)
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "xsec_softhard.pdf"))
if INTERACTIVE:
    plt.show()
print("wrote ../figs/xsec_softhard.pdf")
