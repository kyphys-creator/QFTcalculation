# %% [markdown]
# # Step (9d): MadLoop with the note's general NLO UFO against MadGraph's on-shell EW model, several processes
#
# Research note models/sm, step (9d).  Runs the MadLoop standalone programs built by run_fj_check.sh for processes with
# massless external particles, [virt=QED], at sqrt(s) = 500 GeV, theta = pi/3, mu_R = MZ and 500 GeV:
#   off: loop_qcd_qed_sm-no_widths (on-shell MW, MZ, alpha(MZ) scheme), the inputs p of nunu_madloop.py;
#   fj:  the note's UFO (generated/SM_NLO_FJ_UFO, nlo_ufo.wl; restricted to light masses and widths 0), the same numbers
#        read as the note's MS-bar parameters.
# Both have the same loops (the same Feynman-gauge one-loop diagrams) and differ in the counterterms only, which are
# linear in the renormalization constants.  At the same numbers p, the MS-bar parameters p are the on-shell ones
# p - dp, dp = p(MS-bar) - p(OS) (note Eq. (convOS), from nunu_numeric.wl: de, dMW2, dMZ2; the note's own model), so
#   finite(off) - finite(fj) = sum_i (d born/d p_i) dp_i        (exactly, at one loop)
# with p = aEWM1 (d aEWM1 = -2 aEWM1 de), MZ, MW; the derivatives of MadLoop's born numerically (five-point stencil and
# Richardson; the param_card keeps 11 digits: MadGraph's reader cuts a value to 20 characters).
# The poles (1eps, 2eps: infrared only) must agree.  Writes results/fj_madloop.csv.
# Usage (from Src/): python3 fj_madloop.py  (after run_fj_check.sh);  --restrict <param_card> <card>;  --procs

# %%
import csv
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work", "fj")
INPUT = {"aEWM1": 128.0, "MZ": 91.1876, "MW": 80.369, "MH": 125.2, "MT": 172.57, "ymt": 172.57}
LIGHT = {"MD": 0, "MU": 0, "MS": 0, "MC": 0, "MB": 0, "Me": 0, "MMU": 0, "MTA": 0}
FJ_CARD = ({**{k: v for k, v in INPUT.items() if k != "ymt"}, **LIGHT}, (6, 23, 24, 25))
SQRTS, THETA = 500.0, math.pi / 3
MUS = (91.1876, 500.0)
# name, MadGraph process
PROCS = [("nunu", "ve ve~ > vm vm~"), ("eemm", "e+ e- > mu+ mu-"), ("eenn", "e+ e- > ve ve~"),
         ("vee", "ve e- > ve e-"), ("uuee", "u u~ > e+ e-"), ("ddmm", "d d~ > mu+ mu-"), ("eeaa", "e+ e- > a a")]


def set_card(path, vals, widths=(), dst=None, missing_ok=False):
    """set the values in a param_card (or write the result to dst, e.g. a restriction card); missing_ok: a restricted
    model's card has no entries for the parameters fixed to 0"""
    s = open(path).read()
    for k, v in vals.items():
        s, n = re.subn(r"(\n\s+\d+\s+)\S+(\s+#\s+%s\s*\n)" % k, lambda m: m.group(1) + "%.10e" % v + m.group(2), s)
        assert n == 1 or (n == 0 and missing_ok and v == 0), (k, n)
    for pdg in widths:
        s, n = re.subn(r"(\nDECAY\s+%d\s+)\S+" % pdg, lambda m: m.group(1) + "0.000000e+00", s)
        assert n == 1, pdg
    open(dst or path, "w").write(s)


def run(ml, mu):
    base = os.path.join(ml, "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    e = SQRTS / 2
    c, st = math.cos(THETA), math.sin(THETA)
    pts = [(e, 0, 0, e), (e, 0, 0, -e), (e, e * st, 0, e * c), (e, -e * st, 0, -e * c)]
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % p for p in pts)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {k: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % k, out).group(1)) for k in ("born", "finite", "1eps", "2eps")}


def conversion():
    """de, dMW2, dMZ2 at mu (nunu_numeric.wl: the note's own self-energies, FJ with tadpoles, Feynman gauge row)"""
    with open(os.path.join(HERE, "results", "nunu_conv.csv")) as fh:
        rows = [r for r in csv.DictReader(fh) if r["xiZ"] == "1" and r["xiW"] == "1"]
    return {round(float(r["mu"]), 4): {k: float(r[k]) for k in ("de", "dMW2", "dMZ2")} for r in rows}


if sys.argv[1:] == ["--procs"]:
    print("\n".join(f"{n}|{p}" for n, p in PROCS))
    sys.exit(0)
if len(sys.argv) == 4 and sys.argv[1] == "--restrict":
    set_card(sys.argv[2], FJ_CARD[0], FJ_CARD[1], dst=sys.argv[3])
    sys.exit(0)

# %%
conv = conversion()
rows = []
for name, proc in PROCS:
    off, fj = os.path.join(WORK, name + "_off"), os.path.join(WORK, name + "_fj")
    card_off, card_fj = os.path.join(off, "Cards", "param_card.dat"), os.path.join(fj, "Cards", "param_card.dat")
    set_card(card_fj, FJ_CARD[0], missing_ok=True)
    print(f"{proc}:")
    # d born/d p (born does not depend on mu_R): the five-point stencil at relative steps h = 2e-4 and 2h, Richardson
    # (16 d(h) - d(2h))/15 (the stencil alone has an h^4 error of 5e-8 for MZ, MW at h = 1e-3; smaller h loses digits)
    grad = {}
    for p in ("aEWM1", "MZ", "MW"):
        d = []
        for h in (INPUT[p] * 2e-4, INPUT[p] * 4e-4):
            b = []
            for k in (-2, -1, 1, 2):
                set_card(card_off, {**INPUT, p: INPUT[p] + k * h})
                b.append(run(off, MUS[0])["born"])
            d.append((b[0] - 8 * b[1] + 8 * b[2] - b[3]) / (12 * h))
        grad[p] = (16 * d[0] - d[1]) / 15
    set_card(card_off, INPUT)
    for mu in MUS:
        mo, mf = run(off, mu), run(fj, mu)
        c = conv[round(mu, 4)]
        dp = {"aEWM1": -2 * INPUT["aEWM1"] * c["de"], "MZ": c["dMZ2"] / (2 * INPUT["MZ"]), "MW": c["dMW2"] / (2 * INPUT["MW"])}
        pred = sum(grad[p] * dp[p] for p in dp)
        diff = mo["finite"] - mf["finite"]
        print(f"  mu = {mu:8.4f}: born {mo['born']:.15e} (fj rel {mf['born'] / mo['born'] - 1:+.1e});  finite off {mo['finite']:.15e}, "
              f"fj {mf['finite']:.15e};  off - fj {diff:.15e}, sum dborn/dp dp {pred:.15e} (rel {diff / pred - 1:+.1e}, "
              f"/born {(diff - pred) / mo['born']:+.1e});  "
              f"1eps off {mo['1eps']:.6e} fj {mf['1eps']:.6e}, 2eps off {mo['2eps']:.6e} fj {mf['2eps']:.6e}")
        rows.append([name, proc, mu, mo["born"], mf["born"], mo["finite"], mf["finite"], diff, pred,
                     mo["1eps"], mf["1eps"], mo["2eps"], mf["2eps"], grad["aEWM1"], grad["MZ"], grad["MW"]])
with open(os.path.join(HERE, "results", "fj_madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["name", "process", "mu", "born_off", "born_fj", "finite_off", "finite_fj", "off_minus_fj", "pred",
                "1eps_off", "1eps_fj", "2eps_off", "2eps_fj", "dborn_daEWM1", "dborn_dMZ", "dborn_dMW"])
    w.writerows(rows)
