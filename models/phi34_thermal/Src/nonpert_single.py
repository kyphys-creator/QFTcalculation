# %% [markdown]
# # Step (10): the single-field model against the nonperturbative phase diagram (Gould 2021)
#
# Research note models/phi34_thermal, step (10).  The 3D EFT of the model at NLO (Gould, JHEP 04 (2021) 057, Eqs. (2.20)-(2.26),
# with L_b(mu) = 2 ln(mu/T) + 2 gamma_E - 2 ln 4 pi and the constant c = -0.348723) is shifted by phi3 -> phi3 - g3/lambda3
# (Gould, Eq. (3.3)): V3 = sigma~3 phi3 + r phi3^2/2 + lambda3 phi3^4/4!.  A transition can only occur where sigma~3 = 0
# (Eq. (3.4)); it is first order if r < r* there, second order if r = r*, with r*(mu3) from the lattice,
#   r*(mu3) = [0.0015249(48) + ln(3 mu3/lambda3)/(6 (4 pi)^2)] lambda3^2      (Gould, Eq. (3.5)).
# Checks: (a) sigma~3 sqrt(T) equals the T-independent b of the note (Eq. (14)) at NLO, for any mu3;  r - r* does not
# depend on mu3.  (b) At b = 0 (alpha = alpha_deg, kappa_4 = 1) the transition is of second order at tau* where r = r*;
# compared with the tree level, the one-loop matching alone, and the perturbative step of step (4).  (c) For b != 0 the
# reduced external field h = sigma~3/lambda3^(5/2) at tau* stays nonzero: no transition.
# Units m = 1 (mu = m for the 4D MS-bar parameters, as in the note).  Writes results/nonpert_single.csv.
# Batch: `~/miniforge3/envs/qft/bin/python nonpert_single.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)

LOOP = 1 / (4 * math.pi) ** 2
C_G = -0.348723                    # Gould Eq. (2.25)
RSTAR0, DRSTAR0 = 0.0015249, 0.0000048    # Gould Eq. (3.5), from the lattice study of the Z2 theory
GM1 = 1.5261                       # g/m at kappa_3 = 1; kappa_4 = 1, g/m = GM1 (kappa_4/alpha)^(1/2) (note, premise 9)
step4 = {r[0]: float(r[1]) for r in csv.reader(open(os.path.join(HERE, "results", "thermal_single.csv")))
         if r and r[0] in ("alpha_deg", "tau0_deg", "tau_c_deg", "step_phi_over_T_deg", "alpha_window")}
print(step4)


class EFT3:
    """NLO 3D EFT of V = t phi + phi^2/2 + g phi^3/6 + lambda phi^4/24 (m = 1), MS-bar at the 4D scale mu."""

    def __init__(self, alpha, mu=1.0, mu3_over_lam3=1.0, nlo=True, tadpole=True):
        self.alpha, self.mu, self.k3, self.nlo = alpha, mu, mu3_over_lam3, nlo
        self.g = self.g0 = GM1 / math.sqrt(alpha)                   # g/m at mu = m, as in the note
        self.lam = alpha * self.g ** 2 / 3                          # alpha = 3 lambda m^2/g^2
        self.t = self.g / (32 * math.pi ** 2) if tadpole else 0.0   # tadpole-cancelling linear term at mu = m
        if mu != 1.0:   # run the 4D parameters from m to mu at one loop (beta functions of the zero-temperature note)
            ln = math.log(mu)
            g, l = self.g, self.lam
            self.t += g * 1.0 * LOOP * ln
            self.m2 = 1.0 + (g * g + l) * LOOP * ln
            self.g = g * (1 + 3 * l * LOOP * ln)
            self.lam = l * (1 + 3 * l * LOOP * ln)
        else:
            self.m2 = 1.0

    def b(self):
        """b of the note, Eq. (14): the coefficient of chi about the inflection point (4D, T-independent)."""
        return self.t + self.g ** 3 / (3 * self.lam ** 2) - self.g * self.m2 / self.lam

    def params(self, T):
        Lb = 2 * math.log(self.mu / T) + 2 * np.euler_gamma - 2 * math.log(4 * math.pi)
        g, l, m2, t = self.g, self.lam, self.m2, self.t
        tb = t - 0.5 * (g * m2 * LOOP) * Lb                         # kappa-bar = kappa - beta_kappa L_b/2 (Gould Eq. (2.26))
        m2b = m2 - 0.5 * ((g * g + l * m2) * LOOP) * Lb
        gb = g - 0.5 * (3 * g * l * LOOP) * Lb
        lb = l - 0.5 * (3 * l * l * LOOP) * Lb
        g3, l3 = math.sqrt(T) * gb, T * lb
        mu3 = self.k3 * l3
        two = (math.log(mu3 / (3 * T)) - C_G) / 6 * LOOP if self.nlo else 0.0
        s3 = (tb + gb * T * T / 24) / math.sqrt(T) + g3 * l3 * two
        m3 = m2b + lb * T * T / 24 + l3 * l3 * two
        sig = s3 + g3 ** 3 / (3 * l3 ** 2) - g3 * m3 / l3                  # Gould Eq. (3.3)
        r = m3 - g3 ** 2 / (2 * l3)
        rs = (RSTAR0 + math.log(3 * mu3 / l3) / 6 * LOOP) * l3 ** 2 if self.nlo else 0.0
        return dict(sig=sig, r=r, rstar=rs, l3=l3, x=(r - rs) / l3 ** 2, h=sig / l3 ** 2.5)

    def tau_star(self, drs=0.0):
        """tau = g T/m^2 (g at mu = m) at which r = r* (+ drs lambda3^2)."""
        f = lambda T: self.params(T)["x"] - drs
        return self.g0 * brentq(f, 0.5, 20.0, xtol=1e-14)


# %% [markdown]
# ## Inspect: the diagrams behind the NLO matching relations (Gould 2021, Eqs. (2.20)-(2.26))
#
# One loop: the 3D couplings and the one-loop parts of the mass and tadpole; two loops: their NLO terms.
#
# Drawn by diagrams_thermal.wl (FeynArts) into ../figs/diagrams/; shown before anything is evaluated, only in the
# interactive window.

# %%
if INTERACTIVE:
    from IPython.display import Image, display
    for name in ("oneloop.png", "twoloop.png"):
        fig = os.path.join(HERE, "..", "figs", "diagrams", name)
        display(Image(filename=fig)) if os.path.exists(fig) else print("run diagrams_thermal.wl first:", fig, "is missing")


# %% [markdown]
# ## (a) sigma~3 sqrt(T) = b at NLO, and r - r* independent of mu3

# %%
a_deg = step4["alpha_deg"]
for a in (0.9, a_deg, 1.05):
    for k3 in (0.0786, 1.0, 10.0):
        e = EFT3(a, mu3_over_lam3=k3)
        devs = [e.params(T)["sig"] * math.sqrt(T) / e.b() - 1 if abs(e.b()) > 1e-12 else e.params(T)["sig"] * math.sqrt(T)
                for T in (2.0, 4.0, 8.0)]
        xs = [e.params(T)["x"] for T in (2.0, 4.0, 8.0)]
        print(f"alpha = {a:.6f}, mu3/lambda3 = {k3}: b = {e.b():+.6e};  sigma~3 sqrt(T)/b - 1 at T = 2, 4, 8 m: "
              f"{', '.join(f'{d:+.1e}' for d in devs)};  (r - r*)/lambda3^2 = {', '.join(f'{x:.12f}' for x in xs)}")
print("note, step (4): alpha_deg =", a_deg, "(b = 0)")


# %% [markdown]
# ## (b) b = 0: the second-order point tau*, against tree level, one-loop matching and the perturbative step

# %%
e = EFT3(a_deg)
tau_star = e.tau_star()
dtau = (e.tau_star(drs=-DRSTAR0) - e.tau_star(drs=DRSTAR0)) / 2
tau_lo = EFT3(a_deg, nlo=False).tau_star()
gm = e.g0
tau_tree = math.sqrt(72 / a_deg * (1.5 / a_deg - 1))        # note, Eq. (15) with b = 0
mus = {mu: EFT3(a_deg, mu=mu).tau_star() for mu in (0.5, 2.0)}
print(f"tau* (second order, NLO + lattice r*) = {tau_star:.6f} +- {abs(dtau):.1e} (r* error);  4D scale mu = m/2, 2m: "
      f"{mus[0.5]:.6f}, {mus[2.0]:.6f}")
print(f"tree level (T^2 term only) {tau_tree:.6f};  one-loop matching, r = 0: {tau_lo:.6f};  perturbative step (4): "
      f"V''(0) = 0 at {step4['tau0_deg']:.6f}, first-order step at tau_c = {step4['tau_c_deg']:.6f} with phi/T = "
      f"{step4['step_phi_over_T_deg']:.4f}")
print(f"tau*/tau_c - 1 = {tau_star / step4['tau_c_deg'] - 1:+.3e};  T* = {tau_star / gm:.5f} m = {tau_star / gm * 125.25:.3f} GeV")
# the NLO part of r - r*, relative to the thermal mass lambda T^2/24
T = tau_star / gm
p = e.params(T)
shift = (p["x"] * p["l3"] ** 2 - EFT3(a_deg, nlo=False).params(T)["x"] * p["l3"] ** 2) / (e.lam * T * T / 24)
print(f"(two-loop mass - r*)/(lambda T^2/24) at tau* = {shift:+.4f}")


# %% [markdown]
# ## (c) b != 0: the reduced field h = sigma~3/lambda3^(5/2) where r = r*

# %%
rows_c = []
for da in (-1e-2, -1e-4, -step4["alpha_window"], step4["alpha_window"], 1e-4, 1e-2):
    ea = EFT3(a_deg + da)
    ts = ea.tau_star()
    pp = ea.params(ts / ea.g0)
    rows_c.append((da, ea.b(), ts, pp["h"]))
    print(f"alpha - alpha_deg = {da:+.3e}: b = {ea.b():+.3e} m^3, tau* = {ts:.6f}, h = sigma~3/lambda3^(5/2) = {pp['h']:+.3e} "
          f"(nonzero: no transition, a crossover)")


# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "nonpert_single.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["quantity", "value", "reference"])
    wr.writerows([["alpha_deg", a_deg, "step (4)"], ["tau_star_second_order", tau_star, ""], ["tau_star_rstar_error", abs(dtau), ""],
                  ["tau_star_mu_half", mus[0.5], ""], ["tau_star_mu_two", mus[2.0], ""], ["tau_tree", tau_tree, ""],
                  ["tau_one_loop_matching", tau_lo, ""], ["tau0_perturbative", step4["tau0_deg"], "step (4)"],
                  ["tau_c_perturbative", step4["tau_c_deg"], "step (4)"], ["T_star_GeV", tau_star / gm * 125.25, ""],
                  ["twoloop_minus_rstar_over_thermal_mass", shift, ""]])
    wr.writerow([])
    wr.writerow(["alpha_minus_alpha_deg", "b_m3", "tau_star", "h"])
    wr.writerows(rows_c)
print("wrote results/nonpert_single.csv")
