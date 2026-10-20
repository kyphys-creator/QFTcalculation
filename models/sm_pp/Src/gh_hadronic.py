"""Research note models/sm_pp, step (2e): g g -> H at LO and NLO in the heavy-top effective theory from the note's coefficient
functions (gh_feyncalc.wl), convolved with NNPDF4.0 NLO (LHAPDF 331700, alpha_s from the set), against aMC@NLO at fixed order
(gh_mg5.sh, HC_NLO_X0-heft).

  sigma = sigma_0 sum_ij int_tau^1 dz Delta_ij(z) G_ij(tau/z),  tau = M_H^2/S,  sigma_0 = alpha_s(mu_R)^2 (kHgg cosa)^2/(576 pi v^2)
(sigma_ij = sigma_0 z Delta_ij(z) as for Drell-Yan; G_ij as in dy_hadronic.py), channels g g, q g + g q (q: the ten quarks and
antiquarks), q qbar + qbar q.  The Wilson coefficient C1 = 1 + (11/4) alpha_s/pi adds (11/2)(alpha_s/pi) = 22 a_s to the delta(1 - z)
of Delta_gg; HC_NLO_X0 has it in the finite part of its g g X0 counterterm (gh_madloop.py), so the comparison includes it.
v = 2 M_W s_W/e of the param card's inputs (= (sqrt2 G_F)^-1/2).
Checks: the coefficient functions against gh_feyncalc.wl's values; LO and NLO totals for mu_F = M/2, M, 2M (reweighted) and
mu_R = M/2, M, 2M (separate runs; MG5's mu_R reweighting misses HC_NLO_X0's alpha_s in gHgg); the LO rapidity distribution.  Also: K, the channels, the scale ranges, and the cross section with the exact top-mass LO factor
|A_1/2(tau_t)|^2/|A_1/2(0)|^2 (m_t = 172.5 GeV).
Step (2f): the same against aMC@NLO with the note's own NLO UFO (gh_own_mg5.sh, runs o_LO, o_NLO): no Wilson coefficient, v of its
param card (block HIGGS), all nine (mu_R, mu_F) columns by reweighting.  Writes results/gh_hadronic.csv.  Run with ~/hep/opt/lhc/bin/python.
"""
import csv
import math
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dy_hadronic as dy  # noqa: E402

SRC = Path(__file__).resolve().parent
WORK = SRC / "work" / "gh"
RES = SRC / "results"
MH = 125.2
CA, CF, NF = 3.0, 4.0 / 3.0, 5
BETA0 = 11 - 2 / 3 * NF
ZETA2 = math.pi ** 2 / 6
WILSON = 22.0   # 4 x (11/2): (11/2)(alpha_s/pi) in units of a_s


# ---------------------------------------------------------------- the coefficient functions (units a_s; gh_feyncalc.wl, (e))
def gg_delta(lf, lr, wilson):
    return 24 * ZETA2 - 2 * BETA0 * lf + 2 * BETA0 * lr + (WILSON if wilson else 0.0)


def gg_plus0(lf):
    return -24 * lf


def gg_plus1(lf):
    return 48 + 0 * lf


def gg_reg(z, lf):
    return ((22 * (z - 1) ** 4 - 48 * (1 - 3 * z + 3 * z * z - 2 * z ** 3 + z ** 4) * np.log(1 - z)
             + 24 * (1 - z + z * z) ** 2 * np.log(z)) / ((z - 1) * z) + 24 * lf * (2 - 1 / z - z + z * z))


def qg(z, lf):
    p = 2 - 2 * z + z * z
    return 4 * (-3 + 6 * z - z * z + 4 * p * np.log(1 - z) - 2 * p * np.log(z)) / (3 * z) - 8 * lf * p / (3 * z)


def qqbar(z, lf):
    return 128 * (1 - z) ** 3 / (27 * z) + 0 * lf


def check_coefficients():
    rows = list(csv.reader(open(RES / "gh_feyncalc.csv")))
    val = {r[0]: r[1:] for r in rows[1:]}
    dev = 0.0
    for name, f in (("gg_delta", lambda lf, lr: gg_delta(lf, lr, False)), ("gg_plus0", lambda lf, lr: gg_plus0(lf)),
                    ("gg_plus1", lambda lf, lr: gg_plus1(lf))):
        v0, v1, v2 = (float(x) for x in val[name])
        dev = max(dev, abs(f(0, 0) - v0), abs(f(1, 0) - f(0, 0) - v1), abs(f(0, 1) - f(0, 0) - v2))
    for name, (v0, v1, v2) in val.items():
        m = re.match(r"(gg_reg|qg|qqbar)_z=(.*)", name)
        if not m:
            continue
        z = float(m.group(2))
        f = {"gg_reg": gg_reg, "qg": qg, "qqbar": qqbar}[m.group(1)]
        v0, v1 = float(v0), float(v1)
        dev = max(dev, abs(f(z, 0) - v0) / max(1, abs(v0)), abs(f(z, 1) - f(z, 0) - v1) / max(1, abs(v1)))
    bad = [k for k, v in val.items() if k.startswith("check") and v[0] not in ("0", "0.")]
    return dev, bad


# ---------------------------------------------------------------- the hadronic cross section
def param_card(path):
    vals = {}
    block = None
    for line in open(path):
        s = line.split("#")[0].split()
        if not s:
            continue
        if s[0].lower() == "block":
            block = s[1].lower()
        elif block in ("mass", "sminputs") and len(s) >= 2:
            vals[(block, int(s[0]))] = float(s[1])
    aew = 1 / vals[("sminputs", 1)]
    gf, mz = vals[("sminputs", 2)], vals[("mass", 23)]
    mw = math.sqrt(mz ** 2 / 2 + math.sqrt(mz ** 4 / 4 - aew * math.pi * mz ** 2 / (gf * math.sqrt(2))))
    sw = math.sqrt(1 - mw ** 2 / mz ** 2)
    return {"vev": 2 * mw * sw / math.sqrt(4 * math.pi * aew), "gf": gf}


def card_value(path, block, code):
    """the entry code of block in a param card"""
    cur = None
    for line in open(path):
        s = line.split("#")[0].split()
        if not s:
            continue
        if s[0].lower() == "block":
            cur = s[1].lower()
        elif cur == block.lower() and len(s) >= 2 and s[0] == str(code):
            return float(s[1])
    raise KeyError((block, code))


def sigma(lums, alphas, vev, mur, muf, order, wilson=True, parts=("gg", "qg", "qq"), n1=96, n2=64):
    """sigma (pb) of p p -> H"""
    lum = lums[muf]
    tau = MH * MH / dy.S
    a = alphas(mur)
    sig0 = a * a / (576 * math.pi * vev * vev) * dy.GEV2PB
    as4 = a / (4 * math.pi)
    lf, lr = math.log(muf * muf / (MH * MH)), math.log(mur * mur / (MH * MH))
    g1 = lum.g(21, 21, tau)
    if order == "LO":
        return sig0 * g1
    z, w = dy.znodes(tau, n1, n2)
    gz = lum.g(21, 21, tau / z)
    l1 = math.log(1 - tau)
    nlo = 0.0
    if "gg" in parts:
        nlo += (gg_delta(lf, lr, wilson) * g1 + gg_plus0(lf) * (np.sum(w * (gz - g1) / (1 - z)) + g1 * l1)
                + gg_plus1(lf) * (np.sum(w * (gz - g1) * np.log(1 - z) / (1 - z)) + g1 * l1 * l1 / 2)
                + np.sum(w * gg_reg(z, lf) * gz))
    if "qg" in parts:
        gqg = sum(2 * lum.g(q, 21, tau / z) for q in (1, 2, 3, 4, 5, -1, -2, -3, -4, -5))
        nlo += np.sum(w * qg(z, lf) * gqg)
    if "qq" in parts:
        gqq = sum(2 * lum.g(q, -q, tau / z) for q in (1, 2, 3, 4, 5))
        nlo += np.sum(w * qqbar(z, lf) * gqq)
    return sig0 * (g1 + as4 * nlo)


def lo_rapidity(lum, alphas, vev, mur, edges):
    """LO dsigma in rapidity bins: x1,2 = sqrt(tau) e^(+-y), sigma_0 x1 g(x1) x2 g(x2) dy"""
    tau = MH * MH / dy.S
    a = alphas(mur)
    sig0 = a * a / (576 * math.pi * vev * vev) * dy.GEV2PB
    t, w = np.polynomial.legendre.leggauss(32)
    out = []
    ymax = -0.5 * math.log(tau)
    for lo, hi in zip(edges[:-1], edges[1:]):
        lo, hi = max(lo, -ymax), min(hi, ymax)
        if hi <= lo:
            out.append(0.0)
            continue
        y = 0.5 * (hi - lo) * t + 0.5 * (hi + lo)
        x1, x2 = np.sqrt(tau) * np.exp(y), np.sqrt(tau) * np.exp(-y)
        out.append(sig0 * float(np.sum(0.5 * (hi - lo) * w * lum.xfx(21, np.log(x1)) * lum.xfx(21, np.log(x2)))))
    return np.array(out)


def a_half(tau):
    """A_1/2(tau) = 2 [tau + (tau - 1) f(tau)]/tau^2, tau = M_H^2/(4 m^2) <= 1: f = arcsin^2 sqrt(tau); -> 4/3 for tau -> 0"""
    f = math.asin(math.sqrt(tau)) ** 2
    return 2 * (tau + (tau - 1) * f) / tau ** 2


def main():
    dy.lhapdf.setVerbosity(0)
    pdf = dy.lhapdf.mkPDF(dy.PDFNAME, 0)
    out = []
    dev, bad = check_coefficients()
    print("(1) coefficient functions minus gh_feyncalc.wl's values: max %.1e;  its checks not zero: %s" % (dev, bad or "none"))
    out.append(["check_coefficients_minus_feyncalc", "", "", "%.2e" % dev, "", "", ""])
    ew = param_card(WORK / "pph" / "Cards" / "param_card.dat")
    mu0 = MH
    lums = {f * mu0: dy.Lumi(pdf, f * mu0, MH * MH / dy.S / 4) for f in (1.0, 2.0, 0.5)}
    s1 = sigma(lums, pdf.alphasQ, ew["vev"], mu0, mu0, "NLO")
    s2 = sigma(lums, pdf.alphasQ, ew["vev"], mu0, mu0, "NLO", n1=192, n2=128)
    print("(2) v = %.6f GeV; doubled z nodes: %.1e" % (ew["vev"], s2 / s1 - 1))
    out.append(["check_nodes", "", "", "%.2e" % (s2 / s1 - 1), "", "", ""])
    lo = sigma(lums, pdf.alphasQ, ew["vev"], mu0, mu0, "LO")
    nlo_w = s1
    nlo = sigma(lums, pdf.alphasQ, ew["vev"], mu0, mu0, "NLO", wilson=False)
    parts = {p: sigma(lums, pdf.alphasQ, ew["vev"], mu0, mu0, "NLO", wilson=False, parts=(p,)) - lo for p in ("gg", "qg", "qq")}
    sc = [sigma(lums, pdf.alphasQ, ew["vev"], xr * mu0, xf * mu0, "NLO") / nlo_w - 1 for xr in (0.5, 1, 2) for xf in (0.5, 1, 2)]
    sl = [sigma(lums, pdf.alphasQ, ew["vev"], xr * mu0, xr * mu0, "LO") / lo - 1 for xr in (0.5, 2)]
    rt = (a_half((MH / (2 * 172.5)) ** 2) / (4 / 3)) ** 2
    print("(3) mu = M_H: LO %.4f pb, NLO %.4f pb (without the Wilson coefficient's 11/2: %.4f), K = %.4f (%.4f);  NLO corrections over"
          " LO: gg %+.4f (+ Wilson %+.4f), qg %+.4f, qqbar %+.5f;  9-point range %+.3f %+.3f, LO (mu_R = mu_F) %+.3f %+.3f;"
          "  exact-top LO factor %.5f -> NLO %.3f pb"
          % (lo, nlo_w, nlo, nlo_w / lo, nlo / lo, parts["gg"] / lo, (nlo_w - nlo) / lo, parts["qg"] / lo, parts["qq"] / lo,
             min(sc), max(sc), min(sl), max(sl), rt, rt * nlo_w))
    out.append(["own_mu_MH", "LO,NLO,NLO_noWilson,K", "", "%.6f" % lo, "%.6f" % nlo_w, "%.6f" % nlo, "%.6f" % (nlo_w / lo)])
    out.append(["own_channels_over_LO", "gg,Wilson,qg,qqbar", "", "%.6f" % (parts["gg"] / lo), "%.6f" % ((nlo_w - nlo) / lo),
                "%.6f" % (parts["qg"] / lo), "%.6f" % (parts["qq"] / lo)])
    out.append(["own_scale_ranges", "NLO_min,NLO_max,LO_min,LO_max", "", "%.5f" % min(sc), "%.5f" % max(sc), "%.5f" % min(sl),
                "%.5f" % max(sl)])
    out.append(["own_exact_top_LO_factor", "R_t,NLO_rescaled", "", "%.6f" % rt, "%.5f" % (rt * nlo_w), "", ""])
    # HC_NLO_X0's g g X0 coupling has the order QNP only (its alpha_s^2 is inside gHgg ~ G^2), so MG5's mu_R reweighting does not move
    # it (the LO is the same for every mu_R factor): only the mu_F columns (xi_R = 1) are compared; mu_R is varied by separate runs
    # with mu_R = M/2, 2M as the central scale (runs h_<order>_r05, h_<order>_r2; mu_F = M)
    for suffix, xr0 in (("", 1.0), ("_p", 1.0), ("_r05", 0.5), ("_r2", 2.0)):
        for order in ("LO", "NLO"):
            hw = WORK / "pph" / "Events" / ("h_%s%s" % (order, suffix)) / "MADatNLO.HwU"
            if not hw.exists():
                print("    no %s" % hw)
                continue
            h = dy.read_hwu(hw)
            labels, rows = h["total"]
            for k, xr, xf in dy.scale_columns(labels):
                if xr != 1.0:
                    continue
                xr = xr0
                # aMC@NLO's p p > x0 [QCD] has no q qbar -> x0 g (no FKS pair maps it to the Born g g > x0): compared without it
                own = sigma(lums, pdf.alphasQ, ew["vev"], xr * mu0, xf * mu0, order, parts=("gg", "qg"))
                mg, err = rows[0][k], rows[0][3] * max(1.0, abs(rows[0][k] / rows[0][2]))
                pull = (mg - own) / err
                out.append(["h_%s%s" % (order, suffix), "total", "%g,%g" % (xr, xf), "%.8e" % own, "%.8e" % mg, "%.3e" % err,
                            "%.2f" % pull])
                print("    %-6s muR,F = %3g,%3g  own %.6f  MG5 %.6f +- %.4f  (%+.2f sigma, %+.1e)"
                      % (order + suffix, xr, xf, own, mg, err, pull, mg / own - 1))
            if order == "LO" and xr0 == 1.0:
                labels, rows = h["yH"]
                edges = np.array([r[0] for r in rows] + [rows[-1][1]])
                ylo = lo_rapidity(lums[mu0], pdf.alphasQ, ew["vev"], mu0, edges)
                pulls = [(r[2] - o) / r[3] for r, o in zip(rows, ylo) if r[3] > 0]
                print("    %-6s yH: %d bins, chi2 = %.1f, max |pull| %.2f (sum of own bins / own LO - 1: %.1e)"
                      % (order + suffix, len(pulls), sum(p * p for p in pulls), max(abs(p) for p in pulls), ylo.sum() / lo - 1))
                out.append(["h_%s%s" % (order, suffix), "yH", "%d bins" % len(pulls), "chi2", "%.2f" % sum(p * p for p in pulls),
                            "max_abs_pull", "%.2f" % max(abs(p) for p in pulls)])
    # step (2f): the own NLO UFO (no Wilson coefficient; mu_R and mu_F both by reweighting), v of its param card
    pco = WORK / "ppo" / "Cards" / "param_card.dat"
    if pco.exists():
        vo = card_value(pco, "higgs", 1)
        print("    own UFO: v = %.6f GeV" % vo)
        for order in ("LO", "NLO"):
            hw = WORK / "ppo" / "Events" / ("o_%s" % order) / "MADatNLO.HwU"
            if not hw.exists():
                print("    no %s" % hw)
                continue
            h = dy.read_hwu(hw)
            labels, rows = h["total"]
            for k, xr, xf in dy.scale_columns(labels):
                own = sigma(lums, pdf.alphasQ, vo, xr * mu0, xf * mu0, order, wilson=False, parts=("gg", "qg"))
                mg, err = rows[0][k], rows[0][3] * max(1.0, abs(rows[0][k] / rows[0][2]))
                pull = (mg - own) / err
                out.append(["o_%s" % order, "total", "%g,%g" % (xr, xf), "%.8e" % own, "%.8e" % mg, "%.3e" % err, "%.2f" % pull])
                print("    o_%-4s muR,F = %3g,%3g  own %.6f  MG5 %.6f +- %.4f  (%+.2f sigma, %+.1e)"
                      % (order, xr, xf, own, mg, err, pull, mg / own - 1))
            if order == "LO":
                labels, rows = h["yH"]
                edges = np.array([r[0] for r in rows] + [rows[-1][1]])
                ylo = lo_rapidity(lums[mu0], pdf.alphasQ, vo, mu0, edges)
                pulls = [(r[2] - o) / r[3] for r, o in zip(rows, ylo) if r[3] > 0]
                print("    o_LO   yH: %d bins, chi2 = %.1f, max |pull| %.2f" % (len(pulls), sum(p * p for p in pulls), max(abs(p) for p in pulls)))
                out.append(["o_LO", "yH", "%d bins" % len(pulls), "chi2", "%.2f" % sum(p * p for p in pulls), "max_abs_pull",
                            "%.2f" % max(abs(p) for p in pulls)])
    # q qbar -> x0 g at LO with MadEvent (mu_R = mu_F = M) against the own q qbar part of the NLO
    banner = sorted((WORK / "qqh" / "Events" / "qq").glob("*banner.txt")) if (WORK / "qqh").exists() else []
    if banner:
        txt = banner[0].read_text()
        mg = float(re.findall(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)", txt)[-1])
        log = (WORK / "qqh.log").read_text()
        m = re.findall(r"Cross-section :\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)", log)
        err = float(m[-1][1]) if m else float("nan")
        own_qq = parts["qq"]
        print("    q qbar -> x0 g (LO, MadEvent): own %.6f pb  MG5 %.6f +- %.6f  (%+.2f sigma, %+.1e)"
              % (own_qq, mg, err, (mg - own_qq) / err, mg / own_qq - 1))
        out.append(["qq_LO_madevent", "qqbar_part", "1,1", "%.8e" % own_qq, "%.8e" % mg, "%.3e" % err, "%.2f" % ((mg - own_qq) / err)])
    with open(RES / "gh_hadronic.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "quantity", "xiR,xiF", "own_pb", "mg5_pb", "mg5_err_pb", "pull"])
        w.writerows(out)
    print("written: results/gh_hadronic.csv")


if __name__ == "__main__":
    main()
