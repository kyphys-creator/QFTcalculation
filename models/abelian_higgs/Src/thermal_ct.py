# %% [markdown]
# # Step (10): the one-loop critical temperature with CosmoTransitions
#
# Research note models/abelian_higgs, step (10).  The one-loop potential of thermal.wl with the exact J_B (Landau gauge,
# no resummation): V0 = -m2 phi^2/2 + lam phi^4/4, MS-bar zero-temperature part with (m^2, n, c) = (mh2, 1, 3/2),
# (mG2, 1, 3/2), (mA2, 3, 5/6) at mu = 1, and (T^4/(2 pi^2)) sum n J_B(m^2/T^2).  CosmoTransitions 2.0.7
# (generic_potential: V1 and V1T with its J_B spline; getPhases and calcTcTrans for the phases and the critical
# temperature) against results/thermal.csv (thermal.wl, interpolated exact J_B) for MH = 1/2 and 1 (e = 1/2, MA = 1).
# Also its J_B spline against results/thermal_jb.csv.  Writes results/thermal_ct.csv.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python thermal_ct.py

# %%
import contextlib
import csv
import io
import os
import warnings

import numpy as np
from scipy import optimize

np.product = np.prod                               # numpy 2: removed alias used by cosmoTransitions.helper_functions
warnings.filterwarnings("ignore")
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
from importlib.metadata import version
from cosmoTransitions import finiteT, generic_potential

quiet = lambda: contextlib.redirect_stdout(io.StringIO())
print(f"CosmoTransitions {version('cosmoTransitions')}")

# %% [markdown]
# ## J_B

# %%
with open(os.path.join(HERE, "results", "thermal_jb.csv")) as fh:
    tab = [(float(a), float(b)) for a, b in list(csv.reader(fh))[1:]]
# the spline covers y >= -3.724 (the minimum of J_B; below it the value is held); an array: Jb_spline uses
# np.array(X, copy=False)
sel = [(s, jb) for s, jb in tab if np.sign(s) * s * s >= -3.7]
ys = np.array([np.sign(s) * s * s for s, _ in sel])
dmax = float(np.max(np.abs(finiteT.Jb_spline(ys) - np.array([jb for _, jb in sel]))))
print("(a) CosmoTransitions Jb_spline against the exact J_B of thermal.wl (y = -3.7 ... 64, %d points): max |difference| = %.1e"
      % (len(sel), dmax))


# %% [markdown]
# ## The model and the critical temperature

# %%
class AH(generic_potential.generic_potential):
    def init(self, e, lam, m2):
        self.Ndim = 1
        self.renormScaleSq = 1.0
        self.e, self.lam, self.m2 = e, lam, m2
        self.Tmax = 10.0
        self.x_eps = 1e-6          # tighter than the defaults (1e-3): the minima and the traced phases
        self.T_eps = 1e-6

    def V0(self, X):
        phi = np.asanyarray(X)[..., 0]
        return -self.m2 * phi ** 2 / 2 + self.lam * phi ** 4 / 4

    def boson_massSq(self, X, T):
        phi2 = np.asanyarray(X)[..., 0] ** 2
        m2 = np.stack([-self.m2 + 3 * self.lam * phi2, -self.m2 + self.lam * phi2, self.e ** 2 * phi2], axis=-1)
        return m2, np.array([1, 1, 3]), np.array([1.5, 1.5, 5 / 6])

    def fermion_massSq(self, X):
        # one massless dummy fermion with no degrees of freedom (an empty array breaks Jf_spline)
        phi = np.asanyarray(X)[..., 0]
        return np.zeros(phi.shape + (1,)), np.zeros(1)

    def approxZeroTMin(self):
        return [np.array([np.sqrt(self.m2 / self.lam)])]


with open(os.path.join(HERE, "results", "thermal.csv")) as fh:
    ref = {round(float(r["MH"]), 6): r for r in csv.DictReader(fh)}
rows = []
for mh in (0.5, 1.0):
    e = 0.5
    lam = e ** 2 * mh ** 2 / 2
    m = AH(e, lam, lam * 4)
    with quiet():
        m.getPhases()
        m.calcTcTrans()
    tr = [t for t in m.TcTrans if t["trantype"] == 1]
    t = max(tr, key=lambda x: x["Tcrit"])
    tc = t["Tcrit"]
    # the broken minimum at T_c, refined with the potential itself (the traced phase is a spline)
    phic = abs(float(optimize.fmin(lambda x: m.Vtot(x, tc), t["low_vev"], xtol=1e-12, ftol=1e-16, disp=0)[0]))
    r = ref[round(mh, 6)]
    tc_wl, phic_wl = float(r["Tc_exactJB"]), float(r["phic_exactJB"])
    # the broken minimum of the CosmoTransitions potential at the T_c of thermal.wl: phi_c is steep in T for a weak transition
    phi_at_wl = abs(float(optimize.fmin(lambda x: m.Vtot(x, tc_wl), [phic_wl], xtol=1e-12, ftol=1e-16, disp=0)[0]))
    print("(b) MH = %.1f: CosmoTransitions T_c = %.8f, phi_c = %.6f (phi_c/T_c = %.6f);  thermal.wl %.8f, %.6f;"
          "  relative differences %.1e, %.1e;  CosmoTransitions minimum at the T_c of thermal.wl %.6f (%.1e)" % (
              mh, tc, phic, phic / tc, tc_wl, phic_wl, tc / tc_wl - 1, phic / phic_wl - 1, phi_at_wl, phi_at_wl / phic_wl - 1))
    rows.append([mh, tc, phic, tc_wl, phic_wl])
with open(os.path.join(HERE, "results", "thermal_ct.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["MH", "Tc_cosmotransitions", "phic_cosmotransitions", "Tc_thermalwl", "phic_thermalwl"])
    for r in rows:
        w.writerow(["%.10g" % x for x in r])
print("written results/thermal_ct.csv")
