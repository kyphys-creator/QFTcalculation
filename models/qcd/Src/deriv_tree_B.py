# %% [markdown]
# # Appendix check: colour-split spin sums of g g -> Q Qbar with explicit spinors and polarizations
#
# Research note models/qcd, derivations of the appendices (numpy), with the definitions of tree_sigma.py (its code above the section
# "1. Spin/colour sums against the closed forms" is executed; ampB_lorentz uses the Feynman-rule three-gluon vertex, general gauge).
#   app:tree 「(B) の色で分けたスピンの和。」「偏極の和とゴースト。」 and app:ir 「(B) の色の相関。」 (T2):
#   S_kl(phys) = sum over spins and the two transverse polarizations of A_k A_l^* (A_1 = A_t + A_s, A_2 = A_u - A_s) against
#   8 g^4 F [[tau2/tau1, 1], [1, tau1/tau2]]; the -g sums with the Feynman-rule vertex exceed it by 4 g^4 tau1 tau2 [[1,-1],[-1,1]]; the
#   Eq. (Mtree) form (eps.p terms dropped) with -g sums equals S_kl(phys); the five basic -g sums of the text.  Printed: the largest
#   relative deviation over sqrt(s) = 2.3, 3, 5, 10 and five angles.
# Reads tree_sigma.py.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_tree_B.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_tree_B.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import itertools
import os
import sys
import numpy as np
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules

# %% [markdown]
# ## The definitions of tree_sigma.py

# %%
src_path = os.path.join(HERE, "tree_sigma.py")
src = open(src_path).read()
ns = {"__name__": "tree_sigma_defs"}
exec(compile(src[:src.index("# ## 1. Spin/colour sums against the closed forms")], src_path, "exec"), ns)
kin22, ampB_lorentz, pols, u_spinors, v_spinors, bar, slash, dot, MT, GAM, METRIC = (ns[k] for k in (
    "kin22", "ampB_lorentz", "pols", "u_spinors", "v_spinors", "bar", "slash", "dot", "MT", "GAM", "METRIC"))
one = np.eye(4)

kin22(3.0, 0.0, MT, 0.3)          # inspect: s, p1, p2, k1, k2 at sqrt(s) = 3, cos theta = 0.3 (m = 1)

# %% [markdown]
# ## The three brackets of Eq. (Mtree)

# %%
def reduced(p1, p2, k1, k2, e1, e2, ut, vt):
    """the three brackets of Eq. (Mtree) (Gamma_t/(t-m^2), Gamma_u/(u-m^2), Gamma_s/s) sandwiched"""
    s, t, u = dot(p1 + p2, p1 + p2), dot(p1 - k1, p1 - k1), dot(p1 - k2, p1 - k2)
    At = bar(ut) @ slash(e1) @ (slash(k1 - p1) + MT * one) @ slash(e2) @ vt / (t - MT ** 2)
    Au = bar(ut) @ slash(e2) @ (slash(k1 - p2) + MT * one) @ slash(e1) @ vt / (u - MT ** 2)
    Gs = dot(e1, e2) * (slash(p1) - slash(p2)) + 2 * dot(e1, p2) * slash(e2) - 2 * dot(e2, p1) * slash(e1)
    As = bar(ut) @ Gs @ vt / s
    return At, Au, As


# %% [markdown]
# ## Spin and polarization sums at 20 phase-space points

# %%
worst = {}
def upd(key, val):
    worst[key] = max(worst.get(key, 0.0), val)

for sq in (2.3, 3.0, 5.0, 10.0):
    for c in (-0.9, -0.3, 0.3, 0.7, 0.95):
        s, p1, p2, k1, k2 = kin22(sq, 0.0, MT, c)
        t, u = dot(p1 - k1, p1 - k1), dot(p1 - k2, p1 - k2)
        tau1, tau2, rho = (MT ** 2 - t) / s, (MT ** 2 - u) / s, 4 * MT ** 2 / s
        F = tau1 ** 2 + tau2 ** 2 + rho - rho ** 2 / (4 * tau1 * tau2)
        Sexp = 8 * F * np.array([[tau2 / tau1, 1], [1, tau1 / tau2]])
        G = 4 * tau1 * tau2 * np.array([[1, -1], [-1, 1]])
        phys = [(1.0, e) for e in pols(p1)], [(1.0, e) for e in pols(p2)]
        basis = [(-METRIC[l, l], np.eye(4)[l]) for l in range(4)]
        for mode, P1, P2 in (("phys", *phys), ("-g", basis, basis)):
            S_full = np.zeros((2, 2)); S_red = np.zeros((2, 2))
            sums = dict(ss=0.0, ts=0.0, us=0.0, tt=0.0, tu=0.0)
            for (w1, e1), (w2, e2) in itertools.product(P1, P2):
                for ut in u_spinors(k1, MT):
                    for vt in v_spinors(k2, MT):
                        At, Au, As = ampB_lorentz(p1, p2, k1, k2, e1, e2, ut, vt, 0.7)   # Feynman-rule vertex, xi = 0.7
                        A = np.array([-(At + As), -(Au - As)])                          # g = 1: A_k = -g^2 (...)
                        S_full += w1 * w2 * np.real(np.outer(A.conj(), A))
                        rt, ru, rs = reduced(p1, p2, k1, k2, e1, e2, ut, vt)
                        R = np.array([-(rt + rs), -(ru - rs)])
                        S_red += w1 * w2 * np.real(np.outer(R.conj(), R))
                        a_t, a_u, a_s = -rt, -ru, -rs
                        sums["ss"] += w1 * w2 * abs(a_s) ** 2
                        sums["ts"] += w1 * w2 * np.real(a_t * np.conj(a_s))
                        sums["us"] += w1 * w2 * np.real(a_u * np.conj(a_s))
                        sums["tt"] += w1 * w2 * abs(a_t) ** 2
                        sums["tu"] += w1 * w2 * np.real(a_t * np.conj(a_u))
            if mode == "phys":
                upd("S_kl(phys, Feynman-rule vertex) vs 8F matrix", np.max(np.abs(S_full / Sexp - 1)))
                upd("S_kl(phys, Eq. (Mtree) form) vs 8F matrix", np.max(np.abs(S_red / Sexp - 1)))
            else:
                upd("S_kl(-g, Eq. (Mtree) form) vs 8F matrix", np.max(np.abs(S_red / Sexp - 1)))
                upd("S_kl(-g, Feynman-rule vertex) - S_kl vs 4 tau1 tau2 (1,-1)x(1,-1)", np.max(np.abs(S_full - Sexp - G)) / np.max(np.abs(G)))
                exp = dict(ss=16 * tau1 * tau2, ts=-(8 * tau2 + 2 * rho * (tau1 - tau2) / tau1), us=8 * tau1 + 2 * rho * (tau2 - tau1) / tau2,
                           tt=8 * tau2 / tau1 + 4 * rho / tau1 - 2 * rho ** 2 / tau1 ** 2, tu=2 * rho * (1 - rho) / (tau1 * tau2))
                for k in exp:
                    upd(f"-g sum {k} vs snippet", abs(sums[k] / exp[k] - 1))
Sexp, S_full          # inspect: the last point (sqrt(s) = 10, cos theta = 0.95): the 8F matrix and the -g sum with the Feynman-rule vertex

# %% [markdown]
# ## The largest relative deviations

# %%
for k, v in worst.items():
    print(f"{k}: max relative deviation {v:.2e}")
