#!/usr/bin/env python3
"""Step (2) of the SM note: compare the MadGraph widths and cross sections (work/, from tree_mg5.mg5) with the
numbers of tree_numeric.py (results/tree_numeric.csv, Eq. (widths) and the explicit-matrix cross sections).

Widths: the partial widths are read from the comments of the DECAY blocks of work/tree_widths.dat (17 digits).
Cross sections: the value from the event banner (6 digits) and the error from the log (4 digits).
Output: results/tree_mg5_comparison.csv
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
WORK = HERE / "work"

PDG = {1: "d", 2: "u", 3: "s", 4: "c", 5: "b", 6: "t", 11: "e", 12: "ve", 13: "mu", 14: "vm", 15: "ta", 16: "vt"}
W_CH = {(2, -1): "u_d~", (4, -3): "c_s~", (12, -11): "ve_e+", (14, -13): "vm_mu+", (16, -15): "vt_ta+"}


def read_widths(path):
    out = {}
    parent = None
    for line in open(path):
        m = re.match(r"DECAY\s+(\d+)\s+(\S+)", line)
        if m:
            parent = int(m.group(1))
            out[(parent, "total")] = float(m.group(2))
            continue
        m = re.match(r"\s+(\S+)\s+2\s+(-?\d+)\s+(-?\d+)\s+#\s+(\S+)", line)
        if m and parent is not None:
            out[(parent, (int(m.group(2)), int(m.group(3))))] = float(m.group(4))
    return out


def main():
    ref = {r["quantity"]: float(r["value"]) for r in csv.DictReader(open(RES / "tree_numeric.csv"))}
    mg = read_widths(WORK / "tree_widths.dat")
    rows = []
    for (parent, ch), val in sorted(mg.items(), key=lambda x: str(x[0])):
        if ch == "total":
            continue
        if parent == 24:
            key = "width_W_" + W_CH[ch]
        elif parent == 23:
            key = "width_Z_" + PDG[ch[0]]
        elif parent == 25:
            key = "width_H_" + PDG[ch[0]]
        elif parent == 6:
            key = "width_t_bW"
        else:
            continue
        rows.append([key, val, ref[key], val / ref[key] - 1])
    for parent, name in ((24, "W"), (23, "Z"), (25, "H")):
        rows.append(["width_%s_total" % name, mg[(parent, "total")], ref["width_%s_total" % name],
                     mg[(parent, "total")] / ref["width_%s_total" % name] - 1])
    worst = max(abs(r[3]) for r in rows)
    print("widths compared: %d, max relative difference %.2e (the DECAY totals are printed with 7 digits)"
          % (len(rows), worst))
    log = open(WORK / "tree_mg5.log").read()
    errs = [float(e) for e in re.findall(r"Cross-section :\s+\S+ \+- (\S+) pb", log)]
    runs = [("sigma_eemm_200_pb", WORK / "mg5_eemm/Events/run_01"), ("sigma_eeww_200_pb", WORK / "mg5_eeww/Events/run_01"),
            ("sigma_eeww_500_pb", WORK / "mg5_eeww/Events/run_02")]
    for (key, run), err in zip(runs, errs):
        banner = next(run.glob("*banner.txt")).read_text()
        val = float(re.search(r"Integrated weight \(pb\)\s*:\s*(\S+)", banner).group(1))
        pull = (val - ref[key]) / err
        rows.append([key, val, ref[key], pull])
        print("%-18s MadGraph %.6g +- %.4g pb, explicit matrices %.8g pb, (MG - ours)/error = %+.2f"
              % (key, val, err, ref[key], pull))
    with open(RES / "tree_mg5_comparison.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "madgraph", "tree_numeric", "rel_diff_or_pull"])
        for r in rows:
            w.writerow([r[0], "%.15e" % r[1], "%.15e" % r[2], "%.3e" % r[3]])


if __name__ == "__main__":
    main()
