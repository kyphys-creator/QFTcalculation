# %% [markdown]
# # Step (2): tree-level spin sums and cross sections (spinor QED with e and mu)
#
# Research note models/spinor_qed, step (2).  Independent numerical checks of Eq. (11) (eq:Mtree) and Eq. (12)
# (eq:sumtree), with explicit Dirac matrices, spinors and real transverse polarization vectors, before any trace:
#
# 1. Spin and polarization sums of the Feynman-rule amplitudes against the closed forms of the note:
#    - (A) e-(p1) e+(p2) -> mu-(k1) mu+(k2), (B) Bhabha, with the photon propagator in a general covariant gauge
#      -i [g - (1 - xi) q q/q^2]/q^2: the amplitudes must not depend on xi;
#    - (C) Compton e-(p1) gamma(p2) -> e-(k1) gamma(k2), (D) e-(p1) e+(p2) -> gamma(k1) gamma(k2), summed over the two
#      physical polarizations of each photon: this is the check that replacing the sum by -g is allowed;
#    - Ward identity: replacing a photon polarization by its momentum gives 0.
# 2. Cross sections by numerical integration of Eq. (12) over cos(theta), the closed form of sigma_A (App. G) and the
#    Thomson limit of (C), against MadGraph (tree_mg5.mg5).  (B) has the Coulomb pole at t = 0 and is integrated over
#    |cos theta| < c_B; MadGraph implements this as a cut on the rapidity of e+ and e-, |y| < etal = atanh(beta c_B).
#
# Parameters: m_e = 1, m_mu = 1.7, e = 1 (GeV units in MadGraph).
# Batch:  `python3 tree_sigma.py [mg5_log]`.  With an MG5 log (from tree_mg5.mg5), the "Cross-section" lines are
# compared in order: (A), (B), (C), (D), each at SQRTS, then (C) with |cos theta_e| < 0.98 at sqrt(s) = 4, 6.
# MadGraph's (C) is low at sqrt(s) = 4, 6: it undersamples the backward u-channel peak (cos theta_e -> -1, where
# u -> m^4/s > 0), while its matrix element is right (work/sa_treeC + tree_me_points.f, compared at 21 points below)
# and the cross section with |cos theta_e| < 0.98 agrees.  The cause, found in step (6): MadEvent starts the VEGAS grid of
# a t-channel invariant as for a massless propagator and ignores the pole offset of the massive electron.  With the grid
# of mg5_tpole.py (tree_mg5_tpole.mg5, work/tree_mg5_tpole.log) all four processes agree.  Interactive (VS Code, "Run
# Cell"): the log defaults to work/tree_mg5.log.

# %%
import itertools
import math
import os
import re
import sys

import numpy as np
from scipy.integrate import quad

INTERACTIVE = "ipykernel" in sys.modules
SQRTS = (4.0, 6.0, 10.0)        # must match the order of the launches in tree_mg5.mg5
PROCS = ("A", "B", "C", "D")
GEV2_TO_PB = 0.3893794e9
ME, MMU, EE = 1.0, 1.7, 1.0
ALPHA = EE ** 2 / (4 * math.pi)
COS_B = 0.9                      # Bhabha: |cos theta| < COS_B
ETAL_B = {4.0: 1.04389844857, 6.0: 1.25087255895, 10.0: 1.38387628971}   # the etal values in tree_mg5.mg5
ETAL_C = {4.0: 1.31170377897, 6.0: 1.63682227720}                         # (C) with |cos theta_e| < 0.98
ME_DRIVER = "work/sa_treeC/SubProcesses/P1_ema_ema"                          # MadGraph standalone (C) + tree_me_points.f

# %% [markdown]
# ## Dirac matrices, spinors, polarization vectors
#
# Dirac representation: g0 = diag(1, 1, -1, -1), gi = [[0, s_i], [-s_i, 0]].
# u(p, chi) = (sqrt(E+m) chi, (s.p) chi / sqrt(E+m)),  v(p, eta) = ((s.p) eta / sqrt(E+m), sqrt(E+m) eta),
# so that sum u ubar = pslash + m and sum v vbar = pslash - m.  For a photon moving along
# n = (sin th cos ph, sin th sin ph, cos th): eps_1 = (0, cos th cos ph, cos th sin ph, -sin th),
# eps_2 = (0, -sin ph, cos ph, 0) (real, so eps* = eps).

# %%
I2 = np.eye(2, dtype=complex)
SIG = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
Z2 = np.zeros((2, 2), dtype=complex)
G0 = np.block([[I2, Z2], [Z2, -I2]])
GI = [np.block([[Z2, s], [-s, Z2]]) for s in SIG]
GAM = [G0] + GI                  # gamma^mu, upper index
METRIC = np.array([1.0, -1.0, -1.0, -1.0])
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


def pol_vectors(k):
    """two real transverse polarization vectors of a massless momentum k"""
    kv = k[1:] / np.linalg.norm(k[1:])
    th = math.acos(max(-1.0, min(1.0, kv[2])))
    ph = math.atan2(kv[1], kv[0])
    e1 = np.array([0.0, math.cos(th) * math.cos(ph), math.cos(th) * math.sin(ph), -math.sin(th)])
    e2 = np.array([0.0, -math.sin(ph), math.cos(ph), 0.0])
    return e1, e2


def current(wl, wr):
    """J^nu = wl gamma^nu wr (upper index)"""
    return np.array([wl @ GAM[n] @ wr for n in range(4)])


def jdot(a, b):
    return sum(METRIC[n] * a[n] * b[n] for n in range(4))


def check_spinors(p, mass):
    us = [u_spinor(p, mass, c) for c in CHI]
    vs = [v_spinor(p, mass, c) for c in CHI]
    dirac = max(np.abs((slash(p) - mass * ONE) @ w).max() for w in us) + max(np.abs((slash(p) + mass * ONE) @ w).max() for w in vs)
    comp_u = np.abs(sum(np.outer(w, bar(w)) for w in us) - (slash(p) + mass * ONE)).max()
    comp_v = np.abs(sum(np.outer(w, bar(w)) for w in vs) - (slash(p) - mass * ONE)).max()
    return dirac, comp_u, comp_v


# %% [markdown]
# ## CM kinematics (theta = angle of k1 to p1)

# %%
def along(e, pabs, cth, sign=1.0):
    sth = math.sqrt(max(0.0, 1 - cth * cth))
    return np.array([e, sign * pabs * sth, 0.0, sign * pabs * cth])


def kin_pair(sqrts, m_in, m_out, cth):
    """a(p1) b(p2) -> c(k1) d(k2) with masses m_in, m_in -> m_out, m_out"""
    e = sqrts / 2
    p, k = math.sqrt(e * e - m_in ** 2), math.sqrt(e * e - m_out ** 2)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    k1 = along(e, k, cth)
    k2 = np.array([e, -k1[1], -k1[2], -k1[3]])
    return p1, p2, k1, k2


def kin_compton(sqrts, cth):
    s = sqrts ** 2
    pa, ee = (s - ME ** 2) / (2 * sqrts), (s + ME ** 2) / (2 * sqrts)
    p1, p2 = np.array([ee, 0, 0, pa]), np.array([pa, 0, 0, -pa])
    k1 = along(ee, pa, cth)
    k2 = np.array([pa, -k1[1], -k1[2], -k1[3]])
    return p1, p2, k1, k2


def invariants(p1, p2, k1, k2):
    return mdot(p1 + p2, p1 + p2), mdot(p1 - k1, p1 - k1), mdot(p1 - k2, p1 - k2)


# %% [markdown]
# ## Amplitudes from the Feynman rules (Eq. (11)), general xi for the internal photon

# %%
def exch(ja, jb, q, xi):
    """photon exchange between currents ja, jb:  [ja.jb - (1-xi)(q.ja)(q.jb)/q^2]/q^2  (times e^2)"""
    q2 = mdot(q, q)
    return (jdot(ja, jb) - (1 - xi) * mdot(q, ja) * mdot(q, jb) / q2) / q2


def amps_A(sqrts, cth, xi=1.0):
    p1, p2, k1, k2 = kin_pair(sqrts, ME, MMU, cth)
    out = []
    for a, b, c, d in itertools.product(CHI, CHI, CHI, CHI):
        je = current(bar(v_spinor(p2, ME, b)), u_spinor(p1, ME, a))
        jm = current(bar(u_spinor(k1, MMU, c)), v_spinor(k2, MMU, d))
        out.append(EE ** 2 * exch(je, jm, p1 + p2, xi))
    return np.array(out)


def amps_B(sqrts, cth, xi=1.0):
    p1, p2, k1, k2 = kin_pair(sqrts, ME, ME, cth)
    out = []
    for a, b, c, d in itertools.product(CHI, CHI, CHI, CHI):
        u1, v2, u3, v4 = u_spinor(p1, ME, a), v_spinor(p2, ME, b), u_spinor(k1, ME, c), v_spinor(k2, ME, d)
        mt = exch(current(bar(u3), u1), current(bar(v2), v4), p1 - k1, xi)
        ms = exch(current(bar(u3), v4), current(bar(v2), u1), p1 + p2, xi)
        out.append(EE ** 2 * (mt - ms))
    return np.array(out)


def amps_C(sqrts, cth, replace=None):
    """replace = 'in' or 'out': the polarization of p2 or k2 is replaced by the momentum (Ward identity)"""
    p1, p2, k1, k2 = kin_compton(sqrts, cth)
    s, t, u = invariants(p1, p2, k1, k2)
    eps_in = [p2 / p2[0]] if replace == "in" else pol_vectors(p2)
    eps_out = [k2 / k2[0]] if replace == "out" else pol_vectors(k2)
    out = []
    for a, c in itertools.product(CHI, CHI):
        u1, ub3 = u_spinor(p1, ME, a), bar(u_spinor(k1, ME, c))
        for ei, eo in itertools.product(eps_in, eps_out):
            gam = (slash(eo) @ (slash(p1 + p2) + ME * ONE) @ slash(ei) / (s - ME ** 2)
                   + slash(ei) @ (slash(p1 - k2) + ME * ONE) @ slash(eo) / (u - ME ** 2))
            out.append(-EE ** 2 * ub3 @ gam @ u1)
    return np.array(out)


def amps_D(sqrts, cth, replace=None):
    """replace = 1 or 2: the polarization of k1 or k2 is replaced by the momentum"""
    p1, p2, k1, k2 = kin_pair(sqrts, ME, 0.0, cth)
    s, t, u = invariants(p1, p2, k1, k2)
    eps1 = [k1 / k1[0]] if replace == 1 else pol_vectors(k1)
    eps2 = [k2 / k2[0]] if replace == 2 else pol_vectors(k2)
    out = []
    for a, b in itertools.product(CHI, CHI):
        u1, vb2 = u_spinor(p1, ME, a), bar(v_spinor(p2, ME, b))
        for e1, e2 in itertools.product(eps1, eps2):
            gam = (slash(e2) @ (slash(p1 - k1) + ME * ONE) @ slash(e1) / (t - ME ** 2)
                   + slash(e1) @ (slash(p1 - k2) + ME * ONE) @ slash(e2) / (u - ME ** 2))
            out.append(-EE ** 2 * vb2 @ gam @ u1)
    return np.array(out)


KIN = {"A": lambda rs, c: kin_pair(rs, ME, MMU, c), "B": lambda rs, c: kin_pair(rs, ME, ME, c),
       "C": kin_compton, "D": lambda rs, c: kin_pair(rs, ME, 0.0, c)}
AMPS = {"A": amps_A, "B": amps_B, "C": amps_C, "D": amps_D}


def spinsum(proc, sqrts, cth):
    return float(np.sum(np.abs(AMPS[proc](sqrts, cth)) ** 2))


# %% [markdown]
# ## Closed forms, Eq. (12)

# %%
def note_A(s, t, u):
    sm = ME ** 2 + MMU ** 2
    return 8 * EE ** 4 / s ** 2 * ((t - sm) ** 2 + (u - sm) ** 2 + 2 * s * sm)


def note_B(s, t, u):
    m2 = ME ** 2
    return 8 * EE ** 4 * (((s - 2 * m2) ** 2 + (u - 2 * m2) ** 2 + 4 * m2 * t) / t ** 2
                          + ((t - 2 * m2) ** 2 + (u - 2 * m2) ** 2 + 4 * m2 * s) / s ** 2
                          + 2 * (u - 2 * m2) * (u - 6 * m2) / (s * t))


def note_C(s, t, u):
    m2 = ME ** 2
    a, b = s - m2, u - m2
    return 8 * EE ** 4 * (-b / a - a / b + 4 * m2 * (1 / a + 1 / b) + 4 * m2 ** 2 * (1 / a + 1 / b) ** 2)


def note_D(s, t, u):
    m2 = ME ** 2
    a, b = t - m2, u - m2
    return 8 * EE ** 4 * (b / a + a / b - 4 * m2 * (1 / a + 1 / b) - 4 * m2 ** 2 * (1 / a + 1 / b) ** 2)


NOTE = {"A": note_A, "B": note_B, "C": note_C, "D": note_D}


def note_at(proc, sqrts, cth):
    return NOTE[proc](*invariants(*KIN[proc](sqrts, cth)))


# %%
pt = np.array([math.sqrt(1.7 ** 2 + ME ** 2), 0.6, -0.9, 1.3])
pt[0] = math.sqrt(pt[1] ** 2 + pt[2] ** 2 + pt[3] ** 2 + ME ** 2)
print("spinor checks (Dirac eq., completeness u, v; expect ~1e-16):", ["%.1e" % x for x in check_spinors(pt, ME)])
k_test = np.array([2.0, 2.0 * 0.48, 2.0 * 0.6, 2.0 * 0.64])
k_test[0] = np.linalg.norm(k_test[1:])
e1, e2 = pol_vectors(k_test)
print("polarization vectors: eps.k, eps.eps, eps1.eps2 (expect 0, -1, 0):",
      ["%.1e" % mdot(e1, k_test), "%.1e" % mdot(e2, k_test), "%.3f" % mdot(e1, e1), "%.3f" % mdot(e2, e2), "%.1e" % mdot(e1, e2)])

POINTS = {proc: [(rs, c) for rs in ((3.5, 5.0, 10.0, 30.0) if proc == "A" else (2.2, 5.0, 10.0, 30.0))
                 for c in (-0.95, -0.5, 0.0, 0.3, 0.77, 0.95)] for proc in PROCS}
dev = {}
for proc in PROCS:
    dev[proc] = max(abs(note_at(proc, rs, c) - spinsum(proc, rs, c)) / spinsum(proc, rs, c) for rs, c in POINTS[proc])
print("max relative deviation, explicit spinors and polarizations vs Eq. (12), over 24 points each:")
for proc in PROCS:
    print(f"  ({proc}) {dev[proc]:.2e}")

# %% [markdown]
# ## Gauge checks: xi independence of (A), (B); Ward identity in (C), (D)

# %%
xi_dev = 0.0
for proc in ("A", "B"):
    for rs, c in POINTS[proc]:
        ref = AMPS[proc](rs, c, 1.0)
        for xi in (0.0, 3.0):
            xi_dev = max(xi_dev, np.abs(AMPS[proc](rs, c, xi) - ref).max() / np.abs(ref).max())
print(f"xi independence: max_spins |M(xi) - M(1)| / max|M(1)| for xi = 0, 3 over (A), (B): {xi_dev:.1e}")
ward = 0.0
for rs, c in POINTS["C"]:
    scale = np.abs(amps_C(rs, c)).max()
    ward = max(ward, np.abs(amps_C(rs, c, "in")).max() / scale, np.abs(amps_C(rs, c, "out")).max() / scale)
for rs, c in POINTS["D"]:
    scale = np.abs(amps_D(rs, c)).max()
    ward = max(ward, np.abs(amps_D(rs, c, 1)).max() / scale, np.abs(amps_D(rs, c, 2)).max() / scale)
print(f"Ward identity: max |M(eps -> k/k0)| / max|M| over (C), (D): {ward:.1e}")
print("check point sqrt(s) = 5, cos = 0.3 (compare with tree_feyncalc.wl):")
print("  " + "   ".join(f"({p}) {spinsum(p, 5.0, 0.3):.15g}" for p in PROCS))

# %% [markdown]
# ## Cross sections
#
# dsigma/dOmega = S |k_f| / (64 pi^2 s |p_i|) (1/4) sum|M|^2, S = 1/2 for (D) (identical photons), 1 otherwise.
# For (B), cos theta is restricted to |cos| < c_max = tanh(etal)/beta_e, the cut that MadGraph applies.

# %%
def cmom(sqrts, m1, m2):
    s = sqrts ** 2
    return math.sqrt((s - (m1 + m2) ** 2) * (s - (m1 - m2) ** 2)) / (2 * sqrts)


def sigma_pb(proc, sqrts, epsrel=1e-12, etal_c=None):
    s = sqrts ** 2
    masses = {"A": ((ME, ME), (MMU, MMU)), "B": ((ME, ME), (ME, ME)), "C": ((ME, 0.0), (ME, 0.0)), "D": ((ME, ME), (0.0, 0.0))}[proc]
    pi, kf = cmom(sqrts, *masses[0]), cmom(sqrts, *masses[1])
    sym = 0.5 if proc == "D" else 1.0
    lo, hi = -1.0, 1.0
    if proc == "B":
        beta = math.sqrt(1 - 4 * ME ** 2 / s)
        hi = math.tanh(ETAL_B[sqrts]) / beta
        lo = -hi
    if proc == "C" and etal_c is not None:      # rapidity cut on the electron: |y| = atanh(beta_e |cos|) < etal_c
        hi = math.tanh(etal_c) / (pi / math.sqrt(pi ** 2 + ME ** 2))
        lo = -hi
    f = lambda c: 0.25 * note_at(proc, sqrts, c)
    integral, _ = quad(f, lo, hi, epsabs=0, epsrel=epsrel, limit=200)
    return sym * kf / (64 * math.pi ** 2 * s * pi) * 2 * math.pi * integral * GEV2_TO_PB


def sigma_A_closed(sqrts):
    s = sqrts ** 2
    be, bm = math.sqrt(1 - 4 * ME ** 2 / s), math.sqrt(1 - 4 * MMU ** 2 / s)
    return 4 * math.pi * ALPHA ** 2 / (3 * s) * bm / be * (3 - be ** 2) * (3 - bm ** 2) / 4 * GEV2_TO_PB


print("sigma_A: closed form (App. G) vs integral of Eq. (12):",
      ", ".join(f"{abs(sigma_A_closed(rs) / sigma_pb('A', rs) - 1):.1e}" for rs in SQRTS))
# Thomson limit of (C): photon energy w in the electron rest frame, s = m^2 + 2 m w.  Klein-Nishina at small x = w/m:
# sigma/sigma_T = 1 - 2x + 26x^2/5 + O(x^3).  The integrand cancels to ~1e-8 at x = 1e-4, hence the looser tolerance.
for w in (1e-3, 1e-4):
    rs = math.sqrt(ME ** 2 + 2 * ME * w)
    sig_t = 8 * math.pi * ALPHA ** 2 / (3 * ME ** 2) * GEV2_TO_PB
    x = w / ME
    print(f"sigma_C / sigma_Thomson at x = w/m = {w:g}: {sigma_pb('C', rs, 1e-7) / sig_t:.9f}   (1 - 2x + 26x^2/5 = {1 - 2 * x + 26 * x * x / 5:.9f})")

logfile = sys.argv[1] if (len(sys.argv) > 1 and not INTERACTIVE) else ("work/tree_mg5.log" if INTERACTIVE else None)
mg5 = []
if logfile and os.path.exists(logfile):
    text = open(logfile).read()
    mg5 = [(float(a), float(b)) for a, b in re.findall(r"Cross-section :\s+([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb", text)]
mg5                                                          # inspect: (sigma, error) from MadGraph in pb

# %% [markdown]
# ## Comparison with MadGraph
#
# The log prints sigma with 4 significant digits; the pull uses err_eff = max(err, half a unit of the last digit).

# %%
print(f"{'proc':>4} {'sqrt(s)':>8} {'analytic [pb]':>15} {'MadGraph [pb]':>24} {'err_eff':>9} {'(MG-an)/err_eff':>16}")
i = 0
pulls = []
for proc in PROCS:
    for rs in SQRTS:
        an = sigma_pb(proc, rs)
        if i < len(mg5):
            x, e = mg5[i]
            half_ulp = 0.5 * 10 ** (math.floor(math.log10(abs(x))) - 3)
            e_eff = max(e, half_ulp)
            pulls.append((x - an) / e_eff)
            print(f"{proc:>4} {rs:8.2f} {an:15.6e} {x:13.5e} +- {e:8.2e} {e_eff:9.2e} {(x - an) / e_eff:16.2f}")
        else:
            print(f"{proc:>4} {rs:8.2f} {an:15.6e}")
        i += 1
if pulls:
    print(f"max |pull| = {max(abs(x) for x in pulls):.2f} over {len(pulls)} runs;  (C) at 4, 6: "
          f"MG/analytic - 1 = {mg5[6][0] / sigma_pb('C', 4.0) - 1:+.4f}, {mg5[7][0] / sigma_pb('C', 6.0) - 1:+.4f}")

# %% [markdown]
# ## (C) without the backward peak, and MadGraph's matrix element
#
# With |cos theta_e| < 0.98 MadGraph agrees with the integral of Eq. (12): the deficit is in the backward region.
# Its standalone matrix element (averaged over the initial helicities: (1/4) sum|M|^2) is compared at fixed points.

# %%
for j, rs in enumerate((4.0, 6.0)):
    an = sigma_pb("C", rs, etal_c=ETAL_C[rs])
    if 12 + j < len(mg5):
        x, e = mg5[12 + j]
        print(f"   C {rs:8.2f} |cos|<0.98 {an:15.6e} {x:13.5e} +- {e:8.2e} {(x - an) / e:16.2f}")
    print(f"   C {rs:8.2f}: fraction of sigma_C at |cos theta_e| > 0.98 = {1 - an / sigma_pb('C', rs):.4f}, "
          f"at u > 0 (cos < {(ME ** 2 / (2 * cmom(rs, ME, 0.0)) - (rs ** 2 + ME ** 2) / (2 * rs)) / cmom(rs, ME, 0.0):.5f}) "
          f"= {quad(lambda c: note_at('C', rs, c), -1, (ME ** 2 / (2 * cmom(rs, ME, 0.0)) - (rs ** 2 + ME ** 2) / (2 * rs)) / cmom(rs, ME, 0.0), epsrel=1e-12)[0] / quad(lambda c: note_at('C', rs, c), -1, 1, epsrel=1e-12, limit=200)[0]:.4f}")

if os.path.exists(os.path.join(ME_DRIVER, "me_points")):
    import subprocess
    pts = [(rs, c) for rs in SQRTS for c in (-0.99, -0.9, -0.5, 0.0, 0.5, 0.9, 0.99)]
    lines = "\n".join(" ".join(f"{x:.17e}" for v in kin_compton(rs, c) for x in v) for rs, c in pts) + "\n"
    res = subprocess.run(["./me_points"], input=lines, capture_output=True, text=True, cwd=ME_DRIVER)
    vals = [float(x) for x in res.stdout.split() if x[0] in "0123456789-+."]
    dme = max(abs(v / (0.25 * note_at("C", rs, c)) - 1) for (rs, c), v in zip(pts, vals))
    print(f"MadGraph standalone (1/4) sum|M_C|^2 vs Eq. (12) at {len(vals)} points: max relative deviation {dme:.1e}")


# %% [markdown]
# ## MadGraph with the grid of mg5_tpole.py
#
# MadEvent samples a t-channel invariant as x = -t/s on a VEGAS grid that it starts logarithmic above a cut-dependent x_o, as
# for a massless propagator; the pole offset -m^2/s of a massive one is not used (setgrid itype 1), so the region next to the
# electron pole (u -> m^2 in (C)) starts in one wide bin.  mg5_tpole.py starts the grid logarithmic around the pole for
# massive t-channel propagators: (C) (u-channel electron) and (D) (t- and u-channel electron); (A) and (B) keep MadGraph's grid.
# tree_mg5_tpole.mg5 repeats the main runs with it, then (C) at sqrt(s) = 4 with 1e5 events.  The cross sections are read to
# 6 digits from the run banners, the errors from work/tree_mg5_tpole.log.

# %%
TPOLE_LOG = "work/tree_mg5_tpole.log"


def banner_sigma(proc, k):
    run = f"run_{k:02d}"
    text = open(f"work/mg5_tree{proc}_tpole/Events/{run}/{run}_tag_1_banner.txt").read()
    return float(re.search(r"Integrated weight \(pb\)\s*:\s*(\S+)", text).group(1))


if os.path.exists(TPOLE_LOG):
    tp_err = [float(b) for b in re.findall(r"Cross-section :\s+[0-9.eE+-]+ \+- ([0-9.eE+-]+) pb", open(TPOLE_LOG).read())]
    runs = [(proc, rs, k + 1) for proc in PROCS for k, rs in enumerate(SQRTS)] + [("C", 4.0, 4)]
    print(f"{'proc':>4} {'sqrt(s)':>8} {'analytic [pb]':>15} {'MadGraph, pole grid [pb]':>27} {'(MG-an)/err':>12}")
    for (proc, rs, k), e in zip(runs, tp_err):
        an, x = sigma_pb(proc, rs), banner_sigma(proc, k)
        print(f"{proc:>4} {rs:8.2f} {an:15.6e} {x:14.6e} +- {e:8.2e} {(x - an) / e:12.2f}" + ("   (1e5 events)" if k == 4 else ""))
