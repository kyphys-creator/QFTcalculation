"""Step (3) of the Higgs note: H -> f fbar at NLO in QCD (and QED) in the massless limit, with the MS-bar Yukawa couplings.

Eq. (hqq) (hqq_massless_feyncalc.wl, exact in d; hqq_gluonmass.wl, a gluon mass):
  Gamma(mu) = Gamma_0(y(mu)) [1 + (C alpha(mu)/pi)(17/4 + (3/2) ln(mu^2/M_H^2))],   Gamma_0 = N_c y^2 M_H/(16 pi)  (beta = 1),
C alpha = C_F alpha_s for the quarks (plus Q^2 alpha for the photon), Q^2 alpha for the leptons, with the couplings of the NLO
note's inputs at mu = M_H, M_H/2, 2 M_H (models/sm_nlo/Src/nlo_inputs.py: one-loop running with the gauge and Yukawa couplings,
so the weak part of the running of y stays until the weak correction of step (5)).  Against Eq. (hqqpole), the same order in
the pole Yukawa coupling sqrt(2) m/v_G: Gamma_0(y_pole) [1 + (C_F alpha_s/pi)(9/4 + (3/2) ln(m^2/M_H^2))] (alpha_s(M_H)), whose
large logarithm the MS-bar coupling resums.  The quark masses of the kinematics (beta^3) are the subject of step (4).
Writes results/hqq_widths.csv.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "sm_nlo" / "Src"))
from nlo_inputs import POLE, at  # noqa: E402

GF = 1.1663788e-5
VG = (math.sqrt(2) * GF)**-0.5
MH = POLE["MH"]
CF = 4 / 3
FERM = [("b", 3, -1 / 3, "MB", lambda p: p["yd"][2]), ("c", 3, 2 / 3, "MC", lambda p: p["yu"][1]),
        ("tau", 1, -1, "MTA", lambda p: p["ye"][2]), ("mu", 1, -1, "MMU", lambda p: p["ye"][1])]
p = {xi: at(xi * MH) for xi in (1.0, 0.5, 2.0)}


def g0(nc, y):
    return nc * y**2 * MH / (16 * math.pi)


def k(mu):
    return 17 / 4 + 1.5 * math.log(mu**2 / MH**2)


rows = []
print("H -> f fbar, massless limit [MeV]: LO, NLO QCD, NLO QCD + QED at mu = M_H (spread over mu = M_H/2, M_H, 2 M_H)")
for name, nc, q, mk, yf in FERM:
    vals = {}
    for xi, pp in p.items():
        mu = xi * MH
        lo = g0(nc, yf(pp))
        qcd = CF * pp["alphas"] / math.pi * k(mu) if nc == 3 else 0.0
        qed = q**2 * pp["alpha"] / math.pi * k(mu)
        vals[xi] = (lo, lo * (1 + qcd), lo * (1 + qcd + qed))
    spread = [(max(v[i] for v in vals.values()) - min(v[i] for v in vals.values())) / vals[1.0][i] for i in range(3)]
    c = vals[1.0]
    corr_qcd = c[1] / c[0] - 1
    corr_all = c[2] / c[0] - 1
    m = POLE[mk]
    ypole = math.sqrt(2) * m / VG
    pole_lo = g0(nc, ypole)
    pole_nlo = pole_lo * (1 + (CF * p[1.0]["alphas"] / math.pi * (9 / 4 + 1.5 * math.log(m**2 / MH**2)) if nc == 3 else 0.0))
    print("  %-4s LO %.6f, NLO QCD %.6f (%+.3f%%), + QED %.6f (%+.3f%%);  spread over mu: LO %.2f%%, NLO QCD %.2f%%, + QED %.2f%%"
          % (name, 1e3 * c[0], 1e3 * c[1], 100 * corr_qcd, 1e3 * c[2], 100 * corr_all, 100 * spread[0], 100 * spread[1], 100 * spread[2]))
    if nc == 3:
        print("       pole Yukawa: LO %.6f, NLO %.6f (the bracket %.4f)" % (1e3 * pole_lo, 1e3 * pole_nlo, pole_nlo / pole_lo))
    rows.append([name, "%.10e" % c[0], "%.10e" % c[1], "%.10e" % c[2], "%.6f" % corr_qcd, "%.6f" % corr_all,
                 "%.6f" % spread[0], "%.6f" % spread[1], "%.6f" % spread[2], "%.10e" % pole_lo, "%.10e" % pole_nlo]
                + ["%.10e" % vals[xi][j] for xi in (0.5, 2.0) for j in range(3)])
with open(HERE / "results" / "hqq_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["fermion", "lo", "nlo_qcd", "nlo_qcd_qed", "corr_qcd", "corr_qcd_qed", "spread_lo", "spread_nlo_qcd",
                "spread_nlo_qcd_qed", "pole_lo", "pole_nlo", "lo_half", "nlo_qcd_half", "nlo_all_half", "lo_2", "nlo_qcd_2", "nlo_all_2"])
    w.writerows(rows)
print("wrote results/hqq_widths.csv")
