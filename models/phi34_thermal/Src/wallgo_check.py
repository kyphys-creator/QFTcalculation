# %% [markdown]
# # Step (12): the bubble-wall speed in local thermal equilibrium (WallGo 1.1.2)
#
# Research note models/phi34_thermal, step (12).  Steps (3), (9) took the wall speed as an input, v_w = 0.95
# (detonation) and 0.44 (deflagration).  The general form has no particle content, so only the hydrodynamic part of the
# wall speed can be computed: in local thermal equilibrium (LTE) entropy is conserved across the wall,
# T_+ gamma_+ = T_- gamma_- (WallGo, arXiv:2411.04970; Ai, Laurent, van de Vis 2023).  Out-of-equilibrium friction only
# slows the wall further, so v_w(LTE) is an upper bound; WallGo returns 1 when no deflagration or hybrid exists in LTE
# (then LTE does not bound v_w).  The potential given to WallGo is the general form plus the radiation term
# -pi^2 g* T^4/90 (g* = 106.75), with its exact minima and derivatives.
# Checks: (a) BP1-BP4 at the percolation temperatures of TransitionListener, against its LTE wall speed (step (11)).
# (b) v_w(LTE) at the note's T_n for the SM-like coefficients and BP1-BP4, and the LISA SNR of step (3) with it.
# (c) the points of step (9) where SNR = 10 for v_w = 0.95 or 0.44: v_w(LTE) and the SNR with it.
# Each v_w(LTE) is computed with three temperature scales of WallGo's phase tracing, s/2, s, 2s with
# s = min(1 GeV, (T_1 - T)/2), T_1 the temperature where the broken phase ends; the spread is printed.
# Writes results/wallgo_check.csv.
# Batch: `~/miniforge3/envs/qft/bin/python wallgo_check.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

# %%
import csv
import logging
import math
import os
import sys
import warnings

import numpy as np

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import tptlib as tl
import WallGo

GSTAR = 106.75
# WallGo warns when c_b^2 > 1/3 (the general form at large phi/T) and when its tracing steps are coarse
warnings.filterwarnings("ignore", module="WallGo")
logging.getLogger().setLevel(logging.ERROR)


class DinePotential(WallGo.EffectivePotential):
    """The general form plus the field-independent radiation term."""
    fieldCount = 1
    effectivePotentialError = 1e-15

    def __init__(self, D, E, T0, lam):
        self.D, self.E, self.T0, self.lam = D, E, T0, lam

    def evaluate(self, fields, temperature):
        p = np.asarray(fields)[..., 0]
        T = np.asarray(temperature)
        return (self.D * (T * T - self.T0 ** 2) * p * p - self.E * T * p ** 3 + self.lam / 4 * p ** 4
                - math.pi ** 2 / 90 * GSTAR * T ** 4)

    # Exact minima and derivatives of the polynomial.  With WallGo's numerical ones (Nelder-Mead minima, finite
    # differences) its template model gets c_b^2 = 0.340 at the T_perc of BP1 instead of the exact 0.309, which makes its
    # epsilon negative and stops the run (at T_n of BP1 they give 0.3088 against 0.3081).
    def findLocalMinimum(self, initialGuess, temperature, tol=None, method=None):
        T = np.atleast_1d(np.asarray(temperature, dtype=float))
        guess = np.asarray(initialGuess, dtype=float).reshape(-1)
        n = max(T.size, guess.size)
        T, guess = np.resize(T, n), np.resize(guess, n)
        loc = np.empty(n)
        for i in range(n):
            cands = []
            if self.D * (T[i] ** 2 - self.T0 ** 2) > 0:
                cands.append(0.0)
            disc = 9 * self.E ** 2 * T[i] ** 2 - 8 * self.lam * self.D * (T[i] ** 2 - self.T0 ** 2)
            if disc >= 0:
                cands.append((3 * self.E * T[i] + math.sqrt(disc)) / (2 * self.lam))
            loc[i] = min(cands, key=lambda c: abs(c - guess[i]))
        fields = WallGo.Fields.castFromNumpy(loc[:, None])
        return fields, self.evaluate(fields, T)

    def derivT(self, fields, temperature):
        p, T = np.asarray(fields)[..., 0], np.asarray(temperature)
        res = 2 * self.D * T * p * p - self.E * p ** 3 - 4 * math.pi ** 2 / 90 * GSTAR * T ** 3
        # like WallGo's own finite-difference derivT: a scalar for one field point at a scalar temperature
        return res.reshape(()) if (T.ndim == 0 and res.size == 1) else res

    def derivField(self, fields, temperature):
        p, T = np.asarray(fields)[..., 0], np.asarray(temperature)
        return (2 * self.D * (T * T - self.T0 ** 2) * p - 3 * self.E * T * p * p + self.lam * p ** 3)[..., None]

    def deriv2FieldT(self, fields, temperature):
        p, T = np.asarray(fields)[..., 0], np.asarray(temperature)
        return (4 * self.D * T * p - 3 * self.E * p * p)[..., None]

    def deriv2Field2(self, fields, temperature):
        p, T = np.asarray(fields)[..., 0], np.asarray(temperature)
        return (2 * self.D * (T * T - self.T0 ** 2) - 6 * self.E * T * p + 3 * self.lam * p * p)[..., None, None]

    def allSecondDerivatives(self, fields, temperature):
        p, T = np.asarray(fields)[..., 0], np.asarray(temperature)
        return (self.deriv2Field2(fields, temperature), self.deriv2FieldT(fields, temperature),
                2 * self.D * p * p - 12 * math.pi ** 2 / 90 * GSTAR * T * T)


class DineModel(WallGo.GenericModel):
    def __init__(self, D, E, T0, lam):
        self.veff = DinePotential(D, E, T0, lam)

    @property
    def fieldCount(self):
        return 1

    def getEffectivePotential(self):
        return self.veff


def phi_minus(D, E, T0, lam, T):
    return (3 * E * T + math.sqrt(9 * E * E * T * T - 8 * lam * D * (T * T - T0 * T0))) / (2 * lam)


def t_end_broken(D, E, T0, lam):
    """T_1, where the broken minimum disappears: 9 E^2 T^2 = 8 lambda_T D (T^2 - T0^2) (inf if it never does)."""
    x = 1 - 9 * E * E / (8 * lam * D)
    return T0 / math.sqrt(x) if x > 0 else math.inf


def wallgo_manager(D, E, T0, lam, T, scale):
    manager = WallGo.WallGoManager()
    manager.setVerbosity(logging.ERROR)
    manager.registerModel(DineModel(D, E, T0, lam))
    pm = phi_minus(D, E, T0, lam, T)
    manager.setupThermodynamicsHydrodynamics(
        WallGo.PhaseInfo(temperature=T, phaseLocation1=WallGo.Fields([0.0]), phaseLocation2=WallGo.Fields([pm])),
        WallGo.VeffDerivativeSettings(temperatureVariationScale=scale, fieldValueVariationScale=pm))
    return manager


def vw_lte(D, E, T0, lam, T):
    """WallGo's v_w(LTE) at the tracing scales s/2, s, 2s (central value, spread), and the template model at T: its v_w(LTE),
    v_J, c_b^2, alpha_N, psi_N = w_b/w_s."""
    s = min(1.0, (t_end_broken(D, E, T0, lam) - T) / 2)
    v = {}
    for f in (0.5, 1.0, 2.0):
        manager = wallgo_manager(D, E, T0, lam, T, f * s)
        v[f] = manager.wallSpeedLTE()
        if f == 1.0:
            tm = WallGo.HydrodynamicsTemplateModel(manager.thermodynamics)
    return dict(scale=s, vw_LTE=v[1.0], vw_spread=max(abs(v[f] - v[1.0]) for f in v), vw_template=tm.findvwLTE(),
                vJ_template=tm.vJ, cb2=tm.cb2, alN=tm.alN, psiN=tm.psiN)


def snr(s, Tn, vw):
    return tl.snr(tl.GWSource(s["alpha_theta"], s["betaH"], Tn, vw).h2_total)


def snr_max_below(s, Tn, vmax):
    """The largest SNR for v_w in (0, vmax], on a grid."""
    return max(snr(s, Tn, v) for v in np.linspace(0.02, vmax, 99))


with open(os.path.join(HERE, "results", "dine_form.csv")) as fh:
    step1 = {r[0]: float(r[1]) for r in csv.reader(fh) if r and r[0] in ("D", "E", "T0", "lambda_T_Tc")}
with open(os.path.join(HERE, "results", "strong_pt.csv")) as fh:
    rows = list(csv.reader(fh))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
points = [("SM-like", step1["E"], step1["lambda_T_Tc"])]
points += [(r[0], float(r[1 + keys.index("E")]), float(r[1 + keys.index("lam")])) for r in rows[ib + 1:] if r and r[0].startswith("BP")]
D, T0 = step1["D"], step1["T0"]
print("WallGo", WallGo.__file__)


# %% [markdown]
# ## (a) Against TransitionListener's LTE wall speed at its percolation temperature (step (11))

# %%
with open(os.path.join(HERE, "results", "transitionlistener_check.csv")) as fh:
    tlrows = {r["name"]: r for r in csv.DictReader(fh)}
out = []
for name, E, lam in points[1:]:
    Tp, vtl = float(tlrows[name]["Tperc_TL"]), float(tlrows[name]["v_wall_TL"])
    r = dict(name=name, part="a", T=Tp, vw_TL=vtl, **vw_lte(D, E, T0, lam, Tp))
    out.append(r)
    print(f"(a) {name}: T_perc = {Tp:.6g} GeV: v_w(LTE) WallGo {r['vw_LTE']:.6f} (spread {r['vw_spread']:.1e}), template "
          f"{r['vw_template']:.6f}, TransitionListener {vtl:.6f};  c_b^2 {r['cb2']:.6f}, alpha_N {r['alN']:.6g}, "
          f"psi_N {r['psiN']:.6f}")


# %% [markdown]
# ## (b) v_w(LTE) at the note's T_n, and the LISA SNR of step (3) with it

# %%
for name, E, lam in points:
    m = tl.DineForm(D, E, T0, lam)
    Tn = m.nucleation()
    s = m.summary(Tn)
    r = dict(name=name, part="b", T=Tn, **vw_lte(D, E, T0, lam, Tn))
    vw = r["vw_LTE"]
    r.update(alpha_theta=s["alpha_theta"], betaH=s["betaH"], snr_095=snr(s, Tn, 0.95), snr_044=snr(s, Tn, 0.44))
    if 0 < vw < 1:
        r.update(snr_LTE=snr(s, Tn, vw), snr_max_LTE=snr_max_below(s, Tn, vw))
        kind = "deflagration" if vw < math.sqrt(r["cb2"]) else "hybrid"
    else:
        kind = "no deflagration or hybrid: v_w not bounded in LTE"
    out.append(r)
    print(f"(b) {name}: T_n = {Tn:.6g} GeV (T_1 - T_n = {t_end_broken(D, E, T0, lam) - Tn:.3g} GeV), alpha_theta = "
          f"{s['alpha_theta']:.4g}: v_w(LTE) {vw:.6f} (spread {r['vw_spread']:.1e}; template {r['vw_template']:.6f}), "
          f"c_b {math.sqrt(r['cb2']):.4f}, psi_N {r['psiN']:.4f}: {kind}")
    print(f"      SNR: v_w = 0.95 {r['snr_095']:.3e}, 0.44 {r['snr_044']:.3e}"
          + (f", v_w(LTE) {r['snr_LTE']:.3e}, largest for v_w <= v_w(LTE) {r['snr_max_LTE']:.3e}" if 0 < vw < 1 else ""))


# %% [markdown]
# ## (c) The SNR = 10 points of step (9) (R = 9/8, T0 of the largest SNR)

# %%
with open(os.path.join(HERE, "results", "lisa_scan.csv")) as fh:
    lrows = list(csv.reader(fh))
ih = [k for k, r in enumerate(lrows) if r and r[0] == "name" and "E_over_ESM" in r][0]
hdr = lrows[ih]
for r in lrows[ih + 1:]:
    if not r or not r[0].startswith("R=9/8"):
        break
    d = dict(zip(hdr, r))
    lam = float(d["name"].split("lambda_T=")[1])
    E, Dp, T0p, vw0 = float(d["E"]), float(d["D10"]), float(d["T0"]), float(d["vw"])
    m = tl.DineForm(Dp, E, T0p, lam)
    Tn = m.nucleation()
    s = m.summary(Tn)
    rr = dict(name=f"{d['name']}, v_w={vw0}", part="c", T=Tn, **vw_lte(Dp, E, T0p, lam, Tn))
    vw = rr["vw_LTE"]
    rr.update(alpha_theta=s["alpha_theta"], betaH=s["betaH"], snr_assumed=snr(s, Tn, vw0),
              snr_LTE=snr(s, Tn, vw) if 0 < vw < 1 else float("nan"))
    out.append(rr)
    print(f"(c) {rr['name']}: alpha_theta {s['alpha_theta']:.3g}: SNR {rr['snr_assumed']:.3g} with v_w = {vw0};  v_w(LTE) {vw:.4f} "
          f"(template {rr['vw_template']:.4f}), c_b^2 {rr['cb2']:.3f}, psi_N {rr['psiN']:.3f}")


# %% [markdown]
# ## Output

# %%
cols = ["name", "part", "T", "scale", "vw_LTE", "vw_spread", "vw_template", "vJ_template", "cb2", "alN", "psiN", "vw_TL",
        "alpha_theta", "betaH", "snr_095", "snr_044", "snr_assumed", "snr_LTE", "snr_max_LTE"]
with open(os.path.join(HERE, "results", "wallgo_check.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(cols)
    for r in out:
        wr.writerow([r.get(c, "") for c in cols])
print("wrote results/wallgo_check.csv")
