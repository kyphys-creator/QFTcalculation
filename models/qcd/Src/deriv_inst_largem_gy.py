# %% [markdown]
# # Appendix check: the large-mass expansion against the Gel'fand-Yaglom determinant
#
# Research note models/qcd, derivations of the appendices (numpy).  app:inst 「大きい質量の展開。」 (N2c): the large-m expansion from the exact
# DeWitt-recursion coefficients A_3..A_8 (deriv_inst_dewitt_modp.py 8) against the Gel'fand-Yaglom values of results/inst_gy.csv (inst_gy.py),
# and against the literature m^-8 coefficient -7916/148225 used in inst_gy.py.
# Reads results/inst_gy.csv.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_largem_gy.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_largem_gy.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import csv
import os
import sys
import numpy as np
from fractions import Fraction as F
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules

# %% [markdown]
# ## The coefficients of the large-m expansion

# %%
A = {3: F(1, 75), 4: F(17, 735), 5: F(-116, 2835), 6: F(25624, 571725), 7: F(-3267232, 96621525), 8: F(132784, 131756625)}
gam = {3: 1, 4: 1, 5: 2, 6: 6, 7: 24, 8: 120}
coef = {k: -gam[k]*A[k] for k in A}            # coefficient of m^{-2(k-2)}
print("large-m coefficients -Gamma(k-2) A_k of m^-(2k-4):", {2*k - 4: str(c) for k, c in coef.items()})
def series(m, kmax, lit=False):
    s = -np.log(m)/6
    for k in range(3, kmax + 1):
        c = coef[k]
        if lit and k == 6: c = F(-7916, 148225)
        s += float(c)/m**(2*k - 4)
    return s
series(3.0, 6, lit=True), series(3.0, 6), series(3.0, 8)          # inspect: the series at m rho = 3 (literature A_6; DeWitt A_6; to m^-12)

# %% [markdown]
# ## Against the Gel'fand-Yaglom values of results/inst_gy.csv

# %%
rows = list(csv.DictReader(open(os.path.join(HERE, 'results', 'inst_gy.csv'))))
print(" m    Gamma~(GY)      L-dep    | GY - series to m^-8: lit. A_6 | DeWitt A_6 | DeWitt to m^-10 | to m^-12")
for r in rows:
    m = float(r['m_rho'])
    if m < 2: continue
    G = float(r['Gamma_tilde']); Ld = float(r['L_dependence'])
    print(f"{m:4.1f}  {G:.10f}  {Ld:.1e}  | {G - series(m, 6, lit=True):+.2e} | {G - series(m, 6):+.2e} | {G - series(m, 7):+.2e} | {G - series(m, 8):+.2e}")
rows[:2]          # inspect: the first rows of results/inst_gy.csv
