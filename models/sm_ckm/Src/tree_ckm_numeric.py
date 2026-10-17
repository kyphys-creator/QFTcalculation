#!/usr/bin/env python3
"""Step (2) of the CKM note: tree-level numbers with the CKM matrix, explicit matrices (no FeynCalc, no MadGraph).

The Dirac matrices, spinors, polarization vectors and the benchmark of the SM note are imported from
models/sm/Src/tree_numeric.py (the SM note's step (2)); the CKM matrix is Eq. (Vstd) at the benchmark Eq. (bench).
1. Explicit-matrix sum|M|^2 against tree_ckm_feyncalc.wl (results/tree_ckm_points.csv), Gamma = 0 there:
   u dbar -> nu_e e+ and u sbar -> nu_e e+ (massless, s-channel W), u ubar -> d sbar (massless, t-channel W), and
   t sbar -> W+ H with m_t, m_s in unitary gauge (s-channel W, t-channel top, u-channel s; FeynCalc used R_xi).
   The closed forms of the note (Sec. tree) for the first three are compared too.
2. Widths: W+ -> u_i dbar_j (|V_ij|^2 times the SM note's Eq. (widths)), t -> d_j W+ (|V_tj|^2), the unitarity sums.
3. Cross sections at sqrt s = 200 GeV for MadGraph (fixed-energy parton beams, spin and colour average 1/36):
   u dbar -> e+ nu_e, u sbar -> e+ nu_e with the W width of the param card in the s channel; u ubar -> d sbar
   (t-channel W without width, as MadGraph's default zerowidth_tchannel).
Output: results/tree_ckm_numeric.csv
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
RES.mkdir(exist_ok=True)
sys.path.insert(0, str(HERE.parent.parent / "sm" / "Src"))
import tree_numeric as smt  # noqa: E402  (the SM note's step (2): benchmark, Dirac algebra, widths)

ee, MW, sw = smt.ee, smt.MW, smt.sw
g = ee / sw
vev = smt.vev
MH, WW = 125.0, 2.085                      # W width of the param card (s-channel propagator only)
MASS = smt.MASS
UP, DN = ["u", "c", "t"], ["d", "s", "b"]


def ckm(s12, s23, s13, dl):
    """PDG standard parametrization, Eq. (Vstd) (rows u, c, t; columns d, s, b)."""
    c12, c23, c13 = (math.sqrt(1 - x**2) for x in (s12, s23, s13))
    e = np.exp(1j * dl)
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


V = ckm(0.22501, 0.04183, 0.003732, 1.147)
GAM, PL, slash, dot = smt.GAM, smt.PL, smt.slash, smt.dot
XI = smt.XI


def spinors_u(p):
    return [smt.u_spinor(p, x) for x in XI]


def spinors_vbar(p):
    return [smt.bar(smt.v_spinor(p, x)) for x in XI]


def spinors_ubar(p):
    return [smt.bar(smt.u_spinor(p, x)) for x in XI]


def spinors_v(p):
    return [smt.v_spinor(p, x) for x in XI]


def massless_kin(sqrt_s, cos_t):
    E = sqrt_s / 2
    sin_t = math.sqrt(1 - cos_t**2)
    p1, p2 = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])
    k1 = np.array([E, E * sin_t, 0, E * cos_t])
    return p1, p2, k1, p1 + p2 - k1


# ---------------------------------------------------------------- 1. explicit matrices
def m2_ud_enu(sqrt_s, cos_t, i, j, width):
    """u_i(p1) dbar_j(p2) -> nu_e(k1) e+(k2), massless; theta between u_i and nu_e.  iM = [ubar_nu (i g/sqrt2 gamma_mu PL)
    v_e] (-i g^{mu nu}/(s - MW^2 + i MW Gamma)) [vbar_d (i g/sqrt2 conj(V_ij) gamma_nu PL) u_u]; colour sum 3."""
    p1, p2, k1, k2 = massless_kin(sqrt_s, cos_t)
    s = sqrt_s**2
    prop = -1j / (s - MW**2 + 1j * MW * width)
    tot = 0.0
    for uu in spinors_u(p1):
        for vb in spinors_vbar(p2):
            jq = np.array([vb @ GAM[m] @ PL @ uu for m in range(4)])
            for ub in spinors_ubar(k1):
                for vv in spinors_v(k2):
                    jl = np.array([ub @ GAM[m] @ PL @ vv for m in range(4)])
                    im = (1j * g / math.sqrt(2)) ** 2 * np.conj(V[i, j]) * prop * dot(jl, jq)
                    tot += abs(im) ** 2
    return 3 * tot


def m2_uu_ds(sqrt_s, cos_t):
    """u(p1) ubar(p2) -> d(k1) sbar(k2), massless; t-channel W (the k k part vanishes on massless spinors), theta
    between u and d.  iM = [ubar_d (i g/sqrt2 conj(V_ud) gamma PL) u_u] (-i/(t - MW^2)) [vbar_u (i g/sqrt2 V_us gamma PL)
    v_s]; colour sum 9."""
    p1, p2, k1, k2 = massless_kin(sqrt_s, cos_t)
    t = dot(p1 - k1, p1 - k1)
    tot = 0.0
    for uu in spinors_u(p1):
        for ub in spinors_ubar(k1):
            j1 = np.array([ub @ GAM[m] @ PL @ uu for m in range(4)])
            for vb in spinors_vbar(p2):
                for vv in spinors_v(k2):
                    j2 = np.array([vb @ GAM[m] @ PL @ vv for m in range(4)])
                    im = (1j * g / math.sqrt(2)) ** 2 * np.conj(V[0, 0]) * V[0, 1] * (-1j / (t - MW**2)) * dot(j1, j2)
                    tot += abs(im) ** 2
    return 9 * tot


def m2_ts_wh(sqrt_s, cos_t):
    """t(p1) sbar(p2) -> W+(k1) H(k2), masses mt, ms, unitary gauge, Gamma = 0; theta between t and W+.
    (a) s-channel W with -i(g - q q/MW^2)/(s - MW^2) and H W Wbar = i e MW/sw g; (b) the top emits H (-i mt/v) and
    then annihilates with sbar into W+; (c) the s quark line: W+ first, then H (-i ms/v).  Vertex dbar_s u_t Wbar:
    i g/sqrt2 conj(V_ts) gamma PL.  Colour sum 3."""
    mt, ms = MASS["t"], MASS["s"]
    s = sqrt_s**2
    pin = math.sqrt(smt.lam(s, mt**2, ms**2)) / (2 * sqrt_s)
    pout = math.sqrt(smt.lam(s, MW**2, MH**2)) / (2 * sqrt_s)
    e1, e2 = (s + mt**2 - ms**2) / (2 * sqrt_s), (s + ms**2 - mt**2) / (2 * sqrt_s)
    e3 = (s + MW**2 - MH**2) / (2 * sqrt_s)
    sin_t = math.sqrt(1 - cos_t**2)
    p1, p2 = np.array([e1, 0, 0, pin]), np.array([e2, 0, 0, -pin])
    k1 = np.array([e3, pout * sin_t, 0, pout * cos_t])
    k2 = p1 + p2 - k1
    q = p1 + p2
    wv = 1j * g / math.sqrt(2) * np.conj(V[2, 1])
    eps = smt.pol_vectors(k1, MW)
    qt, qu = p1 - k1, p1 - k2                      # internal s (diagram c) and top (diagram b)
    one = np.eye(4)
    tot = 0.0
    for uu in spinors_u(p1):
        for vb in spinors_vbar(p2):
            jq = np.array([vb @ GAM[m] @ PL @ uu for m in range(4)])
            for h in (+1, -1, 0):
                ec = eps[h].conj()
                # (a) [vbar wv gamma_mu PL u] (-i)(g^{mu nu} - q^mu q^nu/MW^2)/(s - MW^2) (i e MW/sw) e*_nu
                ia = wv * (-1j) * (dot(jq, ec) - dot(jq, q) * dot(q, ec) / MW**2) / (s - MW**2) * (1j * ee * MW / sw)
                # (b) vbar (wv e*slash PL) (i (qu slash + mt)/(qu^2 - mt^2)) (-i mt/v) u
                ib = vb @ (wv * slash(ec) @ PL) @ (1j * (slash(qu) + mt * one) / (dot(qu, qu) - mt**2)) @ (
                    -1j * mt / vev * one) @ uu
                # (c) vbar (-i ms/v) (i (qt slash + ms)/(qt^2 - ms^2)) (wv e*slash PL) u
                ic = vb @ (-1j * ms / vev * one) @ (1j * (slash(qt) + ms * one) / (dot(qt, qt) - ms**2)) @ (
                    wv * slash(ec) @ PL) @ uu
                tot += abs(ia + ib + ic) ** 2
    return 3 * tot


def closed_ud_enu(sqrt_s, cos_t, i, j, width):
    """note: N_c g^4 |V_ij|^2 u^2/|s - MW^2 + i MW Gamma|^2, u = (p_u - p_e+)^2 = -s (1 + cos theta)/2 (theta: u, nu)."""
    s = sqrt_s**2
    u = -s * (1 + cos_t) / 2
    return 3 * g**4 * abs(V[i, j]) ** 2 * u**2 / ((s - MW**2) ** 2 + (MW * width) ** 2)


def closed_uu_ds(sqrt_s, cos_t):
    """note: N_c^2 g^4 |V_ud|^2 |V_us|^2 u^2/(t - MW^2)^2, t = -s (1 - cos)/2, u = -s (1 + cos)/2 (theta: u, d)."""
    s = sqrt_s**2
    t, u = -s * (1 - cos_t) / 2, -s * (1 + cos_t) / 2
    return 9 * g**4 * abs(V[0, 0]) ** 2 * abs(V[0, 1]) ** 2 * u**2 / (t - MW**2) ** 2


# ---------------------------------------------------------------- 2. widths
def width_W_q(i, j):
    return abs(V[i, j]) ** 2 * smt.width_W(UP[i], DN[j])


def width_t_q(j):
    mt, mq = MASS["t"], MASS[DN[j]]
    xq, xw = (mq / mt) ** 2, (MW / mt) ** 2
    if mq + MW >= mt:
        return 0.0
    return abs(V[2, j]) ** 2 * ee**2 * mt**3 / (64 * math.pi * sw**2 * MW**2) * math.sqrt(smt.lam(1, xq, xw)) * (
        (1 - xq) ** 2 + xw * (1 + xq) - 2 * xw**2)


def sigma_q(m2, sqrt_s):
    """2 -> 2 massless parton cross section in pb, spin and colour average 1/36."""
    val, _ = quad(lambda c: m2(sqrt_s, c), -1, 1, epsabs=0, epsrel=1e-11, limit=200)
    return smt.GEV2_TO_PB * val / 36 / (32 * math.pi * sqrt_s**2)


def main():
    rows = []
    # 1. against FeynCalc
    fc = list(csv.DictReader(open(RES / "tree_ckm_points.csv")))
    worst = {}
    for r in fc:
        proc, rs, c, ref = r["process"], float(r["sqrt_s"]), float(r["cos_theta"]), float(r["sumM2_feyncalc"])
        if proc.startswith("u dbar"):
            mine = m2_ud_enu(rs, c, 0, 0, 0.0)
        elif proc.startswith("u sbar"):
            mine = m2_ud_enu(rs, c, 0, 1, 0.0)
        elif proc.startswith("u ubar"):
            mine = m2_uu_ds(rs, c)
        else:
            mine = m2_ts_wh(rs, c)
        worst[proc] = max(worst.get(proc, 0.0), abs(mine / ref - 1))
    for proc, w in worst.items():
        print("explicit matrices vs FeynCalc  %-34s max relative difference %.2e" % (proc, w))
        rows.append(["matrices_vs_feyncalc_" + proc.split(" (")[0].replace(" ", "_").replace(">", ""), w])
    cl = max(max(abs(m2_ud_enu(rs, c, i, j, WW) / closed_ud_enu(rs, c, i, j, WW) - 1) for (i, j) in ((0, 0), (0, 1), (1, 2)))
             for rs in (90.0, 200.0) for c in (-0.7, 0.1, 0.8))
    cl2 = max(abs(m2_uu_ds(rs, c) / closed_uu_ds(rs, c) - 1) for rs in (200.0, 1000.0) for c in (-0.7, 0.1, 0.8))
    print("closed forms of the note vs explicit matrices: u_i dbar_j -> nu e+ %.2e, u ubar -> d sbar %.2e" % (cl, cl2))
    rows += [["closed_ud_enu_vs_matrices", cl], ["closed_uu_ds_vs_matrices", cl2]]

    # 2. widths
    wq = {(i, j): width_W_q(i, j) for i in (0, 1) for j in range(3)}
    wl = {f: smt.width_W(n, f) for n, f in (("ve", "e"), ("vm", "mu"), ("vt", "ta"))}
    for (i, j), w in wq.items():
        rows.append(["width_W_%s_%s~" % (UP[i], DN[j]), w])
    for f, w in wl.items():
        rows.append(["width_W_lep_%s" % f, w])
    tot = sum(wq.values()) + sum(wl.values())
    rows.append(["width_W_total", tot])
    had = sum(wq.values())
    had_v1 = smt.width_W("u", "d") + smt.width_W("c", "s")
    had0 = 2 * 3 * ee**2 * MW / (48 * math.pi * sw**2)
    print("Gamma(W -> hadrons): CKM %.10e, V = 1 %.10e GeV (rel. %.2e, from the quark masses); massless 2 N_c Gamma_0 = %.10e"
          % (had, had_v1, had / had_v1 - 1, had0))
    rows += [["width_W_hadrons", had], ["width_W_hadrons_V1", had_v1]]
    wt = [width_t_q(j) for j in range(3)]
    for j in range(3):
        rows.append(["width_t_%sW" % DN[j], wt[j]])
    print("Gamma(t -> d_j W+) = %s GeV; sum %.10e, V = 1 (t -> b W+) %.10e (rel. %.2e, from m_d, m_s vs m_b)"
          % (", ".join("%.6e" % x for x in wt), sum(wt), smt.width_t(), sum(wt) / smt.width_t() - 1))
    rows += [["width_t_total", sum(wt)], ["width_t_bW_V1", smt.width_t()]]

    # 3. cross sections for MadGraph
    for (i, j, name) in ((0, 0, "udbar_enu"), (0, 1, "usbar_enu")):
        sv = sigma_q(lambda r, c: closed_ud_enu(r, c, i, j, WW), 200.0)
        sm_ = sigma_q(lambda r, c: m2_ud_enu(r, c, i, j, WW), 200.0)
        print("sigma(%s, 200 GeV) = %.8e pb (closed form), %.8e pb (explicit matrices)" % (name, sv, sm_))
        rows.append(["sigma_%s_200_pb" % name, sv])
    sv = sigma_q(closed_uu_ds, 200.0)
    print("sigma(u ubar -> d sbar, 200 GeV) = %.8e pb" % sv)
    rows.append(["sigma_uubar_dsbar_200_pb", sv])
    with open(RES / "tree_ckm_numeric.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "value"])
        for r in rows:
            w.writerow([r[0], "%.15e" % r[1]])


if __name__ == "__main__":
    main()
