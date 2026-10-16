# %% [markdown]
# # Appendix check: the tr a_6 density of Kwon, Lee and Min on BPST against the correct one (the origin of -7916/148225)
#
# Research note models/qcd, derivations of the appendices (exact rational arithmetic).  app:inst 「大きい質量の展開。」 and the step (10)
# checks (「文献との食い違い。」): the literature m^-8 coefficient -7916/148225 (Dunne, Hur, Lee, Min, hep-th/0502087) comes from the a_6
# integral of Kwon, Lee and Min (KLM, hep-ph/0008028), who evaluated the FHSS formula on BPST (isospin 1/2, rho = 1).
# (a) the printed KLM densities and integrals and the printed large-mass series, read from the arXiv sources (downloaded into work/arxiv/
#     when missing; data only); normalization int a~_n d^4x = 16 pi^2 A_n checked on their a_5;
# (b) the correct density: the FHSS O_6 (as printed) on BPST, exact at 10 radii, = -(256/51975)[2876 - 86148 u + 338016 u^2 - 704340 u^3
#     + 141750 u^4]/(1+u)^12, A_6 = 25624/571725 (deriv_inst_fhss.py, DeWitt recursion);
# (c) KLM's printed numerator [2876, -86418, 404961, -765270, 397710] integrates to 193568/1334025 pi^2, not to their 63328/444675 pi^2;
#     with 86418 -> 86148 (a transposition typo) it gives exactly their value, and A_6 = 63328/(16*444675) = 3958/444675 gives
#     -Gamma(4) A_6 = -7916/148225: the literature coefficient comes from a density that differs from the correct one in the u^2, u^3, u^4
#     coefficients;
# (d) KLM's formula for D_l F_mn on BPST (their eq. delfmunu) is right (exact comparison at two points);
# (e) simple misreadings of the FHSS conventions (derivative order, index order, sign of i, partial instead of covariant derivatives,
#     one mis-indexed copy of the two-factor term) do not reproduce the KLM numerator.
# Reads the arXiv sources (work/arxiv/hep-ph_0008028/, hep-th_0502087/, hep-th_9707189/).  Writes nothing else; run_deriv_inst_a6_check.sh
# saves the printed output as results/deriv_inst_klm.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python -I deriv_inst_klm.py   (about 1.5 minutes)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import itertools
import math
import os
import re
import sys
from fractions import Fraction as Fr
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import deriv_inst_hk_lib as H
beta = H.beta

# %% [markdown]
# ## (a) What KLM and DHLM printed (read from the arXiv sources)

# %%
klm_tex = H.read_tex("hep-ph/0008028", "mass_instan.tex")
dhlm_tex = H.read_tex("hep-th/0502087", "massive7.tex")
m5 = re.search(r"\{(\d+) \((\d+) x\^2 \\rho\^8 - (\d+) \\rho\^\{10\}\)\\over (\d+)\(x\^2 \+ \\rho\^2\)\^\{10\}\}\s*"
               r"\\nonumber \\\\\s*&=&-\{(\d+)\\over(\d+)\} \{\\pi\^2\\over\\rho\^6\}", klm_tex)
p5, q5, r5, s5, n5, d5 = (int(x) for x in m5.groups())
I5 = Fr(p5, s5) * (Fr(-r5) * beta(2, 8) + Fr(q5) * beta(3, 7))
print(f"(a) KLM a~_5: int {p5}({q5} u - {r5})/({s5}(1+u)^10) d^4x = {I5} pi^2 (printed -{n5}/{d5} pi^2);  16 A_5 = {16 * Fr(-116, 2835)}")
i6 = klm_tex.index(r"\int d^4x\,\tilde{a}_6(x)")
blk = klm_tex[i6:klm_tex.index(r"\end{eqnarray}", i6)]
pre = re.search(r"&=&(-)\\int d\^4x\\, \{(\d+)\\over (\d+)\(\\rho\^2 \+x\^2\)\^\{12\}\}", blk)
bracket = re.search(r"\[(.*?)\]", blk, re.S).group(1)
cf = {int(p or 0)//2: int(s + n) for s, n, p, _ in re.findall(r"([+-]?)\s*(\d+)\s*(?:x\^(\d+))?\\rho\^\{?(\d+)\}?", bracket)}
KLM = [cf[j] for j in range(5)]
res6 = re.search(r"\{(\d+)\\over(\d+)\} \{\\pi\^2\\over\\rho\^\{8\}\}", blk)
KLM_I = Fr(int(res6.group(1)), int(res6.group(2)))
PRE = Fr(-int(pre.group(2)), int(pre.group(3)))
poly = "".join(f" {'-' if c < 0 else '+'} {abs(c)}" + (f" u^{j}" if j else "") for j, c in enumerate(KLM)).lstrip(" +")
print(f"    KLM a~_6 density as printed: ({PRE}) [{poly}]/(1+u)^12;  printed integral {KLM_I} pi^2")
ser_klm = re.search(r"label\{gammabarlargemass\}(.*?)\\end\{equation\}", klm_tex, re.S).group(1)
ser_klm = [(s, int(n), int(dd), int(k)) for s, n, dd, k in re.findall(r"([+-])\{(\d+)\\over(\d+)\}\{1\\over m\^(\d)\\rho\^\d\}", ser_klm)]
ser_dhlm = [(s, int(n), int(dd), int(k)) for s, n, dd, k in re.findall(r"([+-])\\frac\{(\d+)\}\{(\d+) m\^(\d)\}", dhlm_tex[dhlm_tex.index(r"-\frac{\ln m}{6}"):])][:4]
fmt = lambda L: ", ".join(f"m^-{k}: {s}{n}/{dd}" for s, n, dd, k in L)
print(f"    large-mass series, KLM eq. (gammabarlargemass): {fmt(ser_klm)}")
print(f"    large-mass series, DHLM (hep-th/0502087):        {fmt(ser_dhlm)}")
KLM          # inspect: KLM's printed numerator, coefficients of u^0..u^4

# %% [markdown]
# ## (b) The correct density: FHSS O_6 as printed, exactly on BPST (isospin 1/2)

# %%
O, _ = H.load_fhss()
terms = [t for t in O[6] if all(f[0] == "F" for f in t["factors"])]
radii = [Fr(0), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(4, 3), Fr(3, 2), Fr(2), Fr(5, 2), Fr(3)]

def run(name, ex, perm=lambda s: s, sel=lambda t: True, sign=lambda t: 1):
    vals = []
    for r in radii:
        s = Fr(0)
        for t in terms:
            if not sel(t):
                continue
            tt = dict(t)
            tt["factors"] = [[f[0], perm(f[1])] for f in t["factors"]]
            s += sign(t) * Fr(t["num"], t["den"]) * ex[r].value(tt)
        vals.append(s / 720)
    c, I = H.fit_integrate(radii, vals, 12)
    print(f"{name}: numerator {[str(x * Fr(51975, -256)) for x in c]}, A_6 = {I / 16} = {float(I / 16):.6f}", flush=True)
    return [x * Fr(51975, -256) for x in c]

ex = {r: H.ExactTerms(H.bpst_jets([r, 0, 0, 0], 4), "1/2") for r in radii}
print("(b) ", end="")
ours = run("FHSS as printed (F_klmn = D_k D_l F_mn)", ex)
ours          # inspect: the correct numerator in KLM's normalization

# %% [markdown]
# ## (c) KLM's integral: the printed numerator, the 86418 -> 86148 typo, and the literature coefficient

# %%
klmI = PRE * sum(Fr(c) * beta(j + 2, 10 - j) for j, c in enumerate(KLM))
klm_fix = list(KLM)
klm_fix[1] = -86148
klmIf = PRE * sum(Fr(c) * beta(j + 2, 10 - j) for j, c in enumerate(klm_fix))
oursI = PRE * sum(Fr(c) * beta(j + 2, 10 - j) for j, c in enumerate(ours))
print(f"(c) correct numerator {[str(x) for x in ours]}: integral/pi^2 = {oursI}, A_6 = {oursI / 16}")
print(f"    KLM eq. printed {KLM}: integral/pi^2 = {klmI} (KLM state {KLM_I}); with 86418 -> 86148: {klmIf}")
print(f"    KLM (typo fixed) minus correct: {[str(x - y) for x, y in zip(klm_fix, ours)]}")
A6klm = klmIf / 16
print(f"    KLM: A_6 = {klmIf}/16 = {A6klm}, -Gamma(4) A_6 = {-6 * A6klm} (literature m^-8 coefficient);"
      f"  correct: A_6 = {oursI / 16}, -Gamma(4) A_6 = {-6 * oursI / 16}")
klmIf == KLM_I, -6 * A6klm == Fr(-7916, 148225)          # inspect: the typo-fixed integral is KLM's value; it gives the literature coefficient

# %% [markdown]
# ## (d) KLM's D_l F_mn on BPST

# %%
# KLM eq. (delfmunu): D_l F_mn = (8/(1+x^2)^3)[2 eta_amn x_l - eta_alm x_n + eta_aln x_m + d_lm eta_ans x_s - d_ln eta_ams x_s]
for x0 in ([Fr(1, 2), 0, 0, 0], [Fr(1, 3), Fr(1, 2), Fr(-2, 3), Fr(1)]):
    J = H.bpst_jets(x0, 1)
    u = sum(v * v for v in x0)
    bad = 0
    for l in range(4):
        for m in range(4):
            for n in range(4):
                for a in range(3):
                    br = 2 * H.eta(a, m, n) * x0[l] - H.eta(a, l, m) * x0[n] + H.eta(a, l, n) * x0[m]
                    br += (l == m) * sum(H.eta(a, n, s) * x0[s] for s in range(4)) - (l == n) * sum(H.eta(a, m, s) * x0[s] for s in range(4))
                    bad += J[3][l, m, n, a] != Fr(8) / (1 + u) ** 3 * br
    print(f"(d) KLM D_l F_mn formula at x0 = {[str(v) for v in x0]}: {bad} of 192 components differ")

# %% [markdown]
# ## (e) Simple misreadings of the FHSS conventions

# %%
print("(e) KLM numerator (typo fixed): [2876, -86148, 404961, -765270, 397710]")
run("derivative order reversed (D_l D_k F_mn)", ex, perm=lambda s: s[:-2][::-1] + s[-2:])
run("field-strength indices first (D_m D_n F_kl)", ex, perm=lambda s: s[2:] + s[:2])
run("odd-number-of-factor terms with flipped sign (F -> -F, equivalently i -> -i)", ex, sign=lambda t: (-1) ** len(t["factors"]))
for k in range(2, 7):
    run(f"  contribution of the terms with {k} factors", ex, sel=lambda t, k=k: len(t["factors"]) == k)
for nc in [0, 1, 2, 3]:
    exn = {r: H.ExactTerms(H.bpst_jets([r, 0, 0, 0], 4, ncov=nc), "1/2") for r in radii}
    run(f"only the innermost {nc} derivative(s) covariant, outer ones partial", exn)
    exs = {r: H.ExactTerms(H.bpst_jets([r, 0, 0, 0], 4, ncov=nc, outer_sign=-1), "1/2") for r in radii}
    run(f"innermost {nc} derivative(s) correct, outer ones with the wrong-sign commutator", exs)
# single mis-indexed copy of the only two-factor term (D^4F D^4F): can it alone produce the KLM difference?
t2 = [t for t in terms if len(t["factors"]) == 2][0]
delta = [0, 0, 66945, -60930, 255960]  # KLM (typo fixed) minus correct, numerator units
assert delta == [x - y for x, y in zip(klm_fix, ours)]
a, b = t2["factors"][0][1], t2["factors"][1][1]
seen = {}
for pb in sorted(set(itertools.permutations(b))):          # sorted: a fixed order (the set order depends on the string hashes)
    bb = "".join(pb)
    tt = {"num": 1, "den": 1, "imag": t2["imag"], "factors": [["F", a], ["F", bb]]}
    v = [ex[r].value(tt) * Fr(t2["num"], t2["den"]) / 720 for r in radii]
    c, _ = H.fit_integrate(radii, v, 12)
    key = tuple(x * Fr(51975, -256) for x in c) + (0,) * (5 - len(c))
    seen[key] = bb
    if bb == b:
        ref = key          # the numerator of the term as printed (several index orders give the same numerator)
hits = [bb for k, bb in seen.items() if any(lam != 0 and all(lam * (x - y) == dl for x, y, dl in zip(k, ref, delta))
                                         for lam in ([Fr(delta[4]) / (k[4] - ref[4])] if k[4] != ref[4] else []))]
print(f"two-factor term {t2['factors']} (coefficient {t2['num']}/{t2['den']}): {len(seen)} distinct index orders of the 2nd factor;"
      f" orders reproducing the KLM difference: {hits}")
