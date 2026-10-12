# %% [markdown]
# # Step (8): perturbative unitarity of the coupled phi phi and psi psibar partial waves (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (8), Eq. (pw), App. pw.  m = 1, M = 0.7 (pole masses); couplings y, lambda (MS-bar).
# Helicity partial waves (Jacob-Wick), with the two-body states |z; l1 l2> along the z axis and their rotations:
#     a^J_fi(s) = sqrt(beta_i beta_f) S_i S_f/(32 pi) int_{-1}^{1} dc d^J_{l_i l_f}(theta) M_fi(s, theta),
#     beta = 2|p|/sqrt(s),  S = 1/sqrt(2) for phi phi,  l = l1 - l2,
# so that S_J = 1 + 2 i a^J is unitary in the space of the open two-body states: Abs a^J = a^J a^J+, the eigenvalues of the
# hermitian a^J lie on the circle |a - i/2| = 1/2 and |Re a| <= 1/2 (diagonal elements |Re a_ii| <= 1/2, off-diagonal
# |a_fi| <= 1/2 in any basis).
# States: J = 0: phi phi, psi psibar(++), psi psibar(--) (l = 0);  J = 1: psi psibar (++, --, +-, -+);  J = 2: phi phi and the
# four psi psibar states;  J = 1/2, 3/2: psi(+-1/2) phi.  Spinors in the chiral basis, helicity eigenstates along +-z,
# rotated with exp(-i theta Sigma_y/2), so that the final state at angle theta is the rotated initial state.
# Tree amplitudes (Feynman rules of App. rules):  phi phi -> phi phi: -lambda;  psi psibar -> phi phi: y^2 vbar (M - q)u/(q^2-M^2)
# summed over q = p1 - k1, p1 - k2;  psi psibar -> psi psibar: y^2 [(vbar2 g5 u1)(ubar3 g5 v4)/(s - m^2) - (ubar3 g5 u1)(vbar2 g5 v4)
# /(t - m^2)];  psi phi -> psi phi: y^2 ubar3 (M - P)u1/(P^2 - M^2) for P = p1 + k1 (s) and p1 - k2 (u).
# Checks: the spin sums against Eqs. (11) (step (2) values), the hermiticity of a^J, the convergence of the angular quadrature,
# the high-energy limits (App. pw): J = 0: (y^2/16 pi) [[-1, -2], [-2, -1]] in (++, --) (eigenvalues -3, +1; Allwicher et al.,
# model 1 with N = 1) and -lambda/(32 pi); J = 1/2: -3 y^2/(32 pi) for both helicities.
# Bounds:
#   (A) tree unitarity at fixed couplings: max over s and J of the largest |eigenvalue| of a^J <= 1/2.  a^J = y^2 P_J(s) + lambda
#       Q_J(s) is linear in (y^2, lambda), so the allowed region is convex and is found along rays in the (y^2, lambda) plane.
#   (B) tree unitarity with the one-loop running couplings (App. rgfit): y^2(mu) <= 8 pi/3 and |lambda(mu)| <= 16 pi (the
#       high-energy limits of (A)) for m <= mu <= E -> bounds on the couplings at mu = m for E = 10 m, 100 m.
#   (C) one-loop unitarity of the elements that contain phi phi (the one-loop psi psibar -> psi psibar is not computed):
#       |Re a_{phiphi,phiphi}| <= 1/2 and |a_{psipsibar,phiphi}| <= 1/2 with the S-matrix elements of Eqs. (16), (20) (COLLIER,
#       work/pw_collier, split into coupling structures) for 2m < sqrt(s) <= 4m, mu = m (band: mu = m/2, 2m with running couplings).
#       The one-loop partial waves also check the projection: Abs a^(1) = (a^(0) a^(0))_{fi} for these elements.
# Writes results/pw.csv and ../figs/pw_d4.pdf.  Usage (from Src/):  ~/miniforge3/envs/qft/bin/python pw_numeric.py
# Batch: as above.  Interactive: "Run Cell" (# %%) in VS Code.

# %%
import csv
import math
import os
import subprocess
import sys

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
MPHI, MPSI = 1.0, 0.7
K = (4 * math.pi) ** 2
mp.mp.dps = 30
H = (0.5, -0.5)
NQ = 48                          # Gauss-Legendre nodes on each half of cos(theta)

# %% [markdown]
# ## Dirac matrices and helicity spinors (chiral basis)

# %%
I2, Z2 = np.eye(2), np.zeros((2, 2))
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]])
SZ = np.array([[1, 0], [0, -1]], complex)
G0 = np.block([[Z2, I2], [I2, Z2]]).astype(complex)
GI = [np.block([[Z2, s], [-s, Z2]]) for s in (SX, SY, SZ)]
G5 = np.block([[-I2, Z2], [Z2, I2]]).astype(complex)
GLOW = [G0, -GI[0], -GI[1], -GI[2]]                 # gamma_mu, so that slash(p) = p^mu gamma_mu
SIGMA_Y = np.block([[SY, Z2], [Z2, SY]])
ONE = np.eye(4)
UP, DN = np.array([1, 0], complex), np.array([0, 1], complex)


def slash(p):
    return sum(p[i] * GLOW[i] for i in range(4))


def mdot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def bar(w):
    return w.conj() @ G0


def sqrt_psigma(e, pz, sign):
    """sqrt(p.sigma) (sign = +1) or sqrt(p.sigmabar) (sign = -1) for p = (e, 0, 0, pz)"""
    return np.diag([math.sqrt(e - sign * pz), math.sqrt(e + sign * pz)]).astype(complex)


def u_z(e, pz, lam):
    """u spinor along +z (pz > 0) or -z, helicity lam: xi eigenvector of sigma.phat with eigenvalue 2 lam"""
    xi = UP if (lam > 0) == (pz >= 0) else DN
    return np.concatenate([sqrt_psigma(e, pz, 1) @ xi, sqrt_psigma(e, pz, -1) @ xi])


def v_z(e, pz, lam):
    """v spinor along +-z, helicity lam: eta eigenvector of sigma.phat with eigenvalue -2 lam"""
    eta = DN if (lam > 0) == (pz >= 0) else UP
    return np.concatenate([sqrt_psigma(e, pz, 1) @ eta, -sqrt_psigma(e, pz, -1) @ eta])


def rot(theta):
    return expm(-0.5j * theta * SIGMA_Y)


def rot4(v, theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([v[0], c * v[1] + s * v[3], v[2], -s * v[1] + c * v[3]])


def energies(rs, ma, mb):
    ea = (rs * rs + ma * ma - mb * mb) / (2 * rs)
    return ea, rs - ea, math.sqrt(max(ea * ea - ma * ma, 0.0))


def state(kind, hel, rs, theta):
    """momenta and spinors of a two-body state along R(theta) z (first particle) and -R(theta) z (second)"""
    R = rot(theta)
    if kind == "phiphi":
        e, _, k = energies(rs, MPHI, MPHI)
        return {"k": [rot4(np.array([e, 0, 0, k]), theta), rot4(np.array([e, 0, 0, -k]), theta)]}
    if kind == "psipsibar":
        e, _, p = energies(rs, MPSI, MPSI)
        return {"p": rot4(np.array([e, 0, 0, p]), theta), "pb": rot4(np.array([e, 0, 0, -p]), theta),
                "u": R @ u_z(e, p, hel[0]), "v": R @ v_z(e, -p, hel[1])}
    e1, e2, p = energies(rs, MPSI, MPHI)                  # psi phi
    return {"p": rot4(np.array([e1, 0, 0, p]), theta), "k": rot4(np.array([e2, 0, 0, -p]), theta), "u": R @ u_z(e1, p, hel[0])}


def amp(ki, hi, kf, hf, rs, theta):
    """(coefficient of y^2, coefficient of lambda) of M(initial along z -> final at theta)"""
    i, f = state(ki, hi, rs, 0.0), state(kf, hf, rs, theta)
    if ki == kf == "phiphi":
        return 0.0, -1.0
    if ki == "psipsibar" and kf == "phiphi":
        return sum(bar(i["v"]) @ (MPSI * ONE - slash(i["p"] - k)) @ i["u"] / (mdot(i["p"] - k, i["p"] - k) - MPSI ** 2)
                   for k in f["k"]), 0.0
    if ki == "phiphi" and kf == "psipsibar":
        return sum(bar(f["u"]) @ (MPSI * ONE - slash(f["p"] - k)) @ f["v"] / (mdot(f["p"] - k, f["p"] - k) - MPSI ** 2)
                   for k in i["k"]), 0.0
    if ki == kf == "psipsibar":
        s = rs * rs
        q = i["p"] - f["p"]
        ms = (bar(i["v"]) @ G5 @ i["u"]) * (bar(f["u"]) @ G5 @ f["v"]) / (s - MPHI ** 2)
        mt = -(bar(f["u"]) @ G5 @ i["u"]) * (bar(i["v"]) @ G5 @ f["v"]) / (mdot(q, q) - MPHI ** 2)
        return ms + mt, 0.0
    # psi phi -> psi phi
    tot = 0
    for P in (i["p"] + i["k"], i["p"] - f["k"]):
        tot += bar(f["u"]) @ (MPSI * ONE - slash(P)) @ i["u"] / (mdot(P, P) - MPSI ** 2)
    return tot, 0.0

# %% [markdown]
# ## Checks of the amplitudes: spin sums (step (2)) and time reversal

# %%
th = math.acos(0.3)
sB = sum(abs(amp("psipsibar", (a, b), "phiphi", None, 5.0, th)[0]) ** 2 for a in H for b in H)
sBb = sum(abs(amp("phiphi", None, "psipsibar", (a, b), 5.0, th)[0]) ** 2 for a in H for b in H)
sC = sum(abs(amp("psipsibar", (a, b), "psipsibar", (c, d), 5.0, th)[0]) ** 2 for a in H for b in H for c in H for d in H)
print(f"sum|M|^2 at sqrt(s) = 5, cos = 0.3 (y = 1): psi psibar -> phi phi {sB:.15f} (step (2): 0.711692751300461),"
      f" phi phi -> psi psibar {sBb:.15f}, psi psibar -> psi psibar {sC:.14f} (step (2): 11.21332568891513)")

# %% [markdown]
# ## Partial-wave matrices

# %%
def wigner_d(j, mp_, m, theta):
    """Wigner small d^j_{m' m}(theta) (explicit sum)"""
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    f = math.factorial
    tot = 0.0
    for k in range(0, int(round(2 * j)) + 1):
        a, b, cc, d = j + m - k, k, j - k - mp_, k - m + mp_
        if min(a, b, cc, d) < -1e-9:
            continue
        a, b, cc, d = (int(round(x)) for x in (a, b, cc, d))
        tot += (-1) ** (k - m + mp_) * c ** (2 * j + m - mp_ - 2 * k) * s ** (2 * k - m + mp_) / (f(a) * f(b) * f(cc) * f(d))
    jm = lambda x: math.factorial(int(round(x)))
    return math.sqrt(jm(j + mp_) * jm(j - mp_) * jm(j + m) * jm(j - m)) * tot


# check against the known forms for J <= 2
_t = 0.7
_dev = max(abs(wigner_d(j, a, b, _t) - ref) for j, a, b, ref in (
    (0.5, 0.5, 0.5, math.cos(_t / 2)), (0.5, 0.5, -0.5, -math.sin(_t / 2)), (1, 0, 0, math.cos(_t)),
    (1, 1, 1, (1 + math.cos(_t)) / 2), (1, 1, 0, -math.sin(_t) / math.sqrt(2)), (1, 1, -1, (1 - math.cos(_t)) / 2),
    (1.5, 0.5, 0.5, (3 * math.cos(_t) - 1) / 2 * math.cos(_t / 2)), (2, 0, 0, (3 * math.cos(_t) ** 2 - 1) / 2),
    (2, 1, 1, (2 * math.cos(_t) - 1) * (1 + math.cos(_t)) / 2), (2, 1, -1, (2 * math.cos(_t) + 1) * (1 - math.cos(_t)) / 2)))
print(f"Wigner d against closed forms (J <= 2): max dev. {_dev:.1e}")


def nodes(A, n):
    """cos(theta) nodes: on [0, 1] c = A - e^u, on [-1, 0] the mirror image (n Gauss-Legendre nodes in u each), which flattens
    1/(A - c) and 1/(A + c) peaks (A > 1); for A = inf plain Gauss-Legendre"""
    xg, wg = np.polynomial.legendre.leggauss(n)
    if not math.isfinite(A):
        return np.concatenate([(xg - 1) / 2, (xg + 1) / 2]), np.concatenate([wg / 2, wg / 2])
    ua, ub = math.log(A - 1), math.log(A)
    u = ua + (ub - ua) * (xg + 1) / 2
    c, w = A - np.exp(u), np.exp(u) * (ub - ua) / 2 * wg
    return np.concatenate([c, -c]), np.concatenate([w, w])


def peak_A(rs):
    """the nearest propagator singularity in cos(theta) among the processes (fermion exchange in psi psibar <-> phi phi and
    psi phi -> psi phi, phi exchange in psi psibar -> psi psibar)"""
    e = rs / 2
    p, k = math.sqrt(e * e - MPSI ** 2), math.sqrt(max(e * e - MPHI ** 2, 1e-30))
    cands = [1 + MPHI ** 2 / (2 * p * p)]
    if rs > 2 * MPHI:
        cands.append((2 * e * e - MPHI ** 2) / (2 * p * k))
    if rs > MPSI + MPHI:
        e1, e2, q = energies(rs, MPSI, MPHI)
        cands.append((2 * e1 * e2 - MPHI ** 2) / (2 * q * q))
    return min(cands)


STATES = {0: [("phiphi", None, 0)] + [("psipsibar", (a, a), 0) for a in H],
          1: [("psipsibar", (a, a), 0) for a in H] + [("psipsibar", (0.5, -0.5), 1), ("psipsibar", (-0.5, 0.5), -1)],
          2: [("phiphi", None, 0)] + [("psipsibar", (a, a), 0) for a in H] + [("psipsibar", (0.5, -0.5), 1), ("psipsibar", (-0.5, 0.5), -1)],
          0.5: [("psiphi", (a,), a) for a in H], 1.5: [("psiphi", (a,), a) for a in H]}


def beta(kind, rs):
    if kind == "phiphi":
        return math.sqrt(1 - 4 * MPHI ** 2 / rs ** 2) if rs > 2 * MPHI else 0.0
    if kind == "psipsibar":
        return math.sqrt(1 - 4 * MPSI ** 2 / rs ** 2)
    return 2 * energies(rs, MPSI, MPHI)[2] / rs if rs > MPSI + MPHI else 0.0


def pw_matrices(rs, J, n=NQ):
    """P (y^2 part) and Q (lambda part) of a^J at sqrt(s) = rs"""
    sts = [st for st in STATES[J] if beta(st[0], rs) > 0 and abs(st[2]) <= J]
    c, w = nodes(peak_A(rs), n)
    P, Q = np.zeros((len(sts), len(sts)), complex), np.zeros((len(sts), len(sts)), complex)
    for a, (ki, hi, li) in enumerate(sts):
        for b, (kf, hf, lf) in enumerate(sts):
            ty = tl = 0.0
            for ci, wi in zip(c, w):
                theta = math.acos(ci)
                my, ml = amp(ki, hi, kf, hf, rs, theta)
                d = wigner_d(J, li, lf, theta)
                ty += wi * d * my
                tl += wi * d * ml
            norm = math.sqrt(beta(ki, rs) * beta(kf, rs)) * (1 / math.sqrt(2) if ki == "phiphi" else 1) \
                * (1 / math.sqrt(2) if kf == "phiphi" else 1) / (32 * math.pi)
            P[b, a], Q[b, a] = norm * ty, norm * tl
    return P, Q, sts


P5, Q5, _ = pw_matrices(5.0, 0)
P5n, Q5n, _ = pw_matrices(5.0, 0, 2 * NQ)
print(f"J = 0 at sqrt(s) = 5: hermiticity {np.abs(P5 - P5.conj().T).max():.1e}, quadrature (n vs 2n) {np.abs(P5 - P5n).max():.1e}")
np.round(16 * math.pi * P5.real, 6)          # inspect: y^2 part times 16 pi

# %% [markdown]
# ## High-energy limits

# %%
for rs in (1e2, 1e3, 1e4):
    P0, Q0, _ = pw_matrices(rs, 0)
    Ph, _, _ = pw_matrices(rs, 0.5)
    ev0 = np.linalg.eigvalsh(P0) * 16 * math.pi
    evh = np.linalg.eigvalsh(Ph) * 32 * math.pi
    print(f"sqrt(s) = {rs:7.0f}: J = 0 eigenvalues x 16 pi/y^2 {np.round(ev0, 6)} (-> -3, 0, 1), phi phi x 32 pi/lambda "
          f"{Q0[0, 0].real * 32 * math.pi:.6f} (-> -1); J = 1/2 x 32 pi/y^2 {np.round(evh, 6)} (-> -3, -3)")

# entries of the J = 0 matrix at sqrt(s) = 1e4 against the closed form (y^2/16 pi)[[-1, -2], [-2, -1]], -lambda/(32 pi)
P4, Q4, _ = pw_matrices(1e4, 0)
dev_ent = max(abs(16 * math.pi * P4[1:, 1:] - np.array([[-1, -2], [-2, -1]])).max(), abs(32 * math.pi * Q4[0, 0] + 1))
print(f"J = 0 entries at sqrt(s) = 1e4 (psi psibar block, phi phi): max dev. from the closed form {dev_ent:.1e}"
      f" (x 16 pi, x 32 pi); the phi phi - 3P0 mixing there: {16 * math.pi * abs(P4[0, 1]):.2e} (-> 0)")
# helicity amplitudes point by point against the massless forms (App. pw), sqrt(s) = 1e4, y = 1; the phi mass is kept in the
# t-channel propagator: (++)->(++) = -1, (++)->(--) = -1 - t/(t - m^2), psi(+) phi -> psi(+) phi = -(1/cos(theta/2) + cos(theta/2))
dev_pt = 0.0
for c in (-0.9, -0.3, 0.3, 0.9, 0.999999):
    th_ = math.acos(c)
    t_ = -1e8 * (1 - c) / 2
    dev_pt = max(dev_pt, abs(amp("psipsibar", (0.5, 0.5), "psipsibar", (0.5, 0.5), 1e4, th_)[0] + 1),
                 abs(amp("psipsibar", (0.5, 0.5), "psipsibar", (-0.5, -0.5), 1e4, th_)[0] + 1 + t_ / (t_ - MPHI ** 2)))
    if c < 0.95:
        dev_pt = max(dev_pt, abs(amp("psiphi", (0.5,), "psiphi", (0.5,), 1e4, th_)[0] + 1 / math.cos(th_ / 2) + math.cos(th_ / 2)))
print(f"helicity amplitudes at sqrt(s) = 1e4 against the massless forms (5 angles): max dev. {dev_pt:.1e}")
# the mixing: 16 pi |a_{phiphi, psipsibar(hh)}| = sqrt(2) y^2 (M/sqrt s) [ln(s/M^2) - 2] at leading order: the slope in ln(s) is sqrt(2)
mix = {rs: 16 * math.pi * abs(pw_matrices(rs, 0, 2 * NQ)[0][0, 1]) * rs / MPSI for rs in (1e4, 1e5, 1e6)}
print("mixing x 16 pi sqrt(s)/M at sqrt(s) = 1e4, 1e5, 1e6:", {k: round(v, 4) for k, v in mix.items()},
      f" slope in ln(s/M^2): {(mix[1e6] - mix[1e5]) / math.log(100):.5f}, {(mix[1e5] - mix[1e4]) / math.log(100):.5f}"
      f" (sqrt 2 = {math.sqrt(2):.5f})")
print("  against the leading form sqrt(2) [ln(s/M^2) - 2] (App. pw):",
      {k: f"{v / (math.sqrt(2) * (math.log(k * k / MPSI ** 2) - 2)) - 1:+.1e}" for k, v in mix.items()})

# %% [markdown]
# ## Scan in sqrt(s): the J = 0 matrices, and the other J

# %%
RS = np.concatenate([2 * MPSI + np.geomspace(1e-4, 0.6, 40), np.geomspace(2 * MPHI + 1e-4, 1e4, 120)])
RS = np.unique(np.sort(np.concatenate([RS, [2.0 + 1e-6]])))
scan = {J: [pw_matrices(rs, J) for rs in RS] for J in (0, 0.5, 1, 1.5, 2)}


def max_eig(J, y2, lam):
    """max over the scan of the largest |eigenvalue| of a^J, and the sqrt(s) where it occurs"""
    vals = [np.max(np.abs(np.linalg.eigvalsh(y2 * P + lam * Q))) if len(P) else 0.0 for P, Q, _ in scan[J]]
    i = int(np.argmax(vals))
    return vals[i], RS[i]


for J in (0, 0.5, 1, 1.5, 2):
    v1, r1 = max_eig(J, 1.0, 0.0)
    v2, r2 = max_eig(J, 0.0, 1.0)
    print(f"J = {J}: max |eig| for y = 1, lambda = 0: {v1 * 16 * math.pi:.4f}/(16 pi) at sqrt(s) = {r1:.4g};"
          f"  for y = 0, lambda = 1: {v2 * 32 * math.pi:.4f}/(32 pi) at sqrt(s) = {r2:.4g}")

v_half = max_eig(0.5, 1.0, 0.0)
print(f"J = 1/2 alone at fixed couplings: y <= {math.sqrt(0.5 / v_half[0]):.4f} (set at sqrt(s) = {v_half[1]:.3g});"
      f" massless limit sqrt(16 pi/3) = {math.sqrt(16 * math.pi / 3):.4f}")

# %% [markdown]
# ## (A) tree unitarity at fixed couplings: the region in (y^2, lambda)

# %%
def boundary(direction, J_list=(0, 0.5, 1, 1.5, 2)):
    """largest t with (y^2, lambda) = t (cos d, sin d) allowed, and the J, sqrt(s) that set it"""
    best = (0.0, None, None)
    for J in J_list:
        v, r = max_eig(J, math.cos(direction), math.sin(direction))
        if v > best[0]:
            best = (v, J, r)
    return 0.5 / best[0], best[1], best[2]


DIRS = np.linspace(-math.pi / 2, math.pi / 2, 181)
region = [(d,) + boundary(d) for d in DIRS]
y2_max0 = boundary(0.0)
lam_max0, lam_min0 = boundary(math.pi / 2), boundary(-math.pi / 2)
print(f"(A) lambda = 0: y^2 <= {y2_max0[0]:.6f} (8 pi/3 = {8 * math.pi / 3:.6f}), y <= {math.sqrt(y2_max0[0]):.4f}, set by J = {y2_max0[1]}"
      f" at sqrt(s) = {y2_max0[2]:.4g}")
print(f"(A) y = 0: {-lam_min0[0]:.4f} <= lambda <= {lam_max0[0]:.4f} (16 pi = {16 * math.pi:.4f})")
# the region against the rectangle y^2 <= 8 pi/3, |lambda| <= 16 pi (all 181 rays, corners included)
rect = [min(8 * math.pi / 3 / math.cos(d) if math.cos(d) > 1e-12 else math.inf,
            16 * math.pi / abs(math.sin(d)) if abs(math.sin(d)) > 1e-12 else math.inf) for d in DIRS]
worst = max(zip(region, rect), key=lambda z: (z[1] - z[0][1]) / z[1])
d_w = worst[0][0]
print(f"(A) region vs the rectangle y^2 <= 8 pi/3, |lambda| <= 16 pi (181 rays): largest shortfall {(worst[1] - worst[0][1]) / worst[1]:.1e}"
      f" at y^2 = {worst[0][1] * math.cos(d_w):.2f}, lambda = {worst[0][1] * math.sin(d_w):.2f}, set at sqrt(s) = {worst[0][3]:.3g} (J = {worst[0][2]});"
      f" rays with shortfall > 1e-3: {sum((q - r[1]) / q > 1e-3 for r, q in zip(region, rect))}, smallest |lambda| among them"
      f" {min(abs(r[1] * math.sin(r[0])) for r, q in zip(region, rect) if (q - r[1]) / q > 1e-3):.2f}")


def y_max_at(lam):
    """largest y allowed by (A) at fixed lambda (bisection; the region is convex)"""
    lo, hi = 0.0, 20.0
    for _ in range(60):
        mid = (lo + hi) / 2
        ok = all(max_eig(J, mid, lam)[0] <= 0.5 for J in (0, 0.5, 1, 1.5, 2))
        lo, hi = (mid, hi) if ok else (lo, mid)
    return math.sqrt(lo)


for lam in (-40.0, -16 * math.pi * 0.9, 1.0, 40.0, 16 * math.pi * 0.95):
    print(f"(A) lambda = {lam:8.3f}: y <= {y_max_at(lam):.4f}")

# %% [markdown]
# ## (B) tree unitarity with running couplings, up to the energy E

# %%
def rhs(t, v):
    y2, lam = v
    return [10 * y2 ** 2 / K, (3 * lam ** 2 + 8 * lam * y2 - 48 * y2 ** 2) / K]


def allowed_up_to(y0, lam0, E):
    """y^2(mu) <= 8 pi/3 and |lambda(mu)| <= 16 pi for m <= mu <= E (one-loop running from mu = m)"""
    if y0 ** 2 > 8 * math.pi / 3 or abs(lam0) > 16 * math.pi:
        return False
    ev = lambda t, v: min(8 * math.pi / 3 - v[0], 16 * math.pi - abs(v[1]))
    ev.terminal = True
    sol = solve_ivp(rhs, [0, math.log(E)], [y0 ** 2, lam0], events=ev, rtol=1e-10, atol=1e-12)
    return sol.status == 0


def y_max_running(lam0, E):
    lo, hi = 0.0, math.sqrt(8 * math.pi / 3)
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if allowed_up_to(mid, lam0, E) else (lo, mid)
    return lo


for E in (10.0, 100.0):
    analytic = math.sqrt((8 * math.pi / 3) / (1 + 5 / (3 * math.pi) * math.log(E)))
    print(f"(B) E = {E:5.0f} m: lambda(m) = 1: y(m) <= {y_max_running(1.0, E):.4f};  y-condition alone (analytic) y(m) <= {analytic:.4f}")
# lambda at y = 0: lambda(m) <= 16 pi/[1 + (3/pi) ln(E/m)] (App. pw) against the numerical integration
for E in (10.0, 100.0):
    lo, hi = 0.0, 16 * math.pi
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if allowed_up_to(0.0, mid, E) else (lo, mid)
    print(f"(B) E = {E:5.0f} m, y = 0: lambda(m) <= {lo:.10f} (numerical), {16 * math.pi / (1 + 3 / math.pi * math.log(E)):.10f} (closed form)")
t_bench = None
for E in np.geomspace(10, 1e7, 400):
    if not allowed_up_to(1.0, 1.0, E):
        t_bench = E
        break
print(f"(B) benchmark y = lambda = 1 at mu = m stays within the high-energy limits up to E = {t_bench:.3g} m")

# %% [markdown]
# ## One-loop partial waves of the elements with phi phi (COLLIER), the unitarity check and (C)

# %%
def dx(x, p2, ma2, mb2):
    return x * mb2 + (1 - x) * ma2 - x * (1 - x) * p2


SP = {"B0phi": float(-mp.quad(lambda x: mp.log(dx(x, 1.0, 0.49, 0.49)), [0, 1])),
      "B0pphi": float(mp.quad(lambda x: x * (1 - x) / dx(x, 1.0, 0.49, 0.49), [0, 1])),
      "B0psi": float(-mp.quad(lambda x: mp.log(dx(x, 0.49, 0.49, 1.0)), [0, 1])),
      "B1psi": float(mp.quad(lambda x: x * mp.log(dx(x, 0.49, 0.49, 1.0)), [0, 1])),
      "B0ppsi": float(mp.quad(lambda x: x * (1 - x) / dx(x, 0.49, 0.49, 1.0), [0, 1])),
      "B1ppsi": float(-mp.quad(lambda x: x * x * (1 - x) / dx(x, 0.49, 0.49, 1.0), [0, 1]))}

RS1 = np.concatenate([2 * MPHI + np.geomspace(1e-3, 2.0, 30), [5.0, 10.0]])
MUS = (0.5, 1.0, 2.0)
nodes1 = {rs: nodes(peak_A(rs), NQ) for rs in RS1}
with open(os.path.join(HERE, "work", "pw_nodes.txt"), "w") as fh:
    for rs in RS1:
        for c in nodes1[rs][0]:
            for mu in MUS:
                fh.write("%.17e %.17e %.17e\n" % (rs, c, mu))
subprocess.run([os.path.join(HERE, "work", "pw_collier"), "pw_nodes.txt", "pw_amp.csv"], cwd=os.path.join(HERE, "work"),
               check=True, capture_output=True)
loop = {}
with open(os.path.join(HERE, "work", "pw_amp.csv")) as fh:
    for r in csv.DictReader(fh):
        key = (round(float(r["sqrts"]), 9), round(float(r["mu"]), 9))
        loop.setdefault(key, []).append({k: complex(float(r["re_" + k]), float(r["im_" + k])) for k in ("ay", "al", "b", "mAl", "mAy")})


def loop_structures(rs, mu):
    """J = 0 one-loop partial waves of the S-matrix elements of Eqs. (16), (20) (pole masses, couplings at the scale mu), split
    into coupling structures and into dispersive (index 0) and absorptive (index 1) parts:
      a^(1)_{phiphi,phiphi} = lambda^2 A_ll + y^4 A_yy + lambda y^2 A_ly,   a^(1)_{phiphi,psipsibar(hh)} = y^4 B_yy[h] + lambda y^2 B_ly[h]"""
    L = math.log(mu ** 2)
    c, w = nodes1[rs]
    rows = loop[(round(rs, 9), round(mu, 9))]
    res = 4 * (SP["B0phi"] + L + SP["B0pphi"])                                  # residue term of Eq. (16) / (lambda y^2)
    dmp = SP["B0psi"] + SP["B1psi"] + L / 2                                    # (4 pi)^2 (M_p - M)/(M y^2)
    drs = (SP["B1psi"] - L / 2 + 2 * 0.49 * (SP["B0ppsi"] + SP["B1ppsi"])) - 2 * (SP["B0phi"] + L + SP["B0pphi"])
    bphi, bpsi = beta("phiphi", rs), beta("psipsibar", rs)
    nA, nB = 0.5 * bphi / (32 * math.pi * K), math.sqrt(bphi * bpsi) / math.sqrt(2) / (32 * math.pi * K)
    out = {k: np.zeros(2, complex) for k in ("A_ll", "A_yy", "A_ly")}
    out.update({(k, h): np.zeros(2, complex) for k in ("B_yy", "B_ly") for h in H})
    ist = {h: state("psipsibar", (h, h), rs, 0.0) for h in H}
    for ci, wi, r in zip(c, w, rows):
        k1 = state("phiphi", None, rs, math.acos(ci))["k"][0]
        for part, f in ((0, lambda z: z.real), (1, lambda z: z.imag)):
            out["A_ll"][part] += wi * nA * f(r["mAl"])
            out["A_yy"][part] += wi * nA * f(r["mAy"])
            out["A_ly"][part] += wi * nA * (res if part == 0 else 0.0)
        for h in H:
            st = ist[h]
            vu, vku = bar(st["v"]) @ st["u"], bar(st["v"]) @ slash(k1) @ st["u"]
            t = mdot(st["p"] - k1, st["p"] - k1)
            X, W = t - 0.49, 2 * 0.49 + 2 - rs * rs - t - 0.49
            b0 = 1 / X - 1 / W
            for part, f in ((0, lambda z: z.real), (1, lambda z: z.imag)):
                conv_a = -MPSI * dmp * (1 / X + 1 / W) if part == 0 else 0.0
                conv_b = (drs * b0 - 2 * 0.49 * dmp * (1 / X ** 2 - 1 / W ** 2)) if part == 0 else 0.0
                out[("B_yy", h)][part] += wi * nB * ((f(r["ay"]) + conv_a) * vu + (f(r["b"]) + conv_b) * vku)
                out[("B_ly", h)][part] += wi * nB * f(r["al"]) * vu
    return out


LS = {(rs, mu): loop_structures(rs, mu) for rs in RS1 for mu in MUS}
TREE0 = {rs: pw_matrices(rs, 0)[:2] for rs in RS1}


def elements(rs, y2, lam, mu, part):
    o = LS[(rs, mu)]
    A = lam ** 2 * o["A_ll"][part] + y2 ** 2 * o["A_yy"][part] + lam * y2 * o["A_ly"][part]
    B = [y2 ** 2 * o[("B_yy", h)][part] + lam * y2 * o[("B_ly", h)][part] for h in H]
    return A, B


# unitarity check at y = lambda = 1, mu = m: Abs a^(1) = (a^(0) a^(0)+)_{fi} for f = phi phi
dev_u, where = 0.0, None
for rs in RS1:
    P, Q = TREE0[rs]
    a0 = P + Q
    pred = a0 @ a0.conj().T
    A, B = elements(rs, 1.0, 1.0, 1.0, 1)
    for got, ref in ((A, pred[0, 0]), (B[0], pred[0, 1]), (B[1], pred[0, 2])):
        d = abs(got - ref) / abs(pred[0, 0])
        if d > dev_u:
            dev_u, where = d, rs
print(f"one-loop partial-wave unitarity (elements with phi phi, {len(RS1)} energies, y = lambda = 1): max dev. {dev_u:.1e}"
      f" (relative to Abs a_phiphiphiphi), at sqrt(s) = {where:.4f}")
dev_far = 0.0
for rs in RS1:
    if math.sqrt(rs ** 2 / 4 - 1) < 0.1:
        continue
    P, Q = TREE0[rs]
    pred = (P + Q) @ (P + Q).conj().T
    A, B = elements(rs, 1.0, 1.0, 1.0, 1)
    dev_far = max(dev_far, max(abs(g - r) / abs(pred[0, 0]) for g, r in ((A, pred[0, 0]), (B[0], pred[0, 1]), (B[1], pred[0, 2]))))
print(f"  the same for phi momentum p >= 0.1 m: {dev_far:.1e}")

# %% [markdown]
# ## (C) one-loop unitarity of the elements with phi phi near threshold (sqrt(s) <= 4m)

# %%
def run_to(y0, lam0, mu):
    if mu == 1.0:
        return y0 ** 2, lam0
    sol = solve_ivp(rhs, [0, math.log(mu)], [y0 ** 2, lam0], rtol=1e-11, atol=1e-13)
    return sol.y[0, -1], sol.y[1, -1]


RS_C = [rs for rs in RS1 if rs <= 4.0 + 1e-9]


def c_ok(y0, lam0, mu):
    y2, lam = run_to(y0, lam0, mu)
    for rs in RS_C:
        P, Q = TREE0[rs]
        A0, A1 = elements(rs, y2, lam, mu, 0), elements(rs, y2, lam, mu, 1)
        diag = lam * Q[0, 0].real + A0[0].real                                   # Re a_{phiphi,phiphi}
        if abs(diag) > 0.5:
            return False
        for j in (0, 1):
            off = y2 * P[0, j + 1] + A0[1][j] + 1j * A1[1][j]                     # a_{phiphi,psipsibar} (tree real)
            if abs(off) > 0.5:
                return False
    return True


def y_max_C(lam0, mu):
    lo, hi = 0.0, 8.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if c_ok(mid, lam0, mu) else (lo, mid)
    return lo


def lam_lim_C(y0, mu, sign):
    lo, hi = 0.0, 200.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if c_ok(y0, sign * mid, mu) else (lo, mid)
    return sign * lo


for mu in MUS:
    print(f"(C) mu = {mu}: lambda = 0: y <= {y_max_C(0.0, mu):.4f};  lambda = 1: y <= {y_max_C(1.0, mu):.4f};"
          f"  y = 1: {lam_lim_C(1.0, mu, -1):.3f} <= lambda <= {lam_lim_C(1.0, mu, 1):.3f}")

# %% [markdown]
# ## Table and figure: the regions of (B) and (C) as contours on a grid (the allowed y at fixed lambda need not be an interval)

# %%
def metric_B(y0, lam0, E):
    """max over m <= mu <= E of max(y^2/(8 pi/3), |lambda|/(16 pi)); allowed if <= 1"""
    ev = lambda t, v: 4.0 - max(v[0] / (8 * math.pi / 3), abs(v[1]) / (16 * math.pi))     # stop well outside
    ev.terminal = True
    sol = solve_ivp(rhs, [0, math.log(E)], [y0 ** 2, lam0], events=ev, rtol=1e-9, atol=1e-11, dense_output=True)
    if sol.status == 1:
        return 4.0
    ts = np.linspace(0, math.log(E), 200)
    v = sol.sol(ts)
    return float(np.max(np.maximum(v[0] / (8 * math.pi / 3), np.abs(v[1]) / (16 * math.pi))))


def metric_C(y0, lam0, mu):
    """max over 2m < sqrt(s) <= 4m of max(|Re a_{phiphi,phiphi}|, |a_{phiphi,psipsibar}|)/(1/2); allowed if <= 1"""
    y2, lam = run_to(y0, lam0, mu)
    worst = 0.0
    for rs in RS_C:
        P, Q = TREE0[rs]
        A0, A1 = elements(rs, y2, lam, mu, 0), elements(rs, y2, lam, mu, 1)
        worst = max(worst, abs(lam * Q[0, 0].real + A0[0].real),
                    *(abs(y2 * P[0, j + 1] + A0[1][j] + 1j * A1[1][j]) for j in (0, 1)))
    return worst / 0.5


YG, LG = np.linspace(0, 5.4, 55), np.linspace(-56, 56, 57)
grid = {("B", E): np.array([[metric_B(yv, lv, E) for yv in YG] for lv in LG]) for E in (10.0, 100.0)}
grid.update({("C", mu): np.array([[metric_C(yv, lv, mu) for yv in YG] for lv in LG]) for mu in MUS})
with open(os.path.join(HERE, "results", "pw.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["y_m", "lambda_m", "metric_A", "metric_B_E10", "metric_B_E100", "metric_C_mu1", "metric_C_mu0.5", "metric_C_mu2"])
    for i, lv in enumerate(LG):
        for j, yv in enumerate(YG):
            mA = max(yv ** 2 / (8 * math.pi / 3), abs(lv) / (16 * math.pi))
            w.writerow([yv, lv, mA, grid[("B", 10.0)][i, j], grid[("B", 100.0)][i, j], grid[("C", 1.0)][i, j],
                        grid[("C", 0.5)][i, j], grid[("C", 2.0)][i, j]])
print("wrote results/pw.csv (metrics on the (y, lambda) grid; allowed where <= 1)")

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(3.4, 6.4), gridspec_kw={"height_ratios": [1.4, 1], "hspace": 0.5})
ya = math.sqrt(8 * math.pi / 3)
ax.plot([0, ya, ya, 0], [16 * math.pi, 16 * math.pi, -16 * math.pi, -16 * math.pi], color="k", ls="-", lw=1.0)
ax.contour(YG, LG, grid[("B", 10.0)], levels=[1.0], colors="C0", linestyles="--", linewidths=1.0)
ax.contour(YG, LG, grid[("B", 100.0)], levels=[1.0], colors="C0", linestyles=":", linewidths=1.0)
ax.contour(YG, LG, grid[("C", 1.0)], levels=[1.0], colors="C1", linestyles="-.", linewidths=1.0)
for mu in (0.5, 2.0):
    ax.contour(YG, LG, grid[("C", mu)], levels=[1.0], colors="C1", linestyles="-.", linewidths=0.5)
ax.plot([1.0], [1.0], marker="*", color="C3", ms=8, ls="none")
handles = [plt.Line2D([], [], color="k", ls="-", lw=1.0), plt.Line2D([], [], color="C0", ls="--"),
           plt.Line2D([], [], color="C0", ls=":"), plt.Line2D([], [], color="C1", ls="-.", lw=1.0),
           plt.Line2D([], [], color="C1", ls="-.", lw=0.5), plt.Line2D([], [], color="C3", marker="*", ls="none", ms=8)]
ax.legend(handles, ["(A) tree", r"(B) up to $E=10m$", r"(B) up to $E=100m$", r"(C) one loop, $\mu=m$",
                    r"(C), $\mu=m/2,\ 2m$", "benchmark"], fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.16),
          ncol=2, frameon=False)
ax.set_xlim(0, 5.4)
ax.set_ylim(-56, 56)
ax.set_xlabel(r"$y$ ($\mu=m$)")
ax.set_ylabel(r"$\lambda$ ($\mu=m$)")
p_axis = [math.sqrt(rs ** 2 / 4 - 1) for rs in RS1[:-2]]
for lab, idx, col in (("A", None, "C0"), ("B++", 0, "C1"), ("B--", 1, "C2")):
    got, ref = [], []
    for rs in RS1[:-2]:
        P, Q = TREE0[rs]
        pred = (P + Q) @ (P + Q).conj().T
        A, B = elements(rs, 1.0, 1.0, 1.0, 1)
        got.append((A if idx is None else B[idx]).real)
        ref.append((pred[0, 0] if idx is None else pred[0, idx + 1]).real)
    name = {"A": r"$\phi\phi\to\phi\phi$", "B++": r"$\psi\bar\psi(++)\to\phi\phi$", "B--": r"$\psi\bar\psi(--)\to\phi\phi$"}[lab]
    ax2.plot(p_axis, got, color=col, ls="-", label=name)
    ax2.plot(p_axis, ref, color=col, ls="none", marker="o", mfc="none", ms=3.5)
ax2.set_xscale("log")
ax2.set_xlabel(r"$p/m$ ($\phi$ momentum)")
ax2.set_ylabel(r"$\mathrm{Abs}\,a^{(1)}_0$ ($y=\lambda=1$)")
ax2.axhline(0, color="0.6", lw=0.5, zorder=0)
ax2.legend(fontsize=6.5)
fig.subplots_adjust(left=0.17, right=0.97, top=0.98, bottom=0.08)
figpath = os.path.join(HERE, "..", "figs", "pw_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
