"""Step (2) of the NLO note: Eq. (inclusive) applied to the LO widths of step (1).

Each LO partial width at mu = M (results/lo_widths.csv) is multiplied by the massless inclusive factor of Eq. (inclusive),
  leptons 1 + (3/4) alpha Q^2/pi,   quarks 1 + (3/4) alpha Q^2/pi + alpha_s/pi,   neutrinos 1,
with the MS-bar alpha and alpha_s at mu = M (nlo_inputs.py).  The quark masses enter only the LO widths (the m_b, m_c terms of
the correction are step (3)).  For W -> q qbar' only the QCD factor: the photon also couples to the W, and the QED part alone
is not gauge invariant (step (4)).  The measured values (PDG 2024) are references.  Writes results/ir_inclusive.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
lo = {r[0]: float(r[1]) for r in list(csv.reader(open(HERE / "results" / "lo_widths.csv")))[1:]}
Q = {"e": -1, "mu": -1, "ta": -1, "u": 2 / 3, "c": 2 / 3, "d": -1 / 3, "s": -1 / 3, "b": -1 / 3}
PDG = {"Gamma_ll": (0.083984, 0.000086), "Gamma_inv": (0.4990, 0.0015), "Gamma_had": (1.7444, 0.0020),
       "Gamma_Z": (2.4955, 0.0023), "R_l": (20.767, 0.025), "Gamma_W": (2.085, 0.042)}

pz, pw = at(POLE["MZ"]), at(POLE["MW"])
aZ, asZ, asW = pz["alpha"], pz["alphas"], pw["alphas"]


def factor_z(f):
    return 1 + 0.75 * aZ * Q[f]**2 / math.pi + (asZ / math.pi if f in "udscb" else 0.0)


nlo = {"Z_" + f: lo["Z_" + f] * factor_z(f) for f in Q}
inv = 3 * lo["Z_ve"]
had = sum(nlo["Z_" + q] for q in "udscb")
had_lo = sum(lo["Z_" + q] for q in "udscb")
gz = inv + sum(nlo["Z_" + l] for l in ("e", "mu", "ta")) + had
w_had_lo = sum(lo["W_" + c] for c in ("ud", "us", "ub", "cd", "cs", "cb"))
gw = lo["W_total"] + w_had_lo * asW / math.pi
rows = [("Gamma_ll", lo["Z_e"], nlo["Z_e"]), ("Gamma_inv", inv, inv), ("Gamma_had", had_lo, had), ("Gamma_Z", lo["Z_total"], gz),
        ("R_l", had_lo / lo["Z_e"], had / nlo["Z_e"]), ("Gamma_W", lo["W_total"], gw)]
print("Eq. (inclusive) on the LO widths: alpha(M_Z) = 1/%.4f, alpha_s(M_Z) = %.5f (alpha_s/pi = %.4f%%), alpha_s(M_W) = %.5f"
      % (1 / aZ, asZ, 100 * asZ / math.pi, asW))
out = []
for name, a, b in rows:
    m, e = PDG[name]
    print("  %-10s LO %.6f  with Eq. (inclusive) %.6f  (%+.3f%%)   measured %.6f +- %.6f: LO %+.2f%%, corrected %+.2f%%"
          % (name, a, b, 100 * (b / a - 1), m, e, 100 * (a / m - 1), 100 * (b / m - 1)))
    out.append([name, "%.8e" % a, "%.8e" % b, m, e])
with open(HERE / "results" / "ir_inclusive.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "lo", "lo_times_inclusive", "measured", "error"])
    w.writerows(out)
print("wrote results/ir_inclusive.csv")
