"""Research note models/sm_pp, step (4a): the SSM Z' of stage 6 of the LHC tools (environment.pdf; tests/lhc/zprime/ZpSSM.fr, the
runs and limits of tests/lhc/test_zprime.py, read here without change) at NLO in QCD with the note's Drell-Yan coefficient functions.

  dsigma/dQ^2 = (sigma_0(Q^2)/Q^2) sum_q 2 { [G_qqbar (x) Delta_qqbar] + [(G_qg + G_qbarg) (x) Delta_qg] }   (dy_hadronic.py),
  sigma_0 = (1/3) Q^2/(48 pi) g^4 (gL_q^2 + gR_q^2)(gL_e^2 + gR_e^2)/((Q^2 - M^2)^2 + M^2 Gamma^2),  g = e/(s_W c_W), gL = T3 - Q s_W^2,
  gR = -Q s_W^2 (stage 6's own_sigma: q qbar -> Z' -> e+ e-, one lepton flavour), q = u, d, s, c (stage 6: the b is massive and not
  in the proton), NNPDF4.0 NLO, mu_R = mu_F = M fixed (as stage 6's MG5 runs), Gamma of MadWidth (the run's banner).
The coefficient functions are those of the photon and the Z (vector and axial currents give the same Delta for massless quarks,
step (1)), so the Z' needs only its sigma_0.
Checks: (1) LO against stage 6's own integral (test_zprime.own_sigma) and MG5's LO (runs m<M> without cuts, xs<M> with m_ll > 225
GeV; references of stage 6); (2) doubled nodes; then the NLO: K = sigma_NLO/sigma_LO for the whole m_ll range (10 GeV to 13 TeV)
and |m_ll - M| < 2 Gamma, the 9-point scale range, and K(m) = (dsigma/dm)_NLO/(dsigma/dm)_LO on a grid of m_ll for each M
(results/zp_kfactor.csv, for the NLO limits of zp_limit.py).
Writes results/zp_hadronic.csv.  Run with ~/hep/opt/lhc/bin/python (from Src/).
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
import dy_hadronic as dy  # noqa: E402

LHC = SRC.parents[2] / "environment" / "tests" / "lhc"
sys.path.insert(0, str(LHC))
import test_zprime as tz  # noqa: E402

RES = SRC / "results"
QUARKS = (("u", 2), ("d", 1), ("s", 3), ("c", 4))
QLO, QHI = 10.0, 12999.0   # the m_ll range of stage 6's own integral


def zp_params(M):
    """the run's parameters: g = e/(s_W c_W), s_W^2, the couplings, the MadWidth width, MG5's LO sigma (pb, e and mu together)"""
    vals, W, xs, _ = tz.card(M)
    g, sw2 = tz.ew(vals)
    cpl = {f: tz.couplings(f, sw2)[:2] for f in ("u", "d", "s", "c", "e")}
    return dict(M=M, W=W, g=g, sw2=sw2, cpl=cpl, xs_mg5=xs, xs_mg5_cut=tz.xs_cut(M), vals=vals)


def sigma0(q2, q, p):
    """q qbar -> Z' -> e+ e- at shat = Q^2 (GeV^-2), averaged over the colours and spins"""
    glq, grq = p["cpl"][q]
    gle, gre = p["cpl"]["e"]
    M, W = p["M"], p["W"]
    return q2 / (48 * math.pi) * p["g"] ** 4 * (glq ** 2 + grq ** 2) * (gle ** 2 + gre ** 2) / ((q2 - M * M) ** 2 + M * M * W * W) / 3


def dsigma_dq2(q2, p, lum, as4pi, lf, order, n1=96, n2=64):
    """dsigma/dQ^2 (GeV^-4) at one Q^2"""
    tot = 0.0
    for q, pid in QUARKS:
        tot += sigma0(q2, q, p) / q2 * dy.conv(lum, [(pid, -pid)], [(pid, 21), (-pid, 21)], q2 / dy.S, lf, as4pi, order, n1, n2)
    return tot


def sigma(p, lums, alphas, xr, xf, order, qlo=QLO, qhi=QHI, nq=40, n1=96, n2=64):
    """sigma(p p -> Z' -> e+ e-) in pb for qlo < m_ll < qhi, mu_R = xr M, mu_F = xf M"""
    M = p["M"]
    lum = lums[xf * M]
    as4pi = alphas(xr * M) / (4 * math.pi)
    q2s, dq2 = dy.qnodes(qlo, qhi, M, p["W"], nq)
    tot = 0.0
    for q2, dq in zip(q2s, dq2):
        lf = math.log((xf * M) ** 2 / q2)
        tot += dq * dsigma_dq2(q2, p, lum, as4pi, lf, order, n1, n2)
    return tot * dy.GEV2PB


def main():
    RES.mkdir(exist_ok=True)
    dy.lhapdf.setVerbosity(0)
    pdf = dy.lhapdf.mkPDF(dy.PDFNAME, 0)
    out, kout = [], []
    print("(1) LO against stage 6 (own integral of test_zprime.py; MG5 LO, references of stage 6);  (2) doubled nodes;  (3) NLO")
    for M in tz.MASSES:
        p = zp_params(M)
        lums = {f * M: dy.Lumi(pdf, f * M, QLO ** 2 / dy.S / 2) for f in (1.0, 2.0, 0.5)}
        lo = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "LO")
        st6 = tz.own_sigma(M, p["W"], p["vals"], pdf)
        lo_cut = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "LO", qlo=225.0)
        nlo = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "NLO")
        nlo2 = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "NLO", nq=80, n1=192, n2=128)
        nlo_cut = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "NLO", qlo=225.0)
        pk = (M - 2 * p["W"], M + 2 * p["W"])
        lo_pk = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "LO", qlo=pk[0], qhi=pk[1])
        nlo_pk = sigma(p, lums, pdf.alphasQ, 1.0, 1.0, "NLO", qlo=pk[0], qhi=pk[1])
        sc = [sigma(p, lums, pdf.alphasQ, xr, xf, "NLO") / nlo - 1 for xr in (0.5, 1.0, 2.0) for xf in (0.5, 1.0, 2.0)]
        # stage 6's sigma_SSM: MG5 (e and mu together), halved per flavour
        mg, mgc = p["xs_mg5"] / 2, (p["xs_mg5_cut"] / 2 if p["xs_mg5_cut"] else float("nan"))
        print("    M = %4d GeV (Gamma/M %.4f): LO %.6g pb (stage 6 own %+.1e;  MG5 %+.1e, m_ll > 225: %+.1e);  nodes %+.1e;"
              "  NLO %.6g pb, K = %.4f (m_ll > 225: %.4f, |m - M| < 2 Gamma: %.4f);  9-point %+.3f %+.3f"
              % (M, p["W"] / M, lo, st6 / lo - 1, mg / lo - 1, mgc / lo_cut - 1, nlo2 / nlo - 1, nlo, nlo / lo, nlo_cut / lo_cut,
                 nlo_pk / lo_pk, min(sc), max(sc)))
        out.append([M, "%.6g" % p["W"], "%.8e" % lo, "%.8e" % st6, "%.8e" % mg, "%.8e" % nlo, "%.6f" % (nlo / lo),
                    "%.6f" % (nlo_cut / lo_cut), "%.6f" % (nlo_pk / lo_pk), "%.5f" % min(sc), "%.5f" % max(sc), "%.2e" % (nlo2 / nlo - 1)])
        # K(m) on a grid of m_ll (mu_F = mu_R = M), for the reweighting of the stage-6 events
        lum = lums[M]
        as4pi = pdf.alphasQ(M) / (4 * math.pi)
        for m in np.concatenate([np.geomspace(QLO, 0.9 * M, 40), np.linspace(0.9 * M, min(1.1 * M, QHI), 21)[1:],
                                 np.geomspace(min(1.1 * M, QHI), QHI, 12)[1:]]):
            q2 = m * m
            lf = math.log(M * M / q2)
            k = dsigma_dq2(q2, p, lum, as4pi, lf, "NLO") / dsigma_dq2(q2, p, lum, as4pi, lf, "LO")
            kout.append([M, "%.6g" % m, "%.6f" % k])
    with open(RES / "zp_hadronic.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["M_GeV", "Gamma_GeV", "LO_pb", "stage6_own_LO_pb", "stage6_MG5_LO_pb", "NLO_pb", "K", "K_mll_gt_225",
                    "K_peak_2Gamma", "scale_min", "scale_max", "nodes_check"])
        w.writerows(out)
    with open(RES / "zp_kfactor.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["M_GeV", "m_ll_GeV", "K"])
        w.writerows(kout)
    print("written: results/zp_hadronic.csv, results/zp_kfactor.csv")


if __name__ == "__main__":
    main()
