"""Functional determinants around the Fubini bounce (research note models/sm, step (10)).

Units R = 1.  Operators of Laplace type in d = 4, O = -d^2 + E(x), split into O(4) partial waves.  A partial-wave block is a
set of channels i with free angular momenta k_i (free solutions r^k_i) and a matrix potential E_ij(r); the Gel'fand-Yaglom
ratio det O_block/det O_free is det T(infinity) with Psi = diag(r^k) T the matrix of regular solutions,
    T_i'' + (2 k_i + 3)/r T_i' = sum_j r^(k_j - k_i) E_ij(r) T_j,   T(0) = 1.
The first two Born orders in E (T = 1 + T1 + T2 + ...) give B1 = tr T1(inf), B2 = tr T2(inf) - tr(T1(inf)^2)/2; the sum over
partial waves of B1 + B2 is the first- and second-order Feynman diagram, replaced by its MS-bar value in dimensional
regularization (the massless tadpole Tr[G0 E] = 0 and -1/2 Tr[(G0 E)^2] from momentum space, A2 below).
"""
import math

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import zeta

K16 = 16 * math.pi ** 2


def gy_block(ks, E, rmax=None, born=True, rtol=1e-11, atol=1e-13):
    """ks: free angular momenta of the channels; E(r): n x n matrix.  Returns (ln det T, B1, B2) at r = rmax
    (default 4000 (1 + max k)).  The ODE system integrates T, T1, T2 (each n x n) in t = ln r."""
    ks = np.asarray(ks, dtype=float)
    n = len(ks)
    rmax = rmax or (1e6 if ks.min() == 0 else 4000.0 * (1 + ks.max()))     # the l = 0 tail approaches like ln r/r^2
    r0 = 1e-4 / (1 + ks.max())
    dk = ks[None, :] - ks[:, None]                      # k_j - k_i

    def Et(r):
        return np.power(r, dk) * E(r)

    # variables: X (n x n) and P = r X' for X = T, T1, T2;  r d/dr (r X') = r^2 X'' + r X' = r^2 (Et X) - (2k+2) r X'
    def rhs(t, y):
        r = math.exp(t)
        Y = y.reshape(6 if born else 2, n, n)
        e = r * r * Et(r)
        c = (2 * ks + 2)[:, None]
        T, PT = Y[0], Y[1]
        out = [PT, e @ T - c * PT]
        if born:
            T1, P1, T2, P2 = Y[2], Y[3], Y[4], Y[5]
            out += [P1, e - c * P1, P2, e @ T1 - c * P2]
        return np.concatenate([o.ravel() for o in out])

    I = np.eye(n)
    Z = np.zeros((n, n))
    y0 = [I, Z] + ([Z, Z, Z, Z] if born else [])
    sol = solve_ivp(rhs, (math.log(r0), math.log(rmax)), np.concatenate([a.ravel() for a in y0]), method="DOP853",
                    rtol=rtol, atol=atol)
    Y = sol.y[:, -1].reshape(6 if born else 2, n, n)
    sign, ld = np.linalg.slogdet(Y[0])
    out = [ld if sign > 0 else complex(ld, math.pi)]
    if born:
        T1, T2 = Y[2], Y[4]
        out += [float(np.trace(T1)), float(np.trace(T2) - 0.5 * np.trace(T1 @ T1))]
    return tuple(out)


def tail_sum(w, lfit, ks=(2, 3, 4, 5)):
    """sum_{l >= 0} w_l with the tail beyond the data fitted to sum_k c_k (l+1)^-k on l in lfit"""
    w = np.asarray(w)
    l = np.arange(lfit[0], lfit[1] + 1)
    M = np.array([[(x + 1.0) ** (-k) for k in ks] for x in l])
    c = np.linalg.lstsq(M, w[lfit[0]: lfit[1] + 1], rcond=None)[0]
    return float(np.sum(w[: lfit[1] + 1])) + sum(ck * zeta(k, lfit[1] + 2) for ck, k in zip(c, ks)), c


def A2_from(trEE, mu=1.0, pmax=200.0):
    """MS-bar second-order term -1/2 int d^4p/(2pi)^4 trEE(p) (2 - ln(p^2/mu^2))/(16 pi^2), trEE(p) = tr[E~(p) E~(-p)]"""
    f = lambda p: p ** 3 * trEE(p) * (2 - math.log(p * p / mu ** 2))
    val = quad(f, 0, 1, limit=400)[0] + quad(f, 1, pmax, limit=800)[0]
    return -0.5 * 2 * math.pi ** 2 / (2 * math.pi) ** 4 * val / K16


# ---- the sectors of the SM around the Fubini bounce h = A/(1 + r^2), A^2 = 8/|lambda| (R = 1) ----
def fourier_hb(p):    # 4d Fourier transform of 1/(1+r^2): 4 pi^2 K_1(p)/p
    from scipy.special import k1
    return 4 * math.pi ** 2 * k1(p) / p


def fourier_hb2(p):   # of 1/(1+r^2)^2: 2 pi^2 K_0(p)
    from scipy.special import k0
    return 2 * math.pi ** 2 * k0(p)


def ag_blocks(xV, l):
    """background Feynman gauge, one real massive vector with its Goldstone, coupling e with xV = e^2/|lambda|:
    U_V = 8 xV/(1+r^2)^2, U_G = -8/(1+r^2)^2 (lambda h^2), mixing 2 e h' = -4 sqrt(8 xV) r/(1+r^2)^2 between the Goldstone
    and the radial vector component.  Returns [(degeneracy, ks, E)] for the scalar-harmonic level l: the coupled
    (+, -, G) block (degeneracy (l+1)^2; (+, G) for l = 0) and the transverse vectors at Cartesian degree n = l (l >= 1,
    degeneracy 2 l (l+2))."""
    UV = lambda r: 8 * xV / (1 + r * r) ** 2
    UG = lambda r: -8.0 / (1 + r * r) ** 2
    mix = lambda r: -4 * math.sqrt(8 * xV) * r / (1 + r * r) ** 2
    out = []
    if l == 0:
        E = lambda r: np.array([[UV(r), mix(r)], [mix(r), UG(r) + UV(r)]])
        out.append(((l + 1) ** 2, [1, 0], E))
    else:
        a, b = math.sqrt((l + 2) / (2 * l + 2)), math.sqrt(l / (2 * l + 2))
        E = lambda r, a=a, b=b: np.array([[UV(r), 0.0, a * mix(r)], [0.0, UV(r), b * mix(r)],
                                          [a * mix(r), b * mix(r), UG(r) + UV(r)]])
        out.append(((l + 1) ** 2, [l + 1, l - 1, l], E))
        out.append((2 * l * (l + 2), [l], lambda r: np.array([[UV(r)]])))
    return out


def ag_trEE(xV, p):
    """tr[E~(p) E~(-p)] of the 5 x 5 (4 vector components + Goldstone) potential, with the 4 of the vector trace"""
    uv = 8 * xV * fourier_hb2(p)
    ug = -8 * fourier_hb2(p)
    e2A2 = 8 * xV                     # e^2 A^2
    return 4 * uv ** 2 + (ug + uv) ** 2 + 8 * e2A2 * p * p * fourier_hb(p) ** 2


def top_blocks(xt, k):
    """the squared Dirac operator -d^2 + m^2 + gamma.dm, m = (y/sqrt 2) h = 2 sqrt(xt)/(1+r^2), xt = y^2/|lambda|: for each
    k >= 0 two 2 x 2 channels (L_k, R_{k+1}) and (R_k, L_{k+1}) of degeneracy (k+1)(k+2) each"""
    m = lambda r: 2 * math.sqrt(xt) / (1 + r * r)
    dm = lambda r: -4 * math.sqrt(xt) * r / (1 + r * r) ** 2
    E = lambda r: np.array([[m(r) ** 2, dm(r)], [dm(r), m(r) ** 2]])
    return [(2 * (k + 1) * (k + 2), [k, k + 1], E)]


def top_trEE(xt, p):
    """tr over the 4 Dirac components: 4 |FT(m^2)|^2 + 4 p^2 |FT(m)|^2"""
    m2 = 4 * xt * fourier_hb2(p)
    m1 = 2 * math.sqrt(xt) * fourier_hb(p)
    return 4 * m2 ** 2 + 4 * p * p * m1 ** 2


def sector_sum(blocks, lmax, special=None, fit=None):
    """sum_l sum_blocks deg [ln det T - B1 - B2]; special: {l: replacement of the summed term} (zero modes)"""
    w = []
    for l in range(lmax + 1):
        if special and l in special:
            w.append(special[l])
            continue
        tot = 0.0
        for deg, ks, E in blocks(l):
            ld, b1, b2 = gy_block(ks, E)
            if isinstance(ld, complex):
                raise ValueError("negative determinant in block l = %d" % l)
            tot += deg * (ld - b1 - b2)
        w.append(tot)
    S, c = tail_sum(w, fit or (lmax // 3, lmax))
    return S, w, c


def higgs_lndet(lmax=200):
    """MS-bar ln|det' O_h/det O_0| (mu = 1/R) with the zero modes replaced by the collective-coordinate normalization:
    returns (value, pieces).  O_h = -d^2 - 24/(1+r^2)^2; for l = 0 and 1 the ratio is D0 = 1/(2 pi A^2) and D1 = 1/(4 pi A^2)
    per mode, i.e. the zero-mode factors sqrt(2 pi) A (dilatation) and 2 sqrt(pi) A (each translation) are written as
    D^(-1/2); the A-dependence is kept outside: here A = 1 and the caller adds -1/2 (5 ln(1/A^2)) = 5 ln A."""
    U = lambda r: np.array([[-24.0 / (1 + r * r) ** 2]])
    b0 = gy_block([0], U)
    b1 = gy_block([1], U)
    D0, D1 = 1 / (2 * math.pi), 1 / (4 * math.pi)
    special = {0: math.log(D0) - b0[1] - b0[2], 1: 4 * (math.log(D1) - b1[1] - b1[2])}
    S, w, c = sector_sum(lambda l: [((l + 1) ** 2, [l], U)], lmax, special)
    A2 = A2_from(lambda p: (24 * fourier_hb2(p)) ** 2)
    return S + A2, {"sum": S, "A2": A2, "tail": c}


# ---- massive (IR-regularized) versions for threshold modes: matrix blocks ----
def _free_massive(k, m, r):
    """regular free solution of -d^2 + k(k+2)/r^2 + m^2, normalized to r^k at r -> 0, and r d/dr ln of it"""
    from scipy.special import ive
    x = m * r
    if x < 1e-8:
        return r ** k, k
    lnphi = math.lgamma(k + 2) + (k + 1) * math.log(2 / m) + math.log(ive(k + 1, x)) + x - math.log(r)
    dln = x * ive(k + 2, x) / ive(k + 1, x) + k          # r phi'/phi = x I_{k+2}/I_{k+1} + k
    return math.exp(lnphi) if lnphi < 700 else float("inf"), dln, lnphi


def gy_block_massive(ks, E, eps, rmax=None, rtol=1e-11, Minv=None):
    """ln det[(O + eps)/(O_0 + eps)] for a matrix block: Psi = diag(phi_k) T, phi_k the massive free solutions,
    T_i'' + (2 phi_i'/phi_i + 3/r) T_i' = sum_j (phi_j/phi_i) E_ij T_j, T(0) = 1.  With Minv, the block is
    O = M(-d^2 - 3/r d + k(k+2)/r^2) + E regulated by eps M (the non-minimal l = 0 block of background R_xi):
    the same equations with E -> Minv E."""
    if Minv is not None:
        E0, E = E, (lambda r: Minv @ E0(r))
    ks = np.asarray(ks, dtype=float)
    n = len(ks)
    m = math.sqrt(eps)
    rmax = rmax or 60.0 / m
    r0 = 1e-4 / (1 + ks.max())

    def rhs(t, y):
        r = math.exp(t)
        info = [_free_massive(k, m, r) for k in ks]
        lnp = np.array([i[2] if len(i) > 2 else k * math.log(r) for i, k in zip(info, ks)])
        dln = np.array([i[1] for i in info])
        ratio = np.exp(lnp[None, :] - lnp[:, None])           # phi_j/phi_i
        Y = y.reshape(2, n, n)
        T, P = Y[0], Y[1]
        e = r * r * (ratio * E(r))
        # P = r T': dP/dt = r^2 T'' + r T' = e T - (2 dln + 2) P
        return np.concatenate([P.ravel(), (e @ T - (2 * dln + 2)[:, None] * P).ravel()])

    y0 = np.concatenate([np.eye(n).ravel(), np.zeros(n * n)])
    sol = solve_ivp(rhs, (math.log(r0), math.log(rmax)), y0, method="DOP853", rtol=rtol, atol=1e-30)
    T = sol.y[: n * n, -1].reshape(n, n)
    sign, ld = np.linalg.slogdet(T)
    return ld, sign


def green_inner_matrix(ks, E, f, eps, rmax=None, n=8000, Minv=None):
    """<f, (O + eps)^-1 f> = int r^3 f.g dr for a matrix block (f(r) -> vector), with the matrix Green's function from the
    regular solutions (r^k e_j at 0) and the decaying ones (K_{k+1}(m r)/r e_j at rmax).  With Minv as in
    gy_block_massive: (O + eps M)^-1 f = (Minv O + eps)^-1 Minv f."""
    if Minv is not None:
        E0, E = E, (lambda r: Minv @ E0(r))
    from scipy.special import kve
    ks = np.asarray(ks, dtype=float)
    nc = len(ks)
    m = math.sqrt(eps)
    rmax = rmax or 40.0 / m
    r0 = 1e-4 / (1 + ks.max())
    rs = np.geomspace(r0, rmax, n)

    def ode(r, y):
        Y = y[: nc * nc].reshape(nc, nc)
        dY = y[nc * nc:].reshape(nc, nc)
        L = np.diag(ks * (ks + 2)) / r ** 2
        dd = -3 * dY / r + (L + E(r) + eps * np.eye(nc)) @ Y
        return np.concatenate([dY.ravel(), dd.ravel()])

    Yr0 = np.diag(r0 ** ks)
    dYr0 = np.diag([k * r0 ** (k - 1) if k > 0 else 0.0 for k in ks])
    s1 = solve_ivp(ode, (r0, rmax), np.concatenate([Yr0.ravel(), dYr0.ravel()]), t_eval=rs, method="DOP853", rtol=1e-11,
                   atol=1e-300)
    x = m * rmax
    Kd = np.array([kve(k + 1, x) / rmax for k in ks])
    dKd = np.array([(m * (-kve(k + 2, x) + (k + 1) / x * kve(k + 1, x)) - kve(k + 1, x) / rmax) / rmax for k in ks])
    s2 = solve_ivp(ode, (rmax, r0), np.concatenate([np.diag(Kd).ravel(), np.diag(dKd).ravel()]), t_eval=rs[::-1],
                   method="DOP853", rtol=1e-11, atol=1e-300)
    Yr = s1.y[: nc * nc].T.reshape(-1, nc, nc)
    dYr = s1.y[nc * nc:].T.reshape(-1, nc, nc)
    Yd = s2.y[: nc * nc][:, ::-1].T.reshape(-1, nc, nc)
    dYd = s2.y[nc * nc:][:, ::-1].T.reshape(-1, nc, nc)
    F = np.array([f(r) for r in rs])                       # (n, nc)
    Fs = F if Minv is None else F @ Minv.T                 # the source Minv f
    # G(r, s) = Yd(r) A(s) (r > s), Yr(r) B(s) (r < s);  Yd A - Yr B = 0,  Yd' A - Yr' B = -1/s^3
    A = np.zeros((len(rs), nc, nc))
    B = np.zeros((len(rs), nc, nc))
    for i, s in enumerate(rs):
        M = np.block([[Yd[i], -Yr[i]], [dYd[i], -dYr[i]]])
        rhsM = np.vstack([np.zeros((nc, nc)), -np.eye(nc) / s ** 3])
        X = np.linalg.solve(M, rhsM)
        A[i], B[i] = X[:nc], X[nc:]
    wA = np.einsum("ijk,ik->ij", A, Fs) * rs[:, None] ** 3
    wB = np.einsum("ijk,ik->ij", B, Fs) * rs[:, None] ** 3
    dr = np.diff(rs)
    cA = np.vstack([np.zeros(nc), np.cumsum(0.5 * dr[:, None] * (wA[1:] + wA[:-1]), axis=0)])
    cBrev = np.cumsum((0.5 * dr[:, None] * (wB[1:] + wB[:-1]))[::-1], axis=0)[::-1]
    cB = np.vstack([cBrev, np.zeros(nc)])
    g = np.einsum("ijk,ik->ij", Yd, cA) + np.einsum("ijk,ik->ij", Yr, cB)
    integrand = rs ** 3 * np.sum(F * g, axis=1)
    return float(np.sum(0.5 * dr * (integrand[1:] + integrand[:-1])))


def ghost_R0(xV):
    """the l = 0 Gel'fand-Yaglom ratio of the ghost operator -d^2 + 8 xV/(1+r^2)^2 (closed form, c = -xV)"""
    import cmath
    from scipy.special import loggamma
    kap = cmath.sqrt(1 - 8 * xV)
    return float(np.exp((loggamma(1) + loggamma(2) - loggamma(1.5 - kap / 2) - loggamma(1.5 + kap / 2)).real))


def ag_sector(xV, lmax=200):
    """ln of the factor of one real massive vector with its Goldstone and ghosts (background Feynman gauge, mu = 1/R,
    A = 1): -1/2 ln det'_AG + ln det_gh, with the l = 0 threshold (global rotation) mode of the AG block replaced by the
    collective coordinate on the orbit (factor sqrt(2 pi) A/R0_ghost per broken generator; the orbit volume 2 pi^2 is
    added by the caller, and ln A per generator).  Returns (value, pieces)."""
    blk0 = ag_blocks(xV, 0)[0]
    _, b1, b2 = gy_block(blk0[1], blk0[2])
    R0g = ghost_R0(xV)
    lnD0 = -math.log(2 * math.pi) + 2 * math.log(R0g)
    S, w, c = sector_sum(lambda l: ag_blocks(xV, l), lmax, special={0: lnD0 - b1 - b2})
    A2 = A2_from(lambda p: ag_trEE(xV, p)) + 2 * xV ** 2 / 3
    UVm = lambda r: np.array([[8 * xV / (1 + r * r) ** 2]])
    Sg, wg, cg = sector_sum(lambda l: [((l + 1) ** 2, [l], UVm)], lmax)
    A2g = A2_from(lambda p: (8 * xV * fourier_hb2(p)) ** 2)
    val = -0.5 * (S + A2) + Sg + A2g
    return val, {"AG_sum": S, "AG_A2": A2, "gh_sum": Sg, "gh_A2": A2g, "R0_ghost": R0g, "tail": c, "tail_gh": cg}


def top_sector(xt, lmax=200):
    """+ N_c/2 ln det(-d^2 + m^2 + gamma.dm) (MS-bar, mu = 1/R), N_c = 3"""
    S, w, c = sector_sum(lambda k: top_blocks(xt, k), lmax)
    A2 = A2_from(lambda p: top_trEE(xt, p))
    return 1.5 * (S + A2), {"sum": S, "A2": A2, "tail": c}


# ---- background R_xi with xi != 1: the non-minimal vector operator ----
def ag_blocks_xi(xV, l, xi):
    """one real vector with its Goldstone in background R_xi (F = d.A - xi e h G): the (S, L, G) block at scalar-harmonic
    level l >= 1 ((S, G) for l = 0) in the radial components a (x_mu/r Y), b (r d_mu Y/sqrt(l(l+2))), g (Y), written as
    O = -M d^2 - (C/r) d + D/r^2 + E(r) with constant M, C, D (derived symbolically in vacuum_gauge_check.py).  E holds
    e^2 h^2 on a, b, (lambda + xi e^2) h^2 on g and the mixing 2 e h' between a and g.  Returns (M, C, D, E, cols) with
    cols the free regular solutions (power p, vector v): r^(l-1) (l, L, 0) = grad(r^l Y), the solution with divergence
    r^l Y (power l + 1), and r^l for g.  The transverse modes (-Delta_l + e^2 h^2) and the ghost (-Delta_l + xi e^2 h^2)
    are scalar channels."""
    q = 1 - 1 / xi
    uv = lambda r: 8 * xV / (1 + r * r) ** 2
    ug = lambda r: -8.0 / (1 + r * r) ** 2
    mx = lambda r: -4 * math.sqrt(8 * xV) * r / (1 + r * r) ** 2
    if l == 0:
        M, C, D = np.diag([1 / xi, 1.0]), np.diag([3 / xi, 3.0]), np.diag([3 / xi, 0.0])
        E = lambda r: np.array([[uv(r), mx(r)], [mx(r), ug(r) + xi * uv(r)]])
        return M, C, D, E, [(1, np.array([1.0, 0.0])), (0, np.array([0.0, 1.0]))]
    L = math.sqrt(l * (l + 2))
    M = np.diag([1 / xi, 1.0, 1.0])
    C = np.array([[3 / xi, q * L, 0.0], [-q * L, 3.0, 0.0], [0.0, 0.0, 3.0]])
    D = np.array([[L * L + 3 / xi, -(1 + 1 / xi) * L, 0.0], [(1 - 3 / xi) * L, L * L / xi - 1, 0.0], [0.0, 0.0, L * L]])
    beta, gamma = np.linalg.solve(np.array([[l + 4.0, 2.0 * l], [2.0, 4.0 * l + 4]]), [1.0, q])   # A = beta x D + gamma r^2 dD
    cols = [(l - 1, np.array([float(l), L, 0.0])), (l + 1, np.array([beta + gamma * l, gamma * L, 0.0])),
            (l, np.array([0.0, 0.0, 1.0]))]
    E = lambda r: np.array([[uv(r), 0.0, mx(r)], [0.0, uv(r), 0.0], [mx(r), 0.0, ug(r) + xi * uv(r)]])
    return M, C, D, E, cols


def gy_block_general(M, C, D, E, cols, rmax, rtol=1e-11, atol=1e-13):
    """Gel'fand-Yaglom for O = -M d^2 - (C/r) d + D/r^2 + E(r): Psi = V diag(r^p) T with (p, v) the free regular columns,
    T'' = (R^-1 Et R) T - (R^-1 W R) T'/r, Et = V^-1 M^-1 E V, W = 2P + V^-1 M^-1 C V, R = diag(r^p), T(0) = 1, and the
    first two Born orders as in gy_block.  Returns (ln det T, B1, B2, sign) at rmax."""
    n = len(cols)
    p = np.array([c[0] for c in cols], dtype=float)
    V = np.array([c[1] for c in cols]).T
    Vi, Mi = np.linalg.inv(V), np.linalg.inv(M)
    for pj, v in cols:                       # the free columns solve the characteristic equation (relative test)
        scale = (abs(pj * (pj - 1)) * np.abs(M).max() + abs(pj) * np.abs(C).max() + np.abs(D).max()) * np.abs(v).max()
        assert np.abs((-pj * (pj - 1) * M - pj * C + D) @ v).max() < 1e-12 * scale, "not a free solution"
    W = 2 * np.diag(p) + Vi @ Mi @ C @ V
    dp = p[None, :] - p[:, None]
    r0 = 1e-4 / (2 + p.max())
    I = np.eye(n)

    def rhs(t, y):
        r = math.exp(t)
        Y = y.reshape(6, n, n)
        sc = np.power(r, dp)
        Et = sc * (Vi @ Mi @ (r * r * E(r)) @ V)
        Wt = sc * W - I                       # in t = ln r: X_tt = r^2 Et X - (W - 1) X_t
        srcs = (Y[0], I, Y[2])
        out = []
        for k in range(3):
            out += [Y[2 * k + 1], Et @ srcs[k] - Wt @ Y[2 * k + 1]]
        return np.concatenate([o.ravel() for o in out])
    Z = np.zeros((n, n))
    sol = solve_ivp(rhs, (math.log(r0), math.log(rmax)), np.concatenate([I.ravel()] + [Z.ravel()] * 5),
                    method="DOP853", rtol=rtol, atol=atol)
    Y = sol.y[:, -1].reshape(6, n, n)
    sign, ld = np.linalg.slogdet(Y[0])
    return ld, float(np.trace(Y[2])), float(np.trace(Y[4]) - 0.5 * np.trace(Y[2] @ Y[2])), sign


def A2_ag_xi(xV, xi, pmax=200.0):
    """MS-bar second-order terms -1/2 Tr[(K^-1 E)^2] (mu = 1/R) of the vector-Goldstone system with the R_xi propagator
    (delta - (1 - xi) k k/k^2)/k^2, and of the ghost.  The d-dimensional bubbles (in 1/(16 pi^2), a = 1 - xi, P = p^2):
    vector-vector 6 - 4a + a^2/2 - (4 - 2a + a^2) ln P, mixing P[(2 - a) - (1 - a/4) ln P], scalar 2 - ln P (derived in
    vacuum_gauge_check.py).  Returns (A2_AG, A2_ghost)."""
    a = 1 - xi

    def f_ag(p):
        Lp = math.log(p * p)
        uv, ug = 8 * xV * fourier_hb2(p), (-8 + 8 * xi * xV) * fourier_hb2(p)
        return p ** 3 * (uv * uv * (6 - 4 * a + a * a / 2 - (4 - 2 * a + a * a) * Lp) + ug * ug * (2 - Lp)
                         + 8 * 8 * xV * fourier_hb(p) ** 2 * p * p * ((2 - a) - (1 - a / 4) * Lp))

    def f_gh(p):
        return p ** 3 * (8 * xi * xV * fourier_hb2(p)) ** 2 * (2 - math.log(p * p))
    norm = -0.5 / (8 * math.pi ** 2) / K16
    integ = lambda f: quad(f, 0, 1, limit=400)[0] + quad(f, 1, pmax, limit=800)[0]
    return norm * integ(f_ag), norm * integ(f_gh)


def ag_sector_xi(xV, xi, lmax=120):
    """ag_sector in background R_xi: -1/2 ln det'_AG + ln det_gh (MS-bar, mu = 1/R, A = 1) with the l = 0 threshold
    mode as in ag_sector (factor sqrt(2 pi) A/theta_inf, theta_inf = R_0 of the ghost -d^2 + xi e^2 h^2)"""
    UVm = lambda r: np.array([[8 * xV / (1 + r * r) ** 2]])
    Ugh = lambda r: np.array([[8 * xi * xV / (1 + r * r) ** 2]])
    w, wg = [], []
    for l in range(lmax + 1):
        if l == 0:
            _, b1, b2, _ = gy_block_general(*ag_blocks_xi(xV, 0, xi), rmax=1e6)
            w.append(-math.log(2 * math.pi) + 2 * math.log(ghost_R0(xi * xV)) - b1 - b2)
        else:
            ld, b1, b2, _ = gy_block_general(*ag_blocks_xi(xV, l, xi), rmax=4000.0 * (l + 3))
            lt, t1, t2 = gy_block([l], UVm)
            w.append((l + 1) ** 2 * (ld - b1 - b2) + 2 * l * (l + 2) * (lt - t1 - t2))
        lg, g1, g2 = gy_block([l], Ugh)
        wg.append((l + 1) ** 2 * (lg - g1 - g2))
    S, Sg = tail_sum(w, (lmax // 3, lmax))[0], tail_sum(wg, (lmax // 3, lmax))[0]
    A2, A2g = A2_ag_xi(xV, xi)
    return -0.5 * (S + A2) + Sg + A2g

