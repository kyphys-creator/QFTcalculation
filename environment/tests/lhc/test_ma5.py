"""Stage 4 of the LHC tools (environment.pdf): MadAnalysis5 1.11.0, PADForSFS, ATLAS-SUSY-2016-07 (the runs of run_stage4.sh).

The cutflows of MadAnalysis5's SFS run on our 1 TeV gluino sample (m(chi0_1) = 825 GeV) in the three signal regions of
Table 9 of Araz, Fuks, Polykratis (arXiv:2006.09387), normalized to the 7262.2 initial events of the table (36.1 fb^-1),
against the table's SFS and PAD (Delphes) columns, which are references: the number after each cut, the cut efficiency
n_i/n_{i-1}, and the Monte Carlo error of ours (binomial, from the raw counts).  Our cross section (MG5, LO matched) against the
one the table implies, 7262.2/36.1 fb^-1 = 0.2012 pb (a reference too).  Before that, the widths of the run: the squark widths
of the param_card (MadWidth, two-body: about 200 GeV; the model's card has 0.29 to 7.4 GeV, which weights the on-shell squark
of q g -> q~ g~ -> q g~ g~ by up to 715), the gluino width against MadSpin's own partial width (which MadSpin prints when it
exceeds the card's total), and the fraction of the decayed LHE events with a parton not from a gluino decay of pT > 1.5 TeV
(the Jacobian peak of q~ -> q g~ at 2.1 TeV: at least 0.054 with the model's squark widths).  Last, MadAnalysis5's own
95% CL limits and 1-CLs (Spey) of the best and the three signal regions, as information; and, after run_stage4.sh
--controls, the samples with fewer jets from the matrix elements (none: the jets from Pythia's shower; 0, 1 jet with MLM)
and with twice the matching scales.
"""
import glob
import gzip
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LUMI = 36.1e3      # pb^-1
PAPER = {          # Table 9 of arXiv:2006.09387: (cut, PAD, SFS)
    "3j_Meff_1300": [("Initial", 7262.2, 7262.2), ("Preselection", 1129.8, 1092.0), ("At least 2 jets", 1125.0, 1087.5),
                     ("At least 3 jets", 1073.0, 1032.9), ("dphi(jk, MET) > 0.4", 848.5, 821.6),
                     ("dphi(j3, MET) > 0.2", 767.6, 743.9), ("pT(j1) > 700", 53.9, 54.8), ("pT(j2) > 50", 53.9, 54.8),
                     ("pT(j3) > 50", 53.9, 54.8), ("MET/sqrt(HT) > 16", 43.0, 44.4), ("Meff(3) > 1300", 43.0, 44.4)],
    "4j_Meff_1400": [("Initial", 7262.2, 7262.2), ("Preselection", 1129.8, 1092.0), ("At least 2 jets", 1125.0, 1087.5),
                     ("At least 4 jets", 857.4, 821.2), ("dphi(jk, MET) > 0.4", 677.1, 652.3),
                     ("dphi(jl, MET) > 0.4", 522.0, 500.8), ("pT(j4) > 100", 113.5, 112.5), ("|eta(j)| < 2", 91.1, 89.0),
                     ("Aplanarity > 0.04", 54.5, 52.9), ("MET/Meff(4) > 0.25", 49.2, 48.2), ("Meff(4) > 1400", 27.0, 27.5)],
    "6j_Meff_1200": [("Initial", 7262.2, 7262.2), ("Preselection", 1129.8, 1092.0), ("At least 2 jets", 1125.0, 1087.5),
                     ("At least 6 jets", 244.2, 225.2), ("dphi(jk, MET) > 0.4", 194.0, 179.5),
                     ("dphi(jl, MET) > 0.2", 154.9, 143.3), ("|eta(j)| < 2", 101.4, 93.0), ("MET/Meff(6) > 0.25", 85.9, 78.2),
                     ("Meff(6) > 1200", 67.6, 61.6)],
}


def read_saf(path):
    """the counters of an MA5 cutflow file: [(name, raw entries, sum of weights)]"""
    txt = Path(path).read_text()
    out = []
    for block in re.findall(r"<(?:InitialCounter|Counter)>(.*?)</(?:InitialCounter|Counter)>", txt, re.S):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        name = re.findall(r'"([^"]*)"', lines[0])[0]
        n = [float(x) for x in lines[1].split("#")[0].split()]
        w = [float(x) for x in lines[2].split("#")[0].split()]
        out.append((name, n[0] - n[1], w[0] - w[1]))
    return out


def widths(log):
    card = (OUT / "gluino_proc" / "Cards" / "param_card.dat").read_text()
    w = {int(a): float(b) for a, b in re.findall(r"^DECAY\s+(\d+)\s+([-+0-9.eE]+)", card, re.M)}
    sq = [w[p] for p in (1000001, 1000002, 1000003, 1000004, 1000005, 1000006, 2000001, 2000002, 2000003, 2000004, 2000005,
                         2000006)]
    ms = re.findall(r"partial width \(([0-9.eE+-]+)\) larger than total width \(([0-9.eE+-]+)\)[^\n]*1000021", log)
    print("(a) widths: squarks %.1f to %.1f GeV (12, MadWidth two-body);  gluino %.5e GeV;  MadSpin: %s" % (
        min(sq), max(sq), w[1000021], "partial width %s > total %s" % ms[-1] if ms else "no partial width above the total"))
    lhe = glob.glob(str(OUT / "gluino_proc" / "Events" / "run_01_decayed_1" / "unweighted_events.lhe.gz"))[0]
    n = nhard = 0
    with gzip.open(lhe, "rt") as f:
        ev = None
        for line in f:
            if line.startswith("<event"):
                ev = []
            elif line.startswith("</event"):
                n += 1
                nhard += any(st == 1 and abs(pid) in (1, 2, 3, 4, 5, 21) and (m < 1 or abs(ev[m - 1][0]) != 1000021)
                             and math.hypot(px, py) > 1500 for pid, st, m, px, py in ev)
                ev = None
            elif ev is not None and not line.startswith(("<", "#")):
                x = line.split()
                if len(x) == 13:
                    ev.append((int(x[0]), int(x[1]), int(x[2]), float(x[6]), float(x[7])))
    print("    decayed LHE: %d of %d events (%.4f) with a parton not from a gluino decay of pT > 1.5 TeV" % (nhard, n, nhard / n))


def cutflows(work):
    """{signal region: [(name, raw entries, sum of weights)]} of an MA5 work directory"""
    out = {}
    for sr in PAPER:
        files = glob.glob(str(work / "Output" / "SAF" / "*" / "atlas_susy_2016_07*" / "Cutflows" / ("%s.saf" % sr)))
        if files:
            out[sr] = read_saf(files[0])
    return out


def controls():
    """the samples of --controls against the paper's SFS column: preselection, pT(j1) > 700 GeV (3j), N jets (4j, 6j), final"""
    for tag, what in (("gluino0", "p p > go go, jets from the shower"), ("gluino1", "+ 0, 1 jet, MLM"),
                      ("gluino2x", "+ 0, 1, 2 jets, MLM with xqcut 250 GeV, qCut 375 GeV")):
        cf = cutflows(OUT / ("ma5_" + tag))
        if len(cf) < 3:
            continue
        log = (OUT / ("%s_launch.log" % tag)).read_text(errors="replace")
        sig = (re.findall(r"Matched cross-section :\s+([0-9.eE+-]+)", log) or re.findall(r"Cross-section :\s+([0-9.eE+-]+)", log))[-1]
        print("(e) %s (%s; %s pb): efficiencies ours (SFS) and the final numbers normalized to 7262.2:" % (tag, what, sig))
        parts = []
        for sr, c in cf.items():
            ref = PAPER[sr]
            n0 = c[0][1]
            eff = [c[i][2] / c[i - 1][2] for i in range(1, len(c))]
            pick = {"3j_Meff_1300": (1, 6), "4j_Meff_1400": (3, 6), "6j_Meff_1200": (3,)}[sr]
            effs = ", ".join("%s %.3f (%.3f)" % (ref[i][0], eff[i - 1], ref[i][2] / ref[i - 1][2]) for i in pick)
            last = 7262.2 * c[-1][2] / c[0][2]
            err = last * math.sqrt(max(1 - c[-1][1] / n0, 0) / max(c[-1][1], 1))
            print("    %s: %s;  final %.1f +- %.1f (SFS %.1f, PAD %.1f; ours/SFS %.2f)" % (sr, effs, last, err, ref[-1][2],
                                                                                         ref[-1][1], last / ref[-1][2]))


def main():
    work = OUT / "ma5_gluino"
    log = (OUT / "gluino_launch.log").read_text()
    widths(log)
    sig, err = (float(x) for x in re.findall(r"Matched cross-section :\s+([0-9.eE+-]+)\s+\+-\s+([0-9.eE+-]+)", log)[-1])
    print("(b) the 1 TeV gluino sample: MG5 matched cross section %.4f +- %.4f pb, x 36.1 fb^-1 = %.1f events;  the paper's "
          "table implies %.4f pb (7262.2 events; a reference)" % (sig, err, sig * LUMI, 7262.2 / LUMI))
    for sr, ref in PAPER.items():
        files = glob.glob(str(work / "Output" / "SAF" / "*" / "atlas_susy_2016_07*" / "Cutflows" / ("%s.saf" % sr)))
        if not files:
            print("  %s: no cutflow file" % sr)
            continue
        cf = read_saf(files[0])
        n0, w0 = cf[0][1], cf[0][2]
        print("(c) %s: %d cuts in MA5 (%d in the paper's table); ours normalized to 7262.2 initial events" % (sr, len(cf), len(ref)))
        print("    %-34s %9s %7s %8s | %-22s %8s %8s %7s %7s" % ("MA5 cut", "ours", "eff", "MC err", "paper's cut", "PAD",
                                                               "SFS", "eff SFS", "1-e/eS"))
        prev, prevref = None, None
        for i, (name, n, w) in enumerate(cf):
            v = 7262.2 * w / w0
            eff = (w / prev) if prev else float("nan")
            mcerr = v * math.sqrt(max(1 - n / n0, 0) / max(n, 1))
            line = "    %-34s %9.1f %7.3f %8.1f" % (name[:34], v, eff, mcerr)
            if i < len(ref):
                rn, pad, sfs = ref[i]
                es = sfs / prevref if prevref else float("nan")
                line += " | %-22s %8.1f %8.1f %7.3f %+7.3f" % (rn, pad, sfs, es, 1 - eff / es if prevref else float("nan"))
                prevref = sfs
            print(line)
            prev = w
        last = 7262.2 * cf[-1][2] / w0
        print("    final: ours %.1f +- %.1f (MC);  paper SFS %.1f, PAD %.1f;  ours/SFS = %.3f" % (
            last, last * math.sqrt(max(1 - cf[-1][1] / n0, 0) / max(cf[-1][1], 1)), ref[-1][2], ref[-1][1], last / ref[-1][2]))
    cls = glob.glob(str(work / "Output" / "SAF" / "*" / "CLs_output.dat"))
    if cls:
        rows = []
        for line in Path(cls[0]).read_text().splitlines():
            m = re.match(r"\s*atlas_susy_2016_07\s+(\S+)\s+(\d)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+?)(\d\.\d{10})\s+\|\|\s+(\S+)", line)
            if m:
                rows.append((m.group(1), int(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)), float(m.group(6))))
        for sr, best, exp, obs, cl, eff in rows:
            if best or sr in PAPER:
                print("(d) MadAnalysis5's limit (Spey, its own output, not checked here): %-13s %s sigma95 exp %.3f pb, obs %.3f pb, "
                      "1-CLs %.3f at %.4g pb, efficiency %.5f" % (sr, "(best)" if best else "      ", exp, obs, cl, sig, eff))


if __name__ == "__main__":
    main()
    controls()
