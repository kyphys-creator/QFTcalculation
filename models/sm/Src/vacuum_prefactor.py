# %% [markdown]
# # Step (10f): the one-loop prefactor of the electroweak vacuum decay rate, with the leading gravitational correction
#
# Research note models/sm, step (10).  Everything from the note's own model and running (step (8), sm_running.py):
#   Gamma/V = int dR/R R^-4 exp[-S0(R) - dS_grav(R)] F(R),  S0 = 8 pi^2/(3 |lambda(1/R)|),
#   dS_grav = 32 pi^2/(45 lambda^2 (R Mbar)^2) (vacuum_gravity.py), couplings in MS-bar at mu = 1/R.
# F(R) is the one-loop factor around the Fubini bounce h = A R/(r^2 + R^2), A^2 = 8/|lambda| (bounce_det.py, R = 1 units):
#   Higgs     -1/2 ln det' O_h + 5 ln A      (dilatation and the four translations as collective coordinates)
#   W, Z      2 ag_sector(x_W) + ag_sector(x_Z) + 3 ln A + ln(2 pi^2), x_W = g^2/(4|lambda|), x_Z = (g^2 + g'^2)/(4|lambda|):
#             each real massive vector with its Goldstone and ghosts in the background Feynman gauge; the l = 0 global-rotation
#             (threshold) mode of each broken generator is a collective coordinate on the S^3 orbit (volume 2 pi^2)
#   top       top_sector(x_t), x_t = y_t^2/|lambda|, N_c = 3   (the light fermions and the photon/gluons are left out)
# Checks (own): the partial-wave content of the vector field (an uncoupled vector = four scalars); the Faddeev-Popov
# factor of the l = 0 threshold mode with two different normalizable functions; the mu-independence of -S0 + ln F sector
# by sector (the ln mu terms against the note's one-loop beta_lambda); the R integral against its saddle point; the spline
# of ln F against a direct evaluation; the top channels and the gauge-Goldstone levels against their closed forms.
# Reference (Andreassen-Frost-Schwartz, arXiv:1707.08124 v4, read from its source): their closed forms for the Higgs and
# for the Goldstone limit agree with ours, and so does their quoted top factor; their gauge-sector formula differs from
# ours by exactly two terms, (i) one transverse mode per level s >= 1 (the S^3 transverse vector
# harmonics number 2 s (s + 2), not 2 (s + 1)^2, so the ghosts do not cancel them) and (ii) the l = 0 Born terms, which
# the diagrams contain and which their gauge formula does not subtract from R_0' = 1 (their global-symmetry Goldstone
# formula does).  Reference (Chigusa-Moroi-Shoji, arXiv:1803.03902): their Fermi-gauge formula differs from ours by (i)
# alone (they use the same transverse basis, but subtract the l = 0 Born terms).  Then log10(Gamma/V),
# P = (Gamma/V) T_U^4 and tau = (Gamma/V)^(-1/4), without and with gravity, for the
# note's start and, as a reference, the literature start and three-loop running.
# Writes results/vacuum_prefactor.csv and results/vacuum_prefactor_grid.csv.  Batch: python3 vacuum_prefactor.py
# (the 75 sector determinants run in 13 parallel processes; about 25 minutes)

# %%
import csv
import math
import time
from concurrent.futures import ProcessPoolExecutor

import mpmath as mp
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.special import loggamma, zeta as hzeta

from bounce_det import ag_blocks, ag_sector, gy_block, higgs_lndet, sector_sum, top_sector, A2_from, ag_trEE, \
    fourier_hb2, top_trEE
from sm_running import MPL, RES, run, starts, at

MBAR = MPL / math.sqrt(8 * math.pi)
L10 = math.log(10)
HBAR_GEV_S, YEAR_S = 6.582119569e-25, 3.15576e7
T_U = 13.8e9 * YEAR_S / HBAR_GEV_S                 # GeV^-1, as in vacuum_decay.py
GRID = np.arange(14.5, 19.51, 0.5)                 # log10(1/R / GeV)
CASES = [("note", "B_note_PDG_yt_QCD3", ("note", 2)), ("reference", "A_Buttazzo_NNLO", ("lit", 3))]
AFS_POINT = {"lam": -0.0138, "yt": 0.402, "g": 0.515, "gp": 0.460}     # their mu* couplings (reference)


def couplings(sol, lmu):
    c = at(sol, 10 ** lmu)
    lam, g2, gp2, yt2 = c["lam"], c["g2"] ** 2, 0.6 * c["g1"] ** 2, c["yt"] ** 2
    return {"lam": lam, "xW": g2 / (4 * abs(lam)), "xZ": (g2 + gp2) / (4 * abs(lam)), "xt": yt2 / abs(lam),
            "g2": g2, "gp2": gp2, "yt2": yt2}


def vector_count(lmax=80):
    """an uncoupled vector with U_V delta_mu nu in the (+, -, T) partial waves against four scalars, and with the
    transverse count 2 (l+1)^2 instead of 2 l (l+2)"""
    UV = lambda r: np.array([[16.0 / (1 + r * r) ** 2]])          # x_V = 2

    def vec(l, nT):
        out = [((l + 1) ** 2, [l + 1], UV)]
        if l >= 1:
            out += [((l + 1) ** 2, [l - 1], UV), (nT(l), [l], UV)]
        return out
    Sv = sector_sum(lambda l: vec(l, lambda l: 2 * l * (l + 2)), lmax)[0]
    Sw = sector_sum(lambda l: vec(l, lambda l: 2 * (l + 1) ** 2), lmax)[0]
    Ss = sector_sum(lambda l: [((l + 1) ** 2, [l], UV)], lmax)[0]
    return Sv, 4 * Ss, Sw


def threshold_check(xV, eps=1e-8):
    """Faddeev-Popov factor of the l = 0 (+, G) block's threshold mode z = (theta'/e, theta h_b), theta the ghost's l = 0
    zero-energy solution with theta(0) = 1, from two normalizable f: |<f, z>|/sqrt(2 pi) [R(eps) <f, (O + eps)^-1 f>]^(-1/2)
    (the 4d inner products with the l = 0 harmonic 1/sqrt(2 pi^2)).  Normalized to the unit global rotation at infinity,
    z/theta_inf, this is the factor sqrt(2 pi)/theta_inf used in ag_sector, so the value should be sqrt(2 pi) for both f."""
    from scipy.integrate import solve_ivp, quad
    from bounce_det import gy_block_massive, green_inner_matrix
    _, ks, E = ag_blocks(xV, 0)[0]
    th = solve_ivp(lambda r, y: [y[1], -3 * y[1] / r + 8 * xV / (1 + r * r) ** 2 * y[0]], (1e-6, 1e6), [1.0, 0.0],
                   method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)
    e = math.sqrt(8 * xV)
    z = lambda r: (th.sol(r)[1] / e, th.sol(r)[0] / (1 + r * r))
    ld, sg = gy_block_massive(ks, E, eps)
    out = []
    for f in (lambda r: np.array([r * math.exp(-r * r), math.exp(-r * r)]),
              lambda r: np.array([0.3 * r ** 3 * math.exp(-r * r / 2), (1 - r * r) * math.exp(-r * r)])):
        fz = quad(lambda r: r ** 3 * (f(r)[0] * z(r)[0] + f(r)[1] * z(r)[1]), 0, 50, limit=400)[0]
        gi = green_inner_matrix(ks, E, f, eps)
        out.append(math.sqrt(2 * math.pi ** 2) * abs(fz) / math.sqrt(2 * math.pi) / math.sqrt(abs(sg * math.exp(ld) * gi)))
    return out


def task(t):
    kind, x = t
    if kind == "ag":
        return t, ag_sector(x)[0]
    if kind == "top":
        return t, top_sector(x)[0]
    if kind == "higgs":
        return t, higgs_lndet(200)[0]
    if kind == "count":
        return t, vector_count()
    raise ValueError(kind)


# ---- reference (AFS) closed forms, evaluated here; the functions R_s are theirs, the sums ours ----
mp.mp.dps = 40
GE = float(mp.euler)
ZP = float(mp.diff(mp.zeta, -1))


def _tail(t):
    t = np.array([float(v) for v in t])
    n = len(t)
    s = np.arange(1, n + 1, dtype=float)
    k = n // 2
    c = np.linalg.lstsq(np.vstack([s[k:] ** -3, s[k:] ** -4, s[k:] ** -5]).T, t[k:], rcond=None)[0]
    return t.sum() + c[0] * hzeta(3, n + 1) + c[1] * hzeta(4, n + 1) + c[2] * hzeta(5, n + 1)


def afs_lnR(s, xA):          # their R_s(x) = det(-Delta_s - 3 x lambda h_b^2)/det(-Delta_s); x = e^2/(3|lambda|) for mass e h_b
    kap = mp.sqrt(1 - 24 * mp.mpf(xA))
    return mp.re(mp.loggamma(1 + s) + mp.loggamma(2 + s) - mp.loggamma(mp.mpf(3) / 2 + s - kap / 2)
                 - mp.loggamma(mp.mpf(3) / 2 + s + kap / 2))


def afs_lnR_sub(s, xA):      # its x and x^2 terms
    xA = mp.mpf(xA)
    return (6 * (s + 1) * xA + 18 * (3 + 2 * s - 2 * (s + 1) ** 2 * mp.psi(1, 1 + s)) * xA ** 2) / (s + 1) ** 2


def afs_gauge(xV, smax=3000):
    """their boxed R_xi formula for one real vector with its Goldstone (mu = 1/R, without J_G and the orbit)"""
    xA, gl, L = xV / 3, -xV, -math.log(2)
    Sfp = _tail([(s + 1) ** 2 * (afs_lnR(s, xA) - afs_lnR_sub(s, xA)) for s in range(1, smax + 1)])
    SfGp = 85 / 18 - 2 * math.pi ** 2 / 3 + 2 * GE / 3 - 4 * ZP + math.log(2)
    mSl = (5 / 18 + GE / 3 + L / 3) - gl * (7 / 3 + 2 * GE + 2 * L) + gl ** 2 * (0.5 + GE + L)
    Sd = (4 * math.pi ** 2 - 121 / 3) * gl - 2.5 * gl ** 2
    return -1.5 * Sfp - 0.5 * SfGp + mSl + 0.5 * Sd


def cms_gauge(xV):
    """Chigusa-Moroi-Shoji (arXiv:1803.03902, Fermi gauge, angular-momentum regularization converted to MS-bar) for one
    real vector with its Goldstone: ln A' - ln A at mu = 1/R, with their S_sigma from its t-integral (reference)"""
    z = -(1 - mp.sqrt(1 - 8 * mp.mpf(xV))) / 2
    H = mp.harmonic
    S = mp.quad(lambda t: (-z + z ** 2 * (-mp.mpf(53) / 36 + t + (1 - t) * H(t * z - z) / 6 + t * H(t * z) / 6)
                           + z ** 3 / 12 * (-7 + 14 * t + 6 * (1 - t) ** 2 * H(t * z - z) + 6 * t ** 2 * H(t * z))
                           + z ** 4 / 9 * (-1 + 3 * (1 - t) * t + 3 * (1 - t) ** 3 * H(t * z - z) + 3 * t ** 3 * H(t * z))),
                [0, 1])
    x, L = mp.mpf(xV), -mp.log(2)
    val = ((mp.mpf(1) / 3 + 2 * x + x ** 2) * (1 + mp.euler + L) - 1 - x ** 2 * (mp.mpf(31) / 3 - mp.pi ** 2) + mp.mpf(3) / 4
           - mp.euler / 3 - 2 * mp.log(mp.glaisher) + mp.log(mp.pi) / 2 - 1.5 * S - 1.5 * (mp.loggamma(1 - z) + mp.loggamma(2 + z)))
    return float(mp.re(val))


def transverse_residual(xV, smax=3000):
    """(i): sum_{s>=1} [ln R_s - its x, x^2 terms], the one transverse mode per level left over by the ghosts"""
    return _tail([afs_lnR(s, xV / 3) - afs_lnR_sub(s, xV / 3) for s in range(1, smax + 1)])


def l0_born(xV):
    """(ii): the l = 0 Born terms of our scheme, 1/2 (B1 + B2) of the (+, G) block minus those of the ghost"""
    blk = ag_blocks(xV, 0)[0]
    _, b1, b2 = gy_block(blk[1], blk[2])
    _, g1, g2 = gy_block([0], lambda r: np.array([[8 * xV / (1 + r * r) ** 2]]))
    return 0.5 * (b1 + b2) - (g1 + g2)


def top_channel_check(xt, ks=(0, 1, 5)):
    """ln det T of the 2 x 2 top channel (k, k+1) against the closed form 2 ln[Gamma(n)^2/|Gamma(n + i sqrt(x_t))|^2],
    n = k + 2 (the R_j of AFS with |j| + 1/2 = n)"""
    from bounce_det import top_blocks
    out = []
    for k in ks:
        _, kk, E = top_blocks(xt, k)[0]
        ld = gy_block(kk, E)[0]
        n = k + 2
        out.append((k, ld, 2 * float(2 * loggamma(n).real - 2 * loggamma(complex(n, math.sqrt(xt))).real)))
    return out


def afs_higgs():
    """their real-scalar result with J_d J_T^4 R^5 at A = 1: (2 pi/5)^(5/2) (25/36) sqrt(5/6) exp(-5/4 + 6 zeta'(-1) - 3 ln 2)"""
    return 2.5 * math.log(2 * math.pi / 5) + math.log(25 / 36) + 0.5 * math.log(5 / 6) - 1.25 + 6 * ZP - 3 * math.log(2)


def afs_goldstone0():
    """their global-symmetry Goldstone, Eq. (detGfinal), with J_G at A = 1: sqrt(2 pi) sqrt(1/2) exp(-1/12 + 2 zeta'(-1) - ln2/3)"""
    return 0.5 * math.log(2 * math.pi) + 0.5 * math.log(0.5) - 1 / 12 + 2 * ZP - math.log(2) / 3


# ---- mu-independence: d ln F/d ln mu from the A2 terms against (8 pi^2/(3 lambda^2)) beta_lambda, sector by sector ----
def dlnF_dlnmu(xW, xZ, xt):
    e = math.e
    d = lambda f: A2_from(f, mu=e) - A2_from(f, mu=1.0)
    higgs = -0.5 * d(lambda p: (24 * fourier_hb2(p)) ** 2)

    def vec(x):
        return -0.5 * d(lambda p: ag_trEE(x, p)) + d(lambda p: (8 * x * fourier_hb2(p)) ** 2)
    top = 1.5 * d(lambda p: top_trEE(xt, p))
    return higgs, 2 * vec(xW) + vec(xZ), top


def ln_F(sec_h, ag_W, ag_Z, top, lam):
    lnA = 0.5 * math.log(8 / abs(lam))
    higgs = -0.5 * sec_h + 5 * lnA
    gauge = 2 * ag_W + ag_Z + 3 * lnA + math.log(2 * math.pi ** 2)
    return higgs + gauge + top, (higgs, gauge, top)


def rate(lmus, S, lnF):
    """log10(Gamma/V / GeV^4) = log10 int d ln mu mu^4 exp(-S + ln F), and the saddle point"""
    expo = 4 * lmus * L10 - S + lnF
    k = int(np.argmax(expo))
    m = expo[k]
    val = m + math.log(np.trapezoid(np.exp(expo - m), lmus * L10))
    h = lmus[1] - lmus[0]
    d2 = (expo[k + 1] - 2 * expo[k] + expo[k - 1]) / (h * L10) ** 2
    saddle = m + 0.5 * math.log(2 * math.pi / -d2)
    return val / L10, saddle / L10, lmus[k]


def main():
    t0 = time.time()
    sols = {name: run(*starts[start], 10 * MPL, rge) for name, start, rge in CASES}
    coup = {name: [couplings(sols[name], lm) for lm in GRID] for name, *_ in CASES}
    # the saddle region of the note's case with gravity, for the spline check
    tasks = {("higgs", 0.0), ("count", 0.0), ("ag", 0.0)}
    pA = AFS_POINT
    xA_W, xA_Z, xA_t = pA["g"] ** 2 / 4 / abs(pA["lam"]), (pA["g"] ** 2 + pA["gp"] ** 2) / 4 / abs(pA["lam"]), \
        pA["yt"] ** 2 / abs(pA["lam"])
    tasks |= {("ag", xA_W), ("ag", xA_Z), ("top", xA_t)}
    for name in coup:
        for c in coup[name]:
            tasks |= {("ag", c["xW"]), ("ag", c["xZ"]), ("top", c["xt"])}
    lmid = 16.75
    cmid = couplings(sols["note"], lmid)
    tasks |= {("ag", cmid["xW"]), ("ag", cmid["xZ"]), ("top", cmid["xt"])}
    tasks = sorted(tasks, key=lambda t: (t[0] != "count", -t[1]))
    with ProcessPoolExecutor(max_workers=13) as ex:
        val = dict(ex.map(task, tasks))
    print("%d sector determinants in %.0f s" % (len(tasks), time.time() - t0))

    # %% checks
    Sv, S4, Sw = val[("count", 0.0)]
    print("vector partial waves (x_V = 2): (+, -, T) with 2l(l+2) transverse modes %.8f, four scalars %.8f; with 2(l+1)^2: %.8f"
          % (Sv, S4, Sw))
    lnh = val[("higgs", 0.0)]
    print("Higgs at A = 1: ours %.6f, AFS (reference) %.6f" % (-0.5 * lnh, afs_higgs()))
    print("Goldstone limit x -> 0 at A = 1: ours %.6f, AFS global-symmetry formula (reference) %.6f"
          % (val[("ag", 0.0)], afs_goldstone0()))
    print("l = 0 threshold mode at x = %.4f: Faddeev-Popov factor with theta(0) = 1 for two f: %.8f, %.8f (sqrt(2 pi) = %.8f)"
          % ((xA_W, *threshold_check(xA_W), math.sqrt(2 * math.pi))))
    for x in (xA_W, xA_Z):
        ours, ref, i, ii = val[("ag", x)], afs_gauge(x), transverse_residual(x), l0_born(x)
        print("gauge sector x = %.4f: ours %.6f; AFS formula (reference) + ln sqrt(2 pi) %.6f; + (i) %.6f + (ii) %.6f = %.6f "
              "(ours - that = %.1e)" % (x, ours, ref + 0.5 * math.log(2 * math.pi), i, ii,
                                        ref + 0.5 * math.log(2 * math.pi) + i + ii,
                                        ours - ref - 0.5 * math.log(2 * math.pi) - i - ii))
    print("   x -> 0: (ii) = %.6f, -(pi^2/3 - 2) = %.6f (their gauge formula at g -> 0 against their global one)"
          % (l0_born(0.0), -(math.pi ** 2 / 3 - 2)))
    for x in (0.0, xA_W, xA_Z):
        ours, ref = val[("ag", x)], cms_gauge(x)
        i = transverse_residual(x) if x > 0 else 0.0
        print("gauge sector x = %.4f: ours %.6f; Chigusa-Moroi-Shoji formula (reference) %.6f; ours - that %.6f, (i) %.6f"
              % (x, ours, ref, ours - ref, i))
    for l in (1, 2, 5):
        blk = ag_blocks(xA_Z, l)[0]
        ld = gy_block(blk[1], blk[2])[0]
        print("   level l = %d at x = %.4f: ln det of the (+, -, G) block %.10f, closed form 3 ln R_l + ln(l/(l+2)) %.10f"
              % (l, xA_Z, ld, 3 * float(afs_lnR(l, xA_Z / 3)) + math.log(l / (l + 2))))
    for k, ld, ref in top_channel_check(xA_t):
        print("top channel k = %d at x_t = %.4f: Gel'fand-Yaglom %.10f, closed form %.10f" % (k, xA_t, ld, ref))
    c = coup["note"][5]
    lam = c["lam"]
    dh, dg, dt = dlnF_dlnmu(c["xW"], c["xZ"], c["xt"])
    K = 16 * math.pi ** 2
    pre = 8 * math.pi ** 2 / (3 * lam ** 2) / K
    bh = pre * 24 * lam ** 2
    bg = pre * (3 / 8 * (2 * c["g2"] ** 2 + (c["g2"] + c["gp2"]) ** 2) - lam * (9 * c["g2"] + 3 * c["gp2"]))
    bt = pre * (-6 * c["yt2"] ** 2 + 12 * c["yt2"] * lam)
    # the lambda^2 part of the three Goldstones (1/3 each) sits in the vector sectors; move it to the scalar column
    print("mu-independence at 1/R = 10^%.1f GeV: d ln F/d ln mu (scalars %.6f, vectors %.6f, top %.6f) against "
          "(8 pi^2/(3 lambda^2)) beta_lambda (%.6f, %.6f, %.6f)" % (GRID[5], dh + 1.0, dg - 1.0, dt, bh, bg, bt))

    # AFS point (reference): our sectors against their quoted factors and their gauge formula evaluated here
    lnF_A, (hA, gA, tA) = ln_F(lnh, val[("ag", xA_W)], val[("ag", xA_Z)], val[("top", xA_t)], pA["lam"])
    lnJG = 0.5 * math.log(2 * math.pi * 8 / abs(pA["lam"]))
    gA_ref = 2 * afs_gauge(xA_W) + afs_gauge(xA_Z) + 3 * lnJG + math.log(2 * math.pi ** 2)
    di = (2 * transverse_residual(xA_W) + transverse_residual(xA_Z)) / L10
    dii = (2 * l0_born(xA_W) + l0_born(xA_Z)) / L10
    print("at the AFS couplings (reference; their quoted factors in brackets): log10 of Higgs with J_d J_T^4 %.2f [7 - 2], "
          "gauge + Goldstone with V J_G^3 %.2f [1 + 5 - 38 - 14; their formula evaluated here %.2f, ours - that = "
          "(i) %.2f + (ii) %.2f], top %.2f [25], product %.2f [-16]"
          % (hA / L10, gA / L10, gA_ref / L10, di, dii, tA / L10, lnF_A / L10))

    # %% the rate
    rows, grid_rows = [], []
    for name, start, rge in CASES:
        lF = []
        for lm, cc in zip(GRID, coup[name]):
            v, parts = ln_F(lnh, val[("ag", cc["xW"])], val[("ag", cc["xZ"])], val[("top", cc["xt"])], cc["lam"])
            lF.append(v)
            grid_rows.append([name, "%.2f" % lm, "%.6f" % cc["lam"], "%.5f" % cc["xW"], "%.5f" % cc["xZ"], "%.5f" % cc["xt"]]
                             + ["%.6f" % (p / L10) for p in parts] + ["%.6f" % (v / L10)])
        spl = CubicSpline(GRID, lF)
        if name == "note":
            vm, _ = ln_F(lnh, val[("ag", cmid["xW"])], val[("ag", cmid["xZ"])], val[("top", cmid["xt"])], cmid["lam"])
            print("spline of ln F at 10^%.2f GeV: %.5f, direct %.5f" % (lmid, spl(lmid), vm))
        lmus = np.linspace(GRID[0], GRID[-1], 4001)
        lam_f = np.array([sols[name].sol(lm * L10)[6] for lm in lmus])
        S0 = 8 * math.pi ** 2 / (3 * np.abs(lam_f))
        dS = 32 * math.pi ** 2 / (45 * lam_f ** 2) * (10 ** lmus / MBAR) ** 2
        for grav in (False, True):
            S = S0 + (dS if grav else 0.0)
            lg, lg_s, lstar = rate(lmus, S, spl(lmus))
            lg1, _, lstar1 = rate(lmus, S, 0.0 * lmus)                  # F = 1 for comparison
            k = int(np.argmin(np.abs(lmus - lstar)))
            log10P = lg + 4 * math.log10(T_U)
            log10tau = -lg / 4 + math.log10(HBAR_GEV_S / YEAR_S)
            print("%-9s %-12s: log10(Gamma/V/GeV^4) = %.2f (saddle point %.2f; F = 1: %.2f), log10 P = %.1f, tau = 10^%.1f yr; "
                  "peak 1/R = 10^%.2f GeV, S = %.1f, log10 F = %.2f"
                  % (name, "with gravity" if grav else "flat", lg, lg_s, lg1, log10P, log10tau, lstar, S[k],
                     float(spl(lstar)) / L10))
            rows.append([name, "with_gravity" if grav else "flat", "%.3f" % lg, "%.3f" % lg_s, "%.3f" % lg1, "%.2f" % log10P,
                         "%.2f" % log10tau, "%.3f" % lstar, "%.2f" % S[k], "%.3f" % (float(spl(lstar)) / L10)])
    with open(RES / "vacuum_prefactor.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "gravity", "log10_rate_GeV4", "log10_rate_saddle", "log10_rate_F1", "log10_P", "log10_tau_yr",
                    "log10_invR_peak_GeV", "S_peak", "log10_F_peak"])
        w.writerows(rows)
    with open(RES / "vacuum_prefactor_grid.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case", "log10_invR_GeV", "lambda", "xW", "xZ", "xt", "log10_higgs", "log10_gauge_goldstone",
                    "log10_top", "log10_F"])
        w.writerows(grid_rows)
    print("wrote results/vacuum_prefactor.csv and results/vacuum_prefactor_grid.csv (%.0f s)" % (time.time() - t0))


if __name__ == "__main__":
    main()
