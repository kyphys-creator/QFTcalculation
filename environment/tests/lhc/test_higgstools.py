"""Stage 5 of the LHC tools (environment.pdf): HiggsTools 1.3 (HiggsPredictions, HiggsSignals) with HSDataSet v1.1 (run_stage5.sh).

  (a) HiggsSignals' chi^2 of the SM Higgs boson at M_H = 125.2 GeV (the mass of the Higgs note), with HiggsPredictions' own SM
      (effective couplings 1: the cross sections and the branching ratios of its SM tables);
  (b) the input path: the same SM with every partial width set again by hand (setDecayWidth) to HiggsPredictions' own SM values
      (not the combined mode inv) gives the same chi^2;
  (c) the partial widths of the Higgs note (models/sm_higgs/Src/results/total_width.csv: NLO QCD and electroweak corrections,
      Gamma = 3.890 MeV) in place of HiggsPredictions' (the production unchanged): the branching ratios side by side, and the
      chi^2 and Delta chi^2 against (a).
Run with ~/hep/opt/lhc/bin/python; the Higgs module is in the virtual environment (built from ~/hep/HiggsTools-1.3).
"""
import csv
from pathlib import Path

import Higgs.predictions as HP
import Higgs.signals as HS

HERE = Path(__file__).resolve().parent
NOTE = HERE.parents[2] / "models" / "sm_higgs" / "Src" / "results" / "total_width.csv"
HSDATA = Path.home() / "hep" / "data" / "hsdataset-v1.1"
MH = 125.2
CH = {"bb": "bb", "WW": "WW", "gg": "gg", "tautau": "tautau", "cc": "cc", "ZZ": "ZZ", "gamgam": "gamgam", "Zgam": "Zgam",
      "mumu": "mumu", "ss": "ss"}


def sm():
    pred = HP.Predictions()
    h = pred.addParticle(HP.NeutralScalar("h", "even"))
    h.setMass(MH)
    HP.effectiveCouplingInput(h, HP.smLikeEffCouplings)
    return pred, h


def main():
    signals = HS.Signals(str(HSDATA))
    pred, h = sm()
    chi0 = signals(pred)
    print("(a) HiggsSignals (HSDataSet v1.1, %d observables): chi^2 of HiggsPredictions' SM at M_H = %.1f GeV = %.4f;"
          " Gamma_H = %.6e GeV" % (signals.observableCount(), MH, chi0, h.totalWidth()))
    pred2, h2 = sm()
    for d in HP.Decay.__members__.values():
        # inv is the combined mode directInv + ZZ -> 4 nu; setting it would count ZZ -> 4 nu twice (as directInv)
        if d not in (HP.Decay.none, HP.Decay.inv):
            w = h.br(d) * h.totalWidth()
            if w > 0:
                h2.setDecayWidth(d, w)
    chi1 = signals(pred2)
    print("(b) the same widths set again by hand: chi^2 = %.4f (difference %.1e), Gamma_H = %.6e GeV" % (chi1, chi1 - chi0, h2.totalWidth()))
    rows = {r["channel"]: r for r in csv.DictReader(open(NOTE))}
    pred3, h3 = sm()
    small = float(rows["dd + uu + ee"]["gamma_GeV"])
    for k, d in CH.items():
        h3.setDecayWidth(getattr(HP.Decay, d), float(rows[k]["gamma_GeV"]))
    for d in ("uu", "dd", "ee"):
        h3.setDecayWidth(getattr(HP.Decay, d), small / 3)
    chi2 = signals(pred3)
    print("(c) the Higgs note's partial widths (total %.6e GeV in the note; %.6e GeV in HiggsPredictions after setting them):" % (
        float(rows["total"]["gamma_GeV"]), h3.totalWidth()))
    print("    %-8s %10s %10s %10s" % ("channel", "note", "HiggsTools", "note/HT-1"))
    for k, d in CH.items():
        a, b = h3.br(getattr(HP.Decay, d)), h.br(getattr(HP.Decay, d))
        print("    %-8s %10.5f %10.5f %+10.3f" % (k, a, b, a / b - 1))
    print("    chi^2 = %.4f, Delta chi^2 against HiggsPredictions' SM = %+.4f" % (chi2, chi2 - chi0))


if __name__ == "__main__":
    main()
