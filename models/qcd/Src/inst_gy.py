# %% [markdown]
# # Step (10): 't Hooft's determinants by the Gel'fand-Yaglom method (isospin 1/2 and 1) and the quark-mass dependence
#
# Research note models/qcd, step (10).  rho = 1.  Partial waves and the mass corrections from inst_gylib.py.
# (a) massless pairs: ODE versus the exact ratios (2l+1)/(2l+2) (t = 1/2), (2l+1)/(2l+3), 2l/(2l+2) (t = 1);
#     the mass-correction formulation versus the direct ODE.
# (b) alpha(1/2) from the massless sum with the counterterms 2L^2 + 4L - (1/6) ln L + 127/72 - (1/3) ln 2 (Dunne-Hur-Lee-Min).
# (c) Gamma~(m) = alpha(1/2) + lim_L [sum_{l<=L} d_l(m) - (m^2/2) ln L] + m^2/2 - m^2 ln 2 + (m^2/2) ln m  (d_l = mass correction of group l;
#     the tail beyond L from a fit in l^-p and ln l l^-p), compared with the small-mass expansion (Hur-Lee-Min) and the large-mass
#     expansion (-ln m/6 - 1/75 m^2 - 17/735 m^4 + 232/2835 m^6 - 7916/148225 m^8).
# (d) decoupling: for m -> infinity Gamma~_t(m) = -(T(R)/3) ln m - (2 T(R)/75)/m^2 + O(m^-4) with no constant (MS-bar); fitting the m^2 and the
#     constant terms of the partial-wave sum gives beta_t (m^2 counterterm) and alpha(t); t = 1 checks alpha(1) = 0.443307.
# -> results/inst_gy.csv (m, Gamma~, expansions), results/inst_alpha.csv
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python inst_gy.py   (about 11 minutes on 7 processes)

# %%
import csv, os, sys, time
import numpy as np, mpmath as mp
from multiprocessing import Pool
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.getcwd()
sys.path.insert(0, HERE)
import inst_gylib as GY
LMAX = 1000
ZP = mp.zeta(-1, derivative=1)
ALPHA = {0.5: float(-mp.mpf(5)/72 - mp.log(2)/6 - 2*ZP)}
ALPHA[1.0] = 4*ALPHA[0.5] + np.log(2) - 5/6
TR = {0.5: 0.5, 1.0: 2.0}                      # T(R) = t(t+1)(2t+1)/3
CHM = 127/72 - np.log(2)/3                     # Dunne-Hur-Lee-Min constant (t = 1/2)

def large_m(m):
    return -np.log(m)/6 - 1/(75*m**2) - 17/(735*m**4) + 232/(2835*m**6) - 7916/(148225*m**8)
def small_m(m):
    """Hur-Lee-Min: alpha + (m^2/2)(ln(m/2) + gamma + 1/2) + m^4 (-ln^2 m/4 + ln m (1/2 - gamma + ln 2)/2 + C), C = -0.382727"""
    lm = np.log(m)
    return ALPHA[0.5] + m*m/2*(np.log(m/2) + np.euler_gamma + 0.5) + m**4*(-lm*lm/4 + lm*(0.5 - np.euler_gamma + np.log(2))/2 - 0.382727)

# %% [markdown]
# ## (a) massless pairs and the mass-correction formulation

# %%
if __name__ == "__main__":
    for t, l in ((0.5, 0), (0.5, 3), (1.0, 0), (1.0, 3)):
        ch = GY.channels(t, 2*l)
        if t == 0.5:
            ode = GY.lnR_direct(l, l + .5, .5, 0, K=1e5) + GY.lnR_direct(l + .5, l, .5, 0, K=1e5)
        else:
            ode = GY.lnR_direct(l, l + 1, 1.0, 0, K=1e5) + GY.lnR_direct(l + 1, l, 1.0, 0, K=1e5)
        print(f"(a) t = {t}, l = {l}: massless pair ODE {ode:.12f}, exact {ch[0][1]:.12f}, diff {ode - ch[0][1]:+.1e}")
    for t, l, m in ((0.5, 1, 0.5), (0.5, 10, 2.0), (1.0, 3, 1.0), (1.0, 10, 1.0)):
        ch = GY.channels(t, 2*l)
        new = ch[0][1] + sum(GY.Delta(g, k, m) for g, k in ch[0][2])
        old = (GY.lnR_direct(l, l + .5, .5, m) + GY.lnR_direct(l + .5, l, .5, m)) if t == 0.5 else (GY.lnR_direct(l, l + 1, 1.0, m) + GY.lnR_direct(l + 1, l, 1.0, m))
        print(f"    t = {t}, l = {l}, m = {m}: pair, mass correction {new:.12f}, direct {old:.12f}, diff {new - old:+.1e}")

# %% [markdown]
# ## (b) alpha(1/2) from the massless sum

# %%
if __name__ == "__main__":
    for L in (100, 1000, 10000):
        s = sum((2*l + 1)*(2*l + 2)*np.log((2*l + 1)/(2*l + 2)) for l in np.arange(0, L + 0.25, 0.5))
        v = s + 2*L*L + 4*L - np.log(L)/6 + CHM
        print(f"(b) L = {L}: sum + counterterms = {v:.12f}  (alpha(1/2) = {ALPHA[0.5]:.12f}, diff {v - ALPHA[0.5]:+.2e}, ~1/L)")

# %% [markdown]
# ## (c), (d) the mass corrections

# %%
def tail_basis_sum(kind, p, L):
    """sum over l = n/2 > L of l^-p (kind 0) or ln(l) l^-p (kind 1)"""
    if kind == 0:
        return float(2**p*mp.zeta(p, 2*L + 1))
    return float(2**p*(-mp.zeta(p, 2*L + 1, derivative=1) - mp.log(2)*mp.zeta(p, 2*L + 1)))
BASIS = [(0, 2), (1, 2), (0, 3), (1, 3), (0, 4), (1, 4), (0, 5)]

def G_of_m(pool, t, m, L=LMAX):
    """lim_L [sum_{l<=L} d_l(m) - T(R) m^2 ln L] (d_l ~ (T(R)/2) m^2/l, l in steps of 1/2); returns the values for L/2 and L"""
    a = TR[t]/2
    ls = np.arange(0, L + 0.25, 0.5)
    d = np.array([x[1] for x in pool.map(GY.group, [(t, n2, m) for n2 in range(2*L + 1)])])
    S = np.cumsum(d); out = []
    for LL in (L//2, L):
        sel = (ls >= LL/3) & (ls <= LL)
        x = ls[sel]; y = d[sel] - 2*a*m*m*(np.log(x) - np.log(x - 0.5))
        A = np.array([(np.log(x) if k else 1.0)*x**-p for k, p in BASIS]).T
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        out.append(S[2*LL] - 2*a*m*m*np.log(LL) + sum(c*tail_basis_sum(k, p, LL) for c, (k, p) in zip(coef, BASIS)))
    return out

if __name__ == "__main__":
    rows = []; Gt = {0.5: {}, 1.0: {}}
    with Pool(7) as pool:
        for m in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0):
            t0 = time.time()
            g = G_of_m(pool, 0.5, m); Gt[0.5][m] = g[1]
            Gam = ALPHA[0.5] + g[1] + m*m/2 - m*m*np.log(2) + m*m/2*np.log(m)
            rows.append([m, Gam, abs(g[1] - g[0]), small_m(m), large_m(m)])
            print(f"(c) m = {m}: Gamma~ = {Gam:.9f} (L-dependence {abs(g[1]-g[0]):.0e});  small-m {small_m(m) - Gam:+.1e}, large-m {large_m(m) - Gam:+.1e}  ({time.time()-t0:.0f}s)", flush=True)
        for m in (2.0, 3.0, 4.0, 5.0, 6.0, 8.0):
            t0 = time.time()
            Gt[1.0][m] = G_of_m(pool, 1.0, m)[1]
            print(f"    t = 1, m = {m}: G = {Gt[1.0][m]:.9f}  ({time.time()-t0:.0f}s)", flush=True)
    with open(os.path.join(HERE, "results", "inst_gy.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["m_rho", "Gamma_tilde", "L_dependence", "small_m_expansion", "large_m_expansion"])
        w.writerows([[f"{x:.10g}" for x in r] for r in rows])
    # (d) decoupling fits: G + T m^2 ln m + (T/3) ln m - d2/m^2 = -alpha - beta m^2 + d4/m^4 + d6/m^6 (+ d8/m^8)
    arows = []
    for t in (0.5, 1.0):
        T = TR[t]
        ms = np.array(sorted(m for m in Gt[t] if m >= 2)); G = np.array([Gt[t][m] for m in ms])
        y = G + T*ms**2*np.log(ms) + T/3*np.log(ms) + 2*T/75/ms**2
        A = np.array([-np.ones_like(ms), -ms**2, ms**-4., ms**-6.]).T
        sol, *_ = np.linalg.lstsq(A, y, rcond=None)
        beta_ex = 2*T*(0.5 - np.log(2))
        A2 = np.array([-np.ones_like(ms), ms**-4., ms**-6., ms**-8.]).T
        sol2, *_ = np.linalg.lstsq(A2, y + beta_ex*ms**2, rcond=None)
        print(f"(d) t = {t}: free fit alpha = {sol[0]:.7f}, beta = {sol[1]:.7f} (2T(1/2 - ln 2) = {beta_ex:.7f});  beta fixed: alpha = {sol2[0]:.7f}"
              f"  (closed form {ALPHA[t]:.7f}, diff {sol2[0] - ALPHA[t]:+.1e})")
        arows.append([t, sol[0], sol[1], beta_ex, sol2[0], ALPHA[t]])
    with open(os.path.join(HERE, "results", "inst_alpha.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["t", "alpha_free_fit", "beta_free_fit", "beta_exact", "alpha_beta_fixed", "alpha_closed_form"])
        w.writerows([[f"{x:.10g}" for x in r] for r in arows])
    print("wrote results/inst_gy.csv, results/inst_alpha.csv")
