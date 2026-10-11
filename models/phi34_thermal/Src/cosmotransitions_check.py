# %% [markdown]
# # Step (7): cross-check with an independent tool, CosmoTransitions 2.0.7
#
# Research note models/phi34_thermal, step (7).  CosmoTransitions (Wainwright 2012) is used as installed in the qft
# environment (pip, version 2.0.7); numpy 2 removed np.product, which its helper_functions use, so np.product = np.prod is
# set here before the import (the installed package is not edited).
# (a) tunneling1D.SingleFieldInstanton against tptlib.bounce: the zero-temperature tree potential (d = 3, 4), the Dine form
#     at T_n (step (1), benchmarks of step (2)), and the thermal decay of the single-field model (step (5)).
# (b) generic_potential with the Dine form (SM-like, BP2, BP4): phase tracing (T0, T1), critical temperature, and the
#     nucleation temperature with the criterion of this note (Gamma = H^4) against the closed forms and tptlib.bounce.
# (c) the single-field model (alpha = 0.9, 1.05, kappa_4 = 1, high T + daisy): traced phases, the end of the metastable
#     phase against T_sp, no critical temperature, no transition out of the high-temperature phase.
# Writes results/cosmotransitions_check.csv.
# Batch: `~/miniforge3/envs/qft/bin/python cosmotransitions_check.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import contextlib
import csv
import io
import math
import os
import sys
import warnings

import numpy as np
from scipy.optimize import brentq

np.product = np.prod                               # numpy 2: removed alias used by cosmoTransitions.helper_functions
warnings.filterwarnings("ignore")
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
sys.path.insert(0, HERE)
import tptlib as tl
import cosmoTransitions
from cosmoTransitions import generic_potential, transitionFinder, tunneling1D

quiet = lambda: contextlib.redirect_stdout(io.StringIO())     # CosmoTransitions prints its progress
FP = dict(xtol=1e-10, phitol=1e-10, npoints=4000)             # tight tolerances of SingleFieldInstanton.findProfile
MH, GM1 = 125.25, 1.5261
from importlib.metadata import version
print(f"CosmoTransitions {version('cosmoTransitions')} at {os.path.dirname(cosmoTransitions.__file__)}")
rows_out = []


def ct_action(V, dV, d2V, phi_t, phi_f, d=3):
    inst = tunneling1D.SingleFieldInstanton(phi_t, phi_f, V, dV, d2V, alpha=d - 1)
    with quiet():
        prof = inst.findProfile(**FP)
    return inst.findAction(prof)


# %% [markdown]
# ## (a) Bounce actions: SingleFieldInstanton vs tptlib.bounce

# %%
for d in (3, 4):
    for a in (0.3, 0.5, 0.7, 0.9):
        V = lambda f, a=a: f * f / 2 + f ** 3 / 6 + a * f ** 4 / 72
        dV = lambda f, a=a: f + f * f / 2 + a * f ** 3 / 18
        d2V = lambda f, a=a: 1 + f + a * f * f / 6
        fm = -9 / (2 * a) * (1 + math.sqrt(1 - 8 * a / 9))
        sc, so = ct_action(V, dV, d2V, fm, 0.0, d), tl.bounce(V, dV, 0.0, fm, d=d)["S"]
        print(f"tree, d = {d}, alpha = {a}: CosmoTransitions {sc:.10f}, tptlib {so:.10f} (rel. {sc / so - 1:+.1e})")
        rows_out.append((f"S{d}_tree_alpha{a}", sc, so))

with open(os.path.join(HERE, "results", "dine_form.csv")) as fh:
    step1 = {r[0]: float(r[1]) for r in csv.reader(fh) if r[0] != "quantity"}
with open(os.path.join(HERE, "results", "strong_pt.csv")) as fh:
    rows = list(csv.reader(fh))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
dpts = [("SM-like", step1["lambda_T_Tc"], step1["E"], step1["Tn"])]
dpts += [(r[0],) + tuple(float(r[1 + keys.index(k)]) for k in ("lam", "E", "Tn")) for r in rows[ib + 1:ib + 5]]
for name, lam, E, Tn in dpts:
    dm = tl.DineForm(step1["D"], E, step1["T0"], lam)
    V = lambda p: dm.V(p, Tn)
    dV = lambda p: 2 * dm.D * (Tn * Tn - dm.T0 ** 2) * p - 3 * dm.E * Tn * p * p + dm.lam * p ** 3
    d2V = lambda p: 2 * dm.D * (Tn * Tn - dm.T0 ** 2) - 6 * dm.E * Tn * p + 3 * dm.lam * p * p
    a = dm.alpha(Tn)
    pt = -(a * dm.E * Tn / (3 * dm.lam)) * tl.fminus(a)
    sc, so = ct_action(V, dV, d2V, pt, 0.0) / Tn, tl.bounce(V, dV, 0.0, pt, d=3)["S"] / Tn
    print(f"Dine form {name} at T_n: S_3/T CosmoTransitions {sc:.8f}, tptlib {so:.8f} (rel. {sc / so - 1:+.1e})")
    rows_out.append((f"S3T_dine_{name}", sc, so))

gm_of = lambda al: GM1 / math.sqrt(al)
for al in (0.5, 0.7, 0.9):
    sf = tl.SingleField(al, gm_of(al))
    tsp = sf.tau_spinodal("ht")
    for tau in (0.5 * tsp, 0.9 * tsp):
        xf, xt = sf.false_true(tau, "ht")
        V = lambda x: sf.v_ht(x, tau)                  # CosmoTransitions passes arrays
        dV = lambda x: sf.dv_ht(x, tau)
        d2V = lambda x: (dV(x + 1e-6) - dV(x - 1e-6)) / 2e-6
        sc = ct_action(V, dV, d2V, xt, xf) / (sf.gm * tau)
        so = sf.s3T(tau, "ht")[0]
        print(f"single field alpha = {al}, tau = {tau:.4f}: S_3/T CosmoTransitions {sc:.8f}, tptlib {so:.8f} (rel. {sc / so - 1:+.1e})")
        rows_out.append((f"S3T_single_alpha{al}_tau{tau:.3f}", sc, so))


# %% [markdown]
# ## (b) The Dine form: phases, critical and nucleation temperatures

# %%
def crit(S, T):
    """Gamma = H^4 of this note: S/T - (3/2) ln(S/2 pi T) - 4 ln(M_Pl/(1.66 g*^(1/2) T)); > 0 means a low rate."""
    if T <= 0 or not math.isfinite(S):
        return 1e300                                # no tunnelling (stable) or undefined
    if S <= 0:
        return -1e300                               # no barrier: immediate decay
    sT = S / T
    return sT - 1.5 * math.log(max(sT, 1e-300) / (2 * math.pi)) - 4 * math.log(tl.MPL / (1.66 * math.sqrt(106.75) * T))


class Dine(generic_potential.generic_potential):
    def init(self, D, E, T0, lam, Tmax):
        self.Ndim = 1
        self.D, self.E, self.T0, self.lam = D, E, T0, lam
        self.Tmax, self.x_eps, self.T_eps = Tmax, 1e-4, 1e-6

    def Vtot(self, X, T, include_radiation=True):
        p, T = np.asanyarray(X)[..., 0], np.asanyarray(T)
        return self.D * (T * T - self.T0 ** 2) * p * p - self.E * T * p ** 3 + self.lam / 4 * p ** 4

    def approxZeroTMin(self):
        return [np.array([3 * self.E * self.T0 / self.lam + 1.0])]


def tn_generic(dm):
    """T_n of this note's criterion with S_3 from tptlib.bounce (no interpolation of S_3(alpha))."""
    def f(T):
        a = dm.alpha(T)
        pt = -(a * dm.E * T / (3 * dm.lam)) * tl.fminus(a)
        V = lambda p: dm.V(p, T)
        dV = lambda p: 2 * dm.D * (T * T - dm.T0 ** 2) * p - 3 * dm.E * T * p * p + dm.lam * p ** 3
        return -crit(tl.bounce(V, dV, 0.0, pt, d=3)["S"], T)
    a0 = dm.alpha(dm.nucleation())                 # bracket in alpha around the interpolated T_n
    return brentq(f, dm.T_of_alpha(max(a0 - 0.01, 0.01)), dm.T_of_alpha(min(a0 + 0.01, 0.99)), xtol=1e-12 * dm.T0)


FT = dict(V_spline_samples=None, tunneling_findProfile_params=FP)
for name, lam, E, Tn in [dpts[0], dpts[2], dpts[4]]:
    dm = tl.DineForm(step1["D"], E, step1["T0"], lam)
    M = Dine(step1["D"], E, step1["T0"], lam, 1.05 * dm.T_of_alpha(9 / 8))     # trace past T1
    with quiet():
        M.getPhases(tracingArgs=dict(dtstart=1e-6, tjump=1e-6))
        M.calcTcTrans()
        M.findAllTransitions(tunnelFromPhase_args=dict(nuclCriterion=crit, Ttol=1e-9, fullTunneling_params=FT))
    ph = sorted(M.phases.values(), key=lambda p: p.T[0])
    T1_ct, T0_ct = ph[0].T[-1], ph[1].T[0]
    tc_ct, tn_ct = M.TcTrans[0]["Tcrit"], M.TnTrans[0]["Tnuc"]
    tn_g = tn_generic(dm)
    print(f"Dine form {name}: T0 CosmoTransitions {T0_ct:.6f} vs {dm.T0:.6f};  T1 {T1_ct:.6f} vs {dm.T_of_alpha(9 / 8):.6f};  "
          f"T_c {tc_ct:.10f} vs {dm.T_of_alpha(1.0):.10f} (rel. {tc_ct / dm.T_of_alpha(1.0) - 1:+.1e});  "
          f"T_n {tn_ct:.8f} vs tptlib.bounce {tn_g:.8f} (rel. {tn_ct / tn_g - 1:+.1e}) and steps (1), (2) {Tn:.8f} "
          f"(rel. {Tn / tn_g - 1:+.1e})")
    rows_out += [(f"T0_{name}", T0_ct, dm.T0), (f"T1_{name}", T1_ct, dm.T_of_alpha(9 / 8)),
                 (f"Tc_{name}", tc_ct, dm.T_of_alpha(1.0)), (f"Tn_{name}", tn_ct, tn_g), (f"Tn_interp_{name}", Tn, tn_g)]


# %% [markdown]
# ## (c) The single-field model: phases traced by CosmoTransitions

# %%
class Single(generic_potential.generic_potential):
    """V in GeV^4 of the field chi (GeV) = (m^2/g) chi_hat, from tptlib.SingleField.v_ht (m = m_h)."""

    def init(self, alpha, gm, Tlow, Thigh):
        self.Ndim = 1
        self.sf, self.gm = tl.SingleField(alpha, gm), gm
        self.fs, self.vs = MH / gm, MH ** 4 / gm ** 2
        self.Tlow, self.Tmax, self.x_eps, self.T_eps = Tlow, Thigh, 1e-4, 1e-5

    def Vtot(self, X, T, include_radiation=True):
        return self.vs * self.sf.v_ht(np.asanyarray(X)[..., 0] / self.fs, np.asanyarray(T) * self.gm / MH)


for al in (0.9, 1.05):
    M = Single(al, gm_of(al), 0.3 * MH, 6 * MH)
    pts = [[np.array([x * M.fs]), M.Tlow] for x, _ in M.sf.minima(M.Tlow * M.gm / MH, "ht")]
    with quiet():
        ph = transitionFinder.traceMultiMin(M.Vtot, M.dgradV_dT, M.d2V, pts, tLow=M.Tlow, tHigh=M.Tmax,
                                            deltaX_target=100 * M.x_eps, dtstart=1e-5, tjump=1e-5)
        transitionFinder.removeRedundantPhases(M.Vtot, ph, M.x_eps * 1e-2, M.x_eps * 10)
        M.phases = ph
        M.calcTcTrans()
    glob = max(ph.values(), key=lambda p: p.T[-1])
    meta = min(ph.values(), key=lambda p: p.T[-1])
    Ts = np.linspace(meta.T[0], meta.T[-1] * (1 - 1e-6), 400)
    dv = np.array([M.Vtot(meta.valAt(T), T) - M.Vtot(glob.valAt(T), T) for T in Ts])
    with quiet():
        tr = transitionFinder.tunnelFromPhase(ph, glob, M.Vtot, M.gradV, 0.999 * meta.T[-1], nuclCriterion=crit)
    tsp = M.sf.tau_spinodal("ht") / M.gm
    print(f"alpha = {al}: {len(ph)} phases; global phase T = {glob.T[0] / MH:.3f}-{glob.T[-1] / MH:.3f} m, metastable phase ends at "
          f"T = {meta.T[-1] / MH:.6f} m vs T_sp = {tsp:.6f} m (rel. {meta.T[-1] / MH / tsp - 1:+.1e});  min over T of "
          f"[V(metastable) - V(global)] = {dv.min():.4e} GeV^4 (> 0);  critical temperatures: {len(M.TcTrans)};  "
          f"transition out of the high-T phase: {tr}")
    rows_out += [(f"Tsp_over_m_alpha{al}", meta.T[-1] / MH, tsp), (f"min_dV_alpha{al}", dv.min(), 0.0),
                 (f"n_Tc_alpha{al}", len(M.TcTrans), 0)]


# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "cosmotransitions_check.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["quantity", "cosmotransitions", "this_note"])
    wr.writerows(rows_out)
print("wrote results/cosmotransitions_check.csv")
