"""Stage 2 of the EFT and dark-matter tools (environment.pdf): DirectDM 2.2.3 (Python, two local patches) and 1.2.1
(Mathematica), against own formulas with each version's own nucleon inputs.

  Real-scalar Higgs portal, L = -(lambda_hs/2) S^2 |H|^2: integrating out the Higgs at q^2 = 0 gives
        L_eff = (lambda_hs/(2 m_h^2)) sum_q m_q S^2 qbar q = C sum_q Q_{3,q},  C = lambda_hs/m_h^2,
  with DirectDM's real-scalar operators Q_{3,q} = (m_q/2) S^2 qbar q, Q_5 = (alpha_s/(24 pi)) S^2 G G (1708.02678,
  App. A; they carry 1/2 relative to the complex scalar). A heavy quark gives m_Q Qbar Q -> -(alpha_s/(12 pi)) G G (LO),
  so C_5 = -C per heavy flavour. The nucleon coefficient of O_1 = 1 and the cross section:
        c_1^N = C/(2 m_S) [sum_{q=u,d,s} sigma_q^N + (2/9) m_G],    sigma_SI^N = mu_N^2 (c_1^N)^2/pi,
        = lambda_hs^2 mu_N^2 (sum sigma_q + 2 m_G/9)^2/(4 pi m_h^4 m_S^2)   (the usual f_N m_N = sum sigma_q + 2 m_G/9).
  Dirac DM: vector C_{1,q} (chibar gamma chi)(qbar gamma q) -> c_1^p = 2 C_u + C_d, c_1^n = C_u + 2 C_d;
            axial C_{4,q} (chibar gamma gamma5 chi)(qbar gamma gamma5 q) -> c_4^N = -4 sum_q C_q Delta q^N.
Usage: python3 test_directdm.py     (reads out/ddm_mma.json, written by ddm_mma.wl)
"""
import json
import math
import warnings
from pathlib import Path

warnings.simplefilter("ignore")   # odeint warns about integrations of zero length (mu0 = mu = mb), which return mu0's value
import directdm as ddm                                       # noqa: E402
from directdm.num.num_input import Num_input                # noqa: E402

HERE = Path(__file__).resolve().parent
C0, MDM, QV = 1e-6, 100.0, 1e-3      # coefficient [GeV^-2], DM mass [GeV], |q| [GeV] (q = 0 divides by zero in cNR)
CU, CD, CS = 1e-6, 0.4e-6, -0.2e-6
LAM_HS, MS = 0.1, 100.0               # the Higgs-portal point used again in stages 3 and 4


def row(n, what, result, verdict):
    print(f"{n:2d}  {what:58s} {result:60s} {verdict}")


def main():
    ip = Num_input().input_parameters
    mma = json.load(open(HERE / "out" / "ddm_mma.json"))
    print(f"{'':2s}  {'check':58s} {'result':60s} verdict")
    ownS = lambda sig, mG: C0 / (2 * MDM) * (sig + 2 / 9 * mG)
    py_own = {"p": ownS(ip["sigmaup"] + ip["sigmadp"] + ip["sigmas"], ip["mG"]),
              "n": ownS(ip["sigmaun"] + ip["sigmadn"] + ip["sigmas"], ip["mG"])}
    mma_own = {"p": ownS((17 + 32 + 41.3) * 1e-3, 0.848), "n": ownS((15 + 36 + 41.3) * 1e-3, 0.848)}   # DirectDM/inputs.m

    c3 = ddm.WC_3f({"C63u": C0, "C63d": C0, "C63s": C0, "C65": -3 * C0}, DM_type="R").cNR(MDM, QV)
    d = max(abs(c3["cNR1" + N] / py_own[N] - 1) for N in "pn")
    dm = max(abs(mma["R3"][N] / mma_own[N] - 1) for N in "pn")
    row(1, "real scalar, 3 flavours (2 GeV), c_1^{p,n} vs own", f"Python {d:.1e}, Mathematica {dm:.1e}",
        "agree" if max(d, dm) < 1e-12 else "see text")
    w5 = ddm.WC_5f({"C63u": C0, "C63d": C0, "C63s": C0, "C63c": C0, "C63b": C0, "C65": -C0}, DM_type="R")
    c5 = w5.cNR(MDM, QV, RGE=False)
    d = max(abs(c5["cNR1" + N] / py_own[N] - 1) for N in "pn")
    dm = abs(mma["R5_norun"] / mma_own["p"] - 1)
    row(2, "   5 flavours (M_Z), b and c decoupled at LO, no running", f"Python {d:.1e}, Mathematica {dm:.1e}",
        "agree" if max(d, dm) < 1e-12 else "see text")
    c5r = w5.cNR(MDM, QV, RGE=True)
    d = c5r["cNR1p"] / py_own["p"] - 1
    dm = mma["R5_run"] / mma_own["p"] - 1
    row(3, "   5 flavours with QCD/QED running and thresholds", f"c_1^p shifts: Python {d:+.4f}, Mathematica {dm:+.4f}",
        "RG effect")
    cv = ddm.WC_3f({"C61u": CU, "C61d": CD, "C61s": CS}, DM_type="D").cNR(MDM, QV)
    d = max(abs(cv["cNR1p"] / (2 * CU + CD) - 1), abs(cv["cNR1n"] / (CU + 2 * CD) - 1))
    dm = abs(mma["Dvec_p1"] / (2 * CU + CD) - 1)
    row(4, "Dirac, vector, c_1 = 2 C_u + C_d", f"Python {d:.1e}, Mathematica {dm:.1e} (q^2 = 1e-6 GeV^2)",
        "agree" if max(d, dm) < 1e-8 else "see text")
    ca = ddm.WC_3f({"C64u": CU, "C64d": CD, "C64s": CS}, DM_type="D").cNR(MDM, QV)
    Du, Dd = (ip["DeltauDeltad"] + ip["gA"]) / 2, (ip["DeltauDeltad"] - ip["gA"]) / 2
    own4 = {"p": -4 * (CU * Du + CD * Dd + CS * ip["Deltas"]), "n": -4 * (CU * Dd + CD * Du + CS * ip["Deltas"])}
    d = max(abs(ca["cNR4" + N] / own4[N] - 1) for N in "pn")
    gA = 1.2723
    Dum, Ddm = round((0.521 + gA) / 2, 3), round((0.521 - gA) / 2, 3)          # DirectDM/inputs.m rounds to 0.001
    dm = abs(mma["Dax_p4"] / (-4 * (CU * Dum + CD * Ddm + CS * (-0.031))) - 1)
    row(5, "Dirac, axial, c_4 = -4 sum C_q Delta q", f"Python {d:.1e}, Mathematica {dm:.1e}", "agree" if max(d, dm) < 1e-12 else "see text")
    # the Higgs-portal point for stages 3 and 4
    C = LAM_HS / ip["Mh"] ** 2
    w = ddm.WC_5f({**{f"C63{q}": C for q in "udscb"}, "C65": -C}, DM_type="R")
    mp = ip["mproton"]
    mu = MS * mp / (MS + mp)
    to_cm2 = 0.3893794e-27
    for rge in [False, True]:
        c1 = w.cNR(MS, QV, RGE=rge)["cNR1p"]
        sig = mu ** 2 * c1 ** 2 / math.pi * to_cm2
        own = LAM_HS ** 2 * mu ** 2 * (ip["sigmaup"] + ip["sigmadp"] + ip["sigmas"] + 2 / 9 * ip["mG"]) ** 2 \
            / (4 * math.pi * ip["Mh"] ** 4 * MS ** 2) * to_cm2
        row(6 if not rge else 7, f"sigma_SI^p, lambda_hs = {LAM_HS}, m_S = {MS} GeV, " + ("LO" if not rge else "with running"),
            f"{sig:.5e} cm^2 (own LO {own:.5e}, ratio {sig/own:.5f})", "agree" if not rge and abs(sig / own - 1) < 1e-12 else
            ("RG effect" if rge else "see text"))


if __name__ == "__main__":
    main()
