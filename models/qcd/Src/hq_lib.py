# %% [markdown]
# # Step (9): Born functions, scale coefficients, threshold and high-energy limits of heavy-quark pair production (library)
#
# Research note models/qcd, step (9).  sigma_ij = alpha_s^2/m^2 [f0 + 4 pi alpha_s (f1 + fbar1 ln(mu^2/m^2))], rho = 4 m^2/s,
# alpha_s = alpha_s^(n_l), SU(3), n_l = 5.  f0 from Eq. (sigtree); fbar1 from Eq. (hqfbar) (RG + MS-bar mass factorization, App. L);
# threshold expansions (Coulomb + soft logarithms, Czakon-Mitov Nucl. Phys. B824 (2010) 111, Eqs. (26)-(27)) and high-energy limits
# (ibid., Eqs. (30)-(31)); the MS-bar mass shift of f1, fbar1 (App. L).  Imported by hq_hadronic.py and hq_plot.py.

# %%
import mpmath as mp
mp.mp.dps = 30
CA, CF, TF, NL = mp.mpf(3), mp.mpf(4)/3, mp.mpf(1)/2, 5
B0 = 11*CA/3 - 4*TF*NL/3             # beta_0^(n_l) = 23/3

def f0_qq(rho):
    rho = mp.mpf(rho)
    if rho >= 1: return mp.mpf(0)
    b = mp.sqrt(1 - rho)
    return mp.pi/27*b*rho*(2 + rho)

def f0_gg(rho):
    # SU(3) (note Eq. (sigtree), sigma_B with alpha_s^2/m^2 stripped): (pi rho/192) [(rho^2 + 16 rho + 16) L - 28 b - 31 rho b]
    rho = mp.mpf(rho)
    if rho >= 1: return mp.mpf(0)
    b = mp.sqrt(1 - rho); L = mp.log((1 + b)/(1 - b))
    return mp.pi*rho/192*((rho**2 + 16*rho + 16)*L - 28*b - 31*rho*b)

def conv(P, f, rho, plus=None, delta=0):
    """int_rho^1 dz [P(z) + plus(z)_+ + delta delta(1-z)] f(rho/z); plus distributions with f(rho/z) = 0 for z < rho"""
    rho = mp.mpf(rho)
    r = mp.quad(lambda z: P(z)*f(rho/z), [rho, (1 + rho)/2, 1]) if P else mp.mpf(0)
    if plus:
        f1 = f(rho)
        r += mp.quad(lambda z: plus(z)*(f(rho/z) - f1), [rho, (1 + rho)/2, 1]) - f1*mp.quad(plus, [0, rho])
    return r + delta*f(rho)

Pqq_plus = lambda z: CF*(1 + z*z)/(1 - z)
Pgg_plus = lambda z: 2*CA*z/(1 - z)
Pgg_reg = lambda z: 2*CA*((1 - z)/z + z*(1 - z))
Pgg_delta = (11*CA - 4*NL*TF)/6 - 2*CA     # z/(1-z)_+ = [z/(1-z)]_+ - delta(1-z): Pgg_plus applies the plus prescription to z/(1-z)
Pgq = lambda z: CF*(1 + (1 - z)**2)/z          # gluon from a quark
Pqg = lambda z: TF*(z*z + (1 - z)**2)          # quark from a gluon

def fbar_qq(rho):
    return (B0*f0_qq(rho) - 2*conv(None, f0_qq, rho, plus=Pqq_plus))/(8*mp.pi**2)

def fbar_gg(rho):
    return (B0*f0_gg(rho) - 2*conv(Pgg_reg, f0_gg, rho, plus=Pgg_plus, delta=Pgg_delta))/(8*mp.pi**2)

def fbar_qg(rho):
    return -(conv(Pgq, f0_gg, rho) + conv(Pqg, f0_qq, rho))/(8*mp.pi**2)

# threshold expansions (Czakon-Mitov, Nucl. Phys. B824 (2010) 111, Eqs. (26)-(27)), up to O(beta) corrections, SU(3)
def thr_qq(b):
    b = mp.mpf(b); rho = 1 - b*b; L = mp.log(8*b*b); l2 = mp.log(2)
    br = ((CF - CA/2)*mp.pi**2/(2*b) + 2*CF*L**2 - (8*CF + CA)*L + CF*(8 - mp.pi**2/3 + 3*l2 - 2*l2**2)
          + CA*(mp.mpf(77)/9 - mp.pi**2/4 - 2*l2) + NL*(-mp.mpf(5)/9 + 2*l2/3) - mp.mpf(8)/9)
    return f0_qq(rho)/(4*mp.pi**2)*br

def thr_gg(b):
    b = mp.mpf(b); rho = 1 - b*b; L = mp.log(8*b*b); l2 = mp.log(2); N = mp.mpf(3)
    br = ((CF - (N**2 - 4)*CA/(2*(N**2 - 2)))*mp.pi**2/(2*b) + 2*CA*L**2 - (9*N**2 - 20)*CA/(N**2 - 2)*L
          + CA*((21*N**2 - 50)/(N**2 - 2) - (17*N**2 - 40)*mp.pi**2/(24*(N**2 - 2)) + (N**2 - 4)*l2/(N**2 - 2) - 2*l2**2)
          + CF*(-5 + mp.pi**2/4))
    return f0_gg(rho)/(4*mp.pi**2)*br

# high-energy limits (Czakon-Mitov Eqs. (30), (31)), SU(3)
def he_gq():
    N = mp.mpf(3); return (924*N**2 - 1025)/(10800*N**2*mp.pi)
def he_gg():
    return 2*CA/CF*he_gq()

def msbar_shift(f0, rho):
    """(f1, fbar1) shifts for the MS-bar mass m(mu), mu = mu_R: C_F/(2 pi^2) (rho f0' - f0), 3 C_F/(8 pi^2) (rho f0' - f0);
    for m(m) only the f1 shift (the running of m(mu) cancels the fbar1 shift)"""
    rho = mp.mpf(rho); d = rho*mp.diff(f0, rho) - f0(rho)
    return CF/(2*mp.pi**2)*d, 3*CF/(8*mp.pi**2)*d

if __name__ == "__main__":
    for b in (0.1, 0.3, 0.5, 0.7, 0.9):
        rho = 1 - b*b
        print(b, mp.nstr(f0_qq(rho), 15), mp.nstr(f0_gg(rho), 15), mp.nstr(fbar_qq(rho), 15), mp.nstr(fbar_gg(rho), 15), mp.nstr(fbar_qg(rho), 15),
              mp.nstr(thr_qq(b), 10), mp.nstr(thr_gg(b), 10))
    print("high energy: f1_gq ->", mp.nstr(he_gq(), 12), " f1_gg ->", mp.nstr(he_gg(), 12))
