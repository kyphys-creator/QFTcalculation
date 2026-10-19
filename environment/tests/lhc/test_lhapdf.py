"""Stage 1 of the LHC tools (environment.pdf): LHAPDF 6 and the PDF sets.

  (a) the sum rules of each set's central member at Q = 100 GeV, from the grids (x from the grid's x_min to 1):
        momentum  int_0^1 dx x [g + sum_q (q + qbar)] = 1,   valence  int (u - ubar) = 2, int (d - dbar) = 1, int (s - sbar) = 0;
        a grid that stops at x_min = 1e-6 (PDF4LHC21) misses the valence below it (about 1%);
  (b) LO sigma(p p -> e+ e-), 13 TeV, 60 < m_ee < 120 GeV, no lepton cuts, against MadGraph (madevent):
        sigma = sum_q int dM^2 dy (1/s) [f_q(x1) f_qbar(x2) + f_qbar(x1) f_q(x2)] sigma_hat_q(M^2),  x_{1,2} = (M/sqrt s) e^{+-y},
        sigma_hat_q = (1/N_c) (shat/(48 pi)) sum_{i,j = L,R} |e^2 Q_q Q_e/shat + g_i^q g_j^e/(shat - M_Z^2 + i M_Z Gamma_Z)|^2,
        g_L^f = (e/(s c))(T3 - Q s^2), g_R^f = -(e/(s c)) Q s^2, the parameters of MG5's 'sm' (aEWM1, Gf, MZ, WZ; M_W derived),
        the four flavours u, d, s, c of MG5's default proton, a fixed factorization scale M_Z;
  (c) LO sigma(g g -> H) in the heavy-top EFT UFO of models/sm_higgs (the operator -(1/4) cHgg (H/v) G G):
        sigma = pi^2 Gamma(H -> g g)/(8 M_H s) int_tau^1 dx/x g(x) g(tau/x),  Gamma = cHgg^2 M_H^3/(8 pi v^2),  tau = M_H^2/s,
        v = 2 M_W s_W/e of that UFO (aEWM1, MZ, MW inputs), a fixed factorization scale M_H.
The MG5 values are read from the runs of run_stage1.sh (out/); the parameters from the param_card each run used.
Usage: python3 test_lhapdf.py [sumrules | dy | ggh]
"""
import cmath
import math
import re
import sys
from pathlib import Path

import warnings

from scipy.integrate import IntegrationWarning, quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / "hep/MG5_aMC_v3_8_1/HEPTools/lhapdf6_py3/lib/python3.12/site-packages"))
import lhapdf  # noqa: E402

lhapdf.setVerbosity(0)
SETS = ["NNPDF40_nlo_as_01180", "CT18NNLO", "PDF4LHC21_40"]
SQRTS = 13000.0
GEV2PB = 0.3893794e9


def card(path):
    """name -> value of a param_card (the comment after # names the parameter; MG5 3.8 writes the names in lower case)"""
    vals = {}
    for line in open(path):
        m = re.match(r"\s+\d+(?:\s+\d+)?\s+([-+0-9.eE]+)\s+#\s+(\S+)", line)
        if m:
            vals[m.group(2).lower()] = float(m.group(1))
        m = re.match(r"DECAY\s+(\d+)\s+([-+0-9.eE]+)", line)
        if m:
            vals["w%s" % m.group(1)] = float(m.group(2))
    return vals


def mg5_sigma(run):
    """the cross section [pb] and its error of the madevent run in out/<run>_proc: the log prints 4 digits, so the value is
    read from the banner's 'Integrated weight (pb)' and the error from the first line of SubProcesses/results.dat"""
    proc = HERE / "out" / ("%s_proc" % run)
    banner = sorted((proc / "Events" / "run_01").glob("*banner.txt"))[-1].read_text()
    val = float(re.search(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)", banner).group(1))
    err = float((proc / "SubProcesses" / "results.dat").read_text().split()[1])
    return val, err


def sumrules():
    print("(a) sum rules of the central members at Q = 100 GeV (LHAPDF %s)" % lhapdf.version())
    for name in SETS:
        p = lhapdf.mkPDF(name, 0)
        q2 = 100.0**2
        xmin = max(p.xMin, 1e-9)

        def xf(pid, x):
            return p.xfxQ2(pid, x, q2)

        def integ(fun):
            # split in ln x below 0.1 (x f is small but f = xf/x is large)
            lo = quad(lambda t: fun(math.exp(t)) * math.exp(t), math.log(xmin), math.log(0.1), limit=400, epsrel=1e-9)[0]
            hi = quad(fun, 0.1, 1.0, limit=400, epsrel=1e-9)[0]
            return lo + hi

        # xfxQ2 returns x f(x): the momentum sum integrates x f, the valence numbers f = (x f)/x
        mom = integ(lambda x: xf(21, x) + sum(xf(i, x) + xf(-i, x) for i in range(1, 7)))
        uv = integ(lambda x: (xf(2, x) - xf(-2, x)) / x)
        dv = integ(lambda x: (xf(1, x) - xf(-1, x)) / x)
        sv = integ(lambda x: (xf(3, x) - xf(-3, x)) / x)
        print("  %-22s members %3d, x_min %.0e, alpha_s(M_Z) %.5f (set metadata %s);  momentum %.6f, u_v %.5f, d_v %.5f, "
              "s - sbar %+.1e" % (name, p.set().size, p.xMin, p.alphasQ(91.1876), p.set().get_entry("AlphaS_MZ"), mom, uv, dv, sv))


def dy():
    c = card(HERE / "out" / "dy_param_card.dat")
    aew, gf, mz, wz = 1 / c["aewm1"], c["gf"], c["mz"], c["w23"]
    mw = math.sqrt(mz**2 / 2 + math.sqrt(mz**4 / 4 - math.pi * aew * mz**2 / (math.sqrt(2) * gf)))
    s2 = 1 - mw**2 / mz**2
    e2 = 4 * math.pi * aew
    e, sc = math.sqrt(e2), math.sqrt(s2 * (1 - s2))
    ferm = {1: (-1 / 3, -0.5), 2: (2 / 3, 0.5), 3: (-1 / 3, -0.5), 4: (2 / 3, 0.5)}
    ge = ((e / sc) * (-0.5 + s2), (e / sc) * s2)                    # e-: Q = -1, T3 = -1/2

    def shat_sigma(sh, q, t3):
        gq = ((e / sc) * (t3 - q * s2), -(e / sc) * q * s2)
        prop = 1 / complex(sh - mz**2, mz * wz)
        tot = sum(abs(e2 * q * (-1) / sh + gq[i] * ge[j] * prop)**2 for i in (0, 1) for j in (0, 1))
        return sh / (48 * math.pi) * tot / 3

    s = SQRTS**2
    print("(b) LO sigma(p p -> e+ e-), 13 TeV, 60 < m_ee < 120 GeV, mu_F = M_Z;  MG5 'sm': M_W = %.4f, s_W^2 = %.5f" % (mw, s2))
    for name in SETS[:1]:
        p = lhapdf.mkPDF(name, 0)
        q2 = mz**2

        def dsig(m2):
            tau = m2 / s
            ymax = -0.5 * math.log(tau)

            def fy(y):
                x1, x2 = math.sqrt(tau) * math.exp(y), math.sqrt(tau) * math.exp(-y)
                return sum((p.xfxQ2(i, x1, q2) * p.xfxQ2(-i, x2, q2) + p.xfxQ2(-i, x1, q2) * p.xfxQ2(i, x2, q2))
                           * shat_sigma(m2, *ferm[i]) for i in ferm) / (x1 * x2)
            return quad(fy, -ymax, ymax, epsrel=1e-9, limit=200)[0] / s

        own = quad(dsig, 60.0**2, 120.0**2, points=[mz**2], epsrel=1e-8, limit=200)[0] * GEV2PB
        mg, err = mg5_sigma("dy")
        print("  %s: own %.6g pb;  MG5 %.6g +- %.2g pb;  MG5/own - 1 = %+.2e (%.2f sigma)"
              % (name, own, mg, err, mg / own - 1, (mg - own) / err))


def ggh():
    c = card(HERE / "out" / "ggh_param_card.dat")
    aew, mz, mw, mh, chgg = 1 / c["aewm1"], c["mz"], c["mw"], c["mh"], c["chgg"]
    sw = math.sqrt(1 - mw**2 / mz**2)
    vev = 2 * mw * sw / math.sqrt(4 * math.pi * aew)
    gam = chgg**2 * mh**3 / (8 * math.pi * vev**2)
    s = SQRTS**2
    tau = mh**2 / s
    print("(c) LO sigma(g g -> H), 13 TeV, mu_F = M_H, the HEFT UFO: v = %.4f GeV, cHgg = %g, Gamma(H -> g g) = %.6e GeV"
          % (vev, chgg, gam))
    p = lhapdf.mkPDF(SETS[0], 0)
    q2 = mh**2
    lum = quad(lambda t: p.xfxQ2(21, math.exp(t), q2) * p.xfxQ2(21, tau / math.exp(t), q2) / tau,
               math.log(tau), 0.0, epsrel=1e-10, limit=400)[0]          # int dx/x g(x) g(tau/x), with x g = xfx
    own = math.pi**2 * gam / (8 * mh * s) * lum * GEV2PB
    mg, err = mg5_sigma("ggh")
    print("  %s: own %.6g pb;  MG5 %.6g +- %.2g pb;  MG5/own - 1 = %+.2e (%.2f sigma)"
          % (SETS[0], own, mg, err, mg / own - 1, (mg - own) / err))


if __name__ == "__main__":
    warnings.simplefilter("ignore", IntegrationWarning)   # quad's roundoff note at epsrel 1e-9; the values are stable to 1e-7
    which = sys.argv[1:] or ["sumrules", "dy", "ggh"]
    for w in which:
        {"sumrules": sumrules, "dy": dy, "ggh": ggh}[w]()
