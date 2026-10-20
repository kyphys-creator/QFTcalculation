"""Research note models/sm_pp, step (3): MC@NLO with Pythia 8 against the note's own calculations.

(3a) The own LO V + jet and H + jet transverse-momentum spectra (O(alpha_s) above p_T = 0), from the 4-dimensional real emission
of steps (1) and (2), convolved with NNPDF4.0 NLO, against the p_T > 0 bins of the fixed-order NLO runs (there only the real
emission enters: the Born, virtual and counter-events have p_T = 0):
  Drell-Yan (dy_feyncalc.wl, (a)):  dsigma_ij/dQ^2 dv = (sigma_0(Q^2)/shat) a_s (1 - z) r_ij(z, v),  shat = Q^2/z,
     t = (p1 - k)^2 = -shat (1 - z) v,  u = -shat (1 - z)(1 - v),  p_T^2 = t u/shat = shat (1 - z)^2 v (1 - v),
     r_qqbar = 2 C_F [u/t + t/u + 2 Q^2 shat/(u t)],  r_qg = -2 T_R [u/shat + shat/u + 2 Q^2 t/(u shat)],
     dsigma/dQ^2 = (sigma_0/Q^2) sum 2 [G (x) D_bin] as in dy_hadronic.py (D_bin = (1 - z) int dv r restricted to the p_T bin);
     m_ee > 50 GeV, mu_R = mu_F = M_Z (run zpeak_NLO of dy_mg5.sh, histogram ptV);
  g g -> H (gh_tree.py; c = cHgg = -alpha_s/(3 pi), no Wilson coefficient):  sum|M|^2 = 24 c^2 g_s^2/v^2 (M^8 + s^4 + t^4 + u^4)/(s t u)
     (g g, average 1/256),  -4 c^2 g_s^2/v^2 (s^2 + u^2)/t (q g, t = (p_q,in - p_q,out)^2, 1/96),  4 c^2 g_s^2/v^2 (t^2 + u^2)/s (q qbar, 1/36),
     dsigma/dt = avg|M|^2/(16 pi shat^2),  sigma_bin = sum_ab int dz/z G_ab(tau/z) sigma_bin,ab(shat = M_H^2/z);
     mu_R = mu_F = M_H, without q qbar (not in p p > h [QCD]) (run o_NLO of gh_own_mg5.sh, histogram ptH).
(3b) MC@NLO with Pythia 8 (mc_mg5.sh, parton level, py8an_HwU_mc.f) against the own NLO: the total (the sum of the event weights,
equal to the NLO integral: m_ee > 50 GeV and 66 < m_ee < 116 GeV for the Z; the H without the Wilson coefficient and q qbar), the
rapidity of the boson (Z: the own NLO of dy_hadronic.py in 66-116 GeV; H: the fixed-order NLO run o_NLO, an MG5-internal
comparison, the own NLO rapidity of g g -> H not being derived), and its p_T against the own LO V + jet, H + jet of (3a).
Writes results/mc_hadronic.csv.  Run with ~/hep/opt/lhc/bin/python (from Src/).
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dy_hadronic as dy  # noqa: E402
import gh_hadronic as gh  # noqa: E402

SRC = Path(__file__).resolve().parent
RES = SRC / "results"
CF, TR = 4.0 / 3.0, 0.5
MZ0, MH = 91.188, 125.2
LEG = {n: np.polynomial.legendre.leggauss(n) for n in (16, 24, 32, 48, 64, 96)}
QUARK_IDS = (1, 2, 3, 4, 5, -1, -2, -3, -4, -5)


# ---------------------------------------------------------------- the v and z nodes of a p_T bin
def gl(a, b, n):
    t, w = LEG[n]
    return 0.5 * (b - a) * t + 0.5 * (b + a), 0.5 * (b - a) * w


def v_nodes(wa, wb, n):
    """v in (0, 1/2] with wa < v(1 - v) < wb (wb <= 1/4); shape (len(wa), n).  The mirror v -> 1 - v is added by the callers."""
    va = 0.5 * (1 - np.sqrt(np.maximum(1 - 4 * wa, 0.0)))
    vb = 0.5 * (1 - np.sqrt(np.maximum(1 - 4 * np.minimum(wb, 0.25), 0.0)))
    t, w = LEG[n]
    v = 0.5 * (vb - va)[:, None] * t[None, :] + 0.5 * (vb + va)[:, None]
    return v, 0.5 * (vb - va)[:, None] * w[None, :]


def z_nodes(tau, q2, pa, pb, n):
    """z in (tau, z_a) with p_T,max(z) = sqrt(shat)(1 - z)/2 > pa, split at z_b (p_T,max = pb); shat = q2/z"""
    def zmax(p):
        a = 4 * p * p / q2
        return ((2 + a) - math.sqrt((2 + a) ** 2 - 4)) / 2
    za, zb = zmax(pa), zmax(pb)
    zs, ws = [], []
    if za <= tau:
        return np.array([]), np.array([])
    lo = tau
    u, wu = gl(0.0, 1.0, n)
    if zb > tau:
        # below z_b the upper end of the v range opens as sqrt(z_b - z): ln z on (tau, z_b/2), then z = z_b - (z_b - zm) u^2
        zm = max(tau, zb / 2)
        if zm > tau:
            lz, wl = gl(math.log(tau), math.log(zm), n)
            zs.append(np.exp(lz))
            ws.append(wl * np.exp(lz))
        zs.append(zb - (zb - zm) * u * u)
        ws.append(wu * 2 * u * (zb - zm))
        lo = zb
    # the upper piece ends at the square-root edge z_a: z = z_a - (z_a - lo) u^2
    zs.append(za - (za - lo) * u * u)
    ws.append(wu * 2 * u * (za - lo))
    return np.concatenate(zs), np.concatenate(ws)


# ---------------------------------------------------------------- Drell-Yan: V + jet
def r_qq(z, v):
    return 2 * CF * ((1 - v) / v + v / (1 - v) + 2 * z / ((1 - z) ** 2 * v * (1 - v)))


def r_qg(z, v):
    return 2 * TR * ((1 - z) * (1 - v) + 1 / ((1 - z) * (1 - v)) - 2 * z * v / (1 - v))


def dy_pt_bins(edges, ew, lum, alphas, mu, qlo=50.0, qhi=dy.SQRTS, nq=40, nz=32, nv=24):
    """sigma (pb) in the p_T bins (edges[k], edges[k+1]) for k >= 1, p p -> gamma*/Z -> e+ e- + jet at O(alpha_s), qlo < m_ee < qhi"""
    as4pi = alphas(mu) / (4 * math.pi)
    q2s, dq2 = dy.qnodes(qlo, qhi, ew["mz"], ew["wz"], nq)
    out = np.zeros(len(edges) - 1)
    chans = dy.channels("z")
    for q2, dq in zip(q2s, dq2):
        tau = q2 / dy.S
        s0 = {pair: dy.sigma0(q2, pair, ew) for pair, _, _ in chans}
        for k in range(1, len(edges) - 1):
            pa, pb = edges[k], edges[k + 1]
            z, wz = z_nodes(tau, q2, pa, pb, nz)
            if len(z) == 0:
                continue
            sh = q2 / z
            wa, wb = pa * pa / (sh * (1 - z) ** 2), pb * pb / (sh * (1 - z) ** 2)
            v, wv = v_nodes(wa, wb, nv)
            zz = z[:, None]
            dqq = (1 - z) * np.sum(wv * (r_qq(zz, v) + r_qq(zz, 1 - v)), axis=1)
            dqg = (1 - z) * np.sum(wv * (r_qg(zz, v) + r_qg(zz, 1 - v)), axis=1)
            tot = 0.0
            for pair, pqq, pqg in chans:
                gqq = sum(lum.g(i, j, tau / z) for i, j in pqq)
                gqg = sum(lum.g(i, j, tau / z) for i, j in pqg)
                tot += s0[pair] * 2 * np.sum(wz * (dqq * gqq + dqg * gqg))
            out[k] += dq * tot / q2 * as4pi
    return out * dy.GEV2PB


# ---------------------------------------------------------------- g g -> H: H + jet
def h_pt_bins(edges, lum, alphas, vev, mu, parts=("gg", "qg"), nz=32, nv=24):
    """sigma (pb) in the p_T bins (k >= 1), p p -> H + jet at O(alpha_s^3) in the heavy-top theory (no Wilson coefficient)"""
    a = alphas(mu)
    c2g2 = (a / (3 * math.pi)) ** 2 * 4 * math.pi * a / vev ** 2
    m2 = MH * MH
    tau = m2 / dy.S
    out = np.zeros(len(edges) - 1)
    for k in range(1, len(edges) - 1):
        pa, pb = edges[k], edges[k + 1]
        z, wz = z_nodes(tau, m2, pa, pb, nz)
        if len(z) == 0:
            continue
        sh = m2 / z
        wa, wb = pa * pa / (sh * (1 - z) ** 2), pb * pb / (sh * (1 - z) ** 2)
        v, wv = v_nodes(wa, wb, nv)
        s = sh[:, None]
        tot = np.zeros(len(z))
        for vv in (v, 1 - v):
            t, u = -s * (1 - z[:, None]) * vv, -s * (1 - z[:, None]) * (1 - vv)
            # dsigma/dv = (1 - z) shat avg|M|^2/(16 pi shat^2)
            fac = (1 - z[:, None]) / (16 * math.pi * s)
            if "gg" in parts:
                mgg = 24 * c2g2 * (m2 ** 4 + s ** 4 + t ** 4 + u ** 4) / (s * t * u) / 256
                tot += np.sum(wv * fac * mgg, axis=1) * lum.g(21, 21, tau / z)
            if "qg" in parts:
                mqg = -4 * c2g2 * (s * s + u * u) / t / 96
                gqg = sum(2 * lum.g(q, 21, tau / z) for q in QUARK_IDS)
                tot += np.sum(wv * fac * mqg, axis=1) * gqg
            if "qq" in parts:
                mqq = 4 * c2g2 * (t * t + u * u) / s / 36
                gqq = sum(2 * lum.g(q, -q, tau / z) for q in (1, 2, 3, 4, 5))
                tot += np.sum(wv * fac * mqq, axis=1) * gqq
        out[k] = np.sum(wz / z * tot)
    return out * dy.GEV2PB


def compare_fo(name, own, h, out, kmin=1):
    """own against the fixed-order histogram rows for the bins k >= kmin"""
    rows = h[1]
    pulls = []
    for k in range(kmin, len(rows)):
        mg, err = rows[k][2], rows[k][3]
        if err <= 0:
            continue
        p = (mg - own[k]) / err
        pulls.append(p)
        out.append([name, "%g-%g" % (rows[k][0], rows[k][1]), "%.6e" % own[k], "%.6e" % mg, "%.3e" % err, "%.2f" % p])
    lo = rows[kmin][0]
    print("    %-22s p_T > %g GeV: %d bins, chi2 = %.1f, max |pull| %.2f;  sum own %.5f pb, MG5 %.5f pb"
          % (name, lo, len(pulls), sum(p * p for p in pulls), max(abs(p) for p in pulls), own[kmin:].sum(),
             sum(r[2] for r in rows[kmin:])))


def mc_hwu(proc, run="mc"):
    """the showered histograms of mc_mg5.sh (None if not run)"""
    f = sorted((SRC / "work" / "mc" / proc / "Events" / run).glob("plot_PYTHIA8*.HwU"))
    return dy.read_hwu(f[-1]) if f else None


def ratio_line(name, mc, own, edges, ranges, out):
    """MC@NLO over own in p_T ranges: sums of bins, the MC error from the bin errors in quadrature"""
    rows = mc[1]
    parts = []
    for lo, hi in ranges:
        ks = [k for k in range(len(rows)) if rows[k][0] >= lo - 1e-9 and rows[k][1] <= hi + 1e-9]
        m = sum(rows[k][2] for k in ks)
        e = math.sqrt(sum(rows[k][3] ** 2 for k in ks))
        o = sum(own[k] for k in ks)
        parts.append("%g-%g GeV %.4f(%d)" % (lo, hi, m / o, round(1e4 * e / o)))
        out.append([name, "%g-%g" % (lo, hi), "%.6e" % o, "%.6e" % m, "%.3e" % e, "%.4f" % (m / o)])
    print("    %-22s MC@NLO / own LO: %s" % (name, ",  ".join(parts)))


def compare_hist(name, ref, mc, out, ref_err=None):
    """bin by bin: (mc - ref)/sqrt(err_mc^2 + err_ref^2) over bins with mc error > 0"""
    rows = mc[1]
    pulls, rat = [], []
    for k, r in enumerate(rows):
        e2 = r[3] ** 2 + (ref_err[k] ** 2 if ref_err is not None else 0.0)
        if r[3] <= 0 or ref[k] == 0:
            continue
        p = (r[2] - ref[k]) / math.sqrt(e2)
        pulls.append(p)
        if abs(0.5 * (r[0] + r[1])) < 2.5:
            rat.append(r[2] / ref[k])
        out.append([name, "%g-%g" % (r[0], r[1]), "%.6e" % ref[k], "%.6e" % r[2], "%.3e" % math.sqrt(e2), "%.2f" % p])
    print("    %-22s %d bins, chi2 = %.1f, max |pull| %.2f;  MC/ref in |y| < 2.5: %.4f to %.4f;  sums %.5f / %.5f"
          % (name, len(pulls), sum(p * p for p in pulls), max(abs(p) for p in pulls), min(rat), max(rat),
             sum(r[2] for r in rows), sum(ref)))


def main():
    RES.mkdir(exist_ok=True)
    dy.lhapdf.setVerbosity(0)
    pdf = dy.lhapdf.mkPDF(dy.PDFNAME, 0)
    out = []
    edges = np.arange(0.0, 251.0, 5.0)
    # (3a) Drell-Yan
    ew = dy.param_card(dy.WORK / "z" / "Cards" / "param_card.dat")
    lum = dy.Lumi(pdf, MZ0, 50.0 ** 2 / dy.S / 2)
    own_v = dy_pt_bins(edges, ew, lum, pdf.alphasQ, MZ0)
    own_v2 = dy_pt_bins(edges, ew, lum, pdf.alphasQ, MZ0, nq=80, nz=64, nv=48)
    print("(3a) V + jet, doubled nodes: max rel %.1e" % np.max(np.abs(own_v2[1:] / own_v[1:] - 1)))
    for run in ("zpeak_NLO", "zpeak_NLO_p"):
        h = dy.read_hwu(dy.WORK / "z" / "Events" / run / "MADatNLO.HwU")
        compare_fo("ptV " + run, own_v, h["ptV"], out)
    # (3a) g g -> H
    vo = gh.card_value(gh.WORK / "ppo" / "Cards" / "param_card.dat", "higgs", 1)
    lumh = dy.Lumi(pdf, MH, MH * MH / dy.S / 4)
    own_h = h_pt_bins(edges, lumh, pdf.alphasQ, vo, MH)
    own_h2 = h_pt_bins(edges, lumh, pdf.alphasQ, vo, MH, nz=64, nv=48)
    own_hq = h_pt_bins(edges, lumh, pdf.alphasQ, vo, MH, parts=("qq",))
    print("(3a) H + jet, doubled nodes: max rel %.1e;  q qbar -> H g above 5 GeV (not in [QCD]): %.5f pb"
          % (np.max(np.abs(own_h2[1:] / own_h[1:] - 1)), own_hq[1:].sum()))
    h = gh.dy.read_hwu(gh.WORK / "ppo" / "Events" / "o_NLO" / "MADatNLO.HwU")
    compare_fo("ptH o_NLO", own_h, h["ptH"], out)
    # (3b) MC@NLO with Pythia 8
    hz = mc_hwu("z")
    if hz is None:
        print("    no MC@NLO run of the Z (mc_mg5.sh)")
    else:
        lums = {MZ0: lum}
        for name, qlo, qhi in (("total", 50.0, dy.SQRTS), ("mB 66-116", 66.0, 116.0)):
            own = dy.bin_sigma("z", ew, lums, pdf.alphasQ, MZ0, MZ0, qlo, qhi, "NLO")
            m, e = hz[name][1][0][2], hz[name][1][0][3]
            print("(3b) Z %-10s own NLO %.4f pb  MC@NLO %.4f +- %.4f  (%+.2f sigma, %+.1e)" % (name, own, m, e, (m - own) / e, m / own - 1))
            out.append(["Z " + name, "", "%.6e" % own, "%.6e" % m, "%.3e" % e, "%.2f" % ((m - own) / e)])
        yrows = hz["yB 66-116"][1]
        yedges = np.array([r[0] for r in yrows] + [yrows[-1][1]])
        yown = dy.y_sigma("z", ew, lums, pdf.alphasQ, MZ0, 66.0, 116.0, yedges, "NLO", [(1.0, 1.0)])[(1.0, 1.0)]
        compare_hist("Z yB 66-116 vs own NLO", yown, hz["yB 66-116"], out)
        hfo = dy.read_hwu(dy.WORK / "z" / "Events" / "zpeak_NLO_p" / "MADatNLO.HwU")
        compare_hist("Z yB 66-116 vs FO NLO", [r[2] for r in hfo["yV 66-116"][1]], hz["yB 66-116"], out,
                     ref_err=[r[3] for r in hfo["yV 66-116"][1]])
        ratio_line("Z ptB", hz["ptB"], own_v, edges, ((5, 20), (20, 50), (50, 100), (100, 150), (150, 250)), out)
        low = hz["ptB 0-30"][1]
        tot = hz["total"][1][0][2]
        peak = max(low, key=lambda r: r[2])
        print("    Z ptB below 5 GeV: %.3f of the total;  the largest 1-GeV bin %g-%g GeV" % (sum(r[2] for r in low[:5]) / tot, peak[0], peak[1]))
    hh = mc_hwu("h")
    if hh is None:
        print("    no MC@NLO run of the H (mc_mg5.sh)")
    else:
        own = gh.sigma({MH: lumh}, pdf.alphasQ, vo, MH, MH, "NLO", wilson=False, parts=("gg", "qg"))
        m, e = hh["total"][1][0][2], hh["total"][1][0][3]
        print("(3b) H total      own NLO %.4f pb  MC@NLO %.4f +- %.4f  (%+.2f sigma, %+.1e)" % (own, m, e, (m - own) / e, m / own - 1))
        out.append(["H total", "", "%.6e" % own, "%.6e" % m, "%.3e" % e, "%.2f" % ((m - own) / e)])
        hfo = gh.dy.read_hwu(gh.WORK / "ppo" / "Events" / "o_NLO" / "MADatNLO.HwU")
        compare_hist("H yB vs FO NLO", [r[2] for r in hfo["yH"][1]], hh["yB"], out, ref_err=[r[3] for r in hfo["yH"][1]])
        ratio_line("H ptB", hh["ptB"], own_h, edges, ((5, 20), (20, 50), (50, 100), (100, 150), (150, 250)), out)
        low = hh["ptB 0-30"][1]
        tot = hh["total"][1][0][2]
        peak = max(low, key=lambda r: r[2])
        print("    H ptB below 5 GeV: %.3f of the total;  the largest 1-GeV bin %g-%g GeV" % (sum(r[2] for r in low[:5]) / tot, peak[0], peak[1]))
    with open(RES / "mc_hadronic.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["quantity", "bin", "own_pb", "mg5_pb", "mg5_err_pb", "pull"])
        w.writerows(out)
    print("written: results/mc_hadronic.csv")


if __name__ == "__main__":
    main()
