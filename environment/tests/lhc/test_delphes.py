"""Stage 3 of the LHC tools (environment.pdf): Delphes 3.5.1 on ROOT 6.32.14, read with uproot (the runs of run_stage3.sh).

  (a) MG5's own Delphes run (detector=Delphes, its default CMS card): the Delphes tree has an entry for every event;
  (b) GenJets: Delphes' GenJetFinder of the CMS card (anti-kT, R = 0.5, pT > 20 GeV, on the stable particles without
      neutrinos) against own FastJet 3.5 (Python) with the same definition on the stable non-neutrino particles of the
      Particle branch, event by event (the jet count, and pT, eta, phi in decreasing pT);
  (c) the tracking efficiency (ElectronTrackingEfficiency: ElePropagated -> EleTracked) and the electron efficiency
      (ElectronEfficiency: EleFiltered -> EleEfficient) in the regions of the card's formulas: the fraction kept against the
      formula, with the binomial error.  Both modules draw per candidate with the formula at its momentum pT and at the eta of
      its POSITION (propagated to the calorimeter; the Track branch's EtaOuter), not of its momentum, unless
      UseMomentumVector is set: binning in the momentum eta puts the curling low-pT electrons, whose position eta is beyond
      2.5, into the wrong regions;
  (d) the momentum smearing (EleTracked -> EleSmeared, matched by the momentum eta and phi, which the smearing keeps): the
      spread of (pT_after/pT_before - 1)/sigma, sigma = min(1, the card's relative resolution) at pT_before and EtaOuter
      (the module draws a log-normal with mean pT and width sigma pT: 1 expected).
Run with ~/hep/opt/lhc/bin/python.
"""
import math
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def mg5_run():
    f = sorted((OUT / "s3_proc" / "Events" / "run_01").glob("*delphes_events.root"))[-1]
    t = uproot.open(f)["Delphes"]
    ne = ak.num(t["Electron.PT"].array())
    print("(a) MG5's Delphes run (%s): %d entries in the tree (expect 10000); electrons per event %.3f, events with two %.3f"
          % (f.name, t.num_entries, ak.mean(ne), ak.mean(ne == 2)))


def genjets(t):
    import fastjet
    p = t.arrays(["Particle.Status", "Particle.PID", "Particle.Px", "Particle.Py", "Particle.Pz", "Particle.E"])
    sel = (p["Particle.Status"] == 1) & (abs(p["Particle.PID"]) != 12) & (abs(p["Particle.PID"]) != 14) & \
          (abs(p["Particle.PID"]) != 16)
    parts = ak.zip({"px": p["Particle.Px"][sel], "py": p["Particle.Py"][sel], "pz": p["Particle.Pz"][sel],
                    "E": p["Particle.E"][sel]})
    jd = fastjet.JetDefinition(fastjet.antikt_algorithm, 0.5)
    jets = fastjet.ClusterSequence(parts, jd).inclusive_jets(min_pt=20.0)
    pt = np.hypot(jets.px, jets.py)
    order = ak.argsort(pt, ascending=False)
    jets, pt = jets[order], pt[order]
    pz, pp = jets.pz, np.sqrt(jets.px**2 + jets.py**2 + jets.pz**2)
    eta = 0.5 * np.log((pp + pz) / (pp - pz))
    phi = np.arctan2(jets.py, jets.px)
    g = t.arrays(["GenJet.PT", "GenJet.Eta", "GenJet.Phi"])
    n_own, n_del = ak.num(pt), ak.num(g["GenJet.PT"])
    same = n_own == n_del
    nmis = int(ak.sum(~same))
    dpt = ak.flatten(abs(pt[same] / g["GenJet.PT"][same] - 1))
    deta = ak.flatten(abs(eta[same] - g["GenJet.Eta"][same]))
    dphi = ak.flatten(abs((phi[same] - g["GenJet.Phi"][same] + np.pi) % (2 * np.pi) - np.pi))
    print("(b) GenJets (anti-kT R = 0.5, pT > 20 GeV): %d jets in %d events (Delphes), %d own;  events with a different count %d;"
          % (ak.sum(n_del), len(n_del), ak.sum(n_own), nmis))
    print("    in the others, max |pT_own/pT_Delphes - 1| = %.1e, max |d eta| = %.1e, max |d phi| = %.1e"
          % (ak.max(dpt), ak.max(deta), ak.max(dphi)))
    if nmis:
        k = np.where(~ak.to_numpy(same))[0][:3]
        for i in k:
            print("    event %d: Delphes %s, own %s" % (i, np.round(ak.to_numpy(g["GenJet.PT"][i]), 3), np.round(ak.to_numpy(pt[i]), 3)))


def region_test(t, name, before, after, regions, etavar="EtaOuter"):
    b = t.arrays([before + ".PT", before + "." + etavar])
    a = t.arrays([after + ".PT", after + "." + etavar])
    pb, eb = ak.to_numpy(ak.flatten(b[before + ".PT"])), np.abs(ak.to_numpy(ak.flatten(b[before + "." + etavar])))
    pa, ea = ak.to_numpy(ak.flatten(a[after + ".PT"])), np.abs(ak.to_numpy(ak.flatten(a[after + "." + etavar])))
    print("(c) %s (%s -> %s), regions in %s: %d -> %d candidates" % (name, before, after, etavar, len(pb), len(pa)))
    chi2 = 0.0
    for label, f, eps in regions:
        nb, na = int(np.sum(f(pb, eb))), int(np.sum(f(pa, ea)))
        if nb == 0:
            print("    %-36s formula %.2f: none" % (label, eps))
            continue
        frac = na / nb
        sig = math.sqrt(max(eps * (1 - eps), 1e-12) / nb)
        pull = (frac - eps) / sig if eps * (1 - eps) > 0 else float("nan")
        if eps * (1 - eps) > 0:
            chi2 += pull**2
        print("    %-36s formula %.2f: kept %d of %d = %.4f +- %.4f (pull %+.2f)" % (label, eps, na, nb, frac, sig, pull))
    return chi2


def smearing(t):
    b = t.arrays(["EleTracked.PT", "EleTracked.Eta", "EleTracked.Phi", "EleTracked.EtaOuter"])
    a = t.arrays(["EleSmeared.PT", "EleSmeared.Eta", "EleSmeared.Phi"])
    rs = {k: [] for k in ("|eta| <= 0.5", "0.5 < |eta| <= 1.5", "1.5 < |eta| <= 2.5")}   # in EtaOuter
    nmatch, nall = 0, 0
    for ev in range(len(b)):
        pb, eb, fb, ob = (ak.to_numpy(b["EleTracked." + x][ev]) for x in ("PT", "Eta", "Phi", "EtaOuter"))
        pa, ea, fa = (ak.to_numpy(a["EleSmeared." + x][ev]) for x in ("PT", "Eta", "Phi"))
        for i in range(len(pb)):
            nall += 1
            j = np.where((np.abs(ea - eb[i]) < 1e-5) & (np.abs(fa - fb[i]) < 1e-5))[0]
            if len(j) != 1 or pb[i] <= 0.1:
                continue
            nmatch += 1
            ae, pt = abs(ob[i]), pb[i]
            if ae <= 0.5:
                key, s = "|eta| <= 0.5", math.sqrt(0.03**2 + pt**2 * 1.3e-3**2)
            elif ae <= 1.5:
                key, s = "0.5 < |eta| <= 1.5", math.sqrt(0.05**2 + pt**2 * 1.7e-3**2)
            elif ae <= 2.5:
                key, s = "1.5 < |eta| <= 2.5", math.sqrt(0.15**2 + pt**2 * 3.1e-3**2)
            else:
                continue
            s = min(s, 1.0)
            rs[key].append((pa[j[0]] / pt - 1) / s)
    print("(d) electron momentum smearing (EleTracked -> EleSmeared): %d of %d matched by eta, phi" % (nmatch, nall))
    for k, v in rs.items():
        v = np.array(v)
        if len(v) > 1:
            print("    %-20s %5d electrons: mean %+.3f +- %.3f, spread %.3f +- %.3f (expect 0, 1)"
                  % (k, len(v), v.mean(), v.std() / math.sqrt(len(v)), v.std(), v.std() / math.sqrt(2 * len(v))))


def main():
    mg5_run()
    t = uproot.open(OUT / "delphes_checks.root")["Delphes"]
    genjets(t)
    trk = [("|eta| <= 1.5, 0.1 < pT <= 1", lambda p, e: (e <= 1.5) & (p > 0.1) & (p <= 1.0), 0.73),
           ("|eta| <= 1.5, 1 < pT <= 100", lambda p, e: (e <= 1.5) & (p > 1.0) & (p <= 100.0), 0.95),
           ("|eta| <= 1.5, pT > 100", lambda p, e: (e <= 1.5) & (p > 100.0), 0.99),
           ("1.5 < |eta| <= 2.5, 0.1 < pT <= 1", lambda p, e: (e > 1.5) & (e <= 2.5) & (p > 0.1) & (p <= 1.0), 0.50),
           ("1.5 < |eta| <= 2.5, 1 < pT <= 100", lambda p, e: (e > 1.5) & (e <= 2.5) & (p > 1.0) & (p <= 100.0), 0.83),
           ("1.5 < |eta| <= 2.5, pT > 100", lambda p, e: (e > 1.5) & (e <= 2.5) & (p > 100.0), 0.90),
           ("|eta| > 2.5 or pT <= 0.1", lambda p, e: (e > 2.5) | (p <= 0.1), 0.0)]
    region_test(t, "tracking efficiency", "ElePropagated", "EleTracked", trk, etavar="Eta")   # the wrong variable, for the record
    c1 = region_test(t, "tracking efficiency", "ElePropagated", "EleTracked", trk)
    ele = [("pT <= 10", lambda p, e: p <= 10.0, 0.0),
           ("|eta| <= 1.5, pT > 10", lambda p, e: (e <= 1.5) & (p > 10.0), 0.95),
           ("1.5 < |eta| <= 2.5, pT > 10", lambda p, e: (e > 1.5) & (e <= 2.5) & (p > 10.0), 0.85),
           ("|eta| > 2.5, pT > 10", lambda p, e: (e > 2.5) & (p > 10.0), 0.0)]
    c2 = region_test(t, "electron efficiency", "EleFiltered", "EleEfficient", ele)
    print("    chi^2 of the pulls: tracking %.2f (6 regions), electron %.2f (2 regions)" % (c1, c2))
    smearing(t)


if __name__ == "__main__":
    main()
