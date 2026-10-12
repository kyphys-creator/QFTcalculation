# %% [markdown]
# # Step (2): tree-level spin sums and cross sections (pseudoscalar Yukawa + phi^4)
#
# Research note models/yukawa_ps, step (2).  Two independent checks of Eq. (11) (eq:Mtree) and of eq:MtreeD:
#
# 1. Spin sums from explicit Dirac matrices and spinors (Dirac representation), built from the Feynman-rule amplitudes
#    before any trace or Dirac-equation simplification:
#    - (B) psi(p1) psibar(p2) -> phi(k1) phi(k2):  M = y^2 vbar(p2) [g5 (p1-k1+M) g5/(t-M^2) + g5 (p1-k2+M) g5/(u-M^2)] u(p1)
#    - (C) psi(p1) psibar(p2) -> psi(p3) psibar(p4):  M = y^2 [vb2 g5 u1][ub3 g5 v4]/(s-m^2) - y^2 [ub3 g5 u1][vb2 g5 v4]/(t-m^2)
#    - (D) psi(p1) psi(p2) -> psi(p3) psi(p4):  M = y^2 [ub3 g5 u1][ub4 g5 u2]/(t-m^2) - y^2 [ub4 g5 u1][ub3 g5 u2]/(u-m^2)
#    The sums over all spins are compared with the closed forms of the note (and with the CM-frame form of (B)).
# 2. Cross sections, Eq. (12) (eq:sigma) and sigma_D, by numerical integration over cos(theta), against MadGraph.
#
# Parameters: m = 1, M = 0.7, y = lambda = 1 (GeV units in MadGraph).
# Batch:  `python3 tree_sigma.py [mg5_log]`.  With an MG5 log (from tree_mg5.mg5), the "Cross-section" lines are
# compared in order: (A), (B), (C), (D), each at SQRTS.  Interactive (VS Code, "Run Cell"): the log defaults to
# work/tree_mg5.log.

# %%
import itertools
import math
import os
import re
import sys

import numpy as np
from scipy.integrate import quad

INTERACTIVE = "ipykernel" in sys.modules
SQRTS = (2.5, 5.0, 10.0)        # must match the order of the launches in tree_mg5.mg5
PROCS = ("A", "B", "C", "D")
GEV2_TO_PB = 0.3893794e9
MPHI, MPSI, Y, LAM = 1.0, 0.7, 1.0, 1.0

# %% [markdown]
# ## Dirac matrices and spinors
#
# Dirac representation: g0 = diag(1, 1, -1, -1), gi = [[0, s_i], [-s_i, 0]], g5 = i g0 g1 g2 g3 = [[0, 1], [1, 0]].
# u(p, chi) = (sqrt(E+M) chi, (s.p) chi / sqrt(E+M)),  v(p, eta) = ((s.p) eta / sqrt(E+M), sqrt(E+M) eta),
# so that sum u ubar = pslash + M and sum v vbar = pslash - M.

# %%
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
G0 = np.block([[I2, Z2], [Z2, -I2]])
GI = [np.block([[Z2, s], [-s, Z2]]) for s in SIG]
G5 = 1j * G0 @ GI[0] @ GI[1] @ GI[2]
ONE = np.eye(4, dtype=complex)
CHI = [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]


def slash(p):
    return p[0] * G0 - p[1] * GI[0] - p[2] * GI[1] - p[3] * GI[2]


def mdot(p, q):
    return p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3]


def u_spinor(p, mass, chi):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + mass)
    return np.concatenate([n * chi, sp @ chi / n])


def v_spinor(p, mass, eta):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + mass)
    return np.concatenate([sp @ eta / n, n * eta])


def bar(w):
    return w.conj() @ G0


def four(e, pabs, cth):
    sth = math.sqrt(max(0.0, 1 - cth * cth))
    return np.array([e, pabs * sth, 0.0, pabs * cth])


def check_spinors(p, mass):
    """(pslash - M) u = 0, (pslash + M) v = 0, completeness relations."""
    us = [u_spinor(p, mass, c) for c in CHI]
    vs = [v_spinor(p, mass, c) for c in CHI]
    dirac = max(np.abs((slash(p) - mass * ONE) @ w).max() for w in us) + max(np.abs((slash(p) + mass * ONE) @ w).max() for w in vs)
    comp_u = np.abs(sum(np.outer(w, bar(w)) for w in us) - (slash(p) + mass * ONE)).max()
    comp_v = np.abs(sum(np.outer(w, bar(w)) for w in vs) - (slash(p) - mass * ONE)).max()
    return dirac, comp_u, comp_v


# %% [markdown]
# ## Spin sums: explicit spinors vs the closed forms of the note

# %%
def kin_B(sqrts, cth):
    e = sqrts / 2
    p, k = math.sqrt(e * e - MPSI ** 2), math.sqrt(e * e - MPHI ** 2)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    k1 = four(e, k, cth)
    k2 = np.array([e, -k1[1], -k1[2], -k1[3]])
    return p1, p2, k1, k2, p, k


def kin_CD(sqrts, cth):
    e = sqrts / 2
    p = math.sqrt(e * e - MPSI ** 2)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    p3 = four(e, p, cth)
    p4 = np.array([e, -p3[1], -p3[2], -p3[3]])
    return p1, p2, p3, p4


def spinsum_B(sqrts, cth):
    p1, p2, k1, k2, _, _ = kin_B(sqrts, cth)
    t, u = mdot(p1 - k1, p1 - k1), mdot(p1 - k2, p1 - k2)
    gam = (G5 @ (slash(p1 - k1) + MPSI * ONE) @ G5 / (t - MPSI ** 2)
           + G5 @ (slash(p1 - k2) + MPSI * ONE) @ G5 / (u - MPSI ** 2))
    tot = 0.0
    for a, b in itertools.product(CHI, CHI):
        amp = Y ** 2 * bar(v_spinor(p2, MPSI, b)) @ gam @ u_spinor(p1, MPSI, a)
        tot += abs(amp) ** 2
    return tot


def spinsum_C(sqrts, cth):
    p1, p2, p3, p4 = kin_CD(sqrts, cth)
    s, t = mdot(p1 + p2, p1 + p2), mdot(p1 - p3, p1 - p3)
    tot = 0.0
    for a, b, c, d in itertools.product(CHI, CHI, CHI, CHI):
        u1, v2, u3, v4 = u_spinor(p1, MPSI, a), v_spinor(p2, MPSI, b), u_spinor(p3, MPSI, c), v_spinor(p4, MPSI, d)
        amp = (Y ** 2 * (bar(v2) @ G5 @ u1) * (bar(u3) @ G5 @ v4) / (s - MPHI ** 2)
               - Y ** 2 * (bar(u3) @ G5 @ u1) * (bar(v2) @ G5 @ v4) / (t - MPHI ** 2))
        tot += abs(amp) ** 2
    return tot


def spinsum_D(sqrts, cth):
    p1, p2, p3, p4 = kin_CD(sqrts, cth)
    t, u = mdot(p1 - p3, p1 - p3), mdot(p1 - p4, p1 - p4)
    tot = 0.0
    for a, b, c, d in itertools.product(CHI, CHI, CHI, CHI):
        u1, u2, u3, u4 = (u_spinor(q, MPSI, x) for q, x in ((p1, a), (p2, b), (p3, c), (p4, d)))
        amp = (Y ** 2 * (bar(u3) @ G5 @ u1) * (bar(u4) @ G5 @ u2) / (t - MPHI ** 2)
               - Y ** 2 * (bar(u4) @ G5 @ u1) * (bar(u3) @ G5 @ u2) / (u - MPHI ** 2))
        tot += abs(amp) ** 2
    return tot


def note_B(s, t, u):
    x, w = t - MPSI ** 2, u - MPSI ** 2
    return 2 * Y ** 4 * (x * w - MPHI ** 4) * (t - u) ** 2 / (x * x * w * w)


def note_B_cm(sqrts, cth):
    """CM-frame form: sum|M_B|^2 = 32 y^4 p^2 k^4 cos^2 (s - 4 p^2 cos^2) / ((t-M^2)^2 (u-M^2)^2)."""
    p1, p2, k1, k2, p, k = kin_B(sqrts, cth)
    s = sqrts ** 2
    t, u = mdot(p1 - k1, p1 - k1), mdot(p1 - k2, p1 - k2)
    return 32 * Y ** 4 * p ** 2 * k ** 4 * cth ** 2 * (s - 4 * p ** 2 * cth ** 2) / ((t - MPSI ** 2) ** 2 * (u - MPSI ** 2) ** 2)


def note_C(s, t, u):
    m2 = MPHI ** 2
    return 4 * Y ** 4 * (s * s / (s - m2) ** 2 + t * t / (t - m2) ** 2 + s * t / ((s - m2) * (t - m2)))


def note_D(s, t, u):
    m2 = MPHI ** 2
    return 4 * Y ** 4 * (t * t / (t - m2) ** 2 + u * u / (u - m2) ** 2 + t * u / ((t - m2) * (u - m2)))


def mandelstam_B(sqrts, cth):
    p1, p2, k1, k2, _, _ = kin_B(sqrts, cth)
    return sqrts ** 2, mdot(p1 - k1, p1 - k1), mdot(p1 - k2, p1 - k2)


def mandelstam_CD(sqrts, cth):
    p1, p2, p3, p4 = kin_CD(sqrts, cth)
    return sqrts ** 2, mdot(p1 - p3, p1 - p3), mdot(p1 - p4, p1 - p4)


# %%
pt = four(2.0, 1.7, 0.4)
pt[0] = math.sqrt(1.7 ** 2 + MPSI ** 2)
print("spinor checks (Dirac eq., completeness u, v; expect ~1e-16):", ["%.1e" % x for x in check_spinors(pt, MPSI)])
points = [(rs, c) for rs in (2.1, 2.5, 5.0, 10.0) for c in (-0.9, -0.3, 0.0, 0.3, 0.77)]
def rel(a, ref, scale):
    """relative deviation; where sum|M|^2 vanishes (B at cos = 0) the deviation is taken relative to `scale`."""
    return abs(a - ref) / max(abs(ref), scale)


dev = {"B": 0.0, "B_cm": 0.0, "C": 0.0, "D": 0.0}
zeroB = 0.0
for rs, c in points:
    s, t, u = mandelstam_B(rs, c)
    ref = spinsum_B(rs, c)
    scale = 1e-6 * spinsum_B(rs, 0.77)
    dev["B"] = max(dev["B"], rel(note_B(s, t, u), ref, scale))
    dev["B_cm"] = max(dev["B_cm"], rel(note_B_cm(rs, c), ref, scale))
    if c == 0.0:
        zeroB = max(zeroB, abs(ref) / spinsum_B(rs, 0.77))
    s, t, u = mandelstam_CD(rs, c)
    dev["C"] = max(dev["C"], rel(note_C(s, t, u), spinsum_C(rs, c), 0.0))
    dev["D"] = max(dev["D"], rel(note_D(s, t, u), spinsum_D(rs, c), 0.0))
print("max relative deviation, explicit spinors vs note over", len(points), "points:")
for key, val in dev.items():
    print(f"  {key:5s} {val:.2e}")
print(f"  (B) at cos = 0: explicit-spinor sum / its value at cos = 0.77 = {zeroB:.1e}  (the note's formula is exactly 0)")
print("check point sqrt(s) = 5, cos = 0.3 (compare with tree_feyncalc.wl):")
print(f"  (B) {spinsum_B(5.0, 0.3):.15f}   (C) {spinsum_C(5.0, 0.3):.14f}   (D) {spinsum_D(5.0, 0.3):.14f}")

# %% [markdown]
# ## Cross sections, Eq. (12) (eq:sigma) and sigma_D
#
# sigma = S k/(64 pi^2 s p) * 2 pi int dc (1/4) sum|M|^2 for fermion beams (S = 1/2 for identical final particles):
# (A) S = 1/2, k = p, no spin average:  sigma_A = lambda^2 / (32 pi s);  (B) S = 1/2;  (C) S = 1;  (D) S = 1/2.

# %%
def sigma_pb(proc, sqrts):
    s = sqrts ** 2
    if proc == "A":
        return LAM ** 2 / (32 * math.pi * s) * GEV2_TO_PB
    if proc == "B":
        p, k = math.sqrt(s / 4 - MPSI ** 2), math.sqrt(s / 4 - MPHI ** 2)
        f = lambda c: 0.25 * note_B(*mandelstam_B(sqrts, c))
        sym, flux = 0.5, k / (64 * math.pi ** 2 * s * p)
    else:
        f = (lambda c: 0.25 * note_C(*mandelstam_CD(sqrts, c))) if proc == "C" else (lambda c: 0.25 * note_D(*mandelstam_CD(sqrts, c)))
        sym, flux = (1.0 if proc == "C" else 0.5), 1 / (64 * math.pi ** 2 * s)
    integral, _ = quad(f, -1, 1, epsabs=0, epsrel=1e-12)
    return sym * flux * 2 * math.pi * integral * GEV2_TO_PB


logfile = sys.argv[1] if (len(sys.argv) > 1 and not INTERACTIVE) else ("work/tree_mg5.log" if INTERACTIVE else None)
mg5 = []
if logfile and os.path.exists(logfile):
    text = open(logfile).read()
    mg5 = [(float(a), float(b)) for a, b in re.findall(r"Cross-section :\s+([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb", text)]
mg5                                                          # inspect: (sigma, error) from MadGraph in pb

# %% [markdown]
# ## Comparison with MadGraph
#
# The log prints sigma with 4 significant digits.  For (A) |M|^2 is constant, so MadGraph's integration error is ~0 and
# the printed value is limited by rounding; the pull therefore uses err_eff = max(err, half a unit of the last printed
# digit).

# %%
print(f"{'proc':>4} {'sqrt(s)':>8} {'analytic [pb]':>15} {'MadGraph [pb]':>24} {'err_eff':>9} {'(MG-an)/err_eff':>16}")
i = 0
for proc in PROCS:
    for rs in SQRTS:
        an = sigma_pb(proc, rs)
        if i < len(mg5):
            x, e = mg5[i]
            half_ulp = 0.5 * 10 ** (math.floor(math.log10(abs(x))) - 3)
            e_eff = max(e, half_ulp)
            print(f"{proc:>4} {rs:8.2f} {an:15.6e} {x:13.5e} +- {e:8.2e} {e_eff:9.2e} {(x - an) / e_eff:16.2f}")
        else:
            print(f"{proc:>4} {rs:8.2f} {an:15.6e}")
        i += 1
