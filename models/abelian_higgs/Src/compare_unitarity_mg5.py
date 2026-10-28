#!/usr/bin/env python3
"""Step (9) of the abelian Higgs note: MadGraph standalone matrix elements with longitudinal gauge bosons (polarized
syntax zp{0}, work/sa_<process>_<gauge>, built by run_unitarity_check.sh and evaluated with tree_me_points.f at the
points of unitarity_feyncalc.wl, h width 0) against |M|^2 of the hand formulas (results/unitarity_points.csv, 20 digits).
SMATRIX divides by the identical-particle factor IDEN of matrix.f; it is multiplied back here (a fixed polarization has
no helicity average).
Output: results/unitarity_mg5_comparison.csv
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
WORK = HERE / "work"


def main():
    pts = list(csv.DictReader(open(RES / "unitarity_points.csv")))
    rows, worst = [], 0.0
    for proc, gauges in (("LL", "uf"), ("LLhh", "uf"), ("hh", "u"), ("Lh", "uf")):
        ref = [float(p["M2"]) for p in pts if p["process"] == proc]
        kin = [(p["sqrt_s"], p["cos_theta"]) for p in pts if p["process"] == proc]
        for g in gauges:
            gname = {"u": "unitary", "f": "Feynman"}[g]
            sub = next((WORK / f"sa_{proc}_{g}" / "SubProcesses").glob("P1_*"))
            iden = int(re.search(r"DATA IDEN/\s*(\d+)/", (sub / "matrix.f").read_text()).group(1))
            mg = [iden * float(x) for x in (WORK / f"me_out_{proc}_L_{g}.txt").read_text().split()]
            for (rs, c), a, b in zip(kin, mg, ref):
                d = a / b - 1
                worst = max(worst, abs(d))
                rows.append([proc, gname, rs, c, "%.16e" % a, "%.16e" % b, "%.2e" % d])
            print("%-5s %-8s IDEN %d: max |MadGraph/hand - 1| = %.1e over %d points" % (
                proc, gname, iden, max(abs(float(r[6])) for r in rows if r[0] == proc and r[1] == gname), len(ref)))
    with open(RES / "unitarity_mg5_comparison.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["process", "gauge", "sqrt_s", "cos_theta", "M2_madgraph", "M2_hand", "rel_diff"])
        w.writerows(rows)
    print("largest relative difference %.1e; written results/unitarity_mg5_comparison.csv" % worst)


if __name__ == "__main__":
    main()
