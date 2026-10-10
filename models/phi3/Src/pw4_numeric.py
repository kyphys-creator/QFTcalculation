# %% [markdown]
# # Step (12): perturbative unitarity and perturbativity of phi phi -> phi phi in d = 4
#
# Partial waves of the identical-particle amplitude (note, App. P):
#   a_l(s) = beta/(64 pi) int_{-1}^{1} dc P_l(c) M(s, c),   beta = sqrt(1 - 4 m^2/s),
# normalized so that the elastic unitarity relation, Eq. (18) projected on P_l, reads Im a_l = |a_l|^2; hence
# |Re a_l| <= 1/2.  Only even l occur (t <-> u).  At tree level (m = 1)
#   a_0^(0) = beta/(32 pi) g^2 [ -1/(s - 1) + 2 ln(s - 3)/(s - 4) ].
# At one loop the S-matrix element M_phys = M0 + M1_phys (Eq. (20); pole mass m, g defined by g_0 = mu^eps g) is
# projected; M1 (MS-bar, mu = m) at the quadrature nodes comes from COLLIER (work/xsec_collier, step (7)).
# Checks: the quadrature against the closed form of a_0^(0); the projected unitarity Im a_l^(1) = |a_l^(0)|^2 (l = 0, 2).
# Bounds on g/m:
#   (A) tree unitarity              g^2 max_s |Re a_0^(0)| <= 1/2;
#   (B) perturbativity              |Re a_0^(1)(s)| <= |Re a_0^(0)(s)| for all s;
#   (C) one-loop unitarity          |Re a_0^(0) + Re a_0^(1)| <= 1/2 for all s;
#   (D) vertex perturbativity       g_os/g - 1 <= 1, g_os = g [1 - g^2 C0(m^2,m^2,m^2)/(4pi)^2 - (3/4) g^2 m^2 B0'(m^2)/(4pi)^2]
#       (the on-shell three-point coupling, including the residue factor R^(3/2)).
# (B) and (C) are also given with g replaced by g_os (scheme dependence of the one-loop bounds).
# Comparison with the Higgs trilinear coupling: g_SM = 3 m_h^2/v, i.e. g/m_h = 3 m_h/v (Di Luzio, Groeber, Spannowsky 2017).
#
# Writes results/pw4.csv and ../figs/pw4_d4.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python pw4_numeric.py` (from Src/; run run_xsec_check.sh once so that work/xsec_collier exists).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import subprocess
import sys

import numpy as np
from scipy.integrate import quad
from scipy.special import eval_legendre

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
K4 = (4 * math.pi) ** 2
B0M = 2 - math.pi / math.sqrt(3)                 # B0(m^2) at mu = m        (App. J)
B0PM = 2 * math.pi / (3 * math.sqrt(3)) - 1       # m^2 B0'(m^2)             (App. J)
C0M = -0.6712531057479                            # C0(m^2, m^2, m^2; m, m, m)  (step (3), Feynman-parameter value)
NGL = 64                                          # Gauss-Legendre nodes per sqrt(s)
MH, VEV = 125.25, 246.22                          # GeV, for the comparison with the Higgs trilinear coupling


def tree(s, c):
    p2 = s / 4 - 1
    t, u = -2 * p2 * (1 - c), -2 * p2 * (1 + c)
    return -(1 / (s - 1) + 1 / (t - 1) + 1 / (u - 1))


def conversion4(s, c):
    """Eq. (20): M1_phys - M1(MS-bar, mu = m) for m_p = g = 1."""
    p2 = s / 4 - 1
    xs = (s, -2 * p2 * (1 - c), -2 * p2 * (1 + c))
    return sum(2 * B0PM / (x - 1) - B0M / (x - 1) ** 2 for x in xs) / (2 * K4)


def a0_tree_closed(s):
    beta = math.sqrt(1 - 4 / s)
    return beta / (32 * math.pi) * (-1 / (s - 1) + 2 * math.log(s - 3) / (s - 4))


# %% [markdown]
# ## Quadrature nodes and the one-loop amplitude from COLLIER
# By the t <-> u symmetry, int_{-1}^{1} = 2 int_0^1 for even l.  The t-channel peak at c -> 1 (width m^2/(2 p^2)) is
# flattened by y = ln((m^2 - t)/m^2), as in step (7): c = 1 - (e^y - 1)/(2 p^2), dc = e^y dy/(2 p^2), y in [0, ln(1 + 2 p^2)].

# %%
# sqrt(s) = 2 sqrt(1 + (p/m)^2): logarithmic in the CM momentum p from 0.01 m (the J = 0 ratio a^(1)/a^(0) has a finite
# threshold limit, reached to 1e-4 there) to 10 m, refined where |a_0^(0)| is largest
RS = np.unique(np.concatenate([2 * np.sqrt(1 + np.geomspace(0.01, 10.0, 80) ** 2), np.linspace(2.2, 3.0, 17)]))


def nodes(rs):
    p2 = rs * rs / 4 - 1
    x, w = np.polynomial.legendre.leggauss(NGL)
    ymax = math.log(1 + 2 * p2)
    y = 0.5 * ymax * (x + 1)
    c = 1 - (np.exp(y) - 1) / (2 * p2)
    return c, 0.5 * ymax * w * np.exp(y) / (2 * p2)


work = os.path.join(HERE, "work")
exe = os.path.join(work, "xsec_collier")
if not os.path.exists(exe):
    subprocess.run(["gfortran", "-I" + os.path.expanduser("~/hep/include"), "xsec_collier.f90",
                    "-L" + os.path.expanduser("~/hep/lib"), "-lcollier", "-o", exe], cwd=HERE, check=True)
with open(os.path.join(work, "pw4_nodes.txt"), "w") as fh:
    for rs in RS:
        for c in nodes(rs)[0]:
            fh.write(f"{rs:.17e} {c:.17e}\n")
    fh.write(f"{5.0:.17e} {0.3:.17e}\n")              # step (5) point, as a regression check
subprocess.run([exe, "pw4_nodes.txt", "pw4_m1_nodes.csv"], cwd=work, check=True, capture_output=True)
m1 = {}
with open(os.path.join(work, "pw4_m1_nodes.csv")) as fh:
    for r in csv.DictReader(fh):
        m1[(float(r["sqrts"]), float(r["costheta"]))] = complex(float(r["re_m1"]), float(r["im_m1"]))
reg = m1[(5.0, 0.3)]
print(f"regression: M1(sqrt(s) = 5, cos = 0.3) = {reg.real:.12e} + {reg.imag:.12e} i   (step (5): 7.356033343800e-04 + 5.055001340376e-04 i)")
assert abs(reg - (7.356033343800272e-04 + 5.055001340375805e-04j)) < 1e-14

# %% [markdown]
# ## Partial waves at tree level and at one loop, and the projected unitarity relation

# %%
rows = []
for rs in RS:
    s = rs * rs
    beta = math.sqrt(1 - 4 / s)
    c, w = nodes(rs)
    mt = np.array([tree(s, ci) for ci in c])
    mph = np.array([m1[(float(f"{rs:.17e}"), float(f"{ci:.17e}"))] + conversion4(s, ci) for ci in c])
    a = {}
    for l in (0, 2):
        pl = eval_legendre(l, c)
        a[(l, 0)] = beta / (64 * math.pi) * 2 * np.sum(w * pl * mt)
        a[(l, 1)] = beta / (64 * math.pi) * 2 * np.sum(w * pl * mph)
    rows.append(dict(rs=rs, a00=a[(0, 0)], a01=a[(0, 1)], a20=a[(2, 0)], a21=a[(2, 1)]))
dq = max(abs(r["a00"] / a0_tree_closed(r["rs"] ** 2) - 1) for r in rows)
du0 = max(abs(r["a01"].imag / r["a00"] ** 2 - 1) for r in rows)
du2 = max(abs(r["a21"].imag / r["a20"] ** 2 - 1) for r in rows if r["rs"] > 2.25)   # a_2 ~ beta^5 is tiny closer to threshold
print(f"a_0^(0): quadrature vs closed form, largest relative deviation {dq:.1e}")
print(f"unitarity Im a_l^(1) = |a_l^(0)|^2: largest relative deviation {du0:.1e} (l = 0), {du2:.1e} (l = 2, sqrt(s) > 2.25 m)")
rows[np.argmax([r["a00"] for r in rows])]                     # inspect: where |a_0^(0)| is largest (g = m = 1)

# %% [markdown]
# ## Bounds on g/m
# With g = m = 1 values a^(0), a^(1): a_0 = g^2 a^(0) + g^4 a^(1).  The scheme with g_os replaces
# a^(1) by a^(1) - 2 d a^(0), d = [-C0(m^2,m^2,m^2) - (3/4) m^2 B0'(m^2)]/(4pi)^2  (M0 is proportional to g^2).

# %%
d_os = (-C0M - 0.75 * B0PM) / K4
print(f"g_os = g (1 + {d_os * K4:.4f} g^2/(4 pi)^2)")


def bounds(shift):
    re0 = np.array([r["a00"] for r in rows])
    re1 = np.array([r["a01"].real for r in rows]) - shift * re0
    gA = math.sqrt(0.5 / re0.max())
    gB = math.sqrt(np.min(re0 / np.abs(re1)))
    gC_s = []
    for x0, x1 in zip(re0, re1):                  # smallest g > 0 with |x0 g^2 + x1 g^4| = 1/2
        roots = [r.real for r in np.roots([x1, 0, x0, 0, -0.5]) if abs(r.imag) < 1e-12 and r.real > 0]
        roots += [r.real for r in np.roots([x1, 0, x0, 0, 0.5]) if abs(r.imag) < 1e-12 and r.real > 0]
        gC_s.append(min(roots) if roots else np.inf)
    return gA, gB, min(gC_s), re1, np.array(gC_s)


gA, gB, gC, re1, gC_s = bounds(0.0)
_, gB_os, gC_os, re1_os, gC_s_os = bounds(2 * d_os)
gD = math.sqrt(1 / d_os)
gsm = 3 * MH / VEV
table = [("(A) tree unitarity |Re a0| <= 1/2", gA, None),
         ("(B) perturbativity |Re a0^(1)| <= |Re a0^(0)|", gB, gB_os),
         ("(C) one-loop unitarity |Re a0| <= 1/2", gC, gC_os),
         ("(D) vertex perturbativity g_os/g - 1 <= 1", gD, None)]
imin = {k: rs for k, rs in (("A", RS[np.argmax([r["a00"] for r in rows])]), ("B", RS[np.argmin(np.array([r["a00"] for r in rows]) / np.abs(re1))]), ("C", RS[np.argmin(gC_s)]))}
print("sqrt(s)/m where each bound is strongest:", {k: round(float(v), 4) for k, v in imin.items()})
print(f"\n{'criterion':48} {'g/m (g)':>9} {'g/m (g_os)':>11} {'kappa (g)':>10} {'kappa (g_os)':>13}")
for name, g1, g2 in table:
    print(f"{name:48} {g1:9.2f} {g2 if g2 else float('nan'):11.2f} {g1 / gsm:10.2f} {(g2 / gsm) if g2 else float('nan'):13.2f}")
print(f"\nHiggs: g_SM/m_h = 3 m_h/v = {gsm:.4f};  Di Luzio et al. (2017): kappa <~ 6.5 (tree, SM quartic kept), <~ 6 (one-loop vertex)")

# %% [markdown]
# ## Output

# %%
with open(os.path.join(HERE, "results", "pw4.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["sqrts", "a0_tree", "re_a0_1loop", "im_a0_1loop", "a2_tree", "re_a2_1loop", "im_a2_1loop",
                 "re_a0_1loop_gos", "gmax_C", "gmax_C_gos"])
    for r, x1os, gc, gco in zip(rows, re1_os, gC_s, gC_s_os):
        wr.writerow([r["rs"], r["a00"], r["a01"].real, r["a01"].imag, r["a20"], r["a21"].real, r["a21"].imag, x1os, gc, gco])
    wr.writerow([])
    wr.writerow(["criterion", "gmax_over_m_g", "gmax_over_m_gos", "kappa_g", "kappa_gos"])
    for name, g1, g2 in table:
        wr.writerow([name, g1, g2 if g2 else "", g1 / gsm, (g2 / gsm) if g2 else ""])

# %% [markdown]
# ## Figure: the largest g/m allowed at each sqrt(s), and the projected unitarity relation

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
rs_arr = np.array([r["rs"] for r in rows])
pm = np.sqrt(rs_arr ** 2 / 4 - 1)                      # CM momentum p/m
re0 = np.array([r["a00"] for r in rows])
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.25, 4.1), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
ax1.plot(pm, np.sqrt(0.5 / re0), color="k", lw=0.9, ls="-", label="(A) tree unitarity")
ax1.plot(pm, np.sqrt(re0 / np.abs(re1)), color="#5d81b4", lw=0.9, ls="--", label="(B) perturbativity")
ax1.plot(pm, np.sqrt(re0 / np.abs(re1_os)), color="#5d81b4", lw=0.7, ls=":", label=r"(B) with $g_{\rm os}$")
ax1.plot(pm, gC_s, color="#e09b24", lw=0.9, ls="-.", label="(C) one-loop unitarity")
ax1.axhline(gD, color="0.6", lw=0.7, ls="-", label="(D) vertex")
ax1.set_ylim(0, 46)
ax1.set_ylabel(r"largest $g/m$")
ax1.legend(loc="upper center", fontsize=6.5, ncol=2)
ax2.plot(pm, 1e5 * np.array([r["a01"].imag for r in rows]), color="k", lw=0.9, ls="-", label=r"$\mathrm{Im}\,a_0^{(1)}$")
ax2.plot(pm[::5], 1e5 * re0[::5] ** 2, "o", ms=3.5, mfc="none", mec="#eb6235", label=r"$|a_0^{(0)}|^2$")
ax2.set_ylabel(r"$10^5\times$ ($g=m$)")
ax2.set_xlabel(r"$p/m$  ($\sqrt{s}=2\sqrt{m^2+p^2}$)")
ax2.set_xscale("log")
ax2.legend(loc="upper left")
ax1.set_title(r"$d=4$, $\phi\phi\to\phi\phi$, $J=0$", fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "pw4_d4.pdf"))
print("wrote results/pw4.csv and figs/pw4_d4.pdf")
