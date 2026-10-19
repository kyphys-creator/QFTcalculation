"""Step (4) of the Higgs note: H -> b bbar, c cbar, tau tau, mu mu at NLO QCD and QED with the quark and lepton masses.

  MS-bar Yukawa (the note's):  Gamma(mu) = Gamma_0(y(mu)) [1 + (C_F alpha_s(mu)/pi + Q^2 alpha(mu)/pi) K_MS(mu)],
                               K_MS(mu) = K_OS + 2 + (3/2) ln(mu^2/m^2)   (hqq_massive_virtual.wl checks this relation),
  pole Yukawa sqrt(2) m/v_G:   Gamma = Gamma_0(y_pole) [1 + (C_F alpha_s(M_H)/pi + Q^2 alpha(M_H)/pi) K_OS],
with Gamma_0 = N_c y^2 M_H beta^3/(16 pi), the pole masses in beta and in K_OS (results/hqq_massive.csv: K_OS extrapolated to
delta -> 0, equal to Drees-Hikasa's Delta_H(beta)), the couplings of the NLO note's inputs at mu = M_H, M_H/2, 2 M_H (the QCD
factor for the quarks only).  Against the massless widths of step (3) (results/hqq_widths.csv).  Writes
results/hqq_massive_widths.csv.
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
FERM = [("b", "H_b", 3, -1 / 3, "MB", lambda p: p["yd"][2]), ("c", "H_c", 3, 2 / 3, "MC", lambda p: p["yu"][1]),
        ("tau", "H_ta", 1, -1, "MTA", lambda p: p["ye"][2]), ("mu", "H_mu", 1, -1, "MMU", lambda p: p["ye"][1])]
KOS = {r["channel"]: float(r["K_OS"]) for r in csv.DictReader(open(HERE / "results" / "hqq_massive.csv")) if float(r["delta"]) == 0}
ML = {r["fermion"]: r for r in csv.DictReader(open(HERE / "results" / "hqq_widths.csv"))}
p = {xi: at(xi * MH) for xi in (1.0, 0.5, 2.0)}


def g0(nc, y, m):
    return nc * y**2 * MH / (16 * math.pi) * (1 - 4 * m**2 / MH**2)**1.5


rows = []
print("H -> f fbar with the masses [MeV]: MS-bar y(mu) at mu = M_H (mu = M_H/2, 2 M_H), the pole Yukawa coupling, the massless value")
for name, ch, nc, q, mk, yf in FERM:
    m = POLE[mk]
    kos = KOS[ch]
    res = {}
    for xi, pp in p.items():
        mu = xi * MH
        kms = kos + 2 + 1.5 * math.log(mu**2 / m**2)
        c = (CF * pp["alphas"] if nc == 3 else 0.0) + q**2 * pp["alpha"]
        lo = g0(nc, yf(pp), m)
        res[xi] = (lo, lo * (1 + c * kms / math.pi), kms)
    lo, nlo, kms = res[1.0]
    spread_lo = (max(r[0] for r in res.values()) - min(r[0] for r in res.values())) / lo
    spread_nlo = (max(r[1] for r in res.values()) - min(r[1] for r in res.values())) / nlo
    ypole = math.sqrt(2) * m / VG
    c0 = (CF * p[1.0]["alphas"] if nc == 3 else 0.0) + q**2 * p[1.0]["alpha"]
    pole_lo = g0(nc, ypole, m)
    pole_nlo = pole_lo * (1 + c0 * kos / math.pi)
    ml_nlo = float(ML[name]["nlo_qcd_qed"])
    print("  %-4s K_OS = %.6f, K_MS(M_H) = %.6f (massless 17/4);  LO %.6f, NLO %.6f (%+.3f%%);  spread over mu: LO %.2f%%, NLO %.2f%%"
          % (name, kos, kms, 1e3 * lo, 1e3 * nlo, 100 * (nlo / lo - 1), 100 * spread_lo, 100 * spread_nlo))
    print("       massless (step (3)) NLO %.6f: the masses change the NLO width by %+.3f%%;  pole Yukawa: LO %.6f, NLO %.6f"
          % (1e3 * ml_nlo, 100 * (nlo / ml_nlo - 1), 1e3 * pole_lo, 1e3 * pole_nlo))
    rows.append([name, "%.10f" % kos, "%.10f" % kms, "%.10e" % lo, "%.10e" % nlo, "%.6f" % spread_lo, "%.6f" % spread_nlo,
                 "%.10e" % ml_nlo, "%.10e" % pole_lo, "%.10e" % pole_nlo]
                + ["%.10e" % res[xi][j] for xi in (0.5, 2.0) for j in (0, 1)])
with open(HERE / "results" / "hqq_massive_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["fermion", "K_OS", "K_MS_MH", "lo", "nlo", "spread_lo", "spread_nlo", "nlo_massless", "pole_lo", "pole_nlo",
                "lo_half", "nlo_half", "lo_2", "nlo_2"])
    w.writerows(rows)
print("wrote results/hqq_massive_widths.csv")
