# %% [markdown]
# # Step (2): tree amplitudes with explicit polarization vectors (abelian Higgs model)
#
# Research note models/abelian_higgs, step (2).  Independent numerical checks of the tree formulas of the note with
# explicit helicity polarization vectors (no polarization sums by -g + k k/M^2):
#
# 1. completeness of the polarization vectors, sum_lambda eps^mu eps^nu* = -g^{mu nu} + k^mu k^nu/MA^2;
# 2. sum|M|^2 of A A -> A A (Eq. Maa) and A A -> h h (Eq. Mahh) over all 81 / 9 helicity combinations against the exact
#    FeynCalc values of tree_feyncalc.wl (results/tree_feyncalc_points.csv);
# 3. A A -> h h from the six R_xi diagrams written out (A exchange with the full R_xi propagator, G exchange with mass
#    sqrt(xi) MA): independent of xi, and the xi part of the A exchange cancels the G exchange diagram by diagram;
# 4. equivalence theorem: A_L A_L -> A_L A_L against G G -> G G and A_L A_L -> h h against G G -> h h (Landau gauge);
# 5. Gamma(h -> A A) from the helicity sum against Eq. (width), and the cross sections of A A -> A A, A A -> h h,
#    h h -> h h by integration over cos(theta) (for tree_mg5.mg5);
# 6. the phase-space points for the MadGraph standalone matrix elements (work/me_points_*.txt) and their values in
#    MadGraph's normalization (average over the initial helicities, 1/2 for identical final particles).
# Output: results/tree_numeric.csv.
# Parameters: the benchmark point, e = 1/2, MA = 1, MH = 5/2 (GeV units in MadGraph).
# Batch:  `python3 tree_numeric.py`  (from any directory).  Interactive (VS Code, "Run Cell"): run from the top.

# %%
import csv
import itertools
import math
import os
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path(os.getcwd())
RES = HERE / "results"
WORK = HERE / "work"
RES.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

EE, MA, MH = 0.5, 1.0, 2.5
V = MA / EE
LAM = EE ** 2 * MH ** 2 / (2 * MA ** 2)
GEV2_TO_PB = 0.3893793721e9
G = np.diag([1.0, -1.0, -1.0, -1.0])
rows = []          # (quantity, value, reference, relative difference)


def dot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


# %% [markdown]
# ## Kinematics and polarization vectors
#
# 2 -> 2 in the CM frame: particle 1 along +z, particle 3 at angle theta in the xz plane.  For a vector boson of
# momentum k = (E, |k| n), n = (sin th, 0, cos th):  eps(+-) = (0, -+(e_th +- i e_ph))/sqrt 2 with
# e_th = (cos th, 0, -sin th), e_ph = (0, 1, 0), and eps(0) = (|k|, E n)/MA.  Incoming vectors carry eps, outgoing eps*.

# %%
def momenta(rs, c, m1, m2, m3, m4):
    s = rs * rs
    p = math.sqrt((s - (m1 + m2) ** 2) * (s - (m1 - m2) ** 2)) / (2 * rs)
    q = math.sqrt((s - (m3 + m4) ** 2) * (s - (m3 - m4) ** 2)) / (2 * rs)
    e1, e2 = (s + m1 ** 2 - m2 ** 2) / (2 * rs), (s + m2 ** 2 - m1 ** 2) / (2 * rs)
    e3, e4 = (s + m3 ** 2 - m4 ** 2) / (2 * rs), (s + m4 ** 2 - m3 ** 2) / (2 * rs)
    sn = math.sqrt(max(0.0, 1 - c * c))
    k1 = np.array([e1, 0, 0, p]); k2 = np.array([e2, 0, 0, -p])
    k3 = np.array([e3, q * sn, 0, q * c]); k4 = np.array([e4, -q * sn, 0, -q * c])
    return k1, k2, k3, k4


def pols(k, m):
    """eps(+1), eps(-1), eps(0) of a vector boson of mass m and momentum k."""
    kv = k[1:]
    kk = np.linalg.norm(kv)
    th = math.atan2(math.hypot(kv[0], kv[1]), kv[2])
    ph = math.atan2(kv[1], kv[0])
    eth = np.array([math.cos(th) * math.cos(ph), math.cos(th) * math.sin(ph), -math.sin(th)])
    eph = np.array([-math.sin(ph), math.cos(ph), 0.0])
    ep = np.concatenate([[0], -(eth + 1j * eph) / math.sqrt(2)])
    em = np.concatenate([[0], (eth - 1j * eph) / math.sqrt(2)])
    n = kv / kk
    e0 = np.concatenate([[kk], k[0] * n]) / m
    return [ep, em, e0.astype(complex)]


# completeness: sum eps eps* = -g + k k/M^2 (lower indices of g written as G, k with upper indices)
k1, k2, k3, k4 = momenta(6.0, 0.7, MA, MA, MA, MA)
worst = 0.0
for k in (k1, k2, k3, k4):
    s_ = sum(np.outer(e, e.conj()) for e in pols(k, MA))
    worst = max(worst, np.max(np.abs(s_ - (-G + np.outer(k, k) / MA ** 2))))
print("1. completeness of the polarization vectors, max |sum eps eps* - (-g + k k/M^2)| = %.1e" % worst)
rows.append(["completeness_maxdiff", worst, 0.0, worst])

# %% [markdown]
# ## Amplitudes (note Eqs. (Maa), (MLL), (Mahh), (Mhh), (Mgghh), (et))

# %%
def m_aaaa(e1, e2, e3c, e4c, s, t, u):
    return -4 * EE ** 2 * MA ** 2 * (dot(e1, e2) * dot(e3c, e4c) / (s - MH ** 2) + dot(e1, e3c) * dot(e2, e4c) / (t - MH ** 2)
                                     + dot(e1, e4c) * dot(e2, e3c) / (u - MH ** 2))


def m_aahh(e1, e2, p1, p2, s, t, u):
    e12 = dot(e1, e2)
    return (2 * EE ** 2 * e12 * (1 + 3 * MH ** 2 / (s - MH ** 2))
            + 4 * EE ** 2 * (MA ** 2 * e12 + dot(e1, p1) * dot(e2, p2)) / (t - MA ** 2)
            + 4 * EE ** 2 * (MA ** 2 * e12 + dot(e1, p2) * dot(e2, p1)) / (u - MA ** 2))


def m_aahh_rxi(e1, e2, k1, k2, p1, p2, s, xi):
    """the six R_xi diagrams: contact, s-channel h, t/u-channel A (full R_xi propagator), t/u-channel G."""
    e12 = dot(e1, e2)
    m = 2 * EE ** 2 * e12 + 12 * EE * MA * LAM * V * e12 / (s - MH ** 2)
    parts = {}
    for (pa, pb) in ((p1, p2), (p2, p1)):
        q = k1 - pa
        q2 = dot(q, q)
        # (2 i e MA)^2 eps1^mu (-i)[g_{mu nu} - (1 - xi) q_mu q_nu/(q^2 - xi MA^2)]/(q^2 - MA^2) eps2^nu, divided by i
        a_u = 4 * EE ** 2 * MA ** 2 * (e12 - dot(e1, q) * dot(e2, q) / MA ** 2) / (q2 - MA ** 2)
        a_x = 4 * EE ** 2 * dot(e1, q) * dot(e2, q) / (q2 - xi * MA ** 2)
        # G exchange: e (p_h - p_G).eps at both vertices, i/(q^2 - xi MA^2)
        g_x = (EE * dot(e1, k1 - 2 * pa)) * (EE * dot(e2, k2 - 2 * pb)) / (q2 - xi * MA ** 2)
        m += a_u + a_x + g_x
        parts.setdefault("ax_plus_g", []).append(a_x + g_x)
    return m, parts


def m_hhhh(s, t, u):
    return -6 * LAM - 9 * MH ** 4 / V ** 2 * (1 / (s - MH ** 2) + 1 / (t - MH ** 2) + 1 / (u - MH ** 2))


def m_gggg(s, t, u):
    return -6 * LAM - MH ** 4 / V ** 2 * (1 / (s - MH ** 2) + 1 / (t - MH ** 2) + 1 / (u - MH ** 2))


def m_gghh(s, t, u):
    """Landau gauge, massless G."""
    return (-2 * LAM - 3 * MH ** 4 / (V ** 2 * (s - MH ** 2)) - MH ** 4 / V ** 2 * (1 / t + 1 / u)
            - EE ** 2 * (s - u + MH ** 4 / t) / (t - MA ** 2) - EE ** 2 * (s - t + MH ** 4 / u) / (u - MA ** 2))


def mandelstam(k1, k2, k3):
    return dot(k1 + k2, k1 + k2), dot(k1 - k3, k1 - k3), dot(k2 - k3, k2 - k3)


def sum_aaaa(rs, c):
    k1, k2, k3, k4 = momenta(rs, c, MA, MA, MA, MA)
    s, t, u = mandelstam(k1, k2, k3)
    P = [pols(k, MA) for k in (k1, k2, k3, k4)]
    return sum(abs(m_aaaa(a, b, cc.conj(), d.conj(), s, t, u)) ** 2 for a, b, cc, d in itertools.product(*P))


def sum_aahh(rs, c):
    k1, k2, p1, p2 = momenta(rs, c, MA, MA, MH, MH)
    s, t, u = mandelstam(k1, k2, p1)
    return sum(abs(m_aahh(a, b, p1, p2, s, t, u)) ** 2 for a, b in itertools.product(pols(k1, MA), pols(k2, MA)))


def sum_hhhh(rs, c):
    k1, k2, p1, p2 = momenta(rs, c, MH, MH, MH, MH)
    return m_hhhh(*mandelstam(k1, k2, p1)) ** 2


# %% [markdown]
# ## 2. Helicity sums against FeynCalc (exact values)

# %%
ref = list(csv.DictReader(open(RES / "tree_feyncalc_points.csv")))
print("2. sum|M|^2 over all helicities vs FeynCalc (exact):")
for r in ref:
    rs, c = float(r["sqrt_s"]), float(Fraction(r["cos_theta"]))
    ours = sum_aaaa(rs, c) if r["process"] == "AAAA" else sum_aahh(rs, c)
    fc = float(r["sum_M2"])
    d = ours / fc - 1
    rows.append(["sumM2_%s_%g_%s" % (r["process"], rs, r["cos_theta"]), ours, fc, d])
    print("   %s sqrt(s) = %6g cos = %5s : %.16e  FeynCalc %.16e  rel. diff %+.1e" % (r["process"], rs, r["cos_theta"], ours, fc, d))

# %% [markdown]
# ## 3. A A -> h h in R_xi: independence of xi, diagram by diagram

# %%
worst_xi, worst_part = 0.0, 0.0
for rs, c in ((6.0, 0.7), (6.0, -0.5), (20.0, 0.2)):
    k1, k2, p1, p2 = momenta(rs, c, MA, MA, MH, MH)
    s, t, u = mandelstam(k1, k2, p1)
    for a, b in itertools.product(pols(k1, MA), pols(k2, MA)):
        ref_u = m_aahh(a, b, p1, p2, s, t, u)
        for xi in (0.0, 0.5, 1.0, 3.0, 10.0):
            m, parts = m_aahh_rxi(a, b, k1, k2, p1, p2, s, xi)
            worst_xi = max(worst_xi, abs(m - ref_u) / max(abs(ref_u), 1e-300))
            worst_part = max(worst_part, max(abs(x) for x in parts["ax_plus_g"]))
print("3. A A -> h h, R_xi diagrams (xi = 0, 1/2, 1, 3, 10) vs Eq. (Mahh): max rel. diff %.1e;"
      " max |xi part of A exchange + G exchange| = %.1e" % (worst_xi, worst_part))
rows.append(["aahh_rxi_vs_unitary_maxrel", worst_xi, 0.0, worst_xi])
rows.append(["aahh_xpart_plus_G_max", worst_part, 0.0, worst_part])

# %% [markdown]
# ## 4. Equivalence theorem
#
# Longitudinal amplitudes at cos(theta) = 0.4 against the Goldstone amplitudes (Landau gauge, massless G).  The
# difference falls like MA^2/E^2.

# %%
print("4. equivalence theorem (cos theta = 0.4):")
c = 0.4
for E in (3.0, 10.0, 100.0, 1000.0):
    rs = 2 * E
    k1, k2, k3, k4 = momenta(rs, c, MA, MA, MA, MA)
    s, t, u = mandelstam(k1, k2, k3)
    mll = m_aaaa(pols(k1, MA)[2], pols(k2, MA)[2], pols(k3, MA)[2], pols(k4, MA)[2], s, t, u).real
    q1, q2, q3, q4 = momenta(rs, c, 0.0 + 1e-300, 0.0 + 1e-300, 0.0 + 1e-300, 0.0 + 1e-300)
    mg = m_gggg(*mandelstam(q1, q2, q3))
    k1, k2, p1, p2 = momenta(rs, c, MA, MA, MH, MH)
    s, t, u = mandelstam(k1, k2, p1)
    mlh = m_aahh(pols(k1, MA)[2], pols(k2, MA)[2], p1, p2, s, t, u).real
    q1, q2, p1g, p2g = momenta(rs, c, 1e-300, 1e-300, MH, MH)
    mgh = m_gghh(*mandelstam(q1, q2, p1g))
    print("   E = %7g: A_L A_L -> A_L A_L %.10f, G G -> G G %.10f (diff %.2e);"
          "  A_L A_L -> h h %.10f, G G -> h h %.10f (sum %.2e)" % (E, mll, mg, mll - mg, mlh, mgh, mlh + mgh))
    rows.append(["ET_AAAA_minus_GGGG_E%g" % E, mll - mg, 0.0, mll - mg])
    rows.append(["ET_AAhh_plus_GGhh_E%g" % E, mlh + mgh, 0.0, mlh + mgh])
print("   -6 lambda = %.10f" % (-6 * LAM))

# %% [markdown]
# ## 5. Width and cross sections
#
# Gamma = (1/2)(1/(2 MH)) (beta/(8 pi)) sum|M|^2 with the explicit helicity sum.  sigma = (1/(64 pi^2 s)) (q/p)
# int dOmega <|M|^2> x (1/2 for identical final particles); <|M|^2> averages over the 9 initial helicities of A A.

# %%
k = np.array([MH, 0, 0, 0.0])
qv = math.sqrt(MH ** 2 / 4 - MA ** 2)
pa = np.array([MH / 2, 0, 0, qv]); pb = np.array([MH / 2, 0, 0, -qv])
sum_w = sum(abs(2 * EE * MA * dot(a.conj(), b.conj())) ** 2 for a, b in itertools.product(pols(pa, MA), pols(pb, MA)))
beta = math.sqrt(1 - 4 * MA ** 2 / MH ** 2)
gam = 0.5 / (2 * MH) * beta / (8 * math.pi) * sum_w
x = MA ** 2 / MH ** 2
gam_note = EE ** 2 * MH ** 3 / (32 * math.pi * MA ** 2) * beta * (1 - 4 * x + 12 * x ** 2)
print("5. Gamma(h -> A A): helicity sum %.16e, Eq. (width) %.16e, rel. diff %.1e" % (gam, gam_note, gam / gam_note - 1))
rows.append(["width_h_AA", gam, gam_note, gam / gam_note - 1])


def sigma(proc, rs):
    if proc == "AAAA":
        f, avg, mi, mf = sum_aaaa, 9.0, MA, MA
    elif proc == "AAhh":
        f, avg, mi, mf = sum_aahh, 9.0, MA, MH
    else:
        f, avg, mi, mf = sum_hhhh, 1.0, MH, MH
    s = rs * rs
    p = math.sqrt(s / 4 - mi ** 2); q = math.sqrt(s / 4 - mf ** 2)
    val, err = quad(lambda cc: f(rs, cc) / avg, -1, 1, epsabs=0, epsrel=1e-12, limit=200)
    return 0.5 * 2 * math.pi * val * q / (p * 64 * math.pi ** 2 * s) * GEV2_TO_PB


SIGMA_POINTS = [("AAAA", 6.0), ("AAAA", 20.0), ("AAhh", 6.0), ("AAhh", 20.0), ("hhhh", 6.0), ("hhhh", 20.0)]
for proc, rs in SIGMA_POINTS:
    sg = sigma(proc, rs)
    print("   sigma(%s, sqrt s = %g) = %.10e pb" % (proc, rs, sg))
    rows.append(["sigma_%s_%g_pb" % (proc, rs), sg, float("nan"), float("nan")])

# %% [markdown]
# ## 6. Points for the MadGraph standalone matrix elements
#
# MadGraph's SMATRIX is sum|M|^2 / IDEN with IDEN = (initial helicities) x (identical final particles):
# 18 for zp zp > zp zp and zp zp > h h, 2 for h h > h h.

# %%
ME_POINTS = {"AAAA": [(6.0, 0.7), (6.0, -0.3), (20.0, 0.5), (200.0, 0.2), (2000.0, 0.2)],
             "AAhh": [(6.0, 0.7), (6.0, -0.5), (20.0, 0.2), (200.0, 0.2), (2000.0, 0.2)],
             "hhhh": [(6.0, 0.7), (20.0, 0.2)]}
IDEN = {"AAAA": 18.0, "AAhh": 18.0, "hhhh": 2.0}
MASSES = {"AAAA": (MA, MA, MA, MA), "AAhh": (MA, MA, MH, MH), "hhhh": (MH, MH, MH, MH)}
fc = {(r["process"], float(r["sqrt_s"]), float(Fraction(r["cos_theta"]))): float(r["sum_M2"]) for r in ref}
with open(RES / "tree_me_points.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["process", "sqrt_s", "cos_theta", "smatrix_ours", "smatrix_exact"])
    for proc, pts in ME_POINTS.items():
        with open(WORK / ("me_points_%s.txt" % proc), "w") as pf:
            for rs, c in pts:
                ks = momenta(rs, c, *MASSES[proc])
                pf.write(" ".join("%.17e" % x for kk in ks for x in kk) + "\n")
                ours = {"AAAA": sum_aaaa, "AAhh": sum_aahh, "hhhh": sum_hhhh}[proc](rs, c) / IDEN[proc]
                exact = fc.get((proc, rs, c), float("nan")) / IDEN[proc]
                w.writerow([proc, rs, c, "%.17e" % ours, "%.17e" % exact])
print("6. points for MadGraph written to work/me_points_*.txt, values to results/tree_me_points.csv")

with open(RES / "tree_numeric.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value", "reference", "rel_diff"])
    for r in rows:
        w.writerow([r[0], "%.17e" % r[1], "%.17e" % r[2], "%.3e" % r[3]])
print("written results/tree_numeric.csv")
