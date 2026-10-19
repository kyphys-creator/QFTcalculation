"""Step (8) of the NLO note: the NLO predictions with their uncertainties against the measured values.

The predictions of steps (4a)-(6) at mu = M (results/zweak_widths.csv, zpole.csv, wweak_widths.csv, tweak_widths.csv,
mw_summary.csv) and three estimates of the terms beyond NLO, added in quadrature:
  d_mu      half the spread of the NLO value over mu = M/2, M, 2M (the couplings and alpha_s run to mu);
  d_scheme  the same one-loop prediction in another scheme: the on-shell G_mu scheme of step (7) (results/scheme.csv: the tree
            in G_F, M_W, M_Z plus the one-loop conversion C) for the widths and ratios; for sin^2 theta_eff and the asymmetries the
            couplings of the SM note's alpha scheme (step (5)); for M_W the largest of the forms equivalent at one loop and the SM
            note's value (step (6));
  d_HO      a known higher order not probed by mu: for M_W the O(alpha alpha_s) correction to Delta rho (step (6); the
            Djouadi-Verzegnassi coefficient, a reference).  For sin^2 theta_eff it is the size of the alpha-scheme difference and is
            not added again.
The measured values (PDG 2024 for the Z, LEP and SLD for the asymmetries, the PDG 2026 release for the W and the top width) are
references; the pulls with the experimental error alone and with experiment and theory in quadrature.  Writes results/summary.csv.
"""
import csv
import math
from pathlib import Path

import wweak_widths as ww
import zweak_widths as zw
from nlo_inputs import POLE, at

HERE = Path(__file__).resolve().parent
R = HERE / "results"
CF = 4 / 3
# the G_mu tree couplings (the pole masses of the SM note's fit, as scheme_compare.py)
GF = 1.1663788e-5
mwp, mzp = 80.3692 / math.sqrt(1 + (2.085 / 80.3692)**2), 91.188 / math.sqrt(1 + (2.4955 / 91.188)**2)
g02, G02, s02 = 4 * math.sqrt(2) * GF * mwp**2, 4 * math.sqrt(2) * GF * mzp**2, 1 - mwp**2 / mzp**2
conv = {round(float(r["mu"]), 3): r for r in csv.DictReader(open(R / "scheme.csv")) if r["gauge"].startswith("{xiZ -> 2, xiW -> 2")}


def F(t3, q, s2, b2):   # the coupling factor of Gamma_0(Z -> f fbar)
    return (3 - b2) / 2 * (t3 - 2 * q * s2)**2 + b2 * t3**2


def z_gmu():
    MZ = POLE["MZ"]
    p, c = at(MZ), conv[round(MZ, 3)]
    cz, dwz = float(c["dZ_minus_dHat"]), float(c["dW_minus_dZ"])
    out = {}
    for name, key, t3, q, mk, ch, quark in zw.FERM:
        b2 = 1.0 if q == 0 else 1 - 4 * POLE[mk]**2 / MZ**2
        h = 1e-6
        dlnF = (math.log(F(t3, q, s02 + h, b2)) - math.log(F(t3, q, s02 - h, b2))) / (2 * h)
        ratio = G02 / p["gZ"]**2 * F(t3, q, s02, b2) / F(t3, q, p["s2"], b2)
        C = cz + dlnF * (-(1 - s02) * dwz)
        k = zw.keff(name, t3, q, mk, ch)
        corr = zw.dw[(name, round(MZ, 3))] + q**2 * p["alpha"] * k / math.pi + (p["alphas"] * CF * k / math.pi if quark else 0.0)
        out[name] = zw.lo[key][0] * ratio * (1 + corr + C)
    return zw.observables(out)


def w_gmu():
    MW = POLE["MW"]
    p, c = at(MW), conv[round(MW, 3)]
    C = float(c["dW_minus_dHat"])
    out = {n: ww.lo[key][0] * g02 / p["g"]**2 * (1 + ww.dew[(n, round(MW, 3))] + (p["alphas"] / math.pi if quark else 0.0) + C)
           for n, key, quark in ww.CHANS}
    return ww.observables(out)


def t_both():
    MT = POLE["MT"]
    p, C = at(MT), float(conv[round(MT, 3)]["dW_minus_dHat"])
    K = next(float(r["K"]) for r in csv.DictReader(open(R / "ir_massive.csv")) if r["channel"] == "t_bW" and float(r["delta"]) == 0)
    d = {r["channel"]: float(r["delta_EW"]) for r in csv.DictReader(open(R / "treal.csv")) if abs(float(r["mu"]) - MT) < 1e-6}
    qcd = p["alphas"] * CF * K / math.pi
    ms = sum(zw.lo[k][0] * (1 + d[n] + qcd) for n, k in (("tdW", "t_d"), ("tsW", "t_s"), ("tbW", "t_b")))
    gm = sum(zw.lo[k][0] * g02 / p["g"]**2 * (1 + d[n] + qcd + C) for n, k in (("tdW", "t_d"), ("tsW", "t_s"), ("tbW", "t_b")))
    return ms, gm


def dmu(row, val):   # half the spread over mu = M/2, M, 2M from the percentage columns
    x = [0.0, float(row["nlo_mu_half_pct"]), float(row["nlo_mu_2_pct"])]
    return (max(x) - min(x)) / 200 * abs(val)


rows = []


def add(name, val, d_mu, d_sch, d_ho, meas, err, unit=""):
    th = math.sqrt(d_mu**2 + d_sch**2 + d_ho**2)
    pe = (val - meas) / err if err else float("nan")
    pt = (val - meas) / math.sqrt(err**2 + th**2) if err else float("nan")
    rows.append([name, val, d_mu, d_sch, d_ho, th, meas, err, pe, pt, unit])


zr = {r["quantity"]: r for r in csv.DictReader(open(R / "zweak_widths.csv"))}
zg = z_gmu()
for k in ("Gamma_ll", "Gamma_inv", "Gamma_had", "Gamma_Z", "R_l", "R_b", "R_c", "sigma0_had"):
    v = float(zr[k]["nlo"])
    add(k, v, dmu(zr[k], v), abs(v - zg[k]), 0.0, float(zr[k]["measured"]), float(zr[k]["error"]), "nb" if k == "sigma0_had" else "GeV" if k[0] == "G" else "")
pr = {r["quantity"]: r for r in csv.DictReader(open(R / "zpole.csv"))}
for k in ("s2eff_lept", "A_l", "A_b", "A_c", "AFB0_l", "AFB0_b", "AFB0_c"):
    v = float(pr[k]["nlo"])
    d_mu = (max(v, float(pr[k]["nlo_mu_half"]), float(pr[k]["nlo_mu_2"])) - min(v, float(pr[k]["nlo_mu_half"]), float(pr[k]["nlo_mu_2"]))) / 2
    add(k, v, d_mu, abs(float(pr[k]["nlo_alpha_scheme"]) - v), 0.0, float(pr[k]["measured"]), float(pr[k]["error"]))
wr = {r["quantity"]: r for r in csv.DictReader(open(R / "wweak_widths.csv"))}
wg = w_gmu()
for k in ("Gamma_W", "BR_e", "BR_mu", "BR_tau", "BR_had"):
    v = float(wr[k]["nlo"])
    add(k, v, dmu(wr[k], v), abs(v - wg[k]), 0.0, float(wr[k]["measured"]), float(wr[k]["error"]), "GeV" if k == "Gamma_W" else "")
tr = {r["quantity"]: r for r in csv.DictReader(open(R / "tweak_widths.csv"))}
tms, tgm = t_both()
v = float(tr["Gamma_t"]["nlo"])
add("Gamma_t", v, dmu(tr["Gamma_t"], v), abs(tms - tgm), 0.0, 1.42, 0.15 if v < 1.42 else 0.19, "GeV")
ms = {r["quantity"]: float(r["value"]) for r in csv.DictReader(open(R / "mw_summary.csv"))}
mw_bw = ms["MW_BW_mu_Mt"]
trunc = max(abs(ms[k] - ms["MW_pole_mu_Mt"]) for k in ("MW_pole_sqrt_form", "MW_pole_inverse_sqrt_form", "MW_pole_SM_note"))
add("M_W (Breit-Wigner)", mw_bw, ms["mu_spread_MeV"] / 2000, trunc, abs(ms["dMW_alpha_alphas_MeV"]) / 1000, 80.3692, 0.0133, "GeV")
add("M_W (PDG 2026)", mw_bw, ms["mu_spread_MeV"] / 2000, trunc, abs(ms["dMW_alpha_alphas_MeV"]) / 1000, 80.3625, 0.0077, "GeV")

print("%-19s %-12s %-30s %-11s %-19s %s" % ("quantity", "NLO", "d_mu, d_scheme, d_HO -> theory", "", "measured", "pull: exp; exp + th"))
for name, val, a, b, c, th, m, e, pe, pt, u in rows:
    print("%-19s %-12.6g %-9.2g %-9.2g %-9.2g -> %-9.2g %-11.6g +- %-9.2g %+6.2f; %+6.2f" % (name, val, a, b, c, th, m, e, pe, pt))
with open(R / "summary.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "nlo", "d_mu", "d_scheme", "d_HO", "d_theory", "measured", "error", "pull_exp", "pull_exp_theory", "unit"])
    for r in rows:
        w.writerow([r[0]] + ["%.8g" % x for x in r[1:10]] + [r[10]])
print("wrote results/summary.csv")
