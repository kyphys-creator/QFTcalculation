"""Step (6) of the NLO note: the predicted W mass against the measured one (results/mw.csv, mw.wl).

The pole mass of mw.wl, M_W = M_Z c-hat(mu) (1 + (dZ - dW)/2), at mu = M_t and its mu dependence (M_Z/2 ... 2 M_t); the forms
equivalent at one loop, M_Z c-hat sqrt(1 + dZ - dW) and M_Z c-hat/sqrt(1 - dZ + dW), for the size of the truncation; the SM
note's value (its fit's own c-hat^2, models/sm/Src/results/msbar_fit.csv).  The measured mass is the Breit-Wigner mass with a
running width, M_BW = M_pole sqrt(1 + Gamma_W^2/M^2) (Gamma_W of step (4b), results/wweak_widths.csv).  The O(alpha alpha_s)
correction to Delta rho, -(2/3)(1 + pi^2/3)(alpha_s/pi) Delta rho_tb (Djouadi-Verzegnassi; a reference coefficient), moves
M_W by (M_W/2) c^2/(c^2 - s^2) delta Delta rho at fixed alpha, G_F, M_Z.  Measured: PDG 2024 (the note's input), PDG 2026
release (references).  Writes results/mw_summary.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "results" / "mw.csv")))
mt_row = rows[0]
mw, d, c2 = float(mt_row["MW_pole"]), float(mt_row["dZ_minus_dW"]), float(mt_row["c2hat"])
mz = 91.188 / math.sqrt(1 + (2.4955 / 91.188)**2)
gw = next(float(r["nlo"]) for r in csv.DictReader(open(HERE / "results" / "wweak_widths.csv")) if r["quantity"] == "Gamma_W")
bw = lambda m: m * math.sqrt(1 + (gw / m)**2)
mus = {round(float(r["mu"]), 3): float(r["MW_pole"]) for r in rows[3:]}
mus[round(POLE["MT"], 3)] = mw
lo = {round(float(r["mu"]), 3): mz * math.sqrt(float(r["c2hat"])) for r in rows[3:]}   # the tree M_Z c-hat(mu)
lo[round(POLE["MT"], 3)] = mz * math.sqrt(c2)
alt = [mz * math.sqrt(c2 * (1 + d)), mz * math.sqrt(c2 / (1 - d))]
sm = next(float(r["MW_pole_predicted_GeV"]) for r in csv.DictReader(open(HERE.parent.parent / "sm" / "Src" / "results" / "msbar_fit.csv"))
          if r["case"] == "PDG2024_alpha_scheme")
# Delta rho of the top-bottom doublet with G_F (the pole masses), and its O(alpha alpha_s) correction
GF, mt, mb = 1.1663788e-5, POLE["MT"], POLE["MB"]
a, b = mt**2, mb**2
drho = 3 * GF / (8 * math.sqrt(2) * math.pi**2) * (a + b - 2 * a * b / (a - b) * math.log(a / b))
als = at(mt)["alphas"]
ddrho = -2 / 3 * (1 + math.pi**2 / 3) * als / math.pi * drho
c2os = (mw / mz)**2
dmw = mw / 2 * c2os / (c2os - (1 - c2os)) * ddrho
meas = {"PDG 2024": (80.3692, 0.0133), "PDG 2026": (80.3625, 0.0077)}
print("M_W pole at mu = M_t: %.5f GeV (three gauges);  dZ - dW = %.6f, c-hat^2 = %.8f" % (mw, d, c2))
print("  mu = " + ", ".join("%.2f: %.5f" % (k, v) for k, v in sorted(mus.items())) + " GeV;  spread %.1f MeV"
      % (1000 * (max(mus.values()) - min(mus.values()))))
print("  the tree M_Z c-hat(mu) at the same mu: " + ", ".join("%.5f" % v for k, v in sorted(lo.items())) + " GeV;  spread %.1f MeV"
      % (1000 * (max(lo.values()) - min(lo.values()))))
print("  the forms sqrt(1 + d), 1/sqrt(1 - d): %.5f, %.5f GeV;  the SM note (its fit's c-hat^2): %.5f GeV (%+.1f MeV)"
      % (alt[0], alt[1], sm, 1000 * (sm - mw)))
print("  Breit-Wigner (Gamma_W = %.4f GeV of step (4b)): %.5f GeV (pole + %.1f MeV)" % (gw, bw(mw), 1000 * (bw(mw) - mw)))
print("  Delta rho_tb = %.6f;  O(alpha alpha_s): %.6f (alpha_s(m_t) = %.5f) -> delta M_W = %+.1f MeV" % (drho, ddrho, als, 1000 * dmw))
out = [["MW_pole_mu_Mt", "%.6f" % mw], ["MW_tree_spread_MeV", "%.2f" % (1000 * (max(lo.values()) - min(lo.values())))], ["MW_BW_mu_Mt", "%.6f" % bw(mw)], ["mu_spread_MeV", "%.2f" % (1000 * (max(mus.values()) - min(mus.values())))],
       ["MW_pole_sqrt_form", "%.6f" % alt[0]], ["MW_pole_inverse_sqrt_form", "%.6f" % alt[1]], ["MW_pole_SM_note", "%.6f" % sm],
       ["drho_tb", "%.8f" % drho], ["ddrho_alpha_alphas", "%.8f" % ddrho], ["dMW_alpha_alphas_MeV", "%.2f" % (1000 * dmw)]]
for k, (m, e) in meas.items():
    print("  measured %s: %.4f +- %.4f GeV (Breit-Wigner):  NLO %+.1f MeV = %+.2f sigma;  with the O(alpha alpha_s) estimate %+.2f sigma"
          % (k, m, e, 1000 * (bw(mw) - m), (bw(mw) - m) / e, (bw(mw + dmw) - m) / e))
    out.append(["pull_" + k.replace(" ", ""), "%.3f" % ((bw(mw) - m) / e)])
with open(HERE / "results" / "mw_summary.csv", "w", newline="") as fh:
    csv.writer(fh).writerows([["quantity", "value"]] + out)
print("wrote results/mw_summary.csv")
