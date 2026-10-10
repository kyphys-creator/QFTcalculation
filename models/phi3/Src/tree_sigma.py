# %% [markdown]
# # Step (2): tree-level sigma(phi phi -> phi phi) for comparison with MadGraph
#
# From Eq. (16) (eq:Mtree) of the research note:
# - M = -g^2 [1/(s-m^2) + 1/(t-m^2) + 1/(u-m^2)],   m = g = 1 (GeV units in MadGraph);
# - CM frame, equal masses: |p_f| = |p_i| = p,  p^2 = s/4 - m^2,  t = -2 p^2 (1 - cos th),  u = -2 p^2 (1 + cos th);
# - d sigma / d Omega = |M|^2 / (64 pi^2 s),  sigma = (1/2) * 2 pi * int_{-1}^{1} dc |M|^2 / (64 pi^2 s)
#   (the 1/2 is for the two identical final-state particles).
#
# Batch:  `python3 tree_sigma.py [mg5_log]`.  With an MG5 log (from tree_mg5.mg5), the "Cross-section" lines are
# compared in order with SQRTS below.  Interactive (VS Code, "Run Cell"): the log defaults to work/tree_mg5.log.

# %%
import math
import os
import re
import sys

from scipy.integrate import quad

INTERACTIVE = "ipykernel" in sys.modules
SQRTS = (2.5, 5.0, 10.0)        # must match the order of the launches in tree_mg5.mg5
GEV2_TO_PB = 0.3893794e9


def amplitude(s, c, m=1.0, g=1.0):
    p2 = s / 4 - m * m
    t = -2 * p2 * (1 - c)
    u = -2 * p2 * (1 + c)
    return -g * g * (1 / (s - m * m) + 1 / (t - m * m) + 1 / (u - m * m))


def sigma_pb(sqrts, m=1.0, g=1.0):
    s = sqrts ** 2
    integral, _ = quad(lambda c: amplitude(s, c, m, g) ** 2, -1, 1, epsabs=0, epsrel=1e-12)
    return 0.5 * 2 * math.pi * integral / (64 * math.pi ** 2 * s) * GEV2_TO_PB


# %% [markdown]
# ## The amplitude at the FeynCalc check point, and the MadGraph cross sections

# %%
print(f"M(sqrt(s)=5, cos=0.3) = {amplitude(25.0, 0.3):.12f}   (FeynCalc: 0.1463531980407785)")
logfile = sys.argv[1] if (len(sys.argv) > 1 and not INTERACTIVE) else ("work/tree_mg5.log" if INTERACTIVE else None)
mg5 = []
if logfile and os.path.exists(logfile):
    text = open(logfile).read()
    mg5 = [(float(a), float(b)) for a, b in re.findall(r"Cross-section :\s+([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb", text)]
mg5                                                          # inspect: (sigma, error) from MadGraph in pb

# %% [markdown]
# ## Comparison with the numerical integral of |M|^2

# %%
print(f"{'sqrt(s)':>8} {'analytic [pb]':>15} {'MadGraph [pb]':>24} {'(MG-an)/err':>12}")
for i, rs in enumerate(SQRTS):
    an = sigma_pb(rs)
    if i < len(mg5):
        x, e = mg5[i]
        print(f"{rs:8.2f} {an:15.6e} {x:13.5e} +- {e:8.2e} {(x - an) / e:12.2f}")
    else:
        print(f"{rs:8.2f} {an:15.6e}")
