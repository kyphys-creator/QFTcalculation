"""Research note models/sm_pp, step (2f): MadLoop's virtual correction to g g -> H with the note's own NLO UFO against the note's
own F^(1) (gh_feyncalc.wl, section (f)).

The UFO is generated/QCDH_NLO_UFO (gh_nlo_ufo.wl: QCDH.fr, NLOCT's QCD counterterms and the own g g H R2 and UV vertices of
gh_r2.wl).  Its work copy (work/gh/QCDH_NLO_UFO, also used by gh_own_mg5.sh) gets dummy M_Z, M_W, M_t and inert Z, W, t particles
(no vertices), which MadGraph5_aMC@NLO's NLO templates need (fks_singular.f uses mdl_MZ, mdl_MW and, in its 6 -> 5 flavour
counterterm that is switched off, mdl_MT; coupl.inc declares only the masses of particles; as the QCD note's ee_mg5.py), and a QED
coupling order that no vertex carries (fks_singular.f indexes its orders by the QED position).  g g > h [virt=QCD], output standalone,
COLLIER (MLReductionLib = 7), check_sa.f patched to read the point and MU_R (models/sm/Src/patch_check_sa.py); MH = 125.2,
alpha_s = 0.118, kHgg = 1, mu_R = M/2, M, 2 M:
  born  against  (cHgg/v)^2 M_H^4/64  (cHgg = -alpha_s/(3 pi); averaged over the 2 x 2 helicities and 8 x 8 colours),
  2eps/born, 1eps/born, finite/born  against  a_s (A, B, C) of gh_feyncalc.wl (a_s = alpha_s/(4 pi), MadLoop's normalization;
  no Wilson coefficient: the UFO's counterterm is the operator's alpha_s renormalization only).
Usage (from Src/): ~/hep/opt/lhc/bin/python gh_own_madloop.py [--fresh]   (writes results/gh_own_madloop.csv; about 10 seconds;
--fresh remakes the work copy of the UFO and the standalone output)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from gh_madloop import AS, MG5, MH, PATCH, run_check, set_param

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "gh"


def own_ufo():
    """the work copy of generated/QCDH_NLO_UFO with dummy M_Z, M_W, M_t, inert Z, W, t (no vertices) and a QED order"""
    dst = WORK / "QCDH_NLO_UFO"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(HERE / "generated" / "QCDH_NLO_UFO", dst, ignore=shutil.ignore_patterns("*.pyc", "__pycache__", "*.pkl"))
    with open(dst / "parameters.py", "a") as fh:
        fh.write("\n# research note models/sm_pp: dummy M_Z, M_W, M_t for MadGraph5_aMC@NLO's NLO templates (no particle couples to them)\n"
                 "MZ = Parameter(name = 'MZ', nature = 'external', type = 'real', value = 91.188, texname = '\\\\text{MZ}', lhablock = 'MASS', lhacode = [ 23 ])\n"
                 "MW = Parameter(name = 'MW', nature = 'external', type = 'real', value = 80.379, texname = '\\\\text{MW}', lhablock = 'MASS', lhacode = [ 24 ])\n"
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
    with open(dst / "coupling_orders.py", "a") as fh:
        fh.write("\n# research note models/sm_pp: a QED order that no vertex carries (aMC@NLO's fks_singular.f indexes by its position)\n"
                 "QED = CouplingOrder(name = 'QED', expansion_order = 99, hierarchy = 2)\n")
    return dst


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / "ml_own"
    if "--fresh" in sys.argv:
        shutil.rmtree(out, ignore_errors=True)
    if not (out / "SubProcesses").exists():
        own_ufo()
        (WORK / "ml_own.mg5").write_text("set automatic_html_opening False\nimport model ./QCDH_NLO_UFO\n"
                                         "generate g g > h [virt=QCD]\noutput standalone ./ml_own\n")
        r = subprocess.run([str(MG5), "ml_own.mg5"], cwd=WORK, capture_output=True, text=True)
        (WORK / "ml_own.log").write_text(r.stdout + r.stderr)
        if r.returncode != 0 or not (out / "SubProcesses").exists():
            sys.exit("MG5 output failed: work/gh/ml_own.log")
    set_param(out / "Cards" / "param_card.dat", {"MH": MH, "aS": AS, "kHgg": 1.0})
    vev = float(re.search(r"\n\s*1\s+(\S+)\s+#\s*vev\b", open(out / "Cards" / "param_card.dat").read()).group(1))
    card = out / "Cards" / "MadLoopParams.dat"
    s, n = re.subn(r"(#MLReductionLib\n)[^\n]*", lambda m: m.group(1) + "7", open(card).read())
    assert n == 1
    open(card, "w").write(s)
    d = next(p for p in sorted((out / "SubProcesses").iterdir()) if p.is_dir() and p.name.startswith("P"))
    if "MU_R.input" not in open(d / "check_sa.f").read():
        subprocess.run([sys.executable, str(PATCH), str(d / "check_sa.f")], check=True)
    subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
    ref = {}
    for row in csv.reader(open(HERE / "results" / "gh_feyncalc.csv")):
        if row and row[0].startswith("madloop_ABC_muR_over_MH="):
            ref[float(row[0].split("=")[1])] = tuple(float(x) for x in row[1:4])
    a_s = AS / (4 * math.pi)
    born_own = (AS / (3 * math.pi) / vev) ** 2 * MH ** 4 / 64
    rows, worst = [], 0.0
    for f in (0.5, 1.0, 2.0):
        r = run_check(d, f * MH)
        got = (r["2eps"] / r["born"] / a_s, r["1eps"] / r["born"] / a_s, r["finite"] / r["born"] / a_s)
        exp = ref[f]
        dev = [g - e for g, e in zip(got, exp)]
        worst = max(worst, max(abs(x) / max(1.0, abs(e)) for x, e in zip(dev, exp)))
        print("mu_R = %.2f M_H: born %.12e (own %.12e, %.1e);  MadLoop/a_s  A %.12f  B %.12f  C %.12f;  own A %.12f  B %.12f  C %.12f;  "
              "differences %.1e %.1e %.1e" % ((f, r["born"], born_own, r["born"] / born_own - 1) + got + exp + tuple(dev)))
        rows.append([f] + ["%.15e" % x for x in got + exp] + ["%.15e" % r["born"], "%.15e" % born_own])
    print("largest difference (relative to max(1, |own|)): %.1e" % worst)
    with open(HERE / "results" / "gh_own_madloop.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muR_over_MH", "ml_A", "ml_B", "ml_C", "own_A", "own_B", "own_C", "ml_born", "own_born"])
        w.writerows(rows)
    print("written: results/gh_own_madloop.csv")


if __name__ == "__main__":
    main()
