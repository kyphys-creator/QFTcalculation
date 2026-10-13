# %% [markdown]
# # Step (8): the anomalous magnetic moment -- F2(q^2), F2(0) = alpha/(2 pi), and the two-loop vacuum-polarization contribution
#
# Research note models/spinor_qed, step (8), Eqs. (eq:proj), (eq:g2vp), (eq:g2asym), App. g2.
# - K F2(q^2)/e^2 = 2 m^2 int_0^1 dw/(m^2 - q^2 w(1-w)) (Eq. (7)/(5), q^2 < 4 m^2; mpmath) against COLLIER (g2_collier.f90), Package-X
#   and LoopTools (g2_feyncalc.wl, the FeynArts vertex projected on F2); K F2(0)/e^2 = 2: a = F2(0) = alpha/(2 pi) for e and mu.
# - The two-loop contribution of a vacuum-polarization loop of mass m to the g-2 of a lepton of mass M, r = M/m, in units of
#   (alpha/pi)^2 (alpha = alpha(0): the loop is subtracted at q^2 = 0, Pibar = Pi^R(q^2) - Pi^R(0)):
#     A(r) = int_0^1 dx (1-x) (pi/alpha) Pibar(t),   t = -x^2 M^2/(1-x)          (x-representation, App. g2)
#          = int_0^1 du int_0^1 dv u^2 (1-u) v^2 (1 - v^2/3)/(u^2 (1 - v^2) + 4 (1-u)/r^2)   (dispersive form = Passera Eq. (4)),
#   (pi/alpha) Pibar(t) = 2 int_0^1 dz z(1-z) ln(1 - z(1-z) t/m^2).  Asymptotics (App. g2): A -> (1/3) ln r - 25/36 (r >> 1),
#   A -> r^2/45 (r << 1).  The x-integral is done (i) adaptively with mpmath (30 digits) and (ii) by Gauss-Legendre on fixed
#   nodes (logarithmic in x on [x0, 1/2] and in y = sqrt(1-x) on [1/2, 1]) with Pibar from mpmath, Package-X (30 digits), LoopTools
#   and COLLIER (|t| >= 0.05; the series -2 sum_n t^n B(n+2, n+2)/n below).  The double integral and Passera's closed form
#   (M. Passera, J. Phys. G 31 (2005) R75, Eq. (5)) are independent checks; literature values: Passera Eqs. (6), (7), and
#   A(1) = 119/36 - pi^2/3.
# Writes results/g2.csv and ../figs/g2_vp.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python g2_numeric.py --nodes` writes work/g2_nodes.txt (run first), then without arguments
# after g2_feyncalc.wl (run_g2_check.sh).  Interactive: "Run Cell" in VS Code (the node file must exist).

# %%
import csv
import math
import os
import subprocess
import sys

import mpmath as mp
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
mp.mp.dps = 30
ME, MMU = 1.0, 1.7
ALPHA0 = 1 / 137.035999084               # alpha(0), CODATA 2018
R_MUE = 206.768283                       # m_mu/m_e, CODATA 2018 (the note's applications)
TS = 0.05                                # LoopTools and COLLIER for |t| >= TS m^2
N1, N2 = 96, 64                          # Gauss-Legendre nodes on [x0, 1/2] (log x) and [1/2, 1] (x = 1 - y^2)
CASES = [   # (label, r = M/m, literature value or None)
    ("mu, e loop (benchmark 1.7)", 1.7, None),
    ("e, mu loop (benchmark 1/1.7)", 1 / 1.7, None),
    ("equal masses", 1.0, mp.mpf(119) / 36 - mp.pi ** 2 / 3),
    ("Passera (6): m_mu/m_e = 206.7682838", 206.7682838, mp.mpf("1.0942583111")),
    ("Passera (7): m_mu/m_tau", 105.6583692 / 1776.99, mp.mpf("0.000078064")),
    ("mu, e loop (physical)", R_MUE, None),
    ("e, mu loop (physical)", 1 / R_MUE, None),
]


def gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return (b - a) / 2 * x + (a + b) / 2, (b - a) / 2 * w


def nodes(r):
    """x nodes and weights of the x-representation, 1 - x, and t = -x^2 r^2/(1-x) (m = 1, M = r).  Both segments are
    logarithmic: x = x0 (1/(2 x0))^u on [x0, 1/2] and x = 1 - y^2, y = y0 (sqrt(1/2)/y0)^v on [1/2, 1 - y0^2], so that the
    scales x ~ 1/r (r >> 1) and 1 - x ~ r^2 (r << 1) are resolved; 1 - x = y^2 is kept exactly."""
    x0, y0 = 1e-7 / max(r, 1.0), 1e-7 * min(r, 1.0)
    lg, lgy = math.log(0.5 / x0), math.log(math.sqrt(0.5) / y0)
    u, wu = gl(N1, 0.0, 1.0)
    xa = x0 * np.exp(u * lg)
    wa = wu * xa * lg
    v, wv = gl(N2, 0.0, 1.0)
    y = y0 * np.exp(v * lgy)
    wy = wv * y * lgy
    x, w = np.concatenate([xa, 1 - y * y]), np.concatenate([wa, wy * 2 * y])
    omx = np.concatenate([1 - xa, y * y])
    return x, w, omx, -x * x * r * r / omx


ALL_T = np.concatenate([nodes(r)[3] for _, r, _ in CASES])
if "--nodes" in sys.argv:
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    with open(os.path.join(HERE, "work", "g2_nodes.txt"), "w") as fh:
        fh.writelines(f"{t:.17e}\n" for t in ALL_T)
    print(f"wrote work/g2_nodes.txt ({len(ALL_T)} nodes, {len(CASES)} mass ratios)")
    sys.exit(0)

# %% [markdown]
# ## The hand formulas: Pibar and F2 (mpmath)

# %%
def pibar(t):
    """(pi/alpha) Pibar(t) for m = 1, t < 0: 2 int z(1-z) ln(1 - z(1-z) t)"""
    t = mp.mpf(t)
    if abs(t) < 0.5:                     # -2 sum_n t^n B(n+2, n+2)/n
        return -2 * mp.nsum(lambda n: t ** n / n * mp.beta(n + 2, n + 2), [1, mp.inf])
    b = mp.sqrt(1 - 4 / t)
    lb = mp.log((b + 1) ** 2 * (-t) / 4)          # ln((b+1)/(b-1)), b - 1 = (-4/t)/(b + 1)
    return -(mp.mpf(1) / 3) * ((1 + 2 / t) * (2 - b * lb) - mp.mpf(1) / 3)


def pibar_fp(t):        # the Feynman-parameter integral itself
    return 2 * mp.quad(lambda z: z * (1 - z) * mp.log1p(-z * (1 - z) * mp.mpf(t)), [0, 0.5, 1])


def f2_fp(q2, m):       # K F2/e^2, q^2 < 4 m^2
    return 2 * m * m * mp.quad(lambda w: 1 / (m * m - q2 * w * (1 - w)), [0, 0.5, 1])


print("Pibar: series/closed form against the Feynman-parameter integral at t = -1e-6, -0.3, -3, -1e6:",
      [mp.nstr(pibar(t) - pibar_fp(t), 3) for t in (-1e-6, -0.3, -3.0, -1e6)])
print("K F2(0)/e^2 =", mp.nstr(f2_fp(0, ME), 20), "(e),", mp.nstr(f2_fp(0, MMU), 20), "(mu):  F2(0) = 2 e^2/K = alpha/(2 pi)")

# %% [markdown]
# ## COLLIER, Package-X and LoopTools

# %%
subprocess.run(["./g2_collier", "g2_nodes.txt", "../results/g2_collier_pibar.csv", "../results/g2_collier_f2.csv"],
               cwd=os.path.join(HERE, "work"), check=True, capture_output=True)


def read_csv(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


fc = read_csv("g2_feyncalc_pibar.csv")
cl = read_csv("g2_collier_pibar.csv")
assert len(fc) == len(cl) == len(ALL_T)
PIB = {"mpmath": [], "Package-X": [], "LoopTools": [], "COLLIER": []}
for t, a, b in zip(ALL_T, fc, cl):
    ref = pibar(t)
    PIB["mpmath"].append(ref)
    PIB["Package-X"].append(mp.mpf(a["pibar_px"]))
    PIB["LoopTools"].append(ref if a["pibar_lt"] == "nan" else mp.mpf(a["pibar_lt"]))     # the series below |t| = TS
    PIB["COLLIER"].append(ref if b["pibar"] == "nan" else mp.mpf(b["pibar"]))
use = np.abs(ALL_T) >= TS
for tool in ("Package-X", "LoopTools", "COLLIER"):
    rel = max(abs(x / y - 1) for x, y, u in zip(PIB[tool], PIB["mpmath"], use) if u or tool == "Package-X")
    print(f"Pibar at the nodes: {tool} against mpmath, max relative deviation {mp.nstr(rel, 3)}"
          + ("" if tool == "Package-X" else f"  ({int(use.sum())} of {len(use)} nodes, |t| >= {TS})"))

F2 = {}
for r in read_csv("g2_collier_f2.csv"):
    F2[(r["func"], float(r["q2"]), "COLLIER")] = complex(float(r["re_f2"]), float(r["im_f2"]))
for r in read_csv("g2_feyncalc_f2.csv"):
    F2[(r["func"], float(r["q2"]), "Package-X")] = complex(float(r["re_px"]), float(r["im_px"]))
    F2[(r["func"], float(r["q2"]), "LoopTools")] = complex(float(r["re_lt"]), float(r["im_lt"]))
f2rows = []
f2dev = {}
for (func, q2, tool), v in sorted(F2.items()):
    m = ME if func == "F2_e" else MMU
    ref = complex(f2_fp(q2, m)) if q2 < 4 * m * m else F2[(func, q2, "COLLIER")]
    dev = abs(v - ref) / abs(ref)
    f2dev[tool] = max(f2dev.get(tool, 0.0), dev)
    f2rows.append(["F2", func, q2, tool, v.real, v.imag, ref.real, dev])
print("K F2/e^2 at q^2 = -5 ... 10 for e and mu: max relative deviation from the Feynman-parameter integral (q^2 < 4m^2; "
      "COLLIER above):", {k: f"{x:.1e}" for k, x in f2dev.items()})
print("K F2(0)/e^2:", {f"{f},{t}": round(F2[(f, 0.0, t)].real, 15) for f in ("F2_e", "F2_mu") for t in ("Package-X", "LoopTools", "COLLIER")})

# %% [markdown]
# ## The two-loop vacuum-polarization coefficient A(r)

# %%
def a_xrep(r):           # adaptive, 30 digits
    f = lambda x: (1 - x) * pibar(-x * x * r * r / (1 - x))
    pts = [0, 1 / mp.mpf(r), 0.5, 1] if r > 2 else [0, 0.5, 1]
    return mp.quad(f, pts)


def a_double(r):         # the dispersive form, Passera Eq. (4)
    x2 = 1 / mp.mpf(r) ** 2
    return mp.quad(lambda u, v: u * u * (1 - u) * v * v * (1 - v * v / 3) / (u * u * (1 - v * v) + 4 * x2 * (1 - u)), [0, 1], [0, 1])


def a_passera(r):        # Passera Eq. (5), x = m/M = 1/r
    x = 1 / mp.mpf(r)
    if x == 1:
        return mp.mpf(119) / 36 - mp.pi ** 2 / 3
    ln = mp.log
    v = (-mp.mpf(25) / 36 - ln(x) / 3 + x ** 2 * (4 + 3 * ln(x)) + x ** 4 * (mp.pi ** 2 / 3 - 2 * ln(x) * ln(1 / x - x) - mp.polylog(2, x * x))
         + x / 2 * (1 - 5 * x * x) * (mp.pi ** 2 / 2 - ln(x) * ln((1 - x) / (1 + x)) - mp.polylog(2, x) + mp.polylog(2, -x)))
    return mp.re(v)


def a_asym(r):
    return mp.log(r) / 3 - mp.mpf(25) / 36 if r > 1 else mp.mpf(r) ** 2 / 45


rows = []
ofs = 0
print(f"{'case':38} {'r':>12} {'A (mpmath, adaptive)':>24} {'double integral':>9} {'Passera (5)':>9} "
      + " ".join(f"{t:>9}" for t in ("mpmath", "Package-X", "LoopTools", "COLLIER")) + f" {'literature':>16} {'asympt.':>9}")
RES = {}
for label, r, lit in CASES:
    x, w, omx, t = nodes(r)
    n = len(x)
    ref = a_xrep(r)
    dbl, pas = a_double(r), a_passera(r)
    gls = {tool: mp.fsum(mp.mpf(wi) * mp.mpf(oi) * pv for oi, wi, pv in zip(omx, w, PIB[tool][ofs:ofs + n]))
           for tool in PIB}
    ofs += n
    RES[label] = ref
    rel = lambda v: abs(v / ref - 1)
    print(f"{label:38} {r:12.7g} {mp.nstr(ref, 20):>24} {mp.nstr(rel(dbl), 2):>9} {mp.nstr(rel(pas), 2):>9} "
          + " ".join(f"{mp.nstr(rel(gls[tool]), 2):>9}" for tool in gls)
          + f" {(mp.nstr(lit, 12) if lit is not None else '-'):>16} {mp.nstr(a_asym(r) / ref - 1, 2):>9}")
    rows.append(["A", label, r, "", "", float(ref), float(dbl), float(pas)] + [float(gls[t]) for t in gls]
                + [float(lit) if lit is not None else "", float(a_asym(r))])
print(f"literature: Passera (6) 1.0942583111(84) -> ours {mp.nstr(RES[CASES[3][0]], 13)};  Passera (7) 0.000078064(25) -> ours "
      f"{mp.nstr(RES[CASES[4][0]], 8)};  119/36 - pi^2/3 = {mp.nstr(CASES[2][2], 16)} -> ours {mp.nstr(RES['equal masses'], 16)}")

# physical contributions (alpha(0)): one loop and the two vacuum-polarization loops (e and mu) of this model
ap = ALPHA0 / math.pi
amu = {"one loop alpha/(2 pi)": ALPHA0 / (2 * math.pi), "e loop": ap * ap * float(RES["mu, e loop (physical)"]),
       "mu loop": ap * ap * float(RES["equal masses"])}
ael = {"one loop alpha/(2 pi)": ALPHA0 / (2 * math.pi), "e loop": ap * ap * float(RES["equal masses"]),
       "mu loop": ap * ap * float(RES["e, mu loop (physical)"])}
print("a_mu (alpha(0) = 1/137.035999084, m_mu/m_e = 206.768283):", {k: f"{v:.10e}" for k, v in amu.items()})
print("a_e:", {k: f"{v:.10e}" for k, v in ael.items()})
# the benchmark of this note: e(m_e) = 1 read as alpha(0) = 1/(4 pi)
ab = 1 / (4 * math.pi) / math.pi
print(f"benchmark alpha = 1/(4 pi): a_mu = {1 / (8 * math.pi ** 2):.8f} + {ab * ab * float(RES['mu, e loop (benchmark 1.7)'] + RES['equal masses']):.8f}, "
      f"a_e = {1 / (8 * math.pi ** 2):.8f} + {ab * ab * float(RES['equal masses'] + RES['e, mu loop (benchmark 1/1.7)']):.8f}")
for k, v in amu.items():
    rows.append(["a_mu", k, R_MUE, "", "", v] + [""] * 8)
for k, v in ael.items():
    rows.append(["a_e", k, 1 / R_MUE, "", "", v] + [""] * 8)

with open(os.path.join(HERE, "results", "g2.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["kind", "label", "r", "q2", "tool", "value", "double_or_ref", "passera_or_dev", "gl_mpmath", "gl_packagex",
                 "gl_looptools", "gl_collier", "literature", "asymptotic"])
    wr.writerows(rows)
    wr.writerows([[x[0], x[1], "", x[2], x[3], x[4], x[6], x[7]] + [""] * 6 for x in f2rows])
print("wrote results/g2.csv")

# %% [markdown]
# ## Figure: A(r) and where the x-integral comes from

# %%
def pibar_np(t):         # float version of pibar (series below |t| = 0.5)
    t = np.asarray(t, float)
    out = np.empty_like(t)
    s = np.abs(t) < 0.5
    ts = t[s]
    out[s] = -2 * sum(ts ** n / n * math.gamma(n + 2) ** 2 / math.gamma(2 * n + 4) for n in range(1, 40))
    tl = t[~s]
    b = np.sqrt(1 - 4 / tl)
    lb = np.log((b + 1) ** 2 * (-tl) / 4)
    out[~s] = -((1 + 2 / tl) * (2 - b * lb) - 1 / 3) / 3
    return out


def a_np(r):
    x, w, omx, t = nodes(r)
    return float(np.sum(w * omx * pibar_np(t)))


COLORS = {"curve": "#2a78d6", "asym": "#eb6834", "pts": "#1baf7a"}     # validated categorical slots 1-3 (dataviz palette)
rs = np.geomspace(1e-3, 1e3, 145)
av = np.array([a_np(r) for r in rs])
print(f"figure curve: max relative deviation of the float GL curve from mpmath at the cases "
      f"{max(abs(a_np(r) / float(RES[l]) - 1) for l, r, _ in CASES):.1e}")
fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.6))
ax = axes[0]
ax.plot(rs, av, color=COLORS["curve"], lw=2, label=r"$A(r)$")
big, small = rs > 20, rs < 0.6
ax.plot(rs[big], np.log(rs[big]) / 3 - 25 / 36, color=COLORS["asym"], lw=1.5, ls="--", label=r"$\frac{1}{3}\ln r-\frac{25}{36}$")
ax.plot(rs[small], rs[small] ** 2 / 45, color=COLORS["asym"], lw=1.5, ls=":", label=r"$r^2/45$")
for label, r, lit in CASES:
    if lit is not None:
        ax.plot(r, float(lit), ls="none", marker="o", ms=9, mfc="none", mec="0.25", mew=1.2)
    ax.plot(r, float(RES[label]), ls="none", marker="o", ms=4, color=COLORS["pts"])
ax.plot([], [], ls="none", marker="o", ms=9, mfc="none", mec="0.25", label="literature")
ax.plot([], [], ls="none", marker="o", ms=4, color=COLORS["pts"], label="this note")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1e-8, 5)
ax.set_xlabel(r"$r=M/m$ (lepton / loop)")
ax.set_ylabel(r"$A(r)$  [units of $(\alpha/\pi)^2$]")
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax = axes[1]
xx = np.linspace(1e-5, 1 - 1e-7, 4000)
for r, ls, col, lab in ((R_MUE, "-", COLORS["curve"], r"$r=206.8$ ($a_\mu$, e loop)"), (1.7, "--", COLORS["curve"], r"$r=1.7$"),
                        (1.0, ":", "0.35", r"$r=1$"), (1 / 1.7, "--", COLORS["asym"], r"$r=1/1.7$"),
                        (1 / R_MUE, "-", COLORS["asym"], r"$r=1/206.8$ ($a_e$, $\mu$ loop)")):
    ax.plot(xx, (1 - xx) * pibar_np(-xx * xx * r * r / (1 - xx)) / a_np(r), lw=1.8, ls=ls, color=col, label=lab)
ax.set_xlim(0, 1)
ax.set_ylim(0, 3.6)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$(1-x)\,\bar\Pi(t)\,(\pi/\alpha)\,/A(r)$")
ax.legend(frameon=False, fontsize=8, loc="upper left")
for ax in axes:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(alpha=0.3, lw=0.5)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "g2_vp.pdf"))
print("wrote ../figs/g2_vp.pdf")
if INTERACTIVE:
    plt.show()
