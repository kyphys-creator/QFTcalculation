# %% [markdown]
# # Step (8): e+ e- -> hadrons with MadGraph5_aMC@NLO (NLO for u ubar and t tbar, LO events for the thrust distribution)
#
# Research note models/qcd, step (8).  All runs: fixed-energy beams (lpp = 0), alpha_s = aS = 0.118 at a fixed scale 91.188 (MadGraph
# runs aS from M_Z), e = 1 (alpha = 1/(4 pi)), m_t = 1 (pole mass, step (5) UFO), no jet cuts.
# (1) aMC@NLO, fixed order: e+ e- > u u~ [QCD] at sqrt(s) = 10 and e+ e- > t t~ [QCD] at beta = 0.3, 0.5, 0.7, 0.9 with the NLO UFO of step (5).
#     MadGraph5_aMC@NLO's NLO templates (fks_singular.f, ewsudakov_functions_dummy.f) and its launch need M_Z and M_W: the model has no
#     Z or W, so a work copy of the UFO gets dummy masses MZ = 91.188, MW = 80.379 and inert Z, W particles (no vertices).  The default jet
#     cut ptj = 10 GeV would remove the whole phase space at these energies: ptj = 0, etaj = -1.
# (2) MadEvent LO: e+ e- > u u~ g at sqrt(s) = 10 with s_ij > y s for all pairs (mmjj = sqrt(y s), y = 0.01, i.e. thrust T < 1 - y),
#     100000 unweighted events.
# The aMC@NLO log prints the cross section with 4 significant digits (rounding comparable to the statistical error): the full
# value is in the last Events/run_NN/res_<k>.txt: the second line after 'Total ABS and Total:' (the first is the integral of |weights|,
# larger when the FKS subtraction gives negative weights, as for light quarks).
# Writes results/ee_mg5.csv (process, sqrt(s), beta, sigma, error in pb) and work/ee_mg5_thrust.txt (thrust of each event).
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python ee_mg5.py [--parse]   (about 4 minutes; --parse re-reads existing runs).
# Interactive: "Run Cell" in VS Code.

# %%
import csv
import glob
import gzip
import math
import os
import re
import shutil
import subprocess
import sys

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
WORK = os.path.join(HERE, "work")
MG5 = os.path.expanduser("~/hep/bin/mg5_aMC")
ENV = dict(os.environ, PATH=os.path.expanduser("~/hep/bin") + ":" + os.environ["PATH"])
if "SDKROOT" not in ENV:
    ENV["SDKROOT"] = subprocess.run(["xcrun", "--show-sdk-path"], capture_output=True, text=True).stdout.strip()
BETAS = (0.3, 0.5, 0.7, 0.9)
SQRTS_UU = 10.0
Y_CUT = 0.01
NEV = 100000
SEEDS = (11, 22, 33, 44)      # aMC@NLO's quoted error can underestimate the run-to-run scatter: four seeds per point
PARSE_ONLY = "--parse" in sys.argv or os.environ.get("EE_MG5_PARSE") == "1"     # EE_MG5_PARSE=1 for a cell-by-cell check

# %% [markdown]
# ## Work copies of the UFOs

# %%
amc = os.path.join(WORK, "QCD_NLO_UFO_amc")
if os.path.isdir(amc):
    shutil.rmtree(amc)
shutil.copytree(os.path.join(HERE, "generated", "QCD_NLO_UFO"), amc)
with open(os.path.join(amc, "parameters.py"), "a") as fh:
    fh.write("\n# research note models/qcd, step (8): dummy M_Z, M_W for MadGraph5_aMC@NLO's NLO templates (no particle couples to them)\n"
             "MZ = Parameter(name = 'MZ', nature = 'external', type = 'real', value = 91.188, texname = '\\\\text{MZ}', lhablock = 'MASS', lhacode = [ 23 ])\n"
             "MW = Parameter(name = 'MW', nature = 'external', type = 'real', value = 80.379, texname = '\\\\text{MW}', lhablock = 'MASS', lhacode = [ 24 ])\n")
with open(os.path.join(amc, "particles.py"), "a") as fh:
    fh.write("\n# research note models/qcd, step (8): inert Z and W (no vertices), so that coupl.inc declares mdl_MZ, mdl_MW\n"
             "Z = Particle(pdg_code = 23, name = 'Z', antiname = 'Z', spin = 3, color = 1, mass = Param.MZ, width = Param.ZERO,\n"
             "             texname = 'Z', antitexname = 'Z', charge = 0, GhostNumber = 0)\n"
             "W__plus__ = Particle(pdg_code = 24, name = 'W+', antiname = 'W-', spin = 3, color = 1, mass = Param.MW, width = Param.ZERO,\n"
             "                     texname = 'W+', antitexname = 'W-', charge = 1, GhostNumber = 0)\n"
             "W__minus__ = W__plus__.anti()\n")
lo = os.path.join(WORK, "QCD_UFO")
if os.path.isdir(lo):
    shutil.rmtree(lo)
shutil.copytree(os.path.join(HERE, "generated", "QCD_UFO"), lo)
print("UFO work copies:", amc, lo)

# %% [markdown]
# ## aMC@NLO at fixed order

# %%
def nlo_launch(outdir, ebeam, seed):
    return ("launch %s\nfixed_order=ON\ndone\nset lpp1 0\nset lpp2 0\nset ebeam1 %.15g\nset ebeam2 %.15g\nset fixed_ren_scale True\n"
            "set fixed_fac_scale True\nset mur_ref_fixed 91.188\nset muf_ref_fixed 91.188\nset req_acc_FO 0.0002\nset ptj 0.0\nset etaj -1.0\n"
            "set iseed %d\nset aS 0.118\ndone\n") % (outdir, ebeam, ebeam, seed)


def run_mg5(name, text):
    cmd = os.path.join(WORK, name + ".mg5")
    with open(cmd, "w") as fh:
        fh.write("set automatic_html_opening False\n" + text)
    log = os.path.join(WORK, name + ".log")
    with open(log, "w") as fh:
        subprocess.run([MG5, cmd], cwd=HERE, stdout=fh, stderr=subprocess.STDOUT, env=ENV, check=False)
    return open(log).read()


def full_result(outdir, run):
    """sigma, error (pb) from the last res_<k>.txt of Events/run_<run>: after 'Total ABS and Total:' the first line is the integral of
    |weights| and the second the cross section (they differ when the FKS subtraction gives negative weights)"""
    files = glob.glob(os.path.join(outdir, "Events", "run_%02d" % run, "res_*.txt"))
    last = max(files, key=lambda f: int(re.search(r"res_(\d+)\.txt", f).group(1)))
    m = re.search(r"Total:\s*\n\s*[0-9.eE+-]+\s*\+-\s*[0-9.eE+-]+[^\n]*\n\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)", open(last).read())
    return float(m.group(1)), float(m.group(2))


rows = []
uu_dir = os.path.join(WORK, "ee_amc_uu")
if not PARSE_ONLY:
    run_mg5("ee_amc_uu", "import model ./work/QCD_NLO_UFO_amc\ngenerate e+ e- > u u~ [QCD]\noutput %s -f\n" % uu_dir
            + "".join(nlo_launch(uu_dir, SQRTS_UU / 2, sd) for sd in SEEDS))
for j, sd in enumerate(SEEDS):
    res = full_result(uu_dir, j + 1)
    print("u ubar, NLO, seed", sd, ":", res)
    rows.append(["uu_nlo", SQRTS_UU, 1.0, res[0], res[1], sd])
tt_dir = os.path.join(WORK, "ee_amc_tt")
text = "import model ./work/QCD_NLO_UFO_amc\ngenerate e+ e- > t t~ [QCD]\noutput %s -f\n" % tt_dir
for b in BETAS:
    for sd in SEEDS:
        text += nlo_launch(tt_dir, 1 / math.sqrt(1 - b * b), sd)
if not PARSE_ONLY:
    run_mg5("ee_amc_tt", text)
for i, b in enumerate(BETAS):
    for j, sd in enumerate(SEEDS):
        r = full_result(tt_dir, i * len(SEEDS) + j + 1)
        print("t tbar, NLO, beta", b, "seed", sd, ":", r)
        rows.append(["tt_nlo", 2 / math.sqrt(1 - b * b), b, r[0], r[1], sd])

# %% [markdown]
# ## MadEvent LO: e+ e- > u u~ g, thrust < 1 - y

# %%
uug_dir = os.path.join(WORK, "ee_me_uug")
txt = "" if PARSE_ONLY else run_mg5("ee_me_uug", ("import model ./work/QCD_UFO\ngenerate e+ e- > u u~ g\noutput %s -f\nlaunch %s\n0\nset lpp1 0\nset lpp2 0\n"
                            "set ebeam1 %.15g\nset ebeam2 %.15g\nset nevents %d\nset fixed_ren_scale True\nset fixed_fac_scale True\nset scale 91.188\n"
                            "set use_syst False\nset ptj 0\nset drjj 0\nset etaj -1\nset mmjj %.15g\nset aS 0.118\n0\n")
              % (uug_dir, uug_dir, SQRTS_UU / 2, SQRTS_UU / 2, NEV, math.sqrt(Y_CUT) * SQRTS_UU))
lhe = os.path.join(uug_dir, "Events", "run_01", "unweighted_events.lhe.gz")
thrusts, xsec = [], None
with gzip.open(lhe, "rt") as fh:
    ev = None
    for line in fh:
        if "Integrated weight (pb)" in line:
            xsec = float(line.split(":")[1])
        if line.startswith("<event"):
            ev = []
        elif line.startswith("</event"):
            es = [float(r[9]) for r in ev[1:] if r[1] == "1"]       # final-state energies
            thrusts.append(2 * max(es) / SQRTS_UU)
            ev = None
        elif ev is not None:
            ev.append(line.split())
with open(os.path.join(WORK, "ee_mg5_thrust.txt"), "w") as fh:
    fh.write("\n".join("%.15g" % t for t in thrusts) + "\n")
m = re.search(r"Cross-section :\s*([0-9.eE+-]+)\s*\+-\s*([0-9.eE+-]+)", txt or open(os.path.join(WORK, "ee_me_uug.log")).read())
rows.append(["uug_lo_ycut", SQRTS_UU, Y_CUT, xsec, float(m.group(2)) if m else float("nan"), 0])
print(f"u ubar g: {len(thrusts)} events, sigma = {xsec} pb (log: {m.group(1) if m else '?'} +- {m.group(2) if m else '?'})")
with open(os.path.join(HERE, "results", "ee_mg5.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "sqrt_s", "beta_or_y", "sigma_pb", "error_pb", "seed"])
    w.writerows(rows)
print("wrote results/ee_mg5.csv, work/ee_mg5_thrust.txt")
