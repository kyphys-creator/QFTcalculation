# Library of the heat-kernel checks deriv_inst_fhss.py, deriv_inst_klm.py, deriv_inst_vdv.py, deriv_inst_planewave.py (research note
# models/qcd, app:inst 「大きい質量の展開。」 and the step (10) checks of the m^-8 coefficient, A_6 of the BPST instanton).
#   fetch_arxiv(id): the LaTeX source of an arXiv paper in work/arxiv/<id>/src/ (downloaded from https://arxiv.org/e-print/<id> when
#     missing); the sources are data: they are only read and matched with regular expressions, never executed or committed;
#   exact heat-kernel coefficients for constant non-commuting potentials (any d) and the evaluation of the FHSS invariants on them;
#   the parser of the FHSS coefficients O_1..O_6 (Fliegner, Haberl, Schmidt, Schubert, hep-th/9707189);
#   exact BPST data: Taylor series of A_mu, covariant derivatives of G_{mu nu} at rational points, exact contractions (modular arithmetic
#     + CRT), the FHSS invariants on BPST, the exact r-integration of P(u)/(1+u)^m;
#   the plane-wave (symbol) method for the pointwise tr a_n (floating point, and modulo a prime);
#   the worker functions of multiprocessing.Pool (rank test of O_n, plane-wave runs), importable also when the scripts run cell by cell.
# The code is that of the investigation of 2026-10-16 (reorganized into one module; the computations are unchanged).
import gzip
import io
import itertools
import math
import os
import re
import shutil
import tarfile
import urllib.request
from fractions import Fraction

import numpy as np

Fr = Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
ARXIV = os.path.join(HERE, "work", "arxiv")


# ======================================================================================================
# arXiv sources (data)
def fetch_arxiv(aid, url=None):
    """directory of the extracted LaTeX source of arXiv:aid, work/arxiv/<aid with / -> _>/src (eprint.bin downloaded when missing)"""
    d = os.path.join(ARXIV, aid.replace("/", "_"))
    src = os.path.join(d, "src")
    if os.path.isdir(src) and os.listdir(src):
        return src
    os.makedirs(d, exist_ok=True)
    raw = os.path.join(d, "eprint.bin")
    if not os.path.exists(raw):
        req = urllib.request.Request(url or f"https://arxiv.org/e-print/{aid}", headers={"User-Agent": "deriv_inst_hk_lib.py (research-note check)"})
        with urllib.request.urlopen(req, timeout=120) as r, open(raw + ".part", "wb") as f:
            shutil.copyfileobj(r, f)
        os.replace(raw + ".part", raw)
    data = open(raw, "rb").read()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    tmp = src + ".part"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    if tarfile.is_tarfile(io.BytesIO(data)):
        with tarfile.open(fileobj=io.BytesIO(data)) as t:
            t.extractall(tmp, filter="data")
    else:                                      # a single gzipped LaTeX file
        open(os.path.join(tmp, aid.split("/")[-1] + ".tex"), "wb").write(data)
    os.replace(tmp, src)
    return src


def read_tex(aid, name):
    """text of the file name of the source of arXiv:aid (latin-1)"""
    return open(os.path.join(fetch_arxiv(aid), name), encoding="latin-1").read()


def load_fhss():
    """FHSS O_1..O_6 parsed from hep-th/9707189 (HD-THEP-97-24.tex): ({n: terms}, summary lines); every index appears twice in a term"""
    tex = read_tex("hep-th/9707189", "HD-THEP-97-24.tex")
    bl = fhss_blocks(tex)
    res, lines = {}, []
    for n in sorted(bl):
        terms = fhss_parse(bl[n])
        for t in terms:  # every index appears exactly twice in a term
            idx = "".join(f[1] for f in t["factors"])
            for c in set(idx):
                assert idx.count(c) == 2, (n, t)
        res[n] = terms
        nf = [t for t in terms if all(f[0] == "F" for f in t["factors"])]
        lines.append(f"O_{n}: {len(terms)} terms, {len(nf)} without V; LaTeX round trip identical: {fhss_roundtrip(bl[n], terms)}")
    return res, lines


# ======================================================================================================
# Constant non-commuting gauge potentials: exact heat-kernel coefficients and evaluation of
# FHSS invariants, in d dimensions (d = len(A)).
#
# Conventions (as in the QCD note): D_mu = d_mu - i A_mu, -D^2 = (p - A)^2 on e^{ipx} v for
# constant matrices A_mu.  K(x,x;t) = int d^dp/(2pi)^d tr exp(-t (p-A)^2) = (4 pi t)^{-d/2} sum_n t^n tr a_n.
# Omega_{mu nu} = [D_mu, D_nu] = -[A_mu, A_nu];  adjoint D_k X = -i [A_k, X].
# FHSS (hep-th/9707189): D = d + i A' (A' = -A), [D_mu, D_nu] = i F_{mu nu}  =>  F^FHSS = -i Omega,
# F^FHSS_{k l m ...} = D_k D_l ... F^FHSS.
#
# tr a_n (exact) = sum_{k=n}^{2n} (-1)^k/k! < tr Y^k >_{t^n},  Y = -2 p.A + A.A, with the Gaussian
# moments <p^alpha> = prod (alpha_mu - 1)!!/(2t)^{alpha_mu/2}.

def dfact(n):
    return 1 if n <= 0 else n * dfact(n - 2)


def exact_tr_a(A, nmax):
    """tr a_n, n = 0..nmax, for constant matrices A[mu] (mu = 0..d-1).  Polynomial in p with matrix coeffs."""
    N = A[0].shape[0]
    d = len(A)
    S = sum(A[m] @ A[m] for m in range(d))
    z = (0,) * d
    Y = {z: S}
    for m in range(d):
        e = [0] * d
        e[m] = 1
        Y[tuple(e)] = -2 * A[m]
    res = [0j] * (nmax + 1)
    res[0] = complex(N)
    P = {z: np.eye(N, dtype=complex)}
    for k in range(1, 2 * nmax + 1):
        Q = {}
        for a, M in P.items():
            for b, Mb in Y.items():
                c = tuple(x + y for x, y in zip(a, b))
                if sum(c) > 2 * nmax:
                    continue
                Q[c] = Q.get(c, 0) + M @ Mb
        P = Q
        for alpha, M in P.items():
            if any(x % 2 for x in alpha):
                continue
            n = k - sum(alpha) // 2
            if 1 <= n <= nmax:
                w = 1.0
                for x in alpha:
                    w *= dfact(x - 1) / 2 ** (x // 2)
                res[n] += (-1) ** k / math.factorial(k) * w * np.trace(M)
    return res


def fhss_tensors(A, maxrank):
    """F^FHSS with derivatives: dict rank -> array (d,)*rank + (N,N); rank 2 = F_{mn}, rank 3 = D_k F_{mn}, ..."""
    N = A[0].shape[0]
    d = len(A)
    F = np.zeros((d, d, N, N), dtype=complex)
    for m in range(d):
        for n in range(d):
            F[m, n] = -1j * (-(A[m] @ A[n] - A[n] @ A[m]))
    T = {2: F}
    for r in range(3, maxrank + 1):
        prev = T[r - 1]
        new = np.zeros((d,) * r + (N, N), dtype=complex)
        for k in range(d):
            new[k] = -1j * (np.einsum("ab,...bc->...ac", A[k], prev) - np.einsum("...ab,bc->...ac", prev, A[k]))
        T[r] = new
    return T


def term_einsum(factors):
    nf = len(factors)
    mats = "ABCDEFGHIJ"
    return ",".join(idx + mats[i] + mats[(i + 1) % nf] for i, (typ, idx) in enumerate(factors)) + "->"


class FHSSEval:
    """Evaluate the V-free part of O_n term by term on constant fields."""

    def __init__(self, terms):
        self.terms = [t for t in terms if all(f[0] == "F" for f in t["factors"])]
        self.subs = [term_einsum(t["factors"]) for t in self.terms]
        self.coef = [Fraction(t["num"], t["den"]) * (1j if t["imag"] else 1) for t in self.terms]
        self.paths = {}

    def values(self, T):
        out = []
        for i, t in enumerate(self.terms):
            ops = [T[len(f[1])] for f in t["factors"]]
            key = (i, ops[0].shape[0])
            if key not in self.paths:
                self.paths[key] = np.einsum_path(self.subs[i], *ops, optimize="optimal")[0]
            out.append(np.einsum(self.subs[i], *ops, optimize=self.paths[key]))
        return np.array(out)

    def total(self, T):
        return sum(complex(c) * x for c, x in zip(self.coef, self.values(T)))


def random_A(N, rng, herm=True, scale=1.0, d=4):
    A = []
    for _ in range(d):
        M = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
        if herm:
            M = (M + M.conj().T) / 2
        A.append(scale * M)
    return A


# ======================================================================================================
# Parse the inverse-mass coefficients O_1..O_6 of Fliegner-Haberl-Schmidt-Schubert
# (hep-th/9707189, Annals Phys. 264 (1998) 51) from the arXiv LaTeX source.
#
# Each term: {"num": int, "den": int, "imag": bool, "factors": [["F", "klmn"], ["V", ""], ...]}
# Index letters: k=kappa l=lambda m=mu n=nu r=rho s=sigma t=tau.
# F with indices i1..in (n>=2): D_{i1}...D_{i(n-2)} F_{i(n-1) in}  (FHSS: F_{klmn} = D_k D_l F_{mn});
# V with indices: D..D V.  The source file is treated as data only (read, regex-parsed).

GREEK = {"kappa": "k", "lambda": "l", "mu": "m", "nu": "n", "rho": "r", "sigma": "s", "tau": "t"}


def fhss_blocks(tex):
    """Return {n: latex string of O_n} for the eqnarray blocks starting with 'O_n &=&'."""
    out = {}
    for m in re.finditer(r"O_(\d)\s*&=&(.*?)\\ear", tex, re.S):
        out[int(m.group(1))] = m.group(2)
    # O_6 (Appendix C) continues in a second eqnarray after a \newpage: append it
    i6 = tex.index("O_6 &=&")
    e1 = tex.index("\\ear", i6)
    b2 = tex.index("\\bear", e1)
    between = tex[e1 + 4:b2].strip()
    assert between == "\\newpage", repr(between)
    e2 = tex.index("\\ear", b2)
    out[6] = out[6] + " " + tex[b2 + 5:e2]
    assert "Appendix C" in tex[i6 - 300:i6] and "\\bear" not in tex[b2 + 5:e2]
    return out


def fhss_clean(body):
    body = body.replace("\\nonumber", " ").replace("\\\\", " ").replace("&&", " ").replace("\\;", " ")
    body = body.replace("\\mbox{i}", " I ")
    for g, c in GREEK.items():
        body = body.replace("\\" + g, c)
    body = re.sub(r"\s+", " ", body)
    return body.strip()


_F = r"(?:(?:V(?:\^\d+)?(?:_\{[a-z ]*\})?)|(?:F_\{[a-z ]*\}))"
TERM = re.compile(r"([+-])?\s*(?:\\frac\{(\d+)\}\{(\d+)\}|(\d+))?\s*(I)?\s*(" + _F + r"(?:\s*" + _F + r")*)")
FACT = re.compile(r"(V)(?:\^(\d+))?(?:_\{([a-z ]*)\})?|F_\{([a-z ]*)\}")


def fhss_parse(body):
    s = fhss_clean(body)
    terms = []
    pos = 0
    while pos < len(s):
        m = TERM.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError("cannot parse at: " + s[pos:pos + 80])
        sign = -1 if m.group(1) == "-" else 1
        if m.group(2):
            num, den = int(m.group(2)), int(m.group(3))
        elif m.group(4):
            num, den = int(m.group(4)), 1
        else:
            num, den = 1, 1
        facs = []
        for f in FACT.finditer(m.group(6)):
            if f.group(1):
                p = int(f.group(2)) if f.group(2) else 1
                idx = (f.group(3) or "").replace(" ", "")
                if p > 1 and idx:
                    raise ValueError("V^p with indices")
                facs += [["V", idx]] * p
            else:
                facs.append(["F", f.group(4).replace(" ", "")])
        terms.append({"num": sign * num, "den": den, "imag": bool(m.group(5)), "factors": facs})
        pos = m.end()
        while pos < len(s) and s[pos] == " ":
            pos += 1
    return terms


def fhss_roundtrip(body, terms):
    """Regenerate the cleaned token string from the parsed terms (check of the transcription)."""
    s = fhss_clean(body).replace(" ", "")
    out = []
    for i, t in enumerate(terms):
        sg = "-" if t["num"] < 0 else ("+" if i > 0 or s.startswith("+") else "")
        a, b = abs(t["num"]), t["den"]
        c = "" if (a, b) == (1, 1) else (str(a) if b == 1 else "\\frac{%d}{%d}" % (a, b))
        f = ""
        k = 0
        fs = t["factors"]
        while k < len(fs):
            if fs[k] == ["V", ""]:
                p = 1
                while k + p < len(fs) and fs[k + p] == ["V", ""]:
                    p += 1
                f += "V" + ("^%d" % p if p > 1 else "")
                k += p
            else:
                f += fs[k][0] + ("_{%s}" % fs[k][1] if fs[k][1] else "")
                k += 1
        out.append(sg + c + ("I" if t["imag"] else "") + f)
    return "".join(out) == s


# ======================================================================================================
# Exact covariant derivatives of the BPST field strength at a rational point x0 (rho = 1, g = 1).
#
# A^a_mu(x) = 2 eta_{a mu nu} x_nu / (x^2 + 1),  A = A^a T^a,  D_mu = d_mu - i A_mu.
# Lie-algebra components (T^a = sigma^a/2 or (T^a)_{bc} = -i eps_{abc}):
#   G^c_{mu nu} = d_mu A^c_nu - d_nu A^c_mu + eps_{abc} A^a_mu A^b_nu,
#   (D_k X)^c   = d_k X^c + eps_{abc} A^a_k X^b.
# Taylor series in y around x0 (truncated, exact Fractions); D^j G at y = 0 for j = 0..jmax.
# Returned: dict rank -> object array (4,)*rank + (3,) with rank = j + 2;
# component [k1..kj, m, n, c] = (D_k1 ... D_kj G_{mn})^c (x0).
# Options ncov / outer_sign only serve to test hypotheses about the KLM evaluation.

EPS = np.zeros((3, 3, 3), dtype=int)
for a, b, c in itertools.permutations(range(3)):
    EPS[a, b, c] = int(np.sign(np.prod([b - a, c - a, c - b])))


def eta(a, m, n):
    """'t Hooft symbol eta_{a m n}, m,n = 0..3 with 3 the fourth direction; a = 0..2."""
    if m < 3 and n < 3:
        return int(EPS[a, m, n])
    if n == 3 and m < 3:
        return 1 if a == m else 0
    if m == 3 and n < 3:
        return -1 if a == n else 0
    return 0


def padd(p, q, s=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + s * v
        if r[k] == 0:
            del r[k]
    return r


def pmul(p, q, K):
    r = {}
    for a, va in p.items():
        da = sum(a)
        for b, vb in q.items():
            if da + sum(b) > K:
                continue
            c = (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])
            r[c] = r.get(c, 0) + va * vb
    return {k: v for k, v in r.items() if v != 0}


def pscale(p, s):
    return {k: v * s for k, v in p.items()} if s != 0 else {}


def pdiff(p, mu):
    r = {}
    for a, v in p.items():
        if a[mu] > 0:
            b = list(a)
            b[mu] -= 1
            r[tuple(b)] = v * a[mu]
    return r


def ptrunc(p, K):
    return {k: v for k, v in p.items() if sum(k) <= K}


def bpst_A_series(x0, K):
    """A^a_mu(x0 + y) as truncated series in y (exact): list [a][mu] of polys (dict exponent -> Fraction)."""
    x0 = [Fraction(v) for v in x0]
    c = 1 + sum(v * v for v in x0)
    w = {}
    for m in range(4):
        e = [0] * 4
        e[m] = 1
        if x0[m] != 0:
            w[tuple(e)] = 2 * x0[m] / c
        e[m] = 2
        w[tuple(e)] = Fraction(1) / c
    f = {(0, 0, 0, 0): Fraction(1)}
    term = {(0, 0, 0, 0): Fraction(1)}
    for k in range(1, K + 1):
        term = pmul(term, pscale(w, -1), K)
        f = padd(f, term)
    f = pscale(f, Fraction(1) / c)
    X = []
    for m in range(4):
        e = [0] * 4
        e[m] = 1
        p = {tuple(e): Fraction(1)}
        if x0[m] != 0:
            p[(0, 0, 0, 0)] = x0[m]
        X.append(p)
    A = [[None] * 4 for _ in range(3)]
    for a in range(3):
        for mu in range(4):
            s = {}
            for nu in range(4):
                e = eta(a, mu, nu)
                if e:
                    s = padd(s, pscale(X[nu], 2 * e))
            A[a][mu] = pmul(s, f, K)
    return A


def bpst_jets(x0, jmax, ncov=None, outer_sign=0):
    K = jmax + 1
    A = bpst_A_series(x0, K)

    def covd(X, k, deg, sgn=1):
        out = []
        for c in range(3):
            s = pdiff(X[c], k)
            for a in range(3):
                for b in range(3):
                    e = sgn * EPS[a, b, c]
                    if e:
                        s = padd(s, pscale(pmul(A[a][k], X[b], deg), e))
            out.append(ptrunc(s, deg))
        return out

    G = {}
    deg = K - 1
    for m in range(4):
        for n in range(4):
            comp = []
            for c in range(3):
                s = padd(pdiff(A[c][n], m), pdiff(A[c][m], n), -1)
                for a in range(3):
                    for b in range(3):
                        e = EPS[a, b, c]
                        if e:
                            s = padd(s, pscale(pmul(A[a][m], A[b][n], deg), e))
                comp.append(ptrunc(s, deg))
            G[(m, n)] = comp
    series = {2: G}
    for j in range(1, jmax + 1):
        deg = K - 1 - j
        new = {}
        for key, X in series[j + 1].items():
            for k in range(4):
                if ncov is None or j <= ncov:
                    new[(k,) + key] = covd(X, k, deg)
                elif outer_sign == -1:
                    new[(k,) + key] = covd(X, k, deg, sgn=-1)
                else:
                    new[(k,) + key] = [ptrunc(pdiff(X[c], k), deg) for c in range(3)]
        series[j + 2] = new
    out = {}
    for rank, d in series.items():
        arr = np.empty((4,) * rank + (3,), dtype=object)
        for key, X in d.items():
            for c in range(3):
                arr[key + (c,)] = X[c].get((0, 0, 0, 0), Fraction(0))
        out[rank] = arr
    return out


# ======================================================================================================
# Exact evaluation of trace/contraction networks of integer tensors by modular arithmetic + CRT.
#
# A network is a list of subscript strings (every index letter appears in exactly two operands: full
# contraction to a scalar) with operands drawn from a fixed set of integer tensors ('slots').  The value
# is computed mod several primes p < 2^20 with int64 numpy einsum (pairwise along an optimal path,
# reduced mod p after each step; every pairwise sum has < 2^20 terms, so no int64 overflow),
# reconstructed by CRT in the symmetric range and checked against a float64 evaluation.  The number of
# primes is set by a float upper bound (the same contraction of the absolute values).

def primes_below(start, n):
    out = []
    c = start if start % 2 else start - 1
    while len(out) < n:
        if all(c % q for q in range(3, int(c ** 0.5) + 1, 2)):
            out.append(c)
        c -= 2
    return out


PRIMES = primes_below((1 << 20) - 1, 40)


def pairwise(subs, arrs, path, red=None):
    ops = list(zip(subs, arrs))
    for grp in path:
        group = [ops[i] for i in grp]
        for k in sorted(grp, reverse=True):
            del ops[k]
        s1, a1 = group[0]
        for s2, a2 in group[1:]:
            keep = "".join(ch for ch in s1 + s2 if (s1 + s2).count(ch) == 1)
            a1 = np.einsum(f"{s1},{s2}->{keep}", a1, a2)
            if red is not None:
                a1 = a1 % red
            s1 = keep
        ops.append((s1, a1))
    assert len(ops) == 1 and ops[0][0] == ""
    return ops[0][1]


def get_path(subs, shapes):
    dummy = [np.zeros(s) for s in shapes]
    p = np.einsum_path(",".join(subs) + "->", *dummy, optimize="optimal")[0]
    return [tuple(x) for x in p[1:]]


def to_int_scaled(arr):
    """Fraction object array -> (D, int object array) with arr = int_arr / D."""
    D = 1
    for v in arr.flat:
        D = D * v.denominator // math.gcd(D, v.denominator)
    ia = np.empty(arr.shape, dtype=object)
    for idx, v in np.ndenumerate(arr):
        ia[idx] = int(v * D)
    return D, ia


class Slots:
    def __init__(self, int_tensors, nprimes=24):
        self.fl = {k: np.vectorize(float, otypes=[float])(a) for k, a in int_tensors.items()}
        self.ab = {k: np.abs(a) for k, a in self.fl.items()}
        self.ps = PRIMES[:nprimes]
        self.res = {p: {k: np.vectorize(lambda v, p=p: v % p, otypes=[np.int64])(a) for k, a in int_tensors.items()}
                    for p in self.ps}
        self.paths = {}

    def contract(self, subs, keys):
        sig = (tuple(subs), tuple(keys))
        if sig not in self.paths:
            self.paths[sig] = get_path(subs, [self.fl[k].shape for k in keys])
        path = self.paths[sig]
        bound = float(pairwise(subs, [self.ab[k] for k in keys], path))
        fval = float(pairwise(subs, [self.fl[k] for k in keys], path))
        if bound == 0:
            return 0
        nbits = math.ceil(math.log2(bound + 1)) + 4
        npr = nbits // 19 + 2
        if npr > len(self.ps):
            raise RuntimeError("need more primes: %d" % npr)
        x, M = 0, 1
        for p in self.ps[:npr]:
            r = int(pairwise(subs, [self.res[p][k] for k in keys], path, red=p)) % p
            t = ((r - x) * pow(M, -1, p)) % p
            x += M * t
            M *= p
        if x > M // 2:
            x -= M
        assert abs(x - fval) <= 1e-8 * bound + 1e-6, (x, fval, bound)
        return x


# ======================================================================================================
# Exact BPST densities of the FHSS basis invariants (V = 0) at rational points x0.
#
# term value = (i if 'imag') * tr( prod_j F^FHSS[...] )  [the FHSS rational coefficient is applied later],
# F^FHSS = -G (G the hermitian field strength of D = d - i A; see the first section).
# isospin 1/2: X = X^a sigma^a/2 = i R(X), R(X) = (1/2) X^a L(e_a) (quaternion units e_a = -i sigma_a as
#              real 4x4 left-multiplication matrices), tr_2 = tr_4/2.
# isospin 1:   X = X^a T^a, (T^a)_{bc} = -i eps_{abc}: X = -i M(X), M_{bc} = X^a eps_{abc}.
# All arithmetic real and exact (integer scaling + modular contraction of the section above).

QM = np.zeros((4, 4, 4), dtype=int)  # basis_i * basis_j = sum_k QM[i,j,k] basis_k, basis (1,e1,e2,e3)
for i in range(4):
    QM[0, i, i] = 1
    QM[i, 0, i] = 1
for a in range(3):
    QM[a + 1, a + 1, 0] = -1
    for b in range(3):
        for c in range(3):
            if EPS[a, b, c]:
                QM[a + 1, b + 1, c + 1] = EPS[a, b, c]
LQ = np.array([[[Fraction(int(QM[a + 1, j, k])) for j in range(4)] for k in range(4)] for a in range(3)], dtype=object)
MTe = np.array([[[Fraction(int(EPS[a, b, c])) for c in range(3)] for b in range(3)] for a in range(3)], dtype=object)


def rep_tensors(jets, iso):
    out = {}
    for rank, G in jets.items():
        if iso == "1/2":
            out[rank] = np.tensordot(G, LQ, axes=([-1], [0])) * Fraction(1, 2)
        else:
            out[rank] = np.tensordot(G, MTe, axes=([-1], [0]))
    return out


class ExactTerms:
    def __init__(self, jets, iso):
        R = rep_tensors(jets, iso)
        self.iso = iso
        self.D = {}
        ints = {}
        for rank, arr in R.items():
            self.D[rank], ints[rank] = to_int_scaled(arr)
        self.slots = Slots(ints)

    def value(self, t):
        facs = t["factors"]
        k = len(facs)
        mats = "ABCDEFGHIJ"
        subs = [f[1] + mats[i] + mats[(i + 1) % k] for i, f in enumerate(facs)]
        keys = [len(f[1]) for f in facs]
        x = self.slots.contract(subs, keys)
        den = 1
        for kk in keys:
            den *= self.D[kk]
        # phase: i^imag * (-1)^k (F = -G) * (i^k [iso 1/2] or (-i)^k [iso 1])
        ph = complex((1 if not t["imag"] else 1j) * (-1) ** k * ((1j) ** k if self.iso == "1/2" else (-1j) ** k))
        assert abs(ph.imag) < 1e-12 and abs(abs(ph.real) - 1) < 1e-12, (t, ph)
        norm = Fraction(1, 2) if self.iso == "1/2" else Fraction(1)
        return int(round(ph.real)) * norm * Fraction(x, den)


# ======================================================================================================
# Exact r-dependence and integral over R^4 of the BPST densities of the FHSS basis invariants.
#
# Each density is fitted exactly as P(u)/(1+u)^(2n), u = r^2, by rational interpolation in u on the
# first deg+1 radii and verified on all remaining radii (deg raised until the check passes);
# int d^4x P(u)/(1+u)^m = pi^2 sum_j p_j B(j+2, m-j-2).
# A_n = (1/16 pi^2) int tr a_n,  tr a_n = (-1)^n/n! O_n  (FHSS).

def interp_poly(us, vs):
    n = len(us)
    coeffs = [Fr(0)] * n
    for i in range(n):
        basis = [Fr(1)]
        den = Fr(1)
        for j in range(n):
            if j == i:
                continue
            basis = [Fr(0)] + basis
            for k in range(len(basis) - 1):
                basis[k] -= us[j] * basis[k + 1]
            den *= us[i] - us[j]
        for k in range(n):
            coeffs[k] += vs[i] * basis[k] / den
    return coeffs


def peval(c, u):
    return sum(ck * u ** k for k, ck in enumerate(c))


def beta(a, b):
    return Fr(math.factorial(a - 1) * math.factorial(b - 1), math.factorial(a + b - 1))


def fit_integrate(radii, vals, m):
    us = [r * r for r in radii]
    ws = [v * (1 + u) ** m for v, u in zip(vals, us)]
    for deg in range(0, len(us) - 2):
        c = interp_poly(us[:deg + 1], ws[:deg + 1])
        if all(peval(c, u) == w for u, w in zip(us, ws)):
            while c and c[-1] == 0:
                c.pop()
            assert len(c) - 1 + 2 < m, "integral diverges"
            return c, sum(cj * beta(j + 2, m - j - 2) for j, cj in enumerate(c))
    raise RuntimeError("no exact fit")


# ======================================================================================================
# Pointwise heat-kernel coefficients tr a_n(x,x) of -D^2 by the plane-wave (symbol) method -- an
# independent route (no Fock-Schwinger gauge, no DeWitt recursion, no invariant basis).
#
# K(x,x;t) = int d^4p/(2pi)^4 tr[e^{-ipx} e^{t D^2} e^{ipx} 1](x),  e^{-ipx} (-D^2) e^{ipx} = p^2 - 2i p.D - D^2.
# With D_mu = d_mu + calA_mu, calA = -i A (antihermitian; real quaternion for isospin 1/2):
#   tr a_n(x) = sum_k (-1)^k/k! sum_{|alpha| = 2(k-n)} (-1)^{k-n} w(alpha) tr[(Y^k)_alpha 1](x),
#   Y = 2 p.D - D^2,  w(alpha) = prod_mu (alpha_mu - 1)!!/2^{alpha_mu/2}  (Gaussian moments, (4 pi t)^-2 out),
# where (Y^k)_alpha is the coefficient of p^alpha.  A term of Y^k with p-degree a contains 2k - a D's;
# tr a_n collects exactly 2n D's, so a partial product with 2k - a D's applied only needs its y-Taylor
# polynomial to degree 2 n_max - (2k - a).  Everything is a polynomial in y = x - x0 (numerical, float).

def monos(nvar, maxdeg):
    out = []
    for d in range(maxdeg + 1):
        for c in itertools.combinations_with_replacement(range(nvar), d):
            e = [0] * nvar
            for i in c:
                e[i] += 1
            out.append(tuple(e))
    return out


class YPoly:
    """Polynomials in y (4 variables), flattened over monomials sorted by degree, degree <= Dmax."""

    def __init__(self, Dmax):
        self.Dmax = Dmax
        self.mon = monos(4, Dmax)
        self.idx = {m: i for i, m in enumerate(self.mon)}
        self.deg = np.array([sum(m) for m in self.mon])
        self.count = [int((self.deg <= D).sum()) for D in range(Dmax + 1)]  # prefix length for degree <= D
        # derivative maps: d/dy_mu monomial j -> (target index, factor)
        self.dsrc, self.dtgt, self.dfac = [], [], []
        for mu in range(4):
            s, t, f = [], [], []
            for j, m in enumerate(self.mon):
                if m[mu] > 0:
                    mm = list(m)
                    mm[mu] -= 1
                    s.append(j)
                    t.append(self.idx[tuple(mm)])
                    f.append(m[mu])
            self.dsrc.append(np.array(s))
            self.dtgt.append(np.array(t))
            self.dfac.append(np.array(f, dtype=float))
        # pair table for products, sorted by target
        mon = np.array(self.mon)
        ia, ib = np.nonzero(self.deg[:, None] + self.deg[None, :] <= Dmax)
        tgt = np.array([self.idx[tuple(x)] for x in (mon[ia] + mon[ib])])
        order = np.lexsort((ib, tgt))
        self.ia, self.ib, self.ic = ia[order], ib[order], tgt[order]
        self.pdeg = self.deg[self.ia] + self.deg[self.ib]

    def diff(self, f, mu, D):
        """d/dy_mu of f (shape (P, n, N, N)) truncated to degree D."""
        n = self.count[D]
        out = np.zeros(f.shape[:1] + (n,) + f.shape[2:], dtype=f.dtype)
        s, t, fac = self.dsrc[mu], self.dtgt[mu], self.dfac[mu]
        sel = (t < n) & (s < f.shape[1])
        out[:, t[sel]] = f[:, s[sel]] * fac[sel][None, :, None, None]
        return out

    def lmul(self, A, f, D, maxpairs=3_000_000):
        """A(y) f(y) (A: (nA, N, N) coefficients; f: (P, nf, N, N)) truncated to degree D."""
        n = self.count[D]
        nf = f.shape[1]
        sel = (self.pdeg <= D) & (self.ib < nf) & (self.ia < A.shape[0])
        ia, ib, ic = self.ia[sel], self.ib[sel], self.ic[sel]
        out = np.zeros(f.shape[:1] + (n,) + f.shape[2:], dtype=f.dtype)
        if len(ia) == 0:
            return out
        st = np.flatnonzero(np.r_[True, ic[1:] != ic[:-1]])
        Aa = A[ia]
        P = f.shape[0]
        pc = max(1, maxpairs // len(ia))
        for p0 in range(0, P, pc):
            prods = np.matmul(Aa[None], f[p0:p0 + pc][:, ib])
            out[p0:p0 + pc][:, ic[st]] = np.add.reduceat(prods, st, axis=1)
        return out


def heat_coeffs(Acoef, N, nmax, yp=None):
    """Acoef[mu]: array (n_ymon(2 nmax), N, N) of Taylor coefficients of calA_mu(x0 + y) (flattened by yp).
    Returns tr a_n(x0) for n = 0..nmax (complex)."""
    Dmax = 2 * nmax
    if yp is None:
        yp = YPoly(Dmax)
    pm = {a: monos(4, a)[-math.comb(a + 3, 3):] for a in range(2 * nmax + 1)}  # homogeneous degree a
    pidx = {a: {m: i for i, m in enumerate(pm[a])} for a in pm}
    pup = {}  # p_mu * monomial: index map degree a -> a+1
    for a in range(2 * nmax):
        for mu in range(4):
            tg = []
            for m in pm[a]:
                mm = list(m)
                mm[mu] += 1
                tg.append(pidx[a + 1][tuple(mm)])
            pup[(a, mu)] = np.array(tg)
    w = {}
    for a in range(0, 2 * nmax + 1, 2):
        w[a] = np.array([math.prod(math.prod(range(x - 1, 0, -2)) if x > 1 else 1 for x in m) / 2 ** (a // 2)
                         if all(x % 2 == 0 for x in m) else 0.0 for m in pm[a]])

    def Dop(f, mu, D):
        return yp.diff(f, mu, D) + yp.lmul(Acoef[mu], f, D)

    res = np.zeros(nmax + 1, dtype=complex)
    res[0] = N
    # state: a -> array (n_pmon(a), n_ymon(D(a,k)), N, N);  D(a,k) = 2 nmax - (2k - a)
    I = np.zeros((1, yp.count[Dmax], N, N), dtype=complex)
    I[0, 0] = np.eye(N)
    state = {0: I}
    for k in range(1, 2 * nmax + 1):
        new = {}
        for a, f in state.items():
            Dcur = 2 * nmax - (2 * (k - 1) - a)
            # 2 p_mu D_mu: a -> a+1, degree Dcur - 1
            if Dcur - 1 >= 0:
                for mu in range(4):
                    g = 2 * Dop(f, mu, Dcur - 1)
                    tgt = new.setdefault(a + 1, np.zeros((len(pm[a + 1]), yp.count[Dcur - 1], N, N), dtype=complex))
                    tgt[pup[(a, mu)]] += g  # injective index map
            # -D_mu D_mu: a -> a, degree Dcur - 2
            if Dcur - 2 >= 0:
                acc = None
                for mu in range(4):
                    g = Dop(Dop(f, mu, Dcur - 1), mu, Dcur - 2)
                    acc = g if acc is None else acc + g
                if a in new:
                    new[a] = new[a] - acc
                else:
                    new[a] = -acc
        state = new
        for a, f in state.items():
            if a % 2:
                continue
            n = k - a // 2
            if 1 <= n <= nmax:
                val = np.einsum("p,pii->", w[a], f[:, 0])
                res[n] += (-1) ** k / math.factorial(k) * (-1) ** (a // 2) * val
    return res


# ======================================================================================================
# Exact (modular) version of the plane-wave method above, for isospin 1/2.
#
# Real representation: calA = -i A^a sigma^a/2 = (1/2) A^a e_a (quaternion units e_a = -i sigma_a),
# represented by real 4x4 left-multiplication matrices; the real 4-dim representation is two copies of the
# doublet, so tr_2 a_n = tr_4 a_n / 2.  All quantities are rational at rational x0; they are computed modulo a
# prime p < 2^30 with int64 numpy arithmetic (every product reduced mod p before summation).
# tr a_n(x0) = sum_k (-1)^k/k! sum_{|alpha| = 2(k-n)} (-1)^{k-n} w(alpha) tr[(Y^k)_alpha 1](x0),  Y = 2 p.D - D^2.

def modinv(x, p):
    return pow(int(x) % p, -1, p)


def frac_mod(fr, p):
    return (fr.numerator % p) * modinv(fr.denominator, p) % p


class YPolyMod(YPoly):
    def diff(self, f, mu, D, p):
        n = self.count[D]
        out = np.zeros(f.shape[:1] + (n,) + f.shape[2:], dtype=np.int64)
        s, t, fac = self.dsrc[mu], self.dtgt[mu], self.dfac[mu].astype(np.int64)
        sel = (t < n) & (s < f.shape[1])
        out[:, t[sel]] = (f[:, s[sel]] * fac[sel][None, :, None, None]) % p
        return out

    def lmul(self, A, f, D, p, maxpairs=1_500_000):
        n = self.count[D]
        nf = f.shape[1]
        sel = (self.pdeg <= D) & (self.ib < nf) & (self.ia < A.shape[0])
        ia, ib, ic = self.ia[sel], self.ib[sel], self.ic[sel]
        out = np.zeros(f.shape[:1] + (n,) + f.shape[2:], dtype=np.int64)
        if len(ia) == 0:
            return out
        st = np.flatnonzero(np.r_[True, ic[1:] != ic[:-1]])
        Aa = A[ia]
        P = f.shape[0]
        pc = max(1, maxpairs // len(ia))
        for p0 in range(0, P, pc):
            prods = np.matmul(Aa[None], f[p0:p0 + pc][:, ib]) % p  # entries < 4 p^2 < 2^62 before reduction
            out[p0:p0 + pc][:, ic[st]] = np.add.reduceat(prods, st, axis=1) % p
        return out


def heat_coeffs_mod(Acoef, N, nmax, yp, p):
    """Acoef[mu]: int64 array (n_ymon(2 nmax), N, N) of Taylor coefficients mod p.  Returns tr_N a_n mod p."""
    Dmax = 2 * nmax
    pm = {a: monos(4, a)[-math.comb(a + 3, 3):] for a in range(2 * nmax + 1)}
    pidx = {a: {m: i for i, m in enumerate(pm[a])} for a in pm}
    pup = {}
    for a in range(2 * nmax):
        for mu in range(4):
            tg = []
            for m in pm[a]:
                mm = list(m)
                mm[mu] += 1
                tg.append(pidx[a + 1][tuple(mm)])
            pup[(a, mu)] = np.array(tg)
    inv2 = modinv(2, p)
    w = {}
    for a in range(0, 2 * nmax + 1, 2):
        ww = []
        for m in pm[a]:
            if any(x % 2 for x in m):
                ww.append(0)
            else:
                num = math.prod(math.prod(range(x - 1, 0, -2)) if x > 1 else 1 for x in m)
                ww.append(num * pow(inv2, a // 2, p) % p)
        w[a] = np.array(ww, dtype=np.int64)

    def Dop(f, mu, D):
        return (yp.diff(f, mu, D, p) + yp.lmul(Acoef[mu], f, D, p)) % p

    res = [0] * (nmax + 1)
    res[0] = N % p
    I = np.zeros((1, yp.count[Dmax], N, N), dtype=np.int64)
    I[0, 0] = np.eye(N, dtype=np.int64)
    state = {0: I}
    for k in range(1, 2 * nmax + 1):
        new = {}
        for a, f in state.items():
            Dcur = 2 * nmax - (2 * (k - 1) - a)
            if Dcur - 1 >= 0:
                for mu in range(4):
                    g = (2 * Dop(f, mu, Dcur - 1)) % p
                    tgt = new.setdefault(a + 1, np.zeros((len(pm[a + 1]), yp.count[Dcur - 1], N, N), dtype=np.int64))
                    tgt[pup[(a, mu)]] = (tgt[pup[(a, mu)]] + g) % p
            if Dcur - 2 >= 0:
                acc = None
                for mu in range(4):
                    g = Dop(Dop(f, mu, Dcur - 1), mu, Dcur - 2)
                    acc = g if acc is None else (acc + g) % p
                new[a] = ((new[a] if a in new else 0) - acc) % p
        state = new
        for a, f in state.items():
            if a % 2:
                continue
            n = k - a // 2
            if 1 <= n <= nmax:
                tr = np.trace(f[:, 0], axis1=1, axis2=2) % p
                val = int((w[a] * tr % p).sum() % p)
                sgn = (-1) ** k * (-1) ** (a // 2)
                res[n] = (res[n] + sgn * val * modinv(math.factorial(k), p)) % p
    return res


# ======================================================================================================
# Worker functions of multiprocessing.Pool
_RANK = {}


def rank_init(terms, n, N, dim):
    """worker state of the rank test: the FHSS evaluator of O_n (V-free terms) on random constant gl(N) potentials in d = dim"""
    ev = FHSSEval(terms)
    _RANK.update(ev=ev, n=n, N=N, dim=dim, maxrank=max(len(f[1]) for t in ev.terms for f in t["factors"]))


def rank_work(seed):
    """(values of the basis invariants, (-1)^n n! tr a_n exact) on one random configuration"""
    n, N = _RANK["n"], _RANK["N"]
    rng = np.random.default_rng(seed)
    A = random_A(N, rng, herm=False, scale=1.0 / math.sqrt(N), d=_RANK["dim"])
    T = fhss_tensors(A, _RANK["maxrank"])
    return _RANK["ev"].values(T), exact_tr_a(A, n)[n] * (-1) ** n * math.factorial(n)


LQ_INT = [[[int(QM[a + 1, j, k]) for j in range(4)] for k in range(4)] for a in range(3)]  # L(e_a)_{kj}
_YP = {}


def pw_task(args):
    """BPST (rho = 1, isospin 1/2) tr_2 a_n(x0) mod p, n = 0..nmax, at x0 = (r,0,0,0) by the plane-wave method; returns (p, str(r), values)"""
    p, r, nmax = args
    if nmax not in _YP:
        _YP[nmax] = YPolyMod(2 * nmax)
    YP = _YP[nmax]
    A = bpst_A_series([r, 0, 0, 0], 2 * nmax)
    inv2 = modinv(2, p)
    L = np.array(LQ_INT, dtype=np.int64) % p
    Ac = []
    for mu in range(4):
        cm = np.zeros((YP.count[2 * nmax], 4, 4), dtype=np.int64)
        for a in range(3):
            for e, v in A[a][mu].items():
                cm[YP.idx[e]] = (cm[YP.idx[e]] + frac_mod(v, p) * inv2 % p * L[a]) % p
        Ac.append(cm)
    tr4 = heat_coeffs_mod(Ac, 4, nmax, YP, p)
    return p, str(r), [x * inv2 % p for x in tr4]
