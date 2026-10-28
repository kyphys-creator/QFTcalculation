# %% [markdown]
# # Step (5): FormCalc's Fortran code for the NLO width of h -> A A, compiled and run
#
# Research note models/abelian_higgs, step (5).  Builds the code that nlo_width_fortran.wl wrote to work/fc_haa (FormCalc's
# driver programs, LoopTools 2.16 from ~/hep/lib, Homebrew gfortran as for MadGraph) and runs it for the decay at rest,
#     ./run uuu 2.5          (unpolarized, sqrt(s) = MH),
# in several builds: the default (Delta = 0, mu = 1) and run.F with DELTA = 1e3, 1e7 (LoopTools' UV regulator; the
# result must not change) and MUDIM = mu^2 for mu = 1/2, 2, 5.  The driver prints dGamma/dcos(theta) at four angles:
# the tree part and the one-loop part 2 Re(M0* M1) (with the counterterm dCTAAh), so
#     Gamma_tree = 2 x (tree),   one-loop / tree = delta_OS of Eq. (nlowidth).
# Compared with results/nlo_width.csv (nlo_width_numeric.wl): Gamma_0 and delta_OS at mu = 1, 2, and at one loop
#     delta_OS(mu) = delta_OS(1) - (2 e^2/(3 K)) ln mu   (the running of e^2 in Gamma_0, K = 16 pi^2).
# Writes results/nlo_width_fortran.csv.  Usage (from Src/, after nlo_width_fortran.wl):
#     ~/miniforge3/envs/qft/bin/python formcalc_fortran.py

# %%
import csv
import math
import os
import subprocess

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
CODE = os.path.join(HERE, "work", "fc_haa")
HOME = os.path.expanduser("~")
env = dict(os.environ, FC="/opt/homebrew/bin/gfortran", LT=os.path.join(HOME, "hep", "lib"))
if "SDKROOT" not in env:
    env["SDKROOT"] = subprocess.run(["xcrun", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()


def sh(cmd, log):
    with open(os.path.join(CODE, log), "w") as fh:
        r = subprocess.run(cmd, cwd=CODE, env=env, stdout=fh, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise RuntimeError("%s failed, see work/fc_haa/%s" % (" ".join(cmd), log))


# %% [markdown]
# ## Build

# %%
sh(["./configure"], "configure.log")
# (name, Delta, mu): the default build and run.F with DELTA or MUDIM defined
builds = [("run", 0.0, 1.0), ("run_d3", 1e3, 1.0), ("run_d7", 1e7, 1.0),
          ("run_mu05", 0.0, 0.5), ("run_mu2", 0.0, 2.0), ("run_mu5", 0.0, 5.0)]
for name, delta, mu in builds[1:]:
    with open(os.path.join(CODE, name + ".F"), "w") as fh:
        if delta:
            fh.write("#define DELTA %.17gD0\n" % delta)
        if mu != 1.0:
            fh.write("#define MUDIM %.17gD0\n" % mu ** 2)
        fh.write('#include "run.F"\n')
sh(["make"] + [b[0] for b in builds], "make.log")
print("built:", ", ".join(b[0] for b in builds))

# %% [markdown]
# ## Run and compare

# %%
def run(name):
    sh(["./" + name, "uuu", "2.5"], name + ".out")
    out = os.path.join(CODE, name + ".uuu.00002", "0000001")
    lines = open(out).read().splitlines()
    vals = [tuple(float(x) for x in ln[2:].split()) for i, ln in enumerate(lines)
            if ln.startswith("|+") and lines[i - 1].startswith("| ")]
    tree = {v[0] for v in vals}
    loop = {v[1] for v in vals}
    assert len(vals) == 4, out
    return vals[0], max(tree) - min(tree), max(loop) - min(loop)


with open(os.path.join(HERE, "results", "nlo_width.csv")) as fh:
    rows = list(csv.reader(fh))
gamma0 = float([r for r in rows if r[0] == "Gamma0"][0][1])
dos = {float(r[1]): float(r[2]) for r in rows[1:] if r[0] == "1."}   # xi = 1: mu -> delta_OS
e, K = 0.5, 16 * math.pi ** 2
res = []
for name, delta, mu in builds:
    (tree, loop), dtree, dloop = run(name)
    ratio = loop / tree
    pred = dos[1.0] - 2 * e ** 2 / (3 * K) * math.log(mu)
    print("%-8s Delta = %-6g mu = %-4g: Gamma_tree = %.15f (/Gamma_0 - 1 = %.1e), one-loop/tree = %.15f, "
          "delta_OS = %.15f (rel. %.1e)%s;  spread over cos(theta) %.0e, %.0e"
          % (name, delta, mu, 2 * tree, 2 * tree / gamma0 - 1, ratio, pred, ratio / pred - 1,
             "" if mu not in dos else ", nlo_width.csv %.1e" % (ratio / dos[mu] - 1), dtree, dloop))
    res.append([name, delta, mu, 2 * tree, ratio, pred, ratio / pred - 1])
with open(os.path.join(HERE, "results", "nlo_width_fortran.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["build", "Delta", "mu", "Gamma_tree", "delta_OS_fortran", "delta_OS_note", "rel_diff"])
    for r in res:
        w.writerow([r[0]] + ["%.17g" % x for x in r[1:]])
print("written results/nlo_width_fortran.csv")
