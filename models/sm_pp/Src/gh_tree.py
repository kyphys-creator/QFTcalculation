"""Research note models/sm_pp, step (2c'): the tree matrix elements of the real emission, g g -> x0 g, u g -> x0 u, u u~ -> x0 g,
from MadGraph's standalone output of HC_NLO_X0-heft (the work copy of gh_madloop.py) against the note's 4-dimensional sums
(gh_feyncalc.wl, (b)), with c = cHgg = -alpha_s/(3 pi), g_s^2 = 4 pi alpha_s, v from the param card, M = MX0:
  sum|M|^2:  g g -> H g   24 c^2 g_s^2/v^2 (M^8 + s^4 + t^4 + u^4)/(s t u)     (average 1/256)
             q g -> H q   -4 c^2 g_s^2/v^2 (s^2 + u^2)/t, t = (p_q,in - p_q,out)^2 (average 1/96)
             q qbar -> H g 4 c^2 g_s^2/v^2 (t^2 + u^2)/s                       (average 1/36)
at three random points each.  Writes results/gh_tree.csv.  Usage (from Src/): ~/hep/opt/lhc/bin/python gh_tree.py"""
import csv
import math
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "gh"
MG5 = Path.home() / "hep" / "bin" / "mg5_aMC"
sys.path.insert(0, str(HERE))
import gh_madloop as ml  # noqa: E402

AS, MH = 0.118, 125.2
PROCS = [("gg", "g g > x0 g / t"), ("ug", "u g > x0 u / t"), ("uu", "u u~ > x0 g / t")]


def mdot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def point(rng, sqrts):
    """p1 + p2 -> H(q) + k (massless k), random angles"""
    e = sqrts / 2
    p1, p2 = (e, 0, 0, e), (e, 0, 0, -e)
    kk = (sqrts ** 2 - MH ** 2) / (2 * sqrts)
    c, ph = rng.uniform(-0.9, 0.9), rng.uniform(0, 2 * math.pi)
    s_ = math.sqrt(1 - c * c)
    k = (kk, kk * s_ * math.cos(ph), kk * s_ * math.sin(ph), kk * c)
    q = (sqrts - kk, -k[1], -k[2], -k[3])
    return p1, p2, q, k


def main():
    out = WORK / "tree_out"
    if not (out / "SubProcesses").exists():
        if not (WORK / "HC_NLO_X0_UFO").exists():
            ml.work_ufo()
        cmds = "set automatic_html_opening False\nimport model ./HC_NLO_X0_UFO-heft\n"
        cmds += "generate %s\n" % PROCS[0][1] + "".join("add process %s\n" % p[1] for p in PROCS[1:]) + "output standalone ./tree_out\n"
        (WORK / "tree.mg5").write_text(cmds)
        r = subprocess.run([str(MG5), "tree.mg5"], cwd=WORK, capture_output=True, text=True)
        (WORK / "tree.log").write_text(r.stdout + r.stderr)
    ml.set_param(out / "Cards" / "param_card.dat", {"MX0": MH, "aS": AS})
    vev = None
    for line in open(out / "Cards" / "param_card.dat"):
        pass
    import gh_hadronic as gh
    vev = gh.param_card(out / "Cards" / "param_card.dat")["vev"]
    c2g2 = (AS / (3 * math.pi)) ** 2 * 4 * math.pi * AS / vev ** 2
    rng = random.Random(7)
    rows, worst = [], 0.0
    subs = sorted(p for p in (out / "SubProcesses").iterdir() if p.is_dir() and p.name.startswith("P"))
    for tag, proc in PROCS:
        key = {"gg": "gg_x0g", "ug": "ug_x0u", "uu": "uux_x0g"}[tag]
        d = next(p for p in subs if p.name.endswith(key) or ("_" + key + "_") in p.name + "_")
        subprocess.run(["make", "check"], cwd=d, capture_output=True, text=True, check=True)
        for i in range(3):
            p1, p2, q, k = point(rng, rng.uniform(200, 1500))
            (d / "PS.input").write_text("".join("%.17e %.17e %.17e %.17e\n" % p for p in (p1, p2, q, k)))
            o = subprocess.run(["./check"], cwd=d, capture_output=True, text=True).stdout
            m = re.search(r"Matrix element\s*=\s*(\S+)", o)
            mg = float(m.group(1))
            s, t, u = 2 * mdot(p1, p2), -2 * mdot(p1, k), -2 * mdot(p2, k)
            if tag == "gg":
                own = 24 * c2g2 * (MH ** 8 + s ** 4 + t ** 4 + u ** 4) / (s * t * u) / 256
            elif tag == "ug":
                own = -4 * c2g2 * (s * s + u * u) / t / 96
            else:
                own = 4 * c2g2 * (t * t + u * u) / s / 36
            worst = max(worst, abs(mg / own - 1))
            print("%-14s point %d: MadGraph %.15e  own %.15e  (%+.1e)" % (proc, i, mg, own, mg / own - 1))
            rows.append([proc, i, "%.15e" % mg, "%.15e" % own])
    print("largest relative difference: %.1e" % worst)
    with open(HERE / "results" / "gh_tree.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["process", "point", "madgraph", "own"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
