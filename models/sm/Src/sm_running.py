"""The note's running of the SM couplings (research note models/sm, steps (8) and (10)).

rhs_note(state, order): d/d ln mu of (g1^2, g2^2, g3^2, yt^2, yb^2, ytau^2, lambda, m^2) with the note's own beta functions
(order 1: Eq. (beta); order 2: plus the two-loop gaugeless terms of beta_yt, beta_gS, beta_lambda computed from the note's
model, results/twoloop_sym_beta.csv and twoloop_lambda_beta.csv).  run(state0, mu0, mu1, rge) with rge = ("note", 1 or 2)
or ("lit", 2 or 3) (sm_rge.py, Buttazzo et al., for comparison only).  starts: the starting points of step (8).
"""
import csv
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import sm_rge

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
K = sm_rge.K
MPL = 1.2209e19

# %% [markdown]
# ## The note's two-loop gaugeless terms, read from the Mathematica results

# %%
yt_s, gS_s, la_s = sp.symbols("yt gS la")


def read_expr(path, key):
    for row in csv.reader(open(path)):
        if row and row[0] == key:
            return sp.sympify(row[1].replace("^", "**"), locals={"yt": yt_s, "gS": gS_s, "la": la_s})
    raise KeyError(key)


b2y = read_expr(RES / "twoloop_sym_beta.csv", "K2_beta_yt_two_loop")
b2g = read_expr(RES / "twoloop_sym_beta.csv", "K2_beta_gS_two_loop")
b2l = read_expr(RES / "twoloop_lambda_beta.csv", "K2_beta_la_two_loop")
f2y, f2g, f2l = (sp.lambdify((yt_s, gS_s, la_s), e, "math") for e in (b2y, b2g, b2l))


def rhs_note(state, order):
    """d/d ln mu of (g1^2, g2^2, g3^2, yt^2, yb^2, ytau^2, lambda, m^2): order 1 = Eq. (beta); order 2 = Eq. (beta) + the
    note's two-loop gaugeless terms of yt, gS, lambda"""
    out = sm_rge.rhs(state, 1)
    if order >= 2:
        yt, gS, la = math.sqrt(state[3]), math.sqrt(state[2]), state[6]
        out[3] += 2 * yt * f2y(yt, gS, la) / K ** 2      # d yt^2 / d ln mu = 2 yt beta_yt
        out[2] += 2 * gS * f2g(yt, gS, la) / K ** 2
        out[6] += f2l(yt, gS, la) / K ** 2
    return out


def state0(gY, g2, g3, yt, yb, ytau, lam, m):
    return [5 / 3 * gY ** 2, g2 ** 2, g3 ** 2, yt ** 2, yb ** 2, ytau ** 2, lam, m ** 2]


def run(s0, mu0, mu1, rge):
    kind, order = rge
    f = (lambda t, y: rhs_note(y, order)) if kind == "note" else (lambda t, y: sm_rge.rhs(y, order))
    return solve_ivp(f, (math.log(mu0), math.log(mu1)), s0, method="DOP853", rtol=1e-11, atol=1e-14, dense_output=True)


def at(sol, mu):
    y = sol.sol(math.log(mu))
    return {"g1": math.sqrt(y[0]), "g2": math.sqrt(y[1]), "g3": math.sqrt(y[2]), "yt": math.sqrt(y[3]), "lam": y[6],
            "m": math.sqrt(y[7])}


def lambda_zero(sol):
    ts = np.linspace(sol.t[0], sol.t[-1], 4000)
    ls = sol.sol(ts)[6]
    i = np.nonzero(np.sign(ls[:-1]) != np.sign(ls[1:]))[0]
    if len(i) == 0:
        return float("nan")
    return math.exp(brentq(lambda t: sol.sol(t)[6], ts[i[0]], ts[i[0] + 1], xtol=1e-12))


RGES = [("note", 1), ("note", 2), ("lit", 2), ("lit", 3)]
LABEL = {("note", 1): "note 1-loop", ("note", 2): "note 1-loop + 2-loop gaugeless", ("lit", 2): "literature 2-loop",
         ("lit", 3): "literature 3-loop"}

# %% [markdown]
# ## Starting points

# %%
fit = {r[0]: r for r in csv.reader(open(RES / "msbar_fit.csv"))}
lamP, yt1P, yt3P, g2P, gYP, mP, vP, g3P = (float(x) for x in fit["PDG2024_MW_scheme"][1:9])
ybMR, ytauMR = 0.015480097, 0.0099944422
ybB, ytauB = ybMR * 4.2 / 4.18, ytauMR * 1.777 / 1.77686
rB = [float(x) for x in fit["Buttazzo_inputs_g3_1.1666"][1:9]]
rM = [float(x) for x in fit["MartinRobertson_inputs_alpha_scheme"][1:9]]
starts = {"A_Buttazzo_NNLO": (state0(0.35830, 0.64779, 1.1666, 0.93690, ybB, ytauB, 0.12604, 131.55), 173.34),
          "A_note_at_Buttazzo_inputs_yt_QCD3": (state0(rB[4], rB[3], rB[7], rB[2], ybB, ytauB, rB[0], rB[5]), 173.34),
          "C_Martin_Robertson": (state0(0.35853877, 0.64765961, 1.1636241, 0.93480082, ybMR, ytauMR, 0.12603842,
                                        math.sqrt(2) * 92.878850), 173.1),
          "C_note_at_MR_inputs_yt_QCD3": (state0(rM[4], rM[3], rM[7], rM[2], ybMR, ytauMR, rM[0], rM[5]), 173.1),
          "B_note_PDG_yt_QCD3": (state0(gYP, g2P, g3P, yt3P, ybMR, ytauMR, lamP, mP), 172.57),
          "B_note_PDG_yt_one_loop": (state0(gYP, g2P, g3P, yt1P, ybMR, ytauMR, lamP, mP), 172.57)}
