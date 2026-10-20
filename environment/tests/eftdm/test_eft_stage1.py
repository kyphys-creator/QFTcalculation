"""Stage 1 of the EFT and dark-matter tools (environment.pdf): wilson (master d21596fa, 2.5.2 + fixes) and DsixTools 2.1.

  (B) SMEFT running in a pure-QCD toy (g, g', lambda, m^2 and the Yukawas set to 1e-6 or less), 1 TeV -> M_Z, one loop:
        a = g_s^2,  a(mu) = a0/(1 + 2 b0 a0 ln(mu/Lambda)/(16 pi^2)),  b0 = 11 - 4 n_g/3 = 7,
        the quark bilinears run with gamma_S = -6 C_F = -8, gamma_T = 2 C_F = 8/3 (dC/dln mu = gamma g_s^2 C/(16 pi^2)):
        C_ledq, C_lequ1 ~ a^{4/7},  C_lequ3 ~ a^{-4/21},  C_lq1 (vector currents) constant,  C_HG/g_s^2 constant;
  (A) SMEFT running with the full one-loop RGEs and the same SM input at 1 TeV in both tools (DsixTools' sample couplings,
      with the Yukawa matrices replaced by their singular values, so that no flavour rotation is involved), 13 Warsaw
      coefficients -> all coefficients at M_Z, compared through DsixTools' WCxf export; not an independent check
      (wilson's SMEFT RGEs were ported from DsixTools);
  (C) tree-level SMEFT -> WET matching at M_Z (no running), down-quark basis, so no CKM factors:
        V^LL_ed = C_lq1 + C_lq3,  V^LL_nud = C_lq1 - C_lq3,  S^RL_ed = C_ledq  (JMS basis);
  (D) WET running M_Z -> 5 GeV (5 flavours), one-loop ADMs:
        without QED  S ~ alpha_s^{12/23}, T ~ alpha_s^{-4/23}, V^LL_ed constant, with each tool's own alpha_s(mu);
        with QED     wilson against DsixTools at the same alpha_s(M_Z) = 0.1181 and alpha_e(M_Z) of DsixTools, with
                     wilson's alpha_s taken at one loop (wilson treats QED at first order with a fixed alpha_e,
                     DsixTools integrates the RGEs with running alpha_s and alpha_e; these approximations differ at the
                     1e-3 level of the coefficients).
The DsixTools numbers come from stage1_dsixtools.wl (out/dsix_*.json); `prepare` writes its input out/stage1_in.json.
Usage: python3 test_eft_stage1.py [prepare | check]
"""
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np

from wilson import wcxf
from wilson.run.smeft import SMEFT
from wilson.run.wet.classes import WETrunner
from wilson.util import smeftutil

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LAMBDA, MZ, MLOW = 1000.0, 91.1876, 5.0
TIGHT = dict(rtol=1e-11, atol=1e-22)          # solve_ivp tolerances for wilson; the defaults are rtol 1e-3, atol 1e-6

# (B) the pure-QCD toy: tiny but nonzero couplings (zero Yukawas make DsixTools' flavour rotation undefined, zero m^2
#     and lambda give 0^-2 in its RGEs)
TOY_SM = {"g": 1e-6, "gp": 1e-6, "gs": 1.0, "Lambda": 1e-12, "m2": 1e-12, "y": 1e-6}
TOY_WC = {"ledq_1111": 1e-6, "lequ1_1111": 1e-6, "lequ3_1111": 1e-6, "lq1_1111": 1e-6, "phiG": 1e-6}
# (A) DsixTools' sample SM couplings (IO/SMInput.dat) at the UV scale; Yukawas: singular values of its matrices
SM_A = {"g": 0.629787, "gp": 0.345367, "gs": 1.218232, "Lambda": 0.257736, "m2": 7812.5}
WC_A = {"phiG": 1.0e-6, "phiBox": -0.5e-6, "phiD": 0.3e-6, "uG_33": (0.4 + 0.1j) * 1e-6, "phil1_12": (0.5 - 0.2j) * 1e-6,
        "lq1_1123": 0.7e-6, "lq3_2223": -0.4e-6, "ledq_1111": (0.2 + 0.3j) * 1e-6, "lequ1_2233": 0.6e-6,
        "lequ3_2233": -0.2e-6, "qq1_1133": 0.3e-6, "dd_1112": (0.1 + 0.05j) * 1e-6, "eu_1133": -0.25e-6}
# (C) tree matching
A_C, B_C, C_C = 1.0e-6, 0.3e-6, (0.5 - 0.2j) * 1e-6
WC_C = {"lq1_1111": A_C, "lq3_1111": B_C, "lq1_1123": A_C, "lq3_1123": -B_C, "ledq_1111": C_C}
# (D) WET running
WC_D = {"SedRL_1111": 1e-6, "TeuRR_1111": 1e-6, "SeuRR_1111": 1e-6, "VedLL_1111": 1e-6}
ALPHAS_D = 0.1181                                   # DsixTools' default alpha_s(M_Z)


def yukawas_A():
    """singular values of the Yukawa matrices of DsixTools' IO/SMInput.dat (Gamma_u has CKM mixing and a phase)"""
    sm = {}
    block = None
    for line in open(Path.home() / "Library/Wolfram/Applications/DsixTools/IO/SMInput.dat"):
        t = line.split("#")[0].split()
        if not t:
            continue
        if t[0].lower() == "block":
            block = t[1]
            sm[block] = {}
            continue
        sm[block][tuple(int(x) for x in t[:-1])] = float(t[-1])
    out = {}
    for k, (re_, im_) in {"Gu": ("GU", "IMGU"), "Gd": ("GD", "IMGD"), "Ge": ("GE", "IMGE")}.items():
        m = np.zeros((3, 3), complex)
        for (i, j), v in sm[re_].items():
            m[i - 1, j - 1] += v
        for (i, j), v in sm.get(im_, {}).items():
            m[i - 1, j - 1] += 1j * v
        out[k] = np.sort(np.linalg.svd(m, compute_uv=False))
    return out


def dsix_name(key):
    """wilson's internal name -> DsixTools' symbol (phil1 -> CHl1, phiBox -> CHbox, lq1 -> Clq1, ...)"""
    return "C" + key.replace("phi", "H").replace("Box", "box")


def sym_entries(wcdict):
    """the WCxf values as all entries (redundant ones included) of wilson's symmetrized arrays, for DsixTools' NewInput:
    DsixTools averages each array with its symmetry partners, so it must be given every redundant entry"""
    C = smeftutil.wcxf2arrays_symmetrized(wcdict)
    ent = []
    for k, v in C.items():
        if k in smeftutil.dim4_keys:
            continue
        a = np.atleast_1d(np.asarray(v, dtype=complex))
        for idx in zip(*np.nonzero(np.abs(a) > 0)):
            val = complex(a[idx])
            ent.append([dsix_name(k), [int(i) + 1 for i in idx] if np.ndim(v) else [], val.real, val.imag])
    return ent


def sm_dict(sm, y):
    d = {k: sm[k] for k in ["g", "gp", "gs", "Lambda", "m2"]}
    for k in ["Gu", "Gd", "Ge"]:
        d[k] = np.diag(y[k]).astype(complex)
    return d


def prepare():
    OUT.mkdir(exist_ok=True)
    y_toy = {k: TOY_SM["y"] * np.array([1.0, 2.0, 3.0]) for k in ["Gu", "Gd", "Ge"]}
    y_a = yukawas_A()
    data = {
        "B": {"sm": {k: TOY_SM[k] for k in ["g", "gp", "gs", "Lambda", "m2"]}, "y": {k: v.tolist() for k, v in y_toy.items()},
              "wc": sym_entries(TOY_WC), "scale_in": LAMBDA, "scale_out": MZ},
        "A": {"sm": SM_A, "y": {k: v.tolist() for k, v in y_a.items()}, "wc": sym_entries(WC_A),
              "scale_in": LAMBDA, "scale_out": MZ},
        "D": {"alpha_s": ALPHAS_D, "scale_in": MZ, "scale_out": MLOW},   # the coefficients WC_D are set in the .wl file
    }
    json.dump(data, open(OUT / "stage1_in.json", "w"), indent=1)
    # the same coefficients as a WCxf file, for DsixTools' own WCxf reader (ReadInputFiles)
    wc = wcxf.WC("SMEFT", "Warsaw", LAMBDA, wcxf.WC.dict2values(WC_A))
    with open(OUT / "caseA_wcxf.json", "w") as f:
        wc.dump(f, fmt="json")
    print("wrote out/stage1_in.json and out/caseA_wcxf.json")


def run_smeft(wcdict, sm, y, **tol):
    s = SMEFT(wcxf.WC("SMEFT", "Warsaw", LAMBDA, wcxf.WC.dict2values(wcdict)), get_smpar=False)
    s.C_in.update(sm_dict(sm, y))
    return s._rgevolve(MZ, **tol)


def rel(a, b):
    return abs(a / b - 1)


def row(n, what, result, verdict):
    print(f"{n:2d}  {what:62s} {result:58s} {verdict}")


def check():
    dB = json.load(open(OUT / "dsix_B.json"))
    dA = json.load(open(OUT / "dsix_A.json"))
    dAw = json.load(open(OUT / "dsix_A_wcxf.json"))
    dC = json.load(open(OUT / "dsix_C.json"))
    dD = json.load(open(OUT / "dsix_D.json"))
    print(f"{'':2s}  {'check':62s} {'result':58s} verdict")

    # (B) pure-QCD toy
    y_toy = {k: TOY_SM["y"] * np.array([1.0, 2.0, 3.0]) for k in ["Gu", "Gd", "Ge"]}
    a0 = TOY_SM["gs"] ** 2
    a = a0 / (1 + 2 * 7 * a0 / (16 * math.pi ** 2) * math.log(MZ / LAMBDA))
    own = {"gs": math.sqrt(a), "ledq": (a / a0) ** (4 / 7), "lequ1": (a / a0) ** (4 / 7), "lequ3": (a / a0) ** (-4 / 21),
           "lq1": 1.0, "phiG": a / a0}
    for tag, tol in [("tight", TIGHT), ("default", {})]:
        C = run_smeft(TOY_WC, TOY_SM, y_toy, **tol)
        w = {"gs": C["gs"].real, "phiG": C["phiG"].real / 1e-6,
             **{k: C[k][0, 0, 0, 0].real / 1e-6 for k in ["ledq", "lequ1", "lequ3", "lq1"]}}
        d = dB[tag]
        dw = max(rel(w[k], own[k]) for k in own)
        dd = max(rel(d[k] / (1 if k == "gs" else 1e-6), own[k]) for k in own)
        verdict = ("agree" if max(dw, dd) < 1e-9 else "see text") if tag == "tight" else "note"
        row(1 if tag == "tight" else 2, f"B: pure-QCD toy, {tag} ODE tolerances, vs own power laws",
            f"max rel. diff wilson {dw:.1e}, DsixTools {dd:.1e}", verdict)

    # (A) full one-loop RGEs, same input
    y_a = yukawas_A()
    C = run_smeft(WC_A, SM_A, y_a, **TIGHT)
    Cdef = run_smeft(WC_A, SM_A, y_a)
    wn = smeftutil.arrays2wcxf_nonred(C)
    wndef = smeftutil.arrays2wcxf_nonred(Cdef)
    vals = {k: (complex(v["Re"], v["Im"]) if isinstance(v, dict) else complex(v)) for k, v in dAw["values"].items()}
    big = max(abs(v) for v in wn.values())
    keys = [k for k in wn if abs(wn[k]) > 1e-3 * big]
    md = max(abs(vals.get(k, 0) - wn[k]) / abs(wn[k]) for k in keys)
    worst = max(keys, key=lambda k: abs(vals.get(k, 0) - wn[k]) / abs(wn[k]))
    row(3, "A: SMEFT, full SM, 1 TeV -> M_Z, Warsaw coefficients (WCxf export)",
        f"{len(keys)} > 1e-3 of the largest: max rel. diff {md:.1e} ({worst})",
        "agree" if md < 1e-6 else "see text")      # DsixTools writes 7 significant digits
    # the export has 7 significant digits: a coefficient agrees if it is within that rounding or within 1e-9 of the largest
    diff = {k: abs(vals.get(k, 0) - wn[k]) for k in wn}
    bad = [k for k in wn if diff[k] > 5e-7 * abs(wn[k]) and diff[k] > 1e-9 * big]
    worst = max(wn, key=lambda k: diff[k] / max(5e-7 * abs(wn[k]), 1e-9 * big))
    row(4, f"   all {len(wn)} coefficients (within the 7 digits or 1e-9 of the largest)",
        f"{len(bad)} outside; worst {worst}: diff {diff[worst]/abs(wn[worst]):.1e} rel., {diff[worst]/big:.1e} of the largest",
        "agree" if not bad else ("agree to 1e-8 of the largest" if diff[worst] < 1e-8 * big else "see text"))
    # le_3311 differs by 3e-6 (1.3e-9 of the largest); unchanged with DsixTools at PrecisionGoal 13 and wilson at rtol 1e-13,
    # so a small difference between the two codes' RGEs, not the integration
    sm_d = max(rel(dA["sm"][k], C[k].real) for k in ["gs", "g", "gp", "Lambda", "m2"])
    row(5, "   SM couplings at M_Z (g_s, g, g', lambda, m^2)", f"max rel. diff {sm_d:.1e}", "agree" if sm_d < 1e-8 else "see text")
    mdef = max(abs(wndef[k] - wn[k]) / abs(wn[k]) for k in keys)
    row(6, "   wilson with solve_ivp's default tolerances (Wilson.match_run)", f"max rel. diff to tight {mdef:.1e}", "note")
    imp = dA["import"]
    row(7, "   DsixTools' WCxf reader: phil1_12, lq1_1123, dd_1112 in its arrays",
        f"{imp['CHl1_12']/WC_A['phil1_12'].real:.3f}, {imp['Clq1_1123']/WC_A['lq1_1123']:.3f}, "
        f"{imp['Cdd_1112']/0.5e-7:.3f} x wilson's", "differ (DsixTools)")

    # (C) tree matching
    out = wilson_match(WC_C)
    ownC = {"VedLL_1111": A_C + B_C, "VnudLL_1111": A_C - B_C, "VedLL_1123": A_C - B_C, "VnudLL_1123": A_C + B_C,
            "SedRL_1111": C_C}
    dw = max(rel(out[k], v) for k, v in ownC.items())
    exact = dC["LedVLL"] == [1, 1, 0] and dC["LnudVLL"] == [1, -1, 0] and dC["LedSRL"] == [0, 0, 1]
    row(8, "C: tree SMEFT -> WET matching at M_Z vs own", f"wilson max rel. diff {dw:.1e}; DsixTools MatchEW "
        f"coefficients {'= own' if exact else '!= own'}", "agree" if dw < 1e-12 and exact else "see text")

    # (D) WET running
    keys_d = ["SedRL_1111", "TeuRR_1111", "SeuRR_1111", "VedLL_1111"]
    pw = {"SedRL_1111": 12 / 23, "SeuRR_1111": 12 / 23, "TeuRR_1111": -4 / 23, "VedLL_1111": 0.0}
    r = WETrunner(wcxf.WC("WET", "JMS", MZ, WC_D), parameters={"alpha_s": ALPHAS_D}, qed_order=0)
    o = r.run(MLOW).dict
    x = r._get_running_parameters(MLOW, 5)["alpha_s"] / r._get_running_parameters(MZ, 5)["alpha_s"]
    dw = max(rel(o[k].real / 1e-6, x ** pw[k]) for k in keys_d)
    g0, g1 = dD["noqed"]["gQCD_in"], dD["noqed"]["gQCD_out"]
    a_own = (g0 ** 2 / (4 * math.pi)) / (1 - 23 / 3 / (2 * math.pi) * (g0 ** 2 / (4 * math.pi)) * math.log(MZ / MLOW))
    xd = a_own / (g0 ** 2 / (4 * math.pi))
    dd = max(rel(dD["noqed"][k] / 1e-6, xd ** pw[k]) for k in keys_d)
    das = rel(g1 ** 2 / (4 * math.pi), a_own)
    row(9, "D: WET M_Z -> 5 GeV without QED vs own power laws", f"wilson {dw:.1e}; DsixTools {dd:.1e} "
        f"(its 1-loop alpha_s(5) vs own {das:.1e})", "agree" if max(dw, dd, das) < 1e-7 else "see text")

    class WET1(WETrunner):     # wilson with alpha_s at one loop, as DsixTools with LEFTLoopOrder 1
        def _get_running_parameters(self, scale, f, loop=3):
            return WETrunner._get_running_parameters(self, scale, f, loop=1)
    ae = dD["qed"]["eQED_in"] ** 2 / (4 * math.pi)
    o1 = WET1(wcxf.WC("WET", "JMS", MZ, WC_D), parameters={"alpha_s": ALPHAS_D, "alpha_e": ae}, qed_order=1).run(MLOW).dict
    o0 = WET1(wcxf.WC("WET", "JMS", MZ, WC_D), parameters={"alpha_s": ALPHAS_D, "alpha_e": ae}, qed_order=0).run(MLOW).dict
    qed = {k: o1[k].real / o0[k].real - 1 for k in keys_d}
    dq = max(rel(o1[k].real / 1e-6, dD["qed"][k] / 1e-6) for k in keys_d)
    row(10, "   with QED: wilson (1-loop alpha_s, fixed alpha_e) vs DsixTools",
        f"max rel. diff {dq:.1e}; QED shifts {min(qed.values()):+.3f} .. {max(qed.values()):+.3f}",
        "agree" if dq < 1e-3 else "see text")
    w = WETrunner(wcxf.WC("WET", "JMS", MZ, WC_D), qed_order=1).run(MLOW).dict
    print(f"    (wilson's defaults, alpha_s(M_Z) = 0.1185 at 3 loops, alpha_e = 1/127.9: S_ed {w['SedRL_1111'].real/1e-6:.6f}, "
          f"T_eu {w['TeuRR_1111'].real/1e-6:.6f}, S_eu {w['SeuRR_1111'].real/1e-6:.6f}, V_ed {w['VedLL_1111'].real/1e-6:.6f})")


def wilson_match(wcdict):
    from wilson import Wilson
    out = Wilson(wcdict, scale=MZ, eft="SMEFT", basis="Warsaw").match_run(MZ, "WET", "JMS").dict
    return {k: complex(v) for k, v in out.items()}


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    for arg in sys.argv[1:] or ["check"]:
        {"prepare": prepare, "check": check}[arg]()
