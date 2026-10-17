# %% [markdown]
# # Step (8): running of the SM couplings with the note's own beta functions, the zero of lambda, FJ versus beta_t masses
#
# The RGEs used here are the note's own:
#   one loop: Eq. (beta) of the note for all couplings (checked in step (4) against the two-point poles of the model and the
#             general formulas with the explicit field content);
#   two loops: the gaugeless terms of beta_yt, beta_gS, beta_lambda computed from the note's FeynArts model in the symmetric
#             phase (twoloop_sym_eval.wl, twoloop_lambda_eval.wl; read from results/twoloop_sym_beta.csv and
#             results/twoloop_lambda_beta.csv).  The electroweak two-loop terms (those with g, g') are not computed.
# The literature RGEs (sm_rge.py: Buttazzo et al., appendix B, full two and three loops) are used only for comparison: the
# difference shows the size of what the note does not compute.
#   (A) start: Buttazzo et al. NNLO values at mu = M_t = 173.34 GeV, and the note's one-loop matching of their inputs (step (7));
#   (B) start: step (7) (PDG 2024, M_W scheme, mu = M_t = 172.57 GeV), y_t at one loop and with the pure QCD corrections to
#   three loops (with the sensitivity of lambda(M_Pl) to the starting values);  (C) start: Martin-Robertson (173.1 GeV), and the
#   note's one-loop matching of their inputs.
# lambda(mu) = 0 at mu = Lambda_lambda.  FJ versus beta_t: FJ v^2 = mu^2/lambda = m^2/(2 lambda), M_W = g v/2; beta_t (Landau
# gauge) v_beta = v + T/M_H^2 (note Eq. (T) at xi = 0), run with -gamma_Phi^L (one loop, Eq. (vbeta)).
# The running itself is in sm_running.py (shared with vacuum_decay.py, step (10)).
# Output: results/rg_run.csv, ../ResearchNote/fig_rg.pdf.  Batch: python3 rg_run.py

# %%
import csv
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from sm_running import K, LABEL, MPL, RES, RGES, at, b2g, b2l, b2y, lambda_zero, run, starts, vP

HERE = Path(__file__).resolve().parent
NOTE = HERE.parent / "ResearchNote"

print("note's two-loop (gaugeless) K^2 beta: yt:", b2y, "; gS:", b2g, "; la:", b2l)

rows, sols = [], {}
for name, (s0, mu0) in starts.items():
    print("start", name, "(mu0 = %.2f GeV):" % mu0)
    for rge in RGES:
        sol = run(s0, mu0, MPL, rge)
        sols[(name, rge)] = sol
        v = at(sol, MPL)
        z = lambda_zero(sol)
        print("    %-32s yt(M_Pl) %.4f  g3(M_Pl) %.4f  lambda(M_Pl) %+.4f;  Lambda_lambda = 10^%.2f GeV"
              % (LABEL[rge], v["yt"], v["g3"], v["lam"], math.log10(z)))
        rows.append([name, LABEL[rge], v["g1"], v["g2"], v["g3"], v["yt"], v["lam"], v["m"], math.log10(z)])
print("Buttazzo et al. (their three-loop running of the NNLO values): yt 0.3825, g3 0.4873, lambda -0.0143, "
      "Lambda_lambda ~ 2 Lambda_V = 10^9.8 GeV")
# sensitivity of lambda(M_Pl) to the starting values (start B with QCD3, the note's RGEs)
s0B, muB = starts["B_note_PDG_yt_QCD3"]
baseB = at(sols[("B_note_PDG_yt_QCD3", ("note", 2))], MPL)["lam"]
for i, name, d in ((6, "lambda(M_t)", 0.001), (3, "y_t(M_t)", 0.001), (2, "g3(M_t)", 0.001)):
    s1 = list(s0B)
    s1[i] = s0B[i] + d if i == 6 else (math.sqrt(s0B[i]) + d) ** 2
    print("    d lambda(M_Pl) / d %s = %+.3f" % (name, (at(run(s1, muB, MPL, ("note", 2)), MPL)["lam"] - baseB) / d))

# %% [markdown]
# ## FJ versus beta_t masses (start B with QCD3, the note's RGEs)

# %%
sol = sols[("B_note_PDG_yt_QCD3", ("note", 2))]
zB = lambda_zero(sol)
mu0 = 172.57
g1sq, g2sq, g3sq, t, b, tau, la, m2 = sol.sol(math.log(mu0))
vFJ = math.sqrt(m2 / (2 * la))
gpsq = 3 / 5 * g1sq
MW2, MZ2, MH2 = g2sq * vFJ ** 2 / 4, (g2sq + gpsq) * vFJ ** 2 / 4, m2
mt2, mb2, mtau2 = t * vFJ ** 2 / 2, b * vFJ ** 2 / 2, tau * vFJ ** 2 / 2
a0 = lambda x: x * (1 - math.log(x / mu0 ** 2))
T = (2 * MW2 * (3 * a0(MW2) - 2 * MW2) + MZ2 * (3 * a0(MZ2) - 2 * MZ2) + 1.5 * MH2 * a0(MH2)
     - 4 * (3 * mt2 * a0(mt2) + 3 * mb2 * a0(mb2) + mtau2 * a0(mtau2))) / (K * vFJ)
vb0 = vFJ + T / MH2
print("FJ v(M_t) = sqrt(m^2/(2 lambda)) = %.3f GeV (step (7): %.3f GeV);  beta_t (Landau) v_beta = %.3f GeV "
      "(Martin-Robertson, two loops: 246.601)" % (vFJ, vP, vb0))
mus = np.exp(np.linspace(math.log(mu0), math.log(min(0.999 * zB, 1e11)), 400))
ys = sol.sol(np.log(mus))
vfj = np.sqrt(ys[7] / (2 * ys[6]))
gam = lambda tt: (lambda y: (3 * y[3] + 3 * y[4] + y[5] - 9 / 4 * y[1] - 3 / 4 * 3 / 5 * y[0]) / K)(sol.sol(tt))
solv = solve_ivp(lambda tt, lv: [-gam(tt)], (math.log(mu0), math.log(mus[-1])), [math.log(vb0)], dense_output=True,
                 rtol=1e-11, atol=1e-13)
vb = np.exp(solv.sol(np.log(mus))[0])
MWfj, MWb = np.sqrt(ys[1]) * vfj / 2, np.sqrt(ys[1]) * vb / 2
for mu in (mu0, 1e3, 1e5, 1e7, 1e9):
    j = np.argmin(np.abs(mus - mu))
    print("    mu = %.3g GeV: M_W(FJ) = %.2f GeV, M_W(beta_t, Landau) = %.2f GeV, lambda = %+.4f"
          % (mus[j], MWfj[j], MWb[j], ys[6][j]))
print("    Lambda_lambda = 10^%.2f GeV: v_FJ -> infinity there" % math.log10(zB))

# %% [markdown]
# ## Figure and table

# %%
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.style.use(str(NOTE / "physrev.mplstyle"))
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.6))
mm = np.exp(np.linspace(math.log(172.57), math.log(MPL), 600))
for rge, lab, ls in ((("note", 1), "PDG 2024 start: note 1-loop", "-"),
                     (("note", 2), "PDG 2024 start: note 1-loop + 2-loop gaugeless", "-"),
                     (("lit", 3), "PDG 2024 start: literature 3-loop (reference)", "--")):
    ax[0].plot(np.log10(mm), sols[("B_note_PDG_yt_QCD3", rge)].sol(np.log(mm))[6], ls, label=lab)
mmA = np.exp(np.linspace(math.log(173.34), math.log(MPL), 600))
ax[0].plot(np.log10(mmA), sols[("A_Buttazzo_NNLO", ("note", 2))].sol(np.log(mmA))[6],
           label="Buttazzo NNLO start: note 1-loop + 2-loop gaugeless")
ax[0].plot(np.log10(mmA), sols[("A_Buttazzo_NNLO", ("lit", 3))].sol(np.log(mmA))[6], "--",
           label="Buttazzo NNLO start: literature 3-loop (reference)")
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
    w.writerow(["start", "rge", "g1_MPl", "g2_MPl", "g3_MPl", "yt_MPl", "lambda_MPl", "m_MPl_GeV", "log10_Lambda_lambda_GeV"])
    for r in rows:
        w.writerow(r[:2] + ["%.6g" % x for x in r[2:]])
    w.writerow(["FJ_v_Mt_GeV", "", "%.6g" % vFJ])
    w.writerow(["betat_Landau_v_Mt_GeV", "", "%.6g" % vb0])
print("wrote results/rg_run.csv and ResearchNote/fig_rg.pdf")
