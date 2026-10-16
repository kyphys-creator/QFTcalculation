# Step (10) library: Gel'fand-Yaglom ratios of -D^2 + m^2 (isospin t = 1/2, 1) in the BPST background, rho = 1 (regular gauge).
# Partial waves (l, j), l = 0, 1/2, 1, ..., j in |l - t| .. l + t, degeneracy (2l+1)(2j+1):
#   H = -d_r^2 - (3/r) d_r + 4 l(l+1)/r^2 + U(r) + m^2,  U = 4 (j(j+1) - l(l+1))/(r^2+1) - 4 t(t+1)/(r^2+1)^2,
#   ln R = ln(psi/psi_free)(r -> infinity), psi, psi_free ~ r^(2l) at r -> 0  (note Eq. (instrad) and app:inst).
# Groups with the same l: t = 1/2: the pair (l, l+1/2) & (l+1/2, l); t = 1: the pair (l, l+1) & (l+1, l) and the single (l, l) (l >= 1/2).
# The massless solutions psi0 are elementary (inst_bpst.wl); the mass correction Delta = lim (ln(psi/psi0) - ln(psi_free^(k)/r^(2k))) is
# integrated with the free reference of the large-r angular momentum k, which removes the large cancellations inside a pair.
import numpy as np
from scipy.integrate import solve_ivp

def U(r, l, j, t):
    return 4*(j*(j + 1) - l*(l + 1))/(r*r + 1) - 4*t*(t + 1)/(r*r + 1)**2

def lnR_direct(l, j, t, m, K=1e4, rtol=1e-13):
    """ln R by direct integration (tau = ln r): Y = r psi_free'/psi_free, Z = r (psi'/psi - psi_free'/psi_free), S' = Z (used for checks)"""
    def f(tau, y):
        r = np.exp(tau); Y, Z = y[1], y[2]
        return [Z, 4*l*(l + 1) + m*m*r*r - Y*Y - 2*Y, r*r*U(r, l, j, t) - Z*Z - 2*(Y + 1)*Z]
    r0 = 1e-3/(1 + l); Z0 = U(0.0, l, j, t)*r0*r0/(4*l + 4); Y0 = 2*l + m*m*r0*r0/(4*l + 4)
    R = K*(2*l + 2)/m if m > 0 else K
    sol = solve_ivp(f, (np.log(r0), np.log(R)), [Z0/2, Y0, Z0], method="LSODA", rtol=rtol, atol=1e-30)
    c = 4*(j*(j + 1) - l*(l + 1))
    return sol.y[0, -1] + (c/(2*m*R) + c/(4*m*m*R*R) if m > 0 else 0.0)

def channels(t, n):
    """group with l = n/2: list of (degeneracy, massless ln ratio, [(g, k), ...]); r psi0'/psi0 = 2k + g(r^2) with k the large-r angular momentum"""
    l = n/2; out = []
    if t == 0.5:
        ga = lambda x, l=l: -((2*l + 2) + (2*l + 3)*x)/(((2*l + 2) + (2*l + 1)*x)*(1 + x))
        gb = lambda x: 1/(1 + x)
        out.append(((2*l + 1)*(2*l + 2), np.log((2*l + 1)/(2*l + 2)), [(ga, l + 0.5), (gb, l)]))
    else:
        A, B, C = (2*l + 2)*(2*l + 3)/2, (2*l + 1)*(2*l + 3), (2*l + 1)*(2*l + 2)/2
        ga = lambda x, A=A, B=B, C=C: -2*(A + 2*A*x + (B - C)*x*x)/((A + B*x + C*x*x)*(1 + x))
        gb = lambda x: 2/(1 + x)
        out.append(((2*l + 1)*(2*l + 3), np.log((2*l + 1)/(2*l + 3)), [(ga, l + 1), (gb, l)]))
        if l >= 0.5:
            gc = lambda x, l=l: -4*x/(((2*l + 2) + 2*l*x)*(1 + x))
            out.append(((2*l + 1)**2, np.log(2*l/(2*l + 2)), [(gc, l)]))
    return out

def Delta(g, k, m, K=1e4, rtol=1e-12, atol=1e-20):
    """mass correction: tau = ln r, Pf = r d/dr ln(psi_free^(k)/r^(2k)), Q = r d/dr [ln(psi/psi0) - ln(psi_free^(k)/r^(2k))], Delta = int Q dtau;
    dPf = m^2 r^2 - Pf^2 - 2(2k+1) Pf,  dQ = -(2 Pf + Q) Q - 2 (P0 + 1) Q - 2 g Pf,  P0 = r psi0'/psi0 = 2k + g.  Series start Pf = p r^2, Q = q r^2."""
    def f(tau, y):
        r = np.exp(tau); x = r*r; Pf, Q = y[1], y[2]
        gg = g(x)
        return [Q, m*m*x - Pf*Pf - 2*(2*k + 1)*Pf, -(2*Pf + Q)*Q - 2*(gg + 2*k + 1)*Q - 2*gg*Pf]
    p = m*m/(4*k + 4); g0 = g(0.0); q = -g0*p/(2*k + g0 + 2)
    r0 = 1e-4/(1 + k); R = K*(2*k + 2)/m
    sol = solve_ivp(f, (np.log(r0), np.log(R)), [q*r0*r0/2, p*r0*r0, q*r0*r0], method="LSODA", rtol=rtol, atol=atol)
    return sol.y[0, -1]

def group(args):
    """(massless sum, mass correction) of the group l = n/2"""
    t, n, m = args
    a0 = 0.0; dm = 0.0
    for deg, ln0, gk in channels(t, n):
        a0 += deg*ln0
        if m > 0:
            dm += deg*sum(Delta(g, k, m) for g, k in gk)
    return a0, dm
