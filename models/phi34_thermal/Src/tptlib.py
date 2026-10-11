"""tptlib.py -- shared functions of the finite-temperature note (models/phi34_thermal).

The high-temperature potential of Dine et al. (note, Eq. (1)), V = D (T^2 - T0^2) phi^2 - E T phi^3 + lambda_T phi^4/4, is the
phi^3 + phi^4 potential of the zero-temperature note with alpha(T) = R (1 - T0^2/T^2), R = lambda_T D/E^2 (note, App. A).
  s3(a), w3(a)        S3(alpha) of the zero-temperature note (d = 3) and dS3/dalpha (Hermite interpolation of step (9),
                      thin-wall continuation beyond alpha = 0.99)
  fminus(a), v(f, a)  the second minimum f_- of v(f) = f^2/2 + f^3/6 + alpha f^4/72, and v
  DineForm            critical temperatures, nucleation temperature (Gamma = T^4 (S3/2 pi T)^(3/2) e^(-S3/T) = H^4),
                      beta/H, and the strength alpha_theta = 4 Delta theta/(3 w_+) (Caprini et al. 2020, Eq. (12)) in closed form,
                      Delta theta = D T0^2 phi_-^2/2 (note, Apps. B, C).
  kappa_v, GWSource   efficiency of bulk motion (Espinosa et al. 2010) and the GW spectra today from sound waves
                      (Hindmarsh et al. 2017 erratum, Caprini et al. 2020) and turbulence (Caprini et al. 2016) (note, App. D)
  h2_sens, snr, pls   LISA sensitivity (Science Requirements Document, Eq. (3)), SNR (Caprini et al. 2020, Eq. (33)), and the
                      power-law sensitivity (Thrane and Romano 2013)
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


# ---- gravitational waves from sound waves and turbulence, and the LISA sensitivity (step (3); note, App. D) ----
CS = 1 / math.sqrt(3)                              # sound speed of the radiation fluid
H100 = 1e5 / 3.0856775814913673e22                 # 100 km/s/Mpc [1/s]
H_LITTLE = 0.678                                   # Caprini et al. 2020 (Planck)
T_OBS = 9.46e7                                     # 4 yr x 75 % duty cycle [s] (Caprini et al. 2020; SciRD Sec. 3.6)
OMEGA_TILDE = 1.2e-2                               # Hindmarsh et al. 2017, erratum
Z_P = 10.0                                         # peak of k R_* (Hindmarsh et al. 2017; Caprini et al. 2020 Eq. (31))
EPS_TURB = 0.05                                    # kappa_turb = eps kappa_v (Caprini et al. 2016 Eq. (21))


def v_jouguet(a):
    """Jouguet velocity (Espinosa et al. 2010, Eq. (97))."""
    return (math.sqrt(2 * a / 3 + a * a) + math.sqrt(1 / 3)) / (1 + a)


def kappa_v(a, vw):
    """Efficiency of bulk fluid motion kappa(alpha, xi_w) (Espinosa et al. 2010, Eqs. (95)-(102); log = natural log)."""
    kA = vw ** 1.2 * 6.9 * a / (1.36 - 0.037 * math.sqrt(a) + a)
    kB = a ** 0.4 / (0.017 + (0.997 + a) ** 0.4)
    kC = math.sqrt(a) / (0.135 + math.sqrt(0.98 + a))
    kD = a / (0.73 + 0.083 * math.sqrt(a) + a)
    xJ = v_jouguet(a)
    if vw <= CS:
        return CS ** 2.2 * kA * kB / ((CS ** 2.2 - vw ** 2.2) * kB + vw * CS ** 1.2 * kA)
    if vw < xJ:
        dk = -0.9 * math.log(math.sqrt(a) / (1 + math.sqrt(a)))
        return kB + (vw - CS) * dk + (vw - CS) ** 3 / (xJ - CS) ** 3 * (kC - kB - (xJ - CS) * dk)
    return ((xJ - 1) ** 3 * xJ ** 2.5 * vw ** -2.5 * kC * kD
            / (((xJ - 1) ** 3 - (vw - 1) ** 3) * xJ ** 2.5 * kC + (vw - 1) ** 3 * kD))


def F_gw0(gstar):
    """Redshift factor of Omega_gw to today (Caprini et al. 2020, Eq. (20)); Omega, not h^2 Omega."""
    return 3.57e-5 * (100 / gstar) ** (1 / 3)


def hstar(T, gstar):
    """Hubble rate at T redshifted to today [Hz] (Caprini et al. 2016, Eq. (11))."""
    return 16.5e-6 * (T / 100) * (gstar / 100) ** (1 / 6)


def C_sw(s):
    """Spectral shape of the sound-wave spectrum (Caprini et al. 2020, Eq. (30))."""
    return s ** 3 * (7 / (4 + 3 * s * s)) ** 3.5


class GWSource:
    """Sound waves and turbulence for (alpha_theta, beta/H, T_*, v_w, g*), T_* = T_n."""

    def __init__(self, alpha, betaH, T, vw, gstar=106.75):
        self.alpha, self.betaH, self.T, self.vw, self.gstar = alpha, betaH, T, vw, gstar
        self.kappa = kappa_v(alpha, vw)
        self.K = self.kappa * alpha / (1 + alpha)                         # Caprini et al. 2020, Eq. (11)
        self.Uf = math.sqrt(0.75 * self.K)                                # K = Gamma U_f^2, Gamma = 4/3 (Eq. (22))
        self.HR = (8 * math.pi) ** (1 / 3) * max(vw, CS) / betaH          # Eq. (6)
        self.Htsh = self.HR / self.Uf                                     # shock formation time (Table 1)
        self.fp = 26e-6 / self.HR * (Z_P / 10) * (T / 100) * (gstar / 100) ** (1 / 6)   # Eq. (31) [Hz]
        self.fsw16 = 1.9e-5 / vw * betaH * (T / 100) * (gstar / 100) ** (1 / 6)        # Caprini et al. 2016, Eq. (15)
        self.fturb = 2.7e-5 / vw * betaH * (T / 100) * (gstar / 100) ** (1 / 6)        # Eq. (18)

    def h2_sw(self, f):
        """h^2 dOmega/dln f of sound waves today: Hindmarsh et al. 2017 erratum Eq. (2) (total 3 K^2 H R Omega~),
        times min(1, H tau_sh) (Caprini et al. 2020, Eq. (32))."""
        return (H_LITTLE ** 2 * 3 * 0.687 * F_gw0(self.gstar) * self.K ** 2 * self.HR * OMEGA_TILDE
                * min(1.0, self.Htsh) * C_sw(f / self.fp))

    def h2_sw_c20(self, f):
        """Caprini et al. 2020, Eqs. (29), (32) as printed (total K^2 H R/c_s Omega~; suppression H R/K^(1/2))."""
        return (H_LITTLE ** 2 * 0.687 * F_gw0(self.gstar) * self.K ** 2 * self.HR / CS * OMEGA_TILDE
                * min(1.0, self.HR / math.sqrt(self.K)) * C_sw(f / self.fp))

    def h2_sw_c16(self, f):
        """Caprini et al. 2016, Eqs. (13)-(15)."""
        return 2.65e-6 / self.betaH * self.K ** 2 * (100 / self.gstar) ** (1 / 3) * self.vw * C_sw(f / self.fsw16)

    def h2_turb(self, f):
        """Caprini et al. 2016, Eqs. (16)-(18), kappa_turb = eps kappa_v."""
        x = f / self.fturb
        S = x ** 3 / ((1 + x) ** (11 / 3) * (1 + 8 * math.pi * f / hstar(self.T, self.gstar)))
        return 3.35e-4 / self.betaH * (EPS_TURB * self.K) ** 1.5 * (100 / self.gstar) ** (1 / 3) * self.vw * S

    def h2_total(self, f):
        return self.h2_sw(f) + self.h2_turb(f)


def Sh_lisa(f):
    """Strain sensitivity of the LISA Science Requirements Document, Eq. (3) [1/Hz]."""
    SI = 5.76e-48 * (1 + (0.4e-3 / f) ** 2)
    SII = 3.6e-41
    return 0.5 * 20 / 3 * (SI / (2 * math.pi * f) ** 4 + SII) * (1 + (f / 25e-3) ** 2)


def h2_sens(f):
    """h^2 Omega_sens = (2 pi^2/(3 H100^2)) f^3 S_h (Caprini et al. 2020, Eq. (34))."""
    return 2 * math.pi ** 2 / (3 * H100 ** 2) * f ** 3 * Sh_lisa(f)


FGRID = np.geomspace(1e-5, 1.0, 6001)


def snr(h2_of_f, fgrid=FGRID):
    """SNR = [T int df (h^2 Omega/h^2 Omega_sens)^2]^(1/2) (Caprini et al. 2020, Eq. (33)), trapezoid in ln f."""
    r = h2_of_f(fgrid) / h2_sens(fgrid)
    return math.sqrt(T_OBS * np.trapezoid(r ** 2 * fgrid, np.log(fgrid)))


def pls(fgrid=FGRID, snr_thr=10.0, betas=np.linspace(-8, 8, 321), fref=1e-3):
    """Power-law sensitivity (Thrane and Romano 2013, Eqs. (29), (30)) with the SNR of Caprini et al. 2020, Eq. (33)."""
    s = h2_sens(fgrid)
    out = np.zeros_like(fgrid)
    for b in betas:
        w = (fgrid / fref) ** b
        om = snr_thr / math.sqrt(T_OBS * np.trapezoid((w / s) ** 2 * fgrid, np.log(fgrid)))
        out = np.maximum(out, om * w)
    return out
