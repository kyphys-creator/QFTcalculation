# %% [markdown]
# # Step (4): one-loop phi phi -> phi phi and psi psibar -> phi phi -- tools compared, unitarity, figure
#
# Research note models/yukawa_ps, Eqs. (13), (14) and eq:M1B, eq:unitB, at m = mu = 1, M = 0.7, y = lambda = 1.
#
# 1. Values: (A) (4 pi)^2 M1(phi phi -> phi phi); (B) a, b with (4 pi)^2 M1(psi psibar -> phi phi) = a vbar(p2) u(p1)
#    + b vbar(p2) k1slash u(p1), from FeynCalc + Package-X, FeynCalc + LoopTools (scat_feyncalc.wl), FormCalc + LoopTools
#    (scat_formcalc.wl) and COLLIER (the note's hand formulas, scat_collier.f90).
# 2. Unitarity (the absorptive parts, i.e. the imaginary parts of the coefficient functions), with explicit Dirac
#    spinors and an angular quadrature over the intermediate state:
#    (A) Im M1 = lambda^2 p/(16 pi sqrt s) + (1/2) p_psi/(16 pi^2 sqrt s) int dOmega sum_spins M(phi phi -> psi psibar) M*(phi phi -> psi psibar)
#        (Eq. (14));
#    (B) Abs M1(psi psibar -> phi phi) = (1/2) p/(16 pi^2 sqrt s) int dOmega sum_spins M(psi psibar -> psi psibar) M*(phi phi -> psi psibar)
#                                       + (1/2) (1/2) k/(16 pi^2 sqrt s) int dOmega M(psi psibar -> phi phi) (-lambda),
#        compared spin configuration by spin configuration with Im a vbar u + Im b vbar k1slash u (divided by (4 pi)^2).
# 3. Figure ../figs/scat_d4.pdf: cos(theta) dependence at sqrt(s) = 5 (COLLIER scan) with the tool values and the unitarity
#    integrals.
# Reads results/scat_{feyncalc,formcalc,collier,collier_scan}.csv, writes results/scat_comparison.csv.
# Batch: `~/miniforge3/envs/qft/bin/python scat_numeric.py` (from Src/).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import itertools
import math
import os
import sys

import numpy as np

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
MPHI, MPSI, Y, LAM = 1.0, 0.7, 1.0, 1.0
K16 = (4 * math.pi) ** 2


def read_csv(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


def cval(row, key):
    return complex(float(row["re_" + key]), float(row["im_" + key]))


fc = read_csv("scat_feyncalc.csv")
fo = read_csv("scat_formcalc.csv")
co = read_csv("scat_collier.csv")
scan = read_csv("scat_collier_scan.csv")
assert len(fc) == len(fo) == len(co)
fc[:1]          # inspect

# %% [markdown]
# ## Values from the four routes (reference: COLLIER, i.e. the note's formulas)

# %%
rows, worst = [], {}
print(f"{'sqrt(s)':>7} {'cos':>5}  {'quantity':8} {'COLLIER (note)':>34}   rel. dev. FC+PX   FC+LT   FormCalc+LT")
for f, o, c in zip(fc, fo, co):
    rs, ct = float(c["sqrts"]), float(c["costheta"])
    scale_b = abs(cval(c, "a")) + abs(cval(c, "b"))
    for q, ref, scale, vals in (("a", cval(c, "a"), scale_b, (cval(f, "a_px"), cval(f, "a_lt"), cval(o, "a"))),
                                ("b", cval(c, "b"), scale_b, (cval(f, "b_px"), cval(f, "b_lt"), cval(o, "b"))),
                                ("M1_A", cval(c, "mA"), abs(cval(c, "mA")), (cval(f, "mA_px"), cval(f, "mA_lt"), cval(o, "mA")))):
        devs = [abs(v - ref) / scale for v in vals]
        rows.append((rs, ct, q, ref.real, ref.imag, *devs))
        print(f"{rs:7.2f} {ct:5.2f}  {q:8} {ref.real:+16.12f} {ref.imag:+16.12f} i   {devs[0]:.1e}   {devs[1]:.1e}   {devs[2]:.1e}")
        for name, d in zip(("FeynCalc+Package-X", "FeynCalc+LoopTools", "FormCalc+LoopTools"), devs):
            key = ("A" if q == "M1_A" else "B", name)
            worst[key] = max(worst.get(key, 0.0), d)
print("max deviation from COLLIER (A: relative to |M1|; B: relative to |a| + |b|):")
for (proc, name), d in sorted(worst.items()):
    print(f"  ({proc}) {name:20s} {d:.1e}")

# %% [markdown]
# ## Dirac matrices, spinors and tree amplitudes (as in tree_sigma.py)

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


def u_sp(p, m, chi):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + m)
    return np.concatenate([n * chi, sp @ chi / n])


def v_sp(p, m, eta):
    sp = p[1] * SIG[0] + p[2] * SIG[1] + p[3] * SIG[2]
    n = math.sqrt(p[0] + m)
    return np.concatenate([sp @ eta / n, n * eta])


def bar(w):
    return w.conj() @ G0


def vec(e, pabs, cth, phi=0.0):
    sth = math.sqrt(max(0.0, 1 - cth * cth))
    return np.array([e, pabs * sth * math.cos(phi), pabs * sth * math.sin(phi), pabs * cth])


def m_phiphi_to_psipsibar(ka, kb, q1, r1, q2, r2):
    """M(phi(ka) phi(kb) -> psi(q1, r1) psibar(q2, r2)) = y^2 ubar(q1) [ka/((q1-ka)^2-M^2) + kb/((q1-kb)^2-M^2)] v(q2)."""
    g = slash(ka) / (mdot(q1 - ka, q1 - ka) - MPSI ** 2) + slash(kb) / (mdot(q1 - kb, q1 - kb) - MPSI ** 2)
    return Y ** 2 * bar(u_sp(q1, MPSI, r1)) @ g @ v_sp(q2, MPSI, r2)


def m_psipsibar_to_phiphi(p1, s1, p2, s2, ka, kb):
    """M(psi(p1) psibar(p2) -> phi(ka) phi(kb)) = y^2 vbar(p2) [ka/((p1-ka)^2-M^2) + kb/((p1-kb)^2-M^2)] u(p1)."""
    g = slash(ka) / (mdot(p1 - ka, p1 - ka) - MPSI ** 2) + slash(kb) / (mdot(p1 - kb, p1 - kb) - MPSI ** 2)
    return Y ** 2 * bar(v_sp(p2, MPSI, s2)) @ g @ u_sp(p1, MPSI, s1)


def m_psipsibar_to_psipsibar(p1, s1, p2, s2, q1, r1, q2, r2):
    """M_C = M_s - M_t (s- and t-channel phi exchange; the sign convention of the note's App. tree)."""
    u1, v2, uq1, vq2 = u_sp(p1, MPSI, s1), v_sp(p2, MPSI, s2), u_sp(q1, MPSI, r1), v_sp(q2, MPSI, r2)
    ms = Y ** 2 * (bar(v2) @ G5 @ u1) * (bar(uq1) @ G5 @ vq2) / (mdot(p1 + p2, p1 + p2) - MPHI ** 2)
    mt = Y ** 2 * (bar(uq1) @ G5 @ u1) * (bar(v2) @ G5 @ vq2) / (mdot(p1 - q1, p1 - q1) - MPHI ** 2)
    return ms - mt


# Angular quadrature over the intermediate direction: Gauss-Legendre in cos, uniform (periodic) in the azimuth.  At high
# energy the integrands peak around two different directions (p1 and k1), so a fine grid is used; the sums over the
# intermediate spins are done with the completeness relations sum u ubar = qslash + M, sum v vbar = qslash - M
# (checked against explicit spinor sums in tree_sigma.py), which turns each cut into a 4 x 4 matrix integrand.
NC, NP = 240, 240
XC, WC = np.polynomial.legendre.leggauss(NC)
PHIS = 2 * math.pi * (np.arange(NP) + 0.5) / NP
WPHI = 2 * math.pi / NP
GAM = np.array([G0, -GI[0], -GI[1], -GI[2]])          # gamma_mu with lower index: slash(p) = p^mu gamma_mu


def grid(e, qabs):
    """four-vectors q1, q2 = (e, +-qabs n) on the grid, and the weights."""
    cth, ph = np.meshgrid(XC, PHIS, indexing="ij")
    sth = np.sqrt(1 - cth ** 2)
    n = np.stack([sth * np.cos(ph), sth * np.sin(ph), cth], axis=-1).reshape(-1, 3)
    w = (WC[:, None] * WPHI * np.ones_like(ph)).reshape(-1)
    q1 = np.concatenate([np.full((len(n), 1), e), qabs * n], axis=1)
    q2 = np.concatenate([np.full((len(n), 1), e), -qabs * n], axis=1)
    return q1, q2, w


def vslash(q):
    return np.einsum("nm,mij->nij", q, GAM)


def vmdot(a, b):
    return a[..., 0] * b[..., 0] - a[..., 1] * b[..., 1] - a[..., 2] * b[..., 2] - a[..., 3] * b[..., 3]


def gamma_tree(q1, ka, kb):
    """ka/((q1-ka)^2 - M^2) + kb/((q1-kb)^2 - M^2) on the grid (the Dirac matrix of the psi psibar <-> phi phi tree)."""
    da = vmdot(q1 - ka, q1 - ka) - MPSI ** 2
    db = vmdot(q1 - kb, q1 - kb) - MPSI ** 2
    return slash(ka)[None] / da[:, None, None] + slash(kb)[None] / db[:, None, None]

# %% [markdown]
# ## Unitarity of phi phi -> phi phi (Eq. (14))

# %%
def unit_A(sqrts, cth):
    e = sqrts / 2
    p = math.sqrt(e * e - MPHI ** 2)
    ppsi = math.sqrt(e * e - MPSI ** 2)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    k1 = vec(e, p, cth)
    k2 = np.array([e, -k1[1], -k1[2], -k1[3]])
    q1, q2, w = grid(e, ppsi)
    # sum_spins M(p1 p2 -> q1 q2) M*(k1 k2 -> q1 q2) = y^4 tr[(q1 + M) G_i (q2 - M) G_f]
    gi, gf = gamma_tree(q1, p1, p2), gamma_tree(q1, k1, k2)
    mat = (vslash(q1) + MPSI * ONE) @ gi @ (vslash(q2) - MPSI * ONE) @ gf
    integral = Y ** 4 * np.sum(w * np.trace(mat, axis1=1, axis2=2))
    im_phi = LAM ** 2 * p / (16 * math.pi * sqrts)
    im_psi = 0.5 * ppsi / (16 * math.pi ** 2 * sqrts) * integral
    return im_phi, im_psi


unitA = []
for c in co:
    rs, ct = float(c["sqrts"]), float(c["costheta"])
    im_phi, im_psi = unit_A(rs, ct)
    lhs = cval(c, "mA").imag / K16
    unitA.append((rs, ct, lhs, im_phi + im_psi.real, abs(im_psi.imag)))
    print(f"(A) sqrt(s) = {rs:5.2f}, cos = {ct:4.2f}:  Im M1 = {lhs:+.12e},  phi phi cut {im_phi:+.6e} + psi psibar cut "
          f"{im_psi.real:+.6e} = {im_phi + im_psi.real:+.12e},  rel. dev. {abs(lhs - im_phi - im_psi.real) / abs(lhs):.1e}")

# %% [markdown]
# ## Unitarity of psi psibar -> phi phi, spin configuration by spin configuration
#
# psi psibar cut: sum_spins M_C(p1 p2 -> q1 q2) M*(k1 k2 -> q1 q2), M_C = M_s - M_t;  the t-channel part gives
# -y^4 vbar(p2) g5 (q2 - M) G_f (q1 + M) g5 u(p1) / ((p1 - q1)^2 - m^2), the s-channel part
# y^4 [vbar(p2) g5 u(p1)] tr[(q1 + M) g5 (q2 - M) G_f] / (s - m^2) (zero: gamma5 with three vectors).
# phi phi cut: M(p1 p2 -> l1 l2)(-lambda) = -lambda y^2 vbar(p2) G(l) u(p1).

# %%
def unit_B(sqrts, cth, a, b):
    e = sqrts / 2
    p = math.sqrt(e * e - MPSI ** 2)
    k = math.sqrt(e * e - MPHI ** 2)
    p1, p2 = np.array([e, 0, 0, p]), np.array([e, 0, 0, -p])
    k1 = vec(e, k, cth)
    k2 = np.array([e, -k1[1], -k1[2], -k1[3]])
    q1, q2, w = grid(e, p)
    gf = gamma_tree(q1, k1, k2)
    tden = vmdot(p1 - q1, p1 - q1) - MPHI ** 2
    tmat = -Y ** 4 * (G5[None] @ (vslash(q2) - MPSI * ONE) @ gf @ (vslash(q1) + MPSI * ONE) @ G5[None]) / tden[:, None, None]
    strace = np.trace((vslash(q1) + MPSI * ONE) @ G5[None] @ (vslash(q2) - MPSI * ONE) @ gf, axis1=1, axis2=2)
    smat_coef = Y ** 4 * np.sum(w * strace) / (sqrts ** 2 - MPHI ** 2)        # multiplies vbar g5 u
    psi_mat = 0.5 * p / (16 * math.pi ** 2 * sqrts) * np.einsum("n,nij->ij", w, tmat)
    psi_s = 0.5 * p / (16 * math.pi ** 2 * sqrts) * smat_coef
    l1, l2, wl = grid(e, k)
    phi_mat = 0.5 * 0.5 * k / (16 * math.pi ** 2 * sqrts) * (-LAM) * Y ** 2 * np.einsum("n,nij->ij", wl, slash_sum(l1, l2, p1))
    out = []
    for s1, s2 in itertools.product(CHI, CHI):
        u1, v2 = u_sp(p1, MPSI, s1), v_sp(p2, MPSI, s2)
        lhs = (a.imag * (bar(v2) @ u1) + b.imag * (bar(v2) @ slash(k1) @ u1)) / K16
        rhs_psi = bar(v2) @ psi_mat @ u1 + psi_s * (bar(v2) @ G5 @ u1)
        rhs_phi = bar(v2) @ phi_mat @ u1
        out.append((lhs, rhs_psi, rhs_phi))
    return out


def slash_sum(l1, l2, p1):
    """l1/((p1-l1)^2-M^2) + l2/((p1-l2)^2-M^2) on the grid (the Dirac matrix of M(psi(p1) psibar(p2) -> phi(l1) phi(l2)))."""
    d1 = vmdot(p1[None] - l1, p1[None] - l1) - MPSI ** 2
    d2 = vmdot(p1[None] - l2, p1[None] - l2) - MPSI ** 2
    return vslash(l1) / d1[:, None, None] + vslash(l2) / d2[:, None, None]


unitB = []
for c in co:
    rs, ct = float(c["sqrts"]), float(c["costheta"])
    res = unit_B(rs, ct, cval(c, "a"), cval(c, "b"))
    scale = max(abs(r[0]) for r in res)
    dev = max(abs(r[0] - r[1] - r[2]) for r in res) / scale
    unitB.append((rs, ct, dev, res))
    print(f"(B) sqrt(s) = {rs:5.2f}, cos = {ct:4.2f}:  max over the 4 spin configurations |Abs M1 - cuts| / max|Abs M1| = {dev:.1e};"
          f"  e.g. {res[0][0].real:+.6e} vs {res[0][1].real:+.6e} (psi psibar) {res[0][2].real:+.6e} (phi phi)")

with open(os.path.join(HERE, "results", "scat_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sqrts", "costheta", "quantity", "re_collier", "im_collier", "dev_fc_px", "dev_fc_lt", "dev_formcalc_lt"])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["sqrts", "costheta", "im_M1_A", "unitarity_A", "dev_unit_B"])
    for (rs, ct, lhs, rhs, _), (_, _, devb, _) in zip(unitA, unitB):
        w.writerow([rs, ct, lhs, rhs, devb])
print("wrote results/scat_comparison.csv")

# %% [markdown]
# ## Figure: cos(theta) dependence at sqrt(s) = 5

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
cs = np.array([float(r["costheta"]) for r in scan])
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.4))
series = {"mA": (axes[0], r"$(4\pi)^2\mathcal{M}^{(1)}_A$", r"$\phi\phi\to\phi\phi$"),
          "a": (axes[1], r"$a$", r"$\psi\bar\psi\to\phi\phi$: $a$"),
          "b": (axes[2], r"$b$", r"$\psi\bar\psi\to\phi\phi$: $b$")}
for key, (ax, lab, title) in series.items():
    v = np.array([cval(r, key) for r in scan])
    ax.plot(cs, v.real, color="C0", ls="-", label="Re " + lab)
    ax.plot(cs, v.imag, color="C1", ls="--", label="Im " + lab)
    for c, f, o in zip(co, fc, fo):
        if float(c["sqrts"]) != 5.0:
            continue
        ct = float(c["costheta"])
        vpx = cval(f, key + "_px") if key != "mA" else cval(f, "mA_px")
        vfo = cval(o, key)
        for part, col in ((lambda z: z.real, "C0"), (lambda z: z.imag, "C1")):
            ax.plot([ct], [part(vpx)], "o", ms=4, mfc="none", color=col)
            ax.plot([ct], [part(vfo)], "x", ms=4, color=col)
    if key == "mA":
        for rs, ct, lhs, rhs, _ in unitA:
            if rs == 5.0:
                ax.plot([ct], [K16 * rhs], "s", ms=6, mfc="none", color="k")
    ax.set_xlabel(r"$\cos\theta$")
    ax.set_title(title + r", $\sqrt{s}=5m$", fontsize=8)
    ax.legend(fontsize=6.5, loc="best")
fig.tight_layout()
figpath = os.path.join(HERE, "..", "figs", "scat_d4.pdf")
fig.savefig(figpath)
print("wrote", os.path.relpath(figpath, HERE))
if INTERACTIVE:
    plt.show()
