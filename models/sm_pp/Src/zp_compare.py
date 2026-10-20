"""Research note models/sm_pp, step (4c): aMC@NLO at fixed order with the note's Z' NLO UFO (zp_mg5.sh) against the own LO and NLO
of zp_hadronic.py: sigma(p p -> Z' -> e+ e-) with m_ee > 225 GeV and in |m_ee - M| < 2 Gamma, M = 1, 3, 5 TeV, all nine
(mu_R, mu_F) columns (reweighting), the widths of the MG5 runs; the 3 TeV NLO also from the second run (another seed,
req_acc_FO = 3e-4; the first run's m_ee > 225 GeV total was 2.9 sigma high).  Writes results/zp_compare.csv.
Run with ~/hep/opt/lhc/bin/python.
"""
import csv
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC))
import zp_hadronic as zh  # noqa: E402

dy = zh.dy
RUNS = {1000: 29.1391, 3000: 88.6729, 5000: 147.960}   # the widths of zp_mg5.sh
WINDOWS = {1000: "window 1000", 3000: "window 3000", 5000: "window 5000"}


def main():
    dy.lhapdf.setVerbosity(0)
    pdf = dy.lhapdf.mkPDF(dy.PDFNAME, 0)
    out = []
    worst = 0.0
    for M, W in RUNS.items():
        p = zh.zp_params(M)
        p["W"] = W
        lums = {f * M: dy.Lumi(pdf, f * M, 225.0 ** 2 / dy.S / 2) for f in (1.0, 2.0, 0.5)}
        for order in ("LO", "NLO") + (("NLO_p",) if M == 3000 else ()):
            h = dy.read_hwu(SRC / "work" / "zp" / "ppzp" / "Events" / ("m%d_%s" % (M, order)) / "MADatNLO.HwU")
            run = order
            order = order.split("_")[0]
            for name, qlo, qhi in (("total", 225.0, zh.QHI), (WINDOWS[M], M - 2 * W, M + 2 * W)):
                labels, rows = h[name]
                cols = dy.scale_columns(labels) if order == "NLO" else [(2, 1.0, 1.0)]
                pulls = []
                for k, xr, xf in cols:
                    own = zh.sigma(p, lums, pdf.alphasQ, xr, xf, order, qlo=qlo, qhi=qhi)
                    mg, err = rows[0][k], rows[0][3] * max(1.0, abs(rows[0][k] / rows[0][2]))
                    pull = (mg - own) / err
                    pulls.append(pull)
                    worst = max(worst, abs(pull))
                    out.append([M, run, name, "%g,%g" % (xr, xf), "%.8e" % own, "%.8e" % mg, "%.3e" % err, "%.2f" % pull])
                    if (xr, xf) == (1.0, 1.0):
                        print("    M = %4d %-5s %-12s own %.6e pb  MG5 %.6e +- %.1e  (%+.2f sigma, %+.1e)"
                              % (M, run, name, own, mg, err, pull, mg / own - 1))
                if len(cols) > 1:
                    print("        all %d scale columns: pulls %+.2f to %+.2f" % (len(cols), min(pulls), max(pulls)))
    print("largest |pull|: %.2f" % worst)
    with open(SRC / "results" / "zp_compare.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["M_GeV", "order", "quantity", "xiR,xiF", "own_pb", "mg5_pb", "mg5_err_pb", "pull"])
        w.writerows(out)
    print("written: results/zp_compare.csv")


if __name__ == "__main__":
    main()
