#!/usr/bin/env python3
"""Step (2) of the abelian Higgs note: compare MadGraph (work/, from tree_mg5.mg5 and the standalone drivers built by
run_tree_check.sh) with tree_numeric.py and the exact FeynCalc values.

- Gamma(h -> zp zp): the partial width from the comment of the DECAY block of work/tree_widths.dat (16 digits).
- Standalone matrix elements at the points of tree_numeric.py (work/me_out_<process>_<gauge>.txt, h width set to 0):
  against the exact FeynCalc value (A A -> A A, A A -> h h) or Eq. (Mhh) (h h -> h h), in unitary and Feynman gauge.
- Cross sections: the value from the run banner (6 digits) and the error from the log (4 digits), in the order of
  tree_mg5.mg5.
Output: results/tree_mg5_comparison.csv
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
WORK = HERE / "work"


def main():
    num = {r["quantity"]: r for r in csv.DictReader(open(RES / "tree_numeric.csv"))}
    rows = []
    # width
    m = re.search(r"2\s+32\s+32\s+#\s+(\S+)", (WORK / "tree_widths.dat").read_text())
    mg_w = float(m.group(1))
    ours_w = float(num["width_h_AA"]["reference"])
    rows.append(["width_h_AA", mg_w, ours_w, mg_w / ours_w - 1])
    print("Gamma(h -> zp zp): MadGraph %.16e, Eq. (width) %.16e, rel. diff %+.1e" % (mg_w, ours_w, mg_w / ours_w - 1))
    # standalone matrix elements
    pts = list(csv.DictReader(open(RES / "tree_me_points.csv")))
    for proc, gauges in (("AAAA", ("u", "f")), ("AAhh", ("u", "f")), ("hhhh", ("u",))):
        mine = [p for p in pts if p["process"] == proc]
        for g in gauges:
            vals = [float(x) for x in (WORK / ("me_out_%s_%s.txt" % (proc, g))).read_text().split()]
            assert len(vals) == len(mine), (proc, g)
            for p, v in zip(mine, vals):
                exact = float(p["smatrix_exact"])
                refv = exact if exact == exact else float(p["smatrix_ours"])
                d = v / refv - 1
                key = "me_%s_%s_%s_%s" % (proc, "unitary" if g == "u" else "Feynman", p["sqrt_s"], p["cos_theta"])
                rows.append([key, v, refv, d])
                print("%-38s MadGraph %.16e  reference %.16e  rel. diff %+.1e" % (key, v, refv, d))
    # cross sections
    log = (WORK / "tree_mg5.log").read_text()
    errs = [float(e) for e in re.findall(r"Cross-section :\s+\S+ \+- (\S+) pb", log)]
    runs = [("sigma_AAAA_6_pb", "mg5_aaaa", "run_01"), ("sigma_AAAA_20_pb", "mg5_aaaa", "run_02"),
            ("sigma_AAhh_6_pb", "mg5_aahh", "run_01"), ("sigma_AAhh_20_pb", "mg5_aahh", "run_02"),
            ("sigma_hhhh_6_pb", "mg5_hhhh", "run_01"), ("sigma_hhhh_20_pb", "mg5_hhhh", "run_02")]
    assert len(errs) == len(runs)
    for (key, d, run), err in zip(runs, errs):
        banner = next((WORK / d / "Events" / run).glob("*banner.txt")).read_text()
        val = float(re.search(r"Integrated weight \(pb\)\s*:\s*(\S+)", banner).group(1))
        ours = float(num[key]["value"])
        pull = (val - ours) / err
        rows.append([key, val, ours, pull])
        print("%-18s MadGraph %.6g +- %.4g pb, tree_numeric.py %.8g pb, (MG - ours)/error = %+.2f" % (key, val, err, ours, pull))
    with open(RES / "tree_mg5_comparison.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "madgraph", "reference", "rel_diff_or_pull"])
        for r in rows:
            w.writerow([r[0], "%.16e" % r[1], "%.16e" % r[2], "%.3e" % r[3]])


if __name__ == "__main__":
    main()
