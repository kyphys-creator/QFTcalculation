# %% [markdown]
# # Step (11c): the general form of Dine et al. in TransitionListener 2.1.0
#
# Research note models/phi34_thermal, step (11).  V = D (T^2 - T0^2) phi^2 - E T phi^3 + lambda_T phi^4/4 is given to
# TransitionListener as a user potential: Vtot is the general form plus the field-independent radiation of g* = 106.75
# (one massless scalar + 105.75 from the bath), and the energy density is e = V - T dV/dT of the same Vtot, so that the
# strength alpha_theta = (Delta e + 3 Delta V)/(4 rho_rad) and the Hubble rate (with Delta V) are those of the note's
# potential; dgradV_dT, which TransitionListener takes from the particle loops V1T, is given the T-dependent part of the
# general form.  Internal units are GeV (v_GeV = internal_scale).  Stages 1-3 of TransitionListener (phases, transitions,
# observables at the percolation temperature) for the SM-like coefficients and BP1-BP4; compared with tptlib.  The Tnuc
# that TransitionListener reports solves N(T) = (4 pi/3) v_w^3 int Gamma/H^4 (1 - P) dT/T = 1; tptlib is evaluated the same way.
# Writes ../results/transitionlistener_check.csv.  Run with the tl environment:
#   ~/miniforge3/envs/tl/bin/python transitionlistener_check.py      (from Src/review_tools/)

# %%
import csv
import math
import os
import sys

import numpy as np

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
SRC = os.path.dirname(HERE)
sys.path.insert(0, SRC)
import tptlib as tl

from transitionlistener.generic_potential import generic_potential
from transitionlistener.particles import MassSpectrum, Scalar, Fermion
from transitionlistener.interface.pipeline import _compute_single_point
import transitionlistener

GSTAR = 106.75


class DineTL(generic_potential):
    """The general form of Dine et al. as a TransitionListener potential (internal units = GeV)."""

    model_parameters = {
        "D": {"default": 0.1666, "min": 0, "max": np.inf},
        "E": {"default": 0.01, "min": 0, "max": np.inf},
        "T0_GeV": {"default": 163.5, "min": 0, "max": np.inf},
        "lam": {"default": 0.1, "min": 0, "max": np.inf},
    }

    def init(self, input_dict, verbose=False):
        self.verbose = verbose
        self.Ndim = 1
        self.mp = self.set_modelparams(input_dict)
        self.D, self.E = self.mp["D"]["value"], self.mp["E"]["value"]
        self.T0, self.lam = self.mp["T0_GeV"]["value"], self.mp["lam"]["value"]
        self.v_GeV = self.v_stable                                   # conversion factor 1: internal units are GeV
        self.conversionFactor = self.computeConversionFactor(self.v_stable, self.v_GeV)
        self.daisy = "off"                                           # not used: Vtot is given directly
        self.X0 = np.array([self.T0 * math.sqrt(2 * self.D / self.lam)])   # minimum of V at T = 0
        self.v = self.X0[0]                                          # used by TransitionListener as the vev scale
        self.renormScaleSq = self.X0[0] ** 2
        phi = Scalar(name="m_phi", latex_name=r"$m_\phi$", dof=1, is_SM=False)
        # a fermion with no degrees of freedom: some bookkeeping of TransitionListener needs a non-empty fermion list
        psi = Fermion(name="m_psi", latex_name=r"$m_\psi$", dof=0, is_SM=False)
        self.mass_spectrum = MassSpectrum([phi], [], [psi],
                                          boson_massSq_fn=lambda X, T: np.zeros(np.asarray(X)[..., 0].shape + (1,)),
                                          fermion_massSq_fn=lambda X: np.zeros(np.asarray(X)[..., 0].shape + (1,)))
        self.kin_coupled_e_geff = lambda T, cf: (GSTAR - 1) + 0.0 * np.asarray(T, dtype=float)
        self.kin_coupled_p_geff = lambda T, cf: (GSTAR - 1) + 0.0 * np.asarray(T, dtype=float)
        self.derived_param_names = []
        self.derived_param_plot_names = []

    def setConfigParameters(self):
        self.config.tracingConf.gen_mirror_phases = False

    def forbidPhaseCrit(self, X):
        return (np.array([X])[..., 0] < -1.0).any()

    def approxZeroTMin(self):
        return [self.X0]

    def V_D(self, X, T):
        X = np.asanyarray(X)
        p = X[..., 0]
        T = np.asanyarray(T)
        return self.D * (T * T - self.T0 ** 2) * p * p - self.E * T * p ** 3 + self.lam / 4 * p ** 4

    def dV_D_dT(self, X, T):
        p = np.asanyarray(X)[..., 0]
        return 2 * self.D * np.asanyarray(T) * p * p - self.E * p ** 3

    def V0(self, X):
        return self.V_D(X, 0.0)

    def V1T_from_X(self, X, T):
        """The T-dependent part, D T^2 phi^2 - E T phi^3: TransitionListener's dgradV_dT differentiates this one."""
        return self.V_D(X, T) - self.V_D(X, 0.0)

    def V1_from_X(self, X):
        return np.asanyarray(X)[..., 0] * 0.0

    def Vct(self, X):
        return np.asanyarray(X)[..., 0] * 0.0

    def Vtot(self, X, T, include_radiation=True, include_decoupled=True):
        T = np.asanyarray(T, dtype=float)
        y = self.V_D(X, T)
        if include_radiation:
            y = y - np.pi ** 2 / 90 * GSTAR * T ** 4
        return y

    def radiationEnergyDensity(self, X, T, include_decoupled=True):
        return np.pi ** 2 / 30 * GSTAR * np.asanyarray(T, dtype=float) ** 4

    def energyDensity(self, X, T, include_decoupled=True):
        e = self.V_D(X, T) - np.asanyarray(T) * self.dV_D_dT(X, T) - self.V_D(self.X0, 0.0)
        return e + self.radiationEnergyDensity(X, T)


# %% [markdown]
# ## The five points of steps (1), (2) and the reference values of tptlib

# %%
with open(os.path.join(SRC, "results", "dine_form.csv")) as fh:
    step1 = {r[0]: float(r[1]) for r in csv.reader(fh) if r and r[0] in ("D", "E", "T0", "lambda_T_Tc")}
with open(os.path.join(SRC, "results", "strong_pt.csv")) as fh:
    rows = list(csv.reader(fh))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
points = [("SM-like", step1["E"], step1["lambda_T_Tc"])]
points += [(r[0], float(r[1 + keys.index("E")]), float(r[1 + keys.index("lam")])) for r in rows[ib + 1:] if r and r[0].startswith("BP")]
D, T0 = step1["D"], step1["T0"]
print(f"TransitionListener {transitionlistener.__file__}; D = {D}, T0 = {T0}")

def tnuc_integral(ref, vw, rho_vac):
    """T where N(T) = (4 pi/3) v_w^3 int_T^Tc Gamma/H^4 dT'/T' = 1 (TransitionListener's Tnuc, with 1 - P = 1), from the
    actions of tptlib and H^2 = 8 pi (rho_rad + rho_vac)/(3 M_Pl^2) as in the user potential above."""
    from scipy.integrate import quad
    from scipy.optimize import brentq
    lnr = lambda T: (4 * math.log(T) + 1.5 * math.log(ref.s3T(T) / (2 * math.pi)) - ref.s3T(T)
                     - 2 * math.log(8 * math.pi / 3 * (math.pi ** 2 / 30 * GSTAR * T ** 4 + rho_vac) / tl.MPL ** 2))
    Tc = ref.T_of_alpha(1.0)
    Tn = ref.nucleation()
    def N(T):
        top = min(Tc * (1 - 1e-9), T * 1.2)
        return 4 * math.pi / 3 * vw ** 3 * quad(lambda u: math.exp(lnr(math.exp(u))), math.log(T), math.log(top),
                                                epsabs=0, epsrel=1e-10, limit=200)[0]
    return brentq(lambda T: math.log(N(T)), max(0.95 * Tn, ref.T_of_alpha(0.05)), Tn, xtol=1e-12 * Tn)


out = []
for name, E, lam in points:
    ref = tl.DineForm(D, E, T0, lam)
    Tn = ref.nucleation()
    ctx, err = _compute_single_point({"D": D, "E": E, "T0_GeV": T0, "lam": lam}, DineTL, timeout=-1, verbose=False,
                                     include_smbhb=False, max_stage=3)
    if err is not None:
        print(f"{name}: TransitionListener error: {err!r}")
        out.append(dict(name=name, error=repr(err)))
        continue
    obs = ctx["strongest_transition_observables"]
    get = lambda k: float(obs.get(k, float("nan"))) if obs.get(k) is not None else float("nan")
    Tc, Tnuc, Tp = get("Tcrit_SM_GeV"), get("Tnuc_SM_GeV"), get("Tperc_SM_GeV")
    s_p = ref.summary(Tp) if Tp == Tp else None
    r = dict(name=name, Tc_TL=Tc, Tc_ref=ref.T_of_alpha(1.0), Tnuc_TL=Tnuc, Tnuc_ref=Tn, Tperc_TL=Tp,
             alpha_theta_TL=get("alpha_theta"), alpha_theta_ref_at_Tp=s_p["alpha_theta"] if s_p else float("nan"),
             betaH_S3_TL=get("betaH_S3"), betaH_ref_at_Tp=s_p["betaH"] if s_p else float("nan"), betaH_RH_TL=get("betaH_RH"),
             RH_TL=get("RH"), v_wall_TL=get("v_wall"))
    vw = r["v_wall_TL"] if r["v_wall_TL"] == r["v_wall_TL"] else 0.95
    r["Tnuc_ref_integral"] = tnuc_integral(ref, vw, lam / 4 * (T0 * math.sqrt(2 * D / lam)) ** 4)
    out.append(r)
    print(f"{name}: T_nuc (integral criterion, v_w = {vw:.4g}) TL {Tnuc:.8g} vs tptlib {r['Tnuc_ref_integral']:.8g} "
          f"(rel. {Tnuc / r['Tnuc_ref_integral'] - 1:+.1e})")
    print(f"{name}: T_c {Tc:.10g} vs {r['Tc_ref']:.10g} (rel. {Tc / r['Tc_ref'] - 1:+.1e});  T_nuc {Tnuc:.8g} vs {Tn:.8g} "
          f"(rel. {Tnuc / Tn - 1:+.1e});  T_perc {Tp:.8g};  at T_perc: alpha_theta {r['alpha_theta_TL']:.6g} vs "
          f"{r['alpha_theta_ref_at_Tp']:.6g} (rel. {r['alpha_theta_TL'] / r['alpha_theta_ref_at_Tp'] - 1:+.1e}), beta/H(S3) "
          f"{r['betaH_S3_TL']:.6g} vs {r['betaH_ref_at_Tp']:.6g} (rel. {r['betaH_S3_TL'] / r['betaH_ref_at_Tp'] - 1:+.1e}), "
          f"(beta/H)_RH {r['betaH_RH_TL']:.6g}")


# %% [markdown]
# ## Output

# %%
cols = ["name", "Tc_TL", "Tc_ref", "Tnuc_TL", "Tnuc_ref", "Tnuc_ref_integral", "Tperc_TL", "alpha_theta_TL", "alpha_theta_ref_at_Tp", "betaH_S3_TL",
        "betaH_ref_at_Tp", "betaH_RH_TL", "RH_TL", "v_wall_TL", "error"]
with open(os.path.join(SRC, "results", "transitionlistener_check.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(cols)
    for r in out:
        wr.writerow([r.get(c, "") for c in cols])
print("wrote results/transitionlistener_check.csv")
