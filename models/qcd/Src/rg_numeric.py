# %% [markdown]
# # Step (6): beta_0, gamma_m and the other RG coefficients from the mu-dependence; decoupling of the top quark
#
# Research note models/qcd, step (6), Eqs. (rge), (run), (rgslope), (rgW), App. rg.  g = 1 (alpha_s = 1/(4 pi)), m = m_t = 1, SU(3).
# At fixed parameters an MS-bar quantity is linear in ln mu^2 at one loop; its slope mu d/dmu follows from the RG equation of the
# quantity (K/g^2 units, K = (4 pi)^2, n_f = 6):
#   1PI:  K Pi^R: C_A (13/3 - xi) (gluon + ghost loops), -(8/3) T_F per quark (sum -2 gamma_A);  K Pitilde^R: -(3 - xi) C_A/2 (2 gamma_c);
#         K Sigma_V^R: -2 xi C_F (-2 gamma_psi);  K Sigma_S^R: 2 (3 + xi) C_F (2 gamma_psi - gamma_m/m);
#   pole mass K (Sigma_V + Sigma_S)(m^2): 6 C_F (-gamma_m/m);  residue K (R_t - 1): -6 C_F (IR pole -(3 - xi) C_F);  K Pi_t(0): -(8/3) T_F;
#   beta_0 from the two-point functions alone:  beta/g = gamma_A + 2 gamma_c - xi C_A g^2/K (the last term is the ghost vertex,
#         Z~_1 = 1 - xi C_A g^2/(2 K eps); 0 in the Landau gauge), i.e.  beta_0 = slope(Pi)/2 - slope(Pitilde) + xi C_A;
#   S-matrix element (Eq. (rgW)): d(K W)/d ln mu^2 = K W_-1 + beta_0 B(4) (+ ln mu^2 K W_-2), beta_0 = 7 for the MS-bar coupling with
#         n_f = 6 (LoopTools, rg_feyncalc.wl (d)) and 23/3 for alpha_s^(n_l) (MadLoop, Eq. (18));
#   decoupling: K [Pi_t(k^2) - Pi_t(0)] = -(4/3) T_F [k^2/(5 m^2) + 3 k^4/(140 m^4) + ...];  in MadLoop (alpha_s^(n_l)) the top part of
#         u ubar -> d dbar is W(m_t) - W(no top) = [Pi_t(s) - Pi_t(0)] B (the s-channel gluon), -> 0 as s/(5 m_t^2).
# Slopes from mu = 1/2 and 2: [X(2) - X(1/2)]/(2 ln 2) per ln mu (1PI), /(2 ln 4) per ln mu^2 (K W); X(1) - mean = (ln 4)^2/2 K W_-2.
# Tools: Package-X and LoopTools (rg_feyncalc.wl -> results/rg_feyncalc_onepi.csv, rg_feyncalc.csv), COLLIER (work/rg_collier ->
# results/rg_collier_onepi.csv), MadLoop (results/madloop.csv of step (5) for (A), (B); work/ml_C = u u~ > d d~ [virt=QCD] and
# work/ml_C5 = the same / t, built by run_rg_check.sh, at s = 10, t = -3).
# Writes results/rg_comparison.csv, results/rg_decoupling.csv and ../figs/rg_running.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python rg_numeric.py` (from Src/; run_rg_check.sh builds the helpers).  Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import re
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
KK = (4 * math.pi) ** 2
CA, CF, TF, NF, NL = 3.0, 4.0 / 3.0, 0.5, 6, 5
B06 = 11 * CA / 3 - 4 * TF * NF / 3          # 7
B05 = 11 * CA / 3 - 4 * TF * NL / 3          # 23/3
MUS = (0.5, 1.0, 2.0)
MTS = (1.0, 2.0, 3.0, 5.0, 10.0, 30.0, 100.0, 1000.0)
mp.mp.dps = 40


def read_csv(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


def cz(r, k):
    return complex(float(r["re_" + k]), float(r["im_" + k]))


# %% [markdown]
# ## The 1PI brackets: COLLIER, Package-X, LoopTools

# %%
subprocess.run(["./rg_collier", "../results/rg_collier_onepi.csv"], cwd=os.path.join(HERE, "work"), check=True, capture_output=True)
ONEPI = {}                                        # {(func, arg, xi, tool): {mu: (pole - expected, fin)}}
for r in read_csv("rg_collier_onepi.csv"):
    key = (r["func"], round(float(r["arg"]), 6), round(float(r["xi"]), 6), "COLLIER")
    ONEPI.setdefault(key, {})[round(float(r["mu"]), 6)] = (cz(r, "pole"), cz(r, "fin"))
for r in read_csv("rg_feyncalc_onepi.csv"):
    for tool, tag in (("Package-X", "px"), ("LoopTools", "lt")):
        key = (r["func"], round(float(r["arg"]), 6), round(float(r["xi"]), 6), tool)
        ONEPI.setdefault(key, {})[round(float(r["mu"]), 6)] = (cz(r, "pole_" + tag), cz(r, "fin_" + tag))
len(ONEPI)                                        # inspect

# %%
EXPECT = {"PiYM": lambda xi: CA * (13 / 3 - xi), "Ghost": lambda xi: -CA * (3 - xi) / 2, "PiQ0": lambda xi: -8 / 3 * TF,
          "PiT": lambda xi: -8 / 3 * TF, "SigV_t": lambda xi: -2 * xi * CF, "SigS_t": lambda xi: 2 * (3 + xi) * CF,
          "SigV_u": lambda xi: -2 * xi * CF, "Mpole": lambda xi: 6 * CF, "R_Q": lambda xi: -6 * CF, "PiT0": lambda xi: -8 / 3 * TF,
          "PiTsub": lambda xi: 0.0}


def slope_lnmu(vals):
    """mu d/dmu from mu = 1/2 and 2, and the deviation of mu = 1 from the mean (linearity)"""
    a, b, c = vals[0.5][1], vals[1.0][1], vals[2.0][1]
    return (c - a) / (2 * math.log(2)), abs(b - (a + c) / 2)


rows = []
worst = {}
for (func, arg, xi, tool), vals in sorted(ONEPI.items()):
    sl, lin = slope_lnmu(vals)
    ex = EXPECT[func](xi)
    pole = max(abs(vals[m][0]) for m in MUS)
    dev = max(abs(sl - ex), lin, pole)
    worst[(func, tool)] = max(worst.get((func, tool), 0.0), dev)
    rows.append(["1PI", func, arg, xi, tool, sl.real, sl.imag, ex, abs(sl - ex), lin, pole])
print(f"{'function':8} " + " ".join(f"{t:>10}" for t in ("Package-X", "LoopTools", "COLLIER"))
      + "   (max over points, xi, of |slope - expected|, |X(1) - mean|, |pole - expected|)")
for f in EXPECT:
    print(f"{f:8} " + " ".join(f"{worst[(f, t)]:10.1e}" for t in ("Package-X", "LoopTools", "COLLIER")))

# %% [markdown]
# ## The RG coefficients read from the slopes (COLLIER); beta_0 from the two-point functions

# %%
c1 = lambda f, arg, xi: slope_lnmu(ONEPI[(f, arg, xi, "COLLIER")])[0].real
for xi in (0.0, 1.0, 3.0):
    s_pi = c1("PiYM", 2.0, xi) + 5 * c1("PiQ0", 2.0, 0.0) + c1("PiT", 2.0, 0.0)
    g_a, g_c = -s_pi / 2, c1("Ghost", 2.0, xi) / 2
    g_psi = -c1("SigV_t", 2.0, xi) / 2
    g_m = 2 * g_psi - c1("SigS_t", 2.0, xi)
    b0 = -(g_a + 2 * g_c - xi * CA)
    print(f"xi = {xi:.0f}: gamma_A = {g_a:+.12f}, gamma_c = {g_c:+.12f}, gamma_psi = {g_psi:+.12f}, gamma_m/m = {g_m:+.12f} "
          f"(pole mass {-c1('Mpole', 1.0, xi):+.12f}; -8);  beta_0 = -(gamma_A + 2 gamma_c - xi C_A) = {b0:.12f} (7);  "
          f"residue slope - 2 x IR pole = {c1('R_Q', 1.0, xi) - 2 * CF * (-(3 - xi)):+.12f} (-2 gamma_psi = {-2 * xi * CF:+.4f})")
    rows.append(["beta_0 (1PI)", "", "", xi, "COLLIER", b0, 0.0, B06, abs(b0 - B06), 0.0, 0.0])

# %% [markdown]
# ## Decoupling in the gluon two-point function: Pi_t(k^2) - Pi_t(0) against the exact value (mpmath, 40 digits)

# %%
def bsub(k2, m=1.0):
    """K [Pi_t(k^2) - Pi_t(0)]/g^2 = -(4/3) T_F [(1 + 2 m^2/k^2)(B0(k^2) - B0(0)) - 1/3], independent of mu"""
    z = mp.mpf(k2) / mp.mpf(m) ** 2
    beta = mp.sqrt(1 - 4 / z + 0j)
    db = 2 - beta * mp.log((beta + 1) / (beta - 1))
    return complex(-(mp.mpf(4) / 3) * mp.mpf(TF) * ((1 + 2 / z) * db - mp.mpf(1) / 3))


print(f"{'k^2':>8} {'exact':>22} {'series k^2/5+3k^4/140':>22} " + " ".join(f"{t:>11}" for t in ("Package-X", "LoopTools", "COLLIER"))
      + "  (relative deviation, mu = 1)")
for x in (-1.0, -0.1, -0.01, -0.001, 0.001, 0.01, 0.1, 1.0):
    ex = bsub(x)
    ser = -4 / 3 * TF * (x / 5 + 3 * x * x / 140)
    devs = [abs(ONEPI[("PiTsub", x, 0.0, t)][1.0][1] - ex) / abs(ex) for t in ("Package-X", "LoopTools", "COLLIER")]
    print(f"{x:8.3f} {ex.real:+22.15e} {ser:+22.15e} " + " ".join(f"{d:11.1e}" for d in devs))
    rows.append(["decoupling Pi", "PiTsub", x, 0.0, "LoopTools/COLLIER", ex.real, 0.0, ser, max(devs[1:]), 0.0, 0.0])

# %% [markdown]
# ## The S-matrix element: LoopTools (MS-bar, n_f = 6) against Eq. (rgW); beta_0 from the slopes (LoopTools, MadLoop)

# %%
W1 = {}
for r in read_csv("scat_mathematica.csv"):
    W1.setdefault(r["process"], {})[int(r["eps_power"])] = complex(float(r["re_KW"]), float(r["im_KW"]))
LT = {}
for r in read_csv("rg_feyncalc.csv"):
    LT.setdefault(r["process"], {})[float(r["mu"])] = (float(r["born4"]), cz(r, "m2"), cz(r, "m1"), cz(r, "fin"))


def predict(p, lam, b4, beta0=B06):
    L = math.log(lam * lam)
    w = W1[p]
    return (w[-2], w[-1] + L * w[-2], w[0] + L * (w[-1] + beta0 * b4) + L * L / 2 * w[-2])


for p in ("A", "B"):
    b4 = LT[p][1.0][0]
    dev = max(abs(LT[p][lam][1 + k] - predict(p, lam, b4)[k]) / abs(predict(p, lam, b4)[k]) for lam in MUS for k in range(3))
    fa, fb, fc = (LT[p][lam][3] for lam in MUS)
    sl = (fc - fa) / (2 * math.log(4))
    bfit = (sl.real - LT[p][1.0][2].real) / b4
    lin = abs((fa + fc) / 2 - fb - math.log(4) ** 2 / 2 * LT[p][1.0][1]) / abs(fb)
    print(f"({p}) LoopTools vs Eq. (rgW) from step (4), mu = 1/2, 1, 2 (all eps orders): max relative deviation {dev:.1e};  "
          f"beta_0 fit {bfit:.12f} (7);  Im slope - Im K W_-1 = {abs(sl.imag - LT[p][1.0][2].imag):.1e};  curvature check {lin:.1e}")
    rows.append(["K W", p, "", 1.0, "LoopTools", bfit, sl.imag, B06, abs(bfit - B06), lin, dev])
ML = {}
for r in read_csv("madloop.csv"):
    ML.setdefault(r["process"], {})[float(r["mu_over_m"])] = {k: float(r["ml_" + k]) for k in ("born", "finite", "1eps", "2eps")}


def beta_madloop(v):
    """MadLoop: finite = [2 Re K W4_fin + (pi^2/12) 2 Re K W4_-2]/(K avg), 1eps, born = B4/avg; d(K W4_fin)/dL = K W4_-1 + beta0 B4 (+ L K W4_-2)"""
    return KK / (2 * v[1.0]["born"]) * ((v[2.0]["finite"] - v[0.5]["finite"]) / (2 * math.log(4)) - v[1.0]["1eps"])


for p in ("A", "B"):
    b = beta_madloop(ML[p])
    print(f"({p}) MadLoop (alpha_s^(n_l), step (5) runs): beta_0 fit {b:.12f} (23/3 = {B05:.12f})")
    rows.append(["K W", p, "", 1.0, "MadLoop", b, 0.0, B05, abs(b - B05), 0.0, 0.0])

# %% [markdown]
# ## MadLoop u ubar -> d dbar: beta_0^(5) and the decoupling of the top quark

# %%
def momenta_massless(s, t):
    e = math.sqrt(s) / 2
    c = 1 + t / (2 * e * e)
    st = math.sqrt(1 - c * c)
    return [(e, 0, 0, e), (e, 0, 0, -e), (e, e * st, 0, e * c), (e, -e * st, 0, -e * c)]


def set_mt(proc, mt):
    card = os.path.join(HERE, "work", proc, "Cards", "param_card.dat")
    s = open(card).read()
    s = re.sub(r"(\n +6 +)\S+( +# MT)", lambda mm: mm.group(1) + repr(float(mt)) + mm.group(2), s)
    with open(card, "w") as fh:
        fh.write(s)


def run_madloop(proc, mu, s=10.0, t=-3.0):
    base = os.path.join(HERE, "work", proc, "SubProcesses")
    d = os.path.join(base, next(x for x in sorted(os.listdir(base)) if x.startswith("P0_")))
    with open(os.path.join(d, "PS.input"), "w") as fh:
        fh.writelines("%.17e %.17e %.17e %.17e\n" % m for m in momenta_massless(s, t))
    with open(os.path.join(d, "MU_R.input"), "w") as fh:
        fh.write("%.17e\n" % mu)
    out = subprocess.run(["./check"], cwd=d, capture_output=True, text=True, check=True).stdout
    return {key: float(re.search(r"Matrix element %s\s*=\s*(\S+)" % key, out).group(1)) for key in ("born", "finite", "1eps", "2eps")}


set_mt("ml_C", 1.0)
vc = {mu: run_madloop("ml_C", mu) for mu in MUS}
vc5 = {mu: run_madloop("ml_C5", mu) for mu in MUS}
print(f"(C) u ubar -> d dbar, MadLoop: beta_0 fit {beta_madloop(vc):.12f} (with the top, m_t = m),  {beta_madloop(vc5):.12f} (/ t);  "
      f"23/3 = {B05:.12f}")
rows.append(["K W", "C", "", 1.0, "MadLoop", beta_madloop(vc), 0.0, B05, abs(beta_madloop(vc) - B05), 0.0, 0.0])
ref = vc5[1.0]
dec = []
for mt in MTS:
    set_mt("ml_C", mt)
    v = run_madloop("ml_C", 1.0)
    top = (v["finite"] - ref["finite"]) * KK / (2 * ref["born"])        # Re K W_top/(g^2 B)
    pred = bsub(10.0, mt).real
    lead = -4 / 3 * TF * 10.0 / (5 * mt * mt)
    dec.append([mt, top, pred, lead, abs(top - pred), abs(v["1eps"] - ref["1eps"]) * KK / (2 * ref["born"]),
                abs(v["2eps"] - ref["2eps"]) * KK / (2 * ref["born"])])
set_mt("ml_C", 1.0)
print(f"{'m_t':>7} {'MadLoop W_top/B':>22} {'Pi_t(s) - Pi_t(0)':>22} {'-(2/3) s/(5 m_t^2)':>20} {'|diff|':>9} {'|d pole|':>9}   (K/g^2 units, s = 10)")
for d in dec:
    print(f"{d[0]:7.0f} {d[1]:+22.15e} {d[2]:+22.15e} {d[3]:+20.12e} {d[4]:9.1e} {max(d[5], d[6]):9.1e}")
with open(os.path.join(HERE, "results", "rg_decoupling.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["mt", "madloop_top", "pred_top", "leading", "abs_diff", "abs_d_1eps", "abs_d_2eps"])
    w.writerows(dec)
with open(os.path.join(HERE, "results", "rg_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["kind", "quantity", "arg", "xi", "tool", "re_value", "im_slope", "expected", "abs_dev", "linearity", "pole_or_dev"])
    w.writerows(rows)
print("wrote results/rg_comparison.csv, results/rg_decoupling.csv")

# %% [markdown]
# ## Figure: fixed parameters against the running of Eq. (run); the top pole mass; decoupling

# %%
def g2_run(lam, beta0=B06):      # g(m) = 1:  1/g^2(mu) = 1 + (beta0/K) ln mu^2
    return 1 / (1 + beta0 / KK * math.log(lam * lam))


mus = np.geomspace(0.25, 4.0, 33)
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))
ax = axes[0]
for p, col in (("A", "C0"), ("B", "C1")):
    b4 = LT[p][1.0][0]
    c0 = W1[p][0].real
    yf = lambda lam: b4 + 2 / KK * (c0 + B06 * math.log(lam * lam) * b4)              # IR logarithms removed, g = 1
    yr = lambda lam: g2_run(lam) ** 2 * b4 + g2_run(lam) ** 3 * 2 / KK * (c0 + B06 * math.log(lam * lam) * b4)
    ax.plot(mus, [yf(m) / yf(1) for m in mus], color=col, lw=1, ls="-", label=f"({p}) $g$ fixed")
    ax.plot(mus, [yr(m) / yr(1) for m in mus], color=col, lw=1, ls="--", label=f"({p}) $g(\\mu)$")
    pts = []
    for lam in MUS:
        L = math.log(lam * lam)
        wt = (LT[p][lam][3] - L * LT[p][1.0][2] - L * L / 2 * LT[p][1.0][1]).real
        pts.append((b4 + 2 / KK * wt) / yf(1))
    ax.plot(MUS, pts, ls="none", marker="o", ms=3.4, color=col)
    print(f"({p}) Y(mu)/Y(m) at mu = 1/4, 4: fixed {yf(0.25) / yf(1):.6f}, {yf(4) / yf(1):.6f};  running {yr(0.25) / yr(1):.6f}, {yr(4) / yr(1):.6f}")
ax.set_xscale("log")
ax.set_xlabel(r"$\mu/m$")
ax.set_ylabel(r"$Y(\mu)/Y(m)$")
ax.set_title(r"(A), (B): $\sqrt{s}=\sqrt{10}\,m$, $t=-3m^2$", fontsize=8)
ax.legend(frameon=False, fontsize=6, loc="upper left", ncol=1)

ax = axes[1]
mp_fix = [1 + CF * (4 + 3 * math.log(m * m)) / KK for m in mus]
mrun = lambda lam: g2_run(lam) ** (3 * CF / B06)
mp_run = [mrun(m) * (1 + CF * g2_run(m) * (4 + 3 * math.log(m * m / mrun(m) ** 2)) / KK) for m in mus]
ax.plot(mus, mp_fix, color="C0", lw=1, ls="-", label=r"$m=1$, $g=1$ fixed")
ax.plot(mus, mp_run, color="C1", lw=1, ls="--", label=r"$m(\mu)$, $g(\mu)$")
ax.plot(MUS, [1 + ONEPI[("Mpole", 1.0, 1.0, "COLLIER")][m][1].real / KK for m in MUS], ls="none", marker="s", ms=3.4, color="C0", label="COLLIER")
print(f"m_pole at mu = 1/4, 4: fixed {mp_fix[0]:.6f}, {mp_fix[-1]:.6f};  running {mp_run[0]:.6f}, {mp_run[-1]:.6f}")
ax.set_xscale("log")
ax.set_xlabel(r"$\mu/m$")
ax.set_ylabel(r"$m_{\mathrm{p}}/m(m)$")
ax.set_title("top pole mass", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper left")
for ax in axes[:2]:
    ax.set_xticks([0.25, 0.5, 1, 2, 4], ["1/4", "1/2", "1", "2", "4"])
    ax.minorticks_off()

ax = axes[2]
mtl = np.geomspace(1.0, 1000.0, 400)
ax.plot(mtl, [abs(bsub(10.0, x).real) for x in mtl], color="C0", lw=1, ls="-", label=r"$|\Pi_t(s)-\Pi_t(0)|$")
ax.plot(mtl, [4 / 3 * TF * 10.0 / (5 * x * x) for x in mtl], color="C1", lw=1, ls="--", label=r"$\frac{2}{3}\,\frac{s}{5m_t^2}$")
ax.plot([d[0] for d in dec], [abs(d[1]) for d in dec], ls="none", marker="o", ms=3.4, color="C0", label="MadLoop")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$m_t/m$  ($s=10m^2$, $t=-3m^2$)")
ax.set_ylabel(r"$|W_t|/(g^2B/K)$")
ax.set_title(r"$u\bar u\to d\bar d$, top part ($\alpha_s^{(5)}$)", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="lower left")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "rg_running.pdf"))
print("wrote ../figs/rg_running.pdf")
if INTERACTIVE:
    plt.show()
