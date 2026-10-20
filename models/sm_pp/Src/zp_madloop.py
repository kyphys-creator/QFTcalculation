"""Research note models/sm_pp, step (4b): MadLoop's virtual correction to u u~ > e+ e- through the SSM Z' with the note's NLO UFO
(generated/QCDZp_NLO_UFO of zp_generate_nlo.sh) against the note's own form factor (step (1)).

The work copy work/zp/QCDZp_NLO_UFO (also used by zp_mg5.sh) gets inert Z (mass MZ, the model's electroweak input), W (MW, internal)
and t (dummy MT = 172.5) particles without vertices, which MadGraph5_aMC@NLO's NLO templates need (as gh_own_madloop.py).
u u~ > e+ e- [virt=QCD], output standalone, COLLIER, check_sa.f patched to read the point and MU_R (models/sm/Src/patch_check_sa.py);
MZp = 3000 GeV, WZp of stage 6 (MadWidth, 88.6729 GeV), alpha_s = 0.118, sqrt(shat) = 2500 GeV, the electron at 90 degrees:
  born  against  (shat^2/(4 N_c)) sum_ij |A_ij|^2,  A_ij = g^2 g_i^u g_j^e/(shat - M^2 + i M Gamma)  (i, j = L, R; g = e/(s_W c_W));
  2eps/born, 1eps/born, finite/born in units of a_s = alpha_s/(4 pi) (MadLoop's normalization, (4 pi)^eps/Gamma(1 - eps) taken
  out) against 2 Re F^(1) of the massless-quark vector and axial form factor at Q^2 = shat + i0 (step (1)):
     A = -4 C_F,  B = -6 C_F,  C = C_F (2 pi^2 - 16)   at mu_R^2 = shat,  and B + A L, C + B L + A L^2/2 with L = ln(mu_R^2/shat).
Usage (from Src/): ~/hep/opt/lhc/bin/python zp_madloop.py [--fresh]   (writes results/zp_madloop.csv)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from gh_madloop import MG5, PATCH, set_param

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "zp"
AS, MZP, WZP, ROOTS = 0.118, 3000.0, 88.6729, 2500.0
CF, NC = 4.0 / 3.0, 3


def zp_ufo():
    """the work copy of generated/QCDZp_NLO_UFO with inert Z, W, t (no vertices)"""
    dst = WORK / "QCDZp_NLO_UFO"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(HERE / "generated" / "QCDZp_NLO_UFO", dst, ignore=shutil.ignore_patterns("*.pyc", "__pycache__", "*.pkl"))
    with open(dst / "parameters.py", "a") as fh:
        fh.write("\n# research note models/sm_pp: dummy M_t for MadGraph5_aMC@NLO's NLO templates (no particle couples to it)\n"
                 "MT = Parameter(name = 'MT', nature = 'external', type = 'real', value = 172.5, texname = '\\\\text{MT}', lhablock = 'MASS', lhacode = [ 6 ])\n")
    with open(dst / "particles.py", "a") as fh:
        fh.write("\n# research note models/sm_pp: inert Z, W and t (no vertices), so that coupl.inc declares mdl_MZ, mdl_MW, mdl_MT\n"
                 "Z = Particle(pdg_code = 23, name = 'Z', antiname = 'Z', spin = 3, color = 1, mass = Param.MZ, width = Param.ZERO,\n"
                 "             texname = 'Z', antitexname = 'Z', charge = 0, GhostNumber = 0)\n"
                 "W__plus__ = Particle(pdg_code = 24, name = 'W+', antiname = 'W-', spin = 3, color = 1, mass = Param.MW, width = Param.ZERO,\n"
                 "                     texname = 'W+', antitexname = 'W-', charge = 1, GhostNumber = 0)\n"
                 "W__minus__ = W__plus__.anti()\n"
                 "t = Particle(pdg_code = 6, name = 't', antiname = 't~', spin = 2, color = 3, mass = Param.MT, width = Param.ZERO,\n"
                 "             texname = 't', antitexname = 't~', charge = 2/3, GhostNumber = 0)\n"
                 "t__tilde__ = t.anti()\n")
    return dst


def set_width(path, pdg, w):
    s = open(path).read()
    s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "%.10e" % w, s)
    assert n == 1
    open(path, "w").write(s)


def card_inputs(path):
    vals = {}
    for line in open(path):
        m = re.match(r"\s*\d+\s+(\S+)\s+#\s*(\w+)", line)
        if m:
            vals[m.group(2).lower()] = float(m.group(1))
    return vals


def run_point(d, mu):
    e = ROOTS / 2
    pts = [(e, 0, 0, e), (e, 0, 0, -e), (e, e, 0, 0), (e, -e, 0, 0)]
    with open(d / "PS.input", "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(d / "MU_R.input", "w") as fh:
        fh.write("%.17e\n" % mu)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {k: float(m.group(1)) if (m := re.search(r"Matrix element %s\s*=\s*(\S+)" % k, o)) else 0.0
            for k in ("born", "finite", "1eps", "2eps")}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / "ml_zp"
    if "--fresh" in sys.argv:
        shutil.rmtree(out, ignore_errors=True)
    if not (out / "SubProcesses").exists():
        zp_ufo()
        (WORK / "ml_zp.mg5").write_text("set automatic_html_opening False\nimport model ./QCDZp_NLO_UFO\n"
                                        "generate u u~ > e+ e- [virt=QCD]\noutput standalone ./ml_zp\n")
        r = subprocess.run([str(MG5), "ml_zp.mg5"], cwd=WORK, capture_output=True, text=True)
        (WORK / "ml_zp.log").write_text(r.stdout + r.stderr)
        if r.returncode != 0 or not (out / "SubProcesses").exists():
            sys.exit("MG5 output failed: work/zp/ml_zp.log")
    pc = out / "Cards" / "param_card.dat"
    set_param(pc, {"MZp": MZP, "aS": AS})
    set_width(pc, 32, WZP)
    card = out / "Cards" / "MadLoopParams.dat"
    s, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + "7", open(card).read())
    assert n == 1
    open(card, "w").write(s)
    d = next(p for p in sorted((out / "SubProcesses").iterdir()) if p.is_dir() and p.name.startswith("P"))
    if "MU_R.input" not in open(d / "check_sa.f").read():
        subprocess.run([sys.executable, str(PATCH), str(d / "check_sa.f")], check=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    # own Born: the couplings from the card's electroweak inputs (as SM.fr and stage 6)
    v = card_inputs(pc)
    aew = 1 / v["aewm1"]
    mw = math.sqrt(v["mz"] ** 2 / 2 + math.sqrt(v["mz"] ** 4 / 4 - aew * math.pi * v["mz"] ** 2 / (v["gf"] * math.sqrt(2))))
    sw2 = 1 - mw ** 2 / v["mz"] ** 2
    g2 = 4 * math.pi * aew / (sw2 * (1 - sw2))
    gu = {"L": 0.5 - 2 / 3 * sw2, "R": -2 / 3 * sw2}
    ge = {"L": -0.5 + sw2, "R": sw2}
    sh = ROOTS ** 2
    prop = 1 / (sh - MZP ** 2 + 1j * MZP * WZP)
    born_own = sh ** 2 / (4 * NC) * sum(abs(g2 * gu[i] * ge[j] * prop) ** 2 for i in "LR" for j in "LR")
    a_s = AS / (4 * math.pi)
    A0, B0, C0 = -4 * CF, -6 * CF, CF * (2 * math.pi ** 2 - 16)
    rows, worst = [], 0.0
    for f in (1.0, 2.0, 0.5):
        r = run_point(d, f * ROOTS)
        L = math.log(f * f)
        got = (r["2eps"] / r["born"] / a_s, r["1eps"] / r["born"] / a_s, r["finite"] / r["born"] / a_s)
        exp = (A0, B0 + A0 * L, C0 + B0 * L + A0 * L * L / 2)
        dev = [g - e for g, e in zip(got, exp)]
        worst = max(worst, max(abs(x) / max(1.0, abs(e)) for x, e in zip(dev, exp)))
        print("mu_R = %.2f sqrt(shat): born %.12e (own %.12e, %+.1e);  MadLoop/a_s  A %.12f  B %.12f  C %.12f;  own %.12f  %.12f  %.12f;"
              "  differences %.1e %.1e %.1e" % ((f, r["born"], born_own, r["born"] / born_own - 1) + got + exp + tuple(dev)))
        rows.append([f] + ["%.15e" % x for x in got + exp] + ["%.15e" % r["born"], "%.15e" % born_own])
    print("largest difference (relative to max(1, |own|)): %.1e" % worst)
    with open(HERE / "results" / "zp_madloop.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muR_over_sqrt_shat", "ml_A", "ml_B", "ml_C", "own_A", "own_B", "own_C", "ml_born", "own_born"])
        w.writerows(rows)
    print("written: results/zp_madloop.csv")


if __name__ == "__main__":
    main()
