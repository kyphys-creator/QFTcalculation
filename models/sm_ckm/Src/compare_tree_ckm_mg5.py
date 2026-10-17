#!/usr/bin/env python3
"""Step (2) of the CKM note: compare the MadGraph widths and cross sections (work/, from tree_ckm_mg5.mg5) with
tree_ckm_numeric.py (results/tree_ckm_numeric.csv), and u u~ > w+ w- of this UFO with the SM note's UFO (V = 1).

Widths: partial widths from the comments of the DECAY blocks of work/tree_ckm_widths.dat.
Cross sections: the value from the event banner and the error from the log, in the order of tree_ckm_mg5.mg5.
Output: results/tree_ckm_mg5_comparison.csv
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
WORK = HERE / "work"
QNAME = {1: "d", 2: "u", 3: "s", 4: "c", 5: "b", 6: "t"}
LNAME = {11: "e", 13: "mu", 15: "ta"}


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
            out[(parent, tuple(sorted((int(m.group(2)), int(m.group(3))))))] = float(m.group(4))
    return out


def key_of(parent, ch):
    a, b = ch
    if parent == 24:
        if abs(a) in LNAME or abs(b) in LNAME:
            lep = LNAME[abs(a)] if abs(a) in LNAME else LNAME[abs(b)]
            return "width_W_lep_" + lep
        up = QNAME[max(a, b)]
        dn = QNAME[-min(a, b)]
        return "width_W_%s_%s~" % (up, dn)
    if parent == 6:
        q = [x for x in ch if x != 24][0]
        return "width_t_%sW" % QNAME[q]
    return None


def read_dropped(log):
    """MadGraph sets a partial width of a coloured particle below its QCD scale to zero and prints it:
    'partial width of particle t lower than QCD scale:X. Set it to zero. ([24, 1])'."""
    out = {}
    for m in re.finditer(r"partial width of particle (\S+) lower than QCD scale:(\S+)\. Set it to zero\. \(\[(-?\d+), (-?\d+)\]\)", log):
        if m.group(1) == "t":
            out[(6, tuple(sorted((int(m.group(3)), int(m.group(4))))))] = float(m.group(2))
    return out


def main():
    ref = {r["quantity"]: float(r["value"]) for r in csv.DictReader(open(RES / "tree_ckm_numeric.csv"))}
    mg = read_widths(WORK / "tree_ckm_widths.dat")
    log = open(WORK / "tree_ckm_mg5.log").read()
    dropped = read_dropped(log)
    print("top partial widths that MadGraph set to zero (below its QCD scale), read from the log:", dropped)
    mg.update(dropped)
    rows = []
    for (parent, ch), val in sorted(mg.items(), key=lambda x: str(x[0])):
        if ch == "total" or parent not in (24, 6):
            continue
        key = key_of(parent, ch)
        rows.append([key, val, ref[key], val / ref[key] - 1])
        print("%-20s MadGraph %.12e  ours %.12e  rel %+.2e" % (key, val, ref[key], val / ref[key] - 1))
    tot = mg[(24, "total")]
    rows.append(["width_W_total", tot, ref["width_W_total"], tot / ref["width_W_total"] - 1])
    # MadGraph's top total omits the two channels it set to zero: compare it with t -> b W+ alone
    tot = mg[(6, "total")]
    rows.append(["width_t_total_MG_vs_bW", tot, ref["width_t_bW"], tot / ref["width_t_bW"] - 1])
    print("widths compared: %d, max relative difference %.2e (the DECAY totals are printed with 7 digits)"
          % (len(rows), max(abs(r[3]) for r in rows)))
    errs = [float(e) for e in re.findall(r"Cross-section :\s+\S+ \+- (\S+) pb", log)]
    names = ["udbar_enu", "usbar_enu", "uubar_dsbar", "uuww_ckm", "uuww_v1"]
    dirs = ["mg5_udenu", "mg5_usenu", "mg5_uuds", "mg5_uuww", "mg5_uuww_v1"]
    vals = {}
    for name, d, err in zip(names, dirs, errs):
        banner = next((WORK / d / "Events" / "run_01").glob("*banner.txt")).read_text()
        vals[name] = (float(re.search(r"Integrated weight \(pb\)\s*:\s*(\S+)", banner).group(1)), err)
    for name in names[:3]:
        val, err = vals[name]
        r = ref["sigma_%s_200_pb" % name]
        rows.append(["sigma_%s_200_pb" % name, val, r, (val - r) / err])
        print("sigma(%-12s) MadGraph %.6g +- %.3g pb, ours %.8g pb, (MG - ours)/error = %+.2f" % (name, val, err, r, (val - r) / err))
    # the two runs use the same random numbers (iseed = 0, same run card), so equal integrands give equal numbers;
    # the relative difference of the banner values (6 digits) is the test, not a pull with independent errors
    (a, ea), (b, eb) = vals["uuww_ckm"], vals["uuww_v1"]
    rows.append(["sigma_uuww_500_ckm_vs_v1_rel", a, b, a / b - 1])
    print("sigma(u u~ > w+ w-, 500 GeV): CKM UFO %.6g +- %.3g pb, SM note's UFO (V = 1) %.6g +- %.3g pb, rel. %.1e"
          " (same random numbers)" % (a, ea, b, eb, a / b - 1))
    with open(RES / "tree_ckm_mg5_comparison.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "madgraph", "reference", "rel_diff_or_pull"])
        for r in rows:
            w.writerow([r[0], "%.15e" % r[1], "%.15e" % r[2], "%.3e" % r[3]])


if __name__ == "__main__":
    main()
