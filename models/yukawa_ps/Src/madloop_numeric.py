# %% [markdown]
# # Step (5): MadLoop against the S-matrix elements (on-shell) and the MS-bar amplitudes (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (5).  Runs the MadLoop standalone programs built by run_madloop_check.sh
# (work/ml_<OS|MSbar>_<A|B>) at the six points of step (4) with mu_R = m, and at sqrt(s) = 5m, cos(theta) = 0.3 with
# mu_R = m/2, 2m, 5m.  m = mu = 1, M = 0.7, y = lambda = 1; the param-card masses are the MS-bar masses for the MS-bar
# UFO and the pole masses for the OS UFO.
#
# MadLoop returns the Born and the finite part of the virtual, averaged over the initial spins and with the
# identical-particle factor 1/2 of the final state:  born = avg sum|M0|^2,  finite = avg sum 2 Re(M0* M1).
# (A) phi phi -> phi phi:  born = lambda^2/2,  finite = M0 Re M1 = -lambda Re M1.
#     MS-bar: (4 pi)^2 M1(mu) = (4 pi)^2 M1(m) + ln(mu/m) (3 lambda^2 - 48 y^4)                   [Eq. (13)]
#     OS:     (4 pi)^2 (M_phys - M0) = (4 pi)^2 M1 + 4 lambda y^2 [B0^MM + m^2 B0^MM'](m^2)
#             + ln(mu/m) (3 lambda^2 + 8 lambda y^2 - 48 y^4)                                         [Eq. (16)]
# (B) psi psibar -> phi phi:  born = (1/8) sum|M0|^2,  finite = (1/4) Re sum M0* M1, with M0 = b0 vbar k1slash u,
#     b0 = y^2 [1/(t-M^2) - 1/(u-M^2)] and (4 pi)^2 M1 = a vbar u + b vbar k1slash u:
#         sum M0* M1 = b0/(4 pi)^2 [a sum (vbar k1 u)* (vbar u) + b sum |vbar k1 u|^2]
#                    = b0/(4 pi)^2 [2 M (t - u) a + 2 ((t-M^2)(u-M^2) - m^4) b].
#     MS-bar: a, b of Eq. (18) (results/scat_collier.csv at mu = m) plus the mu-dependence
#         d a/d ln mu = y^4 M [1/(t-M^2) + 1/(u-M^2)],  d b/d ln mu = y^4 sum_x sigma_x [2M^2/(x-M^2)^2 - 5/(x-M^2)];
#     OS: eq:MphysB (pole masses and residues, App. scatB):
#         a_phys = a - y^4 M (B0 + B1)(M^2) [1/(t-M^2) + 1/(u-M^2)],
#         b_phys = b + [(4 pi)^2 (dR_psi + dR_phi)] b0 - 2 M^2 y^4 (B0 + B1)(M^2) [1/(t-M^2)^2 - 1/(u-M^2)^2],
#         (4 pi)^2 dR_psi = y^2 [B1 + 2 M^2 (B0' + B1')](M^2; M^2, m^2),  (4 pi)^2 dR_phi = -2 y^2 [B0 + m^2 B0'](m^2; M^2, M^2);
#         d b_phys/d ln mu = -10 y^2 b0, d a_phys/d ln mu = 0 (the running of y in the tree).
# The two-point functions at the special points come from their Feynman-parameter integrals (mpmath).
# Writes results/madloop.csv.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python madloop_numeric.py
#
# Batch: as above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

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
MPHI, MPSI, Y, LAM = 1.0, 0.7, 1.0, 1.0
K16 = (4 * math.pi) ** 2
TOL = 1e-10
mp.mp.dps = 30

# %% [markdown]
# ## Two-point functions at the special points (mu = 1)

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


m2, bm2 = MPHI ** 2, MPSI ** 2
SPEC = {
    "B0psi": b0(bm2, bm2, m2), "B1psi": b1(bm2, bm2, m2), "B0ppsi": b0p(bm2, bm2, m2), "B1ppsi": b1p(bm2, bm2, m2),
    "B0phi": b0(m2, bm2, bm2), "B0pphi": b0p(m2, bm2, bm2)}
dRpsi = Y ** 2 * (SPEC["B1psi"] + 2 * bm2 * (SPEC["B0ppsi"] + SPEC["B1ppsi"]))       # (4 pi)^2 (R_psi - 1)
dRphi = -2 * Y ** 2 * (SPEC["B0phi"] + m2 * SPEC["B0pphi"])                           # (4 pi)^2 (R_phi - 1)
dMpsi = Y ** 2 * (SPEC["B0psi"] + SPEC["B1psi"])                                      # (4 pi)^2 (M_p - M)/M
SPEC, dRpsi, dRphi, dMpsi                                                              # inspect

# %% [markdown]
# ## Kinematics and the MadLoop standalone runs

# %%
def kin(proc, rs, ct):
    e = rs / 2
    if proc == "A":
        p = math.sqrt(e * e - m2)
        st = math.sqrt(1 - ct * ct)
        mom = [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * ct), (e, -p * st, 0, -p * ct)]
        t = -2 * p * p * (1 - ct)
        return mom, rs * rs, t, 4 * m2 - rs * rs - t
    p, k = math.sqrt(e * e - bm2), math.sqrt(e * e - m2)
    st = math.sqrt(1 - ct * ct)
    mom = [(e, 0, 0, p), (e, 0, 0, -p), (e, k * st, 0, k * ct), (e, -k * st, 0, -k * ct)]
    t = bm2 + m2 - 2 * (e * e - p * k * ct)
    return mom, rs * rs, t, 2 * bm2 + 2 * m2 - rs * rs - t


def run_madloop(scheme, proc, rs, ct, mu):
    base = os.path.join(HERE, "work", f"ml_{scheme}_{proc}", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    mom = kin(proc, rs, ct)[0]
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in mom)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps", "2eps")}

# %% [markdown]
# ## Predictions from step (4) (COLLIER values of Eqs. (13), (18) at mu = m)

# %%
ref = {}
with open(os.path.join(HERE, "results", "scat_collier.csv")) as fh:
    for r in csv.DictReader(fh):
        key = (round(float(r["sqrts"]), 6), round(float(r["costheta"]), 6))
        ref[key] = {q: complex(float(r["re_" + q]), float(r["im_" + q])) for q in ("a", "b", "mA")}


def predictions(proc, rs, ct, mu):
    _, s, t, u = kin(proc, rs, ct)
    v = ref[(rs, ct)]
    lnmu = math.log(mu)
    if proc == "A":
        m0 = -LAM
        m1_ms = (v["mA"].real + lnmu * (3 * LAM ** 2 - 48 * Y ** 4)) / K16
        m1_os = (v["mA"].real + 4 * LAM * Y ** 2 * (SPEC["B0phi"] + m2 * SPEC["B0pphi"])
                 + lnmu * (3 * LAM ** 2 + 8 * LAM * Y ** 2 - 48 * Y ** 4)) / K16
        return {"born": m0 * m0 / 2, "MSbar": m0 * m1_ms, "OS": m0 * m1_os}
    X, W = t - bm2, u - bm2
    b0t = Y ** 2 * (1 / X - 1 / W)
    sv_ku = 2 * ((t - bm2) * (u - bm2) - m2 ** 2)          # sum |vbar k1 u|^2
    sv_x = 2 * MPSI * (t - u)                               # sum (vbar k1 u)* (vbar u)
    a, b = v["a"].real, v["b"].real
    da = Y ** 4 * MPSI * (1 / X + 1 / W)
    db = Y ** 4 * sum(sg * (2 * bm2 / x ** 2 - 5 / x) for sg, x in ((1, X), (-1, W)))
    a_ms, b_ms = a + lnmu * da, b + lnmu * db
    a_os = a - Y ** 4 * MPSI * dMpsi / Y ** 2 * (1 / X + 1 / W)
    b_os = b + (dRpsi + dRphi) * b0t - 2 * bm2 * Y ** 2 * dMpsi * (1 / X ** 2 - 1 / W ** 2) - lnmu * 10 * Y ** 2 * b0t
    fin = lambda aa, bb: 0.25 * b0t / K16 * (sv_x * aa + sv_ku * bb)
    return {"born": b0t ** 2 * sv_ku / 8, "MSbar": fin(a_ms, b_ms), "OS": fin(a_os, b_os)}

# %% [markdown]
# ## Inspect: the diagrams that MadLoop evaluates (drawn when MadGraph wrote the standalone code)

# %%
if INTERACTIVE:
    import shutil
    import tempfile
    from IPython.display import Image, display
    GS = shutil.which("gs") or "/opt/homebrew/bin/gs"
    for proc in ("A", "B"):
        with open(os.path.join(HERE, "work", f"ml_OS_{proc}.log")) as fh:
            print(f"ml_OS_{proc}:", next(line.strip() for line in fh if "Contributing diagrams" in line))
        base = os.path.join(HERE, "work", f"ml_OS_{proc}", "SubProcesses")
        dML = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
        tmpML = tempfile.mkdtemp()
        for ps in ("born_matrix.ps", "loop_matrix.ps"):
            subprocess.run([GS, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                            "-sOutputFile=" + os.path.join(tmpML, ps[:-3] + "_%02d.png"), os.path.join(dML, ps)], check=True)
            for png in sorted(f for f in os.listdir(tmpML) if f.startswith(ps[:-3] + "_")):
                display(Image(filename=os.path.join(tmpML, png)))

# %% [markdown]
# ## MadLoop at the six points and at several mu_R

# %%
runs = [(rs, ct, 1.0) for rs in (2.5, 5.0, 10.0) for ct in (0.3, 0.9)] + [(5.0, 0.3, mu) for mu in (0.5, 2.0, 5.0)]
rows, worst = [], {}
print(f"{'proc':4} {'scheme':6} {'sqrt(s)':>7} {'cos':>4} {'mu_R':>5} {'finite (MadLoop)':>22} {'prediction':>22} "
      f"{'rel.dev':>8} {'born dev':>8} {'1/eps':>9}")
for proc in ("A", "B"):
    for scheme in ("OS", "MSbar"):
        for rs, ct, mu in runs:
            v = run_madloop(scheme, proc, rs, ct, mu)
            pr = predictions(proc, rs, ct, mu)
            dfin = abs(v["finite"] - pr[scheme]) / abs(pr[scheme])
            dborn = abs(v["born"] - pr["born"]) / pr["born"]
            ok = dfin < TOL and dborn < TOL and abs(v["1eps"]) < 1e-12 * abs(pr[scheme]) / 1e-3 and v["2eps"] == 0
            print(f"{proc:4} {scheme:6} {rs:7.1f} {ct:4.1f} {mu:5.1f} {v['finite']:+22.15e} {pr[scheme]:+22.15e} {dfin:8.1e} "
                  f"{dborn:8.1e} {v['1eps']:+9.1e}" + ("" if ok else "   <- check"))
            worst[(proc, scheme)] = max(worst.get((proc, scheme), 0.0), dfin)
            rows.append([proc, scheme, rs, ct, mu, v["born"], v["finite"], v["1eps"], v["2eps"], pr["born"], pr[scheme], dborn, dfin])
print("max relative deviation of the finite part:", {k: f"{d:.1e}" for k, d in worst.items()})

with open(os.path.join(HERE, "results", "madloop.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["proc", "scheme", "sqrts", "costheta", "mu_R", "born_madloop", "finite_madloop", "eps1_madloop", "eps2_madloop",
                "born_pred", "finite_pred", "reldev_born", "reldev_finite"])
    w.writerows(rows)
print("wrote results/madloop.csv")
