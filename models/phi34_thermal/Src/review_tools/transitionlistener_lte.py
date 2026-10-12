# %% [markdown]
# # Step (12): TransitionListener's LTE wall speed and the sound speed it uses
#
# Research note models/phi34_thermal, step (12).  TransitionListener 2.1.0 (Hydrodynamics.calcWallVelocityLTE) takes the
# sound speeds c^2 = (dV/dT)/(T d^2V/dT^2) with both temperature derivatives at the fixed field value phi(T_perc) of the
# phase.  Along the phase, d^2p/dT^2 = -(V_TT + V_phiT dphi/dT) with dphi/dT = -V_phiT/V_phiphi, so the fixed-phi value
# misses the term V_phiT^2/V_phiphi.  For BP1-BP4 at its percolation temperatures this script feeds TransitionListener's
# own matching equations (find_vJ, find_vw) with the exact w, p, e of the general form plus radiation (g* = 106.75) and
# c^2 (i) at fixed phi, as TransitionListener does, and (ii) along the phase.  (i) must give the v_wall of step (11);
# (ii) is compared with the template model of WallGo in ../wallgo_check.py.
# Writes ../results/transitionlistener_lte.csv.  Run with the tl environment:
#   ~/miniforge3/envs/tl/bin/python transitionlistener_lte.py      (from Src/review_tools/)

# %%
import csv
import math
import os

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
SRC = os.path.dirname(HERE)

from transitionlistener.hydrodynamics import Hydrodynamics

GSTAR = 106.75
A = math.pi ** 2 / 90 * GSTAR

with open(os.path.join(SRC, "results", "dine_form.csv")) as fh:
    step1 = {r[0]: float(r[1]) for r in csv.reader(fh) if r and r[0] in ("D", "T0")}
with open(os.path.join(SRC, "results", "strong_pt.csv")) as fh:
    rows = list(csv.reader(fh))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
bps = [(r[0], float(r[1 + keys.index("E")]), float(r[1 + keys.index("lam")])) for r in rows[ib + 1:] if r and r[0].startswith("BP")]
with open(os.path.join(SRC, "results", "transitionlistener_check.csv")) as fh:
    tlrows = {r["name"]: r for r in csv.DictReader(fh)}
D, T0 = step1["D"], step1["T0"]

# the matching equations of TransitionListener need no potential: an instance without __init__ is enough
hyd = Hydrodynamics.__new__(Hydrodynamics)
hyd.verbose = False


def inputs(E, lam, T, along_phase):
    """psi_N, alpha_N (TransitionListener's definition), c_s^2, c_b^2 at T."""
    pm = (3 * E * T + math.sqrt(9 * E * E * T * T - 8 * lam * D * (T * T - T0 * T0))) / (2 * lam)
    V = lambda p: D * (T * T - T0 ** 2) * p * p - E * T * p ** 3 + lam / 4 * p ** 4 - A * T ** 4
    VT = lambda p: 2 * D * T * p * p - E * p ** 3 - 4 * A * T ** 3

    def VTT(p):
        res = 2 * D * p * p - 12 * A * T * T
        if along_phase and p != 0:
            res -= (4 * D * T * p - 3 * E * p * p) ** 2 / (2 * D * (T * T - T0 ** 2) - 6 * E * T * p + 3 * lam * p * p)
        return res
    ws, wb = -T * VT(0.0), -T * VT(pm)
    cs2, cb2 = VT(0.0) / (T * VTT(0.0)), VT(pm) / (T * VTT(pm))
    ps, pb = -V(0.0), -V(pm)
    alN = ((ws - ps - ps / cb2) - (wb - pb - pb / cb2)) / (3 * ws)
    return wb / ws, alN, cs2, cb2


def tl_vw(psiN, alN, cs2, cb2):
    try:
        return hyd.find_vw(alN, cb2, cs2, psiN)
    except ValueError:          # the root brackets of TransitionListener fail: no deflagration or hybrid
        return float("nan")


# %% [markdown]
# ## BP1-BP4 at TransitionListener's percolation temperatures

# %%
out = []
for name, E, lam in bps:
    T, vtl = float(tlrows[name]["Tperc_TL"]), float(tlrows[name]["v_wall_TL"])
    r = dict(name=name, T=T, v_wall_TL=vtl)
    for tag, along in (("fixedphi", False), ("phase", True)):
        psiN, alN, cs2, cb2 = inputs(E, lam, T, along)
        r.update({f"cb2_{tag}": cb2, f"alN_{tag}": alN, f"vJ_{tag}": hyd.find_vJ(alN, cb2), f"vw_{tag}": tl_vw(psiN, alN, cs2, cb2)})
    r["psiN"] = psiN
    out.append(r)
    print(f"{name}: T_perc = {T:.6g} GeV, psi_N = {psiN:.6f};  fixed phi: c_b^2 {r['cb2_fixedphi']:.6f}, v_J {r['vJ_fixedphi']:.6f}, "
          f"v_w {r['vw_fixedphi']:.6f} (TransitionListener {vtl:.6f}, rel. {r['vw_fixedphi'] / vtl - 1:+.1e});  along the phase: "
          f"c_b^2 {r['cb2_phase']:.6f}, v_J {r['vJ_phase']:.6f}, v_w {r['vw_phase']:.6f}")


# %% [markdown]
# ## Output

# %%
cols = ["name", "T", "psiN", "cb2_fixedphi", "alN_fixedphi", "vJ_fixedphi", "vw_fixedphi", "v_wall_TL", "cb2_phase", "alN_phase",
        "vJ_phase", "vw_phase"]
with open(os.path.join(SRC, "results", "transitionlistener_lte.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(cols)
    for r in out:
        wr.writerow([r.get(c, "") for c in cols])
print("wrote results/transitionlistener_lte.csv")
