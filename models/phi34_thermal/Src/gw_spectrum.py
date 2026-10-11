# %% [markdown]
# # Step (3): gravitational waves from sound waves and turbulence at the benchmarks, and the LISA sensitivity
#
# Research note models/phi34_thermal, step (3).  Inputs: the benchmarks BP1-BP4 and the scan of step (2)
# (results/strong_pt.csv: alpha_theta, beta/H, T_n), with T_* = T_n and g* = 106.75.
#   kappa(alpha, v_w): Espinosa, Konstandin, No, Servant 2010, Eqs. (95)-(102); K = kappa alpha/(1 + alpha), U_f^2 = 3K/4
#   H R_* = (8 pi)^(1/3) max(v_w, c_s)/(beta/H)                                (Caprini et al. 2020, Eq. (6))
#   sound waves: h^2 dOmega/dln f = h^2 3 x 0.687 F_gw,0 K^2 (H R_*) Omega~ C(f/f_p) min(1, H R_*/U_f),
#     Omega~ = 1.2e-2, C(s) = s^3 (7/(4 + 3 s^2))^(7/2), f_p = 26 uHz (z_p/10)/(H R_*) (T_*/100 GeV)(g*/100)^(1/6)
#     (Hindmarsh, Huber, Rummukainen, Weir 2017, erratum Eq. (2); Caprini et al. 2020, Eqs. (20), (30)-(32))
#     compared with Caprini et al. 2020 Eqs. (29), (32) as printed and Caprini et al. 2016 Eqs. (13)-(15)
#   turbulence: Caprini et al. 2016, Eqs. (16)-(18), kappa_turb = 0.05 kappa_v
#   LISA: S_h of the Science Requirements Document (Eq. (3)), h^2 Omega_sens = 2 pi^2 f^3 S_h/(3 H100^2), SNR with
#     T = 9.46e7 s (Caprini et al. 2020, Eqs. (33), (34)); power-law sensitivity for SNR = 10 (Thrane and Romano 2013).
# Checks: the normalisation of C (0.687), F_gw,0 and the redshifted Hubble rate from entropy conservation, the peak-frequency
# coefficient 26 uHz = (z_p/2 pi) x 16.5 uHz, the continuity of the kappa fits, the tangent of the power-law sensitivity.
# Writes results/gw_spectrum.csv and ../figs/gw_spectrum.pdf.
# Batch: `~/miniforge3/envs/qft/bin/python gw_spectrum.py` (from Src/).
# Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one; a bare expression at the end of a
# cell shows its value, and figures are drawn inline.

# %%
import csv
import math
import os
import sys

import numpy as np
from scipy.integrate import quad

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is Src/
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import tptlib as tl

rows = list(csv.reader(open(os.path.join(HERE, "results", "strong_pt.csv"))))
ib = [k for k, r in enumerate(rows) if r and r[0] == "benchmark"][0]
keys = rows[ib][1:]
bench = [dict(name=r[0], **dict(zip(keys, map(float, r[1:])))) for r in rows[ib + 1:] if r and r[0].startswith("BP")]
scan = [dict(zip(keys, map(float, r))) for r in rows[1:ib - 1] if r and not math.isnan(float(r[4]))]
print(f"{len(bench)} benchmarks, {len(scan)} scan points")


# %% [markdown]
# ## Checks of the conversion factors

# %%
# (a) normalisation of the spectral shape: 0.687 = 1/int C(s) dln s
IC = quad(lambda s: tl.C_sw(s) / s, 0, np.inf)[0]
print(f"int C(s) dln s = {IC:.5f}, 1/int = {1 / IC:.5f} (0.687 in Caprini et al. 2020, Eq. (29))")

# (b) F_gw,0 = Omega_gamma,0 (g_s0/g_s*)^(4/3) (g*/g0), g_s0 = 3.91, g0 = 2, T_gamma,0 = 2.725 K, H0 = 67.8 km/s/Mpc
HBAR = 6.582119569e-25                             # GeV s
KB = 8.617333262e-14                               # GeV/K
HBARC = 1.97326980e-14                             # GeV cm
Tg0 = 2.725 * KB
rho_gamma = math.pi ** 2 / 15 * Tg0 ** 4                                        # GeV^4
rho_c_h2 = 3 * (tl.H100 * HBAR) ** 2 * tl.MPL ** 2 / (8 * math.pi)              # GeV^4 (h = 1)
Og_h2 = rho_gamma / rho_c_h2
F100 = Og_h2 / tl.H_LITTLE ** 2 * (3.91 / 100) ** (4 / 3) * (100 / 2)
print(f"Omega_gamma h^2 = {Og_h2:.5e} (rho_c/h^2 = {rho_c_h2 / HBARC ** 3:.5e} GeV/cm^3);  F_gw,0(g* = 100) = {F100:.4e} "
      f"vs 3.57e-5 (rel. {F100 / 3.57e-5 - 1:+.1e})")

# (c) Hubble rate at T_* = 100 GeV, g* = 100 redshifted by entropy conservation, a_*/a_0 = (g_s0/g_s*)^(1/3) T_0/T_*
hst = 1.66 * math.sqrt(100) * 100 ** 2 / tl.MPL * (3.91 / 100) ** (1 / 3) * Tg0 / 100 / HBAR
Z_P_coef = tl.Z_P / (2 * math.pi) * hst * 1e6
print(f"h_* = {hst * 1e6:.3f} uHz vs 16.5 uHz (rel. {hst / 16.5e-6 - 1:+.1e});  (z_p/2 pi) h_* = {Z_P_coef:.2f} uHz "
      f"vs 26 uHz (rel. {Z_P_coef / 26 - 1:+.1e})")

# (d) the kappa fits are continuous at c_s and at the Jouguet velocity, and reach kappa_D at v_w = 1
for a in (1e-3, 0.01, 0.0714, 0.3):
    xJ = tl.v_jouguet(a)
    e = 1e-9
    print(f"alpha = {a}: v_J = {xJ:.5f};  kappa(c_s -/+) = {tl.kappa_v(a, tl.CS - e):.6e}/{tl.kappa_v(a, tl.CS + e):.6e};  "
          f"kappa(v_J -/+) = {tl.kappa_v(a, xJ - e):.6e}/{tl.kappa_v(a, xJ + e):.6e};  kappa(1) = {tl.kappa_v(a, 1.0):.6e} "
          f"vs kappa_D = {a / (0.73 + 0.083 * math.sqrt(a) + a):.6e}")


# %% [markdown]
# ## LISA: sensitivity and power-law sensitivity (SNR = 10)

# %%
F = tl.FGRID
S = tl.h2_sens(F)
P = tl.pls()
i, j = int(np.argmin(S)), int(np.argmin(P))
print(f"h^2 Omega_sens: min {S[i]:.3e} at f = {F[i] * 1e3:.3f} mHz;  power-law sensitivity (SNR = 10): min {P[j]:.3e} at "
      f"f = {F[j] * 1e3:.3f} mHz")
# a power law tangent to the curve has SNR = 10
b, fref = 2.0, 1e-3
om = 10 / math.sqrt(tl.T_OBS * np.trapezoid(((F / fref) ** b / S) ** 2 * F, np.log(F)))
print(f"tangent check: SNR of Omega_beta (f/f_ref)^beta (beta = {b}) = {tl.snr(lambda f: om * (f / fref) ** b):.6f}")


# %% [markdown]
# ## Benchmarks: spectra, peak amplitudes, SNR (v_w = 0.95 detonation, 0.44 deflagration)

# %%
out = []
for vw in (0.95, 0.44):
    for s in bench:
        g = tl.GWSource(s["alpha_theta"], s["betaH"], s["Tn"], vw)
        FW = np.geomspace(1e-5, 1e2, 7001)                # the turbulence peak can lie above the LISA band
        turb = g.h2_turb(FW)
        k = int(np.argmax(turb))
        r = dict(name=s["name"], vw=vw, alpha=s["alpha_theta"], betaH=s["betaH"], Tn=s["Tn"], vJ=tl.v_jouguet(s["alpha_theta"]),
                 kappa=g.kappa, K=g.K, Uf=g.Uf, HR=g.HR, Htsh=g.Htsh, fp=g.fp, sw_peak=g.h2_sw(g.fp),
                 sw_c20_peak=g.h2_sw_c20(g.fp), sw_c16_peak=g.h2_sw_c16(g.fsw16), fturb_peak=FW[k], turb_peak=turb[k],
                 snr=tl.snr(g.h2_total), snr_sw=tl.snr(g.h2_sw))
        out.append(r)
        print(f"{r['name']} v_w = {vw}: kappa = {r['kappa']:.4f}, K = {r['K']:.3e}, U_f = {r['Uf']:.4f}, H R_* = {r['HR']:.3e}, "
              f"H tau_sh = {r['Htsh']:.3e}, f_p = {r['fp'] * 1e3:.3f} mHz;  peak h^2 Omega_sw = {r['sw_peak']:.3e} "
              f"(C20 {r['sw_c20_peak']:.3e}, C16 {r['sw_c16_peak']:.3e});  turbulence {r['turb_peak']:.3e} at "
              f"{r['fturb_peak'] * 1e3:.2f} mHz;  SNR = {r['snr']:.3e} (sound waves {r['snr_sw']:.3e})")


# %% [markdown]
# ## The scan of step (2): the largest SNR (v_w = 0.95)

# %%
best = None
for s in scan:
    g = tl.GWSource(s["alpha_theta"], s["betaH"], s["Tn"], 0.95)
    q = tl.snr(g.h2_total)
    if best is None or q > best[0]:
        best = (q, s)
q, s = best
print(f"largest SNR in the scan: {q:.3e} at lambda_T = {s['lam']:.4f}, E = {s['E']:.5f}, alpha_theta = {s['alpha_theta']:.4f}, "
      f"beta/H = {s['betaH']:.1f}, phi_n/T_n = {s['phin_Tn']:.3f}")

# what SNR = 10 would need, keeping two of (alpha_theta, beta/H, T_n) of BP4 (v_w = 0.95)
from scipy.optimize import brentq
b4 = bench[-1]
need_b = brentq(lambda x: math.log(tl.snr(tl.GWSource(b4["alpha_theta"], x, b4["Tn"], 0.95).h2_total) / 10), 1, b4["betaH"])
need_a = brentq(lambda x: math.log(tl.snr(tl.GWSource(x, b4["betaH"], b4["Tn"], 0.95).h2_total) / 10), b4["alpha_theta"], 10)
print(f"SNR = 10 needs beta/H = {need_b:.1f} at the alpha_theta of BP4, or alpha_theta = {need_a:.3f} at its beta/H")


# %% [markdown]
# ## Output and figure

# %%
cols = list(out[0].keys())
with open(os.path.join(HERE, "results", "gw_spectrum.csv"), "w", newline="") as fh:
    wr = csv.writer(fh)
    wr.writerow(cols)
    for r in out:
        wr.writerow([r[c] for c in cols])
    wr.writerow([])
    wr.writerow(["check", "value", "reference"])
    wr.writerows([["int_C_dlns_inverse", 1 / IC, 0.687], ["F_gw0_g100", F100, 3.57e-5], ["hstar_uHz", hst * 1e6, 16.5],
                  ["fp_coefficient_uHz", Z_P_coef, 26], ["sens_min", S[i], F[i]], ["pls_min", P[j], F[j]],
                  ["scan_max_snr", q, s["lam"]], ["betaH_for_snr10_BP4", need_b, ""], ["alpha_for_snr10_BP4", need_a, ""]])

import matplotlib
if not INTERACTIVE:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use(os.path.join(HERE, "..", "ResearchNote", "physrev.mplstyle"))
fig, ax = plt.subplots(figsize=(3.25, 2.6))
ax.plot(F, S, color="0.55", ls="-", lw=0.9)
ax.plot(F, P, color="0.55", ls="--", lw=0.9)
ax.text(2.5e-3, 2e-10, "LISA sensitivity", ha="center", va="bottom", fontsize=6, color="0.4")
ax.text(1.5e-3, 3e-14, "PLS (SNR = 10)", ha="right", va="top", fontsize=6, color="0.4")
for s, col in zip(bench, ("#5d81b4", "#e09b24", "#8eb031", "#eb6235")):
    g = tl.GWSource(s["alpha_theta"], s["betaH"], s["Tn"], 0.95)
    ax.plot(F, g.h2_total(F), color=col, ls="-", lw=1.0, label=s["name"])
    if s["name"] == "BP4":
        ax.plot(F, g.h2_turb(F), color=col, ls=":", lw=0.9, label="BP4 turbulence")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1e-5, 1)
ax.set_ylim(1e-24, 1e-2)
ax.set_xlabel(r"$f$ [Hz]")
ax.set_ylabel(r"$h^2\Omega_{\mathrm{gw}}(f)$")
ax.legend(loc="upper center", fontsize=6, ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "..", "figs", "gw_spectrum.pdf"))
print("wrote results/gw_spectrum.csv and figs/gw_spectrum.pdf")
