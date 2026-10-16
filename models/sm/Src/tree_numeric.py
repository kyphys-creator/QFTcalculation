#!/usr/bin/env python3
"""Step (2) of the SM note: tree-level numbers with explicit matrices (no FeynCalc, no MadGraph).

1. e-(p1) e+(p2) -> W-(k1) W+(k2) (massless electron) from the Feynman rules of the note (Tables rules-f,
   rules-sv): explicit Dirac matrices (chiral basis), spinors u = (sqrt(p.sigma) xi, sqrt(p.sigmabar) xi),
   v = (sqrt(p.sigma) eta, -sqrt(p.sigmabar) eta), helicity polarization vectors.  sum|M|^2 over all spins and
   polarizations is compared with tree_feyncalc.wl (results/tree_eeww_points.csv).
2. The longitudinal W pair: each of the three diagrams (nu t-channel, photon, Z) grows like s/MW^2; the
   coefficients are in the ratio 1/(2 sw^2) : Q_e : (cw/sw) g_L^e for a left-handed electron and 0 : Q_e :
   (cw/sw) g_R^e for a right-handed one, and both sums vanish (note Sec. tree).  Checked up to sqrt s = 30 TeV.
3. Widths of W, Z, H, t (Eq. (widths)) and the cross sections of e+ e- -> mu+ mu- (Eq. (eeff) with the Z width of
   the param card) and e+ e- -> W+ W- (from 1.) at the benchmark, for the MadGraph comparison (run_tree_check.sh).

Benchmark (note, assumption 7): 1/alpha = 128, MW = 80, MZ = 91, MH = 125, MT = 165, MB = 2.86, ... GeV.
Output: results/tree_numeric.csv
"""
import csv
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
RES.mkdir(exist_ok=True)

# ---------------------------------------------------------------- benchmark (MS-bar values)
ee = math.sqrt(4 * math.pi / 128.0)
MW, MZ, MH = 80.0, 91.0, 125.0
cw = MW / MZ
sw = math.sqrt(1 - cw**2)
vev = 2 * MW * sw / ee
WZ = 2.4955                                          # Z width of the param card (only in the s-channel propagator)
MASS = {"e": 0.000487, "mu": 0.1027, "ta": 1.746, "u": 0.00127, "c": 0.619, "t": 165.0,
        "d": 0.00271, "s": 0.0546, "b": 2.86}
FERM = {  # name: (Q, T3, Nc)
    "ve": (0, 0.5, 1), "vm": (0, 0.5, 1), "vt": (0, 0.5, 1),
    "e": (-1, -0.5, 1), "mu": (-1, -0.5, 1), "ta": (-1, -0.5, 1),
    "u": (2 / 3, 0.5, 3), "c": (2 / 3, 0.5, 3), "t": (2 / 3, 0.5, 3),
    "d": (-1 / 3, -0.5, 3), "s": (-1 / 3, -0.5, 3), "b": (-1 / 3, -0.5, 3)}


def mass(f):
    return MASS.get(f, 0.0)


def gL(f):
    q, t3, _ = FERM[f]
    return (t3 - q * sw**2) / (sw * cw)


def gR(f):
    q, _, _ = FERM[f]
    return -q * sw / cw


def lam(a, b, c):
    return a * a + b * b + c * c - 2 * a * b - 2 * b * c - 2 * c * a


# ---------------------------------------------------------------- Eq. (widths)
def width_W(f1, f2):
    x1, x2 = (mass(f1) / MW) ** 2, (mass(f2) / MW) ** 2
    if math.sqrt(x1) + math.sqrt(x2) >= 1:
        return 0.0
    return FERM[f1][2] * ee**2 * MW / (48 * math.pi * sw**2) * math.sqrt(lam(1, x1, x2)) * (
        1 - (x1 + x2) / 2 - (x1 - x2) ** 2 / 2)


def width_Z(f):
    x = (mass(f) / MZ) ** 2
    if 4 * x >= 1:
        return 0.0
    beta = math.sqrt(1 - 4 * x)
    return FERM[f][2] * ee**2 * MZ / (24 * math.pi) * beta * (
        (gL(f) ** 2 + gR(f) ** 2) * (1 - x) + 6 * gL(f) * gR(f) * x)


def width_H(f):
    m = mass(f)
    if 2 * m >= MH:
        return 0.0
    return FERM[f][2] * m**2 * MH / (8 * math.pi * vev**2) * (1 - 4 * m**2 / MH**2) ** 1.5


def width_t():
    mt, mb = MASS["t"], MASS["b"]
    xb, xw = (mb / mt) ** 2, (MW / mt) ** 2
    return ee**2 * mt**3 / (64 * math.pi * sw**2 * MW**2) * math.sqrt(lam(1, xb, xw)) * (
        (1 - xb) ** 2 + xw * (1 + xb) - 2 * xw**2)


# ---------------------------------------------------------------- explicit matrices
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]], dtype=complex),
       np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
GAM = [np.block([[Z2, I2], [I2, Z2]])] + [np.block([[Z2, s], [-s, Z2]]) for s in SIG]
G5 = np.block([[-I2, Z2], [Z2, I2]])
PL, PR = (np.eye(4) - G5) / 2, (np.eye(4) + G5) / 2
METRIC = np.diag([1.0, -1.0, -1.0, -1.0])


def slash(p):
    return sum(METRIC[m, m] * p[m] * GAM[m] for m in range(4))


def dot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def sqrtm_psd(a):
    w, v = np.linalg.eigh(a)
    return v @ np.diag(np.sqrt(np.clip(w, 0, None))) @ v.conj().T


def psig(p):
    return p[0] * I2 - sum(p[i + 1] * SIG[i] for i in range(3))


def psigbar(p):
    return p[0] * I2 + sum(p[i + 1] * SIG[i] for i in range(3))


XI = [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]


def u_spinor(p, xi):
    return np.concatenate([sqrtm_psd(psig(p)) @ xi, sqrtm_psd(psigbar(p)) @ xi])


def v_spinor(p, eta):
    return np.concatenate([sqrtm_psd(psig(p)) @ eta, -sqrtm_psd(psigbar(p)) @ eta])


def bar(sp):
    return sp.conj() @ GAM[0]


def pol_vectors(k, m):
    """helicity +1, -1, 0 polarization vectors of a massive vector with momentum k (contravariant components)."""
    kv = np.array(k[1:])
    kk = np.linalg.norm(kv)
    n = kv / kk
    th, ph = math.acos(max(-1.0, min(1.0, n[2]))), math.atan2(n[1], n[0])
    e1 = np.array([math.cos(th) * math.cos(ph), math.cos(th) * math.sin(ph), -math.sin(th)])
    e2 = np.array([-math.sin(ph), math.cos(ph), 0.0])
    eps = {}
    for h in (+1, -1):
        sv = -h * (e1 + 1j * h * e2) / math.sqrt(2)
        eps[h] = np.concatenate([[0.0], sv])
    eps[0] = np.concatenate([[kk / m], k[0] / m * n])
    return eps


def lower(a):
    return METRIC @ a


def gamma_vvv(p1, p2, p3):
    """Gamma^{mu1 mu2 mu3}(p1, p2, p3) of Eq. (GammaS) as a rank-3 array with upper indices."""
    g = np.diag([1.0, -1.0, -1.0, -1.0])  # g^{mu nu}
    t = np.zeros((4, 4, 4), dtype=complex)
    t += np.einsum("ab,c->abc", g, p1 - p2)
    t += np.einsum("bc,a->abc", g, p2 - p3)
    t += np.einsum("ca,b->abc", g, p3 - p1)
    return t


def eeww_amplitudes(sqrt_s, cos_t, he=None, hw=None):
    """three diagrams M_nu, M_gamma, M_Z of e-(p1) e+(p2) -> W-(k1) W+(k2), summed over the requested helicities.
    he: list of (xi, eta) index pairs for the electron and positron spin basis; hw: list of (h1, h2)."""
    s = sqrt_s**2
    E = sqrt_s / 2
    beta = math.sqrt(1 - 4 * MW**2 / s)
    sin_t = math.sqrt(1 - cos_t**2)
    p1 = np.array([E, 0, 0, E])
    p2 = np.array([E, 0, 0, -E])
    k1 = np.array([E, E * beta * sin_t, 0, E * beta * cos_t])
    k2 = p1 + p2 - k1
    q = p1 + p2
    g = ee / sw
    eps1, eps2 = pol_vectors(k1, MW), pol_vectors(k2, MW)
    vtx_gamma = gamma_vvv(q, -k1, -k2)            # {A, W, Wbar}, W creates W-(k1), Wbar creates W+(k2)
    out = []
    he = he or [(a, b) for a in range(2) for b in range(2)]
    hw = hw or [(a, b) for a in (+1, -1, 0) for b in (+1, -1, 0)]
    for (i, j) in he:
        u1 = u_spinor(p1, XI[i])
        v2b = bar(v_spinor(p2, XI[j]))
        for (h1, h2) in hw:
            e1c, e2c = eps1[h1].conj(), eps2[h2].conj()
            # t channel: vbar (i g/sqrt2 e2*slash P_L) (i (p1-k1)slash/t) (i g/sqrt2 e1*slash P_L) u
            tt = dot(p1 - k1, p1 - k1)
            i_mnu = v2b @ (1j * g / math.sqrt(2) * slash(e2c) @ PL) @ (1j * slash(p1 - k1) / tt) @ (
                1j * g / math.sqrt(2) * slash(e1c) @ PL) @ u1
            # boson current J^sigma = Gamma^{sigma mu nu} e1*_mu e2*_nu (indices lowered on the polarizations)
            J = np.einsum("smn,m,n->s", vtx_gamma, lower(e1c), lower(e2c))
            Jl = lower(J)
            cur_A = np.array([v2b @ GAM[m] @ u1 for m in range(4)])
            cur_Z = np.array([v2b @ GAM[m] @ (gL("e") * PL + gR("e") * PR) @ u1 for m in range(4)])
            # photon: (i e Q_e gamma_rho) (-i g^{rho sigma}/s) (-i e Gamma)
            i_mA = (1j * ee * (-1)) * (-1j / s) * (-1j * ee) * (cur_A @ Jl)
            # Z (Feynman gauge; the k k part vanishes on the massless current): (i e gamma(gL PL + gR PR))
            #   (-i/(s - MZ^2 + i MZ WZ)) (-i e cw/sw Gamma)
            i_mZ = (1j * ee) * (-1j / (s - MZ**2 + 1j * MZ * WZ)) * (-1j * ee * cw / sw) * (cur_Z @ Jl)
            out.append((i_mnu / 1j, i_mA / 1j, i_mZ / 1j))
    return out


def eeww_sum_m2(sqrt_s, cos_t, width_z=True):
    global WZ
    keep = WZ
    if not width_z:
        WZ = 0.0
    tot = sum(abs(a + b + c) ** 2 for (a, b, c) in eeww_amplitudes(sqrt_s, cos_t))
    WZ = keep
    return tot


def eemm_sum_m2(s, cos_t):
    """Eq. (eeff) for e+ e- -> mu+ mu- (massless), Z width WZ."""
    t = -s / 2 * (1 - cos_t)
    u = -s / 2 * (1 + cos_t)
    prop = 1 / (s - MZ**2 + 1j * MZ * WZ)
    gl, gr = gL("e"), gR("e")
    A = {(a, b): 1 / s + ca * cb * prop for (a, ca) in (("L", gl), ("R", gr)) for (b, cb) in (("L", gl), ("R", gr))}
    return 4 * ee**4 * (u**2 * (abs(A["L", "L"]) ** 2 + abs(A["R", "R"]) ** 2) +
                        t**2 * (abs(A["L", "R"]) ** 2 + abs(A["R", "L"]) ** 2))


GEV2_TO_PB = 0.3893793721e9


def sigma(sum_m2, sqrt_s, m_final):
    """2 -> 2 cross section from sum|M|^2 (spin average 1/4), massless initial state."""
    s = sqrt_s**2
    beta = math.sqrt(lam(1, (m_final / sqrt_s) ** 2, (m_final / sqrt_s) ** 2))
    val, _ = quad(lambda c: sum_m2(sqrt_s, c), -1, 1, epsabs=0, epsrel=1e-11, limit=200)
    return GEV2_TO_PB * val / 4 * beta / (32 * math.pi * s)


def main():
    rows = []
    # 1. e+ e- -> W+ W- against FeynCalc (Gamma_Z = 0 there)
    fc = list(csv.DictReader(open(RES / "tree_eeww_points.csv")))
    worst = 0.0
    for r in fc:
        rs, c, ref = float(r["sqrt_s"]), float(r["cos_theta"]), float(r["sumM2_feyncalc"])
        mine = eeww_sum_m2(rs, c, width_z=False)
        worst = max(worst, abs(mine / ref - 1))
    print("e+ e- -> W+ W-: explicit matrices vs FeynCalc at %d points, max relative difference %.2e"
          % (len(fc), worst))
    rows.append(["eeww_matrices_vs_feyncalc_maxrel", worst])

    # 2. longitudinal W pairs: e_L- e_R+ (xi = (1,0) for the electron is helicity -1 along +z in this basis)
    print("longitudinal W pair, cos theta = 0.3:  sqrt s,  M_nu, M_gamma, M_Z (in units of s/MW^2),  |sum|")
    ratio_ref_L = np.array([1 / (2 * sw**2), -1.0, cw / sw * gL("e")])
    ratio_ref_R = np.array([0.0, -1.0, cw / sw * gR("e")])
    for rs in (200.0, 1000.0, 3000.0, 30000.0):
        for (label, he) in (("e-_L e+_R", [(1, 0)]), ("e-_R e+_L", [(0, 1)])):
            (mnu, ma, mz), = eeww_amplitudes(rs, 0.3, he=he, hw=[(0, 0)])
            norm = rs**2 / MW**2
            print("  %7.0f %s  %+.6e %+.6e %+.6e   |sum| = %.3e" % (rs, label, abs(mnu) / norm, abs(ma) / norm,
                                                                     abs(mz) / norm, abs(mnu + ma + mz)))
            rows.append(["eeww_LL_%s_%g_abs_sum" % (label.replace(" ", ""), rs), abs(mnu + ma + mz)])
            if rs == 30000.0:
                vec = np.array([mnu, ma, mz])
                ref = ratio_ref_L if label.startswith("e-_L") else ratio_ref_R
                k = np.argmax(np.abs(ref))
                rat = (vec / vec[k]).real * ref[k]
                print("     ratio of the s/MW^2 coefficients at 30 TeV:", np.round(rat, 6), " hand:", np.round(ref, 6))
                rows.append(["eeww_ratio_%s_maxdev" % label.replace(" ", ""), float(np.max(np.abs(rat - ref)))])

    # 3. widths and cross sections for MadGraph
    wW = {"ve e+": width_W("ve", "e"), "vm mu+": width_W("vm", "mu"), "vt ta+": width_W("vt", "ta"),
          "u d~": width_W("u", "d"), "c s~": width_W("c", "s")}
    wZ = {f: width_Z(f) for f in FERM if f != "t"}
    wH = {f: width_H(f) for f in ("b", "c", "ta", "mu", "s", "d", "u", "e")}
    wt = width_t()
    for name, d in (("W", wW), ("Z", wZ), ("H", wH)):
        for ch, val in d.items():
            rows.append(["width_%s_%s" % (name, ch.replace(" ", "_")), val])
        rows.append(["width_%s_total" % name, sum(d.values())])
        print("Gamma(%s) total %.10e GeV" % (name, sum(d.values())))
    rows.append(["width_t_bW", wt])
    print("Gamma(t -> b W+) %.10e GeV" % wt)
    for rs in (200.0,):
        sv = sigma(lambda r, c: eemm_sum_m2(r * r, c), rs, 0.0)
        rows.append(["sigma_eemm_%g_pb" % rs, sv])
        print("sigma(e+ e- -> mu+ mu-, sqrt s = %g) = %.8e pb" % (rs, sv))
    for rs in (200.0, 500.0):
        sv = sigma(lambda r, c: eeww_sum_m2(r, c), rs, MW)
        rows.append(["sigma_eeww_%g_pb" % rs, sv])
        print("sigma(e+ e- -> W+ W-, sqrt s = %g) = %.8e pb" % (rs, sv))
    with open(RES / "tree_numeric.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "value"])
        for r in rows:
            w.writerow([r[0], "%.15e" % r[1]])


if __name__ == "__main__":
    main()
