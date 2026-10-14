# %% [markdown]
# # Step (6): total cross section of phi phi scattering to one loop in d = 4 (phi^3 + phi^4)
#
# Total cross section (research note models/phi34, step (6), Eq. (16)).
#
#     sigma_tot = sigma0(2->2) + sigma1(2->2) + sigma(2->3),   inputs m_p = 1, MS-bar g = lambda = 1 at mu = m.
#   sigma0 = (1/2) int dOmega |M0|^2/(64 pi^2 s) (Eq. (15)), M0 = -g^2 sum_x 1/(x - m^2) - lambda;
#   sigma1 = int dOmega M0 Re M1_phys/(64 pi^2 s) = (2 pi/(64 pi^2 s)) * 2 int_0^1 dc M0 Re M1_phys
#            (the integrand is even in c = cos(theta)); Gauss-Legendre nodes in y = ln((m^2 - t)/m^2);
#            M1_phys = M1 (MS-bar, mu = m, COLLIER, xsec_collier) + Delta M of Eq. (12),
#            Delta M = 1/(2(4pi)^2) sum_x [2 B0'/(x-m^2) - (B0 + A0)/(x-m^2)^2] + B0'/(4pi)^2  (g = lambda = 1, A0 = m^2);
#            MadLoop (work/ml_OS from run_madloop_check.sh, mu_R = m) is run at the same nodes for comparison;
#   sigma(2->3) = (1/3!) (1/(4 p sqrt(s))) int |M|^2 dPhi_3, tree level,
#            M = -g^3 sum_{15 cubic trees} 1/((P1^2 - m^2)(P2^2 - m^2)) - g lambda sum_{10 pairs} 1/((P_i + P_j)^2 - m^2);
#            adaptive (VEGAS-type) Monte Carlo over dPhi_3 = dPhi_2(P; k1, Q) dQ^2/(2 pi) dPhi_2(Q; k2, k3);
#            compared with MadGraph (work/xsec_mg5_2to3.log, sqrt(s) = 4, 5, 10).
# Writes results/xsec.csv and ../figs/xsec_d4.pdf.
# Usage (from Src/):  ~/miniforge3/envs/qft/bin/python xsec_numeric.py
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys
import re
import subprocess

import numpy as np
from scipy.integrate import quad

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
GEV2_TO_PB = 0.3893794e9
K = 16 * math.pi ** 2
B0M = 2 - math.pi / math.sqrt(3)              # B0(m^2; m, m) at mu = m
B0PM = 2 * math.pi / (3 * math.sqrt(3)) - 1   # m^2 B0'(m^2; m, m)
SQRTS_GRID = [2.05, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 15.0, 20.0]
SQRTS_ML = [2.5, 5.0, 10.0]
SQRTS_MG5 = [4.0, 5.0, 10.0]        # order of the launches in xsec_mg5_2to3.mg5
NGL = (32, 64)                      # Gauss-Legendre nodes for c in [0, 1]; the larger one is the result
TOL = 1e-10


# %% [markdown]
# ## Tree amplitude, kinematics and Gauss-Legendre nodes in y = ln((m^2 - t)/m^2)

# %%
def tree(s, t):
    u = 4 - s - t
    return -(1 / (s - 1) + 1 / (t - 1) + 1 / (u - 1)) - 1          # g = lambda = m = 1


def tu(s, c):
    p2 = s / 4 - 1
    return -2 * p2 * (1 - c), -2 * p2 * (1 + c)


def conversion(s, t, u):
    """Delta M of Eq. (12) at mu = m, g = lambda = 1 (A0 = m^2 = 1)."""
    return sum(2 * B0PM / (x - 1) - (B0M + 1) / (x - 1) ** 2 for x in (s, t, u)) / (2 * K) + B0PM / K


def gl_nodes(rs, n):
    """Nodes and weights for int_0^1 dc, through y = ln(1 - t) in [0, ln(1 + 2 p^2)] (m = 1):
    t = 1 - e^y, c = 1 + t/(2 p^2), |dc| = e^y dy/(2 p^2)."""
    p2 = rs * rs / 4 - 1
    z, w = np.polynomial.legendre.leggauss(n)
    ymax = math.log(1 + 2 * p2)
    y = ymax * (z + 1) / 2
    wy = w * ymax / 2
    t = 1 - np.exp(y)
    return 1 + t / (2 * p2), wy * np.exp(y) / (2 * p2)


def sigma0_quad(rs):
    s = rs * rs
    val, _ = quad(lambda c: tree(s, tu(s, c)[0]) ** 2, -1, 1, epsabs=0, epsrel=1e-13)
    return 0.5 * 2 * math.pi * val / (64 * math.pi ** 2 * s)


# %% [markdown]
# ## sigma^(1): M1 at the nodes from COLLIER

# %%
# ---------------- M1 at the nodes (COLLIER) ----------------
nodes = [(rs, c, w, n) for n in NGL for rs in SQRTS_GRID for c, w in zip(*gl_nodes(rs, n))]
with open(os.path.join(HERE, "work", "xsec_nodes.txt"), "w") as fh:
    fh.writelines("%.17e %.17e\n" % (rs, c) for rs, c, _, _ in nodes)
subprocess.run(["./xsec_collier", "xsec_nodes.txt", "xsec_m1_nodes.csv"], cwd=os.path.join(HERE, "work"),
               check=True, capture_output=True)
with open(os.path.join(HERE, "work", "xsec_m1_nodes.csv")) as fh:
    m1 = [float(r["re_m1"]) for r in csv.DictReader(fh)]


def sigma_2to2(rs, n, values):
    """(sigma0, sigma1) from Gauss-Legendre nodes; values[i] = Re M1 (MS-bar, mu = m) at node i."""
    s = rs * rs
    pref = 2 * math.pi / (64 * math.pi ** 2 * s) * 2
    s0 = s1 = 0.0
    for (c, w), re_m1 in zip(zip(*gl_nodes(rs, n)), values):
        t, u = tu(s, c)
        m0 = tree(s, t)
        s0 += w * m0 * m0 / 2
        s1 += w * m0 * (re_m1 + conversion(s, t, u))
    return pref * s0, pref * s1


res = {}
i = 0
for n in NGL:
    for rs in SQRTS_GRID:
        res[(rs, n)] = sigma_2to2(rs, n, m1[i:i + n])
        i += n


# %% [markdown]
# ## Inspect: the diagrams that MadLoop evaluates
#
# MadGraph draws them when it writes the standalone code (work/ml_OS; run_madloop_check.sh): born_matrix.ps
# (tree) and loop_matrix.ps (one loop; the UV counterterm diagrams are counted in the log but not drawn).
# The label QCD=n is the coupling order PHI, renamed QCD for MadLoop's loop interface (run_madloop_check.sh).
# Shown before any ./check run, only in the interactive window (needs Ghostscript, `gs`).

# %%
if INTERACTIVE:
    import shutil
    import tempfile
    from IPython.display import Image, display
    GS = shutil.which("gs") or "/opt/homebrew/bin/gs"
    for scheme in ("OS",):
        with open(os.path.join(HERE, "work", f"ml_{scheme}.log")) as fh:
            print(f"ml_{scheme}:", next(line.strip() for line in fh if "Contributing diagrams" in line))
    dML = os.path.join(HERE, "work", "ml_OS", "SubProcesses", "P0_phiphi_phiphi")
    tmpML = tempfile.mkdtemp()
    for ps in ("born_matrix.ps", "loop_matrix.ps"):
        subprocess.run([GS, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                        "-sOutputFile=" + os.path.join(tmpML, ps[:-3] + "_%02d.png"), os.path.join(dML, ps)], check=True)
        for png in sorted(f for f in os.listdir(tmpML) if f.startswith(ps[:-3] + "_")):
            display(Image(filename=os.path.join(tmpML, png)))


# %% [markdown]
# ## MadLoop at the same nodes

# %%
# ---------------- MadLoop at the same nodes ----------------
def run_madloop(rs, c):
    d = os.path.join(HERE, "work", "ml_OS", "SubProcesses", "P0_phiphi_phiphi")
    e = rs / 2
    p = math.sqrt(e * e - 1)
    st = math.sqrt(1 - c * c)
    mom = [(e, 0, 0, p), (e, 0, 0, -p), (e, p * st, 0, p * c), (e, -p * st, 0, -p * c)]
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % q for q in mom)
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("1.0\n")
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return (float(re.search(r"Matrix element born\s*=\s*(\S+)", out).group(1)),
            float(re.search(r"Matrix element finite\s*=\s*(\S+)", out).group(1)))


ml = {}
n = NGL[-1]
for rs in SQRTS_ML:
    s = rs * rs
    pref = 2 * math.pi / (64 * math.pi ** 2 * s) * 2
    vals = [run_madloop(rs, c) for c in gl_nodes(rs, n)[0]]
    w = gl_nodes(rs, n)[1]
    ml[rs] = (pref * sum(wi * b for wi, (b, _) in zip(w, vals)), pref * sum(wi * f for wi, (_, f) in zip(w, vals)))


# %% [markdown]
# ## sigma(2 -> 3): adaptive Monte Carlo (VEGAS-type) in two parametrizations

# %%
# ---------------- 2 -> 3 (adaptive Monte Carlo) ----------------
# The cross section is dominated, increasingly with s, by a narrow region where two t-channel-like
# propagators are both small (two particles close to the beam directions).  Uniform sampling of
# (Q^2, cos1, phi1, cos2, phi2) then underestimates its error; a VEGAS-type separable grid adapted
# to (f J)^2 (Lepage's algorithm, 8 adaptation + 8 final iterations) is used instead, with three
# seeds; the quoted error is the larger of the combined internal error and the spread of the seeds.
PAIRINGS = []
for e in range(5):
    rest = [k for k in range(5) if k != e]
    a = rest[0]
    for b in rest[1:]:
        PAIRINGS.append(((a, b), tuple(k for k in rest if k not in (a, b))))
PAIRS = [(a, b) for a in range(5) for b in range(a + 1, 5)]       # the 10 one-propagator diagrams
assert len(PAIRINGS) == 15 and len(PAIRS) == 10


def lam(a, b, c):
    return a * a + b * b + c * c - 2 * (a * b + b * c + c * a)


def mdot(a, b):
    return a[:, 0] * b[:, 0] - np.sum(a[:, 1:] * b[:, 1:], axis=1)


def integrand(rs, x):
    """x: (n, 5) in [0,1]^5 -> sigma-integrand times the flat Jacobian of (Q^2, cos1, phi1, cos2, phi2)."""
    s = rs * rs
    p = math.sqrt(s / 4 - 1)
    q2min, q2max = 4.0, (rs - 1) ** 2
    q2 = q2min + (q2max - q2min) * x[:, 0]
    c1, f1 = 2 * x[:, 1] - 1, 2 * np.pi * x[:, 2]
    c2, f2 = 2 * x[:, 3] - 1, 2 * np.pi * x[:, 4]
    vol = (q2max - q2min) * (4 * np.pi) ** 2
    m = len(q2)
    mq = np.sqrt(q2)
    k1m = np.sqrt(np.maximum(lam(s, 1.0, q2), 0)) / (2 * rs)
    e1 = (s + 1 - q2) / (2 * rs)
    s1 = np.sqrt(1 - c1 * c1)
    k1 = np.column_stack([e1, k1m * s1 * np.cos(f1), k1m * s1 * np.sin(f1), k1m * c1])
    qv = -k1[:, 1:]
    eq = rs - e1
    k2m = np.sqrt(np.maximum(q2 / 4 - 1, 0))
    s2 = np.sqrt(1 - c2 * c2)
    d2 = np.column_stack([s2 * np.cos(f2), s2 * np.sin(f2), c2])
    k2r = np.column_stack([mq / 2, k2m[:, None] * d2])
    k3r = np.column_stack([mq / 2, -k2m[:, None] * d2])
    beta = qv / eq[:, None]
    b2 = np.sum(beta * beta, axis=1)
    gam = eq / mq

    def boost(v):
        bp = np.sum(beta * v[:, 1:], axis=1)
        coef = np.where(b2 > 0, (gam - 1) * bp / np.where(b2 > 0, b2, 1), 0) + gam * v[:, 0]
        return np.column_stack([gam * (v[:, 0] + bp), v[:, 1:] + coef[:, None] * beta])

    p1 = np.array([rs / 2, 0, 0, p])
    p2 = np.array([rs / 2, 0, 0, -p])
    q = [np.broadcast_to(-p1, (m, 4)), np.broadcast_to(-p2, (m, 4)), k1, boost(k2r), boost(k3r)]
    amp = np.zeros(m)
    for (a, b), (c, d) in PAIRINGS:
        pa, pc = q[a] + q[b], q[c] + q[d]
        amp += 1 / ((mdot(pa, pa) - 1) * (mdot(pc, pc) - 1))
    for a, b in PAIRS:                                  # one cubic and one quartic vertex (lambda/g = 1)
        pa = q[a] + q[b]
        amp += 1 / (mdot(pa, pa) - 1)
    f = amp ** 2 / (2 * np.pi) * (k1m / (16 * np.pi ** 2 * rs)) * (k2m / (16 * np.pi ** 2 * mq))
    return f * vol / (6 * 4 * p * rs)


def vegas(func, dim, nbins=64, n_adapt=8, n_final=8, neval=400_000, alpha=1.5, seed=1):
    rng = np.random.default_rng(seed)
    edges = np.tile(np.linspace(0, 1, nbins + 1), (dim, 1))
    results = []
    for it in range(n_adapt + n_final):
        y = rng.uniform(0, 1, (neval, dim))
        ib = np.minimum((y * nbins).astype(int), nbins - 1)
        frac = y * nbins - ib
        lo = np.take_along_axis(edges, ib.T, axis=1).T
        hi = np.take_along_axis(edges, ib.T + 1, axis=1).T
        x = lo + (hi - lo) * frac
        jac = np.prod((hi - lo) * nbins, axis=1)
        fj = func(x) * jac
        mean = fj.mean()
        var = fj.var() / neval
        if it >= n_adapt:
            results.append((mean, var))
        # adapt each dimension's grid with the binned sum of (f J)^2
        if it < n_adapt + n_final - 1:
            for d in range(dim):
                w = np.bincount(ib[:, d], weights=fj * fj, minlength=nbins)
                w = np.convolve(np.concatenate([[w[0]], w, [w[-1]]]), [1, 1, 1], "valid") / 3   # smoothing
                w = w / w.sum()
                w = np.where(w > 0, ((w - 1) / np.log(np.where(w > 0, w, 1))) ** alpha, 0)     # damping
                cw = np.concatenate([[0], np.cumsum(w)])
                cw /= cw[-1]
                edges[d] = np.interp(np.linspace(0, 1, nbins + 1), cw, edges[d])
    wts = np.array([1 / v for _, v in results])
    vals = np.array([m for m, _ in results])
    mean = (wts * vals).sum() / wts.sum()
    err = 1 / math.sqrt(wts.sum())
    chi2 = ((vals - mean) ** 2 * wts).sum() / max(len(vals) - 1, 1)
    return mean, err, chi2



# Cross-check with an independent parametrization of the same phase space:
# dPhi_3 = (2 pi)^-5 d^3k1/(2E1) d^3k2/(2E2) /(2E3) delta(sqrt(s) - E1 - E2 - E3), k3 = -k1 - k2, with the
# delta function solved for |k2| along the sampled direction of k2 (0, 1 or 2 roots of a quadratic).
def integrand_b(rs, x):
    s = rs * rs
    p = math.sqrt(s / 4 - 1)
    k1max = math.sqrt(lam(s, 1.0, 4.0)) / (2 * rs)
    k1 = k1max * x[:, 0]
    c1, f1 = 2 * x[:, 1] - 1, 2 * np.pi * x[:, 2]
    c2, f2 = 2 * x[:, 3] - 1, 2 * np.pi * x[:, 4]
    vol = k1max * (4 * np.pi) ** 2
    s1, s2 = np.sqrt(1 - c1 ** 2), np.sqrt(1 - c2 ** 2)
    k1v = k1[:, None] * np.column_stack([s1 * np.cos(f1), s1 * np.sin(f1), c1])
    n2 = np.column_stack([s2 * np.cos(f2), s2 * np.sin(f2), c2])
    e1 = np.sqrt(k1 ** 2 + 1)
    A = rs - e1
    b = np.sum(k1v * n2, axis=1)
    C = A * A - k1 ** 2
    qa, qb, qc = 4 * (A * A - b * b), 4 * C * b, 4 * A * A - C * C
    disc = qb * qb - 4 * qa * qc
    m = len(k1)
    total = np.zeros(m)
    p1 = np.array([rs / 2, 0, 0, p]); p2 = np.array([rs / 2, 0, 0, -p])
    for sign in (+1, -1):
        xr = (-qb + sign * np.sqrt(np.maximum(disc, 0))) / (2 * qa)
        e2 = np.sqrt(xr ** 2 + 1)
        k3v = -k1v - xr[:, None] * n2
        e3 = np.sqrt(np.sum(k3v ** 2, axis=1) + 1)
        ok = (disc >= 0) & (xr >= 0) & (np.abs(e1 + e2 + e3 - rs) < 1e-9 * rs)
        dfdx = xr / e2 + (xr + b) / e3
        k1q = np.column_stack([e1, k1v]); k2q = np.column_stack([e2, xr[:, None] * n2]); k3q = np.column_stack([e3, k3v])
        q = [np.broadcast_to(-p1, (m, 4)), np.broadcast_to(-p2, (m, 4)), k1q, k2q, k3q]
        amp = np.zeros(m)
        for (a, bb), (c, d) in PAIRINGS:
            pa, pc = q[a] + q[bb], q[c] + q[d]
            amp += 1 / ((mdot(pa, pa) - 1) * (mdot(pc, pc) - 1))
        for a, bb in PAIRS:
            pa = q[a] + q[bb]
            amp += 1 / (mdot(pa, pa) - 1)
        # (2 pi)^-5 * k1^2 dk1 dOmega1/(2 E1) * x^2 dOmega2/(2 E2) /(2 E3) / |df/dx|
        w = (2 * np.pi) ** -5 * k1 ** 2 / (2 * e1) * xr ** 2 / (2 * e2) / (2 * e3) / np.abs(dfdx)
        total += np.where(ok, amp ** 2 * w, 0)
    return total * vol / (6 * 4 * p * rs)


def sigma_2to3(rs, seeds=(1, 2, 3)):
    if rs <= 3:
        return 0.0, 0.0, 0.0
    runs = [vegas(lambda x: integrand(rs, x), 5, seed=sd) for sd in seeds]
    w = np.array([1 / r[1] ** 2 for r in runs])
    vals = np.array([r[0] for r in runs])
    mean = (w * vals).sum() / w.sum()
    err = max(1 / math.sqrt(w.sum()), vals.std(ddof=1) / math.sqrt(len(vals)))
    return mean, err, max(r[2] for r in runs)


mg5_all = []
logf = os.path.join(HERE, "work", "xsec_mg5_2to3.log")
if os.path.exists(logf):
    for a, b in re.findall(r"Cross-section\s*:\s*(\S+)\s*\+-\s*(\S+)\s*pb", open(logf).read()):
        mg5_all.append((float(a) / GEV2_TO_PB, float(b) / GEV2_TO_PB))
mg5_23 = mg5_all[:3]                # sqrt(s) = 4, 5, 10 with 10000 events
mg5_10 = mg5_all[3:]                # sqrt(s) = 10 again (iseed 777, 4242, 31 with sde_strategy 2, 32 with hard_survey 2)


# %% [markdown]
# ## Results

# %%
# ---------------- output ----------------
rows = []
print(f"{'sqrt(s)':>7} {'sigma0':>14} {'sigma1':>14} {'s1/s0':>9} {'n=32 vs 64':>10} {'sigma(2->3)':>22} {'s23/s0':>9}")
mc = {}
for rs in SQRTS_GRID:
    s0q = sigma0_quad(rs)
    s0, s1 = res[(rs, NGL[-1])]
    s1lo = res[(rs, NGL[0])][1]
    assert abs(s0 - s0q) / s0q < 1e-12, (rs, s0, s0q)
    mc[rs] = sigma_2to3(rs)
    print(f"{rs:7.1f} {s0:14.7e} {s1:14.7e} {s1 / s0:9.2e} {abs(s1lo - s1) / abs(s1):10.1e} "
          f"{mc[rs][0]:12.5e}+-{mc[rs][1]:8.1e} {mc[rs][0] / s0:9.2e}  (max chi2/dof {mc[rs][2]:.2f})")
    rows.append([rs, s0, s1, abs(s1lo - s1) / abs(s1), mc[rs][0], mc[rs][1], s0 + s1 + mc[rs][0]])

print("\nMadLoop at the same nodes (n = %d):" % NGL[-1])
for rs in SQRTS_ML:
    s0, s1 = res[(rs, NGL[-1])]
    d0, d1 = abs(ml[rs][0] - s0) / s0, abs(ml[rs][1] - s1) / abs(s1)
    print(f"  sqrt(s) = {rs:5.1f}: sigma0 {ml[rs][0]:.12e} (rel. dev. {d0:.1e}), sigma1 {ml[rs][1]:.12e} (rel. dev. {d1:.1e})"
          + ("" if d0 < TOL and d1 < TOL else "   <- disagrees"))
print("\n2 -> 3: adaptive MC (parametrization A), independent parametrization B, MadGraph:")
mcb = {}
for rs in SQRTS_MG5:
    runs = [vegas(lambda x: integrand_b(rs, x), 5, seed=sd) for sd in (1, 2, 3)]
    w = np.array([1 / r[1] ** 2 for r in runs])
    vals = np.array([r[0] for r in runs])
    mcb[rs] = ((w * vals).sum() / w.sum(), max(1 / math.sqrt(w.sum()), vals.std(ddof=1) / math.sqrt(3)))
for rs, (v, e) in zip(SQRTS_MG5, mg5_23):
    (a_, ea), (b_, eb) = mc[rs][:2], mcb[rs]
    print(f"  sqrt(s) = {rs:5.1f}: A {a_:.5e} +- {ea:.1e}, B {b_:.5e} +- {eb:.1e} ((A-B)/err {(a_ - b_) / math.hypot(ea, eb):+.2f}), "
          f"MG5 {v:.5e} +- {e:.1e} ((MG5-A)/err {(v - a_) / math.hypot(e, ea):+.2f})")
if mg5_10:
    allv = [mg5_23[2]] + mg5_10
    vals = np.array([v for v, _ in allv])
    print(f"  sqrt(s) = 10: MadGraph runs (pb) " + ", ".join(f"{v * GEV2_TO_PB:.3f}+-{e * GEV2_TO_PB:.3f}" for v, e in allv)
          + f";  mean {vals.mean() * GEV2_TO_PB:.3f}, spread (std) {vals.std(ddof=1) * GEV2_TO_PB:.3f};  "
          f"A {mc[10.0][0] * GEV2_TO_PB:.3f}+-{mc[10.0][1] * GEV2_TO_PB:.3f}, B {mcb[10.0][0] * GEV2_TO_PB:.3f}+-{mcb[10.0][1] * GEV2_TO_PB:.3f} pb")

with open(os.path.join(HERE, "results", "xsec.csv"), "w", newline="") as fh:
    wtr = csv.writer(fh)
    wtr.writerow(["sqrts", "sigma0", "sigma1", "sigma1_rel_change_n32", "sigma23_mc", "sigma23_mc_err", "sigma_tot",
                  "sigma0_madloop", "sigma1_madloop", "sigma23_mcB", "sigma23_mcB_err", "sigma23_mg5", "sigma23_mg5_err"])
    for r in rows:
        rs = r[0]
        mlv = ml.get(rs, ("", ""))
        mbv = mcb.get(rs, ("", ""))
        mgv = dict(zip(SQRTS_MG5, mg5_23)).get(rs, ("", ""))
        wtr.writerow(r + list(mlv) + list(mbv) + list(mgv))

# ---------------- figure ----------------

# %% [markdown]
# ## Figure

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
x = np.array(SQRTS_GRID)
s0 = np.array([r[1] for r in rows])
s1 = np.array([r[2] for r in rows])
s23 = np.array([r[4] for r in rows])
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 3.8), sharex=True)
ax1.plot(x, s0, color="k", lw=0.9, label=r"$\sigma^{(0)}_{2\to2}$")
ax1.plot(x, np.abs(s1), color="#5d81b4", lw=0.9, ls="--", label=r"$|\sigma^{(1)}_{2\to2}|$")
ax1.plot(x[x > 3], s23[x > 3], color="#eb6235", lw=0.9, ls="-.", label=r"$\sigma_{2\to3}$")
ax1.plot(SQRTS_ML, [ml[r][1] for r in SQRTS_ML], "x", ms=4, color="#5d81b4", label="MadLoop")
if mg5_23:
    ax1.errorbar(SQRTS_MG5[:len(mg5_23)], [v for v, _ in mg5_23], yerr=[e for _, e in mg5_23], fmt="o", ms=3.5,
                 mfc="none", color="#eb6235", label="MadGraph")
ax1.set_yscale("log")
ax1.set_ylim(1e-7, 1.0)
ax1.set_ylabel(r"$\sigma\ [m^{-2}]$")
ax1.legend(loc="upper right", ncol=2)
ax2.plot(x, s1 / s0, color="#5d81b4", lw=0.9, ls="--", label=r"$\sigma^{(1)}_{2\to2}/\sigma^{(0)}_{2\to2}$")
ax2.plot(x[x > 3], (s23 / s0)[x > 3], color="#eb6235", lw=0.9, ls="-.", label=r"$\sigma_{2\to3}/\sigma^{(0)}_{2\to2}$")
ax2.axhline(0, color="0.6", lw=0.5)
ax2.set_xlabel(r"$\sqrt{s}/m$")
ax2.set_ylabel("ratio")
ax2.legend(loc="lower right")
ax2.set_ylim(-0.2, 0.15)
fig.savefig(os.path.join(HERE, "..", "figs", "xsec_d4.pdf"))
print("\nwrote results/xsec.csv and figs/xsec_d4.pdf")
