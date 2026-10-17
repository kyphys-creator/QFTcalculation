# %% [markdown]
# # Step (10): the RG-improved effective potential of the SM and the decay of the electroweak vacuum
#
# Research note models/sm, step (10).  Everything is computed with the note's own model:
#   - V = V0 + V1 in Landau gauge: V0 = -m^2 h^2/4 + lambda h^4/4 (m^2 = 2 mu^2 of the note) and the one-loop
#     Coleman-Weinberg term V1 = sum_i n_i M_i^4 [ln(M_i^2/mu^2) - c_i]/(64 pi^2) with the field-dependent masses of the
#     note's Feynman rules (H, G^0, G^+-, W, Z, t, b, tau; c = 3/2 for scalars and fermions, 5/6 for vectors, MS-bar).
#     Checks (symbolic): the one-loop RG equation [d/d ln mu + beta d/dg - gamma_Phi h d/dh] V = 0 for the h^4 and h^2
#     terms with the note's Eq. (beta) and the Landau-gauge gamma_Phi of Eq. (vbeta); and dV1/dh at h = v equals -T of the
#     note's Eq. (T) at xi = 0 (the tadpole is minus the slope of the potential).
#   - RG improvement as in the Yukawa note: V_eff(h) = V(xi(mu) h; g(mu), mu) with mu = kappa h, xi = exp(-int gamma_Phi),
#     the couplings run with the note's equations from the note's starting values (step (7), sm_running.py).
#     lambda_eff(h) = 4 V_eff(h)/h^4 for the field h normalized at M_t: its zero is the instability scale Lambda_I.
#     The kinetic term carries the same xi^2, so the bounce is solved for the canonical field h^ = xi h with
#     lambda^_eff(h^) = 4 V(h^; g(mu), mu)/h^^4, mu = kappa h^ (minimum lambda^_min at h^_min).
#   - Bounce: for constant lambda < 0 the Fubini solution h = sqrt(8/|lambda|) R/(r^2 + R^2), S = 8 pi^2/(3 |lambda|) (all R);
#     with the running lambda^_eff the O(4) equation is solved by shooting on h(0) (phi34 note), classified by the sign of
#     the constant a of the tail h = a + c/r^2; checks: S against 8 pi^2/(3 |lambda^_min|), Derrick's T/S = 2, and the
#     Fubini profiles in the true potential (stationary in R).
#   - Decay: Gamma/V = A R^-4 exp(-S) with A = 1 (the one-loop prefactor is not computed; A -> 10^{+-k} changes log10 P by
#     +-k); P = (Gamma/V) T_U^4 over the age of the universe T_U = 13.8 Gyr, tau = (Gamma/V)^{-1/4}.  The shift of y_t(M_t)
#     that would make P = 1.  The gravitational correction and the one-loop prefactor are in vacuum_gravity.py and
#     vacuum_prefactor.py.
# The literature starting values and RGEs (Buttazzo et al. NNLO, three-loop running) go through the same steps as a reference.
# Writes results/vacuum_decay.csv and ../ResearchNote/fig_veff.pdf.  Batch: python3 vacuum_decay.py

# %%
import csv
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, minimize_scalar

import sm_rge
from sm_running import K, MPL, RES, lambda_zero, run, starts

HERE = Path(__file__).resolve().parent
NOTE = HERE.parent / "ResearchNote"

# %% [markdown]
# ## The one-loop effective potential (Landau gauge) and its checks

# %%
h, mu, v = sp.symbols("h mu v", positive=True)
la, m2, g1sq, g2sq, g3sq, t, b, tau = sp.symbols("la m2 g1sq g2sq g3sq t b tau", real=True)
gpsq = sp.Rational(3, 5) * g1sq
# (number of degrees of freedom with sign, field-dependent mass^2, constant c)
FIELDS = [("H", 1, -m2 / 2 + 3 * la * h ** 2, sp.Rational(3, 2)), ("G", 3, -m2 / 2 + la * h ** 2, sp.Rational(3, 2)),
          ("W", 6, g2sq * h ** 2 / 4, sp.Rational(5, 6)), ("Z", 3, (g2sq + gpsq) * h ** 2 / 4, sp.Rational(5, 6)),
          ("t", -12, t * h ** 2 / 2, sp.Rational(3, 2)), ("b", -12, b * h ** 2 / 2, sp.Rational(3, 2)),
          ("tau", -4, tau * h ** 2 / 2, sp.Rational(3, 2))]
V0 = -m2 * h ** 2 / 4 + la * h ** 4 / 4
V1 = sum(n * M2 ** 2 * (sp.log(M2 / mu ** 2) - c) for _, n, M2, c in FIELDS) / (64 * sp.pi ** 2)

# check 1: the one-loop RG equation, h^4 and h^2 terms (the h^0 term is the running vacuum energy)
KS = 16 * sp.pi ** 2
one = {k: sp.nsimplify(x, rational=True) for k, x in sm_rge.loops(g1sq, g2sq, g3sq, t, b, tau, la)[0].items()}  # K d/d ln mu^2
dlnmu = {s: 2 * one[k] / KS for s, k in ((g1sq, "g1sq"), (g2sq, "g2sq"), (g3sq, "g3sq"), (t, "ytsq"), (b, "ybsq"),
                                         (tau, "ytausq"), (la, "lam"))}
dlnmu[m2] = 2 * one["m2rel"] * m2 / KS
gam = (3 * t + 3 * b + tau - sp.Rational(9, 4) * g2sq - sp.Rational(3, 4) * gpsq) / KS     # note Eq. (vbeta), Landau gauge
rg = sum(sp.diff(V0, s) * d for s, d in dlnmu.items()) - gam * h * sp.diff(V0, h) + sp.diff(V1, mu) * mu
rg = sp.expand(rg * KS)
print("check 1, one-loop RG equation of V0 + V1 (times K): h^4 term", sp.simplify(rg.coeff(h, 4)), ", h^2 term",
      sp.simplify(rg.coeff(h, 2)))

# check 2: dV1/dh at h = v (m^2 = 2 lambda v^2, Goldstone bosons massless; their term m^4 ln m^2 has zero slope there)
V1noG = sum(n * M2 ** 2 * (sp.log(M2 / mu ** 2) - c) for f, n, M2, c in FIELDS if f != "G") / (64 * sp.pi ** 2)
slope = sp.diff(V1noG, h).subs(h, v).subs(m2, 2 * la * v ** 2)
MW2, MZ2, MH2 = g2sq * v ** 2 / 4, (g2sq + gpsq) * v ** 2 / 4, 2 * la * v ** 2
mt2, mb2, mtau2 = t * v ** 2 / 2, b * v ** 2 / 2, tau * v ** 2 / 2
a0 = lambda x: x * (1 - sp.log(x / mu ** 2))
T_note = (2 * MW2 * (3 * a0(MW2) - 2 * MW2) + MZ2 * (3 * a0(MZ2) - 2 * MZ2) + sp.Rational(3, 2) * MH2 * a0(MH2)
          - 4 * (3 * mt2 * a0(mt2) + 3 * mb2 * a0(mb2) + mtau2 * a0(mtau2))) / (KS * v)       # note Eq. (T), xi = 0
print("check 2, dV1/dh(v) + T(xi = 0):", sp.simplify(sp.expand(sp.expand_log(slope + T_note, force=True))))

pars = (h, mu, la, m2, g1sq, g2sq, g3sq, t, b, tau)
V0f = sp.lambdify(pars, V0, "numpy")
# real part: the scalar masses^2 turn negative where lambda < 0 (ln|M^2|)
V1f = sp.lambdify(pars, sum(n * M2 ** 2 * (sp.log(sp.Abs(M2) / mu ** 2) - c) for _, n, M2, c in FIELDS)
                  / (64 * sp.pi ** 2), "numpy")

# %% [markdown]
# ## RG improvement: lambda_eff(h)

# %%
MU_TOP = 10 * MPL      # run far enough for mu = kappa h with kappa <= 2 and h <= M_Pl


class Improved:
    """V_eff(h) = V(xi h; g(mu), mu), mu = kappa h, xi = exp(-int gamma_Phi d ln mu) from the start of the running"""

    def __init__(self, start, rge, kappa=1.0):
        s0, self.mu0 = starts[start]
        self.sol = run(s0, self.mu0, MU_TOP, rge)
        self.kappa = kappa
        gam_t = lambda lt: (lambda y: (3 * y[3] + 3 * y[4] + y[5] - 9 / 4 * y[1] - 3 / 4 * 3 / 5 * y[0]) / K)(self.sol.sol(lt))
        self.Gamma = solve_ivp(lambda lt, g: [gam_t(lt)], (math.log(self.mu0), math.log(MU_TOP)), [0.0], method="DOP853",
                               rtol=1e-12, atol=1e-14, dense_output=True)
        self.lam_zero = lambda_zero(self.sol)

    def couplings(self, mu):
        return self.sol.sol(math.log(mu))

    def lam_eff(self, hval, loop=True, rescale=True):
        """rescale = True: 4 V(xi h; g(mu), mu)/h^4 for the field h normalized at the start of the running (instability
        scale); rescale = False: 4 V(h; g(mu), mu)/h^4 for the canonical field at mu (the bounce, whose kinetic term
        carries the same xi^2)"""
        muv = self.kappa * hval
        g1, g2, g3, tt, bb, ta, lm, mm2 = self.couplings(muv)
        hh = math.exp(-self.Gamma.sol(math.log(muv))[0]) * hval if rescale else hval
        V = V0f(hh, muv, lm, mm2, g1, g2, g3, tt, bb, ta)
        if loop:
            V += V1f(hh, muv, lm, mm2, g1, g2, g3, tt, bb, ta)
        return 4 * V / hval ** 4


def scales(imp, hmin=1e4, hmax=MPL, rescale=True):
    """the zero Lambda_I and the minimum (lambda_min, h_min) of lambda_eff for hmin <= h <= hmax"""
    f = lambda x: imp.lam_eff(math.exp(x), rescale=rescale)
    lh = np.linspace(math.log(hmin), math.log(hmax), 800)
    le = np.array([f(x) for x in lh])
    i = np.nonzero(np.sign(le[:-1]) != np.sign(le[1:]))[0]
    LI = math.exp(brentq(f, lh[i[0]], lh[i[0] + 1], xtol=1e-12)) if len(i) else float("nan")
    j = int(np.argmin(le))
    if 0 < j < len(lh) - 1:
        r = minimize_scalar(f, bracket=(lh[j - 1], lh[j], lh[j + 1]), tol=1e-12)
        hm, lm = math.exp(r.x), r.fun
    else:
        hm, lm = math.exp(lh[j]), le[j]      # at the edge: no minimum below hmax
    return LI, hm, lm, (lh, le)


CASES = [("note", "B_note_PDG_yt_QCD3", ("note", 2), 1.0),
         ("note, kappa = 1/2", "B_note_PDG_yt_QCD3", ("note", 2), 0.5),
         ("note, kappa = 2", "B_note_PDG_yt_QCD3", ("note", 2), 2.0),
         ("note, one-loop running", "B_note_PDG_yt_QCD3", ("note", 1), 1.0),
         ("note, yt one-loop matching", "B_note_PDG_yt_one_loop", ("note", 2), 1.0),
         ("note matching of the Buttazzo inputs (M_t = 173.34 GeV)", "A_note_at_Buttazzo_inputs_yt_QCD3", ("note", 2), 1.0),
         ("reference: note start, literature 3-loop running", "B_note_PDG_yt_QCD3", ("lit", 3), 1.0),
         ("reference: Buttazzo NNLO start, literature 3-loop running", "A_Buttazzo_NNLO", ("lit", 3), 1.0)]
imps, res = {}, {}
for name, start, rge, kappa in CASES:
    imp = Improved(start, rge, kappa)
    LI, hx, lx, curve = scales(imp)                       # the field normalized at the start (xi included)
    _, hm, lm, curve_c = scales(imp, rescale=False)       # the canonical field: the bounce
    imps[name], res[name] = imp, {"LI": LI, "hmin": hm, "lmin": lm, "lmin_xi": lx, "hmin_xi": hx, "curve": curve,
                                  "curve_c": curve_c, "Lambda_lambda": imp.lam_zero}
    print("%-58s Lambda_lambda = 10^%.2f GeV, Lambda_I = 10^%.2f GeV (lambda_eff with xi: min %+.5f at 10^%.2f GeV);"
          " canonical field: min %+.5f at 10^%.2f GeV" % (name, math.log10(imp.lam_zero), math.log10(LI), lx,
                                                          math.log10(hx), lm, math.log10(hm)))

# %% [markdown]
# ## The bounce
# phi = h/h_s, rho = r h_s (h_s = h_min): phi'' + 3 phi'/rho = dv/dphi, v(phi) = lambda_eff(h_s phi) phi^4/4.
# Too large phi(0): the field crosses 0 (overshoot); too small: it turns back towards larger fields (undershoot).
# For constant lambda < 0 every phi(0) gives a Fubini solution; the running selects the stationary one.

# %%
class Bounce:
    def __init__(self, imp, hs, hlo=1e4, hhi=None):
        self.hs = hs
        hhi = hhi or MU_TOP / max(imp.kappa, 1.0) / 1.0001
        lh = np.linspace(math.log(hlo), math.log(hhi), 1500)
        self.spl = CubicSpline(lh, [imp.lam_eff(math.exp(x), rescale=False) for x in lh])
        self.dspl = self.spl.derivative()
        self.lhlo, self.lhhi = lh[0], lh[-1]

    def lam(self, phi):
        x = min(max(math.log(self.hs * max(phi, 1e-300)), self.lhlo), self.lhhi)
        return float(self.spl(x)), (float(self.dspl(x)) if self.lhlo < x < self.lhhi else 0.0)

    def v(self, phi):
        return self.lam(phi)[0] * phi ** 4 / 4

    def dv(self, phi):
        l, dl = self.lam(phi)
        return phi ** 3 * (l + dl / 4)

    def shoot(self, phi0, rho_max=None):
        """integrate out to rho_max (where the field has fallen to ~1e-8 phi0) and classify by the asymptotic constant
        a = phi + rho phi'/2 of the free tail phi = a + c/rho^2: a < 0 overshoot (crosses 0), a > 0 undershoot"""
        rho_max = rho_max or 3e4 / phi0
        rho0 = 1e-6 / phi0
        y0 = [phi0 + self.dv(phi0) * rho0 ** 2 / 8, self.dv(phi0) * rho0 / 4]
        over = lambda r, y: y[0]
        over.terminal, over.direction = True, -1
        turn = lambda r, y: y[1]
        turn.terminal, turn.direction = True, 1
        sol = solve_ivp(lambda r, y: [y[1], self.dv(y[0]) - 3 * y[1] / r], (rho0, rho_max), y0, method="DOP853",
                        rtol=1e-12, atol=1e-30, events=(over, turn), dense_output=True)
        if sol.t_events[0].size:
            return "over", sol, -1.0
        if sol.t_events[1].size:
            return "under", sol, 1.0
        asym = sol.y[0, -1] + sol.t[-1] * sol.y[1, -1] / 2
        return ("over" if asym < 0 else "under"), sol, asym / phi0

    def solve(self, lo, hi, n=60):
        """bisection on ln phi(0) between lo and hi, which must shoot differently"""
        klo, khi = self.shoot(lo)[0], self.shoot(hi)[0]
        assert klo != khi, (klo, khi)
        a, b2 = math.log(lo), math.log(hi)
        for _ in range(n):
            mid = 0.5 * (a + b2)
            if self.shoot(math.exp(mid))[0] == klo:
                a = mid
            else:
                b2 = mid
        self.phi0 = math.exp(0.5 * (a + b2))
        self.sol = self.shoot(self.phi0)[1]
        return self.phi0

    def action(self):
        """S = 2 pi^2 int rho^3 (phi'^2/2 + v) up to the point where the trajectory leaves the bounce"""
        r = np.geomspace(self.sol.t[0], self.sol.t[-1], 20001)
        y = self.sol.sol(r)
        f = r ** 3 * (0.5 * y[1] ** 2 + np.array([self.v(p) for p in y[0]]))
        kin = r ** 3 * 0.5 * y[1] ** 2
        trap = lambda g: float(np.sum(0.5 * (g[1:] + g[:-1]) * np.diff(r)))
        return 2 * math.pi ** 2 * trap(f), 2 * math.pi ** 2 * trap(kin), r, y


for name in ("note", "reference: Buttazzo NNLO start, literature 3-loop running"):
    imp, rr = imps[name], res[name]
    bo = Bounce(imp, rr["hmin"])
    phi0 = bo.solve(2.0, 3.0)
    S, Tkin, r, y = bo.action()
    lc, _ = bo.lam(phi0)
    # the Fubini radius of the bounce: phi(0) = sqrt(8/|lambda|)/R
    R = math.sqrt(8 / abs(rr["lmin"])) / phi0
    print("%s: bounce phi(0) = %.6f (h(0) = 10^%.3f GeV), R = %.3f/h_min (1/R = 10^%.2f GeV); S = %.3f, "
          "8 pi^2/(3|lambda_min|) = %.3f, 8 pi^2/(3|lambda_eff(h(0))|) = %.3f; kinetic T/S = %.6f (Derrick, d = 4: T/S = 2)"
          % (name, phi0, math.log10(phi0 * rr["hmin"]), R, math.log10(rr["hmin"] / R), S,
             8 * math.pi ** 2 / (3 * abs(rr["lmin"])), 8 * math.pi ** 2 / (3 * abs(lc)), Tkin / S))
    rr.update({"phi0": phi0, "S": S, "R": R / rr["hmin"], "bounce": (r, y)})
    # independent check: the Fubini profiles phi = phi_c/(1 + rho^2/rho_R^2), phi_c = sqrt(8/|lambda_min|)/rho_R, in the true
    # potential; the action is stationary in rho_R at the bounce
    def s_fubini(lr):
        rhoR = math.exp(lr)
        rho = np.geomspace(1e-4 * rhoR, 1e5 * rhoR, 40001)
        ph = math.sqrt(8 / abs(rr["lmin"])) / rhoR / (1 + (rho / rhoR) ** 2)
        dph = -2 * ph * rho / rhoR ** 2 / (1 + (rho / rhoR) ** 2)
        g = rho ** 3 * (0.5 * dph ** 2 + np.array([bo.v(x) for x in ph]))
        return 2 * math.pi ** 2 * float(np.sum(0.5 * (g[1:] + g[:-1]) * np.diff(rho)))
    lrs = np.linspace(math.log(R) - 3, math.log(R) + 3, 61)
    sf = [s_fubini(x) for x in lrs]
    k = int(np.argmax(sf)) if sf[30] > sf[0] else int(np.argmin(sf))
    ext = minimize_scalar(lambda x: (-1 if sf[30] > sf[0] else 1) * s_fubini(x), bracket=(lrs[k - 1], lrs[k], lrs[k + 1]),
                          tol=1e-10)
    print("    Fubini profiles in the true potential: S stationary (%s) at rho_R = %.3f (bounce: %.3f), S = %.3f "
          "(shooting %.3f, rel. %.1e)" % ("maximum" if sf[30] > sf[0] else "minimum", math.exp(ext.x), R,
                                         s_fubini(ext.x), S, s_fubini(ext.x) / S - 1))
    rr["S_fubini_family"] = s_fubini(ext.x)

# %% [markdown]
# ## Decay probability and lifetime
# Gamma/V = A R^-4 exp(-S) with the Fubini radius R of the bounce (A = 1 here; the one-loop prefactor is in
# vacuum_prefactor.py.  A factor 10^{+-k} in A changes log10 P by +-k, against S/ln 10 ~ 10^3).  P = (Gamma/V) T_U^4
# (T_U = 13.8 Gyr); the lifetime
# tau = (Gamma/V)^{-1/4} = R exp(S/4).  The other cases use the Fubini estimate S = 8 pi^2/(3|lambda_min|) and
# R = sqrt(8/|lambda_min|)/(2.32 h_min) (the bounce of the main case has phi(0) = h(0)/h_min = 2.32).

# %%
HBAR_GEV_S, YEAR_S = 6.582119569e-25, 3.15576e7
T_U = 13.8e9 * YEAR_S / HBAR_GEV_S                 # GeV^-1
for name, *_ in CASES:
    rr = res[name]
    if "S" not in rr:
        rr["S"] = 8 * math.pi ** 2 / (3 * abs(rr["lmin"]))
        rr["R"] = math.sqrt(8 / abs(rr["lmin"])) / (2.32 * rr["hmin"])
    rr["log10P"] = 4 * math.log10(T_U / rr["R"]) - rr["S"] / math.log(10)
    rr["log10tau_yr"] = math.log10(rr["R"] * HBAR_GEV_S / YEAR_S) + rr["S"] / (4 * math.log(10))
    print("%-58s S = %8.1f, 1/R = 10^%.2f GeV, log10 P = %+.0f, tau = 10^%.0f yr" % (name, rr["S"], -math.log10(rr["R"]),
          rr["log10P"], rr["log10tau_yr"]))
# P = 1 needs S = 4 ln(T_U/R), with R of the main case
Scrit = 4 * math.log(T_U / res["note"]["R"])
print("P = 1 at S = %.1f, i.e. |lambda_min| = %.4f" % (Scrit, 8 * math.pi ** 2 / (3 * Scrit)))

# %% [markdown]
# ## How far is the boundary?  Shift y_t(M_t) of the main start until P = 1 (the note's RGEs)

# %%
def lmin_for_dyt(dyt):
    s0, mu0 = starts["B_note_PDG_yt_QCD3"]
    s1 = list(s0)
    s1[3] = (math.sqrt(s0[3]) + dyt) ** 2
    starts["_shifted"] = (s1, mu0)
    imp = Improved("_shifted", ("note", 2))
    return scales(imp, rescale=False)[2], imp


lcrit = -8 * math.pi ** 2 / (3 * Scrit)
dyt_crit = brentq(lambda d: lmin_for_dyt(d)[0] - lcrit, 0.0, 0.05, xtol=1e-7)
yt0 = math.sqrt(starts["B_note_PDG_yt_QCD3"][0][3])
print("P = 1 needs y_t(M_t) = %.4f + %.4f (relative %+.2f%%; at tree level M_t larger by about %.1f GeV)"
      % (yt0, dyt_crit, 100 * dyt_crit / yt0, 172.57 * dyt_crit / yt0))

# %% [markdown]
# ## Figure and table

# %%
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use(str(NOTE / "physrev.mplstyle"))
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.6))
STY = {"note": ("C0", "-"), "note, one-loop running": ("C1", "-"), "note, yt one-loop matching": ("C2", "-"),
       "note matching of the Buttazzo inputs (M_t = 173.34 GeV)": ("C4", "-"),
       "reference: note start, literature 3-loop running": ("C0", "--"),
       "reference: Buttazzo NNLO start, literature 3-loop running": ("C3", "--")}
LAB = {"note": "note (PDG 2024 start, note RGEs)", "note, one-loop running": "note, one-loop RGEs",
       "note, yt one-loop matching": r"note, $y_t$ one-loop matching",
       "note matching of the Buttazzo inputs (M_t = 173.34 GeV)": r"note matching, $M_t=173.34$ inputs",
       "reference: note start, literature 3-loop running": "note start, literature 3-loop RGEs (ref.)",
       "reference: Buttazzo NNLO start, literature 3-loop running": "Buttazzo NNLO start, lit. 3-loop (ref.)"}
for name, (c, ls) in STY.items():
    lh, le = res[name]["curve"]
    ax[0].plot(lh / math.log(10), le, ls, color=c, label=LAB[name])
    lh, le = res[name]["curve_c"]
    ax[1].plot(lh / math.log(10), le, ls, color=c)
lo = res["note, kappa = 1/2"]["curve_c"][1]
hi = res["note, kappa = 2"]["curve_c"][1]
ax[1].fill_between(res["note"]["curve_c"][0] / math.log(10), np.minimum(lo, hi), np.maximum(lo, hi), color="C0", alpha=0.25, lw=0)
ax[1].axhline(-8 * math.pi ** 2 / (3 * Scrit), color="k", lw=0.6, ls=":")
ax[1].text(6.3, -8 * math.pi ** 2 / (3 * Scrit) + 0.002, r"$P=1$", fontsize=6)
for a in ax:
    a.axhline(0, color="k", lw=0.4)
    a.set_xlabel(r"$\log_{10}(h/\mathrm{GeV})$")
    a.set_xlim(6, math.log10(MPL))
    a.set_ylim(-0.055, 0.06)
ax[0].set_ylabel(r"$\lambda_{\mathrm{eff}}(h)$ (field at $M_t$)")
ax[1].set_ylabel(r"$\hat\lambda_{\mathrm{eff}}(\hat h)$ (canonical field)")
ax[0].legend(fontsize=5, frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig(NOTE / "fig_veff.pdf")

with open(RES / "vacuum_decay.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["case", "start", "rge", "kappa", "log10_Lambda_lambda_GeV", "log10_Lambda_I_GeV", "lambda_eff_min_xi",
                "log10_h_min_xi_GeV", "lambda_hat_min", "log10_h_min_GeV", "S", "log10_invR_GeV", "log10_P", "log10_tau_yr"])
    for name, start, rge, kappa in CASES:
        rr = res[name]
        w.writerow([name, start, "%s %d" % rge, kappa] + ["%.6g" % x for x in (
            math.log10(rr["Lambda_lambda"]), math.log10(rr["LI"]), rr["lmin_xi"], math.log10(rr["hmin_xi"]), rr["lmin"],
            math.log10(rr["hmin"]), rr["S"], -math.log10(rr["R"]), rr["log10P"], rr["log10tau_yr"])])
    w.writerow(["P_equals_1", "", "", "", "", "", "", "", "%.6g" % (-8 * math.pi ** 2 / (3 * Scrit)), "", "%.6g" % Scrit])
    w.writerow(["delta_yt_for_P_equals_1", "", "", "", "%.6g" % dyt_crit])
print("wrote results/vacuum_decay.csv and ResearchNote/fig_veff.pdf")
