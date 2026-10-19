"""Step (4a) of the NLO note: the Z partial widths at NLO (weak, QED and QCD) and the Z-pole observables.

  Gamma_f(mu) = Gamma_0,f(mu) [1 + delta_weak,f(mu) + Q_f^2 alpha(mu) K^QED_f/pi + alpha_s(mu) C_F K^QCD_f/pi]   (alpha_s for quarks)
with Gamma_0 at mu = M, M/2, 2M (results/lo_widths.csv, step (1)), delta_weak at the same mu (results/zweak.csv, zweak.wl), and
the K of steps (2), (3): 3/4 for the massless u, d, s, e, the Born-weighted K_V, K_A of results/ir_massive.csv for c, b, mu, tau
(the same K for QED and QCD; their weights are taken at mu = M_Z).  The mixed O(alpha alpha_s) and the higher orders are not
included.  The observables: Gamma_ll (= Gamma_ee), Gamma_inv, Gamma_had, Gamma_Z, R_l = Gamma_had/Gamma_ee, R_b, R_c,
sigma0_had = 12 pi Gamma_ee Gamma_had/(M_Z^2 Gamma_Z^2); the measured values (PDG 2024) are references.  The mu dependence
(mu = M_Z/2, 2 M_Z) of the NLO values against that of the LO values.  Writes results/zweak_widths.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
GEV2NB = 0.3893794e6
CF = 4 / 3
MZ = POLE["MZ"]
lo = {r[0]: [float(x) for x in r[1:]] for r in list(csv.reader(open(HERE / "results" / "lo_widths.csv")))[1:]}   # mu = M, M/2, 2M
dw = {}
for r in csv.DictReader(open(HERE / "results" / "zweak.csv")):
    dw[(r["fermion"], round(float(r["mu"]), 3))] = float(r["delta_weak"])
Kd = {r["channel"]: float(r["K"]) for r in csv.DictReader(open(HERE / "results" / "ir_massive.csv")) if float(r["delta"]) == 0.0}
# zweak name, LO key, T3, Q, mass key, K channel (None: massless, K = 3/4), quark
FERM = [("nu1", "Z_ve", 0.5, 0, "Me", None, False), ("nu2", "Z_ve", 0.5, 0, "Me", None, False), ("nu3", "Z_ve", 0.5, 0, "Me", None, False),
        ("l1", "Z_e", -0.5, -1, "Me", None, False), ("l2", "Z_mu", -0.5, -1, "MMU", "Z_mu", False),
        ("l3", "Z_ta", -0.5, -1, "MTA", "Z_ta", False), ("u1", "Z_u", 0.5, 2 / 3, "MU", None, True),
        ("u2", "Z_c", 0.5, 2 / 3, "MC", "Z_c", True), ("d1", "Z_d", -0.5, -1 / 3, "MD", None, True),
        ("d2", "Z_s", -0.5, -1 / 3, "MS", None, True), ("d3", "Z_b", -0.5, -1 / 3, "MB", "Z_b", True)]
PDG = {"Gamma_ll": (0.083984, 0.000086), "Gamma_inv": (0.4990, 0.0015), "Gamma_had": (1.7444, 0.0020), "Gamma_Z": (2.4955, 0.0023),
       "R_l": (20.767, 0.025), "R_b": (0.21629, 0.00066), "R_c": (0.1721, 0.0030), "sigma0_had": (41.481, 0.033)}
s2Z = at(MZ)["s2"]


def keff(name, t3, q, mk, ch):
    if ch is None:
        return 0.75
    b2 = 1 - 4 * POLE[mk]**2 / MZ**2
    v, a = t3 - 2 * q * s2Z, t3
    wv, wa = v**2 * (3 - b2) / 2, a**2 * b2
    return (wv * Kd[ch + "_V"] + wa * Kd[ch + "_A"]) / (wv + wa)


def widths(imu, with_weak=True, with_qcdqed=True):
    mu = (MZ, MZ / 2, 2 * MZ)[imu]
    p = at(mu)
    out = {}
    for name, key, t3, q, mk, ch, quark in FERM:
        g0 = lo[key][imu]
        k = keff(name, t3, q, mk, ch)
        corr = 0.0
        if with_weak:
            corr += dw[(name, round(mu, 3))]
        if with_qcdqed:
            corr += q**2 * p["alpha"] * k / math.pi + (p["alphas"] * CF * k / math.pi if quark else 0.0)
        out[name] = g0 * (1 + corr)
    return out


def observables(w):
    had = sum(w[n] for n in ("u1", "u2", "d1", "d2", "d3"))
    inv = w["nu1"] + w["nu2"] + w["nu3"]
    gz = had + inv + w["l1"] + w["l2"] + w["l3"]
    return {"Gamma_ll": w["l1"], "Gamma_inv": inv, "Gamma_had": had, "Gamma_Z": gz, "R_l": had / w["l1"], "R_b": w["d3"] / had,
            "R_c": w["u2"] / had, "sigma0_had": 12 * math.pi * w["l1"] * had / (MZ**2 * gz**2) * GEV2NB}


def main():
    obs_lo = [observables(widths(i, False, False)) for i in range(3)]
    obs_qq = observables(widths(0, False, True))
    obs = [observables(widths(i)) for i in range(3)]
    print("delta_weak at mu = M_Z: " + ", ".join("%s %+.5f%%" % (n, 100 * dw[(n, round(MZ, 3))]) for n, *_ in FERM))
    print("%-11s %-22s %-22s %-22s %-18s  %s" % ("quantity", "LO", "LO + QED, QCD", "NLO (+ weak)", "measured", "mu = M/2, 2M: LO; NLO"))
    rows = []
    for k in PDG:
        m, e = PDG[k]
        a, b, c = obs_lo[0][k], obs_qq[k], obs[0][k]
        dlo = [100 * (obs_lo[i][k] / a - 1) for i in (1, 2)]
        dnl = [100 * (obs[i][k] / c - 1) for i in (1, 2)]
        print("%-11s %.6f (%+.2f%%)  %.6f (%+.2f%%)  %.6f (%+.2f%%)  %.5f +- %.5f   %+.3f%% %+.3f%%;  %+.3f%% %+.3f%%"
              % (k, a, 100 * (a / m - 1), b, 100 * (b / m - 1), c, 100 * (c / m - 1), m, e, *dlo, *dnl))
        rows.append([k, "%.8e" % a, "%.8e" % b, "%.8e" % c, m, e, "%.4f" % dlo[0], "%.4f" % dlo[1], "%.4f" % dnl[0], "%.4f" % dnl[1]])
        if k in ("Gamma_Z", "R_b", "Gamma_inv", "sigma0_had", "R_l"):
            print("            NLO - measured = %+.2f sigma" % ((c - m) / e))
    # the mu dependence of the electroweak part alone (LO + weak, no QED, QCD factors): what the weak correction is to cancel
    obs_ew = [observables(widths(i, True, False)) for i in range(3)]
    print("mu = M/2, 2M with LO + weak only (the alpha_s(mu) of the QCD factor left out): " + ";  ".join(
        "%s %+.3f%% %+.3f%%" % (k, 100 * (obs_ew[1][k] / obs_ew[0][k] - 1), 100 * (obs_ew[2][k] / obs_ew[0][k] - 1))
        for k in ("Gamma_ll", "Gamma_inv", "Gamma_had", "Gamma_Z")))
    with open(HERE / "results" / "zweak_widths.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "lo", "lo_qed_qcd", "nlo", "measured", "error", "lo_mu_half_pct", "lo_mu_2_pct", "nlo_mu_half_pct",
                    "nlo_mu_2_pct"])
        w.writerows(rows)
    print("wrote results/zweak_widths.csv")


if __name__ == "__main__":
    main()
