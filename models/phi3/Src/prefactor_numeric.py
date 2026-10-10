# %% [markdown]
# # Step (14): one-loop prefactor of the false-vacuum decay rate in d = 4
#
# Callan-Coleman (note, App. R):
#   Gamma/V = (S_B/2pi)^2 |det' M / det M_0|^{-1/2} e^{-S_B} [1 + O(g^2/m^2)],
#   M = -d^2 + V''(phi_B) = m^2 [-d_x^2 + 1 + f(x)],   M_0 = m^2 [-d_x^2 + 1],
# with x = m r and phi_B = (m^2/g) f the bounce of step (13).  The fluctuation operator does not depend on g, so
#   Gamma/V = m^4 (S_B/2pi)^2 D^{-1/2} e^{-S_B},   ln D = ln |det' M/det M_0|_ren (m = 1),
# and the whole one-loop correction is one number ln D (for given mu/m; R is the residue in the note).
# Partial waves l (degeneracy (l+1)^2).  Gel'fand-Yaglom: det M_l/det M_l^free = T_l(infinity), where
#   T'' + [2 I_{l+2}(x)/I_{l+1}(x) + (2l+3)/x] T' = f T,   T(0) = 1, T'(0) = 0   (T = psi_l/psi_l^free).
# l = 0: T_0(infinity) < 0 (the one negative mode).  l = 1: four zero modes (translations), removed analytically,
#   det' M_1/det M_1^free = C_4/(4 pi^2 f''(0) A)  per mode,   f -> -A K_1(x)/x,   f''(0) = (f0 + f0^2/2)/4,
# and checked by shifting M -> M + lambda (Dunne-Min 2005, Eq. (3.13), is the same formula).
# Renormalization (MS-bar, tadpoles cancelled by Y as everywhere in the note): the first-order term Tr[G0 V] is
# cancelled by Y; the second-order term -1/2 Tr[G0 V G0 V] (V = f) diverges logarithmically and is taken in MS-bar
# in momentum space,
#   A_2(mu) = -1/2 int d^4p/(2pi)^4 |V~(p)|^2 B0_E(p)/(16 pi^2),   B0_E = 2 - b ln((b+1)/(b-1)) + ln(mu^2/m^2),
#   b = sqrt(1 + 4m^2/p^2);
# the third and higher orders are finite and come from the partial waves with the exact first- and second-order
# Born terms h1, h2 subtracted:
#   ln D = sum_l (l+1)^2 [ln|T_l| - h1_l - h2_l + h1_l^2/2] + A_2(mu)     (ln|T_1| -> ln of the zero-mode formula).
# Checks: two-sided shooting reproduces f(0) and C_4 of step (13) and gives A, which a Green's-function integral
# reproduces; h1 against its closed form int x f I_{l+1} K_{l+1} dx; the large-l coefficients of h1 and
# h2 - h1^2/2; the zero mode by lambda-shift; one negative mode; Parseval; the local WKB formula of Dunne-Min
# (their Eq. (4.12), alpha = 0) converted to our scheme; mu-independence of the rate.
#
# Writes results/prefactor.csv and ../figs/prefactor_d4.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python prefactor_numeric.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.optimize import brentq
from scipy.special import ive, j1, kv, kve, zeta

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
STEP13 = dict(f0=-17.343868599974236, C4=817.7137733676353)      # results/bounce.csv
GSTEP12 = {"(A) tree unitarity": 9.81, "(B) perturbativity": 8.73, "(C) one-loop unitarity": 7.87}
MH, H0 = 125.25, 1.44e-42              # GeV; H_0 = 67.4 km/s/Mpc in GeV
K16 = 16 * math.pi ** 2
B0MM = 2 - math.pi / math.sqrt(3)       # B0(m^2; m, m) at mu = m (note, Sec. 3)
GOS1 = 0.5144                            # g_os = g [1 + GOS1 g^2/((4 pi)^2 m^2)] (note, App. P)
XM, XR = 2.0, 40.0                       # matching point and outer end of the bounce


def vprime(f):
    return f + f * f / 2


# %% [markdown]
# ## The bounce on [0, 40] by two-sided shooting
# Forward from x = 1e-5 (regular series, f(0) = f0) and backward from x = 40 with the linear tail f = -A K_1(x)/x;
# Newton on (f0, A) so that f and f' match at x = 2.  Unlike the one-sided shooting of step (13), this gives the
# profile to the far tail, and A, which the zero mode needs.  Check: A from the Green's function of the linear
# operator, A = (1/2) int x^2 I_1(x) f^2 dx.

# %%
def forward(f0, xend=XM, rtol=1e-13):
    x0 = 1e-5
    a = vprime(f0) / 8
    return solve_ivp(lambda x, y: [y[1], vprime(y[0]) - 3 / x * y[1]], (x0, xend), [f0 + a * x0 ** 2, 2 * a * x0],
                     method="DOP853", rtol=rtol, atol=1e-18, dense_output=True)


def backward(A, rtol=1e-13):
    y0 = [-A * kv(1, XR) / XR, A * kv(2, XR) / XR]
    return solve_ivp(lambda x, y: [y[1], vprime(y[0]) - 3 / x * y[1]], (XR, XM), y0,
                     method="DOP853", rtol=rtol, atol=1e-30, dense_output=True)


def mismatch(f0, A):
    return forward(f0).y[:, -1] - backward(A).y[:, -1]


f0, A = STEP13["f0"], None
fw = forward(f0, xend=10.0)
A = -fw.y[0, -1] * 10.0 / kv(1, 10.0)                  # rough start from f(10)
for it in range(8):
    r = mismatch(f0, A)
    J = np.empty((2, 2))
    for j, (df0, dA) in enumerate(((1e-9 * abs(f0), 0), (0, 1e-7 * A))):
        J[:, j] = (mismatch(f0 + df0, A + dA) - r) / (df0 + dA)
    step = np.linalg.solve(J, -r)
    f0, A = f0 + step[0], A + step[1]
    if abs(step[0]) < 1e-15 * abs(f0) and abs(step[1]) < 1e-13 * A:
        break
FW, BW = forward(f0), backward(A)


def fval(x):
    """Bounce profile f(x) (scalar)."""
    if x <= XM:
        return FW.sol(x)[0]
    if x <= XR:
        return BW.sol(x)[0]
    return -A * kv(1, x) / x


def fvec(x):
    x = np.asarray(x, float)
    out = np.empty_like(x)
    m1, m2 = x <= XM, (x > XM) & (x <= XR)
    out[m1] = FW.sol(x[m1])[0]
    out[m2] = BW.sol(x[m2])[0]
    m3 = x > XR
    out[m3] = -A * kv(1, x[m3]) / x[m3]
    return out


XG = np.linspace(0.0, XR, 400001)
XG[0] = 1e-12
FG = fvec(XG)
FPG = np.concatenate([FW.sol(XG[XG <= XM])[1], BW.sol(XG[XG > XM])[1]])
S_kin = 2 * math.pi ** 2 * simpson(XG ** 3 * FPG ** 2 / 2, x=XG)
S_pot = 2 * math.pi ** 2 * simpson(XG ** 3 * (FG ** 2 / 2 + FG ** 3 / 6), x=XG)
C4 = S_kin + S_pot
A_int = 0.5 * simpson(XG ** 2 * ive(1, XG) * np.exp(XG) * FG ** 2, x=XG)
fpp0 = vprime(f0) / 4
print(f"two-sided shooting: f(0) = {f0:.13f} (step 13: {STEP13['f0']:.13f}),  C_4 = {C4:.10f} "
      f"(step 13: {STEP13['C4']:.10f}, rel. {C4 / STEP13['C4'] - 1:.1e}),  Derrick T + 2U = {(S_kin + 2 * S_pot) / S_kin:.1e} T")
print(f"tail f -> -A K_1(x)/x:  A = {A:.12f} (Newton)  vs  (1/2) int x^2 I_1 f^2 = {A_int:.12f}  (rel. {A_int / A - 1:.1e})")
dict(f0=f0, A=A, C4=C4)          # inspect

# %% [markdown]
# ## Partial waves: T_l, h1_l, h2_l
# All l in one ODE system (the Bessel ratios I_{nu+1}/I_nu for every nu come from one backward recurrence).
# Start at x = 1e-4 with the regular series T = 1 + f0 x^2/(4(l+2)), h1 = f0 x^2/(4(l+2)), h2 = f0^2 x^4/(32(l+2)(l+3)).
# The potential has fallen below 1e-12 at x = 34, where the integration stops.

# %%
def rho_all(numax, z):
    """rho[nu] = I_{nu+1}(z)/I_nu(z) for nu = 0..numax, by the stable backward recurrence."""
    n = numax + 40 + int(2 * z)
    r = z / ((n + 1) + math.sqrt((n + 1) ** 2 + z * z))
    out = np.empty(numax + 1)
    for k in range(n - 1, -1, -1):
        r = z / (2 * (k + 1) + z * r)
        if k <= numax:
            out[k] = r
    return out


def radial(ls, kappa=1.0, born=True, xmax=34.0, rtol=1e-12, dense=False):
    """Integrate T (and h1, h2) for the partial waves ls; free reference mass kappa (kappa^2 = 1 + lambda)."""
    ls = np.asarray(ls)
    nl, x0 = len(ls), 1e-4
    a = f0 / (4 * (ls + 2))
    b = f0 * f0 / (32 * (ls + 2) * (ls + 3))
    rows = [1 + a * x0 ** 2, 2 * a * x0]
    if born:
        rows += [a * x0 ** 2, 2 * a * x0, b * x0 ** 4, 4 * b * x0 ** 3]
    y0 = np.concatenate(rows)
    numax = int(ls.max()) + 1

    def rhs(x, y):
        f = fval(x)
        c = 2 * kappa * rho_all(numax, kappa * x)[ls + 1] + (2 * ls + 3) / x
        Y = y.reshape(-1, nl)
        out = [Y[1], f * Y[0] - c * Y[1]]
        if born:
            out += [Y[3], f - c * Y[3], Y[5], f * Y[2] - c * Y[5]]
        return np.concatenate(out)
    sol = solve_ivp(rhs, (x0, xmax), y0, method="DOP853", rtol=rtol, atol=1e-16, dense_output=dense)
    return sol


# check the Bessel ratio against scipy where scipy does not underflow
rchk = max(abs(rho_all(30, z)[nu] / (ive(nu + 1, z) / ive(nu, z)) - 1) for z in (0.01, 0.5, 3.0, 17.0, 33.0) for nu in (0, 1, 5, 20, 30))
print(f"Bessel ratio I_(nu+1)/I_nu by recurrence vs scipy: max rel. difference {rchk:.1e}")
LMAX = 200
LS = np.arange(LMAX + 1)
sol = radial(LS)
Y = sol.y[:, -1].reshape(6, -1)
Tinf, h1, h2 = Y[0], Y[2], Y[4]
print(f"partial waves l = 0..{LMAX}: {sol.t.size} steps;  T_0(inf) = {Tinf[0]:.10f} (< 0: negative mode),  "
      f"T_1(inf) = {Tinf[1]:.1e} (zero modes),  T_2(inf) = {Tinf[2]:.10f}")
{l: float(Tinf[l]) for l in (0, 1, 2, 3, 10, 50)}       # inspect

# %% [markdown]
# ## Checks of the Born terms
# h1_l(infinity) = int_0^infinity x f(x) I_{l+1}(x) K_{l+1}(x) dx (first-order perturbation theory with the radial
# Green's function).  Large l: h1 (l+1) -> (1/2) int x f dx and (h2 - h1^2/2)(l+1)^3 -> -(1/8) int x^3 f^2 dx
# (Dunne-Min, Eqs. (3.16), (4.14)); int x^3 f^2 dx = C_4/pi^2 (from dS_B/dm^2 = C_4/g^2).

# %%
I1 = simpson(XG * FG, x=XG)
I3 = simpson(XG ** 3 * FG, x=XG)
I3f2 = simpson(XG ** 3 * FG ** 2, x=XG)
with np.errstate(invalid="ignore", over="ignore"):
    IK = [np.nan_to_num(ive(l + 1, XG) * kve(l + 1, XG), nan=1 / (2 * (l + 1))) for l in range(31)]   # x -> 0: 1/(2 nu)
h1q = np.array([simpson(XG * FG * IK[l], x=XG) for l in range(31)])
print(f"h1 (ODE) vs int x f I K dx, l = 0..30: max abs. difference {np.max(np.abs(h1q - h1[:31])):.1e}")
print(f"h1 (l+1) at l = 200: {h1[200] * 201:.6f}   vs (1/2) int x f = {I1 / 2:.6f}")
q2 = (h2 - h1 ** 2 / 2) * (LS + 1.0) ** 3
print(f"(h2 - h1^2/2)(l+1)^3 at l = 200: {q2[200]:.5f}   vs -(1/8) int x^3 f^2 = {-I3f2 / 8:.5f};  "
      f"int x^3 f^2 = {I3f2:.10f} vs C_4/pi^2 = {C4 / math.pi ** 2:.10f}")

# %% [markdown]
# ## Zero modes (l = 1) and the negative mode (l = 0)
# Zero modes: det' M_1/det M_1^free = lim_{lambda->0} T_1(infinity; lambda)/lambda, with M -> M + lambda (free mass
# kappa = sqrt(1 + lambda)); the analytic value is C_4/(4 pi^2 f''(0) A) (App. R).
# Negative mode: the eigenvalue e_- of M/m^2 is -lambda* where T_0(infinity; lambda*) = 0.

# %%
c_zero = C4 / (4 * math.pi ** 2 * fpp0 * A)
lam = 1e-3
tp = radial([1], kappa=math.sqrt(1 + lam), born=False).y[0, -1]
tm = radial([1], kappa=math.sqrt(1 - lam), born=False).y[0, -1]
lam2 = 5e-4
tp2 = radial([1], kappa=math.sqrt(1 + lam2), born=False).y[0, -1]
tm2 = radial([1], kappa=math.sqrt(1 - lam2), born=False).y[0, -1]
c_lam = (4 * (tp2 - tm2) / (2 * lam2) - (tp - tm) / (2 * lam)) / 3          # Richardson on the central difference
print(f"zero modes: det' M_1/det M_1^free = {c_zero:.10e} (analytic) vs {c_lam:.10e} (lambda-shift), rel. {c_lam / c_zero - 1:.1e}")
T0lam = lambda la: radial([0], kappa=math.sqrt(1 + la), born=False).y[0, -1]
lam_neg = brentq(T0lam, 1e-3, 16.5, xtol=1e-14, rtol=1e-13)
signs = [int(np.sign(T0lam(la))) for la in (0.0, 0.5 * lam_neg, 1.5 * lam_neg, 5.0, 10.0, 16.0)]
print(f"negative mode: e_- = {-lam_neg:.10f} m^2 (one sign change of T_0(inf; lambda) on [0, 16]: {signs})")
sdn = radial([0, 1, 2, 3, 4, 5], born=False, dense=True)
Tn = sdn.sol(np.linspace(1e-4, 34.0, 20001))
nodes = [int(np.sum(np.diff(np.sign(Tn[i])) != 0)) for i in range(6)]
print(f"Sturm: zeros of T_l(x) on (0, 34] for l = 0..5: {nodes} (= negative modes per wave);  "
      f"min T_1 = {Tn[1].min():.1e}, min T_2 = {Tn[2].min():.3f}")

# %% [markdown]
# ## The finite part of the partial-wave sum
# r_l = ln|T_l| - h1 - h2 + h1^2/2 (third and higher orders); for l = 1, ln|T_1| -> ln(det' M_1/det M_1^free).
# (l+1)^2 r_l falls like (l+1)^-3; the tail beyond l = 200 is summed from a fit (l+1)^2 r_l = sum_k c_k (l+1)^-k,
# k = 3..6, with Hurwitz zeta functions.

# %%
lnT = np.log(np.abs(Tinf))
lnT[1] = math.log(c_zero)
rl = lnT - h1 - h2 + h1 ** 2 / 2
wl = (LS + 1.0) ** 2 * rl


def tail_sum(w, lfit=(60, LMAX), ks=(3, 4, 5, 6)):
    l = np.arange(lfit[0], lfit[1] + 1)
    M = np.array([(l + 1.0) ** (-k) for k in ks]).T
    c = np.linalg.lstsq(M, w[l], rcond=None)[0]
    return float(np.sum(w[: lfit[1] + 1])) + sum(ck * zeta(k, lfit[1] + 2) for ck, k in zip(c, ks)), c


Sigma, cfit = tail_sum(wl)
Sigma_b, _ = tail_sum(wl, lfit=(100, LMAX), ks=(3, 4, 5))
Sigma_c, _ = tail_sum(wl[:151], lfit=(50, 150))
print(f"sum_l (l+1)^2 r_l = {Sigma:.9f}   (fit l = 100..200, 3 terms: {Sigma_b:.9f};  L = 150: {Sigma_c:.9f});  "
      f"partial sum to l = 200: {np.sum(wl):.9f};  leading tail coefficient c_3 = {cfit[0]:.4f}")
Ylo = radial(LS, rtol=1e-10).y[:, -1].reshape(6, -1)
lnTlo = np.log(np.abs(Ylo[0]))
lnTlo[1] = math.log(c_zero)
Sigma_lo, _ = tail_sum((LS + 1.0) ** 2 * (lnTlo - Ylo[2] - Ylo[4] + Ylo[2] ** 2 / 2))
print(f"  rtol 1e-12 -> 1e-10 changes the sum by {Sigma_lo - Sigma:.1e}")
print(f"  of which l = 0: {wl[0]:.9f} (ln|T_0| = {lnT[0]:.9f}),  l = 1: {wl[1]:.9f} (4 ln of the zero-mode factor = {4 * lnT[1]:.9f})")

# %% [markdown]
# ## The second-order term in MS-bar (momentum space)
# V~(p) = (4 pi^2/p) int_0^infinity x^2 J_1(p x) f(x) dx; int d^4p/(2pi)^4 = (1/(8 pi^2)) int p^3 dp.
# Parseval: int d^4p/(2pi)^4 |V~|^2 = int d^4x f^2 = 2 pi^2 int x^3 f^2 = 2 C_4.

# %%
pn, pw = np.polynomial.legendre.leggauss(400)
PMAX = 40.0
P = (pn + 1) * PMAX / 2
PW = pw * PMAX / 2
Xh = XG[XG <= 34.0]
Fh = FG[: Xh.size]
Vt = np.array([4 * math.pi ** 2 / p * simpson(Xh ** 2 * j1(p * Xh) * Fh, x=Xh) for p in P])
beta = np.sqrt(1 + 4 / P ** 2)
B0E = 2 - 2 * beta * np.arctanh(1 / beta)
pars = np.sum(PW * P ** 3 * Vt ** 2) / (8 * math.pi ** 2)
A2m = -0.5 * np.sum(PW * P ** 3 * Vt ** 2 * B0E) / (8 * math.pi ** 2) / K16
dA2 = -0.5 * pars / K16                                 # coefficient of ln(mu^2/m^2) in A_2
print(f"Parseval: int d^4p/(2pi)^4 |V~|^2 = {pars:.8f} vs 2 C_4 = {2 * C4:.8f} (rel. {pars / (2 * C4) - 1:.1e});  "
      f"|V~(p = {PMAX:.0f})| = {abs(Vt[-1]):.1e}")
print(f"A_2(mu = m) = {A2m:.9f};  A_2(mu) = A_2(m) + ({dA2:.6f}) ln(mu^2/m^2)  [expected -C_4/(16 pi^2) = {-C4 / K16:.6f}]")
lnD = Sigma + A2m
print(f"ln D (mu = m) = {Sigma:.9f} + ({A2m:.9f}) = {lnD:.9f};   D^(-1/2) = {math.exp(-lnD / 2):.6e}")

# %% [markdown]
# ## Check: the local WKB formula of Dunne and Min (PRD 72, 125004 (2005), Eq. (4.12))
# Their potential (1/2) Phi^2 - (1/2) Phi^3 + (alpha/8) Phi^4 at alpha = 0 is ours with Phi = -f/3, so V(r) = f.
# Their Gamma_MS includes the collective-coordinate factor -2 ln(S/2pi) with the dimensionless action S = C_4/9,
# and keeps the MS-bar first-order term A_1 = Tr[G0 V]_MS-bar = -(1/8) int x^3 f dx (no tadpole counterterm in their
# model).  So 2 Gamma_MS + 4 ln(S/2pi) - A_1 must equal our ln D(mu = m).  Their l-sum subtracts the local large-l
# asymptotics instead of the Born terms, and their finite part is local in V instead of A_2.

# %%
Phi_inf, Phi0 = A / 3, -f0 / 3
Up0 = Phi0 - 1.5 * Phi0 ** 2
Ivv = simpson(XG ** 3 * FG * (FG + 2), x=XG)
Iloc = simpson(XG[1:] ** 3 * FG[1:] * (FG[1:] + 2) * (0.5 - np.euler_gamma - np.log(XG[1:] / 2)), x=XG[1:])
wdm = (LS + 1.0) ** 2 * (lnT - (I1 / 2) / (LS + 1.0) + (Ivv / 8) / (LS + 1.0) ** 3)
wdm[:2] = 0.0
Sdm, _ = tail_sum(wdm)
Gamma_dm = 0.5 * lnT[0] - 2 * math.log(abs(math.pi / 2 * Phi_inf * Up0)) + 0.5 * Sdm - 0.75 * I1 + Iloc / 16
Sbar = C4 / 9
A1 = -I3 / 8
lnD_dm = 2 * Gamma_dm + 4 * math.log(Sbar / (2 * math.pi)) - A1
print(f"Dunne-Min Gamma_MS (alpha = 0) = {Gamma_dm:.9f};  2 Gamma + 4 ln(S/2pi) - A_1 = {lnD_dm:.9f}  vs  ln D = {lnD:.9f}  "
      f"(difference {lnD_dm - lnD:.1e})")
print(f"  their zero-mode factor (pi/2) Phi_inf U'(Phi0) vs ours: (S/2pi)/c = {Sbar / (2 * math.pi * c_zero):.10f}, "
      f"|(pi/2) Phi_inf U'(Phi0)| = {abs(math.pi / 2 * Phi_inf * Up0):.10f}")

# %% [markdown]
# ## The rate
# Gamma/V = m^4 (S_B/2pi)^2 exp(-S_B - ln D/2), S_B = C_4 m^2/g^2, MS-bar m and g at mu = m.  mu-independence:
# d(-S_B)/d ln mu = -C_4/(16 pi^2) from mu dm^2/dmu = g^2/(4 pi)^2 (note, Eq. (15)), and d(-ln D/2)/d ln mu =
# -dA2 (the ln(mu^2) coefficient above) -> they cancel.  On-shell inputs: m^2 = m_p^2 + g^2 B0(m^2)/(2(4pi)^2) and
# g^2 = g_os^2 [1 - 2 x 0.5144 g_os^2/((4 pi)^2 m^2)] give S_B = C_4 m_p^2/g_os^2 + C_4 (B0/2 + 2 x 0.5144)/(4 pi)^2.

# %%
rg = -C4 / K16 - dA2                                      # d/d ln mu of (-S_B - ln D/2): ln D/2 has dA2 ln(mu^2)/2 = dA2 ln mu
print(f"mu-independence: d(-S_B)/d ln mu + d(-ln D/2)/d ln mu = {-C4 / K16:.6f} + {-dA2:.6f} = {rg:.1e}")
dS_mp = C4 * B0MM / 2 / K16
dS_gos = C4 * 2 * GOS1 / K16
print(f"on-shell inputs: S_B = C_4 m^2/g^2 = C_4 m_p^2/g^2 + {dS_mp:.4f} = C_4 m_p^2/g_os^2 + {dS_mp + dS_gos:.4f}")
sb_cosmo = 4 * math.log(MH / H0)
expo = lambda S: S - 2 * math.log(S / (2 * math.pi)) + lnD / 2          # -ln(Gamma/(V m^4))
rows = []
for name, g in GSTEP12.items():
    S = C4 / g ** 2
    rows.append((name, g, S, math.exp(-S), math.exp(-expo(S))))
    print(f"  {name:24} g/m = {g:5.2f}: S_B = {S:7.3f}, e^-S_B = {math.exp(-S):.3e}, "
          f"Gamma/(V m^4) = {math.exp(-expo(S)):.3e}  (prefactor {math.exp(S - expo(S)):.3f})")
S_cos = brentq(lambda S: expo(S) - sb_cosmo, 50, 1000)
print(f"cosmological condition Gamma H_0^-4 < 1 (m = m_h): tree S_B > {sb_cosmo:.2f} (g/m < {math.sqrt(C4 / sb_cosmo):.4f});  "
      f"one loop S_B > {S_cos:.2f} (g/m < {math.sqrt(C4 / S_cos):.4f});  "
      f"prefactor at the bound = exp({S_cos - expo(S_cos):.3f});  with on-shell inputs g_os/m_p < "
      f"{math.sqrt(C4 / (S_cos - dS_mp - dS_gos)):.4f}")

# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "prefactor.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value"])
    for k, v in (("f0", f0), ("A", A), ("A_green", A_int), ("C4", C4), ("T0_inf", Tinf[0]), ("e_minus", -lam_neg),
                 ("zero_mode_analytic", c_zero), ("zero_mode_lambda", c_lam), ("sum_l", Sigma), ("A2_mu_m", A2m),
                 ("dA2_dln_mu2", dA2), ("lnD_mu_m", lnD), ("lnD_dunne_min", lnD_dm), ("int_x_f", I1), ("int_x3_f", I3),
                 ("int_x3_f2", I3f2), ("S_cosmo_one_loop", S_cos), ("g_over_m_cosmo_one_loop", math.sqrt(C4 / S_cos)),
                 ("dS_onshell", dS_mp + dS_gos)):
        w.writerow([k, v])
    w.writerow([])
    w.writerow(["l", "T_inf", "h1", "h2", "r_l"])
    for l in range(LMAX + 1):
        w.writerow([l, Tinf[l], h1[l], h2[l], rl[l]])
    w.writerow([])
    w.writerow(["criterion_step12", "g_over_m", "S_B", "exp_minus_S_B", "Gamma_over_V_m4"])
    for row in rows:
        w.writerow(row)

# %% [markdown]
# ## Figure: T_l(x) for the lowest waves, and the convergence of the partial-wave sum

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1), gridspec_kw={"height_ratios": [1, 1.2]})
sd = radial([0, 1, 2, 3], born=False, xmax=12.0, dense=True)
xx = np.linspace(1e-4, 12.0, 600)
yy = sd.sol(xx)
for i, (l, color, ls_) in enumerate(((0, "#eb6235", "-"), (1, "k", "--"), (2, "#5d81b4", "-."), (3, "#8cc2a3", ":"))):
    ax1.plot(xx, yy[i], color=color, lw=0.9, ls=ls_, label=f"$l={l}$")
ax1.axhline(0, color="0.6", lw=0.5)
ax1.set_xlim(0, 12)
ax1.set_xlabel(r"$x=mr$")
ax1.set_ylabel(r"$T_l(x)$")
ax1.legend(loc="upper right", ncol=2)
lp = LS[2:] + 1.0
ax2.plot(lp, (LS[2:] + 1.0) ** 2 * np.abs(lnT[2:]), color="0.5", lw=0.9, ls="--", label=r"$(l+1)^2|\ln T_l|$")
ax2.plot(lp, np.abs(wl[2:]), color="k", lw=0.9, label=r"$(l+1)^2|r_l|$")
ax2.plot(lp[30:], np.abs(cfit[0]) / lp[30:] ** 3, color="#eb6235", lw=0.6, ls=":", label=r"$\propto(l+1)^{-3}$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel(r"$l+1$")
ax2.set_ylabel("contribution of wave $l$")
ax2.legend(loc="center right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "prefactor_d4.pdf"))
print("wrote results/prefactor.csv and figs/prefactor_d4.pdf")
