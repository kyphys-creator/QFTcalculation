# %% [markdown]
# # Appendix check: the unique Bose-antisymmetric rank-3 tensor (three-gluon vertex)
#
# Research note models/qcd, derivations of the appendices (sympy).
#   app:vertex 「3グルーオンの頂点の図の種類ごとの極。」 (R8): a rank-3 tensor built from g^{mu nu} and the external momenta, linear in the
#   momenta (p1 + p2 + p3 = 0) and antisymmetric under the exchange of any two legs (index and momentum together), is unique up to a
#   constant and equals the Lorentz part of the tree three-gluon vertex g^{mu nu}(p1-p2)^rho + g^{nu rho}(p2-p3)^mu + g^{rho mu}(p3-p1)^nu
#   (null space of the linear conditions at two random rational momentum configurations).
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_vertex_bose.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_vertex_bose.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import itertools, random
import sympy as sp
INTERACTIVE = "ipykernel" in sys.modules

g = sp.diag(1, -1, -1, -1)
random.seed(3)
def rvec():
    return [sp.Rational(random.randint(-9, 9), random.randint(1, 5)) for _ in range(4)]

# basis: g^{ij} p_k^{l} for the three slot pairs (i,j) with third slot l, and p_k in {p1, p2}

# %% [markdown]
# ## The six basis tensors g^{ij} p_k^l

# %%
def T_basis(n, P):
    """P = (p1, p2, p3) as upper-index component lists; returns 4x4x4 array of basis element n"""
    pair_slots = [((0, 1), 2), ((1, 2), 0), ((2, 0), 1)]
    (i, j), l = pair_slots[n // 2]
    p = P[n % 2]
    arr = {}
    for idx in itertools.product(range(4), repeat=3):
        arr[idx] = g[idx[i], idx[j]]*p[idx[l]]
    return arr

def T_of(c, P):
    out = {idx: 0 for idx in itertools.product(range(4), repeat=3)}
    for n in range(6):
        b = T_basis(n, P)
        for idx in out:
            out[idx] += c[n]*b[idx]
    return out


# %% [markdown]
# ## The antisymmetry conditions at two random momentum configurations

# %%
c = sp.symbols('c0:6')
eqs = []
for trial in range(2):
    p1, p2 = rvec(), rvec()
    p3 = [-p1[i] - p2[i] for i in range(4)]
    T = T_of(c, (p1, p2, p3))
    # exchange legs 1<->2: indices (mu,nu,rho)->(nu,mu,rho), momenta p1<->p2 (p3 unchanged)
    T12 = T_of(c, (p2, p1, p3))
    # exchange legs 2<->3: momenta p2<->p3; in the basis p3 must be re-expressed: use basis in terms of (p1, p3) then
    # the 'p2' slot momentum is p3 and the 'p1' slot stays p1, i.e. evaluate with (p1, p3, p2) where index 1 of P is p3
    T23 = T_of(c, (p1, p3, p2))
    for idx in T:
        eqs.append(sp.expand(T12[(idx[1], idx[0], idx[2])] + T[idx]))
        eqs.append(sp.expand(T23[(idx[0], idx[2], idx[1])] + T[idx]))
M = sp.Matrix([[sp.diff(e, ci) for ci in c] for e in eqs if e != 0])
M.shape, M.rank()          # inspect: (number of nonzero conditions, 6 unknowns) and the rank

# %% [markdown]
# ## The solution space

# %%
ns = M.nullspace()
print("dimension of the solution space:", len(ns))
sol = ns[0]/ns[0][0]
print("solution (coefficients of g^{mn}p1^r, g^{mn}p2^r, g^{nr}p1^m, g^{nr}p2^m, g^{rm}p1^n, g^{rm}p2^n):", list(sol))
# tree: g^{mn}(p1-p2)^r + g^{nr}(p2-p3)^m + g^{rm}(p3-p1)^n with p3=-p1-p2:
tree = [1, -1, 1, 2, -2, -1]
print("tree coefficients:", tree)
ok = len(ns) == 1 and all(sp.simplify(sol[i] - tree[i]) == 0 for i in range(6))
print("OK  unique antisymmetric structure = tree" if ok else "FAIL")
list(sol), tree          # inspect: the solution and the tree vertex
