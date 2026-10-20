"""Stage 5 of the LHC tools (environment.pdf): SModelS 3.2.1 with a part of its database 3.2.1 (run_stage5.sh).

  (a) the gluino point of stage 4 (m(g~) = 1000 GeV, m(chi0_1) = 825 GeV, g~ -> q q~ chi0_1 with MadWidth's branching ratios,
      sigma = MG5's matched cross section of out/gluino_launch.log): SModelS's r = sigma BR / UL of the T1 map of ATLAS-SUSY-2016-07
      (ATLAS's upper limits) against own r (own linear interpolation of the same map on its Delaunay triangulation, and the
      light-quark part of the branching ratios, which T1 counts), and against MadAnalysis5's r = sigma/sigma95 of stage 4 (the
      best signal region, Spey; the matched sample and the one with the jets from the shower only; the b-quark decays give jets
      too and pass the cuts, so sigma95 compares with the UL of T1 directly);
  (b) a 1Lbb point (m(chi1+-) = m(chi2_0) = 700 GeV, m(chi0_1) = 150 GeV, BR(chi2_0 -> h chi0_1) = BR(chi1+- -> W chi0_1) = 1),
      with sigma = UL/mu_UL of the point from test_pyhf.py (d), the cross section ATLAS assumed: SModelS's r from the upper-limit
      map of ATLAS-SUSY-2019-08 (the HEPData table, so 1/mu_UL of ATLAS) and from the efficiency maps of ATLAS-SUSY-2019-08-eff
      combined with its statistical models (pyhf with BkgOnly.json or with simplified.json; each in a copy of the database with
      only that model), against 1/mu_UL of own pyhf on the HEPData likelihood of the point.  The distributed database lists the
      onnx model (a neural network) first, which needs smodels.statistics.hep_olll, missing from the PyPI sdist of 3.2.1.
The database is the local text database ~/hep/data/smodels-db-3.2.1 (3 results); nothing is downloaded (the proxy variables of
run_stage5.sh block the network).  Run with ~/hep/opt/lhc/bin/python.
"""
import ast
import csv
import glob
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
DB = Path.home() / "hep" / "data" / "smodels-db-3.2.1"
# the gluino partial widths of stage 4 (set_gluino_card.py edits a card when imported, so read its PARTIAL line)
PARTIAL = ast.literal_eval(re.search(r"^PARTIAL = (\{.*\})$", (HERE / "set_gluino_card.py").read_text(), re.M).group(1))

from smodels.base.model import Model  # noqa: E402
from smodels.base.physicsUnits import GeV, fb  # noqa: E402
from smodels.decomposition import decomposer  # noqa: E402
from smodels.experiment.databaseObj import Database  # noqa: E402
from smodels.matching.theoryPrediction import theoryPredictionsFor  # noqa: E402
from smodels.share.models.mssm import BSMList  # noqa: E402
from smodels.share.models.SMparticles import SMList  # noqa: E402

HEAVY = [1000001, 1000002, 1000003, 1000004, 1000005, 1000006, 2000001, 2000002, 2000003, 2000004, 2000005, 2000006,
         1000011, 1000012, 1000013, 1000014, 1000015, 1000016, 2000011, 2000013, 2000015, 1000023, 1000025, 1000035,
         1000024, 1000037, 1000021, 1000039]


def slha(masses, decays, xsecs):
    """a minimal SLHA file: masses, decay tables {pid: [(br, [daughters])]}, 13 TeV cross sections {(pid1, pid2): pb}"""
    lines = ["BLOCK MASS"]
    m = {p: 5000.0 for p in HEAVY}
    m.update({25: 125.0, 35: 5000.0, 36: 5000.0, 37: 5000.0})
    m.update(masses)
    lines += ["   %d  %.6e" % (p, v) for p, v in sorted(m.items())]
    for p in sorted(m):
        if p in decays:
            lines.append("DECAY %d 1.0" % p)
            lines += ["   %.6e   %d   %s" % (br, len(d), "   ".join(str(x) for x in d)) for br, d in decays[p]]
        elif p in (1000022,):
            lines.append("DECAY %d 0.0" % p)
        elif p != 25:
            lines.append("DECAY %d 1.0" % p)
            lines.append("   1.0   2   1000022   %d" % (5 if p < 1000020 or p > 2000000 else 22))
    for (a, b), pb in xsecs.items():
        lines.append("XSECTION  1.30E+04  2212 2212 2 %d %d" % (a, b))
        lines.append("  0  0  0  0  0  0  %.6e  smodels-test" % pb)
    return "\n".join(lines) + "\n"


def predictions(db, text):
    model = Model(BSMparticles=BSMList, SMparticles=SMList)
    model.updateParticles(inputFile=text, promptWidth=1e-11 * GeV, stableWidth=1e-25 * GeV)
    top = decomposer.decompose(model, sigmacut=0.0001 * fb, massCompress=True, invisibleCompress=True, minmassgap=5 * GeV)
    return theoryPredictionsFor(db, top, combinedResults=True, useBestDataset=False)


def own_t1_ul(m1, m2):
    """own linear interpolation of the T1 upper-limit map of ATLAS-SUSY-2016-07 (fb)"""
    txt = (DB / "13TeV" / "ATLAS" / "ATLAS-SUSY-2016-07" / "data" / "T1.txt").read_text()
    pts = re.findall(r"\[\[\[([0-9.E+-]+)\*GeV,([0-9.E+-]+)\*GeV\],\[[^\]]*\]\],([0-9.E+-]+)\*fb\]", txt)
    xy = np.array([[float(a), float(b)] for a, b, _ in pts])
    ul = np.array([float(c) for _, _, c in pts])
    tri = Delaunay(xy)
    s = tri.find_simplex([m1, m2])
    T = tri.transform[s]
    bary = T[:2].dot(np.array([m1, m2]) - T[2])
    w = np.append(bary, 1 - bary.sum())
    return float(w.dot(ul[tri.simplices[s]])), len(pts)


def ma5_best(work):
    f = glob.glob(str(OUT / work / "Output" / "SAF" / "*" / "CLs_output.dat"))
    if not f:
        return None
    for line in Path(f[0]).read_text().splitlines():
        m = re.match(r"\s*atlas_susy_2016_07\s+(\S+)\s+1\s+([0-9.eE+-]+)\s+([0-9.eE+-]+?)(\d\.\d{10})", line)
        if m:
            return m.group(1), float(m.group(3))
    return None


def part_a(db):
    log = (OUT / "gluino_launch.log").read_text()
    sig = float(re.findall(r"Matched cross-section :\s+([0-9.eE+-]+)", log)[-1])
    tot = sum(PARTIAL.values())
    dec = {1000021: [(w / tot, [1000022, q, -q]) for q, w in PARTIAL.items()]}
    text = slha({1000021: 1000.0, 1000022: 825.0}, dec, {(1000021, 1000021): sig})
    preds = [p for p in predictions(db, text) if p.dataset.globalInfo.id == "ATLAS-SUSY-2016-07"]
    light = sum(w for q, w in PARTIAL.items() if q != 5) / tot
    ul_own, n = own_t1_ul(1000.0, 825.0)
    r_own = sig * 1e3 * light ** 2 / ul_own
    print("(a) the gluino point of stage 4: sigma = %.4f pb (MG5, matched), BR(g~ -> q q~ chi0_1, q = u, d, s, c) = %.4f" % (sig, light))
    for p in preds:
        print("    SModelS: %s %s, txnames %s: sigma BR = %.5g fb, UL = %.5g fb, r = %.4f" % (
            p.dataset.globalInfo.id, p.dataType(short=True), [t.txName for t in p.txnames], p.xsection.asNumber(fb),
            p.getUpperLimit().asNumber(fb), p.getRValue()))
    print("    own: the T1 map (%d points) interpolated at (1000, 825) GeV: UL = %.5g fb; sigma BR^2 = %.5g fb; r = %.4f" % (
        n, ul_own, sig * 1e3 * light ** 2, r_own))
    for work, what in (("ma5_gluino", "matched, 0-2 jets"), ("ma5_gluino0", "jets from the shower only")):
        b = ma5_best(work)
        if b:
            lsig = sig
            if work == "ma5_gluino0":
                lsig = float(re.findall(r"set signal.xsection = (\S+)", (OUT / "ma5_gluino0.ma5").read_text())[0])
            print("    MadAnalysis5 (stage 4, %s): best region %s, sigma95 = %.4f pb, r = sigma/sigma95 = %.3f (sigma %.4f pb);"
                  " sigma95/UL(T1) = %.3f" % (what, b[0], b[1], lsig / b[1], lsig, b[1] * 1e3 / ul_own))


def part_b(dbs):
    rows = {(float(r["m1"]), float(r["m2"])): r for r in csv.DictReader(open(OUT / "stage5_1lbb.csv"))}
    ul = {}
    for r in csv.reader((Path.home() / "hep" / "data" / "hepdata-ins1755298" / "Upper_limits_1Lbb.csv").read_text().splitlines()):
        if r and r[0][:1].isdigit():
            ul[(float(r[0]), float(r[1]))] = float(r[2])
    k = (700.0, 150.0)
    mu = float(rows[k]["mu_ul"])
    sig = ul[k] / mu
    dec = {1000023: [(1.0, [1000022, 25])], 1000024: [(1.0, [1000022, 24])]}
    text = slha({1000024: 700.0, 1000023: 700.0, 1000022: 150.0}, dec, {(1000023, 1000024): sig})
    print("(b) the 1Lbb point (700, 150) GeV: sigma = UL/mu_UL = %.5g/%.4f = %.5g pb (own pyhf: mu_UL obs %.4f, 1/mu_UL = %.4f)" % (
        ul[k], mu, sig, mu, 1 / mu))
    for n, (label, d) in enumerate(dbs):
        try:
            preds = predictions(d, text)
        except ModuleNotFoundError as e:
            print("    SModelS, %s: fails, %s (the module is not in the PyPI sdist of SModelS 3.2.1)" % (label, e))
            continue
        for p in preds:
            if not p.dataset.globalInfo.id.startswith("ATLAS-SUSY-2019-08"):
                continue
            if p.dataType(short=True) == "em" or (n > 0 and p.dataType(short=True) == "ul"):
                continue   # the single signal regions; the upper-limit map once
            r_obs = p.getRValue()
            print("    SModelS, %s: %s %s: sigma BR = %.5g fb, r = %.4f, r/(1/mu_UL) - 1 = %+.3f" % (
                label, p.dataset.globalInfo.id, p.dataType(short=True), p.xsection.asNumber(fb), r_obs, r_obs * mu - 1))


def db_copy(tag, model):
    """a copy of the database with one statistical model of ATLAS-SUSY-2019-08-eff: ("pyhf", "BkgOnly.json"),
    ('pyhf', 'simplified.json') or ('onnx', 'combined.onnx'); the distributed one lists onnx first, then the other two"""
    dst = OUT / ("smodels-db-" + tag)
    if not dst.exists():
        shutil.copytree(DB, dst, ignore=shutil.ignore_patterns("*.pcl"))
        g = dst / "13TeV" / "ATLAS" / "ATLAS-SUSY-2019-08-eff" / "globalInfo.txt"
        t = g.read_text()
        t2 = t.replace("statModels: { 'bkgonly': [ ( 'onnx', 'combined.onnx' ),\n                           ( 'pyhf', 'simplified.json'),\n"
                       "                           ( 'full_pyhf', 'BkgOnly.json' ) ]}",
                       "statModels: { 'bkgonly': [ ( '%s', '%s' ) ]}" % model)
        if t2 == t:
            raise SystemExit("statModels line not found in %s" % g)
        g.write_text(t2)
    return Database(str(dst))


def main():
    db = Database(str(DB))
    part_a(db)
    part_b([("pyhf (BkgOnly.json, the full likelihood)", db_copy("fullpyhf", ("pyhf", "BkgOnly.json"))),
            ("pyhf (simplified.json)", db_copy("simplified", ("pyhf", "simplified.json"))),
            ("the database as distributed (onnx first)", db)])


if __name__ == "__main__":
    main()
