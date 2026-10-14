# %% [markdown]
# # Step (10): photon-photon scattering -- tools, low- and high-energy limits, optical theorem, cross section
#
# Research note models/spinor_qed, step (10), Eqs. (eq:lblamp)-(eq:lblopt), App. lbl.  X = M/alpha^2 per flavour (m = 1 for
# the electron, 1.7 for the muon of the benchmark); the kinematics and helicity vectors of the note (lbl_collier.f90 header).
# - Tools at nine check points (both flavours): Package-X (reference, exact kinematics), LoopTools (lbl_feyncalc.wl), FormCalc +
#   LoopTools (lbl_formcalc.wl), COLLIER with the four-dimensional numerator plus the R2 vertex (lbl_collier.f90; also without
#   R2), MadLoop (|M|^2 per helicity; MadGraph includes the factor 1/2 of the identical final photons).
# - Low energy (electron loop): X against Euler-Heisenberg (Eq. (eq:lbllow)) and the O(k^6) terms of lbl_feyncalc.wl (c).
# - High energy: |X| against the massless amplitudes 8 M^(1) of Bern et al., JHEP 11 (2001) 031, Eq. (2.4) (their
#   t = (k1 - k4)^2 is our u).
# - Forward amplitude f(s) = (1/4) sum_{l1 l2} M(l1 l2 -> l1 l2)/alpha^2 (with the vectors of the note eps_4 -> -eps_2^* at
#   theta -> 0, so f = -(1/4) sum X): Im f = s sigma(gamma gamma -> e+ e-)/alpha^2 = 4 pi F(s) (Breit-Wheeler), Re f from the
#   twice-subtracted dispersion relation, and the sum rule f/s^2 -> 8 int ds F/s^3 = 11/45 (Eq. (eq:lblopt)).
# - Cross section (electron loop) against the low-energy limit 973/(10125 pi) alpha^4 omega^6/m^8 and the massless limit
#   alpha^4 J/(2 pi s); MadEvent's loop-induced cross section (benchmark, both flavours) at sqrt(s) = 1, 2, 3, 6.
# Writes results/lbl.csv and ../figs/lbl.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python lbl_numeric.py --points` writes the point files (run first), then without arguments
# after lbl_feyncalc.wl, lbl_formcalc.wl and the MadGraph runs (run_lbl_check.sh).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import re
import subprocess
import sys
from fractions import Fraction

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
ALPHA_B = 1 / (4 * math.pi)              # benchmark e = 1
ALPHA0 = 1 / 137.035999084               # physical alpha(0)
ME_MEV = 0.51099895000
HBARC_MEV_FM = 197.3269804
GEV2_PB = 0.3893793721e9                 # 1 GeV^-2 in pb
M_MU = 1.7
# check points: label, w = sqrt(s)/2, cos theta, sin theta (exact)
CHECK = [("P1", "1/20", "3/5", "4/5"), ("P2", "1/2", "-4/5", "3/5"), ("P3", "9/10", "5/13", "12/13"),
         ("P4", "6/5", "-12/13", "5/13"), ("P5", "2", "7/25", "24/25"), ("P6", "3", "-24/25", "7/25"),
         ("P7", "5", "20/29", "21/29"), ("P8", "25", "-8/17", "15/17"), ("P9", "50", "0", "1")]
LOW = [(f"L{k}", f"1/{2 ** k}", "3/5", "4/5") for k in range(1, 7)]                       # s = 1 ... 1/1024
HIGH = [(f"H{w}{'a' if c == '0' else 'b'}", str(w), c, sn) for w in (5, 15, 50, 150, 500) for c, sn in (("0", "1"), ("3/5", "4/5"))]
NFWD = 10 ** 6                           # forward points: 1 - cos theta = 2/(n^2 + 1)
FWD_W = ["1/2", "3/4", "9/8", "2", "5"]  # s = 1, 9/4, 81/16, 16, 100
FWD = [(f"F{i}", w, f"{NFWD ** 2 - 1}/{NFWD ** 2 + 1}", f"{2 * NFWD}/{NFWD ** 2 + 1}") for i, w in enumerate(FWD_W)]
NFWD_CL = 10 ** 4                        # COLLIER (double precision): 1 - cos theta = 2e-8
S_SCAN = np.geomspace(1e-2, 1e5, 71)     # |X| at 90 degrees (figure; below, double precision loses the one-flip amplitude)
S_FWD_SCAN = np.geomspace(0.05, 1e3, 61)
RS_XS = np.geomspace(0.2, 300, 41)       # sqrt(s)/m for the cross section (electron loop; COLLIER loses digits below)
RS_ME = [1.0, 2.0, 3.0, 6.0]             # MadEvent (benchmark, both flavours)


def gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return (b - a) / 2 * x + (a + b) / 2, (b - a) / 2 * w


def cos_nodes():
    """cos theta in [0, 1): 24 Gauss-Legendre nodes on [0, 0.9] and 24 in ln(1 - c) on [ln 1e-9, ln 0.1]"""
    c1, w1 = gl(24, 0.0, 0.9)
    y, wy = gl(24, math.log(1e-9), math.log(0.1))
    x = np.exp(y)
    return np.concatenate([c1, 1 - x]), np.concatenate([w1, wy * x])


C_NODES, C_WEIGHTS = cos_nodes()


def sval(w):
    return 4 * float(Fraction(w)) ** 2


if "--points" in sys.argv:
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    with open(os.path.join(HERE, "work", "lbl_points_exact.txt"), "w") as fh:
        # label w c sn flavours precision LoopTools
        fh.writelines(f"{p[0]} {p[1]} {p[2]} {p[3]} both {80 if p[0] == 'P1' else 30} 1\n" for p in CHECK)
        fh.writelines(f"{p[0]} {p[1]} {p[2]} {p[3]} e 80 1\n" for p in LOW)
        fh.writelines(f"{p[0]} {p[1]} {p[2]} {p[3]} e 30 1\n" for p in HIGH)
        fh.writelines(f"{p[0]} {p[1]} {p[2]} {p[3]} e 100 0\n" for p in FWD)
    cfwd = 1 - 2 / (NFWD_CL ** 2 + 1)
    with open(os.path.join(HERE, "work", "lbl_points.txt"), "w") as fh:
        fh.writelines(f"{sval(p[1]):.17e} {float(Fraction(p[2])):.17e} 2\n" for p in CHECK)
        fh.writelines(f"{sval(p[1]):.17e} {float(Fraction(p[2])):.17e} 1\n" for p in LOW + HIGH[:6])
        fh.writelines(f"{sval(w):.17e} {cfwd:.17e} 1\n" for w in FWD_W)
        fh.writelines(f"{s:.17e} 0.0 1\n" for s in S_SCAN)
        fh.writelines(f"{s:.17e} {cfwd:.17e} 1\n" for s in S_FWD_SCAN)
        fh.writelines(f"{rs * rs:.17e} {c:.17e} 1\n" for rs in RS_XS for c in C_NODES)
        fh.writelines(f"{rs * rs:.17e} {c:.17e} 2\n" for rs in RS_ME for c in C_NODES)
    with open(os.path.join(HERE, "work", "lbl_ml_points.input"), "w") as fh:
        fh.write(f"{len(CHECK)}\n")
        for p in CHECK:
            w, c, sn = (float(Fraction(x)) for x in p[1:4])
            for v in ((w, 0, 0, w), (w, 0, 0, -w), (w, w * sn, 0, w * c), (w, -w * sn, 0, -w * c)):
                fh.write("%.17e %.17e %.17e %.17e\n" % v)
    print("wrote work/lbl_points_exact.txt, work/lbl_points.txt, work/lbl_ml_points.input")
    sys.exit(0)

# %% [markdown]
# ## Reading the tools

# %%
HELS = [tuple(1 if (h >> (3 - i)) & 1 else -1 for i in range(4)) for h in range(16)]   # MadGraph's order


def read_csv(name, sub="results"):
    with open(os.path.join(HERE, sub, name)) as fh:
        return list(csv.DictReader(fh))


def cplx(r, re_key, im_key):
    return complex(float(r[re_key]), float(r[im_key]))


# COLLIER's values at all points (about 2700 points x 16 helicities, 9 MB) stay in work/; results/lbl.csv has the comparisons
subprocess.run(["./work/lbl_collier", "work/lbl_points.txt", "work/lbl_collier.csv"], cwd=HERE, check=True, capture_output=True)
CL = read_csv("lbl_collier.csv", sub="work")
FC = read_csv("lbl_feyncalc.csv")
FM = read_csv("lbl_formcalc.csv")


def key(s, c):
    return (round(float(s), 9), round(float(c), 12))


def by_point(rows, fields):
    """{(s, c): {helicity: tuple of values}}; the first row of a point/helicity wins"""
    out = {}
    for r in rows:
        k = key(r["s"], r["cos"])
        lam = tuple(int(r[f"l{i}"]) for i in range(1, 5))
        out.setdefault(k, {}).setdefault(lam, tuple(f(r) for f in fields))
    return out


cl = by_point(CL, [lambda r: cplx(r, "re_e", "im_e"), lambda r: cplx(r, "re_mu", "im_mu"), lambda r: complex(float(r["re_r2"]), float(r["im_r2"])),
                   lambda r: float(r["cdiff"])])
fc = by_point(FC, [lambda r: cplx(r, "re_px_e", "im_px_e"), lambda r: cplx(r, "re_lt_e", "im_lt_e") if r["re_lt_e"] != "nan" else None,
                   lambda r: cplx(r, "re_px_mu", "im_px_mu"), lambda r: cplx(r, "re_lt_mu", "im_lt_mu") if r["re_lt_mu"] != "nan" else None])
fm = by_point(FM, [lambda r: cplx(r, "re_e", "im_e"), lambda r: cplx(r, "re_mu", "im_mu")])


def run_madloop():
    base = os.path.join(HERE, "work", "ml_lbl", "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    with open(os.path.join(HERE, "work", "lbl_ml_points.input")) as src, open(os.path.join(d, "points.input"), "w") as dst:
        dst.write(src.read())
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        w = line.split()
        if w and w[0] == "HEL":
            res[(int(w[1]) - 1, tuple(int(x) for x in w[3:7]))] = float(w[8])
    return res


# %% [markdown]
# ## Inspect: the diagrams that MadLoop evaluates (drawn when MadGraph wrote the standalone code)

# %%
if INTERACTIVE:
    import shutil
    import tempfile
    from IPython.display import Image, display
    GS = shutil.which("gs") or "/opt/homebrew/bin/gs"
    with open(os.path.join(HERE, "work", "lbl_mg5.log")) as fh:
        print("ml_lbl:", next(line.strip() for line in fh if "Contributing diagrams" in line))
    base = os.path.join(HERE, "work", "ml_lbl", "SubProcesses")
    dML = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    tmpML = tempfile.mkdtemp()
    subprocess.run([GS, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r70",
                    "-sOutputFile=" + os.path.join(tmpML, "loop_matrix_%02d.png"), os.path.join(dML, "loop_matrix.ps")], check=True)
    for png in sorted(f for f in os.listdir(tmpML) if f.startswith("loop_matrix_")):
        display(Image(filename=os.path.join(tmpML, png)))

# %% [markdown]
# ## MadLoop per helicity at the check points

# %%
ML = run_madloop()

# %% [markdown]
# ## Tools at the check points (both flavours)

# %%
rows = []
print(f"{'pt':>3} {'s':>7} {'cos':>7} {'sum|X|^2/16':>14} {'LoopTools':>10} {'FormCalc':>10} {'COLLIER':>10} {'no R2':>8} {'MadLoop':>10} {'C pairs':>8}")
dev_tools = {}
for i, p in enumerate(CHECK):
    s, c = sval(p[1]), float(Fraction(p[2]))
    k = key(s, c)
    ref = {lam: fc[k][lam][0] + fc[k][lam][2] for lam in HELS}
    norm = max(abs(v) for v in ref.values())
    d = {"LoopTools": max(abs(fc[k][l][1] + fc[k][l][3] - ref[l]) for l in HELS) / norm,
         "FormCalc": max(abs(fm[k][l][0] + fm[k][l][1] - ref[l]) for l in HELS) / norm,
         "COLLIER": max(abs(cl[k][l][0] + cl[k][l][1] - ref[l]) for l in HELS) / norm,
         "COLLIER without R2": max(abs(cl[k][l][0] + cl[k][l][1] - 2 * cl[k][l][2] - ref[l]) for l in HELS) / norm,
         "MadLoop": max(abs(2 * ML[(i, l)] / ALPHA_B ** 4 - abs(ref[l]) ** 2) for l in HELS) / norm ** 2}
    cdiff = max(cl[k][l][3] for l in HELS)
    msq = sum(abs(v) ** 2 for v in ref.values()) / 16
    for t, v in d.items():
        dev_tools[t] = max(dev_tools.get(t, 0), v)
    print(f"{p[0]:>3} {s:7.4g} {c:7.4f} {msq:14.8g} " + " ".join(f"{d[t]:10.1e}" for t in ("LoopTools", "FormCalc", "COLLIER")) +
          f" {d['COLLIER without R2']:8.1e} {d['MadLoop']:10.1e} {cdiff:8.1e}")
    rows.append(["check", p[0], s, c, msq] + [d[t] for t in ("LoopTools", "FormCalc", "COLLIER", "COLLIER without R2", "MadLoop")] + [cdiff])
print("max deviation (relative to max_h |X_h|; MadLoop: |X|^2 relative to max |X|^2):", {t: f"{v:.1e}" for t, v in dev_tools.items()})
# parity and Bose symmetry of the reference: |X(l)| = |X(-l)|
par = max(abs(abs(fc[key(sval(p[1]), float(Fraction(p[2])))][l][0]) - abs(fc[key(sval(p[1]), float(Fraction(p[2])))][tuple(-x for x in l)][0]))
          for p in CHECK for l in HELS)
print(f"parity |X(l)| - |X(-l)| (Package-X, electron): max {par:.1e}")

# %% [markdown]
# ## Low energy: Euler-Heisenberg and the O(k^6) terms (electron loop, m = 1)

# %%
G = np.diag([1.0, -1, -1, -1])
EPS4 = np.zeros((4, 4, 4, 4))
for perm in __import__("itertools").permutations(range(4)):
    EPS4[perm] = np.linalg.det(np.eye(4)[list(perm)])


def polvec(ct, st, cph, lam):
    return np.concatenate([[0], (-lam * np.array([ct * cph, 0, -st]) - 1j * np.array([0, cph, 0])) / math.sqrt(2)])


def vectors(s, c, lam):
    w, sn = math.sqrt(s) / 2, math.sqrt(max(0.0, 1 - c * c))
    q = [np.array([w, 0, 0, w]), np.array([w, 0, 0, -w]), -np.array([w, w * sn, 0, w * c]), -np.array([w, -w * sn, 0, -w * c])]
    e = [polvec(1, 0, 1, lam[0]), polvec(-1, 0, 1, lam[1]), np.conj(polvec(c, sn, 1, lam[2])), np.conj(polvec(-c, sn, -1, lam[3]))]
    return q, e


def x_eh(s, c, lam):
    """Euler-Heisenberg, X = 8 c1 sum (f.f)(f.f) + 8 c2 sum (f.ft)(f.ft), c1 = 1/90, c2 = 7/360 (m = 1)"""
    q, e = vectors(s, c, lam)
    F = [np.outer(q[i], e[i]) - np.outer(e[i], q[i]) for i in range(4)]
    Fl = [G @ f @ G for f in F]
    Ft = [0.5 * np.einsum("abcd,cd->ab", EPS4, f) for f in Fl]
    ff = lambda i, j: np.sum(Fl[i] * F[j])
    fd = lambda i, j: np.sum(Fl[i] * Ft[j])
    P = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    return 8 / 90 * sum(ff(*a) * ff(*b) for a, b in P) + 8 * 7 / 360 * sum(fd(*a) * fd(*b) for a, b in P)


def mand(s, c):
    return s, -s / 2 * (1 - c), -s / 2 * (1 + c)


# O(k^4) and O(k^6) in the conventions of the note (lbl_feyncalc.wl (c)), m = 1
CLASSES = {(1, 1, 1, 1): "++++", (1, -1, 1, -1): "+-+-", (1, -1, -1, 1): "+--+", (1, 1, -1, -1): "++--", (1, 1, 1, -1): "+++-"}


def x46(lam, s, c):
    s, t, u = mand(s, c)
    return {(1, 1, 1, 1): (-11 / 45 * s * s, -4 / 315 * s ** 3), (1, -1, 1, -1): (-11 / 45 * u * u, -4 / 315 * u ** 3),
            (1, -1, -1, 1): (-11 / 45 * t * t, -4 / 315 * t ** 3), (1, 1, -1, -1): ((s * s + t * t + u * u) / 15, 2 / 63 * s * t * u),
            (1, 1, 1, -1): (0.0, s * t * u / 315)}[lam]


print(f"{'pt':>3} {'s':>9} " + " ".join(f"{n:>22}" for n in CLASSES.values()) + "   (X/X_EH - 1)/(X_6/X_EH), +++-: X/X_6 - 1")
low_rows = {}
for p in LOW:
    s, c = sval(p[1]), float(Fraction(p[2]))
    k = key(s, c)
    vals = []
    for lam in CLASSES:
        x = fc[k][lam][0]
        x4, x6 = x46(lam, s, c)
        assert abs(x_eh(s, c, lam) - x4) <= 1e-12 * max(abs(x4), s * s)
        r = (x / x6 - 1) if x4 == 0 else ((x / x4 - 1) / (x6 / x4))
        vals.append(r)
    low_rows[p[0]] = (s, vals)
    print(f"{p[0]:>3} {s:9.3e} " + " ".join(f"{(v.real if abs(v.imag) < 1e-12 else v):22.12f}" for v in vals))
    rows.append(["low", p[0], s, c] + [v.real for v in vals])
# the same ratio from COLLIER and LoopTools (double precision) at the smallest s
for tool, idx in (("LoopTools", 1), ("COLLIER", None)):
    s, c = sval(LOW[-1][1]), 0.6
    k = key(s, c)
    x = fc[k][(1, 1, 1, 1)][1] if idx else cl[k][(1, 1, 1, 1)][0]
    print(f"  {tool} at s = {s:.3e}: X(++++)/X_EH - 1 = {(x / x46((1, 1, 1, 1), s, c)[0] - 1).real:.6e} "
          f"(Package-X {(fc[k][(1, 1, 1, 1)][0] / x46((1, 1, 1, 1), s, c)[0] - 1).real:.6e})")

# %% [markdown]
# ## High energy: the massless amplitudes of Bern et al.

# %%
def bern(lam, s, c, lib=math):
    """8 M^(1) of Bern et al. (2001), Eq. (2.4); their t = (k1 - k4)^2 = our u (lib = mp for mpmath arguments)"""
    tB, uB = -s / 2 * (1 + c), -s / 2 * (1 - c)
    L = lib.log

    def mpppp(s, t, u):
        return -0.5 * (t * t + u * u) / s ** 2 * (L(t / u) ** 2 + lib.pi ** 2) - (t - u) / s * L(t / u) - 1

    def mpmmp(s, t, u):
        return (-0.5 * (t * t + s * s) / u ** 2 * L(-t / s) ** 2 - (t - s) / u * L(-t / s) - 1
                - 1j * lib.pi * ((t * t + s * s) / u ** 2 * L(-t / s) + (t - s) / u))

    l = tuple(lam)
    if l in ((1, 1, 1, 1), (-1, -1, -1, -1)):
        return 8 * mpppp(s, tB, uB)
    if l in ((1, -1, -1, 1), (-1, 1, 1, -1)):
        return 8 * mpmmp(s, tB, uB)
    if l in ((1, -1, 1, -1), (-1, 1, -1, 1)):
        return 8 * mpmmp(s, uB, tB)
    return 8.0


print(f"{'pt':>5} {'s':>8} {'cos':>4} " + " ".join(f"{n:>9}" for n in CLASSES.values()) + "   |X|/|8 M^(1)| - 1 (Package-X); LoopTools, COLLIER max dev from Package-X")
for p in HIGH:
    s, c = sval(p[1]), float(Fraction(p[2]))
    k = key(s, c)
    devs = [abs(fc[k][lam][0]) / abs(bern(lam, s, c)) - 1 for lam in CLASSES]
    norm = max(abs(fc[k][l][0]) for l in HELS)
    dlt = max(abs(fc[k][l][1] - fc[k][l][0]) for l in HELS) / norm
    dcl = max(abs(cl[k][l][0] - fc[k][l][0]) for l in HELS) / norm if k in cl else float("nan")
    print(f"{p[0]:>5} {s:8.0e} {c:4.1f} " + " ".join(f"{d:9.2e}" for d in devs) + f"   {dlt:8.1e} {dcl:8.1e}")
    rows.append(["high", p[0], s, c] + devs + [dlt, dcl])


def jcoef():
    """J = int_{-1}^{1} dc [|M--++|^2 + 4|M-+++|^2 + |M++++|^2 + |M+--+|^2 + |M+-+-|^2] (massless M^(1), s = 1), written with
    x = 1 - c (t_B = -(2 - x)/2, u_B = -x/2) so that ln(-t_B) = log1p(-x/2) keeps its digits at x -> 0"""
    def f(x):
        tB, uB = -(2 - x) / 2, -x / 2
        lt, lu = mp.log1p(-x / 2), mp.log(x / 2)          # ln(-t_B/s), ln(-u_B/s)
        lr = lt - lu                                       # ln(t_B/u_B)
        pppp = -0.5 * (tB ** 2 + uB ** 2) * (lr ** 2 + mp.pi ** 2) - (tB - uB) * lr - 1
        pmmp = -0.5 * (tB ** 2 + 1) / uB ** 2 * lt ** 2 - (tB - 1) / uB * lt - 1 - 1j * mp.pi * ((tB ** 2 + 1) / uB ** 2 * lt + (tB - 1) / uB)
        pmpm = -0.5 * (uB ** 2 + 1) / tB ** 2 * lu ** 2 - (uB - 1) / tB * lu - 1 - 1j * mp.pi * ((uB ** 2 + 1) / tB ** 2 * lu + (uB - 1) / tB)
        return 1 + 4 + abs(pppp) ** 2 + abs(pmmp) ** 2 + abs(pmpm) ** 2
    return 2 * mp.quad(f, [0, mp.mpf("1e-6"), mp.mpf("1e-3"), mp.mpf("0.1"), 1])


J = float(jcoef())
print(f"massless limit: s sigma/alpha^4 -> J/(2 pi) = {J / (2 * math.pi):.10f} (J = {J:.10f})")

# %% [markdown]
# ## Forward amplitude: optical theorem and dispersion relation

# %%
def F_bw(s):
    """s sigma(gamma gamma -> f fbar)/(4 pi alpha^2), m = 1 (Breit-Wheeler)"""
    s = mp.mpf(s)
    if s <= 4:
        return mp.mpf(0)
    r = 4 / s
    b = mp.sqrt(1 - r)
    return (1 + r - r * r / 2) * mp.log((1 + b) / (1 - b)) - b * (1 + r)


def re_f_disp(s):
    """Re f(s) = (2 s^2/pi) PV int_4^inf ds' 4 pi F(s')/(s' (s'^2 - s^2)) = 4 s [PV int g/(s' - s) - int g/(s' + s)], g = F/s'"""
    s = mp.mpf(s)
    g = lambda x: F_bw(x) / x
    second = mp.quad(lambda x: g(x) / (x + s), [4, 8, 40, mp.inf])
    if s <= 4:
        first = mp.quad(lambda x: g(x) / (x - s), [4, 8, 40, mp.inf])
    else:
        cc = 2 * s - 4                    # symmetric interval around s: the PV of 1/(x - s) vanishes there
        first = mp.quad(lambda x: (g(x) - g(s)) / (x - s), [4, s, cc]) + mp.quad(lambda x: g(x) / (x - s), [cc, 2 * cc, mp.inf])
    return 4 * s * (first - second)


sumrule = 8 * mp.quad(lambda x: F_bw(x) / x ** 3, [4, 8, 40, mp.inf])
print(f"sum rule 8 int F/s^3 = {mp.nstr(sumrule, 20)}, 11/45 = {mp.nstr(mp.mpf(11) / 45, 20)}")


def fwd(tab, k, idx):
    return -0.25 * sum(tab[k][(l1, l2, l1, l2)][idx] for l1 in (-1, 1) for l2 in (-1, 1))


print(f"{'pt':>3} {'s':>8} {'Re f (dispersion)':>22} {'Im f = 4 pi F':>20} {'Package-X Re, Im dev':>22} {'COLLIER Re, Im dev':>22}")
cfwd_cl = 1 - 2 / (NFWD_CL ** 2 + 1)
for p, w in zip(FWD, FWD_W):
    s = sval(w)
    rd, im = re_f_disp(s), 4 * mp.pi * F_bw(s)
    fp = fwd(fc, key(s, float(Fraction(p[2]))), 0)
    fcl = fwd(cl, key(s, cfwd_cl), 0)
    dp = (abs(fp.real - float(rd)) / abs(float(rd)), abs(fp.imag - float(im)) / max(abs(float(im)), 1))
    dc = (abs(fcl.real - float(rd)) / abs(float(rd)), abs(fcl.imag - float(im)) / max(abs(float(im)), 1))
    print(f"{p[0]:>3} {s:8.4g} {mp.nstr(rd, 16):>22} {mp.nstr(im, 14):>20} {dp[0]:10.1e} {dp[1]:10.1e} {dc[0]:10.1e} {dc[1]:10.1e}")
    rows.append(["forward", p[0], s, float(rd), float(im)] + list(dp) + list(dc))

# %% [markdown]
# ## Cross section

# %%
def sigma_hat(s, nf_mass=None):
    """sigma/(alpha^4/m^2) of the electron loop from COLLIER: (1/(128 pi s)) int_0^1 dc sum_h |X_h|^2; with nf_mass, both flavours"""
    tot = 0.0
    for c, wt in zip(C_NODES, C_WEIGHTS):
        k = key(s, c)
        tot += wt * sum(abs(cl[k][l][0] + (cl[k][l][1] if nf_mass else 0)) ** 2 for l in HELS)
    return tot / (128 * math.pi * s)


SIG = np.array([sigma_hat(rs * rs) for rs in RS_XS])


def sigma46(s):
    """the same with the amplitudes to O(k^6) (lbl_feyncalc.wl (c)): four classes twice, the eight one-flip ones |stu|/315"""
    tot = 0.0
    for c, wt in zip(C_NODES, C_WEIGHTS):
        ss, tt, uu = mand(s, c)
        tot += wt * (2 * sum(abs(sum(x46(l, s, c))) ** 2 for l in list(CLASSES)[:4]) + 8 * (ss * tt * uu / 315) ** 2)
    return tot / (128 * math.pi * s)
sig_eh = lambda rs: 973 / (10125 * math.pi) * (rs / 2) ** 6
sig_ml = lambda rs: J / (2 * math.pi * rs * rs)
ipk = int(np.argmax(SIG))
# parabola through the three grid points around the maximum (in ln sqrt(s))
xl = np.log(RS_XS[ipk - 1:ipk + 2])
cf = np.polyfit(xl, SIG[ipk - 1:ipk + 2], 2)
rs_pk = math.exp(-cf[1] / (2 * cf[0]))
sig_pk = float(np.polyval(cf, math.log(rs_pk)))
ub_unit = ALPHA0 ** 4 * (HBARC_MEV_FM / ME_MEV) ** 2 * 1e-26 / 1e-30     # alpha^4/m_e^2 in microbarn
for i in range(4):
    print(f"sigma at sqrt(s) = {RS_XS[i]:.4f}: ratio to Euler-Heisenberg {SIG[i] / sig_eh(RS_XS[i]):.6f}, "
          f"to the O(k^6) amplitudes {SIG[i] / sigma46(RS_XS[i] ** 2):.8f}")
for i in (-4, -3, -2, -1):
    print(f"sigma at sqrt(s) = {RS_XS[i]:.1f}: ratio to the massless limit {SIG[i] / sig_ml(RS_XS[i]):.6f}")
print(f"peak at sqrt(s) = {rs_pk:.4f} m, sigma = {sig_pk:.6f} alpha^4/m^2 = {sig_pk * ub_unit:.4f} microbarn (physical alpha, m_e)")
for rs, sg in zip(RS_XS, SIG):
    rows.append(["sigma", "", rs, sg])
# MadEvent (benchmark: e = 1, m_e = 1 GeV, m_mu = 1.7 GeV): three runs per energy (seeds 1, 2, 3); the quoted error of a
# single run is not reliable, so the mean is compared with the spread of the three (standard error of the mean)
me_xs = []
with open(os.path.join(HERE, "work", "lbl_me_launch.log")) as fh:
    for line in fh:
        m = re.search(r"Cross-section :\s+(\S+)\s+\+-\s+(\S+)\s+pb", line)
        if m:
            me_xs.append((float(m.group(1)), float(m.group(2))))
assert len(me_xs) == 3 * len(RS_ME)
print(f"{'sqrt s':>6} {'ours (pb)':>12} {'MadEvent runs (pb, quoted error)':>48} {'mean':>10} {'sem':>6} {'pull':>6}")
for i, rs in enumerate(RS_ME):
    runs = me_xs[3 * i:3 * i + 3]
    ours = sigma_hat(rs * rs, nf_mass=True) * ALPHA_B ** 4 * GEV2_PB
    vals = np.array([v for v, _ in runs])
    mean, sem = vals.mean(), vals.std(ddof=1) / math.sqrt(3)
    print(f"{rs:6.1f} {ours:12.4f} " + " ".join(f"{v:9.2f}({e:5.2f})" for v, e in runs) + f" {mean:10.2f} {sem:6.2f} {(mean - ours) / sem:6.2f}")
    rows.append(["madevent", "", rs, ours] + [x for r in runs for x in r] + [mean, sem, (mean - ours) / sem, (mean - ours) / ours])

with open(os.path.join(HERE, "results", "lbl.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(["kind", "label", "x1", "x2", "..."])
    wr.writerows(rows)
print("wrote results/lbl.csv")

# %% [markdown]
# ## Figure

# %%
COLORS = {"a": "#2a78d6", "b": "#eb6834", "c": "#1baf7a"}     # validated categorical slots 1-3 (dataviz palette)
fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.6))
ax = axes[0]
ax.plot(RS_XS, SIG, color=COLORS["a"], lw=2, label="one loop (COLLIER)")
rlo, rhi = np.geomspace(0.1, 1.5, 20), np.geomspace(6, 600, 20)
ax.plot(rlo, [sig_eh(x) for x in rlo], color=COLORS["c"], lw=1.6, ls="--", label="Euler–Heisenberg", zorder=3)
ax.plot(rhi, [sig_ml(x) for x in rhi], color=COLORS["b"], lw=1.6, ls=":", label=r"massless, $J/(2\pi s)$", zorder=3)
ax.axvline(rs_pk, color="0.6", lw=0.8, ls=":")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1e-9, 1)
ax.set_xlabel(r"$\sqrt{s}/m$")
ax.set_ylabel(r"$\sigma\ [\alpha^4/m^2]$")
ax.legend(frameon=False, fontsize=8, loc="lower center")
ax = axes[1]
lab = {(1, 1, 1, 1): r"$++\to++$", (1, 1, -1, -1): r"$++\to--$", (1, -1, -1, 1): r"$+-\to-+$", (1, 1, 1, -1): r"$++\to+-$"}
cols = [COLORS["a"], COLORS["b"], COLORS["c"], "0.35"]
for (lam, name), col in zip(lab.items(), cols):
    ax.plot(S_SCAN, [abs(cl[key(s, 0.0)][lam][0]) for s in S_SCAN], color=col, lw=1.8, label=name)
    sl = np.geomspace(1e-3, 0.3, 20)
    ax.plot(sl, [abs(sum(x46(lam, s, 0.0))) for s in sl], color=col, lw=1, ls="--")
    sh = S_SCAN[S_SCAN > 300]
    ax.plot(sh, [abs(bern(lam, s, 0.0)) for s in sh], color=col, lw=1, ls=":")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1e-3, 2e5)
ax.set_ylim(1e-12, 100)
ax.set_xlabel(r"$s/m^2$  ($\theta=90^\circ$)")
ax.set_ylabel(r"$|M|/\alpha^2$")
ax.legend(frameon=False, fontsize=8, loc="lower right")
ax = axes[2]
fsc = [fwd(cl, key(s, cfwd_cl), 0) for s in S_FWD_SCAN]
ax.plot(S_FWD_SCAN, [f.real / s for f, s in zip(fsc, S_FWD_SCAN)], color=COLORS["a"], lw=2, label=r"Re $f/s$")
ax.plot(S_FWD_SCAN, [f.imag / s for f, s in zip(fsc, S_FWD_SCAN)], color=COLORS["b"], lw=2, label=r"Im $f/s$")
sd = S_FWD_SCAN[::4]
ax.plot(sd, [float(re_f_disp(s)) / s for s in sd], ls="none", marker="o", ms=4, color="0.3", label="dispersion")
ax.plot(sd, [float(4 * mp.pi * F_bw(s)) / s for s in sd], ls="none", marker="s", ms=4, mfc="none", color="0.3",
        label=r"$4\pi F$")
ax.set_xscale("log")
ax.set_xlabel(r"$s/m^2$")
ax.set_ylabel(r"forward amplitude $f/s$")
ax.legend(frameon=False, fontsize=8, loc="upper left")
for ax in axes:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(alpha=0.3, lw=0.5)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "lbl.pdf"))
print("wrote ../figs/lbl.pdf")
if INTERACTIVE:
    plt.show()
