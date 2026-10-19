"""Step (4b) of the NLO note: the W partial widths at NLO (electroweak and QCD) and the branching ratios.

  Gamma_f(mu) = Gamma_0,f(mu) [1 + delta_EW,f(mu) + alpha_s(mu)/pi]   (the QCD term for the quarks only)
with Gamma_0 at mu = M, M/2, 2M (results/lo_widths.csv, step (1)) and delta_EW at the same mu (results/wreal.csv: virtual + soft
+ hard photon, the photon inclusive, extrapolated to delta -> 0; wweak.wl, wreal.wl).  The QCD factor is that of massless
quarks, C_F (3/4) alpha_s/pi = alpha_s/pi (step (2)); the quark masses in it (m_c, m_b over M_W) are not included, nor the mixed
O(alpha alpha_s) and the higher orders.  The observables: the three leptonic widths, Gamma_had, Gamma_W, the branching ratios
and the ratios of the leptonic widths (lepton universality).  The measured values (PDG 2026 release) are references.
The mu dependence (mu = M_W/2, 2 M_W) of the NLO values against that of the LO values.  Writes results/wweak_widths.csv.
"""
import csv
import math
from pathlib import Path

from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
MW = POLE["MW"]
lo = {r[0]: [float(x) for x in r[1:]] for r in list(csv.reader(open(HERE / "results" / "lo_widths.csv")))[1:]}   # mu = M, M/2, 2M
dew = {(r["channel"], round(float(r["mu"]), 3)): float(r["delta_EW"]) for r in csv.DictReader(open(HERE / "results" / "wreal.csv"))}
# wreal name, LO key, quark
CHANS = [("lnu1", "W_e", False), ("lnu2", "W_mu", False), ("lnu3", "W_ta", False), ("ud", "W_ud", True), ("us", "W_us", True),
         ("ub", "W_ub", True), ("cd", "W_cd", True), ("cs", "W_cs", True), ("cb", "W_cb", True)]
PDG = {"Gamma_W": (2.14, 0.05), "BR_e": (0.1071, 0.0016), "BR_mu": (0.1063, 0.0015), "BR_tau": (0.1138, 0.0021),
       "BR_had": (0.6741, 0.0027)}
ORDER = ["Gamma_e", "Gamma_mu", "Gamma_tau", "Gamma_had", "Gamma_W", "BR_e", "BR_mu", "BR_tau", "BR_had", "mu/e", "tau/e", "tau/mu"]


def widths(imu, with_ew=True, with_qcd=True):
    mu = (MW, MW / 2, 2 * MW)[imu]
    a_s = at(mu)["alphas"]
    out = {}
    for name, key, quark in CHANS:
        corr = (dew[(name, round(mu, 3))] if with_ew else 0.0) + (a_s / math.pi if (with_qcd and quark) else 0.0)
        out[name] = lo[key][imu] * (1 + corr)
    return out


def observables(w):
    had = sum(w[n] for n, _, q in CHANS if q)
    lep = [w["lnu1"], w["lnu2"], w["lnu3"]]
    gw = had + sum(lep)
    return {"Gamma_e": lep[0], "Gamma_mu": lep[1], "Gamma_tau": lep[2], "Gamma_had": had, "Gamma_W": gw, "BR_e": lep[0] / gw,
            "BR_mu": lep[1] / gw, "BR_tau": lep[2] / gw, "BR_had": had / gw, "mu/e": lep[1] / lep[0], "tau/e": lep[2] / lep[0],
            "tau/mu": lep[2] / lep[1]}


def main():
    obs_lo = [observables(widths(i, False, False)) for i in range(3)]
    obs_q = observables(widths(0, False, True))
    obs = [observables(widths(i)) for i in range(3)]
    print("delta_EW at mu = M_W: " + ", ".join("%s %+.5f%%" % (n, 100 * dew[(n, round(MW, 3))]) for n, *_ in CHANS))
    print("  e minus mu (the lepton mass drops out, KLN): %.1e;  tau minus mu: %.1e"
          % (dew[("lnu1", round(MW, 3))] - dew[("lnu2", round(MW, 3))], dew[("lnu3", round(MW, 3))] - dew[("lnu2", round(MW, 3))]))
    print("%-10s %-22s %-22s %-22s %-18s  %s" % ("quantity", "LO", "LO + QCD", "NLO (+ EW)", "measured", "mu = M/2, 2M: LO; NLO"))
    rows = []
    for k in ORDER:
        a, b, c = obs_lo[0][k], obs_q[k], obs[0][k]
        m, e = PDG.get(k, (float("nan"), float("nan")))
        dlo = [100 * (obs_lo[i][k] / a - 1) for i in (1, 2)]
        dnl = [100 * (obs[i][k] / c - 1) for i in (1, 2)]
        meas = "%.4f +- %.4f" % (m, e) if k in PDG else ""
        print("%-10s %.6f (%+.2f%%)  %.6f (%+.2f%%)  %.6f (%+.2f%%)  %-18s  %+.3f%% %+.3f%%;  %+.3f%% %+.3f%%"
              % (k, a, 100 * (a / c - 1), b, 100 * (b / c - 1), c, 0.0, meas, *dlo, *dnl))
        rows.append([k, "%.8e" % a, "%.8e" % b, "%.8e" % c, m if k in PDG else "", e if k in PDG else "", "%.4f" % dlo[0], "%.4f" % dlo[1],
                     "%.4f" % dnl[0], "%.4f" % dnl[1]])
        if k in PDG:
            print("           NLO - measured = %+.2f%% = %+.2f sigma" % (100 * (c / m - 1), (c - m) / e))
    print("(the percentages after LO and LO + QCD: relative to the NLO value)")
    print("BR(W -> l nu) with lepton universality (PDG 2026: 0.1086 +- 0.0009): NLO BR_e %.5f (%+.2f sigma)"
          % (obs[0]["BR_e"], (obs[0]["BR_e"] - 0.1086) / 0.0009))
    obs_ew = [observables(widths(i, True, False)) for i in range(3)]
    print("mu = M/2, 2M with LO + EW only (no QCD factor): " + ";  ".join(
        "%s %+.3f%% %+.3f%%" % (k, 100 * (obs_ew[1][k] / obs_ew[0][k] - 1), 100 * (obs_ew[2][k] / obs_ew[0][k] - 1))
        for k in ("Gamma_e", "Gamma_had", "Gamma_W", "BR_e")))
    with open(HERE / "results" / "wweak_widths.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["quantity", "lo", "lo_qcd", "nlo", "measured", "error", "lo_mu_half_pct", "lo_mu_2_pct", "nlo_mu_half_pct",
                    "nlo_mu_2_pct"])
        w.writerows(rows)
    print("wrote results/wweak_widths.csv")


if __name__ == "__main__":
    main()
