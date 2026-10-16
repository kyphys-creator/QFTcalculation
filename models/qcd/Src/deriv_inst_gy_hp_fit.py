# %% [markdown]
# # Appendix check: the m^-8 coefficient c8 from the high-precision Gel'fand-Yaglom values of Gamma~'' and Gamma~'''
#
# Research note models/qcd, derivations of the appendices (numpy, sympy).  app:inst 「大きい質量の展開。」 and the step (10) checks
# (「文献との食い違い。」): Gamma~ = -(1/12) ln u + sum_k c_2k u^-k (u = (m rho)^2, rho = 1) with c2, c4, c6 = -1/75, -17/735, 232/2835 and
# c_2k = -Gamma(k) A_{k+2} from the DeWitt recursion (deriv_inst_dewitt_modp.py: A_6, A_7, A_8; NMAX = 9, 10: A_9, A_10).  Weighted
# least-squares fits of G2 = Gamma~'' and G3 = Gamma~''' (results/inst_gy_hp.csv, the 17 masses m rho = 2.5..10 of the base set) jointly:
# (a) all coefficients free from c2 (reproduces c2, c4, c6);
# (b) c8 fixed to the recursion value -51248/190575 or to the literature value -7916/148225, c10.. free: chi^2 comparison;
# (c) c8, c10 (c8..c12, c8..c14) fixed to the recursion values, the higher ones free;
# (d) c8 free (c2..c6 exact): stability over fit windows and numbers of terms, and the envelope of the fits with chi^2/dof < 1;
# (e) c8..c16 free: the full coefficient lists;
# (f) hypothesis tests allowing many (possibly large) higher coefficients: c8 free, = literature, = recursion, c8..c14 = recursion
#     (then c16 against the recursion's -Gamma(8) A_10);
# (g) an additional exponentially small term C e^{-2 a m} m^p cannot mimic the series;
# (h) table of Gamma~, Gamma~'', Gamma~''' and of Gamma~ minus the series (c8..c14 fitted, m >= 3.5); the figure R_j -> c8 against 1/u
#     (work/inst_gy_hp/c8_extrapolation.png, not used in the note).
# Reads results/inst_gy_hp.csv (deriv_inst_gy_hp.py).  Writes work/inst_gy_hp/c8_extrapolation.png; run_deriv_inst_a6_check.sh saves the
# printed output as results/deriv_inst_gy_hp_fit.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_gy_hp_fit.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import os
import sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
import matplotlib
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

# %% [markdown]
# ## The data (base set, m rho >= 2.5) and the coefficients of the series

# %%
D = np.genfromtxt(os.path.join(HERE, "results", "inst_gy_hp.csv"), delimiter=",", names=True)
ALL = D
D = D[D["m"] >= 2.5 - 1e-9]
ms, G, E = D["m"], {2: D["G2"], 3: D["G3"]}, {2: D["dG2"], 3: D["dG3"]}
KNOWN = {1: -1/75, 2: -17/735, 3: 232/2835}
DEWITT = {4: -51248/190575, 5: 26137856/32207175, 6: -1062272/8783775,
          7: -720*40094573632/586396035225}   # c14 = -Gamma(7) A_9 (recursion rerun with NMAX = 9) = -49.23
LIT8 = -7916/148225
A10 = Fr(-11563272201088, 57733355104425)    # deriv_inst_dewitt_modp.py 10
C16 = -5040*A10                              # c16 = -Gamma(8) A_10
print(f"{len(ms)} masses m rho = {ms.min():g}..{ms.max():g}; recursion: c8 = {DEWITT[4]:+.6f}, c10 = {DEWITT[5]:+.6f}, c12 = {DEWITT[6]:+.6f},"
      f" c14 = {DEWITT[7]:+.4f}, c16 = {float(C16):+.2f};  literature c8 = {LIT8:+.6f}")
ms          # inspect: the masses

# %% [markdown]
# ## The fit: Gamma~'' and Gamma~''' of u^-k and of the logarithm

# %%
def bas(u, j, k):
    if j == 2: return k*(k + 1)*u**(-k - 2)
    if j == 3: return -k*(k + 1)*(k + 2)*u**(-k - 3)
def logpart(u, j):
    return 1/(12*u**2) if j == 2 else -1/(6*u**3)

def fit(ms, G, E, js, fixed, free):
    """weighted least squares; errors of the coefficients scaled by sqrt(chi2/dof) when > 1"""
    rows, rhs = [], []
    for j in js:
        for i, m in enumerate(ms):
            u = m*m
            y = G[j][i] - logpart(u, j) - sum(c*bas(u, j, k) for k, c in fixed.items())
            rows.append([bas(u, j, k)/E[j][i] for k in free]); rhs.append(y/E[j][i])
    A = np.array(rows); b = np.array(rhs)
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    cov = np.linalg.inv(A.T @ A); chi2 = float(((A @ c - b)**2).sum()); dof = max(len(b) - len(free), 1)
    s = max(1.0, np.sqrt(chi2/dof))
    return dict(zip(free, c)), dict(zip(free, np.sqrt(np.diag(cov))*s)), chi2/dof

def show(tag, c, e, chi):
    s = ", ".join(f"c{2*k} = {c[k]:+.6g} +- {e[k]:.1e}" for k in sorted(c))
    print(f"  {tag}: {s}  chi2/dof = {chi:.3g}")

sub = lambda sel: ({j: G[j][sel] for j in (2, 3)}, {j: E[j][sel] for j in (2, 3)})
fit(ms[ms >= 3.5 - 1e-9], *sub(ms >= 3.5 - 1e-9), (2, 3), dict(KNOWN), [4, 5, 6, 7])          # inspect: c8..c14 free, m >= 3.5

# %% [markdown]
# ## (a)-(e) Fits

# %%
print("(a) all coefficients free from c2 (known: c2 = -0.0133333, c4 = -0.0231293, c6 = 0.0818342)")
for mmin in (3.0, 3.5, 4.0):
    sel = ms >= mmin - 1e-9
    for nf in (6, 7, 8):
        c, e, chi = fit(ms[sel], *sub(sel), (2, 3), {}, list(range(1, 1 + nf)))
        show(f"m>={mmin} {nf} free", {k: c[k] for k in list(c)[:5]}, e, chi)
print("(b) c8 fixed: DeWitt vs literature; c10.. free")
for name, c8 in (("DeWitt", DEWITT[4]), ("literature", LIT8)):
    for mmin in (3.0, 3.5, 4.0):
        sel = ms >= mmin - 1e-9
        for nf in (2, 3, 4):
            c, e, chi = fit(ms[sel], *sub(sel), (2, 3), {**KNOWN, 4: c8}, list(range(5, 5 + nf)))
            show(f"c8 {name:10s} m>={mmin} {nf} free", c, e, chi)
print("(c) c8, c10 fixed to DeWitt (c12.. free); c8..c12 fixed (c14.. free); c8..c14 fixed (c16.. free)")
for nfix in (5, 6, 7):
    for mmin in (3.0, 3.25, 3.5, 3.75, 4.0, 4.5):
        sel = ms >= mmin - 1e-9
        for nf in (1, 2, 3, 4):
            fx = dict(KNOWN); fx.update({k: v for k, v in DEWITT.items() if k <= nfix})
            c, e, chi = fit(ms[sel], *sub(sel), (2, 3), fx, list(range(nfix + 1, nfix + 1 + nf)))
            show(f"fixed through c{2*nfix} m>={mmin} {nf} free", c, e, chi)
print("(d) c8 free with c2..c6 known: stability table")
for mmin in (3.0, 3.25, 3.5, 3.75, 4.0, 4.5):
    for mmax in (6.0, 8.0, 10.0):
        sel = (ms >= mmin - 1e-9) & (ms <= mmax + 1e-9)
        for nf in (3, 4, 5):
            if sel.sum() < nf + 2: continue
            c, e, chi = fit(ms[sel], *sub(sel), (2, 3), dict(KNOWN), list(range(4, 4 + nf)))
            show(f"m=[{mmin},{mmax}] {nf} free", {k: c[k] for k in list(c)[:3]}, e, chi)
print("(e) c8..c16 free (c2..c6 known): full coefficient lists incl. c14")
for mmin in (3.0, 3.25, 3.5, 3.75, 4.0):
    sel = ms >= mmin - 1e-9
    for nf in (4, 5, 6):
        c, e, chi = fit(ms[sel], *sub(sel), (2, 3), dict(KNOWN), list(range(4, 4 + nf)))
        show(f"m>={mmin} {nf} free", c, e, chi)
# summary: envelope of acceptable (chi2/dof < 1) fits in (d)
acc = []
for mmin in (3.0, 3.25, 3.5, 3.75, 4.0, 4.5):
    for mmax in (6.0, 8.0, 10.0):
        sel = (ms >= mmin - 1e-9) & (ms <= mmax + 1e-9)
        for nf in (3, 4, 5):
            if sel.sum() < nf + 2: continue
            c, e, chi = fit(ms[sel], *sub(sel), (2, 3), dict(KNOWN), list(range(4, 4 + nf)))
            if chi < 1: acc.append((c[4], c[5], c[6]))
acc = np.array(acc)
print(f"SUMMARY (d), {len(acc)} fits with chi2/dof < 1: c8 in [{acc[:,0].min():.5f}, {acc[:,0].max():.5f}], mean {acc[:,0].mean():.5f};"
      f" c10 in [{acc[:,1].min():.4f}, {acc[:,1].max():.4f}]; c12 in [{acc[:,2].min():.3f}, {acc[:,2].max():.3f}]")
acc[:, 0]          # inspect: c8 of the acceptable fits of (d)

# %% [markdown]
# ## (f) Hypothesis tests with many free higher coefficients

# %%
hyps = [("c8 free", {}, 4), ("c8 = literature", {4: LIT8}, 5), ("c8 = recursion", {4: DEWITT[4]}, 5),
        ("c8,c10 = recursion", {k: DEWITT[k] for k in (4, 5)}, 6),
        ("c8..c12 = recursion", {k: DEWITT[k] for k in (4, 5, 6)}, 7), ("c8..c14 = recursion", dict(DEWITT), 8)]
print("(f) hypothesis tests (c2..c6 exact; nf free higher coefficients for m >= m_min)")
for name, fx, k0 in hyps:
    print(f"=== {name}")
    for mmin in (3.0, 3.5, 4.0, 4.5, 5.0):
        sel = ms >= mmin - 1e-9
        for nf in (3, 4, 5, 6):
            if sel.sum()*2 <= nf + 2: continue
            c, e, chi = fit(ms[sel], *sub(sel), (2, 3), {**KNOWN, **fx}, list(range(k0, k0 + nf)))
            print(f"  m>={mmin} n={sel.sum():2d} {nf} free: chi2/dof = {chi:9.3g}   " + ", ".join(f"c{2*k}={c[k]:+.4g}(+-{e[k]:.1g})" for k in sorted(c)))
print(f"recursion (deriv_inst_dewitt_modp.py 10): A_10 = {A10}, c16 = -Gamma(8) A_10 = {C16} = {float(C16):+.2f}")

# %% [markdown]
# ## (g) An additional exponentially small term C e^{-2 a m} m^p

# %%
uu, P, Aa = sp.symbols('u p a', positive=True)
f = sp.exp(-2*Aa*sp.sqrt(uu))*uu**(P/2)
fd = {j: sp.lambdify((uu, P, Aa), sp.diff(f, uu, j), 'numpy') for j in (2, 3)}
def fit_exp(sel, fixed, free, p=None, a=1.0):
    rows, rhs = [], []
    for j in (2, 3):
        for m, g, e in zip(ms[sel], G[j][sel], E[j][sel]):
            u = m*m
            y = g - logpart(u, j) - sum(c*bas(u, j, k) for k, c in fixed.items())
            r = [bas(u, j, k) for k in free] + ([fd[j](u, p, a)] if p is not None else [])
            rows.append(np.array(r)/e); rhs.append(y/e)
    Am = np.array(rows); b = np.array(rhs)
    sc = np.abs(Am).max(0); c, *_ = np.linalg.lstsq(Am/sc, b, rcond=None); c = c/sc
    chi = float(((Am @ c - b)**2).sum())/max(len(b) - len(c), 1)
    return c, chi
KN, DW = KNOWN, DEWITT
print("(g) fits with an additional term C e^(-2 a m) m^p")
for mmin in (3.0, 3.5):
    sel = ms >= mmin - 1e-9
    print(f"--- m >= {mmin}")
    for a in (1.0, 2.0):
        for p in (-4, -2, 0, 2, 4):
            c3, chi3 = fit_exp(sel, {**KN, 4: DW[4]}, [5, 6, 7], p, a)
            c4, chi4 = fit_exp(sel, {**KN, 4: DW[4], 5: DW[5]}, [6, 7, 8], p, a)
            c2, chi2 = fit_exp(sel, {**KN, **{k: v for k, v in DW.items() if k <= 6}}, [7, 8], p, a)
            c5, chi5 = fit_exp(sel, {**KN, **DW}, [8, 9], p, a)
            print(f"  e^(-2*{a}*m) m^{p:+d}: c8 fixed: c10 = {c3[0]:+.4f} c12 = {c3[1]:+.3f} chi2/dof = {chi3:.3g} | "
                  f"c8,c10 fixed: c12 = {c4[0]:+.3f} chi2/dof = {chi4:.3g} | c8..c12 fixed: chi2/dof = {chi2:.3g} | c8..c14 fixed: chi2/dof = {chi5:.3g}")

# %% [markdown]
# ## (h) Table and figure

# %%
sel = ms >= 3.5 - 1e-9
c, e, chi = fit(ms[sel], {j: G[j][sel] for j in (2, 3)}, {j: E[j][sel] for j in (2, 3)}, (2, 3), dict(KNOWN), [4, 5, 6, 7])
cs = {**KNOWN, **c}
ser = lambda m: -np.log(m)/6 + sum(v*m**(-2*k) for k, v in cs.items())
print("(h) isospin 1/2 scalar in the BPST background, rho = 1, u = (m rho)^2.  Gamma~ as in note eq:instmass (MS-bar, DHLM counterterms).")
print("    G2 = d^2 Gamma~/du^2, G3 = d^3 Gamma~/du^3 (no counterterm/alpha dependence); errors: tail-fit spread + integration-parameter check")
print(f"    last column: Gamma~ - large-m series with c2..c6 exact and c8..c14 fitted (m>=3.5): {', '.join(f'c{2*k}={v:+.5f}' for k, v in c.items())}")
print(f"#{'m':>6} {'Gamma~(m)':>20} {'err':>8} {'Gamma~2(u)':>24} {'err':>8} {'Gamma~3(u)':>24} {'err':>8} {'Gamma~-series':>14}")
for r in ALL:
    m = r["m"]; dser = r["G0"] - ser(m) if m >= 2.5 else np.nan
    print(f"{m:7.3f} {r['G0']:+20.12e} {r['dG0']:8.1e} {r['G2']:+24.16e} {r['dG2']:8.1e} {r['G3']:+24.16e} {r['dG3']:8.1e} {dser:+14.2e}")

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
plt.rcParams["legend.frameon"] = False
u = ms**2
def known(u, j): return logpart(u, j) + sum(c*bas(u, j, k) for k, c in KNOWN.items())
R2 = (G[2] - known(u, 2))*u**6/20; R3 = (G[3] - known(u, 3))*u**7/(-120)
x = np.linspace(1e-4, 1/6.0, 200); uu = 1/x
fit2 = sum(c[k]*bas(uu, 2, k) for k in c)*uu**6/20; fit3 = sum(c[k]*bas(uu, 3, k) for k in c)*uu**7/(-120)
fig, ax = plt.subplots(figsize=(3.4, 2.6))
ax.plot(1/u, R2, "o", ms=3, color="C0", label=r"$R_2$ from $\tilde\Gamma''$")
ax.plot(1/u, R3, "s", ms=3, color="C1", label=r"$R_3$ from $\tilde\Gamma'''$")
ax.plot(x, fit2, "-", color="C0", lw=0.8); ax.plot(x, fit3, "-", color="C1", lw=0.8)
ax.axhline(-51248/190575, color="C2", ls="--", lw=0.8, label=r"$-51248/190575$ (DeWitt)")
ax.axhline(-7916/148225, color="C3", ls=":", lw=0.8, label=r"$-7916/148225$ (lit.)")
ax.set_xlabel(r"$1/(m\rho)^2$"); ax.set_ylabel(r"$R_j\to c_8$")
ax.set_xlim(0, 0.17); ax.set_ylim(-0.30, 0.0)
ax.legend(fontsize=6, loc="upper left")
fig.tight_layout()
os.makedirs(os.path.join(HERE, "work", "inst_gy_hp"), exist_ok=True)
fig.savefig(os.path.join(HERE, "work", "inst_gy_hp", "c8_extrapolation.png"), dpi=200)
print("    figure R_j = (G_j - known terms) u^(j+4)/(...) -> c8: work/inst_gy_hp/c8_extrapolation.png; fit used for the curves (m>=3.5, c8..c14):",
      {f"c{2*k}": round(float(v), 5) for k, v in c.items()}, "chi2/dof", chi)
