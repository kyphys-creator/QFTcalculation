"""Step (7) of the NLO note: the widths in the MS-bar couplings (steps (4a)-(4c)) against the on-shell G_mu scheme at one loop.

MS-bar:   Gamma(mu) = Gamma_0(g(mu), s^2(mu)) [1 + delta(mu)]   (results/lo_widths.csv; zweak.csv, wreal.csv, treal.csv)
G_mu:     Gamma     = Gamma_0(g0, s0^2) [1 + delta(mu) + C(mu)],
the tree in the couplings g0^2 = 4 sqrt2 G_F M_W^2, G0^2 = 4 sqrt2 G_F M_Z^2, s0^2 = 1 - M_W^2/M_Z^2 (the pole masses of the SM
note's fit), and C the one-loop change of the tree from those to the MS-bar couplings (results/scheme.csv, scheme.wl):
  Z -> nu nubar:  C = dZ - DeltaHat;   Z -> e+ e-:  C = dZ - DeltaHat + (d ln Gamma_0/d s^2) (-c0^2 (dW - dZ));
  W -> e nu, t -> b W:  C = dW - DeltaHat  (the same V_tb in both; the CKM conversion of the CKM note's step (6) is left out).
Z -> e+ e- with the weak correction only (the photonic factor is common).  The G_mu result has no mu at O(alpha): its mu
dependence and the MS-bar minus G_mu difference are O(alpha^2).  Writes results/scheme_compare.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
GF = 1.1663788e-5
mw = 80.3692 / math.sqrt(1 + (2.085 / 80.3692)**2)
mz = 91.188 / math.sqrt(1 + (2.4955 / 91.188)**2)
g02, G02, s02 = 4 * math.sqrt(2) * GF * mw**2, 4 * math.sqrt(2) * GF * mz**2, 1 - mw**2 / mz**2
lo = {r[0]: [float(x) for x in r[1:]] for r in list(csv.reader(open(HERE / "results" / "lo_widths.csv")))[1:]}   # mu = M, M/2, 2M
conv = {round(float(r["mu"]), 3): r for r in csv.DictReader(open(HERE / "results" / "scheme.csv")) if r["gauge"].startswith("{xiZ -> 2, xiW -> 2")}
delta = {}
for f, col, key in (("zweak.csv", "fermion", "delta_weak"), ("wreal.csv", "channel", "delta_EW"), ("treal.csv", "channel", "delta_EW")):
    for r in csv.DictReader(open(HERE / "results" / f)):
        delta[(r[col], round(float(r["mu"]), 3))] = float(r[key])


def fe(s2):   # Z -> e+ e-: (3 - beta^2)/2 v^2 + beta^2 a^2 with v = -1/2 + 2 s^2, a = -1/2
    b2 = 1 - 4 * POLE["Me"]**2 / POLE["MZ"]**2
    return (3 - b2) / 2 * (-0.5 + 2 * s2)**2 + b2 * 0.25


def dlnfe(s2, h=1e-6):
    return (math.log(fe(s2 + h)) - math.log(fe(s2 - h))) / (2 * h)


# name, LO key, delta name, mass of the decaying particle
CH = [("Z -> nu nubar", "Z_ve", "nu1", POLE["MZ"]), ("Z -> e+ e- (weak)", "Z_e", "l1", POLE["MZ"]),
      ("W -> e nu", "W_e", "lnu1", POLE["MW"]), ("t -> b W", "t_b", "tbW", POLE["MT"])]
rows = []
print("the G_mu tree couplings: g0^2 = %.8f, G0^2 = %.8f, s0^2 = %.8f (M_W = %.5f, M_Z = %.5f GeV, the pole masses of the SM note)"
      % (g02, G02, s02, mw, mz))
for name, key, dn, M in CH:
    print(name + ":")
    res = []
    for i, mu in enumerate((M, M / 2, 2 * M)):
        p = at(mu)
        gz2, g2, s2 = p["gZ"]**2, p["g"]**2, p["s2"]
        c = conv[round(mu, 3)]
        cw, cz, dwz = float(c["dW_minus_dHat"]), float(c["dZ_minus_dHat"]), float(c["dW_minus_dZ"])
        if key == "Z_ve":
            ratio, C = G02 / gz2, cz
        elif key == "Z_e":
            ratio, C = G02 / gz2 * fe(s02) / fe(s2), cz + dlnfe(s02) * (-(1 - s02) * dwz)
        else:
            ratio, C = g02 / g2, cw
        g0ms = lo[key][i]
        g0os = g0ms * ratio
        d = delta[(dn, round(mu, 3))]
        gms, gos = g0ms * (1 + d), g0os * (1 + d + C)
        res.append((mu, g0ms, g0os, d, C, 1 / ratio - 1, gms, gos))
        print("  mu = %8.3f: LO MS-bar %.6f, LO G_mu %.6f;  delta %+.5f%%, C %+.5f%% (the exact tree ratio - 1: %+.5f%%);"
              "  NLO MS-bar %.6f, NLO G_mu %.6f, MS-bar/G_mu - 1 = %+.2e"
              % (mu, g0ms, g0os, 100 * d, 100 * C, 100 * (1 / ratio - 1), gms, gos, gms / gos - 1))
    r0 = res[0]
    print("  at mu = M: MS-bar/G_mu - 1 = (C_exact - C) + C_exact delta + ... = %+.2e %+.2e = %+.2e  (both O(alpha^2))"
          % (r0[5] - r0[4], r0[5] * r0[3], r0[5] - r0[4] + r0[5] * r0[3]))
    sp = lambda k: max(r[k] for r in res) / min(r[k] for r in res) - 1
    print("  spread over mu: LO MS-bar %.3f%%, NLO MS-bar %.4f%%, NLO G_mu %.4f%%;  delta + C of G_mu %+.5f%% .. %+.5f%%"
          % (100 * sp(1), 100 * sp(6), 100 * sp(7), 100 * min(r[3] + r[4] for r in res), 100 * max(r[3] + r[4] for r in res)))
    for r in res:
        rows.append([name, "%.4f" % r[0], "%.8e" % r[1], "%.8e" % r[2], "%.8e" % r[3], "%.8e" % r[4], "%.8e" % r[5], "%.8e" % r[6],
                     "%.8e" % r[7], "%.3e" % (r[6] / r[7] - 1)])
with open(HERE / "results" / "scheme_compare.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["channel", "mu", "lo_msbar", "lo_gmu", "delta", "C", "exact_tree_ratio_minus_1", "nlo_msbar", "nlo_gmu", "msbar_over_gmu_minus_1"])
    w.writerows(rows)
print("wrote results/scheme_compare.csv")
