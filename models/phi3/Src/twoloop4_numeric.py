# %% [markdown]
# # Step (16): the two-loop self-energy in d = 4 against TSIL, pySecDec and feyntrop
#
# Research note, step (16).  The two-loop self-energy is Sigma^(2) = g^4/(16 pi^2)^2 Shat (MS-bar, mu = m); Shat in
# terms of eight master integrals comes from the IBP reduction (twoloop4_feyncalc.wl, Kira 3.1 = FIRE 7.1), the masters
# from AMFlow 2.0 (twoloop4_amflow.wl, 30 digits) at s = p^2 = -1, 1, 5, 12 (m = 1).  All masters are compared in the
# normalization of TSIL's "bold" integrals: Euclidean, measure E^(eps gamma_E) d^Dk/pi^(D/2) per loop, propagators
# 1/(k^2 + m^2), i.e. (-1)^(sum nu) E^(L eps gamma_E) times the Minkowski integral with d^Dq/(i pi^(D/2)) and
# 1/(q^2 - m^2 + i0).
# (a) The masters A, B, A B, the vacuum sunrise I, the sunrise S and T, the four-propagator U and the kite M from AMFlow
#     against TSIL 1.46 (Martin, Robertson; twoloop4_tsil.c), coefficient by coefficient in eps.
# (b) The two-loop masters I, S, T, U, M from pySecDec 1.6.6 (sector decomposition, contour deformation above the
#     thresholds), built in work/twoloop4_psd.
# (c) The finite kite M from feyntrop 1.1.0 (tropical Monte Carlo, analytic continuation above the thresholds).
# (d) The finite part of Shat against MR05's renormalized two-loop self-energy of a scalar with a cubic coupling,
#     -(M + V)/2 (TSIL), and the pole mass at the reference point g = m = mu = 1:
#     s_p = m^2 + Sigma1(m^2) + Sigma2(m^2) + Sigma1(m^2) Sigma1'(m^2),  Sigma1 = -g^2 B/(32 pi^2).
# Writes results/twoloop4_comparison.csv and ../figs/twoloop4_d4.pdf.
# Batch (from Src/, after twoloop4_feyncalc.wl and twoloop4_amflow.wl):  ~/miniforge3/envs/qft/bin/python twoloop4_numeric.py
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one.

# %%
import csv
import os
import shutil
import subprocess
import sys
import time

import mpmath as mp

mp.mp.dps = 30
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
RES = os.path.join(HERE, "results")
WORK = os.path.join(HERE, "work")
POINTS = [-1, 1, 5, 12]
os.makedirs(WORK, exist_ok=True)


def read_csv(name):
    with open(os.path.join(RES, name)) as fh:
        return list(csv.DictReader(fh))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300) if abs(b) > 1e-12 else abs(a - b)


# AMFlow masters, TSIL normalization: {(s, name): {eps power: complex}}
NAMES = {"se110": "A", "se111": "B", "se210101": "I", "se201101": "S", "se201102": "T", "se211101": "U",
         "se211111": "M", "se211100": "AB"}
amf = {}
for r in read_csv("twoloop4_amflow.csv"):
    key = (int(r["s"]), NAMES[r["integral"]])
    amf.setdefault(key, {})[int(r["eps_power"])] = complex(mp.mpf(r["re"]), mp.mpf(r["im"]))
shat_amf = {int(r["s"]): complex(mp.mpf(r["re_finite"]), mp.mpf(r["im_finite"])) for r in read_csv("twoloop4_sigma.csv")}
print("AMFlow: ", len(amf), "master values at s =", POINTS)


# %% [markdown]
# ## (a) TSIL 1.46 against AMFlow, coefficient by coefficient

# %%
tsil_bin = os.path.join(WORK, "twoloop4_tsil")
subprocess.run(["cc", "-O2", "-DTSIL_SIZE_DOUBLE", "-I" + os.path.expanduser("~/hep/include"), "-o", tsil_bin,
                os.path.join(HERE, "twoloop4_tsil.c"), "-L" + os.path.expanduser("~/hep/lib"), "-ltsil", "-lm"], check=True)
out = subprocess.run([tsil_bin], capture_output=True, text=True, check=True).stdout
with open(os.path.join(RES, "twoloop4_tsil.csv"), "w") as fh:
    fh.write(out)
tsil = {}
for r in csv.DictReader(out.splitlines()):
    tsil.setdefault((float(r["s"]), r["function"]), {})[int(r["eps_power"])] = complex(float(r["re"]), float(r["im"]))


def tsil_master(s, name):
    if name == "AB":       # product of the one-loop bold integrals
        a, b = tsil[(s, "A")], tsil[(s, "B")]
        return {k: sum(a.get(i, 0) * b.get(k - i, 0) for i in range(-1, 2)) for k in (-2, -1, 0)}
    return tsil[(s, name)]


rows = []
worst_a = {}
for s in POINTS:
    for name in ("A", "B", "AB", "I", "S", "T", "U", "M"):
        t = tsil_master(float(s), name)
        for k, v in t.items():
            d = rel(amf[(s, name)][k], v)
            worst_a[name] = max(worst_a.get(name, 0), d)
            rows.append(["a_tsil", s, name, k, amf[(s, name)][k].real, amf[(s, name)][k].imag, v.real, v.imag, d])
print("(a) largest relative difference AMFlow vs TSIL per master (all points, eps^-2 ... eps^0, A and B to eps^1):")
print("    " + ",  ".join(f"{n} {worst_a[n]:.1e}" for n in worst_a))


# %% [markdown]
# ## (b) pySecDec 1.6.6: the two-loop masters
#
# One package per master in work/twoloop4_psd (regenerated each run), with the prefactor (-1)^(sum nu) E^(2 eps gamma_E)
# that turns pySecDec's Minkowski integral into the TSIL normalization.  GNU make 4 (gmake) is needed for the build.

# %%
# package names: "I" is reserved in pySecDec (sympy's imaginary unit)
PSD_POWERS = {"Ivac": [1, 0, 1, 0, 1], "Ssun": [0, 1, 1, 0, 1], "Tsun": [0, 1, 1, 0, 2], "Ufour": [1, 1, 1, 0, 1], "Mkite": [1, 1, 1, 1, 1]}
PSD_MASTER = {"Ivac": "I", "Ssun": "S", "Tsun": "T", "Ufour": "U", "Mkite": "M"}
psd_dir = os.path.join(WORK, "twoloop4_psd")
if os.path.isdir(psd_dir):
    shutil.rmtree(psd_dir)
os.makedirs(psd_dir)
gen = '''import pySecDec as psd
props = ['(q1)**2-msq', '(q1-p)**2-msq', '(q2)**2-msq', '(q2-p)**2-msq', '(q1-q2)**2-msq']
def li(powers):
    return psd.LoopIntegralFromPropagators(propagators=props, loop_momenta=['q1', 'q2'], external_momenta=['p'],
        powerlist=powers, replacement_rules=[('p*p', 's')], regulators=['eps'], dimensionality='4-2*eps')
if __name__ == "__main__":
    pk = [psd.LoopPackage(name, li(pw), additional_prefactor='(-1)**%d*exp(2*EulerGamma*eps)' % sum(pw))
          for name, pw in @POWERS@.items()]
    psd.sum_package('masters', pk, regulators=['eps'], requested_orders=[0], real_parameters=['s', 'msq'])
'''.replace('@POWERS@', repr(PSD_POWERS))
with open(os.path.join(psd_dir, "generate.py"), "w") as fh:
    fh.write(gen)
t0 = time.time()
subprocess.run([sys.executable, "generate.py"], cwd=psd_dir, check=True, capture_output=True)
subprocess.run(["gmake", "-C", "masters", "disteval", "-j8"], cwd=psd_dir, check=True, capture_output=True)
print(f"(b) pySecDec packages generated and built in {time.time() - t0:.0f} s")

from pySecDec.integral_interface import DistevalLibrary
psd_val = {}
for name in PSD_POWERS:
    lib = DistevalLibrary(os.path.join(psd_dir, "masters", "disteval", name + ".json"), verbose=False)
    for s in POINTS:
        r = lib(parameters={"s": float(s), "msq": 1.0}, epsrel=1e-8, epsabs=1e-12, format="json")["sums"][name]
        psd_val[(s, PSD_MASTER[name])] = {k[0]: (complex(v[0]), abs(complex(v[1]))) for k, v in r.items()}
worst_b, pull_b = {}, {}
for (s, name), d in psd_val.items():
    for k, (v, err) in d.items():
        ref = amf[(s, name)][k]
        worst_b[name] = max(worst_b.get(name, 0), rel(v, ref))
        pull_b[name] = max(pull_b.get(name, 0), abs(v - ref) / max(err, 1e-300))
        rows.append(["b_pysecdec", s, name, k, v.real, v.imag, ref.real, ref.imag, rel(v, ref)])
print("(b) pySecDec vs AMFlow, largest relative difference / largest |difference|/error per master:")
print("    " + ",  ".join(f"{n} {worst_b[n]:.1e} / {pull_b[n]:.1f}" for n in PSD_MASTER.values()))


# %% [markdown]
# ## (c) feyntrop 1.1.0: the finite kite M
#
# Graph: external vertices 0 (p in) and 1 (p out), internal vertices 2, 3; edges (0,2) q1, (0,3) p-q1, (2,1) q2,
# (3,1) p-q2, (2,3) q1-q2.  sp[0,0] = p^2 = s.  The deformation parameter Lambda is used above the thresholds.

# %%
sys.path.append(os.path.expanduser("~/hep/feyntrop-1.1.0"))
cwd0 = os.getcwd()
os.chdir(os.path.expanduser("~/hep/feyntrop-1.1.0"))          # py_feyntrop calls ./feyntrop
from py_feyntrop import tropical_integration, sp
EDGES = [((0, 2), 1, 'mm'), ((0, 3), 1, 'mm'), ((2, 1), 1, 'mm'), ((3, 1), 1, 'mm'), ((2, 3), 1, 'mm')]
ft_val = {}
for s in POINTS:
    res, _ = tropical_integration(int(1e8), 4, 0.5 if s > 4 else 0.0, 1, EDGES, [(sp[0, 0], 'pp')], [('mm', 1), ('pp', s)])
    (re, dre), (im, dim) = res[0][0], res[0][1]       # prefactor Gamma(1 + 2 eps) = 1 at eps^0
    ft_val[s] = (complex(re, im), abs(complex(dre, dim)))
os.chdir(cwd0)
print("(c) feyntrop kite M vs AMFlow:")
for s in POINTS:
    v, err = ft_val[s]
    ref = amf[(s, "M")][0]
    rows.append(["c_feyntrop", s, "M", 0, v.real, v.imag, ref.real, ref.imag, rel(v, ref)])
    print(f"    s = {s:3d}: {v.real:.6f} {v.imag:+.6f} i  (error {err:.1e})  vs  {ref.real:.6f} {ref.imag:+.6f} i;  "
          f"|difference|/error {abs(v - ref) / err:.1f}")


# %% [markdown]
# ## (d) The two-loop self-energy and the pole mass

# %%
print("(d) finite part of Shat: AMFlow (Kira/FIRE reduction + counterterm insertion) vs MR05 -(M + V)/2 (TSIL):")
for s in POINTS:
    ref = tsil[(float(s), "Shat_MR05")][0]
    rows.append(["d_shat", s, "Shat", 0, shat_amf[s].real, shat_amf[s].imag, ref.real, ref.imag, rel(shat_amf[s], ref)])
    print(f"    s = {s:3d}: {shat_amf[s].real:.15f} {shat_amf[s].imag:+.15f} i  vs  {ref.real:.15f} {ref.imag:+.15f} i;  "
          f"relative difference {rel(shat_amf[s], ref):.1e}")


def b_fin(s):          # MS-bar B at m = mu = 1, Feynman-parameter integral
    return -mp.quad(lambda x: mp.log(1 - x * (1 - x) * s), [0, 1])


def db_ds(s):
    return mp.quad(lambda x: x * (1 - x) / (1 - x * (1 - x) * s), [0, 1])


g = 1
f = 1 / (16 * mp.pi**2)
b1, bp1 = b_fin(1), db_ds(1)
sig1, sig1p = -g**2 * b1 * f / 2, -g**2 * bp1 * f / 2
sp1 = 1 + sig1
sp2 = 1 + sig1 + g**4 * f**2 * mp.mpf(shat_amf[1].real) + sig1 * sig1p
t1 = tsil[(1.0, "pole_mass_sq_one_loop")][0].real
t2 = tsil[(1.0, "pole_mass_sq_two_loop")][0].real
print(f"(d) B(m^2) = {mp.nstr(b1, 15)} (2 - pi/sqrt 3 = {mp.nstr(2 - mp.pi / mp.sqrt(3), 15)}),  dB/ds(m^2) = {mp.nstr(bp1, 15)} "
      f"(TSIL {tsil[(1.0, 'dBds_at_x')][0].real:.15f})")
print(f"(d) pole mass squared at g = m = mu = 1: one loop {mp.nstr(sp1, 15)} (TSIL {t1:.15f}),  two loops {mp.nstr(sp2, 15)} "
      f"(TSIL {t2:.15f});  relative difference {abs(float(sp2) - t2) / t2:.1e}")
print(f"    coefficients: m_p^2/m^2 = 1 + a1 g^2/m^2 + a2 g^4/m^4,  a1 = {mp.nstr(-b1 * f / 2, 10)},  "
      f"a2 = {mp.nstr(f**2 * (mp.mpf(shat_amf[1].real) + b1 * bp1 / 4), 10)}")
rows.append(["d_pole", 1, "pole_mass_sq_two_loop_g1", 0, float(sp2), 0.0, t2, 0.0, abs(float(sp2) - t2) / t2])


# %% [markdown]
# ## Figure: Shat(s) from TSIL with the AMFlow points

# %%
import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False     # legends without the white box of physrev.mplstyle
grid = list(csv.DictReader(subprocess.run([tsil_bin, "grid"], capture_output=True, text=True, check=True).stdout.splitlines()))
sg = [float(r["s"]) for r in grid]
fig, ax = plt.subplots(figsize=(3.4, 2.5))
ax.plot(sg, [float(r["re"]) for r in grid], color="C0", label=r"Re (TSIL)")
ax.plot(sg, [float(r["im"]) for r in grid], color="C1", ls="--", label=r"Im (TSIL)")
ax.plot(POINTS, [shat_amf[s].real for s in POINTS], "o", ms=3.5, color="C0", label="Re (AMFlow)")
ax.plot(POINTS, [shat_amf[s].imag for s in POINTS], "s", ms=3.5, color="C1", label="Im (AMFlow)")
for th in (4, 9):
    ax.axvline(th, color="0.7", lw=0.6, ls=":")
ax.set_xlabel(r"$s/m^2$")
ax.set_ylabel(r"$\hat\Sigma=\Sigma^{(2)}(16\pi^2)^2/g^4$")
ax.legend(frameon=False, fontsize=7)
fig.tight_layout()
figdir = os.path.join(HERE, "..", "figs")
fig.savefig(os.path.join(figdir, "twoloop4_d4.pdf"))
print("wrote ../figs/twoloop4_d4.pdf")


# %% [markdown]
# ## Output

# %%
with open(os.path.join(RES, "twoloop4_comparison.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["check", "s", "quantity", "eps_power", "re", "im", "re_ref", "im_ref", "rel_diff"])
    for r in rows:
        w.writerow([r[0], r[1], r[2], r[3]] + [f"{x:.15e}" for x in r[4:8]] + [f"{r[8]:.3e}"])
print("wrote results/twoloop4_comparison.csv")
