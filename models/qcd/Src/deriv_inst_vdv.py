# %% [markdown]
# # Appendix check: van de Ven's general a_2..a_6 (hep-th/9708152): a_6 as printed fails on constant potentials but agrees on BPST
#
# Research note models/qcd, derivations of the appendices (numpy).  app:inst 「大きい質量の展開。」, the step (10) checks
# (「文献との食い違い。」) and app:details: van de Ven's index-free heat-kernel coefficients, transcribed from the LaTeX source of
# hep-th/9708152 (sect. 6 and appendix C; downloaded into work/arxiv/ when missing; data only), potential X = 0, evaluated numerically from
# Fock-Schwinger-gauge Taylor data.  Notation: K = (4 pi t)^{-d/2} e^{-sigma/2t} sum_j a_j t^j/j!, so tr a_n(ours) = tr a_n(vdV)/n!.
# (a) term counts of a_1..a_6 (1, 2, 4, 10, 26, 75; X-free 0, 1, 2, 5, 12, 34);
# (b) random constant non-commuting potentials (N = 3, d = 4) against the exact heat kernel: a_2..a_5 agree to ~1e-13, a_6 does not
#     (relative difference ~2); consistency checks of the notation (vdV's box-moving identities, hermiticity of the hat terms);
# (c) least squares of the 34 X-free a_6 structures (plus one dagger variant) against the exact constant-field a_6 on 70 configurations:
#     the exact result is not in their span (relative residual 3e-4 >> 1e-12), so the printed a_6 cannot be repaired by changing coefficients;
# (d) on BPST (rho = 1, 12 radii; isospin 1/2 and 1): the pointwise vdV densities equal the DeWitt-recursion polynomials (isospin 1/2) and
#     A_2..A_6 agree with the exact values of deriv_inst_fhss.py to the float precision, because 27 of the 34 a_6 structures vanish on BPST
#     (they contain Z_1 ~ D_mu F_{mu nu} = 0).
# Reads the arXiv source (work/arxiv/hep-th_9708152/).  Writes nothing else; run_deriv_inst_a6_check.sh saves the printed output as
# results/deriv_inst_vdv.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python -I deriv_inst_vdv.py   (about 1 minute)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import itertools
import math
import os
import re
import sys
from fractions import Fraction
from fractions import Fraction as Fr
import numpy as np
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
sys.path.insert(0, HERE)
import deriv_inst_hk_lib as H


# %% [markdown]
# ## Fock-Schwinger-gauge Taylor data of a gauge field around a base point (numerical, dense polynomials)

# %%
# Fock-Schwinger-gauge Taylor data of a gauge field around a base point (numerical, dense polynomials).
#
# van de Ven convention: nabla = d + A with antihermitian A (A_vdV = -i A_ours), F = [nabla, nabla].
# Polynomials in y (4 variables) truncated at total degree K: arrays of shape (K+1,)*4 + (N,N).
# FS gauge: transporter Phi along the ray, (y.d) Phi = -(y.A(x0+y)) Phi, Phi(0) = 1;
# A'_mu = Phi^-1 A_mu Phi + Phi^-1 d_mu Phi  (then y.A' = 0).
# Z = d.A' + A'.A' (potential X = 0), Zd = Z^dagger = -d.A' + A'.A'.
DIM = 4


class PolyRing:
    def __init__(self, K, N, dtype=complex):
        self.K, self.N, self.dtype = K, N, dtype
        self.shape = (K + 1,) * DIM
        self.deg = np.indices(self.shape).sum(axis=0)
        self.mask = self.deg <= K
        self.monos = [tuple(a) for a in np.argwhere(self.mask)]
        mon = np.array(self.monos)
        idx = {m: i for i, m in enumerate(self.monos)}
        dg = mon.sum(axis=1)
        ia, ib = np.nonzero(dg[:, None] + dg[None, :] <= K)
        tgt = np.array([idx[tuple(x)] for x in (mon[ia] + mon[ib])])
        order = np.argsort(tgt, kind="stable")
        self.ia, self.ib, self.ic = ia[order], ib[order], tgt[order]
        self.pdeg = dg[self.ia] + dg[self.ib]
        self.mon = mon

    def zero(self):
        return np.zeros(self.shape + (self.N, self.N), dtype=self.dtype)

    def const(self, M):
        p = self.zero()
        p[(0,) * DIM] = M
        return p

    def trunc(self, p, K=None):
        K = self.K if K is None else K
        q = p.copy()
        q[self.deg > K] = 0
        return q

    def mul(self, P, R, K=None):
        K = self.K if K is None else K
        Pf = P[tuple(self.mon.T)]
        Rf = R[tuple(self.mon.T)]
        sel = self.pdeg <= K
        ia, ib, ic = self.ia[sel], self.ib[sel], self.ic[sel]
        prods = np.matmul(Pf[ia], Rf[ib])
        starts = np.flatnonzero(np.r_[True, ic[1:] != ic[:-1]])
        Q = self.zero()
        Q[tuple(self.mon[ic[starts]].T)] = np.add.reduceat(prods, starts, axis=0)
        return Q

    def diff(self, p, mu):
        q = self.zero()
        src = [slice(None)] * DIM
        dst = [slice(None)] * DIM
        src[mu] = slice(1, None)
        dst[mu] = slice(0, -1)
        fac = np.arange(1, self.K + 1).reshape([-1 if i == mu else 1 for i in range(DIM)] + [1, 1])
        q[tuple(dst)] = p[tuple(src)] * fac
        return q

    def ymul(self, p, mu):
        q = self.zero()
        src = [slice(None)] * DIM
        dst = [slice(None)] * DIM
        src[mu] = slice(0, -1)
        dst[mu] = slice(1, None)
        q[tuple(dst)] = p[tuple(src)]
        q[self.deg > self.K] = 0
        return q

    def lap(self, p):
        return sum(self.diff(self.diff(p, m), m) for m in range(DIM))

    def homog(self, p, k):
        q = np.zeros_like(p)
        q[self.deg == k] = p[self.deg == k]
        return q

    def taylor_tensor(self, p, s, l):
        """T_{mu1..mul} = d^l Box^s p (0): array (DIM,)*l + (N,N)."""
        q = p
        for _ in range(s):
            q = self.lap(q)
        T = np.zeros((DIM,) * l + (self.N, self.N), dtype=self.dtype)
        for idx in itertools.product(range(DIM), repeat=l):
            al = [0] * DIM
            for m in idx:
                al[m] += 1
            if sum(al) > self.K:
                raise ValueError("degree too high")
            T[idx] = q[tuple(al)] * np.prod([math.factorial(x) for x in al])
        return T


def fs_gauge(ring, Afun):
    """Afun: list of DIM polynomials A_mu(x0+y) (vdV convention).  Returns A'_mu, Z, Zd and checks."""
    K = ring.K
    yA = sum(ring.ymul(Afun[m], m) for m in range(DIM))
    I = np.eye(ring.N, dtype=ring.dtype)
    Phi = ring.const(I)
    for k in range(1, K + 1):
        Phi = Phi - ring.homog(ring.mul(yA, Phi, K=k), k) / k
    Phii = ring.const(I)
    for k in range(1, K + 1):
        Phii = Phii + ring.homog(ring.mul(Phii, yA, K=k), k) / k
    chk_inv = np.abs(ring.mul(Phii, Phi) - ring.const(I)).max()
    Ap = []
    for m in range(DIM):
        # Phi exact through degree K, d Phi through K-1: A' exact through K-1
        Ap.append(ring.trunc(ring.mul(Phii, ring.mul(Afun[m], Phi)) + ring.mul(Phii, ring.diff(Phi, m)), K - 1))
    chk_fs = np.abs(sum(ring.ymul(Ap[m], m) for m in range(DIM))).max()
    divA = sum(ring.diff(Ap[m], m) for m in range(DIM))
    AA = sum(ring.mul(Ap[m], Ap[m]) for m in range(DIM))
    # d.A' exact through K-2
    return Ap, ring.trunc(divA + AA, K - 2), ring.trunc(-divA + AA, K - 2), (chk_inv, chk_fs)


# %% [markdown]
# ## van de Ven's notation: parser of the LaTeX and evaluator

# %%
# van de Ven, 'Index-free heat kernel coefficients' (hep-th/9708152): parse a_1..a_5 (sect. 6) and a_6
# (appendix C) from the LaTeX source and evaluate them (potential X = 0) from Fock-Schwinger-gauge data.
#
# Notation (vdV): K = (4 pi t)^{-d/2} e^{-sigma/2t} sum_j a_j t^j / j!  (a_j^vdV = j! a_j^std).
# Z = X + d.A + A.A in FS gauge (X = 0 here); Z_j = d^j Z(0) (symmetric); Zd = Z^dagger = Z - 2 d.A;
# Y_j^nu = A^nu_{,mu1..muj}(0).  A group Z_{(j} ... Z_{k)} symmetrizes all its derivative indices and
# contracts them in pairs (= average over perfect matchings); Z_{(2j)} = Box^j Z(0); Z_{(2)(2} = box plus
# 2 group indices; an odd label Z_{(3)} = box plus one free index, contracted with the free index of the
# other odd factor/group (implemented by merging them into one group, equivalent when one side carries a
# single free index - the only case occurring).  Hats act on all group indices to their right:
#   HZ_n R = Z_n R + 2/(n+1) Y_{n+1}^nu d^sp_nu R,
# d^sp_nu converting one group index (of any factor to the right; g ways for a factor with g group indices)
# into the special index nu.  {F} = F + F^dagger if F is not self-adjoint: tr{F} = 2 Re tr F.
def extract_blocks(tex):
    i = tex.index(r"\bea\label{a1-a5}")
    blk = tex[i:tex.index(r"\ena", i)]
    out = {}
    for m in re.finditer(r"\\sa_(\d)\s*&=&(.*?)(?=\\sa_\d\s*&=&|$)", blk, re.S):
        out[int(m.group(1))] = m.group(2)
    j = tex.index(r"\section{$\sa_6$ in flat space}")
    j = tex.index(r"&&\sa_6 =", j)
    out[6] = tex[j + len(r"&&\sa_6 ="):tex.index(r"\ena", j)]
    return out


def clean(s):
    s = re.sub(r"%[^\n]*", "", s)
    for t in [r"\non", "&&", r"\\", r"\,", "\n"]:
        s = s.replace(t, " ")
    return re.sub(r"\s+", "", s)


FACTOR = re.compile(r"\\(HZ|Z)(?:_\{([^}]*)\}|_(\d))?(\\do)?(?:\^\{(\d+)\}|\^(\d)|\\sp\{(\d+)\})?")
COEF = re.compile(r"\\sfrac(\{\d+\}|\d)(\{\d+\}|\d)")


def parse_terms(body):
    s = clean(body)
    raw = [t for t in s.split("+") if t]
    terms = []
    for t in raw:
        coef = Fraction(1)
        m = COEF.match(t)
        if m:
            coef = Fraction(int(m.group(1).strip("{}")), int(m.group(2).strip("{}")))
            t = t[m.end():]
        curly = False
        if t.startswith(r"\{"):
            assert t.endswith(r"\}"), t
            curly = True
            t = t[2:-2]
        facs = []
        pos = 0
        while pos < len(t):
            m = FACTOR.match(t, pos)
            if not m:
                raise ValueError("cannot parse " + t[pos:])
            sub = m.group(2) if m.group(2) is not None else m.group(3)
            pw = m.group(5) or m.group(6) or m.group(7)
            facs += [dict(hat=m.group(1) == "HZ", sub=sub, dag=m.group(4) is not None)] * (int(pw) if pw else 1)
            pos = m.end()
        terms.append(dict(coef=coef, curly=curly, factors=facs, latex=t))
    return terms


def classify(f):
    if f["hat"]:
        assert not f["dag"]
        return dict(role="hat", n=int(f["sub"]) if f["sub"] else 0)
    kind = "Zd" if f["dag"] else "Z"
    sub = f["sub"]
    if sub is None:
        return dict(role="bare", kind=kind)
    m = re.fullmatch(r"\((\d+)\)", sub)
    if m:
        v = int(m.group(1))
        return dict(role="box", kind=kind, g=0, b=v // 2) if v % 2 == 0 else dict(role="odd", kind=kind, g=1, b=(v - 1) // 2)
    m = re.fullmatch(r"\((\d+)\)\((\d+)", sub)
    if m:
        return dict(role="open", kind=kind, g=int(m.group(2)), b=int(m.group(1)) // 2)
    m = re.fullmatch(r"(\d+)\)\((\d+)\)", sub)
    if m:
        return dict(role="close", kind=kind, g=int(m.group(1)), b=int(m.group(2)) // 2)
    m = re.fullmatch(r"\((\d+)", sub)
    if m:
        return dict(role="open", kind=kind, g=int(m.group(1)), b=0)
    m = re.fullmatch(r"(\d+)\)", sub)
    if m:
        return dict(role="close", kind=kind, g=int(m.group(1)), b=0)
    raise ValueError(sub)


def structure(term):
    """Assign factors to groups; None if the term contains an undifferentiated Z (= X = 0)."""
    fs = [classify(f) for f in term["factors"]]
    if any(f["role"] == "bare" for f in fs):
        return None
    gid, cur, odd_group = 0, None, None
    paren = {}
    out, pending = [], []
    for f in fs:
        f = dict(f)
        if f["role"] == "open":
            gid += 1
            cur = gid
            paren[cur] = [f]
            f["grp"] = cur
        elif f["role"] == "hat" and cur is not None:
            f["grp"] = cur
            paren[cur].append(f)
        elif f["role"] == "close":
            f["grp"] = cur
            paren[cur].append(f)
            cur = None
        elif f["role"] == "box":
            gid += 1
            f["grp"] = gid
        elif f["role"] == "odd":
            if odd_group is None:
                gid += 1
                odd_group = gid
            for h in pending:
                h["grp"] = odd_group
            pending = []
            f["grp"] = odd_group
        elif f["role"] == "hat":
            assert odd_group is not None, term["latex"]
            pending.append(f)
        out.append(f)
    assert cur is None and not pending, term["latex"]
    for g, mem in paren.items():  # an odd-total paren group joins the odd factors
        if sum(x["n"] if x["role"] == "hat" else x["g"] for x in mem) % 2:
            assert odd_group is not None, term["latex"]
            for x in out:
                if x["grp"] == g:
                    x["grp"] = odd_group
    return out


class Lab:
    n = 0

    @classmethod
    def new(cls):
        cls.n += 1
        return cls.n


def expand_group(factors):
    """-> list of (coef, [factor]) with factor = dict(kind in Z/Zd/Y, g, b, der=[labels], vec=label|None)."""
    R = None
    for f in reversed(factors):
        if f["role"] != "hat":
            base = dict(kind=f["kind"], g=f["g"], b=f["b"], der=[], vec=None)
            R = [(Fraction(1), [base])] if R is None else [(c, [base] + L) for c, L in R]
            continue
        n = f["n"]
        new = []
        if n >= 1:  # Z_0 = X = 0
            new += [(c, [dict(kind="Z", g=n, b=0, der=[], vec=None)] + L) for c, L in R]
        nu = Lab.new()
        for c, L in R:
            for j, fj in enumerate(L):
                if fj["g"] > 0:
                    L2 = [dict(x, der=list(x["der"])) for x in L]
                    L2[j]["g"] -= 1
                    L2[j]["der"].append(nu)
                    new.append((c * Fraction(2, n + 1) * fj["g"], [dict(kind="Y", g=n + 1, b=0, der=[], vec=nu)] + L2))
        R = new
    return R


def multigraphs(gs):
    m = len(gs)
    pairs = [(i, k) for i in range(m) for k in range(i, m)]

    def rec(idx, rem, cur):
        if idx == len(pairs):
            if all(r == 0 for r in rem):
                yield dict(cur)
            return
        i, k = pairs[idx]
        rng = range(rem[i] // 2 + 1) if i == k else range(min(rem[i], rem[k]) + 1)
        for e in rng:
            rem2 = list(rem)
            if i == k:
                rem2[i] -= 2 * e
            else:
                rem2[i] -= e
                rem2[k] -= e
            cur[(i, k)] = e
            yield from rec(idx + 1, rem2, cur)
        cur.pop((i, k), None)

    yield from rec(0, list(gs), {})


def dfact(n):
    return 1 if n <= 0 else n * dfact(n - 2)


class Evaluator:
    def __init__(self, ring, Ap, Z, Zd):
        self.ring, self.Ap, self.Z, self.Zd = ring, Ap, Z, Zd
        self.cache = {}

    def tensor(self, kind, s, l):
        key = (kind, s, l)
        if key not in self.cache:
            if kind == "Y":
                self.cache[key] = np.stack([self.ring.taylor_tensor(self.Ap[nu], s, l) for nu in range(4)], axis=l)
            else:
                self.cache[key] = self.ring.taylor_tensor(self.Z if kind == "Z" else self.Zd, s, l)
        return self.cache[key]

    def term(self, term):
        st = structure(term)
        if st is None:
            return 0.0
        order = []
        groups = {}
        for f in st:
            groups.setdefault(f["grp"], []).append(f)
            if f["grp"] not in order:
                order.append(f["grp"])
        exp = {g: expand_group(groups[g]) for g in order}
        slots = [f["grp"] for f in st]
        total = 0j
        for combo in itertools.product(*[exp[g] for g in order]):
            coef = Fraction(1)
            fb = {}
            for g, (c, L) in zip(order, combo):
                coef *= c
                fb[g] = list(L)
            ctr = {g: 0 for g in order}
            seq = []
            for g in slots:
                seq.append((g, fb[g][ctr[g]]))
                ctr[g] += 1
            total += float(coef) * self.contract(seq, order)
        val = float(term["coef"]) * total
        return 2 * val.real if term["curly"] else val

    def contract(self, seq, order):
        groups = {g: [i for i, (gg, _) in enumerate(seq) if gg == g] for g in order}
        per_group = []
        for g in order:
            idx = groups[g]
            gs = [seq[i][1]["g"] for i in idx]
            M2 = sum(gs)
            assert M2 % 2 == 0
            alts = []
            for e in multigraphs(gs):
                w = Fraction(math.prod(math.factorial(x) for x in gs))
                for (i, k), v in e.items():
                    w /= math.factorial(v) * (2 ** v if i == k else 1)
                alts.append((w / dfact(M2 - 1), {(idx[i], idx[k]): v for (i, k), v in e.items()}))
            per_group.append(alts)
        nf = len(seq)
        total = 0j
        for combo in itertools.product(*per_group):
            w = Fraction(1)
            E = {}
            for ww, e in combo:
                w *= ww
                E.update(e)
            nxt = [0]
            axes = [[] for _ in range(nf)]
            lap = [0] * nf
            for (i, k), v in E.items():
                if i == k:
                    lap[i] += v
                else:
                    for _ in range(v):
                        nxt[0] += 1
                        axes[i].append(("c", nxt[0]))
                        axes[k].append(("c", nxt[0]))
            ops = []
            remap = {}
            for i, (g, f) in enumerate(seq):
                der = axes[i] + [("h", x) for x in f["der"]]
                T = self.tensor(f["kind"], f["b"] + lap[i], len(der))
                sub = der + ([("h", f["vec"])] if f["kind"] == "Y" else []) + [("m", i), ("m", (i + 1) % nf)]
                ops += [T, [remap.setdefault(x, len(remap)) for x in sub]]
            assert len(remap) <= 52
            total += float(w) * complex(np.einsum(*ops, [], optimize="greedy"))
        return total


# %% [markdown]
# ## (a) The source; term counts

# %%
tex = H.read_tex("hep-th/9708152", "ncnotes12.tex")
bl = extract_blocks(tex)
terms = {n: parse_terms(bl[n]) for n in range(1, 7)}
print("(a) term counts a_1..a_6:", [len(terms[n]) for n in range(1, 7)], " X-free:", [sum(structure(t) is not None for t in terms[n]) for n in range(1, 7)])
[t["latex"] for t in terms[3]]          # inspect: the four terms of a_3 as printed

# %% [markdown]
# ## (b) Constant non-commuting potentials (N = 3, d = 4): a_2..a_6 against the exact heat kernel; consistency of the notation

# %%
print("(b) random constant potentials, N = 3, d = 4: tr a_n(ours) = tr a_n(vdV)/n! against the exact heat kernel")
N, nfit = 3, 70
ring = PolyRing(12, N)
rng = np.random.default_rng(7)


def setup(Ah):
    Ap, Z, Zd, chk = fs_gauge(ring, [ring.const(-1j * a) for a in Ah])
    return Evaluator(ring, Ap, Z, Zd), chk


def val(ev, latex):
    t = parse_terms(latex)[0]
    t["curly"] = False
    t["coef"] = Fraction(1)
    return ev.term(t)


for c in range(2):
    Ah = H.random_A(N, rng, herm=True, scale=0.6)
    ex = H.exact_tr_a(Ah, 6)
    ev, chk = setup(Ah)
    print(f"config {c} (FS checks {chk[0]:.0e}, {chk[1]:.0e}):")
    for n in range(2, 7):
        tot = sum(ev.term(t) for t in terms[n]) / math.factorial(n)
        print(f"   n = {n}: exact {ex[n].real:+.12e}  vdV {tot.real:+.12e}  rel.diff {abs(tot - ex[n]) / abs(ex[n]):.1e}")
    if c == 0:
        l1 = val(ev, r"\Z_{(2}\do\Z_{2)(2)}")
        r1 = Fraction(5, 6) * val(ev, r"\Z_{(2}\do\Z_{4)}") + Fraction(1, 6) * val(ev, r"\Z_{(2)}\do\Z_{(4)}")
        l2, r2 = val(ev, r"\Z_{(1}\do\Z_{1)(2)}"), val(ev, r"\Z_{(1}\do\Z_{3)}")
        l3, r3 = val(ev, r"\Z_{(3}\do\Z_{1)(2)}"), val(ev, r"\Z_{(2)(1}\do\Z_{3)}")
        print(f"   box-moving identities: rel. diffs {abs(l1 - r1) / abs(l1):.0e}, {abs(l2 - r2) / abs(l2):.0e}, {abs(l3 - r3) / abs(l3):.0e}")
        worst = 0
        for a, b in [(r"\Z_{(1}\do\HZ_1\HZ\Z_{2)}", r"\Z_{(2}\do\HZ\HZ_1\Z_{1)}"), (r"\Z_{(1}\do\HZ^2\Z_{3)}", r"\Z_{(3}\do\HZ^2\Z_{1)}"),
                     (r"\Z_{(1}\do\HZ_3\Z_{2)}", r"\Z_{(2}\do\HZ_3\Z_{1)}"), (r"\Z_{(1}\do\HZ\HZ_2\Z_{1)}", r"\Z_{(1}\do\HZ_2\HZ\Z_{1)}")]:
            va, vb = val(ev, a), val(ev, b)
            worst = max(worst, abs(va - vb.conjugate()) / abs(va))
        print(f"   hermiticity: tr(label-swapped hat term) = conj tr(hat term) to {worst:.0e}")

# %% [markdown]
# ## (c) Least squares of the X-free a_6 structures against the exact constant-field a_6

# %%
print("(c) least squares of the X-free a_6 structures on 70 constant configurations")
t6 = [t for t in terms[6] if structure(t) is not None]
extra = parse_terms(r"\sfrac37\{\Z_{(2}\do\Z_{2)}\Z_{(2)}\}")
rows, rhs = [], []
for c in range(nfit):
    Ah = H.random_A(N, rng, herm=True, scale=0.6)
    ev, _ = setup(Ah)
    row = []
    for t in t6 + extra:
        tt = dict(t)
        tt["coef"] = Fraction(1)
        row.append(ev.term(tt).real)
    rows.append(row)
    rhs.append((H.exact_tr_a(Ah, 6)[6] * 720).real)
M, b = np.array(rows), np.array(rhs)
coef = np.array([float(t["coef"]) for t in t6] + [0.0])
i37 = [i for i, t in enumerate(t6) if t["latex"] == r"\Z_{(2}\Z_{2)}\Z_{(2)}"][0]
print("a_6 as printed: rel. residual on %d configs %.2e" % (nfit, np.abs(M @ coef - b).max() / np.abs(b).max()))
c2 = coef.copy()
c2[-1], c2[i37] = c2[i37], 0
print("a_6 with Z_(2 -> Z_(2^dagger in the 3/7 term: rel. residual %.2e" % (np.abs(M @ c2 - b).max() / np.abs(b).max()))
sc = np.linalg.norm(M, axis=0)
x, *_ = np.linalg.lstsq(M / sc, b, rcond=1e-12)
s = np.linalg.svd(M / sc, compute_uv=False)
print("best least-squares combination of the 35 structures: rank %d, rel. residual %.2e (not in the span if >> 1e-12)"
      % (int((s > s[0] * 1e-10).sum()), np.abs((M / sc) @ x - b).max() / np.abs(b).max()))
print("max |entry| / max |exact|: %.1e (float rounding ~1e-16 of this)" % (np.abs(M).max() / np.abs(b).max()))

# %% [markdown]
# ## (d) BPST: pointwise densities, A_2..A_6, the a_6 structures that vanish on BPST

# %%
print("(d) BPST, rho = 1, x0 = (r,0,0,0) at 12 radii")
t6 = [t for t in terms[6] if structure(t) is not None]
DEW = {2: ["-8"], 3: ["192/5", "-256/5"], 4: ["-1248/7", "5120/7", "-2304/7"],
       5: ["6656/7", "-2430976/315", "650240/63", "-16384/7"],
       6: ["-327424/55", "38797312/495", "-305211392/1485", "1497088/11", "-204800/11"]}
EXACT = {"1/2": {2: Fr(-1, 12), 3: Fr(1, 75), 4: Fr(17, 735), 5: Fr(-116, 2835), 6: Fr(25624, 571725)},
         "1": {2: Fr(-1, 3), 3: Fr(4, 75), 4: Fr(208, 735), 5: Fr(-9248, 19845), 6: Fr(245888, 1715175)}}
sig = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
eps = np.array(H.EPS, dtype=float)
K = 12
radii = [Fr(0), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(4, 3), Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(4), Fr(5)]
B = lambda a, b: math.gamma(a) * math.gamma(b) / math.gamma(a + b)
for iso in ["1/2", "1"]:
    gens = [-1j * s / 2 for s in sig] if iso == "1/2" else [-eps[a].astype(complex) for a in range(3)]
    N = gens[0].shape[0]
    ring = PolyRing(K, N)
    dens = {n: [] for n in range(2, 7)}
    termmax = np.zeros(len(t6))
    maxdev = {n: 0.0 for n in range(2, 7)}
    for r in radii:
        A = H.bpst_A_series([r, 0, 0, 0], K)
        Afun = []
        for mu in range(4):
            p = ring.zero()
            for a in range(3):
                for e, v in A[a][mu].items():
                    p[e] += float(v) * gens[a]
            Afun.append(p)
        Ap, Z, Zd, chk = fs_gauge(ring, Afun)
        ev = Evaluator(ring, Ap, Z, Zd)
        u = r * r
        for n in range(2, 7):
            v = sum(ev.term(t) for t in terms[n]).real / math.factorial(n)
            dens[n].append(v)
            if iso == "1/2":
                dw = float(sum(Fr(c) * u ** j for j, c in enumerate(DEW[n])) / (1 + u) ** (2 * n))
                maxdev[n] = max(maxdev[n], abs(v - dw) / abs(dw))
        if iso == "1/2":
            for i, t in enumerate(t6):
                tt = dict(t)
                tt["coef"] = Fr(1)
                termmax[i] = max(termmax[i], abs(ev.term(tt)) / (1 + float(u)) ** -12)
    if iso == "1/2":
        print("isospin 1/2, max relative deviation of the vdV pointwise density from the DeWitt polynomial over 12 radii:",
              {n: f"{v:.0e}" for n, v in maxdev.items()})
        zero = [t["latex"] for i, t in enumerate(t6) if termmax[i] < 1e-8 * termmax.max()]
        print(f"a_6 structures vanishing on BPST at all radii: {len(zero)} of {len(t6)}")
    uu = np.array([float(r * r) for r in radii])
    for n in range(2, 7):
        y = np.array(dens[n]) * (1 + uu) ** (2 * n)
        V = np.vander(uu, n - 1, increasing=True)
        sc = np.abs(V).max(axis=0)
        c, *_ = np.linalg.lstsq(V / sc, y, rcond=None)
        c /= sc
        An = sum(cj * B(j + 2, 2 * n - j - 2) for j, cj in enumerate(c)) / 16
        print(f"iso {iso} n = {n}: vdV A_n = {An:+.12f} (fit residual {np.abs(V @ c - y).max() / np.abs(y).max():.0e})"
              f"   exact (FHSS) {EXACT[iso][n]} = {float(EXACT[iso][n]):+.12f}   diff {An - float(EXACT[iso][n]):+.1e}", flush=True)
