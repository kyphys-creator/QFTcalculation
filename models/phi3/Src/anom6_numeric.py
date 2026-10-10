"""Field anomalous dimension, mass running and beta in d = 6 from the 1PI functions (research note, step (10)).

B0^(6)(p^2) and C0^(6) (MS-bar, note Eqs. (11)-(13); m = g = 1) from FeynCalc + Package-X, FeynCalc + LoopTools
(results/anom6_feyncalc.csv) and COLLIER (results/anom6_collier.csv) for mu = 1, 1/2, 2.
The renormalized 1PI functions obey  mu d Gamma^(n)/d mu = n gamma_phi Gamma^(n),  gamma_phi = (1/2) mu d ln Z/d mu
(Gamma^(n) = Z^(n/2) Gamma_0^(n), phi_0 = Z^(1/2) phi).  At one loop, with Sigma = -g^2 B0^(6)/(2K), K = (4pi)^3:
    n = 2, Gamma^(2) = p^2 - m^2 - Sigma:   -mu dSigma/dmu = gamma + 2 gamma_phi (p^2 - m^2),   gamma = mu dm^2/dmu,
    n = 3, Gamma^(3) = -g + g^3 C0^(6)/K:     beta = T + 3 g gamma_phi,   T = (g^3/K) mu dC0^(6)/dmu.
The two-point slopes at eight p^2 fix (gamma, gamma_phi) by least squares; T then gives beta.  Expected (note, App. D):
    gamma_phi = g^2/(12 K),  gamma = -5 g^2 m^2/(6 K),  beta = -3 g^3/(4 K).
Literature: Borinsky, Gracey, Kompaniets, Schnetz, Phys. Rev. D 103, 116024 (2021) [arXiv:2103.16224], Eqs. (28)-(30), give
the Lee-Yang theory (g -> i g) in d = 6 - eps with beta = mu dg/dmu, gamma_phi = mu d ln Z_phi/dmu (phi_0 = Z_phi phi),
gamma_{m^2} = mu d ln Z_{m^2}/dmu (m_0^2 = m^2 Z_{m^2}):  beta = -(eps/2) g + (3/4) g^3,  gamma_phi = -g^2/12,
gamma_{m^2} = -(5/6) g^2.  Undoing g -> i g (g^2 -> -g^2, beta -> -beta for the cubic term) and reading their g^2 as
g^2/K: beta = -(3/4) g^3/K, gamma_phi = g^2/(12 K), mu d ln m^2/dmu = -gamma_{m^2} = -(5/6) g^2/K.
Writes results/anom6_comparison.csv and ../figs/anom6_d6.pdf.
Usage (from Src/):  ~/miniforge3/envs/qft/bin/python anom6_numeric.py
"""
import csv
import math
import os

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
K = (4 * math.pi) ** 3
GPHI, GAMMA, BETA = 1 / (12 * K), -5 / (6 * K), -3 / (4 * K)
MUS = (0.5, 1.0, 2.0)
TOL = 1e-9     # Package-X's numerical C0 limits it to ~1e-12 here (cf. steps (5), (8))

# the literature values (Lee-Yang form, coupling g_LY^2 = -g^2/K) mapped back to the real coupling
LY = {"beta3": 3 / 4, "gphi": -1 / 12, "gm2": -5 / 6}
LIT = {"beta": -LY["beta3"] / K, "gphi": -LY["gphi"] / K, "gamma": LY["gm2"] / K}
for k, ref in (("beta", BETA), ("gphi", GPHI), ("gamma", GAMMA)):
    assert abs(LIT[k] / ref - 1) < 1e-15, k
print("Borinsky-Gracey-Kompaniets-Schnetz (2021), Eqs. (28)-(30), mapped to the real coupling, equal the note's "
      "beta, gamma_phi and mu dm^2/dmu: ok")


def b0_closed(p2, mu):
    """d = 4 MS-bar B0(p^2; 1, 1) for any real p^2 (App. G)."""
    p2 = mp.mpf(p2)
    L = mp.log(1 / mp.mpf(mu) ** 2)
    if p2 == 0:
        return -L
    if p2 < 0:
        b = mp.sqrt(1 - 4 / p2)
        return 2 - L - b * mp.log((b + 1) / (b - 1))
    if p2 < 4:
        bt = mp.sqrt(4 / p2 - 1)
        return 2 - L - 2 * bt * mp.atan(1 / bt)
    b = mp.sqrt(1 - 4 / p2)
    return 2 - L - b * mp.log((1 + b) / (1 - b)) + 1j * mp.pi * b


def b06_closed(p2, mu):
    """Eq. (13) with m = 1."""
    return -1 + mp.mpf(p2) / 9 + mp.log(1 / mp.mpf(mu) ** 2) / 3 - mp.mpf(2) / 3 * (1 - mp.mpf(p2) / 4) * b0_closed(p2, mu)


def read(path, cols):
    out = {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            key = (r["func"], round(float(r["arg1"]), 6), round(float(r["arg2"]), 6), round(float(r["arg3"]), 6),
                   round(float(r["mu"]), 6))
            out[key] = {c: complex(float(r["re_" + c]), float(r["im_" + c])) for c in cols}
    return out


fc = read(os.path.join(HERE, "results", "anom6_feyncalc.csv"), ["packagex", "looptools"])
co = read(os.path.join(HERE, "results", "anom6_collier.csv"), ["collier"])
data = {k: {**fc[k], **co[k]} for k in fc}
tools = ("packagex", "looptools", "collier")

# ---------------- the values: tools against each other and against Eq. (13) ----------------
rows = []
print(f"\n{'X':4} {'args':>14} {'mu':>4} {'Re X (COLLIER)':>22} {'Im X (COLLIER)':>22} | PX  LT  closed form (B0^(6) only)")
worst = {"B06": 0.0, "C06": 0.0}
for key in sorted(data):
    func, a1, a2, a3, mu = key
    v = data[key]
    ref = v["collier"]
    dev = {k: abs(v[k] - ref) / abs(ref) if abs(ref) > 0 else abs(v[k]) for k in tools}
    dcl = abs(complex(b06_closed(a1, mu)) - ref) / abs(ref) if func == "B06" else float("nan")
    checked = ("packagex", "looptools") if func == "B06" else ("packagex",)   # LoopTools C0^(6) below threshold: record only
    bad = [k for k in checked if dev[k] > TOL] + (["closed form"] if func == "B06" and dcl > TOL else [])
    worst[func] = max([worst[func]] + [dev[k] for k in checked] + ([dcl] if func == "B06" else []))
    args = f"{a1:g}" if func == "B06" else f"{a1:g},{a2:g},{a3:g}"
    print(f"{func:4} {args:>14} {mu:4.1f} {ref.real:+22.15e} {ref.imag:+22.15e} | {dev['packagex']:7.1e} "
          f"{dev['looptools']:7.1e} {dcl:7.1e}" + ("   <- disagrees: " + ",".join(bad) if bad else ""))
    rows.append([func, a1, a2, a3, mu, ref.real, ref.imag, *(x for k in tools for x in (v[k].real, v[k].imag)), dcl])
print(f"largest deviation from COLLIER (and Eq. (13)): B0^(6) {worst['B06']:.1e}, C0^(6) (Package-X) {worst['C06']:.1e}")

# ---------------- slopes in ln(mu) and the fits ----------------
def slope(func, args, k):
    v = {mu: data[(func, *args, mu)][k] for mu in MUS}
    s = (v[2.0] - v[0.5]) / (2 * math.log(2))
    lin = abs(v[1.0] - (v[2.0] + v[0.5]) / 2) / max(abs(v[1.0]), 1e-300)
    return s, lin


p2s = sorted({key[1] for key in data if key[0] == "B06"})
invs = sorted({key[1:4] for key in data if key[0] == "C06"})
fit_rows, slope_rows = [], []
print("\n1PI functions: expected gamma_phi = %.10e, gamma = mu dm^2/dmu = %.10e, beta = %.10e" % (GPHI, GAMMA, BETA))
fits = {}
for k in tools:
    S, X, lins, ims = [], [], [], []
    for p2 in p2s:
        s, lin = slope("B06", (p2, 1.0, 1.0), k)
        S.append(s.real / (2 * K))                         # -mu dSigma/dmu = (g^2/(2K)) mu dB0^(6)/dmu
        X.append([1.0, 2 * (p2 - 1)])
        lins.append(lin)
        ims.append(abs(s.imag))                            # Im B0^(6) does not depend on mu
        slope_rows.append(["B06", p2, k, s.real / (2 * K), GAMMA + 2 * GPHI * (p2 - 1)])
    (gam, gph), *_ = np.linalg.lstsq(np.array(X), np.array(S), rcond=None)
    res = max(abs(np.array(X) @ np.array([gam, gph]) - np.array(S))) / abs(GAMMA)
    T = []
    for inv in invs:
        s, lin = slope("C06", inv, k)
        T.append(s.real / K)                               # T = (g^3/K) mu dC0^(6)/dmu
        if np.isfinite(s.imag):
            ims.append(abs(s.imag))
        slope_rows.append(["C06", "%g,%g,%g" % inv, k, s.real / K, -1 / K])
        if np.isfinite(s.real) and (k != "looptools" or inv == (1.0, 1.0, 5.0)):
            lins.append(lin)
    T = [x for x in T if np.isfinite(x)]                   # LoopTools has no C0^(6) at zero momenta
    Tm = float(np.mean(T))
    bet = Tm + 3 * gph
    fits[k] = (gph, gam, bet)
    print(f"  {k:9}: gamma_phi = {gph:+.10e} (rel. dev. {abs(gph / GPHI - 1):.1e}),  gamma = {gam:+.10e} "
          f"(rel. dev. {abs(gam / GAMMA - 1):.1e}),  beta = {bet:+.10e} (rel. dev. {abs(bet / BETA - 1):.1e})")
    print(f"             two-point fit residual {res:.0e};  spread of T over the vertex points {np.ptp(T) * K:.0e} "
          f"(units g^3/K);  linearity in ln mu {max(lins):.0e};  |mu d Im/d mu| {max(ims):.0e}")
    fit_rows.append([k, gph, gam, bet, GPHI, GAMMA, BETA, res, float(np.ptp(T) * K), max(lins)])

# the mass running from the S-matrix element (step (9)) and from the two-point function
rg = {}
with open(os.path.join(HERE, "results", "rg4_comparison.csv")) as fh:
    for r in csv.reader(fh):
        if len(r) == 10 and r[0] == "d=6, MS-bar m":
            rg[r[1]] = (float(r[2]), float(r[3]))
print("\nstep (9) (S-matrix element) vs step (10) (1PI functions):")
for k in tools:
    print(f"  {k:9}: gamma {rg[k][0]:+.10e} vs {fits[k][1]:+.10e} (rel. diff. {abs(fits[k][1] / rg[k][0] - 1):.1e}),  "
          f"beta {rg[k][1]:+.10e} vs {fits[k][2]:+.10e} (rel. diff. {abs(fits[k][2] / rg[k][1] - 1):.1e})")

with open(os.path.join(HERE, "results", "anom6_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["func", "arg1", "arg2", "arg3", "mu", "re_ref_collier", "im_ref_collier",
                *(f"{c}_{k}" for k in tools for c in ("re", "im")), "reldev_closed_form"])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["func", "args", "tool", "slope", "slope_expected"])
    w.writerows(slope_rows)
    w.writerow([])
    w.writerow(["tool", "gamma_phi_fit", "gamma_fit", "beta_fit", "gamma_phi_expected", "gamma_expected",
                "beta_expected", "fit_residual", "T_spread", "linearity"])
    w.writerows(fit_rows)

# ---------------- figure ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
figdir = os.path.join(HERE, "..", "figs")
os.makedirs(figdir, exist_ok=True)
x = np.linspace(-6, 9, 2)
fig, ax = plt.subplots(figsize=(3.25, 2.2))
ax.plot(x, K * (GAMMA + 2 * GPHI * (x - 1)), color="k", lw=0.9, ls="-", label=r"$\gamma+2\gamma_\phi(p^2-m^2)$")
style = {"packagex": dict(marker="o", ms=4.5, mfc="none", mec="#5d81b4", ls="none", label="Package-X"),
         "looptools": dict(marker="x", ms=4, color="#e09b24", ls="none", label="LoopTools"),
         "collier": dict(marker="+", ms=6, color="#e25759", ls="none", label="COLLIER")}
for k in tools:
    ax.plot(p2s, [K * r[3] for r in slope_rows if r[0] == "B06" and r[2] == k], **style[k])
ax.axvline(4, color="0.7", lw=0.6, ls=":")
ax.set_xlabel(r"$p^2/m^2$")
ax.set_ylabel(r"$-(4\pi)^3g^{-2}\,\mu\,\partial\Sigma/\partial\mu$")
ax.set_title(r"$d=6$, $m=g=1$", fontsize=8)
ax.set_ylim(-3.2, 0.7)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(figdir, "anom6_d6.pdf"))
print("\nwrote results/anom6_comparison.csv and figs/anom6_d6.pdf")
