"""Stage 4 of the EFT and dark-matter tools (environment.pdf): micrOMEGAs 7.1.10 on the same model as MadDM in stage 3
(FeynRules SM + real scalar DM, m_S = 100 GeV, lambda_hs = 0.1), against own formulas with micrOMEGAs' inputs, and
micrOMEGAs' own model SingletDM at the same point as an independent implementation.

  (a) <sigma v>(x) for x = 15 .. 30: the own Gondolo-Gelmini average of test_maddm.py (s-channel Higgs, tree level),
      with the Higgs width micrOMEGAs computes (!WH);
  (b) the scalar nucleon amplitude (Dirac-normalized, sigma_SI = 4 mu^2 A^2/pi):
        A^N = lambda M_N/(4 m_h^2 m_S) [sum_{u,d,s} f_Tq^N + (2/27) f_TG^N sum_{Q=c,b,t} (1 + (11/4 - 16/9) alpha_s(m_Q)/pi)],
      with M_N = 0.939, alpha_s(m_c) = 0.39, alpha_s(m_b) = 0.22, alpha_s(m_t) from micrOMEGAs (sources/directDet.c), and
      its default f_Tq (the same numbers as MadDM's); without the QCD factor this is the LO formula of stages 2 and 3;
  (c) Omega h^2 from dY/ds3 = M_Pl (2 pi^2 h_eff/45)^{2/3} <sigma v> (Y^2 - Y_eq^2)/sqrt(8 pi/3 pi^2/30 g_eff),
      s3 = T (2 pi^2 h_eff/45)^{1/3}, Y_eq = 45/(4 pi^4) x^2 K_2(x)/h_eff, with micrOMEGAs' table Data/hgEff/DHS.thg
      (Drees, Hajkarim, Schmitz), M_Pl = 1.22091e19 GeV, Omega h^2 = 2.742e8 m Y_inf (sources/omega.c), integrated to
      x -> infinity (MadDM stops at x_end = 1000 of its maddm_card, which for s-wave annihilation leaves Omega about
      x_f/1000 = 2% too large; test_maddm.py follows MadDM).
Usage: python3 test_micromegas.py      (reads out/micromegas_fr.txt, out/micromegas_native.txt, out/maddm_hp)
"""
import math
import re
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import kve

import test_maddm as tm

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
PB = 3.8937966e8          # GeV^-2 -> pb, as micrOMEGAs
MPL, OMEGA_C = 1.22091e19, 2.742e8
MN = 0.939


def parse(path):
    txt = open(path).read()
    d = {"vSigma": {float(a): float(b) for a, b in re.findall(r"vSigma\s+(\S+)\s+(\S+)", txt)}}
    m = re.search(r"Omega\s+(\S+)\s+Xf\s+(\S+)", txt)
    d["Omega"], d["Xf"] = float(m.group(1)), float(m.group(2))
    m = re.search(r"A0\s+(\S+)\s+(\S+)", txt)
    d["A0"] = (float(m.group(1)), float(m.group(2)))
    m = re.search(r"WH\s+([0-9.eE+-]+)", txt)
    d["WH"] = float(m.group(1)) if m else None
    m = re.search(r"alphaQCD\(MT\)\s+(\S+)", txt)
    d["asMT"] = float(m.group(1)) if m else None
    m = re.search(r"FF p (\S+) (\S+) (\S+) n (\S+) (\S+) (\S+)", txt)
    if m:
        v = [float(x) for x in m.groups()]
        d["FF"] = {"p": dict(zip("uds", v[:3])), "n": dict(zip("uds", v[3:]))}
    d["channels"] = {b: float(a) for a, b in re.findall(r"^\s+([0-9.]+)% \S+ \S+ ->(.+?)\s*$", txt, re.M)}
    return d


def dhs_tables():
    t = np.loadtxt(Path.home() / "hep/micromegas_7.1.10/Data/hgEff/DHS.thg", comments="#")
    t = t[np.argsort(t[:, 0])]
    return t[:, 0], t[:, 1], t[:, 2]          # T, heff, geff


def interp3(T, xs, ys):
    """local cubic interpolation through the 4 nearest points (as micrOMEGAs' polint3)"""
    i = int(np.clip(np.searchsorted(xs, T) - 2, 0, len(xs) - 4))
    xx, yy = xs[i:i + 4], ys[i:i + 4]
    return sum(yy[k] * np.prod([(T - xx[j]) / (xx[k] - xx[j]) for j in range(4) if j != k]) for k in range(4))


def relic_dhs(model):
    m = model.m
    Ts, he, ge = dhs_tables()
    heff = lambda T: interp3(T, Ts, he)
    geff = lambda T: interp3(T, Ts, ge)
    xgrid = np.concatenate([np.linspace(3, 60, 115), np.geomspace(60.5, 1000, 60)])
    svgrid = np.array([model.taacs(x) for x in xgrid])
    svi = lambda x: math.exp(np.interp(x, xgrid, np.log(svgrid)))

    def yeq(T):
        x = m / T
        return 45 / (4 * math.pi ** 4) * x * x * kve(2, x) * math.exp(-x) / heff(T)

    def rhs(lnT, y):                  # dY/dlnT = dY/ds3 * ds3/dlnT, s3 = T (2 pi^2 heff/45)^(1/3)
        T = math.exp(lnT)
        h, g = heff(T), geff(T)
        dlnh = (math.log(heff(T * 1.001)) - math.log(heff(T / 1.001))) / (2 * math.log(1.001))
        ds3 = T * (2 * math.pi ** 2 * h / 45) ** (1 / 3) * (1 + dlnh / 3)
        dyds3 = MPL * (2 * math.pi ** 2 * h / 45) ** (2 / 3) / math.sqrt(8 * math.pi / 3 * math.pi ** 2 / 30 * g) \
            * svi(m / T) * (y[0] ** 2 - yeq(T) ** 2)
        return [dyds3 * ds3]
    # to x = 1000 numerically, then the rest of the annihilation (Y >> Y_eq) analytically, as micrOMEGAs (iColl):
    # 1/Y_inf = 1/Y(x_e) + int_{T_0}^{T_e} dT (ds3/dT) dY/ds3 / Y^2, with h_eff, g_eff constant below the table (T < T_min)
    sol = solve_ivp(rhs, (math.log(m / 3), math.log(m / 1000)), [yeq(m / 3)], method="Radau", rtol=1e-10, atol=1e-25)
    ye = sol.y[0, -1]
    tail = solve_ivp(lambda lnT, y: [-rhs(lnT, [1.0])[0]] if math.exp(lnT) > Ts[0] else
                     [-rhs(math.log(Ts[0]), [1.0])[0] * math.exp(2 * (lnT - math.log(Ts[0])))],
                     (math.log(m / 1000), math.log(m / 1e7)), [0.0], rtol=1e-10, atol=1e-30)
    return OMEGA_C * m / (1 / ye + tail.y[0, -1])


def row(n, what, result, verdict):
    print(f"{n:2d}  {what:56s} {result:64s} {verdict}")


def main():
    fr = parse(OUT / "micromegas_fr.txt")
    nat = parse(OUT / "micromegas_native.txt")
    card = tm.read_card(OUT / "maddm_hp" / "Cards" / "param_card.dat")
    md = tm.Model(card)
    md.WH = fr["WH"]
    print(f"{'':2s}  {'check':56s} {'result':64s} verdict")
    d = max(abs(fr["vSigma"][x] / PB / md.taacs(x) - 1) for x in fr["vSigma"])
    row(1, "<sigma v>(x = 15, 20, 25, 30) vs own", f"max rel. diff {d:.1e} (own at x = 20: {md.taacs(20.0)*PB:.5f} pb)",
        "agree" if d < 1e-3 else "see text")
    FF = fr["FF"]
    for N, k in [("p", 0), ("n", 1)]:
        fTG = 1 - sum(FF[N].values())
        qcd = sum(1 + (11 / 4 - 16 / 9) * a / math.pi for a in (0.39, 0.22, fr["asMT"]))
        own = md.lam * MN / (4 * md.MH ** 2 * md.m) * (sum(FF[N].values()) + 2 / 27 * fTG * qcd)
        lo = md.lam * MN / (4 * md.MH ** 2 * md.m) * (sum(FF[N].values()) + 2 / 9 * fTG)
        if N == "p":
            dp, ratio = fr["A0"][k] / own - 1, fr["A0"][k] / lo
        else:
            dn = fr["A0"][k] / own - 1
    row(2, "scalar nucleon amplitudes A^{p,n} vs own (its QCD factor)", f"p {dp:+.1e}, n {dn:+.1e}; vs LO: x {ratio:.4f}",
        "agree" if max(abs(dp), abs(dn)) < 1e-6 else "see text")
    oh2 = relic_dhs(md)
    d = fr["Omega"] / oh2 - 1
    row(3, "Omega h^2 vs own Boltzmann solution (DHS g_eff, h_eff)", f"micrOMEGAs {fr['Omega']:.6f}, own {oh2:.6f} ({d:+.1e})",
        "agree" if abs(d) < 3e-3 else "see text")
    out2 = tm.maddm_out(OUT / "maddm_hp", "run_02")
    oh2_m = tm.relic(md, tm.gstar_maddm(OUT / "maddm_hp"))
    row(4, "   MadDM (eps_ode 1e-4) vs micrOMEGAs: g_* tables, x_end",
        f"MadDM/micrO {out2['Omegah^2'][0]/fr['Omega']:.4f}; own(MadDM g*)/own(DHS) {oh2_m/oh2:.4f}", "explained" if
        abs(out2['Omegah^2'][0] / fr['Omega'] / (oh2_m / oh2) - 1) < 5e-3 else "see text")
    mad_sig = 4 * (md.m * 0.938 / (md.m + 0.938)) ** 2 / math.pi
    row(5, "micrOMEGAs' own SingletDM (laSH = 0.05) vs the FeynRules model",
        f"Omega h^2 {nat['Omega']:.6f} ({nat['Omega']/fr['Omega']-1:+.3f}), A^p {nat['A0'][0]:.4e} ({nat['A0'][0]/fr['A0'][0]-1:+.3f})",
        "independent model")
    ch = ", ".join(f"{k} {v:.2f} %" for k, v in list(fr["channels"].items())[:3])
    print(f"    (micrOMEGAs channels of 1/Omega, FeynRules model: {ch}; x_f = {fr['Xf']:.2f})")


if __name__ == "__main__":
    main()
