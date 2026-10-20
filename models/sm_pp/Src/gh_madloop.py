"""Research note models/sm_pp, step (2c): MadLoop's virtual correction to g g -> H in the heavy-top effective theory against the
note's own F^(1) (gh_feyncalc.wl, section (f)).

The NLO UFO is HC_NLO_X0 1.3 (F. Demartin, M. Zaro; FeynRules model database, HiggsCharacterisation, HC_NLO_X0_UFO.zip, 123075 bytes,
in ~/hep/src/smpp2-dl/extracted), restriction heft (5 massless flavours, no Yukawa), its g g X0 coupling -i cosa kHgg gHgg with
gHgg = -alpha_s/(3 pi v): the note's cHgg/v with kHgg = cosa = 1.  Its R2 and UV vertices are what this check tests (the note's own
NLOCT run on QCDH.fr leaves unevaluated Feynman-parameter integrals in them).  A work copy holds only the .py sources and cards (the
archive's .pyc and pickled model are not used).  g g > x0 / t [virt=QCD], output standalone, COLLIER (MLReductionLib = 7),
check_sa.f patched to read the point and MU_R (models/sm/Src/patch_check_sa.py); MX0 = 125.2, alpha_s = 0.118, mu_R = M/2, M, 2 M:
  2eps/born, 1eps/born, finite/born  against  a_s (A, B, C + 22) of gh_feyncalc.wl (a_s = alpha_s/(4 pi), MadLoop's
  normalization; 22 a_s = (11/2) alpha_s/pi, the Wilson coefficient in HC_NLO_X0's counterterm).
Usage (from Src/): ~/hep/opt/lhc/bin/python gh_madloop.py [--fresh]   (writes results/gh_madloop.csv; about 1 minute;
--fresh remakes the work copy of the UFO and the standalone output)
"""
import csv
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "gh"
SRCUFO = Path.home() / "hep" / "src" / "smpp2-dl" / "extracted" / "HC_NLO_X0_UFO"
PATCH = HERE.parent.parent / "sm" / "Src" / "patch_check_sa.py"
MG5 = Path.home() / "hep" / "bin" / "mg5_aMC"
AS, MH = 0.118, 125.2


def work_ufo():
    """a work copy with the .py sources and the cards only, and one local patch of CT_parameters.py.

    The g g X0 UV counterterm (alpha_s renormalization of gHgg ~ alpha_s) is split by loop particles: [[u],[d],[s]] (2 T_F/3 each,
    pole only), c, b, t, and [[G]] (11 C_A/6, with the Wilson coefficient's -(11/4) alpha_s/pi as its finite part).  MG5 3.8.1 keeps
    a counterterm only for the loop particles of the generated loops; g g > x0 / t has gluon and ghost loops only, so the u, d, s part
    is dropped: MadLoop's single pole is 4 a_s below the n_f = 5 one of the FKS subtraction and aMC@NLO stops ("Poles do not cancel").
    The patch moves the u, d, s poles (3 x 2 T_F/3 = 2 T_F) into the [[G]] entry and sets the [[u],[d],[s]] entry to 0; for massless
    quarks the moved part is a pure pole, so the finite part is unchanged."""
    dst = WORK / "HC_NLO_X0_UFO"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for f in SRCUFO.iterdir():
        if f.is_file() and (f.suffix in (".py", ".dat") or f.name == "README"):
            shutil.copy2(f, dst / f.name)
    ct = dst / "CT_parameters.py"
    s = ct.read_text()
    old_g = "value = {-1:'complex(0,1)/2.*cosa*kHgg*gHgg*G**2/(4.*cmath.pi**2)*(11.*CA/6.)',"
    new_g = ("value = {-1:'complex(0,1)/2.*cosa*kHgg*gHgg*G**2/(4.*cmath.pi**2)*(11.*CA/6. - 2.*TF)',"
             "  # research note models/sm_pp: + the u, d, s poles")
    old_q = ("G_UV_ggX0_hq = CTParameter(name = 'G_UV_ggX0_hq',\n                           type = 'complex',\n"
             "                           value = {-1:'-complex(0,1)/2.*cosa*kHgg*gHgg*G**2/(4.*cmath.pi**2)*(2.*TF/3.)'},")
    new_q = ("G_UV_ggX0_hq = CTParameter(name = 'G_UV_ggX0_hq',\n                           type = 'complex',\n"
             "                           value = {-1:'0.'},  # research note models/sm_pp: moved into G_UV_ggX0_hg")
    assert s.count(old_g) == 1 and s.count(old_q) == 1
    ct.write_text(s.replace(old_g, new_g).replace(old_q, new_q))
    return dst


def set_param(path, vals):
    """vals: {name in the comment: value}"""
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s*\d+\s+)\S+(\s+#\s*%s\b[^\n]*\n)" % re.escape(k), lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1, (k, n)
    open(path, "w").write(s)


def run_check(d, mu):
    pts = [(MH / 2, 0, 0, MH / 2), (MH / 2, 0, 0, -MH / 2), (MH, 0, 0, 0)]
    with open(d / "PS.input", "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(d / "MU_R.input", "w") as fh:
        fh.write("%.17e\n" % mu)
    o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {k: float(m.group(1)) if (m := re.search(r"Matrix element %s\s*=\s*(\S+)" % k, o)) else 0.0
            for k in ("born", "finite", "1eps", "2eps")}


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / "ml_out"
    if "--fresh" in sys.argv:
        shutil.rmtree(out, ignore_errors=True)
    if not (out / "SubProcesses").exists():
        work_ufo()
        (WORK / "ml.mg5").write_text("set automatic_html_opening False\nimport model ./HC_NLO_X0_UFO-heft\n"
                                     "generate g g > x0 / t [virt=QCD]\noutput standalone ./ml_out\n")
        r = subprocess.run([str(MG5), "ml.mg5"], cwd=WORK, capture_output=True, text=True)
        (WORK / "ml.log").write_text(r.stdout + r.stderr)
        if r.returncode != 0 or not (out / "SubProcesses").exists():
            sys.exit("MG5 output failed: work/gh/ml.log")
    set_param(out / "Cards" / "param_card.dat", {"MX0": MH, "aS": AS})
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
    rows, worst = [], 0.0
    for f in (0.5, 1.0, 2.0):
        r = run_check(d, f * MH)
        got = (r["2eps"] / r["born"] / a_s, r["1eps"] / r["born"] / a_s, r["finite"] / r["born"] / a_s)
        # HC_NLO_X0's [[G]] counterterm has the Wilson coefficient's (11/4) alpha_s/pi as finite part: 2 x 11/4 x 4 = 22 in a_s
        exp = (ref[f][0], ref[f][1], ref[f][2] + 22.0)
        dev = [g - e for g, e in zip(got, exp)]
        worst = max(worst, max(abs(x) / max(1.0, abs(e)) for x, e in zip(dev, exp)))
        print("mu_R = %.2f M_H: MadLoop/a_s  A %.12f  B %.12f  C %.12f;  own A %.12f  B %.12f  C %.12f;  differences %.1e %.1e %.1e"
              % ((f,) + got + exp + tuple(dev)))
        rows.append([f] + ["%.15e" % x for x in got + exp] + ["%.15e" % r["born"]])
    print("largest difference (relative to max(1, |own|)): %.1e" % worst)
    with open(HERE / "results" / "gh_madloop.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["muR_over_MH", "ml_A", "ml_B", "ml_C", "own_A", "own_B", "own_C_plus_22", "ml_born"])
        w.writerows(rows)
    print("written: results/gh_madloop.csv")


if __name__ == "__main__":
    main()
