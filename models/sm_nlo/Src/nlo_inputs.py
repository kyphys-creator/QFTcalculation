"""Inputs of the NLO note (models/sm_nlo): the MS-bar parameters at a scale mu and the pole masses.

Start at mu = M_t = 172.57 GeV, as the CKM note's step (10) (models/sm_ckm/Src/ckm_planck.py):
  g', g, g_s, lambda, v_FJ, y_t (pure QCD corrections to three loops): the SM note's step (7) (PDG 2024, M_W scheme;
  models/sm/Src/results/msbar_fit.csv); y_b, y_tau of Martin and Robertson at M_t (the SM note's step (8)); the light
  Yukawa couplings from the benchmark mass ratios of the CKM note (Eq. (bench)): y_q = y_b m_q/m_b, y_l = y_tau m_l/m_tau;
  V(M_t): the CKM note's step (6) conversion of the PDG standard parameters at mu = M_t (G(M_t) with x_t = 2 y_t^2/g^2 and
  M_W = g v_FJ/2).
Running: the CKM note's one-loop equations (Eq. (betaY) for the Yukawa matrices, the gauge couplings and lambda at one loop).
at(mu) returns the couplings, the singular values of the Yukawa matrices, V and the derived e, s^2 = g'^2/(g^2 + g'^2),
g_Z = sqrt(g^2 + g'^2) at mu.  POLE: the pole masses for the kinematics (PDG 2024; u, d, s massless).
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
CKMSRC = HERE.parent.parent / "sm_ckm" / "Src"
sys.path.insert(0, str(CKMSRC))
from rg2_ckm_general import K, SMSRC, dag, note_beta1  # noqa: E402

MT_START = 172.57
POLE = {"MZ": 91.1876, "MW": 80.3692, "MH": 125.20, "MT": 172.57, "MB": 4.78, "MC": 1.67, "MS": 0.0, "MD": 0.0, "MU": 0.0,
        "MTA": 1.77693, "MMU": 0.1056584, "Me": 0.000510999}
TOL = dict(method="DOP853", rtol=1e-12, atol=1e-15)

fit = {r[0]: r for r in csv.reader(open(SMSRC / "results" / "msbar_fit.csv"))}
LAM, YT1, YT3, G2, GY, MPOT, VFJ, G3 = (float(x) for x in fit["PDG2024_MW_scheme"][1:9])
YB, YTAU = 0.015480097, 0.0099944422
MQ = {"u": 0.00127, "c": 0.619, "d": 0.00271, "s": 0.0546, "b": 2.86}
ML = {"e": 0.000487, "mu": 0.1027, "tau": 1.746}


def ckm(s12, s23, s13, dl):
    c12, c23, c13 = (math.sqrt(1 - x**2) for x in (s12, s23, s13))
    e = np.exp(1j * dl)
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


def jarlskog(V):
    return np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]))


def gamma_angle(V):
    return np.angle(-V[0, 0] * np.conj(V[0, 2]) / (V[1, 0] * np.conj(V[1, 2])))


def std_params(V):
    a = np.abs(V)
    s13 = a[0, 2]
    c13 = math.sqrt(1 - s13**2)
    s12, s23 = a[0, 1] / c13, a[1, 2] / c13
    dl = math.asin(jarlskog(V) / (math.sqrt(1 - s12**2) * math.sqrt(1 - s23**2) * c13**2 * s12 * s23 * s13))
    return s12, s23, s13, dl


# the CKM note's step (6): V^phys = V(mu) (1 + Delta(mu))
def G_of(yt, g, mw, mu):
    xt = 2 * yt**2 / g**2
    kg = yt**2 / 8 * (-(5 * xt - 11) / (xt - 1) + 6 * xt * (xt - 2) * math.log(xt) / (xt - 1)**2) \
        - 0.75 * yt**2 * math.log(mu**2 / mw**2)
    return kg / K


def deltas(V, G):
    d = np.zeros((3, 3), complex)
    for i in range(2):
        d[i, 2] = G * abs(V[2, 2])**2
        d[i, 0] = -G * abs(V[2, 0])**2
        d[i, 1] = G * (abs(V[2, 1])**2 + 2 * V[i, 2] * np.conj(V[2, 2]) * V[2, 1] / V[i, 1])
    return d


PDG_CKM = (0.22501, 0.04183, 0.003732, 1.147)
VPDG = ckm(*PDG_CKM)


def msbar_V(G):
    D = deltas(VPDG, G)
    target = np.array([abs(VPDG[0, 1]) / (1 + D[0, 1].real), abs(VPDG[1, 2]) / (1 + D[1, 2].real),
                       abs(VPDG[0, 2]) / (1 + D[0, 2].real), gamma_angle(VPDG) - (D[0, 0] - D[0, 2] - D[1, 0] + D[1, 2]).imag])

    def res(p):
        V = ckm(*p)
        return np.array([abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2]), gamma_angle(V)]) - target
    p = np.array(PDG_CKM, float)
    for _ in range(30):
        r = res(p)
        Jm = np.zeros((4, 4))
        for k in range(4):
            dp = np.zeros(4); dp[k] = 1e-7 * max(abs(p[k]), 1e-3)
            Jm[:, k] = (res(p + dp) - r) / dp[k]
        p = p - np.linalg.solve(Jm, r)
        if np.max(np.abs(r)) < 1e-15:
            break
    return ckm(*p)


def pack(Yu, Yd, Ye, gp, g, gs, lam):
    return np.concatenate([np.concatenate([m.real.ravel(), m.imag.ravel()]) for m in (Yu, Yd, Ye)] + [[gp, g, gs, lam]])


def unpack(y):
    m = [y[18 * k:18 * k + 9].reshape(3, 3) + 1j * y[18 * k + 9:18 * k + 18].reshape(3, 3) for k in range(3)]
    return (*m, *y[54:58])


def rhs(t, y):
    Yu, Yd, Ye, gp, g, gs, lam = unpack(y)
    bu, bd, be = (b / K for b in note_beta1(Yu, Yd, Ye, gs, g, gp))
    tr = lambda x: np.trace(x).real
    Hu, Hd, He = Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye)
    T = 3 * tr(Hu) + 3 * tr(Hd) + tr(He)
    dl = (24 * lam**2 + 4 * lam * T - 2 * (3 * tr(Hu @ Hu) + 3 * tr(Hd @ Hd) + tr(He @ He))
          - 3 * lam * (3 * g**2 + gp**2) + 3 / 8 * (2 * g**4 + (g**2 + gp**2)**2)) / K
    return pack(bu, bd, be, 41 / 6 * gp**3 / K, -19 / 6 * g**3 / K, -7 * gs**3 / K, dl)


def ckm_of(Yu, Yd):
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    return dag(Uu[:, ::-1]) @ Ud[:, ::-1], su[::-1], sd[::-1]


def start():
    G = G_of(YT3, G2, G2 * VFJ / 2, MT_START)
    V0 = msbar_V(G)
    yu = np.array([YB * MQ["u"] / MQ["b"], YB * MQ["c"] / MQ["b"], YT3])
    yd = YB * np.array([MQ["d"], MQ["s"], MQ["b"]]) / MQ["b"]
    ye = YTAU * np.array([ML["e"], ML["mu"], ML["tau"]]) / ML["tau"]
    return G, V0, pack(np.diag(yu).astype(complex), V0 @ np.diag(yd), np.diag(ye).astype(complex), GY, G2, G3, LAM)


G_MT, V_MT, Y_MT = start()
_sols = {}


def at(mu):
    """the MS-bar parameters at mu (one-loop running from M_t)"""
    if mu == MT_START:
        y = Y_MT
    else:
        key = round(math.log(mu), 12)
        if key not in _sols:
            _sols[key] = solve_ivp(rhs, (math.log(MT_START), math.log(mu)), Y_MT, **TOL).y[:, -1]
        y = _sols[key]
    Yu, Yd, Ye, gp, g, gs, lam = unpack(y)
    V, yu, yd = ckm_of(Yu, Yd)
    ye = np.linalg.svd(Ye, compute_uv=False)[::-1]
    e = g * gp / math.sqrt(g**2 + gp**2)
    return {"mu": mu, "gp": gp, "g": g, "gs": gs, "lam": lam, "yu": yu, "yd": yd, "ye": ye, "V": V, "e": e,
            "s2": gp**2 / (g**2 + gp**2), "gZ": math.sqrt(g**2 + gp**2), "alpha": e**2 / (4 * math.pi),
            "alphas": gs**2 / (4 * math.pi)}


if __name__ == "__main__":
    for mu in (POLE["MZ"], POLE["MW"], POLE["MH"], MT_START):
        p = at(mu)
        print("mu = %8.4f: g' %.6f g %.6f g_s %.6f lambda %.6f  1/alpha %.4f s^2 %.6f alpha_s %.5f  y_t %.5f y_b %.6f y_tau %.6f"
              "  |V_cb| %.6f" % (mu, p["gp"], p["g"], p["gs"], p["lam"], 1 / p["alpha"], p["s2"], p["alphas"], p["yu"][2],
                                 p["yd"][2], p["ye"][2], abs(p["V"][1, 2])))
