# %% [markdown]
# # Step (8): perturbative unitarity of phi phi -> phi phi in phi^3 + phi^4: bounds in (g/m, lambda) = (kappa_3, kappa_4)
#
# Partial waves of the identical-particle amplitude (note, Eq. (18) (eq:pw), App. K; the normalization of the phi^3 note):
#   a_l(s) = beta/(64 pi) int_{-1}^{1} dc P_l(c) M(s, c),   beta = sqrt(1 - 4 m^2/s),   Im a_l = |a_l|^2 (elastic),
# hence |Re a_l| <= 1/2.  Only even l occur (t <-> u).  At tree level (m = 1)
#   a_0^(0) = beta/(32 pi) [g^2 F(s) - lambda],   F(s) = -1/(s - 1) + 2 ln(s - 3)/(s - 4).
# At one loop the S-matrix element M_phys of Eq. (12) (pole mass m, MS-bar g and lambda at mu = m) is projected.  It is split
# into coupling structures, M_phys - M0 = g^4 P + g^2 lambda Q + lambda^2 R, with P, Q, R from COLLIER (pw_collier.f90, the
# MS-bar M1 at mu = m) plus the conversion terms of Eq. (12):
#   P += sum_x [B0'/(x - 1) - B0/(2 (x - 1)^2)]/(4pi)^2,   Q += -sum_x A0/(2 (x - 1)^2)/(4pi)^2 + B0'/(4pi)^2,   R += 0.
# Checks: the quadrature against the closed form of a_0^(0); the projected unitarity relation for each structure,
#   Im p_0 = f_0^2,  Im q_0 = -2 f_0 e_0,  Im r_0 = e_0^2   (a_0^(0) = g^2 f_0 - lambda e_0),   and Im q_2 = Im r_2 = 0;
# the step (4) amplitude at sqrt(s) = 5, cos = 0.3; lambda = 0 reproduces the phi^3 bounds (phi3/Src/results/pw4.csv).
# Bounds in the (g/m, lambda) plane:
#   (A) tree unitarity       |Re a_0^(0)(s)| <= 1/2 for all s (closed form: lambda < 16 pi, g^2 <= min_s (16 pi/beta + lambda)/F);
#   (B) high-energy perturbativity of lambda: for s >> m^2 with mu = sqrt(s), Re a_0 = -lambda (1 - 4 lambda/(4pi)^2)/(32 pi)
#       (App. K), so the one-loop term equals the tree at lambda(sqrt(s)) = 4 pi^2; with the running from mu = m up to E,
#       lambda(m) <= 4 pi^2/(1 + (3/4) ln(E/m)).  Checked against the projected lambda^2 structure at the top of the grid.
#   (C) one-loop unitarity   |Re a_0^(0) + Re a_0^(1)| <= 1/2 near threshold (sqrt(s) <= 4m, where the g bound is set), with
#       mu = m; the band from mu = m/2 and 2m (couplings run from mu = m with the one-loop solution, App. J;
#       a_0^(1)(mu) = a_0^(1)(m) + ln(mu/m) (-6 g^2 lambda f_0 + 3 lambda^2 e_0)/(4pi)^2 from the mu-dependence of Eq. (12)).
#       At higher energies the lambda^2 ln(s/m^2) terms of the fixed-order a_0^(1) grow, and the lambda direction is (B).
#   Perturbativity at the energy s* where |Re a_0^(0)| is largest: the ratio |Re a_0^(1)(s*)/Re a_0^(0)(s*)| on the (A) boundary.
# Higgs: m = m_h, g = kappa_3 3 m_h^2/v, lambda = kappa_4 3 m_h^2/v^2 (Eq. (14) (eq:kappa)).
#
# Writes results/pw.csv and ../figs/pw_d4.pdf (the same layout as the phi^3 note's pw4_d4.pdf).
# Batch: `~/miniforge3/envs/qft/bin/python pw_numeric.py` (from Src/; run_pw_check.sh builds work/pw_collier).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import subprocess
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import eval_legendre

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K = (4 * math.pi) ** 2
B0M = 2 - math.pi / math.sqrt(3)                 # B0(m^2) at mu = m
B0PM = 2 * math.pi / (3 * math.sqrt(3)) - 1       # m^2 B0'(m^2)
A0M = 1.0                                         # A0(m^2) at mu = m
NGL = 64
MH, VEV = 125.25, 246.22                          # GeV
G_SM, L_SM = 3 * MH / VEV, 3 * MH ** 2 / VEV ** 2  # g/m and lambda of the SM Higgs (kappa_3 = kappa_4 = 1)


def bigF(s):
    return -1 / (s - 1) + 2 * math.log(s - 3) / (s - 4)


def kin(s, c):
    p2 = s / 4 - 1
    return s, -2 * p2 * (1 - c), -2 * p2 * (1 + c)


def tree_t(s, c):                                 # M0 = g^2 T - lambda
    return -sum(1 / (x - 1) for x in kin(s, c))


def conv(s, c):                                   # conversion terms of Eq. (12), split into (P, Q, R)
    xs = kin(s, c)
    cp = sum(B0PM / (x - 1) - B0M / (2 * (x - 1) ** 2) for x in xs) / K
    cq = (-sum(A0M / (2 * (x - 1) ** 2) for x in xs) + B0PM) / K
    return cp, cq, 0.0


# %% [markdown]
# ## Quadrature nodes and the one-loop structures from COLLIER
# As in the phi^3 note: int_{-1}^{1} = 2 int_0^1 for even l, and y = ln((m^2 - t)/m^2) flattens the t-channel peak.

# %%
RS = np.unique(np.concatenate([2 * np.sqrt(1 + np.geomspace(0.01, 10.0, 80) ** 2), np.linspace(2.2, 3.0, 17)]))


def nodes(rs):
    p2 = rs * rs / 4 - 1
    x, w = np.polynomial.legendre.leggauss(NGL)
    ymax = math.log(1 + 2 * p2)
    y = 0.5 * ymax * (x + 1)
    c = 1 - (np.exp(y) - 1) / (2 * p2)
    return c, 0.5 * ymax * w * np.exp(y) / (2 * p2)


work = os.path.join(HERE, "work")
exe = os.path.join(work, "pw_collier")
if not os.path.exists(exe):
    subprocess.run(["gfortran", "-I" + os.path.expanduser("~/hep/include"), "pw_collier.f90",
                    "-L" + os.path.expanduser("~/hep/lib"), "-lcollier", "-o", exe], cwd=HERE, check=True)
with open(os.path.join(work, "pw_nodes.txt"), "w") as fh:
    for rs in RS:
        for c in nodes(rs)[0]:
            fh.write(f"{rs:.17e} {c:.17e}\n")
    fh.write(f"{5.0:.17e} {0.3:.17e}\n")              # step (4) point, as a regression check
subprocess.run([exe, "pw_nodes.txt", "pw_structures.csv"], cwd=work, check=True, capture_output=True)
st = {}
with open(os.path.join(work, "pw_structures.csv")) as fh:
    for r in csv.DictReader(fh):
        st[(float(r["sqrts"]), float(r["costheta"]))] = tuple(complex(float(r["re_" + k]), float(r["im_" + k])) for k in "pqr")
reg = sum(st[(5.0, 0.3)])
print(f"regression: M1(sqrt(s) = 5, cos = 0.3) = {reg.real:.15e} + {reg.imag:.15e} i   (step (4): -1.578556592309178e-02 + 5.014307850308829e-03 i)")
assert abs(reg - (-1.578556592309178e-02 + 5.014307850308829e-03j)) < 1e-15


# %% [markdown]
# ## Partial waves: tree (f_0, e_0) and one-loop structures (p_l, q_l, r_l); projected unitarity

# %%
rows = []
for rs in RS:
    s = rs * rs
    beta = math.sqrt(1 - 4 / s)
    c, w = nodes(rs)
    tt = np.array([tree_t(s, ci) for ci in c])
    ss = np.array([st[(float(f"{rs:.17e}"), float(f"{ci:.17e}"))] for ci in c])
    cv = np.array([conv(s, ci) for ci in c])
    row = dict(rs=rs, beta=beta)
    for l in (0, 2):
        pl = eval_legendre(l, c)
        proj = lambda f: beta / (64 * math.pi) * 2 * np.sum(w * pl * f)
        row[f"f{l}"] = proj(tt)
        row[f"e{l}"] = proj(np.ones_like(tt))
        for j, k in enumerate("pqr"):
            row[f"{k}{l}"] = proj(ss[:, j] + cv[:, j])
    rows.append(row)
R = {k: np.array([r[k] for r in rows]) for k in rows[0]}
fcl = R["beta"] / (32 * math.pi) * np.array([bigF(rs * rs) for rs in RS])
print(f"f_0: quadrature vs closed form, largest relative deviation {max(abs(R['f0'] / fcl - 1)):.1e};  "
      f"e_0 vs beta/(32 pi) {max(abs(R['e0'] / (R['beta'] / (32 * math.pi)) - 1)):.1e}")
uni = {"p0": max(abs(R["p0"].imag / R["f0"] ** 2 - 1)),
       "q0": max(abs(R["q0"].imag / (-2 * R["f0"] * R["e0"]) - 1)),
       "r0": max(abs(R["r0"].imag / R["e0"] ** 2 - 1))}
far = R["rs"] > 2.25                               # a_2 ~ beta^5 is tiny closer to threshold
uni["p2"] = max(abs(R["p2"].imag[far] / R["f2"][far] ** 2 - 1))
uni["q2, r2 (abs / f_2^2)"] = max(max(abs(R["q2"].imag[far]) / R["f2"][far] ** 2), max(abs(R["r2"].imag[far]) / R["f2"][far] ** 2))
print("projected unitarity, largest relative deviation: " + ",  ".join(f"{k} {v:.1e}" for k, v in uni.items()))
print(f"F(s) > 0 on the grid: {bool(np.all(fcl > 0))};  max_s beta F/(32 pi) = {fcl.max():.6e} at sqrt(s) = {RS[np.argmax(fcl)]:.3f}")


# %% [markdown]
# ## The lambda^2 structure from the closed form of B0, and its high-energy limit (B)
# R = sum_x B0(x)/(2 (4pi)^2) involves B0 only; B0(x) = 2 - beta_x ln((beta_x + 1)/(beta_x - 1)) with beta_x = sqrt(1 - 4/x)
# (m = mu = 1, x - i0).  For s >> m^2 the projection is (8 - 3 ln(s/mu^2) + i pi)/(2 (4pi)^2), i.e. 4/(4pi)^2 at mu = sqrt(s).

# %%
def b0_closed(x):
    bx = np.sqrt(complex(1 - 4 / x))
    return 2 - bx * np.log((bx + 1) / (bx - 1) + 0j) if x < 0 or x > 4 else 2 - 2 * math.sqrt(4 / x - 1) * math.atan(1 / math.sqrt(4 / x - 1))


def b0_cut(x):                                    # x > 4: the -i0 prescription gives + i pi beta
    bx = math.sqrt(1 - 4 / x)
    return 2 - bx * math.log((1 + bx) / (1 - bx)) + 1j * math.pi * bx


dr = 0.0
for k, rs in enumerate(RS):
    s = rs * rs
    c, w = nodes(rs)
    vals = []
    for ci in c:
        _, t, u = kin(s, ci)
        vals.append((b0_cut(s) + b0_closed(t) + b0_closed(u)) / (2 * K))
    r0c = R["beta"][k] / (64 * math.pi) * 2 * np.sum(w * np.array(vals))
    dr = max(dr, abs(r0c / R["r0"][k] - 1))
print(f"r_0 (lambda^2 structure): COLLIER vs the closed form of B0, largest relative deviation {dr:.1e}")
lnmu_top = 0.5 * math.log(RS[-1] ** 2)
r_top = (R["r0"][-1].real + lnmu_top * 3 * R["e0"][-1] / K) / R["e0"][-1]
print(f"(B) at sqrt(s) = {RS[-1]:.2f} m with mu = sqrt(s): Re r_0/e_0 = {r_top:.5f}  (s -> infinity: 4/(4pi)^2 = {4 / K:.5f})")
LAM_B = 4 * math.pi ** 2
lam_one = (1 + math.sqrt(1 + 64 * math.pi / K)) * K / 8           # |Re a_0| = 1/2 at one loop with mu = sqrt(s)
print(f"(B) lambda(sqrt(s)) <= 4 pi^2 = {LAM_B:.4f} (kappa_4 <= {LAM_B / L_SM:.2f});  one-loop |Re a_0| reaches 1/2 only at "
      f"lambda = {lam_one:.2f};  max over lambda of |Re a_0| below 4 pi^2: {K / 16 / (32 * math.pi):.4f} at lambda = (4pi)^2/8")
for E in (10.0, 100.0):
    print(f"    perturbative up to E = {E:5.0f} m: lambda(m) <= {LAM_B / (1 + 0.75 * math.log(E)):.3f} "
          f"(kappa_4 <= {LAM_B / (1 + 0.75 * math.log(E)) / L_SM:.2f});  tree unitarity up to E: lambda(m) <= "
          f"{16 * math.pi / (1 + 3 / math.pi * math.log(E)):.3f}")


# %% [markdown]
# ## (A) tree unitarity: closed form of the allowed region

# %%
def gA2(lam):
    """g^2 bound of (A) at given lambda: min over s of (16 pi/beta + lambda)/F(s) (m = 1)."""
    f = lambda lp: (16 * math.pi / math.sqrt(1 - 4 / (4 + 4 * math.exp(2 * lp))) + lam) / bigF(4 + 4 * math.exp(2 * lp))
    grid = np.linspace(math.log(1e-3), math.log(1e3), 2001)
    i = int(np.argmin([f(x) for x in grid]))
    res = minimize_scalar(f, bounds=(grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]), method="bounded",
                          options={"xatol": 1e-12})
    return res.fun, 2 * math.sqrt(1 + math.exp(2 * res.x))     # (g^2 bound, sqrt(s)/m where it bites)


LAM_A = 16 * math.pi
for lam in (0.0, L_SM, 10.0, 30.0, LAM_A * 0.999):
    g2, rsA = gA2(lam)
    print(f"(A) lambda = {lam:8.4f}: g/m <= {math.sqrt(g2):.4f} (sqrt(s) = {rsA:.3f} m);  kappa_3 <= {math.sqrt(g2) / G_SM:.3f}")
print(f"(A) lambda <= 16 pi = {LAM_A:.4f}  (s -> infinity);  kappa_4 <= {LAM_A / L_SM:.2f}")


# %% [markdown]
# ## (C) one-loop unitarity, with the mu band

# %%
def run_couplings(g, lam, lnmu):
    """One-loop running from mu = m (App. J): lambda(mu) = lambda/(1 - 3 lambda ln(mu/m)/(4pi)^2), g/lambda fixed."""
    if lam == 0:
        return g, 0.0
    lmu = lam / (1 - 3 * lam * lnmu / K)
    return g * lmu / lam, lmu


THR = RS <= 4.0 + 1e-12                           # the threshold region of (C)


def re_a0(g, lam, lnmu=0.0, sel=THR):
    """Re a_0 at one loop on the s grid (sel) for couplings (g, lambda) defined at mu = m, evaluated at the scale mu."""
    gm, lm = run_couplings(g, lam, lnmu)
    a = gm ** 2 * R["f0"][sel] - lm * R["e0"][sel]
    a1 = (gm ** 4 * R["p0"][sel] + gm ** 2 * lm * R["q0"][sel] + lm ** 2 * R["r0"][sel]).real
    a1 = a1 + lnmu * (-6 * gm ** 2 * lm * R["f0"][sel] + 3 * lm ** 2 * R["e0"][sel]) / K
    return a, a1


def violation(g, lam, lnmu=0.0):
    a, a1 = re_a0(g, lam, lnmu)
    return np.max(np.abs(a + a1)) - 0.5


def g_bound(lam, lnmu=0.0, gmax=40.0):
    """Smallest g > 0 where (C) is violated at fixed lambda (scan, then bisection); nan if lambda alone violates it."""
    if violation(0.0, lam, lnmu) > 0:
        return float("nan")
    gs = np.linspace(0, gmax, 801)
    v = [violation(g, lam, lnmu) for g in gs]
    i = next(k for k in range(len(gs)) if v[k] > 0)
    return brentq(lambda g: violation(g, lam, lnmu), gs[i - 1], gs[i], xtol=1e-12)


LN2 = math.log(2)
bC = {}
for name, lnmu in (("mu=m", 0.0), ("mu=m/2", -LN2), ("mu=2m", LN2)):
    bC[name] = dict(g0=g_bound(0.0, lnmu), gSM=g_bound(L_SM, lnmu), g20=g_bound(20.0, lnmu), gB=g_bound(LAM_B, lnmu))
    print(f"(C) {name:7}: g/m <= {bC[name]['g0']:.4f} (lambda = 0), {bC[name]['gSM']:.4f} (kappa_4 = 1), "
          f"{bC[name]['g20']:.4f} (lambda = 20), {bC[name]['gB']:.4f} (lambda = 4 pi^2)")
for lam in (0.0, 20.0, LAM_B):
    g = bC["mu=m"]["g0" if lam == 0 else ("g20" if lam == 20.0 else "gB")]
    a, a1 = re_a0(g, lam)
    i = int(np.argmax(np.abs(a + a1)))
    print(f"    lambda = {lam:6.3f}: the bound is set at sqrt(s) = {RS[THR][i]:.3f} m, Re a_0^(0) = {a[i]:+.4f}, Re a_0^(1) = {a1[i]:+.4f}")
lam_only = brentq(lambda l: violation(0.0, l), 1.0, 200.0)
print(f"(C) with lambda alone in the threshold region: violated only at lambda = {lam_only:.2f}")


# %% [markdown]
# ## lambda = 0 reproduces the phi^3 bounds

# %%
phi3 = {}
with open(os.path.join(HERE, "..", "..", "phi3", "Src", "results", "pw4.csv")) as fh:
    for r in csv.reader(fh):
        if r and r[0].startswith("("):
            phi3[r[0][:3]] = float(r[1])
gA_grid = math.sqrt(0.5 / R["f0"].max())
print(f"lambda = 0: (A) on the grid {gA_grid:.10f} vs phi^3 {phi3['(A)']:.10f};  (C) {bC['mu=m']['g0']:.10f} vs phi^3 {phi3['(C)']:.10f}")
assert abs(gA_grid / phi3["(A)"] - 1) < 1e-12 and abs(bC["mu=m"]["g0"] / phi3["(C)"] - 1) < 1e-9


# %% [markdown]
# ## Boundaries in the plane, and perturbativity on the (A) boundary

# %%
lams = np.linspace(0, 60, 241)
curveA = np.array([math.sqrt(gA2(l)[0]) if l < LAM_A else np.nan for l in lams])
curveC = {name: np.array([g_bound(l, lnmu) if l <= LAM_B + 1e-9 else np.nan for l in lams])
          for name, lnmu in (("mu=m", 0.0), ("mu=m/2", -LN2), ("mu=2m", LN2))}
ratio_A = []
for l, g in zip(lams, curveA):
    if np.isnan(g):
        ratio_A.append(np.nan)
        continue
    a, a1 = re_a0(g, l)
    i = int(np.argmax(np.abs(a)))
    ratio_A.append(abs(a1[i] / a[i]) if l <= LAM_B else np.nan)
ratio_A = np.array(ratio_A)
print(f"on the (A) boundary (lambda <= 4 pi^2, sqrt(s) <= 4m): |Re a_0^(1)/Re a_0^(0)| at the s of the largest |Re a_0^(0)| ranges "
      f"{np.nanmin(ratio_A):.2f} ... {np.nanmax(ratio_A):.2f}")
gmaxC = np.nanmax(curveC["mu=m"])
print(f"(C) largest g/m on the boundary {gmaxC:.3f} at lambda = {lams[np.nanargmax(curveC['mu=m'])]:.2f}")


# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "pw.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["sqrts", "beta", "f0", "e0", "re_p0", "im_p0", "re_q0", "im_q0", "re_r0", "im_r0", "f2", "re_p2", "im_p2"])
    for r in rows:
        wr.writerow([r["rs"], r["beta"], r["f0"], r["e0"], r["p0"].real, r["p0"].imag, r["q0"].real, r["q0"].imag,
                     r["r0"].real, r["r0"].imag, r["f2"], r["p2"].real, r["p2"].imag])
    wr.writerow([])
    wr.writerow(["lambda", "g_over_m_A", "g_over_m_C_mu_m", "g_over_m_C_mu_m/2", "g_over_m_C_mu_2m", "ratio_on_A"])
    for k, l in enumerate(lams):
        wr.writerow([l, curveA[k], curveC["mu=m"][k], curveC["mu=m/2"][k], curveC["mu=2m"][k], ratio_A[k]])
    wr.writerow([])
    wr.writerow(["bound", "mu=m", "mu=m/2", "mu=2m"])
    for key in ("g0", "gSM", "g20", "gB"):
        wr.writerow([key, *(bC[n][key] for n in ("mu=m", "mu=m/2", "mu=2m"))])


# %% [markdown]
# ## Figure: the allowed region in (g/m, lambda) and the projected unitarity relation

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 5.0), gridspec_kw={"height_ratios": [1.7, 1]})
gg = np.linspace(0, 16, 200)
for alpha in (1.0, 9 / 8):                      # alpha = 3 lambda m^2/g^2 = 1, 9/8, inside lambda < 16 pi
    la = alpha * gg ** 2 / 3
    ax1.plot(gg[la <= LAM_A], la[la <= LAM_A], color="0.6", lw=0.6, ls=":")
okC = lams <= LAM_B / (1 + 0.75 * LN2) + 1e-9      # the band only while lambda(2m) <= 4 pi^2, i.e. (B) at mu = 2m
ax1.fill_betweenx(lams[okC], np.fmin(curveC["mu=m/2"], curveC["mu=2m"])[okC], np.fmax(curveC["mu=m/2"], curveC["mu=2m"])[okC],
                  color="#e09b24", alpha=0.3, lw=0)
ax1.plot(curveA, lams, color="k", lw=0.9, ls="-", label="(A) tree")
ax1.plot([0, math.sqrt(gA2(LAM_A * 0.9999)[0])], [LAM_A, LAM_A], color="k", lw=0.9, ls="-")
lam10 = LAM_B / (1 + 0.75 * math.log(10))
ax1.plot([0, math.sqrt(gA2(LAM_B)[0])], [LAM_B, LAM_B], color="#5d81b4", lw=0.9, ls="--",
         label=r"(B) $\lambda(\sqrt{s})\leq4\pi^2$")
ax1.plot([0, math.sqrt(gA2(lam10)[0])], [lam10, lam10], color="#5d81b4", lw=0.6, ls=(0, (1, 1.5)),
         label=r"(B) up to $\sqrt{s}=10m$")
ax1.plot(curveC["mu=m"], lams, color="#e09b24", lw=0.9, ls="-.", label=r"(C) one loop, $\mu=m$")
ax1.plot([G_SM], [L_SM], "o", ms=3.5, color="#eb6235", zorder=6)
ax1.set_xlim(0, 16)
ax1.set_ylim(0, 72)
ax1.set_xlabel(r"$g/m$")
ax1.set_ylabel(r"$\lambda$")
ax1.legend(loc="upper left", fontsize=6, ncol=2, columnspacing=1.0, handlelength=2.2)
top = ax1.secondary_xaxis("top", functions=(lambda x: x / G_SM, lambda k: k * G_SM))
top.set_xlabel(r"$\kappa_3$")
right = ax1.secondary_yaxis("right", functions=(lambda y: y / L_SM, lambda k: k * L_SM))
right.set_ylabel(r"$\kappa_4$")
pm = np.sqrt(RS ** 2 / 4 - 1)
for key, ref, col, lab in (("p0", R["f0"] ** 2, "k", r"$g^4$"), ("q0", -2 * R["f0"] * R["e0"], "#5d81b4", r"$g^2\lambda$"),
                           ("r0", R["e0"] ** 2, "#eb6235", r"$\lambda^2$")):
    ax2.plot(pm, 1e4 * R[key].imag, color=col, lw=0.9, ls="-", label=lab)
    ax2.plot(pm[::6], 1e4 * ref[::6], "o", ms=3.0, mfc="none", mec=col)
ax2.set_xscale("log")
ax2.set_xlabel(r"$p/m$  ($\sqrt{s}=2\sqrt{m^2+p^2}$)")
ax2.set_ylabel(r"$10^4\,\mathrm{Im}\,a_0^{(1)}$ terms")
ax2.legend(loc="upper left", fontsize=6.5, ncol=3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "pw_d4.pdf"))
print("wrote results/pw.csv and figs/pw_d4.pdf")
