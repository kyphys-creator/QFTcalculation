# %% [markdown]
# # Step (6) of the CKM note: from the PDG |V_ij| to the MS-bar V(M_Z) and V(M_t)
#
# The PDG values are taken as the |V_ij| of the low-energy semileptonic (four-fermion) couplings after the universal
# electroweak corrections (relative to muon decay) are removed.  Step (6) (sl_ckm_check.wl) gives, at zero momentum with
# massless light quarks,  V_ij^phys = V_ij(mu) (1 + Delta_ij(mu)),  Delta_ij = G(mu) c_ij  with
#   c_ib = |V_tb|^2,  c_id = -|V_td|^2,  c_is = |V_ts|^2 + 2 V_ib V_tb^* V_ts / V_is,
#   K G = (y_t^2/8) [-(5 x_t - 11)/(x_t - 1) + 6 x_t (x_t - 2) ln x_t/(x_t - 1)^2] - (3/4) y_t^2 ln(mu^2/M_W^2),
# x_t = M_T^2/M_W^2 (MS-bar), K = 16 pi^2.  This script
#   (a) evaluates G(M_Z) at the note's benchmark (the MS-bar masses at M_Z of Eq. (bench));
#   (b) solves for the standard parameters (s12, s23, s13, delta) of the MS-bar V(M_Z) from the PDG |V_us|, |V_cb|,
#       |V_ub| and the angle gamma (Im Delta = 0 for the four entries of gamma, so gamma is unchanged);
#   (c) runs V from M_Z to M_t with the one-loop matrix equations of the note (Eq. (betaY), the gauge couplings at one
#       loop) and compares with the fixed-order conversion at mu = M_t, G(M_t) = G(M_Z) - (3/(2K)) y_t^2 ln(M_t/M_Z).
# Writes results/ckm_pdg_msbar.csv.  Run: python3 ckm_pdg_msbar.py

# %%
import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
K = 16 * math.pi**2


def dag(m):
    return np.conj(m.T)


def ckm(s12, s23, s13, dl):
    c12, c23, c13 = (math.sqrt(1 - x**2) for x in (s12, s23, s13))
    e = np.exp(1j * dl)
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


def gamma_angle(V):
    return np.angle(-V[0, 0] * np.conj(V[0, 2]) / (V[1, 0] * np.conj(V[1, 2])))


def jarlskog(V):
    return np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]))


# %% [markdown]
# ## (a) G(M_Z) at the benchmark

# %%
ee, mw, mz, mt_ms = math.sqrt(4 * math.pi / 128), 80.0, 91.0, 165.0
sw = math.sqrt(1 - mw**2 / mz**2)
vev = 2 * mw * sw / ee
yt2 = 2 * mt_ms**2 / vev**2


def g_of_mu(mu, yt2=yt2, mt=mt_ms, mw=mw):
    xt = mt**2 / mw**2
    kg = yt2 / 8 * (-(5 * xt - 11) / (xt - 1) + 6 * xt * (xt - 2) * math.log(xt) / (xt - 1)**2) \
        - 0.75 * yt2 * math.log(mu**2 / mw**2)
    return kg / K


G_MZ = g_of_mu(mz)
print("(a) G(M_Z) = %.6e   (sl_ckm_check.wl: 2.302754e-3);  y_t^2 = %.6f, x_t = %.6f" % (G_MZ, yt2, mt_ms**2 / mw**2))


def deltas(V, G):
    d = np.zeros((3, 3), complex)
    for i in range(2):
        d[i, 2] = G * abs(V[2, 2])**2
        d[i, 0] = -G * abs(V[2, 0])**2
        d[i, 1] = G * (abs(V[2, 1])**2 + 2 * V[i, 2] * np.conj(V[2, 2]) * V[2, 1] / V[i, 1])
    return d


# %% [markdown]
# ## (b) PDG 2024 standard parameters -> MS-bar V(M_Z)

# %%
PDG = {"s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "delta": 1.147}
PDG_ERR = {"s12": 0.00068, "s23": 0.00079, "s13": 0.000090, "delta": 0.026}
Vphys = ckm(PDG["s12"], PDG["s23"], PDG["s13"], PDG["delta"])
D_MZ = deltas(Vphys, G_MZ)
target = np.array([abs(Vphys[0, 1]) / (1 + D_MZ[0, 1].real), abs(Vphys[1, 2]) / (1 + D_MZ[1, 2].real),
                   abs(Vphys[0, 2]) / (1 + D_MZ[0, 2].real),
                   gamma_angle(Vphys) - (D_MZ[0, 0] - D_MZ[0, 2] - D_MZ[1, 0] + D_MZ[1, 2]).imag])


def residual(p):
    V = ckm(*p)
    return np.array([abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2]), gamma_angle(V)]) - target


def newton(p0, f, steps=30):
    p = np.array(p0, float)
    for _ in range(steps):
        r = f(p)
        Jm = np.zeros((len(p), len(p)))
        for k in range(len(p)):
            dp = np.zeros(len(p)); dp[k] = 1e-7 * max(abs(p[k]), 1e-3)
            Jm[:, k] = (f(p + dp) - r) / dp[k]
        p = p - np.linalg.solve(Jm, r)
        if np.max(np.abs(r)) < 1e-15:
            break
    return p


pMZ = newton([PDG["s12"], PDG["s23"], PDG["s13"], PDG["delta"]], residual)
VMZ = ckm(*pMZ)
print("(b) imaginary parts of Delta in gamma (expect 0): %.1e" % abs((D_MZ[0, 0] - D_MZ[0, 2] - D_MZ[1, 0] + D_MZ[1, 2]).imag))
print("(b) MS-bar V(M_Z) from the PDG values: s12 %.6f, s23 %.6f, s13 %.7f, delta %.6f" % tuple(pMZ))
print("    relative change from PDG: s12 %.2e, s23 %.2e, s13 %.2e, delta %.2e;  J %.2e" % (
    pMZ[0] / PDG["s12"] - 1, pMZ[1] / PDG["s23"] - 1, pMZ[2] / PDG["s13"] - 1, pMZ[3] / PDG["delta"] - 1,
    jarlskog(VMZ) / jarlskog(Vphys) - 1))
print("    PDG errors (relative): s12 %.1e, s23 %.1e, s13 %.1e, delta %.1e" % tuple(PDG_ERR[k] / PDG[k] for k in PDG))
# the converse check: V(M_Z) (1 + Delta) reproduces |V^phys|
# (the u and c rows; the top row of V^phys is fixed by unitarity, not by a semileptonic decay)
back = np.abs(VMZ * (1 + deltas(VMZ, G_MZ)))[:2]
print("    |V(M_Z)(1 + Delta)| - |V^PDG|, u and c rows, max relative (expect ~G^2 ~ 5e-6 or less): %.1e" %
      np.max(np.abs(back - np.abs(Vphys)[:2]) / np.abs(Vphys)[:2]))
print("    top row: |V_td|, |V_ts|, |V_tb| of V(M_Z) relative to the PDG matrix: %.2e, %.2e, %.2e" %
      tuple(np.abs(VMZ[2]) / np.abs(Vphys[2]) - 1))

# %% [markdown]
# ## (c) running to M_t

# %%
MT_POLE = 172.57          # PDG 2024 (the scale mu = M_t)
gsB = math.sqrt(4 * math.pi * 0.118)
gB, gpB = ee / sw, ee / math.sqrt(1 - sw**2)
yu = math.sqrt(2) * np.array([0.00127, 0.619, 165.0]) / vev
yd = math.sqrt(2) * np.array([0.00271, 0.0546, 2.86]) / vev
ye = math.sqrt(2) * np.array([0.000487, 0.1027, 1.746]) / vev


def beta(state):
    Yu, Yd, Ye, gs, g, gp = state
    Hu, Hd, He = Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye)
    T = np.trace(3 * Hu + 3 * Hd + He).real
    I3 = np.eye(3)
    bu = (1.5 * (Hu - Hd) + (T - 8 * gs**2 - 9 / 4 * g**2 - 17 / 12 * gp**2) * I3) @ Yu
    bd = (1.5 * (Hd - Hu) + (T - 8 * gs**2 - 9 / 4 * g**2 - 5 / 12 * gp**2) * I3) @ Yd
    be = (1.5 * He + (T - 9 / 4 * g**2 - 15 / 4 * gp**2) * I3) @ Ye
    return [bu / K, bd / K, be / K, -7 * gs**3 / K, -19 / 6 * g**3 / K, 41 / 6 * gp**3 / K]


def rk4_run(state, t0, t1, n=2000):
    h = (t1 - t0) / n
    s = list(state)
    for _ in range(n):
        k1 = beta(s)
        k2 = beta([a + h / 2 * b for a, b in zip(s, k1)])
        k3 = beta([a + h / 2 * b for a, b in zip(s, k2)])
        k4 = beta([a + h * b for a, b in zip(s, k3)])
        s = [a + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(s, k1, k2, k3, k4)]
    return s


def ckm_from(Yu, Yd):
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    W = dag(Uu[:, ::-1]) @ Ud[:, ::-1]
    return W, su[::-1], sd[::-1]


def std_params(W):
    s13 = abs(W[0, 2]); c13 = math.sqrt(1 - s13**2)
    s12, s23 = abs(W[0, 1]) / c13, abs(W[1, 2]) / c13
    c12, c23 = math.sqrt(1 - s12**2), math.sqrt(1 - s23**2)
    J = jarlskog(W)
    return s12, s23, s13, math.asin(J / (c12 * c23 * c13**2 * s12 * s23 * s13)), J


rows = []
for label, V0 in (("PDG as MS-bar (benchmark)", Vphys), ("PDG converted (step 6)", VMZ)):
    s = rk4_run([np.diag(yu).astype(complex), V0 @ np.diag(yd), np.diag(ye).astype(complex), gsB, gB, gpB],
                math.log(mz), math.log(MT_POLE))
    W, su, sd = ckm_from(s[0], s[1])
    p = std_params(W)
    print("(c) %-26s V(M_t): s12 %.6f, s23 %.6f, s13 %.7f, delta %.6f, J %.5e;  y_t(M_t) %.5f" % (label, *p, su[2]))
    rows.append((label, p, su[2]))
# fixed order at mu = M_t: G(M_t) = G(M_Z) - (3/(2K)) y_t^2 ln(M_t/M_Z) with the running y_t at the midpoint
yt2_mid = (rows[1][2]**2 + yt2) / 2
G_MT = G_MZ - 1.5 * yt2_mid / K * math.log(MT_POLE / mz)
D_MT = deltas(Vphys, G_MT)
fo_cb = abs(Vphys[1, 2]) / (1 + D_MT[1, 2].real)
run_cb = rows[1][1][1] * math.sqrt(1 - rows[1][1][2]**2)
# the same running applied to V(M_Z) = V^PDG (benchmark): the CKM running alone
run_cb_bench = rows[0][1][1] * math.sqrt(1 - rows[0][1][2]**2)
print("(c) G(M_t) = %.5e;  |V_cb(M_t)|: fixed order %.7f, running %.7f (relative difference %.1e)" %
      (G_MT, fo_cb, run_cb, run_cb / fo_cb - 1))
print("    |V_cb(M_t)|/|V_cb^PDG| - 1: with the conversion %.3e, PDG taken as MS-bar at M_Z %.3e" %
      (run_cb / abs(Vphys[1, 2]) - 1, run_cb_bench / abs(Vphys[1, 2]) - 1))

out = [("G_MZ", G_MZ), ("G_Mt", G_MT)]
out += [("s12_MZ", pMZ[0]), ("s23_MZ", pMZ[1]), ("s13_MZ", pMZ[2]), ("delta_MZ", pMZ[3]), ("J_MZ", jarlskog(VMZ)),
        ("J_PDG", jarlskog(Vphys))]
for (label, p, ytm), tag in zip(rows, ("bench", "conv")):
    out += [("s12_Mt_" + tag, p[0]), ("s23_Mt_" + tag, p[1]), ("s13_Mt_" + tag, p[2]), ("delta_Mt_" + tag, p[3]),
            ("J_Mt_" + tag, p[4])]
out += [("Vcb_Mt_fixed_order", fo_cb), ("Vcb_Mt_running", run_cb)]
with open(RES / "ckm_pdg_msbar.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value"])
    for k, v in out:
        w.writerow([k, repr(float(v))])
print("wrote results/ckm_pdg_msbar.csv")
