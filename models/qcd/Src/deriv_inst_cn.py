# %% [markdown]
# # Appendix check: the SU(N) gauge-orientation zero modes, the volume of SU(N)/H and C_N
#
# Research note models/qcd, derivations of the appendices (sympy, numpy, mpmath).  app:inst 「集団座標と1ループの積分。」 (N3):
# (a) singular-gauge BPST (g = 1): Lambda = h(r) T with T a constant generator in an isospin-c channel of the adjoint (c = 2: triplet,
#     c = 3/4: doublet); D^2 Lambda = 0, the norms 2 int tr (D Lambda)^2; an explicit SU(3) matrix check of the doublet mode at random points;
# (b) Vol(U(n)) (metric tr dU^+ dU) = (2 pi)^(n(n+1)/2)/prod_{k<n} k! from U(n)/U(n-1) = S^(2n-1); Gr_2(C^N); Vol(SU(N)/H) in the omega metric
#     (U = exp(i omega^k T^k), tr T^k T^l = delta/2) = 2^(4N-5) pi^(2N-2)/((N-1)!(N-2)!), also as Vol(SU(N))/Vol(H);
# (c) C_N^PV assembled from the zero modes and alpha(1/2), alpha(1), against (2 e^(5/6)/pi^2) e^(-kappa N)/((N-1)!(N-2)!) (inst_density.py)
#     and N = 2 against e^(-alpha(1))/(4 pi^2).
# Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_inst_cn.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_inst_cn.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import sys
import math
import numpy as np, sympy as sp, mpmath as mp
INTERACTIVE = "ipykernel" in sys.modules
r, rho = sp.symbols('r rho', positive=True)

# %% [markdown]
# ## (a) The orientation zero modes

# %%
print("(a) zero modes D_mu (h T) in singular gauge")
for name, c, h, expect in (("triplet", sp.Integer(2), r**2/(r**2 + rho**2), 4*sp.pi**2*rho**2),
                           ("doublet", sp.Rational(3, 4), r/sp.sqrt(r**2 + rho**2), 2*sp.pi**2*rho**2)):
    eq = sp.simplify(sp.diff(h, r, 2) + 3/r*sp.diff(h, r) - 4*rho**4*c*h/(r**2*(r**2 + rho**2)**2))
    dens = sp.simplify(sp.diff(h, r)**2 + 4*rho**4*c*h**2/(r**2*(r**2 + rho**2)**2))   # 2 tr(D Lambda)^2 with tr TT = 1/2
    norm = sp.simplify(sp.integrate(2*sp.pi**2*r**3*dens, (r, 0, sp.oo)))
    print(f"    {name}: h = {h}, D^2 Lambda = {eq}, 2 tr (D Lambda)^2 = {dens}, norm^2 = {norm} (expected {expect}), h -> {sp.limit(h, r, sp.oo)}")

# %% [markdown]
# ### Explicit SU(3) check of the doublet mode

# %%
# explicit SU(3): singular-gauge A_mu = 2 etabar_{a mu nu} x_nu rho^2/(x^2 (x^2+rho^2)) t^a, t^a = sigma^a/2 in the upper-left block
eps3 = np.zeros((3, 3, 3)); eps3[0, 1, 2] = eps3[1, 2, 0] = eps3[2, 0, 1] = 1; eps3[0, 2, 1] = eps3[2, 1, 0] = eps3[1, 0, 2] = -1
etab = np.zeros((3, 4, 4))
for a in range(3):
    etab[a, :3, :3] = eps3[a]; etab[a, a, 3] = -1; etab[a, 3, a] = 1
sig = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], complex)]
t3 = [np.pad(s/2, ((0, 1), (0, 1))) for s in sig]
gm = np.zeros((3, 3), complex); gm[0, 2] = gm[2, 0] = 0.5; T4 = gm              # lambda_4/2 (doublet)
gm = np.zeros((3, 3), complex); gm[1, 2] = -0.5j; gm[2, 1] = 0.5j; T7 = gm      # lambda_7/2 (doublet)
R0 = 1.0
def A_sing(x):
    x2 = x @ x
    return [sum(2*etab[a, m] @ x*R0**2/(x2*(x2 + R0**2))*t3[a] for a in range(3)) for m in range(4)]
def dens_doublet(x, T, eps=1e-6):
    hfun = lambda y: np.sqrt(y @ y)/np.sqrt(y @ y + R0**2)
    A = A_sing(x); tot = 0.0
    for m in range(4):
        e = np.zeros(4); e[m] = eps
        dL = (hfun(x + e) - hfun(x - e))/(2*eps)*T - 1j*hfun(x)*(A[m] @ T - T @ A[m])
        tot += 2*np.real(np.trace(dL @ dL))
    return tot
rng = np.random.default_rng(1)
for T, nm in ((T4, "lambda_4/2"), (T7, "lambda_7/2")):
    vals = []
    for _ in range(4):
        x = rng.normal(size=4); x *= 0.7/np.linalg.norm(x)
        vals.append(dens_doublet(x, T))
    print(f"    SU(3) doublet generator {nm}: 2 tr(D Lambda)^2 at |x| = 0.7 in random directions: {np.round(vals, 10)}, formula 4/(r^2+1)^3 = {4/(0.49 + 1)**3:.10f}")

# %% [markdown]
# ## (b) Group volumes

# %%
print("(b) group volumes")
def volU_tr(n):
    return (2*sp.pi)**sp.Rational(n*(n + 1), 2)/sp.prod([sp.factorial(k) for k in range(1, n)])
for n in range(1, 6):
    # fibration U(n)/U(n-1) = S^(2n-1): tr-metric = 2|du|^2 on the 2(n-1) mixing directions, |du|^2 on the phase of u
    sph = sp.sqrt(2)**(2*n - 2)*2*sp.pi**n/sp.factorial(n - 1)
    ok = sp.simplify(volU_tr(n) - (volU_tr(n - 1) if n > 1 else 1)*sph) == 0
    print(f"    Vol_tr(U({n})) = {volU_tr(n)}; recursion via S^{2*n - 1}: {ok}")
print(f"    Vol_omega(SU(2)) = 2^(3/2) Vol_tr(SU(2)) with Vol_tr(SU(2)) = Vol_tr(U(2))/(Vol(U(1) centre)/2) = {sp.simplify(2**sp.Rational(3, 2)*volU_tr(2)/(2*sp.pi*sp.sqrt(2)/2))} (expected 16 pi^2)")
for N in range(2, 7):
    gr_tr = sp.simplify(volU_tr(N)/(volU_tr(2)*volU_tr(N - 2))) if N > 2 else 1
    gr_om = 2**(2*(N - 2))*gr_tr                       # omega metric = 2 x tr metric, dim Gr_2 = 4(N-2)
    coset = sp.simplify(gr_om*8*sp.pi**2)
    formula = 2**(4*N - 5)*sp.pi**(2*N - 2)/(sp.factorial(N - 1)*sp.factorial(N - 2))
    print(f"    N = {N}: Vol_tr(Gr_2) = {gr_tr}, Vol_omega(SU(N)/H) = {coset}  vs 2^(4N-5) pi^(2N-2)/((N-1)!(N-2)!) = {formula}: {sp.simplify(coset - formula) == 0}")
# cross-check with Vol(SU(N))/Vol(H): Vol_omega(SU(N)) = 2^((N^2-1)/2) sqrt(N) (2pi)^((N-1)(N+2)/2)/prod k!, H = {diag(e^{i phi} 1_2, V)}
def volSU_om(n):
    return 2**sp.Rational(n*n - 1, 2)*sp.sqrt(n)*(2*sp.pi)**sp.Rational((n - 1)*(n + 2), 2)/sp.prod([sp.factorial(k) for k in range(1, n)])
for N in range(3, 7):
    volH = 2*sp.sqrt(sp.Rational(N, 2))*2**sp.Rational((N - 2)**2, 2)*volU_tr(N - 2)    # double cover of U(N-2), centre stretched by sqrt(N/2)
    print(f"    N = {N}: Vol(SU(N))/Vol(H) = {sp.simplify(volSU_om(N)/volH)}")
[volSU_om(n) for n in range(2, 5)]          # inspect: Vol_omega(SU(N)), N = 2, 3, 4

# %% [markdown]
# ## (c) C_N

# %%
print("(c) C_N")
ZP = mp.zeta(-1, derivative=1)
a12 = -mp.mpf(5)/72 - mp.log(2)/6 - 2*ZP
a1 = 4*a12 + mp.log(2) - mp.mpf(5)/6
kappa = 2*a12 + 2*mp.log(2)
for N in range(2, 6):
    vol = mp.mpf(2)**(4*N - 5)*mp.pi**(2*N - 2)/(math.factorial(N - 1)*math.factorial(N - 2))
    # zero modes: (8pi^2/g^2)^2 (16pi^2/g^2)^(1/2) (4pi^2 rho^2/g^2)^(3/2) (2pi^2 rho^2/g^2)^(2(N-2)) (mu/sqrt(2pi))^(4N): coefficient of (8pi^2/g^2)^(2N) rho^(4N-5) mu^(4N)
    zm = mp.sqrt(2)*mp.mpf(2)**(-1.5)*mp.mpf(4)**(-2*(N - 2))*(2*mp.pi)**(-2*N)
    nonzero = mp.e**(-a1 - 2*(N - 2)*a12)
    CN = vol*zm*nonzero
    CN_formula = 2*mp.e**(mp.mpf(5)/6)/mp.pi**2*mp.e**(-kappa*N)/(math.factorial(N - 1)*math.factorial(N - 2))
    print(f"    N = {N}: assembled C_N^PV = {mp.nstr(CN, 15)}, (2e^(5/6)/pi^2) e^(-kappa N)/((N-1)!(N-2)!) = {mp.nstr(CN_formula, 15)}, MS-bar x e^(N/6) = {mp.nstr(CN*mp.e**(mp.mpf(N)/6), 10)}")
print(f"    N = 2 directly: e^(-alpha(1))/(4 pi^2) = {mp.nstr(mp.e**(-a1)/(4*mp.pi**2), 15)};  kappa = {mp.nstr(kappa, 12)}")
CN, CN_formula          # inspect: N = 5
