# Library of deriv_inst_gy_hp.py and deriv_inst_gy_hp_fit.py (research note models/qcd, app:inst 「大きい質量の展開。」, step (10) checks):
# high-precision Gel'fand-Yaglom values of Gamma~(u) and of its u = m^2 derivatives for the isospin-1/2 scalar in the BPST background
# (rho = 1, regular gauge).  The C code deriv_inst_gy_hp.c integrates, per partial wave, the mass correction of inst_gylib.py together with its
# first three u-derivatives (sensitivity equations); build() compiles it into work/inst_gy_hp/.  Then:
#   waves(t, n), wave(...), group(t, n, m): the degeneracy-weighted d^j/du^j (j = 0..3) of the mass correction of the group l = n/2;
#   compute(t, m, L, kw, pool): all groups n = 0..2L;
#   gamma_derivs(d, t, m): G_j = d^j Gamma~/du^j from the partial-wave sums with a fitted large-l tail;
#   analyse(d, t, m, L): central value and the spread over tail-fit variants (the error estimate).
# Gamma~_t(u) = alpha(t) + lim_L [sum_{l<=L} d_l(u) - T u ln L] + T u (1 - 2 ln 2) + (T/2) u ln u   (T = T(t): 1/2, 2), so
#   G1 = lim[sum d' - T ln L] + T(1 - 2 ln 2) + (T/2)(ln u + 1),  G2 = sum d'' + T/(2u),  G3 = sum d''' - T/(2u^2).
# The functions are importable, so that the worker processes of multiprocessing.Pool can use them (also when run cell by cell).
import ctypes
import os
import subprocess
import sys

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work", "inst_gy_hp")
SRC = os.path.join(HERE, "deriv_inst_gy_hp.c")
LIBNAME = "libgyd.dylib" if sys.platform == "darwin" else "libgyd.so"
CFLAGS = ["-O3", "-ffp-contract=off", "-shared", "-fPIC"]      # no fused multiply-add: the same bits as the investigation's build


# ---------- build: DOP853 weights from scipy -> work/inst_gy_hp/dop853coef.h, then the shared library
def write_coef(path):
    """DOP853 8th-order Runge-Kutta weights, first 12 stages, from scipy"""
    from scipy.integrate._ivp import dop853_coefficients as d
    with open(path, 'w') as f:
        f.write('/* DOP853 8th-order weights (first 12 stages), from scipy.integrate._ivp.dop853_coefficients */\n')
        f.write('static const double RKC[12] = {' + ','.join(repr(float(x)) for x in d.C[:12]) + '};\n')
        f.write('static const double RKB[12] = {' + ','.join(repr(float(x)) for x in d.B) + '};\n')
        f.write('static const double RKA[12][12] = {' + ','.join('{' + ','.join(repr(float(x)) for x in row) + '}' for row in d.A[:12, :12]) + '};\n')


def build():
    """write the header and compile deriv_inst_gy_hp.c into work/inst_gy_hp/libgyd.dylib; returns the compiler command (relative paths)"""
    os.makedirs(WORK, exist_ok=True)
    write_coef(os.path.join(WORK, "dop853coef.h"))
    cmd = ["cc"] + CFLAGS + ["-I", os.path.join("work", "inst_gy_hp"), "-o", os.path.join("work", "inst_gy_hp", LIBNAME), "deriv_inst_gy_hp.c"]
    subprocess.run(cmd, cwd=HERE, check=True)
    return " ".join(cmd)


# ---------- the ctypes wrapper (loaded on first use)
_D = ctypes.c_double
_P = ctypes.POINTER(ctypes.c_double)
_LIB = None


def _lib():
    global _LIB
    if _LIB is None:
        _LIB = ctypes.CDLL(os.path.join(WORK, LIBNAME))
        _LIB.gy_wave.argtypes = [ctypes.c_int] + [_D]*7 + [_D]*5 + [ctypes.c_int, _P, _P, _P]
        _LIB.gy_wave.restype = ctypes.c_int
    return _LIB


DEF = dict(K=16.0, Z0=240.0, r0fac=1e-4, hfac=0.7, hmax=0.02, ngl=48)
_GL = {}


def _gl(n):
    if n not in _GL:
        s, w = np.polynomial.legendre.leggauss(n)
        _GL[n] = (np.ascontiguousarray((s + 1)/2), np.ascontiguousarray(w/2))
    return _GL[n]


def waves(t, n):
    """list of (degeneracy, type, l_origin, k, c, tt, A, B, C) for the group l = n/2"""
    l = n/2
    if t == 0.5:
        deg = (2*l + 1)*(2*l + 2)
        return [(deg, 0, l, l + 0.5, l + 0.75, 0.5, 0, 0, 0), (deg, 1, l + 0.5, l, -(l + 0.75), 0.5, 0, 0, 0)]
    A, B, C = (2*l + 2)*(2*l + 3)/2, (2*l + 1)*(2*l + 3), (2*l + 1)*(2*l + 2)/2
    out = [((2*l + 1)*(2*l + 3), 2, l, l + 1, 2*(l + 1), 1.0, A, B, C), ((2*l + 1)*(2*l + 3), 3, l + 1, l, -2*(l + 1), 1.0, 0, 0, 0)]
    if l >= 0.5:
        out.append(((2*l + 1)**2, 4, l, l, 0.0, 1.0, 0, 0, 0))
    return out


def wave(typ, lo, k, c, tt, A, B, C, m, K=None, Z0=None, r0fac=None, hfac=None, hmax=None, ngl=None):
    K = DEF["K"] if K is None else K; Z0 = DEF["Z0"] if Z0 is None else Z0
    r0fac = DEF["r0fac"] if r0fac is None else r0fac; hfac = DEF["hfac"] if hfac is None else hfac
    hmax = DEF["hmax"] if hmax is None else hmax; ngl = DEF["ngl"] if ngl is None else ngl
    nu = 2*k + 1
    R = max(K*nu, Z0)/m
    r0 = r0fac/(1 + k)
    s, w = _gl(ngl)
    out = np.zeros(15)
    _lib().gy_wave(typ, lo, k, c, tt, A, B, C, m*m, R, r0, hfac, hmax, ngl,
                   s.ctypes.data_as(_P), w.ctypes.data_as(_P), out.ctypes.data_as(_P))
    return out


def group(t, n, m, **kw):
    """degeneracy-weighted d^j/du^j (j = 0..3) of the mass correction of the group l = n/2; also returns total steps"""
    tot = np.zeros(4); steps = 0
    for deg, typ, lo, k, c, tt, A, B, C in waves(t, n):
        o = wave(typ, lo, k, c, tt, A, B, C, m, **kw)
        tot += deg*o[:4]; steps += o[12]
    return tot, steps


def group_task(args):
    t, n, m, kw = args
    return group(t, n, m, **kw)[0]


def compute(t, m, L, kw, pool):
    """d[n, j], n = 0..2L: the group values of all groups l = n/2 <= L (big n first for load balancing)"""
    tasks = [(t, n, m, kw) for n in range(2*L + 1)]
    order = sorted(range(len(tasks)), key=lambda i: -i)
    res = pool.map(group_task, [tasks[i] for i in order], chunksize=4)
    d = np.zeros((2*L + 1, 4))
    for i, r in zip(order, res): d[i] = r
    return d


def datafile(t, m, L, tag):
    return os.path.join(WORK, "data", f"d_t{t}_m{m:g}_L{L}_{tag}.npy")


# ---------- partial-wave sums with the large-l tail
TR = {0.5: 0.5, 1.0: 2.0}
ZP = mp.zeta(-1, derivative=1)
ALPHA = {0.5: float(-mp.mpf(5)/72 - mp.log(2)/6 - 2*ZP)}
ALPHA[1.0] = ALPHA[0.5]*4 + float(mp.log(2)) - 5/6


def tail_basis_sum(p, j, L):
    """sum over l = n/2 > L (n integer) of l^-p ln(l)^j, j = 0, 1, 2"""
    a = 2*L + 1; ln2 = mp.log(2)
    z0 = mp.zeta(p, a)
    if j == 0:
        return float(2**p*z0)
    z1 = -mp.zeta(p, a, derivative=1)          # sum n^-p ln n
    if j == 1:
        return float(2**p*(z1 - ln2*z0))
    z2 = mp.zeta(p, a, derivative=2)           # sum n^-p ln^2 n
    return float(2**p*(z2 - 2*ln2*z1 + ln2**2*z0))


BASES = {
    0: [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)],
    1: [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)],
    2: [(3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1), (6, 0), (6, 1)],
    3: [(3, 0), (4, 0), (4, 1), (5, 0), (5, 1), (6, 0), (6, 1), (7, 0)],
}

# t = 1: the u-derivatives of the group sums fall only like l^-2 (with logs), so the j = 2, 3 bases start at l^-2
BASES_T1 = {
    0: BASES[0], 1: BASES[1],
    2: [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)],
    3: [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)],
}


def partial_limit(d, j, T, u, L=None, lmin_frac=1/3, basis=None, nbasis=None):
    """lim_L [sum_{l<=L} d_l^(j) - (j<=1) * T u^(1-j) ln L] using the tail fit on [lmin_frac*L, L]"""
    Lmax = (len(d) - 1)//2
    L = Lmax if L is None else L
    ls = np.arange(2*L + 1)/2
    y = d[:2*L + 1, j].copy()
    S = y.sum()
    coef_ct = (T*u if j == 0 else T) if j <= 1 else 0.0
    sel = (ls >= lmin_frac*L) & (ls <= L)
    x = ls[sel]; yy = y[sel] - (coef_ct*(np.log(x) - np.log(x - 0.5)) if coef_ct else 0)
    B = basis if basis is not None else (BASES_T1[j] if T == 2.0 else BASES[j])
    if nbasis is not None: B = B[:nbasis]
    A = np.array([x**-p*np.log(x)**k for p, k in B]).T
    sc = np.abs(A).max(0)                      # scale columns for conditioning
    c, *_ = np.linalg.lstsq(A/sc, yy, rcond=None); c = c/sc
    rem = sum(ci*tail_basis_sum(p, k, L) for ci, (p, k) in zip(c, B))
    return S - (coef_ct*np.log(L) if coef_ct else 0.0) + rem, c


def gamma_derivs(d, t, m, **kw):
    """G0..G3 = d^j Gamma~/du^j"""
    T = TR[t]; u = m*m
    v = [partial_limit(d, j, T, u, **kw)[0] for j in range(4)]
    G0 = ALPHA[t] + v[0] + T*u*(1 - 2*np.log(2)) + T/2*u*np.log(u)
    G1 = v[1] + T*(1 - 2*np.log(2)) + T/2*(np.log(u) + 1)
    G2 = v[2] + T/(2*u)
    G3 = v[3] - T/(2*u*u)
    return np.array([G0, G1, G2, G3])


def analyse(d, t, m, L):
    """central value (L, window 1/4, 6 basis functions) and the largest deviation over the tail-fit variants
    (L, L/2 [t = 1/2] or 3L/4 [t = 1]; window 1/4, 1/3; 5..7 [t = 1/2] or 6..7 [t = 1] basis functions)"""
    central = gamma_derivs(d, t, m, L=L, lmin_frac=0.25, nbasis=6)
    vals = []
    for LL in ((L, L//2) if t == 0.5 else (L, (3*L)//4)):   # t = 1: slower tail, L/2 too short for the fit
        for fr in (0.25, 1/3):
            for nb in ((5, 6, 7) if t == 0.5 else (6, 7)):  # t = 1: 5 basis functions are too few
                vals.append(gamma_derivs(d, t, m, L=LL, lmin_frac=fr, nbasis=nb))
    vals = np.array(vals)
    return central, np.abs(vals - central).max(0)
