"""tptlib.py -- shared functions of the finite-temperature note (models/phi34_thermal).

The high-temperature potential of Dine et al. (note, Eq. (1)), V = D (T^2 - T0^2) phi^2 - E T phi^3 + lambda_T phi^4/4, is the
phi^3 + phi^4 potential of the zero-temperature note with alpha(T) = R (1 - T0^2/T^2), R = lambda_T D/E^2 (note, App. A).
  s3(a), w3(a)        S3(alpha) of the zero-temperature note (d = 3) and dS3/dalpha (Hermite interpolation of step (9),
                      thin-wall continuation beyond alpha = 0.99)
  fminus(a), v(f, a)  the second minimum f_- of v(f) = f^2/2 + f^3/6 + alpha f^4/72, and v
  DineForm            critical temperatures, nucleation temperature (Gamma = T^4 (S3/2 pi T)^(3/2) e^(-S3/T) = H^4),
                      beta/H, and the strength alpha_theta = 4 Delta theta/(3 w_+) (Caprini et al. 2020, Eq. (12)) in closed form,
                      Delta theta = D T0^2 phi_-^2/2 (note, Apps. B, C).
"""
import csv
import math
import os

import numpy as np
from scipy.interpolate import CubicHermiteSpline
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MPL = 1.22091e19                                   # Planck mass [GeV]
TW3 = 32 * math.pi / 9

_rows = [r for r in csv.reader(open(os.path.join(HERE, "..", "..", "phi34", "Src", "results", "bounce.csv"))) if r and r[0] == "3"]
A3 = np.array([float(r[1]) for r in _rows])
S3A = np.array([float(r[3]) for r in _rows])
W3A = np.array([float(r[6]) for r in _rows])
_lnS3 = CubicHermiteSpline(A3, np.log(S3A), W3A / S3A)
_sel = A3 >= 0.94
C_TW = np.polyfit(1 - A3[_sel], (1 - A3[_sel]) ** 2 * S3A[_sel] / TW3, 2)


def s3(a):
    """S3(alpha) of the zero-temperature note (d = 3), S3 = S_3 g^2/m^3."""
    if a <= A3[-1]:
        return float(np.exp(_lnS3(a)))
    x = 1 - a
    return TW3 / x ** 2 * float(np.polyval(C_TW, x))


def w3(a):
    """dS3/dalpha."""
    if a <= A3[-1]:
        return float(_lnS3(a, 1)) * s3(a)
    x = 1 - a
    p, dp = float(np.polyval(C_TW, x)), float(np.polyval(np.polyder(C_TW), x))
    return TW3 * (2 * p / x ** 3 - dp / x ** 2)


def fminus(a):
    return -9 / (2 * a) * (1 + math.sqrt(1 - 8 * a / 9))


def v(f, a):
    return f * f / 2 + f ** 3 / 6 + a * f ** 4 / 72


def h(a):
    """Delta V = (E^4 T^4/lambda_T^3) h(alpha), h = -(2 alpha^3/9) v(f_-)."""
    return -2 * a ** 3 / 9 * v(fminus(a), a)


class DineForm:
    def __init__(self, D, E, T0, lamT, gstar=106.75):
        self.D, self.E, self.T0, self.lam, self.gstar = D, E, T0, lamT, gstar
        self.R = lamT * D / E ** 2

    def alpha(self, T):
        return self.R * (1 - self.T0 ** 2 / T ** 2)

    def T_of_alpha(self, a):
        return self.T0 / math.sqrt(1 - a / self.R)

    def V(self, phi, T):
        return self.D * (T * T - self.T0 ** 2) * phi * phi - self.E * T * phi ** 3 + self.lam / 4 * phi ** 4

    def s3T(self, T):
        a = self.alpha(T)
        return self.E / 36 * (2 * a / self.lam) ** 1.5 * s3(a)

    def hubble(self, T):
        return 1.66 * math.sqrt(self.gstar) * T ** 2 / MPL

    def ln_gamma_over_H4(self, T):
        s = self.s3T(T)
        return 4 * math.log(T) + 1.5 * math.log(s / (2 * math.pi)) - s - 4 * math.log(self.hubble(T))

    def nucleation(self, amin=1e-4):
        """T_n, or None if Gamma < H^4 down to alpha = amin."""
        lo, hi = self.T_of_alpha(amin), self.T_of_alpha(min(0.99999, 0.99999 * self.R))
        if self.ln_gamma_over_H4(lo) < 0:
            return None
        return brentq(self.ln_gamma_over_H4, lo, hi, xtol=1e-13 * hi)

    def summary(self, Tn):
        a = self.alpha(Tn)
        sT = self.s3T(Tn)
        bH = sT * (1.5 / a + w3(a) / s3(a)) * 2 * (self.R - a)
        E, lam = self.E, self.lam
        phin = -(a * E * Tn / (3 * lam)) * fminus(a)
        dV = E ** 4 * Tn ** 4 / lam ** 3 * h(a)                    # V(0) - V(phi_-)
        dth = self.D * self.T0 ** 2 * phin ** 2 / 2               # Delta theta = Delta V - (T/4) d(Delta V)/dT
        rho = math.pi ** 2 * self.gstar * Tn ** 4 / 30            # 3 w_+/4
        return dict(Tn=Tn, alpha_n=a, S3T=sT, betaH=bH, phin_Tn=phin / Tn,
                    Tc=self.T_of_alpha(1.0), T1=self.T_of_alpha(9 / 8), dV=dV,
                    alpha_theta=dth / rho, alpha_e=(4 * dth - 3 * dV) / rho)
