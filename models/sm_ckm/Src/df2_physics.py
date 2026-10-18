# %% [markdown]
# # Step (8) of the CKM note: Delta m_d, Delta m_s and epsilon_K
#
# The box function S is that of this note's model (df2_ckm_check.wl, results/df2_ckm_check.csv: the GIM-subtracted
# zero-momentum boxes, gauge independent and identical to the Inami-Lim S_0), evaluated at the MS-bar masses
# m_t(m_t) = 162.5 GeV, m_c(m_c) = 1.2730 GeV and M_W = 80.3692 GeV.  The effective Hamiltonian follows from the
# normalization found there, K x (coefficient) = -(g^4/(2 M_W^2)) sum lambda_k lambda_l S(x_k, x_l), i.e.
#   H = (G_F^2 M_W^2/(16 pi^2)) sum_{k,l} lambda_k lambda_l eta_{kl} S(x_k, x_l) (qbar Q)_{V-A}(qbar Q)_{V-A},
# with the QCD factors eta and the hadronic matrix elements taken from the literature (inputs below, cited in the
# note; they are not computed here):
#   Delta m_q = (G_F^2/(6 pi^2)) M_W^2 m_Bq (f_Bq^2 Bhat_Bq) eta_B |V_tb V_tq^*|^2 S(x_t),
#   |eps_K| = kappa_eps (G_F^2 f_K^2 m_K M_W^2 Bhat_K)/(12 sqrt2 pi^2 Delta m_K)
#             x |Im[lambda_c^*2 eta_cc S(x_c) + lambda_t^*2 eta_tt S(x_t) + 2 lambda_c^* lambda_t^* eta_ct S(x_c, x_t)]|,
#   lambda_i = V_is^* V_id.
# The CKM matrix: the PDG 2024 standard parameters (V^phys), and for comparison the MS-bar V(M_Z) of step (6).
# Writes results/df2_physics.csv.  Run: python3 df2_physics.py

# %%
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"

S = {r[0]: float(r[1]) for r in list(csv.reader(open(RES / "df2_ckm_check.csv")))[1:]}
PDGMS = {r[0]: float(r[1]) for r in list(csv.reader(open(RES / "ckm_pdg_msbar.csv")))[1:]}


def ckm(s12, s23, s13, dl):
    c12, c23, c13 = (math.sqrt(1 - x**2) for x in (s12, s23, s13))
    e = np.exp(1j * dl)
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


# %% [markdown]
# ## Inputs (literature; GeV unless stated)

# %%
GF = 1.1663788e-5          # PDG 2024
MW = 80.3692               # PDG 2024
HBAR = 6.582119569e-25     # GeV s
INP = {
    # FLAG 2024 (arXiv:2411.04268), N_f = 2+1+1: f_B sqrt(Bhat_B) [GeV]; N_f = 2+1 Bhat_K, f_K
    "fBd_sqrtB": (0.2106, 0.0055), "fBs_sqrtB": (0.2561, 0.0057), "BK": (0.7533, 0.0091), "fK": (0.1557, 0.0007),
    # PDG 2024 masses
    "mBd": 5.27966, "mBs": 5.36692, "mK": 0.497611,
    # QCD factors: eta_B (Buras, Jamin, Weisz 1990), eta_tt (same), eta_ct (Brod, Gorbahn 2010), eta_cc (Brod,
    # Gorbahn 2012), kappa_eps (Buras, Guadagnoli, Isidori 2010)
    "etaB": (0.551, 0.007), "etatt": (0.5765, 0.0065), "etact": (0.496, 0.047), "etacc": (1.87, 0.76),
    "kappa": (0.94, 0.02),
}
EXP = {"dmd": (0.5069, 0.0021), "dms": (17.765, 0.006), "epsK": (2.228e-3, 0.011e-3), "dmK": 3.484e-15}  # PDG 2024
PDG = (0.22501, 0.04183, 0.003732, 1.147)
PDG_ERR = (0.00068, 0.00079, 0.000090, 0.026)


# %% [markdown]
# ## Predictions

# %%
def predictions(V):
    to_ps = 1e-12 / HBAR    # GeV -> ps^-1
    pref = GF**2 / (6 * math.pi**2) * MW**2
    dmd = pref * INP["mBd"] * INP["fBd_sqrtB"][0]**2 * INP["etaB"][0] * abs(V[2, 2] * np.conj(V[2, 0]))**2 * S["S_tt"] * to_ps
    dms = pref * INP["mBs"] * INP["fBs_sqrtB"][0]**2 * INP["etaB"][0] * abs(V[2, 2] * np.conj(V[2, 1]))**2 * S["S_tt"] * to_ps
    lam = [np.conj(V[i, 1]) * V[i, 0] for i in range(3)]          # lambda_i = V_is^* V_id
    lc, lt = np.conj(lam[1]), np.conj(lam[2])
    bracket = lc**2 * INP["etacc"][0] * S["S_cc"] + lt**2 * INP["etatt"][0] * S["S_tt"] + 2 * lc * lt * INP["etact"][0] * S["S_ct"]
    eps = INP["kappa"][0] * GF**2 * INP["fK"][0]**2 * INP["mK"] * MW**2 * INP["BK"][0] / (12 * math.sqrt(2) * math.pi**2 * EXP["dmK"]) \
        * abs(bracket.imag)
    parts = [INP["kappa"][0] * GF**2 * INP["fK"][0]**2 * INP["mK"] * MW**2 * INP["BK"][0] / (12 * math.sqrt(2) * math.pi**2 * EXP["dmK"])
             * abs(x.imag) for x in (lc**2 * INP["etacc"][0] * S["S_cc"], lt**2 * INP["etatt"][0] * S["S_tt"],
                                       2 * lc * lt * INP["etact"][0] * S["S_ct"])]
    return dmd, dms, eps, parts


Vphys = ckm(*PDG)
VMZ = ckm(PDGMS["s12_MZ"], PDGMS["s23_MZ"], PDGMS["s13_MZ"], PDGMS["delta_MZ"])
dmd, dms, eps, parts = predictions(Vphys)
dmd2, dms2, eps2, _ = predictions(VMZ)
# the main uncertainties: f_B sqrt(B) (2 x relative), |V_tq| from the PDG errors of s23, s13, delta (numerically), and
# for eps_K eta_cc, Bhat_K and |V_cb|^4
def spread(fun, k):
    p = list(PDG); p[k] += PDG_ERR[k]; up = fun(ckm(*p)); p[k] -= 2 * PDG_ERR[k]; dn = fun(ckm(*p))
    return abs(up - dn) / 2
dV = [math.sqrt(sum(spread(lambda V: predictions(V)[n], k)**2 for k in range(4))) for n in range(3)]
err_dmd = dmd * math.hypot(2 * INP["fBd_sqrtB"][1] / INP["fBd_sqrtB"][0], dV[0] / dmd)
err_dms = dms * math.hypot(2 * INP["fBs_sqrtB"][1] / INP["fBs_sqrtB"][0], dV[1] / dms)
err_eps = math.sqrt((parts[0] * INP["etacc"][1] / INP["etacc"][0])**2 + (eps * INP["BK"][1] / INP["BK"][0])**2 + dV[2]**2
                    + (parts[2] * INP["etact"][1] / INP["etact"][0])**2 + (eps * INP["kappa"][1] / INP["kappa"][0])**2)
print("S from this note's boxes: S(x_t) %.6f, S(x_c) %.4e, S(x_c, x_t) %.4e" % (S["S_tt"], S["S_cc"], S["S_ct"]))
print("Delta m_d = %.4f +- %.4f ps^-1   (exp %.4f +- %.4f)" % (dmd, err_dmd, *EXP["dmd"]))
print("Delta m_s = %.3f +- %.3f ps^-1   (exp %.3f +- %.3f)" % (dms, err_dms, *EXP["dms"]))
print("|eps_K|   = %.4e +- %.4e   (exp %.4e +- %.4e);  parts cc, tt, ct: %.3e, %.3e, %.3e" % (eps, err_eps, *EXP["epsK"], *parts))
print("Delta m_s / Delta m_d = %.3f (exp %.3f)" % (dms / dmd, EXP["dms"][0] / EXP["dmd"][0]))
print("with the MS-bar V(M_Z) of step (6) instead of V^phys: relative changes %.2e, %.2e, %.2e" %
      (dmd2 / dmd - 1, dms2 / dms - 1, eps2 / eps - 1))
rows = [("dmd_ps", dmd), ("dmd_err", err_dmd), ("dms_ps", dms), ("dms_err", err_dms), ("epsK", eps), ("epsK_err", err_eps),
        ("epsK_cc", parts[0]), ("epsK_tt", parts[1]), ("epsK_ct", parts[2]),
        ("dmd_VMZ_rel", dmd2 / dmd - 1), ("dms_VMZ_rel", dms2 / dms - 1), ("epsK_VMZ_rel", eps2 / eps - 1)]
with open(RES / "df2_physics.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value"])
    for k, v in rows:
        w.writerow([k, repr(float(v))])
print("wrote results/df2_physics.csv")
