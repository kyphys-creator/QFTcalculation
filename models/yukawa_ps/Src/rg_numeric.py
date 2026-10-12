# %% [markdown]
# # Step (7): the RG coefficients from the mu-dependence of the S-matrix elements and pole masses (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (7), Eq. (rgfit), App. rgfit.  m = 1, M = 0.7, y = lambda = 1 at mu = m.
# A physical quantity written with mass parameters (MS-bar or pole) and the MS-bar couplings y(mu), lambda(mu) does not
# depend on mu.  Writing it as tree(parameters) + Y(mu), with Y the one-loop part at fixed parameters, gives
#     (A) phi phi -> phi phi, M0 = -lambda:              mu dY_A/dmu = beta_lambda;
#     (B) psi psibar -> phi phi, (4 pi)^2 M = a vbar u + b vbar k1slash u, tree b0 = y^2 (1/X - 1/W), X = t - M^2, W = u - M^2:
#         mu dY_a/dmu = 0,   mu dY_b/dmu = -(4 pi)^2 [ (2 b0/y) beta_y + 2 M y^2 (1/X^2 - 1/W^2) gamma_M ];
#     (C) pole masses:  m_p^2 = m^2 + Sigma_phi(m^2),  M_p = M [1 + Sigma_V(M^2) + Sigma_S(M^2)]:
#         gamma_m = -mu dSigma_phi/dmu,  gamma_M = -M mu d(Sigma_V + Sigma_S)/dmu.
# Two parametrizations: (i) MS-bar masses: Y_A = M1 + 4 lambda y^2 [B0^MM + m^2 B0^MM'](m^2)/(4pi)^2 (the residue), Y_a = a_phys,
# Y_b = b + (4 pi)^2 (dR_psi + dR_phi) b0 (the mass shift of eq:MphysB moves into the tree b0(M)); expected beta_lambda, beta_y,
# gamma_M of Eq. (8);  (ii) pole masses: Y_A as in (i), Y = (a_phys, b_phys) of eq:MphysB; expected gamma_M = 0.
# The slope of Y at each point is [Y(2) - Y(1/2)]/(2 ln 2) (Y is linear in ln mu at fixed parameters).  B is fitted through the
# interference with the tree, F = (1/4) Re sum M0* M1 = b0/(4 (4pi)^2) [2 M (t - u) Y_a + 2 (X W - m^4) Y_b] (the MadLoop
# finite part), linear in (beta_y, gamma_M); the six points fix both by least squares.
# Tools: FeynCalc + Package-X and FeynCalc + LoopTools (results/rg_feyncalc*.csv, rg_feyncalc.wl), COLLIER (work/rg_collier ->
# results/rg_collier*.csv), MadLoop (work/ml_MSbar_<A|B>: Eqs. (13), (18); work/ml_OS_<A|B>: Eqs. (16), (20), NLOCT on-shell
# counterterms), all at mu = 1/2, 1, 2.  For the MS-bar MadLoop and the FeynCalc/COLLIER amplitudes the residue and mass-shift
# terms are added from their Feynman-parameter integrals (mpmath, B0(mu) = B0(m) + ln mu^2, B1(mu) = B1(m) - (1/2) ln mu^2);
# the on-shell MadLoop contains them through NLOCT's counterterms.
# Also: the three coupling structures of beta_lambda (phi bubbles 3 lambda^2 and fermion boxes -48 y^4 from COLLIER, the residue
# 8 lambda y^2 from MadLoop OS - MS-bar), and the figure: the S-matrix elements at sqrt(s) = 5m, cos(theta) = 0.3 for
# mu = m/4 ... 4m with fixed parameters and with the one-loop running of Eq. (9) (App. rgfit).
# Writes results/rg_comparison.csv and ../figs/rg_d4.pdf.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python rg_numeric.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import csv
import math
import os
import re
import subprocess
import sys

import mpmath as mp
import numpy as np

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
MPHI, MPSI, Y, LAM = 1.0, 0.7, 1.0, 1.0
m2, bm2 = MPHI ** 2, MPSI ** 2
K = (4 * math.pi) ** 2
mp.mp.dps = 30
MUS = (0.5, 1.0, 2.0)
POINTS = [(rs, ct) for rs in (2.5, 5.0, 10.0) for ct in (0.3, 0.9)]
EXPECT = {"beta_lambda": (3 * LAM ** 2 + 8 * LAM * Y ** 2 - 48 * Y ** 4) / K, "beta_y": 5 * Y ** 3 / K,
          "gamma_M": -Y ** 2 * MPSI / K, "gamma_m": (LAM * m2 + 4 * Y ** 2 * m2 - 8 * Y ** 2 * bm2) / K}
EXPECT

# %% [markdown]
# ## Two-point functions at mu = m (Feynman parameters) and their mu-dependence

# %%
def dx(x, p2, ma2, mb2):
    return x * mb2 + (1 - x) * ma2 - x * (1 - x) * p2


def b0(p2, ma2, mb2):
    return float(-mp.quad(lambda x: mp.log(dx(x, p2, ma2, mb2)), [0, 1]))


def b1(p2, ma2, mb2):
    return float(mp.quad(lambda x: x * mp.log(dx(x, p2, ma2, mb2)), [0, 1]))


def b0p(p2, ma2, mb2):
    return float(mp.quad(lambda x: x * (1 - x) / dx(x, p2, ma2, mb2), [0, 1]))


def b1p(p2, ma2, mb2):
    return float(-mp.quad(lambda x: x * x * (1 - x) / dx(x, p2, ma2, mb2), [0, 1]))


SP = {"B0phi": b0(m2, bm2, bm2), "B0pphi": b0p(m2, bm2, bm2), "B0psi": b0(bm2, bm2, m2), "B1psi": b1(bm2, bm2, m2),
      "B0ppsi": b0p(bm2, bm2, m2), "B1ppsi": b1p(bm2, bm2, m2)}


def conv(mu):
    """(4 pi)^2 times: residue of phi (term of Y_A), dR_psi, dR_phi, (M_p - M)/M at the scale mu"""
    L = math.log(mu ** 2)
    res_a = 4 * LAM * Y ** 2 * (SP["B0phi"] + L + m2 * SP["B0pphi"])
    dr_psi = Y ** 2 * (SP["B1psi"] - L / 2 + 2 * bm2 * (SP["B0ppsi"] + SP["B1ppsi"]))
    dr_phi = -2 * Y ** 2 * (SP["B0phi"] + L + m2 * SP["B0pphi"])
    dm_psi = Y ** 2 * (SP["B0psi"] + SP["B1psi"] + L / 2)
    return res_a, dr_psi, dr_phi, dm_psi


def kin(proc, rs, ct):
    e = rs / 2
    st = math.sqrt(1 - ct * ct)
    if proc == "A":
        p = math.sqrt(e * e - m2)
        mom = [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * ct), (e, -p * st, 0, -p * ct)]
        t = -2 * p * p * (1 - ct)
        return mom, rs * rs, t, 4 * m2 - rs * rs - t
    p, k = math.sqrt(e * e - bm2), math.sqrt(e * e - m2)
    mom = [(e, 0, 0, p), (e, 0, 0, -p), (e, k * st, 0, k * ct), (e, -k * st, 0, -k * ct)]
    t = bm2 + m2 - 2 * (e * e - p * k * ct)
    return mom, rs * rs, t, 2 * bm2 + 2 * m2 - rs * rs - t


def bstruct(rs, ct):
    """b0, 1/X^2 - 1/W^2, S+ = 1/X + 1/W, and the interference weights of a and b"""
    _, s, t, u = kin("B", rs, ct)
    X, W = t - bm2, u - bm2
    b0t = Y ** 2 * (1 / X - 1 / W)
    wa = b0t / (4 * K) * 2 * MPSI * (t - u)
    wb = b0t / (4 * K) * 2 * (X * W - m2 ** 2)
    return b0t, 1 / X ** 2 - 1 / W ** 2, 1 / X + 1 / W, wa, wb


def y_case(case, a, b, rs, ct, mu):
    """(Y_a, Y_b) of the parametrization: (i) MS-bar masses, (ii) pole masses; a, b = MS-bar amplitude at the scale mu"""
    b0t, dsq, splus, _, _ = bstruct(rs, ct)
    _, dr_psi, dr_phi, dm_psi = conv(mu)
    ya = a - Y ** 2 * MPSI * dm_psi * splus
    yb = b + (dr_psi + dr_phi) * b0t
    if case == "ii":
        yb -= 2 * bm2 * Y ** 2 * dm_psi * dsq
    return ya, yb

# %% [markdown]
# ## COLLIER at the six points and three scales, the mu scan, and the pole-mass functions

# %%
SCAN = np.geomspace(0.25, 4.0, 33)
nodes = [(rs, ct, mu) for rs, ct in POINTS for mu in MUS] + [(5.0, 0.3, mu) for mu in SCAN]
work = os.path.join(HERE, "work")
with open(os.path.join(work, "rg_nodes.txt"), "w") as fh:
    fh.writelines("%.17e %.17e %.17e\n" % n for n in nodes)
with open(os.path.join(work, "rg_mus.txt"), "w") as fh:
    fh.writelines("%.17e\n" % mu for mu in MUS)
subprocess.run([os.path.join(work, "rg_collier"), "rg_nodes.txt", os.path.join("..", "results", "rg_collier.csv"), "rg_mus.txt",
                os.path.join("..", "results", "rg_collier_pole.csv")], cwd=work, check=True, capture_output=True)
col = {}
with open(os.path.join(HERE, "results", "rg_collier.csv")) as fh:
    for r in csv.DictReader(fh):
        col[(round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6), round(float(r["mu"]), 9))] = \
            {k: float(r[k]) for k in ("re_a", "re_b", "re_mA", "re_mA_lam", "re_mA_y4", "im_a", "im_b", "im_mA")}
colpole = {round(float(r["mu"]), 9): {k: float(v) for k, v in r.items()} for r in csv.DictReader(open(os.path.join(HERE, "results", "rg_collier_pole.csv")))}
fc = {}
with open(os.path.join(HERE, "results", "rg_feyncalc.csv")) as fh:
    for r in csv.DictReader(fh):
        fc[(round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6), round(float(r["mu"]), 9))] = {k: float(v) for k, v in r.items()}
fcpole = {round(float(r["mu"]), 9): {k: float(v) for k, v in r.items()} for r in csv.DictReader(open(os.path.join(HERE, "results", "rg_feyncalc_pole.csv")))}
col[(5.0, 0.3, 1.0)]          # inspect

# %% [markdown]
# ## MadLoop at the six points and three scales

# %%
if INTERACTIVE:          # the diagrams that MadLoop evaluates (drawn when MadGraph wrote the standalone code), before the runs
    import shutil
    import tempfile
    from IPython.display import Image, display
    gs = shutil.which("gs") or "/opt/homebrew/bin/gs"
    for name in ("ml_OS_A", "ml_OS_B"):
        base = os.path.join(work, name, "SubProcesses")
        d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
        tmp = tempfile.mkdtemp()
        for ps in ("born_matrix.ps", "loop_matrix.ps"):
            subprocess.run([gs, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                            "-sOutputFile=" + os.path.join(tmp, ps[:-3] + "_%02d.png"), os.path.join(d, ps)], check=True)
        for png in sorted(os.listdir(tmp)):
            display(Image(filename=os.path.join(tmp, png)))

# %%
def run_madloop(name, proc, rs, ct, mu):
    base = os.path.join(work, name, "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in kin(proc, rs, ct)[0])
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return float(re.search(r"Matrix element finite\s*=\s*(\S+)", out).group(1))


ml = {(name, rs, ct, mu): run_madloop(name, name[-1], rs, ct, mu)
      for name in ("ml_MSbar_A", "ml_OS_A", "ml_MSbar_B", "ml_OS_B") for rs, ct in POINTS for mu in MUS}
len(ml)

# %% [markdown]
# ## The one-loop parts Y for each tool and parametrization, and the agreement of the tools

# %%
def tool_values(tool, rs, ct, mu):
    """{'YA': ..., 'F_i': ..., 'F_ii': ..., 'Ya_i': ..., 'Yb_i': ..., 'Ya_ii': ..., 'Yb_ii': ...} (Ya, Yb only where a, b are known)"""
    key = (rs, ct, mu)
    res_a = conv(mu)[0]
    _, _, _, wa, wb = bstruct(rs, ct)
    out = {}
    if tool in ("px", "lt", "collier"):
        if tool == "collier":
            a, b, mA = col[key]["re_a"], col[key]["re_b"], col[key]["re_mA"]
        else:
            a, b, mA = fc[key]["re_a_" + tool], fc[key]["re_b_" + tool], fc[key]["re_mA_" + tool]
        out["YA"] = (mA + res_a) / K
        for case in ("i", "ii"):
            ya, yb = y_case(case, a, b, rs, ct, mu)
            out["Ya_" + case], out["Yb_" + case] = ya, yb
            out["F_" + case] = wa * ya + wb * yb
        out["M1"], out["a"], out["b"] = mA, a, b
    elif tool == "madloop_msbar":
        out["YA"] = ml[("ml_MSbar_A", rs, ct, mu)] / (-LAM) + res_a / K          # finite = -lambda Re M1
        fin = ml[("ml_MSbar_B", rs, ct, mu)]                                      # = wa a + wb b (MS-bar)
        for case in ("i", "ii"):
            da, db = y_case(case, 0.0, 0.0, rs, ct, mu)                       # the residue and mass-shift terms
            out["F_" + case] = fin + wa * da + wb * db
        out["M1"] = K * ml[("ml_MSbar_A", rs, ct, mu)] / (-LAM)
    elif tool == "madloop_os":
        out["YA"] = ml[("ml_OS_A", rs, ct, mu)] / (-LAM)
        out["F_ii"] = ml[("ml_OS_B", rs, ct, mu)]
    return out


TOOLS = ("px", "lt", "collier", "madloop_msbar", "madloop_os")
vals = {(tool, rs, ct, mu): tool_values(tool, rs, ct, mu) for tool in TOOLS for rs, ct in POINTS for mu in MUS}
dev = {}
for tool in ("px", "lt", "madloop_msbar"):
    d = 0.0
    for rs, ct in POINTS:
        for mu in MUS:
            ref, v = vals[("collier", rs, ct, mu)], vals[(tool, rs, ct, mu)]
            d = max(d, abs(v["M1"] - ref["M1"]) / abs(ref["M1"]), abs(v["F_i"] - ref["F_i"]) / abs(ref["F_i"]))
    dev[tool] = d
d_os = max(max(abs(vals[("madloop_os", rs, ct, mu)][q] - vals[("collier", rs, ct, mu)][q]) / abs(vals[("collier", rs, ct, mu)][q])
               for q in ("YA", "F_ii")) for rs, ct in POINTS for mu in MUS)
print("max relative deviation from COLLIER (18 values each of M1 and F):", {k: f"{v:.1e}" for k, v in dev.items()},
      f" on-shell MadLoop vs eq:Mphys/eq:MphysB: {d_os:.1e}")
d_im = max(abs(col[(rs, ct, mu)]["im_" + q] - col[(rs, ct, 1.0)]["im_" + q]) for rs, ct in POINTS for mu in MUS for q in ("a", "b", "mA"))
print(f"imaginary parts (COLLIER): largest change with mu {d_im:.1e}")

# %% [markdown]
# ## Slopes in ln(mu) and the fits

# %%
LN = 2 * math.log(2.0)
# at fixed parameters Y is linear in ln(mu): Y(m) is the mean of Y(m/2) and Y(2m)
lin = max(abs(v[(tool, rs, ct, 1.0)][q] - 0.5 * (v[(tool, rs, ct, 0.5)][q] + v[(tool, rs, ct, 2.0)][q])) / abs(v[(tool, rs, ct, 1.0)][q])
          for v in (vals,) for tool in TOOLS for rs, ct in POINTS for q in vals[(tool, rs, ct, 1.0)])
print(f"linearity in ln(mu): max |Y(m) - [Y(m/2) + Y(2m)]/2| / |Y(m)| = {lin:.1e}")


def slope(tool, q, rs, ct):
    return (vals[(tool, rs, ct, 2.0)][q] - vals[(tool, rs, ct, 0.5)][q]) / LN


rows, fits = [], {}
for case in ("i", "ii"):
    for tool in TOOLS:
        if tool == "madloop_os" and case == "i":
            continue
        # (A): beta_lambda = slope of Y_A (the same at all points)
        sA = [slope(tool, "YA", rs, ct) for rs, ct in POINTS]
        bl = float(np.mean(sA))
        # (B): slope of F = wb * (-(4 pi)^2) [(2 b0/y) beta_y + 2 M y^2 (1/X^2 - 1/W^2) gamma_M]
        A, rhs = [], []
        for rs, ct in POINTS:
            b0t, dsq, _, _, wb = bstruct(rs, ct)
            A.append([-K * wb * 2 * b0t / Y, -K * wb * 2 * MPSI * Y ** 2 * dsq])
            rhs.append(slope(tool, "F_" + case, rs, ct))
        (by, gM), resid, _, _ = np.linalg.lstsq(np.array(A), np.array(rhs), rcond=None)
        res_max = float(np.max(np.abs(np.array(A) @ np.array([by, gM]) - np.array(rhs))) / np.max(np.abs(rhs)))
        fits[(case, tool)] = {"beta_lambda": bl, "beta_y": by, "gamma_M": gM, "spreadA": float(np.ptp(sA)), "resB": res_max}
        if tool in ("px", "lt", "collier"):
            fits[(case, tool)]["a_slope"] = max(abs(slope(tool, "Ya_" + case, rs, ct)) for rs, ct in POINTS)
for (case, tool), f in fits.items():
    gM_exp = EXPECT["gamma_M"] if case == "i" else 0.0
    dl = abs(f["beta_lambda"] - EXPECT["beta_lambda"]) / abs(EXPECT["beta_lambda"])
    dy = abs(f["beta_y"] - EXPECT["beta_y"]) / EXPECT["beta_y"]
    dg = abs(f["gamma_M"] - gM_exp) / abs(EXPECT["gamma_M"])
    extra = f"  max |slope Y_a| {f['a_slope']:.1e}" if "a_slope" in f else ""
    print(f"({case:2s}) {tool:14s} beta_lambda rel. {dl:.1e}  beta_y rel. {dy:.1e}  gamma_M {'rel.' if case == 'i' else 'abs/|exp|'} {dg:.1e}"
          f"  (fit residual {f['resB']:.1e}){extra}")
    rows.append([case, tool, f["beta_lambda"] * K, f["beta_y"] * K, f["gamma_M"] * K, dl, dy, dg])

# %% [markdown]
# ## The three coupling structures of beta_lambda, and gamma_m, gamma_M from the pole masses

# %%
s_lam = np.mean([(col[(rs, ct, 2.0)]["re_mA_lam"] - col[(rs, ct, 0.5)]["re_mA_lam"]) / LN for rs, ct in POINTS])
s_y4 = np.mean([(col[(rs, ct, 2.0)]["re_mA_y4"] - col[(rs, ct, 0.5)]["re_mA_y4"]) / LN for rs, ct in POINTS])
s_res = np.mean([K * (slope("madloop_os", "YA", rs, ct) - (vals[("madloop_msbar", rs, ct, 2.0)]["M1"] - vals[("madloop_msbar", rs, ct, 0.5)]["M1"]) / LN / K)
                 for rs, ct in POINTS])
print(f"beta_lambda structures (times (4 pi)^2): phi bubbles {s_lam:.15f} (3 lambda^2), fermion boxes {s_y4:.15f} (-48 y^4),"
      f" residue (MadLoop OS - MS-bar) {s_res:.15f} (8 lambda y^2)")


def pole_slopes(tool):
    if tool == "collier":
        sig = {mu: -(2 * Y ** 2 * (m2 * colpole[mu]["re_B0MM_m2"] - 2 * colpole[mu]["re_A0M"]) + LAM / 2 * colpole[mu]["re_A0m"])
               for mu in MUS}
        vs = {mu: Y ** 2 * (colpole[mu]["re_B0Mm_M2"] + colpole[mu]["re_B1Mm_M2"]) for mu in MUS}
    else:
        sig = {mu: fcpole[mu]["re_sigphi_" + tool] for mu in MUS}
        vs = {mu: fcpole[mu]["re_sigV_" + tool] + fcpole[mu]["re_sigS_" + tool] for mu in MUS}
    gm = -(sig[2.0] - sig[0.5]) / LN / K
    gM = -MPSI * (vs[2.0] - vs[0.5]) / LN / K
    return gm, gM


for tool in ("px", "lt", "collier"):
    gm, gM = pole_slopes(tool)
    print(f"pole masses, {tool:8s}: gamma_m rel. {abs(gm - EXPECT['gamma_m']) / EXPECT['gamma_m']:.1e},"
          f"  gamma_M rel. {abs(gM - EXPECT['gamma_M']) / abs(EXPECT['gamma_M']):.1e}")
    rows.append(["pole", tool, float("nan"), float("nan"), gM * K, float("nan"), float("nan"), abs(gM - EXPECT["gamma_M"]) / abs(EXPECT["gamma_M"])])
    rows.append(["pole", tool + "_gamma_m", gm * K, float("nan"), float("nan"), abs(gm - EXPECT["gamma_m"]) / EXPECT["gamma_m"], float("nan"), float("nan")])

with open(os.path.join(HERE, "results", "rg_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["case", "tool", "K_beta_lambda_or_K_gamma_m", "K_beta_y", "K_gamma_M", "rel_dev_1", "rel_dev_beta_y", "dev_gamma_M"])
    w.writerows(rows)
print("wrote results/rg_comparison.csv")

# %% [markdown]
# ## Figure: the S-matrix elements at sqrt(s) = 5m, cos(theta) = 0.3 against mu, fixed and running parameters

# %%
R_PLUS, R_MINUS = (1 + math.sqrt(145)) / 3, (1 - math.sqrt(145)) / 3


def running(t):
    """one-loop solution of Eq. (9) and gamma_M: y^2, lambda, M at t = ln(mu/m), from y = lambda = 1, M = 0.7 at mu = m"""
    z = 1 / (1 - 10 * Y ** 2 * t / K)
    y2 = Y ** 2 * z
    c = (LAM / Y ** 2 - R_PLUS) / (LAM / Y ** 2 - R_MINUS)
    zz = c * z ** (math.sqrt(145) / 5)
    r = (R_PLUS - zz * R_MINUS) / (1 - zz)
    return y2, r * y2, MPSI * z ** (-0.1)


def s_matrix(mu, run):
    """phi phi -> phi phi: M_A = M0 + Y_A;  psi psibar -> phi phi: sum|M|^2 = sum|M0|^2 + 2 Re sum M0* M1 = sum|M0|^2 + 8 F,
    in the MS-bar parametrization (i); Y at fixed parameters (COLLIER at the scale mu), tree with the running parameters"""
    t = math.log(mu)
    y2, lam, mm = running(t) if run else (Y ** 2, LAM, MPSI)
    c = col[(5.0, 0.3, round(mu, 9))]
    mA = -lam + (c["re_mA"] + conv(mu)[0]) / K
    _, s, tt, u = kin("B", 5.0, 0.3)
    X, W = tt - mm ** 2, u - mm ** 2
    b0t = y2 * (1 / X - 1 / W)
    tree = b0t ** 2 * 2 * ((tt - bm2) * (u - bm2) - m2 ** 2)          # sum|M0|^2 = b0^2 sum|vbar k1 u|^2
    ya, yb = y_case("i", c["re_a"], c["re_b"], 5.0, 0.3, mu)
    _, _, _, wa, wb = bstruct(5.0, 0.3)
    return mA, tree + 8 * (wa * ya + wb * yb)


ref = s_matrix(1.0, False)
curves = {run: np.array([[(v - r) / r for v, r in zip(s_matrix(mu, run), ref)] for mu in SCAN]) for run in (False, True)}
for j, name in enumerate(("phi phi -> phi phi", "psi psibar -> phi phi")):
    fixed, ran = curves[False][:, j], curves[True][:, j]
    print(f"{name}: max |relative change| for mu = m/4 ... 4m: fixed parameters {np.max(np.abs(fixed)):.2e},"
          f" running {np.max(np.abs(ran)):.2e}  (ends {ran[0]:+.2e}, {ran[-1]:+.2e})")
# the remainder is (1/2) d^2 tree/dt^2 t^2: second derivative of the tree with the running parameters (central differences)
h = 1e-3
d2s = []
for j, name in enumerate(("phi phi -> phi phi", "psi psibar -> phi phi")):
    def tree_run(t, j=j):
        y2, lam, mm = running(t)
        if j == 0:
            return -lam
        _, s, tt, u = kin("B", 5.0, 0.3)
        return (y2 * (1 / (tt - mm ** 2) - 1 / (u - mm ** 2))) ** 2 * 2 * ((tt - bm2) * (u - bm2) - m2 ** 2)
    d2 = (tree_run(h) - 2 * tree_run(0.0) + tree_run(-h)) / h ** 2
    d2s.append(d2)
    pred = 0.5 * d2 * math.log(4.0) ** 2 / ref[j]
    print(f"{name}: (1/2) tree'' ln^2(4)/value = {pred:+.3e}; mean of the two ends {0.5 * (curves[True][0, j] + curves[True][-1, j]):+.3e}")

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
for j, (ax, title) in enumerate(zip(axes, (r"$\phi\phi\to\phi\phi$: $\mathcal{M}_A$", r"$\psi\bar\psi\to\phi\phi$: $\sum|\mathcal{M}_B|^2$"))):
    ax.plot(SCAN, curves[False][:, j], color="C0", ls="--", label="fixed parameters")
    ax.plot(SCAN, curves[True][:, j], color="C1", ls="-", label="running (one loop)")
    ax.plot(SCAN, 0.5 * d2s[j] * np.log(SCAN) ** 2 / ref[j], color="k", ls=":", lw=0.8,
            label=r"$\frac{1}{2}\ddot{\mathcal{M}}^{(0)}\ln^2(\mu/m)$")
    ax.axhline(0, color="0.6", lw=0.5, zorder=0)
    ax.set_xscale("log")
    ax.set_xticks([0.25, 0.5, 1, 2, 4])
    ax.set_xticklabels(["1/4", "1/2", "1", "2", "4"])
    ax.minorticks_off()
    ax.set_xlabel(r"$\mu/m$")
    ax.set_title(title, fontsize=8)
axes[0].set_ylabel(r"relative change from $\mu=m$")
axes[0].legend(fontsize=7)
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "rg_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
