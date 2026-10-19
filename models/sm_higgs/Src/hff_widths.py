"""Step (5) of the Higgs note: H -> f fbar at NLO with QCD, QED and the weak correction, MS-bar Yukawa couplings.

  Gamma(mu) = Gamma_0(y(mu)) [1 + (C_F alpha_s(mu)/pi + Q^2 alpha(mu)/pi) K_MS(mu) + delta_weak(mu)],
K_MS(mu) = K_OS + 2 + (3/2) ln(mu^2/m^2) of step (4) (results/hqq_massive.csv), delta_weak(mu) of hff_weak.wl (results/hff_weak.csv,
the couplings run to mu), Gamma_0 = N_c y^2 M_H beta^3/(16 pi) with the pole masses in beta, at mu = M_H, M_H/2, 2 M_H.  The
spread over mu of LO, of LO + QCD + QED (step (4)) and with the weak correction.  Writes results/hff_widths.csv.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "sm_nlo" / "Src"))
from nlo_inputs import POLE, at  # noqa: E402

MH = POLE["MH"]
CF = 4 / 3
FERM = [("b", "H_b", "d3", 3, -1 / 3, "MB", lambda p: p["yd"][2]), ("c", "H_c", "u2", 3, 2 / 3, "MC", lambda p: p["yu"][1]),
        ("tau", "H_ta", "l3", 1, -1, "MTA", lambda p: p["ye"][2]), ("mu", "H_mu", "l2", 1, -1, "MMU", lambda p: p["ye"][1])]
KOS = {r["channel"]: float(r["K_OS"]) for r in csv.DictReader(open(HERE / "results" / "hqq_massive.csv")) if float(r["delta"]) == 0}
DW = {(r["fermion"], round(float(r["mu"]), 1)): float(r["delta_weak"]) for r in csv.DictReader(open(HERE / "results" / "hff_weak.csv"))}
p = {xi: at(xi * MH) for xi in (1.0, 0.5, 2.0)}


def g0(nc, y, m):
    return nc * y**2 * MH / (16 * math.pi) * (1 - 4 * m**2 / MH**2)**1.5


def spread(v):
    return (max(v) - min(v)) / v[0]


rows = []
print("H -> f fbar at NLO [MeV], MS-bar y(mu): LO, + QCD + QED, + weak at mu = M_H;  delta_weak at mu = M_H, M_H/2, 2 M_H;  spreads")
for name, ch, wn, nc, q, mk, yf in FERM:
    m = POLE[mk]
    vals = []
    for xi in (1.0, 0.5, 2.0):
        pp, mu = p[xi], xi * MH
        kms = KOS[ch] + 2 + 1.5 * math.log(mu**2 / m**2)
        c = (CF * pp["alphas"] if nc == 3 else 0.0) + q**2 * pp["alpha"]
        lo = g0(nc, yf(pp), m)
        dw = DW[(wn, round(mu, 1))]
        vals.append((lo, lo * (1 + c * kms / math.pi), lo * (1 + c * kms / math.pi + dw), dw))
    lo, qq, full, dw = vals[0]
    sp = [spread([v[i] for v in vals]) for i in range(3)]
    print("  %-4s LO %.6f, + QCD + QED %.6f, + weak %.6f (%+.3f%% of LO);  delta_weak %+.4f%%, %+.4f%%, %+.4f%%;  spread LO %.2f%%, "
          "QCD + QED %.2f%%, + weak %.2f%%" % (name, 1e3 * lo, 1e3 * qq, 1e3 * full, 100 * (full / lo - 1), *(100 * v[3] for v in vals),
                                             *(100 * x for x in sp)))
    rows.append([name, "%.10e" % lo, "%.10e" % qq, "%.10e" % full] + ["%.8f" % v[3] for v in vals] + ["%.6f" % x for x in sp]
                + ["%.10e" % vals[i][2] for i in (1, 2)])
with open(HERE / "results" / "hff_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["fermion", "lo", "nlo_qcd_qed", "nlo_full", "dweak_MH", "dweak_MH_half", "dweak_2MH", "spread_lo", "spread_qcd_qed",
                "spread_full", "nlo_full_half", "nlo_full_2"])
    w.writerows(rows)
print("wrote results/hff_widths.csv")
