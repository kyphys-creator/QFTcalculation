# %% [markdown]
# # Appendix check: the O(a^2) term of the clover charge of the BPST instanton
#
# Research note models/qcd, derivations of the appendices (sympy, numpy).  app:inst 「格子の O(a^2)。」 (N4): BPST (rho = 1, g = 1, regular
# gauge).
# (i) F^cl_{mu nu}(x) = (i/8a^2)[(C - C^+) - traceless] with C the sum of the four leaves at x (exact links, as in inst_lattice.py), compared
#     at a point with G_{mu nu} + (a^2/6)(D_mu^2 + D_nu^2) G_{mu nu}: (F^cl - G)/a^2 -> (1/6)(D_mu^2 + D_nu^2) G as a -> 0;
# (ii) eps_{mu nu rho sig} tr[G_{mu nu} (D_rho^2 + D_sig^2) G_{rho sig}] integrates to -4 sum int tr(D_rho G_{rho sig})^2 = -4 (96 pi^2/5);
#      Q_cl - Q = (a^2/6)(2/32 pi^2) int eps tr[G (D^2 + D^2) G] = -(4/5) a^2;
# (iii) the lattice data of results/inst_lattice.csv (inst_lattice.py): fit of Q_clover - Q in a^2, a^4.
# Reads results/inst_lattice.csv.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_clover.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_clover.py   (about 15 s)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import itertools, csv
import os
import sys
import numpy as np, sympy as sp
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
X = sp.symbols('x1:5', real=True)
I = sp.I
def eta(a, m, n):
    if m < 3 and n < 3: return sp.LeviCivita(a, m, n)
    if n == 3 and m < 3: return 1 if a == m else 0
    if m == 3 and n < 3: return -1 if a == n else 0
    return 0
sig = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -I], [I, 0]]), sp.Matrix([[1, 0], [0, -1]])]
r2 = sum(xi**2 for xi in X)
A = [sum((2*eta(a, m, n)*X[n]/(r2 + 1)*sig[a]/2 for a in range(3) for n in range(4)), sp.zeros(2)) for m in range(4)]
G = [[sp.simplify(A[n].diff(X[m]) - A[m].diff(X[n]) - I*(A[m]*A[n] - A[n]*A[m])) for n in range(4)] for m in range(4)]
Dad = lambda m, M: M.diff(X[m]) - I*(A[m]*M - M*A[m])
x0 = [0.3, -0.2, 0.5, 0.1]
sub = dict(zip(X, x0))
num = lambda M: np.array(M.subs(sub).evalf(), dtype=complex)
G[0][1]          # inspect: G_12 of BPST (regular gauge, rho = 1)

# %% [markdown]
# ## Exact links and the clover

# %%
# exact links
def link(x, mu, a):
    x = np.array(x, float)
    c2 = 1.0 + sum(x[k]**2 for k in range(4) if k != mu); c = np.sqrt(c2)
    Iint = (np.arctan((x[mu] + a)/c) - np.arctan(x[mu]/c))/c
    v = np.array([2*sum(float(eta(b, mu, n))*x[n] for n in range(4)) for b in range(3)])*Iint
    th = np.linalg.norm(v)
    s = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]
    vs = sum(v[b]*s[b] for b in range(3))
    return np.cos(th/2)*np.eye(2) - 1j*np.sin(th/2)*vs/th if th > 0 else np.eye(2, dtype=complex)   # exp(-i v.sigma/2)
def U(x, mu, a, sign=+1):
    """link from x to x + sign a mu-hat"""
    if sign > 0: return link(x, mu, a)
    xm = np.array(x, float); xm[mu] -= a
    return link(xm, mu, a).conj().T
def plaq_path(x, steps, a):
    M = np.eye(2, dtype=complex); y = np.array(x, float)
    for mu, sg in steps:
        M = M @ U(y, mu, a, sg); y[mu] += sg*a
    return M
def clover(x, mu, nu, a):
    leaves = [[(mu, 1), (nu, 1), (mu, -1), (nu, -1)], [(nu, 1), (mu, -1), (nu, -1), (mu, 1)],
              [(mu, -1), (nu, -1), (mu, 1), (nu, 1)], [(nu, -1), (mu, 1), (nu, 1), (mu, -1)]]
    C = sum(plaq_path(x, L, a) for L in leaves)
    Am = C - C.conj().T
    Am = Am - np.trace(Am)/2*np.eye(2)
    return 1j/(8*a*a)*Am

# %% [markdown]
# ## (i) The clover field strength at a point

# %%
print("(i) clover at x0 =", x0)
for (mu, nu) in ((0, 1), (0, 3), (2, 3)):
    G0 = num(G[mu][nu])
    corr = num(sp.simplify(Dad(mu, Dad(mu, G[mu][nu])) + Dad(nu, Dad(nu, G[mu][nu]))))/6
    for a in (0.04, 0.02, 0.01):
        Fc = clover(x0, mu, nu, a)
        ratio = (Fc - G0)/a**2
        print(f"    (mu,nu) = ({mu+1},{nu+1}), a = {a}: max|(F^cl - G)/a^2 - (1/6)(D_mu^2+D_nu^2)G| = {np.max(np.abs(ratio - corr)):.2e}"
              f"  (size of (1/6)(D^2+D^2)G: {np.max(np.abs(corr)):.3f})")
clover(x0, 0, 1, 0.01), num(G[0][1])          # inspect: F^cl_12 at a = 0.01 and G_12 at x0

# %% [markdown]
# ## (ii) The O(a^2) term of the charge

# %%
# (ii) symbolic densities
r = sp.symbols('r', positive=True)
def radial_int(expr):
    e = sp.simplify(expr.subs({X[0]: r, X[1]: 0, X[2]: 0, X[3]: 0}))
    return sp.integrate(2*sp.pi**2*r**3*e, (r, 0, sp.oo)), e
# sum_{rho sig} tr(D_rho G_{rho sig})^2 (no sum inside)
w = sp.simplify(sum(((Dad(rh, G[rh][sg]))**2).trace() for rh in range(4) for sg in range(4)))
print("(ii) sum_{rho sig} tr(D_rho G_{rho sig})^2 =", sp.factor(w))
Wint, _ = radial_int(w)
print("     its integral =", Wint)
# eps tr[G_{mu nu} (D_rho^2 + D_sig^2) G_{rho sig}] -- not spherically symmetric pointwise, integrate in spherical coordinates
cd = 0
for mu, nu, rh, sg in itertools.permutations(range(4)):
    e = sp.LeviCivita(mu, nu, rh, sg)
    cd += e*(G[mu][nu]*(Dad(rh, Dad(rh, G[rh][sg])) + Dad(sg, Dad(sg, G[rh][sg])))).trace()
cd = sp.simplify(cd)
print("     eps tr[G (D_rho^2 + D_sig^2) G] =", sp.factor(cd))
# self-duality: eps_{mu nu rho sig} G_{mu nu} = 2 G_{rho sig}  ->  integrand = 4 sum tr[G_{rho sig} D_rho^2 G_{rho sig}]
alt = sp.simplify(4*sum((G[rh][sg]*Dad(rh, Dad(rh, G[rh][sg]))).trace() for rh in range(4) for sg in range(4)))
print("     4 sum tr[G_{rho sig} D_rho^2 G_{rho sig}] equal pointwise:", sp.simplify(cd - alt) == 0)
b1, b2, b3 = sp.symbols('b1:4', real=True)
sph = {X[0]: r*sp.cos(b1), X[1]: r*sp.sin(b1)*sp.cos(b2), X[2]: r*sp.sin(b1)*sp.sin(b2)*sp.cos(b3), X[3]: r*sp.sin(b1)*sp.sin(b2)*sp.sin(b3)}
cds = sp.simplify(cd.subs(sph))
cint = sp.integrate(sp.integrate(sp.integrate(sp.integrate(cds*r**3*sp.sin(b1)**2*sp.sin(b2), (b3, 0, 2*sp.pi)), (b2, 0, sp.pi)), (b1, 0, sp.pi)), (r, 0, sp.oo))
print("     int eps tr[G (D^2+D^2) G] =", sp.simplify(cint), " vs -4 x", Wint, "=", -4*Wint)
print("     Q_cl - Q = (a^2/6)(2/(32 pi^2)) x int =", sp.simplify(cint*sp.Rational(2, 6)/(32*sp.pi**2)), "a^2")

# %% [markdown]
# ## (iii) The lattice data of inst_lattice.py

# %%
# (iii) lattice data
rows = list(csv.DictReader(open(os.path.join(HERE, 'results', 'inst_lattice.csv'))))
a = np.array([float(rw['a_over_rho']) for rw in rows]); dq = np.array([float(rw['Q_clover']) - float(rw['Q_continuum_same_sites']) for rw in rows])
c, *_ = np.linalg.lstsq(np.array([a**2, a**4]).T, dq, rcond=None)
print(f"(iii) lattice: Q_clover - continuum = {c[0]:+.4f} a^2 {c[1]:+.4f} a^4  (expected -4/5 a^2)")
c          # inspect: the fit coefficients of a^2, a^4
