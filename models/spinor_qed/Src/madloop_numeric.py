# %% [markdown]
# # Step (5): MadLoop against the one-loop e+ e- -> mu+ mu- interference (MS-bar charge and alpha(0))
#
# Research note models/spinor_qed, step (5).  Runs the MadLoop standalone programs built by run_madloop_check.sh
# (work/ml_<MS|a0>) at the nine points of step (4) with mu_R = 1, and at sqrt(s) = 6, t = -8 with mu_R = 1/2, 2, 5.
# e = 1, m_e = 1, m_mu = 1.7 (pole masses: the UFOs have on-shell mass and field counterterms).
#
# MadLoop returns the Born and the virtual averaged over the initial spins (1/4):
#   born = B(4)/4,   finite = Re W/2,   1eps = Re(1/eps coefficient of W)/2   (W = sum_spins M0^* M1).
# Its loop numerators are four-dimensional with NLOCT's R2 vertices and the external states are four-dimensional, so the
# prediction is the four-dimensional-spin-sum value of Eq. (17):
#   K W^(4)(mu = 1) = K W(CDR, mu = 1) + 16 [f_IR(s; m_e) + f_IR(s; m_mu) + G(t) - G(u)]   (K = (4 pi)^2, e = 1),
# with K W(CDR) from the note's formulas evaluated with COLLIER (results/scat_collier.csv, total) and the bracket of
# Eqs. (16), (17) with mpmath.  The mu-dependence (mu_UV = mu_IR = mu_R; the UFO's MU_R):
#   MS (e = e(mu)):        K W^(4)(mu) = K W^(4)(1) + [P - (8/3) B(4)] ln mu^2
#                          (P = IR pole of K W; -(8/3) B(4) ln mu^2 from the MS-bar vacuum polarization of e and mu);
#   a0 (e = e_OS):         K W_OS = K W^(4)(mu) + (4/3) sum_f ln(mu^2/m_f^2) B(4)   (W_OS = W - Pi^R(0) B, Eq. (18)),
#                          which leaves only the IR logarithm P ln mu^2.
# The pole is the same in both schemes and at all mu: 1eps = Re P/(2K).  The CDR value (scat_collier.csv) and the
# FormCalc value (scat_formcalc.csv, four-dimensional spin sums, mu = 1) are shown for comparison.
# Writes results/madloop.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python madloop_numeric.py
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

# %%
import csv
import math
import os
import re
import subprocess
import sys

import mpmath as mp

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
ME, MMU = 1.0, 1.7
KK = (4 * math.pi) ** 2
TOL = 1e-10
mp.mp.dps = 30


def born4(s, t):
    u = 2 * ME ** 2 + 2 * MMU ** 2 - s - t
    sig = ME ** 2 + MMU ** 2
    return 8 / s ** 2 * ((t - sig) ** 2 + (u - sig) ** 2 + 2 * s * sig)


def read(name):
    out = {}
    with open(os.path.join(HERE, "results", name)) as fh:
        for r in csv.DictReader(fh):
            if r["class"].strip() != "total":
                continue
            z = lambda k: complex(float(r["re_" + k]), float(r["im_" + k]))
            out[(round(float(r["s"]), 8), round(float(r["t"]), 8))] = {"pole": z("uv") + z("ir"), "fin": z("fin")}
    return out


cdr = read("scat_collier.csv")          # the note's formulas with COLLIER (CDR)
fc4 = read("scat_formcalc.csv")         # FormCalc + LoopTools (four-dimensional spin sums)
cdr[(16.0, -6.0)]                       # inspect

# %% [markdown]
# ## Eq. (17): the bracket of Eq. (16) with mpmath

# %%
def f_ir(s, m):
    s, m = mp.mpf(s), mp.mpf(m)
    b = mp.sqrt(1 - 4 * m * m / s)
    return (s - 2 * m * m) / (s * b) * (mp.log((1 + b) / (1 - b)) - 1j * mp.pi) - 1


def g_ir(x):
    m2, mm2, x = mp.mpf(ME) ** 2, mp.mpf(MMU) ** 2, mp.mpf(x)
    return (m2 + mm2 - x) * mp.quad(lambda w: 1 / (w * m2 + (1 - w) * mm2 - x * w * (1 - w)), [0, 1])


def bracket(s, t):
    u = 2 * ME ** 2 + 2 * MMU ** 2 - s - t
    return complex(f_ir(s, ME) + f_ir(s, MMU) + g_ir(t) - g_ir(u))


def kw4(s, t, mu, scheme):
    """K W/e^6 with four-dimensional spin sums: {'fin', 'pole'}"""
    c, b4 = cdr[(s, t)], born4(s, t)
    fin = c["fin"] + 16 * bracket(s, t) + (c["pole"] - 8 / 3 * b4) * math.log(mu ** 2)
    if scheme == "a0":
        fin += 4 / 3 * (math.log(mu ** 2 / ME ** 2) + math.log(mu ** 2 / MMU ** 2)) * b4
    return {"fin": fin, "pole": c["pole"]}


kw4(16.0, -6.0, 1.0, "MS"), fc4[(16.0, -6.0)]     # inspect: Eq. (17) against FormCalc

# %% [markdown]
# ## Kinematics and the MadLoop standalone runs

# %%
def momenta(s, t):
    e = math.sqrt(s) / 2
    p, k = math.sqrt(e * e - ME ** 2), math.sqrt(e * e - MMU ** 2)
    c = (t - ME ** 2 - MMU ** 2 + 2 * e * e) / (2 * p * k)
    st = math.sqrt(1 - c * c)
    return c, [(e, 0, 0, p), (e, 0, 0, -p), (e, k * st, 0, k * c), (e, -k * st, 0, -k * c)]


def run_madloop(scheme, s, t, mu):
    base = os.path.join(HERE, "work", f"ml_{scheme}", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta(s, t)[1])
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps", "2eps")}

# %% [markdown]
# ## Inspect: the diagrams that MadLoop evaluates (drawn when MadGraph wrote the standalone code)

# %%
if INTERACTIVE:
    import shutil
    import tempfile
    from IPython.display import Image, display
    GS = shutil.which("gs") or "/opt/homebrew/bin/gs"
    with open(os.path.join(HERE, "work", "ml_MS.log")) as fh:
        print("ml_MS:", next(line.strip() for line in fh if "Contributing diagrams" in line))
    base = os.path.join(HERE, "work", "ml_MS", "SubProcesses")
    dML = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    tmpML = tempfile.mkdtemp()
    for ps in ("born_matrix.ps", "loop_matrix.ps"):
        subprocess.run([GS, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                        "-sOutputFile=" + os.path.join(tmpML, ps[:-3] + "_%02d.png"), os.path.join(dML, ps)], check=True)
        for png in sorted(f for f in os.listdir(tmpML) if f.startswith(ps[:-3] + "_")):
            display(Image(filename=os.path.join(tmpML, png)))

# %% [markdown]
# ## MadLoop at the nine points (mu_R = 1) and at several mu_R

# %%
POINTS = sorted(cdr)
runs = [(s, t, 1.0) for s, t in POINTS] + [(36.0, -8.0, mu) for mu in (0.5, 2.0, 5.0)]
rows, worst = [], {}
print(f"{'scheme':6} {'sqrt(s)':>7} {'t':>6} {'mu_R':>5} {'finite (MadLoop)':>22} {'prediction':>22} {'rel.dev':>8} "
      f"{'born dev':>8} {'1eps dev':>8} {'CDR dev':>8}")
for scheme in ("MS", "a0"):
    for s, t, mu in runs:
        v = run_madloop(scheme, s, t, mu)
        pr = kw4(s, t, mu, scheme)
        b4 = born4(s, t)
        fin_pred, pole_pred, born_pred = pr["fin"].real / (2 * KK), pr["pole"].real / (2 * KK), b4 / 4
        dfin = abs(v["finite"] - fin_pred) / abs(fin_pred)
        dborn = abs(v["born"] - born_pred) / born_pred
        dpole = abs(v["1eps"] - pole_pred) / abs(pole_pred)
        # the CDR value at the same mu and scheme (Eq. (17) not applied): MadLoop is not CDR
        fin_cdr = fin_pred - 16 * bracket(s, t).real / (2 * KK)
        dcdr = abs(v["finite"] - fin_cdr) / abs(fin_cdr)
        ok = dfin < TOL and dborn < TOL and dpole < TOL and v["2eps"] == 0
        print(f"{scheme:6} {math.sqrt(s):7.1f} {t:6.1f} {mu:5.1f} {v['finite']:+22.15e} {fin_pred:+22.15e} {dfin:8.1e} "
              f"{dborn:8.1e} {dpole:8.1e} {dcdr:8.1e}" + ("" if ok else "   <- check"))
        for k, x in (("finite", dfin), ("born", dborn), ("1eps", dpole)):
            worst[(scheme, k)] = max(worst.get((scheme, k), 0.0), x)
        worst[(scheme, "CDR (no Eq. 17)")] = max(worst.get((scheme, "CDR (no Eq. 17)"), 0.0), dcdr)
        rows.append([scheme, math.sqrt(s), momenta(s, t)[0], s, t, mu, v["born"], v["finite"], v["1eps"], v["2eps"],
                     born_pred, fin_pred, pole_pred, fin_cdr, dborn, dfin, dpole, dcdr])
fc_dev = max(abs(kw4(s, t, 1.0, "MS")["fin"] - fc4[(s, t)]["fin"]) / abs(fc4[(s, t)]["fin"]) for s, t in POINTS)
print("max relative deviation:", {f"{a}/{b}": f"{x:.1e}" for (a, b), x in worst.items()})
print(f"prediction (COLLIER CDR + Eq. (17)) against FormCalc at mu = 1: {fc_dev:.1e}")

with open(os.path.join(HERE, "results", "madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["scheme", "sqrts", "costheta", "s", "t", "mu_R", "born_madloop", "finite_madloop", "eps1_madloop", "eps2_madloop",
                "born_pred", "finite_pred", "eps1_pred", "finite_cdr", "reldev_born", "reldev_finite", "reldev_eps1", "reldev_cdr"])
    w.writerows(rows)
print("wrote results/madloop.csv")
