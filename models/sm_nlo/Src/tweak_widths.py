"""Step (4c) of the NLO note: the top width at NLO (electroweak and QCD).

  Gamma(t -> d_j W+)(mu) = Gamma_0,j(mu) [1 + delta_EW,j(mu) + alpha_s(mu) C_F K/pi]
with Gamma_0 at mu = m_t, m_t/2, 2 m_t (results/lo_widths.csv, step (1)), delta_EW at the same mu (results/treal.csv: virtual +
soft + hard photon, the photon inclusive, delta -> 0; tweak.wl, treal.wl) and the K of t -> b W+ of step (3) (results/ir_massive.csv,
m_b = 4.78 GeV) for all three (t -> s W+, d W+ are 0.18% of the width; their K with a massless quark differs from that of the b by
the b mass).  The mixed O(alpha alpha_s) and the higher orders are not included.  The measured width (PDG 2026 release) is a
reference.  The mu dependence of the NLO values against that of the LO values.  Writes results/tweak_widths.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
MT = POLE["MT"]
CF = 4 / 3
lo = {r[0]: [float(x) for x in r[1:]] for r in list(csv.reader(open(HERE / "results" / "lo_widths.csv")))[1:]}   # mu = M, M/2, 2M
dew = {(r["channel"], round(float(r["mu"]), 3)): float(r["delta_EW"]) for r in csv.DictReader(open(HERE / "results" / "treal.csv"))}
K = next(float(r["K"]) for r in csv.DictReader(open(HERE / "results" / "ir_massive.csv")) if r["channel"] == "t_bW" and float(r["delta"]) == 0)
CHANS = [("tdW", "t_d"), ("tsW", "t_s"), ("tbW", "t_b")]
MEAS = (1.42, 0.19, 0.15)


def widths(imu, with_ew=True, with_qcd=True):
    mu = (MT, MT / 2, 2 * MT)[imu]
    a_s = at(mu)["alphas"]
    return {n: lo[key][imu] * (1 + (dew[(n, round(mu, 3))] if with_ew else 0) + (a_s * CF * K / math.pi if with_qcd else 0))
            for n, key in CHANS}


def obs(w):
    tot = sum(w.values())
    return {"Gamma_tbW": w["tbW"], "Gamma_t": tot, "BR_tbW": w["tbW"] / tot}


print("delta_EW at mu = m_t: " + ", ".join("%s %+.4f%%" % (n, 100 * dew[(n, round(MT, 3))]) for n, _ in CHANS) +
      ";  the QCD factor alpha_s(m_t) C_F K/pi = %+.4f%% (K = %.6f)" % (100 * at(MT)["alphas"] * CF * K / math.pi, K))
mb = {r["channel"]: float(r["delta_EW"]) for r in csv.DictReader(open(HERE / "results" / "treal.csv")) if abs(float(r["mu"]) - MT) < 1e-6}
print("  t -> b W+ at m_b/3, m_b/10 minus m_b (the collinear logarithm cancels; powers of m_b/m_t remain): %.1e, %.1e"
      % (mb["tbW_mb3"] - mb["tbW"], mb["tbW_mb10"] - mb["tbW"]))
o_lo = [obs(widths(i, False, False)) for i in range(3)]
o_q = obs(widths(0, False, True))
o = [obs(widths(i)) for i in range(3)]
o_ew = [obs(widths(i, True, False)) for i in range(3)]
rows = []
print("%-10s %-11s %-11s %-11s %-11s  %s" % ("quantity", "LO", "LO + QCD", "LO + EW", "NLO", "mu = M/2, 2M: LO; LO + EW; NLO"))
for k in ("Gamma_tbW", "Gamma_t", "BR_tbW"):
    d = [[100 * (x[i][k] / x[0][k] - 1) for i in (1, 2)] for x in (o_lo, o_ew, o)]
    print("%-10s %.6f   %.6f   %.6f   %.6f    %+.3f%% %+.3f%%;  %+.3f%% %+.3f%%;  %+.3f%% %+.3f%%"
          % (k, o_lo[0][k], o_q[k], o_ew[0][k], o[0][k], *d[0], *d[1], *d[2]))
    rows.append([k, "%.8e" % o_lo[0][k], "%.8e" % o_q[k], "%.8e" % o_ew[0][k], "%.8e" % o[0][k]] + ["%.4f" % x for x in sum(d, [])])
g = o[0]["Gamma_t"]
print("Gamma_t at NLO %.4f GeV;  the measured %.2f +%.2f -%.2f GeV (PDG 2026, reference): %+.1f%%, %+.2f sigma"
      % (g, MEAS[0], MEAS[1], MEAS[2], 100 * (g / MEAS[0] - 1), (g - MEAS[0]) / (MEAS[1] if g > MEAS[0] else MEAS[2])))
with open(HERE / "results" / "tweak_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "lo", "lo_qcd", "lo_ew", "nlo", "lo_mu_half_pct", "lo_mu_2_pct", "lo_ew_mu_half_pct", "lo_ew_mu_2_pct",
                "nlo_mu_half_pct", "nlo_mu_2_pct"])
    w.writerows(rows)
print("wrote results/tweak_widths.csv")
