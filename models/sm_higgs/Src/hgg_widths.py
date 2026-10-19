"""Step (6) of the Higgs note: Gamma(H -> g g) at NLO QCD with the heavy-top K factor.

  Gamma = Gamma_0(alpha_s^(5)(mu)) [1 + E(mu) alpha_s^(5)(mu)/pi],
  E(mu) = 73/4 - (7/6) N_F + ((33 - 2 N_F)/6) ln(mu^2/M_H^2)   (hgg_eft_feyncalc.wl: real + virtual + MS-bar alpha_s of the operator)
          + 11/2                                                (twice the Wilson coefficient's 11/4; a reference: Spira et al.)
N_F = 5.  Gamma_0 is Eq. (loop) with the exact top, bottom and charm loops (pole masses) of step (2); only its alpha_s^2 is
alpha_s^(5).  The note's inputs run alpha_s in the full SM (six flavours, the top not decoupled); the effective theory's alpha_s
has five: alpha_s^(5)(mu) = alpha_s^(6)(mu) [1 + (alpha_s/(6 pi)) ln(m_t^2/mu^2)] (one-loop decoupling at mu, the pole m_t).
At mu = M_H, M_H/2, 2 M_H.  Writes results/hgg_widths.csv.
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
MH, MT = POLE["MH"], POLE["MT"]
NF = 5


def f(t):
    if t <= 1:
        return math.asin(math.sqrt(t))**2
    r = math.sqrt(1 - 1 / t)
    return -0.25 * (math.log((1 + r) / (1 - r)) - 1j * math.pi)**2


def a_half(t):
    return 2 * (t + (t - 1) * f(t)) / t**2


amp = 0.75 * sum(a_half(MH**2 / (4 * POLE[k]**2)) for k in ("MT", "MB", "MC"))
amp_t = 0.75 * a_half(MH**2 / (4 * MT**2))


def g0(als, a=amp):
    return als**2 * MH**3 / (72 * math.pi**3 * VG**2) * abs(a)**2


rows = []
print("Gamma(H -> g g) [MeV]: (3/4) sum A_1/2 = %.5f%+.5fi (top alone %.5f; the heavy-top limit 1)" % (amp.real, amp.imag, amp_t))
for xi in (1.0, 0.5, 2.0):
    mu = xi * MH
    a6 = at(mu)["alphas"]
    a5 = a6 * (1 + a6 / (6 * math.pi) * math.log(MT**2 / mu**2))
    e_me = 73 / 4 - 7 / 6 * NF + (33 - 2 * NF) / 6 * math.log(mu**2 / MH**2)
    e = e_me + 11 / 2
    lo6, lo5 = g0(a6), g0(a5)
    nlo = lo5 * (1 + e * a5 / math.pi)
    print("  mu = %6.1f: alpha_s^(6) %.5f, alpha_s^(5) %.5f;  LO %.6f (alpha_s^(6)), %.6f (alpha_s^(5));  E = %.4f (operator %.4f + 11/2);"
          "  K = %.4f;  NLO %.6f" % (mu, a6, a5, 1e3 * lo6, 1e3 * lo5, e, e_me, 1 + e * a5 / math.pi, 1e3 * nlo))
    rows.append([mu, a6, a5, lo6, lo5, e, nlo])
lo = [r[4] for r in rows]
nl = [r[6] for r in rows]
print("  spread over mu: LO %.2f%%, NLO %.2f%%;  mu = M_H/2, 2 M_H relative to M_H: LO %+.2f%%, %+.2f%%; NLO %+.2f%%, %+.2f%%"
      % (100 * (max(lo) - min(lo)) / lo[0], 100 * (max(nl) - min(nl)) / nl[0], 100 * (lo[1] / lo[0] - 1), 100 * (lo[2] / lo[0] - 1),
         100 * (nl[1] / nl[0] - 1), 100 * (nl[2] / nl[0] - 1)))
print("  the top loop with its mass against the heavy-top limit at LO: |A_t|^2 ratio %.4f" % abs(amp_t)**2)
with open(HERE / "results" / "hgg_widths.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["mu", "alphas6", "alphas5", "lo_alphas6_GeV", "lo_alphas5_GeV", "E", "nlo_GeV"])
    w.writerows([["%.4f" % r[0]] + ["%.10e" % x for x in r[1:]] for r in rows])
print("wrote results/hgg_widths.csv")
