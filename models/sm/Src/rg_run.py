# %% [markdown]
# # Step (8): running of the SM couplings, the zero of lambda, and FJ versus beta_t masses (SM note)
#
# The RGEs of sm_rge.py (one- and two-loop parts checked against the general formulas in rg_twoloop.py; three-loop
# parts and the four-loop QCD term of g3 transcribed from Buttazzo et al., appendix B) are integrated from mu0 ~ M_t
# to M_Pl = 1.2209e19 GeV.
#   (A) start: Buttazzo et al. NNLO values at mu = M_t = 173.34 GeV (their Eqs. (55)-(60)); at three loops their
#       values at M_Pl (their Eq. (sys:Pl)) must be reproduced; the one- and two-loop runs show the order dependence;
#   (B) start: the one-loop matching of step (7) (PDG 2024, M_W scheme, mu = M_t = 172.57 GeV), with y_t at one loop
#       and with the pure QCD corrections to three loops;
#   (C) start: the Martin-Robertson reference point (mu = 173.1 GeV).
# lambda(mu) = 0 at mu = Lambda_lambda.  FJ versus beta_t: in FJ, v^2 = mu^2/lambda = m^2/(2 lambda) and M_W = g v/2;
# in the beta_t scheme (Landau gauge) v_beta = v + T/M_H^2 (note Eq. (T) at xi = 0) runs with -gamma_Phi^L (one loop,
# Eq. (vbeta)).  Output: results/rg_run.csv, ../ResearchNote/fig_rg.pdf.  Batch: python3 rg_run.py

# %%
import csv
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import sm_rge

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
NOTE = HERE.parent / "ResearchNote"
K = sm_rge.K
MPL = 1.2209e19


def state0(gY, g2, g3, yt, yb, ytau, lam, m):
    return [5 / 3 * gY ** 2, g2 ** 2, g3 ** 2, yt ** 2, yb ** 2, ytau ** 2, lam, m ** 2]


def run(s0, mu0, mu1, order):
    return solve_ivp(lambda t, y: sm_rge.rhs(y, order), (math.log(mu0), math.log(mu1)), s0, method="DOP853",
                     rtol=1e-11, atol=1e-14, dense_output=True)


def at(sol, mu):
    y = sol.sol(math.log(mu))
    return {"g1": math.sqrt(y[0]), "g2": math.sqrt(y[1]), "g3": math.sqrt(y[2]), "yt": math.sqrt(y[3]),
            "lam": y[6], "m": math.sqrt(y[7])}


def lambda_zero(sol):
    ts = np.linspace(sol.t[0], sol.t[-1], 4000)
    ls = sol.sol(ts)[6]
    i = np.nonzero(np.sign(ls[:-1]) != np.sign(ls[1:]))[0]
    if len(i) == 0:
        return float("nan")
    t0 = brentq(lambda t: sol.sol(t)[6], ts[i[0]], ts[i[0] + 1], xtol=1e-12)
    return math.exp(t0)


rows = []

# %% [markdown]
# ## (A) Buttazzo et al. starting values

# %%
# y_b, y_tau at M_t from m_b(m_b) = 4.2 GeV and M_tau = 1.777 GeV: Martin-Robertson's values scaled to these masses
ybB, ytauB = 0.015480097 * 4.2 / 4.18, 0.0099944422 * 1.777 / 1.77686
sA = state0(0.35830, 0.64779, 1.1666, 0.93690, ybB, ytauB, 0.12604, 131.55)
butPl = {"g1": 0.6154, "g2": 0.5055, "g3": 0.4873, "yt": 0.3825, "lam": -0.0143, "m": 129.4}
print("(A) Buttazzo et al. NNLO values at M_t = 173.34 GeV, run to M_Pl:")
solsA = {}
for order in (1, 2, 3):
    sol = run(sA, 173.34, MPL, order)
    solsA[order] = sol
    v = at(sol, MPL)
    z = lambda_zero(sol)
    print("    %d loops: g1 %.4f  g2 %.4f  g3 %.4f  yt %.4f  lambda %+.4f  m %.1f GeV;  Lambda_lambda = 10^%.2f GeV"
          % (order, v["g1"], v["g2"], v["g3"], v["yt"], v["lam"], v["m"], math.log10(z)))
    rows.append(["A_Buttazzo_start", order, v["g1"], v["g2"], v["g3"], v["yt"], v["lam"], v["m"], math.log10(z)])
print("    Buttazzo et al. (3 loops): g1 %.4f  g2 %.4f  g3 %.4f  yt %.4f  lambda %+.4f  m %.1f GeV;  "
      "Lambda_lambda ~ 2 Lambda_V = 10^%.1f GeV" % (butPl["g1"], butPl["g2"], butPl["g3"], butPl["yt"], butPl["lam"],
                                                    butPl["m"], 9.5 + math.log10(2)))
vA3 = at(solsA[3], MPL)
print("    3 loops - Buttazzo:", {k: round(float(vA3[k] - butPl[k]), 5) for k in butPl})
print("    (their m(M_Pl) = 129.4 GeV in Eq. (sys:Pl) disagrees with their own Fig. 2, where m rises to about 0.14 TeV;"
      " the 1- and 2-loop m^2 RGEs used here are checked against the general formulas)")

# %% [markdown]
# ## (B) step (7) values (PDG 2024), (C) Martin-Robertson

# %%
fit = {r[0]: r for r in csv.reader(open(RES / "msbar_fit.csv"))}
pw = fit["PDG2024_MW_scheme"]
lamP, yt1P, yt3P, g2P, gYP, mP, vP, g3P = (float(x) for x in pw[1:9])
ybMR, ytauMR = 0.015480097, 0.0099944422
rB = [float(x) for x in fit["Buttazzo_inputs_g3_1.1666"][1:9]]
rM = [float(x) for x in fit["MartinRobertson_inputs_alpha_scheme"][1:9]]
cases = {"ours_at_Buttazzo_inputs_QCD3": (state0(rB[4], rB[3], rB[7], rB[2], ybB, ytauB, rB[0], rB[5]), 173.34),
         "ours_at_MR_inputs_QCD3": (state0(rM[4], rM[3], rM[7], rM[2], ybMR, ytauMR, rM[0], rM[5]), 173.1),
         "B_ours_yt_one_loop": (state0(gYP, g2P, g3P, yt1P, ybMR, ytauMR, lamP, mP), 172.57),
         "B_ours_yt_QCD3": (state0(gYP, g2P, g3P, yt3P, ybMR, ytauMR, lamP, mP), 172.57),
         "C_Martin_Robertson": (state0(0.35853877, 0.64765961, 1.1636241, 0.93480082, ybMR, ytauMR, 0.12603842,
                                       math.sqrt(2) * 92.878850), 173.1)}
print("(B), (C):")
solsB = {}
for name, (s0, mu0) in cases.items():
    for order in (2, 3):
        sol = run(s0, mu0, MPL, order)
        solsB[(name, order)] = sol
        v = at(sol, MPL)
        z = lambda_zero(sol)
        print("    %-30s %d loops: yt(M_Pl) %.4f  lambda(M_Pl) %+.4f  m(M_Pl) %.1f GeV;  Lambda_lambda = 10^%.2f GeV"
              % (name, order, v["yt"], v["lam"], v["m"], math.log10(z)))
        rows.append([name, order, v["g1"], v["g2"], v["g3"], v["yt"], v["lam"], v["m"], math.log10(z)])
# sensitivity of lambda(M_Pl) to the starting values (3 loops, case B with QCD3)
base = at(solsB[("B_ours_yt_QCD3", 3)], MPL)["lam"]
s0 = cases["B_ours_yt_QCD3"][0]
for i, name, d in ((6, "lambda(M_t)", 0.001), (3, "y_t(M_t)", 0.001), (2, "g3(M_t)", 0.001)):
    s1 = list(s0)
    s1[i] = s0[i] + d if i == 6 else (math.sqrt(s0[i]) + d) ** 2
    print("    d lambda(M_Pl) / d %s = %+.3f" % (name, (at(run(s1, 172.57, MPL, 3), MPL)["lam"] - base) / d))

# %% [markdown]
# ## FJ versus beta_t masses (case B with QCD3, two-loop running)

# %%
sol = solsB[("B_ours_yt_QCD3", 2)]
zB = lambda_zero(sol)
mu0 = 172.57
y0 = sol.sol(math.log(mu0))
g1sq, g2sq, g3sq, t, b, tau, la, m2 = y0
vFJ = math.sqrt(m2 / (2 * la))
gpsq = 3 / 5 * g1sq
MW2, MZ2, MH2 = g2sq * vFJ ** 2 / 4, (g2sq + gpsq) * vFJ ** 2 / 4, m2
mt2, mb2, mtau2 = t * vFJ ** 2 / 2, b * vFJ ** 2 / 2, tau * vFJ ** 2 / 2
a0 = lambda x: x * (1 - math.log(x / mu0 ** 2))
# note Eq. (T) in Landau gauge (Goldstone A0 terms vanish), MS-bar finite parts at mu0
T = (2 * MW2 * (3 * a0(MW2) - 2 * MW2) + MZ2 * (3 * a0(MZ2) - 2 * MZ2) + 1.5 * MH2 * a0(MH2)
     - 4 * (3 * mt2 * a0(mt2) + 3 * mb2 * a0(mb2) + mtau2 * a0(mtau2))) / (K * vFJ)
vb0 = vFJ + T / MH2
print("FJ v(M_t) = sqrt(m^2/(2 lambda)) = %.3f GeV (step (7): v_G (1 + DeltaHat/2) = %.3f GeV, a two-loop difference);  beta_t (Landau gauge) v_beta = v + T/M_H^2 = %.3f GeV  (Martin-Robertson, two loops: 246.601)"
      % (vFJ, vP, vb0))
mus = np.exp(np.linspace(math.log(mu0), math.log(min(0.999 * zB, 1e11)), 400))
ys = sol.sol(np.log(mus))
vfj = np.sqrt(ys[7] / (2 * ys[6]))
# v_beta: d ln v_beta / d ln mu = -gamma_Phi^L = -(T_y - 9/4 g^2 - 3/4 g'^2)/K
gam = lambda tt: (lambda y: (3 * y[3] + 3 * y[4] + y[5] - 9 / 4 * y[1] - 3 / 4 * 3 / 5 * y[0]) / K)(sol.sol(tt))
solv = solve_ivp(lambda tt, lv: [-gam(tt)], (math.log(mu0), math.log(mus[-1])), [math.log(vb0)], dense_output=True,
                 rtol=1e-11, atol=1e-13)
vb = np.exp(solv.sol(np.log(mus))[0])
MWfj, MWb = np.sqrt(ys[1]) * vfj / 2, np.sqrt(ys[1]) * vb / 2
for mu in (mu0, 1e3, 1e5, 1e7, 1e9):
    j = np.argmin(np.abs(mus - mu))
    print("    mu = %.3g GeV: M_W(FJ) = %.2f GeV, M_W(beta_t, Landau) = %.2f GeV, lambda = %+.4f"
          % (mus[j], MWfj[j], MWb[j], ys[6][j]))
print("    Lambda_lambda (two loops) = 10^%.2f GeV: v_FJ -> infinity there (v^2 = mu^2/lambda)" % math.log10(zB))

# %% [markdown]
# ## Figure and table

# %%
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use(str(NOTE / "physrev.mplstyle"))
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.6))
mm = np.exp(np.linspace(math.log(173.34), math.log(MPL), 600))
for order, lab in ((1, "Buttazzo NNLO start, 1-loop RGE"), (2, "Buttazzo NNLO start, 2-loop RGE"),
                   (3, "Buttazzo NNLO start, 3-loop RGE")):
    ax[0].plot(np.log10(mm), solsA[order].sol(np.log(mm))[6], label=lab)
mm2 = np.exp(np.linspace(math.log(172.57), math.log(MPL), 600))
for name, lab in (("B_ours_yt_one_loop", r"this note, PDG 2024, $y_t$ 1 loop"),
                  ("B_ours_yt_QCD3", r"this note, PDG 2024, $y_t$ with QCD$^3$")):
    ax[0].plot(np.log10(mm2), solsB[(name, 3)].sol(np.log(mm2))[6], label=lab)
ax[0].axhline(0, color="k", lw=0.4)
ax[0].set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
ax[0].set_ylabel(r"$\lambda(\mu)$")
ax[0].legend(fontsize=5.5, frameon=False)
ax[1].plot(np.log10(mus), MWfj, label=r"FJ: $gv/2$, $v^2=\mu^2/\lambda$")
ax[1].plot(np.log10(mus), MWb, label=r"$\beta_t$ (Landau): $gv_\beta/2$")
ax[1].set_ylim(40, 200)
ax[1].set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
ax[1].set_ylabel(r"$\overline{\mathrm{MS}}$ $M_W(\mu)$ [GeV]")
ax[1].legend(fontsize=6, frameon=False)
fig.tight_layout()
fig.savefig(NOTE / "fig_rg.pdf")
with open(RES / "rg_run.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["case", "loops", "g1_MPl", "g2_MPl", "g3_MPl", "yt_MPl", "lambda_MPl", "m_MPl_GeV",
                "log10_Lambda_lambda_GeV"])
    for r in rows:
        w.writerow([r[0], r[1]] + ["%.6g" % x for x in r[2:]])
    w.writerow(["FJ_v_Mt_GeV", "", "%.6g" % vFJ])
    w.writerow(["betat_Landau_v_Mt_GeV", "", "%.6g" % vb0])
print("wrote results/rg_run.csv and ResearchNote/fig_rg.pdf")
