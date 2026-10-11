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

with open(os.path.join(HERE, "..", "..", "phi34", "Src", "results", "bounce.csv")) as _fh:
    _rows = [r for r in csv.reader(_fh) if r and r[0] == "3"]
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


# ---- the single-field thermal potential (step (4); note, App. E) ----
# Units: chi = f + 3/alpha (f = g phi/m^2; chi = 0 is the inflection point phi = -g/lambda of the tree potential),
# tau = g T/m^2, potentials in m^6/g^2, gm = g/m.  MS-bar at mu = m with the tadpole-cancelling linear term of the
# zero-temperature note (t = m^2 g/(4 pi)^2/2 at one loop).
LN_AB = 2 * math.log(4 * math.pi) + 1.5 - 2 * np.euler_gamma        # J_B high-T expansion: -(y^2/32) ln(y/a_b)
ZETA3 = 1.2020569031595942


def jb_quad(y):
    """J_B(y) = int_0^inf dx x^2 ln(1 - exp(-sqrt(x^2 + y))); real part for -(2 pi)^2 < y < 0."""
    from scipy.integrate import quad
    if y >= 0:
        return quad(lambda x: x * x * math.log1p(-math.exp(-math.sqrt(x * x + y))), 0, 60 + math.sqrt(y),
                    epsabs=1e-14, epsrel=1e-11, limit=400)[0]
    assert y > -(2 * math.pi) ** 2
    r = math.sqrt(-y)
    # x < r: E = i s, s = (r^2 - x^2)^(1/2), Re ln(1 - e^(-i s)) = ln(2 sin(s/2)); x > r: u = (x^2 - r^2)^(1/2)
    a = quad(lambda t: t * math.sqrt(r * r - t * t) * math.log(2 * math.sin(t / 2)), 0, r,
             epsabs=1e-14, epsrel=1e-11, limit=400)[0]
    b = quad(lambda u: u * math.sqrt(u * u + r * r) * math.log1p(-math.exp(-u)), 0, 60, epsabs=1e-14, epsrel=1e-11, limit=400)[0]
    return a + b


def jb_nonanalytic(y):
    """The non-analytic part -(pi/6) Re y^(3/2) - (y^2/32) ln|y| of J_B (vectorised)."""
    y = np.asarray(y, dtype=float)
    ay = np.where(y == 0, 1.0, np.abs(y))
    return -math.pi / 6 * np.where(y > 0, y, 0.0) ** 1.5 - y * y / 32 * np.log(ay)


_JB = {}


def jb(y):
    """Re J_B(y) from a cubic spline of the analytic part J_B - (non-analytic part) on -30 <= y <= 120 (0 beyond)."""
    if "spl" not in _JB:
        from scipy.interpolate import CubicSpline
        ys = np.concatenate([np.linspace(-30, -2, 141)[:-1], np.linspace(-2, 2, 401)[:-1], np.linspace(2, 120, 591)])
        S = np.array([jb_quad(t) for t in ys]) - jb_nonanalytic(ys)
        _JB["spl"] = CubicSpline(ys, S)
    y = np.asarray(y, dtype=float)
    assert np.all(y >= -30)
    return np.where(y <= 120, _JB["spl"](np.minimum(y, 120)) + jb_nonanalytic(np.minimum(y, 120)), 0.0)


def jb_prime(y):
    """d Re J_B/dy from the spline of the analytic part and the derivative of the non-analytic part."""
    jb(0.0)
    y = np.asarray(y, dtype=float)
    yc = np.minimum(y, 120)
    ay = np.where(yc == 0, 1.0, np.abs(yc))
    dna = -math.pi / 4 * np.sqrt(np.where(yc > 0, yc, 0.0)) - yc / 16 * np.log(ay) - yc / 32
    return np.where(y <= 120, _JB["spl"](yc, 1) + dna, 0.0)


def jb_hight(y):
    """High-temperature expansion through y^3 (note, App. E): -pi^4/45 + pi^2 y/12 - pi y^(3/2)/6 - (y^2/32) ln(y/a_b)
    + zeta(3) y^3/(384 pi^2)."""
    return (-math.pi ** 4 / 45 + math.pi ** 2 * y / 12 - math.pi / 6 * y ** 1.5 - y * y / 32 * math.log(y / math.exp(LN_AB))
            + ZETA3 * y ** 3 / (384 * math.pi ** 2))


class SingleField:
    """phi^3 + phi^4 with its own thermal loops; V(chi) = h chi + (even in chi) at one loop (note, Sec. 3)."""

    def __init__(self, alpha, gm, tadpole=True):
        self.alpha, self.gm = alpha, gm
        self.h = 3 * (1 - alpha) / alpha ** 2 + (gm ** 2 / (32 * math.pi ** 2) if tadpole else 0.0)
        self.A0 = 1 - 1.5 / alpha                               # M^2/m^2 at chi = 0
        self.fminus = -9 / (2 * alpha) * (1 + math.sqrt(max(0.0, 1 - 8 * alpha / 9)))

    def M2(self, x):
        return self.A0 + self.alpha * x * x / 6

    def Pi(self, tau):
        return self.alpha * tau * tau / 72                      # lambda T^2/24 in m^2

    def v_tree(self, x):
        return self.h * x + 0.5 * self.A0 * x * x + self.alpha * x ** 4 / 72

    def v_lo(self, x, tau):
        return self.v_tree(x) + tau * tau / 24 * self.M2(x)

    def LT(self, tau):
        return np.log((tau / self.gm) ** 2) + 2 * math.log(4 * math.pi) - 2 * np.euler_gamma

    def v_ht(self, x, tau):
        """High-T expansion with the daisy-resummed zero mode (Arnold-Espinosa)."""
        M2 = self.M2(x)
        return (self.v_lo(x, tau) - tau * self.gm / (12 * math.pi) * np.maximum(M2 + self.Pi(tau), 0.0) ** 1.5
                + self.gm ** 2 / (64 * math.pi ** 2) * M2 * M2 * self.LT(tau))

    def dv_ht(self, x, tau):
        """d v_ht/d chi."""
        M2 = self.M2(x)
        dM2 = self.alpha * x / 3
        return (self.h + self.A0 * x + self.alpha * x ** 3 / 18 + tau * tau / 24 * dM2
                - tau * self.gm / (12 * math.pi) * 1.5 * np.sqrt(np.maximum(M2 + self.Pi(tau), 0.0)) * dM2
                + self.gm ** 2 / (64 * math.pi ** 2) * 2 * M2 * dM2 * self.LT(tau))

    def v_full(self, x, tau):
        """Full one loop: tree + CW (mu = m) + (T^4/2 pi^2) Re J_B(M^2/T^2) + daisy correction of the zero mode."""
        M2 = self.M2(x)
        aM2 = np.where(M2 == 0, 1.0, np.abs(M2))
        cw = self.gm ** 2 / (64 * math.pi ** 2) * M2 * M2 * (np.log(aM2) - 1.5)
        th = tau ** 4 / (2 * math.pi ** 2 * self.gm ** 2) * jb(self.gm ** 2 * M2 / tau ** 2)
        dz = -tau * self.gm / (12 * math.pi) * (np.maximum(M2 + self.Pi(tau), 0.0) ** 1.5 - np.maximum(M2, 0.0) ** 1.5)
        return self.v_tree(x) + cw + th + dz

    def dv_full(self, x, tau):
        """d v_full/d chi."""
        M2 = self.M2(x)
        dM2 = self.alpha * x / 3
        aM2 = np.where(M2 == 0, 1.0, np.abs(M2))
        dcw = self.gm ** 2 / (64 * math.pi ** 2) * 2 * M2 * dM2 * (np.log(aM2) - 1.0)
        dth = tau * tau / (2 * math.pi ** 2) * jb_prime(self.gm ** 2 * M2 / tau ** 2) * dM2
        ddz = -tau * self.gm / (12 * math.pi) * 1.5 * (np.sqrt(np.maximum(M2 + self.Pi(tau), 0.0))
                                                       - np.sqrt(np.maximum(M2, 0.0))) * dM2
        return self.h + self.A0 * x + self.alpha * x ** 3 / 18 + dcw + dth + ddz

    def minima(self, tau, which="ht", n=4001):
        """Local minima (chi, v) sorted by v, from a grid and a bounded refinement."""
        from scipy.optimize import minimize_scalar
        fun = {"lo": self.v_lo, "ht": self.v_ht, "full": self.v_full}[which]
        xs = np.linspace(self.fminus + 3 / self.alpha - 3, 3 / self.alpha + 3, n)
        v = fun(xs, tau)
        out = []
        for i in range(1, n - 1):
            if v[i] < v[i - 1] and v[i] <= v[i + 1]:
                r = minimize_scalar(lambda x: float(fun(x, tau)), bounds=(xs[i - 1], xs[i + 1]), method="bounded",
                                    options={"xatol": 1e-12})
                out.append((float(r.x), float(r.fun)))
        return sorted(out, key=lambda p: p[1])

    def false_true(self, tau, which="ht"):
        """(chi_false, chi_true) at tau, or None if there is only one minimum."""
        mins = self.minima(tau, which)
        return (mins[1][0], mins[0][0]) if len(mins) >= 2 else None

    def s3T(self, tau, which="ht"):
        """S_3/T of the thermal decay of the metastable minimum (S_3 = (m^3/g^2) S_hat, T = m^2 tau/g)."""
        ft = self.false_true(tau, which)
        V = (lambda x: self.v_ht(x, tau)) if which == "ht" else (lambda x: self.v_full(x, tau))
        dV = (lambda x: float(self.dv_ht(x, tau))) if which == "ht" else (lambda x: float(self.dv_full(x, tau)))
        b = bounce(lambda x: V(x) if np.ndim(x) else float(V(x)), dV, ft[0], ft[1], d=3)
        return b["S"] / (self.gm * tau), b

    def ln_gamma_over_H4(self, tau, which="ht", m=125.25, gstar=106.75):
        """ln(Gamma/H^4), Gamma = T^4 (S_3/2 pi T)^(3/2) e^(-S_3/T), H = 1.66 g*^(1/2) T^2/M_Pl, T = tau m/(g/m) [GeV]."""
        sT = self.s3T(tau, which)[0]
        T = tau * m / self.gm
        return 4 * math.log(T) + 1.5 * math.log(sT / (2 * math.pi)) - sT - 4 * math.log(1.66 * math.sqrt(gstar) * T ** 2 / MPL)

    def tau_decay(self, which="ht", lo=None, frac=0.97, xtol=1e-7):
        """Temperature (tau) above which the metastable minimum decays within a Hubble time (Gamma = H^4)."""
        from scipy.optimize import brentq
        tsp = self.tau_spinodal(which)
        if lo is None:
            lo = max(0.5, self.gm * math.sqrt(max(0.0, -self.A0) / 25)) if which == "full" else 0.3
        f = lambda t: self.ln_gamma_over_H4(t, which)
        assert f(lo) < 0 < f(frac * tsp)
        return brentq(f, lo, frac * tsp, xtol=xtol), tsp

    def tau_spinodal(self, which="ht", lo=None, hi=20.0):
        """Highest tau at which a second local minimum (on the disfavoured side) exists (bisection)."""
        two = lambda t: len(self.minima(t, which, n=2001)) >= 2
        if lo is None:                                  # full one loop: Re J_B needs y = g^2 M^2/(m^2 tau^2) > -30
            lo = max(1.0, self.gm * math.sqrt(max(0.0, -self.A0) / 25)) if which == "full" else 0.2
        if not two(lo):
            return float("nan")
        assert not two(hi)
        while hi - lo > 1e-7:
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if two(mid) else (lo, mid)
        return 0.5 * (lo + hi)

    def tau_spinodal_lo_closed(self):
        """Leading order (tree + T^2 term): |h| = (2|a|/3) (6|a|/alpha)^(1/2) with a = A0 + alpha tau^2/72 (note, App. E)."""
        asp = (1.5 * abs(self.h) * math.sqrt(self.alpha / 6)) ** (2 / 3)
        t2 = 72 / self.alpha * (-self.A0 - asp)
        return math.sqrt(max(t2, 0.0)) if t2 > -1e-12 else float("nan")


# ---- generic O(d)-symmetric bounce by overshoot/undershoot (step (5); note, App. F) ----
def bounce(V, dV, phi_f, phi_t, d=3, eps_lin=1e-3, rtol=1e-12):
    """O(d) bounce of the scalar potential V (callables V, dV) from the false minimum phi_f towards the true one phi_t.
    phi(0) = phi_t + (phi_z - phi_t) e^(-u) (phi_z: V(phi_z) = V(phi_f) on the true side); bisection in u between
    undershoot and overshoot.  Near phi_t the start uses the linearised solution
    phi - phi_t = delta Gamma(d/2) (2/(mu r))^(d/2 - 1) I_(d/2-1)(mu r), mu^2 = V''(phi_t).
    Returns S = Omega_(d-1) int r^(d-1) [phi'^2/2 + V - V(phi_f)], the kinetic part T, phi(0) and the wall radius."""
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq, minimize_scalar
    from scipy.special import iv, gamma
    s = 1.0 if phi_f > phi_t else -1.0                          # direction from the true towards the false minimum
    Vf = V(phi_f)
    rb = minimize_scalar(lambda p: -V(p), bounds=sorted((phi_f, phi_t)), method="bounded", options={"xatol": 1e-14})
    phi_b = rb.x
    phi_z = brentq(lambda p: V(p) - Vf, phi_t + 1e-14 * (phi_b - phi_t), phi_b - 1e-12 * (phi_b - phi_t), xtol=1e-15)
    Delta = phi_z - phi_t
    hh = 1e-5 * abs(Delta)
    mu2 = (dV(phi_t + hh) - dV(phi_t - hh)) / (2 * hh)
    mu = math.sqrt(mu2)
    nu = d / 2 - 1
    lin = lambda x: gamma(d / 2) * (2 / x) ** nu * iv(nu, x) if x > 1e-8 else 1.0 + x * x / (2 * d)
    dlin = lambda x: gamma(d / 2) * (2 / x) ** nu * iv(nu + 1, x) if x > 1e-8 else x / d     # d/dx of lin

    def rhs(r, y):
        return [y[1], dV(y[0]) - (d - 1) / r * y[1]]

    def over(r, y):
        return s * (y[0] - phi_f)
    over.terminal, over.direction = True, 1

    def under(r, y):
        return s * y[1]
    under.terminal, under.direction = True, -1

    def shoot(u, dense=False):
        delta = Delta * math.exp(-u)
        if abs(delta) < eps_lin * abs(Delta):
            x0 = brentq(lambda x: lin(x) - eps_lin * abs(Delta) / abs(delta), 1e-12, 800.0)
            r0, y0 = x0 / mu, [phi_t + delta * lin(x0), delta * mu * dlin(x0)]
        else:
            p0 = phi_t + delta
            r0 = 1e-6 / mu
            y0 = [p0 + dV(p0) * r0 * r0 / (2 * d), dV(p0) * r0 / d]
        sol = solve_ivp(rhs, (r0, r0 + 400.0 / mu), y0, method="DOP853", rtol=rtol, atol=1e-14 * abs(Delta),
                        events=(over, under), dense_output=dense)
        kind = "over" if sol.t_events[0].size else "under"
        return kind, sol, r0

    lo, hi = 0.0, 1.0
    while shoot(hi)[0] == "under":
        lo, hi = hi, hi + 2.0
        if hi > 60:
            raise RuntimeError("no overshoot")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if shoot(mid)[0] == "under":
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-14 * max(1.0, hi):
            break
    kind, sol, r0 = shoot(lo, dense=True)
    r = np.linspace(r0, sol.t[-1], 40001)
    y = sol.sol(r)
    om = 2 * math.pi ** (d / 2) / gamma(d / 2)
    T = om * np.trapezoid(r ** (d - 1) * 0.5 * y[1] ** 2, r)
    try:
        Vr = np.asarray(V(y[0]), dtype=float)
        assert Vr.shape == y[0].shape
    except Exception:
        Vr = np.array([V(p) for p in y[0]])
    U = om * np.trapezoid(r ** (d - 1) * (Vr - Vf), r)
    if r0 > 1e-6 / mu:                                         # the core r < r0 sits at phi ~ phi_t (linear solution)
        U += om * r0 ** d / d * (V(phi_t) - Vf)
    Rw = r[np.argmin(np.abs(y[0] - 0.5 * (phi_t + phi_f)))]
    return dict(S=T + U, T=T, U=U, S_derrick=2 * T / d, phi0=y[0][0], R=Rw, u=lo, r_end=sol.t[-1],
                phi_end=y[0][-1], phi_b=phi_b, phi_z=phi_z)
