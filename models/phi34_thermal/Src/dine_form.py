# %% [markdown]
# # Step (1): the high-temperature potential of Dine et al., its critical temperatures, and the nucleation temperature
#
# Research note models/phi34_thermal, step (1).  The high-temperature potential (Dine, Leigh, Huet, Linde, Linde 1992,
# Eqs. (7)-(11))
#   V(phi, T) = D (T^2 - T0^2) phi^2 - E T phi^3 + lambda_T phi^4/4
# is the phi^3 + phi^4 potential of the zero-temperature note (models/phi34, Eq. (13)) with
#   m^2 = M^2(T) = 2 D (T^2 - T0^2),   g = -6 E T,   lambda = 6 lambda_T,
#   alpha(T) = 3 lambda m^2/g^2 = lambda_T M^2/(2 E^2 T^2) = (lambda_T D/E^2)(1 - T0^2/T^2)     (note, App. A).
# Hence the critical temperatures alpha = 9/8 (T1, second minimum appears), 1 (Tc, degenerate), 0 (T0, phi = 0 unstable),
# and the three-dimensional bounce action from step (9) of the zero-temperature note,
#   S3/T = M^3 S3(alpha)/(36 E^2 T^3) = (E/36) (2 alpha/lambda_T)^(3/2) S3(alpha).
# Nucleation (note, App. B): Gamma = T^4 (S3/(2 pi T))^(3/2) exp(-S3/T) = H^4, H = 1.66 sqrt(g*) T^2/M_Pl;
#   beta/H = T d(S3/T)/dT = (S3/T) [3/(2 alpha) + W(alpha)/S3(alpha)] 2 (lambda_T D/E^2 - alpha)   (lambda_T constant),
#   W = dS3/dalpha from step (9).
# Checks: the closed-form critical temperatures against the numerical minima of V(phi, T); S3/T against the fit of Dine
# et al. (Eqs. (26), (27)); beta/H against a numerical derivative; Gamma/H^4 = 1 at T_n.
# SM-like benchmark: Dine et al. Eqs. (8)-(11) with today's masses; lambda_T is evaluated at T_c (Dine et al.: lambda_T1,
# lambda_Tc, lambda_T0 are equal to good accuracy).
# Input: ../../phi34/Src/results/bounce.csv (d = 3: S3(alpha), W(alpha)).  Writes results/dine_form.csv.
# Batch: `~/miniforge3/envs/qft/bin/python dine_form.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.interpolate import CubicHermiteSpline
from scipy.optimize import brentq, minimize_scalar

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
MPL = 1.22091e19                                   # Planck mass [GeV]
GSTAR = 106.75
MW, MZ, MT, MH, VEV = 80.37, 91.19, 172.6, 125.25, 246.22     # GeV
LN_AB, LN_AF = 2 * math.log(4 * math.pi) - 2 * np.euler_gamma, 2 * math.log(math.pi) - 2 * np.euler_gamma


# %% [markdown]
# ## S3(alpha) from step (9) of the zero-temperature note, with its thin-wall continuation

# %%
src = os.path.join(HERE, "..", "..", "phi34", "Src", "results", "bounce.csv")
rows = [r for r in csv.reader(open(src)) if r and r[0] == "3"]
A3 = np.array([float(r[1]) for r in rows])
S3a = np.array([float(r[3]) for r in rows])
W3a = np.array([float(r[6]) for r in rows])
lnS3 = CubicHermiteSpline(A3, np.log(S3a), W3a / S3a)
TW3 = 32 * math.pi / 9
# beyond the last point (alpha = 0.99): (1 - alpha)^2 S3/TW3 = 1 + c1 (1 - alpha) + c2 (1 - alpha)^2, fitted on alpha >= 0.94
sel = A3 >= 0.94
c_tw = np.polyfit(1 - A3[sel], (1 - A3[sel]) ** 2 * S3a[sel] / TW3, 2)


def s3(a):
    """S3(alpha) of the zero-temperature note (d = 3), S3 = S_3 g^2/m^3."""
    if a <= A3[-1]:
        return float(np.exp(lnS3(a)))
    x = 1 - a
    return TW3 / x ** 2 * float(np.polyval(c_tw, x))


def w3(a):
    """dS3/dalpha."""
    if a <= A3[-1]:
        return float(lnS3(a, 1)) * s3(a)
    x = 1 - a
    p, dp = float(np.polyval(c_tw, x)), float(np.polyval(np.polyder(c_tw), x))
    return TW3 * (2 * p / x ** 3 - dp / x ** 2)


print(f"S3(alpha): {len(A3)} points of step (9); thin-wall continuation c = {c_tw[::-1]} (intercept 1 expected)")
print(f"continuity at alpha = 0.99: spline {s3(0.99):.6f}, continuation {TW3 / 0.01 ** 2 * float(np.polyval(c_tw, 0.01)):.6f}")


# %% [markdown]
# ## The SM-like coefficients (Dine et al. Eqs. (4), (8)-(11))

# %%
D = (2 * MW ** 2 + MZ ** 2 + 2 * MT ** 2) / (8 * VEV ** 2)
E = (2 * MW ** 3 + MZ ** 3) / (4 * math.pi * VEV ** 3)
B = 3 / (64 * math.pi ** 2 * VEV ** 4) * (2 * MW ** 4 + MZ ** 4 - 4 * MT ** 4)
T0 = math.sqrt((MH ** 2 - 8 * B * VEV ** 2) / (4 * D))
LAM = MH ** 2 / (2 * VEV ** 2)


def lam_T(T):
    return LAM - 3 / (16 * math.pi ** 2 * VEV ** 4) * (
        2 * MW ** 4 * (math.log(MW ** 2 / T ** 2) - LN_AB) + MZ ** 4 * (math.log(MZ ** 2 / T ** 2) - LN_AB)
        - 4 * MT ** 4 * (math.log(MT ** 2 / T ** 2) - LN_AF))


# T_c with lambda_T evaluated at T_c (fixed point of T_c^2 = T0^2/(1 - E^2/(lambda_T(T_c) D)))
Tc = T0
for _ in range(50):
    Tc = T0 / math.sqrt(1 - E ** 2 / (lam_T(Tc) * D))
LT = lam_T(Tc)
print(f"D = {D:.6f}, E = {E:.6e}, B = {B:.6e}, T0 = {T0:.4f} GeV, lambda = {LAM:.5f}, lambda_T(T_c) = {LT:.5f}")


# %% [markdown]
# ## The map to alpha, and the critical temperatures (closed form vs numerical minima)

# %%
R = LT * D / E ** 2                                # alpha(T) = R (1 - T0^2/T^2)


def alpha(T):
    return R * (1 - T0 ** 2 / T ** 2)


def T_of_alpha(a):
    return T0 / math.sqrt(1 - a / R)


def V(phi, T):
    return D * (T * T - T0 * T0) * phi * phi - E * T * phi ** 3 + LT / 4 * phi ** 4


crit = {"T1": (9 / 8, 1.5), "Tc": (1.0, 2.0), "T0": (0.0, 3.0)}           # alpha, phi/(E T/lambda_T)
num = {}
# T1: the second minimum appears (V' has a double root); Tc: the two minima are degenerate
def second_min(T):
    r = minimize_scalar(lambda p: V(p, T), bounds=(0.5 * E * T / LT, 4 * E * T / LT), method="bounded",
                        options={"xatol": 1e-14 * T})
    return r.x, r.fun


num["Tc"] = brentq(lambda T: second_min(T)[1], T0 * (1 + 1e-9), T_of_alpha(1.05), xtol=1e-14)
disc = lambda T: (3 * E * T) ** 2 - 8 * LT * D * (T * T - T0 * T0)      # V'/phi = 2DM - 3ETphi + lam phi^2: discriminant
num["T1"] = brentq(disc, T0 * (1 + 1e-9), T0 * 1.1, xtol=1e-14)
for key, (a, cphi) in crit.items():
    Tcf = T_of_alpha(a)
    line = f"{key}: closed form {Tcf:.10f} GeV (alpha = {a})"
    if key in num:
        line += f",  numerical {num[key]:.10f} GeV (rel. {num[key] / Tcf - 1:.1e})"
        if key == "Tc":
            line += f";  phi_c/T_c = {second_min(num['Tc'])[0] / num['Tc']:.8f} vs 2E/lambda_T = {2 * E / LT:.8f}"
    print(line)


# %% [markdown]
# ## S3/T, the nucleation temperature, beta/H

# %%
def s3_over_T(T):
    a = alpha(T)
    return E / 36 * (2 * a / LT) ** 1.5 * s3(a)


def dine_fit(T):
    a = alpha(T)
    M = math.sqrt(2 * D * (T * T - T0 * T0))
    return 4.85 * M ** 3 / (E ** 2 * T ** 3) * (1 + a / 4 * (1 + 2.4 / (1 - a) + 0.26 / (1 - a) ** 2))


def hubble(T):
    return 1.66 * math.sqrt(GSTAR) * T ** 2 / MPL


def nucleation(T):
    """ln(Gamma/H^4)."""
    s = s3_over_T(T)
    return 4 * math.log(T) + 1.5 * math.log(s / (2 * math.pi)) - s - 4 * math.log(hubble(T))


Tn = brentq(nucleation, T_of_alpha(0.3), T_of_alpha(0.99999), xtol=1e-13)
an = alpha(Tn)
sn = s3_over_T(Tn)
bH = sn * (1.5 / an + w3(an) / s3(an)) * 2 * (R - an)
cd = lambda h: Tn * (s3_over_T(Tn + h) - s3_over_T(Tn - h)) / (2 * h)
h = 1e-6 * Tn
bH_num = (4 * cd(h / 2) - cd(h)) / 3                 # Richardson on the central difference
phin = (2 * D * (Tn ** 2 - T0 ** 2)) / (-6 * E * Tn) * (-9 / (2 * an) * (1 + math.sqrt(1 - 8 * an / 9)))   # (m^2/g) f_-
print(f"T_n = {Tn:.6f} GeV (T_c - T_n = {num['Tc'] - Tn:.3e} GeV), alpha(T_n) = {an:.6f}, S3/T = {sn:.4f}, "
      f"ln(Gamma/H^4) at T_n = {nucleation(Tn):.1e}")
print(f"S3/T at T_n: this note {sn:.4f}, Dine et al.'s fit {dine_fit(Tn):.4f} (rel. {dine_fit(Tn) / sn - 1:+.4f})")
print(f"beta/H = {bH:.6e} (analytic), {bH_num:.6e} (numerical derivative), rel. {bH_num / bH - 1:.1e};  "
      f"phi_n/T_n = {phin / Tn:.5f}")


# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "dine_form.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["quantity", "value"])
    for k, v in (("D", D), ("E", E), ("B", B), ("T0", T0), ("lambda", LAM), ("lambda_T_Tc", LT), ("R", R),
                 ("T1", T_of_alpha(9 / 8)), ("Tc", T_of_alpha(1.0)), ("Tc_numerical", num["Tc"]), ("T1_numerical", num["T1"]),
                 ("phic_over_Tc", 2 * E / LT), ("Tn", Tn), ("alpha_n", an), ("S3_over_T_n", sn), ("dine_fit_n", dine_fit(Tn)),
                 ("beta_over_H", bH), ("beta_over_H_numerical", bH_num), ("phin_over_Tn", phin / Tn)):
        wr.writerow([k, v])
print("wrote results/dine_form.csv")
