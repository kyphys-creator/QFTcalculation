# %% [markdown]
# # Step (7): the two-loop masters with pySecDec; two-loop running of alpha_s and Lambda_QCD
#
# Research note models/qcd, step (7), Eqs. (z2), (run2), App. G.
# (a) pySecDec 1.6.6 (sector decomposition, Euclidean point q^2 = -1) for the two masters of twoloop_feyncalc.wl, bubble^2
#     J[k2, {1,1,1,1,0}] and sunset J[k2, {1,0,0,1,1}], with the prefactor E^(2 eps gamma_E) of J = E^(eps gamma_E) int d^Dl/(i pi^(D/2))
#     per loop, against the exact Gamma-function forms (results/twoloop_masters.csv, twoloop_eval.wl).
# (b) Two-loop running, a = alpha_s:  da/d ln mu^2 = -b0 a^2 - b1 a^3,  b0 = beta_0/(4 pi), b1 = beta_1/(4 pi)^2,
#     beta_0 = 11 - 2 n_f/3, beta_1 = 102 - 38 n_f/3 (SU(3); beta_1 of step (7)).  Exact implicit solution
#         b0 ln(mu^2/mu0^2) = 1/a - 1/a0 + (b1/b0) ln[a (b0 + b1 a0)/(a0 (b0 + b1 a))]
#     against a numerical integration (SciPy) and MadGraph's ALPHAS(Q) with nloop = 2 (work/alfas_mg5 2; Template/LO/Source/
#     alfas_functions.f solves the same implicit equation by Newton's method), alpha_s^(5)(M_Z) = 0.118, n_f = 5 for 5 GeV - 1 TeV.
# (c) Lambda: the exact two-loop convention  ln(mu^2/Lambda^2) = 1/(b0 a) + (b1/b0^2) ln[b0 a/(1 + b1 a/b0)]  (the implicit solution
#     with mu0 -> Lambda) and the truncated expansion  a = [1 - (b1/b0^2) ln t/t]/(b0 t), t = ln(mu^2/Lambda^2);  Lambda^(6) from
#     alpha_s^(6)(m_t) = alpha_s^(5)(m_t) (one-loop matching at mu = m_t, enough for two-loop running).
# Writes results/twoloop_numeric.csv and ../figs/twoloop_running.pdf.
# Usage (from Src/, after twoloop_eval.wl):  ~/miniforge3/envs/qft/bin/python twoloop_numeric.py.  Interactive: "Run Cell" in VS Code.

# %%
import csv
import math
import os
import shutil
import subprocess
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    import matplotlib
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
WORK = os.path.join(HERE, "work")
MZ, MT, ASMZ = 91.188, 172.5, 0.118
rows = []


def beta(nf):
    return 11 - 2 * nf / 3, 102 - 38 * nf / 3


exact = {}
with open(os.path.join(HERE, "results", "twoloop_masters.csv")) as fh:
    for r in csv.DictReader(fh, delimiter=";"):
        exact[r["master"]] = [float(r[k]) for k in ("eps-2", "eps-1", "eps0", "eps1", "eps2")]
exact                                      # inspect

# %% [markdown]
# ## (a) pySecDec 1.6.6: the two masters at q^2 = -1

# %%
PSD = {"bub2": ([1, 1, 1, 1, 0], "{1, 1, 1, 1, 0}"), "sun": ([1, 0, 0, 1, 1], "{1, 0, 0, 1, 1}")}
psd_dir = os.path.join(WORK, "twoloop_psd")
if os.path.isdir(psd_dir):
    shutil.rmtree(psd_dir)
os.makedirs(psd_dir)
gen = '''import pySecDec as psd
props = ['(l1)**2', '(l2)**2', '(l1-q)**2', '(l2-q)**2', '(l1-l2)**2']
def li(powers):
    return psd.LoopIntegralFromPropagators(propagators=props, loop_momenta=['l1', 'l2'], external_momenta=['q'],
        powerlist=powers, replacement_rules=[('q*q', 's')], regulators=['eps'], dimensionality='4-2*eps')
if __name__ == "__main__":
    pk = [psd.LoopPackage(name, li(pw), additional_prefactor='exp(2*EulerGamma*eps)') for name, pw in @POWERS@.items()]
    psd.sum_package('masters', pk, regulators=['eps'], requested_orders=[1], real_parameters=['s'])
'''.replace('@POWERS@', repr({k: v[0] for k, v in PSD.items()}))
with open(os.path.join(psd_dir, "generate.py"), "w") as fh:
    fh.write(gen)
t0 = time.time()
subprocess.run([sys.executable, "generate.py"], cwd=psd_dir, check=True, capture_output=True)
subprocess.run(["gmake", "-C", "masters", "disteval", "-j8"], cwd=psd_dir, check=True, capture_output=True)
print(f"(a) pySecDec packages generated and built in {time.time() - t0:.0f} s")
from pySecDec.integral_interface import DistevalLibrary
for name, (pw, key) in PSD.items():
    lib = DistevalLibrary(os.path.join(psd_dir, "masters", "disteval", name + ".json"), verbose=False)
    r = lib(parameters={"s": -1.0}, epsrel=1e-10, epsabs=1e-14, format="json")["sums"][name]
    ref = exact[key]
    for k, v in r.items():
        val, err = complex(v[0]), abs(complex(v[1]))
        e = ref[k[0] + 2]
        rows.append(["a_pysecdec", key, k[0], val.real, val.imag, e, abs(val - e), err])
        print(f"(a) J[k2, {key}] eps^{k[0]:+d}: pySecDec {val.real:+.12f} {val.imag:+.1e}i (+- {err:.1e}), exact {e:+.12f}, "
              f"|diff| {abs(val - e):.1e}")

# %% [markdown]
# ## (b) two-loop running: exact implicit solution, numerical integration, MadGraph (nloop = 2)

# %%
def a2loop(mu, a0=ASMZ, mu0=MZ, nf=5):
    b0, b1 = (x / (4 * math.pi) ** k for x, k in zip(beta(nf), (1, 2)))
    rhs = b0 * math.log(mu * mu / (mu0 * mu0))
    f = lambda a: 1 / a - 1 / a0 + b1 / b0 * math.log(a * (b0 + b1 * a0) / (a0 * (b0 + b1 * a))) - rhs
    return brentq(f, 1e-4, 5.0, xtol=1e-16, rtol=1e-15)


def a1loop(mu, a0=ASMZ, mu0=MZ, nf=5):
    return a0 / (1 + beta(nf)[0] / (4 * math.pi) * a0 * math.log(mu * mu / (mu0 * mu0)))


qs = np.geomspace(5.0, 1000.0, 41)
b0, b1 = beta(5)[0] / (4 * math.pi), beta(5)[1] / (4 * math.pi) ** 2
sol = solve_ivp(lambda t, y: [-b0 * y[0] ** 2 - b1 * y[0] ** 3], [0, math.log(qs[-1] ** 2 / MZ ** 2)], [ASMZ], rtol=1e-12, atol=1e-15,
                dense_output=True, method="DOP853")
sol_dn = solve_ivp(lambda t, y: [-b0 * y[0] ** 2 - b1 * y[0] ** 3], [0, math.log(qs[0] ** 2 / MZ ** 2)], [ASMZ], rtol=1e-12, atol=1e-15,
                   dense_output=True, method="DOP853")
num = np.array([(sol if q >= MZ else sol_dn).sol(math.log(q * q / MZ ** 2))[0] for q in qs])
ex2 = np.array([a2loop(q) for q in qs])
print(f"(b) two-loop alpha_s^(5): numerical integration vs the implicit solution, 5 GeV - 1 TeV: max relative deviation "
      f"{np.max(np.abs(num / ex2 - 1)):.1e}")
mg = {}
for nl in (1, 2):
    out = subprocess.run([os.path.join(WORK, "alfas_mg5"), str(nl)], input="".join(f"{q:.17e}\n" for q in qs), capture_output=True,
                         text=True, check=True).stdout
    mg[nl] = np.array([float(line.split()[1]) for line in out.split("\n") if line.strip()])
d1 = np.max(np.abs(mg[1] / np.array([a1loop(q) for q in qs]) - 1))
d2 = np.max(np.abs(mg[2] / ex2 - 1))
print(f"(b) MadGraph ALPHAS against the closed forms: nloop = 1 {d1:.1e}, nloop = 2 {d2:.1e}  (41 scales, 5 GeV - 1 TeV)")
# MadGraph's NEWTON1 stops when the relative Newton step is below TOL = 5e-4 (quadratic convergence leaves <~ (5e-4)^2);
# one more Newton step on its own equation, b0 T + F2(a_in) - F2(a) = 0 with F2(a) = 1/a + C1 ln(C1 a/(1 + C1 a)), C1 = b1/b0:
c1 = b1 / b0
f2 = lambda a: 1 / a + c1 * math.log(c1 * a / (1 + c1 * a))
step = lambda a, q: a - (b0 * math.log(q * q / MZ ** 2) + f2(ASMZ) - f2(a)) * a * a * (1 + c1 * a)
d2n = np.max(np.abs(np.array([step(a, q) for a, q in zip(mg[2], qs)]) / ex2 - 1))
print(f"(b) MadGraph nloop = 2 after one more Newton step: {d2n:.1e}  (the 1.8e-7 is MadGraph's stopping tolerance TOL = 5e-4)")
rows.append(["b_running", "madgraph_nloop2_one_more_newton_step", "", d2n, 0, 0, 0, 0])
rows += [["b_running", "numerical", "", float(np.max(np.abs(num / ex2 - 1))), 0, 0, 0, 0],
         ["b_running", "madgraph_nloop1", "", d1, 0, 0, 0, 0], ["b_running", "madgraph_nloop2", "", d2, 0, 0, 0, 0]]
for q in (5.0, MT, 1000.0):
    print(f"    alpha_s^(5)({q:g} GeV): one loop {a1loop(q):.6f}, two loops {a2loop(q):.6f}")

# %% [markdown]
# ## (c) Lambda_QCD at one and two loops

# %%
def lam_exact(a, mu, nf):
    b0, b1 = beta(nf)[0] / (4 * math.pi), beta(nf)[1] / (4 * math.pi) ** 2
    return mu * math.exp(-0.5 * (1 / (b0 * a) + b1 / b0 ** 2 * math.log(b0 * a / (1 + b1 * a / b0))))


def lam_trunc(a, mu, nf):
    b0, b1 = beta(nf)[0] / (4 * math.pi), beta(nf)[1] / (4 * math.pi) ** 2
    f = lambda L: (lambda t: (1 - b1 / b0 ** 2 * math.log(t) / t) / (b0 * t))(math.log(mu * mu / (L * L))) - a
    return brentq(f, 1e-3, 1.0, xtol=1e-15)


def lam_1loop(a, mu, nf):
    return mu * math.exp(-2 * math.pi / (beta(nf)[0] * a))


a5mt = a2loop(MT)
lams = {"one loop": (lam_1loop(ASMZ, MZ, 5), lam_1loop(a1loop(MT), MT, 6)),
        "two loops, exact": (lam_exact(ASMZ, MZ, 5), lam_exact(a5mt, MT, 6)),
        "two loops, truncated": (lam_trunc(ASMZ, MZ, 5), lam_trunc(a5mt, MT, 6))}
for k, (l5, l6) in lams.items():
    print(f"(c) Lambda^(5) = {1e3 * l5:7.2f} MeV, Lambda^(6) = {1e3 * l6:7.2f} MeV  ({k})")
    rows.append(["c_lambda", k, "", l5, l6, 0, 0, 0])
# the exact convention is the implicit solution with mu0 -> Lambda: it reproduces alpha_s(M_Z) at any mu
print(f"(c) check: two-loop alpha_s^(5)(m_t) from Lambda^(5) (exact convention) = "
      f"{brentq(lambda a: lam_exact(a, MT, 5) - lams['two loops, exact'][0], 0.01, 1.0, xtol=1e-16):.12f}, from M_Z: {a5mt:.12f}")
with open(os.path.join(HERE, "results", "twoloop_numeric.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["kind", "item", "order", "value1", "value2", "reference", "abs_dev", "error"])
    w.writerows(rows)
print("wrote results/twoloop_numeric.csv")

# %% [markdown]
# ## Figure: alpha_s at one and two loops; the size of the two-loop term

# %%
plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))
qq = np.geomspace(2.0, 1e4, 300)
ax = axes[0]
ax.plot(qq, [a1loop(q) for q in qq], color="C0", lw=1, ls="--", label="one loop")
ax.plot(qq, [a2loop(q) for q in qq], color="C1", lw=1, ls="-", label="two loops")
ax.plot(qs[::4], mg[1][::4], ls="none", marker="o", ms=2.8, color="C0", label="MadGraph, nloop = 1")
ax.plot(qs[::4], mg[2][::4], ls="none", marker="s", ms=2.8, color="C1", label="MadGraph, nloop = 2")
ax.set_xscale("log")
ax.set_xlabel(r"$\mu$ [GeV]")
ax.set_ylabel(r"$\alpha_s^{(5)}(\mu)$")
ax.set_title(r"$\alpha_s^{(5)}(M_Z)=0.118$", fontsize=8)
ax.legend(frameon=False, fontsize=6.5, loc="upper right")
ax = axes[1]
ax.plot(qq, [a2loop(q) / a1loop(q) - 1 for q in qq], color="C1", lw=1)
ax.axhline(0, color="0.6", lw=0.5)
ax.set_xscale("log")
ax.set_xlabel(r"$\mu$ [GeV]")
ax.set_ylabel(r"$\alpha_s^{\rm 2\,loop}/\alpha_s^{\rm 1\,loop}-1$")
ax.set_title(r"$\Lambda^{(5)}$: %.0f MeV (one loop), %.0f MeV (two loops)" % (1e3 * lams["one loop"][0], 1e3 * lams["two loops, exact"][0]), fontsize=8)
fig.tight_layout()
os.makedirs(os.path.join(HERE, "..", "figs"), exist_ok=True)
fig.savefig(os.path.join(HERE, "..", "figs", "twoloop_running.pdf"))
print("wrote ../figs/twoloop_running.pdf")
if INTERACTIVE:
    plt.show()
