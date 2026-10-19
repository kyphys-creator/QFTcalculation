"""Step (3) of the NLO note: the QCD and QED corrections with the masses, applied to the LO widths of step (1).

K of ir_massive_real.wl (results/ir_massive.csv, delta -> 0; Gamma^(1)/Gamma_0 = (alpha C/pi) K) for each current:
  Z -> f fbar:  Gamma = Gamma_0^V [1 + (alpha_s C_F + alpha Q^2) K_V/pi] + Gamma_0^A [1 + (alpha_s C_F + alpha Q^2) K_A/pi]
                (alpha_s only for quarks), Gamma_0^V : Gamma_0^A = v^2 (3 - beta^2)/2 : a^2 beta^2 of Eq. (lo); K = 3/4 for the
                massless u, d, s, e (the massless limit of step (2)), the massive K for c, b, mu, tau (pole masses);
  t -> d_j W+:  Gamma = Gamma_0 (1 + alpha_s(m_t) C_F K_t/pi), K_t of m_b = 4.78 GeV for all three (the m_b dependence of K is
                below 1e-3 and t -> s W+, d W+ are 0.2% of the width).
The MS-bar alpha, alpha_s and s^2 at mu = M (nlo_inputs.py); the measured values (PDG 2024) are references.  The corrections
of step (2) (results/ir_inclusive.csv: massless K for all) are shown for comparison.  Writes results/ir_massive_widths.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
lo = {r[0]: float(r[1]) for r in list(csv.reader(open(HERE / "results" / "lo_widths.csv")))[1:]}
K = {}
for r in csv.DictReader(open(HERE / "results" / "ir_massive.csv")):
    if float(r["delta"]) == 0.0:
        K[r["channel"]] = float(r["K"])
step2 = {r["quantity"]: float(r["lo_times_inclusive"]) for r in csv.DictReader(open(HERE / "results" / "ir_inclusive.csv"))}
CF = 4 / 3
# name: (T3, Q, mass key, K channel or None for massless)
FERM = {"e": (-0.5, -1, "Me", None), "mu": (-0.5, -1, "MMU", "Z_mu"), "ta": (-0.5, -1, "MTA", "Z_ta"),
        "u": (0.5, 2 / 3, "MU", None), "c": (0.5, 2 / 3, "MC", "Z_c"), "d": (-0.5, -1 / 3, "MD", None),
        "s": (-0.5, -1 / 3, "MS", None), "b": (-0.5, -1 / 3, "MB", "Z_b")}
PDG = {"Gamma_ll": (0.083984, 0.000086), "Gamma_had": (1.7444, 0.0020), "Gamma_Z": (2.4955, 0.0023),
       "R_l": (20.767, 0.025), "R_b": (0.21629, 0.00066), "R_c": (0.1721, 0.0030),
       "Gamma_t": (1.42, 0.15)}   # Gamma_t: +0.19 -0.15, the lower error (the value is below)

pz, pt = at(POLE["MZ"]), at(POLE["MT"])
aZ, asZ, s2, ast = pz["alpha"], pz["alphas"], pz["s2"], pt["alphas"]


def z_width(f):
    t3, q, mk, ch = FERM[f]
    m = POLE[mk]
    b2 = 1 - 4 * m**2 / POLE["MZ"]**2
    v, a = t3 - 2 * q * s2, t3
    wv, wa = v**2 * (3 - b2) / 2, a**2 * b2
    kv, ka = (0.75, 0.75) if ch is None else (K[ch + "_V"], K[ch + "_A"])
    c = (asZ * CF if f in "udscb" else 0.0) + aZ * q**2
    g0 = lo["Z_" + f]
    return g0 * (wv * (1 + c * kv / math.pi) + wa * (1 + c * ka / math.pi)) / (wv + wa), (wv * kv + wa * ka) / (wv + wa)


nlo, keff = {}, {}
for f in FERM:
    nlo[f], keff[f] = z_width(f)
had_lo = sum(lo["Z_" + q] for q in "udscb")
had = sum(nlo[q] for q in "udscb")
gz = 3 * lo["Z_ve"] + sum(nlo[l] for l in ("e", "mu", "ta")) + had
gt0 = lo["t_total"]
gt = gt0 * (1 + ast * CF * K["t_bW"] / math.pi)
print("alpha(M_Z) = 1/%.4f, alpha_s(M_Z) = %.5f, s^2(M_Z) = %.6f, alpha_s(m_t) = %.5f" % (1 / aZ, asZ, s2, ast))
print("effective K (Born-weighted V and A): " + ", ".join("%s %.6f" % (f, keff[f]) for f in FERM))
print("  Z -> b bbar: QCD correction %.4f%% (massless: alpha_s/pi = %.4f%%)" % (100 * asZ * CF * keff["b"] / math.pi, 100 * asZ / math.pi))
print("  t -> b W+:   QCD correction %.4f%% (K_t = %.6f; alpha_s C_F K_t/pi = %.5f alpha_s)"
      % (100 * ast * CF * K["t_bW"] / math.pi, K["t_bW"], CF * K["t_bW"] / math.pi))
rows = [("Gamma_ll", lo["Z_e"], step2["Gamma_ll"], nlo["e"]), ("Gamma_had", had_lo, step2["Gamma_had"], had),
        ("Gamma_Z", lo["Z_total"], step2["Gamma_Z"], gz), ("R_l", had_lo / lo["Z_e"], step2["R_l"], had / nlo["e"]),
        ("R_b", lo["Z_b"] / had_lo, None, nlo["b"] / had), ("R_c", lo["Z_c"] / had_lo, None, nlo["c"] / had),
        ("Gamma_t", gt0, None, gt)]
out = []
for name, a, b, c in rows:
    m, e = PDG[name]
    b2 = "%.6f (%+.2f%%)" % (b, 100 * (b / m - 1)) if b is not None else "-"
    print("  %-9s LO %.6f (%+.2f%%)  step (2) %s  step (3) %.6f (%+.2f%%)   measured %.6f +- %.6f"
          % (name, a, 100 * (a / m - 1), b2, c, 100 * (c / m - 1), m, e))
    out.append([name, "%.8e" % a, "" if b is None else "%.8e" % b, "%.8e" % c, m, e])
with open(HERE / "results" / "ir_massive_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "lo", "step2_massless", "step3_massive", "measured", "error"])
    w.writerows(out)
print("wrote results/ir_massive_widths.csv")
