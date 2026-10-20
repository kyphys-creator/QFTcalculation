"""Research note models/sm_pp, step (1), the comparison with the measured W cross sections: the effect of the CKM matrix.
The note and MG5's loop_sm use V_CKM = 1.  With the PDG values (reference), every pair u_i dbar_j -> W+ (d_j ubar_i -> W-) enters with
|V_ij|^2, its q g legs too (sum_j |V_uj|^2 = 1 for u g -> W+ d_j); the coefficient functions are the same (dy_hadronic.py).
The W totals (1e-3 GeV < m_enu < 13 TeV, mu = M_W, NNPDF4.0 NLO) with diagonal and with PDG |V_ij| -> results/dy_ckm.csv.
Run with ~/hep/opt/lhc/bin/python (about 1 minute)."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dy_hadronic as d  # noqa: E402

# |V_ij| (PDG 2024, reference): (up-type pid, down-type pid)
VCKM = {(2, 1): 0.97367, (2, 3): 0.22431, (2, 5): 0.00382, (4, 1): 0.221, (4, 3): 0.975, (4, 5): 0.0411}
MU0 = 80.419002


def main():
    d.lhapdf.setVerbosity(0)
    pdf = d.lhapdf.mkPDF(d.PDFNAME, 0)
    rows = [["process", "order", "diagonal_pb", "pdg_ckm_pb", "ratio"]]
    orig = d.channels
    for proc in ("wp", "wm"):
        ew = d.param_card(d.WORK / proc / "Cards" / "param_card.dat")
        lums = {MU0: d.Lumi(pdf, MU0, 1e-6 / d.S / 2)}
        for order in ("LO", "NLO"):
            diag, ckm = 0.0, 0.0
            for (i, j), v in VCKM.items():
                quark, antiquark = (i, -j) if proc == "wp" else (j, -i)
                d.channels = lambda p, a=quark, b=antiquark: [(("u", "d"), [(a, b)], [(a, 21), (b, 21)])]
                s = d.bin_sigma(proc, ew, lums, pdf.alphasQ, MU0, MU0, 1e-3, d.SQRTS, order)
                ckm += v * v * s
                if (i, j) in ((2, 1), (4, 3)):
                    diag += s
            d.channels = orig
            rows.append([proc, order, "%.4f" % diag, "%.4f" % ckm, "%.5f" % (ckm / diag)])
            print("%s %-3s: diagonal CKM %.2f pb, PDG CKM %.2f pb, ratio %.4f" % (proc, order, diag, ckm, ckm / diag))
    with open(d.RES / "dy_ckm.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print("written: results/dy_ckm.csv")


if __name__ == "__main__":
    main()
