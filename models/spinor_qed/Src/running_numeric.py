# %% [markdown]
# # Step (9): the running coupling -- dispersion relation, effective charge, Landau poles, Uehling potential
#
# Research note models/spinor_qed, step (9), Eqs. (eq:disp), (eq:aeff), (eq:uehling), App. run.  Units m = 1 for one loop.
# - Dispersion relation (App. g2): Pibar(q^2) = -q^2 int_{4m^2}^inf ds rho(s)/(s (s - q^2 - i0)), rho = (alpha/3pi)(1 + 2m^2/s) beta,
#   Im Pibar(s + i0) = -pi rho(s): the real part from the (principal-value) integral of rho against Package-X, LoopTools and
#   COLLIER (running_feyncalc.wl, running_collier.f90) at spacelike and timelike q^2, and their imaginary parts against -pi rho.
# - Effective charge alpha(q^2) = alpha(0)/(1 - Pibar(q^2)), N_f = 2 (e, mu): for -q^2 = Q^2 >> m_f^2 it equals the MS-bar
#   alpha(mu) at mu = e^(-5/6) Q (matched to alpha(0) by Eq. (os)) up to O(m^2/Q^2); below a threshold the loop decouples,
#   Pibar_f -> (alpha/15pi) Q^2/m_f^2.  Landau poles: MS-bar mu_L (Eq. (run)) and on-shell Q_L (1 = sum_f Pibar_f(-Q_L^2)),
#   Q_L = e^(5/6) mu_L.
# - Uehling potential of a static charge Ze, V = -(Z alpha/r)[1 + dV], dV = (2 alpha/3pi) int_1^inf du e^(-2 m r u)
#   (1 + 1/(2u^2)) sqrt(u^2 - 1)/u^2, against the z-representation (4 alpha/pi) int dz z(1-z) E1(m r/sqrt(z(1-z))), the direct
#   Fourier transform of Pibar(-Q^2)/Q^2 and the spectral integral with rho from the tools' Im Pi; limits (2 alpha/3pi)[ln(1/mr)
#   - gamma_E - 5/6] (mr << 1) and (alpha/(4 sqrt pi)) e^(-2mr)/(mr)^(3/2) (mr >> 1).
# - Applications (Z = 1, point nucleus, Schroedinger wave functions with the reduced mass): the 2P - 2S shift of muonic hydrogen
#   from the electron loop, against 205.0074 meV (Antognini et al., Ann. Phys. 331 (2013) 127, Table 1, #1, Pachucki); the 2S
#   shift of hydrogen against the delta-function limit -(4 alpha (Z alpha)^4/(15 pi n^3)) m_r^3/m_e^2.
# Writes results/running.csv and ../figs/running.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python running_numeric.py --nodes` writes work/running_q2.txt (run first), then without
# arguments after running_feyncalc.wl (run_running_check.sh).  Interactive: "Run Cell" in VS Code (the node file must exist).

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
ALPHA0 = 1 / mp.mpf("137.035999084")     # alpha(0), CODATA 2018
R_MUE = mp.mpf("206.7682830")            # m_mu/m_e
R_PE = mp.mpf("1836.15267343")           # m_p/m_e
ME_MEV = mp.mpf("0.51099895000")         # m_e in MeV
NF = 2
Q2_PTS = [-100, -10, -1, -0.1, 0.5, 2, 3.9, 4.5, 6, 10, 100]      # q^2/m^2 for the dispersion check
R_PTS = [1e-3, 1e-2, 0.1, 0.3, 1.0, 2.0, 5.0]                       # m r for the Uehling potential
NU, NH = 64, 48


def gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return (b - a) / 2 * x + (a + b) / 2, (b - a) / 2 * w


def unodes_r(r):
    """u = cosh(theta), theta in [0, acosh(max(2, 40/r))]: sqrt(u^2-1) du = sinh^2 dtheta; e^(-2 r u) < e^(-80) beyond"""
    th, w = gl(NU, 0.0, math.acosh(max(2.0, 40.0 / r)))
    return np.cosh(th), w * np.sinh(th)          # u, weight for f(u) du


def unodes_tail():
    """for the muonic-hydrogen integral: u = cosh(theta) on [1, 2], u = 1/v on [2, inf)"""
    th, w = gl(NH, 0.0, math.acosh(2.0))
    v, wv = gl(NH, 0.0, 0.5)
    return np.concatenate([np.cosh(th), 1 / v]), np.concatenate([w * np.sinh(th), wv / v ** 2])


S_NODES = np.concatenate([4 * unodes_r(r)[0] ** 2 for r in R_PTS] + [4 * unodes_tail()[0] ** 2])
ALL_Q2 = np.concatenate([np.array(Q2_PTS, float), S_NODES])
if "--nodes" in sys.argv:
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    with open(os.path.join(HERE, "work", "running_q2.txt"), "w") as fh:
        fh.writelines(f"{q:.17e}\n" for q in ALL_Q2)
    print(f"wrote work/running_q2.txt ({len(ALL_Q2)} values: {len(Q2_PTS)} check points, {len(S_NODES)} spectral nodes)")
    sys.exit(0)

# %% [markdown]
# ## The hand formulas (mpmath): rho, Pibar (closed form and dispersion integral)

# %%
def rho(s):              # (pi/alpha) rho(s), m = 1
    s = mp.mpf(s)
    return (1 + 2 / s) * mp.sqrt(1 - 4 / s) / 3 if s > 4 else mp.mpf(0)


def pibar(t):            # (pi/alpha) Pibar(t), m = 1, any real t (t > 4 with +i0)
    t = mp.mpf(t)
    if abs(t) < 0.5:
        return -2 * mp.nsum(lambda n: t ** n / n * mp.beta(n + 2, n + 2), [1, mp.inf])
    if t < 0:
        b = mp.sqrt(1 - 4 / t)
        lb = mp.log((b + 1) ** 2 * (-t) / 4)
        return -((1 + 2 / t) * (2 - b * lb) - mp.mpf(1) / 3) / 3
    if t < 4:            # below threshold: beta = i sqrt(4/t - 1)
        bb = mp.sqrt(4 / t - 1)
        return -((1 + 2 / t) * (2 - 2 * bb * mp.atan(1 / bb)) - mp.mpf(1) / 3) / 3
    b = mp.sqrt(1 - 4 / t)       # above threshold, B0 - B0(0) = 2 - b [ln((1+b)/(1-b)) - i pi]
    return -((1 + 2 / t) * (2 - b * (mp.log((1 + b) / (1 - b)) - 1j * mp.pi)) - mp.mpf(1) / 3) / 3


def pibar_disp(q2):      # real part from the dispersion integral (principal value above threshold)
    q2 = mp.mpf(q2)
    g = lambda s: rho(s) / s
    if q2 <= 4:
        return -q2 * mp.quad(lambda s: g(s) / (s - q2), [4, 8, 40, mp.inf])
    c = 2 * q2 - 4                        # symmetric interval around q2: PV of 1/(s - q2) vanishes there
    pv = mp.quad(lambda s: (g(s) - g(q2)) / (s - q2), [4, q2, c]) + mp.quad(lambda s: g(s) / (s - q2), [c, mp.inf])
    return -q2 * pv


for q2 in (-10, 2, 6):
    v = pibar(q2)
    print(f"q^2 = {q2}: closed form {mp.nstr(v, 15)}, dispersion integral {mp.nstr(pibar_disp(q2), 15)}, -pi rho = {mp.nstr(-mp.pi * rho(q2), 15)}")

# %% [markdown]
# ## Package-X, LoopTools, COLLIER against the dispersion relation

# %%
subprocess.run(["./running_collier", "running_q2.txt", "../results/running_collier.csv"], cwd=os.path.join(HERE, "work"),
               check=True, capture_output=True)


def read_csv(name):
    with open(os.path.join(HERE, "results", name)) as fh:
        return list(csv.DictReader(fh))


cl = read_csv("running_collier.csv")
fc = read_csv("running_feyncalc.csv")
assert len(cl) == len(fc) == len(ALL_Q2)
TOOLS = {"Package-X": [complex(float(r["re_px"]), float(r["im_px"])) / 4 for r in fc],      # (pi/alpha) Pibar = K Pibar/(4 e^2)
         "LoopTools": [complex(float(r["re_lt"]), float(r["im_lt"])) / 4 for r in fc],
         "COLLIER": [complex(float(r["re"]), float(r["im"])) / 4 for r in cl]}
rows = []
dev = {}
print(f"{'q^2/m^2':>8} {'dispersion (Re)':>22} {'-pi rho (Im)':>14}  " + "  ".join(f"{t:>20}" for t in TOOLS))
for i, q2 in enumerate(Q2_PTS):
    re_d, im_d = pibar_disp(q2), -mp.pi * rho(q2)
    devs = []
    for tool, vals in TOOLS.items():
        d = max(abs(vals[i].real - float(re_d)) / abs(float(re_d)), abs(vals[i].imag - float(im_d)))
        dev[tool] = max(dev.get(tool, 0.0), d)
        devs.append(d)
    print(f"{q2:8.2f} {mp.nstr(re_d, 16):>22} {mp.nstr(im_d, 10):>14}  " + "  ".join(f"{d:20.1e}" for d in devs))
    rows.append(["dispersion", q2, "", float(re_d), float(im_d)] + devs)
print("max deviation (relative Re, absolute Im):", {k: f"{v:.1e}" for k, v in dev.items()})
# rho from the tools' imaginary parts at the spectral nodes
rdev = {tool: max(abs(-vals[len(Q2_PTS) + j].imag / math.pi - float(rho(s))) / float(rho(s))
                  for j, s in enumerate(S_NODES) if s > 4.0001) for tool, vals in TOOLS.items()}
print("rho = -Im Pibar/pi at the", len(S_NODES), "spectral nodes, max relative deviation:", {k: f"{v:.1e}" for k, v in rdev.items()})

# %% [markdown]
# ## Effective charge, decoupling, Landau poles

# %%
def inv_alpha_eff(Q, a0, masses):        # 1/alpha(-Q^2) = (1/alpha(0)) (1 - sum Pibar)
    return (1 - a0 / mp.pi * sum(pibar(-(Q / m) ** 2) for m in masses)) / a0


def inv_alpha_ms(mu, a0, masses):        # Eq. (os) with Eq. (run): 1/alpha(mu) = 1/alpha(0) - (1/3pi) sum ln(mu^2/m_f^2)
    return 1 / a0 - sum(mp.log(mu ** 2 / m ** 2) for m in masses) / (3 * mp.pi)


PHYS = (ALPHA0, [mp.mpf(1), R_MUE])
a0_bench = 1 / (4 * mp.pi + mp.log(1 / mp.mpf("1.7") ** 2) / (3 * mp.pi))    # alpha(0) of e(m_e) = 1, Eq. (os)
BENCH = (a0_bench, [mp.mpf(1), mp.mpf("1.7")])
print(f"benchmark: alpha(0)^-1 = {mp.nstr(1 / a0_bench, 10)} (note: 12.454);  physical: alpha(0)^-1 = {mp.nstr(1 / ALPHA0, 13)}")
for Q in (mp.mpf(10) ** k for k in (3, 5, 8)):
    d = inv_alpha_eff(Q, *PHYS) - inv_alpha_ms(Q * mp.exp(-mp.mpf(5) / 6), *PHYS)
    print(f"Q = 1e{int(mp.log10(Q))} m_e: 1/alpha_eff(-Q^2) - 1/alpha_MSbar(e^(-5/6) Q) = {mp.nstr(d, 5)}  "
          f"(expected -(1/3pi) sum 6 m_f^2/Q^2 = {mp.nstr(-sum(6 / (Q / m) ** 2 for m in PHYS[1]) / (3 * mp.pi), 5)})")
for x in (mp.mpf("0.1"), mp.mpf("0.01")):
    t = -x * x
    print(f"decoupling: Pibar_f(-Q^2)/[(alpha/15pi) Q^2/m_f^2] at Q/m_f = {x}: {mp.nstr(pibar(t) / (-t / 15), 12)}  (1 - 3Q^2/(28 m^2) = {mp.nstr(1 - 3 * x * x / 28, 12)})")

LANDAU = {}
for name, (a0, masses) in (("benchmark", BENCH), ("physical", PHYS)):
    mu_l = mp.findroot(lambda L: inv_alpha_ms(mp.exp(L), a0, masses), 3 * mp.pi / (2 * NF * a0))            # ln(mu_L/m_e)
    q_l = mp.findroot(lambda L: inv_alpha_eff(mp.exp(L), a0, masses), mu_l + mp.mpf(5) / 6)                 # ln(Q_L/m_e)
    LANDAU[name] = (mu_l, q_l)
    print(f"{name}: ln(mu_L/m_e) = {mp.nstr(mu_l, 15)} (MS-bar),  ln(Q_L/m_e) = {mp.nstr(q_l, 15)} (on-shell),  difference "
          f"{mp.nstr(q_l - mu_l, 15)} (5/6 = {mp.nstr(mp.mpf(5) / 6, 15)});  mu_L/m_e = {mp.nstr(mp.exp(mu_l), 6)}")
    rows.append(["landau", name, "", float(mu_l), float(q_l)])
mu_bench_direct = 3 * mp.pi ** 2
print(f"benchmark MS-bar from e(m_e) = 1 directly (Eq. (run)): ln(mu_L/m_e) = 3 pi^2 = {mp.nstr(mu_bench_direct, 15)}")

# %% [markdown]
# ## The Uehling potential

# %%
def du_urep(r):          # (pi/alpha) dV, m r = r
    return mp.mpf(2) / 3 * mp.quad(lambda u: mp.exp(-2 * r * u) * (1 + 1 / (2 * u * u)) * mp.sqrt(u * u - 1) / u ** 2, [1, 2, mp.inf])


def du_zrep(r):
    return 4 * mp.quad(lambda z: z * (1 - z) * mp.e1(r / mp.sqrt(z * (1 - z))), [0, 0.5, 1])


def du_ft(r):            # -(2/pi) int_0^inf sin(Q r) Pibar(-Q^2)/Q dQ / (-1)
    return 2 / mp.pi * mp.quadosc(lambda Q: mp.sin(Q * r) / Q * pibar(-Q * Q), [0, mp.inf], omega=r)


def du_short(r):
    return mp.mpf(2) / 3 * (-mp.log(r) - mp.euler - mp.mpf(5) / 6)


def du_long(r):
    return mp.sqrt(mp.pi) / 4 * mp.exp(-2 * r) / r ** 1.5


ofs = len(Q2_PTS)
UE = {}
print(f"{'m r':>7} {'(pi/alpha) dV (u)':>22} {'z-rep':>9} {'Fourier':>9} " + " ".join(f"{t:>9}" for t in TOOLS) + f" {'limit':>9}")
for r in R_PTS:
    u, w = unodes_r(r)
    ref = du_urep(r)
    z, f = du_zrep(r), du_ft(r)
    spec = {}
    for tool, vals in TOOLS.items():           # dV = int ds (rho/s) e^(-sqrt(s) r), s = 4u^2: ds/s = 2 du/u
        rh = np.array([-vals[ofs + j].imag / math.pi for j in range(len(u))])
        spec[tool] = float(np.sum(w * rh * 2 / u * np.exp(-2 * r * u)))
    ofs += len(u)
    lim = du_short(r) if r < 0.5 else du_long(r)
    UE[r] = float(ref)
    rel = lambda v: abs(mp.mpf(v) / ref - 1)
    print(f"{r:7.3g} {mp.nstr(ref, 16):>22} {mp.nstr(rel(z), 2):>9} {mp.nstr(rel(f), 2):>9} "
          + " ".join(f"{mp.nstr(rel(spec[t]), 2):>9}" for t in TOOLS) + f" {mp.nstr(lim / ref - 1, 2):>9}")
    rows.append(["uehling", r, "", float(ref), float(z), float(f)] + [spec[t] for t in TOOLS] + [float(lim)])
for r in (mp.mpf("1e-6"), mp.mpf(30)):
    lim = du_short(r) if r < 1 else du_long(r)
    print(f"limit at m r = {mp.nstr(r, 3)}: u-representation / limit - 1 = {mp.nstr(du_urep(r) / lim - 1, 3)}")

# %% [markdown]
# ## Muonic hydrogen (2P - 2S) and hydrogen (2S): first-order Uehling shifts

# %%
def shift_2p2s(m_lep, m_nuc, rho_vals=None):
    """E(2P) - E(2S) from the electron loop, units of m_e, Z = 1; Schroedinger wave functions with the reduced mass.
    int r^2 dr dV(r) [|R21|^2 - |R20|^2] with dV = -(alpha/r)(alpha/pi) int du f(u) e^(-2ur), f = (2/3)(1 + 1/2u^2) sqrt(u^2-1)/u^2:
    the r integral gives (1/a^3)[-1/(2 lam^2) + 1/(a lam^3) - 1/(2 a^2 lam^4)], lam = 1/a + 2u (App. run)."""
    mr = m_lep * m_nuc / (m_lep + m_nuc)
    a = 1 / (ALPHA0 * mr)
    br = lambda u: (-1 / (2 * (1 / a + 2 * u) ** 2) + 1 / (a * (1 / a + 2 * u) ** 3) - 1 / (2 * a ** 2 * (1 / a + 2 * u) ** 4)) / a ** 3
    if rho_vals is None:
        integ = mp.quad(lambda u: mp.mpf(2) / 3 * (1 + 1 / (2 * u * u)) * mp.sqrt(u * u - 1) / u ** 2 * br(u), [1, 2, 10, mp.inf])
    else:                # rho from a tool at the nodes: f(u) du = (pi/alpha) rho(4u^2) 2 du/u
        u, w = unodes_tail()
        integ = mp.fsum(mp.mpf(wi) * rv * 2 / mp.mpf(ui) * br(mp.mpf(ui)) for ui, wi, rv in zip(u, w, rho_vals))
    return -ALPHA0 * ALPHA0 / mp.pi * integ


def shift_2s_hydrogen():
    mr = R_PE / (1 + R_PE)
    a = 1 / (ALPHA0 * mr)
    br = lambda u: (1 / (1 / a + 2 * u) ** 2 - 2 / (a * (1 / a + 2 * u) ** 3) + 3 / (2 * a ** 2 * (1 / a + 2 * u) ** 4)) / (2 * a ** 3)
    full = -ALPHA0 * ALPHA0 / mp.pi * mp.quad(lambda u: mp.mpf(2) / 3 * (1 + 1 / (2 * u * u)) * mp.sqrt(u * u - 1) / u ** 2 * br(u), [1, 2, 10, mp.inf])
    delta = -4 * ALPHA0 ** 5 * mr ** 3 / (15 * mp.pi * 8)
    return full, delta


e_mu = shift_2p2s(R_MUE, R_PE)
ofs_t = len(ALL_Q2) - len(unodes_tail()[0])
LIT_MUH = mp.mpf("205.0074")
print(f"muonic hydrogen E(2P) - E(2S), electron loop (Uehling, NR): {mp.nstr(e_mu * ME_MEV * 1e9, 10)} meV   (literature 205.0074 meV)")
for tool, vals in TOOLS.items():
    rv = [mp.mpf(-vals[ofs_t + j].imag / math.pi) for j in range(len(unodes_tail()[0]))]
    print(f"   with rho from {tool:9}: {mp.nstr(shift_2p2s(R_MUE, R_PE, rv) * ME_MEV * 1e9, 10)} meV")
full, delta = shift_2s_hydrogen()
HZ = ME_MEV * 1e6 / mp.mpf("4.135667696e-15")       # m_e c^2/h in Hz (h in eV s)
mr_h = R_PE / (1 + R_PE)
corr = mp.mpf(5) / 384 * ALPHA0 ** 6 * mr_h ** 4                   # (5/48) alpha (Z alpha)^5 m_r^4/(n^3 m_e^3), n = 2 (App. run)
print(f"hydrogen 2S Uehling shift: {mp.nstr(full * HZ / 1e6, 8)} MHz (full potential), {mp.nstr(delta * HZ / 1e6, 8)} MHz "
      f"(delta-function limit), ratio {mp.nstr(full / delta, 8)};  with the next term (5/384) alpha^6 m_r^4: "
      f"{mp.nstr((delta + corr) * HZ / 1e6, 8)} MHz, ratio {mp.nstr((delta + corr) / delta, 8)} (difference O((Z alpha)^2) = "
      f"{mp.nstr(ALPHA0 ** 2, 2)})")
rows += [["muonic_H_2P2S_meV", "", "", float(e_mu * ME_MEV * 1e9), float(LIT_MUH)],
         ["hydrogen_2S_MHz", "", "", float(full * HZ / 1e6), float(delta * HZ / 1e6)]]

with open(os.path.join(HERE, "results", "running.csv"), "w", newline="") as fh:
    csv.writer(fh).writerows([["kind", "x", "", "value1", "value2", "more..."]] + rows)
print("wrote results/running.csv")

# %% [markdown]
# ## Figure

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
COLORS = {"eff": "C0", "ms": "C1", "lim": "C2"}     # colors of physrev.mplstyle
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))
ax = axes[0]
qs = np.geomspace(1e-2, 1e6, 241)
aeff = np.array([float(1 / (inv_alpha_eff(mp.mpf(q), *PHYS) * ALPHA0)) for q in qs])
ams = np.array([float(1 / (inv_alpha_ms(mp.mpf(q) * mp.exp(-mp.mpf(5) / 6), *PHYS) * ALPHA0)) for q in qs])
ax.plot(qs, aeff, color=COLORS["eff"], lw=1, ls="-", label=r"$\alpha(-Q^2)$ (on shell)")
ax.plot(qs, ams, color=COLORS["ms"], lw=0.8, ls="--", label=r"$\alpha_{\overline{\rm MS}}(e^{-5/6}Q)$")
for m, lab in ((1, r"$m_e$"), (float(R_MUE), r"$m_\mu$")):
    ax.axvline(m, color="0.6", lw=0.5, ls=":")
    ax.text(m * 1.2, 1.036, lab, fontsize=7, color="0.35")
ax.set_xscale("log")
ax.set_ylim(0.99, 1.04)
ax.set_xlabel(r"$Q/m_e$")
ax.set_ylabel(r"$\alpha/\alpha(0)$  (physical $\alpha$, $e$ and $\mu$)")
ax.legend(frameon=False, fontsize=6.5, loc="lower right")
ax = axes[1]
a0b, msb = BENCH
L = np.linspace(0, float(LANDAU["benchmark"][1]) - 1e-3, 400)
ax.plot(np.exp(L), [float(1 / inv_alpha_eff(mp.exp(x), a0b, msb)) for x in L], color=COLORS["eff"], lw=1, ls="-", label="on shell")
Lm = np.linspace(0, float(LANDAU["benchmark"][0]) - 1e-3, 400)
ax.plot(np.exp(Lm + 5 / 6), [float(1 / inv_alpha_ms(mp.exp(x), a0b, msb)) for x in Lm], color=COLORS["ms"], lw=0.8, ls="--",
        label=r"$\overline{\rm MS}$ at $\mu=e^{-5/6}Q$")
ax.axvline(float(mp.exp(LANDAU["benchmark"][1])), color="0.5", lw=0.5, ls=":")
ax.text(float(mp.exp(LANDAU["benchmark"][1])) * 0.4, 0.07, "Landau pole", rotation=90, ha="right", va="bottom", fontsize=7, color="0.35")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(0.05, 20)
ax.set_xlabel(r"$Q/m_e$")
ax.set_ylabel(r"$\alpha$ (benchmark $e(m_e)=1$)")
ax.legend(frameon=False, fontsize=6.5, loc="upper left")
ax = axes[2]
rr = np.geomspace(1e-4, 8, 160)
dv = np.array([float(du_urep(mp.mpf(x))) for x in rr])
ax.plot(rr, dv, color=COLORS["eff"], lw=1, ls="-", label=r"$(\pi/\alpha)\,\delta V/V_C$")
sm, lg = rr < 0.05, rr > 1.0
ax.plot(rr[sm], [float(du_short(mp.mpf(x))) for x in rr[sm]], color=COLORS["lim"], lw=0.75, ls="--", label=r"$m r\ll1$")
ax.plot(rr[lg], [float(du_long(mp.mpf(x))) for x in rr[lg]], color=COLORS["ms"], lw=0.75, ls=":", label=r"$m r\gg1$")
ax.plot(R_PTS, [UE[r] for r in R_PTS], ls="none", marker="o", ms=2.4, color="0.3", label="tools (spectral)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1e-6, 10)
ax.set_xlabel(r"$m_e r$")
ax.set_ylabel(r"Uehling: $(\pi/\alpha)\,\delta V/V_{\rm Coulomb}$")
ax.legend(frameon=False, fontsize=6.5, loc="lower left")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "running.pdf"))
print("wrote ../figs/running.pdf")
if INTERACTIVE:
    plt.show()
