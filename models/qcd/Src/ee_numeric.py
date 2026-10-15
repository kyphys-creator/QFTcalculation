# %% [markdown]
# # Step (8): e+ e- -> hadrons -- MadGraph against the D-dimensional sum, the optical theorem and the thrust distribution
#
# Research note models/qcd, step (8), Eqs. (rr), (rmass), (thrust).  e = 1 (alpha = 1/(4 pi)), alpha_s = 0.118, m_t = 1, SU(3).
# (a) massless: K = sigma_NLO/sigma_0 of aMC@NLO (e+ e- > u u~ [QCD], sqrt(s) = 10) against 1 + 3 C_F alpha_s/(4 pi) = 1 + alpha_s/pi
#     (ee_feyncalc.wl: virtual + real in D dimensions; ee_optical.wl: Im of the two-loop photon self-energy), with the exact LO
#     sigma_0 = N_c Q_u^2 4 pi alpha^2/(3 s) (GeV^-2 -> pb: 0.3893794e9).
# (b) massive: K(beta) of e+ e- > t t~ [QCD] against 1 + C_F (alpha_s/pi) Delta^(1)(beta), Delta^(1) from AMFlow (ee_amflow.wl) and the closed
#     form; sigma_0 = N_c Q_t^2 (4 pi alpha^2/(3 s)) beta (3 - beta^2)/2; the threshold form pi^2/(2 beta) - 4 (Coulomb).
# (c) thrust: MadEvent's e+ e- > u u~ g events with s_ij > 0.01 s (T < 0.99) against (1/sigma_0) dsigma/dT = C_F alpha_s/(2 pi) f(T),
#     f(T) = 2 (3T^2 - 3T + 2)/(T(1-T)) ln((2T-1)/(1-T)) - 3 (3T-2)(2-T)/(1-T), and the total against C_F alpha_s/(2 pi) F(y).
# Writes results/ee_comparison.csv and ../figs/ee_rratio.pdf.  Usage (from Src/, after ee_mg5.py and ee_amflow.wl):
#   ~/miniforge3/envs/qft/bin/python ee_numeric.py.   Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import sys

import numpy as np
from mpmath import mp, mpf, log as mlog, polylog
from scipy.integrate import quad

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
mp.dps = 30
CF, NC, AS = 4 / 3, 3, 0.118
ALPHA = 1 / (4 * math.pi)
GEV2PB = 0.3893794e9
Y_CUT = 0.01


def read(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


def sigma0(s, q, beta=1.0):
    return NC * q * q * 4 * math.pi * ALPHA ** 2 / (3 * s) * beta * (3 - beta ** 2) / 2 * GEV2PB


def delta1(b):
    """Hoang-Teubner Eqs. (49), (50): Delta^(1) = r1/r0"""
    b = mpf(b)
    p = (1 - b) / (1 + b)
    bb = (1 + b ** 2) * (2 * mlog(1 - p) * mlog(p) + mlog(1 + p) * mlog(p) + 2 * polylog(2, p) + polylog(2, p ** 2)) - 2 * b * (2 * mlog(1 - p) + mlog(1 + p))
    r1 = (3 - b ** 2) / 2 * bb - (1 - b) / 16 * (33 - 39 * b - 17 * b ** 2 + 7 * b ** 3) * mlog(p) + mpf(3) / 8 * b * (5 - 3 * b ** 2)
    return float(r1 / (b * (3 - b ** 2) / 2))


mg = read("ee_mg5.csv")


def seeds(proc, key=None):
    """mean K-factor input over the seeds of one point: (mean sigma, error of the mean from the scatter, MadGraph's error/sqrt(n), n)"""
    xs = [x for x in mg if x["process"] == proc and (key is None or abs(float(x["beta_or_y"]) - key) < 1e-9)]
    v = np.array([float(x["sigma_pb"]) for x in xs])
    e = np.array([float(x["error_pb"]) for x in xs])
    n = len(v)
    return v.mean(), v.std(ddof=1) / math.sqrt(n), math.sqrt(np.sum(e ** 2)) / n, n, float(xs[0]["sqrt_s"])
amf = read("ee_amflow.csv")
rows = []
mg, amf[:2]                               # inspect

# %% [markdown]
# ## (a) massless quarks: R = R_0 (1 + alpha_s/pi)

# %%
m_, ds_, dm_, n_, rs_ = seeds("uu_nlo")
s = rs_ ** 2
k, dk, dkm = m_ / sigma0(s, 2 / 3), ds_ / sigma0(s, 2 / 3), dm_ / sigma0(s, 2 / 3)
kpred = 1 + 3 * CF * AS / (4 * math.pi)
print(f"(a) u ubar, sqrt(s) = {rs_:g}: sigma_0 = {sigma0(s, 2 / 3):.6e} pb;  aMC@NLO K = {k:.6f} +- {dk:.6f} (scatter of {n_} seeds; MadGraph's "
      f"error {dkm:.6f});  1 + alpha_s/pi = {kpred:.6f};  (K - pred)/error = {(k - kpred) / dk:+.2f}")
rows.append(["a_massless_K", rs_, n_, k, dk, kpred, (k - kpred) / dk])

# %% [markdown]
# ## (b) the heavy quark: Delta^(1)(beta), the Coulomb singularity, aMC@NLO

# %%
for x in amf:
    b = float(x["beta"])
    print(f"(b) beta = {b:.1f}: Delta^(1) AMFlow {float(x['delta1_amflow']):.15f}, closed form {delta1(b):.15f}, pi^2/(2 beta) - 4 = {math.pi ** 2 / (2 * b) - 4:.6f}")
    rows.append(["b_delta1_amflow", b, "", float(x["delta1_amflow"]), 0, delta1(b), abs(float(x["delta1_amflow"]) - delta1(b))])
for b in sorted({float(x["beta_or_y"]) for x in mg if x["process"] == "tt_nlo"}):
    m_, ds_, dm_, n_, rs = seeds("tt_nlo", b)
    s0 = sigma0(rs * rs, 2 / 3, b)
    k, dk, dkm = m_ / s0, ds_ / s0, dm_ / s0
    kpred = 1 + CF * AS / math.pi * delta1(b)
    print(f"(b) t tbar beta = {b:.1f} (sqrt(s) = {rs:.6f} m): aMC@NLO K = {k:.6f} +- {dk:.6f} (scatter of {n_} seeds; MadGraph's error {dkm:.6f});  "
          f"1 + C_F (alpha_s/pi) Delta^(1) = {kpred:.6f};  (K - pred)/error = {(k - kpred) / dk:+.2f}")
    rows.append(["b_tt_K", b, rs, k, dk, kpred, (k - kpred) / dk])
for b in (0.1, 0.01, 0.001):
    print(f"(b) threshold: beta = {b:g}: Delta^(1) - (pi^2/(2 beta) - 4) = {delta1(b) - (math.pi ** 2 / (2 * b) - 4):+.6f}  (-> 0 like beta)")

# %% [markdown]
# ## (c) the thrust distribution

# %%
def fthrust(t):
    return 2 * (3 * t * t - 3 * t + 2) / (t * (1 - t)) * math.log((2 * t - 1) / (1 - t)) - 3 * (3 * t - 2) * (2 - t) / (1 - t)


def fy(y):
    return float((3 - 6 * y) * mlog(y / (1 - 2 * y)) + 2 * mlog(y / (1 - y)) ** 2 + mpf(5) / 2 - 6 * y - mpf(9) / 2 * y ** 2
                 + 4 * polylog(2, y / (1 - y)) - mp.pi ** 2 / 3)


ts = np.loadtxt(os.path.join(HERE, "work", "ee_mg5_thrust.txt"))
r = next(x for x in mg if x["process"] == "uug_lo_ycut")
s = float(r["sqrt_s"]) ** 2
sig, dsig = float(r["sigma_pb"]), float(r["error_pb"])
norm = CF * AS / (2 * math.pi)
tot_pred = norm * fy(Y_CUT)
print(f"(c) MadEvent: {len(ts)} events, T in [{ts.min():.4f}, {ts.max():.4f}];  sigma/sigma_0 = {sig / sigma0(s, 2 / 3):.6f} +- {dsig / sigma0(s, 2 / 3):.6f};  "
      f"C_F alpha_s/(2 pi) F(y) = {tot_pred:.6f}")
rows.append(["c_threejet_total", Y_CUT, "", sig / sigma0(s, 2 / 3), dsig / sigma0(s, 2 / 3), tot_pred, (sig / sigma0(s, 2 / 3) - tot_pred) / (dsig / sigma0(s, 2 / 3))])
edges = np.concatenate([np.linspace(2 / 3, 0.95, 18), [0.97, 0.98, 0.99]])
cnt, _ = np.histogram(ts, bins=edges)
shape_pred = np.array([quad(fthrust, a, b, limit=200)[0] for a, b in zip(edges[:-1], edges[1:])]) / fy(Y_CUT)
frac = cnt / len(ts)
err = np.sqrt(cnt) / len(ts)
chi2 = float(np.sum(((frac - shape_pred) / err) ** 2))
print(f"(c) shape: {len(cnt)} bins, chi^2 = {chi2:.1f} for {len(cnt) - 1} degrees of freedom;  largest |pull| {np.max(np.abs((frac - shape_pred) / err)):.2f}")
for a, b, f, e, p in zip(edges[:-1], edges[1:], frac, err, shape_pred):
    rows.append(["c_thrust_bin", a, b, f, e, p, (f - p) / e])
with open(os.path.join(HERE, "results", "ee_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["kind", "x1", "x2", "value", "error", "prediction", "pull_or_absdiff"])
    w.writerows(rows)
print("wrote results/ee_comparison.csv")

# %% [markdown]
# ## Figure: Delta^(1)(beta) and the thrust distribution

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))
ax = axes[0]
bs = np.linspace(0.04, 0.995, 300)
ax.plot(bs, [delta1(b) for b in bs], color="C0", lw=1, label=r"closed form")
ax.plot(bs, math.pi ** 2 / (2 * bs) - 4, color="C1", lw=1, ls="--", label=r"$\pi^2/(2\beta)-4$")
ax.axhline(0.75, color="0.5", lw=0.6, ls=":")
ax.text(0.06, 0.82, r"$3/4$ (massless)", ha="left", fontsize=7, color="0.35")
ax.plot([float(x["beta"]) for x in amf], [float(x["delta1_amflow"]) for x in amf], ls="none", marker="o", ms=3.6, color="C0", label="AMFlow (optical)")
tt = [x for x in rows if x[0] == "b_tt_K"]
ax.errorbar([x[1] for x in tt], [(x[3] - 1) / (CF * AS / math.pi) for x in tt], yerr=[x[4] / (CF * AS / math.pi) for x in tt], ls="none",
            marker="s", ms=3.2, color="C2", label="aMC@NLO")
ax.set_yscale("log")
ax.set_ylim(0.5, 80)
ax.set_xlim(0, 1)
ax.set_xlabel(r"$\beta$")
ax.set_ylabel(r"$\Delta^{(1)}(\beta)$")
ax.set_title(r"$e^+e^-\to Q\bar Q$: $R=R_0[1+C_F\frac{\alpha_s}{\pi}\Delta^{(1)}]$", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper right")
ax = axes[1]
tl = np.linspace(0.67, 0.995, 300)
ax.plot(tl, [fthrust(t) for t in tl], color="C0", lw=1, label="closed form")
mid = (edges[:-1] + edges[1:]) / 2
ax.errorbar(mid, frac * fy(Y_CUT) / np.diff(edges), yerr=err * fy(Y_CUT) / np.diff(edges), ls="none", marker="o", ms=2.8, color="C1",
            label=r"MadGraph ($T<0.99$)")
ax.set_yscale("log")
ax.set_xlabel(r"$T$")
ax.set_ylabel(r"$\sigma_0^{-1}\,d\sigma/dT\;/\;(C_F\alpha_s/2\pi)$")
ax.set_title(r"thrust, $e^+e^-\to q\bar qg$", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper left")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "ee_rratio.pdf"))
print("wrote ../figs/ee_rratio.pdf")
if INTERACTIVE:
    plt.show()
