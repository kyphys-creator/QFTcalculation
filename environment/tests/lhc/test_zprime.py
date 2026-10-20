"""Stage 6 of the LHC tools (environment.pdf): the SSM Z' of zprime/ZpSSM.fr end to end (the runs of run_stage6.sh).

  (a) the Z' width at each mass: MadWidth (two-body, the run's param_card) against own
      Gamma = sum_f N_c M (ee/(sw cw))^2 beta [gV^2 (1 + 2x) + gA^2 (1 - 4x)]/(48 pi),  gV = gL + gR, gA = gL - gR,
      gL = T3 - Q sw^2, gR = -Q sw^2, x = m_f^2/M^2 (t, b, tau massive; SM.fr's inputs aEWM1, Gf, MZ);
  (b) sigma(p p > zp > l+ l-) of MG5 (l = e, mu; NNPDF4.0 NLO, mu_F = M, |m_ll - M| < 15 Gamma, no lepton cuts) against own
      integral of qqbar -> Z' -> l l (u, d, s, c; the Breit-Wigner of the MadWidth width) over the same LHAPDF set: with
      m_ll > 225 GeV (MG5 runs xs<M> with mmll 225) and without a cut (the runs of the samples; MG5 does not cut the Z'
      virtuality for the s-channel syntax 'p p > zp > l+ l-': bwcutoff acts only on resonances of decay chains);
  (c) Delphes (the ATLAS card as distributed, and with the electron and muon isolation summed over the tracks only, as
      ATLAS's track isolation, outside Delta R = 0.01 so that the candidate's own track is not counted; the distributed card
      sums the energy-flow objects, photons included, in Delta R < 0.5 with pT ratio < 0.12, and loses the electrons with
      collinear FSR): the dielectron and dimuon selections of the search (pT > 30 GeV; electrons |eta| < 2.47 without
      1.37-1.52, muons |eta| < 2.5 and opposite charges; m_ll > 225 GeV): A x eff, and the efficiency relative to own fiducial
      region (the hard-process leptons with pT > 30 GeV, |eta| < 2.47 or 2.5), against ATLAS's spin-1 selection efficiency
      (a reference); the relative mass resolution (half width of the central 68% of m_reco/m_true - 1) against ATLAS's
      parametrisation (a reference);
  (d) the limits: the published dielectron and dimuon spectra (139 fb^-1, 225 GeV to 5.8 TeV) with the published background
      function, fitted (normalisation, b, p0..p3 free in each channel); own signal templates (the Delphes m_ll of (c)); the
      binned Poisson likelihood with the background parameters profiled, qtilde, asymptotic CLs (the formulas of test_pyhf.py);
      the 95% CL upper limits on sigma x B(Z' -> l l) per lepton flavour, observed and expected, as fiducial limits (times own
      fiducial acceptance) against ATLAS's for a 3% width (references), and against the SSM cross section of (b): the ratio
      against ATLAS's ratio table, and the SSM mass limit (5.1 TeV in the paper, with NNLO cross sections; a reference).
Run with ~/hep/opt/lhc/bin/python.  Uses LHAPDF from MG5's HEPTools.
"""
import csv
import glob
import math
import re
import sys
from pathlib import Path

import awkward as ak
import numpy as np
import uproot
from scipy.optimize import brentq, minimize
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "zprime"
HD = Path.home() / "hep" / "data" / "hepdata-ins1725190"
sys.path.insert(0, str(Path.home() / "hep" / "MG5_aMC_v3_8_1" / "HEPTools" / "lhapdf6_py3" / "lib" / "python3.12" / "site-packages"))
import lhapdf  # noqa: E402

LUMI = 139.0  # fb^-1
MASSES = [500, 1000, 2000, 3000, 4000, 4500, 5000, 5500, 6000]
# (T3, Q, N_c) and the mass parameter of the restricted UFO (None: massless)
FERMIONS = {"nu": (0.5, 0, 1, None), "e": (-0.5, -1, 1, None), "mu": (-0.5, -1, 1, None), "ta": (-0.5, -1, 1, "MTA"),
            "u": (0.5, 2 / 3, 3, None), "c": (0.5, 2 / 3, 3, None), "t": (0.5, 2 / 3, 3, "MT"),
            "d": (-0.5, -1 / 3, 3, None), "s": (-0.5, -1 / 3, 3, None), "b": (-0.5, -1 / 3, 3, "MB")}
NNU = 3


def card(m):
    """the run's param_card (from the banner): name -> value, and the Z' width"""
    banner = glob.glob(str(OUT / "zp_proc" / "Events" / ("m%d" % m) / "*banner.txt"))[0]
    txt = Path(banner).read_text()
    pc = txt[txt.index("<slha>"):txt.index("</slha>")]
    vals = {}
    for line in pc.splitlines():
        mm = re.match(r"\s*\d+\s+([-+0-9.eE]+)\s+#\s*(\w+)", line)
        if mm:
            vals[mm.group(2).lower()] = float(mm.group(1))
    w = float(re.search(r"^DECAY\s+32\s+([-+0-9.eE]+)", pc, re.M).group(1))
    xs = float(re.findall(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)", txt)[-1])
    return vals, w, xs, txt


def ew(vals):
    """SM.fr's internal parameters from aEWM1, Gf, MZ"""
    aew = 1 / vals["aewm1"]
    mz, gf = vals["mz"], vals["gf"]
    mw = math.sqrt(mz ** 2 / 2 + math.sqrt(mz ** 4 / 4 - aew * math.pi * mz ** 2 / (gf * math.sqrt(2))))
    sw2 = 1 - mw ** 2 / mz ** 2
    ee = 2 * math.sqrt(aew * math.pi)
    return ee / math.sqrt(sw2 * (1 - sw2)), sw2


def couplings(f, sw2):
    t3, q, nc, mpar = FERMIONS[f]
    return t3 - q * sw2, -q * sw2, nc, mpar


def own_width(M, vals):
    g, sw2 = ew(vals)
    tot, parts = 0.0, {}
    for f in FERMIONS:
        gl, gr, nc, mpar = couplings(f, sw2)
        mf = vals[mpar.lower()] if mpar else 0.0
        if 2 * mf >= M:
            continue
        x = (mf / M) ** 2
        beta = math.sqrt(1 - 4 * x)
        gv, ga = gl + gr, gl - gr
        w = nc * M * g ** 2 * beta * (gv ** 2 * (1 + 2 * x) + ga ** 2 * (1 - 4 * x)) / (48 * math.pi)
        w *= NNU if f == "nu" else 1
        parts[f] = w
        tot += w
    return tot, parts


def own_sigma(M, W, vals, pdf, mmin=10.0, mmax=12999.0):
    """sigma(p p > Z' > e+ e-) in pb: sum over q = u, d, s, c of [q(x1) qbar(x2) + qbar(x1) q(x2)] sigma_hat, sigma_hat =
    (1/3) shat/(48 pi) g^4 (gLq^2 + gRq^2)(gLe^2 + gRe^2)/((shat - M^2)^2 + M^2 W^2), mmin < m = sqrt(shat) < mmax"""
    g, sw2 = ew(vals)
    gle, gre, _, _ = couplings("e", sw2)
    S = 13000.0 ** 2
    mlo, mhi = mmin, mmax
    # Gauss-Legendre in m (fine near the peak through the substitution m = M + W tan(t)), and in y
    tl, th = math.atan((mlo - M) / W), math.atan((mhi - M) / W)
    xt, wt = np.polynomial.legendre.leggauss(400)
    t = 0.5 * (th - tl) * xt + 0.5 * (th + tl)
    wts = 0.5 * (th - tl) * wt
    m = M + W * np.tan(t)
    dm = W / np.cos(t) ** 2
    xy, wy = np.polynomial.legendre.leggauss(96)
    total = 0.0
    q2 = M * M
    flav = {"u": 2, "d": 1, "s": 3, "c": 4}
    for i in range(len(m)):
        shat = m[i] ** 2
        tau = shat / S
        ymax = -0.5 * math.log(tau)
        y = ymax * xy
        x1, x2 = np.sqrt(tau) * np.exp(y), np.sqrt(tau) * np.exp(-y)
        lum = 0.0
        for f, pid in flav.items():
            glq, grq, _, _ = couplings(f, sw2)
            c = (glq ** 2 + grq ** 2)
            fq1 = np.array([pdf.xfxQ2(pid, a, q2) for a in x1]) / x1
            fa1 = np.array([pdf.xfxQ2(-pid, a, q2) for a in x1]) / x1
            fq2 = np.array([pdf.xfxQ2(pid, a, q2) for a in x2]) / x2
            fa2 = np.array([pdf.xfxQ2(-pid, a, q2) for a in x2]) / x2
            lum += c * ymax * np.sum(wy * (fq1 * fa2 + fa1 * fq2))
        sig = (1 / 3) * shat / (48 * math.pi) * g ** 4 * (gle ** 2 + gre ** 2) / ((shat - M * M) ** 2 + M * M * W * W)
        # d tau = 2 m dm / S
        total += wts[i] * dm[i] * 2 * m[i] / S * lum * sig
    return total * 0.3893793721e9  # GeV^-2 -> pb


def xs_cut(m):
    """MG5's sigma with mmll > 225 GeV (run xs<M>), pb, and its error"""
    banner = glob.glob(str(OUT / "zp_proc" / "Events" / ("xs%d" % m) / "*banner.txt"))
    if not banner:
        return None
    txt = Path(banner[0]).read_text()
    return float(re.findall(r"Integrated weight \(pb\)\s*:\s*([0-9.eE+-]+)", txt)[-1])


def part_ab():
    pdf = lhapdf.mkPDF("NNPDF40_nlo_as_01180", 0)
    print("(a) the Z' width (MadWidth, two-body) against own formula;  (b) sigma(p p > zp > l+ l-, l = e, mu) of MG5 against own"
          " integral (x 2 flavours), with m_ll > 225 GeV and without a cut")
    res = {}
    for M in MASSES:
        vals, W, xs, _ = card(M)
        w_own, parts = own_width(M, vals)
        s_cut = 2 * own_sigma(M, W, vals, pdf, mmin=225.0)
        s_all = 2 * own_sigma(M, W, vals, pdf)
        s_pk = 2 * own_sigma(M, W, vals, pdf, mmin=M - 2 * W, mmax=M + 2 * W)
        xc = xs_cut(M)
        res[M] = (W, xs, s_all)
        print("    M = %4d GeV: Gamma MadWidth %.6g, own %.6g GeV (%+.1e), Gamma/M = %.4f;  sigma(m_ll > 225) MG5 %s, own %.6g pb (%s);"
              "  no cut: MG5 %.6g, own %.6g pb (%+.2e)" % (
                  M, W, w_own, W / w_own - 1, W / M, "%.6g" % xc if xc else "-", s_cut, "%+.1e" % (xc / s_cut - 1) if xc else "-",
                  xs, s_all, xs / s_all - 1))
        print("        own: |m_ll - M| < 2 Gamma holds %.3f of sigma, m_ll > 225 GeV %.3f (the rest is the off-shell tail that the"
              " parton luminosity raises)" % (s_pk / s_all, s_cut / s_all))
    return res


# ---------------------------------------------------------------- (c) Delphes
CARDS = {"": "the ATLAS card as distributed", "trkiso_": "the ATLAS card with track-only lepton isolation"}


def events(M, tag):
    t = uproot.open(OUT / ("delphes_%sm%d.root" % (tag, M)))["Delphes"]
    a = t.arrays(["Electron.PT", "Electron.Eta", "Electron.Phi", "Electron.Charge", "Muon.PT", "Muon.Eta", "Muon.Phi",
                  "Muon.Charge", "Particle.PID", "Particle.Status", "Particle.PT", "Particle.Eta", "Particle.Phi", "Particle.Mass",
                  "Particle.E", "Particle.Px", "Particle.Py", "Particle.Pz"])
    return a


def mass(pt1, eta1, phi1, pt2, eta2, phi2):
    return np.sqrt(2 * pt1 * pt2 * (np.cosh(eta1 - eta2) - np.cos(phi1 - phi2)))


def select(a, flav):
    if flav == "e":
        pt, eta, phi, q = a["Electron.PT"], a["Electron.Eta"], a["Electron.Phi"], a["Electron.Charge"]
        ok = (pt > 30) & (abs(eta) < 2.47) & ~((abs(eta) > 1.37) & (abs(eta) < 1.52))
    else:
        pt, eta, phi, q = a["Muon.PT"], a["Muon.Eta"], a["Muon.Phi"], a["Muon.Charge"]
        ok = (pt > 30) & (abs(eta) < 2.5)
    pt, eta, phi, q = pt[ok], eta[ok], phi[ok], q[ok]
    two = ak.num(pt) >= 2
    p = ak.pad_none(pt, 2)
    e = ak.pad_none(eta, 2)
    f = ak.pad_none(phi, 2)
    c = ak.pad_none(q, 2)
    mll = ak.fill_none(mass(p[:, 0], e[:, 0], f[:, 0], p[:, 1], e[:, 1], f[:, 1]), 0)
    sel = ak.to_numpy(two) & (ak.to_numpy(mll) > 225)
    if flav == "mu":
        sel &= ak.to_numpy(ak.fill_none(c[:, 0] * c[:, 1], 0)) < 0
    return sel, ak.to_numpy(mll)


def truth(a):
    """the channel (11 or 13), the fiducial flag (both hard-process leptons pT > 30 GeV and |eta| < 2.47 (e) or 2.5 (mu)), and
    m_true (the Z' of status 22)"""
    pid, st = a["Particle.PID"], a["Particle.Status"]
    hard = (st == 23) & ((abs(pid) == 11) | (abs(pid) == 13))
    lp = abs(pid[hard])
    ch = ak.to_numpy(ak.fill_none(ak.firsts(lp), 0))
    pt, eta = a["Particle.PT"][hard], a["Particle.Eta"][hard]
    etamax = np.where(ch == 11, 2.47, 2.5)
    fid = ak.to_numpy(ak.all((pt > 30) & (abs(eta) < etamax[:, None] * ak.ones_like(eta)), axis=1)) & (ak.to_numpy(ak.num(pt)) == 2)
    zp = st == 22
    zp = zp & (pid == 32)
    mt = ak.to_numpy(ak.fill_none(ak.firsts(a["Particle.Mass"][zp]), np.nan))
    return ch, fid, mt


def atlas_eff(flav, M):
    rows, block = [], None
    for line in (HD / "Selection_efficiency_for_spin-0_spin-1_and_spin-2_resonances.csv").read_text().splitlines():
        if line.startswith("#: INDEX"):
            block = int(line.split(",")[1])
        elif block == (2 if flav == "e" else 5) and line[:1].isdigit():
            m, v = line.split(",")
            if v.strip() != "-":
                rows.append((float(m), float(v)))
    rows = np.array(rows)
    return float(np.interp(M, rows[:, 0], rows[:, 1]))


def atlas_resolution(flav, m):
    """ATLAS's relative mass resolution sqrt(kappa sigma_CB^2 + (1 - kappa) sigma_G^2) at m_true (the HEPData parameters and
    the formulas of pseudoCode_massResolutionParametrisation.txt)"""
    name = "Relative_dielectron_mass_resolution_parameters.csv" if flav == "e" else "Relative_dimuon_mass_resolution_parameters.csv"
    p = {}
    pat = r"p_\{\\?(mu|sigma|alpha|kappa|n)(?:_\\mathrm\{(CB|G)\})?,(\d)\} = ([-0-9.]+(?:\s*\\cdot\s*10\^\{-?\d+\})?)"
    for line in (HD / name).read_text().splitlines():
        for key, sub, idx, val in re.findall(pat, line):
            # 'a \cdot 10^{b}' (with or without the spaces) -> 'aeb'
            p[(key + ("_" + sub if sub else ""), int(idx))] = float(re.sub(r"\s*\\cdot\s*10\^\{(-?\d+)\}", r"e\1", val))
    L = math.log(m)
    q = lambda k, i: p[(k, i)]
    if flav == "e":
        s_cb = math.sqrt(q("sigma_CB", 1) ** 2 + (q("sigma_CB", 2) / math.sqrt(m)) ** 2 + (q("sigma_CB", 3) / m) ** 2)
        s_g = math.sqrt(q("sigma_G", 1) ** 2 + (q("sigma_G", 2) / math.sqrt(m)) ** 2 + (q("sigma_G", 3) / m) ** 2)
        k = q("kappa", 1) + q("kappa", 2) * math.exp(-q("kappa", 3) * m) + q("kappa", 4) * m + q("kappa", 5) * m ** 3
    else:
        s_cb = q("sigma_CB", 1) + q("sigma_CB", 2) / m + q("sigma_CB", 3) / m ** 2 + q("sigma_CB", 4) * m + q("sigma_CB", 5) * m ** 2
        s_g = q("sigma_G", 1) + q("sigma_G", 2) / m + q("sigma_G", 3) / m ** 2 + q("sigma_G", 4) * m + q("sigma_G", 5) * m ** 2
        k = q("kappa", 1) + q("kappa", 2) / m + q("kappa", 3) / m ** 2 + q("kappa", 4) * m + q("kappa", 5) * m ** 2
    return math.sqrt(k * s_cb ** 2 + (1 - k) * s_g ** 2)


def part_c(tag):
    print("(c) Delphes, %s: the selections; A x eff, and eff relative to own fiducial region, against ATLAS's spin-1"
          " selection efficiency (a reference); the relative resolution against ATLAS's (a reference)" % CARDS[tag])
    out = {}
    for M in MASSES:
        a = events(M, tag)
        ch, fid, mt = truth(a)
        for flav, code in (("e", 11), ("mu", 13)):
            sel, mll = select(a, flav)
            inch = ch == code
            n = inch.sum()
            nsel = (sel & inch).sum()
            nfid = (fid & inch).sum()
            r = mll[sel & inch] / mt[sel & inch] - 1
            r = r[np.isfinite(r)]
            lo, hi = np.percentile(r, [16, 84]) if len(r) else (np.nan, np.nan)
            out[(M, flav)] = dict(n=n, nsel=nsel, nfid=nfid, mll=mll[sel & inch], aeff=nsel / n, afid=nfid / n)
            print("    M = %4d GeV, %-2s: %4d events, A x eff = %.3f +- %.3f, fiducial A = %.3f, eff/fiducial = %.3f;  ATLAS %.3f;"
                  "  resolution: own %.4f, ATLAS %.4f" % (
                      M, flav, n, nsel / n, math.sqrt(nsel / n * (1 - nsel / n) / n), nfid / n, nsel / nfid, atlas_eff(flav, M),
                      0.5 * (hi - lo), atlas_resolution(flav, M)))
    return out


# ---------------------------------------------------------------- (d) limits
def spectrum(flav):
    name = "Dielectron_invariant_mass_spectrum.csv" if flav == "e" else "Dimuon_invariant_mass_spectrum.csv"
    rows = [r for r in csv.reader((HD / name).read_text().splitlines()) if r and r[0][:1].isdigit()]
    lo = np.array([float(r[1]) for r in rows])
    hi = np.array([float(r[2]) for r in rows])
    n = np.array([float(r[3]) for r in rows]) * (hi - lo) / 10.0
    return lo, hi, np.round(n), n


def bkg_shape(m, flav, b, p):
    x = m / 13000.0
    bw = 2.4952 / ((91.1876 - m) ** 2 + 2.4952 ** 2)
    lx = np.log(x)
    base = (1 - x) if flav == "e" else (1 - x ** (1 / 3))
    return bw * np.power(base, b) * np.power(x, p[0] + p[1] * lx + p[2] * lx ** 2 + p[3] * lx ** 3)


class Channel:
    def __init__(self, flav):
        self.flav = flav
        self.lo, self.hi, self.n, self.nraw = spectrum(flav)
        xg, wg = np.polynomial.legendre.leggauss(8)
        self.mg = 0.5 * (self.hi - self.lo)[:, None] * xg[None, :] + 0.5 * (self.hi + self.lo)[:, None]
        self.wg = 0.5 * (self.hi - self.lo)[:, None] * wg[None, :]
        self.th0 = None

    def bkg(self, th):
        """th = (log N, b, p0, p1, p2, p3): the expected counts per bin"""
        f = np.sum(self.wg * bkg_shape(self.mg, self.flav, th[1], th[2:]), axis=1)
        return math.exp(th[0]) * f / f.sum()

    def nll(self, th, s, n):
        lam = np.maximum(self.bkg(th) + s, 1e-300)
        return float(np.sum(lam - n * np.log(lam)))

    def fit(self, s, n, start, global_search=False):
        if global_search:
            r = minimize(lambda th: self.nll(th, s, n), start, method="Nelder-Mead",
                         options=dict(maxiter=20000, maxfev=20000, xatol=1e-8, fatol=1e-9))
            start = r.x
        r = minimize(lambda th: self.nll(th, s, n), start, method="BFGS", options=dict(gtol=1e-6))
        return r.fun, r.x

    def bkg_fit(self):
        start = np.array([math.log(self.n.sum()), 1.5 if self.flav == "e" else 11.0, -12.0, -1.0, -0.1, 0.0])
        best = None
        for b0 in ((1.5, 3.0, 8.0) if self.flav == "e" else (5.0, 11.0, 20.0)):
            start[1] = b0
            f, th = self.fit(np.zeros_like(self.n), self.n, start, global_search=True)
            if best is None or f < best[0]:
                best = (f, th)
        self.th0 = best[1]
        return best


def cls_limit(chans, templates, mu_hi):
    """95% CL upper limits on mu (observed, median expected): qtilde, asymptotic, the background parameters profiled in each
    channel; the Asimov data = the background-only fit to the observed data"""
    asimov = [c.bkg(c.th0) for c in chans]

    def prof(mu, data):
        return sum(c.fit(mu * t, d, c.th0)[0] for c, t, d in zip(chans, templates, data))

    from scipy.optimize import minimize_scalar

    obs = [c.n for c in chans]
    r = minimize_scalar(lambda x: prof(x, obs), bounds=(0.0, 10 * mu_hi), method="bounded", options=dict(xatol=1e-5 * mu_hi))
    mh_o, n0_o = float(r.x), float(r.fun)
    if prof(0.0, obs) <= n0_o:
        mh_o, n0_o = 0.0, prof(0.0, obs)
    n0_a = prof(0.0, asimov)

    def cls(mu):
        q = 0.0 if mh_o > mu else max(2 * (prof(mu, obs) - n0_o), 0.0)
        qa = max(2 * (prof(mu, asimov) - n0_a), 1e-12)
        sq, sqa = math.sqrt(q), math.sqrt(qa)
        if sq <= sqa:
            clsb, clb = norm.sf(sq), norm.cdf(sqa - sq)
        else:
            clsb, clb = norm.sf((q + qa) / (2 * sqa)), norm.sf((q - qa) / (2 * sqa))
        return clsb / clb, 2 * norm.sf(sqa)

    lim = []
    for k in (0, 1):
        f = lambda mu: math.log(max(cls(mu)[k], 1e-300) / 0.05)
        lo, hi = mu_hi * 1e-4, mu_hi
        while f(hi) > 0:
            lo, hi = hi, hi * 3
        while f(lo) < 0:
            lo /= 3
        lim.append(brentq(f, lo, hi, xtol=1e-4 * lo))
    return lim


def atlas_limit(name, M, width=3.0):
    rows, cur = [], None
    for line in (HD / name).read_text().splitlines():
        if line.startswith("#: RELATIVE WIDTH"):
            cur = float(line.split(",")[1])
        elif cur == width and line[:1].isdigit():
            m, v = line.split(",")
            rows.append((float(m), float(v)))
    rows = np.array(rows)
    return float(np.interp(M, rows[:, 0], rows[:, 1]))


def atlas_ratio(M):
    lines = (HD / "Ratio_of_observed_limits_to_SSM_cross_section.csv").read_text().split("\n\n")
    blk = [b for b in lines if "13000" in b and "EE LUMINOSITY [fb$^{-1}$],139" in b][0]
    rows = np.array([[float(x) for x in l.split(",")] for l in blk.splitlines() if l[:1].isdigit() and "-" not in l.split(",")[1:]])
    return float(np.interp(M / 1000.0, rows[:, 0], rows[:, 1]))


def part_d(sel, xs, tag):
    print("(d) the limits with %s" % CARDS[tag])
    chans = {f: Channel(f) for f in ("e", "mu")}
    print("    the published spectra: %d bins (%.0f-%.0f GeV); counts %d (ee), %d (mumu) (events/10 GeV x width/10 GeV, rounded:"
          " |table - integer| <= %.2e relative)" % (
        len(chans["e"].n), chans["e"].lo[0], chans["e"].hi[-1], chans["e"].n.sum(), chans["mu"].n.sum(),
        max((abs(chans[f].nraw - chans[f].n) / np.maximum(chans[f].n, 1)).max() for f in chans)))
    for f, c in chans.items():
        fval, th = c.bkg_fit()
        b = c.bkg(th)
        chi2 = float(np.sum(np.where(c.n > 0, 2 * (b - c.n + c.n * np.log(np.maximum(c.n, 1e-300) / b)), 2 * b)))
        print("    background-only fit, %-2s: b = %.3f, p0..p3 = %s; deviance %.1f for %d bins - 6 parameters" % (
            f, th[1], np.round(th[2:], 4), chi2, len(c.n)))
    ratios = []
    for M in MASSES:
        tmpl, aeff = [], {}
        for f in ("e", "mu"):
            d = sel[(M, f)]
            h, _ = np.histogram(d["mll"], bins=np.append(chans[f].lo, chans[f].hi[-1]))
            # signal counts per bin for sigma x B = 1 fb (per flavour): L x (A x eff) x the fraction in each bin
            tmpl.append(LUMI * h / d["n"])
            aeff[f] = d["aeff"]
        sig_ssm = xs[M][1] / 2 * 1e3   # fb, per flavour (MG5's sigma of e and mu together, halved)
        res = {}
        for label, cs, ts in (("ee", [chans["e"]], [tmpl[0]]), ("mumu", [chans["mu"]], [tmpl[1]]),
                              ("ll", [chans["e"], chans["mu"]], tmpl)):
            obs, exp = cls_limit(cs, ts, mu_hi=1.0)
            res[label] = (obs, exp)
        afid = {f: sel[(M, f)]["afid"] for f in ("e", "mu")}
        print("    M = %4d GeV: sigma x B 95%% CL [fb], observed/expected: ee %.4g/%.4g, mumu %.4g/%.4g, ll %.4g/%.4g;  SSM (own, LO)"
              " %.4g fb" % (M, *res["ee"], *res["mumu"], *res["ll"], sig_ssm))
        print("        fiducial (x own fiducial A): ee obs %.4g, exp %.4g fb (ATLAS, 3%% width: %.4g, %.4g);  mumu obs %.4g, exp %.4g fb"
              " (ATLAS %.4g, %.4g)" % (
                  res["ee"][0] * afid["e"], res["ee"][1] * afid["e"], atlas_limit("Observed_dielectron_cross-section_limits.csv", M),
                  atlas_limit("Expected_dielectron_cross-section_limits.csv", M), res["mumu"][0] * afid["mu"],
                  res["mumu"][1] * afid["mu"], atlas_limit("Observed_dimuon_cross-section_limits.csv", M),
                  atlas_limit("Expected_dimuon_cross-section_limits.csv", M)))
        r = res["ll"][0] / sig_ssm
        ratios.append((M, r, res["ll"][1] / sig_ssm))
        print("        observed limit / SSM: own %.4g;  ATLAS (NNLO SSM cross section) %.4g" % (r, atlas_ratio(M)))
    v = np.array(ratios)
    for k, label in ((1, "observed"), (2, "expected")):
        lr = np.log(v[:, k])
        i = np.where(np.diff(np.sign(lr)) != 0)[0]
        if len(i):
            i = i[0]
            mlim = v[i, 0] + (v[i + 1, 0] - v[i, 0]) * (0 - lr[i]) / (lr[i + 1] - lr[i])
            print("    SSM mass limit (own LO cross section, %s, interpolating log(limit/sigma) between the masses): %.0f GeV" % (
                label, mlim))
    print("    ATLAS: 5100 GeV observed, with the NNLO SSM cross section (a reference)")


def main():
    xs = part_ab()
    for tag in CARDS:
        sel = part_c(tag)
        part_d(sel, xs, tag)


if __name__ == "__main__":
    main()
