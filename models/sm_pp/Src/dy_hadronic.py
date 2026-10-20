"""Research note models/sm_pp, step (1c): the Drell-Yan cross sections at LO and NLO in QCD from the note's coefficient functions
(dy_feyncalc.wl), convolved with NNPDF4.0 NLO (LHAPDF 331700, alpha_s from the set), against aMC@NLO at fixed order (dy_mg5.sh).

  dsigma/dQ^2 = (sigma_0(Q^2)/Q^2) sum_pairs { 2 [G_qqbar (x) Delta_qqbar] + 2 [(G_qg + G_qbarg) (x) Delta_qg] },
  G_ij(y) = y L_ij(y) = int_{ln y}^0 dt xf_i(e^t) xf_j(y e^-t),  [G (x) Delta](tau) = int_tau^1 dz Delta(z) G(tau/z),  tau = Q^2/S,
with the plus distributions  int dz [g]_+ G(tau/z) = int_tau^1 dz g(z) (G(tau/z) - G(tau)) - G(tau) int_0^tau g.  sigma_0 is the Born
q qbar' -> V* -> leptons at shat = Q^2 in the param card's parameters (alpha(M_Z)^-1 = 132.507, G_F, M_Z; fixed widths):
  sigma_0 = (1/N_c) (Q^2/(48 pi)) sum_{i,j = L,R} |A_ij|^2,  A_ij = e^2 Q_q Q_l/Q^2 + g_Z^2 g_i^q g_j^l/(Q^2 - M_Z^2 + i M_Z Gamma_Z)
(W: A_LL = (g^2/2)/(Q^2 - M_W^2 + i M_W Gamma_W), diagonal CKM as loop_sm).  The parameters are those of the generated processes.
Checks: (1) the coefficient functions here against dy_feyncalc.wl's values (results/dy_feyncalc.csv); (2) the PDF splines against
direct LHAPDF calls; (3) the integration against doubled nodes; (4) LO and NLO against aMC@NLO, every bin and all 9 (mu_R, mu_F)
of MADatNLO.HwU.  Writes results/dy_hadronic.csv.  Run with ~/hep/opt/lhc/bin/python (NumPy, SciPy; LHAPDF of MG5's HEPTools).
"""
import csv
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

sys.path.insert(0, str(Path.home() / "hep" / "MG5_aMC_v3_8_1" / "HEPTools" / "lhapdf6_py3" / "lib" / "python3.12" / "site-packages"))
import lhapdf  # noqa: E402

SRC = Path(__file__).resolve().parent
WORK = SRC / "work" / "dy"
RES = SRC / "results"
SQRTS = 13000.0
S = SQRTS ** 2
GEV2PB = 0.3893793721e9
CF, TR, NC = 4.0 / 3.0, 0.5, 3
ZETA2 = math.pi ** 2 / 6
PDFNAME = "NNPDF40_nlo_as_01180"
# (T3, Q) and the LHAPDF id of each quark
QUARKS = {"d": (-0.5, -1 / 3, 1), "u": (0.5, 2 / 3, 2), "s": (-0.5, -1 / 3, 3), "c": (0.5, 2 / 3, 4), "b": (-0.5, -1 / 3, 5)}
ELECTRON = (-0.5, -1.0)


# ---------------------------------------------------------------- the coefficient functions (units a_s = alpha_s/(4 pi))
def dqq_delta(lf):
    return CF * (8 * ZETA2 - 16) - 6 * CF * lf


def dqq_plus0(lf):
    return -8 * CF * lf


def dqq_plus1(lf):
    return 16 * CF + 0 * lf


def dqq_reg(z, lf):
    return CF * (-8 * (1 + z) * np.log(1 - z) - 4 * (1 + z * z) * np.log(z) / (1 - z)) + 4 * CF * (1 + z) * lf


def dqg(z, lf):
    pqg = z * z + (1 - z) ** 2
    return TR * (2 * pqg * np.log((1 - z) ** 2 / z) + 1 + 6 * z - 7 * z * z) - 2 * TR * pqg * lf


def check_coefficients():
    """against results/dy_feyncalc.csv (Mathematica's values of the derived Delta^(1))"""
    rows = {r[0]: (float(r[1]), float(r[2])) for r in csv.reader(open(RES / "dy_feyncalc.csv")) if r and r[1] not in ("lF^0",) and
            not r[0].startswith("check")}
    dev = 0.0
    for name, f in (("qqbar_delta", dqq_delta), ("qqbar_plus0", dqq_plus0), ("qqbar_plus1", dqq_plus1)):
        dev = max(dev, abs(f(0.0) - rows[name][0]), abs(f(1.0) - f(0.0) - rows[name][1]))
    for name, (v0, v1) in rows.items():
        m = re.match(r"(qqbar_reg|qg)_z=(.*)", name)
        if not m:
            continue
        z = float(m.group(2))
        f = dqq_reg if m.group(1) == "qqbar_reg" else dqg
        dev = max(dev, abs(f(z, 0.0) - v0) / max(1, abs(v0)), abs(f(z, 1.0) - f(z, 0.0) - v1) / max(1, abs(v1)))
    checks = [r for r in csv.reader(open(RES / "dy_feyncalc.csv")) if r and r[0].startswith("check")]
    bad = [r[0] for r in checks if r[1] not in ("0", "0.")]
    return dev, len(checks), bad


# ---------------------------------------------------------------- the parameters of the generated processes
def param_card(path):
    vals = {}
    block = None
    for line in open(path):
        s = line.split("#")[0].split()
        if not s:
            continue
        if s[0].lower() == "block":
            block = s[1].lower()
        elif s[0].lower() == "decay":
            vals["w%s" % s[1]] = float(s[2])
        elif block in ("mass", "sminputs") and len(s) >= 2:
            vals[(block, int(s[0]))] = float(s[1])
    aew = 1 / vals[("sminputs", 1)]
    gf, mz = vals[("sminputs", 2)], vals[("mass", 23)]
    mw = math.sqrt(mz ** 2 / 2 + math.sqrt(mz ** 4 / 4 - aew * math.pi * mz ** 2 / (gf * math.sqrt(2))))
    return {"aew": aew, "mz": mz, "mw": mw, "wz": vals["w23"], "ww": vals["w24"], "sw2": 1 - mw ** 2 / mz ** 2}


def sigma0(q2, pair, ew):
    """sigma_0(Q^2) in GeV^-2 for the pair (a, bbar): ('u', 'u') gamma*/Z; ('u', 'd') W+; ('d', 'u') W-"""
    e2 = 4 * math.pi * ew["aew"]
    sw2 = ew["sw2"]
    a, b = pair
    if a == b:
        t3q, qq, _ = QUARKS[a]
        t3l, ql = ELECTRON
        gz2 = e2 / (sw2 * (1 - sw2))
        prop = 1 / (q2 - ew["mz"] ** 2 + 1j * ew["mz"] * ew["wz"])
        gq = {"L": t3q - qq * sw2, "R": -qq * sw2}
        gl = {"L": t3l - ql * sw2, "R": -ql * sw2}
        amp2 = sum(abs(e2 * qq * ql / q2 + gz2 * gq[i] * gl[j] * prop) ** 2 for i in "LR" for j in "LR")
    else:
        g2 = e2 / sw2
        amp2 = abs(g2 / 2 / (q2 - ew["mw"] ** 2 + 1j * ew["mw"] * ew["ww"])) ** 2
    return q2 / (48 * math.pi) * amp2 / NC


# ---------------------------------------------------------------- the luminosities
class Lumi:
    """G_ij(y) = y L_ij(y) at a fixed mu_F: cubic splines of xf(x) in ln x (from LHAPDF) and of G in ln y"""

    def __init__(self, pdf, muf, ymin, nx=4000, ny=700, nt=128):
        self.pdf, self.q2 = pdf, muf * muf
        # below LHAPDF's xMin = 1e-9 the set is continued by LHAPDF's extrapolator ("continuation"), as MG5 sees it
        lxmin = min(math.log(1e-9), math.log(ymin) - 1.0)
        self.lx = np.linspace(lxmin, 0.0, max(nx, int(nx * lxmin / math.log(1e-9))))
        xf = [pdf.xfxQ2(math.exp(t), self.q2) for t in self.lx]
        self.xf = {pid: CubicSpline(self.lx, [d[pid] for d in xf]) for pid in xf[0]}
        self.ly = np.linspace(math.log(ymin), 0.0, ny)
        self.tg, self.wg = np.polynomial.legendre.leggauss(nt)
        self.cache = {}

    def xfx(self, pid, lnx):
        return self.xf[pid](np.minimum(lnx, 0.0))

    def g_direct(self, i, j, ly):
        """the t integral by Gauss-Legendre (the nodes symmetric about ln y/2)"""
        ly = np.atleast_1d(ly)[:, None]
        t = 0.5 * ly * (1 + self.tg[None, :])
        w = -0.5 * ly * self.wg[None, :]
        return np.sum(w * self.xfx(i, t) * self.xfx(j, ly - t), axis=1)

    def g(self, i, j, y):
        key = (i, j)
        if key not in self.cache:
            gy = self.g_direct(i, j, self.ly[:-1])
            self.cache[key] = CubicSpline(self.ly, np.append(gy, 0.0))
        return self.cache[key](np.log(y))


def check_lumi(pdf, mu):
    """the splines against direct LHAPDF calls: xf at random x (below 0.5, and all: near x = 1 xf is tiny, b ~ 1e-9 at 0.88),
    and G_uubar by the same t integral without splines"""
    lum = Lumi(pdf, mu, 1e-8)
    rng = np.random.default_rng(1)
    dev_xf = [0.0, 0.0]
    for x in 10 ** rng.uniform(-8, -0.05, 200):
        d = pdf.xfxQ2(x, mu * mu)
        for pid in (2, -2, 21, 5):
            r = abs(lum.xfx(pid, math.log(x)) - d[pid]) / abs(d[pid])
            dev_xf = [max(dev_xf[0], r if x < 0.5 else 0.0), max(dev_xf[1], r)]
    dev_g = 0.0
    for y in 10 ** rng.uniform(-7.5, -0.5, 20):
        ly = math.log(y)
        t = 0.5 * ly * (1 + lum.tg)
        w = -0.5 * ly * lum.wg
        direct = sum(wi * pdf.xfxQ2(2, math.exp(ti), mu * mu) * pdf.xfxQ2(-2, math.exp(ly - ti), mu * mu) for ti, wi in zip(t, w))
        dev_g = max(dev_g, abs(lum.g(2, -2, y) - direct) / direct)
    return dev_xf, dev_g


# ---------------------------------------------------------------- the z convolutions
def znodes(tau, n1, n2):
    """z in (tau, 0.5) by Gauss-Legendre in ln z, (0.5, 1) through 1 - z = u^3/2 (the ln(1 - z) end point); weights include dz"""
    zs, ws = [], []
    if tau < 0.5:
        t, w = np.polynomial.legendre.leggauss(n1)
        a, b = math.log(tau), math.log(0.5)
        lz = 0.5 * (b - a) * t + 0.5 * (b + a)
        zs.append(np.exp(lz))
        ws.append(0.5 * (b - a) * w * np.exp(lz))
        lo = 0.0
    else:
        lo = (2 * (1 - tau)) ** (1 / 3)
    t, w = np.polynomial.legendre.leggauss(n2)
    hi = 1.0 if tau < 0.5 else lo
    u = 0.5 * hi * (t + 1)
    zs.append(1 - 0.5 * u ** 3)
    ws.append(0.5 * hi * w * 1.5 * u ** 2)
    return np.concatenate(zs), np.concatenate(ws)


def conv(lum, pairs_qq, pairs_qg, tau, lf, as4pi, order, n1, n2, parts=("qq", "qg")):
    """2 [G_qqbar (x) Delta_qqbar] + 2 [G_qg (x) Delta_qg] summed over the given pid pairs, at one tau (parts: the NLO
    corrections kept)"""
    gt = sum(lum.g(i, j, tau) for i, j in pairs_qq)
    tot = 2 * gt
    if order == "LO":
        return tot
    z, w = znodes(tau, n1, n2)
    gz = sum(lum.g(i, j, tau / z) for i, j in pairs_qq)
    l1 = math.log(1 - tau)
    nlo = (dqq_delta(lf) * gt
           + dqq_plus0(lf) * (np.sum(w * (gz - gt) / (1 - z)) + gt * l1)
           + dqq_plus1(lf) * (np.sum(w * (gz - gt) * np.log(1 - z) / (1 - z)) + gt * l1 * l1 / 2)
           + np.sum(w * dqq_reg(z, lf) * gz))
    gqg = sum(lum.g(i, j, tau / z) for i, j in pairs_qg)
    nlo_qg = np.sum(w * dqg(z, lf) * gqg)
    return tot + 2 * as4pi * (nlo * ("qq" in parts) + nlo_qg * ("qg" in parts))


# ---------------------------------------------------------------- the processes
def channels(proc):
    """[(sigma_0 pair, qqbar pid pairs, qg pid pairs)]"""
    if proc == "z":
        out = []
        for q, (_, _, pid) in QUARKS.items():
            out.append(((q, q), [(pid, -pid)], [(pid, 21), (-pid, 21)]))
        return out
    if proc == "wp":
        return [(("u", "d"), [(2, -1)], [(2, 21), (-1, 21)]), (("c", "s"), [(4, -3)], [(4, 21), (-3, 21)])]
    return [(("d", "u"), [(1, -2)], [(1, 21), (-2, 21)]), (("s", "c"), [(3, -4)], [(3, 21), (-4, 21)])]


def qnodes(qlo, qhi, mv, wv, nq, core=10.0, ratio=1.5):
    """Q^2 nodes and weights (dQ^2) for qlo < Q < qhi: Gauss-Legendre in the Breit-Wigner variable within M -+ core Gamma (nq
    nodes), and in ln Q^2 on geometric pieces outside it (Q_hi/Q_lo <= ratio above 10 GeV, <= 10 below; nq/2 nodes each)"""
    t, w = np.polynomial.legendre.leggauss(nq)
    tl, wl = np.polynomial.legendre.leggauss(max(8, nq // 2))
    q2s, dq2 = [], []

    def bw(a, b):
        ta, tb = math.atan((a * a - mv * mv) / (mv * wv)), math.atan((b * b - mv * mv) / (mv * wv))
        th = 0.5 * (tb - ta) * t + 0.5 * (tb + ta)
        q2s.append(mv * mv + mv * wv * np.tan(th))
        dq2.append(0.5 * (tb - ta) * w * mv * wv / np.cos(th) ** 2)

    def logs(a, b):
        e = [a]
        while e[-1] < b * (1 - 1e-12):
            e.append(min(b, e[-1] * (10.0 if e[-1] < 10.0 else ratio)))
        for lo, hi in zip(e[:-1], e[1:]):
            la, lb = 2 * math.log(lo), 2 * math.log(hi)
            l2 = 0.5 * (lb - la) * tl + 0.5 * (lb + la)
            q2s.append(np.exp(l2))
            dq2.append(0.5 * (lb - la) * wl * np.exp(l2))

    c0, c1 = mv - core * wv, mv + core * wv
    if qlo < c0:
        logs(qlo, min(qhi, c0))
    if max(qlo, c0) < min(qhi, c1):
        bw(max(qlo, c0), min(qhi, c1))
    if qhi > c1:
        logs(max(qlo, c1), qhi)
    return np.concatenate(q2s), np.concatenate(dq2)


def bin_sigma(proc, ew, lums, alphas, mur, muf, qlo, qhi, order, nq=40, n1=96, n2=64, parts=("qq", "qg")):
    """sigma (pb) with qlo < m_ll < qhi (the Q^2 nodes of qnodes)"""
    mv, wv = (ew["mz"], ew["wz"]) if proc == "z" else (ew["mw"], ew["ww"])
    lum = lums[muf]
    as4pi = alphas(mur) / (4 * math.pi)
    q2s, dq2 = qnodes(qlo, qhi, mv, wv, nq)
    tot = 0.0
    for q2, dq in zip(q2s, dq2):
        lf = math.log(muf * muf / q2)
        for pair, pqq, pqg in channels(proc):
            tot += dq * sigma0(q2, pair, ew) / q2 * conv(lum, pqq, pqg, q2 / S, lf, as4pi, order, n1, n2, parts)
    return tot * GEV2PB


# ---------------------------------------------------------------- the rapidity distribution
def r0(z, v):
    """(1 - z)^2 v (1 - v) r_qqbar at eps = 0 (dy_feyncalc.wl, (d2)); R1 at v = 0, 1 is -2 C_F (1 - z)^2"""
    return 2 * CF * ((1 - z) ** 2 * (v * v + (1 - v) ** 2) + 2 * z)


def s0(z, v):
    """(1 - z)(1 - v) r_qg at eps = 0 for q(p1) g(p2); S1 at v = 1 is -4 T_R z (1 - z)"""
    return 2 * TR * ((1 - z) ** 2 * (1 - v) ** 2 + 1 - 2 * z * (1 - z) * v)


class YLumi:
    """for one Q, one ordering (pid i from proton 1, j from proton 2) and the z rows: f(z, t) = xf_i(e^t) xf_j(tau e^-t/z) on a
    uniform t = ln x1 grid in (ln tau, 0), its cumulative integral C (Simpson), and G over a rapidity bin from the Hermite
    interpolation of C (C' = f): y = t + (1/2) ln(z/tau) + y*  ->  G_bin = C(y_hi - c) - C(y_lo - c), c = (1/2) ln(z/tau) + y*"""

    def __init__(self, lum, i, j, tau, zs, nt):
        from scipy.integrate import cumulative_simpson
        self.t0 = math.log(tau)
        self.t = np.linspace(self.t0, 0.0, nt)
        self.h = self.t[1] - self.t[0]
        lx2 = self.t0 - self.t[None, :] - np.log(zs)[:, None]
        f = lum.xfx(i, self.t)[None, :] * np.where(lx2 <= 0, lum.xfx(j, np.minimum(lx2, 0.0)), 0.0)
        self.f = f
        self.c = cumulative_simpson(f, x=self.t, axis=1, initial=0.0)

    def cum(self, rows, t):
        """C at t (clipped to the grid) for the given rows; rows and t broadcast"""
        t = np.clip(t, self.t0, 0.0)
        k = np.minimum(((t - self.t0) / self.h).astype(int), len(self.t) - 2)
        u = (t - self.t[k]) / self.h
        h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
        return (h00 * self.c[rows, k] + h10 * self.h * self.f[rows, k] + h01 * self.c[rows, k + 1]
                + h11 * self.h * self.f[rows, k + 1])

    def gbin(self, rows, cshift, edges):
        """G over the bins: rows, cshift of shape (...), edges (nb + 1) -> (..., nb)"""
        cv = self.cum(rows[..., None], edges - cshift[..., None])
        return np.diff(cv, axis=-1)


def ystar(z, v):
    return 0.5 * np.log((z + v * (1 - z)) / (1 - v * (1 - z)))


def y_conv(lum, ordering, tau, lf, edges, order, n1, n2, nv, nt):
    """the bins of [G (x) Delta] for one ordering ('qq', i, j) or ('qg', i, j) with i the quark ('gq': i the gluon), at one tau:
    (LO, NLO coefficient of a_s) arrays over the bins"""
    kind, i, j = ordering
    zs, wz = znodes(tau, n1, n2)
    zall = np.append(zs, 1.0)
    yl = YLumi(lum, i, j, tau, zall, nt)
    one = len(zs)
    c1 = 0.5 * math.log(1 / tau)
    g1 = yl.gbin(np.array(one), np.array(c1), edges)                     # G(1)
    lo = g1 if kind == "qq" else 0.0 * g1
    if order == "LO":
        return lo, 0.0 * g1
    rows = np.arange(one)
    base = 0.5 * np.log(zs / tau)
    ga = yl.gbin(rows, base + 0.5 * np.log(zs), edges)                   # v = 0
    gb = yl.gbin(rows, base - 0.5 * np.log(zs), edges)                   # v = 1
    tv, wv = np.polynomial.legendre.leggauss(nv)
    v = 0.5 * (tv + 1)
    wv = 0.5 * wv
    zz, vv = zs[:, None], v[None, :]
    gv = yl.gbin(np.broadcast_to(rows[:, None], zz.shape[:1] + vv.shape[1:]), base[:, None] + ystar(zz, vv), edges)  # (nz, nv, nb)
    l1 = math.log(1 - tau)
    zc = zs[:, None]
    if kind == "qq":
        rz0, rz1 = r0(zs, 0.0)[:, None], r0(zs, 1.0)[:, None]
        rv = r0(zz, vv)[..., None]
        vint = np.sum(wv[None, :, None] * ((rv * gv - rz0[:, None, :] * ga[:, None, :]) / vv[..., None]
                                           + (rv * gv - rz1[:, None, :] * gb[:, None, :]) / (1 - vv[..., None])), axis=1)
        brack = 2 * CF * (1 - zc) ** 2 * (ga + gb) - 2 * CF * (1 + zc * zc) * np.log(zc) * (ga + gb) + vint
        nlo = dqq_delta(lf) * g1 + np.sum(wz[:, None] * brack / (1 - zc), axis=0)
        x = (1 + zc * zc) * (ga + gb)
        x1 = 4 * g1
        pd0 = np.sum(wz[:, None] * (x - x1) / (1 - zc), axis=0) + x1 * l1
        pd1 = np.sum(wz[:, None] * (x - x1) * np.log(1 - zc) / (1 - zc), axis=0) + x1 * l1 * l1 / 2
        nlo = nlo + 4 * CF * pd1 - 2 * CF * lf * pd0
        return lo, nlo
    pz = (zc * zc + (1 - zc) ** 2)
    if kind == "qg":   # quark from proton 1: collinear at v = 1
        sv = s0(zz, vv)[..., None]
        gc = gb
        vint = np.sum(wv[None, :, None] * (sv * gv - s0(zs, 1.0)[:, None, None] * gc[:, None, :]) / (1 - vv[..., None]), axis=1)
    else:              # gluon from proton 1: v -> 1 - v, collinear at v = 0
        sv = s0(zz, 1 - vv)[..., None]
        gc = ga
        vint = np.sum(wv[None, :, None] * (sv * gv - s0(zs, 1.0)[:, None, None] * gc[:, None, :]) / vv[..., None], axis=1)
    term = 2 * TR * pz * (2 * np.log(1 - zc) - np.log(zc)) * gc + 4 * TR * zc * (1 - zc) * gc + vint - 2 * TR * lf * pz * gc
    return lo, np.sum(wz[:, None] * term, axis=0)


def orderings(proc):
    out = []
    for pair, pqq, pqg in channels(proc):
        lst = []
        for i, j in pqq:
            lst += [("qq", i, j), ("qq", j, i)]
        for i, j in pqg:
            lst += [("qg", i, j), ("gq", j, i)]
        out.append((pair, lst))
    return out


def y_sigma(proc, ew, lums, alphas, mu0, qlo, qhi, edges, order, scales, nq=40, n1=64, n2=48, nv=48, nt=400):
    """{(xi_R, xi_F): sigma in the rapidity bins (pb)} for qlo < Q < qhi"""
    mv, wv = (ew["mz"], ew["wz"]) if proc == "z" else (ew["mw"], ew["ww"])
    q2s, dq2 = qnodes(qlo, qhi, mv, wv, nq)
    res = {}
    for xf in sorted({s[1] for s in scales}):
        lum = lums[xf * mu0]
        acc_lo, acc_nlo = 0.0, 0.0
        for q2, dq in zip(q2s, dq2):
            lf = math.log((xf * mu0) ** 2 / q2)
            for pair, lst in orderings(proc):
                wgt = dq * sigma0(q2, pair, ew) / q2
                for o in lst:
                    lo, nlo = y_conv(lum, o, q2 / S, lf, edges, order, n1, n2, nv, nt)
                    acc_lo = acc_lo + wgt * lo
                    acc_nlo = acc_nlo + wgt * nlo
        for xr, xf2 in scales:
            if xf2 == xf:
                as4pi = alphas(xr * mu0) / (4 * math.pi) if order == "NLO" else 0.0
                res[(xr, xf)] = (acc_lo + as4pi * acc_nlo) * GEV2PB
    return res


# ---------------------------------------------------------------- MG5's histograms
def read_hwu(path):
    """{histogram title: (column labels, rows)}: rows of [xmin, xmax, central, err, weights...]; the values are the cross sections
    in the bins (pb), not divided by the bin width"""
    text = Path(path).read_text()
    labels = [x.strip() for x in text.splitlines()[0].lstrip("#").split("&") if x.strip()]
    out = {}
    for m in re.finditer(r'<histogram>\s*\d+\s*"([^|"]*)[^"]*"\s*\n(.*?)<\\histogram>', text, re.S):
        rows = [[float(v) for v in line.split()] for line in m.group(2).strip().splitlines()]
        out[m.group(1).strip()] = (labels, rows)
    return out


def scale_columns(labels):
    """[(index, xi_R, xi_F)] of the scale-variation columns.  HwU gives the error of the central column only; the error of a
    reweighted column is taken as that error times max(1, |reweighted/central|) (scaling by the ratio alone gives errors far too
    small where the NLO cancels the LO, e.g. W below 4 GeV with mu_F = 2 M_W)"""
    cols = []
    for k, lab in enumerate(labels):
        m = re.search(r"muR=\s*([0-9.Ee+-]+)\s+muF=\s*([0-9.Ee+-]+)", lab)
        if m:
            cols.append((k, float(m.group(1)), float(m.group(2))))
    return cols


# the W tails, in the runs <run>_<order>_t only (histograms 9-13 of analysis_HwU_dy.f)
WTAILS = ["log10 mV", "mV 0-1", "mV 1-10", "mV 10-50", "mV 150-13000"]
RUNS = [  # proc, run, mll_sf, mu0, the m_V histograms, the rapidity histogram and its m_V range
    ("z", "zpeak", 50.0, 91.188, ["total", "mV 50-150", "mV 66-116"], ("yV 66-116", 66.0, 116.0)),
    ("z", "zhigh", 500.0, 1000.0, ["total", "mV 500-3500"], ("yV", 500.0, SQRTS)),
    # W: no lower cut on m_enu in MG5; from 1e-3 GeV (sigma(0.1 < m < 1 GeV) = 0.72 pb for W+ at LO, below 1e-3 GeV ~1e-5 pb)
    ("wp", "wpeak", 1e-3, 80.419002, ["total", "mV 50-150", "mV 60-100"] + WTAILS, ("yV", 1e-3, SQRTS)),
    ("wm", "wpeak", 1e-3, 80.419002, ["total", "mV 50-150", "mV 60-100"] + WTAILS, ("yV", 1e-3, SQRTS)),
]
SCALES = [(xr, xf) for xf in (1.0, 2.0, 0.5) for xr in (1.0, 2.0, 0.5)]


def main():
    RES.mkdir(exist_ok=True)
    lhapdf.setVerbosity(0)
    pdf = lhapdf.mkPDF(PDFNAME, 0)
    out = []
    dev, nchk, bad = check_coefficients()
    print("(1) coefficient functions minus dy_feyncalc.wl's values: max %.1e;  its %d checks not zero: %s" % (dev, nchk, bad or "none"))
    out.append(["check_coefficients_minus_feyncalc", "", "", "", "%.2e" % dev, "", "", ""])
    dxf, dg = check_lumi(pdf, 91.188)
    print("(2) splines minus direct LHAPDF: xf max rel %.1e (x < 0.5), %.1e (all); G_uubar max rel %.1e" % (dxf[0], dxf[1], dg))
    out.append(["check_spline_xf_xlt05_xf_all_G", "", "", "", "%.2e" % dxf[0], "%.2e" % dxf[1], "%.2e" % dg, ""])
    summary = []
    for proc, run, qmin, mu0, hists, yhist in RUNS:
        ew = param_card(WORK / proc / "Cards" / "param_card.dat")
        lums = {f * mu0: Lumi(pdf, f * mu0, qmin ** 2 / S / 2) for f in (1.0, 2.0, 0.5)}
        own_cache = {}
        ycache = {}

        def own(xr, xf, qlo, qhi, order):
            key = (xr, xf, qlo, qhi, order)
            if key not in own_cache:
                own_cache[key] = bin_sigma(proc, ew, lums, pdf.alphasQ, xr * mu0, xf * mu0, qlo, qhi, order)
            return own_cache[key]

        if proc == "z" and run == "zpeak":
            # (3) the integration: doubled nodes for the 66-116 window at NLO
            a1 = own(1.0, 1.0, 66, 116, "NLO")
            a2 = bin_sigma(proc, ew, lums, pdf.alphasQ, mu0, mu0, 66, 116, "NLO", nq=80, n1=192, n2=128)
            lum2 = {mu0: Lumi(pdf, mu0, qmin ** 2 / S / 2, nx=8000, ny=1400, nt=256)}
            a3 = bin_sigma(proc, ew, lum2, pdf.alphasQ, mu0, mu0, 66, 116, "NLO")
            print("(3) Z 66-116 NLO: %.8g pb; doubled z, Q nodes %.1e, doubled spline and t nodes %.1e" % (a1, a2 / a1 - 1, a3 / a1 - 1))
            out.append(["check_nodes_Z66-116", "", "", "", "%.2e" % (a2 / a1 - 1), "%.2e" % (a3 / a1 - 1), "", ""])
        # (3) the integration of the whole range: doubled Q nodes
        t1 = own(1.0, 1.0, qmin, SQRTS, "NLO")
        t2 = bin_sigma(proc, ew, lums, pdf.alphasQ, mu0, mu0, qmin, SQRTS, "NLO", nq=80, n1=192, n2=128)
        print("(3) %s %s NLO %g-%g GeV: doubled Q and z nodes %.1e" % (proc, run, qmin, SQRTS, t2 / t1 - 1))
        out.append(["check_nodes_%s_%s_total" % (proc, run), "", "", "", "%.2e" % (t2 / t1 - 1), "", "", ""])
        if proc in ("wp", "wm"):
            # MG5 has no lower cut on m_enu: the size of m < 1 GeV and of m < 0.01 GeV
            for order in ("LO", "NLO"):
                tot = own(1.0, 1.0, qmin, SQRTS, order)
                l1, l2 = own(1.0, 1.0, qmin, 1.0, order), own(1.0, 1.0, qmin, 0.01, order)
                print("(3) %s %s: sigma(m < 1 GeV) = %.4f pb (%.1e), sigma(m < 0.01 GeV) = %.1e pb" % (proc, order, l1, l1 / tot, l2))
                out.append(["check_%s_%s_below_1GeV_pb" % (proc, order), "", "", "", "%.4e" % l1, "%.2e" % (l1 / tot), "%.2e" % l2, ""])
        lo_t, nlo_t = own(1.0, 1.0, qmin, SQRTS, "LO"), own(1.0, 1.0, qmin, SQRTS, "NLO")
        qq_t = bin_sigma(proc, ew, lums, pdf.alphasQ, mu0, mu0, qmin, SQRTS, "NLO", parts=("qq",))
        sc = [own(xr, xf, qmin, SQRTS, "NLO") / nlo_t - 1 for xr in (0.5, 1.0, 2.0) for xf in (0.5, 1.0, 2.0)]
        sl = [own(1.0, xf, qmin, SQRTS, "LO") / lo_t - 1 for xf in (0.5, 2.0)]
        print("(4) %s %s  (mu0 = %g GeV, M_W = %.6f, sw2 = %.6f):  own LO %.6e, NLO %.6e pb, K = %.5f (qqbar %+.4f, qg %+.4f);"
              "  9-point scale range NLO %+.4f %+.4f, LO (mu_F) %+.4f %+.4f"
              % (proc, run, mu0, ew["mw"], ew["sw2"], lo_t, nlo_t, nlo_t / lo_t, (qq_t - lo_t) / lo_t, (nlo_t - qq_t) / lo_t,
                 min(sc), max(sc), min(sl), max(sl)))
        out.append(["own_%s_%s" % (proc, run), "K_qqbar_qg_scale_ranges", "", "", "%.6e" % lo_t, "%.6e" % nlo_t,
                    "%.5f,%.5f,%.5f" % (nlo_t / lo_t, (qq_t - lo_t) / lo_t, (nlo_t - qq_t) / lo_t),
                    "%.4f,%.4f,%.4f,%.4f" % (min(sc), max(sc), min(sl), max(sl))])
        for suffix in ("", "_p", "_t"):
            for order in ("LO", "NLO"):
                hw = WORK / proc / "Events" / ("%s_%s%s" % (run, order, suffix)) / "MADatNLO.HwU"
                if not hw.exists():
                    print("    %s%s: no %s" % (order, suffix, hw))
                    continue
                h = read_hwu(hw)
                tag = "%s_%s_%s%s" % (proc, run, order, suffix)
                for name in hists:
                    if name not in h:
                        continue
                    labels, rows = h[name]
                    cols = scale_columns(labels)
                    pulls_c, pulls_all = [], []
                    for r in rows:
                        lo, hi = r[0], r[1]
                        if name == "total":
                            qlo, qhi = qmin, SQRTS
                        elif name.startswith("log10"):
                            qlo, qhi = max(10 ** lo, qmin), min(10 ** hi, SQRTS)
                        else:
                            qlo, qhi = max(lo, qmin), min(hi, SQRTS)
                        if qhi <= qlo or r[3] <= 0:
                            continue
                        for k, xr, xf in cols:
                            o = own(xr, xf, qlo, qhi, order)
                            mg = r[k]
                            err = r[3] * max(1.0, abs(r[k] / r[2]) if r[2] else 1.0)
                            pull = (mg - o) / err if err else float("nan")
                            pulls_all.append(pull)
                            if (xr, xf) == (1.0, 1.0):
                                pulls_c.append(pull)
                            out.append([tag, name, "%g-%g" % (qlo, qhi), "%g,%g" % (xr, xf), "%.8e" % o, "%.8e" % mg, "%.3e" % err,
                                        "%.2f" % pull])
                            if name == "total" or (len(rows) == 1 and (xr, xf) == (1.0, 1.0)) or (name.startswith("log10") and (xr, xf) == (1.0, 1.0) and abs(pull) > 2.5):
                                print("    %-6s %-11s %-12s muR,F = %3g,%3g  own %.6e  MG5 %.6e +- %.1e  (%+.2f sigma, %+.1e)"
                                      % (order + suffix, name, "%g-%g" % (qlo, qhi), xr, xf, o, mg, err, pull, mg / o - 1))
                    if len(pulls_c) > 1:
                        chi2 = sum(p * p for p in pulls_c)
                        print("    %-6s %-11s %d bins: chi2 = %.1f (central scales), max |pull| %.2f (all 9 scales)"
                              % (order + suffix, name, len(pulls_c), chi2, max(abs(p) for p in pulls_all)))
                        summary.append([tag, name, "%d bins" % len(pulls_c), "chi2_central", "%.2f" % chi2, "max_abs_pull_9_scales",
                                        "%.2f" % max(abs(p) for p in pulls_all), ""])
                # the rapidity distribution (own: dy_conv of the (d2) pieces), with overflow bins for the check of its sum
                yname, yqlo, yqhi = yhist
                labels, rows = h[yname]
                cols = scale_columns(labels)
                edges = np.concatenate([[-12.0], [r[0] for r in rows], [rows[-1][1], 12.0]])
                ykey = (order, yqlo, yqhi)
                if ykey not in ycache:
                    ycache[ykey] = y_sigma(proc, ew, lums, pdf.alphasQ, mu0, yqlo, yqhi, edges, order, SCALES)
                    tot = ycache[ykey][(1.0, 1.0)].sum()
                    inc = own(1.0, 1.0, yqlo, yqhi, order)
                    print("    %-6s %-11s own: sum over all y minus the inclusive sigma %.1e (|y| > 5: %.1e)"
                          % (order, yname, tot / inc - 1, (ycache[ykey][(1.0, 1.0)][[0, -1]].sum()) / inc))
                    out.append(["check_y_sum_%s_%s_%s" % (proc, run, order), yname, "%g-%g" % (yqlo, yqhi), "", "%.2e" % (tot / inc - 1),
                                "", "", ""])
                pulls_c, pulls_all = [], []
                # bins at the kinematic limit with sigma below 1e-9 of the histogram (e.g. 1e-13 pb at |y| = 3.25 for
                # m > 500 GeV) hold round-off only: the own value can be -2e-13, MG5's error 4e-14
                htot = sum(r[2] for r in rows)
                nskip = 0
                for b, r in enumerate(rows):
                    if max(abs(ycache[ykey][(1.0, 1.0)][b + 1]), abs(r[2])) < 1e-9 * htot:
                        nskip += 1
                        continue
                    for k, xr, xf in cols:
                        o = ycache[ykey][(xr, xf)][b + 1]
                        mg = r[k]
                        err = r[3] * max(1.0, abs(r[k] / r[2]) if r[2] else 1.0)
                        if err <= 0:
                            continue
                        pull = (mg - o) / err
                        pulls_all.append(pull)
                        if (xr, xf) == (1.0, 1.0):
                            pulls_c.append(pull)
                        out.append([tag, yname, "y %g:%g" % (r[0], r[1]), "%g,%g" % (xr, xf), "%.8e" % o, "%.8e" % mg, "%.3e" % err,
                                    "%.2f" % pull])
                chi2 = sum(p * p for p in pulls_c)
                print("    %-6s %-11s %d bins with events (%d below 1e-9 skipped): chi2 = %.1f (central scales), max |pull| %.2f (all 9 scales)"
                      % (order + suffix, yname, len(pulls_c), nskip, chi2, max(abs(p) for p in pulls_all)))
                summary.append([tag, yname, "%d bins" % len(pulls_c), "chi2_central", "%.2f" % chi2, "max_abs_pull_9_scales",
                                "%.2f" % max(abs(p) for p in pulls_all), ""])
    with open(RES / "dy_hadronic.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "histogram", "bin_GeV", "xiR,xiF", "own_pb", "mg5_pb", "mg5_err_pb", "pull"])
        w.writerows(out)
        w.writerows(summary)
    print("written: results/dy_hadronic.csv")


if __name__ == "__main__":
    main()
