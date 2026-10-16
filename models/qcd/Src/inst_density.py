# %% [markdown]
# # Step (10): the one-instanton density in MS-bar and the dilute-gas topological susceptibility
#
# Research note models/qcd, step (10).  d(rho) = C_N (8 pi^2/g^2)^(2N) rho^-5 exp(-8 pi^2/g^2) prod_f (C_q m_f rho) with the coupling at mu = 1/rho
# (Eq. (instdens)); C_N^PV = (2 e^(5/6)/pi^2) e^(-C_2 N)/((N-1)!(N-2)!), C_2 = 2 alpha(1/2) + 2 ln 2, C_N^MS = C_N^PV e^(N/6), C_q = e^(2 alpha(1/2)).
# SU(3) without quarks: two-loop running coupling (exact implicit solution) with Lambda_MS r0 = 0.602 (Capitani et al.), r0 = 0.5 fm.
# chi(rho_c) = 2 int_0^rho_c d(rho) d rho (instantons and anti-instantons, dilute gas, E(theta) = -chi cos theta); the cut rho_c that gives the
# lattice value chi^(1/4) = 191 MeV (Del Debbio-Giusti-Pica).  -> results/inst_density.csv
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python inst_density.py

# %%
import csv, math, os
import numpy as np, mpmath as mp
from scipy.integrate import quad
from scipy.optimize import brentq
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
HBARC = 0.1973269804                      # GeV fm
ZP = mp.zeta(-1, derivative=1)
A12 = float(-mp.mpf(5)/72 - mp.log(2)/6 - 2*ZP)
A1 = 4*A12 + np.log(2) - 5/6
C1 = 2*np.exp(5/6)/np.pi**2
C2 = 2*A12 + 2*np.log(2)
CQ = np.exp(2*A12)

def C_PV(N):
    return C1*np.exp(-C2*N)/(math.factorial(N - 1)*math.factorial(N - 2))
def C_MS(N):
    return C_PV(N)*np.exp(N/6)

# %%
if __name__ == "__main__":
    print(f"alpha(1/2) = {A12:.9f}, alpha(1) = {A1:.9f}")
    print(f"SU(2) directly: e^(-alpha(1))/(4 pi^2) = {np.exp(-A1)/(4*np.pi**2):.9e}  vs  C_2^PV from C_1, C_2: {C_PV(2):.9e}")
    zp2 = mp.zeta(2, derivative=1)
    c2lit = float(5*mp.log(2)/3 - mp.mpf(17)/36 + (mp.log(2*mp.pi) + mp.euler)/3 - 2*zp2/mp.pi**2)
    print(f"C_1 = 2 e^(5/6)/pi^2 = {C1:.6f};  C_2 = 2 alpha(1/2) + 2 ln 2 = {C2:.9f}  (literature form (5/3) ln 2 - 17/36 + (ln 2pi + gamma)/3 - 2 zeta'(2)/pi^2 = {c2lit:.9f});"
          f"  MS-bar: C_2 - 1/6 = {C2 - 1/6:.6f};  C_q = e^(2 alpha(1/2)) = {CQ:.6f}")
    c3lit = float(-mp.log(2)/3 - mp.mpf(17)/36 + (mp.log(2*mp.pi) + mp.euler)/3 - 2*zp2/mp.pi**2)
    print(f"ln C_q = 2 alpha(1/2) = {2*A12:.9f}  vs  literature C_3^PV = -(1/3) ln 2 - 17/36 + (ln 2pi + gamma)/3 - 2 zeta'(2)/pi^2 = {c3lit:.9f}"
          " (the quark determinant is the same in PV and MS-bar with M = mu, so C_q is not shifted)")
    for N in (2, 3, 4):
        print(f"N = {N}: C_N^PV = {C_PV(N):.6e}, C_N^MS = {C_MS(N):.6e}")

# %% [markdown]
# ## SU(3), no quarks

# %%
N, NF = 3, 0
B0 = 11*N/3 - 2*NF/3; B1 = 34*N**2/3 - (10*N/3 + (N**2 - 1)/N)*NF
LAM = 0.602/0.5*HBARC                      # GeV
def S0(mu):
    """8 pi^2/g^2(mu) = 1/(2a), a = g^2/(16 pi^2): 1/a + (B1/B0) ln(B0 a/(1 + B1 a/B0)) = 2 B0 ln(mu/Lambda) (Eq. (run2))"""
    L = 2*np.log(mu/LAM)
    a = brentq(lambda a: 1/a + B1/B0*np.log(B0*a/(1 + B1*a/B0)) - B0*L, 1e-8, 50.0)
    return 1/(2*a)
def dens(rho):
    s = S0(1/rho)
    return C_MS(N)*s**(2*N)*rho**-5*np.exp(-s)
def chi(rc):
    return 2*quad(dens, 1e-6, rc, limit=400, epsabs=0, epsrel=1e-10)[0]

if __name__ == "__main__":
    rows = []
    for rho_fm in np.concatenate([np.geomspace(0.02, 0.1, 9)[:-1], np.linspace(0.1, 0.6, 26)]):
        rho = rho_fm/HBARC
        rows.append([rho_fm, S0(1/rho), dens(rho)/HBARC**5, chi(rho)**0.25*1000])
    lo = 1e-4/HBARC
    slope = (np.log(dens(1.01*lo)) - np.log(dens(lo)))/np.log(1.01)
    print(f"Lambda_MS = {LAM*1000:.1f} MeV; d ln d/d ln rho at rho = 1e-4 fm: {slope:.3f} (one loop b0 - 5 = {B0 - 5:.0f}, approached logarithmically)")
    for r in rows[::5]:
        print(f"rho = {r[0]:.3f} fm: 8 pi^2/g^2 = {r[1]:.2f}, d(rho) = {r[2]:.4e} fm^-5, chi(rho_c = rho)^(1/4) = {r[3]:.1f} MeV")
    target = 0.191**4
    rc = brentq(lambda r: chi(r) - target, 0.5, 3.5)
    print(f"chi^(1/4) = 191 MeV for rho_c = {rc*HBARC:.3f} fm (8 pi^2/g^2(1/rho_c) = {S0(1/rc):.2f}); density n_I + n_Ibar = {target/HBARC**4:.3f} fm^-4")
    with open(os.path.join(HERE, "results", "inst_density.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["rho_fm", "8pi2_over_g2", "d_fm-5", "chi_quarter_MeV"])
        w.writerows([[f"{x:.8g}" for x in r] for r in rows])
    print("wrote results/inst_density.csv")
