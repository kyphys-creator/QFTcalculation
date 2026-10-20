"""Stage 5 of the LHC tools (environment.pdf): pyhf 0.7.6 against own formulas and the ATLAS 1Lbb likelihood (run_stage5.sh).

  (a) one-bin counting model, n = 59, b = 65 +- 7 (Meff-5j-2000 of ATLAS-SUSY-2016-07, MadAnalysis5's numbers), with the
      signal of stage 4 (out/ma5_gluino: efficiency x cross section x 36.1 fb^-1): CLs at mu = 0.3 and the 95% CL upper limits on
      mu, observed and median expected, from pyhf (uncorrelated_background: Poisson-constrained background, the qtilde test
      statistic, asymptotic) against own code (the same likelihood profiled analytically, the asymptotic formulas of Cowan et
      al.), and own code with a Gaussian constraint and Spey's Asimov data (the auxiliary data at the nominal value) against
      MadAnalysis5's limit (Spey, default.uncorrelated_background) on the same region; the two conventions differ by 4 to 13%;
  (b) the ATLAS 1Lbb search (ATLAS-SUSY-2019-08, HEPData ins1755298): the background-only fit to the control regions, then
      the background in the 9 bins of the three signal regions, against the post-fit backgrounds of HEPData (a reference);
  (c) CLs at mu = 1 for the 125 signal points of the patchset, observed and median expected, interpolated (log CLs, linear on
      the triangulation of the grid) to the points of the published exclusion contours (a reference: CLs = 0.05 there);
  (d) the observed upper limit mu_UL at each point (own secant iteration on log CLs(mu) with pyhf's hypotest), and
      UL(HEPData)/mu_UL, which is the signal cross section of the point and has to depend on m(chi1+-/chi2_0) only.
Run with ~/hep/opt/lhc/bin/python (OMP_NUM_THREADS=1: 14 processes).  The results of (c) and (d) are kept in
out/stage5_1lbb.csv; --reuse reads them instead of computing them again.
"""
import csv
import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pyhf
from scipy.optimize import brentq
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HD = Path.home() / "hep" / "data" / "hepdata-ins1755298"
SR = ["SRLMEM_mct2", "SRMMEM_mct2", "SRHMEM_mct2"]


# ---------------------------------------------------------------- (a) one bin
class OneBin:
    """-ln L of a counting experiment with an auxiliary measurement of the background, profiled analytically.
    poisson: Pois(n | mu s + g b) Pois(aux | g tau), tau = (b/db)^2, aux = tau observed (pyhf's uncorrelated_background,
             shapesys);  gauss: Pois(n | mu s + b + t db) N(t | aux, 1), aux = 0 observed."""

    def __init__(self, s, b, db, kind):
        self.s, self.b, self.db, self.kind = s, b, db, kind
        self.tau = (b / db) ** 2

    def nuis(self, mu, n, aux):
        s, b, db, tau = self.s, self.b, self.db, self.tau
        if self.kind == "poisson":
            # n b/(mu s + g b) - b + aux/g - tau = 0:  (b + tau) b g^2 + ((b + tau) mu s - n b - aux b) g - aux mu s = 0
            A, B, C = (b + tau) * b, (b + tau) * mu * s - n * b - aux * b, -aux * mu * s
            return (n + aux) / (b + tau) if mu == 0 else (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
        # n db/lam - db - (t - aux) = 0, lam = mu s + b + t db:  db t^2 + (db^2 + A - aux db) t + db (A - n) - aux A = 0
        A = mu * s + b
        a2, a1, a0 = db, db * db + A - aux * db, db * (A - n) - aux * A
        return (-a1 + math.sqrt(a1 * a1 - 4 * a2 * a0)) / (2 * a2)

    def nll(self, mu, n, aux):
        x = self.nuis(mu, n, aux)
        if self.kind == "poisson":
            lam = mu * self.s + x * self.b
            return -(n * math.log(lam) - lam) - (aux * math.log(x * self.tau) - x * self.tau)
        lam = mu * self.s + self.b + x * self.db
        return -(n * math.log(lam) - lam) + 0.5 * (x - aux) ** 2

    def muhat(self, n, aux):
        """the unconditional maximum: the main and the auxiliary measurement fitted exactly"""
        if self.kind == "poisson":
            return (n - aux / self.tau * self.b) / self.s
        return (n - self.b - aux * self.db) / self.s

    def qtilde(self, mu, n, aux):
        mh = max(self.muhat(n, aux), 0.0)
        return 0.0 if mh > mu else max(2 * (self.nll(mu, n, aux) - self.nll(mh, n, aux)), 0.0)

    def cls(self, mu, n, asimov="pyhf"):
        """CLs observed and median expected (qtilde, asymptotic: Cowan, Cranmer, Gross, Vitells, EPJC 71 (2011) 1554), with
        the Asimov data of the background-only fit to the observed data: pyhf's (the main and the auxiliary data at the fitted
        nuisance parameter), Spey's 'aposteriori' (the main data there, the auxiliary data kept at the nominal value), or
        'apriori' (the nominal background)"""
        aux = self.tau if self.kind == "poisson" else 0.0
        x0 = self.nuis(0.0, n, aux)
        na, auxa = (x0 * self.b, x0 * self.tau) if self.kind == "poisson" else (self.b + x0 * self.db, x0)
        if asimov == "spey":
            auxa = aux
        elif asimov == "apriori":
            na, auxa = self.b, aux
        q, qa = self.qtilde(mu, n, aux), self.qtilde(mu, na, auxa)
        sq, sqa = math.sqrt(q), math.sqrt(qa)
        if sq <= sqa:
            clsb, clb = norm.sf(sq), norm.cdf(sqa - sq)
        else:
            clsb, clb = norm.sf((q + qa) / (2 * sqa)), norm.sf((q - qa) / (2 * sqa))
        return clsb / clb, 2 * norm.sf(sqa)

    def limit(self, n, asimov="pyhf"):
        return tuple(brentq(lambda m: math.log(max(self.cls(m, n, asimov)[k], 1e-300) / 0.05), 1e-3, 5, xtol=1e-7)
                     for k in (0, 1))


def ma5_region(sr="5j_Meff_2000"):
    """efficiency and MadAnalysis5's limits (Spey) of a signal region of the stage-4 run, and its cross section"""
    import glob
    import re
    f = glob.glob(str(OUT / "ma5_gluino" / "Output" / "SAF" / "*" / "CLs_output.dat"))[0]
    for line in Path(f).read_text().splitlines():
        m = re.match(r"\s*atlas_susy_2016_07\s+(\S+)\s+(\d)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+?)(\d\.\d{10})\s+\|\|\s+(\S+)", line)
        if m and m.group(1) == sr:
            sig = float(re.findall(r"set signal.xsection = (\S+)", (OUT / "ma5_gluino.ma5").read_text())[0])
            return float(m.group(6)), float(m.group(3)), float(m.group(4)), float(m.group(5)), sig
    raise SystemExit("no %s in %s" % (sr, f))


def part_a():
    n, b, db = 59.0, 65.0, 7.0
    eff, exp_ma5, obs_ma5, cls_ma5, sig = ma5_region()
    s = eff * sig * 36.1e3
    model = pyhf.simplemodels.uncorrelated_background(signal=[s], bkg=[b], bkg_uncertainty=[db])
    data = [n] + model.config.auxdata
    cls_obs, cls_exp = pyhf.infer.hypotest(0.3, data, model, test_stat="qtilde", return_expected=True)
    own_p, own_g = OneBin(s, b, db, "poisson"), OneBin(s, b, db, "gauss")
    own_obs, own_exp = own_p.cls(0.3, n)
    print("(a) one bin: n = 59, b = 65 +- 7, s = %.3f (efficiency %.5f x %.4f pb x 36.1 fb^-1)" % (s, eff, sig))
    print("    CLs at mu = 0.3: pyhf obs %.6f exp %.6f;  own (Poisson constraint) obs %.6f exp %.6f;  rel. diff %.1e, %.1e" % (
        float(cls_obs), float(cls_exp), own_obs, own_exp, own_obs / float(cls_obs) - 1, own_exp / float(cls_exp) - 1))
    p_obs, p_exp = pyhf.infer.intervals.upper_limits.toms748_scan(data, model, 0.01, 5.0, rtol=1e-7)
    p_obs, p_exp = float(p_obs), float(p_exp[2])
    o_obs, o_exp = own_p.limit(n)
    print("    mu_UL: pyhf obs %.6f exp %.6f;  own (Poisson) obs %.6f exp %.6f;  rel. diff %.1e, %.1e" % (
        p_obs, p_exp, o_obs, o_exp, o_obs / p_obs - 1, o_exp / p_exp - 1))
    g_obs, g_exp = own_g.limit(n, "spey")
    print("    MadAnalysis5 (Spey: Gaussian constraint, Asimov data with the auxiliary data at the nominal value): sigma95 obs %.6f"
          " exp %.6f pb;  own, the same likelihood and Asimov data: %.6f, %.6f;  rel. diff %.1e, %.1e" % (
              obs_ma5, exp_ma5, g_obs * sig, g_exp * sig, g_obs * sig / obs_ma5 - 1, g_exp * sig / exp_ma5 - 1))
    for label, kind, asi in (("Gaussian, pyhf's Asimov data", "gauss", "pyhf"), ("Gaussian, a priori Asimov data", "gauss", "apriori"),
                             ("Poisson (pyhf)", "poisson", "pyhf")):
        a, e = OneBin(s, b, db, kind).limit(n, asi)
        print("    own, %-30s sigma95 obs %.5f exp %.5f pb (%+.3f, %+.3f against MadAnalysis5)" % (
            label + ":", a * sig, e * sig, a * sig / obs_ma5 - 1, e * sig / exp_ma5 - 1))


# ---------------------------------------------------------------- (b) background-only fit
def part_b():
    spec = json.load(open(HD / "BkgOnly.json"))
    ws = pyhf.Workspace(spec)
    full = ws.model(poi_name=None)
    cr = ws.prune(channels=SR)
    mcr = cr.model(poi_name=None)
    fit = pyhf.infer.mle.fit(cr.data(mcr), mcr)
    pars = full.config.suggested_init()
    names = {}
    for name in mcr.config.par_order:
        sl = mcr.config.par_slice(name)
        names[name] = fit[sl]
    for name in full.config.par_order:
        if name in names:
            pars[full.config.par_slice(name)] = list(names[name])
    pars = np.asarray(pars)
    yields = full.expected_actualdata(pars)
    chans = {}
    for c in full.config.channels:
        chans[c] = yields[full.config.channel_slices[c]]
    # the CR + SR fit, for comparison
    fit2 = pyhf.infer.mle.fit(ws.data(full), full)
    y2 = full.expected_actualdata(fit2)
    ref = {}
    for sr, tab in (("SRLMEM_mct2", "dataMC_SRLM_mct.csv"), ("SRMMEM_mct2", "dataMC_SRMM_mct.csv"), ("SRHMEM_mct2", "dataMC_SRHM_mct.csv")):
        blocks = (HD / tab).read_text().split("\n\n")
        bkg = [b for b in blocks if "otimes$ stat" in b][0]   # 'Expected background' ('Bakground' in two of the tables)
        rows = [r for r in csv.reader(bkg.splitlines()) if r and r[0][0].isdigit()]
        ref[sr] = [(float(r[3]), float(r[4])) for r in rows]
    print("(b) 1Lbb background in the signal regions: HEPData's post-fit (a reference) against pyhf's fit of the CRs only, and of"
          " CRs + SRs")
    pulls = []
    for sr in SR:
        for i, (v, e) in enumerate(ref[sr]):
            a, c = float(chans[sr][i]), float(y2[full.config.channel_slices[sr]][i])
            pulls.append((a - v) / e)
            print("    %-12s bin %d: HEPData %7.3f +- %6.3f;  CR fit %7.3f (%+6.3f sigma);  CR + SR fit %7.3f" % (sr, i + 1, v, e, a, (a - v) / e, c))
    print("    CR fit: max |pull| %.3f over the 9 bins" % max(abs(p) for p in pulls))


# ---------------------------------------------------------------- (c), (d) the signal grid
_BKG, _PS = None, None


def _init():
    global _BKG, _PS
    _BKG = json.load(open(HD / "BkgOnly.json"))
    _PS = pyhf.PatchSet(json.load(open(HD / "patchset.json")))


def _cls(mu, model, data):
    """CLs observed and median expected at mu; the signal strength bounded by [0, 100] (the workspace's [0, 5] is too narrow
    for the weakest points, whose mu_UL is above 5)"""
    bounds = model.config.suggested_bounds()
    bounds[model.config.poi_index] = (0.0, 100.0)
    o, e = pyhf.infer.hypotest(mu, data, model, test_stat="qtilde", return_expected=True, par_bounds=bounds)
    return float(o), float(e)


def point(name):
    ws = pyhf.Workspace(_PS[name].apply(_BKG))
    model = ws.model()
    data = ws.data(model)
    o1, e1 = _cls(1.0, model, data)
    # mu_UL: secant on log(CLs_obs/0.05), starting at mu = 1 and a second point guessed from the slope of CLs near mu = 1
    x0, f0 = 1.0, math.log(o1 / 0.05)
    x1 = x0 * (0.7 if f0 < 0 else 1.4)
    f1 = math.log(_cls(x1, model, data)[0] / 0.05)
    n = 2
    while abs(f1) > 1e-3 and n < 12:
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x2 = min(max(x2, 0.2 * x1), 5 * x1, 99.0)
        x0, f0, x1 = x1, f1, x2
        f1 = math.log(_cls(x1, model, data)[0] / 0.05)
        n += 1
    return name, o1, e1, x1, f1, n


def grid(reuse):
    out = OUT / "stage5_1lbb.csv"
    if reuse and out.exists():
        return [dict(r) for r in csv.DictReader(open(out))]
    ps = pyhf.PatchSet(json.load(open(HD / "patchset.json")))
    names = [p.name for p in ps.patches]
    rows = []
    with ProcessPoolExecutor(max_workers=os.cpu_count(), initializer=_init) as ex:
        for name, o1, e1, mu, f, n in ex.map(point, names):
            m1, m2 = (float(x) for x in name.split("_")[-2:])
            rows.append({"m1": m1, "m2": m2, "cls_obs": o1, "cls_exp": e1, "mu_ul": mu, "resid": f, "evals": n})
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def read_table(name):
    rows = [r for r in csv.reader((HD / name).read_text().splitlines()) if r and r[0][:1].isdigit()]
    return np.array([[float(x) for x in r[:3]] if len(r) >= 3 and r[2] else [float(r[0]), float(r[1])] for r in rows], dtype=object)


def part_cd(rows):
    from scipy.interpolate import griddata
    m = np.array([[float(r["m1"]), float(r["m2"])] for r in rows])
    lo = np.log10([float(r["cls_obs"]) for r in rows])
    le = np.log10([float(r["cls_exp"]) for r in rows])
    print("(c) CLs at mu = 1 on %d signal points (pyhf); interpolated to the published contours (CLs = 0.05 there):" % len(rows))
    for label, f, vals in (("observed", "Observed_limit_1lbb.csv", lo), ("expected", "Expected_limit_1lbb.csv", le)):
        pts = np.array([[float(x) for x in r[:2]] for r in csv.reader((HD / f).read_text().splitlines()) if r and r[0][:1].isdigit()])
        c = griddata(m, vals, pts, method="linear")
        ok = ~np.isnan(c)
        cl = 10 ** c[ok]
        print("    %s: %d of %d contour points inside the grid; CLs there: median %.4f, 16-84%% %.4f-%.4f, min %.4f, max %.4f" % (
            label, ok.sum(), len(pts), np.median(cl), np.percentile(cl, 16), np.percentile(cl, 84), cl.min(), cl.max()))
    ul = {}
    for r in csv.reader((HD / "Upper_limits_1Lbb.csv").read_text().splitlines()):
        if r and r[0][:1].isdigit():
            ul[(float(r[0]), float(r[1]))] = float(r[2])
    by = {}
    bad = [r for r in rows if abs(float(r["resid"])) > 1e-3]
    for r in rows:
        k = (float(r["m1"]), float(r["m2"]))
        if k in ul:
            by.setdefault(k[0], []).append(ul[k] / float(r["mu_ul"]))
    print("(d) mu_UL (own secant on pyhf's CLs, |log(CLs/0.05)| < 1e-3: %d of %d points); UL(HEPData)/mu_UL = the signal cross"
          " section, by m(chi1+-/chi2_0) (spread over m(chi1_0)):" % (len(rows) - len(bad), len(rows)))
    spreads = []
    for m1 in sorted(by):
        v = np.array(by[m1])
        if len(v) > 1:
            spreads.append(v.std() / v.mean())
        print("    m = %6.0f GeV: %2d points, sigma = %.5g pb, rms/mean %.3f, max/min - 1 %.3f" % (
            m1, len(v), v.mean(), v.std() / v.mean() if len(v) > 1 else 0, v.max() / v.min() - 1))
    print("    median rms/mean over the masses with several points: %.3f" % np.median(spreads))


def main():
    reuse = "--reuse" in sys.argv
    part_a()
    part_b()
    rows = grid(reuse)
    part_cd(rows)


if __name__ == "__main__":
    main()
