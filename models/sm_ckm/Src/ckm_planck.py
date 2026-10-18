# %% [markdown]
# # Step (10) of the CKM note: V and J from M_t to the Planck scale
#
# Research note models/sm_ckm, step (10).  The running uses the note's equations:
#   one loop: Eq. (betaY) for the complex 3 x 3 matrices Y_u, Y_d, Y_e (derived from the note's model in step (4)), the gauge
#             couplings and lambda at one loop (the SM note's Eq. (beta), lambda with the traces of H_f, H_f^2);
#   two loops (an estimate of the higher orders): plus beta^(2)_{Y_f} of rg2_ckm_general.py (the general two-loop formulas
#             with the explicit field content and complex matrices, checked there against the SM note's two-loop gaugeless
#             terms from its model and the diagonal limit of Buttazzo et al.) and the two-loop gauge beta functions with
#             traces; lambda stays at one loop (it enters beta_Y first at two loops).
# Start (mu = M_t = 172.57 GeV): the SM note's step (7) MS-bar values (PDG 2024, M_W scheme; models/sm/Src/results/msbar_fit.csv):
#   g', g, g_s, lambda, v_FJ, y_t with the pure QCD corrections to three loops (variant: the one-loop matching); y_b, y_tau of
#   Martin and Robertson at M_t (as the SM note's step (8)); the light Yukawa couplings from the benchmark mass ratios of
#   Eq. (bench) at M_Z, y_q = y_b m_q/m_b and y_l = y_tau m_l/m_tau (the QCD running is the same for all quarks).
#   V(M_t): the step (6) conversion of the PDG standard parameters at mu = M_t, V^phys_ij = V_ij(M_t) (1 + Delta_ij), with
#   G(M_t) of Eq. (Gmu) from the MS-bar x_t = 2 y_t^2/g^2 and M_W = g v_FJ/2 (variant: the pole mass in the logarithm).
# Checks: (i) the closed forms Eq. (yrun), Eq. (Vrun) integrated as an ODE for the singular values and V against the
# matrices (one loop); (ii) a random rotation of the generation bases of Q_L, u_R, d_R, L_L, e_R (one and two loops);
# (iii) the hierarchical limit Eq. (Vhier) integrated along the trajectory; (iv) the Wolfenstein parameters.
# Output: results/ckm_planck.csv, ../ResearchNote/fig_vrun.pdf.  Batch: python3 ckm_planck.py

# %%
import csv
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from rg2_ckm_general import K, SMSRC, dag, gauge_closed, note_beta1, structures

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
NOTE = HERE.parent / "ResearchNote"
MPL = 1.2209e19
MT = 172.57
TOL = dict(method="DOP853", rtol=1e-12, atol=1e-15)

# two-loop coefficients, in the order of structures()
coef = {f: [] for f in "ude"}
for r in csv.DictReader(open(RES / "rg2_ckm_coeffs.csv")):
    coef[r["flavour"]].append(int(r["numerator"]) / int(r["denominator"]))
coef = {f: np.array(c) for f, c in coef.items()}


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


# %% [markdown]
# ## Starting values at M_t

# %%
fit = {r[0]: r for r in csv.reader(open(SMSRC / "results" / "msbar_fit.csv"))}
lamP, yt1P, yt3P, g2P, gYP, mP, vP, g3P = (float(x) for x in fit["PDG2024_MW_scheme"][1:9])
YB, YTAU = 0.015480097, 0.0099944422             # Martin-Robertson at M_t (the SM note's step (8))
MQ = {"u": 0.00127, "c": 0.619, "d": 0.00271, "s": 0.0546, "b": 2.86}     # Eq. (bench), mu = M_Z (ratios only)
ML = {"e": 0.000487, "mu": 0.1027, "tau": 1.746}


def yukawas(yt):
    yu = np.array([YB * MQ["u"] / MQ["b"], YB * MQ["c"] / MQ["b"], yt])
    yd = YB * np.array([MQ["d"], MQ["s"], MQ["b"]]) / MQ["b"]
    ye = YTAU * np.array([ML["e"], ML["mu"], ML["tau"]]) / ML["tau"]
    return yu, yd, ye


# step (6): V^phys = V(mu) (1 + Delta(mu)), Delta of Eq. (Deltaij), G of Eq. (Gmu)
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


PDG = {"s12": 0.22501, "s23": 0.04183, "s13": 0.003732, "delta": 1.147}
PDG_ERR = {"s12": 0.00068, "s23": 0.00079, "s13": 0.000090, "delta": 0.026}
VPDG = ckm(PDG["s12"], PDG["s23"], PDG["s13"], PDG["delta"])


def msbar_V(G):
    """the step (6) solve: standard parameters of V(mu) from the PDG |V_us|, |V_cb|, |V_ub| and gamma"""
    D = deltas(VPDG, G)
    target = np.array([abs(VPDG[0, 1]) / (1 + D[0, 1].real), abs(VPDG[1, 2]) / (1 + D[1, 2].real),
                       abs(VPDG[0, 2]) / (1 + D[0, 2].real), gamma_angle(VPDG) - (D[0, 0] - D[0, 2] - D[1, 0] + D[1, 2]).imag])

    def res(p):
        V = ckm(*p)
        return np.array([abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2]), gamma_angle(V)]) - target
    p = np.array([PDG["s12"], PDG["s23"], PDG["s13"], PDG["delta"]])
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


# %% [markdown]
# ## The running: matrices (one and two loops) and the closed forms (one loop)

# %%
def pack(Yu, Yd, Ye, gp, g, gs, lam):
    return np.concatenate([np.concatenate([m.real.ravel(), m.imag.ravel()]) for m in (Yu, Yd, Ye)] + [[gp, g, gs, lam]])


def unpack(y):
    m = [y[18 * k:18 * k + 9].reshape(3, 3) + 1j * y[18 * k + 9:18 * k + 18].reshape(3, 3) for k in range(3)]
    return (*m, *y[54:58])


def lam_beta1(Hu, Hd, He, g, gp, lam):
    tr = lambda x: np.trace(x).real
    T = 3 * tr(Hu) + 3 * tr(Hd) + tr(He)
    return (24 * lam**2 + 4 * lam * T - 2 * (3 * tr(Hu @ Hu) + 3 * tr(Hd @ Hd) + tr(He @ He))
            - 3 * lam * (3 * g**2 + gp**2) + 3 / 8 * (2 * g**4 + (g**2 + gp**2)**2)) / K


def rhs_matrix(t, y, order):
    Yu, Yd, Ye, gp, g, gs, lam = unpack(y)
    bu, bd, be = (b / K for b in note_beta1(Yu, Yd, Ye, gs, g, gp))
    dg = np.array([41 / 6 * gp**3, -19 / 6 * g**3, -7 * gs**3]) / K
    if order == 2:
        two = []
        for f in "ude":
            _, X = structures(f, Yu, Yd, Ye, gs, g, gp, lam)
            two.append(np.tensordot(coef[f], np.array(X), axes=1) / K**2)
        bu, bd, be = bu + two[0], bd + two[1], be + two[2]
        cl = gauge_closed(Yu, Yd, Ye, gs, g, gp, lam)
        dg = dg + np.array([cl[1], cl[2], cl[3]]) / K**2
    dl = lam_beta1(Yu @ dag(Yu), Yd @ dag(Yd), Ye @ dag(Ye), g, gp, lam)
    return pack(bu, bd, be, *dg, dl)


def dV_closed(V, yu, yd):
    """K dV/dln mu of Eq. (Vrun): -K A_u V + K V A_d (as ckm_rg_handcheck.py)"""
    Hd_u, Hu_d = V @ np.diag(yd**2) @ dag(V), dag(V) @ np.diag(yu**2) @ V
    KAu, KAd = np.zeros((3, 3), complex), np.zeros((3, 3), complex)
    for i in range(3):
        for k in range(3):
            if i != k:
                KAu[i, k] = -1.5 * (yu[i]**2 + yu[k]**2) / (yu[k]**2 - yu[i]**2) * Hd_u[i, k]
                KAd[i, k] = -1.5 * (yd[i]**2 + yd[k]**2) / (yd[k]**2 - yd[i]**2) * Hu_d[i, k]
    return -KAu @ V + V @ KAd


def rhs_closed(t, y):
    yu, yd, ye = y[0:3], y[3:6], y[6:9]
    V = y[9:18].reshape(3, 3) + 1j * y[18:27].reshape(3, 3)
    gp, g, gs, lam = y[27:31]
    T = 3 * np.sum(yu**2) + 3 * np.sum(yd**2) + np.sum(ye**2)
    Hd_u, Hu_d = V @ np.diag(yd**2) @ dag(V), dag(V) @ np.diag(yu**2) @ V
    dyu = yu * (1.5 * yu**2 - 1.5 * np.diag(Hd_u).real + T - 8 * gs**2 - 9 / 4 * g**2 - 17 / 12 * gp**2) / K
    dyd = yd * (1.5 * yd**2 - 1.5 * np.diag(Hu_d).real + T - 8 * gs**2 - 9 / 4 * g**2 - 5 / 12 * gp**2) / K
    dye = ye * (1.5 * ye**2 + T - 9 / 4 * g**2 - 15 / 4 * gp**2) / K
    dV = dV_closed(V, yu, yd) / K
    dg = np.array([41 / 6 * gp**3, -19 / 6 * g**3, -7 * gs**3]) / K
    dl = lam_beta1(np.diag(yu**2), np.diag(yd**2), np.diag(ye**2), g, gp, lam)
    return np.concatenate([dyu, dyd, dye, dV.real.ravel(), dV.imag.ravel(), dg, [dl]])


def ckm_of(Yu, Yd):
    """V = U_u^dagger U_d from the left singular vectors (ascending singular values), and the singular values"""
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    return dag(Uu[:, ::-1]) @ Ud[:, ::-1], su[::-1], sd[::-1]


def observables(V):
    a = np.abs(V)
    J = jarlskog(V)
    lw = a[0, 1] / math.sqrt(a[0, 0]**2 + a[0, 1]**2)
    rb =-V[0, 0] * np.conj(V[0, 2]) / (V[1, 0] * np.conj(V[1, 2]))
    s13 = a[0, 2]
    c13 = math.sqrt(1 - s13**2)
    s12, s23 = a[0, 1] / c13, a[1, 2] / c13
    delta = math.asin(J / (math.sqrt(1 - s12**2) * math.sqrt(1 - s23**2) * c13**2 * s12 * s23 * s13))
    return {"Vus": a[0, 1], "Vcb": a[1, 2], "Vub": a[0, 2], "Vtd": a[2, 0], "Vts": a[2, 1], "Vtb": a[2, 2], "J": J,
            "delta": delta, "lambdaW": lw, "A": s23 / s12**2, "rhobar": rb.real, "etabar": rb.imag}


def run_matrix(Yu, Yd, Ye, gp, g, gs, lam, order, mu1=MPL):
    return solve_ivp(rhs_matrix, (math.log(MT), math.log(mu1)), pack(Yu, Yd, Ye, gp, g, gs, lam), args=(order,),
                     dense_output=True, **TOL)


def at(sol, mu):
    Yu, Yd, Ye, gp, g, gs, lam = unpack(sol.sol(math.log(mu)))
    V, su, sd = ckm_of(Yu, Yd)
    o = observables(V)
    o.update({"yt": su[2], "yb": sd[2], "gs": gs, "lam": lam})
    return o


# %% [markdown]
# ## The runs

# %%
def start(yt, mw_log):
    G = G_of(yt, g2P, mw_log, MT)
    V0 = msbar_V(G)
    yu, yd, ye = yukawas(yt)
    return G, V0, (np.diag(yu).astype(complex), V0 @ np.diag(yd), np.diag(ye).astype(complex), gYP, g2P, g3P, lamP)


MW_FJ = g2P * vP / 2
G0, V0, s0 = start(yt3P, MW_FJ)
print("start at mu = M_t = %.2f GeV (the SM note's step (7), PDG 2024): g' %.6f, g %.6f, g_s %.6f, y_t %.6f, y_b %.6f, "
      "y_tau %.6f, lambda %.6f, v_FJ %.3f GeV" % (MT, gYP, g2P, g3P, yt3P, YB, YTAU, lamP, vP))
print("  G(M_t) = %.5e (x_t = %.4f, M_W = g v_FJ/2 = %.3f GeV);  MS-bar V(M_t): |V_us| %.6f, |V_cb| %.6f, |V_ub| %.7f, "
      "J %.5e;  relative to PDG: %+.2e, %+.2e, %+.2e, %+.2e" %
      (G0, 2 * yt3P**2 / g2P**2, MW_FJ, abs(V0[0, 1]), abs(V0[1, 2]), abs(V0[0, 2]), jarlskog(V0),
       abs(V0[0, 1]) / abs(VPDG[0, 1]) - 1, abs(V0[1, 2]) / abs(VPDG[1, 2]) - 1, abs(V0[0, 2]) / abs(VPDG[0, 2]) - 1,
       jarlskog(V0) / jarlskog(VPDG) - 1))
sol = {1: run_matrix(*s0, 1), 2: run_matrix(*s0, 2)}
SCALES = [("Mt", MT), ("1e3", 1e3), ("1e6", 1e6), ("1e9", 1e9), ("1e12", 1e12), ("1e16", 1e16), ("MPl", MPL)]
KEYS = ["Vus", "Vcb", "Vub", "Vtd", "Vts", "Vtb", "J", "delta", "lambdaW", "A", "rhobar", "etabar", "yt", "yb", "gs", "lam"]
rows = []
for order in (1, 2):
    print("%d loop%s:" % (order, "" if order == 1 else "s"))
    for name, mu in SCALES:
        o = at(sol[order], mu)
        rows.append([order, name, mu] + [o[k] for k in KEYS])
        print("  %-5s |V_us| %.6f |V_cb| %.6f |V_ub| %.7f |V_td| %.7f |V_ts| %.6f J %.5e delta %.5f  A %.5f rhobar %.5f "
              "etabar %.5f  y_t %.4f y_b %.5f lambda %+.4f" % (name, *(o[k] for k in ("Vus", "Vcb", "Vub", "Vtd", "Vts", "J",
                                                                                  "delta", "A", "rhobar", "etabar", "yt",
                                                                                  "yb", "lam"))))
o0, o1, o2 = at(sol[1], MT), at(sol[1], MPL), at(sol[2], MPL)
print("ratio M_Pl / M_t, 1 loop: |V_cb| %.5f |V_ub| %.5f |V_td| %.5f |V_ts| %.5f |V_us| %.7f J %.5f A %.5f lambda_W %.7f "
      "rhobar %.6f etabar %.6f" % tuple(o1[k] / o0[k] for k in ("Vcb", "Vub", "Vtd", "Vts", "Vus", "J", "A", "lambdaW",
                                                               "rhobar", "etabar")))
print("two loops minus one loop at M_Pl, relative: |V_cb| %+.2e |V_ub| %+.2e |V_us| %+.2e J %+.2e" %
      tuple(o2[k] / o1[k] - 1 for k in ("Vcb", "Vub", "Vus", "J")))

# %% [markdown]
# ## Checks

# %%
# (i) the closed forms Eq. (yrun), Eq. (Vrun) as an ODE, one loop
yu0, yd0, ye0 = yukawas(yt3P)
yc = np.concatenate([yu0, yd0, ye0, V0.real.ravel(), V0.imag.ravel(), [gYP, g2P, g3P, lamP]])
sc = solve_ivp(rhs_closed, (math.log(MT), math.log(MPL)), yc, **TOL)
Vc = sc.y[9:18, -1].reshape(3, 3) + 1j * sc.y[18:27, -1].reshape(3, 3)
oc = observables(Vc)
dev_i = max(abs(oc[k] / o1[k] - 1) for k in ("Vus", "Vcb", "Vub", "Vtd", "Vts", "J"))
print("(i) Eq. (yrun), (Vrun) integrated against the matrices, at M_Pl: max relative difference of |V_ij|, J %.1e;  "
      "unitarity of the closed-form V %.1e;  y_t %.1e" % (dev_i, np.max(np.abs(Vc @ dag(Vc) - np.eye(3))),
                                                       abs(sc.y[2, -1] / o1["yt"] - 1)))
# (ii) random rotations of the generation bases (Q_L, u_R, d_R, L_L, e_R)
rng = np.random.default_rng(20261018)


def haar():
    z = (rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))) / math.sqrt(2)
    q, r = np.linalg.qr(z)
    return q @ np.diag(np.diag(r) / np.abs(np.diag(r)))


UQ, Uu, Ud, UL, Ue = (haar() for _ in range(5))
Yu0, Yd0, Ye0 = s0[:3]
rot = (UQ @ Yu0 @ dag(Uu), UQ @ Yd0 @ dag(Ud), UL @ Ye0 @ dag(Ue)) + s0[3:]
dev_ii = {}
for order in (1, 2):
    orot = at(run_matrix(*rot, order), MPL)
    ref = o1 if order == 1 else o2
    dev_ii[order] = max(abs(orot[k] / ref[k] - 1) for k in ("Vus", "Vcb", "Vub", "Vtd", "Vts", "J"))
print("(ii) random rotation of the generation bases: max relative difference of |V_ij|, J at M_Pl: one loop %.1e, two loops "
      "%.1e" % (dev_ii[1], dev_ii[2]))
# (iii) the hierarchical limit: ln(|V_cb(M_Pl)/V_cb(M_t)|) = (3/2K) int (y_t^2 + y_b^2) d ln mu
ts = np.linspace(math.log(MT), math.log(MPL), 4001)
ytb = np.array([sum(s**2 for s in (ckm_of(*unpack(sol[1].sol(t))[:2])[1][2], ckm_of(*unpack(sol[1].sol(t))[:2])[2][2]))
                for t in ts])
integral = 1.5 / K * np.sum((ytb[1:] + ytb[:-1]) / 2 * np.diff(ts))
hier = {k: math.log(o1[k] / o0[k]) / integral for k in ("Vcb", "Vub", "Vtd", "Vts")}
hier["J"] = math.log(o1["J"] / o0["J"]) / (2 * integral)
print("(iii) ln of the ratio M_Pl / M_t over (3/2K) int (y_t^2 + y_b^2) d ln mu = %.5f (J: over twice that):  " % integral
      + ", ".join("%s %.5f" % kv for kv in hier.items()))

# (iv) variants of the start
var = {}
for label, yt, mw in (("yt_one_loop_matching", yt1P, MW_FJ), ("MW_pole_in_G", yt3P, 80.3692)):
    Gv, Vv, sv = start(yt, mw)
    ov0, ov1 = observables(Vv), at(run_matrix(*sv, 1), MPL)
    var[label] = (ov0, ov1)
    print("(iv) variant %-22s: V(M_t) |V_cb| %.6f (%+.1e), at M_Pl |V_cb| %.6f (%+.1e), J %.5e (%+.1e)" %
          (label, ov0["Vcb"], ov0["Vcb"] / o0["Vcb"] - 1, ov1["Vcb"], ov1["Vcb"] / o1["Vcb"] - 1, ov1["J"],
           ov1["J"] / o1["J"] - 1))
print("     PDG relative errors: s12 %.1e, s23 %.1e, s13 %.1e, delta %.1e" % tuple(PDG_ERR[k] / PDG[k] for k in PDG))

with open(RES / "ckm_planck.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["loops", "scale", "mu_GeV"] + KEYS)
    for r in rows:
        w.writerow(r[:2] + ["%.6e" % r[2]] + ["%.10e" % x for x in r[3:]])
    w.writerow([])
    w.writerow(["check", "value"])
    for k, v in (("G_Mt", G0), ("closed_forms_vs_matrices_MPl", dev_i), ("basis_rotation_one_loop", dev_ii[1]),
                 ("basis_rotation_two_loops", dev_ii[2]), ("hier_integral", integral)) + tuple(
            ("hier_ratio_" + k, v) for k, v in hier.items()) + tuple(
            ("variant_%s_Vcb_MPl_rel" % lab, ov1["Vcb"] / o1["Vcb"] - 1) for lab, (_, ov1) in var.items()):
        w.writerow([k, "%.10e" % v])

# %% [markdown]
# ## Figure

# %%
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
plt.style.use(str(NOTE / "physrev.mplstyle"))
mus = np.exp(np.linspace(math.log(MT), math.log(MPL), 300))
fig, ax = plt.subplots(1, 2, figsize=(6.8, 2.6))
curves = {order: [at(sol[order], mu) for mu in mus] for order in (1, 2)}
x = np.log10(mus)
# (a) |V_cb| (|V_ub|, |V_td|, |V_ts| and A lie on it within 0.03), J, |V_us|, in per cent of the value at M_t
for k, lab, c in (("J", r"$J$", "C0"), ("Vcb", r"$|V_{cb}|$ ($\simeq|V_{ub}|,|V_{td}|,|V_{ts}|,A$)", "C1"),
                  ("Vus", r"$|V_{us}|$", "C2")):
    for order, ls in ((1, "-"), (2, "--")):
        ax[0].plot(x, [100 * (cc[k] / curves[1][0][k] - 1) for cc in curves[order]], ls, color=c,
                   label=lab if order == 1 else None)
ax[0].set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
ax[0].set_ylabel(r"change from $\mu=M_t$ (per cent)")
ax[0].legend(fontsize=6, frameon=False, loc="upper left")
# (b) the Wolfenstein parameters that hardly run, in units of 1e-4
for k, lab, c in (("lambdaW", r"$\lambda$", "C2"), ("rhobar", r"$\bar\rho$", "C3"), ("etabar", r"$\bar\eta$", "C4")):
    for order, ls in ((1, "-"), (2, "--")):
        ax[1].plot(x, [1e4 * (cc[k] / curves[1][0][k] - 1) for cc in curves[order]], ls, color=c,
                   label=lab if order == 1 else None)
ax[1].axhline(0, color="k", lw=0.4)
ax[1].set_xlabel(r"$\log_{10}(\mu/\mathrm{GeV})$")
ax[1].set_ylabel(r"change from $\mu=M_t$ ($10^{-4}$)")
ax[1].legend(fontsize=6, frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(NOTE / "fig_vrun.pdf")
print("wrote results/ckm_planck.csv and ResearchNote/fig_vrun.pdf")
